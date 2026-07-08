import React, { useState } from 'react'
import { Download, Loader, FileText, Settings } from 'lucide-react'
import toast from 'react-hot-toast'
import { usePdfExport } from '../../hooks/usePdfExport'
import clsx from 'clsx'

export const PDFExportButton = ({ fileId, analysisData }) => {
  const { isExporting, exportPDF } = usePdfExport()
  const [showOptions, setShowOptions] = useState(false)
  const [includeCharts, setIncludeCharts] = useState(true)
  const [templateStyle, setTemplateStyle] = useState('professional')

  const handleExport = async () => {
    if (!fileId) {
      toast.error('No hay datos para exportar')
      return
    }

    try {
      await exportPDF(fileId, {
        includeCharts,
        templateStyle
      })
      toast.success('PDF generado y descargado')
    } catch (error) {
      toast.error('Error al generar el PDF: ' + error.message)
    }
  }

  return (
    <div className="space-y-3">
      <button
        onClick={handleExport}
        disabled={isExporting || !fileId}
        className={clsx(
          'w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium transition-all',
          isExporting || !fileId
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-primary-600 text-white hover:bg-primary-700 active:scale-95'
        )}
      >
        {isExporting ? (
          <>
            <Loader className="h-5 w-5 animate-spin" />
            Generando PDF...
          </>
        ) : (
          <>
            <FileText className="h-5 w-5" />
            Descargar Informe PDF
          </>
        )}
      </button>

      <button
        onClick={() => setShowOptions(!showOptions)}
        className="w-full text-xs text-gray-500 hover:text-gray-700 flex items-center justify-center gap-1"
      >
        <Settings className="h-3 w-3" />
        {showOptions ? 'Ocultar opciones' : 'Mostrar opciones'}
      </button>

      {showOptions && (
        <div className="bg-gray-50 rounded-lg p-3 space-y-3 animate-fade-in">
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="includeCharts"
              checked={includeCharts}
              onChange={(e) => setIncludeCharts(e.target.checked)}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <label htmlFor="includeCharts" className="text-sm text-gray-700">
              Incluir gráficos
            </label>
          </div>

          <div>
            <label className="text-sm text-gray-700 block mb-1">
              Estilo de plantilla
            </label>
            <select
              value={templateStyle}
              onChange={(e) => setTemplateStyle(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="professional">Profesional</option>
              <option value="modern">Moderno</option>
              <option value="minimal">Minimalista</option>
            </select>
          </div>
        </div>
      )}

      {analysisData?.summary && (
        <div className="text-xs text-gray-400 mt-2 text-center">
          Informe basado en {analysisData.metrics?.length || 0} métricas
        </div>
      )}
    </div>
  )
}