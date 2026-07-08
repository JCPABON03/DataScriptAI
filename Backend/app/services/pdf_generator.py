from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Genera informes en PDF con un diseño minimalista y profesional,
    usando ReportLab.
    """

    # Paleta reducida: un color de acento y escala de grises
    COLOR_TEXT = colors.HexColor('#1A1A1A')       # texto principal, casi negro
    COLOR_MUTED = colors.HexColor('#6B6B6B')       # texto secundario / labels
    COLOR_ACCENT = colors.HexColor('#2F3E46')      # acento único (gris azulado oscuro)
    COLOR_LINE = colors.HexColor('#DADADA')        # líneas divisorias sutiles
    COLOR_ROW_ALT = colors.HexColor('#FAFAFA')     # fondo alterno de tabla, casi blanco

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._build_styles()

    def _build_styles(self):
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=self.COLOR_TEXT,
            alignment=TA_LEFT,
            spaceAfter=6,
            leading=26,
        )

        self.subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=self.COLOR_MUTED,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        self.meta_style = ParagraphStyle(
            'Meta',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=self.COLOR_MUTED,
            alignment=TA_LEFT,
        )

        self.section_style = ParagraphStyle(
            'Section',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=self.COLOR_TEXT,
            spaceBefore=22,
            spaceAfter=10,
            leading=16,
        )

        self.body_style = ParagraphStyle(
            'Body',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=self.COLOR_TEXT,
            alignment=TA_JUSTIFY,
            leading=14,
            spaceAfter=6,
        )

        self.body_muted_style = ParagraphStyle(
            'BodyMuted',
            parent=self.body_style,
            textColor=self.COLOR_MUTED,
        )

        self.table_header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            textColor=colors.white,
            alignment=TA_LEFT,
        )

        self.table_cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            textColor=self.COLOR_TEXT,
            alignment=TA_LEFT,
            leading=13,
        )

        self.caption_style = ParagraphStyle(
            'Caption',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            textColor=self.COLOR_MUTED,
            alignment=TA_CENTER,
            spaceAfter=16,
        )

        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=self.COLOR_MUTED,
            alignment=TA_CENTER,
        )

    def _divider(self, width=6.5 * inch, weight=0.6, color=None):
        color = color or self.COLOR_LINE
        return Table([['']], colWidths=[width], style=[
            ('LINEABOVE', (0, 0), (-1, -1), weight, color),
        ])

    def _priority_label(self, priority: str) -> str:
        return {
            'high': 'Prioridad alta',
            'medium': 'Prioridad media',
            'low': 'Prioridad baja',
        }.get(priority, 'Prioridad media')

    def generate_pdf(self, file_id: str, analysis_data: Dict[str, Any], chart_paths: List[str]) -> str:
        """
        Genera un informe en PDF a partir de los resultados de un análisis de datos.
        """
        try:
            pdf_dir = os.path.join(os.getcwd(), "temp", "pdf")
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = os.path.join(pdf_dir, f"informe_{file_id}.pdf")

            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=64,
                leftMargin=64,
                topMargin=64,
                bottomMargin=56,
            )

            story = []

            # ============ ENCABEZADO ============
            story.append(Paragraph("Informe de análisis de datos", self.title_style))
            story.append(Paragraph("Generado automáticamente a partir del conjunto de datos analizado", self.subtitle_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(
                f"Fecha de generación: {datetime.now().strftime('%d de %B de %Y, %H:%M')} &nbsp;·&nbsp; Versión del informe: 1.0",
                self.meta_style
            ))
            story.append(Spacer(1, 14))
            story.append(self._divider(weight=1, color=self.COLOR_ACCENT))
            story.append(Spacer(1, 8))

            # ============ RESUMEN EJECUTIVO ============
            story.append(Paragraph("Resumen ejecutivo", self.section_style))
            summary = analysis_data.get(
                'summary',
                'No se generó un resumen para este análisis.'
            )
            story.append(Paragraph(summary, self.body_style))

            # ============ MÉTRICAS CLAVE ============
            story.append(Paragraph("Métricas clave", self.section_style))
            metrics = analysis_data.get('metrics', [])

            if metrics:
                metric_data = [[
                    Paragraph('MÉTRICA', self.table_header_style),
                    Paragraph('VALOR', self.table_header_style),
                    Paragraph('DESCRIPCIÓN', self.table_header_style),
                ]]

                for metric in metrics[:8]:
                    name = metric.get('name', '')
                    value = metric.get('value', '')
                    if isinstance(value, (int, float)):
                        value = f"{value:,.2f}"
                    description = metric.get('description', '')
                    metric_data.append([
                        Paragraph(name, self.table_cell_style),
                        Paragraph(str(value), self.table_cell_style),
                        Paragraph(description, self.table_cell_style),
                    ])

                table = Table(metric_data, colWidths=[1.6 * inch, 1.3 * inch, 2.6 * inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_ACCENT),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLOR_ROW_ALT]),
                    ('LINEBELOW', (0, 0), (-1, 0), 0.6, self.COLOR_ACCENT),
                    ('LINEBELOW', (0, 1), (-1, -1), 0.4, self.COLOR_LINE),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(table)
            else:
                story.append(Paragraph("No hay métricas disponibles para este conjunto de datos.", self.body_muted_style))

            # ============ INSIGHTS ============
            story.append(Paragraph("Hallazgos principales", self.section_style))
            insights = analysis_data.get('insights', [])

            if insights:
                for idx, insight in enumerate(insights[:8]):
                    title = insight.get('title', '')
                    desc = insight.get('description', '')
                    priority = insight.get('priority', 'medium')

                    story.append(Paragraph(
                        f'<b>{title}</b> &nbsp;<font size="8" color="#6B6B6B">— {self._priority_label(priority)}</font>',
                        self.body_style
                    ))
                    story.append(Paragraph(desc, self.body_muted_style))
                    if idx < len(insights[:8]) - 1:
                        story.append(Spacer(1, 4))
                        story.append(self._divider(width=6.5 * inch, weight=0.3))
                        story.append(Spacer(1, 4))
            else:
                story.append(Paragraph("No se identificaron hallazgos relevantes.", self.body_muted_style))

            # ============ ANOMALÍAS ============
            story.append(Paragraph("Anomalías detectadas", self.section_style))
            anomalies = analysis_data.get('anomalies', [])

            if anomalies:
                for anomaly in anomalies[:5]:
                    col = anomaly.get('column', 'columna desconocida')
                    count = anomaly.get('outliers_count', 0)
                    pct = anomaly.get('percentage', 0)
                    story.append(Paragraph(
                        f'<b>{col}</b> — {count} valores atípicos ({pct:.1f}% de los registros)',
                        self.body_style
                    ))
            else:
                story.append(Paragraph("No se detectaron anomalías significativas en los datos.", self.body_muted_style))

            # ============ GRÁFICOS ============
            if chart_paths:
                story.append(Paragraph("Visualizaciones", self.section_style))

                for i, chart_path in enumerate(chart_paths):
                    if os.path.exists(chart_path):
                        try:
                            img = Image(chart_path, width=6.3 * inch, height=3.8 * inch)
                            story.append(img)
                            story.append(Paragraph(f"Figura {i + 1}", self.caption_style))
                        except Exception as e:
                            logger.error(f"Error agregando gráfico {i + 1}: {str(e)}")
                            story.append(Paragraph(f"No se pudo cargar la figura {i + 1}.", self.body_muted_style))

            # ============ RECOMENDACIONES ============
            story.append(PageBreak())
            story.append(Paragraph("Recomendaciones", self.section_style))
            recommendations = analysis_data.get('recommendations', [])

            if recommendations:
                for i, rec in enumerate(recommendations[:6], 1):
                    story.append(Paragraph(f'<b>{i}.</b> &nbsp;{rec}', self.body_style))
            else:
                story.append(Paragraph("No hay recomendaciones disponibles para este análisis.", self.body_muted_style))

            # ============ PIE DE PÁGINA ============
            story.append(Spacer(1, 24))
            story.append(self._divider(weight=0.4))
            story.append(Spacer(1, 6))
            story.append(Paragraph(
                "Informe generado automáticamente por el sistema de análisis de datos.",
                self.footer_style
            ))

            doc.build(story)
            logger.info(f"PDF generado exitosamente: {pdf_path}")

            return pdf_path

        except Exception as e:
            logger.error(f"Error generando PDF con ReportLab: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise