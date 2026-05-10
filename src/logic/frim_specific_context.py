from typing import Dict, Any

def get_firm_specific_context(submission_dict: Dict[str, Any], directory_type: str) -> str:
    """Scans the submission for specific triggers like major hires or cross-border volume."""
    firm_specific = []
    
    # 1. Detect Seismic Changes (Hires/Departures)
    dept_info = submission_dict.get("B_department_information", {})
    hires = dept_info.get("B8_hires_departures_last_12_months", []) if directory_type == "Chambers" else dept_info.get("hires_and_departures", [])
    real_hires = [h for h in hires if isinstance(h, dict) and str(h.get("name", "")).strip() not in ["", "N/A", "None"]]
    
    if len(real_hires) >= 2:
        firm_specific.append(f"SEISMIC CHANGE RULE: {len(real_hires)} relevant team moves detected. The narrative MUST NOT treat this as a simple update. Frame this as a structural shift in competitive capacity.")

    # 2. Detect Cross-Border Footprint
    cross_border_count = 0
    matters = submission_dict.get("D_publishable_information", {}).get("publishable_matters", []) + \
              submission_dict.get("E_confidential_information", {}).get("confidential_matters", [])
              
    for m in matters:
        cb_val = str(m.get("D4_cross_border_jurisdictions") or m.get("E4_cross_border", "")).lower()
        if "yes" in cb_val or "usa" in cb_val or "new york" in cb_val:
            cross_border_count += 1
            
    if cross_border_count >= 3:
        firm_specific.append(f"CORE BUSINESS RULE: Strong international footprint detected ({cross_border_count} cross-border matters). Highlight multi-jurisdictional coordination capabilities.")

    return " | ".join(firm_specific) if firm_specific else "Organic growth and standard operations."