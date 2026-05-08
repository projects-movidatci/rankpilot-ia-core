from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import traceback
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import ChambersSubmission

def chambers_ingestion_node(state: AgentState) -> dict:
    updates = {"current_step": "chambers_ingestion", "messages": []}
    
    # 1. Recuperar el texto crudo
    raw_text = getattr(state, "extracted_text", "") or ""
    
    # 🕵️ LOG DE EMERGENCIA: ¿Hay texto?
    if not raw_text.strip():
        print("❌ ERROR CRÍTICO: El nodo Chambers recibió texto VACÍO.")
        updates["messages"].append("⚠️ Chambers Ingestion Aborted: No raw text.")
        return updates

    # 🕵️ Muestra los primeros 500 caracteres en consola para verificar el parsing
    print(f"\n--- [DEBUG] INICIO DEL TEXTO EN CHAMBERS NODE ---\n{raw_text[:500]}\n---")

    llm = get_llm(temperature=0)
    structured_llm = llm.with_structured_output(ChambersSubmission)
    
    # 2. Prompt con "Detección de Tablas Rotas"
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert legal data extraction AI specialized in Chambers and Partners.\n"
            "The user document is a Chambers submission, but the table structure might be flattened or messy.\n\n"
            "SPECIFIC INSTRUCTIONS FOR TABLE HEADERS:\n"
            "- Look for 'Department Head(s)' or 'Head or Heads of department'. Even if the tag is B4, B7, or missing, extract the Name, Email, and Phone.\n"
            "- If you see a line like 'Jorge Labastida jlabastida@pcga.mx +52...', identify 'Jorge Labastida' as the name and the rest as contact info.\n"
            "- Map the 'Department Overview' or 'Best Known For' even if the tag is not B10.\n"
            "- Be flexible with regional variations (USA vs LatAm)."
        )),
        ("user", "Extract data from this text:\n\n{text}")
    ])
    
    chain = prompt | structured_llm
    
    try:
        # 🕵️ Mensaje distintivo para confirmar que ESTAMOS en este nodo
        updates["messages"].append("🚀 EJECUTANDO: chambers_ingestion_node (Modo 1:1 Activo)")
        print("🚀 Ejecutando extracción 1:1 en Chambers Node...")

        extracted_data = chain.invoke({"text": raw_text})
        
        updates["submission"] = extracted_data
        updates["messages"].append("✅ Chambers Ingestion Success.")
        
    except Exception as e:
        error_trace = traceback.format_exc()
        updates["messages"].append(f"❌ Chambers Ingestion Error: {str(e)}")
        print(f"Detalle del error:\n{error_trace}")

    return updates