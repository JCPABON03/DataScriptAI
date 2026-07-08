#!/usr/bin/env python
"""
Script para ejecutar la aplicación FastAPI
"""
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno ANTES de cualquier otra cosa
    load_dotenv()
    
    # Asegurar directorios
    Path("./temp").mkdir(exist_ok=True)
    Path("./temp/pdf").mkdir(exist_ok=True)
    
    # Ejecutar servidor
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

if __name__ == "__main__":
    main()