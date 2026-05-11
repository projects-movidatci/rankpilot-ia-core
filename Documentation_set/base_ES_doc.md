1. ## Vista general:
Este archivo define una clase base abstracta `SubmissionStrategy` para implementar diferentes estrategias de envío de información de directorios legales (por ejemplo, Legal500, Chambers). Describe métodos para auditar los datos de envío frente a un esquema ideal y ensamblar el documento de envío final.

2. ## Clases:
* `SubmissionStrategy`: Una clase base abstracta que define el contrato para estrategias de envío específicas.

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `audit` | `submission_data` (Dict[str, Any]) | Ejecuta el Análisis de Brechas para comparar el estado JSON actual contra el 'Esquema Ideal' de la plantilla específica y devuelve una lista de las brechas identificadas. |
| `assemble` | `submission_data` (Dict[str, Any]), `output_path` (str) | Toma los datos JSON completos e los inyecta en la plantilla original .docx respectiva, devolviendo la ruta al archivo final ensamblado. |
| `_evaluate_nested_fields` | `data` (Dict[str, Any]), `required_fields` (List[str]), `strategy_name` (str) | Método auxiliar para evaluar campos de notación de puntos recursivamente y devolver brechas detalladas, identificando campos faltantes o nulos/vacíos. |