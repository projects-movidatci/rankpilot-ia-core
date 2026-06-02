from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import traceback
import uuid
import sys
from src.core.workflow import build_workflow
from src.core.state import AgentState, MetaData
from src.core.schemas import Legal500Submission, ChambersSubmission, SingleMatterExtraction

api = FastAPI(title="RankPilot API")

# --- BASE DE DATOS EN MEMORIA (Para el Polling) ---
# Almacena el progreso de los trabajos. (En producción masiva se cambiaría por Redis)
JOBS_DB = {}

# 1. Estructura del Payload
class AgentStatePayload(BaseModel):
    submission_id: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = None 
    base64_documents: List[Dict[str, str]] = []
    decoded_file_paths: List[str] = []
    raw_input_text: str = ""
    target_submission_type: Optional[str] = "Legal500"
    input_document_type: Optional[str] = None
    submission: Optional[Dict[str, Any]] = None
    gaps: List[Dict[str, Any]] = []
    dismissed_gaps: List[str] = []
    questions: List[str] = []
    history: List[str] = []
    new_answer: Dict[str, Any] = {"target_field": "", "question_text": "", "answer": ""}
    output_base64: Optional[str] = None
    messages: List[str] = []
    current_step: str = ""
    errors: List[str] = []
    strategic_context: Dict[str, Any] = {}
    lawyer_profiles: List[Dict[str, Any]] = []
    positioning_core: Dict[str, Any] = {}
    positioning_tier: Dict[str, Any] = {}
    executive_summary: Dict[str, Any] = {}

# --- 2. EL WORKER EN SEGUNDO PLANO (La magia de LangGraph) ---
def run_workflow_task(job_id: str, initial_state: dict, config: dict):
    try:
        workflow = build_workflow()
        JOBS_DB[job_id]["status"] = "processing"
        
        # Mapeo visual de progreso basado en los nodos de LangGraph
        progress_map = {
            # --- ACTO 1 (The Intake & Audit Loop) ---
            "classification_node": {"p": 5, "msg": "Extracting and classifying document..."},
            "process_answer_node": {"p": 10, "msg": "Integrating Partner's strategic input..."},
            
            # Ingestion Nodes
            "chambers_ingestion_node": {"p": 15, "msg": "Mapping Chambers raw data to universal schema..."},
            "legal500_ingestion_node": {"p": 15, "msg": "Mapping Legal 500 raw data to universal schema..."},
            "generic_ingestion_node": {"p": 15, "msg": "Mapping raw data to universal schema..."},
            
            "sanitizer_node": {"p": 25, "msg": "Sanitizing preliminary narrative..."},
            
            # --- ACTO 1.5 (Strategic Diagnosis) ---
            "taxonomy_node": {"p": 40, "msg": "Performing strategic taxonomy and complexity analysis..."},
            "rubric_evaluator_node": {"p": 55, "msg": "Scoring matters against the 100-point rubric..."},
            
            "audit_node": {"p": 70, "msg": "Auditing submission for strategic gaps..."},
            "interrogator_node": {"p": 100, "msg": "Audit paused. Ready for Q&A."}, # Pauses the system for Laravel
            
            # --- ACTO 2 y 3 (The Ghostwriter & Executive Assembly) ---
            # If 0 gaps, it flows directly from Audit (70%) to Optimize (80%)
            "optimize_node": {"p": 80, "msg": "Ghostwriting and optimizing matter narratives..."},
            "final_evaluation_node": {"p": 83, "msg": "Final evaluation of matter scores..."},
            "assembly_node": {"p": 86, "msg": "Assembling the final structured document..."},
            "snapshot_generator_node": {"p": 90, "msg": "Generating strategic intelligence snapshot..."},
            "scheduler_node": {"p": 95, "msg": "Building roadmap and evolution timeline..."},
            "executive_writer_node": {"p": 100, "msg": "Drafting final executive letter..."}
        }

        # Ejecutamos con .stream() para ir nodo por nodo
        final_state = initial_state
        for output in workflow.stream(initial_state, config):
            for node_name, state_update in output.items():
                # Acumulamos el estado
                final_state.update(state_update)
                
                # Actualizamos el porcentaje visual para Laravel
                if node_name in progress_map:
                    JOBS_DB[job_id]["progress"] = progress_map[node_name]["p"]
                    JOBS_DB[job_id]["message"] = progress_map[node_name]["msg"]
                else:
                    JOBS_DB[job_id]["message"] = f"Processing {node_name}..."

        # Helper para garantizar serialización JSON segura
        def safe_dump(obj):
            if hasattr(obj, 'model_dump'):
                return obj.model_dump(exclude_none=True)
            if isinstance(obj, list):
                return [safe_dump(i) for i in obj]
            return obj

        # Al terminar, preparamos el JSON final para enviar a Laravel
        sub = final_state.get("submission")
        sub_dict = sub.model_dump() if hasattr(sub, 'model_dump') else None
        
        # Opcional: Extraer el Executive Summary si existe (Acto 3)
        exec_summary = final_state.get("executive_summary")
        exec_summary_dict = exec_summary.model_dump() if hasattr(exec_summary, 'model_dump') else exec_summary
        
        metadata_obj = final_state.get("metadata")
        if hasattr(metadata_obj, 'model_dump'):
            metadata_final = metadata_obj.model_dump()
        elif isinstance(metadata_obj, dict):
            metadata_final = metadata_obj
        else:
            metadata_final = {}

        # 👇 THE FIX: Safe extraction using 'or {}' to prevent NoneType attribute errors 👇
        pub_info = sub_dict.get("D_publishable_information") or {}
        pub_matters = pub_info.get("publishable_matters", []) if isinstance(pub_info, dict) else []
        
        conf_info = sub_dict.get("E_confidential_information") or {}
        conf_matters = conf_info.get("confidential_matters", []) if isinstance(conf_info, dict) else []
        
        prelim_info = sub_dict.get("A_preliminary_information") or {}
        referees = prelim_info.get("A4_contact_persons", []) if isinstance(prelim_info, dict) else []
        
        total_matters = len(pub_matters) + len(conf_matters)
        
        positioning = final_state.get("positioning_core", {})
        confidence = positioning.get("confidence_score", 0) if isinstance(positioning, dict) else getattr(positioning, "confidence_score", 0)

        ui_context_snapshot = {
            "firm_name": metadata_final.get("firm_name", "Unknown Firm"),
            "current_band": metadata_final.get("current_band", "Unknown"),
            "target_band": metadata_final.get("target_band", "Unknown"),
            "matters_count": total_matters,
            "referees_count": len(referees) if referees else 0,
            "lawyers_count": len(final_state.get("lawyer_profiles", [])),
            "initial_confidence": confidence,
            "audit_room_options": final_state.get("ui_audit_options", []) 
        }

        final_agent_state = {
            "submission_id": final_state.get("submission_id"),
            "next_node": final_state.get("next_node"),
            "metadata": metadata_final,
            "submission": sub_dict,
            "gaps": final_state.get("gaps", []),
            "dismissed_gaps": final_state.get("dismissed_gaps", []),
            "questions": final_state.get("questions", []),
            "new_answer": final_state.get("new_answer", {}),
            "output_base64": final_state.get("output_base64"),
            "evolution_path": final_state.get("evolution_path", []),
            "executive_summary": exec_summary_dict,
            "errors": final_state.get("errors", []),
            # 🛡️ THE FIX: Send the tactical flags back to the frontend
            "strategic_context": final_state.get("strategic_context", {}),
            "positioning_core": safe_dump(final_state.get("positioning_core", {})),
            "positioning_tier": safe_dump(final_state.get("positioning_tier", {})),
            "blind_spots": safe_dump(final_state.get("blind_spots", [])),
            "competitive_advantage": safe_dump(final_state.get("competitive_advantage", [])),
            "lawyer_profiles": safe_dump(final_state.get("lawyer_profiles", [])),
            "ui_context_snapshot": ui_context_snapshot
        }

        JOBS_DB[job_id]["progress"] = 100
        JOBS_DB[job_id]["status"] = "completed"
        JOBS_DB[job_id]["data"] = final_agent_state

    except Exception as e:
        print(f"CRITICAL WORKER ERROR: {str(e)}")
        traceback.print_exc()
        JOBS_DB[job_id]["status"] = "failed"
        JOBS_DB[job_id]["message"] = f"Error: {str(e)}"
        JOBS_DB[job_id]["error_details"] = traceback.format_exc()

# --- 3. ENDPOINT INICIAL: Dispara el proceso ---
@api.post("/process")
async def process_documents(request: Request, background_tasks: BackgroundTasks):
    try:
        raw_data = await request.json()
        thread_id = raw_data.get("thread_id", str(uuid.uuid4()))
        state_data = raw_data.get("agent_state", {})
        
        # Limpieza de basura PHP
        submission_data = state_data.get("submission", {})
        if isinstance(submission_data, dict):
            buggy_fields = ["narratives", "individual_nominations", "team_dynamics"]
            for field in buggy_fields:
                val = submission_data.get(field)
                if isinstance(val, dict) and ("stdClass" in val or not val):
                    submission_data[field] = {}
                elif val is None:
                    submission_data[field] = {}

        state_input = AgentStatePayload(**state_data)
        
        sub_model = None
        if submission_data:
            target = state_input.target_submission_type
            if target == "Legal500":
                sub_model = Legal500Submission(**submission_data)
            elif target in ["Chambers", "Chambers and Partners"]:
                sub_model = ChambersSubmission(**submission_data)
            elif target == "MattersAssistant":  # 👈 THE MISSING DOOR
                sub_model = SingleMatterExtraction(**submission_data)
                

        # Parseo de Metadata
        raw_metadata = state_data.get("metadata", {})
        if raw_metadata is None:
            raw_metadata = {}
            
        # 🧹 SANITIZADOR PREVENTIVO: Evitar que Pydantic colapse al intentar validar un archivo vacío
        if "file_base64" in raw_metadata and not raw_metadata.get("file_base64"):
            del raw_metadata["file_base64"]
        try:
            # 🛡️ THE FIX: Extraemos a diccionario limpio
            meta_obj = MetaData(**raw_metadata)
            meta_input = meta_obj.model_dump(exclude_none=True)
        except Exception as e:
            print(f"⚠️ Error construyendo MetaData object: {e}")
            # 🚑 EL SALVAVIDAS: Si Pydantic falla, pasamos el diccionario crudo. ¡NUNCA None!
            meta_input = raw_metadata

        initial_state = {
            "submission_id": state_input.submission_id,
            "metadata": meta_input,
            "base64_documents": state_input.base64_documents,
            "target_submission_type": state_input.target_submission_type,
            "input_document_type": state_input.input_document_type,
            "raw_text": state_input.raw_input_text, 
            "extracted_text": state_input.raw_input_text, 
            "submission": sub_model,
            "gaps": state_input.gaps,
            "dismissed_gaps": state_input.dismissed_gaps,
            "new_answer": state_input.new_answer,
            "errors": state_input.errors,
            # 🛡️ THE FIX: Pass the context into LangGraph
            "strategic_context": state_input.strategic_context,
            "lawyer_profiles": state_input.lawyer_profiles,
            "ui_audit_options": getattr(state_input, "ui_context_snapshot", {}).get("audit_room_options", []),
            "positioning_core": state_input.positioning_core,
            "positioning_tier": state_input.positioning_tier,
            "executive_summary": state_input.executive_summary
        }
        config = {"configurable": {"thread_id": thread_id}}

        # Creamos el Job
        job_id = str(uuid.uuid4())
        JOBS_DB[job_id] = {
            "status": "started", 
            "progress": 0, 
            "message": "Initializing...", 
            "data": None
        }

        # Despachamos al fondo
        background_tasks.add_task(run_workflow_task, job_id, initial_state, config)

        # Devolvemos INMEDIATAMENTE
        return {"job_id": job_id, "status": "started", "thread_id": thread_id}

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "failed", "error": str(e)})

# --- 4. ENDPOINT DE POLLING: Laravel pregunta por este ---
@api.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in JOBS_DB:
        return JSONResponse(status_code=404, content={"error": "Job not found or expired."})
    return JOBS_DB[job_id]