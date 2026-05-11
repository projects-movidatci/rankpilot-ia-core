1. ## Overview:
This file provides utilities to parse markdown-like text formatting (bold and custom color tags) and convert it into `docxtpl.RichText` objects. It includes functions to handle individual string conversions and to recursively process dictionaries and lists.

2. ## Classes:
- `RichText`: (external) Represents rich text formatting for documents, likely for `docxtpl`.

3. ## Functions & Methods:

| Name                                     | Parameters                                  | Responsibility                                                                                                                                                                                                                                                           |
| :--------------------------------------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parse_markdown_to_richtext`             | `text_string: str`                          | Converts specific markdown-like syntax (bold `**text**` and custom red color tags `<red>text</red>` using internal `[RED_START]` and `[RED_END]` markers) within a string into a `docxtpl.RichText` object. It also intelligently handles and exaggerates line breaks for Word. |
| `convert_all_markdown_to_richtext` | `data`                                      | Recursively traverses through dictionaries and lists. If a string value is encountered that contains bold syntax (`**`) or line breaks (`\n`), it calls `parse_markdown_to_richtext` to convert that string in place into a `RichText` object. |