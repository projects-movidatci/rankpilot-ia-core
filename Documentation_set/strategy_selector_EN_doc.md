## Overview:
This file acts as a factory and utility module for selecting and configuring submission strategies, determining configuration file paths, identifying corresponding schema classes, and generating a contextual evaluation framework for legal submissions.

## Classes:
- `SubmissionStrategy`: Base class for all submission strategies.
- `Legal500Strategy`: Strategy specific to Legal500 submissions.
- `ChambersStrategy`: Strategy specific to Chambers submissions.
- `LeadersLeagueStrategy`: Strategy specific to Leaders League submissions.
- `Legal500Submission`: Schema for Legal500 submission data.
- `ChambersSubmission`: Schema for Chambers submission data.
- `LeadersLeagueSubmission`: Schema for Leaders League submission data.

## Functions & Methods:

| Name                  | Parameters                               | Responsibility                                                                                                                                                                     |
| --------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_strategy`        | `sub_type: str`, `config: Dict[str, Any]` | Selects and instantiates the appropriate `SubmissionStrategy` based on the provided `sub_type`. It also assigns the given `config` to the strategy. Defaults to `Legal500Strategy`. |
| `get_config_path`     | `current_target: str`, `guide: str`      | Determines the correct configuration YAML file path based on the `current_target` submission type and keywords found within the `guide` string.                                       |
| `get_schema_class`    | `sub_type: str`                          | Returns the corresponding Pydantic schema class (`Legal500Submission`, `ChambersSubmission`, or `LeadersLeagueSubmission`) based on the `sub_type`. Defaults to `Legal500Submission`. |
| `get_strategic_context` | `submission_dict: dict`                  | Analyzes a `submission_dict` to determine a realistic target for evaluation, define an appropriate evaluation tone, and provide a comprehensive library of possible firm archetypes.   |