1. ## Resumen: Este archivo define modelos Pydantic y cadenas Langchain diseñadas para procesar y optimizar texto legal para diversos propósitos, incluyendo narrativas de firma, descripciones de asuntos y resúmenes de trabajo. Aprovecha los LLM para transformar la entrada bruta en contenido pulido y líder en el mercado.
2. ## Clases:
    - `OptimizedNarrative`: Representa la salida estructurada para una narrativa de firma optimizada, que contiene secciones de "qué nos diferencia" e "iniciativas e innovación".
    - `OptimizedMatter`: Representa la salida estructurada para una descripción de asunto legal optimizada.
    - `OptimizedSummary`: Representa la salida estructurada para un resumen legal condensado.
3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
| --- | --- | --- |
| `get_llm` | `temperature` (float) | Recupera una instancia de Modelo de Lenguaje configurado. |
| `ChatPromptTemplate.from_template` | `template` (str) | Crea una plantilla de prompt para interactuar con Modelos de Lenguaje Grandes basados en chat. |
| `BaseModel` | N/A | Clase base para crear modelos de datos con validación, requerida para modelos Pydantic. |
| `Field` | `description` (str), `default` (any) | Se utiliza dentro de modelos Pydantic para proporcionar metadatos y valores predeterminados para los campos del modelo. |
| `LLM.with_structured_output` | `model` (clase del modelo Pydantic), `output_parser` (opcional) | Configura un LLM para devolver la salida en un formato estructurado, típicamente parseado en un modelo Pydantic. |