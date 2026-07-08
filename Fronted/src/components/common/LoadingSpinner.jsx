import React from 'react'
import { Loader } from 'lucide-react'

export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  }

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <Loader className={`${sizes[size]} animate-spin text-primary-600`} />
    </div>
  )
}