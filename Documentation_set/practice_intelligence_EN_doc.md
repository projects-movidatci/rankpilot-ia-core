1. ## Overview:
This file contains logic for generating practice-specific evaluation rules based on the directory type (e.g., Chambers, Legal500) and the practice area. It aims to provide tailored guidance on what aspects of legal work to highlight for different directories.

2. ## Classes:
There are no classes defined in the provided code snippet.

3. ## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| get_practice_rules | practice_area: str, directory_type: str | Returns the universal evaluation logic based on the practice area and directory type. It normalizes the practice area to uppercase and applies conditional logic to generate specific rule strings for Chambers and Legal500 directories. If no specific rules are found, it returns a standard or default message. |