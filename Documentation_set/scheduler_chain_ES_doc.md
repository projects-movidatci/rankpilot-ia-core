1. ## Resumen:
Este archivo define las estructuras de datos y los prompts para un planificador estratégico que genera una hoja de ruta de 5 pasos para que un bufete de abogados alcance su objetivo realista en las clasificaciones legales, considerando varios contextos operativos y directivas estratégicas.

2. ## Clases:
- `MilestoneSchema`: Representa un único hito estratégico en la hoja de ruta, incluyendo su categoría, título de acción, justificación, instrucciones técnicas, prioridad y fecha de finalización objetivo.
- `SchedulerResponse`: Encapsula la hoja de ruta estratégica completa como una lista de objetos `MilestoneSchema`.

3. ## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `Field` | `description` | Se utiliza dentro de los modelos Pydantic para proporcionar una descripción de los campos del modelo. |
| `ChatPromptTemplate.from_template` | `template` | Crea una plantilla de prompt de chat a partir de una cadena de plantilla dada, permitiendo la interpolación de variables. |
| `PydanticOutputParser` | `pydantic_object` | Inicializa un analizador de salida Pydantic, que está diseñado para analizar la salida del LLM en un modelo Pydantic especificado. |
| `parser.get_format_instructions` | None | Recupera las instrucciones de formato del analizador de salida Pydantic, que se utilizan típicamente para guiar la salida del LLM. |
| `get_llm` | `temperature` | Recupera una instancia de Modelo de Lenguaje configurada. |
| `STRATEGIC_SCHEDULER_PROMPT.partial` | `format_instructions` | Crea una versión parcial de la plantilla de prompt, prellenando ciertas variables como las instrucciones de formato. |
| `scheduler_chain` | None | Define una cadena de LLM que toma un prompt, lo envía a un LLM y luego analiza la salida del LLM utilizando un analizador Pydantic. |