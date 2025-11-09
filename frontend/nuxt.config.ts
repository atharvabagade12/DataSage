export default defineNuxtConfig({
  devtools: { enabled: true },

  srcDir: 'src/',
  
  
  modules: [
    '@pinia/nuxt'
  ],
  
 
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        prependPath: true
      }
    }
  },
  
  
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
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
