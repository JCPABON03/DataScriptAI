import hashlib
import uuid
from datetime import datetime
from typing import Optional, List  # ← Añadir List
import secrets

def generate_file_id() -> str:
    """Genera un ID único para archivos"""
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def generate_secure_filename(original_filename: str) -> str:
    """Genera un nombre de archivo seguro"""
    ext = original_filename.split('.')[-1] if '.' in original_filename else ''
    file_id = generate_file_id()
    return f"{file_id}.{ext}" if ext else file_id

def calculate_file_hash(file_content: bytes) -> str:
    """Calcula el hash SHA-256 del contenido del archivo"""
    return hashlib.sha256(file_content).hexdigest()

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Valida que el archivo tenga una extensión permitida"""
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def sanitize_filename(filename: str) -> str:
    """Sanitiza el nombre del archivo eliminando caracteres peligrosos"""
    import re
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename[:255]  # Limitar longitud