import os
import unicodedata
from typing import List, Dict, Any
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import LawyerRubricEvaluation, ExecutiveLawyerDiagnosis, B9LawyerProfile

def normalize_text(text: str) -> str:
    """Removes accents (ñ -> n) and converts to lowercase for bulletproof matching."""
    if not text: return ""
    return unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()

class LawyerEvaluationOutput(BaseModel):
    rubric_evaluation: LawyerRubricEvaluation
    executive_diagnosis: ExecutiveLawyerDiagnosis

SYSTEM_PROMPT_LAWYER_EVALUATION = """
[ROLE]
You are an elite Directory Researcher and Strategy Consultant for Chambers & Partners. Your objective is to evaluate a specific lawyer's candidacy for a ranking based strictly on the empirical evidence of the matters they worked on this year.

[YOUR MISSION]
You will receive the lawyer's raw B9 biography (what the firm claims) and the text of the actual matters they participated in (the factual evidence). 
You must evaluate them against our 11-Point Bench Strength Rubric and provide an Executive Diagnosis.

[EVALUATION RULES]
1. BE OBJECTIVE AND RUTHLESS: Do not blindly believe the B9 biography. If the B9 claims they are a "leading expert in Fintech" but their associated matters only show routine real estate work, you must penalize their `narrative_consistency` and highlight the risk of overclaiming.
2. NO EVIDENCE = NO SCORE: If the associated matters text is empty or very weak, their scores for `matter_strength` and `role_clarity` must reflect that lack of evidence.
3. MATHEMATICAL ACCURACY: Ensure `total_readiness_score` is the exact sum of the 11 category scores.
"""

def lawyer_evaluation_node(state: AgentState) -> dict:
    print("🔍 Initiating lawyer_evaluation_node: Cross-referencing profiles with matter evidence...")
    
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

    llm = get_llm(temperature=0).with_structured_output(LawyerEvaluationOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_LAWYER_EVALUATION),
        ("human", "Lawyer Name: {name}\nRole: {role}\nTarget Ranking: {target}\n\nRAW B9 BIOGRAPHY:\n{biography}\n\nEVIDENCE (ASSOCIATED MATTERS):\n{matters_evidence}")
    ])
    
    chain = prompt | llm
    updated_profiles = []

    for item in lawyer_profiles:
        # 🛡️ THE FIX: Re-hydrate the dictionary back into a Pydantic object
        profile = B9LawyerProfile(**item) if isinstance(item, dict) else item
        
        print(f"   ▶ Evaluating: {profile.name}...")
        lawyer_matters = []
        associated_ids = []
        name_normalized = normalize_text(profile.name)
        
        for index, matter in enumerate(all_matters):
            matter_id = getattr(matter, "matter_id", None)
            if not matter_id:
                matter_id = f"matter_{index}"
                matter.matter_id = matter_id

            m_dict = matter.model_dump() if hasattr(matter, "model_dump") else vars(matter)
            
            lead_d = str(m_dict.get("D5_lead_partner", ""))
            lead_e = str(m_dict.get("E5_lead_partner", m_dict.get("E5_lead_lawyer", "")))
            others_d = str(m_dict.get("D6_other_team_members", ""))
            others_e = str(m_dict.get("E6_other_team_members", ""))
            
            team_string = f"{lead_d} {lead_e} {others_d} {others_e}"
            
            if name_normalized in normalize_text(team_string):
                val = str(m_dict.get("D3_matter_value", m_dict.get("E3_matter_value", "N/A")))
                desc = str(m_dict.get("D2_summary_of_matter_and_role", m_dict.get("E2_summary_of_matter_and_role", "N/A")))
                lawyer_matters.append(f"Matter Value: {val}\nDescription & Role: {desc}")
                associated_ids.append(matter_id)

        profile.associated_matter_ids = associated_ids
        print(f"     🐞 DEBUG EVALUADOR: {profile.name} -> IDs asociados: {associated_ids}")

        if lawyer_matters:
            matters_evidence = "\n\n--- NEXT MATTER ---\n".join(lawyer_matters)
        else:
            matters_evidence = "[NO MATTER EVIDENCE FOUND FOR THIS LAWYER IN SECTIONS D/E]"

        try:
            role_str = "Partner" if profile.is_partner else "Associate/Counsel"
            target_str = profile.target_ranking if profile.target_ranking else "Not specified"
            
            evaluation_result = chain.invoke({
                "name": profile.name,
                "role": role_str,
                "target": target_str,
                "biography": profile.raw_biography,
                "matters_evidence": matters_evidence
            })
            
            profile.rubric_evaluation = evaluation_result.rubric_evaluation
            profile.executive_diagnosis = evaluation_result.executive_diagnosis
            print(f"     ✅ Score obtained: {profile.rubric_evaluation.total_readiness_score}/110")
            
        except Exception as e:
            print(f"     ❌ Error evaluating {profile.name}: {e}")
        
        updated_profiles.append(profile)

    print("✅ Bench Strength Evaluation complete.")
    return {"lawyer_profiles": updated_profiles, "submission": submission}