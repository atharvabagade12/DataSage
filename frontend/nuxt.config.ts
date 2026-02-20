export default defineNuxtConfig({
  compatibilityDate: '2025-11-25',
  
  devtools: { enabled: true },

  srcDir: 'src/',
  
  
  modules: [
    '@pinia/nuxt'
  ],
  
 
  runtimeConfig: {
    public: {
      // Correct variable: NUXT_PUBLIC_API_BASE
      apiBase: '',
      // Handling user typo: NUXT_PUBLIC_BASE_API
      baseApi: ''
    }
  },
  
  
  ssr: false,
  
  

  
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "~/assets/css/main.css";'
        }
      }
    }
  }
})
