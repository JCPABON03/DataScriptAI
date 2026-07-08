import React from 'react'
import { Loader } from 'lucide-react'

export const UploadProgress = ({ progress, status }) => {
  const statusMessages = {
    uploading: 'Subiendo archivo...',
    processing: 'Procesando datos...',
    analyzing: 'Analizando con IA...',
    complete: '¡Completado!'
  }

  return (
    <div className="card">
      <div className="flex items-center gap-4">
        <Loader className="h-6 w-6 animate-spin text-primary-600" />
        <div className="flex-1">
          <p className="font-medium text-gray-900">
            {statusMessages[status] || 'Procesando...'}
          </p>
          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-500 mt-1">{progress}%</p>
        </div>
      </div>
    </div>
  )
}