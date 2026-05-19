from typing import Dict, Any
import json
from src.core.state import AgentState
from src.chains.executive_writer_chain import executive_writer_chain
import datetime

def executive_writer_node(state: AgentState) -> Dict[str, Any]:
    """
    Executive Writer Agent:
    Synthesizes all technical and strategic data into a high-authority 
    report and a formal Audit Letter.
    """
    print("--- [NODE] Finalizing Executive Synthesis ---")

    # 1. Extraer metadata
    metadata = getattr(state, "metadata", {})
    submission_obj = getattr(state, "submission", None)
    
    # =======================================================
    # 🛡️ FIX: EXTRACCIÓN BLINDADA DEL FIRM NAME Y PRACTICE AREA
    # Soporta tanto el esquema de Chambers como el de Legal 500
    # =======================================================
    firm_name = "the Firm"
    practice_area = "General Law"
    
    # Priority 1: Metadata
    if isinstance(metadata, dict):
        firm_name = metadata.get("firm_name", firm_name)
        practice_area = metadata.get("practice_area", practice_area)
    elif hasattr(metadata, "firm_name"):
        firm_name = getattr(metadata, "firm_name") or firm_name
        practice_area = getattr(metadata, "practice_area") or practice_area
        
    # Priority 2: Submission Object (Chambers & Legal 500 Fallbacks)
    if submission_obj:
        sub_dict = submission_obj.model_dump(exclude_none=True)
        if "A_preliminary_information" in sub_dict and sub_dict["A_preliminary_information"]:
            firm_name = sub_dict["A_preliminary_information"].get("A1_firm_name", firm_name)
            practice_area = sub_dict["A_preliminary_information"].get("A2_practice_area", practice_area)
        elif "identity" in sub_dict and sub_dict["identity"]:
            firm_name = sub_dict["identity"].get("firm_name", firm_name)
            practice_area = sub_dict["identity"].get("practice_area", practice_area)

    # 2. Formatear las entradas complejas a texto legible para el LLM
    pos_core = getattr(state, "positioning_core", {})
    pos_tier = getattr(state, "positioning_tier", {})
    comp_adv = getattr(state, "competitive_advantage", [])
    blind_spots = getattr(state, "blind_spots", [])
    evolution_path = getattr(state, "evolution_path", [])

    formatted_path = "\n".join([
        f"STEP {i+1}: {getattr(step, 'action_title', step.get('action_title', '')) if isinstance(step, dict) else getattr(step, 'action_title', '')} ({getattr(step, 'category', step.get('category', '')) if isinstance(step, dict) else getattr(step, 'category', '')})\n"
        f"WHY: {getattr(step, 'why_it_matters', step.get('why_it_matters', '')) if isinstance(step, dict) else getattr(step, 'why_it_matters', '')}\n"
        f"HOW: {getattr(step, 'technical_instruction', step.get('technical_instruction', '')) if isinstance(step, dict) else getattr(step, 'technical_instruction', '')}\n"
        f"TIMELINE: Must be completed by {getattr(step, 'target_completion_date', step.get('target_completion_date', 'N/A')) if isinstance(step, dict) else getattr(step, 'target_completion_date', 'N/A')}.\n"
        for i, step in enumerate(evolution_path)
    ]) if evolution_path else "No roadmap generated."

    formatted_blind_spots = "\n".join([
        f"- {bs.get('issue', '') if isinstance(bs, dict) else getattr(bs, 'issue', '')}" 
        for bs in blind_spots
    ]) if blind_spots else "None identified."

    # =======================================================
    # 🧠 NEW: INYECTAR TAXONOMY ANALYTICS AL PAYLOAD
    # =======================================================
    strategic_context = getattr(state, "strategic_context", {})
    taxonomy_analytics = strategic_context.get("taxonomy_analytics", {}) if isinstance(strategic_context, dict) else {}
    
    formatted_taxonomy = ""
    if taxonomy_analytics:
        cats = taxonomy_analytics.get("categories", [])
        roles = taxonomy_analytics.get("roles", [])
        comps = taxonomy_analytics.get("complexities", [])
        formatted_taxonomy = (
            f"\n\n--- HARD METRICS: TAXONOMY ANALYTICS ---\n"
            f"Core Categories: {', '.join(cats) if cats else 'None'}\n"
            f"Roles Played: {', '.join(roles) if roles else 'None'}\n"
            f"Complexities Leveraged: {', '.join(comps) if comps else 'None'}"
        )
    
    # We append the Taxonomy Analytics directly to the Positioning Core string
    # so the LLM reads it as part of the technical audit.
    pos_core_string = (json.dumps(pos_core) if isinstance(pos_core, dict) else str(pos_core)) + formatted_taxonomy

    current_date = datetime.date.today().strftime("%B %d, %Y")

    # 3. Preparar el Payload
    input_data = {
        "current_date": current_date,
        "firm_name": firm_name,
        "practice_area": practice_area,
        "positioning_tier": json.dumps(pos_tier) if isinstance(pos_tier, dict) else str(pos_tier),
        "competitive_advantage": ", ".join(comp_adv) if comp_adv else "General Practice",
        "gaps": "0 Structural Gaps (Fully optimized submission)", 
        "blind_spots": formatted_blind_spots,
        "evolution_path": formatted_path,
        "positioning_core": pos_core_string, # 👈 Modified Payload
        "history": "\n".join(getattr(state, "history", []))
    }
    
    try:
        print("--- [DEBUG] Calling Executive Writer LLM ---")
        response = executive_writer_chain.invoke(input_data)
        
        print(f"--- [DEBUG] Synthesis Complete. Overall Score: {response.overall_score} ---")

        # 4. Final State Update
        return {
            "executive_summary": {
                "overall_score": response.overall_score,
                "risk_level": response.risk_level,
                "strategic_verdict": response.strategic_verdict,
                "top_differentiators": comp_adv,
                "audit_letter_markdown": response.audit_letter_markdown
            },
            "current_step": "completed"
        }
    except Exception as e:
        print(f"--- [ERROR] Executive Writer Node Failed: {str(e)} ---")
        import traceback
        traceback.print_exc()
        return {
            "executive_summary": {
                "overall_score": 0,
                "risk_level": "Critical",
                "strategic_verdict": "Synthesis Failed. No actionable insights generated.",
                "top_differentiators": [],
                "audit_letter_markdown": "An error occurred during synthesis. Please review the logs."
            },
            "current_step": "completed_with_errors"
        }