import json
from typing import Any, Union, List, Dict, Optional, Literal
from pydantic import BaseModel, Field, ValidationError
from src.core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from src.core.state import AgentState

class AnswerIntent(BaseModel):
    action: Literal["fill", "dismiss", "clarify"] = Field(
        description="Must be 'fill' (valid data), 'dismiss' (user skips), or 'clarify' (user asks a question or is confused)."
    )
    extracted_value: str = Field(
        description="The extracted data. If action is clarify, leave blank."
    )

    class Config:
        extra = "forbid"

# ==========================================
# UTILITIES: Obtener y Actualizar Campos
# ==========================================
def get_nested_field(data, target):
    """Recupera el valor actual de un campo anidado."""
    keys = target.split('.')
    current = data
    try:
        for key in keys:
            actual_key = int(key) if key.isdigit() else key
            current = current[actual_key]
        return current
    except (KeyError, IndexError, TypeError):
        return None

def update_nested_field(data, target, new_value):
    if '.' in target:
        keys = target.split('.')
        current = data
        try:
            for i, key in enumerate(keys[:-1]):
                next_key = keys[i + 1]
                
                # 1. SI LA LLAVE NO EXISTE O ES NULL, LA INICIALIZAMOS
                if isinstance(current, dict):
                    if key not in current or current[key] is None:
                        current[key] = [] if next_key.isdigit() else {}
                    
                    actual_key = int(key) if key.isdigit() else key
                    current = current[actual_key]
                
                elif isinstance(current, list):
                    idx = int(key)
                    while len(current) <= idx:
                        current.append({} if not next_key.isdigit() else [])
                    current = current[idx]
            
            # 2. INYECCIÓN DEL VALOR FINAL
            final_key = int(keys[-1]) if keys[-1].isdigit() else keys[-1]
            
            if isinstance(current, dict):
                current[final_key] = new_value
            elif isinstance(current, list):
                idx = int(final_key)
                while len(current) <= idx:
                    current.append(None)
                current[idx] = new_value
                
            return True
        except (KeyError, IndexError, TypeError) as e:
            return False
    else:
        if target in data:
            if isinstance(data[target], list):
                if isinstance(new_value, list):
                    data[target].extend(new_value)
                else:
                    data[target].append(new_value)
            else:
                data[target] = new_value
            return True
        
        for key, value in data.items():
            if isinstance(value, dict):
                if update_nested_field(value, target, new_value):
                    return True
        return False

def process_answer_node(state: AgentState) -> dict:
    updates = {"messages": []}
    answer_data = getattr(state, "new_answer", {})
    answer_text = answer_data.get("answer", "").strip().upper()
    question_text = answer_data.get("question_text", "").strip()
    current_gaps = getattr(state, "gaps", []) or []
    dismissed = getattr(state, "dismissed_gaps", []) or []
    current_history = getattr(state, "history", []) or []
    metadata_obj = getattr(state, "metadata", None) or {}
    print(f"metadata recieved in Answer Evaluator: {metadata_obj}")

    # =========================================================
    # 0. GUARDAR LA MEMORIA
    # =========================================================
    if answer_data.get("answer"):
        current_history.append(f"AI: {question_text}")
        current_history.append(f"Partner: {answer_data.get('answer')}")
        updates["history"] = current_history

    # =========================================================
    # 1. COMANDOS TÁCTICOS DE UX
    # =========================================================
    if answer_text == "SKIP_PUBLISHABLE_MATTERS":
        updates["messages"].append("⚙️ [COMMAND] 'SKIP_PUBLISHABLE_MATTERS' detected.")
        campos_casos = [gap.get("field") for gap in current_gaps if "publishable_matters" in gap.get("field", "")]
        updates["dismissed_gaps"] = dismissed + campos_casos
        updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
        return updates

    elif answer_text == "SKIP_CONFIDENTIAL_MATTERS":
        updates["messages"].append("⚙️ [COMMAND] 'SKIP_CONFIDENTIAL_MATTERS' detected.")
        campos_confidenciales = [gap.get("field") for gap in current_gaps if "confidential_matters" in gap.get("field", "")]
        updates["dismissed_gaps"] = dismissed + campos_confidenciales
        updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
        return updates

    elif answer_text == "SKIP_INTERVIEW":
        updates["messages"].append("⚙️ [COMMAND OVERRIDE] 'SKIP_INTERVIEW' detected. Shutting down interrogator permanently.")
        todos_los_campos = [gap.get("field") for gap in current_gaps]
        updates["dismissed_gaps"] = dismissed + todos_los_campos
        updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
        
        # 🧠 THE CLEAN FIX: Store the flag in the existing dictionary
        ctx = getattr(state, "strategic_context", {})
        ctx["force_skip_interview"] = True
        updates["strategic_context"] = ctx
        
        return updates
    
    elif answer_text in ["ANALYZE_MATTERS", "MATTER_ANALYSIS"]:
        updates["messages"].append("⚙️ [COMMAND STRATEGY] 'ANALYZE_MATTERS' detected. Breaking ingestion loop.")
        
        # 🧠 THE SAFE FIX: Save to dictionary
        ctx = getattr(state, "strategic_context", {})
        ctx["trigger_analysis"] = True 
        updates["strategic_context"] = ctx
        
        updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
        return updates
    
    if not answer_data or not answer_data.get("answer"):
        return updates

    target_field = answer_data.get("target_field")
    user_text = answer_data.get("answer")
    submission = getattr(state, "submission", None)

    updates["messages"].append(f"DEBUG: evaluating field '{target_field}' with answer: '{user_text[:30]}...'")

    schema_context = json.dumps(submission.model_json_schema()) if submission else "Unknown Schema"

    try:
        llm = get_llm(temperature=0)
        structured_llm = llm.with_structured_output(AnswerIntent)
        
        system_prompt = (
            "You are an expert data extraction AI evaluating a user's answer for a legal directory submission.\n"
            "Your goal is to extract the user's answer to populate the target field: '{field}'.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. DECIDING THE ACTION:\n"
            "   - 'fill': The user provided valid, relevant information.\n"
            "   - 'dismiss': The user explicitly says 'skip', 'ignore', 'I don't have this', or provides absolute gibberish.\n"
            "   - 'clarify': The user asks a question, requests clarification (e.g., 'What do you mean?'), or expresses confusion. DO NOT dismiss in this case.\n"
            "2. EXTRACTED VALUE: Output the extracted value based on the user's text. If the target is an object or list, format it strictly as a JSON string. If it's a text field, just output the clean text.\n\n"
            "Here is the strict JSON schema for context: \n{schema}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "User's answer: {answer}")
        ])
        
        chain = prompt | structured_llm
        result = chain.invoke({"field": target_field, "answer": user_text, "schema": schema_context})
        
        safe_action = result.action
        
        if "?" in user_text and safe_action == "dismiss":
            safe_action = "clarify"
        elif safe_action == "dismiss" and result.extracted_value and len(str(result.extracted_value)) > 15:
            safe_action = "fill"
        elif safe_action not in ["fill", "dismiss", "clarify"] and result.extracted_value:
            safe_action = "fill"

        updates["messages"].append(f"DEBUG: LLM decided action='{result.action}' -> safe_action='{safe_action}'")

        if safe_action == "clarify":
            updates["messages"].append(f"Answer Evaluator: User requested clarification for '{target_field}'. Leaving gap open.")
            return updates
        
        elif safe_action == "dismiss":
            current_dismissed = getattr(state, "dismissed_gaps", [])
            if target_field not in current_dismissed:
                current_dismissed.append(target_field)
            updates["dismissed_gaps"] = current_dismissed
            updates["messages"].append(f"Answer Evaluator: User dismissed the '{target_field}' field.")
            
        elif safe_action == "fill":
            updates["messages"].append(f"DEBUG: Valor extraído por LLM: {str(result.extracted_value)[:100]}...")
            
            print(f"Answer Evaluator: Attempting to fill '{target_field}' with extracted value.")
            print(f"extracted_value (first 100 chars): {str(result.extracted_value)[:100]}...")

            if target_field.startswith("metadata."):
                meta_key = target_field.split(".")[1]
                
                # 1. 🛡️ SAFE STATE EXTRACTION
                if isinstance(state, dict):
                    metadata_obj = state.get("metadata", {}) or {}
                else:
                    metadata_obj = getattr(state, "metadata", None) or {}
                
                # 2. 🛡️ FORCE RE-VALIDATION (Bypasses the Mutation Trap)
                if hasattr(metadata_obj, "model_dump"):
                    meta_dict = metadata_obj.model_dump()
                elif isinstance(metadata_obj, dict):
                    meta_dict = metadata_obj.copy()
                else:
                    meta_dict = dict(metadata_obj)
                    
                meta_dict[meta_key] = result.extracted_value
                
                updates["metadata"] = meta_dict
                print(f"Answer Evaluator: Metadata '{meta_key}' updated to '{result.extracted_value}'.")
                updates["messages"].append(f"SUCCESS: Metadata '{meta_key}' updated to '{result.extracted_value}'.")
                
                updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
                return updates
            
            print(f"submission before update: {str(submission)[:500]}...")

            if submission:
                sub_dict = submission.model_dump()
                val_to_inject = result.extracted_value
                print(f"sub_dict before injection: {str(sub_dict)[:500]}...")
                try:
                    val_to_inject = json.loads(val_to_inject)
                except (json.JSONDecodeError, TypeError):
                    pass

                # =======================================================
                # 🧠 STRATEGIC BUFFER INTERCEPTION (The New Logic)
                # =======================================================
                if target_field.endswith("editorial_feedback"):
                    updates["messages"].append("DEBUG: Strategic gap detected. Rerouting to 'partner_additional_notes' buffer.")
                    
                    # 1. Reroute the target path
                    new_target = target_field.replace("editorial_feedback", "partner_additional_notes")
                    
                    # 2. Fetch any existing notes to append to them
                    existing_notes = get_nested_field(sub_dict, new_target)
                    
                    if existing_notes:
                        val_to_inject = f"{existing_notes}\n\n[Additional Note]: {val_to_inject}"
                    else:
                        val_to_inject = f"[Strategic Note]: {val_to_inject}"
                        
                    # 3. Overwrite the target field for the injection function
                    target_field = new_target
                    
                    # 4. Auto-dismiss the original 'editorial_feedback' gap so the loop advances
                    current_dismissed = getattr(state, "dismissed_gaps", [])
                    original_gap_field = answer_data.get("target_field")
                    if original_gap_field not in current_dismissed:
                        current_dismissed.append(original_gap_field)
                    updates["dismissed_gaps"] = current_dismissed
                # =======================================================

                try:
                    success = update_nested_field(sub_dict, target_field, val_to_inject)
                    
                    if success:
                        try:
                            updates["submission"] = type(submission)(**sub_dict)
                            updates["messages"].append(f"SUCCESS: Field '{target_field}' updated.")
                            
                            # =======================================================
                            # 🛡️ THE INFINITE LOOP FIX: Universal Auto-Dismiss
                            # =======================================================
                            current_dismissed = getattr(state, "dismissed_gaps", [])
                            original_gap_field = answer_data.get("target_field")
                            
                            if original_gap_field not in current_dismissed:
                                current_dismissed.append(original_gap_field)
                                updates["dismissed_gaps"] = current_dismissed
                                updates["messages"].append(f"✅ Gap successfully dismissed: {original_gap_field}")
                            # =======================================================

                        except ValidationError as e:
                            updates["submission"] = sub_dict 
                            updates["messages"].append(f"WARNING: Type mismatch in '{target_field}', stored as raw data.")
                    else:
                        updates["messages"].append(f"ERROR: Path '{target_field}' not found.")

                except Exception as e:
                    updates["messages"].append(f"CRITICAL ERROR: {str(e)}")
                    updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
                
            else:
                 updates["messages"].append("Answer Evaluator Error: No submission object exists.")

    except Exception as e:
        import traceback
        updates["messages"].append(f"FATAL ERROR: {str(e)} | Traceback: {traceback.format_exc()[:500]}")

    updates["new_answer"] = {"target_field": "", "question_text": "", "answer": ""}
    return updates