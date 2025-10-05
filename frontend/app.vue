<template>
  <div>
    <NuxtPage />
    <Toast />
  </div>
</template>

<script setup>
// ===== CORRECT VERSION =====
const authStore = useAuthStore()

onMounted(() => {
  console.log('🚀 App initialized')
  
  // Restore session if exists (this is the correct function name)
  authStore.restoreSession()
  
  console.log('👤 Auth state restored:', {
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user
  })
})
</script>



// uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload