# 📊 Analytics Dashboard - Análisis de Datos con IA

> Dashboard inteligente que analiza tus archivos CSV usando Google Gemini AI y genera informes profesionales en PDF

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green.svg)
![Gemini](https://img.shields.io/badge/gemini-AI-orange.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [🎯 ¿Qué hace?](#-qué-hace)
- [🚀 Demo Rápida](#-demo-rápida)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🛠️ Tecnologías](#️-tecnologías)
- [🔧 Instalación Detallada](#-instalación-detallada)
- [🔑 Obtener API Key de Gemini](#-obtener-api-key-de-gemini)
- [📊 Ejemplos de CSV](#-ejemplos-de-csv)
- [📋 Funcionalidades](#-funcionalidades)
- [📝 Endpoints API](#-endpoints-api)

---

## 🎯 ¿Qué hace?

Sube un archivo CSV y el sistema:

| Función | Descripción |
|---|---|
| 🤖 **Analiza** | Datos con IA (Gemini) generando insights automáticos |
| 📊 **Visualiza** | Gráficos interactivos (barras, circular, líneas) |
| 💡 **Detecta** | Insights, anomalías y patrones en los datos |
| 📄 **Exporta** | Informes PDF profesionales con métricas y gráficos |
| 📁 **Procesa** | Archivos CSV/TSV de hasta 10MB |

---

## 🚀 Demo Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/JCPABON03/analytics-dashboard.git
cd analytics-dashboard

# 2. Backend
cd Backend
pip install -r requirements.txt
python run.py

# 3. Frontend (en otra terminal)
cd Fronted
npm install
npm run dev


```

---

## 📁 Estructura del Proyecto

```text
analytics-dashboard/
├── Backend/                          # API con FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── upload.py        # Carga de archivos CSV
│   │   │       ├── analysis.py      # Análisis con IA
│   │   │       └── export.py        # Exportación a PDF
│   │   ├── core/
│   │   │   ├── config.py            # Configuración
│   │   │   └── security.py          # Seguridad
│   │   ├── models/
│   │   │   └── schemas.py           # Modelos de datos
│   │   ├── services/
│   │   │   ├── agents/
│   │   │   │   ├── base_agent.py
│   │   │   │   └── data_analyzer.py # Agente de análisis IA
│   │   │   ├── csv_processor.py     # Procesamiento CSV
│   │   │   ├── chart_generator.py   # Generación de gráficos
│   │   │   └── pdf_generator.py     # Generación de PDFs
│   │   └── utils/
│   ├── temp/                        # Archivos temporales
│   ├── .env                         # Variables de entorno
│   ├── .env.example
│   ├── requirements.txt
│   ├── run.py
│   └── test_api.py
├── Fronted/                         # UI con React + Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/              # Componentes reutilizables
│   │   │   │   ├── ConnectionStatus.jsx
│   │   │   │   └── LoadingSpinner.jsx
│   │   │   ├── Dashboard/           # Dashboard principal
│   │   │   │   ├── ChartsSection.jsx
│   │   │   │   ├── InsightsPanel.jsx
│   │   │   │   └── MetricsCards.jsx
│   │   │   ├── Export/              # Exportación a PDF
│   │   │   │   └── PDFExportButton.jsx
│   │   │   └── Upload/              # Carga de CSV
│   │   │       └── CSVUploader.jsx
│   │   ├── hooks/
│   │   │   ├── useApi.js
│   │   │   ├── useAnalysis.js
│   │   │   └── usePdfExport.js
│   │   ├── services/
│   │   │   └── api.js               # Cliente API
│   │   ├── store/                   # Zustand state
│   │   ├── styles/
│   │   │   └── index.css            # Estilos globales
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
├── .gitignore
├── LICENSE
├── README.md
└── start.sh
```

---

## 🛠️ Tecnologías

### Backend

| Tecnología | Versión | Uso |
|---|---|---|
| FastAPI | 0.104.1 | Framework web moderno |
| Google Gemini AI | 0.3.2 | Análisis inteligente |
| Pandas | 2.2.0 | Procesamiento de datos |
| Matplotlib | 3.8.2 | Generación de gráficos |
| Seaborn | 0.13.2 | Visualización avanzada |
| ReportLab | 4.0.7 | Generación de PDFs |
| Pydantic | 2.5.3 | Validación de datos |
| Uvicorn | 0.24.0 | Servidor ASGI |

### Frontend

| Tecnología | Versión | Uso |
|---|---|---|
| React | 18.2.0 | UI moderna |
| Vite | 5.0.8 | Build tool ultrarrápido |
| Tailwind CSS | 3.4.1 | Estilos y diseño |
| Recharts | 2.10.3 | Gráficos interactivos |
| Axios | 1.6.5 | Cliente HTTP |
| Zustand | 4.4.7 | Gestión de estado |
| Lucide React | 0.309.0 | Iconos |

---

## 🔧 Instalación Detallada

### Requisitos Previos

- Python 3.11+
- Node.js 18+
- npm o yarn
- Git

### 1. Backend

```bash
cd Backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
nano .env  # o usa tu editor favorito

# Crear directorios temporales
mkdir -p temp/pdf

# Ejecutar el servidor
python run.py
```

### 2. Frontend

```bash
cd Fronted

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
nano .env  # o usa tu editor favorito

# Ejecutar el servidor de desarrollo
npm run dev
```


---

## 🔑 Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://aistudio.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Get API Key"** en la esquina superior derecha
4. Crea una nueva API Key
5. Copia la clave generada
6. Pégala en `Backend/.env`:

```env
GEMINI_API_KEY=tu_clave_aqui
```

### Verificar que funciona

```bash
cd Backend
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Responde con OK')
print('✅ Gemini funciona:', response.text)
"
```

---

## 📊 Ejemplos de CSV

### Ventas de Productos

```csv
mes,producto,categoria,ventas,unidades,precio_promedio,region,canal
Enero,Smartphone X,Electrónica,42500,85,500.00,Norte,Online
Enero,Tablet Pro,Electrónica,31200,48,650.00,Sur,Online
Enero,Laptop Gamer,Electrónica,58900,38,1550.00,Este,Físico
Enero,Smart TV 4K,Electrónica,87900,15,5860.00,Norte,Físico
Febrero,Smartphone X,Electrónica,52300,95,550.00,Norte,Online
Febrero,Laptop Gamer,Electrónica,75600,42,1800.00,Este,Físico
```

### Pacientes Hospitalarios

```csv
paciente_id,edad,genero,diagnostico,departamento,fecha_ingreso,fecha_alta,dias_internacion,estado_alta,costo_tratamiento,comorbilidades,urgencias
P001,65,M,Neumonía,Medicina Interna,2024-01-15,2024-01-22,7,Alta,24500,Diabetes,No
P002,72,F,Insuficiencia Cardíaca,Cardiología,2024-01-18,2024-01-28,10,Alta,38900,Hipertensión,No
P003,45,M,Apendicitis,Cirugía,2024-01-20,2024-01-24,4,Alta,15900,Ninguna,Si
```

### Ventas Mensuales (Simple)

```csv
mes,ventas_totales,clientes_activos,productos_vendidos,tasa_crecimiento
Enero,125000,145,320,0
Febrero,156000,178,389,24.8
Marzo,198000,210,456,26.9
Abril,234000,267,523,18.2
Mayo,289000,312,678,23.5
```

---

## 📋 Funcionalidades

### Análisis con IA

| Característica | Descripción |
|---|---|
| 🤖 Resumen Ejecutivo | Análisis textual generado por Gemini |
| 📊 Métricas Clave | Promedios, medianas y estadísticas relevantes |
| 💡 Insights | Hallazgos importantes con prioridad (alta/media/baja) |
| ⚠️ Anomalías | Detección de valores atípicos |
| 📋 Recomendaciones | Sugerencias accionables basadas en los datos |

### Visualizaciones

| Tipo | Descripción |
|---|---|
| 📊 Barras | Comparación de métricas |
| 🥧 Circular | Distribución de datos |
| 📈 Líneas | Tendencias en el tiempo |
| 🔄 Interactivas | Tooltips y leyendas |

### Exportación

| Formato | Descripción |
|---|---|
| 📄 PDF Profesional | Informe completo con todos los análisis |
| 🎨 Plantillas | 3 estilos (profesional, moderno, minimalista) |
| 📊 Gráficos Incluidos | Imágenes de las visualizaciones |

---

## 📝 Endpoints API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Estado del servidor |
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Subir archivo CSV |
| POST | `/api/analyze` | Analizar datos con IA |
| POST | `/api/export-pdf` | Generar informe PDF |
| GET | `/api/analyze/{file_id}/results` | Obtener resultados |
| GET | `/api/export/{file_id}/status` | Estado del PDF |
| GET | `/api/export/{file_id}/download` | Descargar PDF |

### Ejemplo de uso con curl

```bash
# Health check
curl http://localhost:8000/api/health

# Subir CSV
curl -X POST -F "file=@datos.csv" http://localhost:8000/api/upload

# Analizar datos
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_id": "20260706_222159_3b36213a"}' \
  http://localhost:8000/api/analyze

# Generar PDF
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_id": "20260706_222159_3b36213a", "include_charts": true}' \
  http://localhost:8000/api/export-pdf \
  --output informe.pdf
```


Desarrollado por [Juan Carlos Pabón Jaimes](https://portafolio-juan-carlos-pabon.vercel.app) — [@JCPABON03](https://github.com/JCPABON03)

Construido con [FastAPI](https://fastapi.tiangolo.com/), [React](https://react.dev/), [Google Gemini AI](https://ai.google.dev/) y [Tailwind CSS](https://tailwindcss.com/).
