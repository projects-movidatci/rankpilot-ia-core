Aquí tienes la traducción del Markdown del inglés al español, manteniendo la estructura de tablas y sin traducir los identificadores entre comillas invertidas:

## Resumen:
Este archivo actúa como un módulo de fábrica y utilidad para seleccionar y configurar estrategias de envío, determinar rutas de archivos de configuración, identificar clases de esquemas correspondientes y generar un marco de evaluación contextual para envíos legales.

## Clases:
- `SubmissionStrategy`: Clase base para todas las estrategias de envío.
- `Legal500Strategy`: Estrategia específica para envíos de Legal500.
- `ChambersStrategy`: Estrategia específica para envíos de Chambers.
- `LeadersLeagueStrategy`: Estrategia específica para envíos de Leaders League.
- `Legal500Submission`: Esquema para datos de envío de Legal500.
- `ChambersSubmission`: Esquema para datos de envío de Chambers.
- `LeadersLeagueSubmission`: Esquema para datos de envío de Leaders League.

## Funciones y Métodos:

| Nombre                  | Parámetros                               | Responsabilidad                                                                                                                                                                     |
| --------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_strategy`        | `sub_type: str`, `config: Dict[str, Any]` | Selecciona e instancia la `SubmissionStrategy` apropiada basándose en el `sub_type` proporcionado. También asigna la `config` dada a la estrategia. Por defecto es `Legal500Strategy`. |
| `get_config_path`     | `current_target: str`, `guide: str`      | Determina la ruta correcta del archivo YAML de configuración basándose en el tipo de envío `current_target` y las palabras clave encontradas dentro de la cadena `guide`.          |
| `get_schema_class`    | `sub_type: str`                          | Devuelve la clase de esquema Pydantic correspondiente (`Legal500Submission`, `ChambersSubmission` o `LeadersLeagueSubmission`) basándose en el `sub_type`. Por defecto es `Legal500Submission`. |
| `get_strategic_context` | `submission_dict: dict`                  | Analiza un `submission_dict` para determinar un objetivo realista para la evaluación, definir un tono de evaluación apropiado y proporcionar una biblioteca completa de posibles arquetipos de bufete.   |