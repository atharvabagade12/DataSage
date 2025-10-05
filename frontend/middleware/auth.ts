export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()

  // Skip auth check for login and public pages
  const publicRoutes = ['/login', '/', '/register']
  if (publicRoutes.includes(to.path)) {
    return
  }

  // Check if user is authenticated
  if (!authStore.isLoggedIn) {
    // Redirect to login with the intended destination
    return navigateTo(`/login?redirect=${to.path}`)
  }

  // Optional: Check token expiry
  if (authStore.token) {
    try {
      // Decode JWT token to check expiry (basic check)
      const tokenData = JSON.parse(atob(authStore.token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      if (tokenData.exp && tokenData.exp < currentTime) {
        // Token expired, logout and redirect
        authStore.logout()
        return navigateTo('/login?message=session_expired')
      }
    } catch (error) {
      // Invalid token format, logout
      authStore.logout()
      return navigateTo('/login?message=invalid_token')
    }
  }
})
