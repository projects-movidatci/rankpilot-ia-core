## Resumen:
Este archivo define la función `audit_node`, que realiza un análisis de brechas. Compara los datos de envío existentes con un esquema ideal, teniendo en cuenta también los campos que el usuario ha descartado explícitamente. La función también incluye lógica para recargar la configuración de forma defensiva si falta en el estado del agente.

## Clases:
* **AgentState**: Representa el estado actual del agente, manteniendo información como datos de envío, configuración y brechas descartadas.

## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `audit_node` | state: AgentState | Compara los datos de envío con un esquema, filtra las brechas descartadas y añade una brecha especial si falta la fecha límite de envío. |