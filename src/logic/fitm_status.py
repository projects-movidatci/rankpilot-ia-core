def get_status_context(status: str, directory_type: str) -> str:
    """Adjusts the tone based on the firm's current band or tier."""
    status_str = str(status).lower()
    
    if any(x in status_str for x in ["unranked", "no rank", "spotlight"]):
        return f"STATUS ({directory_type}): The firm is currently Unranked. Avoid aggressive benchmarking against Tier 1 firms."
    elif "1" in status_str:
        return f"STATUS ({directory_type}): The firm is in Band/Tier 1. The strategy is purely defensive. Be ruthless in eliminating low-value deals; accept ONLY flagship matters."
    elif "2" in status_str:
        return f"STATUS ({directory_type}): The firm is in Band/Tier 2. To challenge for Tier 1, the standard is absolute excellence and market dominance."
    else:
        return f"STATUS ({directory_type}): The firm is mid-tier ({status}). Focus on consistency and upward trajectory."