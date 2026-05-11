1. ## Overview:
This file defines the workflow for a document processing and analysis pipeline using LangGraph. It orchestrates a series of agent nodes structured into three acts: Data Capture, Polishing and Assembly, and Strategic Diagnosis. The workflow handles document classification, ingestion, sanitization, auditing, user interaction, optimization, and final executive writing.

2. ## Classes:
*   `StateGraph`: A class from the `langgraph` library used to define a state machine workflow.
*   `AgentState`: Represents the state object passed between nodes, containing data and configuration for the agents.

3. ## Functions & Methods:

| Name                     | Parameters                     | Responsibility                                                                                                                                                       |
| :----------------------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `route_entry`            | `state: AgentState`            | Reroutes the workflow based on whether a new user answer is present. If yes, it goes to `process_answer_node`; otherwise, it proceeds to `classification_node`.         |
| `route_after_audit`      | `state: AgentState`            | Determines the next step after auditing. If gaps are detected, it goes to `interrogator_node`; otherwise, it proceeds to `optimize_node` to start Act II.               |
| `route_after_classification` | `state: AgentState`            | Routes the workflow after document classification based on AI-detected document type and user-specified metadata. Selects specific ingestion nodes or a generic one. |
| `build_workflow`         |                                | Constructs and compiles the LangGraph state machine, defining nodes and the transitions between them across the three acts of the workflow.                          |