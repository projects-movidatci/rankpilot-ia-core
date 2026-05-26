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
1. NO PASSIVE VOICE: Do not say "He assisted with...". Say "He orchestrated...", "He spearheaded...", or "He structured...".
2. ANCHOR IN FACTS: You MUST explicitly mention their specific technical contributions from the evidence provided. Connect their profile directly to the matters.
3. ALIGN WITH DIAGNOSIS: If the diagnosis says they are an "Associate to Watch candidate", ensure the tone highlights their emerging leadership and bench strength contribution.
4. NO HALLUCINATIONS: Do not invent deals, clients, or skills that are not present in the provided evidence.

[MARKDOWN FORMATTING & PACING RULES]
- NO WALLS OF TEXT: Do not write a single massive block. Break the narrative into exactly 2 or 3 punchy paragraphs.
- DOUBLE SPACING: You MUST use double line breaks (\\n\\n) between paragraphs to ensure strict Markdown and Word compatibility.
- BOLD HIGHLIGHTS: Use **bold text** for key client names, high-value amounts (e.g., **USD 4.5 million**), and core technical roles (e.g., **Lead Counsel**).
- HIGH-IMPACT BULLETS: If the lawyer handled multiple distinct matters, use a clean bulleted list for the evidence section to maximize readability for Chambers researchers.
- NO HEADERS: Do not use markdown headers (like # or ##) to maintain table compatibility in the final document.
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

    print("✅ B9 Narrative Optimization complete.")
    return {"lawyer_profiles": updated_profiles, "submission": submission}