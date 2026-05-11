1. ## Resumen:
Este archivo define estructuras de datos y una función para generar una hoja de ruta estratégica y un resumen ejecutivo para envíos de prácticas legales basándose en texto sin procesar proporcionado e identificar lagunas. Aprovecha un modelo de lenguaje grande (LLM) para procesar esta información y producir un plan estructurado y procesable.

2. ## Clases:
*   **MilestoneSchema**: Define la estructura para una tarea o hito individual en la hoja de ruta estratégica, incluyendo su categoría, título, justificación, instrucciones técnicas, prioridad y fecha límite.
*   **StrategistResponse**: Define la salida estructurada general del agente estratega, incluyendo una lista de hitos, una puntuación general, un nivel de riesgo, un veredicto estratégico para ejecutivos y una carta de auditoría completa en formato markdown.

3. ## Funciones y Métodos:
| Nombre            | Parámetros            | Responsabilidad                                                                                                                                                                                                                                                           |
| :---------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| strategist_agent | state: AgentState     | Orquesta la generación de una hoja de ruta estratégica y un resumen ejecutivo. Inicializa un LLM con capacidades de salida estructurada, prepara el prompt con contexto operativo y texto sin procesar, encadena el prompt con el LLM, invoca la cadena con datos relevantes y devuelve la respuesta procesada para actualizar el estado del agente. |