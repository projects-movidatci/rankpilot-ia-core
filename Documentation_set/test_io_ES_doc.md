1. ## Resumen:
Este archivo contiene pruebas unitarias para los módulos de manejo de documentos, específicamente para decodificar documentos codificados en base64 y extraer texto de archivos PDF y DOCX. Verifica la funcionalidad de `decode_base64_document`, `extract_text_from_pdf` y `extract_text_from_docx`.

2. ## Clases:
*   **TestBase64Handler**: Prueba la funcionalidad de la función `decode_base64_document`.
*   **TestTableExtraction**: Prueba la funcionalidad de `extract_text_from_pdf` y `extract_text_from_docx` para extraer texto, incluyendo estructuras de tablas.

3. ## Funciones y Métodos:

| Nombre                       | Parámetros        | Responsabilidad                                                                     |
| :------------------------- | :---------------- | :--------------------------------------------------------------------------------- |
| `decode_base64_document`   | `b64_string`      | Decodifica una cadena codificada en base64 y la guarda en un archivo con el nombre y ruta dados. |
|                            | `filename`        |                                                                                    |
|                            | `output_dir`      |                                                                                    |
| `test_decode_valid_document`|                   | Prueba la decodificación de una cadena base64 válida a un archivo DOCX y verifica su contenido. |
| `test_decode_invalid_extension`|              | Prueba la decodificación de una cadena base64 con una extensión inválida, esperando que no se cree ningún archivo. |
| `extract_text_from_pdf`    | `pdf_path`        | Extrae el contenido de texto de un archivo PDF, incluyendo estructuras de tablas incrustadas. |
| `extract_text_from_docx`   | `docx_path`       | Extrae el contenido de texto de un archivo DOCX, incluyendo estructuras de tablas incrustadas. |
| `setUp`                    |                   | Prepara archivos PDF y DOCX ficticios con tablas para las pruebas.                          |
| `test_extract_pdf_tables`  |                   | Prueba la extracción de datos de texto y tablas de un archivo PDF ficticio.                 |
| `test_extract_docx_tables` |                   | Prueba la extracción de datos de texto y tablas de un archivo DOCX ficticio.                |
| `tearDown`                 |                   | Limpia los archivos PDF y DOCX ficticios creados durante las pruebas.                     |