import json
from typing import Any, Dict, List
from datetime import datetime, date
import numpy as np
import pandas as pd

class JSONEncoder(json.JSONEncoder):
    """
    JSON Encoder personalizado para tipos no serializables
    """
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        if hasattr(obj, 'dict'):
            return obj.dict()
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)

def safe_json_dumps(data: Any, **kwargs) -> str:
    """
    Convierte datos a JSON de manera segura
    """
    return json.dumps(data, cls=JSONEncoder, **kwargs)

def safe_json_loads(data: str) -> Any:
    """
    Carga JSON de manera segura
    """
    try:
        return json.loads(data)
    except:
        return None

def format_number(value: float, decimals: int = 2) -> str:
    """
    Formatea números con separadores
    """
    if value is None:
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:,.{decimals}f}"
    return str(value)

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca texto a una longitud máxima
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def clean_column_name(name: str) -> str:
    """
    Limpia nombres de columnas
    """
    import re
    # Reemplazar espacios y caracteres especiales
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.lower().strip()

def detect_separator(file_content: str) -> str:
    """
    Detecta el separador de un archivo CSV
    """
    candidates = [',', ';', '\t', '|']
    for sep in candidates:
        if file_content.count(sep) > 10:
            return sep
    return ','  # Default