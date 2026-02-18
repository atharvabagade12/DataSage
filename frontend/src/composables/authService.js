export const useAuth = () => {
  const router = useRouter()
  const { authenticatedFetch, authenticatedPost, authenticatedGet } = useAuthenticatedFetch()
  
  const API_BASE = `/api/auth`
  
  // Get stored token
  const getToken = () => {
    return localStorage.getItem('authToken') || sessionStorage.getItem('token')
  }
  
  // Store token
  const setToken = (token) => {
    localStorage.setItem('authToken', token)
    sessionStorage.setItem('token', token)
  }
  
  // Remove token
  const clearToken = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
    sessionStorage.clear()
  }
  
  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!getToken()
  }
  
  // Register user
  const register = async (username, email, password) => {
    const response = await authenticatedPost(`${API_BASE}/register`, { 
      username, email, password 
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }
    
    return await response.json()
  }
  
  // Login user
  const login = async (username, password) => {
    const response = await authenticatedPost(`${API_BASE}/login`, { 
      username, password 
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    // Store token and user data
    setToken(data.access_token || data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    sessionStorage.setItem('user', JSON.stringify(data.user))
    
    return data
  }
  
  // Logout user
  const logout = async () => {
    try {
      await authenticatedPost(`${API_BASE}/logout`, {})
    } catch (error) {
      console.error('Logout error:', error)
    }
    
    clearToken()
    router.push('/login')
  }
  
  // Verify token
  const verifyToken = async () => {
    try {
      const response = await authenticatedPost(`${API_BASE}/verify-token`, {})
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
