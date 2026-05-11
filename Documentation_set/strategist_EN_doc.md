1. ## Overview:
This file defines data structures and a function for generating a strategic roadmap and executive summary for legal practice submissions based on provided raw text and identified gaps. It leverages a large language model (LLM) to process this information and produce a structured, actionable plan.

2. ## Classes:
*   **MilestoneSchema**: Defines the structure for an individual task or milestone in the strategic roadmap, including its category, title, justification, technical instructions, priority, and deadline.
*   **StrategistResponse**: Defines the overall structured output from the strategist agent, including a list of milestones, an overall score, a risk level, a strategic verdict for executives, and a full audit letter in markdown format.

3. ## Functions & Methods:
| Name            | Parameters            | Responsibility                                                                                                                                                                                                                                                           |
| :-------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| strategist_agent | state: AgentState     | Orchestrates the generation of a strategic roadmap and executive summary. It initializes an LLM with structured output capabilities, prepares the prompt with operational context and raw text, chains the prompt with the LLM, invokes the chain with relevant data, and returns the processed response to update the agent's state. |