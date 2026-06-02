from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.core.state import AgentState
from src.core.llm import get_llm
from src.logic.ranking_history_context import get_unified_ranking_strategy

class StrategicQuestion(BaseModel):
    question: str = Field(
        description="The complete verbal response to the Partner. This is usually a question, but can also be a final closure statement if instructed to end the conversation."
    )

def interrogator_node(state: AgentState) -> dict:
    updates = {"current_step": "interrogator", "messages": []}

    gaps = getattr(state, "gaps", []) or []
    question = ""
    field = ""

    if gaps:
        try:
            submission_data = getattr(state, "submission", None)
            input_type = getattr(state, "input_document_type", "unknown")
            
            previous_answer_obj = getattr(state, "new_answer", {})
            ctx = getattr(state, "strategic_context", {})
            active_cat = ctx.get("active_category")
            
            category_is_depleted = False
            first_gap = gaps[0] if gaps else {}
            
            # If the frontend is locked onto a category, FILTER the gaps!
            if active_cat:
                cat_name = active_cat.replace("category:", "")
                cat_gaps = [g for g in gaps if g.get("ui_category") == cat_name]
                
                # 🛑 THE COMPLETION TRIGGER: No gaps match the locked category!
                if not cat_gaps:
                    category_is_depleted = True
                    target_field_from_frontend = active_cat # Pass for the prompt
                    print(f"🎉 [CATEGORY COMPLETED] No gaps remain for '{cat_name}'. Generating closure.")
                else:
                    first_gap = cat_gaps[0]
                    print(f"🎯 [TRACK LOCKED] Focused on category '{cat_name}'. Targeting gap: {first_gap.get('field')}")

            field = first_gap.get('field', 'unknown')
            reason = first_gap.get('reason', 'Missing information.')

            target_context = ""
            matter_summary = ""
            client_name = "Unknown Client"
            
            try:
                if "publishable_matters" in field or "confidential_matters" in field:
                    parts = field.split(".")
                    if len(parts) >= 3 and parts[2].isdigit():
                        matter_idx = int(parts[2])
                        sub = getattr(state, "submission", None)
                        
                        if sub:
                            if "publishable" in parts[1]:
                                section = getattr(sub, "D_publishable_information", None)
                                matters = getattr(section, "publishable_matters", []) if section else []
                                client_field = "D1_name_of_client"
                                summary_field = "D2_summary_of_matter_and_role"
                            else:
                                section = getattr(sub, "E_confidential_information", None)
                                matters = getattr(section, "confidential_matters", []) if section else []
                                client_field = "E1_name_of_client"
                                summary_field = "E2_summary_of_matter_and_role"

                            if matter_idx < len(matters):
                                client_name = getattr(matters[matter_idx], client_field, "Unknown Client")
                                matter_summary = getattr(matters[matter_idx], summary_field, "")
                                if client_name and client_name != "Unknown Client":
                                    target_context = f"\n[CRITICAL CONTEXT: You are asking about the specific matter for the client: '{client_name}'. YOU MUST MENTION THIS CLIENT NAME IN YOUR QUESTION.]\n"
                
                elif "lawyer_profiles" in field:
                    parts = field.split(".")
                    if len(parts) >= 2 and parts[1].isdigit():
                        lawyer_idx = int(parts[1])
                        profiles = getattr(state, "lawyer_profiles", [])
                        
                        if lawyer_idx < len(profiles):
                            p_dict = profiles[lawyer_idx] if isinstance(profiles[lawyer_idx], dict) else (profiles[lawyer_idx].model_dump() if hasattr(profiles[lawyer_idx], "model_dump") else {})
                            lawyer_name = p_dict.get("name", "the lawyer")
                            target_context = f"\n[CRITICAL CONTEXT: You are asking about the B9 profile for the lawyer: '{lawyer_name}'. YOU MUST MENTION THIS LAWYER BY NAME to gather better evidence for their ranking.]\n"

            except Exception as e:
                print(f"⚠️ Context Injector skipped: {e}")

            if submission_data:
                dump = submission_data.model_dump(exclude_none=True)
                dump_clean = {k: v for k, v in dump.items() if v and str(v) != "{}" and str(v) != "[]"}
                current_submission_context = str(dump_clean).replace("{", "{{").replace("}", "}}")
                submission_dict = dump
            else:
                current_submission_context = "No information extracted yet."
                submission_dict = {}

            def scrub_val(val):
                v = str(val).strip()
                return "" if v.upper() in ["", "N/A", "UNKNOWN", "NONE", "NULL"] else v

            raw_firm_name = ""
            raw_practice_area = ""

            if "A_preliminary_information" in submission_dict and submission_dict["A_preliminary_information"]:
                raw_firm_name = submission_dict["A_preliminary_information"].get("A1_firm_name", "")
                raw_practice_area = submission_dict["A_preliminary_information"].get("A2_practice_area", "")
            elif "identity" in submission_dict and submission_dict["identity"]:
                raw_firm_name = submission_dict["identity"].get("firm_name", "")
                raw_practice_area = submission_dict["identity"].get("practice_area", "")

            firm_name = scrub_val(raw_firm_name) if scrub_val(raw_firm_name) else "your firm"
            practice_area = scrub_val(raw_practice_area) if scrub_val(raw_practice_area) else "this practice area"

            strategy_gaps_exist = any(
                "current_band_status" in g.get('field', '') or 
                "ranking_history_trajectory" in g.get('field', '') 
                for g in gaps
            )

            if not strategy_gaps_exist:
                target_dir = getattr(state, "target_submission_type", "Chambers")
                
                if "A_preliminary_information" in submission_dict and submission_dict["A_preliminary_information"]:
                    raw_band = submission_dict["A_preliminary_information"].get("current_band_status", "")
                    raw_hist = submission_dict["A_preliminary_information"].get("ranking_history_trajectory", "")
                elif "identity" in submission_dict and submission_dict["identity"]:
                    raw_band = submission_dict["identity"].get("current_band_status", "")
                    raw_hist = submission_dict["identity"].get("ranking_history_trajectory", "")
                else:
                    raw_band = ""
                    raw_hist = ""

                current_band = scrub_val(raw_band)
                ranking_history = scrub_val(raw_hist)
                
                if current_band and ranking_history:
                    dynamics = get_unified_ranking_strategy(current_band, ranking_history, target_dir)
                    realistic_target = dynamics.get("strategic_objective", "")
                    evaluation_tone = dynamics.get("editorial_rules", "")

                    strategic_directive = (
                        "[STRATEGIC ALIGNMENT - CRITICAL DIRECTIVE]\n"
                        f"- Firm's Current Status: {current_band}\n"
                        f"- Realistic Target for this submission: {realistic_target}\n"
                        f"- Evaluator Persona & Focus: {evaluation_tone}\n"
                        "CRITICAL RULE: DO NOT flatter the firm by suggesting they are a 'Band 1' candidate unless 'Band 1' is explicitly their Target.\n\n"
                    )
                else:
                    realistic_target = ""
                    evaluation_tone = ""
                    strategic_directive = ""  
            else:
                current_band = ""
                ranking_history = ""
                realistic_target = ""
                evaluation_tone = ""
                strategic_directive = "" 

            print("\n" + "🧠" * 25)
            print("🕵️‍♂️ [DEBUG INTERROGATOR] INYECCIÓN ESTRATÉGICA AL PROMPT")
            print("-" * 50)
            print(f" TARGET FIELD   : {field}")
            print(f" BANDA DETECTADA: {current_band if current_band else 'MISSING - SENDING EMPTY STRING'}")
            print(f" TARGET REALISTA: {realistic_target if realistic_target else 'MISSING - SENDING EMPTY STRING'}")
            print("🧠" * 25 + "\n")

            llm = get_llm(temperature=0.2)
            structured_llm = llm.with_structured_output(StrategicQuestion)

            if category_is_depleted:
                try:
                    # 1. Clean the category name for the prompt
                    selected_cat_clean = active_cat.replace("category:", "").replace("_", " ").title()
                
                    # 👇 THE FIX: Extract the text BEFORE using it in the prompt 👇
                    prev_answer_obj = getattr(state, "new_answer", {})
                    previous_answer_text = prev_answer_obj.get("answer", "") if prev_answer_obj else ""
                    
                    # 2. Force the LLM to ONLY write a 1-sentence validation of the user's last input
                    system_prompt = (
                        "[ROLE & CONTEXT]\n"
                        "You are an elite Legal Ranking Strategist. The Partner just provided their final input. "
                        "Acknowledge their input with a SINGLE, brief sentence of professional validation (e.g., 'Understood, we will omit this detail.' or 'Excellent, that perfectly clarifies the transaction.').\n\n"
                        "[CRITICAL RULE]\n"
                        "DO NOT ASK A QUESTION. DO NOT add any other commentary. ONLY provide the 1-sentence validation."
                    )
                    user_prompt = f"Partner's Input: '{previous_answer_text}'"
                    
                    # 3. Compile and invoke the LLM immediately
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", user_prompt),
                    ])
                    chain = prompt | structured_llm
                    result = chain.invoke({})
                    llm_validation = result.question
                    
                    # 4. Hardcode the deterministic closure notice
                    closure_notice = (
                        f"✅ **Section Complete:** We have successfully captured all required evidence for the **{selected_cat_clean}** track.\n\n"
                        "Please return to the main dashboard to select your next priority."
                    )
                    
                    # 5. Combine them safely
                    final_question = f"{llm_validation}\n\n{closure_notice}"
                    
                    # 6. Pack the payload
                    updates["new_answer"] = {
                        "question_text": final_question,
                        "answer": "",
                        "target_field": active_cat # Keep the lock active to pass the UI check
                    }
                    updates["questions"] = [final_question]
                    updates["messages"].append(f"🎉 Interrogator node: Category '{selected_cat_clean}' depleted. Early return triggered.")
                    
                    if isinstance(state, dict):
                        updates["metadata"] = state.get("metadata", {})
                        updates["submission"] = state.get("submission", None)
                    else:
                        updates["metadata"] = getattr(state, "metadata", None)
                        updates["submission"] = getattr(state, "submission", None)

                    # 🚀 7. THE EARLY RETURN: Exit the function right now
                    return updates
                except Exception as e:
                    print(f"⚠️ LLM failed during category depletion closure generation: {e}. Falling back to generic closure message.")
                    question = f"🎉 Excellent! We have completed all questions for the '{selected_cat_clean}' category. Please return to the main menu to select another focus area."
            
            else:
                system_prompt = (
                    "[ROLE & CONTEXT]\n"
                    "You are an elite Legal Ranking Strategist (former Chambers & Partners/Legal 500 senior editor) consulting for a top-tier transnational law firm. "
                    "You are in a live, high-stakes strategy room with the Managing Partner.\n\n"
                    "[OBJECTIVE]\n"
                    "Conduct a highly efficient, strategic interview to extract necessary information for their directory submission. "
                    "ALWAYS generate exactly ONE clear, targeted question. Do not overwhelm the user with multiple questions at once. "
                    "Frame the request not as filling out a form, but as capturing critical evidence needed to secure the optimal ranking.\n\n"
                    f"{strategic_directive}"
                    f"{target_context}" 
                    "[FORMATTING RULES: MANDATORY MARKDOWN]\n"
                    "You MUST format your entire response in elegant Markdown to provide a superior user experience. Follow these strict typographic rules:\n"
                    "1. If giving a compliment or strategic summary, optionally use a heading like `###` for emphasis, or format it cleanly.\n"
                    "2. Use **bold** exclusively for highlighting firm names, specific client names, jurisdictions, or key legal concepts.\n"
                    "3. If providing options, criteria, or multiple points, ALWAYS use a bulleted list (`- ` or `* `).\n"
                    "4. PACING AND SPACING: Keep paragraphs extremely short (1-2 sentences max). You MUST insert a double line break (\\n\\n) after EVERY paragraph or distinct logical thought to prevent walls of text.\n"
                    "5. Never output raw JSON. Output pure Markdown text.\n\n"
                    "[THE FORBIDDEN LEXICON - STRICTLY ENFORCED]\n"
                    "You will receive system variables representing missing fields (e.g., 'publishable_matters.0.D3_matter_value' or 'identity.firm_name'). "
                    "THESE ARE INTERNAL DATABASE LABELS FOR YOUR EYES ONLY. UNDER NO CIRCUMSTANCES are you allowed to utter them to the Partner.\n"
                    "❌ YOU MUST NEVER USE:\n"
                    "- Bracketed placeholders (e.g., NEVER write '[Partner Name]' or '[Firm Name]'). If you don't know a name, do not use it.\n"
                    "- Array indices or numbers indicating list position (e.g., NEVER say 'Matter 1', 'first confidential matter', 'Client 0').\n"
                    "- Alphanumeric section codes from the form (e.g., NEVER say 'D3', 'E4', 'B2', 'A1').\n"
                    "- System field names (e.g., NEVER say 'matter_value', 'publishable_matters', 'identity.firm_name').\n"
                    "- Robotic phrasing (e.g., NEVER say 'Please provide the information for...', 'The target field needed is...').\n\n"
                    "[TRANSLATION & REFERENCING GUIDE]\n"
                    "Translate the system label into natural, executive language using context clues:\n"
                    "- BAD: 'Provide the identity.firm_name.' -> GOOD: 'To lay the right foundation, could you please confirm the official registered name of the firm?'\n"
                    "- BAD: 'Could you provide the D3 matter value for Publishable Matter 1?' -> GOOD: 'To fully capture the scale of this transaction, are we able to disclose the financial value or size of the deal?'\n\n"
                    "[CRITICAL BEHAVIORAL RULES & TONE: THE 'MAGIC CIRCLE' STANDARD]\n"
                    "1. EFFORTLESS & PREMIUM: Your tone must be strategic, confident, exact, and editorially elegant. Sound like a top-tier London or New York consultant. Make the process feel effortless for the Partner.\n"
                    "2. NO LEGALESE: Completely avoid 'contract drafting' language, academic phrasing, litigation-style memos, or overly bureaucratic terms. Keep it market-facing and crisp.\n"
                    "3. ACCESSIBLE GLOBAL ENGLISH: Your clients operate internationally and many are non-native English speakers. Use clear, direct, and simple vocabulary while maintaining high sophistication. Do NOT use overly complex words, dense phrasing, or obscure idioms.\n"
                    "4. BE ALIVE & HUMAN: Flow naturally. Make it sound like a high-level but approachable strategic discussion, not an interrogation.\n"
                    "5. CONCISE IMPACT: High-level executives value clarity. Do not overwrite. Make every word count."
                )

            previous_answer_obj = getattr(state, "new_answer", {})
            previous_answer_text = previous_answer_obj.get("answer", "") if previous_answer_obj else ""

            history_data = getattr(state, "history", [])
            if history_data and isinstance(history_data, list):
                conversation_history = "\n".join(history_data[-6:])
            else:
                conversation_history = "No previous conversation. This is the beginning."

            is_first_interaction = (len(history_data) == 0) and (not previous_answer_text)

            is_matter_request = "matters" in field.lower()
            is_new_matter_request = is_matter_request and "name_of_client" in field.lower()
            is_strategic_enhancement = "partner_additional_notes" in field.lower() or "editorial_feedback" in field.lower() or "additional_narrative" in field.lower()
            matter_instruction = ""

            confidentiality_instruction = ""
            if "confidential" in field.lower() and "summary_of_matter_and_role" in field.lower():
                confidentiality_instruction = (
                    "\n\n[CRITICAL CONFIDENTIALITY MANDATE]\n"
                    "Since the target field is for a CONFIDENTIAL matter, you MUST explicitly assure the Partner "
                    "that the information they provide will be kept strictly confidential, used ONLY for the directory's "
                    "internal panel evaluation, and will NEVER be published."
                    "At the very end of your response, you MUST add exactly this phrase in italics to guide the user: "
                    "*(If you do not have another confidential matter to add, please click the 'Skip Confidential' button below).* "
                )
            elif "publishable" in field.lower() and "summary_of_matter_and_role" in field.lower():
                confidentiality_instruction = (
                    "\n\n[PUBLISHABLE MANDATE]\n"
                    "Since the target field is for a PUBLISHABLE matter, gently remind the Partner that this "
                    "information will be part of the public record."
                    "At the very end of your response, you MUST add exactly this phrase in italics to guide the user: "
                    "*(If you do not have another publishable information about matters to add, please click the 'Skip Publishable' button below).* "
                )

            if is_matter_request and not is_strategic_enhancement:
                try:
                    matter_index = int(field.split(".")[2]) + 1
                    matter_instruction = (
                        f"\n\n[CRITICAL OVERRIDE: WE NEED MATTER #{matter_index}]\n"
                        f"The system is trying to fill slot #{matter_index} for work highlights. "
                        f"You MUST ask the Partner to provide a COMPLETELY NEW, DIFFERENT matter. "
                        f"DO NOT mention existing clients from the 'Extracted Firm Data'. Actively ask for their next best case to build volume."
                    )
                except Exception as e:
                    matter_instruction = (
                        "\n\n[CRITICAL OVERRIDE: NEW MATTER REQUIRED]\n"
                        "You must ask the Partner to introduce a COMPLETELY NEW, unmentioned case/transaction."
                    )

            # 👇 THE PERFECTED PROMPT ROUTER 👇
            if is_strategic_enhancement:
                # RAMA 4: EL "EDITORIAL PUSH" (Has absolute priority if a specific card was clicked)
                user_prompt = (
                    "--- STRATEGIC ENHANCEMENT REQUIRED ---\n"
                    "We are reviewing a specific matter for the client: **'{client_name}'**.\n"
                    "The Partner previously provided this summary for the matter:\n"
                    "> \"{matter_summary}\"\n\n"
                    "--- RUBRIC FEEDBACK (DO NOT READ THIS OUT LOUD VERBATIM) ---\n"
                    "Our internal evaluation rubric flagged this matter for the following reason:\n"
                    "{reason}\n\n"
                    "{confidentiality_instruction}\n\n"
                    "--- YOUR TASK (THE EDITORIAL PUSH) ---\n"
                    "1. Acknowledge the matter briefly, stating that it is a strong transaction but needs more depth to stand out to the directory researchers.\n"
                    "2. Translate the 'Rubric Feedback' into a highly specific, constructive question.\n"
                    "3. Frame the question explicitly as an opportunity to 'elevate', 'strengthen', or 'flesh out' the narrative for maximum impact.\n"
                    "4. Do NOT ask for a completely new matter. Focus ONLY on asking the Partner to provide the missing details (value, complexity, cross-border elements, etc.) to improve this specific description.\n"
                )
                prompt_vars = {
                    "client_name": client_name,
                    "matter_summary": matter_summary,
                    "reason": reason,
                    "confidentiality_instruction": confidentiality_instruction
                }

            elif is_first_interaction and input_type in ["chambers_submission", "legal500_submission", "leadersleague_submission"] and len(current_submission_context) > 20:
                # RAMA 1: EL "FAN SERVICE"
                safe_target = realistic_target if realistic_target else "To be determined based on this data"
                user_prompt = (
                    "--- EXTRACTED FIRM DATA SO FAR ---\n"
                    "{current_submission_context}\n\n"
                    "--- FIRM PROFILE ---\n"
                    "Firm: {firm_name}\n"
                    "Practice Area: {practice_area}\n"
                    "Strategic Target: {safe_target}\n\n"
                    "--- INTERNAL SYSTEM TARGET (DO NOT SAY THIS OUT LOUD) ---\n"
                    "Target Field needed: {field}\n"
                    "Reason: {reason}\n\n"
                    "{matter_instruction}\n"
                    "{confidentiality_instruction}\n\n"
                    "--- YOUR TASK: THE NARRATIVE EXECUTIVE HOOK ---\n"
                    "The Partner just submitted their initial draft. You must generate a single, cohesive response following this exact flow:\n\n"
                    "1. THE WELCOME: Start with a sophisticated, 1-2 sentence strategic welcome explicitly naming **{firm_name}** and the **{practice_area}** practice.\n"
                    "2. THE NARRATIVE AUDIT: Provide a brief, high-level assessment of their practice's footprint based on the extracted data.\n"
                    "3. THE SPOTLIGHT: Identify EXACTLY ONE (1) highly impressive client, transaction, or matter from the data and state briefly why it strengthens their submission.\n"
                    "4. THE PIVOT: Seamlessly transition from this praise into a collaborative request for the missing information.\n"
                    "5. THE TRANSLATION: Translate '{field}' into a clear, natural question. Ask exactly ONE question."
                )
                prompt_vars = {
                    "field": field,
                    "reason": reason,
                    "current_submission_context": current_submission_context,
                    "matter_instruction": matter_instruction,
                    "confidentiality_instruction": confidentiality_instruction,
                    "firm_name": firm_name,
                    "practice_area": practice_area, 
                    "safe_target": safe_target
                }

            elif is_first_interaction:
                # RAMA 2: START FROM SCRATCH
                user_prompt = (
                    "--- INTERNAL SYSTEM TARGET (DO NOT SAY THIS OUT LOUD) ---\n"
                    "Target Field needed: {field}\n"
                    "Reason: {reason}\n\n"
                    "{matter_instruction}\n"
                    "{confidentiality_instruction}\n\n"
                    "--- YOUR TASK ---\n"
                    "1. Give a brief, highly professional welcome to the strategy session specifically for **{firm_name}** regarding their **{practice_area}** submission.\n"
                    "2. Adapt your welcome to the following persona: {evaluation_tone}\n"
                    "3. Smoothly ask the Partner to provide the information needed to lay the foundation of our submission.\n"
                    "4. Translate '{field}' into a natural human question."
                )
                prompt_vars = {
                    "field": field, 
                    "reason": reason,
                    "evaluation_tone": evaluation_tone,
                    "matter_instruction": matter_instruction,
                    "confidentiality_instruction": confidentiality_instruction,
                    "firm_name": firm_name,
                    "practice_area": practice_area
                }

            else:
                # RAMA 3: EN MEDIO DE LA REUNIÓN
                user_prompt = (
                    "--- FIRM LORE & EXTRACTED DATA SO FAR ---\n"
                    "{current_submission_context}\n\n"
                    "--- CONVERSATION HISTORY ---\n"
                    "{conversation_history}\n\n"
                    "--- RECENT STATEMENT FROM PARTNER ---\n"
                    "Partner's Input: '{previous_answer_text}'\n\n"
                    "--- INTERNAL SYSTEM TARGET (DO NOT SAY THIS OUT LOUD) ---\n"
                    "Target Field needed: {field}\n"
                    "Reason: {reason}\n\n"
                    "{matter_instruction}\n\n"
                    "{confidentiality_instruction}\n\n"
                    "--- YOUR TASK (STRICT RULES) ---\n"
                    "1. DO NOT GREET THE PARTNER. The meeting has been going on for a while.\n"
                    "2. CLARIFICATION & ACTIVE LISTENING: Answer any questions from the Partner's Input first.\n"
                    "3. Smoothly pivot and ask exactly ONE targeted question to obtain the missing information.\n"
                    "4. Translate '{field}' into a conversational request."
                )
                prompt_vars = {
                    "field": field,
                    "reason": reason,
                    "current_submission_context": current_submission_context,
                    "realistic_target": realistic_target,
                    "evaluation_tone": evaluation_tone,
                    "conversation_history": conversation_history,
                    "previous_answer_text": previous_answer_text,
                    "matter_instruction": matter_instruction,
                    "confidentiality_instruction": confidentiality_instruction
                }

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", user_prompt),
            ])
            
            chain = prompt | structured_llm
            result = chain.invoke(prompt_vars)
            question = result.question

        except Exception as e:
            updates["messages"].append(f"LLM generation failed: {e}. Falling back to simple questions.")
            first_gap = gaps[0]
            field = first_gap.get("field", "unknown")
            question = f"We are missing information for '{field}'. Could you provide details?"

    updates["new_answer"] = {
        "question_text": question,
        "answer": "",
        "target_field": field 
    }
    updates["questions"] = [question]
    updates["messages"].append(f"Interrogator node: Generated question for gap in field '{field}' and paused for Laravel.")

    if isinstance(state, dict):
        updates["metadata"] = state.get("metadata", {})
        updates["submission"] = state.get("submission", None)
    else:
        updates["metadata"] = getattr(state, "metadata", None)
        updates["submission"] = getattr(state, "submission", None)

    return updates
