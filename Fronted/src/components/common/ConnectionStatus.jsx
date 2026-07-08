import React, { useState, useEffect } from 'react'
import { CheckCircle, XCircle, Loader } from 'lucide-react'
import { api } from '../../services/api'

export const ConnectionStatus = () => {
  const [status, setStatus] = useState('checking')

  const checkConnection = async () => {
    try {
      await api.health()
      setStatus('connected')
    } catch (error) {
      setStatus('disconnected')
    }
  }

  useEffect(() => {
    checkConnection()
    const interval = setInterval(checkConnection, 30000)
    return () => clearInterval(interval)
  }, [])

  if (status === 'checking') {
    return (
      <div className="flex items-center gap-2 text-sm">
        <Loader className="h-4 w-4 animate-spin text-yellow-500" />
        <span className="text-gray-500">Conectando...</span>
      </div>
    )
  }

  if (status === 'connected') {
    return (
      <div className="flex items-center gap-2 text-sm">
        <CheckCircle className="h-4 w-4 text-green-500" />
        <span className="text-green-600 font-medium">API Conectada</span>
        <span className="text-gray-400 text-xs hidden sm:inline">
          {import.meta.env.VITE_API_URL}
        </span>
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      <XCircle className="h-4 w-4 text-red-500" />
      <span className="text-red-600 font-medium">API Desconectada</span>
      <button 
        onClick={checkConnection}
        className="text-primary-600 hover:text-primary-700 underline ml-1"
      >
        Reintentar
      </button>
    </div>
  )
}