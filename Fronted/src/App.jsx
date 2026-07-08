import React, { useState, useEffect } from 'react'
import { Toaster, toast } from 'react-hot-toast'
import { 
  BarChart3, 
  Upload, 
  FileText, 
  Download,
  RefreshCw 
} from 'lucide-react'

// Componentes
import { ConnectionStatus } from './components/common/ConnectionStatus'
import { CSVUploader } from './components/Upload/CSVUploader'
import { DashboardLayout } from './components/Dashboard/DashboardLayout'
import { MetricsCards } from './components/Dashboard/MetricsCards'
import { ChartsSection } from './components/Dashboard/ChartsSection'
import { InsightsPanel } from './components/Dashboard/InsightsPanel'
import { PDFExportButton } from './components/Export/PDFExportButton'
import { LoadingSpinner } from './components/common/LoadingSpinner'

// Hooks
import { useApi } from './hooks/useApi'
import { useAnalysis } from './hooks/useAnalysis'

function App() {
  const [fileId, setFileId] = useState(null)
  const [analysisData, setAnalysisData] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const { uploadFile, uploadProgress, isUploading } = useApi()
  const { analyzeData, analysisResult, loading: analysisLoading } = useAnalysis()

  const handleFileUpload = async (file) => {
    try {
      const result = await uploadFile(file)
      setFileId(result.file_id)
      toast.success('Archivo subido correctamente')
      
      // Iniciar análisis automáticamente
      await handleAnalyze(result.file_id)
    } catch (error) {
      toast.error('Error al subir el archivo: ' + error.message)
    }
  }

  const handleAnalyze = async (id) => {
    if (!id && !fileId) return
    
    setIsAnalyzing(true)
    try {
      const result = await analyzeData(id || fileId)
      console.log('Datos del análisis:', result)
      setAnalysisData(result)
      toast.success('Archivo analizado correctamente')
    } catch (error) {
      console.error('Error en análisis:', error)
      toast.error('Error en el análisis: ' + error.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleReset = () => {
    setFileId(null)
    setAnalysisData(null)
    toast('Datos reiniciados')
  }

  return (
    <div className="min-h-screen bg-gray-950">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <BarChart3 className="h-8 w-8 text-blue-500" />
              <div>
                <h1 className="text-xl font-bold text-gray-50">
                  Analytics Dashboard
                </h1>
                <p className="text-xs text-gray-400">
                  IA + Multiagentes
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisData ? (
          <div className="animate-fade-in">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-50">
                Análisis de Datos con IA
              </h2>
              <p className="mt-2 text-gray-400">
                Sube tu archivo CSV y deja que la IA analice tus datos
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <CSVUploader 
                  onUpload={handleFileUpload}
                  isUploading={isUploading}
                  progress={uploadProgress}
                />
              </div>
              
              <div className="space-y-4">
                <div className="card bg-gray-900 border-gray-800">
                  <div className="card-accent" />
                  <h3 className="font-semibold text-gray-50 mb-2">
                     ¿Qué hace esta web?
                  </h3>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li className="flex items-start gap-2">
                      <span className="text-blue-400">✓</span>
                      Sube tu CSV y obtén análisis instantáneos
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-400">✓</span>
                      IA con Gemini para insights profundos
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-400">✓</span>
                      Visualizaciones automáticas
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-400">✓</span>
                      Exporta informes profesionales en PDF
                    </li>
                  </ul>
                </div>
                
                {(isUploading || isAnalyzing) && (
                  <div className="card bg-gray-900 border-gray-800">
                    <div className="card-accent" />
                    <div className="flex items-center gap-3">
                      <LoadingSpinner />
                      <div>
                        <p className="font-medium text-gray-50">
                          {isUploading ? 'Subiendo archivo...' : 'Analizando datos...'}
                        </p>
                        {isUploading && uploadProgress > 0 && (
                          <div className="mt-2 w-full bg-gray-800 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${uploadProgress}%` }}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="animate-fade-in space-y-6">
            {/* Título y acciones del dashboard */}
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-50">📊 Dashboard</h2>
                <p className="text-sm text-gray-400">
                  Análisis completado con {analysisData.analyzed_with === 'gemini' ? '🧠 IA Gemini' : '📊 análisis básico'}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleReset}
                  className="bg-gray-800 text-gray-300 px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center gap-2 text-sm"
                >
                  <RefreshCw className="h-4 w-4" />
                  Reiniciar
                </button>
                <button
                  onClick={() => handleAnalyze(fileId)}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 text-sm"
                >
                  <BarChart3 className="h-4 w-4" />
                  Re-analizar
                </button>
              </div>
            </div>

            {/* Métricas */}
            <MetricsCards metrics={analysisData.metrics || []} />
            
            {/* Gráficos - Pasamos todos los datos disponibles */}
            <ChartsSection 
              data={{
                metrics: analysisData.metrics || [],
                charts_data: analysisData.charts_data || {},
                insights: analysisData.insights || []
              }}
              insights={analysisData.insights || []}
            />
            
            {/* Insights y Exportación */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <InsightsPanel 
                insights={analysisData.insights || []}
                anomalies={analysisData.anomalies || []}
                recommendations={analysisData.recommendations || []}
              />
              
              <div className="space-y-4">
                <div className="card bg-gray-900 border-gray-800">
                  <div className="card-accent" />
                  <h3 className="font-semibold text-gray-50 mb-4">
                    📄 Exportar Informe
                  </h3>
                  <PDFExportButton 
                    fileId={fileId}
                    analysisData={analysisData}
                  />
                  <p className="mt-3 text-xs text-gray-400">
                    Genera un informe profesional en PDF con todos los análisis y gráficos
                  </p>
                </div>
                
                <div className="card bg-blue-500/10 border-blue-500/30">
                  <div className="card-accent" />
                  <h4 className="font-medium text-blue-300 mb-1">
                    💡 Resumen del análisis
                  </h4>
                  <p className="text-sm text-blue-200/80">
                    {analysisData.summary || 'Análisis completado exitosamente'}
                  </p>
                  <div className="mt-2 flex gap-2 text-xs text-blue-400/60">
                    <span>📊 {analysisData.metrics?.length || 0} métricas</span>
                    <span>•</span>
                    <span>💡 {analysisData.insights?.length || 0} insights</span>
                    <span>•</span>
                    <span>⚠️ {analysisData.anomalies?.length || 0} anomalías</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App  