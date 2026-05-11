1. ## Overview:
This file defines a function to parse a Chambers submission document, splitting it into logically defined sections (A, B, C, D, E). It dynamically identifies existing sections using regular expressions and segments the text accordingly.

2. ## Classes:
No classes are defined in this file.

3. ## Functions & Methods:

| Name                        | Parameters         | Responsibility                                                                                                                            |
| --------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| chunk_chambers_submission | text: str          | Splits a Chambers submission document into up to 5 logical chunks (A, B, C, D, E) based on predefined regex patterns. Dynamically handles missing sections. If no headers are found, returns the entire text as a single chunk. |