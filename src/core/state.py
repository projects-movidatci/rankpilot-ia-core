import operator
from typing import Annotated, List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from src.core.schemas import BaseSubmission, B9LawyerProfile
import re

class Base64File(BaseModel):
    filename: str
    mime_type: str
    base64_data: str

class MattersAssistantPayload(BaseModel):
    raw_input_text: Optional[str] = Field(None, description="Any raw text notes or forwarded emails from the lawyer.")
    batch_documents: Optional[List[Base64File]] = Field(default_factory=list)

    @validator('batch_documents')
    def validate_file_limit(cls, v):
        if v and len(v) > 10:
            raise ValueError("Limit exceeded: You can only upload a maximum of 10 files. Please combine additional data into a single PDF or DOCX.")
        return v

class PositioningCore(BaseModel):
    practice_model: str = ""
    practice_definition: str = ""
    narrative_guidelines: Union[str, List[str]] = Field(default_factory=list)
    confidence_score: float = 0.0
    signals: List[str] = Field(default_factory=list)

class PositioningTier(BaseModel):
    label: str = ""
    explanation: str = ""

class BlindSpot(BaseModel):
    issue: str = ""
    description: str = ""

class Milestone(BaseModel):
    category: str
    action_title: str
    why_it_matters: str
    technical_instruction: str
    priority_level: int
    target_completion_date: str

class ExecutiveSummary(BaseModel):
    overall_score: int = 0
    risk_level: str = ""
    strategic_verdict: str = ""
    top_differentiators: List[str] = Field(default_factory=list)
    audit_letter_markdown: str = ""

class MetaData(BaseModel):
    file_base64: Optional[Base64File] = None
    target_band: Optional[str] = None
    directory: Optional[str] = None
    guide: str = Field(default="", description="Guide/Book/Research Edition")
    region: str = Field(default="", description="Región")
    practice_area: str = ""
    jurisdiction: str = Field(default="", description="Jurisdicción")
    location: str = ""
    submission_deadline: str = ""
    firm_name: str = ""
    current_band: str = Field(default="Unranked", description="Default assumption if missing.")
    ranking_history: str = Field(default="Stagnation", description="Default assumption to force an ascension narrative.")

    # 👇 THE PERFECTED METADATA VALIDATOR 👇
    @model_validator(mode="before")
    @classmethod
    def sanitize_nulls_from_php(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. GOLDEN RULE: If file_base64 is empty, force it to None
            if "file_base64" in data and not data.get("file_base64"):
                data["file_base64"] = None
                
            # 2. STRATEGIC DEFAULTS
            current_band_val = data.get("current_band")
            if not current_band_val:
                current_band_val = "Unranked"
                data["current_band"] = current_band_val
                
            if not data.get("ranking_history"):
                data["ranking_history"] = "Stagnation"
                
            # 3. DYNAMIC TARGET BAND CALCULATION
            cb_lower = str(current_band_val).lower()
            if "unranked" in cb_lower or "no rank" in cb_lower:
                data["target_band"] = "Band 5" # Entry level target
            else:
                match = re.search(r'\d+', current_band_val)
                if match:
                    current_num = int(match.group())
                    if current_num > 1:
                        data["target_band"] = f"Band {current_num - 1}"
                    else:
                        data["target_band"] = "Band 1" 
                else:
                    data["target_band"] = current_band_val 

            # 4. Clean remaining nulls
            for k, v in data.items():
                if v is None and k not in ["file_base64", "current_band", "target_band", "ranking_history"]:
                    data[k] = ""
                    
        return data

class AgentState(BaseModel):
    submission_id: str = ""
    target_submission_type: Optional[str] = None
    input_document_type: Optional[str] = None
    metadata: Optional[MetaData] = None
    
    base64_documents: List[Dict[str, str]] = Field(default_factory=list)
    decoded_file_paths: List[str] = Field(default_factory=list)
    raw_text: str = "" 
    extracted_text: Optional[str] = None 
    output_base64: Optional[str] = None
    
    submission: Optional[BaseSubmission] = None
    gaps: List[Dict[str, Any]] = Field(default_factory=list) 
    dismissed_gaps: List[str] = Field(default_factory=list)
    new_answer: Dict[str, Any] = Field(default_factory=dict) 
    questions: List[str] = Field(default_factory=list)
    
    positioning_core: Optional[PositioningCore] = None
    positioning_tier: Optional[PositioningTier] = None
    blind_spots: List[BlindSpot] = Field(default_factory=list)
    competitive_advantage: List[str] = Field(default_factory=list)
    evolution_path: List[Milestone] = Field(default_factory=list)
    executive_summary: Optional[ExecutiveSummary] = None
    
    lawyer_profiles: List[B9LawyerProfile] = Field(
        default_factory=list, 
        description="The extracted, evaluated, and optimized B9 lawyer profiles."
    )

    history: List[str] = Field(default_factory=list)
    messages: Annotated[list, operator.add] = Field(default_factory=list)
    current_step: Union[str, int] = "" 
    next_node: str = "" 
    errors: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)

    strategic_context: Dict[str, Any] = Field(default_factory=dict)
    ui_audit_options: List[Dict[str, Any]] = Field(default_factory=list)

    @field_validator("target_submission_type", mode="before")
    @classmethod
    def normalize_submission_type(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        cleaned = value.lower().replace(" ", "").replace("-", "").replace("_", "")
        
        if "matters" in cleaned and "assistant" in cleaned:
            return "MattersAssistant"
        if "legal" in cleaned and "500" in cleaned:
            return "Legal500"
        if "chambers" in cleaned:
            return "Chambers"
        if "leaders" in cleaned and "league" in cleaned:
            return "LeadersLeague"
        return value.capitalize()
    
    @field_validator("submission", mode="before")
    @classmethod
    def sanitize_php_garbage(cls, v: Optional[Any]) -> Optional[Any]:
        if isinstance(v, dict):
            buggy_fields = ["narratives", "individual_nominations", "team_dynamics"]
            for field in buggy_fields:
                if field in v and isinstance(v[field], dict) and "stdClass" in v[field]:
                    v[field] = {}
        return v

    @field_validator("new_answer", mode="before")
    @classmethod
    def sanitize_new_answer(cls, v: Any) -> Dict[str, str]:
        default = {"target_field": "", "question_text": "", "answer": ""}
        if not isinstance(v, dict):
            return default
        return {
            "target_field": str(v.get("target_field") or ""),
            "question_text": str(v.get("question_text") or ""),
            "answer": str(v.get("answer") or "")
        }

    @model_validator(mode="after")
    def serialize_lawyer_profiles(self):
        if self.lawyer_profiles:
            serialized_profiles = []
            for profile in self.lawyer_profiles:
                if hasattr(profile, "model_dump"):
                    serialized_profiles.append(profile.model_dump())
                elif isinstance(profile, dict):
                    serialized_profiles.append(profile)
            self.lawyer_profiles = serialized_profiles # type: ignore
        return self