1. ## Overview:
This file contains a function to analyze a submission dictionary and identify firm-specific strategic contexts based on predefined rules related to major hires/departures and cross-border activity.

2. ## Classes:
None

3. ## Functions & Methods:

| Name | Parameters | Responsibility |
|---|---|---|
| get_firm_specific_context | `submission_dict: Dict[str, Any]`, `directory_type: str` | Analyzes the `submission_dict` to detect seismic changes (hires/departures) and cross-border footprint. It returns a string summarizing the detected contexts, or a default message if no specific contexts are found. |