1. ## Overview:
This file simulates a command-line interface (CLI) for the RankPilot frontend. It allows users to initiate a processing job by providing input in three ways: uploading a document, pasting raw text, or starting with a blank slate. The simulator then polls a FastAPI backend for job status, displays progress, and handles the results, including strategic analysis and potential follow-up questions.

2. ## Classes:
There are no explicit classes defined in this script.

3. ## Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| `print_header` | `texto` | Prints a formatted header with a given text, surrounded by lines of '=' characters for visual separation. |
| `main` | None | Orchestrates the CLI simulation. It presents input options to the user, prepares the initial `agent_state`, sends the first request to the FastAPI backend, and enters a loop to poll for job status and handle responses until the job is completed or fails. It also processes and displays the final strategic analysis and audit room interactions. |