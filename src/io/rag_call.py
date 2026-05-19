import os

def load_rag_context(practice_area: str) -> str:
    if practice_area == "Banking & Finance":
        file_path = "src/rag/banking_core_v1.md"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
    return "No specific RAG available for this practice area."

def load_rubric_rag(practice_area: str) -> str:
    """Loads the 100-point rubric core from the Markdown file."""
    if practice_area == "Banking & Finance":
        # 🛡️ THE FIX: Updated path to match the new Chambers Banking Rubric file
        file_path = "src/rag/03_Chambers_Banking_Scoring_Rubric.md"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
    return "WARNING: Rubric RAG file not found."
