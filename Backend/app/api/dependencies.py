from fastapi import Request, HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def verify_api_key(request: Request):
    """Verifica la API Key si está configurada"""
    api_key = request.headers.get("X-API-Key")
    expected_key = request.app.state.api_key if hasattr(request.app.state, 'api_key') else None
    
    if expected_key and api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

async def verify_file_size(request: Request):
    """Verifica el tamaño máximo del archivo"""
    content_length = request.headers.get("content-length")
    if content_length:
        size = int(content_length)
        max_size = request.app.state.max_upload_size if hasattr(request.app.state, 'max_upload_size') else 10485760
        if size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {max_size / 1024 / 1024:.1f}MB"
            )
    return True