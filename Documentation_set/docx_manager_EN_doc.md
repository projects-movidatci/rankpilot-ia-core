1. ## Overview:
This file provides utilities for generating Word documents from templates. It includes functions to extract text from DOCX files, particularly handling tables by converting them to Markdown format, and a core function to assemble a submission document by merging data into a DOCX template using Jinja2 templating.

2. ## Classes:
* `SilentUndefined`: A custom Jinja2 Undefined class that returns an empty string for undefined variables, preventing rendering errors.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `_clean_table_text` | `text: str` | Cleans text content from table cells by replacing newlines and pipe characters with spaces, ensuring Markdown table integrity. |
| `extract_text_from_docx` | `filepath: str` | Extracts all textual content from a DOCX file, including paragraphs and tables which are specifically formatted into Markdown. Returns `None` if the file is not found or cannot be read. |
| `_convert_booleans_to_yes_no` | `data` | Recursively traverses dictionaries and lists, converting boolean values to their string representations "Yes" or "No". |
| `assemble_submission` | `template_path: str`, `output_dir: str`, `submission_data: dict` | Generates a new DOCX document by merging `submission_data` into a `template_path` DOCX using `docxtpl`. It preprocesses the data by splitting lists based on a 'is_publishable' flag and converting booleans to 'Yes'/'No' strings. The output file is saved in `output_dir`. |