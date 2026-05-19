from src.chains.snapshot_chain import snapshot_chain, archetype_chain
from src.core.state import AgentState
from src.io.strategy_selector import get_strategic_context
from src.logic.ranking_history_context import get_unified_ranking_strategy

def snapshot_generator_node(state: AgentState):
    print("--- [NODE] Generating Final Snapshot ---")
    
    # 🛡️ THE FIX: Use the standard 'updates' dictionary pattern for safe serialization
    updates = {"current_step": "snapshot", "messages": []}
    
    try:
        submission_obj = getattr(state, "submission", None)
        submission_dict = submission_obj.model_dump(exclude_none=True) if submission_obj else {}
        submission_json = submission_obj.model_dump_json() if submission_obj else getattr(state, "raw_text", "")
        
        metadata = getattr(state, "metadata", None)
        practice_area = getattr(metadata, "practice_area", "Unknown") if metadata else "Unknown"
        history = getattr(state, "history", [])
        config = getattr(state, "config", {})
        target_dir = getattr(state, "target_submission_type", "Chambers")
        
        guidelines = config.get("copywriting_guidelines", "Standard evaluation")

        context = get_strategic_context(submission_dict)
        
        # =======================================================
        # 🧠 INYECCIÓN DEL HISTORIAL DE RANKING
        # =======================================================
        def scrub_val(val):
            v = str(val).strip()
            return "" if v.upper() in ["", "N/A", "UNKNOWN", "NONE", "NULL"] else v

        raw_band = ""
        raw_hist = ""
        if "A_preliminary_information" in submission_dict and submission_dict["A_preliminary_information"]:
            raw_band = submission_dict["A_preliminary_information"].get("current_band_status", "")
            raw_hist = submission_dict["A_preliminary_information"].get("ranking_history_trajectory", "")
        elif "identity" in submission_dict and submission_dict["identity"]:
            raw_band = submission_dict["identity"].get("current_band_status", "")
            raw_hist = submission_dict["identity"].get("ranking_history_trajectory", "")

        current_band = scrub_val(raw_band)
        ranking_history = scrub_val(raw_hist)

        if current_band and ranking_history:
            dynamics = get_unified_ranking_strategy(current_band, ranking_history, target_dir)
            target = dynamics.get("strategic_objective", "General Advancement")
            tone = dynamics.get("editorial_rules", "Objective")
        else:
            current_band = "Unknown"
            ranking_history = "Unknown"
            target = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("realistic_target", "Ranked Position")
            tone = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("evaluation_tone", "Objective")
        
        archetypes = getattr(context, "get", lambda k, d: context.get(k, d) if isinstance(context, dict) else d)("possible_archetypes", "Standard Practice")

        # =======================================================
        # 📊 EXTRACCIÓN DE ANALÍTICAS DE TAXONOMÍA
        # =======================================================
        taxonomy_stats = {
            "categories": set(),
            "roles": set(),
            "complexities": set()
        }
        
        if target_dir == "Chambers":
            pub_info = submission_dict.get("D_publishable_information", {})
            pub_matters = pub_info.get("publishable_matters", []) if pub_info else []
            conf_info = submission_dict.get("E_confidential_information", {})
            conf_matters = conf_info.get("confidential_matters", []) if conf_info else []
            
            for m in (pub_matters + conf_matters):
                taxonomy_obj = m.get("taxonomy", {})
                if taxonomy_obj:
                    cat = taxonomy_obj.get("primary_category")
                    role = taxonomy_obj.get("firm_role_taxonomy")
                    complexities = taxonomy_obj.get("complexity_indicators", [])
                    
                    if cat: taxonomy_stats["categories"].add(cat)
                    if role: taxonomy_stats["roles"].add(role)
                    for c in complexities: taxonomy_stats["complexities"].add(c)
        
        taxonomy_summary = (
            f"Core Categories Detected: {', '.join(taxonomy_stats['categories']) if taxonomy_stats['categories'] else 'None'}\n"
            f"Firm Roles Played: {', '.join(taxonomy_stats['roles']) if taxonomy_stats['roles'] else 'None'}\n"
            f"Complexities Leveraged: {', '.join(taxonomy_stats['complexities']) if taxonomy_stats['complexities'] else 'None'}"
        )

        enhanced_submission_json = f"--- TAXONOMY ANALYTICS ---\n{taxonomy_summary}\n\n--- OPTIMIZED SUBMISSION ---\n{submission_json}"

        # PASO 1: Clasificador
        archetype_result = archetype_chain.invoke({
            "possible_archetypes": archetypes,
            "practice_area": practice_area,
            "submission_json": enhanced_submission_json,
            "realistic_target": target
        })

        raw_guidelines = archetype_result.narrative_guidelines
        
        # PASO 2: Auditoría Estratégica
        result = snapshot_chain.invoke({
            "submission_json": enhanced_submission_json,
            "history": "\n".join(history) if history else "No history.",
            "practice_area": practice_area,
            "editorial_rules": guidelines,
            "realistic_target": target,
            "evaluation_tone": tone,
            "selected_archetype": archetype_result.selected_archetype,
            "narrative_guidelines": raw_guidelines,
            "current_band": current_band,        
            "ranking_history": ranking_history   
        })
        
        context["taxonomy_analytics"] = {
            "categories": list(taxonomy_stats["categories"]),
            "roles": list(taxonomy_stats["roles"]),
            "complexities": list(taxonomy_stats["complexities"])
        }

        print("✅ Snapshot successfully generated. Packing raw dictionaries for safe serialization.")

        # 🛡️ THE FIX: Return safe, raw Python dictionaries. Pydantic will auto-parse them.
        updates["strategic_context"] = context
        
        updates["positioning_core"] = {
            "practice_model": archetype_result.selected_archetype,
            "practice_definition": archetype_result.brief_justification,
            "narrative_guidelines": archetype_result.narrative_guidelines,
            "confidence_score": result.confidence_score,
            "signals": result.signals
        }
        print(f"archetipe_result: {archetype_result.selected_archetype}, {archetype_result.brief_justification}")
        print(f"Positioning core details: {updates['positioning_core']}")

        updates["positioning_tier"] = {
            "label": result.positioning_tier.label,
            "explanation": result.positioning_tier.explanation
        }
        
        updates["blind_spots"] = [
            {"issue": bs.issue, "description": bs.description} 
            for bs in result.blind_spots
        ]
        
        updates["competitive_advantage"] = result.competitive_advantage
        updates["messages"].append("Snapshot Node: Strategic diagnostic completed successfully.")

        return updates

    except Exception as e:
        print(f"!!! Error Crítico en Generación de Snapshot: {e}")
        import traceback
        traceback.print_exc()
        
        # Safe fallback
        updates["positioning_tier"] = {"label": "Error", "explanation": "System failure."}
        updates["positioning_core"] = {"practice_model": "Unknown", "practice_definition": "Error in generation"}
        updates["messages"].append(f"Snapshot Node Error: {e}")
        return updates