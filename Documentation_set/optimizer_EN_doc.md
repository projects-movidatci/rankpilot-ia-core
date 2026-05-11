1. ## Overview:
This file contains the logic for the Submission Optimizer node, designed to enhance and refine submission content (like narratives and legal matters) based on provided guidelines and context.

2. ## Classes:
*   **AgentState**: Represents the current state of the agent, holding information like submission data and configuration.

3. ## Functions & Methods:

| Name      | Parameters      | Responsibility                                                                                                                                                                                                                                                         |
| :-------- | :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| optimize_node | state: AgentState | Orchestrates the optimization process for submission content, including narratives, work highlights summaries, and both publishable and confidential legal matters. It applies copywriting guidelines and leverages specialized chains for each content type. |