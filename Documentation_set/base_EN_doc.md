1. ## Overview:
This file defines an abstract base class `SubmissionStrategy` for implementing different strategies for submitting legal directory information (e.g., Legal500, Chambers). It outlines methods for auditing submission data against an ideal schema and assembling the final submission document.

2. ## Classes:
* `SubmissionStrategy`: An abstract base class defining the contract for specific submission strategies.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `audit` | `submission_data` (Dict[str, Any]) | Runs the Gap Analysis to compare the current JSON state against the 'Ideal Schema' of the specific template and returns a list of identified gaps. |
| `assemble` | `submission_data` (Dict[str, Any]), `output_path` (str) | Takes the complete JSON data and injects it into the respective .docx original template, returning the path to the final assembled file. |
| `_evaluate_nested_fields` | `data` (Dict[str, Any]), `required_fields` (List[str]), `strategy_name` (str) | Helper method to evaluate dot-notation fields recursively and return detailed gaps, identifying missing or null/empty fields. |