## Descripción general:
Este archivo define el esquema para un informe ejecutivo y construye una cadena Langchain para sintetizar varios datos de la firma en una carta de auditoría estratégica y métricas resumidas. El objetivo es generar un informe listo para la toma de decisiones para la junta directiva de una firma, destacando su situación actual, ventajas competitivas, riesgos y un plan de mejora.

## Clases:
| Nombre | Deber principal |
|---|---|
| ExecutiveWriterResponse | Define la estructura para la salida del informe ejecutivo, incluida una puntuación general, nivel de riesgo, veredicto estratégico y la carta de auditoría completa en markdown. |

## Funciones y métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| Field | description, default | Se utiliza dentro de los modelos Pydantic para proporcionar metadatos y valores predeterminados para los campos del modelo. |
| BaseModel |  | Clase base de Pydantic para crear modelos de datos con validación. |
| ChatOpenAI | temperature | Inicializa un modelo de chat de OpenAI con una temperatura especificada para controlar la creatividad de la salida. |
| ChatPromptTemplate.from_template | template | Crea una plantilla de prompt de chat a partir de una cadena dada, permitiendo la interpolación de variables. |
| get_llm | temperature | Recupera una instancia del Modelo de Lenguaje (LLM) con una configuración de temperatura especificada. |
| PydanticOutputParser | pydantic_object | Analiza la salida del LLM en un modelo Pydantic, realizando validación de datos. |
| ChatPromptTemplate.partial | format_instructions | Crea una versión parcial de una plantilla de prompt, prellenando variables específicas como las instrucciones de formato. |
| PydanticOutputParser.get_format_instructions |  | Genera las instrucciones necesarias para que el LLM formatee su salida de acuerdo con el modelo Pydantic especificado. |