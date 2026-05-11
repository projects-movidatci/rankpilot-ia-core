```markdown
1. ## Overview:
This file orchestrates the execution of a multi-stage workflow for processing legal submissions, simulating a local test environment for the RankPilot system. It handles document input, state management, interactive question answering, and final output generation, including a strategic diagnosis and assembled submission document.

2. ## Classes:
* `AgentState`: Represents the current state of the agent/workflow, containing information like submission details, metadata, documents, history, and current progress.
* `MetaData`: Contains metadata associated with a submission, such as directory, guide, region, jurisdiction, practice area, and firm name.

3. ## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| `main` | None | The entry point of the script. It initializes the workflow, simulates a user submission with a document or raw text, processes the submission through multiple workflow stages (including interactive gap filling), prints diagnostic information, and saves the final assembled document. |
```