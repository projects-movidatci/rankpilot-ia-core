import yaml
from typing import Dict, Any, List
from src.strategies.base import SubmissionStrategy
from src.io.docx_manager import assemble_submission

class ChambersMatterStrategy(SubmissionStrategy):
    """
    Submission strategy specifically for the single-matter 'Matters Assistant' (Act 0).
    Config-driven based on configs/chambers_matter.yaml.
    """

    def __init__(self, config_path: str = "configs/chambers_matter.yaml"):
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self.config = {}

    def audit(self, submission_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Runs the Gap Analysis for a single matter.
        Checks the required fields defined in chambers_matter.yaml.
        """
        required_fields = self.config.get("required_fields", [])
        yaml_schema = self.config.get("schema", {}).get("sections", {})
        gaps = []

        # Helper to safely check if a deeply nested path exists
        def get_nested_value(data, path):
            keys = path.split('.')
            curr = data
            try:
                for k in keys:
                    if k.isdigit():
                        curr = curr[int(k)]
                    else:
                        curr = curr[k]
                return curr
            except (KeyError, IndexError, TypeError):
                return None

        # Helper to fetch the rich description from the YAML schema
        def get_yaml_description(field_path):
            parts = field_path.split('.')
            if len(parts) >= 2:
                section = parts[0] # Usually 'matter'
                field_name = parts[-1]
                try:
                    return yaml_schema.get(section, {}).get("fields", {}).get(field_name, {}).get("description", None)
                except AttributeError:
                    return None
            return None

        for field_path in required_fields:
            val = get_nested_value(submission_data, field_path)
            
            is_empty_string = isinstance(val, str) and val.strip().upper() in ["", "N/A", "UNKNOWN", "NONE", "NULL"]
            
            if val is None or val == [] or is_empty_string:
                friendly_name = field_path.split('.')[-1].replace("_", " ").title()
                yaml_desc = get_yaml_description(field_path)
                
                # Pass the description to the LLM to guide the user during the Audit Interrogation
                reason = f"FIELD DEFINITION: {yaml_desc}" if yaml_desc else f"Please provide information for {friendly_name}."
                
                gaps.append({
                    "field": field_path, 
                    "reason": reason
                })
                
        return gaps

    def assemble(self, submission_data: Dict[str, Any], output_path: str) -> str:
        """
        Uses python-docx to prepare data and assemble the single-matter docx.
        """
        matter_data = submission_data.get("matter", {})
        
        # 1. Clean trailing newlines
        def clean_strings(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, str):
                        d[k] = v.strip()
                    elif isinstance(v, (dict, list)):
                        clean_strings(v)
            elif isinstance(d, list):
                for i in range(len(d)):
                    if isinstance(d[i], str):
                        d[i] = d[i].strip()
                    elif isinstance(d[i], (dict, list)):
                        clean_strings(d[i])
                        
        clean_strings(matter_data)

        # =========================================================
        # 🛡️ THE JINJA TEMPLATE FIX: Flatten Lists into Strings
        # =========================================================
        for key, value in matter_data.items():
            if isinstance(value, list):
                matter_data[key] = ", ".join(str(v) for v in value) if value else "None"

        # 3. Build the flat context dictionary for Jinja
        context = {
            "matter": matter_data
        }

        # 4. Render the single-matter template
        template_name = self.config.get("template_file", "chambers_single_matter_template.docx")
        template_path = f"templates/{template_name}"
        
        from src.io.docx_manager import assemble_submission
        return assemble_submission(template_path, output_path, context)