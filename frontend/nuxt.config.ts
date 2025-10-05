export default defineNuxtConfig({
  devtools: { enabled: true },

  srcDir: 'src/',
  
  // Add Pinia module
  modules: [
    '@pinia/nuxt'
  ],
  
  // Nitro configuration for API proxy
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        prependPath: true
      }
    }
  },
  
  // Runtime configuration
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },
  
  // SSR configuration
  ssr: false,
  
  
  // css: [
  //   '~/assets/css/main.css'
  // ],
  
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
