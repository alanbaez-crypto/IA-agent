# IA-agent

Base local de comprensión lectora preuniversitaria inspirada en la Ciencia del Texto.
Funciona con Python 3.12, Streamlit y SQLite, sin Codex Cloud, ChatGPT Plus, claves API
ni servicios de pago. El modo predeterminado es una simulación determinista sin conexión.

Permite registrar textos y su fuente, asociar preguntas manuales o propuestas,
y guardar respuesta, evidencia literal, dimensión, proveedor y fecha UTC.
Las dimensiones iniciales son lectura literal, cohesión, macroestructura e inferencia.
Son categorías de trabajo; esta base no constituye un instrumento pedagógico validado.
El simulador copia un fragmento para probar el recorrido; no comprende ni califica.
Las propuestas de Ollama también necesitan revisión humana.

## Inicio en Windows (PowerShell)

Instala Git, Python **3.12 de 64 bits** con el lanzador `py`, VS Code y su extensión
Python de Microsoft. No necesitas extensiones de IA ni suscripciones.

```powershell
git clone https://github.com/alanbaez-crypto/IA-agent.git
cd IA-agent
git switch continuidad/base-local
code .
```

Desde la terminal de VS Code, en la raíz del proyecto:

```powershell
powershell -NoProfile -File .\scripts\setup.ps1
powershell -NoProfile -File .\scripts\test.ps1
powershell -NoProfile -File .\scripts\run.ps1
```

Si tu política impide ejecutar scripts, no necesitas cambiarla: usa los comandos
equivalentes de [la guía de Windows](docs/WINDOWS.md). Selecciona el intérprete
`.venv\Scripts\python.exe` en VS Code. Abre la dirección local que indique Streamlit
en tu propio equipo y detén el servidor con Ctrl+C. No expongas el servidor a Internet.

## Uso y configuración

1. Registra un título, texto y fuente (usa textos propios o autorizados).
2. Selecciona el texto y pulsa **Proponer pregunta**, o registra una manualmente.
3. Consulta las preguntas guardadas. La evidencia debe ser una cita exacta del texto.
4. Revisa el contenido pedagógico antes de usarlo con estudiantes.

SQLite crea `data/ia_agent.sqlite3` al arrancar. No hay cuentas, edición, eliminación,
evaluación automática ni seguimiento de alumnos en esta etapa. No registres datos
personales de estudiantes. Las bases y copias están excluidas de Git.

`.env.example` documenta las variables; no se carga automáticamente. En PowerShell:

```powershell
$env:IA_AGENT_PROVIDER = 'mock'
$env:IA_AGENT_DB = 'data/ia_agent.sqlite3'
```

Ollama es opcional: consulta [instalación, modelos existentes y límites](docs/WINDOWS.md#ollama-opcional).
La aplicación no ejecuta `ollama pull` ni instala modelos. Sin modelo local adecuado,
mantén `mock` y trabaja con preguntas manuales.

## Desarrollo y continuidad

En Linux/macOS: `python3.12 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`,
`.venv/bin/python -m pytest -q` y `.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false`.

- [Windows: instalación, pruebas, mantenimiento y recuperación](docs/WINDOWS.md)
- [Plan de continuidad y límites de esta entrega](docs/CONTINUIDAD.md)
- [Resultados reales de validación y sus límites](docs/VALIDACION.md)

Estructura: `app.py` (interfaz), `ia_agent/storage.py` (SQLite), `providers.py`
(simulador/Ollama), `backup.py` (copias y recuperación), `tests/` (pytest).
`requirements.in` declara dependencias directas; `requirements.txt` fija también
las transitivas verificadas. SQLite y el cliente HTTP usan la biblioteca estándar.
