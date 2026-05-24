from src.core.state import AgentState
from src.io.strategy_selector import get_strategy, get_config_path
import yaml

def audit_node(state: AgentState) -> dict:
    """
    Audit Node (Gap Analysis & Strategic Diagnosis):
    Compares the current JSON against the "Ideal Schema" AND evaluates
    the subjective scores provided by the Rubric Evaluator.
    """
    updates = {"current_step": "audit", "messages": []}

    # =========================================================
    # ☢️ THE NUCLEAR OVERRIDE (Zombie Loop Prevention)
    # =========================================================
    # 🧠 THE CLEAN FIX: Read the flag from the dictionary
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
    
    # =========================================================
    # 🛡️ DEFENSE AGAINST STATE AMNESIA
    # =========================================================
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

    # 1. Get the raw structural gaps from the strategy (Empty fields)
    strategy = get_strategy(sub_type, state_config)
    raw_gaps = strategy.audit(submission_dict)
    
    # 2. Retrieve the fields the user wants to skip
    dismissed_gaps = getattr(state, "dismissed_gaps", [])
    
    # 3. Filter structural gaps
    filtered_gaps = [gap for gap in raw_gaps if gap.get("field") not in dismissed_gaps]

    # =========================================================
    # 🧠 NEW: STRATEGIC DIAGNOSIS (40% Category Rule)
    # =========================================================
    strategic_gaps = []
    
    max_scores = {
        "table_fit": 10, "transaction_significance": 10, "structural_complexity": 15,
        "legal_sophistication": 10, "firm_role_strength": 15, "client_prestige": 10,
        "cross_border_complexity": 10, "innovation_novelty": 10, "narrative_strength": 10
    }

    print(f"submission data arrived at audit node: {str(submission_data)[:500]}...")  # Debug print to check submission content

    if submission_data:
        # Helper function to process matters dynamically
        def evaluate_matters_for_gaps(matters_list, section_path):
            for idx, matter in enumerate(matters_list):
                if not matter.evaluation:
                    continue
                
                # Loop through all 9 criteria
                for category, max_val in max_scores.items():
                    cat_obj = getattr(matter.evaluation, category, None)
                    if cat_obj:
                        # 🛡️ THE 40% CHECK
                        if (cat_obj.score / max_val) <= 0.40:
                            # We target partner_additional_notes so the Optimizer finds it later
                            field_name = f"{section_path}.{idx}.partner_additional_notes"
                            if field_name not in dismissed_gaps:
                                strategic_gaps.append({
                                    "field": field_name,
                                    "reason": f"Strategic enhancement needed for '{category.replace('_', ' ').title()}' (Score: {cat_obj.score}/{max_val}). AI Feedback: {cat_obj.justification}"
                                })
                                # BREAK: Only create ONE gap per weak matter at a time to prevent interrogation fatigue
                                break 

        # Check Publishable Matters
        pub_info = getattr(submission_data, "D_publishable_information", None)
        if pub_info and getattr(pub_info, "publishable_matters", None):
            evaluate_matters_for_gaps(pub_info.publishable_matters, "D_publishable_information.publishable_matters")

        # Check Confidential Matters
        conf_info = getattr(submission_data, "E_confidential_information", None)
        if conf_info and getattr(conf_info, "confidential_matters", None):
            evaluate_matters_for_gaps(conf_info.confidential_matters, "E_confidential_information.confidential_matters")
    print(f"filtered structural gaps: {filtered_gaps}")
    # Combine structural data gaps with strategic narrative gaps
    active_gaps = filtered_gaps + strategic_gaps

    # =========================================================
    # METADATA DEADLINE CHECK (The Dictionary Trap Fix)
    # =========================================================
    # 1. 🛡️ SAFE STATE EXTRACTION
    if isinstance(state, dict):
        metadata = state.get("metadata", {}) or {}
    else:
        metadata = getattr(state, "metadata", None) or {}
        
    # 2. 🛡️ SAFE DEADLINE EXTRACTION
    if isinstance(metadata, dict):
        deadline = metadata.get("submission_deadline", "")
    else:
        deadline = getattr(metadata, "submission_deadline", "")

    print(f"Audit Node: Extracted deadline from state: '{deadline}'")
    print(f"metadata object type: {type(metadata)}; deadline type: {type(deadline)}")
    deadline = str(deadline).strip() if deadline else ""
    
    if not deadline or deadline == "No deadline provided":
        if "metadata.submission_deadline" not in dismissed_gaps:
            # We push this to the VERY TOP of the list because it dictates urgency
            active_gaps.insert(0, {
                "field": "metadata.submission_deadline",
                "reason": "The system requires the official submission deadline to calculate the strategic roadmap and urgency."
            })

    # 4. Update the state
    updates["gaps"] = active_gaps

    updates["messages"].append(
        f"Audit node: Found {len(raw_gaps)} structural gaps & {len(strategic_gaps)} strategic weaknesses. "
        f"Total active queue: {len(active_gaps)} gaps (ignored {len(dismissed_gaps)} dismissed)."
    )

    return updates