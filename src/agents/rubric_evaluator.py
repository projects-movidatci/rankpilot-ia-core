import os
from typing import Union
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState, PositioningCore
from src.core.schemas import PublishableMatter, ConfidentialMatter
from src.io.rag_call import load_rubric_rag
from src.core.schemas import RubricEvaluation

# 1. The Evaluator System Prompt
SYSTEM_PROMPT_EVALUATOR = """
[ROLE]
You are an elite Editorial Evaluator for Chambers & Partners. Your job is to rigorously assess the narrative strength of a legal matter using our strict 100-point scoring rubric.

[KNOWLEDGE BASE (RUBRIC)]
{rubric_rag_content}

[YOUR MISSION]
You will receive the raw text of a legal matter AND its strategic taxonomy (previously extracted by our data analyst).
You must evaluate the matter across all 9 categories in the Knowledge Base, providing a specific score AND a 1-sentence justification for each. Finally, sum the points and provide the final diagnostic output.

[EVALUATION RULES]
1. MATHEMATICAL ACCURACY: You MUST calculate the exact sum of all 9 category scores. The maximum is 100.
2. JUSTIFICATION: For every category, you must provide a brief, evidence-based justification from the raw text explaining why you awarded that specific score.
3. THE 9 CATEGORIES:
   - Table Fit (Max 10)
   - Transaction Significance (Max 10)
   - Structural Complexity (Max 15)
   - Legal Sophistication (Max 10)
   - Firm Role Strength (Max 15)
   - Client Prestige (Max 10)
   - Cross-border Complexity (Max 10)
   - Innovation / Novelty (Max 10)
   - Narrative Strength (Max 10)
4. CLASSIFICATION: Assign the exact label from the rubric based on the total score (e.g., 'Strong Chambers matter').
5. EDITORIAL FEEDBACK: Write a concise, strategic diagnosis using the 'Diagnostic output template' from the rubric. Explicitly state Strengths, Weaknesses, Missing information, and Rewrite priority. Be brutal. If the firm role is vague or the deal value is missing, penalize them and explicitly write it in the missing information.
"""

# 2. Synchronous function to evaluate a single matter
def evaluate_single_matter(matter: Union[PublishableMatter, ConfidentialMatter], rag_content: str, llm) -> Union[PublishableMatter, ConfidentialMatter]:
    """Calls the LLM to score a single matter and generate editorial feedback."""
    
    # Extract raw data
    client_name = getattr(matter, "D1_name_of_client", getattr(matter, "E1_name_of_client", "Unknown Client"))
    description = getattr(matter, "D2_summary_of_matter_and_role", getattr(matter, "E2_summary_of_matter_and_role", ""))
    value = getattr(matter, "D3_matter_value", getattr(matter, "E3_matter_value", "No value provided"))
    
    if not description or description.strip() == "":
        return matter

    # 🛡️ THE DOMINO FIX: Read from the new nested taxonomy object
    taxonomy_obj = getattr(matter, "taxonomy", None)
    
    category = getattr(taxonomy_obj, "primary_category", "Unknown") if taxonomy_obj else "Unknown"
    role = getattr(taxonomy_obj, "firm_role_taxonomy", "Unknown") if taxonomy_obj else "Unknown"
    complexities = getattr(taxonomy_obj, "complexity_indicators", []) if taxonomy_obj else []
    
    matter_context = (
        f"--- RAW DATA ---\n"
        f"Client: {client_name}\nValue: {value}\nDescription: {description}\n\n"
        f"--- STRATEGIC TAXONOMY (From Agent 1) ---\n"
        f"Category: {category}\nFirm Role: {role}\n"
        f"Complexities Detected: {', '.join(complexities) if complexities else 'None'}"
    )

    # 🛡️ THE FIX: Force the LLM to ONLY output the RubricEvaluation, nothing else!
    structured_llm = llm.with_structured_output(RubricEvaluation)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_EVALUATOR),
        ("human", "Evaluate this matter strictly according to the scoring rubric:\n\n{matter_context}")
    ])

    chain = prompt | structured_llm
    
    try:
        # The LLM now ONLY generates the math and feedback, preserving the original text!
        evaluation_result = chain.invoke({
            "rubric_rag_content": rag_content,
            "matter_context": matter_context
        })
        
        # 🛡️ THE FIX: Staple the new evaluation onto the ORIGINAL untouched matter
        matter.evaluation = evaluation_result
        return matter
        
    except Exception as e:
        print(f"❌ Error evaluating matter {matter.matter_id}: {e}")
        return matter

# 3. THE MAIN LANGGRAPH NODE (Synchronous)
def rubric_evaluator_node(state: AgentState) -> dict:
    """Node that evaluates all matters sequentially."""
    updates = {"current_step": "rubric_evaluation", "messages": []}
    updates["messages"].append("🚀 INITIATING: rubric_evaluator_node (Sequential Scoring)")
    print("🚀 Firing massive rubric evaluation...")

    submission = getattr(state, "submission", None)
    
    if not submission:
        updates["messages"].append("⚠️ Rubric Node Aborted: No submission object found in state.")
        return updates

    # =========================================================
    # 🛡️ THE FIX: Safely extract practice_area from dynamic state
    # =========================================================
    if isinstance(state, dict):
        metadata = state.get("metadata", {}) or {}
    else:
        metadata = getattr(state, "metadata", None) or {}
        
    if isinstance(metadata, dict):
        practice_area = metadata.get("practice_area", "Banking & Finance")
    else:
        practice_area = getattr(metadata, "practice_area", "Banking & Finance")

    # 🛡️ THE FIX: Pass the practice_area to the loader
    rag_content = load_rubric_rag(practice_area)
    
    # Temperature 0.2 to allow for nuanced editorial feedback while keeping scores strict
    llm = get_llm(temperature=0.2) 

    publishable = getattr(submission, "D_publishable_information", None)
    pub_matters = publishable.publishable_matters if publishable else []
    
    confidential = getattr(submission, "E_confidential_information", None)
    conf_matters = confidential.confidential_matters if confidential else []

    all_matters = pub_matters + conf_matters
    
    if not all_matters:
        updates["messages"].append("⚠️ Rubric Node: No matters found to evaluate.")
        return updates

    # ========================================================
    # 🛡️ SYNC EXECUTION (Standard Loop)
    # ========================================================
    evaluated_results = []
    for matter in all_matters:
        result = evaluate_single_matter(matter, rag_content, llm)
        evaluated_results.append(result)
    
    # Reconstruct the separated lists
    evaluated_pub = [m for m in evaluated_results if isinstance(m, PublishableMatter)]
    evaluated_conf = [m for m in evaluated_results if isinstance(m, ConfidentialMatter)]

    if publishable:
        publishable.publishable_matters = evaluated_pub
    if confidential:
        confidential.confidential_matters = evaluated_conf

    updates["submission"] = submission

    # 👇 NUEVO CÓDIGO: CÁLCULO DE LA CONFIANZA INICIAL (PROMEDIO) 👇
    total_score_sum = 0
    valid_evaluations_count = 0

    for m in evaluated_results:
        if hasattr(m, "evaluation") and m.evaluation:
            total_score_sum += m.evaluation.total_score
            valid_evaluations_count += 1

    initial_confidence = 0.0
    if valid_evaluations_count > 0:
        # Calculamos el promedio sobre 100 y lo dejamos como float (ej. 72.0)
        # para que tu frontend o main.py pueda renderizarlo como "72%"
        initial_confidence = round(total_score_sum / valid_evaluations_count, 1)

    # Recuperar el positioning_core actual del estado (o crear uno nuevo)
    if isinstance(state, dict):
        current_core = state.get("positioning_core", None)
    else:
        current_core = getattr(state, "positioning_core", None)

    if not current_core:
        current_core = PositioningCore(confidence_score=initial_confidence)
    else:
        # Si ya existe (como Pydantic model o dict), lo actualizamos
        if isinstance(current_core, dict):
            current_core["confidence_score"] = initial_confidence
        else:
            current_core.confidence_score = initial_confidence

    updates["positioning_core"] = current_core
    # 👆 FIN DEL NUEVO CÓDIGO 👆

    updates["messages"].append(f"✅ Rubric Node Success: Evaluated {len(evaluated_results)} matters successfully. Initial Confidence: {initial_confidence}%")
    print(f"✅ Rubric evaluation completed for {len(evaluated_results)} matters. Promedio: {initial_confidence}%")

    return updates

def final_evaluation_node(state: AgentState) -> dict:
    """
    Runs the exact same rubric evaluation, but acts as a separate node in LangGraph 
    so it can safely route to Assembly instead of back to the Auditor.
    """
    # Call your existing evaluator logic
    updates = rubric_evaluator_node(state)
    
    # Overwrite the step and messages so the frontend knows it's the final pass
    updates["current_step"] = "final_evaluation"
    updates["messages"].append("✅ Final Evaluation complete: Matter scores updated based on the optimized narratives.")
    
    return updates