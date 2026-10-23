# Windows, VS Code y Git

## Instalación reproducible

Objetivo: Windows 10/11, x64, Python 3.12 de 64 bits. Descarga Python desde
python.org, Git desde git-scm.com y VS Code desde code.visualstudio.com.
Conserva los instaladores para reinstalar sin depender de ChatGPT. No se requiere Node,
Docker ni base de datos externa. Trabaja en una carpeta local escribible, no dentro
de OneDrive mientras SQLite esté en uso.

Los scripts PowerShell cambian a la raíz del proyecto, comprueban los fallos y
no necesitan activar el entorno virtual. Si Windows bloquea los scripts, ejecuta
estos comandos directamente en la terminal PowerShell de VS Code, desde la raíz:

```powershell
py -3.12 --version
git --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
```

Revisa el resultado de cada comando antes de continuar. La instalación necesita
acceso a `pypi.org` y `files.pythonhosted.org`; Git usa GitHub. La ejecución normal
con `mock` y las pruebas no necesitan Internet. Streamlit tiene desactivada la
telemetría en los comandos indicados. No desactives TLS ni uses `--trusted-host`
para solucionar errores de certificados; revisa fecha, conexión y CA de tu organización.

En VS Code: **Python: Select Interpreter** → `.venv\Scripts\python.exe`.
La configuración incluida habilita pytest en la pestaña de pruebas. Si ya existe
un `.venv` incompatible, cierra la aplicación y renómbralo antes de crearlo de nuevo.
Las rutas de datos relativas se resuelven desde el directorio actual: ejecuta siempre
desde la raíz. No ejecutes pruebas contra tu base real: usan directorios temporales.

## Configuración

No necesitas secretos. `.env.example` es documentación, no un archivo que se lea.
Las variables se definen por terminal y duran esa sesión:

```powershell
$env:IA_AGENT_DB = 'data/ia_agent.sqlite3'
$env:IA_AGENT_PROVIDER = 'mock'
```

### Ollama opcional

Solo si ya dispones de Ollama y un modelo instalado compatible con generación JSON:

```powershell
ollama --version
ollama list
# Si el servicio de escritorio no está activo, en otra terminal:
ollama serve
```

Usa el nombre exacto que aparezca en `ollama list`, sin descargar modelos:

```powershell
$env:IA_AGENT_PROVIDER = 'ollama'
$env:OLLAMA_URL = 'http://127.0.0.1:11434'
$env:OLLAMA_MODEL = 'NOMBRE_EXACTO_YA_INSTALADO'
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

El adaptador solo admite HTTP hacia loopback, llama a `/api/generate` sin streaming,
espera hasta 60 segundos y verifica JSON, dimensión y cita literal. No comprueba la
corrección semántica de la respuesta. Un error 404 puede indicar modelo no instalado;
JSON inválido puede indicar un modelo inadecuado. No ejecutes `pull` por este proyecto.
Si falta memoria, el servicio no existe o falla la generación, vuelve a `mock` y
reinicia Streamlit. CPU, RAM, velocidad y calidad dependen del modelo existente.
El texto seleccionado se envía al proceso Ollama local al pulsar el botón.

## Copias y recuperación

Git conserva el código, **no** los datos ignorados. Haz copias después de cada sesión
de registro y antes de actualizar. El comando utiliza la API de backup de SQLite,
no una copia cruda de una base abierta. Verifica integridad, claves y esquema v1.
Nunca sobrescribe una ruta existente:

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
.\.venv\Scripts\python.exe -m ia_agent.backup backup "backups\ia-agent-$stamp.sqlite3"
.\.venv\Scripts\python.exe -m ia_agent.backup verify "backups\ia-agent-$stamp.sqlite3"
```

Copia los archivos verificados a otro dispositivo. Son datos sin cifrar: protege
el dispositivo y no los publiques. Conserva al menos las últimas tres copias.

Para recuperar, detén Streamlit y todos los procesos que usen la base. Verifica primero
la copia elegida. Si existe la carpeta `data`, renómbrala a una ruta nueva para preservar
la base dañada y cualquier archivo journal/WAL asociado. Ejemplo para la ruta predeterminada:

```powershell
.\.venv\Scripts\python.exe -m ia_agent.backup verify backups\COPIA.sqlite3
# Solo después de que la verificación haya terminado correctamente:
Rename-Item data "data-anterior-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
.\.venv\Scripts\python.exe -m ia_agent.backup restore backups\COPIA.sqlite3
```

Si `data` no existe, omite el renombrado. Si configuraste `IA_AGENT_DB`, preserva la
base y sus archivos auxiliares en esa ubicación, no otra. `restore` exige que la ruta
destino no exista. Inicia la app y comprueba títulos y preguntas. Conserva el original
hasta comprobar la recuperación; no intentes repararlo sobre la única copia.

## Reinstalación y trabajo sin Cloud

Para reconstruir en otra máquina: restaura/clona el código, instala con `requirements.txt`,
ejecuta pytest, restaura la base y arranca la aplicación. `.venv` se recrea; no se copia
entre Windows y Linux. Un snapshot de Codex no es necesario.

Para guardar dependencias sin conexión, ejecuta **en el Windows x64 con Python 3.12
de destino**, mientras tengas Internet:

```powershell
.\.venv\Scripts\python.exe -m pip download --only-binary=:all: -r requirements.txt -d ..\ia-agent-wheelhouse
# En otra instalación compatible, sin red:
.\.venv\Scripts\python.exe -m pip install --no-index --find-links ..\ia-agent-wheelhouse -r requirements.txt
```

El wheelhouse es específico de plataforma/versión. La descarga offline en Windows
es un procedimiento pendiente de verificar allí; no reutilices wheels de Linux.
Conserva una copia local del repositorio y, opcionalmente, un bundle de Git fuera de él:

```powershell
git bundle create ..\IA-agent-backup.bundle --all
git bundle verify ..\IA-agent-backup.bundle
# Recuperar en una carpeta nueva:
git clone ..\IA-agent-backup.bundle IA-agent-recuperado
```

El bundle incluye commits, no cambios sin confirmar ni SQLite. Para guardar trabajo:

```powershell
git status
git switch -c trabajo/descripcion
git add RUTAS_REVISADAS
git diff --cached
git commit -m "Describe el cambio"
```

Revisa que no haya bases, datos o secretos antes del commit. Publica con `git push`
solo cuando decidas compartirlo y tengas acceso; usa Git Credential Manager si GitHub
lo solicita. No pegues tokens en archivos ni comandos compartidos. Para actualizar una
rama ya publicada, usa `git pull --ff-only` con el árbol limpio y una copia previa.
No uses `reset --hard` ni `clean -fd` para solucionar conflictos o recuperar datos.

## Mantenimiento

Mensualmente: copia y verifica SQLite, ejecuta pytest, revisa cambios con Git y
consulta avisos de seguridad de Python/Streamlit. No actualices paquetes automáticamente.
Para una actualización deliberada, abre una rama, modifica `requirements.in`, crea
un entorno virtual limpio, instala, fija el conjunto resuelto con `pip freeze` en
`requirements.txt` (conserva el pin condicional de colorama para Windows), ejecuta
`pip check`, pytest y el recorrido manual. Comprueba también
Windows antes de adoptar un nuevo lock. Conserva el commit y la copia anteriores.
El lock no contiene hashes; pip mantiene su verificación TLS normal. Una versión fijada
no equivale a una auditoría de seguridad.

Errores frecuentes: puerto 8501 ocupado → detén tu proceso anterior o usa
`--server.port 8502`; base bloqueada → cierra otras instancias y reintenta; `ModuleNotFoundError`
→ revisa el intérprete y repite setup; corrupción SQLite → conserva originales y restaura
una copia verificada. No elimines datos para resolver un fallo de dependencias.
