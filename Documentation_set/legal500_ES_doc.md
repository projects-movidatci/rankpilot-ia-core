## Resumen:
Este archivo define la clase `Legal500Strategy`, que implementa una estrategia de envío específicamente diseñada para envíos de Legal500. Carga la configuración de un archivo YAML para definir los campos requeridos para el análisis de brechas y para personalizar el proceso de ensamblaje del documento. La estrategia incluye métodos para auditar los datos de envío comparándolos con los requisitos definidos y para ensamblar un documento de Word estructurado utilizando una plantilla especificada.

## Clases:
* `Legal500Strategy`: Gestiona la configuración, realiza análisis de brechas y ensambla documentos de envío de Legal500.

## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `__init__` | `config_path: str` | Inicializa `Legal500Strategy` con la ruta al archivo YAML de configuración y carga la configuración. |
| `_load_config` | None | Carga la configuración YAML desde `config_path`. Maneja `FileNotFoundError` inicializando una configuración vacía. |
| `audit` | `submission_data: Dict[str, Any]` | Realiza un análisis de brechas en `submission_data` comparándolo con los `required_fields` definidos en la configuración. Utiliza notación de puntos para acceder a campos anidados y devuelve una lista de brechas identificadas con sus razones. |
| `assemble` | `submission_data: Dict[str, Any]`, `output_path: str` | Ensambla el documento de envío de Legal500 utilizando la biblioteca `python-docx`. Procesa y transforma `submission_data` a un formato adecuado para la creación de plantillas, limpia los datos de tipo cadena y llama a `assemble_submission` con una plantilla seleccionada dinámicamente. |