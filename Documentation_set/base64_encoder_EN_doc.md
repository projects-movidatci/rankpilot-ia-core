## Overview:
This file provides utility functions for encoding files into Base64 strings.

## Classes:
N/A

## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| encode_file_to_base64 | filepath: str | Reads a file from the given filepath, encodes its binary content into a Base64 string, and returns it. Returns None if the file is not found or an error occurs during encoding. |