from langgraph.graph import StateGraph, END
from typing import Literal

from src.core.state import AgentState

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

# --- ACTO 1.5: Strategic Analysis (NUEVO) ---
from src.agents.taxonomy import taxonomy_node
from src.agents.rubric_evaluator import rubric_evaluator_node, final_evaluation_node

# --- ACTO 2: Pulido y Ensamblaje ---
from src.agents.optimizer import optimize_node 
from src.agents.assembler import assembly_node

# --- ACTO 3: Diagnóstico Estratégico (RankPilot Engine) ---
from src.agents.snapshot_generator import snapshot_generator_node
from src.agents.executive_writer import executive_writer_node

def route_entry(state: AgentState) -> Literal["process_answer_node", "classification_node"]:
    """
    Ruteo de entrada:
    Si hay una respuesta del usuario, entramos a evaluar esa respuesta.
    Si es un inicio en frío, vamos a clasificar y extraer el PDF.
    """
    new_answer = getattr(state, "new_answer", {}) or {}
    if new_answer.get("answer"):
        return "process_answer_node"
    return "classification_node"

def route_after_audit(state: AgentState) -> str:
    """
    The Master Traffic Controller.
    Decides the next node based on gaps, tactical commands, and analysis status.
    """
    gaps = getattr(state, "gaps", [])
    
    # 🧠 THE SAFE FIX: Read from dictionary
    ctx = getattr(state, "strategic_context", {})
    trigger_analysis = ctx.get("trigger_analysis", False)
    is_analyzed = ctx.get("is_strategically_analyzed", False)

    # 1. THE EXPLICIT COMMAND
    if trigger_analysis:
        print("🚦 ROUTING: Tactical command received. Routing to Strategic Analysis.")
        return "taxonomy_node"

    # 2. THE AUTO-TRIGGER
    if len(gaps) == 0 and not is_analyzed:
        print("🚦 ROUTING: 0 Structural gaps found. Auto-triggering Strategic Analysis.")
        return "taxonomy_node"

    # 3. THE GAPS EXIST
    if len(gaps) > 0:
        print(f"🚦 ROUTING: {len(gaps)} gaps remain. Routing to Interrogator.")
        return "interrogator_node"

    # 4. THE FINISH LINE
    if len(gaps) == 0 and is_analyzed:
        print("🚦 ROUTING: 0 gaps and analysis complete. Advancing to Act 2 (Optimization).")
        return "optimize_node"

    # Fallback safety
    return "interrogator_node"

def route_after_classification(state: AgentState) -> Literal["chambers_ingestion_node", "legal500_ingestion_node", "generic_ingestion_node"]:
    doc_type = getattr(state, "input_document_type", "unknown_draft")
    
    metadata = getattr(state, "metadata", None)
    target_directory = ""
    if metadata:
        target_directory = str(getattr(metadata, "directory", "") or "").lower()

    print(f"\n--- DEBUG ROUTER ---")
    print(f"🤖 IA DETECTÓ (doc_type): '{doc_type}'")
    print(f"👤 USUARIO ELIGIÓ (target_directory): '{target_directory}'")
    print(f"--------------------\n")

    if doc_type == "chambers_submission" and "chambers" in target_directory:
        return "chambers_ingestion_node"
    elif doc_type == "legal500_submission" and ("legal" in target_directory or "500" in target_directory):
        return "legal500_ingestion_node"

    return "generic_ingestion_node"

def build_workflow() -> StateGraph:
    """
    Construye la máquina de estados LangGraph (Arquitectura de 3 Actos).
    """
    workflow = StateGraph(AgentState)

    # ------------------------------------------
    # REGISTRO DE NODOS
    # ------------------------------------------
    # Acto 1
    workflow.add_node("classification_node", classification_node)
    workflow.add_node("chambers_ingestion_node", chambers_ingestion_node)
    workflow.add_node("legal500_ingestion_node", legal500_ingestion_node)
    workflow.add_node("generic_ingestion_node", ingestion_node)
    workflow.add_node("process_answer_node", process_answer_node)
    workflow.add_node("sanitizer_node", sanitizer_node)
    workflow.add_node("audit_node", audit_node)
    workflow.add_node("interrogator_node", interrogator_node)
    
    # Acto 1.5 (Strategic Analysis)
    workflow.add_node("taxonomy_node", taxonomy_node)
    workflow.add_node("rubric_evaluator_node", rubric_evaluator_node)
    
    # Acto 2
    workflow.add_node("optimize_node", optimize_node)
    workflow.add_node("final_evaluation_node", final_evaluation_node)
    workflow.add_node("assembly_node", assembly_node)
    
    # Acto 3
    workflow.add_node("snapshot_generator_node", snapshot_generator_node)
    workflow.add_node("scheduler_node", scheduler_node)
    workflow.add_node("executive_writer_node", executive_writer_node)

    # ------------------------------------------
    # DEFINICIÓN DE ARISTAS (EDGES) Y FLUJO
    # ------------------------------------------
    
    # PUNTO DE ENTRADA
    workflow.set_conditional_entry_point(
        route_entry,
        {
            "process_answer_node": "process_answer_node",
            "classification_node": "classification_node"
        }
    )

    # --- ACTO 1: EL BUCLE DE CAPTURA ---
    workflow.add_conditional_edges(
        "classification_node",
        route_after_classification,
        {
            "chambers_ingestion_node": "chambers_ingestion_node",
            "legal500_ingestion_node": "legal500_ingestion_node",
            "generic_ingestion_node": "generic_ingestion_node"
        }
    )

    workflow.add_edge("chambers_ingestion_node", "sanitizer_node")
    workflow.add_edge("legal500_ingestion_node", "sanitizer_node")
    workflow.add_edge("generic_ingestion_node", "sanitizer_node")
    
    workflow.add_edge("process_answer_node", "sanitizer_node")
    workflow.add_edge("sanitizer_node", "audit_node")

    # Condicional: ¿Preguntamos, analizamos, o pasamos a optimizar?
    workflow.add_conditional_edges(
        "audit_node",
        route_after_audit,
        {
            "interrogator_node": "interrogator_node",  # Pausa el grafo para Input
            "taxonomy_node": "taxonomy_node",          # Entra a fase estratégica
            "optimize_node": "optimize_node"           # Avanza al Acto 2
        }
    )
    workflow.add_edge("interrogator_node", END) 

    # --- ACTO 1.5: DIAGNÓSTICO ESTRATÉGICO ---
    # Una vez que entra a Taxonomía, pasa a Rúbrica, y vuelve al Auditor para recalcular gaps
    workflow.add_edge("taxonomy_node", "rubric_evaluator_node")
    workflow.add_edge("rubric_evaluator_node", "audit_node")

    # --- ACTO 2: GHOSTWRITER Y ENSAMBLAJE ---
    workflow.add_edge("optimize_node", "final_evaluation_node") # 👈 UPDATED
    workflow.add_edge("final_evaluation_node", "assembly_node")
    workflow.add_edge("assembly_node", "snapshot_generator_node")
    workflow.add_edge("snapshot_generator_node", "scheduler_node")

    # --- ACTO 3: REPORTE FINAL ---
    workflow.add_edge("scheduler_node", "executive_writer_node")
    workflow.add_edge("executive_writer_node", END)

    return workflow.compile()