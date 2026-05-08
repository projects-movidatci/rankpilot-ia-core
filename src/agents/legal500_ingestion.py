from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import traceback

from src.core.state import AgentState
from src.core.schemas import Legal500Submission

def legal500_ingestion_node(state: AgentState) -> dict:
    """
    Nodo de Extracción Modular: Especializado EXCLUSIVAMENTE en Legal 500.
    Utiliza el esquema Legal500Submission para un mapeo 1:1 estricto.
    """
    updates = {"current_step": "legal500_ingestion", "messages": []}
    
    # 1. Recuperar el texto crudo del estado
    raw_text = getattr(state, "extracted_text", "") or ""
    
    if not raw_text.strip():
        updates["messages"].append("⚠️ Legal 500 Ingestion Aborted: No raw text available to extract.")
        return updates

    # 2. Configurar el LLM
    # Usamos gpt-4o para asegurar la máxima precisión en el seguimiento del esquema complejo.
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Inyectamos tu esquema Pydantic específico para Legal 500
    structured_llm = llm.with_structured_output(Legal500Submission)
    
    # 3. El Prompt Especializado para Legal 500
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert legal data extraction AI specialized in The Legal 500 submissions.\n"
            "Your task is to map the provided document into the exact Legal500 JSON schema.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. STRICT 1:1 MAPPING: Extract data exactly as it appears in the submission document. Do not invent or infer missing data.\n"
            "2. TEAM DYNAMICS & NOMINATIONS: Pay special attention to the 'Individual Nominations' section. Accurately categorize lawyers into 'Leading Partners', 'Next Generation Partners', and 'Leading Associates' based on the text.\n"
            "3. CONFIDENTIALITY: Strictly differentiate between publishable and confidential work highlights. If a matter is marked confidential, ensure it maps to the 'confidential_matters' list.\n"
            "4. NO SUMMARIZATION: When extracting narratives (e.g., 'What sets us apart', 'Initiatives and innovation') or matter descriptions, extract the full, original text. Do not summarize.\n"
            "5. METRICS: Accurately capture department metrics like partner and associate counts if present."
        )),
        ("user", "Extract the structured data from the following Legal 500 submission document:\n\n{text}")
    ])
    
    chain = prompt | structured_llm
    
    # 4. Ejecución y Manejo de Errores
    try:
        updates["messages"].append("Legal 500 Ingestion: Initiating strict extraction using Legal500Submission schema...")
        
        # Invocamos la cadena
        extracted_data = chain.invoke({"text": raw_text})
        
        # Guardamos la data estructurada en la variable 'submission' del AgentState
        updates["submission"] = extracted_data
        updates["messages"].append("✅ Legal 500 Ingestion Success: Data extracted and mapped perfectly to the Legal500 schema.")
        
    except Exception as e:
        error_trace = traceback.format_exc()
        updates["messages"].append(f"❌ Legal 500 Ingestion Error: {str(e)}")
        print(f"Detalle del error en Legal 500 Ingestion:\n{error_trace}")

    return updates