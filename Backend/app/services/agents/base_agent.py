from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Clase base para todos los agentes
    """
    
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def process(self, data: Any, **kwargs) -> Any:
        """
        Método principal que debe implementar cada agente
        """
        pass
    
    def log_start(self, action: str = "processing"):
        self.logger.info(f"[{self.name}] Iniciando {action}...")
    
    def log_end(self, action: str = "processing"):
        self.logger.info(f"[{self.name}] Finalizado {action}")
    
    def log_error(self, error: Exception):
        self.logger.error(f"[{self.name}] Error: {str(error)}")