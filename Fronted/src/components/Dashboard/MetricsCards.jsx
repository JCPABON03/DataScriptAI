// src/components/Dashboard/MetricsCards.jsx
import React from 'react'
import { TrendingUp, TrendingDown, Minus, Activity, DollarSign, Calendar, Users } from 'lucide-react'

const getMetricIcon = (name) => {
  const name_lower = name.toLowerCase()
  if (name_lower.includes('edad') || name_lower.includes('age')) return <Users className="h-5 w-5 text-blue-400" />
  if (name_lower.includes('costo') || name_lower.includes('cost') || name_lower.includes('tratamiento')) return <DollarSign className="h-5 w-5 text-green-400" />
  if (name_lower.includes('día') || name_lower.includes('day') || name_lower.includes('internación')) return <Calendar className="h-5 w-5 text-purple-400" />
  return <Activity className="h-5 w-5 text-gray-400" />
}

const MetricCard = ({ metric }) => {
  const formatValue = (value) => {
    if (typeof value === 'number') {
      if (value > 1000000) return `${(value / 1000000).toFixed(1)}M`
      if (value > 1000) return `${(value / 1000).toFixed(1)}K`
      return value.toFixed(2)
    }
    return value
  }

  const formatLabel = (name) => {
    // Traducir nombres comunes al español
    const translations = {
      'Edad promedio': 'Edad Promedio',
      'Días de internación promedio': 'Días de Internación',
      'Costo de tratamiento promedio': 'Costo Promedio',
      'Mediana de edad': 'Mediana de Edad',
      'Total de pacientes': 'Total Pacientes'
    }
    return translations[name] || name
  }

  return (
    <div className="card bg-gray-900 border-gray-800 hover:border-gray-700">
      <div className="card-accent" />
      <div className="flex items-start gap-3">
        <div className="p-3 bg-gray-800 rounded-xl">
          {getMetricIcon(metric.name)}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-400 font-medium truncate">
            {formatLabel(metric.name)}
          </p>
          <p className="text-2xl font-bold text-gray-50 mt-1">
            {typeof metric.value === 'number' && metric.name.toLowerCase().includes('costo') 
              ? `$${formatValue(metric.value)}` 
              : formatValue(metric.value)}
          </p>
          {metric.description && (
            <p className="text-xs text-gray-500 mt-1 line-clamp-2">{metric.description}</p>
          )}
        </div>
      </div>
    </div>
  )
}

export const MetricsCards = ({ metrics }) => {
  if (!metrics || metrics.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No hay métricas disponibles
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <MetricCard key={index} metric={metric} />
      ))}
    </div>
  )
}