1. ## Descripción general:
Este archivo define un nodo para un agente responsable de sanitizar y limpiar datos de texto dentro de objetos de envío. Identifica campos de cadena largos, los procesa en lotes utilizando un LLM con directrices editoriales y estratégicas específicas, y luego actualiza el objeto de envío con el texto limpiado.

2. ## Clases:
* **CleanedField**: Representa un campo individual que ha sido limpiado, almacenando su ruta original y el texto sanitizado.
* **SanitizationBatch**: Un contenedor para una lista de objetos `CleanedField`, que representa la salida de un lote de sanitización del LLM.

3. ## Funciones y Métodos:

| Nombre                  | Parámetros        | Responsabilidad                                                                                                                                                                                            |
| :---------------------- | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_long_string_fields` | `data: Any`, `path: str = ""` | Recorre recursivamente una estructura de datos anidada (diccionarios y listas) para encontrar todos los campos de cadena que exceden los 50 caracteres, devolviéndolos como un diccionario con sus rutas en notación de puntos como claves. |
| `apply_cleaned_field`    | `data: Any`, `path: str`, `clean_text: str` | Navega recursivamente una estructura de datos anidada utilizando una ruta de notación de puntos y actualiza el valor en la ubicación especificada con el `clean_text` proporcionado.                               |
| `sanitizer_node`       | `state: AgentState` | Orquesta el proceso de sanitización. Identifica campos de texto largos, los agrupa en lotes, envía cada lote a un LLM para su limpieza basándose en los avisos y directrices predefinidos, y luego actualiza el estado del agente con los datos de envío sanitizados. Maneja errores potenciales durante el procesamiento por lotes y la validación del esquema. |