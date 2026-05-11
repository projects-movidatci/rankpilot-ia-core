## Overview:
This file defines the schema for an executive report and constructs a Langchain chain to synthesize various pieces of firm data into a strategic audit letter and summary metrics. The goal is to generate a decision-ready report for a firm's board of directors, highlighting their current standing, competitive advantages, risks, and a roadmap for improvement.

## Classes:
| Name | Primary Duty |
|---|---|
| ExecutiveWriterResponse | Defines the structure for the output of the executive report, including an overall score, risk level, strategic verdict, and the full audit letter in markdown. |

## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| Field | description, default | Used within Pydantic models to provide metadata and default values for model fields. |
| BaseModel |  | Pydantic's base class for creating data models with validation. |
| ChatOpenAI | temperature | Initializes an OpenAI chat model with a specified temperature for controlling output creativity. |
| ChatPromptTemplate.from_template | template | Creates a chat prompt template from a given string, allowing for variable interpolation. |
| get_llm | temperature | Retrieves an instance of the Language Model (LLM) with a specified temperature setting. |
| PydanticOutputParser | pydantic_object | Parses LLM output into a Pydantic model, performing data validation. |
| ChatPromptTemplate.partial | format_instructions | Creates a partial version of a prompt template, pre-filling specific variables like format instructions. |
| PydanticOutputParser.get_format_instructions |  | Generates the necessary instructions for the LLM to format its output according to the specified Pydantic model. |