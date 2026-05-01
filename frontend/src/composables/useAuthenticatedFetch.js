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
    
    const token = sessionStorage.getItem('token') || 
                  sessionStorage.getItem('authToken') || 
                  localStorage.getItem('token') || 
                  localStorage.getItem('authToken')
    
    const headers = { ...options.headers }
    if (token) headers['Authorization'] = `Bearer ${token}`
    headers['ngrok-skip-browser-warning'] = 'true'

    // Use caller's signal if provided (e.g. verifyToken), else apply 60s default timeout
    const controller = options.signal ? null : new AbortController();
    const timeoutId = controller ? setTimeout(() => controller.abort(), 60000) : null;

    try {
      const response = await fetch(finalUrl, {
        ...options,
        headers,
        signal: options.signal || controller.signal
      });
      if (timeoutId) clearTimeout(timeoutId);
      return response;
    } catch (err) {
      if (timeoutId) clearTimeout(timeoutId);
      throw err;
    }
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
