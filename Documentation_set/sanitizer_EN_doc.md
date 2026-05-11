1. ## Overview:
This file defines a node for an agent responsible for sanitizing and cleaning text data within submission objects. It identifies long string fields, processes them in batches using an LLM with specific editorial and strategic guidelines, and then updates the submission object with the cleaned text.

2. ## Classes:
* **CleanedField**: Represents a single field that has been cleaned, storing its original path and the sanitized text.
* **SanitizationBatch**: A container for a list of `CleanedField` objects, representing the output of a sanitization batch from the LLM.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `get_long_string_fields` | `data: Any`, `path: str = ""` | Recursively traverses a nested data structure (dictionaries and lists) to find all string fields that exceed 50 characters, returning them as a dictionary with their dot-notation path as keys. |
| `apply_cleaned_field` | `data: Any`, `path: str`, `clean_text: str` | Recursively navigates a nested data structure using a dot-notation path and updates the value at the specified location with the provided `clean_text`. |
| `sanitizer_node` | `state: AgentState` | Orchestrates the sanitization process. It identifies long text fields, groups them into batches, sends each batch to an LLM for cleaning based on predefined prompts and guidelines, and then updates the agent's state with the sanitized submission data. It handles potential errors during batch processing and schema validation. |