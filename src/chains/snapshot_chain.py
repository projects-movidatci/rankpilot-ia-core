from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.output_parsers import PydanticOutputParser

# --- 1. ESQUEMA DEL CLASIFICADOR ---
class ArchetypeSelection(BaseModel):
    selected_archetype: str = Field(description="The exact name of the chosen archetype.")
    brief_justification: str = Field(description="1 sentence explaining why.")
    narrative_guidelines: Union[str, List[str]] = Field(
        description="3 strategic bullet points. Can be a single string or a list of strings."
    )

# --- 2. ESQUEMAS DEL SNAPSHOT ---
class PositioningTier(BaseModel):
    label: str = Field(description="One of: 'Elite', 'Consolidated', or 'Market Member'.")
    explanation: str = Field(description="Professional justification for the assigned tier.")

class BlindSpot(BaseModel):
    issue: str = Field(description="A short title for the identified gap.")
    description: str = Field(description="A detailed explanation of why this is a risk.")

class FinalSnapshot(BaseModel):
    confidence_score: float = Field(description="Value between 0.0 and 1.0 based on evidence depth.")
    signals: List[str] = Field(description="Exactly 3 specific evidence-backed signals (e.g., $$$ values, landmark precedents).")
    positioning_tier: PositioningTier = Field(description="Elite, Consolidated, or Market Member.")
    blind_spots: List[BlindSpot] = Field(description="Exactly 4 high-stakes technical gaps.")
    competitive_advantage: List[str] = Field(description="Top 2 'Elite' signals.")


# --- 3. CADENA DEL CLASIFICADOR ---
archetype_parser = PydanticOutputParser(pydantic_object=ArchetypeSelection)

archetype_prompt = ChatPromptTemplate.from_template(
    """
    SYSTEM: You are a strategic legal market classifier.
    Read the following submission data and classify the firm into exactly ONE of the following archetypes:
    {possible_archetypes}
    
    [CONTEXT]
    - Practice Area: {practice_area}
    - Realistic Target: {realistic_target} 
    - Submission Data (Includes Taxonomy Analytics): {submission_json}
    
    [YOUR MISSION]
    1. Choose the archetype that best matches the firm's actual work (Use the Taxonomy Categories and Roles to inform this).
    2. Provide a brief justification.
    3. Generate 3 STRICT 'Narrative Guidelines'.
    
    {format_instructions}
    """
)

llm_classifier = get_llm(temperature=0.0) 
archetype_chain = archetype_prompt.partial(format_instructions=archetype_parser.get_format_instructions()) | llm_classifier | archetype_parser


# --- 4. CADENA DEL SNAPSHOT (Evalúa qué tan lejos están de esa narrativa ideal) ---
parser = PydanticOutputParser(pydantic_object=FinalSnapshot)

snapshot_prompt = ChatPromptTemplate.from_template(
    """
    SYSTEM: 
    You are the "Lead Strategist" for Global Legal Rankings.
    Your mission is to evaluate the current submission and determine how well it aligns with the ideal strategic narrative.
    
    =========================================
    DIRECTORY-SPECIFIC EVALUATION CRITERIA:
    {editorial_rules}
    =========================================
    
    [CRITICAL STRATEGIC CONTEXT]
    - Firm Current Band: {current_band}
    - Firm Trajectory: {ranking_history}
    - Realistic Target: {realistic_target}
    - Evaluation Tone & Directive: {evaluation_tone}
    
    [HARD NARRATIVE RULE - STRICTLY ENFORCED]
    If the submission contains high-quality, complex matters (strong evidence) but the descriptions are poorly written, generic, or lack strategic framing, YOU MUST NOT frame this as a "failure" or "weak practice". 
    Instead, diagnose it explicitly as a "Lack of rankable narrative" or a "Translation Gap" where the firm's excellent work is not being properly communicated to the directory researchers.
    
    [FIRM IDENTITY & IDEAL NARRATIVE]
    - Archetype: **{selected_archetype}**
    - Narrative Guidelines (How they SHOULD be positioning themselves):
    {narrative_guidelines}
    
    GROUNDING MANDATE: 
    If it is not in the submission_json or history, it DOES NOT EXIST. 

    AUDIT PARAMETERS:
    - Practice Area: {practice_area}
    - Optimized Submission Data (Includes Taxonomy Analytics at the very top): {submission_json}

    PHASE 1: THE TECHNICAL CORE 
    - Extract 3 hard evidence signals (deals, precedents, $$$) that strongly support their {selected_archetype} narrative.
    - STRATEGIC REQUIREMENT: Strongly prefer evidence that aligns with the 'Categories' and 'Roles' listed in the TAXONOMY ANALYTICS.

    PHASE 2: THE TIER VERDICT
    - Assign a Tier: [Elite / Consolidated / Market Member].
    - JUSTIFICATION: Compare their actual evidence against the {realistic_target} considering their current trajectory ({ranking_history}).

    PHASE 3: THE NARRATIVE BLIND SPOTS (4 Points)
    Identify exactly 4 areas where their current text fails to follow the 'Narrative Guidelines' or the 'Evaluation Tone'. (Remember the HARD NARRATIVE RULE: distinguish between weak evidence vs. weak writing).

    PHASE 4: THE WEAPONS (2 Competitive Advantages)
    Identify exactly 2 structural or factual strengths that we can highlight in the final report.
    - CRITICAL COMMAND: You MUST leverage the 'Complexities Leveraged' and 'Firm Roles' listed in the TAXONOMY ANALYTICS to articulate exactly why this firm has a structural advantage over competitors.

    {format_instructions}
    """
)

llm = get_llm(temperature=0.2)
snapshot_chain = (
    snapshot_prompt.partial(format_instructions=parser.get_format_instructions())
    | llm
    | parser
)