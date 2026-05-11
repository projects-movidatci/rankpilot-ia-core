Aquí tienes la traducción al español del documento Markdown, manteniendo la estructura y las reglas especificadas:

1. ## Resumen:
Este archivo proporciona la funcionalidad para extraer contenido de texto, incluidas tablas renderizadas como markdown, de documentos PDF utilizando la biblioteca PyMuPDF.

2. ## Clases:
(Ninguna en este archivo)

3. ## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| _clean_table_text | `text` (str) | Limpia una cadena dada reemplazando caracteres de nueva línea y símbolos pipe por espacios para asegurar la compatibilidad con el formato de tabla markdown. |
| extract_text_from_pdf | `filepath` (str) | Extrae todo el texto de un archivo PDF especificado. Incluye lógica para detectar y renderizar tablas encontradas en cada página en un formato de tabla markdown. Devuelve el texto combinado o None si ocurre un error o no se encuentra el archivo. |