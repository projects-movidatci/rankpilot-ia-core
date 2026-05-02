from src.chains.snapshot_chain import snapshot_chain, archetype_chain
from src.core.state import AgentState
from src.io.strategy_selector import get_strategic_context

def snapshot_generator_node(state: AgentState):
    print("--- [NODE] Generating Final Snapshot ---")
    
    try:
        # Reemplazo total de .get() por getattr
        submission_obj = getattr(state, "submission", None)
        submission_dict = submission_obj.model_dump(exclude_none=True) if submission_obj else {}
        submission_json = submission_obj.model_dump_json() if submission_obj else getattr(state, "raw_text", "")
        
        metadata = getattr(state, "metadata", None)
        practice_area = getattr(metadata, "practice_area", "Unknown") if metadata else "Unknown"
        history = getattr(state, "history", [])
        config = getattr(state, "config", {})
        
        # Para diccionarios internos (como config), .get() sigue siendo válido, 
        # pero para el 'state', usamos getattr
        guidelines = config.get("copywriting_guidelines", "Standard evaluation")

        # Contexto Estratégico
        context = get_strategic_context(submission_dict)
        
        # 2. En lugar de usar .get() directamente, usamos getattr con un fallback
        # Esto blinda el código incluso si 'context' llegara a ser un objeto o None
        target = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("realistic_target", "Ranked Position")
        tone = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("evaluation_tone", "Objective")
        archetypes = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("possible_archetypes", "Standard Practice")

        # PASO 1: Clasificador (Sin la variable 'selected_archetype' en el input)[cite: 3]
        archetype_result = archetype_chain.invoke({
            "possible_archetypes": archetypes,
            "practice_area": practice_area,
            "submission_json": submission_json,
            "realistic_target": target
        })

        raw_guidelines = archetype_result.narrative_guidelines
        
        # PASO 2: Auditoría/Maquillaje[cite: 3]
        result = snapshot_chain.invoke({
            "submission_json": submission_json,
            "history": "\n".join(history) if history else "No history.",
            "practice_area": practice_area,
            "editorial_rules": guidelines,
            "realistic_target": target,
            "evaluation_tone": tone,
            "selected_archetype": archetype_result.selected_archetype,
            "narrative_guidelines": raw_guidelines
        })
        
        return {
            "strategic_context": context,
            "positioning_core": {
                "practice_model": archetype_result.selected_archetype,
                "practice_definition": archetype_result.brief_justification,
                "narrative_guidelines": archetype_result.narrative_guidelines,
                "confidence_score": result.confidence_score,
                "signals": result.signals
            },
            "positioning_tier": result.positioning_tier.model_dump(),
            "blind_spots": [bs.model_dump() for bs in result.blind_spots],
            "competitive_advantage": result.competitive_advantage
        }

    except Exception as e:
        print(f"!!! Error Crítico en Generación de Snapshot: {e}")
        import traceback
        traceback.print_exc()
        return {
            "errors": [f"Snapshot Error: {str(e)}"],
            "positioning_tier": {"label": "Error", "explanation": "System failure."},
            "positioning_core": {"practice_model": "Unknown", "practice_definition": "Error in generation"}
        }