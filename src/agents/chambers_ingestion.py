import traceback
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import (
    ChambersSubmission, 
    CoreDataChunk, 
    AllMattersChunk
)

def chambers_ingestion_node(state: AgentState) -> dict:
    """
    Ingestion Node (2-Phase Method):
    Extracts data in 2 phases to optimize latency while bypassing schema limits.
    """
    updates = {"current_step": "ingestion", "messages": []}
    updates["messages"].append("🚀 INITIATING: chambers_ingestion_node (2-Phase Extraction)")
    
    raw_text = getattr(state, "extracted_text", "") or ""
    if not raw_text.strip():
        updates["messages"].append("⚠️ Ingestion Node Aborted: No raw text found.")
        return updates

    llm = get_llm(temperature=0)
    
    try:
        # =========================================================
        # PHASE 1: Extract Core Firm Data
        # =========================================================
        print("⏳ Phase 1/2: Extracting Core Firm Data...")
        core_system_prompt = (
            "You are an elite legal data extractor for Chambers & Partners submissions. "
            "Your exclusive task is to extract high-level firm profile data, department statistics, and feedback.\n\n"
            "TARGET SECTIONS:\n"
            "- Section A (Basic Information)\n"
            "- Section B (Department Information & Metrics)\n"
            "- Section C (Feedback / Barristers & Advocates)\n\n" # <--- FIXED
            "STRICT RULES:\n"
            "1. COMPLETELY IGNORE Sections D and E (Work Highlights / Matters). Do not extract any specific cases here.\n"
            "2. NO HALLUCINATIONS. If a specific metric or detail is missing, leave the field null/empty."
        )
        core_prompt = ChatPromptTemplate.from_messages([
            ("system", core_system_prompt),
            ("human", "Extract the core data from this document:\n\n{text}")
        ])
        core_chain = core_prompt | llm.with_structured_output(CoreDataChunk)
        core_data = core_chain.invoke({"text": raw_text})
        
        # =========================================================
        # PHASE 2: Extract ALL Matters (Publishable & Confidential)
        # =========================================================
        print("⏳ Phase 2/2: Extracting and Sorting All Matters...")
        matters_system_prompt = (
            "You are an elite legal data extractor for Chambers & Partners submissions. "
            "Your exclusive task is to extract ALL Work Highlights and sort them correctly.\n\n"
            "TARGET SECTIONS:\n"
            "- Section D (Publishable Matters) -> Goes into 'publishable_matters'.\n"
            "- Section E (Confidential Matters) -> Goes into 'confidential_matters'.\n\n"
            "STRICT RULES:\n"
            "1. DO NOT mix them up. Pay strict attention to the section headers in the document.\n"
            "2. HIGH FIDELITY: Extract the exact Client Name, Matter Value, and the FULL narrative description. DO NOT summarize or truncate the description; capture the exact original text.\n"
            "3. If there are no matters in a section, return an empty array for that section."
        )
        matters_prompt = ChatPromptTemplate.from_messages([
            ("system", matters_system_prompt),
            ("human", "Extract and sort all matters from this document:\n\n{text}")
        ])
        matters_chain = matters_prompt | llm.with_structured_output(AllMattersChunk)
        matters_data = matters_chain.invoke({"text": raw_text})

        # =========================================================
        # 🕵️‍♂️ DEBUG: INGESTION FIDELITY CHECK
        # =========================================================
        print("\n" + "🔍" * 25)
        print("🕵️‍♂️ [DEBUG INGESTION] RAW EXTRACTED TEXT CHECK")
        print("-" * 50)
        
        # Check the first publishable matter, or fallback to confidential
        test_matter = None
        if getattr(matters_data, "publishable_matters", []):
            test_matter = matters_data.publishable_matters[0]
            desc_field = "D2_summary_of_matter_and_role"
        elif getattr(matters_data, "confidential_matters", []):
            test_matter = matters_data.confidential_matters[0]
            desc_field = "E2_summary_of_matter_and_role"
            
        if test_matter:
            print(f"MATTER ID   : {getattr(test_matter, 'matter_id', 'N/A')}")
            print(f"CLIENT      : {getattr(test_matter, 'D1_name_of_client', getattr(test_matter, 'E1_name_of_client', 'N/A'))}")
            print("--- EXACT EXTRACTED DESCRIPTION ---")
            print(getattr(test_matter, desc_field, "NO DESCRIPTION EXTRACTED"))
        else:
            print("NO MATTERS FOUND IN EXTRACTION.")
            
        print("🔍" * 25 + "\n")
        
        # =========================================================
        # ASSEMBLY: Build the Final ChambersSubmission Object
        # =========================================================
        print("🧩 Assembling final submission object...")
        print(f"client list D0 (Publishable): {[c.client_name for c in getattr(matters_data, 'D0_publishable_clients_list', [])]}")
        print(f"client list E0 (Confidential): {[c.client_name for c in getattr(matters_data, 'E0_confidential_clients_list', [])]}")
        
        def to_dict_safe(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump(exclude_none=True)
            return obj if obj else {}

        # 🛡️ THE NEW FIX: Directly map the D0 and E0 lists extracted by the LLM
        final_submission_dict = {
            "A_preliminary_information": to_dict_safe(getattr(core_data, "A_preliminary_information", None)),
            "B_department_information": to_dict_safe(getattr(core_data, "B_department_information", None)),
            "C_feedback": to_dict_safe(getattr(core_data, "C_feedback", None)),
            "D_publishable_information": {
                "D0_publishable_clients_list": [to_dict_safe(c) for c in getattr(matters_data, "D0_publishable_clients_list", [])],
                "publishable_matters": [to_dict_safe(m) for m in getattr(matters_data, "publishable_matters", [])]
            },
            "E_confidential_information": {
                "E0_confidential_clients_list": [to_dict_safe(c) for c in getattr(matters_data, "E0_confidential_clients_list", [])],
                "confidential_matters": [to_dict_safe(m) for m in getattr(matters_data, "confidential_matters", [])]
            }
        }
        
        final_submission = ChambersSubmission(**final_submission_dict)
        
        updates["submission"] = final_submission
        pub_count = len(final_submission.D_publishable_information.publishable_matters) if final_submission.D_publishable_information else 0
        conf_count = len(final_submission.E_confidential_information.confidential_matters) if final_submission.E_confidential_information else 0
        updates["messages"].append(f"✅ Extraction complete: {pub_count} Publishable, {conf_count} Confidential.")
        print("✅ Ingestion successfully completed.")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR IN INGESTION NODE: {e}")
        traceback.print_exc()
        updates["messages"].append(f"❌ Error during chunked extraction: {str(e)}")

    return updates