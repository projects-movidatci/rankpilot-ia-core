1. ## Overview:
This file contains utility functions for handling base64 encoded documents, specifically for decoding and saving them to a specified directory after validating their file extensions.

2. ## Classes:
There are no classes defined in this file.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| decode_base64_document | b64_string: str, filename: str, output_dir: str = "/tmp" | Decodes a base64 encoded string into a file. It sanitizes the filename, validates the file extension against a predefined list of allowed extensions ('.docx', '.pdf', '.xlsx'), handles potential data URI prefixes in the base64 string, decodes the string, creates the output directory if it doesn't exist, and saves the decoded data to the specified file path. Returns the path to the saved file on success, or None if the file extension is unsupported or an error occurs during decoding or saving. |