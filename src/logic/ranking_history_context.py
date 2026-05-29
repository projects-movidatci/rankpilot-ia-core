from typing import Dict

def get_unified_ranking_strategy(current_band: str, history: str, directory_type: str) -> Dict[str, str]:
    """
    Evaluates the Firm Status (C) and Ranking History (D) as a unified system
    to deduce the exact Strategic Objective (B) and the resulting Editorial Rules.
    """
    band = str(current_band).lower()
    hist = str(history).lower()
    
    objective = "General Advancement"
    rules = "Evaluate objectively based on provided evidence."

    # ---------------------------------------------------------
    # 1. UNRANKED / ENTRY LEVEL
    # ---------------------------------------------------------
    if any(x in band for x in ["unranked", "no rank", "preliminary", "spotlight"]):
        if "descent" in hist:
            objective = "Entry-Level Recovery"
            rules = f"RULE ({directory_type}): The firm fell out of the rankings entirely. Focus purely on credibility recovery, stable institutional clients, and proving baseline market share. Do not use aggressive language."
        elif "first time" in hist:
            objective = "First-Time Entrant (Target Band 4 or Band 5)"
            rules = f"RULE ({directory_type}): This is the firm's first-ever submission for this practice area. The realistic goal is to secure an initial ranking in Band 4 or Band 5. Focus on establishing a clear, compelling baseline of market presence and institutional client trust. Do not force elite top-tier standards; just prove they comfortably meet the directory's minimum threshold for inclusion."
        else:
            objective = "Entry-Level (Target Band 4 or Band 5)"
            rules = f"RULE ({directory_type}): The firm is unranked. Prioritize baseline market integration and standard execution to break into the lower bands. Establish a solid foundation before challenging higher-tier incumbents."

    # ---------------------------------------------------------
    # 2. MID-TIER (Bands 4 and 5)
    # ---------------------------------------------------------
    elif "5" in band or "4" in band:
        if "stagnation" in hist:
            objective = "Stagnation Breakout (Push for Band 3)"
            rules = f"RULE ({directory_type}): The firm is stuck in the lower-mid tiers. You MUST demand new, differentiating evidence of complex deal mechanics. Penalize commoditized, repetitive volume."
        elif "descent" in hist:
            objective = "Mid-Tier Recovery"
            rules = f"RULE ({directory_type}): The firm recently dropped to the lower tiers. Focus on stabilizing the narrative, retaining key partners, and rebuilding trust."
        else:
            objective = "Mid-Tier Promotion"
            rules = f"RULE ({directory_type}): The firm is climbing. Focus on consistency, upward momentum, and proving they can handle work currently done by Band 3 firms."

    # ---------------------------------------------------------
    # 3. UPPER-MID TIER (Band 3)
    # ---------------------------------------------------------
    elif "3" in band:
        if "stagnation" in hist:
            objective = "Consolidation & Breakout (Target Band 2)"
            rules = f"RULE ({directory_type}): The firm is a stagnant Band 3. Demand evidence of significantly growing complexity. They must prove they are consistently beating Band 2 incumbents for mandates."
        elif "ascent" in hist:
            objective = "Consolidate New Position"
            rules = f"RULE ({directory_type}): The firm just reached Band 3. The submission MUST demonstrate sustained consolidation to prove it wasn't a fluke. Focus on stability."
        elif "descent" in hist:
            objective = "Elite Recovery (Reclaim Band 2)"
            rules = f"RULE ({directory_type}): The firm recently dropped from Band 2 to Band 3. The narrative MUST aggressively focus on recovering elite credibility. Highlight retained blue-chip clients and matters that clearly outshine standard Band 3 work."
        else:
            objective = "Upper-Mid Tier Push"
            rules = f"RULE ({directory_type}): The firm is targeting Band 2. Look for highly sophisticated matters, but keep expectations realistic. Do not force Band 1 elite standards yet."

    # ---------------------------------------------------------
    # 4. ELITE CHALLENGER (Band 2)
    # ---------------------------------------------------------
    elif "2" in band:
        objective = "Elite Challenger (Push for Band 1)"
        if "stagnation" in hist:
            rules = f"RULE ({directory_type}): The firm is a stagnant Band 2. The standard is absolute excellence. They MUST provide market-shaping precedents that explicitly steal market share from Band 1 leaders."
        elif "descent" in hist:
            rules = f"RULE ({directory_type}): The firm lost its Band 1 status. The narrative must aggressively reclaim leadership through undeniable, bet-the-company flagship matters."
        elif "ascent" in hist:
            objective = "Consolidate Elite Status"
            rules = f"RULE ({directory_type}): The firm just reached Band 2. They must prove they belong at the elite table permanently. The submission must demonstrate sustained, high-stakes complexity and show them comfortably operating alongside Band 1 incumbents."
        else:
            rules = f"RULE ({directory_type}): The firm is pushing for Band 1. Demand evidence of absolute market dominance and extreme transactional complexity."

    # ---------------------------------------------------------
    # 5. MARKET LEADER (Band 1)
    # ---------------------------------------------------------
    elif "1" in band:
        objective = "Defensive Leadership (Protect Band 1)"
        rules = f"RULE ({directory_type}): The firm is Band 1. The strategy is purely defensive. Be ruthless and nitpicky. Do not accept anything less than flagship, market-defining matters. Eliminate lower-value deals."

    return {
        "strategic_objective": objective,
        "editorial_rules": rules
    }

# =========================================================
# 3. CONTEXT ENGINE (ESTRATEGIA Y ARQUETIPOS - V1 OPTIMIZADO)
# =========================================================
def get_strategic_context(submission_dict: dict, metadata: dict = None) -> dict:
    """
    Evaluates the firm's status and trajectory using Laravel's metadata payload.
    Defaults to a 'Stagnation' history to automatically build an ascension narrative
    without interrogating the user.
    """
    if metadata is None:
        metadata = {}

    # 1. Extract data directly from Laravel's payload
    current_band = metadata.get("current_band", "Band 5")
    target_band = metadata.get("target_band", "Band 4")
    directory_type = metadata.get("directory", "Chambers")
    
    # 2. Force the historical assumption to bypass Audit Room questions
    history = "Stagnation" 

    # 3. Process the logic through your unified strategy engine
    strategy = get_unified_ranking_strategy(current_band, history, directory_type)
    
    # 4. Refine the dynamic target label based on Laravel's target_band
    target_label = f"Ascension Push ({current_band} -> {target_band})"
    if current_band == target_band:
        target_label = f"Defensive Consolidation (Protecting {current_band})"
    elif "unranked" in current_band.lower():
        target_label = f"Entry-Level Breakthrough (Targeting {target_band})"

    # 5. Execute explicit strategic tone and target logic
    status_lower = str(current_band).lower()
    
    if any(x in status_lower for x in ["unranked", "no rank", "preliminary", "spotlight"]):
        target = "Entry-level (Break into Band 4 or Band 3)"
        tone = "Evaluate strictly as an Entry Candidate aiming to break into Band 4 or Band 3. Do not look for market dominance; look for baseline credibility, institutional clients, and solid mid-market execution."
    elif "5" in status_lower or "4" in status_lower:
        target = "Mid-Tier Push (Solidify position and push for Band 3)"
        tone = "Evaluate for Mid-Tier advancement, specifically pushing for Band 3. Focus on consistency, institutional stability, and upward momentum. Penalize commoditized volume."
    elif "3" in status_lower:
        target = "Upper-Mid Tier Push (Consolidate Band 3 and target Band 2)"
        tone = "Evaluate as an ascending firm targeting Band 2. Look for growing complexity and signs they are competing with Band 2 incumbents. Do NOT force Band 1 elite standards yet; keep expectations realistic for a Band 2 push."
    elif "2" in status_lower:
        target = "Elite Challenger (Push for Band 1)"
        tone = "Evaluate as an Elite Challenger targeting Band 1. The standard is absolute excellence. Look for market-shaping precedents and evidence of stealing market share from Band 1 incumbents."
    elif "1" in status_lower:
        target = "Defensive Leadership (Protect Band 1)"
        tone = "Evaluate as Defensive Leadership protecting a Band 1 ranking. Be ruthless and nitpicky. Do not accept anything less than flagship, bet-the-company matters."
    else:
        target = "General Advancement (Improve current standing)"
        tone = "Evaluate objectively based on the provided evidence, identifying the next logical tier of progression."

    # 6. Combine the dynamic label with the explicit target definition
    realistic_target_final = f"{target_label} - {target}"

    full_archetype_library = """
    TRANSACTIONAL (Banking, Corporate, VC, Infra):
    - Elite dealmakers (High-end M&A, bet-the-company deals)
    - Mid-market execution powerhouse (High volume, efficient closing)
    - Lender-driven finance (Institutional bank representation)
    - Borrower-side finance (Complex structuring for corporate borrowers)
    - VC & Emerging Companies (Startups, funding rounds, tech focus)
    - Project Finance & Infra (Long-term asset/state projects)

    DISPUTES (Litigation, Arbitration, Appellate, White-Collar, Liability):
    - Elite arbitration boutique (Cross-border, investor-state, high-value)
    - High-volume litigation machine (Local courts, mass tort, massive volume)
    - White-Collar & Investigations (Criminal defense, crisis management, extreme sensitivity)
    - Sector-specialized disputes (Niche focus like Construction, IP, or E-discovery)

    REGULATORY (Antitrust, Compliance, Tax, Public Law):
    - Regulatory powerhouse (Administrative litigation, shapes public policy)
    - Antitrust & Competition (Merger control, cartel investigations)
    - Compliance & Risk platform (Preventative ESG, high-volume audits)
    - Sector-specialist advisor (Strictly focused on Telecom, Energy, etc.)

    MIXED / FULL-SERVICE:
    - Full-service elite (Tier 1 one-stop-shop for multinationals)
    - Regional cross-border platform (Value derived from multi-country footprint)
    - Full-service mid-market (Accessible end-to-end for local business)
    - Specialist hybrid firm (Multi-practice but strictly within one industry)
    """

    return {
        "realistic_target": realistic_target_final,
        "evaluation_tone": tone,
        "strategic_objective": strategy.get("strategic_objective", "General Advancement"),
        "possible_archetypes": full_archetype_library,
        "current_band": current_band 
    }