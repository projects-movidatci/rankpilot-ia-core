## Overview:
This file defines the `audit_node` function, which performs a gap analysis. It compares existing submission data against an ideal schema, while also accounting for fields that the user has explicitly dismissed. The function also includes logic to defensively reload configuration if it's missing from the agent's state.

## Classes:
* **AgentState**: Represents the current state of the agent, holding information like submission data, configuration, and dismissed gaps.

## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| audit_node | state: AgentState | Compares submission data against a schema, filters out dismissed gaps, and adds a special gap if the submission deadline is missing. |