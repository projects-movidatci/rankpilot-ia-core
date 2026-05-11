# RankPilot: Intelligent Legal Submission Automation

RankPilot is a sophisticated system designed to automate and optimize the process of creating, auditing, and submitting legal firm information to prominent directories such as Legal500, Chambers, and Leaders League. It leverages advanced AI, including Large Language Models (LLMs), to ingest documents, extract and structure data, identify submission gaps, generate strategic insights, and assemble polished final documents. The system aims to reduce manual effort, ensure compliance with directory requirements, and enhance the quality and impact of legal firm submissions.

## Introduction

This document serves as a comprehensive guide to the RankPilot codebase. It outlines the project's overview, architecture, key components, and provides guidance on getting started. RankPilot represents a significant advancement in legal tech, streamlining a complex and time-consuming process into an efficient, AI-driven workflow.

## Project Overview

RankPilot automates the intricate process of preparing and submitting law firm data to legal ranking directories. It begins by ingesting various document formats (PDF, DOCX), classifying their type, and extracting relevant text. Using LLMs, it then structures this information according to predefined schemas for directories like Legal500, Chambers, and Leaders League. The system critically audits submissions for missing information or "gaps," strategically interrogates users for clarifications, and optimizes content for clarity and impact. Finally, it generates executive summaries, strategic roadmaps, and assembles the final, submission-ready documents.

The core of RankPilot is built around an agentic workflow orchestrated by LangGraph, enabling modular processing and dynamic adaptation to user input and identified issues. The system is designed for robustness, incorporating error handling, data sanitization, and intelligent retries.

## Architecture & Design

RankPilot employs a modular, agent-based architecture, heavily influenced by modern AI development patterns, particularly LangGraph for orchestrating complex sequential and conditional workflows.

*   **Agentic Workflow:** The system is composed of numerous "agent nodes," each responsible for a specific task within the overall submission process (e.g., classification, ingestion, auditing, sanitization, optimization, strategy generation). These agents interact by passing an `AgentState` object, which encapsulates the current status and data of the processing job.
*   **LangGraph Orchestration:** LangGraph is used to define the state machine that governs the flow between these agents. This allows for dynamic routing based on the output of previous agents, creating adaptive and resilient workflows. Key routing functions (`route_entry`, `route_after_audit`, `route_after_classification`) manage transitions between different stages of the submission process.
*   **LLM Integration:** Extensive use of Large Language Models (LLMs) is central to RankPilot's functionality. LLMs are employed for:
    *   Document classification.
    *   Data extraction and structuring into Pydantic schemas.
    *   Gap analysis and question generation.
    *   Text sanitization and optimization.
    *   Strategic analysis, executive summary generation, and roadmap creation.
    *   `langchain-openai` and related libraries are used for LLM interactions, often with structured output parsers leveraging Pydantic models.
*   **Pydantic Schemas:** For robust data validation and serialization, Pydantic models are used extensively. These schemas define the expected structure for submission data across different directories (Legal500, Chambers, Leaders League), agent states, and intermediate processing steps.
*   **Strategy Pattern:** For handling different legal directories and their specific requirements, a strategy pattern is implemented. Modules like `chambers`, `legal500`, and `leaders_league` each implement a `SubmissionStrategy` interface, providing tailored `audit` and `assemble` methods.
*   **Modular Design:** Components are organized into logical directories (`agents`, `chains`, `core`, `io`, `logic`, `strategies`, `utils`). This modularity promotes reusability, maintainability, and testability. For example, input/output operations are separated into the `io` module, while core logic resides in `core`.
*   **API Layer:** A FastAPI application (`main.py`) provides an API entry point for processing requests. It manages job queuing and status tracking, allowing external systems or frontends to interact with the RankPilot workflow asynchronously.
*   **Simulation & Testing:** Companion scripts like `interactive_test.py` and `local_workflow_test.py` facilitate local development and testing of the workflow, simulating frontend interactions and end-to-end execution. Unit tests are also present for various modules.

## Directory Guide

```
rankpilot-core/
├── agents/               # Contains all AI agent modules responsible for specific tasks.
│   ├── answer_evaluator.py
│   ├── assembler.py
│   ├── auditor.py
│   ├── chambers_ingestion.py
│   ├── classifier.py
│   ├── executive_writer.py
│   ├── extractor.py
│   ├── interrogator.py
│   ├── legal500_ingestion.py
│   ├── optimizer.py
│   ├── sanitizer.py
│   ├── scheduler.py
│   ├── snapshot_generator.py
│   ├── strategist.py
│   └── updater.py
├── chains/               # Houses Langchain chains for specific LLM-driven processes.
│   ├── executive_writer_chain.py
│   ├── optimizer_chain.py
│   ├── scheduler_chain.py
│   └── snapshot_chain.py
├── configs/              # Configuration files, likely including YAMLs for strategy settings.
├── core/                 # Core utilities and foundational components.
│   ├── engine.py
│   ├── llm.py
│   ├── schemas.py
│   ├── state.py
│   └── workflow.py
├── data/                 # Placeholder for data files (raw, processed).
│   ├── processed/
│   └── raw/
├── Documentation_set/    # Documentation related to the project.
├── src/                  # Source code directory, mirroring the top-level structure.
│   ├── agents/           # Detailed implementation of agents.
│   ├── chains/           # Detailed implementation of chains.
│   ├── core/             # Detailed implementation of core components.
│   ├── io/               # Input/Output utilities (file handling, encoding).
│   ├── logic/            # Business logic and context generation.
│   └── strategies/       # Implementations of submission strategies.
│       ├── base.py
│       ├── chambers.py
│       ├── leaders_league.py
│       └── legal500.py
├── templates/            # Document templates used for assembly.
├── tests/                # Unit and integration tests.
│   ├── test_io.py
│   ├── test_schemas.py
│   ├── test_strategies.py
│   ├── test_workflow.py
│   └── __init__.py
├── utils/                # General utility functions.
├── interactive_test.py   # Script for interactive testing of the workflow.
├── local_workflow_test.py # Script for local end-to-end workflow testing.
├── main.py               # FastAPI application for the RankPilot API.
└── simulador_frontend.py # CLI simulation of a frontend interacting with the API.
```

## Component Table

| Module                       | Responsibility                                                                          | Key Features                                                                                                                                                                                                                              |
| :--------------------------- | :-------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agents/answer_evaluator.py` | Processes user answers, determines intent (fill, dismiss, clarify), updates submission. | Pydantic `AnswerIntent` model, LLM-based answer analysis, nested field updates.                                                                                                                                                           |
| `agents/assembler.py`        | Orchestrates document assembly from processed data.                                     | Filename sanitization, strategy selection for assembly, markdown to rich text conversion, final document placement.                                                                                                                       |
| `agents/auditor.py`          | Performs gap analysis against a schema, accounting for dismissed fields.                | Compares submission data to ideal schema, identifies missing fields, includes deadline checks.                                                                                                                                             |
| `agents/classifier.py`       | Classifies document types using LLMs and loads relevant configurations.                 | Base64 decoding, PDF/DOCX text extraction, LLM-based document type classification, configuration loading based on classification.                                                                                                              |
| `agents/extractor.py`        | Ingests and structures extracted text into defined schemas using LLMs.                  | Schema factory for different submission types, LLM for structured data extraction, error handling with schema fallback, metadata injection.                                                                                                  |
| `agents/executive_writer.py` | Synthesizes data into executive reports and audit letters.                              | Utilizes `executive_writer_chain`, prepares LLM input from state, processes LLM output for high-authority reports.                                                                                                                        |
| `agents/interrogator.py`     | Generates strategic questions to fill identified submission gaps.                       | Pydantic `StrategicQuestion` schema, LLM-driven question generation based on context and gaps, dynamic and contextually relevant questions.                                                                                              |
| `agents/optimizer.py`        | Refines and enhances submission content (narratives, work highlights).                  | Leverages `optimizer_chain`, applies copywriting guidelines, optimizes across different content types (narratives, matters, summaries).                                                                                                   |
| `agents/sanitizer.py`        | Cleans and sanitizes text data in submission objects.                                   | Identifies long string fields, batch processing with LLM for cleaning, `CleanedField` and `SanitizationBatch` models, recursive data structure traversal.                                                                               |
| `agents/scheduler.py`        | Generates a strategic roadmap (5-step plan) for firms.                                  | Utilizes `scheduler_chain`, extracts strategic data from state, formats LLM input, generates `evolution_path` and `current_step`.                                                                                                       |
| `agents/snapshot_generator.py`| Generates a final strategic snapshot and archetype classification.                      | Orchestrates `archetype_chain` and `snapshot_chain`, processes state data for analysis, outputs structured evaluation snapshot.                                                                                                           |
| `agents/strategist.py`       | Generates strategic roadmaps and executive summaries from raw text and gaps.            | Employs LLM for structured output, creates `MilestoneSchema` and `StrategistResponse` models, synthesizes actionable plans.                                                                                                               |
| `agents/updater.py`          | Processes user answers to update submission data via `SubmissionPatch`.                 | Pydantic `FieldUpdate` and `SubmissionPatch` schemas, LLM for answer translation and structuring, `deep_update_field` for merging updates.                                                                                                |
| `chains/`                    | Langchain chains for specific LLM-driven tasks.                                         | Encapsulates prompts, LLMs, and output parsers for complex text generation and structuring tasks (e.g., executive writing, optimization, scheduling, snapshotting).                                                                          |
| `core/llm.py`                | Factory for creating configured LLM instances.                                          | Supports OpenAI and OpenRouter, environment-specific configurations, optional diagnostic message logging.                                                                                                                                   |
| `core/schemas.py`            | Pydantic models for structuring submission data for different directories.            | Comprehensive schemas for Legal500, Chambers, Leaders League submissions, including identity, departments, clients, matters, feedback, etc.                                                                                                   |
| `core/state.py`              | Defines the `AgentState` model and related data structures.                           | Centralized state management, sanitization utilities (`sanitize_nulls_from_php`, `normalize_submission_type`, `sanitize_php_garbage`), handling of user answers (`sanitize_new_answer`).                                                         |
| `core/workflow.py`           | Defines the main LangGraph workflow for document processing.                            | State machine definition (`StateGraph`), agent node orchestration (Acts I, II, III), routing logic for dynamic workflow progression.                                                                                                          |
| `io/`                        | Input/Output utilities.                                                                 | Base64 encoding/decoding, DOCX and PDF parsing, text enrichment, strategy selection utilities.                                                                                                                                             |
| `logic/`                     | Business logic, context generation, and rule definitions.                               | Firm-specific contexts, market contexts, practice intelligence rules, ranking history analysis, strategic objectives.                                                                                                                        |
| `strategies/`                | Implementations of specific submission strategies.                                      | `Legal500Strategy`, `ChambersStrategy`, `LeadersLeagueStrategy` subclasses providing `audit` and `assemble` methods based on directory-specific YAML configurations.                                                                        |
| `templates/`                 | DOCX templates for generating final submission documents.                             | Placeholder for template files used by `docxtpl` during the assembly process.                                                                                                                                                           |
| `interactive_test.py`        | Simulates a stateless frontend for testing the backend API.                             | PDF upload simulation, base64 encoding, iterative answering of backend questions, HTTP POST requests to API.                                                                                                                            |
| `local_workflow_test.py`     | Orchestrates end-to-end workflow execution in a local test environment.                 | Simulates user submission (document/text), state management, interactive gap filling, diagnostic output, final document saving.                                                                                                              |
| `main.py`                    | FastAPI application serving as the RankPilot API.                                       | API endpoints for document processing (`/process`) and status polling (`/status/{job_id}`), background task management for workflow execution, job database simulation (`JOBS_DB`).                                                              |
| `simulador_frontend.py`      | Command-line interface (CLI) simulation of the RankPilot frontend.                      | User input options (upload, raw text, blank slate), polling backend API for status, displaying progress and results, simulating strategic analysis interactions.                                                                             |

## Getting Started

To get started with RankPilot, follow these general steps:

1.  **Prerequisites:**
    *   Python 3.9+
    *   `pip` package manager

2.  **Cloning the Repository:**
    ```bash
    git clone <repository_url>
    cd rankpilot-core
    ```

3.  **Setting up a Virtual Environment:**
    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Installing Dependencies:**
    Install all required Python packages.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is not explicitly provided, you would typically install packages listed in the module summaries or inferred from imports.)*

5.  **Environment Variables:**
    Ensure that necessary environment variables are set, particularly for API keys (e.g., `OPENAI_API_KEY`, `OPENROUTER_API_KEY`) and potentially for environment configuration (`ENVIRONMENT`). Refer to `.env.example` if available for guidance.

6.  **Running the Simulated Frontend/API:**
    *   **To run the FastAPI backend:**
        ```bash
        uvicorn main:app --reload
        ```
    *   **To run the local workflow test:**
        ```bash
        python local_workflow_test.py
        ```
    *   **To run the interactive test (simulating frontend API calls):**
        ```bash
        python interactive_test.py --filepath /path/to/your/document.pdf
        ```
    *   **To run the CLI simulator:**
        ```bash
        python simulador_frontend.py
        ```

7.  **Configuration:**
    *   Review and adjust configuration files in the `configs/` directory as needed, especially for different legal directories.
    *   Ensure API keys and other sensitive information are managed securely.

This setup provides a foundation for running RankPilot's core functionalities, testing workflows, and interacting with the system. For specific use cases or development beyond these basics, consult the individual module documentation and the `Documentation_set` directory.