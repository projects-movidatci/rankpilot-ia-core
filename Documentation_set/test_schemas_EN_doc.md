1. ## Overview:
This file contains unit tests for the `Legal500Submission` schema, ensuring that it correctly parses and validates JSON data against its defined structure.

2. ## Classes:
- `TestSchemas`: A class containing test methods for schema validation.

3. ## Functions & Methods:
| Name                                   | Parameters   | Responsibility                                                                                   |
| :------------------------------------- | :----------- | :----------------------------------------------------------------------------------------------- |
| `test_legal500_submission_schema_matches_json` | `self`       | Tests the `Legal500Submission` schema by creating a sample JSON, instantiating the schema from it, and asserting the correct data types and structure. |