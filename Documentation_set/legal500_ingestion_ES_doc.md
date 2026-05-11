## Resumen:
Este archivo contiene un nodo para la ingesta y extracción de datos estructurados específicamente para envíos de Legal 500 a partir de texto sin formato. Utiliza el esquema Pydantic `Legal500Submission` y un modelo `ChatOpenAI` con capacidades de salida estructurada para garantizar un mapeo estricto de 1:1 de la información extraída.

## Clases:
- `ChatOpenAI`: Se utiliza para interactuar con los modelos de chat de OpenAI (específicamente `gpt-4o`).
- `ChatPromptTemplate`: Se utiliza para definir plantillas de mensajes para el LLM.
- `AgentState`: Representa el estado del agente, conteniendo el texto extraído y otra información relevante.
- `Legal500Submission`: Un esquema Pydantic que define la estructura esperada de los datos de envío de Legal 500.

## Funciones y Métodos:

| Nombre                       | Parámetros                                | Responsabilidad                                                                                                                                    |
| -------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `legal500_ingestion_node`  | `state: AgentState`                       | Ingresa texto sin formato, configura un LLM con salida estructurada para el esquema `Legal500Submission`, define un mensaje especializado e invoca al LLM para extraer y mapear datos. Maneja excepciones potenciales durante la extracción. |