from langchain_core.messages import HumanMessage
from src.core.llm import get_llm

def extract_text_from_image(base64_data: str, mime_type: str) -> str:
    """
    Passes a base64 encoded image to Gemini via OpenRouter to perform Semantic OCR.
    """
    try:
        # Fetch the LLM instance (Configured for Gemini in your llm.py)
        llm = get_llm(temperature=0)
        
        # Construct the multi-modal prompt
        message = HumanMessage(
            content=[
                {
                    "type": "text", 
                    "text": (
                        "You are an expert legal OCR system. Your job is to extract all readable text "
                        "from this image exactly as it appears. Do not summarize, guess, or create new information. "
                        "Maintain the original structure, formatting, tables, and spelling."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # Format the base64 string for LangChain's vision capabilities
                        "url": f"data:{mime_type};base64,{base64_data}"
                    }
                }
            ]
        )
        
        # Invoke the model
        response = llm.invoke([message])
        print(f"Vision OCR Response: {response.content[:200]}...")  # Debug log of the response
        return response.content

    except Exception as e:
        print(f"Vision OCR Error: {str(e)}")
        # Return a fallback string so the rest of the batch doesn't crash
        return f"[OCR FAILED TO READ IMAGE: {str(e)}]"