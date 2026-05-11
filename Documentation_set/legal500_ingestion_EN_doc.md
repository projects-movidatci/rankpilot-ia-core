## Overview:
This file contains a node for ingesting and extracting structured data specifically for Legal 500 submissions from raw text. It utilizes the `Legal500Submission` Pydantic schema and a `ChatOpenAI` model with structured output capabilities to ensure a strict 1:1 mapping of extracted information.

## Classes:
- `ChatOpenAI`: Used for interacting with OpenAI's chat models (specifically `gpt-4o`).
- `ChatPromptTemplate`: Used to define templated prompts for the LLM.
- `AgentState`: Represents the state of the agent, holding extracted text and other relevant information.
- `Legal500Submission`: A Pydantic schema defining the expected structure of Legal 500 submission data.

## Functions & Methods:

| Name                       | Parameters                                | Responsibility                                                                                                                                    |
| -------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `legal500_ingestion_node`  | `state: AgentState`                       | Ingests raw text, configures an LLM with structured output for the `Legal500Submission` schema, defines a specialized prompt, and invokes the LLM to extract and map data. Handles potential exceptions during extraction. |