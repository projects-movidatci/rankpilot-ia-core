from typing import Union
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import PublishableMatter, ConfidentialMatter, SingleMatterExtraction

# =========================================================
# ACT 0: THE MATTERS ASSISTANT OPTIMIZER
# =========================================================
def matters_assistant_optimize_node(state: AgentState) -> dict:
    """
    Act 0 Ghostwriter:
    Takes a single matter, polishes the narrative, elevates the vocabulary,
    and ensures high-quality Chambers/Legal500 tone without needing portfolio context.
    """
    updates = {"current_step": "ma_optimize", "messages": []}

    # 1. Extracción Segura
    if isinstance(state, dict):
        submission = state.get("submission", {})
        metadata = state.get("metadata", {})
    else:
        submission = getattr(state, "submission", None)
        metadata = getattr(state, "metadata", {}) or {}

    if not submission:
        updates["messages"].append("MA Optimizer: No submission found. Skipping.")
        return updates

    # 2. Localizar el texto a optimizar
    if isinstance(submission, dict):
        matter_data = submission.get("matter", {})
    else:
        matter_data = submission.matter.model_dump() if hasattr(submission, "matter") else {}

    raw_summary = matter_data.get("summary_of_matter_and_role", "")

    if not raw_summary or raw_summary == "None":
        updates["messages"].append("MA Optimizer: No summary to optimize. Skipping.")
        return updates

    # 3. Extraer contexto para el LLM
    firm_name = getattr(metadata, "firm_name", "Our Firm")
    practice_area = getattr(metadata, "practice_area", "the practice area")
    jurisdiction = getattr(metadata, "jurisdiction", "the jurisdiction")

    # 4. El Prompt Especializado del Acto 0
    MA_OPTIMIZER_PROMPT = """
        [ROLE]
        You are an elite Legal Ghostwriter and Senior Editor for Chambers & Partners submissions. 

        [FIRM CONTEXT]
        Firm Name: {firm_name}
        Practice Area: {practice_area}
        Jurisdiction: {jurisdiction}

        [CRITICAL MISSION - ZERO DATA LOSS]
        You MUST rewrite the raw description into a fluid, 3-paragraph corporate essay.
        HOWEVER, you are strictly bound to the following data points. You MUST explicitly type these EXACT strings into your essay. Do not generalize them. Failure to include them will result in rejection:
        - Client Name: {client_name}
        - Matter Value: {matter_value}
        - Lead Partner(s): {lead_partner}
        - Other Firms / Opposing Counsel: {other_firms}

        [STRICT FIDELITY & EXPANSION RULES]
        1. THE FLUID ESSAY ARCHITECTURE: You MUST write exactly three distinct paragraphs, separated by a double line break (\n\n). DO NOT use any headings, labels, or bullet points.
           - Paragraph 1: You MUST introduce the Client Name and the Matter Value in the very first sentence to establish the business context.
           - Paragraph 2: The Legal & Structural Complexities. 
           - Paragraph 3: The Firm's Execution. If opposing counsel or other firms are mentioned, state their involvement neutrally to demonstrate peer caliber (do NOT frame them as antagonists or obstacles).
        2. DATA ANCHORING: Weave the exact Client Name, Matter Value, and Partner names seamlessly into the narrative.
        3. ELEVATE LEGAL TERMINOLOGY: Inject highly specific, advanced legal terminology based on the raw facts provided.
        4. ACTIVE LEADERSHIP VERBS: Eradicate weak verbs. Forcefully insert strong leadership verbs (e.g., "spearheaded", "architected", "orchestrated", "navigated").
        5. TONE: Highly technical, objective, and premium corporate. Let the dense legal complexity prove the prestige.
        6. SINGLE OUTPUT ONLY: Generate EXACTLY ONE definitive version of the narrative. Do not offer alternatives, options, or conversational filler.

        [RAW DESCRIPTION]
        {raw_summary}

        Output ONLY the final, rewritten 3-paragraph narrative.
        """

    try:
        # Usamos una temperatura de 0.3 para un buen balance entre precisión y fluidez narrativa
        prompt = ChatPromptTemplate.from_template(MA_OPTIMIZER_PROMPT)
        llm = get_llm(temperature=0.3)
        chain = prompt | llm

        client_name = matter_data.get("client_name", "the client")
        matter_value = matter_data.get("matter_value", "the transaction value")
        
        lead_partners_list = matter_data.get("lead_partners", [])
        lead_partner = ", ".join(lead_partners_list) if lead_partners_list else "the lead partner"
        
        other_firms_list = matter_data.get("other_firms_advising", [])
        other_firms = ", ".join(other_firms_list) if other_firms_list else "opposing counsel"

        # 2. Pasa las variables al prompt
        result = chain.invoke({
            "firm_name": firm_name,
            "practice_area": practice_area,
            "jurisdiction": jurisdiction,
            "client_name": client_name,
            "matter_value": matter_value,
            "lead_partner": lead_partner,
            "other_firms": other_firms,
            "raw_summary": raw_summary
        })

        optimized_text = result.content

        # 5. Inyectar el texto optimizado de vuelta al esquema
        if isinstance(submission, dict):
            submission["matter"]["summary_of_matter_and_role"] = optimized_text
        else:
            submission.matter.summary_of_matter_and_role = optimized_text

        updates["submission"] = submission
        updates["messages"].append("✅ MA Optimize Node: Successfully polished the single matter narrative.")

    except Exception as e:
        updates["messages"].append(f"❌ MA Optimizer Error: {str(e)}")

    return updates

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