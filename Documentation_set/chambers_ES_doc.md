1. ## Resumen:
   Este archivo define `ChambersStrategy`, una estrategia de envío de documentos adaptada para las publicaciones de Chambers (Global y USA). Aprovecha un archivo de configuración YAML para definir los campos requeridos y extraer información descriptiva para auditoría. La estrategia también incluye lógica para ensamblar el documento final utilizando una plantilla DOCX, incluyendo relleno de datos y ajustes de formato.

2. ## Clases:
   - `ChambersStrategy`: Implementa `SubmissionStrategy` y maneja la lógica para auditar y ensamblar documentos de envío de Chambers.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `__init__` | `config_path: str = "configs/chambers_usa.yaml"` | Inicializa `ChambersStrategy` estableciendo la ruta de configuración y cargando la configuración desde el archivo YAML especificado. |
| `_load_config` |  | Lee el archivo de configuración YAML y carga su contenido en `self.config`. Maneja `FileNotFoundError` inicializando `self.config` a un diccionario vacío. |
| `audit` | `submission_data: Dict[str, Any]` | Realiza un análisis de brechas en los `submission_data` proporcionados basándose en los `required_fields` definidos en la configuración cargada. Identifica campos faltantes o vacíos y devuelve una lista de las brechas identificadas, incluyendo la ruta del campo en notación de puntos y su descripción del YAML. |
| `assemble` | `submission_data: Dict[str, Any]`, `output_path: str` | Ensambla el documento de envío de Chambers utilizando una plantilla DOCX. Transforma los `submission_data` de entrada en un contexto de Jinja2, rellena matrices para prevenir errores de `docxtpl`, aplica correcciones booleanas para valores "S/N", limpia los datos de cadena y finalmente llama a `assemble_submission` para generar el archivo DOCX. |