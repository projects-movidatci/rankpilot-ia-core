import os
import asyncio
from typing import List, Union
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import AgentState
from src.core.schemas import PublishableMatter, ConfidentialMatter, StrategicTaxonomy

# 1. Función para cargar tu RAG
def load_banking_rag() -> str:
    """Carga el cerebro taxonómico desde el archivo Markdown."""
    file_path = "src/rag/banking_core_v1.md"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "WARNING: Banking RAG file not found."

# 2. El System Prompt Maestro
SYSTEM_PROMPT_EXTRACTOR = """
[ROLE]
You are an elite Legal Data Analyst for Chambers & Partners. Your ONLY job is to read raw legal matter descriptions and classify them strictly according to our internal taxonomy.

[KNOWLEDGE BASE (RAG)]
{banking_rag_content}

[YOUR MISSION]
You will receive the raw text of a legal matter.
You must extract and classify the strategic data into the required JSON schema. 

[STRICT EXTRACTION RULES]
1. primary_category: Choose EXACTLY ONE category from the Knowledge Base. 
2. adjacent_table_risk: Set to TRUE ONLY IF the matter matches the Capital Markets, Project Finance, or Asset Finance rules. Otherwise, FALSE.
3. client_side: Identify if the firm acted for the Lender, Borrower, Sponsor, Arranger, or Guarantor.
4. firm_role_taxonomy: Classify the firm's role as 'Very Strong', 'Moderate', or 'Weak' based on the Knowledge Base.
5. complexity_indicators: Extract specific features mentioned in the text that match the 'Indicadores de Complejidad'.

NO HALLUCINATIONS. If a piece of information is missing from the raw text, leave it as null or empty.
"""

# 3. Función asíncrona individual (Procesa 1 matter)
def classify_single_matter(matter: Union[PublishableMatter, ConfidentialMatter], rag_content: str, llm) -> Union[PublishableMatter, ConfidentialMatter]:
    """Llama al LLM para clasificar un solo asunto sin destruir la descripción."""
    
    client_name = getattr(matter, "D1_name_of_client", getattr(matter, "E1_name_of_client", "Unknown Client"))
    description = getattr(matter, "D2_summary_of_matter_and_role", getattr(matter, "E2_summary_of_matter_and_role", ""))
    value = getattr(matter, "D3_matter_value", getattr(matter, "E3_matter_value", "No value provided"))
    
    if not description or description.strip() == "":
        return matter

    matter_text = f"Client: {client_name}\nValue: {value}\nDescription: {description}"

    # 🛡️ THE TRUE FIX: We ONLY ask the LLM to output the taxonomy schema!
    structured_llm = llm.with_structured_output(StrategicTaxonomy)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_EXTRACTOR),
        ("human", "Classify this matter strictly according to the RAG rules:\n\n{matter_text}")
    ])

    chain = prompt | structured_llm
    
    try:
        # The LLM now only generates the categories, it doesn't touch the description!
        taxonomy_result = chain.invoke({
            "banking_rag_content": rag_content,
            "matter_text": matter_text
        })
        
        # 🛡️ THE STAPLE: Attach the taxonomy to the untouched original matter
        matter.taxonomy = taxonomy_result
        return matter
        
    except Exception as e:
        print(f"❌ Error clasificando matter {matter.matter_id}: {e}")
        return matter

# 4. EL NODO PRINCIPAL DE LANGGRAPH (Asíncrono)
def taxonomy_node(state: AgentState) -> dict:
    """Nodo que clasifica todos los matters en paralelo."""
    updates = {"current_step": "taxonomy_classification", "messages": []}
    updates["messages"].append("🚀 INICIANDO: taxonomy_node (Procesamiento en Paralelo)")
    print("🚀 Disparando clasificación taxonómica masiva...")

    # Recuperamos el submission del estado (creado por el ingestion_node)
    submission = getattr(state, "submission", None)
    
    if not submission:
        updates["messages"].append("⚠️ Taxonomy Node Aborted: No submission object found in state.")
        return updates

    # Cargamos el cerebro (RAG)
    rag_content = load_banking_rag()
    
    # Instanciamos el LLM (Temperature 0 para máxima precisión)
    llm = get_llm(temperature=0)

    # Separamos los matters
    publishable = getattr(submission, "D_publishable_information", None)
    pub_matters = publishable.publishable_matters if publishable else []
    
    confidential = getattr(submission, "E_confidential_information", None)
    conf_matters = confidential.confidential_matters if confidential else []

    # Unimos todo en una lista de tareas para el event loop
    all_matters = pub_matters + conf_matters
    
    if not all_matters:
        updates["messages"].append("⚠️ Taxonomy Node: No matters found to classify.")
        return updates

    # ========================================================
    # EJECUCIÓN SÍNCRONA (Bucle Clásico)
    # ========================================================
    enriched_results = []
    for matter in all_matters:
        # Llamamos a la función síncrona uno por uno
        result = classify_single_matter(matter, rag_content, llm)
        enriched_results.append(result)
    
    # Reconstruimos las listas separadas a partir de los resultados
    enriched_pub = [m for m in enriched_results if isinstance(m, PublishableMatter)]
    enriched_conf = [m for m in enriched_results if isinstance(m, ConfidentialMatter)]

    # Actualizamos el objeto submission
    if publishable:
        publishable.publishable_matters = enriched_pub
    if confidential:
        confidential.confidential_matters = enriched_conf

    # Guardamos el submission mutado en las actualizaciones del estado
    updates["submission"] = submission
    updates["messages"].append(f"✅ Taxonomy Node Success: Clasificados {len(enriched_results)} matters exitosamente.")
    print(f"✅ Taxonomía completada para {len(enriched_results)} matters.")

    # Toggle the flags for the Router
    updates["trigger_analysis"] = False 
    updates["is_strategically_analyzed"] = True

    ctx = getattr(state, "strategic_context", {})
    ctx["trigger_analysis"] = False 
    ctx["is_strategically_analyzed"] = True
    updates["strategic_context"] = ctx

    return updates