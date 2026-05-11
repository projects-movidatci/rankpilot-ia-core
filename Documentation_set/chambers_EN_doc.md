1. ## Overview:
   This file defines `ChambersStrategy`, a document submission strategy tailored for Chambers (Global and USA) publications. It leverages a YAML configuration file to define required fields and extract descriptive information for auditing. The strategy also includes logic for assembling the final document using a DOCX template, including data padding and formatting adjustments.

2. ## Classes:
   - `ChambersStrategy`: Implements the `SubmissionStrategy` and handles the logic for auditing and assembling Chambers submission documents.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `__init__` | `config_path: str = "configs/chambers_usa.yaml"` | Initializes the `ChambersStrategy` by setting the configuration path and loading the configuration from the specified YAML file. |
| `_load_config` |  | Reads the YAML configuration file and loads its content into `self.config`. Handles `FileNotFoundError` by initializing `self.config` to an empty dictionary. |
| `audit` | `submission_data: Dict[str, Any]` | Performs a gap analysis on the provided `submission_data` based on the `required_fields` defined in the loaded configuration. It identifies missing or empty fields and returns a list of identified gaps, including the field's dot-notation path and its description from the YAML. |
| `assemble` | `submission_data: Dict[str, Any]`, `output_path: str` | Assembles the Chambers submission document using a DOCX template. It transforms the input `submission_data` into a Jinja2 context, pads arrays to prevent `docxtpl` errors, applies boolean fixes for "Y/N" values, cleans up string data, and finally calls `assemble_submission` to generate the DOCX file. |