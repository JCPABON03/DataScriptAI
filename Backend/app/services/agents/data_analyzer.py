import json
import logging
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
import re

from app.core.config import settings
from app.services.agents.base_agent import BaseAgent

# Intentar importar Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI no disponible")

logger = logging.getLogger(__name__)

class DataAnalyzerAgent(BaseAgent):
    """
    Agente que analiza datos usando Gemini AI
    """
    
    def __init__(self):
        super().__init__("DataAnalyzer")
        
        # Log de configuración
        logger.info(f"🔍 GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        logger.info(f"🔍 GEMINI_API_KEY: {'Configurada' if settings.GEMINI_API_KEY else '❌ No configurada'}")
        
        self.gemini_available = GEMINI_AVAILABLE and bool(settings.GEMINI_API_KEY)
        
        if self.gemini_available:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                
                # Listar modelos disponibles
                try:
                    available_models = genai.list_models()
                    model_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
                    logger.info(f"Modelos disponibles para generateContent: {model_names}")
                except Exception as e:
                    logger.warning(f"No se pudieron listar modelos: {str(e)}")
                    model_names = []
                
                # Probar diferentes modelos (usando los disponibles)
                test_models = [
                    'models/gemini-2.5-flash',
                    'models/gemini-2.0-flash',
                    'models/gemini-2.0-flash-lite',
                    'models/gemini-flash-latest'
                ]
                
                self.model = None
                for model_name in test_models:
                    try:
                        logger.info(f"Probando modelo: {model_name}")
                        test_model = genai.GenerativeModel(model_name)
                        # Probar con un mensaje simple
                        test_response = test_model.generate_content("Responde con OK")
                        if test_response and test_response.text:
                            self.model = test_model
                            logger.info(f"gemini configurado con modelo: {model_name}")
                            break
                    except Exception as e:
                        logger.warning(f"Modelo {model_name} no disponible: {str(e)}")
                
                # Si no funcionó, usar el primer modelo disponible de la lista
                if not self.model and model_names:
                    try:
                        first_model = model_names[0]
                        logger.info(f"Usando primer modelo disponible: {first_model}")
                        self.model = genai.GenerativeModel(first_model)
                        logger.info(f"Gemini configurado con modelo: {first_model}")
                    except Exception as e:
                        logger.error(f"Error usando modelo {first_model}: {str(e)}")
                
                if not self.model:
                    logger.error("No se encontró ningún modelo de Gemini disponible")
                    self.gemini_available = False
                
            except Exception as e:
                logger.error(f"Error configurando Gemini: {str(e)}")
                self.gemini_available = False
        else:
            if not GEMINI_AVAILABLE:
                logger.warning("Paquete google-generativeai no instalado")
                logger.warning("   Instalar con: pip install google-generativeai")
            if not settings.GEMINI_API_KEY:
                logger.warning("GEMINI_API_KEY no configurada en .env")
                logger.warning("   Asegúrate de que el archivo .env contenga GEMINI_API_KEY=tu_clave")
    
    def _clean_value(self, value: Any) -> float:
        """Limpia y convierte un valor a float"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Limpiar caracteres no numéricos
            cleaned = re.sub(r'[^\d.,-]', '', value)
            cleaned = cleaned.replace(',', '.')
            try:
                return float(cleaned)
            except:
                return 0.0
        return 0.0
    
    async def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza el DataFrame usando IA
        """
        self.log_start()
        
        logger.info(f"Analizando dataset con {len(df)} filas y {len(df.columns)} columnas")
        logger.info(f"gemini disponible: {self.gemini_available}")
        
        try:
            # Preparar datos para análisis
            data_summary = self._prepare_data_summary(df)
            
            # Intentar usar Gemini
            if self.gemini_available and self.model:
                try:
                    logger.info("🧠 Usando Gemini para el análisis...")
                    result = await self._analyze_with_gemini(data_summary, df)
                    if result and result.get('summary'):
                        # Limpiar y validar los datos
                        result = self._clean_analysis_result(result)
                        logger.info(f"Análisis con Gemini completado: {len(result.get('metrics', []))} métricas, {len(result.get('insights', []))} insights")
                        logger.info(f"Resumen: {result.get('summary', '')[:100]}...")
                        self.log_end()
                        return result
                    else:
                        logger.warning("Gemini devolvió resultado vacío, usando análisis básico")
                except Exception as e:
                    logger.error(f" Error con Gemini: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
                    logger.info("Usando análisis básico como fallback")
            else:
                logger.info("Usando análisis básico (sin IA)")
            
            # Fallback: análisis básico
            result = self._analyze_basic(df)
            self.log_end()
            return result
            
        except Exception as e:
            self.log_error(e)
            return self._analyze_basic(df)
    
    def _clean_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia y valida los resultados del análisis"""
        cleaned = result.copy()
        
        # Limpiar métricas
        if 'metrics' in cleaned and cleaned['metrics']:
            cleaned_metrics = []
            for metric in cleaned['metrics']:
                # Asegurar que value es numérico
                if 'value' in metric:
                    metric['value'] = self._clean_value(metric['value'])
                cleaned_metrics.append(metric)
            cleaned['metrics'] = cleaned_metrics
        
        # Asegurar que hay al menos algunas métricas
        if not cleaned.get('metrics') or len(cleaned['metrics']) == 0:
            cleaned['metrics'] = [
                {"name": "Total de registros", "value": float(result.get('total_rows', 0)), "description": "Número total de filas en el dataset"},
                {"name": "Columnas", "value": float(result.get('total_columns', 0)), "description": "Número total de columnas"}
            ]
        
        # Limpiar insights
        if 'insights' in cleaned and cleaned['insights']:
            for insight in cleaned['insights']:
                if 'priority' not in insight:
                    insight['priority'] = 'medium'
                if 'category' not in insight:
                    insight['category'] = 'general'
        
        return cleaned
    
    def _prepare_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Prepara un resumen de datos para el análisis
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        summary = {
            "shape": list(df.shape),
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "sample": df.head(10).replace({np.nan: None}).to_dict(orient='records'),
            "statistics": {},
        }
        
        # Estadísticas para columnas numéricas
        for col in numeric_cols[:5]:
            try:
                summary["statistics"][col] = {
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                }
            except:
                pass
        
        # Valores únicos para categóricas
        for col in categorical_cols[:5]:
            try:
                summary["statistics"][col] = {
                    "unique_values": df[col].nunique(),
                    "top_values": df[col].value_counts().head(3).to_dict()
                }
            except:
                pass
        
        return summary
    
    async def _analyze_with_gemini(self, data_summary: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
        """
        Usa Gemini para el análisis avanzado
        """
        # Crear un prompt más estructurado y específico
        prompt = f"""
        Eres un analista de datos experto. Analiza el siguiente conjunto de datos y devuelve un JSON válido con esta estructura exacta:

        {{
            "summary": "Un resumen ejecutivo de 2-3 párrafos sobre los datos, destacando los hallazgos más importantes",
            "metrics": [
                {{"name": "Nombre de la métrica", "value": numero, "description": "Breve descripción"}}
            ],
            "insights": [
                {{"title": "Título del insight", "description": "Descripción detallada", "priority": "high|medium|low", "category": "categoría"}}
            ],
            "anomalies": [
                {{"column": "Nombre de columna", "outliers_count": numero, "percentage": numero}}
            ],
            "recommendations": [
                "Recomendación 1",
                "Recomendación 2"
            ]
        }}

        REGLAS IMPORTANTES:
        1. El campo "value" en "metrics" DEBE ser un número (float), NO un string
        2. Ejemplo correcto: {{"name": "Ventas promedio", "value": 45678.5, "description": "..."}}
        3. Ejemplo incorrecto: {{"name": "Categoría", "value": "Electrónica", "description": "..."}}
        4. Solo incluye métricas que tengan valores numéricos
        5. Los números deben usar punto decimal (.), no coma (,)

        Datos del dataset:
        - Total de filas: {data_summary['shape'][0]}
        - Total de columnas: {data_summary['shape'][1]}
        - Columnas: {', '.join(data_summary['columns'])}
        - Columnas numéricas: {', '.join(data_summary['numeric_columns'])}
        - Columnas categóricas: {', '.join(data_summary['categorical_columns'])}
        - Estadísticas: {json.dumps(data_summary['statistics'], indent=2, default=str)}
        - Muestra de datos: {json.dumps(data_summary['sample'], indent=2, default=str)}

        IMPORTANTE: 
        1. Devuelve SOLO el JSON, sin texto adicional
        2. Los valores numéricos deben ser números, no strings
        3. Asegúrate de que el JSON sea válido
        4. Siempre incluye al menos 3 métricas, 3 insights y 2 recomendaciones
        5. LAS MÉTRICAS DEBEN SER SOLO NUMÉRICAS
        """
        
        logger.info(f"Enviando prompt a Gemini...")
        
        try:
            # Usar generate_content con el modelo configurado
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            logger.info(f"Respuesta recibida de Gemini ({len(result_text)} caracteres)")
            
            # Limpiar el texto para extraer JSON
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)
            else:
                # Intentar encontrar JSON sin llaves exteriores
                result_text = result_text.strip()
                if not result_text.startswith('{'):
                    # Buscar cualquier JSON válido
                    json_pattern = r'\{[^{}]*\}'
                    matches = re.findall(json_pattern, result_text)
                    if matches:
                        result_text = matches[0]
            
            # Parsear JSON
            result = json.loads(result_text)
            
            # Validar estructura mínima
            if not result.get('summary'):
                result['summary'] = "Análisis completado con IA"
            if not result.get('metrics'):
                result['metrics'] = []
            if not result.get('insights'):
                result['insights'] = []
            if not result.get('anomalies'):
                result['anomalies'] = []
            if not result.get('recommendations'):
                result['recommendations'] = []
            
            # Agregar metadatos
            result["total_rows"] = len(df)
            result["total_columns"] = len(df.columns)
            result["analyzed_with"] = "gemini"
            
            logger.info(f"Gemini generó {len(result.get('metrics', []))} métricas y {len(result.get('insights', []))} insights")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON de Gemini: {str(e)}")
            logger.error(f"Respuesta recibida: {result_text[:200]}...")
            raise
        except Exception as e:
            logger.error(f"Error en Gemini: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    def _analyze_basic(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Análisis básico sin IA (fallback)
        """
        logger.info("Generando análisis básico...")
        
        result = {
            "summary": f"Análisis básico del dataset con {len(df)} filas y {len(df.columns)} columnas.",
            "metrics": [],
            "insights": [],
            "anomalies": [],
            "recommendations": [],
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "analyzed_with": "basic"
        }
        
        # Métricas básicas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:5]:
            try:
                result["metrics"].append({
                    "name": col,
                    "value": float(df[col].mean()),
                    "description": f"Media de {col}"
                })
            except:
                pass
        
        # Asegurar que hay métricas
        if len(result["metrics"]) == 0:
            result["metrics"].append({
                "name": "Total de registros",
                "value": float(len(df)),
                "description": "Número total de filas"
            })
            result["metrics"].append({
                "name": "Total de columnas",
                "value": float(len(df.columns)),
                "description": "Número total de columnas"
            })
        
        # Insights básicos
        result["insights"].append({
            "title": "Resumen del dataset",
            "description": f"El dataset contiene {len(df)} filas y {len(df.columns)} columnas. {len(numeric_cols)} columnas numéricas y {len(df.select_dtypes(include=['object', 'category']).columns)} categóricas.",
            "priority": "medium",
            "category": "general"
        })
        
        if len(numeric_cols) > 0:
            result["insights"].append({
                "title": "Distribución de datos numéricos",
                "description": f"Las columnas numéricas principales son: {', '.join(numeric_cols[:3])}",
                "priority": "low",
                "category": "estadística"
            })
        
        # Anomalías básicas
        for col in numeric_cols:
            try:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
                if len(outliers) > 0:
                    result["anomalies"].append({
                        "column": col,
                        "outliers_count": int(len(outliers)),
                        "percentage": float(len(outliers) / len(df) * 100)
                    })
            except:
                pass
        
        # Recomendaciones
        result["recommendations"] = [
            "Revisar datos faltantes en el dataset",
            "Considerar normalización de datos numéricos",
            "Explorar relaciones entre variables usando visualizaciones"
        ]
        
        logger.info(f"Análisis básico completado: {len(result['metrics'])} métricas, {len(result['insights'])} insights")
        return result
    
    async def process(self, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Método principal del agente
        """
        if isinstance(data, pd.DataFrame):
            return await self.analyze(data)
        else:
            raise ValueError("Data must be a pandas DataFrame")