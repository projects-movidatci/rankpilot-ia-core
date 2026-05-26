import operator
from typing import Annotated, List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from src.core.schemas import BaseSubmission, B9LawyerProfile

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

# ==========================================
# 1. MODELOS DE RANKPILOT (Positioning & Strategy)
# ==========================================
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

    # 👇 ESTE ES EL ESCUDO CONTRA EL NULL DE LARAVEL 👇
    @model_validator(mode="before")
    @classmethod
    def sanitize_nulls_from_php(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. REGLA DE ORO: Si file_base64 viene vacío (como string "" o null), lo forzamos a None
            if "file_base64" in data and not data.get("file_base64"):
                data["file_base64"] = None
                
            # 2. Para el resto de los campos (Firma, Directorio, etc.), si son null, los hacemos ""
            for k, v in data.items():
                if v is None and k != "file_base64":
                    data[k] = ""
        return data


# ==========================================
# 2. EL SÚPER ESTADO UNIFICADO
# ==========================================
class AgentState(BaseModel):
    """
    El 'Súper Estado' que fusiona el constructor de Submissions y el RankPilot Engine.
    """
    # --- Identificación y Metadata ---
    submission_id: str = ""
    target_submission_type: Optional[str] = None
    input_document_type: Optional[str] = None
    metadata: Optional[MetaData] = None
    
    # --- Archivos y Texto Extraído ---
    base64_documents: List[Dict[str, str]] = Field(default_factory=list)
    decoded_file_paths: List[str] = Field(default_factory=list)
    raw_text: str = "" # Usado por RankPilot para el análisis
    extracted_text: Optional[str] = None # Legacy de Submissions
    output_base64: Optional[str] = None
    
    # --- El Corazón de Submissions ---
    submission: Optional[BaseSubmission] = None
    gaps: List[Dict[str, Any]] = Field(default_factory=list) # Formato dict para dot-notation
    dismissed_gaps: List[str] = Field(default_factory=list)
    new_answer: Dict[str, Any] = Field(default_factory=dict) # Protegido por el Null Killer
    questions: List[str] = Field(default_factory=list)
    
    # --- El Corazón de RankPilot ---
    positioning_core: Optional[PositioningCore] = None
    positioning_tier: Optional[PositioningTier] = None
    blind_spots: List[BlindSpot] = Field(default_factory=list)
    competitive_advantage: List[str] = Field(default_factory=list)
    evolution_path: List[Milestone] = Field(default_factory=list)
    executive_summary: Optional[ExecutiveSummary] = None
    # Evaluación de abogados al estilo B9, con optimización de perfiles:
    lawyer_profiles: List[B9LawyerProfile] = Field(
        default_factory=list, 
        description="The extracted, evaluated, and optimized B9 lawyer profiles."
    )

    # --- Trazabilidad y Logs ---
    history: List[str] = Field(default_factory=list)
    messages: Annotated[list, operator.add] = Field(default_factory=list)
    # Acepta str (Submissions) o int (RankPilot) para evitar quiebres:
    current_step: Union[str, int] = "" 
    next_node: str = "" # Usado por RankPilot para ruteo condicional
    errors: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)

    strategic_context: Dict[str, Any] = Field(default_factory=dict)

    # ==========================================
    # VALIDADORES (Los Escudos de Producción)
    # ==========================================
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
        """El Null Killer de Laravel"""
        default = {"target_field": "", "question_text": "", "answer": ""}
        if not isinstance(v, dict):
            return default
        return {
            "target_field": str(v.get("target_field") or ""),
            "question_text": str(v.get("question_text") or ""),
            "answer": str(v.get("answer") or "")
        }
    @field_validator("new_answer", mode="before")
    @classmethod
    def sanitize_new_answer(cls, v: Any) -> Dict[str, str]:
        """El Null Killer de Laravel"""
        default = {"target_field": "", "question_text": "", "answer": ""}
        if not isinstance(v, dict):
            return default
        return {
            "target_field": str(v.get("target_field") or ""),
            "question_text": str(v.get("question_text") or ""),
            "answer": str(v.get("answer") or "")
        }

    # 🛡️ THE FIX: Force serialization of lawyer profiles to survive the HTTP boundary
    @model_validator(mode="after")
    def serialize_lawyer_profiles(self):
        if self.lawyer_profiles:
            serialized_profiles = []
            for profile in self.lawyer_profiles:
                if hasattr(profile, "model_dump"):
                    # Use model_dump to convert the Pydantic object and all its nested sub-models into a dict
                    serialized_profiles.append(profile.model_dump())
                elif isinstance(profile, dict):
                    serialized_profiles.append(profile)
            
            # Reassign the raw dicts back to the field (FastAPI will accept this natively)
            # We use a type ignore here because Pydantic technically expects the B9LawyerProfile object,
            # but we are purposefully overriding it at the last millisecond before HTTP transport.
            self.lawyer_profiles = serialized_profiles # type: ignore
        return self