import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import logging
from typing import List, Dict, Any, Optional  # ← Añadir importaciones
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)

class ChartGenerator:
    """
    Genera gráficos profesionales para el informe
    """
    
    def __init__(self):
        # Configurar estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        sns.set_palette(sns.color_palette(self.colors))
        
        # Crear directorio para gráficos
        self.charts_dir = Path(settings.LATEX_TEMP_PATH) / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_charts(
        self,
        df: pd.DataFrame,
        analysis: Dict[str, Any],
        max_charts: int = 4
    ) -> List[str]:
        """
        Genera múltiples gráficos basados en los datos
        """
        chart_paths = []
        
        # Seleccionar columnas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        charts_generated = 0
        
        # 1. Distribución de la primera columna numérica
        if numeric_cols and charts_generated < max_charts:
            col = numeric_cols[0]
            path = self._create_distribution_chart(df, col)
            if path:
                chart_paths.append(path)
                charts_generated += 1
        
        # 2. Boxplot de la segunda columna numérica
        if len(numeric_cols) > 1 and charts_generated < max_charts:
            col = numeric_cols[1]
            path = self._create_boxplot_chart(df, col)
            if path:
                chart_paths.append(path)
                charts_generated += 1
        
        # 3. Correlación (si hay suficientes columnas numéricas)
        if len(numeric_cols) >= 3 and charts_generated < max_charts:
            path = self._create_correlation_chart(df, numeric_cols[:8])
            if path:
                chart_paths.append(path)
                charts_generated += 1
        
        # 4. Gráfico de barras para datos categóricos
        if categorical_cols and charts_generated < max_charts:
            col = categorical_cols[0]
            if df[col].nunique() <= 10:
                path = self._create_bar_chart(df, col)
                if path:
                    chart_paths.append(path)
                    charts_generated += 1
        
        # 5. Tendencias (time series)
        if charts_generated < max_charts:
            # Buscar columnas de fecha
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            if date_cols and numeric_cols:
                date_col = date_cols[0]
                num_col = numeric_cols[0]
                path = self._create_trend_chart(df, date_col, num_col)
                if path:
                    chart_paths.append(path)
                    charts_generated += 1
        
        logger.info(f"Generados {len(chart_paths)} gráficos")
        return chart_paths
    
    def _create_distribution_chart(self, df: pd.DataFrame, column: str) -> Optional[str]:
        """
        Crea un histograma con curva de densidad
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Histograma
            sns.histplot(
                data=df,
                x=column,
                kde=True,
                color=self.colors[0],
                bins=30,
                ax=ax
            )
            
            # Línea de media
            mean_val = df[column].mean()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Media: {mean_val:.2f}')
            
            ax.set_title(f'Distribución de {column}', fontsize=14, fontweight='bold')
            ax.set_xlabel(column, fontsize=12)
            ax.set_ylabel('Frecuencia', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            return self._save_chart(fig, f'distribution_{column}')
        except Exception as e:
            logger.error(f"Error creando distribución: {str(e)}")
            return None
    
    def _create_boxplot_chart(self, df: pd.DataFrame, column: str) -> Optional[str]:
        """
        Crea un boxplot para detectar outliers
        """
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            sns.boxplot(
                data=df,
                y=column,
                color=self.colors[1],
                ax=ax
            )
            
            ax.set_title(f'Boxplot de {column}', fontsize=14, fontweight='bold')
            ax.set_ylabel(column, fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            
            return self._save_chart(fig, f'boxplot_{column}')
        except Exception as e:
            logger.error(f"Error creando boxplot: {str(e)}")
            return None
    
    def _create_correlation_chart(self, df: pd.DataFrame, columns: List[str]) -> Optional[str]:
        """
        Crea un heatmap de correlación
        """
        try:
            # Calcular correlación
            corr = df[columns].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Heatmap
            sns.heatmap(
                corr,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
                ax=ax
            )
            
            ax.set_title('Matriz de Correlación', fontsize=14, fontweight='bold')
            
            return self._save_chart(fig, 'correlation_heatmap')
        except Exception as e:
            logger.error(f"Error creando heatmap: {str(e)}")
            return None
    
    def _create_bar_chart(self, df: pd.DataFrame, column: str) -> Optional[str]:
        """
        Crea un gráfico de barras para datos categóricos
        """
        try:
            # Contar valores
            value_counts = df[column].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Barras
            bars = ax.bar(
                value_counts.index.astype(str),
                value_counts.values,
                color=self.colors[:len(value_counts)],
                edgecolor='black',
                linewidth=1
            )
            
            # Agregar valores
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + 0.5,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    fontsize=10
                )
            
            ax.set_title(f'Distribución de {column}', fontsize=14, fontweight='bold')
            ax.set_xlabel(column, fontsize=12)
            ax.set_ylabel('Frecuencia', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Rotar etiquetas si son largas
            if len(max(value_counts.index.astype(str), key=len)) > 10:
                plt.xticks(rotation=45, ha='right')
            
            return self._save_chart(fig, f'bar_{column}')
        except Exception as e:
            logger.error(f"Error creando barras: {str(e)}")
            return None
    
    def _create_trend_chart(self, df: pd.DataFrame, date_col: str, value_col: str) -> Optional[str]:
        """
        Crea un gráfico de tendencia temporal
        """
        try:
            # Agrupar por fecha
            df_grouped = df.groupby(date_col)[value_col].mean().reset_index()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Línea de tendencia
            ax.plot(
                df_grouped[date_col].astype(str),
                df_grouped[value_col],
                marker='o',
                linestyle='-',
                linewidth=2,
                markersize=6,
                color=self.colors[3],
                label=value_col
            )
            
            # Línea de tendencia (media móvil)
            if len(df_grouped) > 5:
                df_grouped['rolling'] = df_grouped[value_col].rolling(window=3, center=True).mean()
                ax.plot(
                    df_grouped[date_col].astype(str),
                    df_grouped['rolling'],
                    linestyle='--',
                    linewidth=2,
                    color=self.colors[4],
                    alpha=0.7,
                    label='Media móvil (3)'
                )
            
            ax.set_title(f'Tendencia de {value_col} en el tiempo', fontsize=14, fontweight='bold')
            ax.set_xlabel(date_col, fontsize=12)
            ax.set_ylabel(value_col, fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            return self._save_chart(fig, f'trend_{value_col}')
        except Exception as e:
            logger.error(f"Error creando tendencia: {str(e)}")
            return None
    
    def _save_chart(self, fig, name: str) -> Optional[str]:
        """
        Guarda el gráfico como imagen
        """
        try:
            # Limpiar nombre
            clean_name = ''.join(c for c in name if c.isalnum() or c in '_-')
            filename = f"{clean_name}.png"
            filepath = self.charts_dir / filename
            
            # Guardar con alta calidad
            fig.savefig(
                filepath,
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none'
            )
            plt.close(fig)
            
            return str(filepath)
        except Exception as e:
            logger.error(f"Error guardando gráfico: {str(e)}")
            plt.close(fig)
            return None