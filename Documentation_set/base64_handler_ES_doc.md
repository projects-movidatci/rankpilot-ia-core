1. ## Resumen:
Este archivo contiene funciones de utilidad para manejar documentos codificados en base64, específicamente para decodificarlos y guardarlos en un directorio especificado después de validar sus extensiones de archivo.

2. ## Clases:
No hay clases definidas en este archivo.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `decode_base64_document` | `b64_string`: str, `filename`: str, `output_dir`: str = "/tmp" | Decodifica una cadena codificada en base64 a un archivo. Sanea el nombre del archivo, valida la extensión del archivo contra una lista predefinida de extensiones permitidas ('.docx', '.pdf', '.xlsx'), maneja posibles prefijos de URI de datos en la cadena base64, decodifica la cadena, crea el directorio de salida si no existe y guarda los datos decodificados en la ruta de archivo especificada. Devuelve la ruta al archivo guardado en caso de éxito, o `None` si la extensión del archivo no es compatible o si ocurre un error durante la decodificación o el guardado. |