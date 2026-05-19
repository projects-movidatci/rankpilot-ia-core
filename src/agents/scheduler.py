from typing import Dict, Any
from src.core.state import AgentState
from src.chains.scheduler_chain import scheduler_chain
import datetime

def scheduler_node(state: AgentState) -> Dict[str, Any]:
    print("--- [NODE] Executing Strategic Scheduler ---")
    
    # 1. Recuperamos los objetos del estado
    core_data = getattr(state, "positioning_core", {})
    context_data = getattr(state, "strategic_context", {})
    submission_obj = getattr(state, "submission", None)
    metadata = getattr(state, "metadata", None)
    
    # --- EXTRACCIÓN AUTÓNOMA DE FIRMA (Desde los esquemas) ---
    dynamic_firm_name = "La firma"
    if submission_obj:
        sub_dict = submission_obj.model_dump() if hasattr(submission_obj, "model_dump") else (submission_obj if isinstance(submission_obj, dict) else {})
        # Búsqueda inteligente según el esquema (Legal 500, Chambers, o LL)
        if sub_dict.get("identity"):
            dynamic_firm_name = sub_dict["identity"].get("firm_name") or "La firma"
        elif sub_dict.get("A_preliminary_information"):
            dynamic_firm_name = sub_dict["A_preliminary_information"].get("A1_firm_name") or "La firma"
        elif sub_dict.get("firm_information"):
            dynamic_firm_name = sub_dict["firm_information"].get("firm_name") or "La firma"

    # --- EXTRACCIÓN DEL CONTEXTO ESTRATÉGICO ---
    def get_val(obj, key, default):
        return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

    realistic_target = get_val(context_data, "realistic_target", "Improve Ranking")
    evaluation_tone = get_val(context_data, "evaluation_tone", "Authoritative")
    # Sacamos la banda que guardó el selector de estrategia
    current_band = get_val(context_data, "current_band", "Unknown Band")

    # --- EXTRAER EL CORE DE POSICIONAMIENTO (ARQUETIPO Y MAQUILLAJE) ---
    selected_archetype = get_val(core_data, "practice_model", "Standard Firm")
    # Ahora sí sobrevivirá porque ya lo agregamos a Pydantic
    narrative_guidelines = get_val(core_data, "narrative_guidelines", "Focus on general optimization.")

    # --- RESTO DEL PROCESAMIENTO ---
    submission_deadline = getattr(metadata, "submission_deadline", "No deadline") if metadata else "No deadline"
    location = getattr(metadata, "location", "Global") if metadata else "Global"
    practice_area = getattr(metadata, "practice_area", "General Law") if metadata else "General Law"
    
    # Formatear Blind Spots
    raw_blind_spots = getattr(state, "blind_spots", [])
    print(f"Raw blind spots extracted for scheduler: {raw_blind_spots}")
    formatted_blind_spots = ""
    for bs in raw_blind_spots:
        issue = getattr(bs, 'issue', bs.get('issue', 'Unknown') if isinstance(bs, dict) else 'Unknown')
        formatted_blind_spots += f"- {issue}\n"

    submission_json = submission_obj.model_dump_json() if submission_obj else "{}"

    # --- DEBUG FINAL (AHORA SÍ, ANTES DE LLAMAR AL LLM) ---
    print("\n" + "🚀" * 30)
    print("📊 [DEBUG] VALORES FINALES PARA EL PROMPT DEL SCHEDULER")
    print("-" * 60)
    print(f" FIRMA (AUTÓNOMA) : {dynamic_firm_name}")
    print(f" BANDA ACTUAL     : {current_band}")
    print(f" TARGET (META)    : {realistic_target}")
    print(f" ARQUETIPO        : {selected_archetype}")
    
    print("\n📝 ESTRATEGIA DE NARRATIVA (NARRATIVE GUIDELINES):")
    if isinstance(narrative_guidelines, list):
        for i, g in enumerate(narrative_guidelines, 1): print(f"   {i}. {g}")
    else:
        print(f"   {narrative_guidelines}")
    print("-" * 60)
    print(f" PROCESANDO CON LLM...")
    print("🚀" * 30 + "\n")

    # Inyección final al LLM
    input_data = {
        "current_date": datetime.date.today().strftime("%B %d, %Y"),
        "submission_deadline": submission_deadline,
        "location": location,
        "practice_area": practice_area,
        "gaps": "Focus on narrative depth", 
        "blind_spots": formatted_blind_spots,
        "submission_json": submission_json,
        "realistic_target": realistic_target,
        "evaluation_tone": evaluation_tone,
        "selected_archetype": selected_archetype,
        "narrative_guidelines": narrative_guidelines,
        "firm_name": dynamic_firm_name,    
        "current_band": current_band       
    }

    try:
        response = scheduler_chain.invoke(input_data)
        return {
            "evolution_path": [m.model_dump() for m in response.evolution_path],
            "current_step": "scheduler_complete" 
        }
    except Exception as e:
        print(f"!!! Scheduler Parser Failure: {e}")
        import traceback
        traceback.print_exc()
        return {"evolution_path": [], "errors": [f"Scheduler Error: {e}"]}