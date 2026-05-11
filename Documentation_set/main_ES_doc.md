Aquí tienes la traducción del Markdown del inglés al español, manteniendo la estructura y los identificadores:

1. ## Resumen:
Este archivo define una aplicación FastAPI que actúa como API para un flujo de trabajo de procesamiento y envío de documentos. Maneja las solicitudes entrantes, inicia el procesamiento en segundo plano utilizando LangGraph y proporciona puntos finales para la consulta del estado de los trabajos. El flujo de trabajo implica la clasificación de documentos, la ingesta de datos, la sanitización, la auditoría de lagunas y la generación potencial de resúmenes ejecutivos y hojas de ruta estratégicas.

2. ## Clases:
- **AgentStatePayload**: Define la estructura para el estado inicial del agente de entrada, que abarca datos del documento, detalles de envío, metadatos e historial de interacciones.
- **FastAPI**: La instancia principal de la aplicación del framework FastAPI.
- **Request**: Representa una solicitud HTTP entrante.
- **BackgroundTasks**: Una utilidad para ejecutar tareas en segundo plano.
- **JSONResponse**: Una utilidad de FastAPI para devolver respuestas JSON.
- **BaseModel**: Una clase Pydantic para validación y serialización de datos.
- **MetaData**: Representa metadatos asociados con un envío (por ejemplo, directorio, jurisdicción, nombre de la firma).
- **Legal500Submission**: Un modelo Pydantic para datos de envío específicos de Legal500.
- **ChambersSubmission**: Un modelo Pydantic para datos de envío específicos de Chambers & Partners.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `run_workflow_task` | `job_id: str`, `initial_state: dict`, `config: dict` | Ejecuta el flujo de trabajo principal de LangGraph en un hilo secundario, actualiza el estado y el progreso del trabajo en `JOBS_DB` y almacena los resultados finales del procesamiento. |
| `process_documents` | `request: Request`, `background_tasks: BackgroundTasks` | El punto final principal de la API (`/process`) que recibe las solicitudes de procesamiento de documentos, valida la entrada, construye el estado inicial, crea un ID de trabajo y añade la ejecución del flujo de trabajo como una tarea en segundo plano. |
| `get_status` | `job_id: str` | Un punto final de la API (`/status/{job_id}`) utilizado para consultar el estado y los resultados de un trabajo de procesamiento específico de la base de datos en memoria `JOBS_DB`. |