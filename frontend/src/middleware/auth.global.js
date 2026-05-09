export default defineNuxtRouteMiddleware((to) => {
  if (process.server) return

  const authStore = useAuthStore()
  const publicRoutes = ['/', '/login', '/register']

  if (publicRoutes.includes(to.path)) {
    return
  }

  if (!authStore.isLoggedIn) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  if (!authStore.token) {
    authStore.logout()
    return navigateTo('/login')
  }

  try {
    const tokenData = JSON.parse(atob(authStore.token.split('.')[1]))
    const currentTime = Math.floor(Date.now() / 1000)

    if (tokenData.exp && tokenData.exp < currentTime) {
      authStore.logout()
      return navigateTo('/login?message=session_expired')
    }
  } catch {
    authStore.logout()
    return navigateTo('/login?message=invalid_token')
  }
})
