1. ## Overview:
This file defines the `scheduler_node` function, which acts as a strategic scheduler in an agent-based system. It processes state data to extract relevant information about the firm, submission, and strategic context, then formats this information into an input dictionary for a `scheduler_chain`. Finally, it invokes the chain and returns the processed response, including an `evolution_path` and the `current_step`.

2. ## Classes:
- `AgentState`: Represents the overall state of the agent, holding various data attributes like `positioning_core`, `strategic_context`, `submission`, `metadata`, and `blind_spots`.

3. ## Functions & Methods:

| Name           | Parameters                               | Responsibility                                                                                                                                                                                                                          |
|----------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `scheduler_node` | `state: AgentState`                      | Orchestrates the extraction of strategic data from the `AgentState`, formats it for a downstream chain, invokes the `scheduler_chain`, and returns the structured output.                                                              |
| `get_val`      | `obj`, `key`, `default`                  | A helper function to safely retrieve a value from a dictionary or object attribute, providing a default if the key/attribute is not found.                                                                                             |