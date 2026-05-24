from typing import Dict, Any
from src.strategies.base import SubmissionStrategy
from src.strategies.legal500 import Legal500Strategy
from src.strategies.chambers import ChambersStrategy
from src.strategies.leaders_league import LeadersLeagueStrategy
from src.strategies.chambers_matter import ChambersMatterStrategy # 👈 NUEVO: Importamos el Matters Assistant
from src.core.schemas import Legal500Submission, ChambersSubmission, LeadersLeagueSubmission, SingleMatterExtraction

# =========================================================
# 1. SELECTOR DE ESTRATEGIAS (CLASES)
# =========================================================
def get_strategy(sub_type: str, config: Dict[str, Any]) -> SubmissionStrategy:
    sub_type = sub_type or "Legal500"
    
    if sub_type == "MattersAssistant":               # 👈 NUEVO: Enrutamiento de estrategia
        strategy = ChambersMatterStrategy()
    elif sub_type == "Legal500":
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
    
    if current_target == "MattersAssistant":         # 👈 NUEVO: Enrutamiento de YAML
        return "configs/chambers_matter.yaml"
    elif current_target == "Legal500":
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
    if sub_type == "MattersAssistant": return SingleMatterExtraction   # 👈 NUEVO: Devolvemos un dict base porque usaremos el JSON dinámico de LangChain
    elif sub_type == "Legal500": return Legal500Submission
    elif sub_type == "Chambers": return ChambersSubmission
    elif sub_type == "LeadersLeague": return LeadersLeagueSubmission
    return Legal500Submission

