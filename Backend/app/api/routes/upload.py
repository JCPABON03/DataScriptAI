from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List  # ← Añadir importación
import os
import shutil
import logging
from datetime import datetime

from app.core.config import settings
from app.core.security import generate_file_id, validate_file_type, sanitize_filename
from app.models.schemas import CSVUploadResponse
from app.services.csv_processor import CSVProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ['.csv', '.tsv']

@router.post("/upload", response_model=CSVUploadResponse)
async def upload_csv(
    file: UploadFile = File(..., description="Archivo CSV a subir")
):
    """
    Sube un archivo CSV para su procesamiento y análisis
    """
    try:
        # Validar extensión
        if not validate_file_type(file.filename, ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no permitido. Permitidos: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Sanitizar nombre
        safe_filename = sanitize_filename(file.filename)
        file_id = generate_file_id()
        
        # Crear directorio temporal
        temp_dir = os.path.join(settings.TEMP_FILE_PATH, file_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Guardar archivo
        file_path = os.path.join(temp_dir, safe_filename)
        
        # Leer contenido para evitar problemas de codificación
        content = await file.read()
        
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Archivo demasiado grande. Máximo: {settings.MAX_UPLOAD_SIZE / 1024 / 1024:.1f}MB"
            )
        
        # Guardar archivo
        with open(file_path, 'wb') as f:
            f.write(content)
        
        logger.info(f"Archivo guardado: {file_path} ({len(content)} bytes)")
        
        # Procesar CSV
        processor = CSVProcessor()
        try:
            df = processor.load_csv(file_path)
            preview = processor.get_preview(df, n=5)
            stats = processor.get_basic_stats(df)
            
            response = CSVUploadResponse(
                file_id=file_id,
                filename=safe_filename,
                rows=len(df),
                columns=len(df.columns),
                column_names=df.columns.tolist(),
                preview=preview,
                stats=stats,
                uploaded_at=datetime.now()
            )
            
            # Guardar metadata en archivo
            import json
            metadata_path = os.path.join(temp_dir, "metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(response.dict(), f, default=str)
            
            return response
            
        except Exception as e:
            logger.error(f"Error procesando CSV: {str(e)}")
            raise HTTPException(
                status_code=422,
                detail=f"Error procesando el archivo CSV: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )

@router.get("/upload/{file_id}/status")
async def get_upload_status(file_id: str):
    """
    Verifica el estado de un archivo subido
    """
    temp_dir = os.path.join(settings.TEMP_FILE_PATH, file_id)
    
    if not os.path.exists(temp_dir):
        raise HTTPException(status_code=404, detail="File not found")
    
    metadata_path = os.path.join(temp_dir, "metadata.json")
    if os.path.exists(metadata_path):
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return {
            "file_id": file_id,
            "exists": True,
            "metadata": metadata,
            "status": "available"
        }
    
    return {
        "file_id": file_id,
        "exists": True,
        "status": "processing"
    }