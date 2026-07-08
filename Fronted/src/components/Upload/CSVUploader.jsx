import React from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileSpreadsheet, X } from 'lucide-react'
import clsx from 'clsx'

export const CSVUploader = ({ onUpload, isUploading, progress }) => {
  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop: (files) => {
      if (files.length > 0 && onUpload) {
        onUpload(files[0])
      }
    },
    accept: {
      'text/csv': ['.csv'],
      'text/tab-separated-values': ['.tsv']
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
    disabled: isUploading
  })

  const file = acceptedFiles[0]

  return (
    <div className="card">
      <div
        {...getRootProps()}
        className={clsx(
          'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all',
          isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400',
          isUploading && 'opacity-50 cursor-not-allowed'
        )}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="space-y-3">
            <Upload className="h-12 w-12 mx-auto text-primary-500 animate-pulse" />
            <div>
              <p className="font-medium text-gray-900">Subiendo archivo...</p>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress || 0}%` }}
                />
              </div>
              <p className="text-sm text-gray-500 mt-1">{progress || 0}%</p>
            </div>
          </div>
        ) : file ? (
          <div className="space-y-3">
            <div className="flex items-center justify-center gap-2">
              <FileSpreadsheet className="h-12 w-12 text-green-500" />
              <div className="text-left">
                <p className="font-medium text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  acceptedFiles.length = 0
                }}
                className="ml-2 p-1 hover:bg-gray-100 rounded-full"
              >
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <Upload className="h-12 w-12 mx-auto text-gray-400" />
            <div>
              <p className="font-medium text-gray-900">
                {isDragActive ? 'Suelta el archivo aquí' : 'Arrastra tu CSV o haz clic'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Soporta archivos CSV y TSV (máx. 10MB)
              </p>
            </div>
          </div>
        )}
      </div>

      {file && !isUploading && (
        <div className="mt-4 flex justify-center">
          <button
            onClick={() => onUpload(file)}
            className="btn-primary flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            Procesar archivo
          </button>
        </div>
      )}
    </div>
  )
}