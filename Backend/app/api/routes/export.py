from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import logging
from datetime import datetime

from app.core.config import settings
from app.services.chart_generator import ChartGenerator
from app.services.pdf_generator import PDFGenerator  # Usamos ReportLab
from app.services.csv_processor import CSVProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

class PDFExportRequest(BaseModel):
    file_id: str
    include_charts: bool = True
    template_style: str = "professional"

@router.post("/export-pdf")
async def export_pdf(
    request: PDFExportRequest,
    background_tasks: BackgroundTasks
):
    """
    Genera un informe PDF profesional usando ReportLab
    """
    try:
        file_id = request.file_id
        include_charts = request.include_charts
        
        logger.info(f"Iniciando exportación para file_id: {file_id}")
        
        # Verificar archivos
        temp_dir = os.path.join(settings.TEMP_FILE_PATH, file_id)
        if not os.path.exists(temp_dir):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Buscar CSV
        csv_files = [f for f in os.listdir(temp_dir) if f.endswith('.csv')]
        if not csv_files:
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        csv_path = os.path.join(temp_dir, csv_files[0])
        
        # Cargar análisis si existe
        analysis_path = os.path.join(temp_dir, "analysis_result.json")
        analysis_data = {}
        if os.path.exists(analysis_path):
            with open(analysis_path, 'r') as f:
                analysis_data = json.load(f)
            logger.info(f"Análisis cargado: {len(analysis_data.get('metrics', []))} métricas")
        else:
            logger.warning("No se encontró análisis previo, usando datos básicos")
            processor = CSVProcessor()
            df = processor.load_csv(csv_path)
            analysis_data = {
                "summary": f"Análisis de datos con {len(df)} filas y {len(df.columns)} columnas",
                "total_rows": len(df),
                "total_columns": len(df.columns)
            }
        
        # Cargar datos para gráficos
        processor = CSVProcessor()
        df = processor.load_csv(csv_path)
        
        # Generar gráficos si se solicitan
        chart_paths = []
        if include_charts:
            chart_generator = ChartGenerator()
            chart_paths = chart_generator.generate_charts(df, analysis_data)
            logger.info(f"Generados {len(chart_paths)} gráficos")
        
        # Generar PDF usando ReportLab (sin LaTeX)
        pdf_generator = PDFGenerator()
        pdf_path = pdf_generator.generate_pdf(file_id, analysis_data, chart_paths)
        
        if not pdf_path or not os.path.exists(pdf_path):
            logger.error("No se generó el PDF")
            raise HTTPException(
                status_code=500,
                detail="Error generating PDF"
            )
        
        logger.info(f"PDF generado exitosamente: {pdf_path}")
        
        # Devolver el PDF
        return FileResponse(
            path=pdf_path,
            filename=f"informe_analisis_{file_id}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando PDF: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error generando PDF: {str(e)}"
        )

@router.get("/export/{file_id}/status")
async def get_export_status(file_id: str):
    """
    Verifica el estado de la exportación
    """
    pdf_dir = os.path.join(os.getcwd(), "temp", "pdf")
    pdf_path = os.path.join(pdf_dir, f"informe_{file_id}.pdf")
    
    if os.path.exists(pdf_path):
        return {
            "file_id": file_id,
            "status": "completed",
            "pdf_url": f"/api/export/{file_id}/download"
        }
    else:
        return {
            "file_id": file_id,
            "status": "not_found"
        }

@router.get("/export/{file_id}/download")
async def download_pdf(file_id: str):
    """
    Descarga el PDF generado
    """
    pdf_dir = os.path.join(os.getcwd(), "temp", "pdf")
    pdf_path = os.path.join(pdf_dir, f"informe_{file_id}.pdf")
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=pdf_path,
        filename=f"informe_analisis_{file_id}.pdf",
        media_type="application/pdf"
    )