/**
 * Authenticated Fetch Composable
 * 
 * Automatically includes JWT authentication token in all API requests.
 * Use this instead of raw fetch() for all backend API calls.
 */

export const useAuthenticatedFetch = () => {
  /**
   * Make an authenticated fetch request
   * @param {string} url - The URL to fetch
   * @param {RequestInit} options - Fetch options (method, body, headers, etc.)
   * @returns {Promise<Response>} - The fetch response
   */
  const authenticatedFetch = async (url, options = {}) => {
    // Get JWT token from storage
    const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken')
    
    // Merge headers with authentication
    const headers = {
      ...options.headers,
    }
    
    // Add Authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    // Make the request with authentication
    return fetch(url, {
      ...options,
      headers
    })
  }

  /**
   * Make an authenticated POST request with JSON body
   * @param {string} url - The URL to post to
   * @param {object} data - The data to send as JSON
   * @returns {Promise<Response>} - The fetch response
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
   * @param {string} url - The URL to get
   * @returns {Promise<Response>} - The fetch response
   */
  const authenticatedGet = async (url) => {
    return authenticatedFetch(url, {
      method: 'GET'
    })
  }

  return {
    authenticatedFetch,
    authenticatedPost,
    authenticatedGet
  }
}
