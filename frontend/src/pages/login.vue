<template>
  <div class="login-container">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="gradient-sphere sphere-1"></div>
      <div class="gradient-sphere sphere-2"></div>
      <div class="gradient-sphere sphere-3"></div>
      <div class="data-particles">
        <span v-for="i in 20" :key="i" class="particle"></span>
      </div>
    </div>

    <!-- Main Content - Centered Layout -->
    <div class="login-wrapper">
      <div class="auth-panel">
        <!-- DataSage Brand Header -->
        <div class="brand-header">
          

          <!-- Brand Title -->
          <div class="brand-title-section">
            <h1 class="brand-title">DataSage</h1>
          </div>
        </div>

        <!-- Auth Container -->
        <div class="auth-container">
          <!-- Tab Navigation -->
          <div class="auth-tabs">
            <button 
              @click="activeTab = 'login'" 
              :class="['tab-btn', { active: activeTab === 'login' }]"
            >
              Sign In
            </button>
            <button 
              @click="activeTab = 'register'" 
              :class="['tab-btn', { active: activeTab === 'register' }]"
            >
              Sign Up
            </button>
            <div class="tab-indicator" :class="{ 'right': activeTab === 'register' }"></div>
          </div>

          <!-- Login Form -->
          <transition name="fade-slide">
            <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
              <div class="form-header">
                <h2>Welcome Back</h2>
                <p>Enter your credentials to access your dashboard</p>
              </div>

              <div class="form-group">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    v-model="loginForm.username"
                    type="text"
                    placeholder="Username"
                    required
                    :disabled="loading"
                    class="form-input"
                    autocomplete="username"
                  />
                </div>
              </div>

              <div class="form-group">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    v-model="loginForm.password"
                    type="password"
                    placeholder="Password"
                    required
                    :disabled="loading"
                    class="form-input"
                    autocomplete="current-password"
                  />
                </div>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading" class="loading-spinner"></span>
                <span v-else>Sign In</span>
              </button>

              <transition name="fade">
                <div v-if="loginError" class="error-message">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  {{ loginError }}
                </div>
              </transition>
            </form>
          </transition>

          <!-- Register Form -->
          <transition name="fade-slide">
            <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
              <div class="form-header">
                <h2>Create Account</h2>
                <p>Join DataSage and unlock powerful ML pipeline</p>
              </div>

              <div class="form-group">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    v-model="registerForm.username"
                    type="text"
                    placeholder="Username"
                    required
                    :disabled="loading"
                    class="form-input"
                    autocomplete="username"
                  />
                </div>
              </div>

              <div class="form-group">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                      <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                  </span>
                  <input 
                    v-model="registerForm.email"
                    type="email"
                    placeholder="Email address"
                    required
                    :disabled="loading"
                    class="form-input"
                    autocomplete="email"
                  />
                </div>
              </div>

              <div class="form-group">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    v-model="registerForm.password"
                    type="password"
                    placeholder="Password"
                    required
                    :disabled="loading"
                    class="form-input"
                    autocomplete="new-password"
                  />
                </div>
              </div>

              <div class="password-strength" v-if="registerForm.password">
                <div class="strength-bars">
                  <div class="bar" :class="{ active: passwordStrength >= 1 }"></div>
                  <div class="bar" :class="{ active: passwordStrength >= 2 }"></div>
                  <div class="bar" :class="{ active: passwordStrength >= 3 }"></div>
                  <div class="bar" :class="{ active: passwordStrength >= 4 }"></div>
                </div>
                <span class="strength-text">{{ passwordStrengthText }}</span>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading" class="loading-spinner"></span>
                <span v-else>Create Account</span>
              </button>

              <transition name="fade">
                <div v-if="registerSuccess" class="success-message">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                  Account created! Entering into dashboard...
                </div>
              </transition>

              <transition name="fade">
                <div v-if="registerError" class="error-message">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  {{ registerError }}
                </div>
              </transition>
            </form>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const { authenticatedPost } = useAuthenticatedFetch();
const API_BASE = `/api/auth`

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('login')
const loading = ref(false)
const loginError = ref('')
const registerError = ref('')
const registerSuccess = ref(false)



const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  email: '',
  password: ''
})


const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return 0
  let strength = 0
  if (password.length >= 8) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  return strength
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return 'Weak'
  if (strength === 2) return 'Fair'
  if (strength === 3) return 'Good'
  return 'Strong'
})

const passwordStrengthColor = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return '#ef4444'
  if (strength === 2) return '#f59e0b'
  if (strength === 3) return '#10b981'
  return '#22c55e'
})


const handleLogin = async () => {
  loading.value = true
  loginError.value = ''
  
  try {
    const response = await authenticatedPost(`${API_BASE}/login`, {
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    localStorage.setItem('authToken', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    sessionStorage.setItem('user', JSON.stringify(data.user))
    
    await router.push('/dashboard')
    
  } catch (error) {
    loginError.value = error.message
  } finally {
    loading.value = false
  }
}


const handleRegister = async () => {
  loading.value = true
  registerError.value = ''
  registerSuccess.value = false
  
  try {
    const response = await authenticatedPost(`${API_BASE}/register`, {
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }
    
    registerSuccess.value = true
    
    // Auto-login after 2 seconds
    setTimeout(async () => {
      try {
        const loginResponse = await fetch(`${API_BASE}/login`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': 'true'
          },
          body: JSON.stringify({
            username: registerForm.username,
            password: registerForm.password
          })
        })
        
        if (loginResponse.ok) {
          const loginData = await loginResponse.json()
          localStorage.setItem('authToken', loginData.access_token)
          localStorage.setItem('user', JSON.stringify(loginData.user))
          sessionStorage.setItem('user', JSON.stringify(loginData.user))
          await router.push('/dashboard')
        }
      } catch (error) {
        activeTab.value = 'login'
      }
    }, 2000)
    
  } catch (error) {
    registerError.value = error.message
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>

*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  background: #0a0a0a;
  overflow: hidden;
  position: relative;
}

/* ====== ANIMATED BACKGROUND ====== */
.animated-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.gradient-sphere {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s infinite ease-in-out;
}

.sphere-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -200px;
  left: -200px;
  animation-delay: 0s;
}

.sphere-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  bottom: -200px;
  right: -200px;
  animation-delay: 5s;
}

.sphere-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(50px, -50px) scale(1.1); }
  50% { transform: translate(-50px, 50px) scale(0.9); }
  75% { transform: translate(30px, 30px) scale(1.05); }
}

.data-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: #fff;
  opacity: 0.3;
  animation: drift 15s infinite linear;
}

@keyframes drift {
  from { transform: translateY(100vh) translateX(0); }
  to { transform: translateY(-100px) translateX(100px); }
}

/* ====== MAIN LAYOUT - CENTERED ====== */
.login-wrapper {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* ====== CENTERED AUTH PANEL ====== */
.auth-panel {
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

/* ====== BRAND HEADER - CENTERED ====== */
.brand-header {
  text-align: center;
  color: white;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.logo-wrapper {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  position: relative;
  transition: all 0.3s ease;
}

.logo-wrapper::before {
  content: '';
  position: absolute;
  inset: -2px;
  padding: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 22px;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0.6;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-title-section {
  text-align: center;
  margin-bottom: 0.5rem;
}

.brand-title {
  font-size: 3rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
  line-height: 2;
  text-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.brand-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-weight: 400;
  line-height: 1.2;
}

.brand-subtitle-accent {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0.2rem 0 0 0;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

/* ====== AUTH CONTAINER ====== */
.auth-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

/* Keep all your existing auth form styles... */
/* ====== TAB NAVIGATION ====== */
.auth-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.25rem;
  border-radius: 12px;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.tab-btn.active {
  color: white;
}

.tab-indicator {
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
  width: calc(50% - 0.25rem);
  height: calc(100% - 0.5rem);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.tab-indicator.right {
  left: 50%;
}

/* ====== FORM STYLES ====== */
.auth-form {
  color: white;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.4);
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.password-strength {
  margin-top: -1rem;
  margin-bottom: 1.5rem;
}

.strength-bars {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.bar.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.strength-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

.error-message,
.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 12px;
  margin-top: 1.5rem;
  font-size: 0.95rem;
  animation: slideInUp 0.3s ease;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.success-message {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ====== TRANSITIONS ====== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ====== PARTICLE POSITIONS ====== */
.particle:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
.particle:nth-child(2) { left: 20%; top: 80%; animation-delay: 1s; }
/* ... keep all your existing particle styles ... */

/* ====== RESPONSIVE DESIGN ====== */
@media (max-width: 768px) {
  .login-wrapper {
    padding: 1rem;
  }
  
  .auth-container {
    padding: 2rem;
  }
  
  .brand-title {
    font-size: 2.5rem;
  }
  
  .logo-wrapper {
    width: 70px;
    height: 70px;
  }
  
  .logo-svg {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .auth-container {
    padding: 1.5rem;
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .form-header h2 {
    font-size: 1.5rem;
  }
}

/* ====== ACCESSIBILITY ====== */
@media (prefers-reduced-motion: reduce) {
  .gradient-sphere,
  .particle,
  .submit-btn {
    animation: none !important;
    transition: none !important;
  }
  
  .submit-btn:hover {
    transform: none !important;
  }
}

/* ====== FOCUS STYLES ====== */
.form-input:focus,
.submit-btn:focus,
.tab-btn:focus {
  outline: 2px solid rgba(102, 126, 234, 0.8);
  outline-offset: 2px;
}
</style>
