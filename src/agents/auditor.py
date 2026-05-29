from src.core.state import AgentState
from src.io.strategy_selector import get_strategy, get_config_path
import yaml

def audit_node(state: AgentState) -> dict:
    updates = {"current_step": "audit", "messages": []}

    ctx = getattr(state, "strategic_context", {})
    force_skip = ctx.get("force_skip_interview", False)
    
    if force_skip:
        updates["gaps"] = []
        updates["messages"].append("Audit node: SKIP_INTERVIEW override is active. Forcing 0 gaps.")
        return updates

    submission_data = getattr(state, "submission", None)
    if submission_data:
        if hasattr(submission_data, "model_dump"):
            submission_dict = submission_data.model_dump(exclude_none=True)
        else:
            submission_dict = submission_data
    else:
        submission_dict = {}

    sub_type = getattr(state, "target_submission_type", "Legal500")
    state_config = getattr(state, "config", {})
    
    if not state_config:
        updates["messages"].append("⚠️ Config was lost in state transmission. Reloading defensively...")
        metadata = getattr(state, "metadata", None)
        guide = getattr(metadata, "guide", "") if metadata else ""
        
        config_path = get_config_path(sub_type, guide)
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                state_config = yaml.safe_load(f)
                updates["config"] = state_config 
        except Exception as e:
            updates["messages"].append(f"❌ Audit Error loading config: {e}")

    strategy = get_strategy(sub_type, state_config)
    raw_gaps = strategy.audit(submission_dict)
    
    dismissed_gaps = getattr(state, "dismissed_gaps", [])
    filtered_gaps = [gap for gap in raw_gaps if gap.get("field") not in dismissed_gaps]

    strategic_gaps = []
    max_scores = {
        "table_fit": 10, "transaction_significance": 10, "structural_complexity": 15,
        "legal_sophistication": 10, "firm_role_strength": 15, "client_prestige": 10,
        "cross_border_complexity": 10, "innovation_novelty": 10, "narrative_strength": 10
    }

    if submission_data:
        def evaluate_matters_for_gaps(matters_list, section_path):
            for idx, matter in enumerate(matters_list):
                if not matter.evaluation:
                    continue
                for category, max_val in max_scores.items():
                    cat_obj = getattr(matter.evaluation, category, None)
                    if cat_obj:
                        if (cat_obj.score / max_val) <= 0.40:
                            field_name = f"{section_path}.{idx}.partner_additional_notes"
                            if field_name not in dismissed_gaps:
                                strategic_gaps.append({
                                    "field": field_name,
                                    "reason": f"Strategic enhancement needed for '{category.replace('_', ' ').title()}' (Score: {cat_obj.score}/{max_val}). AI Feedback: {cat_obj.justification}"
                                })
                                break 
            
            lawyer_profiles = getattr(state, "lawyer_profiles", [])
            if lawyer_profiles:
                for idx, profile in enumerate(lawyer_profiles):
                    p_dict = profile if isinstance(profile, dict) else (profile.model_dump() if hasattr(profile, "model_dump") else {})
                    eval_data = p_dict.get("rubric_evaluation", {})
                    if eval_data:
                        score = eval_data.get("total_readiness_score", 0)
                        if score <= 70:
                            field_name = f"lawyer_profiles.{idx}.additional_narrative"
                            if field_name not in dismissed_gaps:
                                lawyer_name = p_dict.get("name", "Unknown Lawyer")
                                strategic_gaps.append({
                                    "field": field_name,
                                    "reason": f"Strategic enhancement needed for {lawyer_name}. Readiness score is critically low ({score}/110). We need more impactful achievements, client prestige evidence, or clearer role definition to elevate their B9 narrative."
                                })

        pub_info = getattr(submission_data, "D_publishable_information", None)
        if pub_info and getattr(pub_info, "publishable_matters", None):
            evaluate_matters_for_gaps(pub_info.publishable_matters, "D_publishable_information.publishable_matters")

        conf_info = getattr(submission_data, "E_confidential_information", None)
        if conf_info and getattr(conf_info, "confidential_matters", None):
            evaluate_matters_for_gaps(conf_info.confidential_matters, "E_confidential_information.confidential_matters")

    active_gaps = filtered_gaps + strategic_gaps

    if isinstance(state, dict):
        metadata = state.get("metadata", {}) or {}
    else:
        metadata = getattr(state, "metadata", None) or {}
        
    if isinstance(metadata, dict):
        deadline = metadata.get("submission_deadline", "")
    else:
        deadline = getattr(metadata, "submission_deadline", "")

    deadline = str(deadline).strip() if deadline else ""
    
    if not deadline or deadline == "No deadline provided":
        if "metadata.submission_deadline" not in dismissed_gaps:
            active_gaps.insert(0, {
                "field": "metadata.submission_deadline",
                "reason": "The system requires the official submission deadline to calculate the strategic roadmap and urgency."
            })

    # 👇 THE PERFECTED 4-PILLAR UI CATEGORIZATION 👇
    for gap in active_gaps:
        field_lower = gap["field"].lower()
        
        if "lawyer_profiles" in field_lower:
            gap["ui_category"] = "lawyer_development"
        elif "publishable_matters" in field_lower and "partner_additional_notes" in field_lower:
            gap["ui_category"] = "publishable_narrative"
        elif "confidential_matters" in field_lower and "partner_additional_notes" in field_lower:
            gap["ui_category"] = "confidential_narrative"
        else:
            gap["ui_category"] = "structural_content"

    ui_options = []
    structural_count = sum(1 for g in active_gaps if g.get("ui_category") == "structural_content")
    pub_narrative_count = sum(1 for g in active_gaps if g.get("ui_category") == "publishable_narrative")
    conf_narrative_count = sum(1 for g in active_gaps if g.get("ui_category") == "confidential_narrative")
    lawyer_count = sum(1 for g in active_gaps if g.get("ui_category") == "lawyer_development")
    
    total_lawyers = len(getattr(state, "lawyer_profiles", []))

    if structural_count > 0:
        ui_options.append({"id": "category:structural_content", "title": "Structural Content", "subtitle": f"Missing {structural_count} key data points in the submission.", "count": structural_count})
    if pub_narrative_count > 0:
        ui_options.append({"id": "category:publishable_narrative", "title": "Publishable Matters", "subtitle": f"Elevate narrative for {pub_narrative_count} public deals.", "count": pub_narrative_count})
    if conf_narrative_count > 0:
        ui_options.append({"id": "category:confidential_narrative", "title": "Confidential Matters", "subtitle": f"Strengthen narrative for {conf_narrative_count} private deals.", "count": conf_narrative_count})
    if lawyer_count > 0:
        ui_options.append({"id": "category:lawyer_development", "title": "Lawyer Development", "subtitle": f"Improve {lawyer_count} weak profiles out of {total_lawyers} total lawyers.", "count": lawyer_count})

    updates["ui_audit_options"] = ui_options
    updates["gaps"] = active_gaps

    updates["messages"].append(
        f"Audit node: Found {len(raw_gaps)} structural gaps & {len(strategic_gaps)} strategic weaknesses. "
        f"Total active queue: {len(active_gaps)} gaps (ignored {len(dismissed_gaps)} dismissed)."
    )

    return updates