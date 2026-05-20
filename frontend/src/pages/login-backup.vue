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
          <div class="brand-title-section">
            <h1 class="brand-title">DataSage</h1>
            <p class="brand-tagline">Intelligent ML Pipeline Platform</p>
          </div>
        </div>

        <!-- Auth Container -->
        <div class="auth-container">
          <!-- Tab Navigation -->
          <div class="auth-tabs" role="tablist">
            <button
              role="tab"
              :aria-selected="activeTab === 'login'"
              @click="switchTab('login')"
              :class="['tab-btn', { active: activeTab === 'login' }]"
            >
              Sign In
            </button>
            <button
              role="tab"
              :aria-selected="activeTab === 'register'"
              @click="switchTab('register')"
              :class="['tab-btn', { active: activeTab === 'register' }]"
            >
              Sign Up
            </button>
            <div class="tab-indicator" :class="{ 'right': activeTab === 'register' }"></div>
          </div>

          <!-- Login Form -->
          <transition name="fade-slide" mode="out-in">
            <form v-if="activeTab === 'login'" key="login" @submit.prevent="handleLogin" class="auth-form" novalidate>
              <div class="form-header">
                <h2>Welcome Back</h2>
                <p>Enter your credentials to access your dashboard</p>
              </div>

              <!-- Username -->
              <div class="form-group" :class="{ 'has-error': loginErrors.username }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input
                    v-model="loginForm.username"
                    id="login-username"
                    type="text"
                    placeholder="Username"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="username"
                    @blur="validateLoginField('username')"
                  />
                </div>
                <span v-if="loginErrors.username" class="field-error">{{ loginErrors.username }}</span>
              </div>

              <!-- Password -->
              <div class="form-group" :class="{ 'has-error': loginErrors.password }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input
                    v-model="loginForm.password"
                    id="login-password"
                    :type="showLoginPassword ? 'text' : 'password'"
                    placeholder="Password"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="current-password"
                    @blur="validateLoginField('password')"
                  />
                  <button type="button" class="eye-btn" @click="showLoginPassword = !showLoginPassword" :aria-label="showLoginPassword ? 'Hide password' : 'Show password'">
                    <svg v-if="showLoginPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>
                </div>
                <span v-if="loginErrors.password" class="field-error">{{ loginErrors.password }}</span>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading" class="loading-spinner"></span>
                <span v-else>Sign In</span>
              </button>

              <transition name="fade">
                <div v-if="loginError" class="error-message" role="alert">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  {{ loginError }}
                </div>
              </transition>
            </form>
          </transition>

          <!-- Register Form -->
          <transition name="fade-slide" mode="out-in">
            <form v-if="activeTab === 'register'" key="register" @submit.prevent="handleRegister" class="auth-form" novalidate>
              <div class="form-header">
                <h2>Create Account</h2>
                <p>Join DataSage and unlock powerful ML pipelines</p>
              </div>

              <!-- Username -->
              <div class="form-group" :class="{ 'has-error': registerErrors.username }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input
                    v-model="registerForm.username"
                    id="register-username"
                    type="text"
                    placeholder="Username (3–30 characters)"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="username"
                    @blur="validateRegisterField('username')"
                  />
                </div>
                <span v-if="registerErrors.username" class="field-error">{{ registerErrors.username }}</span>
              </div>

              <!-- Email -->
              <div class="form-group" :class="{ 'has-error': registerErrors.email }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                      <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                  </span>
                  <input
                    v-model="registerForm.email"
                    id="register-email"
                    type="email"
                    placeholder="Email address"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="email"
                    @blur="validateRegisterField('email')"
                  />
                </div>
                <span v-if="registerErrors.email" class="field-error">{{ registerErrors.email }}</span>
              </div>

              <!-- Password -->
              <div class="form-group" :class="{ 'has-error': registerErrors.password }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input
                    v-model="registerForm.password"
                    id="register-password"
                    :type="showRegisterPassword ? 'text' : 'password'"
                    placeholder="Password"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="new-password"
                    @blur="validateRegisterField('password')"
                  />
                  <button type="button" class="eye-btn" @click="showRegisterPassword = !showRegisterPassword" :aria-label="showRegisterPassword ? 'Hide password' : 'Show password'">
                    <svg v-if="showRegisterPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>
                </div>
                <span v-if="registerErrors.password" class="field-error">{{ registerErrors.password }}</span>
              </div>

              <!-- Password Strength Meter -->
              <div class="password-strength" v-if="registerForm.password">
                <div class="strength-bars">
                  <div
                    v-for="n in 4"
                    :key="n"
                    class="bar"
                    :class="{ active: passwordStrength >= n }"
                    :style="passwordStrength >= n ? { background: passwordStrengthColor } : {}"
                  ></div>
                </div>
                <span class="strength-text" :style="{ color: passwordStrengthColor }">
                  {{ passwordStrengthText }}
                </span>
              </div>

              <!-- Confirm Password -->
              <div class="form-group" :class="{ 'has-error': registerErrors.confirmPassword }">
                <div class="input-wrapper">
                  <span class="input-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                  </span>
                  <input
                    v-model="registerForm.confirmPassword"
                    id="register-confirm-password"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    placeholder="Confirm password"
                    :disabled="loading"
                    class="form-input"
                    autocomplete="new-password"
                    @blur="validateRegisterField('confirmPassword')"
                  />
                  <button type="button" class="eye-btn" @click="showConfirmPassword = !showConfirmPassword" :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'">
                    <svg v-if="showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>
                </div>
                <span v-if="registerErrors.confirmPassword" class="field-error">{{ registerErrors.confirmPassword }}</span>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading" class="loading-spinner"></span>
                <span v-else>Create Account</span>
              </button>

              <transition name="fade">
                <div v-if="registerSuccess" class="success-message" role="status">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  Account created! Signing you in...
                </div>
              </transition>

              <transition name="fade">
                <div v-if="registerError" class="error-message" role="alert">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
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

const router = useRouter()
const authStore = useAuthStore()

// ─── Tab state ────────────────────────────────────────────────────────────────
const activeTab = ref('login')

function switchTab(tab) {
  activeTab.value = tab
  // Clear errors when switching tabs
  loginError.value = ''
  registerError.value = ''
  registerSuccess.value = false
  Object.keys(loginErrors).forEach(k => (loginErrors[k] = ''))
  Object.keys(registerErrors).forEach(k => (registerErrors[k] = ''))
}

// ─── Shared state ─────────────────────────────────────────────────────────────
const loading = ref(false)

// ─── Login form state ──────────────────────────────────────────────────────────
const loginForm = reactive({ username: '', password: '' })
const loginError = ref('')
const showLoginPassword = ref(false)
const loginErrors = reactive({ username: '', password: '' })

// ─── Register form state ───────────────────────────────────────────────────────
const registerForm = reactive({ username: '', email: '', password: '', confirmPassword: '' })
const registerError = ref('')
const registerSuccess = ref(false)
const showRegisterPassword = ref(false)
const showConfirmPassword = ref(false)
const registerErrors = reactive({ username: '', email: '', password: '', confirmPassword: '' })

// ─── Password strength ────────────────────────────────────────────────────────
const passwordStrength = computed(() => {
  const p = registerForm.password
  if (!p) return 0
  let s = 0
  if (p.length >= 8) s++
  if (/[a-z]/.test(p)) s++
  if (/[A-Z]/.test(p)) s++
  if (/[0-9!@#$%^&*]/.test(p)) s++
  return s
})

const passwordStrengthText = computed(() => {
  const s = passwordStrength.value
  if (s <= 1) return 'Weak'
  if (s === 2) return 'Fair'
  if (s === 3) return 'Good'
  return 'Strong'
})

const passwordStrengthColor = computed(() => {
  const s = passwordStrength.value
  if (s <= 1) return '#ef4444'
  if (s === 2) return '#f59e0b'
  if (s === 3) return '#10b981'
  return '#22c55e'
})

// ─── Validation ───────────────────────────────────────────────────────────────
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validateLoginField(field) {
  if (field === 'username') {
    loginErrors.username = loginForm.username.trim() ? '' : 'Username is required'
  }
  if (field === 'password') {
    loginErrors.password = loginForm.password ? '' : 'Password is required'
  }
}

function validateLogin() {
  validateLoginField('username')
  validateLoginField('password')
  return !loginErrors.username && !loginErrors.password
}

function validateRegisterField(field) {
  if (field === 'username') {
    const u = registerForm.username.trim()
    if (!u) registerErrors.username = 'Username is required'
    else if (u.length < 3) registerErrors.username = 'Username must be at least 3 characters'
    else if (u.length > 30) registerErrors.username = 'Username must be 30 characters or fewer'
    else if (!/^[a-zA-Z0-9_ ]+$/.test(u)) registerErrors.username = 'Only letters, numbers, spaces and underscores allowed'
    else registerErrors.username = ''
  }
  if (field === 'email') {
    const e = registerForm.email.trim()
    if (!e) registerErrors.email = 'Email is required'
    else if (!EMAIL_RE.test(e)) registerErrors.email = 'Please enter a valid email address'
    else registerErrors.email = ''
  }
  if (field === 'password') {
    const p = registerForm.password
    if (!p) registerErrors.password = 'Password is required'
    else if (p.length < 8) registerErrors.password = 'Password must be at least 8 characters'
    else if (passwordStrength.value < 2) registerErrors.password = 'Password is too weak — add uppercase letters or numbers'
    else registerErrors.password = ''
    // Re-validate confirm if already touched
    if (registerForm.confirmPassword) validateRegisterField('confirmPassword')
  }
  if (field === 'confirmPassword') {
    if (!registerForm.confirmPassword) registerErrors.confirmPassword = 'Please confirm your password'
    else if (registerForm.confirmPassword !== registerForm.password) registerErrors.confirmPassword = 'Passwords do not match'
    else registerErrors.confirmPassword = ''
  }
}

function validateRegister() {
  ;['username', 'email', 'password', 'confirmPassword'].forEach(validateRegisterField)
  return !registerErrors.username && !registerErrors.email && !registerErrors.password && !registerErrors.confirmPassword
}


const handleLogin = async () => {
  if (!validateLogin()) return

  loading.value = true
  loginError.value = ''

  try {
    const result = await authStore.login({
      username: loginForm.username.trim(),
      password: loginForm.password
    })

    if (result?.success) {
      await router.push('/dashboard')
    } else {
      loginError.value = 'Invalid Credentials'
    }
  } catch (err) {
    loginError.value = 'Invalid Credentials'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!validateRegister()) return

  loading.value = true
  registerError.value = ''
  registerSuccess.value = false

  try {
    const result = await authStore.signup({
      username: registerForm.username.trim(),
      email: registerForm.email.trim(),
      password: registerForm.password
    })

    if (result?.success) {
      registerSuccess.value = true
      // Auto-navigate after brief success flash
      setTimeout(() => router.push('/dashboard'), 1500)
    } else {
      registerError.value = result?.error || 'Registration failed. Please try again.'
    }
  } catch (err) {
    registerError.value = err.message || 'An unexpected error occurred.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>

* {
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
  25%       { transform: translate(50px, -50px) scale(1.1); }
  50%       { transform: translate(-50px, 50px) scale(0.9); }
  75%       { transform: translate(30px, 30px) scale(1.05); }
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
  border-radius: 50%;
  opacity: 0.3;
  animation: drift 15s infinite linear;
}

@keyframes drift {
  from { transform: translateY(100vh) translateX(0); }
  to   { transform: translateY(-100px) translateX(100px); }
}

/* ====== PARTICLE POSITIONS (all 20) ====== */
.particle:nth-child(1)  { left: 5%;  top: 15%; animation-delay: 0s;    animation-duration: 14s; }
.particle:nth-child(2)  { left: 15%; top: 70%; animation-delay: 1s;    animation-duration: 17s; }
.particle:nth-child(3)  { left: 25%; top: 40%; animation-delay: 2s;    animation-duration: 12s; }
.particle:nth-child(4)  { left: 35%; top: 85%; animation-delay: 3s;    animation-duration: 19s; }
.particle:nth-child(5)  { left: 45%; top: 10%; animation-delay: 4s;    animation-duration: 16s; }
.particle:nth-child(6)  { left: 55%; top: 55%; animation-delay: 5s;    animation-duration: 13s; }
.particle:nth-child(7)  { left: 65%; top: 25%; animation-delay: 6s;    animation-duration: 18s; }
.particle:nth-child(8)  { left: 75%; top: 75%; animation-delay: 7s;    animation-duration: 11s; }
.particle:nth-child(9)  { left: 85%; top: 45%; animation-delay: 8s;    animation-duration: 15s; }
.particle:nth-child(10) { left: 92%; top: 5%;  animation-delay: 9s;    animation-duration: 20s; }
.particle:nth-child(11) { left: 10%; top: 90%; animation-delay: 0.5s;  animation-duration: 16s; }
.particle:nth-child(12) { left: 20%; top: 30%; animation-delay: 1.5s;  animation-duration: 14s; }
.particle:nth-child(13) { left: 30%; top: 60%; animation-delay: 2.5s;  animation-duration: 18s; }
.particle:nth-child(14) { left: 40%; top: 20%; animation-delay: 3.5s;  animation-duration: 12s; }
.particle:nth-child(15) { left: 50%; top: 80%; animation-delay: 4.5s;  animation-duration: 17s; }
.particle:nth-child(16) { left: 60%; top: 35%; animation-delay: 5.5s;  animation-duration: 13s; }
.particle:nth-child(17) { left: 70%; top: 65%; animation-delay: 6.5s;  animation-duration: 19s; }
.particle:nth-child(18) { left: 80%; top: 15%; animation-delay: 7.5s;  animation-duration: 15s; }
.particle:nth-child(19) { left: 88%; top: 50%; animation-delay: 8.5s;  animation-duration: 11s; }
.particle:nth-child(20) { left: 3%;  top: 50%; animation-delay: 9.5s;  animation-duration: 20s; }

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

/* ====== BRAND HEADER ====== */
.brand-header {
  text-align: center;
  color: white;
}

.brand-title-section {
  text-align: center;
}

.brand-title {
  font-size: 3rem;
  font-weight: 800;
  margin: 0 0 0.25rem 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.brand-tagline {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.03em;
}

/* ====== AUTH CONTAINER ====== */
.auth-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

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
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 10px;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
  font-family: inherit;
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
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  margin-bottom: 1.75rem;
}

.form-header h2 {
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.form-header p {
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.25rem;
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
  display: flex;
}

.form-input {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Error border on invalid fields */
.has-error .form-input {
  border-color: rgba(239, 68, 68, 0.6);
}

.has-error .form-input:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.field-error {
  display: block;
  margin-top: 0.35rem;
  font-size: 0.78rem;
  color: #f87171;
  padding-left: 0.25rem;
}

/* ====== EYE BUTTON (password visibility) ====== */
.eye-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
  line-height: 1;
}

.eye-btn:hover {
  color: rgba(255, 255, 255, 0.8);
}

/* ====== SUBMIT BUTTON ====== */
.submit-btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.9rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  letter-spacing: 0.02em;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ====== LOADING SPINNER ====== */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ====== PASSWORD STRENGTH ====== */
.password-strength {
  margin-top: -0.75rem;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.strength-bars {
  display: flex;
  gap: 0.3rem;
  flex: 1;
}

.bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  transition: background 0.35s ease;
}

.strength-text {
  font-size: 0.78rem;
  font-weight: 600;
  white-space: nowrap;
  transition: color 0.35s ease;
  min-width: 44px;
}

/* ====== ALERTS ====== */
.error-message,
.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  margin-top: 1.25rem;
  font-size: 0.9rem;
  animation: slideInUp 0.3s ease;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.success-message {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ====== TRANSITIONS ====== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(16px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-16px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ====== RESPONSIVE DESIGN ====== */
@media (max-width: 768px) {
  .login-wrapper {
    padding: 1rem;
    align-items: flex-start;
    padding-top: 3rem;
  }

  .auth-container {
    padding: 2rem 1.75rem;
  }

  .brand-title {
    font-size: 2.5rem;
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
    font-size: 1.4rem;
  }
}

/* ====== ACCESSIBILITY ====== */
@media (prefers-reduced-motion: reduce) {
  .gradient-sphere,
  .particle {
    animation: none !important;
  }

  .submit-btn,
  .tab-indicator,
  .form-input,
  .bar,
  .strength-text {
    transition: none !important;
  }

  .submit-btn:hover:not(:disabled) {
    transform: none !important;
  }
}

/* ====== FOCUS STYLES (keyboard navigation) ====== */
.form-input:focus-visible,
.submit-btn:focus-visible,
.tab-btn:focus-visible,
.eye-btn:focus-visible {
  outline: 2px solid rgba(102, 126, 234, 0.9);
  outline-offset: 2px;
}
</style>
