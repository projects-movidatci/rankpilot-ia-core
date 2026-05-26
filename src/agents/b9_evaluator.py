import json
from typing import List
from pydantic import BaseModel, Field # Add this import
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import B9LawyerProfile

# --- ADD THIS WRAPPER CLASS ---
class LawyerProfileCollection(BaseModel):
    """Wrapper class to allow LangChain to output a list of profiles."""
    profiles: List[B9LawyerProfile] = Field(
        default_factory=list, 
        description="The extracted list of lawyer profiles."
    )

# =====================================================================
# 2. THE EXTRACTOR PROMPT
# =====================================================================
SYSTEM_PROMPT_B9_EXTRACTION = """
[ROLE]
You are an elite Legal Data Analyst for Chambers & Partners. Your job is to parse the B9 (Lawyers Ranked and Unranked) data of a law firm's submission and extract the profiles of the individual lawyers being proposed or maintained for rankings.

[YOUR MISSION]
You will receive JSON-formatted data representing the B9 section. You must extract each lawyer mentioned and output a structured list of their profiles.

[EXTRACTION RULES]
1. INDIVIDUAL IDENTIFICATION: Identify every single lawyer mentioned in the data.
2. ROLE ASSIGNMENT: Determine if they are a Partner (is_partner = true) or Counsel/Associate/Other (is_partner = false).
3. RANKING STATUS: Infer their `current_ranking` and `target_ranking` if explicitly stated in the comments. If not explicitly mentioned, leave as null.
4. RAW BIOGRAPHY: Extract the exact, complete narrative text provided in the `comments_or_web_link` field. DO NOT summarize it. Copy the sentences exactly so we have the pure baseline argument.
"""

# =====================================================================
# 3. THE LANGGRAPH NODE
# =====================================================================
def b9_extraction_node(state: AgentState) -> dict:
    """
    Extracts and structures lawyer profiles from the B9 section.
    """
    print("🔍 Initiating b9_extraction_node: Extracting lawyer profiles...")
    
    submission = getattr(state, "submission", None)
    if not submission:
        print("⚠️ No submission object found in state. Skipping extraction.")
        return {"lawyer_profiles": []}
        
    dept_info = getattr(submission, "B_department_information", None)
    if not dept_info:
        print("⚠️ No B_department_information found in submission. Skipping extraction.")
        return {"lawyer_profiles": []}
        
    b9_data_list = getattr(dept_info, "B9_lawyers_ranked_unranked", [])
    
    if not b9_data_list:
        print("⚠️ The B9_lawyers_ranked_unranked list is empty. Skipping extraction.")
        return {"lawyer_profiles": []}

    def safe_dump(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump(exclude_none=True)
        return obj if isinstance(obj, dict) else str(obj)

    try:
        b9_text = json.dumps([safe_dump(item) for item in b9_data_list], indent=2)
    except Exception as e:
        print(f"⚠️ Error serializing B9 data: {e}")
        return {"lawyer_profiles": []}

    # 🐛 FIX APPLIED: We pass the BaseModel wrapper class instead of List[]
    llm = get_llm(temperature=0).with_structured_output(LawyerProfileCollection)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_B9_EXTRACTION),
        ("human", "B9 JSON Data:\n\n{b9_text}")
    ])
    
    chain = prompt | llm
    
    try:
        # ✅ FIX 2: Invoke the chain and extract the .profiles list
        extracted_data = chain.invoke({"b9_text": b9_text})
        extracted_profiles = extracted_data.profiles
        
        print(f"✅ Successfully extracted {len(extracted_profiles)} lawyer profiles from Section B9.")
        return {"lawyer_profiles": extracted_profiles}
        
    except Exception as e:
        print(f"❌ Critical error in b9_extraction_node: {e}")
        return {"lawyer_profiles": []}