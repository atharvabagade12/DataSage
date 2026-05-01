import { defineStore } from 'pinia'

interface User {
  id: string;
  username: string;
  email: string;
}

interface LoginResponse {
  success: boolean;
  user: User;
  token?: string;
  access_token?: string;
  message?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),

  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    async login(credentials: any) {
      const { authenticatedPost } = useAuthenticatedFetch()
      this.isLoading = true
      this.error = null
    
      try {
        console.log('🚀 Auth store: Starting login...')
        const payload = {
          username: credentials.username || credentials.email,
          password: credentials.password
        }
        
        const response = await authenticatedPost(`/api/auth/login`, payload)
        
        const data = response instanceof Response ? await response.json() : response

        if (data && (data.success || data.access_token)) {
          this.user = data.user
          this.token = data.token || data.access_token || null
          this.isAuthenticated = true
    
          if (typeof window !== 'undefined') {
            sessionStorage.setItem('user', JSON.stringify(data.user))
            sessionStorage.setItem('token', this.token || '')
          }
    
          return { success: true, user: data.user }
        } else {
          throw new Error(data?.message || 'Login failed')
        }
      } catch (error: any) {
        this.error = error.message || 'Connection failed'
        this.isAuthenticated = false
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async register(username: string, email: string, password: string) {
      const { authenticatedPost } = useAuthenticatedFetch()
      try {
        const response = await authenticatedPost(`/api/auth/register`, { username, email, password })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Registration failed')
        }
        
        return await response.json()
      } catch (error: any) {
        throw new Error(error.message || 'Registration failed')
      }
    },

    async signup(userData: any) {
      this.isLoading = true
      this.error = null
      try {
        const payload = {
          username: userData.username,
          email: userData.email,
          password: userData.password
        }
        const { authenticatedPost } = useAuthenticatedFetch()
        const response = await authenticatedPost(`/api/auth/register`, payload)
        
        const data = response instanceof Response ? await response.json() : response

        if (data && (data.success || data.status === 'success')) {
          return await this.login({
            username: userData.username,
            password: userData.password
          })
        } else {
          throw new Error(data?.message || 'Registration failed')
        }
      } catch (error: any) {
        this.error = error.message || 'Connection failed'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      const { authenticatedPost } = useAuthenticatedFetch()
      try {
        await authenticatedPost(`/api/auth/logout`, {})
      } catch (error) {
        console.warn('Logout API call failed:', error)
      }
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.error = null
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('token')
      }
    },

    restoreSession() {
      if (typeof window !== 'undefined') {
        const user = sessionStorage.getItem('user')
        const token = sessionStorage.getItem('token')
        if (user && token) {
          this.user = JSON.parse(user) as User
          this.token = token
          this.isAuthenticated = true
        }
      }
    }
  }
})
