interface LoginCredentials {
  username: string
  password: string
}

interface RegisterData {
  username: string
  email: string
  password: string
}

interface ApiResponse<T> {
  data?: T
  error?: string
  status?: number
}

export const useAPI = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Global error handler
  const handleApiError = (error: any): string => {
    console.error('API Error:', error)
    
    if (error.status === 401) {
      return 'Invalid credentials'
    } else if (error.status === 400) {
      return error.data?.detail || 'Invalid request'
    } else if (error.status === 422) {
      return 'Validation error. Please check your input.'
    } else if (error.status === 500) {
      return 'Server error. Please try again later.'
    } else if (!navigator.onLine) {
      return 'No internet connection. Please check your network.'
    } else {
      return error.data?.detail || 'An unexpected error occurred'
    }
  }

  const auth = {
    async login(credentials: LoginCredentials): Promise<ApiResponse<any>> {
      try {
        const response = await $fetch(`${apiBase}/api/auth/login`, {
          method: 'POST',
          body: credentials,
          timeout: 60000 // 60 second timeout for cold starts
        })
        return { data: response, status: 200 }
      } catch (error: any) {
        return { 
          error: handleApiError(error), 
          status: error.status || 500 
        }
      }
    },

    async register(userData: RegisterData): Promise<ApiResponse<any>> {
      try {
        const response = await $fetch(`${apiBase}/api/auth/register`, {
          method: 'POST',
          body: userData,
          timeout: 60000
        })
        return { data: response, status: 201 }
      } catch (error: any) {
        return { 
          error: handleApiError(error), 
          status: error.status || 500 
        }
      }
    },

    async getMe(token: string): Promise<ApiResponse<any>> {
      try {
        const response = await $fetch(`${apiBase}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          timeout: 60000
        })
        return { data: response, status: 200 }
      } catch (error: any) {
        return { 
          error: handleApiError(error), 
          status: error.status || 500 
        }
      }
    },

    async verifyToken(token: string): Promise<boolean> {
      try {
        const response = await $fetch<{ valid: boolean }>(`${apiBase}/api/auth/verify-token`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          timeout: 5000
        })
        return response?.valid === true
      } catch (error) {
        console.error('Token verification failed:', error)
        return false
      }
    }
  }

  return { auth }
}
