from src.core.state import AgentState
from src.io.strategy_selector import get_strategy, get_config_path
import yaml

def audit_node(state: AgentState) -> dict:
    """
    Audit Node (Gap Analysis):
    Compares the current JSON against the "Ideal Schema" of the template,
    while explicitly ignoring fields the user has dismissed.
    """
    updates = {"current_step": "audit", "messages": []}

    submission_data = getattr(state, "submission", None)
    if submission_data:
        # Check if it's already a dict or a pydantic model
        if hasattr(submission_data, "model_dump"):
            submission_dict = submission_data.model_dump(exclude_none=True)
        else:
            submission_dict = submission_data
    else:
        submission_dict = {}

    sub_type = getattr(state, "target_submission_type", "Legal500")
    state_config = getattr(state, "config", {})
    
    # =========================================================
    # 🛡️ DEFENSA CONTRA AMNESIA DE ESTADO (EL BUG DEL SKIP)
    # =========================================================
    # Si el frontend o la red perdieron el 'config' (que es un JSON muy pesado), 
    # la estrategia asume que no hay reglas y devuelve 0 gaps.
    # Aquí forzamos su recarga silenciosa si está vacío.
    if not state_config:
        updates["messages"].append("⚠️ Config was lost in state transmission. Reloading defensively...")
        metadata = getattr(state, "metadata", None)
        guide = getattr(metadata, "guide", "") if metadata else ""
        
        config_path = get_config_path(sub_type, guide)
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                state_config = yaml.safe_load(f)
                updates["config"] = state_config # Lo volvemos a inyectar al estado
        except Exception as e:
            updates["messages"].append(f"❌ Audit Error loading config: {e}")

    # 1. Get the raw gaps from the strategy
    strategy = get_strategy(sub_type, state_config)
    raw_gaps = strategy.audit(submission_dict)
    
    # 2. Retrieve the fields the user wants to skip
    dismissed_gaps = getattr(state, "dismissed_gaps", [])
    
    # 3. Filter the gaps: Keep it only if the 'field' name is NOT in the dismissed list
    filtered_gaps = [gap for gap in raw_gaps if gap.get("field") not in dismissed_gaps]

    metadata = getattr(state, "metadata", None)
    deadline = getattr(metadata, "submission_deadline", "") if metadata else ""
    active_gaps = filtered_gaps 
    
    # Si la fecha está vacía o es la de por defecto, agregamos un gap especial
    if not deadline or deadline == "No deadline provided":
        # Verificamos que no haya sido descartado por el usuario
        if "metadata.submission_deadline" not in dismissed_gaps:
            active_gaps.append({
                "field": "metadata.submission_deadline",
                "reason": "The system requires the official submission deadline to calculate the strategic roadmap and urgency."
            })

    # 4. Update the state with the newly filtered list
    updates["gaps"] = active_gaps

    updates["messages"].append(
        f"Audit node: Found {len(raw_gaps)} raw gaps. "
        f"Filtered down to {len(active_gaps)} active gaps (ignored {len(dismissed_gaps)} dismissed)."
    )

    return updates