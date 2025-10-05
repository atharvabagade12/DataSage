export default defineNuxtRouteMiddleware(async (to, from) => {
  if (process.server) return
  
  const { isAuthenticated, verifyToken } = useAuth()
  
  // Public routes
  const publicRoutes = ['/login', '/']
  
  if (publicRoutes.includes(to.path)) {
    return
  }
  
  // Check if user is authenticated
  if (!isAuthenticated()) {
    return navigateTo('/login')
  }
  
  // Verify token is still valid
  const isValid = await verifyToken()
  
  if (!isValid) {
    localStorage.clear()
    sessionStorage.clear()
    return navigateTo('/login')
  }
})
