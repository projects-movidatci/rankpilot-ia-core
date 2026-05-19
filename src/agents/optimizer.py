from typing import Union
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import PublishableMatter, ConfidentialMatter

# 1. The Ghostwriter System Prompt
# 1. The Ghostwriter System Prompt
SYSTEM_PROMPT_OPTIMIZER = """
[ROLE]
You are an elite Legal Ghostwriter and Senior Editor for Chambers & Partners submissions. 
Your exclusive task is to ELEVATE, EXPAND, and ENHANCE legal matter descriptions. You are strictly forbidden from summarizing, simplifying, or truncating the original text.

[FIRM CONTEXT]
Firm Name: {firm_name}
Practice Area: {practice_area}
Jurisdiction: {jurisdiction}

[STRATEGIC DIAGNOSIS (THE FIX LIST)]
{editorial_feedback}

[PARTNER'S NEW STRATEGIC INPUT]
{partner_notes}

[YOUR MISSION]
You will receive the raw data, detected complexities, and original description for a legal transaction. 
You MUST rewrite the matter description into a highly persuasive, comprehensive, and sophisticated narrative that proves the firm's elite market positioning. 
Crucially, you MUST seamlessly weave the 'Partner's New Strategic Input' into the narrative to resolve the weaknesses identified in the 'Strategic Diagnosis'.

[STRICT FIDELITY & EXPANSION RULES]
1. THE 3-PARAGRAPH ARCHITECTURE (ANTI-FLATTENING): You MUST structure your output into EXACTLY THREE distinct paragraphs. You MUST separate each paragraph with a double line break (\n\n). Do not write a single block of text.
   - Paragraph 1: The Client, the Deal Value, and the overarching strategic/business purpose of the transaction.
   - Paragraph 2: The Legal & Structural Complexities. Detail the specific legal mechanics, regulatory hurdles, and bespoke frameworks.
   - Paragraph 3: The Firm's Execution. Explain the firm's exact lead role and how it successfully navigated the challenges.

2. ABSOLUTE ZERO DATA LOSS: You have NO editorial authority to delete data. You MUST retain EVERY single entity name (including all minor subsidiaries and trusts), every government/regulatory body, every exact financial figure (e.g., specific costs per unit), and every jurisdiction mentioned in the raw text. 

3. WEAVE THE COMPLEXITIES & NEW NOTES: Use the 'Complexities' list and the 'Partner's New Strategic Input' to inject specific legal terminology into Paragraph 2 and 3. Explicitly explain HOW the firm overcame hurdles and what specific role they played.

4. ACTIVE LEADERSHIP VERBS: Apply the 'Strategic Diagnosis' feedback. Eradicate weak verbs (e.g., "assisted", "helped", "was involved"). Forcefully insert strong leadership verbs (e.g., "spearheaded", "architected", "orchestrated", "navigated", "structured").

5. TONE: Highly technical, objective, and premium corporate. No marketing fluff, no boastful adjectives like "amazing" or "fantastic." Let the dense legal complexity prove the prestige.

Output ONLY the final, rewritten 3-paragraph narrative. Do not include labels like "Paragraph 1", introductory text, or markdown formatting outside of the text itself.
"""
# 2. Synchronous function to rewrite a single matter
def optimize_single_matter(matter: Union[PublishableMatter, ConfidentialMatter], metadata: dict, llm) -> Union[PublishableMatter, ConfidentialMatter]:
    """Calls the LLM to rewrite the narrative based on the rubric feedback."""
    
    # Extract the rubric evaluation
    evaluation = getattr(matter, "evaluation", None)
    
    feedback = evaluation.editorial_feedback if evaluation else "Ensure the narrative is professional, clear, and highlights the firm's role."
    
    # Extract raw data to feed the ghostwriter
    client_name = getattr(matter, "D1_name_of_client", getattr(matter, "E1_name_of_client", "Unknown Client"))
    description = getattr(matter, "D2_summary_of_matter_and_role", getattr(matter, "E2_summary_of_matter_and_role", ""))
    value = getattr(matter, "D3_matter_value", getattr(matter, "E3_matter_value", "No value provided"))
    
    # 🛡️ THE NEW FIX: Extract the answers from the Interrogation loop!
    partner_notes = getattr(matter, "partner_additional_notes", None)
    if not partner_notes:
        partner_notes = "No additional context provided. Rely on the original description."
        
    taxonomy_obj = getattr(matter, "taxonomy", None)
    complexities = getattr(taxonomy_obj, "complexity_indicators", []) if taxonomy_obj else []

    if not description or description.strip() == "":
        return matter

    raw_matter_data = (
        f"Client: {client_name}\n"
        f"Deal Value: {value}\n"
        f"Complexities: {', '.join(complexities) if complexities else 'None identified'}\n"
        f"Original Description (Needs Polish): {description}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_OPTIMIZER),
        ("human", "Rewrite this matter based on the strategic diagnosis:\n\n{raw_matter_data}")
    ])

    chain = prompt | llm  
    
    try:
        # 🛡️ SYNC EXECUTION
        result = chain.invoke({
            "firm_name": metadata.get("firm_name", "the firm"),
            "practice_area": metadata.get("practice_area", "this practice"),
            "jurisdiction": metadata.get("jurisdiction", "this jurisdiction"),
            "editorial_feedback": feedback,
            "partner_notes": partner_notes, # 👈 PASSED HERE
            "raw_matter_data": raw_matter_data
        })
        
        rewritten_text = result.content.strip()
        
        # Inject the newly ghostwritten text back into the correct field
        if isinstance(matter, PublishableMatter):
            matter.original_draft_summary = matter.D2_summary_of_matter_and_role
            matter.D2_summary_of_matter_and_role = rewritten_text
        else:
            matter.original_draft_summary = matter.E2_summary_of_matter_and_role
            matter.E2_summary_of_matter_and_role = rewritten_text
            
        return matter
        
    except Exception as e:
        print(f"❌ Error optimizing matter {matter.matter_id}: {e}")
        return matter

# 3. THE MAIN LANGGRAPH NODE (Synchronous)
def optimize_node(state: AgentState) -> dict:
    """Node that rewrites and optimizes all matters sequentially."""
    updates = {"current_step": "optimization", "messages": []}
    updates["messages"].append("🚀 INITIATING: optimize_node (The Ghostwriter)")
    print("🚀 Firing massive narrative optimization...")

    submission = getattr(state, "submission", None)
    if not submission:
        return updates

    # Extract Metadata for Firm Context
    if isinstance(state, dict):
        metadata_obj = state.get("metadata", {}) or {}
    else:
        metadata_obj = getattr(state, "metadata", None) or {}
        
    metadata = metadata_obj if isinstance(metadata_obj, dict) else (metadata_obj.model_dump() if hasattr(metadata_obj, "model_dump") else {})

    # Use a slightly higher temperature (e.g., 0.4) for better creative writing flow
    llm = get_llm(temperature=0.4) 

    publishable = getattr(submission, "D_publishable_information", None)
    pub_matters = publishable.publishable_matters if publishable else []
    
    confidential = getattr(submission, "E_confidential_information", None)
    conf_matters = confidential.confidential_matters if confidential else []

    all_matters = pub_matters + conf_matters
    
    if not all_matters:
        return updates

    # ========================================================
    # 🛡️ SYNC EXECUTION (Standard Loop)
    # ========================================================
    optimized_results = []
    for matter in all_matters:
        result = optimize_single_matter(matter, metadata, llm)
        optimized_results.append(result)
    
    # Reconstruct the separated lists
    optimized_pub = [m for m in optimized_results if isinstance(m, PublishableMatter)]
    optimized_conf = [m for m in optimized_results if isinstance(m, ConfidentialMatter)]

    if publishable:
        publishable.publishable_matters = optimized_pub
    if confidential:
        confidential.confidential_matters = optimized_conf

    updates["submission"] = submission
    updates["messages"].append(f"✅ Optimize Node Success: Ghostwrote {len(optimized_results)} narratives.")
    print(f"✅ Narrative optimization completed for {len(optimized_results)} matters.")

    return updates