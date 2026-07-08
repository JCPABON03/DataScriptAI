import React, { useState } from 'react'
import { Lightbulb, AlertTriangle, ThumbsUp, ChevronDown } from 'lucide-react'
import clsx from 'clsx'

const InsightCard = ({ insight }) => {
  const [expanded, setExpanded] = useState(false)

  const priorityStyles = {
    high: 'border-red-500/60 bg-red-500/10',
    medium: 'border-yellow-500/60 bg-yellow-500/10',
    low: 'border-green-500/60 bg-green-500/10'
  }

  const priorityIcons = {
    high: <AlertTriangle className="h-4 w-4 text-red-400" />,
    medium: <AlertTriangle className="h-4 w-4 text-yellow-400" />,
    low: <Lightbulb className="h-4 w-4 text-green-400" />
  }

  return (
    <div
      className={clsx(
        'border-l-4 p-3 rounded-r-lg transition-colors hover:bg-white/[0.03]',
        priorityStyles[insight.priority] || 'border-gray-600 bg-gray-800/50'
      )}
    >
      <div className="flex items-start gap-2">
        <div className="mt-0.5">
          {priorityIcons[insight.priority] || <Lightbulb className="h-4 w-4 text-gray-500" />}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2">
            <h4 className="font-medium text-gray-100 text-sm truncate">
              {insight.title}
            </h4>
            <button
              onClick={() => setExpanded(!expanded)}
              className="ml-2 p-1 text-gray-500 hover:text-gray-200 hover:bg-white/10 rounded-full flex-shrink-0 transition-colors"
            >
              <ChevronDown
                className={clsx('h-3.5 w-3.5 transition-transform duration-200', expanded && 'rotate-180')}
              />
            </button>
          </div>
          <p
            className={clsx(
              'text-sm text-gray-400 transition-all',
              expanded ? 'mt-1' : 'line-clamp-1'
            )}
          >
            {insight.description}
          </p>
          {insight.category && (
            <span className="inline-block mt-1.5 text-xs bg-white/5 text-gray-400 px-2 py-0.5 rounded-full border border-white/10">
              {insight.category}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export const InsightsPanel = ({ insights, anomalies, recommendations }) => {
  const [activeTab, setActiveTab] = useState('insights')

  const tabs = [
    { key: 'insights', label: 'Insights', icon: Lightbulb, count: insights?.length || 0 },
    { key: 'anomalies', label: 'Anomalías', icon: AlertTriangle, count: anomalies?.length || 0 },
    { key: 'recommendations', label: 'Recomendaciones', icon: ThumbsUp, count: recommendations?.length || 0 },
  ]

  return (
    <div className="card">
      <div className="flex border-b border-gray-800 mb-4 -mx-1">
        {tabs.map(({ key, label, icon: Icon, count }) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            className={clsx(
              'px-4 py-2 text-sm font-medium transition-colors relative rounded-t-md',
              activeTab === key
                ? 'text-primary-400'
                : 'text-gray-500 hover:text-gray-300'
            )}
          >
            <span className="flex items-center gap-2">
              <Icon className="h-4 w-4" />
              {label} ({count})
            </span>
            {activeTab === key && (
              <span className="absolute left-0 right-0 -bottom-px h-0.5 bg-primary-500 rounded-full" />
            )}
          </button>
        ))}
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
        {activeTab === 'insights' && (
          insights?.length > 0 ? (
            insights.map((insight, index) => (
              <InsightCard key={index} insight={insight} />
            ))
          ) : (
            <div className="text-center py-8 text-gray-500 text-sm">
              No hay insights disponibles
            </div>
          )
        )}

        {activeTab === 'anomalies' && (
          anomalies?.length > 0 ? (
            anomalies.map((anomaly, index) => (
              <div
                key={index}
                className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 transition-colors hover:bg-red-500/15"
              >
                <h4 className="font-medium text-red-300 text-sm">
                  {anomaly.column || 'Anomalía detectada'}
                </h4>
                <p className="text-sm text-red-400/80 mt-1">
                  {anomaly.outliers_count || 0} valores atípicos encontrados
                  {anomaly.percentage ? ` (${anomaly.percentage.toFixed(1)}% de los datos)` : ''}
                </p>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500 text-sm">
              No se detectaron anomalías
            </div>
          )
        )}

        {activeTab === 'recommendations' && (
          recommendations?.length > 0 ? (
            <ul className="space-y-2">
              {recommendations.map((rec, index) => (
                <li
                  key={index}
                  className="flex items-start gap-3 p-2.5 bg-gray-800/50 border border-white/5 rounded-lg transition-colors hover:bg-gray-800"
                >
                  <span className="flex items-center justify-center h-5 w-5 rounded-full bg-primary-500/15 text-primary-400 font-medium text-xs flex-shrink-0">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-300">{rec}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center py-8 text-gray-500 text-sm">
              No hay recomendaciones disponibles
            </div>
          )
        )}
      </div>
    </div>
  )
}