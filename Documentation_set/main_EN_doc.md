1. ## Overview:
This file defines a FastAPI application acting as an API for a document processing and submission workflow. It handles incoming requests, initiates background processing using LangGraph, and provides endpoints for job status polling. The workflow involves document classification, data ingestion, sanitization, auditing for gaps, and potentially generating executive summaries and strategic roadmaps.

2. ## Classes:
- **AgentStatePayload**: Defines the structure for the input agent state, encompassing document data, submission details, metadata, and interaction history.
- **FastAPI**: The main application instance from the FastAPI framework.
- **Request**: Represents an incoming HTTP request.
- **BackgroundTasks**: A utility to run tasks in the background.
- **JSONResponse**: A FastAPI utility for returning JSON responses.
- **BaseModel**: A Pydantic class for data validation and serialization.
- **MetaData**: Represents metadata associated with a submission (e.g., directory, jurisdiction, firm name).
- **Legal500Submission**: A Pydantic model for Legal500 specific submission data.
- **ChambersSubmission**: A Pydantic model for Chambers & Partners specific submission data.

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| `run_workflow_task` | `job_id: str`, `initial_state: dict`, `config: dict` | Executes the main LangGraph workflow in a background thread, updates job status and progress in `JOBS_DB`, and stores the final processing results. |
| `process_documents` | `request: Request`, `background_tasks: BackgroundTasks` | The main API endpoint (`/process`) that receives document processing requests, validates input, constructs the initial state, creates a job ID, and adds the workflow execution as a background task. |
| `get_status` | `job_id: str` | An API endpoint (`/status/{job_id}`) used for polling the status and results of a specific processing job from the in-memory `JOBS_DB`. |