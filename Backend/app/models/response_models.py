from pydantic import BaseModel
from typing import Optional, Any  # ← Añadir importaciones

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    timestamp: str