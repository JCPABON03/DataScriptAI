from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class CSVUploadResponse(BaseModel):
    file_id: str
    filename: str
    rows: int
    columns: int
    column_names: List[str]
    preview: List[Dict[str, Any]]
    stats: Dict[str, Any]
    uploaded_at: datetime

class AnalysisRequest(BaseModel):
    file_id: str
    analysis_type: Optional[str] = "comprehensive"
    focus_areas: Optional[List[str]] = None

class Metric(BaseModel):
    name: str
    value: float
    description: Optional[str] = None
    trend: Optional[str] = None
    
    @validator('value', pre=True)
    def parse_value(cls, v):
        """Convierte strings a float si es posible"""
        if isinstance(v, str):
            # Limpiar caracteres no numéricos
            import re
            cleaned = re.sub(r'[^\d.,-]', '', v)
            cleaned = cleaned.replace(',', '.')
            try:
                return float(cleaned)
            except:
                return 0.0
        return v

class Insight(BaseModel):
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    category: str

class AnalysisResponse(BaseModel):
    file_id: str
    summary: str
    metrics: List[Metric]
    insights: List[Insight]
    anomalies: List[Dict[str, Any]]
    recommendations: List[str]
    charts_data: Dict[str, Any]
    analyzed_at: datetime
    analyzed_with: Optional[str] = "basic"