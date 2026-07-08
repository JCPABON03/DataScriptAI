import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import json

class Settings(BaseSettings):
    # API
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_URL: str = Field(default="http://localhost:8000", env="API_URL")
    
    # Gemini API
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    # File Upload
    MAX_UPLOAD_SIZE: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    TEMP_FILE_PATH: str = Field(default="./temp", env="TEMP_FILE_PATH")
    
    # LaTeX
    LATEX_COMPILER: str = Field(default="pdflatex", env="LATEX_COMPILER")
    LATEX_TEMP_PATH: str = Field(default="./temp/latex", env="LATEX_TEMP_PATH")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Procesar CORS_ORIGINS si viene como string
        if isinstance(self.CORS_ORIGINS, str):
            try:
                self.CORS_ORIGINS = json.loads(self.CORS_ORIGINS)
            except:
                self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

settings = Settings()

# Validación crítica
if not settings.GEMINI_API_KEY:
    import logging
    logging.warning("GEMINI_API_KEY no configurada. Las funciones de IA no funcionarán.")