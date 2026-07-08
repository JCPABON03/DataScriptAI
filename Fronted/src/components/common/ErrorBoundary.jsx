import React, { Component } from 'react'

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="card border-red-200 bg-red-50">
          <h3 className="text-red-800 font-semibold">Algo salió mal</h3>
          <p className="text-red-600 text-sm mt-1">
            {this.state.error?.message || 'Error inesperado'}
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-3 btn-primary text-sm"
          >
            Reintentar
          </button>
        </div>
      )
    }

    return this.props.children
  }
}