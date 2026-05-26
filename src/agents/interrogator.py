from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.core.state import AgentState
from src.core.llm import get_llm
from src.logic.ranking_history_context import get_unified_ranking_strategy
class StrategicQuestion(BaseModel):
    question: str = Field(
        description="The complete verbal response to the Partner. It MUST include your conversational clarification or validation FIRST, followed immediately by the targeted question."
    )

def interrogator_node(state: AgentState) -> dict:
    """
    Interrogator Node:
    Generates dynamic, strategic questions for the fields marked as null or missing (gaps)
    using an LLM.
    """
    updates = {"current_step": "interrogator", "messages": []}

    gaps = getattr(state, "gaps", []) or []
    question = ""
    field = ""

    if gaps:
        try:
            # 1. 🛠️ PRIMERO EXTRAEMOS LOS DATOS (¡La línea que faltaba arriba!)
            submission_data = getattr(state, "submission", None)
            input_type = getattr(state, "input_document_type", "unknown")
            
            first_gap = gaps[0]
            field = first_gap.get('field', 'unknown')
            reason = first_gap.get('reason', 'Missing information.')

            # =========================================================
            # 🧠 NEW: THE CONTEXT INJECTOR & EDITORIAL EXTRACTOR
            # Extracts the specific client name and current summary.
            # =========================================================
            matter_context = ""
            client_name = "Unknown Client"
            matter_summary = ""
            
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
                                matter_summary = getattr(matters[matter_idx], summary_field, "No summary provided.")
                                
                                if client_name and client_name != "Unknown Client":
                                    matter_context = f"\n[CRITICAL CONTEXT: You are asking about the specific matter for the client: '{client_name}'. YOU MUST MENTION THIS CLIENT NAME IN YOUR QUESTION.]\n"
            except Exception as e:
                print(f"⚠️ Context Injector skipped: {e}")

            # =======================================================
            # 🧠 EXTRACCIÓN E INYECCIÓN DEL CONTEXTO ESTRATÉGICO
            # =======================================================
            if submission_data:
                dump = submission_data.model_dump(exclude_none=True)
                dump_clean = {k: v for k, v in dump.items() if v and str(v) != "{}" and str(v) != "[]"}
                current_submission_context = str(dump_clean).replace("{", "{{").replace("}", "}}")
                submission_dict = dump
            else:
                current_submission_context = "No information extracted yet."
                submission_dict = {}

            # =======================================================
            # 🧠 EXTRACCIÓN GLOBAL (Firm & Practice)
            # =======================================================
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

            # 1. 🎯 CHECK IF STRATEGY GAPS EXIST
            # We look inside the gaps array to see if the priority fields are still missing.
            strategy_gaps_exist = any(
                "current_band_status" in g.get('field', '') or 
                "ranking_history_trajectory" in g.get('field', '') 
                for g in gaps
            )

            # 2. 🚦 CONDITIONAL INJECTION
            if not strategy_gaps_exist:
                print("\n--- 🛠️ [DEBUG] STRATEGY EXTRACTION PIPELINE ---")
                
                # We HAVE the data. Extract it safely.
                target_dir = getattr(state, "target_submission_type", "Chambers")
                
                # 🛑 SCRUBBER: Aggressively destroy default/placeholder strings
                def scrub_val(val):
                    v = str(val).strip()
                    return "" if v.upper() in ["", "N/A", "UNKNOWN", "NONE", "NULL"] else v

                # Extract the raw data based on the directory template
                if "A_preliminary_information" in submission_dict and submission_dict["A_preliminary_information"]:
                    raw_band = submission_dict["A_preliminary_information"].get("current_band_status", "")
                    raw_hist = submission_dict["A_preliminary_information"].get("ranking_history_trajectory", "")
                    print("📂 Source: A_preliminary_information (Chambers)")
                elif "identity" in submission_dict and submission_dict["identity"]:
                    raw_band = submission_dict["identity"].get("current_band_status", "")
                    raw_hist = submission_dict["identity"].get("ranking_history_trajectory", "")
                    print("📂 Source: identity (Legal 500)")
                else:
                    raw_band = ""
                    raw_hist = ""
                    print("📂 Source: NONE (Data missing from dictionary)")

                print(f"🔍 Raw Extraction -> Band: '{raw_band}' | History: '{raw_hist}'")

                # Clean the data
                current_band = scrub_val(raw_band)
                ranking_history = scrub_val(raw_hist)
                
                print(f"🧼 Scrubbed Data  -> Band: '{current_band}' | History: '{ranking_history}'")

                # 🛑 DOUBLE SAFETY CHECK:
                if current_band and ranking_history:
                    print("✅ Safety Check Passed: Valid data found. Injecting Strategic Directives.")
                    dynamics = get_unified_ranking_strategy(current_band, ranking_history, target_dir)
                    realistic_target = dynamics.get("strategic_objective", "")
                    evaluation_tone = dynamics.get("editorial_rules", "")

                    # Build the complete text block to pass to the LLM
                    strategic_directive = (
                        "[STRATEGIC ALIGNMENT - CRITICAL DIRECTIVE]\n"
                        f"- Firm's Current Status: {current_band}\n"
                        f"- Realistic Target for this submission: {realistic_target}\n"
                        f"- Evaluator Persona & Focus: {evaluation_tone}\n"
                        "CRITICAL RULE: DO NOT flatter the firm by suggesting they are a 'Band 1' candidate unless 'Band 1' is explicitly their Target.\n\n"
                    )
                else:
                    print("❌ Safety Check Failed: Junk data detected. Hiding strategy from LLM.")
                    # The data existed in the dict but was useless (e.g. "N/A"). Hide the strategy.
                    realistic_target = ""
                    evaluation_tone = ""
                    strategic_directive = ""  # The prompt sees absolutely nothing.
                
                print("---------------------------------------------------\n")
                
            else:
                # We DO NOT have the data yet. Send an empty "" string.
                current_band = ""
                ranking_history = ""
                realistic_target = ""
                evaluation_tone = ""
                strategic_directive = ""  # The prompt sees absolutely nothing.

            # --- DEBUG DEL INTERROGADOR (CEREBRO ESTRATÉGICO) ---
            print("\n" + "🧠" * 25)
            print("🕵️‍♂️ [DEBUG INTERROGATOR] INYECCIÓN ESTRATÉGICA AL PROMPT")
            print("-" * 50)
            print(f" TARGET FIELD   : {field}")
            print(f" BANDA DETECTADA: {current_band if current_band else 'MISSING - SENDING EMPTY STRING'}")
            print(f" HISTORIAL      : {ranking_history if ranking_history else 'MISSING - SENDING EMPTY STRING'}")
            print(f" TARGET REALISTA: {realistic_target if realistic_target else 'MISSING - SENDING EMPTY STRING'}")
            print("🧠" * 25 + "\n")
            # =======================================================

            llm = get_llm(temperature=0.2)
            structured_llm = llm.with_structured_output(StrategicQuestion)

            # =======================================================
            # THE MASTER SYSTEM PROMPT (La Biblia del Consultor)
            # =======================================================
           # =======================================================
            # THE MASTER SYSTEM PROMPT (La Biblia del Consultor)
            # =======================================================
            system_prompt = (
                "[ROLE & CONTEXT]\n"
                "You are an elite Legal Ranking Strategist (former Chambers & Partners/Legal 500 senior editor) consulting for a top-tier transnational law firm. "
                "You are in a live, high-stakes strategy room with the Managing Partner.\n\n"
                "[OBJECTIVE]\n"
                "Conduct a highly efficient, strategic interview to extract necessary information for their directory submission. "
                "ALWAYS generate exactly ONE clear, targeted question. Do not overwhelm the user with multiple questions at once. "
                "Frame the request not as filling out a form, but as capturing critical evidence needed to secure the optimal ranking.\n\n"
                f"{strategic_directive}"
                f"{matter_context}"
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

            input_type = getattr(state, "input_document_type", "unknown")
            first_gap = gaps[0]
            field = first_gap.get('field', 'unknown')
            reason = first_gap.get('reason', 'Missing information.')
            
            # 2. Rescatar la respuesta anterior (Si la borró el nodo anterior, miraremos el contexto global)
            previous_answer_obj = getattr(state, "new_answer", {})
            previous_answer_text = previous_answer_obj.get("answer", "") if previous_answer_obj else ""

            history_data = getattr(state, "history", [])
            if history_data and isinstance(history_data, list):
                # Unimos los últimos 6 intercambios (para no desbordar tokens)
                conversation_history = "\n".join(history_data[-6:])
            else:
                conversation_history = "No previous conversation. This is the beginning."

            # 3. CONCIENCIA DE ESTADO: ¿Es la primera vez que le hablamos al usuario?
            history_data = getattr(state, "history", [])
            previous_answer_text = getattr(state, "new_answer", {}).get("answer", "").strip()
            
            # 🚨 LA CLAVE: Si el usuario mandó un texto, YA NO es la primera interacción.
            is_first_interaction = (len(history_data) == 0) and (not previous_answer_text)

            submission_data = getattr(state, "submission", None)
            if submission_data:
                # Limpiamos los campos vacíos para ver la "carne" de lo que se extrajo
                dump = submission_data.model_dump(exclude_none=True)
                dump = {k: v for k, v in dump.items() if v and str(v) != "{}" and str(v) != "[]"}
                current_submission_context = str(dump).replace("{", "{{").replace("}", "}}")
            else:
                current_submission_context = "No information extracted yet."

            input_type = getattr(state, "input_document_type", "unknown")

            # =======================================================
            # 4. EL CEREBRO DEL ESTRATEGA (Prompts Dinámicos)
            # =======================================================

            is_matter_request = "matters" in field.lower()
            is_new_matter_request = is_matter_request and "name_of_client" in field.lower()
            
            # 🧠 NUEVO: Detectamos si es una orden de mejora del Rubric Evaluator
            is_strategic_enhancement = "partner_additional_notes" in field.lower() or "editorial_feedback" in field.lower()
            matter_instruction = ""

            # --- NUEVO: DETECCIÓN DE CONFIDENCIALIDAD ---
            confidentiality_instruction = ""
            if "confidential" in field.lower():
                confidentiality_instruction = (
                    "\n\n[CRITICAL CONFIDENTIALITY MANDATE]\n"
                    "Since the target field is for a CONFIDENTIAL matter, you MUST explicitly assure the Partner "
                    "that the information they provide will be kept strictly confidential, used ONLY for the directory's "
                    "internal panel evaluation, and will NEVER be published."
                    "At the very end of your response, you MUST add exactly this phrase in italics to guide the user: "
                    "*(If you do not have another confidential matter to add, please click the 'Skip Confidential' button below).* "
                    "Keep it elegant and unobtrusive."
                )
            elif "publishable" in field.lower():
                confidentiality_instruction = (
                    "\n\n[PUBLISHABLE MANDATE]\n"
                    "Since the target field is for a PUBLISHABLE matter, gently remind the Partner that this "
                    "information will be part of the public record."
                    "At the very end of your response, you MUST add exactly this phrase in italics to guide the user: "
                    "*(If you do not have another publishable information about matters to add, please click the 'Skip Publishable' button below).* "
                    "Keep it elegant and unobtrusive."
                )

            if is_matter_request:
                try:
                    # field = D_publishable_information.publishable_matters.3.D2_summary...
                    # El índice numérico está en la posición [2]
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
                        "You must ask the Partner to introduce a COMPLETELY NEW, unmentioned case/transaction. "
                        "DO NOT ask for more details about the clients already listed in the 'Extracted Firm Data'."
                    )

            # --- RAMIFICACIÓN DE PROMPTS SEGÚN EL ESCENARIO ---
            
            if is_first_interaction and input_type in ["chambers_submission", "legal500_submission", "leadersleague_submission"] and len(current_submission_context) > 20:
                # RAMA 1: EL "FAN SERVICE"
                print("\n--- 🚀 RAMA 1: EL FAN SERVICE (CON PRIMERA INTERACCIÓN Y CONTEXTO RICO) ---")
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
                    "2. THE NARRATIVE AUDIT: Provide a brief, high-level assessment of their practice's footprint based on the extracted data. DO NOT use tables, bullet points, or numbers to count matters. Read the data like a senior editor and summarize the 'vibe' or focus of their work.\n"
                    "3. THE SPOTLIGHT: Identify EXACTLY ONE (1) highly impressive client, transaction, or matter from the data. Explicitly name it and state briefly why it strengthens their submission (e.g., market impact, cross-border elements, complexity, or prestige).\n"
                    "4. THE PIVOT: Seamlessly transition from this praise into a collaborative request for the missing information. Make it feel like the natural next step to secure their ranking.\n"
                    "5. THE TRANSLATION: Remember the FORBIDDEN LEXICON. Translate '{field}' into a clear, natural question in accessible global English. Ask exactly ONE question."
                )
                prompt_vars = {
                    "field": field,
                    "reason": reason,
                    "current_submission_context": current_submission_context,
                    "matter_instruction": matter_instruction,
                    "confidentiality_instruction": confidentiality_instruction,
                    "firm_name": firm_name,         # 👈 PASSED HERE
                    "practice_area": practice_area,  # 👈 PASSED HERE
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
                    "1. Give a brief, highly professional welcome to the strategy session specifically for **{firm_name}** regarding their **{practice_area}** submission.\n" # 👈 UPDATED
                    "2. Adapt your welcome to the following persona: {evaluation_tone}\n"
                    "3. Smoothly ask the Partner to provide the information needed to lay the foundation of our submission.\n"
                    "4. Remember the FORBIDDEN LEXICON: translate '{field}' into a natural human question."
                )
                prompt_vars = {
                    "field": field, 
                    "reason": reason,
                    "evaluation_tone": evaluation_tone,
                    "matter_instruction": matter_instruction,
                    "confidentiality_instruction": confidentiality_instruction,
                    "firm_name": firm_name,         # 👈 PASSED HERE
                    "practice_area": practice_area  # 👈 PASSED HERE
                }

            elif is_strategic_enhancement:
                # RAMA 4: EL "EDITORIAL PUSH" (Mejora de narrativa existente)

                confidentiality_instruction = ""
                if "confidential" in field.lower():
                    confidentiality_instruction = (
                        "\n\n[CRITICAL CONFIDENTIALITY MANDATE]\n"
                        "Since the target field is for a CONFIDENTIAL matter, you MUST explicitly assure the Partner "
                        "that the information they provide will be kept strictly confidential, used ONLY for the directory's "
                        "internal panel evaluation, and will NEVER be published."
                    )
                elif "publishable" in field.lower():
                    confidentiality_instruction = (
                        "\n\n[PUBLISHABLE MANDATE]\n"
                        "Since the target field is for a PUBLISHABLE matter, gently remind the Partner that this "
                        "information will be part of the public record."
                    )

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

            else:
                # RAMA 3: EN MEDIO DE LA REUNIÓN (CONVERSACIÓN ACTIVA)
                conversation_history = "\n".join(history_data[-6:]) if history_data else "No previous conversation."
                
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
                    "2. CLARIFICATION & ACTIVE LISTENING: If the Partner's Input is a question or shows confusion (e.g. asking 'What do you mean?'), YOU MUST ANSWER THEIR QUESTION directly and briefly based on directory standards. Do this FIRST.\n"
                    "3. Smoothly pivot and ask exactly ONE targeted question to obtain the missing information.\n"
                    "4. Remember the FORBIDDEN LEXICON: Translate '{field}' into a conversational request. Do not use array numbers or section codes.\n"
                    "5. Your final output MUST combine BOTH the answer to their doubt AND your new question into a single, natural paragraph."
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
            
            # Pasamos las variables dinámicas
            result = chain.invoke(prompt_vars)

            question = result.question

        except Exception as e:
            # Fallback to simple logic if LLM fails (e.g., no API key in tests)
            updates["messages"].append(f"LLM generation failed: {e}. Falling back to simple questions.")
            first_gap = gaps[0]
            field = first_gap.get("field", "unknown")
            question = f"We are missing information for '{field}'. Could you provide details?"

    updates["new_answer"] = {
        "question_text": question,
        "answer": "",
        "target_field": field  # NEW: Pass the field forward
    }
    updates["questions"] = [question]
    # Better logging to see exactly what gap we are targeting
    updates["messages"].append(f"Interrogator node: Generated question for gap in field '{field}' and paused for Laravel.")

    # =========================================================
    # 🛡️ THE FRONTEND AMNESIA FIX (Safe Dictionary Extraction)
    # =========================================================
    if isinstance(state, dict):
        updates["metadata"] = state.get("metadata", {})
        updates["submission"] = state.get("submission", None)
    else:
        updates["metadata"] = getattr(state, "metadata", None)
        updates["submission"] = getattr(state, "submission", None)

    return updates

