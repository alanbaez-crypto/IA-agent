"""Interfaz local. Ejecutar con python -m streamlit run app.py."""

import sqlite3

import streamlit as st

from ia_agent.config import database_path
from ia_agent.providers import ProviderError, configured_provider
from ia_agent.storage import DIMENSIONS, Store

st.set_page_config(page_title="IA-agent", page_icon="📖")
st.title("IA-agent · Comprensión lectora")
st.caption("Base local de trabajo: textos, preguntas y evidencia. Revisión pedagógica humana requerida.")

store = Store(database_path())
try:
    store.initialize()
except (sqlite3.Error, OSError, ValueError) as exc:
    st.error(f"No se pudo abrir la base de datos: {exc}")
    st.stop()

with st.expander("Registrar texto", expanded=True):
    with st.form("text_form", clear_on_submit=True):
        title = st.text_input("Título")
        body = st.text_area("Texto")
        source = st.text_input("Fuente o referencia (opcional)")
        if st.form_submit_button("Guardar texto"):
            try:
                store.add_text(title, body, source)
                st.success("Texto guardado.")
            except (ValueError, sqlite3.Error) as exc:
                st.error(str(exc))

texts = store.texts()
if not texts:
    st.info("Registra un texto para comenzar. El modo simulado funciona sin conexión.")
    st.stop()

text_id = st.selectbox("Texto de trabajo", [item["id"] for item in texts],
                       format_func=lambda key: next(f'{t["id"]} · {t["title"]}' for t in texts if t["id"] == key))
selected = next(item for item in texts if item["id"] == text_id)
st.subheader(selected["title"])
st.text(selected["body"])
if selected["source"]:
    st.caption(selected["source"])

try:
    provider = configured_provider()
    st.caption(f"Proveedor: {provider.name}")
    if provider.name == "mock":
        st.info("El simulador solo copia un fragmento para demostrar el flujo. No interpreta ni evalúa el texto.")
    if st.button("Proponer pregunta"):
        with st.spinner("Preparando propuesta…"):
            question = provider.generate(selected["body"])
        store.add_question(text_id, question.prompt, question.answer, question.evidence,
                           question.dimension, provider.name)
        st.success("Propuesta guardada; pendiente de revisión humana.")
except (ProviderError, ValueError, sqlite3.Error) as exc:
    st.error(str(exc))

with st.expander("Registrar pregunta manual"):
    with st.form(f"question_form_{text_id}", clear_on_submit=True):
        prompt = st.text_area("Pregunta")
        answer = st.text_area("Respuesta esperada y justificación")
        evidence = st.text_area("Evidencia (cita exacta del texto)")
        dimension = st.selectbox("Dimensión", DIMENSIONS)
        if st.form_submit_button("Guardar pregunta"):
            try:
                store.add_question(text_id, prompt, answer, evidence, dimension)
                st.success("Pregunta guardada.")
            except (ValueError, sqlite3.Error) as exc:
                st.error(str(exc))

st.subheader("Preguntas registradas")
for item in store.questions(text_id):
    with st.expander(f'#{item["id"]} · {item["dimension"]} · {item["prompt"]}'):
        st.write("Respuesta:", item["answer"])
        st.text("Evidencia: " + item["evidence"])
        st.caption(f'Proveedor: {item["provider"]} · {item["created_at"]} UTC · Sin validación pedagógica registrada')
