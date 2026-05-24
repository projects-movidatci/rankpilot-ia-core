from src.core.state import AgentState
from src.io.pdf_parser import extract_text_from_pdf
from src.io.docx_manager import extract_text_from_docx
from src.io.ocr_assist import extract_text_from_image
import base64

def matters_assistant_ingestion_node(state: AgentState) -> dict:
    """
    Act 0: Multi-Modal Batch Ingestion Router
    Processes an array of files, extracts text based on MIME type, and concatenates it.
    """
    updates = {"current_step": "matters_assistant_ingestion", "messages": []}
    
    # In FastAPI, we will inject this payload into state.base64_documents
    batch = getattr(state, "base64_documents", [])
    raw_text = getattr(state, "raw_text", "")
    
    concatenated_data = [f"--- RAW NOTES ---\n{raw_text}\n"] if raw_text else []
    success_count = 0
    
    for file_data in batch:
        # Pydantic dict access
        mime_type = file_data.get("mime_type", "").lower()
        base64_data = file_data.get("base64_data", "")
        filename = file_data.get("filename", "Unknown_File")
        
        try:
            if "pdf" in mime_type:
                text = extract_text_from_pdf(base64_data)
                concatenated_data.append(f"--- SOURCE (PDF): {filename} ---\n{text}")
                success_count += 1
                
            elif "word" in mime_type or "docx" in mime_type:
                text = extract_text_from_docx(base64_data)
                concatenated_data.append(f"--- SOURCE (DOCX): {filename} ---\n{text}")
                success_count += 1
                
            elif "image" in mime_type:
                text = extract_text_from_image(base64_data, mime_type)
                concatenated_data.append(f"--- SOURCE (IMAGE OCR): {filename} ---\n{text}")
                success_count += 1

            elif "text" in mime_type or "raw" in mime_type:
                # Decode the base64 string directly into readable text
                text = base64.b64decode(base64_data).decode('utf-8', errors='ignore')
                concatenated_data.append(f"--- SOURCE (RAW TEXT): {filename} ---\n{text}")
                success_count += 1
                
            else:
                updates["messages"].append(f"⚠️ Skipped {filename}: Unsupported MIME type {mime_type}")
                
        except Exception as e:
            updates["messages"].append(f"❌ Failed to process {filename}: {str(e)}")
            
    # Combine everything into one massive context block
    final_context = "\n\n".join(concatenated_data)
    updates["messages"].append(f"✅ Batch Ingestion Complete: Processed {success_count} files.")
    
    # We map this to 'extracted_text' so the next node can easily read it
    updates["extracted_text"] = final_context
    
    return updates