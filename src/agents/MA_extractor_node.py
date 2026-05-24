from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
# 🛡️ THE FIX: Import the schemas directly from your central core
from src.core.schemas import SingleMatterExtraction, ExtractedMatter

# =========================================================
# THE GENESIS EXTRACTION NODE
# =========================================================
def matters_assistant_extractor_node(state: AgentState) -> dict:
    """
    Act 0: The Genesis Drafter
    Reads the concatenated unstructured text and drafts a pristine Chambers matter from scratch.
    """
    updates = {"current_step": "matters_assistant_extraction", "messages": []}
    
    extracted_text = getattr(state, "extracted_text", "")
    config = getattr(state, "config", {})
    
    if not extracted_text:
        updates["messages"].append("⚠️ No raw text found. Skipping extraction.")
        return updates
        
    editorial_rules = config.get("copywriting_guidelines", "Extract facts accurately and draft a professional summary.")
    
    try:
        llm = get_llm(temperature=0.1)
        structured_llm = llm.with_structured_output(SingleMatterExtraction)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an elite Magic Circle consulting architect.\n"
             "Your task is to extract facts from messy batch data and draft a pristine legal directory matter.\n\n"
             "=== EDITORIAL RULES ===\n"
             "{editorial_rules}\n"
             "======================\n\n"
             "Extract the facts exactly as requested by the schema. Draft the 'summary_of_matter_and_role' "
             "with extreme precision, incorporating the specific lawyers, business context, and maintaining a high-end corporate tone. "
             "If a specific fact is completely missing from the raw text, leave it null or empty. DO NOT HALLUCINATE."
            ),
            ("human", "Here is the raw unstructured batch data:\n\n{raw_text}")
        ])
        
        chain = prompt | structured_llm
        result = chain.invoke({
            "editorial_rules": editorial_rules,
            "raw_text": extracted_text
        })
        
        updates["submission"] = result 
        updates["messages"].append("✅ Genesis Extraction Complete: Drafted single matter successfully.")
        
    except Exception as e:
        updates["messages"].append(f"❌ Genesis Extraction Error: {str(e)}")
        updates["submission"] = SingleMatterExtraction(matter=ExtractedMatter())
        
    return updates