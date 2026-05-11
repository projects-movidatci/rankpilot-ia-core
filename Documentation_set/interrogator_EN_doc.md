## Overview:
This file contains the logic for the 'Interrogator Node', which is responsible for generating dynamic and strategic questions to fill in missing information (gaps) identified in the agent's state. It uses an LLM to create contextually relevant questions based on the current submission data, historical context, and specific strategic directives.

## Classes:
| Name | Primary Duty |
|---|---|
| StrategicQuestion | A Pydantic model to encapsulate the structured output from the LLM, specifically for a single question. |

## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| interrogator_node | state: AgentState | Generates dynamic, strategic questions for the fields marked as null or missing (gaps) using an LLM, incorporating extracted submission data, firm/practice area context, and strategic directives. |