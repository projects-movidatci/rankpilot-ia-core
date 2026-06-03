import yaml
from typing import Dict, Any, List
from src.strategies.base import SubmissionStrategy
from src.io.docx_manager import assemble_submission

class ChambersStrategy(SubmissionStrategy):
    """
    Submission strategy specifically for Chambers (Global and USA).
    Config-driven based on YAML definitions.
    """

    def __init__(self, config_path: str = "configs/chambers_usa.yaml"):
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
        Runs the Gap Analysis.
        CRITICAL: Outputs the FULL dot-notation path and the YAML Description!
        """
        required_fields = self.config.get("required_fields", [])
        
        # 🆕 EXTRACT THE SCHEMA DEFINITIONS FROM YAML
        yaml_schema = self.config.get("schema", {}).get("sections", {})
        gaps = []

        # Helper to safely check if a deeply nested path exists and has data
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

        # 🆕 HELPER TO GET THE RICH DESCRIPTION FROM YAML
        def get_yaml_description(field_path):
            parts = field_path.split('.')
            if len(parts) >= 2:
                section = parts[0]
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
                
                # 🆕 GET THE DESCRIPTION
                yaml_desc = get_yaml_description(field_path)
                
                # 🆕 PASS THE DESCRIPTION TO THE LLM
                reason = f"FIELD DEFINITION: {yaml_desc}" if yaml_desc else f"Please provide information for {friendly_name}."
                
                gaps.append({
                    "field": field_path, 
                    "reason": reason
                })
                
        return gaps

    def assemble(self, submission_data: Dict[str, Any], output_path: str) -> str:
        """
        Uses python-docx to prepare data and assemble the Chambers docx.
        Pads all arrays to prevent IndexError in docxtpl.
        """
        # =========================================================
        # 🧠 THE STRATEGIC SORT: Highest Score First
        # =========================================================
        def safe_sort_matters(matters_list: List[Dict]) -> List[Dict]:
            def get_score(matter: Dict) -> int:
                try:
                    # Navigate the nested dictionary safely
                    eval_data = matter.get("evaluation", {})
                    # If it's a Pydantic model inside the dict, use getattr, otherwise use .get
                    if hasattr(eval_data, "total_score"):
                        return int(getattr(eval_data, "total_score", 0))
                    return int(eval_data.get("total_score", 0))
                except Exception:
                    return 0
            
            # Sort in descending order (highest score first)
            return sorted(matters_list, key=get_score, reverse=True)

        # Apply the sort to the submission_data BEFORE creating the context
        pub_info = submission_data.get("D_publishable_information", {})
        if pub_info and "publishable_matters" in pub_info:
            pub_info["publishable_matters"] = safe_sort_matters(pub_info["publishable_matters"])

        conf_info = submission_data.get("E_confidential_information", {})
        if conf_info and "confidential_matters" in conf_info:
            conf_info["confidential_matters"] = safe_sort_matters(conf_info["confidential_matters"])
        # =========================================================

        # ==========================================
        # 1. TRANSLATION DICTIONARY (Pydantic -> Jinja2)
        # ==========================================
        context = {
            "SectionA": submission_data.get("A_preliminary_information", {}),
            "SectionB": submission_data.get("B_department_information", {}),
            "SectionC": submission_data.get("C_feedback", {}),
            "D_publishable_information": submission_data.get("D_publishable_information", {}),
            "E_confidential_information": submission_data.get("E_confidential_information", {}),
            "target_submission_type": submission_data.get("target_submission_type", "Chambers_Global")
        }

        # Ensure all base sections exist to prevent KeyErrors (Safe fallback)
        context.setdefault("SectionA", {})
        context.setdefault("SectionB", {})
        context.setdefault("SectionC", {})
        context.setdefault("D_publishable_information", {})
        context.setdefault("E_confidential_information", {})

        # FLAG FOR USA vs GLOBAL LOGIC:
        target_type = context.get("target_submission_type", "Chambers_Global")
        context["is_global_template"] = target_type == "Chambers_Global"

        # ---------------------------------------------------------
        # 1. THE PADDING ENGINE (Prevents docxtpl IndexErrors)
        # ---------------------------------------------------------
        def pad_array(parent_dict, key, required_length):
            arr = parent_dict.setdefault(key, [])
            while len(arr) < required_length:
                arr.append({})
            return arr

        # Pad Preliminary Info
        pad_array(context["SectionA"], "A4_contact_persons", 2)
        
        # Pad Department Info
        pad_array(context["SectionB"], "B4_department_heads", 2)
        pad_array(context["SectionB"], "B8_hires_departures_last_12_months", 3)
        pad_array(context["SectionB"], "B9_lawyers_ranked_unranked", 6)

        # Pad Feedback
        pad_array(context["SectionC"], "C1_barristers_advocates", 8)

        # ---------------------------------------------------------
        # 2. BOOLEAN FIXES FOR Y/N
        # ---------------------------------------------------------
        lawyers = context["SectionB"]["B9_lawyers_ranked_unranked"]
        for lawyer in lawyers:
            for key in ["is_partner", "is_ranked"]:
                val = lawyer.get(key)
                if val in [True, "True", "true", "Y", "Yes"]:
                    lawyer[key] = "Y"
                elif val in [False, "False", "false", "N", "No"]:
                    lawyer[key] = "N"
                else:
                    lawyer[key] = ""

        # ---------------------------------------------------------
        # 3. CLEANUP: Strip trailing newlines
        # ---------------------------------------------------------
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
                        
        clean_strings(context)

        # 4. BUILD THE DOCUMENT
        template_name = "USA_Chambers_submission_form_template.docx" if context["is_global_template"] else "USA_Chambers_submission_form_template.docx"
        template_path = f"templates/{template_name}"
        
        return assemble_submission(template_path, output_path, context)