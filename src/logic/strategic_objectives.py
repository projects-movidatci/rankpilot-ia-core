def get_objective_instructions(objective: str, directory_type: str) -> str:
    """Defines the narrative focus based on what the firm wants to achieve."""
    obj = str(objective).lower()
    
    if "entry" in obj:
        return "OBJECTIVE - ENTRY: Focus on building baseline credibility. Prove the firm handles institutional clients and market-standard execution. Do not use overly dominant language."
    elif "promotion" in obj:
        return "OBJECTIVE - PROMOTION: Focus on upward momentum. The narrative must explicitly show a gap between this firm and its current peers, demanding evidence of growing complexity."
    elif "consolidation" in obj:
        return "OBJECTIVE - CONSOLIDATION: The firm recently moved up or is stabilizing. Prove sustained excellence across multiple matters, not just one isolated 'good year'."
    elif "recovery" in obj:
        return "OBJECTIVE - RECOVERY: The firm dropped in rankings or lost key partners. Emphasize institutional continuity, recovery of credibility, and stability of the core client base."
    elif "repositioning" in obj:
        return "OBJECTIVE - REPOSITIONING: The firm is shifting its market focus. Ensure the narrative clearly articulates the new strategic direction and connects it to the submitted matters."
        
    return "OBJECTIVE - GENERAL: Focus on identifying the next logical tier of progression."