1. ## Descripción general:
Este archivo define el flujo de trabajo para un proceso de procesamiento y análisis de documentos utilizando LangGraph. Orquesta una serie de nodos de agente estructurados en tres actos: Captura de datos, Pulido y Ensamblaje, y Diagnóstico estratégico. El flujo de trabajo maneja la clasificación de documentos, la ingesta, la sanitización, la auditoría, la interacción del usuario, la optimización y la redacción ejecutiva final.

2. ## Clases:
*   `StateGraph`: Una clase de la biblioteca `langgraph` utilizada para definir un flujo de trabajo de máquina de estados.
*   `AgentState`: Representa el objeto de estado pasado entre nodos, que contiene datos y configuración para los agentes.

3. ## Funciones y Métodos:

| Nombre                     | Parámetros                     | Responsabilidad                                                                                                                                                                      |
| :----------------------- | :----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `route_entry`            | `state: AgentState`            | Reenvía el flujo de trabajo en función de si hay una nueva respuesta del usuario presente. Si es así, va a `process_answer_node`; de lo contrario, procede a `classification_node`.         |
| `route_after_audit`      | `state: AgentState`            | Determina el siguiente paso después de la auditoría. Si se detectan lagunas, va a `interrogator_node`; de lo contrario, procede a `optimize_node` para iniciar el Acto II.               |
| `route_after_classification` | `state: AgentState`            | Dirige el flujo de trabajo después de la clasificación del documento en función del tipo de documento detectado por IA y los metadatos especificados por el usuario. Selecciona nodos de ingesta específicos o uno genérico. |
| `build_workflow`         |                                | Construye y compila la máquina de estados de LangGraph, definiendo nodos y las transiciones entre ellos a lo largo de los tres actos del flujo de trabajo.                          |