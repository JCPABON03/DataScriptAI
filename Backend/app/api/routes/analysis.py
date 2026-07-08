from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional  # ← Añadir importación
import os
import json
import logging
from datetime import datetime

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.services.agents.data_analyzer import DataAnalyzerAgent
from app.services.csv_processor import CSVProcessor
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

class AnalysisRequestModel(BaseModel):
    file_id: str
    analysis_type: Optional[str] = "comprehensive"

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(
    request: AnalysisRequestModel,
    background_tasks: BackgroundTasks
):
    """
    Analiza los datos usando IA con Gemini
    """
    try:
        file_id = request.file_id
        
        # Verificar que existe el archivo
        temp_dir = os.path.join(settings.TEMP_FILE_PATH, file_id)
        if not os.path.exists(temp_dir):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Buscar archivo CSV
        csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
        if not csv_files:
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        csv_path = os.path.join(temp_dir, csv_files[0])
        
        # Cargar datos
        processor = CSVProcessor()
        df = processor.load_csv(csv_path)
        
        # Inicializar agente analizador
        analyzer = DataAnalyzerAgent()
        
        # Realizar análisis
        logger.info(f"Iniciando análisis para file_id: {file_id}")
        analysis_result = await analyzer.analyze(df)
        
        # Guardar resultados
        results_path = os.path.join(temp_dir, "analysis_result.json")
        with open(results_path, 'w') as f:
            json.dump(analysis_result, f, default=str)
        
        # Crear respuesta
        response = AnalysisResponse(
            file_id=file_id,
            summary=analysis_result.get('summary', ''),
            metrics=analysis_result.get('metrics', []),
            insights=analysis_result.get('insights', []),
            anomalies=analysis_result.get('anomalies', []),
            recommendations=analysis_result.get('recommendations', []),
            charts_data=analysis_result.get('charts_data', {}),
            analyzed_at=datetime.now()
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en el análisis: {str(e)}"
        )

@router.get("/analyze/{file_id}/results")
async def get_analysis_results(file_id: str):
    """
    Obtiene los resultados del análisis previamente realizado
    """
    temp_dir = os.path.join(settings.TEMP_FILE_PATH, file_id)
    results_path = os.path.join(temp_dir, "analysis_result.json")
    
    if not os.path.exists(results_path):
        raise HTTPException(status_code=404, detail="Analysis results not found")
    
    try:
        with open(results_path, 'r') as f:
            results = json.load(f)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading analysis results: {str(e)}"
        )