interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

// Global toast state (shared across all components)
const toasts = ref<Toast[]>([])
let nextId = 1

export function toastState() {
  const removeToast = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    toasts: readonly(toasts),
    removeToast
  }
}

export const useToast = () => {
  const showToast = ({ type = 'info', title, message = '', duration = 5000 }: {
    type?: 'success' | 'error' | 'warning' | 'info'
    title: string
    message?: string
    duration?: number
  }) => {
    const id = nextId++
    
    const toast: Toast = {
      id,
      type,
      title,
      message,
      duration
    }
    
    toasts.value.push(toast)
    
    // Auto-remove after duration (unless duration is 0)
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    
    return id
  }

  const removeToast = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const showSuccess = (title: string, message = '', duration = 5000) => {
    return showToast({ type: 'success', title, message, duration })
  }

  const showError = (title: string, message = '', duration = 7000) => {
    return showToast({ type: 'error', title, message, duration })
  }

  const showWarning = (title: string, message = '', duration = 6000) => {
    return showToast({ type: 'warning', title, message, duration })
  }

  const showInfo = (title: string, message = '', duration = 5000) => {
    return showToast({ type: 'info', title, message, duration })
  }

  const clearAll = () => {
    toasts.value = []
  }

  return {
    toasts: readonly(toasts),
    showToast,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    removeToast,
    clearAll
  }
}
