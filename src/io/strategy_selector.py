from typing import Dict, Any
from src.strategies.base import SubmissionStrategy
from src.strategies.legal500 import Legal500Strategy
from src.strategies.chambers import ChambersStrategy
from src.strategies.leaders_league import LeadersLeagueStrategy
from src.core.schemas import Legal500Submission, ChambersSubmission, LeadersLeagueSubmission

# =========================================================
# 1. SELECTOR DE ESTRATEGIAS (CLASES)
# =========================================================
def get_strategy(sub_type: str, config: Dict[str, Any]) -> SubmissionStrategy:
    sub_type = sub_type or "Legal500"
    
    if sub_type == "Legal500":
        strategy = Legal500Strategy()
    elif sub_type == "Chambers":
        strategy = ChambersStrategy()
    elif sub_type == "LeadersLeague":
        strategy = LeadersLeagueStrategy()
    else:
        print(f"⚠️ [WARNING] Unknown strategy '{sub_type}', defaulting to Legal500.")
        strategy = Legal500Strategy()
        
    strategy.config = config
    return strategy

# =========================================================
# 2. SELECTOR DE CONFIGURACIONES (YAML)
# =========================================================
def get_config_path(current_target: str, guide: str) -> str:
    current_target = current_target or "Legal500"
    guide = str(guide).lower() if guide else ""
    
    if current_target == "Legal500":
        if "asia" in guide or "pacific" in guide: return "configs/legal500_asia.yaml"
        if "canada" in guide or "Canada" in guide: return "configs/legal500_canada.yaml"
        if "Caribbean" in guide or "caribbean" in guide: return "configs/legal500_caribbean.yaml"
        if "Germany" in guide or "germany" in guide: return "configs/legal500_germany.yaml"
        if "Latin America" in guide or "latin america" in guide: return "configs/legal500_latin_america.yaml"
        if "UK" in guide or "uk" in guide or "United Kingdom" in guide or "united kingdom" in guide: return "configs/legal500_uk.yaml"
        if "Europe" in guide or "Africa" in guide or "europe" in guide or "africa" in guide: return "configs/legal500_emea.yaml"
        else: return "configs/legal500_us.yaml"
    elif current_target == "Chambers":
        return "configs/chambers_usa.yaml"
    elif current_target == "LeadersLeague":
        return "configs/leaders_league_argentina_advertising.yaml"
    else:
        return "configs/legal500_us.yaml"
    
def get_schema_class(sub_type: str) -> Any:
    sub_type = sub_type or "Legal500"
    if sub_type == "Legal500": return Legal500Submission
    elif sub_type == "Chambers": return ChambersSubmission
    elif sub_type == "LeadersLeague": return LeadersLeagueSubmission
    return Legal500Submission

# =========================================================
# 3. CONTEXT ENGINE (ESTRATEGIA Y ARQUETIPOS - V1 OPTIMIZADO)
# =========================================================
def get_strategic_context(submission_dict: dict) -> dict:
    # 1. BÚSQUEDA INTELIGENTE DE ESTATUS (Agnóstico al directorio)
    status = "Unranked"
    
    if "identity" in submission_dict:
        # Ruta Legal 500
        status = submission_dict["identity"].get("current_band_status", "Unranked")
    elif "A_preliminary_information" in submission_dict:
        # Ruta Chambers
        status = submission_dict["A_preliminary_information"].get("current_band_status", "Unranked")
    elif "department_information" in submission_dict:
        # Ruta Leaders League
        status = submission_dict["department_information"].get("current_ranking_status", "Unranked")
    elif "current_band_status" in submission_dict:
        # Fallback de seguridad por si viene en la raíz
        status = submission_dict.get("current_band_status", "Unranked")

    # Normalizamos para evaluación interna
    status_lower = str(status).lower()
    
    # 2. TARGET REALISTA Y POSICIÓN DE PARTIDA (Crecimiento Escalona a Escalón)
    if "unranked" in status_lower or "no rank" in status_lower or "preliminary" in status_lower or "spotlight" in status_lower:
        target = "Entry-level (Break into Band 4 or Band 3)"
        tone = "Evaluate strictly as an Entry Candidate aiming to break into Band 4 or Band 3. Do not look for market dominance; look for baseline credibility, institutional clients, and solid mid-market execution."
    elif "5" in status_lower or "4" in status_lower:
        target = "Mid-Tier Push (Solidify position and push for Band 3)"
        tone = "Evaluate for Mid-Tier advancement, specifically pushing for Band 3. Focus on consistency, institutional stability, and upward momentum. Penalize commoditized volume."
    elif "3" in status_lower:
        # Ya no empujamos a Band 1, solo a Band 2.
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

    # 3. LIBRERÍA DE ARQUETIPOS COMPLETA
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
        "realistic_target": target,
        "evaluation_tone": tone,
        "possible_archetypes": full_archetype_library,
        "current_band": status # Guardamos la banda tal cual la sacamos del diccionario
    }