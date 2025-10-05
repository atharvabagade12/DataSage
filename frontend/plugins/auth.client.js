export default defineNuxtPlugin(async () => {
    const authStore = useAuthStore()
    
    // Restore session if exists
    authStore.restoreSession()
  })
  