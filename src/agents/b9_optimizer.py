import os
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import B9LawyerProfile

class OptimizedBiographyOutput(BaseModel):
    optimized_biography: str = Field(
        description="The final, devastatingly effective B9 narrative anchored entirely in the facts of the associated matters, formatted in Markdown."
    )

SYSTEM_PROMPT_B9_OPTIMIZATION = """
[ROLE]
You are an elite Legal Copywriter and Ghostwriter for Chambers & Partners submissions. Your objective is to rewrite a lawyer's B9 profile to make it an unassailable, mathematically backed argument for their ranking using pristine Markdown formatting.

[YOUR MISSION]
You will receive:
1. The lawyer's raw B9 biography (the firm's original claim).
2. The executive diagnosis from our strategic audit.
3. The factual evidence (the texts of the actual matters they worked on).

You must rewrite the biography into a compelling, sophisticated narrative.

[GHOSTWRITING RULES]
1. PRESERVE CORE IDENTITY & NO ENTITY LOSS: You MUST retain the critical background data from the RAW BIOGRAPHY. Crucially, you are forbidden from losing or omitting information about ANY entity mentioned in the original text (e.g., legacy clients, companies, financial institutions, board memberships, or academic institutions). You must seamlessly synthesize every specific name with the new evidence.
2. NO PASSIVE VOICE: Do not say "He assisted with...". Say "He orchestrated...", "He spearheaded...", or "He structured...".
3. ANCHOR IN FACTS: You MUST explicitly mention their specific technical contributions from the evidence provided. Connect their legacy profile directly to the recent matters.
4. ALIGN WITH DIAGNOSIS: If the diagnosis says they are an "Associate to Watch candidate", ensure the tone highlights their emerging leadership and bench strength contribution.
5. SCRUB FLUFF, NOT FACTS: Do not invent deals, clients, or skills (NO HALLUCINATIONS). Remove empty marketing adjectives from the raw biography, but keep the hard factual nouns.
6. NO ENTITY LOSS: You must strictly retain and mention every key entity (e.g., active clients, external advising firms, acquired companies, financial institutions) provided in the original source material. You are forbidden from generalizing or dropping specific entity names during your synthesis.

[MARKDOWN FORMATTING & PACING RULES]
- NO WALLS OF TEXT: Do not write a single massive block. Break the narrative into exactly 2 or 3 punchy paragraphs.
- DOUBLE SPACING: You MUST use double line breaks (\\n\\n) between paragraphs to ensure strict Markdown and Word compatibility.
- BOLD HIGHLIGHTS: Use **bold text** for key client names, high-value amounts (e.g., **USD 4.5 million**), and core technical roles (e.g., **Lead Counsel**).
- HIGH-IMPACT BULLETS: If the lawyer handled multiple distinct matters, use a clean bulleted list for the evidence section to maximize readability for Chambers researchers.
- NO NESTED BULLETS: Keep your bulleted list strictly flat. Do not use sub-bullets or indentation.
- NO HEADERS: Do not use markdown headers (like # or ##) to maintain table compatibility in the final document.
"""

class DepartmentOverviewOutput(BaseModel):
    department_best_known_for: str = Field(
        description="The final 2000-word executive summary of the department, utilizing Markdown bullet points and bolding for evidence."
    )

SYSTEM_PROMPT_DEPARTMENT_OVERVIEW = """
[ROLE]
You are an elite Legal Ghostwriter and Senior Editor for Chambers & Partners submissions.

[YOUR MISSION]
Write the "What is this department best known for?" section. 
You will receive the newly optimized Lawyer Profiles and the Firm's top Matters. You must synthesize this into a master executive summary of the department.

[GHOSTWRITING RULES & THE 'MAGIC CIRCLE' STANDARD]
1. EFFORTLESS & PREMIUM TONE: Sound like a top-tier London or New York consultant. Market-facing, definitive, and exact. NO legalese, NO academic phrasing, and NO passive voice.
2. STRUCTURAL ARCHITECTURE: 
   - Start with a powerful 1-2 sentence introductory paragraph defining the practice's elite positioning.
   - Then, create distinct bullet points grouped by the firm's strategic pillars (e.g., "Cross-Border Finance", "Fintech & Regulatory", "Debt Restructuring").
3. EVIDENCE ANCHORING (CRITICAL): Under every single bullet point, you MUST cite 1 or 2 specific matters from the provided evidence to prove the claim. Do not make empty claims. 
   - Example format: "Examples include advising **[Client Name]** on a **[Value]** facility..."
4. NO ENTITY LOSS: You must strictly retain and mention every key entity (e.g., active clients, external advising firms, acquired companies, financial institutions) provided in the original source material. You are forbidden from generalizing or dropping specific entity names during your synthesis.

[MARKDOWN FORMATTING RULES]
1. STRICT BULLET POINTS: You must use Markdown bullet points (`*` or `-`). 
2. NO NESTED BULLETS: Keep your bulleted list strictly flat. Do not use sub-bullets or indentation, as this will corrupt the final database formatting.
3. BOLD HIGHLIGHTS: You MUST use **bold text** to highlight Client Names and Financial Values to make the document highly scannable for directory researchers.
4. WORD LIMIT: Strictly under 2000 words. Make every word count.
"""

def b9_optimization_node(state: AgentState) -> dict:
    print("✍️ Initiating b9_optimization_node: Ghostwriting B9 narratives...")
    
    lawyer_profiles = state.lawyer_profiles
    if not lawyer_profiles:
        return {"lawyer_profiles": []}
        
    submission = getattr(state, "submission", None)
    if not submission:
        return {"lawyer_profiles": lawyer_profiles}

    all_matters = []
    if hasattr(submission, "D_publishable_information") and submission.D_publishable_information:
        all_matters.extend(getattr(submission.D_publishable_information, "publishable_matters", []))
    if hasattr(submission, "E_confidential_information") and submission.E_confidential_information:
        all_matters.extend(getattr(submission.E_confidential_information, "confidential_matters", []))

    llm = get_llm(temperature=0.4).with_structured_output(OptimizedBiographyOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_B9_OPTIMIZATION),
        ("human", "Lawyer Name: {name}\n\nRAW BIOGRAPHY:\n{raw_bio}\n\nSTRATEGIC DIAGNOSIS:\n{diagnosis}\n\nEVIDENCE (MATTER TEXTS):\n{evidence}")
    ])
    
    chain = prompt | llm
    updated_profiles = []

    for item in lawyer_profiles:
        # 🛡️ THE FIX: Re-hydrate the dictionary back into a Pydantic object
        profile = B9LawyerProfile(**item) if isinstance(item, dict) else item
        
        print(f"   ▶ Ghostwriting profile for: {profile.name}...")
        print(f"     🐞 DEBUG OPTIMIZADOR: {profile.name} -> IDs recibidos: {profile.associated_matter_ids}")
        
        lawyer_matter_texts = []
        
        if not profile.associated_matter_ids:
            print(f"     ⚠️ {profile.name} has no associated matters. Applying light polish only.")
            evidence_text = "[NO FACTUAL EVIDENCE PROVIDED IN SECTIONS D/E. DO NOT MAKE BOLD CLAIMS.]"
        else:
            for matter in all_matters:
                matter_id = getattr(matter, "matter_id", "")
                if matter_id and matter_id in profile.associated_matter_ids:
                    m_dict = matter.model_dump() if hasattr(matter, "model_dump") else vars(matter)
                    text = str(m_dict.get("D2_summary_of_matter_and_role", m_dict.get("E2_summary_of_matter_and_role", "")))
                    if text and text != "None":
                        lawyer_matter_texts.append(text)
            
            if not lawyer_matter_texts:
                evidence_text = "[NO FACTUAL EVIDENCE PROVIDED IN SECTIONS D/E. DO NOT MAKE BOLD CLAIMS.]"
            else:
                evidence_text = "\n\n---\n\n".join(lawyer_matter_texts)

        diagnosis_text = "N/A"
        if profile.executive_diagnosis:
            diagnosis_text = f"Action: {profile.executive_diagnosis.recommended_action}\nRationale: {profile.executive_diagnosis.rationale}"

        try:
            result = chain.invoke({
                "name": profile.name,
                "raw_bio": profile.raw_biography,
                "diagnosis": diagnosis_text,
                "evidence": evidence_text
            })
            
            profile.optimized_biography = result.optimized_biography
            print(f"     ✅ Successfully optimized narrative for {profile.name}.")
            
        except Exception as e:
            print(f"     ❌ Error ghostwriting for {profile.name}: {e}")
            profile.optimized_biography = profile.raw_biography
        
        updated_profiles.append(profile)

        # Inject back into original structure for the Word template
        dept_info = getattr(submission, "B_department_information", None)
        if dept_info:
            b9_list = getattr(dept_info, "B9_lawyers_ranked_unranked", [])
            for sub_lawyer in b9_list:
                if sub_lawyer.name.strip().lower() == profile.name.strip().lower():
                    sub_lawyer.comments_or_web_link = profile.optimized_biography

    # =====================================================================
    # 🧠 NEW: DEPARTMENT OVERVIEW SYNTHESIS (B7/B10)
    # =====================================================================
    print("✍️ Initiating Department Overview Synthesis...")
    
    try:
        # 1. Gather all optimized matter descriptions
        matter_summaries = []
        for matter in all_matters:
            m_dict = matter.model_dump() if hasattr(matter, "model_dump") else vars(matter)
            client = m_dict.get("D1_name_of_client", m_dict.get("E1_name_of_client", "Confidential Client"))
            val = m_dict.get("D3_matter_value", m_dict.get("E3_matter_value", "N/A"))
            desc = m_dict.get("D2_summary_of_matter_and_role", m_dict.get("E2_summary_of_matter_and_role", ""))
            if desc and desc != "None":
                matter_summaries.append(f"Client: {client} | Value: {val}\nSummary: {desc}")
        
        # 2. Gather all optimized lawyer profiles
        lawyer_summaries = []
        for profile in updated_profiles:
            if profile.optimized_biography:
                lawyer_summaries.append(f"Lawyer: {profile.name}\nProfile: {profile.optimized_biography}")
        
        # 3. Compile the payload
        evidence_payload = (
            "--- OPTIMIZED LAWYER PROFILES ---\n" + 
            "\n\n".join(lawyer_summaries) + 
            "\n\n--- TOP MATTER EVIDENCE ---\n" + 
            "\n\n".join(matter_summaries[:10]) # Cap at top 10 matters to prevent token overflow
        )

        # 4. Invoke the LLM
        overview_llm = get_llm(temperature=0.3).with_structured_output(DepartmentOverviewOutput)
        overview_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT_DEPARTMENT_OVERVIEW),
            ("human", "Synthesize the department overview based on this evidence:\n\n{evidence}")
        ])
        
        overview_chain = overview_prompt | overview_llm
        overview_result = overview_chain.invoke({"evidence": evidence_payload})
        
        # 5. Inject back into the submission object
        if dept_info:
            dept_info.department_best_known_for = overview_result.department_best_known_for
            print("     ✅ Successfully synthesized the Department Overview.")

    except Exception as e:
        print(f"     ❌ Error synthesizing Department Overview: {e}")

    # 🛡️ Final Return
    return {"lawyer_profiles": updated_profiles, "submission": submission}