from streamlit.testing.v1 import AppTest

from ia_agent.storage import Store


def test_register_text_and_generate_mock(tmp_path, monkeypatch):
    path = tmp_path / "app.sqlite3"
    monkeypatch.setenv("IA_AGENT_DB", str(path))
    monkeypatch.setenv("IA_AGENT_PROVIDER", "mock")
    app = AppTest.from_file("app.py").run()
    assert not app.exception
    app.text_input[0].set_value("El agua")
    app.text_area[0].set_value("El agua cambia de estado.")
    app.text_input[1].set_value("Ejemplo propio")
    app.button[0].click().run()
    assert not app.exception
    assert len(Store(path).texts()) == 1
    next(button for button in app.button if button.label == "Proponer pregunta").click().run()
    assert not app.exception
    questions = Store(path).questions(1)
    assert len(questions) == 1
    assert questions[0]["provider"] == "mock"
    assert questions[0]["evidence"] == "El agua cambia de estado."


def test_manual_question_and_unavailable_provider(tmp_path, monkeypatch):
    path = tmp_path / "manual.sqlite3"
    monkeypatch.setenv("IA_AGENT_DB", str(path))
    monkeypatch.setenv("IA_AGENT_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "")
    store = Store(path)
    store.initialize()
    key = store.add_text("Ideas", "El texto conecta ideas.")
    app = AppTest.from_file("app.py").run()
    assert not app.exception
    assert any("OLLAMA_MODEL" in error.value for error in app.error)
    app.text_area[1].set_value("¿Qué conecta el texto?")
    app.text_area[2].set_value("Ideas.")
    app.text_area[3].set_value("ideas")
    next(button for button in app.button if button.label == "Guardar pregunta").click().run()
    assert not app.exception
    assert store.questions(key)[0]["provider"] == "manual"

    # Recargar la interfaz mantiene los registros; el proveedor no bloquea trabajo manual.
    reopened = AppTest.from_file("app.py").run()
    assert not reopened.exception
    assert any("¿Qué conecta el texto?" in element.label for element in reopened.expander)
