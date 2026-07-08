import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """
    Maneja operaciones con archivos
    """
    
    @staticmethod
    def create_temp_directory(prefix: str = "temp_") -> str:
        """
        Crea un directorio temporal
        """
        temp_dir = tempfile.mkdtemp(prefix=prefix)
        logger.info(f"Directorio temporal creado: {temp_dir}")
        return temp_dir
    
    @staticmethod
    def delete_directory(path: str):
        """
        Elimina un directorio y su contenido
        """
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                logger.info(f"🧹 Directorio eliminado: {path}")
        except Exception as e:
            logger.error(f"Error eliminando directorio {path}: {str(e)}")
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Obtiene el tamaño de un archivo en bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Error obteniendo tamaño de {file_path}: {str(e)}")
            return 0
    
    @staticmethod
    def is_valid_path(path: str) -> bool:
        """
        Verifica si una ruta existe y es válida
        """
        return os.path.exists(path) and os.path.isdir(path)
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """
        Asegura que un directorio existe, creándolo si es necesario
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creando directorio {path}: {str(e)}")
            return False
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """
        Genera un nombre de archivo seguro
        """
        import re
        # Remover caracteres peligrosos
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        # Limitar longitud
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        return filename