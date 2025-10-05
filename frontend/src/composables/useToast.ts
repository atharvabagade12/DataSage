interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

export const useToast = () => {
  const toasts = ref<Toast[]>([])

  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 15)
    const newToast = { ...toast, id }
    
    toasts.value.push(newToast)
    
    // Auto remove after duration (default 5 seconds)
    setTimeout(() => {
      removeToast(id)
    }, toast.duration || 5000)
    
    return id
  }

  const removeToast = (id: string) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const success = (message: string, duration?: number) => {
    return addToast({ type: 'success', message, duration })
  }

  const error = (message: string, duration?: number) => {
    return addToast({ type: 'error', message, duration })
  }

  const warning = (message: string, duration?: number) => {
    return addToast({ type: 'warning', message, duration })
  }

  const info = (message: string, duration?: number) => {
    return addToast({ type: 'info', message, duration })
  }

  return {
    toasts: readonly(toasts),
    addToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
}
