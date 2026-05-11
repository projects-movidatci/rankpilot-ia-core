1. ## Resumen:
Este archivo define las estructuras de datos (modelos) utilizadas para representar el estado de un proceso de presentación legal, incluyendo tanto los detalles generales de la presentación como los datos específicos generados por un motor "RankPilot" para análisis estratégico y posicionamiento competitivo.

2. ## Clases:
- `PositioningCore`: Contiene datos centrales relacionados con el posicionamiento estratégico de una presentación.
- `PositioningTier`: Define un nivel o grado de posicionamiento estratégico.
- `BlindSpot`: Representa un problema o inconveniente identificado en una presentación.
- `Milestone`: Describe un paso de acción específico en un plan estratégico.
- `ExecutiveSummary`: Resume la evaluación estratégica general y los hallazgos clave.
- `MetaData`: Contiene metadatos sobre la presentación, como detalles del archivo, región y fechas límite.
- `AgentState`: El modelo de estado principal, que unifica los datos de la presentación y los resultados del análisis de RankPilot.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `sanitize_nulls_from_php` | `data: Any` | Sanea los datos convirtiendo los valores `None` en diccionarios a cadenas vacías, probablemente para manejar problemas de transferencia de datos entre sistemas (por ejemplo, desde PHP). |
| `normalize_submission_type` | `value: Optional[str]` | Limpia y normaliza las cadenas del tipo de presentación a un formato consistente (por ejemplo, "Legal500", "Chambers"). |
| `sanitize_php_garbage` | `v: Optional[Any]` | Limpia posibles estructuras de datos "basura" (como `stdClass`) que podrían originarse de sistemas PHP dentro de campos específicos del modelo `submission`. |
| `sanitize_new_answer` | `v: Any` | Asegura que el diccionario `new_answer` tenga las claves esperadas (`target_field`, `question_text`, `answer`) y que sus valores sean cadenas de texto, convirtiendo valores faltantes o no-cadenas a cadenas vacías. |