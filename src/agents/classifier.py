import os
import yaml
import traceback
from typing import Literal
from pydantic import BaseModel, Field

from src.core.state import AgentState
from src.io.base64_handler import decode_base64_document
from src.io.pdf_parser import extract_text_from_pdf
from src.io.docx_manager import extract_text_from_docx
from src.core.llm import get_llm
from src.io.strategy_selector import get_config_path

# Importamos LangChain para la clasificación
from langchain_core.prompts import ChatPromptTemplate

# =========================================================
# ESQUEMA PYDANTIC PARA CLASIFICACIÓN 1:1
# =========================================================
class DocumentClassification(BaseModel):
    document_type: Literal[
        "chambers_submission", 
        "legal500_submission", 
        "leadersleague_submission", 
        "unknown_draft"
    ] = Field(
        description="Identifica el tipo de documento de directorio legal basado en sus etiquetas, títulos o estructura."
    )
    confidence_score: float = Field(
        description="Nivel de confianza en esta clasificación, de 0.0 a 1.0."
    )

def classification_node(state: AgentState) -> dict:
    """
    Preparation Node (Formerly Classification):
    Extracts raw text from Laravel and uploaded documents, then classifies
    the actual document type using an LLM to prevent formatting mismatches.
    """
    updates = {"current_step": "preparation", "messages": []}

    updates["messages"].append("ALERTA ROJA: ESTOY LEYENDO EL NUEVO CODIGO CON CLASIFICADOR IA")

    decoded_file_paths = getattr(state, "decoded_file_paths", []) or []
    b64_docs = getattr(state, "base64_documents", [])
    extracted_text = getattr(state, "extracted_text", "") or ""
    metadata = getattr(state, "metadata", {}) or {}
    current_target = getattr(state, "target_submission_type", None)
    print(f"Preparation Node: Initial metadata state: {metadata}")

    # =========================================================
    # 🛡️ THE FIX: MATTERS ASSISTANT BYPASS (ACT 0)
    # =========================================================
    if current_target.lower() in ["mattersassistant", "matter_assistant", "matterassistant"]:
        updates["messages"].append("Preparation node: Matters Assistant detected. Bypassing standard LLM classification.")
        
        # Set a unique document type so the router knows exactly where to send it
        updates["input_document_type"] = "raw_batch"
        
        # Load the dedicated single-matter YAML config directly
        try:
            config_path = "configs/chambers_matter.yaml" 
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    yaml_config = yaml.safe_load(f)
                    updates["config"] = yaml_config or {}
                    updates["messages"].append(f"Preparation node: Loaded config {config_path}")
            else:
                updates["messages"].append(f"⚠️ Warning: {config_path} not found.")
                updates["config"] = {}
        except Exception as e:
            print(f"❌ Error loading Matters Assistant YAML: {e}")
            updates["config"] = {}
            
        # Return immediately! Skip the rest of the node.
        return updates
    
    if extracted_text.strip():
        updates["messages"].append("Preparation node: Successfully received raw text from Laravel.")

    # 2. Decode Base64 documents to the hard drive
    if b64_docs:
        for doc in b64_docs:
            filename = doc.get("filename", "")
            b64_string = doc.get("base64", "")
            if filename and b64_string:
                path = decode_base64_document(b64_string, filename)
                if path:
                    if path not in decoded_file_paths:
                        decoded_file_paths.append(path)
                    updates["messages"].append(f"Preparation node: Decoded {filename} to {path}")
                else:
                    updates["messages"].append(f"Preparation node Error: Failed to decode {filename}")

    # 3. Extract text from documents and append it to the raw text
    for file_path in decoded_file_paths:
        if not file_path or not os.path.exists(file_path):
            continue

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            continue

        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            try:
                text = extract_text_from_pdf(file_path)
                if text and text.strip() != "":
                    extracted_text += f"\n--- Content from {os.path.basename(file_path)} ---\n{text}"
            except Exception as e:
                updates["messages"].append(f"Debug EXCEPTION in extract_text_from_pdf: {str(e)}")

        elif ext == '.docx':
            try:
                text = extract_text_from_docx(file_path)
                if text:
                    extracted_text += f"\n--- Content from {os.path.basename(file_path)} ---\n{text}"
            except Exception as e:
                updates["messages"].append(f"Debug EXCEPTION in extract_text_from_docx: {str(e)}")

    updates["decoded_file_paths"] = decoded_file_paths
    updates["extracted_text"] = extracted_text
    updates["messages"].append(f"Extraction complete. Total length: {len(extracted_text)} chars.") 

    # =========================================================
    # DEBUG: CLASIFICACIÓN CON VISIBILIDAD MEJORADA
    # =========================================================
    if extracted_text.strip():
        # Aumentamos a 8000 caracteres porque las portadas de firmas 
        # suelen tener mucho texto legal antes de las etiquetas B4/B7
        text_excerpt = extracted_text[:500] 
        
        # LOG DE CONSOLA: Para que veas qué está recibiendo la IA
        print(f"\n--- [DEBUG CLASSIFIER] TEXTO RECIBIDO (Primeros 300 chars) ---")
        print(f"{text_excerpt[:300]}...")
        print(f"-----------------------------------------------------------\n")

        try:
            llm = get_llm(temperature=0)
            structured_llm = llm.with_structured_output(DocumentClassification)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are a legal directory expert. Identify the document type by structural patterns:\n\n"
                    "- CHAMBERS: Look for tags like 'A.1', 'B.4', 'B.7', 'B.20', 'D. Publishable', 'E. Confidential'.\n"
                    "- LEGAL 500: Look for 'What sets us apart', 'Individual Nominations', 'Next Generation Partners'.\n"
                    "- LEADERS LEAGUE: Look for 'Firm Information', 'Peer Feedback', '10 Work Highlights'.\n\n"
                    "Even if B.4 is replaced by B.7, identify it as 'chambers_submission' if the context matches."
                )),
                ("user", "Classify this document:\n\n{text_excerpt}")
            ])
            
            chain = prompt | structured_llm
            res = chain.invoke({"text_excerpt": text_excerpt})
            
            # LOG DE CONSOLA: Ver el veredicto de la IA
            print(f"🤖 IA Veredicto: {res.document_type} (Confianza: {res.confidence_score})")

            # Bajamos el umbral a 0.70 para ser más tolerantes a cambios de región
            if res.confidence_score >= 0.70:
                updates["input_document_type"] = res.document_type
                updates["messages"].append(f"✅ IA identificó: {res.document_type}")
            else:
                updates["input_document_type"] = "unknown_draft"
                updates["messages"].append(f"⚠️ Baja confianza ({res.confidence_score}): unknown_draft")
                
        except Exception as e:
            print(f"❌ Error en LLM Classifier: {e}")
            updates["input_document_type"] = "unknown_draft"
    else:
        updates["input_document_type"] = "text"

    # =========================================================
    # LIMPIEZA DE METADATA Y CONFIG (YAML)
    # =========================================================
    current_target = getattr(state, "target_submission_type", None)
    if current_target:
        current_target = current_target.replace(" ", "")
    else:
        current_target = "Legal500"
    
    updates["target_submission_type"] = current_target

    # Recuperación de Guide y Configuración
    metadata = getattr(state, "metadata", {}) or {}
    guide = getattr(metadata, "guide", "") if hasattr(metadata, "guide") else metadata.get("guide", "")
    guide = str(guide).lower() if guide else ""
    
    config_path = get_config_path(current_target, guide)
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)
            updates["config"] = yaml_config or {}
            updates["messages"].append(f"Preparation node: Loaded config {config_path}")
    except Exception as e:
        print(f"❌ Error cargando YAML: {e}")
        updates["config"] = {}

    # ELIMINADO: El bloque duplicado que cargaba el YAML por segunda vez

    return updates