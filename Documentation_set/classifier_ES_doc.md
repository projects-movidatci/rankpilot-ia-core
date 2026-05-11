1. ## Información general:
Este archivo se encarga de la preparación inicial de documentos para su procesamiento. Decodifica archivos codificados en base64, extrae texto de formatos PDF y DOCX, y utiliza un Modelo de Lenguaje Grande (LLM) para clasificar el tipo de documento. También carga la configuración según el tipo de documento identificado y el objetivo de envío.

2. ## Clases:
* `DocumentClassification`: Un modelo Pydantic para definir el esquema de la clasificación de documentos basada en LLM, incluyendo el tipo de documento y una puntuación de confianza.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `classification_node` | `state: AgentState` | Orquesta el proceso de preparación del documento, incluyendo decodificación, extracción de texto, clasificación basada en LLM y carga de configuración. |