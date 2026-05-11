1. ## Overview:
This file handles the initial preparation of documents for processing. It decodes base64 encoded files, extracts text from PDF and DOCX formats, and uses a Large Language Model (LLM) to classify the document type. It also loads configuration settings based on the identified document type and target submission.

2. ## Classes:
* `DocumentClassification`: A Pydantic model to define the schema for LLM-based document classification, including the document type and a confidence score.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `classification_node` | `state: AgentState` | Orchestrates the document preparation process, including decoding, text extraction, LLM-based classification, and configuration loading. |