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
  
  // Verify token — with a 5-second timeout so a dead backend never freezes the app
  const verifyToken = async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    try {
      const response = await authenticatedFetch(`${API_BASE}/verify-token`, {
        method: 'POST',
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      return response.ok;
    } catch {
      clearTimeout(timeoutId);
      return false; // treat timeout / network error as invalid token (will redirect to login)
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
