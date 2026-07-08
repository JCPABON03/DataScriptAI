import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class CSVProcessor:
    def __init__(self):
        self.df = None
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Carga un archivo CSV y lo procesa
        """
        try:
            # Intentar con diferentes codificaciones
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"CSV cargado con encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("No se pudo leer el archivo CSV con ninguna codificación")
            
            # Limpieza básica
            df = df.replace([np.inf, -np.inf], np.nan)
            
            self.df = df
            return df
            
        except Exception as e:
            logger.error(f"Error cargando CSV: {str(e)}")
            raise
    
    def get_preview(self, df: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene una vista previa de los datos
        """
        return df.head(n).replace({np.nan: None}).to_dict(orient='records')
    
    def get_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula estadísticas básicas del DataFrame
        """
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
            "null_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist(),
            "datetime_columns": df.select_dtypes(include=['datetime64']).columns.tolist(),
        }
        
        # Estadísticas numéricas
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            stats["numeric_stats"] = numeric_df.describe().replace({np.nan: None}).to_dict()
            
            # Correlación si hay suficientes columnas
            if len(numeric_df.columns) > 1:
                try:
                    stats["correlation"] = numeric_df.corr().replace({np.nan: None}).to_dict()
                except:
                    pass
        
        return stats
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia los datos del DataFrame
        """
        df_clean = df.copy()
        
        # Eliminar columnas completamente vacías
        df_clean = df_clean.dropna(axis=1, how='all')
        
        # Eliminar filas duplicadas
        df_clean = df_clean.drop_duplicates()
        
        # Convertir fechas si es posible
        for col in df_clean.columns:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col])
            except:
                pass
        
        return df_clean
    
    def get_column_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtiene información detallada de cada columna
        """
        column_info = {}
        
        for col in df.columns:
            col_data = df[col]
            col_type = str(col_data.dtype)
            
            info = {
                "type": col_type,
                "null_count": int(col_data.isnull().sum()),
                "unique_count": int(col_data.nunique()),
                "null_percentage": float(col_data.isnull().sum() / len(df) * 100),
            }
            
            # Para columnas numéricas
            if pd.api.types.is_numeric_dtype(col_data):
                info.update({
                    "min": float(col_data.min()) if not col_data.isnull().all() else None,
                    "max": float(col_data.max()) if not col_data.isnull().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
                    "std": float(col_data.std()) if not col_data.isnull().all() else None,
                })
            
            # Para columnas categóricas
            elif pd.api.types.is_string_dtype(col_data):
                if col_data.nunique() <= 10:
                    info["top_values"] = col_data.value_counts().head(5).to_dict()
            
            column_info[col] = info
        
        return column_info