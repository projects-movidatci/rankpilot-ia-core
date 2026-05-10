def get_market_context(jurisdiction: str, practice_area: str) -> str:
    """MVP for Jurisdiction context. Will be replaced by RAG database later."""
    base_context = f"Operating in {jurisdiction} for {practice_area}."
    
    if "Mexico" in jurisdiction and "Banking" in practice_area:
        return f"{base_context} Highly competitive market dominated by dual-law (NY/MX) cross-border structuring."
    
    return base_context