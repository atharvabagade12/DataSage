export const useAuth = () => {
  const router = useRouter()
  
  const API_BASE = 'http://localhost:8000/api/auth'
  
  // Get stored token
  const getToken = () => {
    return localStorage.getItem('authToken')
  }
  
  // Store token
  const setToken = (token) => {
    localStorage.setItem('authToken', token)
  }
  
  // Remove token
  const clearToken = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    sessionStorage.clear()
  }
  
  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!getToken()
  }
  
  // Register user
  const register = async (username, email, password) => {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }
    
    return await response.json()
  }
  
  // Login user
  const login = async (username, password) => {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    // Store token and user data
    setToken(data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    sessionStorage.setItem('user', JSON.stringify(data.user))
    
    return data
  }
  
  // Logout user
  const logout = async () => {
    const token = getToken()
    
    if (token) {
      try {
        await fetch(`${API_BASE}/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    clearToken()
    router.push('/login')
  }
  
  // Verify token
  const verifyToken = async () => {
    const token = getToken()
    
    if (!token) return false
    
    try {
      const response = await fetch(`${API_BASE}/verify-token`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      return response.ok
    } catch {
      return false
    }
  }
  
  return {
    register,
    login,
    logout,
    isAuthenticated,
    verifyToken,
    getToken
  }
}
