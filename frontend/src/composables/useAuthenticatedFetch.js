/**
 * Authenticated Fetch Composable
 * 
 * Automatically includes JWT authentication token in all API requests.
 * Use this instead of raw fetch() for all backend API calls.
 */

export const useAuthenticatedFetch = () => {
  const config = useRuntimeConfig()
  
  // Central source of truth for API Base
  // Checks for BOTH the correct NUXT_PUBLIC_API_BASE and the typo NUXT_PUBLIC_BASE_API
  const apiBase = config.public.apiBase || config.public.baseApi || ''
  
  if (process.client) {
    if (config.public.baseApi && !config.public.apiBase) {
      console.warn('⚠️ [AuthenticatedFetch] Using fallback baseApi. Please fix your Vercel env var to NUXT_PUBLIC_API_BASE for consistency.')
    }
    console.log('🔌 [AuthenticatedFetch] Resolved apiBase:', apiBase || '(relative path)')
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

  /**
   * Make an authenticated DELETE request
   */
  const authenticatedDelete = async (url) => {
    return authenticatedFetch(url, {
      method: 'DELETE'
    })
  }

  return {
    authenticatedFetch,
    authenticatedPost,
    authenticatedGet,
    authenticatedDelete,
    resolveUrl,
    resolveWsUrl
  }
}
