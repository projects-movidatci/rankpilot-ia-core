from langgraph.graph import StateGraph, END
from typing import Literal

from src.core.state import AgentState

# --- ACTO 0: Matters Assistant (NUEVO) ---
from src.agents.MA_ingestion_node import matters_assistant_ingestion_node
from src.agents.MA_extractor_node import matters_assistant_extractor_node

# --- ACTO 1: Captura de Datos (Submissions Core) ---
from src.agents.extractor import ingestion_node
from src.agents.classifier import classification_node
from src.agents.sanitizer import sanitizer_node
from src.agents.auditor import audit_node
from src.agents.interrogator import interrogator_node
from src.agents.answer_evaluator import process_answer_node 
from src.agents.scheduler import scheduler_node
from src.agents.chambers_ingestion import chambers_ingestion_node
from src.agents.legal500_ingestion import legal500_ingestion_node

# --- ACTO 1.5: Strategic Analysis ---
from src.agents.taxonomy import taxonomy_node
from src.agents.rubric_evaluator import rubric_evaluator_node, final_evaluation_node

# --- ACTO 2: Pulido y Ensamblaje ---
from src.agents.optimizer import optimize_node, matters_assistant_optimize_node
from src.agents.assembler import assembly_node

# 👇 NUEVAS IMPORTACIONES: MÓDULO DE BENCH STRENGTH 👇
from src.agents.b9_evaluator import b9_extraction_node
from src.agents.lawyer_evaluator import lawyer_evaluation_node
from src.agents.b9_optimizer import b9_optimization_node
# 👆 ============================================== 👆

# --- ACTO 3: Diagnóstico Estratégico (RankPilot Engine) ---
from src.agents.snapshot_generator import snapshot_generator_node
from src.agents.executive_writer import executive_writer_node

def route_entry(state: AgentState) -> str:
    if isinstance(state, dict):
        new_answer = state.get("new_answer", {}) or {}
        target = state.get("target_submission_type", "")
    else:
        new_answer = getattr(state, "new_answer", {}) or {}
        target = getattr(state, "target_submission_type", "")
        
    target_field = new_answer.get("target_field", "")
    answer_text = new_answer.get("answer", "")

    # 👇 THE NEW BYPASS COMMAND 👇
    if target_field == "COMMAND:GENERATE":
        return "MA_optimize_node" if target == "MattersAssistant" else "optimize_node"

    # Si es una señal de categoría desde la UI, ir directo al Interrogador
    if target_field.startswith("category:"):
        return "interrogator_node"
    
    # Si hay una respuesta real del usuario, procesar la respuesta
    if answer_text:
        return "process_answer_node"
        
    # Flujo inicial (Documento en blanco o nuevo upload)
    return "classification_node"

def route_after_audit(state: AgentState) -> str:
    gaps = getattr(state, "gaps", [])
    target = getattr(state, "target_submission_type", "")

    # If there are gaps (either structural or strategic), pause the system.
    if len(gaps) > 0:
        return "interrogator_node"
    
    # If there are 0 gaps, proceed directly to optimization (Ghostwriting)
    if target == "MattersAssistant":
        return "MA_optimize_node" 

    return "optimize_node"

def route_after_classification(state: AgentState) -> Literal["chambers_ingestion_node", "legal500_ingestion_node", "generic_ingestion_node", "MA_ingestion_node"]:
    doc_type = getattr(state, "input_document_type", "unknown_draft")
    metadata = getattr(state, "metadata", None)
    target_directory = str(getattr(metadata, "directory", "") or "").lower() if metadata else ""

    if doc_type == "raw_batch":
        return "MA_ingestion_node"

    if doc_type == "chambers_submission" and "chambers" in target_directory:
        return "chambers_ingestion_node"
    elif doc_type == "legal500_submission" and ("legal" in target_directory or "500" in target_directory):
        return "legal500_ingestion_node"

    return "generic_ingestion_node"

def route_after_sanitizer(state: AgentState) -> str:
    """
    Decide si el flujo debe pasar por el análisis estratégico pesado (Taxonomía y Rúbrica)
    o si puede saltar directamente a la auditoría.
    """
    # 🛡️ FIX: Compatibilidad con diccionarios
    if isinstance(state, dict):
        new_answer = state.get("new_answer", {}) or {}
    else:
        new_answer = getattr(state, "new_answer", {}) or {}
    
    # Fast-track: Si hay una respuesta activa, saltar la evaluación
    if new_answer.get("answer", "").strip():
        return "audit_node"
        
    # Si es un documento nuevo, seguir el camino largo
    return "taxonomy_node"

def build_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)

    # ------------------------------------------
    # REGISTRO DE NODOS
    # ------------------------------------------
    workflow.add_node("MA_ingestion_node", matters_assistant_ingestion_node)
    workflow.add_node("MA_extractor_node", matters_assistant_extractor_node)
    workflow.add_node("classification_node", classification_node)
    workflow.add_node("chambers_ingestion_node", chambers_ingestion_node)
    workflow.add_node("legal500_ingestion_node", legal500_ingestion_node)
    workflow.add_node("generic_ingestion_node", ingestion_node)
    workflow.add_node("process_answer_node", process_answer_node)
    workflow.add_node("sanitizer_node", sanitizer_node)
    workflow.add_node("audit_node", audit_node)
    workflow.add_node("interrogator_node", interrogator_node)
    workflow.add_node("taxonomy_node", taxonomy_node)
    workflow.add_node("rubric_evaluator_node", rubric_evaluator_node)
    
    workflow.add_node("optimize_node", optimize_node)
    workflow.add_node("MA_optimize_node", matters_assistant_optimize_node)
    workflow.add_node("final_evaluation_node", final_evaluation_node)
    
    # 👇 NUEVOS NODOS EN EL GRAFO 👇
    workflow.add_node("b9_extraction_node", b9_extraction_node)
    workflow.add_node("lawyer_evaluation_node", lawyer_evaluation_node)
    workflow.add_node("b9_optimization_node", b9_optimization_node)
    # 👆 ======================= 👆

    workflow.add_node("assembly_node", assembly_node)
    workflow.add_node("snapshot_generator_node", snapshot_generator_node)
    workflow.add_node("scheduler_node", scheduler_node)
    workflow.add_node("executive_writer_node", executive_writer_node)

    # ------------------------------------------
    # DEFINICIÓN DE ARISTAS (EDGES) Y FLUJO
    # ------------------------------------------
    
    workflow.set_conditional_entry_point(
        route_entry,
        {
            "process_answer_node": "process_answer_node",
            "classification_node": "classification_node",
            "interrogator_node": "interrogator_node",
            "optimize_node": "optimize_node",        # 👈 NEW FAST-TRACK
            "MA_optimize_node": "MA_optimize_node"   # 👈 NEW FAST-TRACK
        }
    )

    workflow.add_conditional_edges(
        "classification_node",
        route_after_classification,
        {
            "chambers_ingestion_node": "chambers_ingestion_node",
            "legal500_ingestion_node": "legal500_ingestion_node",
            "generic_ingestion_node": "generic_ingestion_node",
            "MA_ingestion_node": "MA_ingestion_node" 
        }
    )

    # --- ACTO 1 & 1.5: INGESTION, TAXONOMY, RUBRIC, LAWYERS, THEN AUDIT ---
    
    workflow.add_edge("chambers_ingestion_node", "sanitizer_node")
    workflow.add_edge("legal500_ingestion_node", "sanitizer_node")
    workflow.add_edge("generic_ingestion_node", "sanitizer_node")
    
    workflow.add_edge("process_answer_node", "sanitizer_node")
    
    # 🛡️ THE NEW STRICTLY LINEAR STRATEGIC FLOW
    workflow.add_conditional_edges(
        "sanitizer_node",
        route_after_sanitizer,
        {
            "audit_node": "audit_node",
            "taxonomy_node": "taxonomy_node"
        }
    )
    workflow.add_edge("taxonomy_node", "rubric_evaluator_node")
    workflow.add_edge("rubric_evaluator_node", "b9_extraction_node")
    workflow.add_edge("b9_extraction_node", "lawyer_evaluation_node")
    
    # This is the ONLY exit from lawyer_evaluation now. No parallel forks!
    workflow.add_edge("lawyer_evaluation_node", "audit_node") 

    # MA extraction bypasses taxonomy (single matter rules)
    workflow.add_edge("MA_ingestion_node", "MA_extractor_node")
    workflow.add_edge("MA_extractor_node", "audit_node")

    # The router decides if we pause for Laravel or keep going
    workflow.add_conditional_edges(
        "audit_node",
        route_after_audit,
        {
            "interrogator_node": "interrogator_node", 
            "optimize_node": "optimize_node",         
            "MA_optimize_node": "MA_optimize_node"
        }
    )
    
    # The system pauses here and waits for the frontend
    workflow.add_edge("interrogator_node", END) 

    # --- ACTO 2: GHOSTWRITER Y ENSAMBLAJE ---
    workflow.add_edge("MA_optimize_node", "assembly_node")
    workflow.add_edge("optimize_node", "final_evaluation_node")
    
    # 👇 THE B9 OPTIMIZATION FLOW (Strictly isolated in Act 2) 👇
    workflow.add_edge("final_evaluation_node", "b9_optimization_node")
    workflow.add_edge("b9_optimization_node", "assembly_node")
    # 👆 ================================================== 👆
    
    # --- ACTO 3: EXECUTIVE REPORTING ---
    workflow.add_edge("assembly_node", "snapshot_generator_node")
    workflow.add_edge("snapshot_generator_node", "scheduler_node")
    workflow.add_edge("scheduler_node", "executive_writer_node")
    workflow.add_edge("executive_writer_node", END)

    return workflow.compile()