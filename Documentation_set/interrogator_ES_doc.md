## Resumen:
Este archivo contiene la lógica para el 'Nodo Interrogador', que es responsable de generar preguntas dinámicas y estratégicas para rellenar información faltante (brechas) identificadas en el estado del agente. Utiliza un LLM para crear preguntas contextualmente relevantes basadas en los datos de envío actuales, el contexto histórico y directivas estratégicas específicas.

## Clases:
| Nombre | Deber Principal |
|---|---|
| StrategicQuestion | Un modelo Pydantic para encapsular la salida estructurada del LLM, específicamente para una sola pregunta. |

## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| interrogator_node | state: AgentState | Genera preguntas dinámicas y estratégicas para los campos marcados como nulos o faltantes (brechas) utilizando un LLM, incorporando datos de envío extraídos, contexto de la firma/área de práctica y directivas estratégicas. |