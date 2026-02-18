/**
 * Authenticated Fetch Composable
 * 
 * Automatically includes JWT authentication token in all API requests.
 * Use this instead of raw fetch() for all backend API calls.
 */

export const useAuthenticatedFetch = () => {
  const config = useRuntimeConfig()
  
  // Central source of truth for API Base
  // It is CRITICAL that there are no hardcoded localhost fallbacks here
  // which might override the environment variables picked up by Nuxt.
  const apiBase = config.public.apiBase || ''
  
  if (process.client) {
    console.log('🔌 [AuthenticatedFetch] Raw Config:', config.public)
    console.log('🔌 [AuthenticatedFetch] Resolved apiBase:', apiBase)
  }

  /**
   * Helper to resolve the final URL
   */
  const resolveUrl = (url) => {
    // If it's already an absolute URL (starts with http), return as is
    if (url.startsWith('http')) return url
    
    // Ensure URL starts with / if not empty
    const normalizedUrl = url.startsWith('/') ? url : `/${url}`
    
    // Use the config value, or an empty string to allow relative requests if intended
    const base = apiBase
    
    const finalUrl = `${base}${normalizedUrl}`
    
    // Debug log to help troubleshoot Vercel connectivity
    if (process.env.NODE_ENV === 'development' || typeof window !== 'undefined') {
        console.log(`📡 [AuthenticatedFetch] Request: ${finalUrl}`)
    }
    
    return finalUrl
  }

  /**
   * Make an authenticated fetch request
   * @param {string} url - The URL to fetch (relative to apiBase, e.g., '/api/auth/login')
   * @param {RequestInit} options - Fetch options
   * @returns {Promise<Response>} - The fetch response
   */
  const authenticatedFetch = async (url, options = {}) => {
    const finalUrl = resolveUrl(url)
    
    // Get JWT token from storage
    const token = sessionStorage.getItem('token') || 
                  sessionStorage.getItem('authToken') || 
                  localStorage.getItem('token') || 
                  localStorage.getItem('authToken')
    
    // Merge headers with authentication
    const headers = {
      ...options.headers,
    }
    
    // Add Authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    // Add ngrok skip header (safe to include even for non-ngrok URLs)
    headers['ngrok-skip-browser-warning'] = 'true'
    
    // Make the request
    return fetch(finalUrl, {
      ...options,
      headers
    })
  }

  /**
   * Make an authenticated POST request with JSON body
   */
  const authenticatedPost = async (url, data) => {
    return authenticatedFetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
  }

  /**
   * Make an authenticated GET request
   */
  const authenticatedGet = async (url) => {
    return authenticatedFetch(url, {
      method: 'GET'
    })
  }

  /**
   * Helper to resolve the final WebSocket URL
   */
  const resolveWsUrl = (url) => {
    // If it's already an absolute URL, return as is
    if (url.startsWith('ws')) return url
    
    // Ensure URL starts with / if not empty
    const normalizedUrl = url.startsWith('/') ? url : `/${url}`
    
    // Resolve base from apiBase
    let base = apiBase
    
    // Convert http(s) to ws(s)
    const wsBase = base.replace(/^http/, 'ws')
    
    const finalUrl = `${wsBase}${normalizedUrl}`
    
    console.log(`🔌 [AuthenticatedFetch] WebSocket: ${finalUrl}`)
    return finalUrl
  }

  return {
    authenticatedFetch,
    authenticatedPost,
    authenticatedGet,
    resolveUrl,
    resolveWsUrl
  }
}
