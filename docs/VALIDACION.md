# Validación de esta entrega

Fecha: 23 de octubre de 2026. Ejecutada en Linux x86_64, Python 3.12.14,
entorno virtual local, Streamlit 1.50.0 y pytest 8.4.2.

| Comprobación ejecutada | Resultado real |
| --- | --- |
| Instalación desde `requirements.in` y reinstalación con `requirements.txt` | Correctas |
| `.venv/bin/python -m pip check` | `No broken requirements found.` |
| `.venv/bin/python -m pytest -q` | **34 passed in 4.28s**, sin fallos ni omitidos |
| Servidor Streamlit en loopback, telemetría desactivada | Arrancó; health `ok`, página HTML HTTP 200; detenido después |
| CLI `backup`, `verify`, `restore` con datos temporales | Tres operaciones correctas; pregunta recuperada |

Las pruebas ejercitan SQLite persistente, reinicialización, validación de campos,
citas literales, integridad referencial, aislamiento entre textos, SQL parametrizado
y rechazo de versiones futuras. Incluyen copia/restauración y rechazo de sobrescritura
o archivos inválidos. AppTest registra un texto y una propuesta simulada; otra prueba
guarda una pregunta manual aunque falte configuración de Ollama y verifica su recarga.
Todas usan datos temporales.

El adaptador se prueba mediante un servidor HTTP local simulado: ruta, payload,
JSON válido, citas/dimensiones inválidas, campos incorrectos y error HTTP 404.
Se verifica que no admita URLs externas ni credenciales en la URL. **No se ejecutó
inferencia real con Ollama**, no estaba instalado y no se descargaron modelos.

La primera comprobación externa de arranque usó por error el intérprete base al
resolver el enlace del ejecutable del venv y falló por ausencia de Streamlit allí.
Se corrigió la invocación para conservar la ruta del venv y el arranque HTTP pasó.
No fue necesario modificar la aplicación para resolver ese fallo de comprobación.

## Límites y verificación pendiente en Windows

No hay Windows ni PowerShell en esta máquina: los scripts `.ps1`, VS Code, Git
Credential Manager, la instalación de wheels para Windows y la recuperación en un
Windows real están documentados, **no ejecutados**. El lock incluye el pin condicional
de colorama necesario en Windows. Resolver dependencias en Linux no demuestra por
sí solo que todos los binarios estén disponibles en otra plataforma.

Tras revisar la rama, la aceptación local propuesta es: ejecutar setup y pytest en
Windows, arrancar, guardar un texto y pregunta, reiniciar, crear una copia verificada
y recuperarla con otra ruta `IA_AGENT_DB`. Si ya existe un modelo Ollama apropiado,
probar una pregunta y revisar manualmente su respuesta; esta comprobación es opcional.

No se afirma validez pedagógica, comprensión real del simulador, funcionamiento
con todos los modelos, auditoría de seguridad, despliegue ni publicación. No se
utilizaron servicios de pago. Las siguientes etapas requieren aprobación del usuario.
