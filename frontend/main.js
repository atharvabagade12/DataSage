import { createApp } from 'vue'
import { createPinia } from 'pinia'  // ✅ ADD THIS
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())  // ✅ ADD THIS LINE
app.use(router)

app.mount('#app')