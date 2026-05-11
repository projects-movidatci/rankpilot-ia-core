1. ## Overview:
This file provides functionality to extract text content, including tables rendered as markdown, from PDF documents using the PyMuPDF library.

2. ## Classes:
(None in this file)

3. ## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| _clean_table_text | `text` (str) | Cleans a given string by replacing newline characters and pipe symbols with spaces to ensure compatibility with markdown table formatting. |
| extract_text_from_pdf | `filepath` (str) | Extracts all text from a specified PDF file. It includes logic to detect and render tables found on each page into a markdown table format. Returns the combined text or None if an error occurs or the file is not found. |