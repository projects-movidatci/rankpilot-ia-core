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
    """
    Factory function que instancia la estrategia correcta según el tipo,
    e inyecta la configuración dinámica (YAML regional) para evitar defaults.
    """
    # ¡CERO rastro de "guide" o "current_target" aquí!
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
        
    # Inyección de dependencias: Le pasamos el cerebro regional
    strategy.config = config
    
    return strategy

# =========================================================
# 2. SELECTOR DE CONFIGURACIONES (YAML)
# =========================================================
def get_config_path(current_target: str, guide: str) -> str:
    """
    Factory function que determina la ruta exacta del archivo YAML 
    basado en el directorio objetivo y la región/guía enviada por el usuario.
    """
    current_target = current_target or "Legal500"
    guide = str(guide).lower() if guide else ""
    
    # --- RUTEO PARA LEGAL 500 ---
    if current_target == "Legal500":
        if "asia" in guide or "pacific" in guide:
            return "configs/legal500_asia.yaml"
        else:
            return "configs/legal500_us.yaml" # Fallback por defecto
            
    # --- RUTEO PARA CHAMBERS ---
    elif current_target == "Chambers":
        return "configs/chambers_usa.yaml"
        
    # --- RUTEO PARA LEADERS LEAGUE ---
    elif current_target == "LeadersLeague":
        return "configs/leaders_league_argentina_advertising.yaml"
        
    # --- FALLBACK DE EMERGENCIA ABSOLUTO ---
    else:
        print(f"⚠️ [WARNING] Unknown target '{current_target}', defaulting to Legal500 US config.")
        return "configs/legal500_us.yaml"
    
def get_schema_class(sub_type: str) -> Any:
    """
    Factory function que devuelve la clase de Pydantic (esquema) 
    correspondiente al directorio seleccionado.
    """
    sub_type = sub_type or "Legal500"
    
    if sub_type == "Legal500":
        return Legal500Submission
    elif sub_type == "Chambers":
        return ChambersSubmission
    elif sub_type == "LeadersLeague":
        return LeadersLeagueSubmission
    
    return Legal500Submission # Fallback