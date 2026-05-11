## Overview:
This file defines the `Legal500Strategy` class, which implements a submission strategy specifically tailored for Legal500 submissions. It loads configuration from a YAML file to define required fields for gap analysis and to customize the document assembly process. The strategy includes methods for auditing submission data against defined requirements and for assembling a structured Word document using a specified template.

## Classes:
* `Legal500Strategy`: Manages the configuration, conducts gap analysis, and assembles Legal500 submission documents.

## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `__init__` | `config_path: str` | Initializes the `Legal500Strategy` with a path to the configuration YAML file and loads the configuration. |
| `_load_config` | None | Loads the YAML configuration from the specified `config_path`. Handles `FileNotFoundError` by initializing an empty configuration. |
| `audit` | `submission_data: Dict[str, Any]` | Performs a gap analysis on the `submission_data` against the `required_fields` defined in the configuration. It uses dot notation to access nested fields and returns a list of identified gaps with reasons. |
| `assemble` | `submission_data: Dict[str, Any]`, `output_path: str` | Assembles the Legal500 submission document using the `python-docx` library. It processes and transforms the `submission_data` into a format suitable for templating, cleans up string data, and calls `assemble_submission` with a dynamically selected template. |