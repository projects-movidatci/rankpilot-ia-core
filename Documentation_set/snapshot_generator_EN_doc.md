## Overview:
This file defines a node responsible for generating a final snapshot based on the current agent state. It orchestrates calls to archetype and snapshot chains, processing various pieces of information from the state to produce a structured output.

## Classes:
- AgentState: Represents the state of the agent, containing submission data, metadata, history, and configuration.

## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| snapshot_generator_node | state: AgentState | Generates a final positioning snapshot by invoking archetype and snapshot chains, processing state data, and returning a structured dictionary of results or error information. |