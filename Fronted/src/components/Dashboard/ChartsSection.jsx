import React, { useState, useEffect } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts'
import { BarChart3, PieChart as PieChartIcon, LineChart as LineChartIcon } from 'lucide-react'
import clsx from 'clsx'

const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981', '#EF4444']

export const ChartsSection = ({ data, insights }) => {
  const [chartType, setChartType] = useState('bar')
  const [chartData, setChartData] = useState([])

  useEffect(() => {
    // Preparar datos para gráficos cuando cambia data o insights
    if (data && Object.keys(data).length > 0) {
      prepareChartData()
    }
  }, [data, insights])

  const prepareChartData = () => {
    console.log('Preparando datos para gráficos:', data)
    
    // Si hay datos de métricas, usarlos
    if (data && data.metrics && data.metrics.length > 0) {
      const metricsData = data.metrics.map(metric => ({
        name: metric.name || 'Métrica',
        value: typeof metric.value === 'number' ? metric.value : parseFloat(metric.value) || 0,
        description: metric.description || ''
      }))
      console.log('Datos de métricas:', metricsData)
      setChartData(metricsData)
      return
    }

    // Si hay datos de insights, usarlos
    if (insights && insights.length > 0) {
      const insightsData = insights.slice(0, 6).map((insight, index) => ({
        name: insight.category || insight.title || `Insight ${index + 1}`,
        value: Math.floor(Math.random() * 80) + 20, // Valor aleatorio para demo
        priority: insight.priority || 'medium'
      }))
      console.log('Datos de insights:', insightsData)
      setChartData(insightsData)
      return
    }

    // Si no hay datos, mostrar mensaje
    console.warn('No hay datos para visualizar')
    setChartData([])
  }

  const renderChart = () => {
    if (!chartData || chartData.length === 0) {
      return (
        <div className="flex flex-col justify-center items-center h-64 text-gray-400">
          <BarChart3 className="h-12 w-12 mb-2 text-gray-300" />
          <p className="text-sm">No hay datos para visualizar</p>
          <p className="text-xs text-gray-400 mt-1">Sube un archivo CSV para comenzar</p>
        </div>
      )
    }

    console.log(`Renderizando gráfico ${chartType} con ${chartData.length} datos`)

    switch (chartType) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white',
                  border: '1px solid #E5E7EB',
                  borderRadius: '8px',
                  padding: '12px'
                }}
              />
              <Legend />
              <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )
      
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )
      
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white',
                  border: '1px solid #E5E7EB',
                  borderRadius: '8px',
                  padding: '12px'
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#3B82F6" 
                strokeWidth={2}
                dot={{ fill: '#3B82F6', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )
      
      default:
        return null
    }
  }

  return (
    <div className="card">
      <div className="card-accent" />
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <h3 className="font-semibold text-gray-900">Visualizaciones</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setChartType('bar')}
            className={clsx(
              'p-2 rounded-lg transition-colors',
              chartType === 'bar' ? 'bg-blue-600 text-white' : 'bg-gray-100 hover:bg-gray-200'
            )}
            title="Gráfico de barras"
          >
            <BarChart3 className="h-4 w-4" />
          </button>
          <button
            onClick={() => setChartType('pie')}
            className={clsx(
              'p-2 rounded-lg transition-colors',
              chartType === 'pie' ? 'bg-blue-600 text-white' : 'bg-gray-100 hover:bg-gray-200'
            )}
            title="Gráfico circular"
          >
            <PieChartIcon className="h-4 w-4" />
          </button>
          <button
            onClick={() => setChartType('line')}
            className={clsx(
              'p-2 rounded-lg transition-colors',
              chartType === 'line' ? 'bg-blue-600 text-white' : 'bg-gray-100 hover:bg-gray-200'
            )}
            title="Gráfico de líneas"
          >
            <LineChartIcon className="h-4 w-4" />
          </button>
        </div>
      </div>
      
      <div className="w-full">
        {renderChart()}
      </div>
      
      {chartData.length > 0 && (
        <div className="mt-4 text-xs text-gray-400 text-center">
          {chartData.length} puntos de datos visualizados
        </div>
      )}
    </div>
  )
}