1. ## Overview:
This file contains unit tests for the document handling modules, specifically for decoding base64 encoded documents and extracting text from PDF and DOCX files. It verifies the functionality of `decode_base64_document`, `extract_text_from_pdf`, and `extract_text_from_docx`.

2. ## Classes:
*   **TestBase64Handler**: Tests the functionality of the `decode_base64_document` function.
*   **TestTableExtraction**: Tests the functionality of `extract_text_from_pdf` and `extract_text_from_docx` for extracting text, including table structures.

3. ## Functions & Methods:

| Name                       | Parameters        | Responsibility                                                                     |
| :------------------------- | :---------------- | :--------------------------------------------------------------------------------- |
| `decode_base64_document`   | `b64_string`      | Decodes a base64 encoded string and saves it to a file with the given filename and path. |
|                            | `filename`        |                                                                                    |
|                            | `output_dir`      |                                                                                    |
| `test_decode_valid_document`|                   | Tests decoding a valid base64 string into a DOCX file and verifies its content.  |
| `test_decode_invalid_extension`|              | Tests decoding a base64 string with an invalid extension, expecting no file creation. |
| `extract_text_from_pdf`    | `pdf_path`        | Extracts text content from a PDF file, including embedded table structures.        |
| `extract_text_from_docx`   | `docx_path`       | Extracts text content from a DOCX file, including embedded table structures.       |
| `setUp`                    |                   | Sets up dummy PDF and DOCX files with tables for testing.                          |
| `test_extract_pdf_tables`  |                   | Tests the extraction of text and table data from a dummy PDF file.                 |
| `test_extract_docx_tables` |                   | Tests the extraction of text and table data from a dummy DOCX file.                |
| `tearDown`                 |                   | Cleans up the dummy PDF and DOCX files created during testing.                     |