import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.core.state import AgentState
from src.core.llm import get_llm
from src.core.schemas import ChambersSubmission, Legal500Submission, LeadersLeagueSubmission
from src.io.strategy_selector import get_strategic_context
# --- STRUCTURED OUTPUT MODELS ---
class CleanedField(BaseModel):
    field_key: str = Field(description="The exact key/path of the field being cleaned.")
    sanitized_text: str = Field(description="The fully cleaned and formatted text.")

class SanitizationBatch(BaseModel):
    cleaned_fields: List[CleanedField] = Field(description="List of fields that have been sanitized.")

# --- RECURSIVE HELPERS ---
def get_long_string_fields(data: Any, path: str = "") -> Dict[str, str]:
    """Recursively finds all string fields longer than 50 characters to sanitize using dot notation."""
    long_strings = {}
    
    # 🛡️ THE FIX: THE ULTIMATE SANITIZER BLACKLIST
    forbidden_keys = [
        "publishable_matters",           # <--- BLOCKS THE ENTIRE PUBLISHABLE ARRAY
        "confidential_matters",          # <--- BLOCKS THE ENTIRE CONFIDENTIAL ARRAY
        "D2_summary_of_matter_and_role", # (Kept for safety)
        "E2_summary_of_matter_and_role", # (Kept for safety)
        "matter_description",            # (Legal 500 safety)
        "publishable_summary",
        "D1_name_of_client",
        "E1_name_of_client"
    ]

    if isinstance(data, dict):
        for k, v in data.items():
            current_key_path = f"{path}.{k}" if path else k
            
            # DEBUG BLOCK: Check if it's forbidden
            if k in forbidden_keys:
                print(f"🛑 [SANITIZER SHIELD] Protecting forbidden array/field: {current_key_path}")
                continue # Skip traversing this entire branch!
                
            long_strings.update(get_long_string_fields(v, current_key_path))
            
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}.{i}"
            long_strings.update(get_long_string_fields(item, new_path))
            
    elif isinstance(data, str) and len(data) > 50:
        long_strings[path] = data
        
    return long_strings

def apply_cleaned_field(data: Any, path: str, clean_text: str):
    """Recursively applies the cleaned text back to the specific dictionary path."""
    keys = path.split(".")
    current = data
    for key in keys[:-1]:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            current = current[int(key)]
    final_key = keys[-1]
    if isinstance(current, dict):
        current[final_key] = clean_text
    elif isinstance(current, list):
        current[int(final_key)] = clean_text

# --- NODE IMPLEMENTATION ---
def sanitizer_node(state: AgentState) -> dict:
    """
    Sanitizer Node with Batching Logic:
    Processes fields in groups of 5 to prevent LLM output token limits and EOF errors.
    """
    updates = {"current_step": "sanitizer", "messages": []}

    submission_data = getattr(state, "submission", None)
    if not submission_data:
        return updates

    submission_dict = submission_data.model_dump(exclude_none=True)
    target_submission_type = getattr(state, "target_submission_type", "Legal500") or "Legal500"

    # 1. Identificar campos largos
    text_fields_to_clean = get_long_string_fields(submission_dict)

    if not text_fields_to_clean:
        updates["messages"].append("Sanitizer node: No long text fields found to clean.")
        return updates

    # --- LÓGICA DE BATCHING (Grupos de 5) ---
    items = list(text_fields_to_clean.items())
    batch_size = 8
    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    
    # Configuración de Guías Editoriales (desde YAML)
    taml_config = getattr(state, "config", {}) or {}
    custom_guidelines = taml_config.get("copywriting_guidelines", "No additional guidelines provided.")

    # 1. GENERAR CONTEXTO ESTRATÉGICO DINÁMICO
    # Combinamos la data actual con la configuración del YAML[cite: 9, 10]
    config = getattr(state, "config", {}) or {}
    strat_context = get_strategic_context(submission_dict)
    # Aquí inyectamos las reglas del YAML y el tono de la estrategia[cite: 9, 10]
    editorial_guidelines = config.get("copywriting_guidelines", "Follow professional legal standards.")

    llm = get_llm(temperature=0.3)
    # Importante: Algunos modelos requieren max_tokens explícito para salidas largas
    if hasattr(llm, "max_tokens"):
        llm.max_tokens = 4000

    structured_llm = llm.with_structured_output(SanitizationBatch)

    system_prompt = (
        "You are an elite Legal Copywriter and Strategist for top-tier law firms.\n"
        "Your mission is to polish raw text into 'Band 1' level prose while acting as a guardian of critical metadata.\n\n"
        
        "=========================================\n"
        "STRICT PRESERVATION RULES (DO NOT MODIFY):\n"
        "1. WEB LINKS/URLS: Keep all URLs exactly as they are (e.g., bio links). They are vital for researchers. Put each URL on its own separate line.\n"
        "2. RANKING STATUS: Preserve the lines 'Current ranking:' and 'Suggested ranking:' exactly. Do not delete them, and keep them on their own lines.\n"
        "3. CONFIDENTIALITY TAGS: You MUST keep '[CONFIDENTIAL]' or 'CONFIDENTIAL' markers at the start of narratives.\n"
        "4. KEY TITLES: Do not remove headers like 'Key areas of focus:' or 'Standout recent work:'.\n"
        "=========================================\n\n"

        "### STRATEGIC CONTEXT ###\n"
        f"TARGET GOAL: {strat_context['realistic_target']}\n"
        f"EVALUATION TONE: {strat_context['evaluation_tone']}\n\n"
        "### DIRECTORY EDITORIAL RULES (FROM YAML) ###\n"
        f"{editorial_guidelines}\n\n"
        
        "COPYWRITING GUIDELINES:\n"
        f"{custom_guidelines}\n\n"
        
        "INSTRUCTIONS:\n"
        "1. ELEVATE THE PROSE: Rewrite narrative paragraphs across ALL sections (biographies, department overviews, and matter descriptions). "
        "Use active, sophisticated verbs (e.g., 'Orchestrated', 'Spearheaded') and remove repetitive phrasing.\n"
        "2. PARAGRAPH STRUCTURE (CRITICAL): You MUST inject explicit double newlines (\\n\\n) to separate distinct paragraphs, URLs, ranking metadata, headers, and bullet points. Every new concept, link, or ranking MUST be separated by \\n\\n. DO NOT flatten the text.\n"
        "3. STRUCTURE: For biographies, ensure ranking metadata stays at the top, followed by \\n\\n, then the polished 'Key areas of focus'.\n"
        "4. STRIP ONLY ACTUAL JUNK: Remove internal draft notes (e.g. 'check this dates'), broken ASCII characters, "
        "and duplicate headers. Do NOT touch links or ranking bands.\n"
        "5. BOLDING TRIGGERS (CRITICAL): You MUST actively use double asterisks **Text** to bold key elements across ALL sections. "
        "You MUST bold: **Lawyer Names**, **Client Companies**, **Financial Values** (e.g., **USD 250 million**), **Practice Areas** (e.g., **Banking & Finance**), and **Key Laws/Regulations**. DO NOT use any other markdown."
        "6. RED CONFIDENTIALITY TAG (CRITICAL): You must identify any paragraph that begins with 'CONFIDENTIAL' or '[CONFIDENTIAL]'. You MUST wrap the ENTIRE warning paragraph (ALL the Paragraph) in [RED_START] and [RED_END] tags (if the next paragraph is still talking about the confidential context grab it.). You MUST inject \\n\\n immediately after the closing tag to separate the red warning from the main text.\n"
        "Example: [RED_START][CONFIDENTIAL] This amount is strictly confidential. The lawyer conducted a transactional Cross-border...[RED_END]\\n\\n"
    )

    total_cleaned = 0
    for i, batch in enumerate(batches):
        # Crear el contexto de datos "sucios" para este lote
        dirty_data_context = "\n".join([f"KEY: {k}\nTEXT: {v}\n---" for k, v in batch])
        
        user_prompt = (
            f"### BATCH {i+1} of {len(batches)} ###\n"
            "Rewrite the following fields to match the STRATEGIC CONTEXT and EDITORIAL RULES above.\n"
            "CRITICAL FORMATTING: You MUST use **double asterisks** for key terms. "
            "If a narrative contains a confidentiality warning at the beginning, you MUST wrap the ENTIRE warning sentence/paragraph in [RED_START] and [RED_END] tags and immediately follow it with \\n\\n before beginning the main text.\n\n"
            f"{dirty_data_context}"
        )

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", user_prompt),
            ])
            
            chain = prompt | structured_llm
            # El invoke va vacío porque las variables ya están inyectadas en el prompt template
            output = chain.invoke({}) 

            if output and output.cleaned_fields:
                for clean_item in output.cleaned_fields:
                    apply_cleaned_field(submission_dict, clean_item.field_key, clean_item.sanitized_text)
                    total_cleaned += 1
            
        except Exception as batch_error:
            # Si un lote falla (por ejemplo, por contenido sensible o error de red), 
            # el sistema continúa con el siguiente lote para salvar el resto de la información.
            print(f"--- [WARNING] Failed to sanitize batch {i+1}: {batch_error} ---")
            updates["messages"].append(f"Sanitizer: Batch {i+1} failed to process. Keeping raw data for these fields.")

    # 3. Re-validar a través de Pydantic y actualizar el estado
    try:
        if target_submission_type == "Legal500":
            updates["submission"] = Legal500Submission(**submission_dict)
        elif target_submission_type == "LeadersLeague":
            updates["submission"] = LeadersLeagueSubmission(**submission_dict)
        else:
            updates["submission"] = ChambersSubmission(**submission_dict)
            
        updates["messages"].append(f"Sanitizer node: Successfully sanitized {total_cleaned} fields across {len(batches)} batches.")
    except Exception as e:
        print(f"--- [ERROR] Schema validation failed after sanitization: {e} ---")
        updates["messages"].append("Sanitizer: Schema validation failed. Returning original data.")

    return updates