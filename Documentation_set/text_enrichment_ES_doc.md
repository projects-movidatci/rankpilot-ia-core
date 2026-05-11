1. ## Resumen:
Este archivo proporciona utilidades para analizar formato de texto similar a markdown (negrita y etiquetas de color personalizadas) y convertirlo en objetos `docxtpl.RichText`. Incluye funciones para manejar conversiones de cadenas individuales y para procesar recursivamente diccionarios y listas.

2. ## Clases:
- `RichText`: (externa) Representa formato de texto enriquecido para documentos, probablemente para `docxtpl`.

3. ## Funciones y Métodos:

| Nombre                                     | Parámetros                                  | Responsabilidad                                                                                                                                                                                                                                                           |
| :--------------------------------------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parse_markdown_to_richtext`             | `text_string: str`                          | Convierte sintaxis específica similar a markdown (negrita `**texto**` y etiquetas de color rojo personalizadas `<red>texto</red>` usando marcadores internos `[RED_START]` y `[RED_END]`) dentro de una cadena en un objeto `docxtpl.RichText`. También maneja de manera inteligente y exagera los saltos de línea para Word. |
| `convert_all_markdown_to_richtext` | `data`                                      | Recorre recursivamente diccionarios y listas. Si se encuentra un valor de cadena que contiene sintaxis de negrita (`**`) o saltos de línea (`\n`), llama a `parse_markdown_to_richtext` para convertir esa cadena en su lugar en un objeto `RichText`. |