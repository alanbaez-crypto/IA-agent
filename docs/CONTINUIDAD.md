# Continuidad independiente de ChatGPT Plus

La fecha de término indicada es el **7 de noviembre de 2026**. Esta entrega no
requiere suscripción antes ni después de esa fecha. No utiliza APIs de pago,
hosting, almacenamiento externo ni modelos descargados. Coste de servicios previsto:
**US$0/mes**, dentro del máximo de US$10. Hardware, electricidad y conexión propios
no están estimados. No se autoriza ningún gasto ni se registra medio de pago.

## Etapa actual: base mínima para revisión

- Python 3.12 + Streamlit local + SQLite, dependencias fijadas y pytest.
- Registro de textos/fuentes y preguntas con respuesta y evidencia literal.
- Simulador sin red y adaptador opcional a Ollama ya instalado.
- Instalación Windows, mantenimiento, copias, recuperación y continuidad con Git.

El checkout inicial tenía únicamente `README.md`. No existían motor de comprensión,
corpus, pruebas ni criterios de evaluación previos que preservar. El esquema propuesto
es una base de trabajo, no una implementación completa de la Ciencia del Texto.
La organización inicial distingue información explícita, relaciones de cohesión,
macroestructura e inferencias. Guardar una cita literal no prueba por sí mismo que
una inferencia sea válida. No hay calificación ni diagnóstico automatizado del alumno.

## Antes del 7 de noviembre

1. Revisar esta rama y sus resultados. La integración requiere tu aprobación.
2. En tu Windows, conservar el repositorio, instalar con el lock, ejecutar pytest y
   registrar un texto y una pregunta; reiniciar y comprobar persistencia.
3. Crear una copia SQLite, verificarla y ensayar su recuperación en una ubicación nueva.
4. Conservar código/bundle, copias verificadas e instaladores en otro dispositivo.
   Preparar el wheelhouse en Windows si necesitas reinstalación sin red.

Estos son pasos de traspaso propuestos. La ejecución Windows y la publicación de
la rama no se consideran realizadas por haberlas documentado.

## Después del término

Trabajar desde VS Code y PowerShell. Usar Git para cambios pequeños y revisables;
pytest antes de cada integración; preguntas manuales y simulador como flujo gratuito
garantizado sin inferencia real. Ollama es una alternativa únicamente si ya tienes
un modelo apropiado y recursos locales suficientes. No necesitas sustituir Plus
por otro servicio. Mantener un registro mensual de gastos; con esta arquitectura
no hay facturación de proveedores.

## Etapas futuras: detenidas hasta aprobación

1. **Diseño pedagógico:** acordar objetivos y rúbrica de Ciencia del Texto, tratamiento
   de coherencia/cohesión y macroestructura, ejemplos revisados por docentes y criterios
   de calidad para inferencias. No se incorpora corpus sin autorización de uso.
2. **Evaluación:** conjunto pequeño autorizado, revisión humana, medición de errores
   y comparación de preguntas manuales con propuestas de un modelo local adecuado.
3. **Ampliaciones:** edición/revisión de preguntas, exportación, migraciones y, solo si
   se justifica, otro motor local. Una API de pago o despliegue público necesita una
   decisión nueva y presupuesto explícito; no es parte de esta base.

No se ejecutan estas etapas, se mezcla la rama ni se despliega la aplicación en
esta entrega. La aprobación solicitada es para revisar la base y decidir el siguiente
alcance, no para asumir que el motor pedagógico está validado.
