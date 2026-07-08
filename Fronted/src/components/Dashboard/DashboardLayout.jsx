import React from 'react'

export const DashboardLayout = ({ children }) => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <span className="text-sm text-gray-500">
          Análisis en tiempo real
        </span>
      </div>
      {children}
    </div>
  )
}