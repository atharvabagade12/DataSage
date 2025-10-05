import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
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
    // Login action
    // In your auth store (stores/auth.ts), update the login function:
    async login(credentials) {
      this.isLoading = true
      this.error = null
    
      try {
        console.log('🚀 Auth store: Starting login...')
        
        // ✅ CORRECT FORMAT - Backend expects ONLY username and password
        const payload = {
          username: credentials.username || credentials.email,
          password: credentials.password
          
        }
        
        console.log('📡 Sending payload to backend:', payload)
        
        const response = await $fetch('http://localhost:8000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)  // ✅ Send correct format
        })
    
        console.log('✅ Auth store: Login response:', response)
    
        if (response && response.success) {
          // Set auth state
          this.user = response.user
          this.token = response.token || response.access_token
          this.isAuthenticated = true
    
          // Store in session storage
          if (process.client) {
            sessionStorage.setItem('user', JSON.stringify(response.user))
            sessionStorage.setItem('token', response.token || response.access_token)
          }
    
          return { success: true, user: response.user }
        } else {
          throw new Error(response?.message || 'Login failed')
        }
    
      } catch (error) {
        console.error('❌ Auth store: Login error:', error)
        this.error = error.message || 'Connection failed'
        this.isAuthenticated = false
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },


    async register(username: string, email: string, password: string) {
      try {
        const response = await fetch('http://localhost:8000/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, email, password })
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Registration failed')
        }
        
        return await response.json()
      } catch (error: any) {
        throw new Error(error.message || 'Registration failed')
      }
    },
    // Signup action
    async signup(userData) {
      this.isLoading = true
      this.error = null
    
      try {
        console.log('🚀 Auth store: Starting signup...')
        console.log('🔍 Input userData:', userData)  // ← Add this
        
        const payload = {
          username: userData.username,
          email: userData.email,
          password: userData.password
        }
        
        console.log('📡 Sending payload:', payload)  // ← Add this
        console.log('📡 Payload JSON:', JSON.stringify(payload))  // ← Add this
        
        const response = await $fetch('http://localhost:8000/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)
        })
    
        console.log('✅ Auth store: Register response:', response)
    
        if (response && response.success) {
          // Auto-login after signup
          return await this.login({
            username: userData.username,  // ✅ Use username for login
            password: userData.password
          })
        } else {
          throw new Error(response?.message || 'Registration failed')
        }
    
      } catch (error) {
        console.error('❌ Auth store: Register error:', error)
        this.error = error.message || 'Connection failed'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    // Logout action
    async logout() {
      try {
        await $fetch('http://localhost:8000/api/auth/logout', {
          method: 'POST'
        })
      } catch (error) {
        console.warn('Logout API call failed:', error)
      }

      // Clear state regardless of API response
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.error = null

      // Clear session storage
      if (process.client) {
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('token')
      }
    },

    // Restore session
    restoreSession() {
      if (process.client) {
        const user = sessionStorage.getItem('user')
        const token = sessionStorage.getItem('token')

        if (user && token) {
          this.user = JSON.parse(user)
          this.token = token
          this.isAuthenticated = true
        }
      }
    },

    // Clear error
    clearError() {
      this.error = null
    }
  }
})
