<template>
  <div class="login-container">
    <!-- Ambient Glow System (Identical to landing page theme) -->
    <div class="ambient-glow">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
    </div>
    
    <!-- Cyber Dotted Blueprint Overlay & Texturing -->
    <div class="hero-grid-overlay"></div>
    <div class="noise-overlay"></div>

    <!-- Drifting Atmospheric Stars -->
    <div class="data-particles">
      <span v-for="i in 20" :key="i" class="particle"></span>
    </div>

    <!-- Centered Content Grid Wrapper -->
    <div class="login-wrapper">
      <div class="auth-panel">
        
        <!-- Premium logo header section -->
        <div class="brand-header" @click="router.push('/')" title="Return to Landing Page">
          <div class="branding-logo-box">
            <div class="logo-image-wrapper">
              <img src="@/assets/logo.jpeg" alt="DataSage Logo" class="logo-img" />
            </div>
          </div>
          <div class="branding-text">
            <h1 class="brand-title">DataSage</h1>
            <p class="brand-tagline"></p>
          </div>
        </div>

        <!-- Glassmorphism Auth Card -->
        <div class="auth-card glass-panel">
          <div class="auth-glow"></div>

          <!-- Sliding Glass Tab Selectors -->
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

          <!-- Form transition block -->
          <div class="form-container-relative">
            <transition name="fade-slide" mode="out-in">
              
              <!-- SIGN IN FORM -->
              <form v-if="activeTab === 'login'" key="login" @submit.prevent="handleLogin" class="auth-form" novalidate>
                <div class="form-header">
                  <h2 class="form-title">Welcome Back</h2>
                  <p class="form-subtitle">Access your cognitive machine learning workspace</p>
                </div>

                <!-- Username Input (Floating Label) -->
                <div class="form-group" :class="{ 'has-error': loginErrors.username, 'has-content': loginForm.username || focus.loginUsername }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="username"
                      @focus="focus.loginUsername = true"
                      @blur="focus.loginUsername = false; validateLoginField('username')"
                    />
                    <label for="login-username" class="floating-label">Username</label>
                  </div>
                  <span v-if="loginErrors.username" class="field-error">{{ loginErrors.username }}</span>
                </div>

                <!-- Password Input (Floating Label) -->
                <div class="form-group" :class="{ 'has-error': loginErrors.password, 'has-content': loginForm.password || focus.loginPassword }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="current-password"
                      @focus="focus.loginPassword = true"
                      @blur="focus.loginPassword = false; validateLoginField('password')"
                    />
                    <label for="login-password" class="floating-label">Password</label>
                    
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

                <!-- Sign in button -->
                <button type="submit" class="submit-btn" :disabled="loading">
                  <span v-if="loading" class="loading-spinner"></span>
                  <span v-else class="btn-content">
                    <span>Sign In to Workspace</span>
                    <span class="btn-arrow">→</span>
                  </span>
                  <span class="btn-shine"></span>
                </button>

                <!-- Failure Alerts -->
                <transition name="fade">
                  <div v-if="loginError" class="error-message" role="alert">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    {{ loginError }}
                  </div>
                </transition>
              </form>

              <!-- SIGN UP FORM -->
              <form v-else key="register" @submit.prevent="handleRegister" class="auth-form" novalidate>
                <div class="form-header">
                  <h2 class="form-title">Create Account</h2>
                  <p class="form-subtitle">Join DataSage and compile raw data pipelines instantly</p>
                </div>

                <!-- Username Input -->
                <div class="form-group" :class="{ 'has-error': registerErrors.username, 'has-content': registerForm.username || focus.registerUsername }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="username"
                      @focus="focus.registerUsername = true"
                      @blur="focus.registerUsername = false; validateRegisterField('username')"
                    />
                    <label for="register-username" class="floating-label">Username</label>
                  </div>
                  <span v-if="registerErrors.username" class="field-error">{{ registerErrors.username }}</span>
                </div> 

                <!-- Email Input -->
                <div class="form-group" :class="{ 'has-error': registerErrors.email, 'has-content': registerForm.email || focus.registerEmail }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="email"
                      @focus="focus.registerEmail = true"
                      @blur="focus.registerEmail = false; validateRegisterField('email')"
                    />
                    <label for="register-email" class="floating-label">Email address</label>
                  </div>
                  <span v-if="registerErrors.email" class="field-error">{{ registerErrors.email }}</span>
                </div>

                <!-- Password Inpu -->
                <div class="form-group" :class="{ 'has-error': registerErrors.password, 'has-content': registerForm.password || focus.registerPassword }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="new-password"
                      @focus="focus.registerPassword = true"
                      @blur="focus.registerPassword = false; validateRegisterField('password')"
                    />
                    <label for="register-password" class="floating-label">Password</label>
                    
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

                <!-- Confirm Password Input  -->
                <div class="form-group" :class="{ 'has-error': registerErrors.confirmPassword, 'has-content': registerForm.confirmPassword || focus.registerConfirmPassword }">
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
                      :disabled="loading"
                      class="form-input"
                      autocomplete="new-password"
                      @focus="focus.registerConfirmPassword = true"
                      @blur="focus.registerConfirmPassword = false; validateRegisterField('confirmPassword')"
                    />
                    <label for="register-confirm-password" class="floating-label">Confirm password</label>
                    
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

                <!-- Submit Button -->
                <button type="submit" class="submit-btn" :disabled="loading">
                  <span v-if="loading" class="loading-spinner"></span>
                  <span v-else class="btn-content">
                    <span>Compile Platform Account</span>
                    <span class="btn-arrow">→</span>
                  </span>
                  <span class="btn-shine"></span>
                </button>

                <!-- Feedback Notifications -->
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

// Focus tracking for input floating labels
const focus = reactive({
  loginUsername: false,
  loginPassword: false,
  registerUsername: false,
  registerEmail: false,
  registerPassword: false,
  registerConfirmPassword: false
})

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  width: 100vw;
  background: #030307;
  color: #fff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow-x: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ====== CINEMATIC BACKGROUNDS ====== */
.ambient-glow {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(140px);
  opacity: 0.15;
  mix-blend-mode: screen;
  animation: float-orb 25s ease-in-out infinite alternate;
}

.orb-1 {
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, #00f0ff 0%, rgba(0, 240, 255, 0) 70%);
  top: -15%;
  left: -10%;
}

.orb-2 {
  width: 60vw;
  height: 60vw;
  background: radial-gradient(circle, #9d4edd 0%, rgba(157, 78, 221, 0) 75%);
  bottom: -15%;
  right: -15%;
  animation-delay: -5s;
}

.orb-3 {
  width: 45vw;
  height: 45vw;
  background: radial-gradient(circle, #3b82f6 0%, rgba(59, 130, 246, 0) 80%);
  top: 25%;
  left: 20%;
  animation-delay: -10s;
}

@keyframes float-orb {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(4%, -4%) scale(1.04); }
  100% { transform: translate(-4%, 4%) scale(0.96); }
}

.hero-grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
  pointer-events: none;
  z-index: 0;
}

.noise-overlay {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.012;
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 0;
}

/* ====== BACKGROUND PARTICLES ====== */
.data-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: #fff;
  border-radius: 50%;
  opacity: 0.15;
  animation: drift 15s infinite linear;
}

@keyframes drift {
  from { transform: translateY(105vh) translateX(0); }
  to   { transform: translateY(-10vh) translateX(80px); }
}

.particle:nth-child(1)  { left: 5%;  top: 15%; animation-delay: 0s;    animation-duration: 18s; }
.particle:nth-child(2)  { left: 15%; top: 70%; animation-delay: 1.5s;  animation-duration: 21s; }
.particle:nth-child(3)  { left: 25%; top: 40%; animation-delay: 3s;    animation-duration: 15s; }
.particle:nth-child(4)  { left: 35%; top: 85%; animation-delay: 0.5s;  animation-duration: 23s; }
.particle:nth-child(5)  { left: 45%; top: 10%; animation-delay: 4s;    animation-duration: 19s; }
.particle:nth-child(6)  { left: 55%; top: 55%; animation-delay: 2s;    animation-duration: 16s; }
.particle:nth-child(7)  { left: 65%; top: 25%; animation-delay: 5s;    animation-duration: 22s; }
.particle:nth-child(8)  { left: 75%; top: 75%; animation-delay: 1s;    animation-duration: 14s; }
.particle:nth-child(9)  { left: 85%; top: 45%; animation-delay: 6s;    animation-duration: 17s; }
.particle:nth-child(10) { left: 93%; top: 5%;  animation-delay: 2.5s;  animation-duration: 24s; }
.particle:nth-child(11) { left: 8%;  top: 90%; animation-delay: 3.5s;  animation-duration: 20s; }
.particle:nth-child(12) { left: 18%; top: 32%; animation-delay: 0.8s;  animation-duration: 16s; }
.particle:nth-child(13) { left: 28%; top: 62%; animation-delay: 4.5s;  animation-duration: 22s; }
.particle:nth-child(14) { left: 38%; top: 22%; animation-delay: 1.2s;  animation-duration: 15s; }
.particle:nth-child(15) { left: 48%; top: 82%; animation-delay: 5.5s;  animation-duration: 21s; }
.particle:nth-child(16) { left: 58%; top: 37%; animation-delay: 2.2s;  animation-duration: 17s; }
.particle:nth-child(17) { left: 68%; top: 67%; animation-delay: 6.5s;  animation-duration: 23s; }
.particle:nth-child(18) { left: 78%; top: 17%; animation-delay: 0.3s;  animation-duration: 19s; }
.particle:nth-child(19) { left: 88%; top: 52%; animation-delay: 3.8s;  animation-duration: 14s; }
.particle:nth-child(20) { left: 96%; top: 78%; animation-delay: 4.8s;  animation-duration: 25s; }

/* ====== CENTERED STRUCTURE ====== */
.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 480px;
  padding: 3rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-panel {
  display: flex;
  flex-direction: column;
  gap: 2.2rem;
  width: 100%;
}

/* ====== BRAND HEADER (ABOVE CARD) ====== */
.brand-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  text-align: center;
  cursor: pointer;
  user-select: none;
  transition: opacity 0.25s ease;
}

.brand-header:hover {
  opacity: 0.9;
}

.branding-logo-box {
  width: 52px;
  height: 52px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.4),
    0 0 20px rgba(0, 240, 255, 0.06);
  padding: 3px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.brand-header:hover .branding-logo-box {
  transform: translateY(-2px);
  border-color: rgba(0, 240, 255, 0.25);
  box-shadow: 
    0 12px 32px rgba(0, 0, 0, 0.5),
    0 0 25px rgba(0, 240, 255, 0.15);
}

.logo-image-wrapper {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.branding-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.brand-title {
  font-size: 2.2rem;
  font-weight: 900;
  font-family: 'Outfit', sans-serif;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
}

.brand-tagline {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.45);
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ====== MODERN GLASSMORPHISM CARD ====== */
.auth-card {
  background: rgba(10, 10, 18, 0.45);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  padding: 2.5rem 2.2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 24px 60px rgba(0, 0, 0, 0.6),
    0 0 100px rgba(157, 78, 221, 0.03);
}

.auth-glow {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 80px;
  background: radial-gradient(ellipse, rgba(0, 240, 255, 0.08) 0%, rgba(0, 240, 255, 0) 70%);
  pointer-events: none;
  z-index: 0;
}

/* ====== SLIDING GLASS TABS ====== */
.auth-tabs {
  display: flex;
  position: relative;
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.04);
  padding: 0.25rem;
  border-radius: 12px;
  margin-bottom: 2.2rem;
  z-index: 2;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.92rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 10px;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
  font-family: inherit;
}

.tab-btn.active {
  color: #fff;
}

.tab-indicator {
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
  width: calc(50% - 0.25rem);
  height: calc(100% - 0.5rem);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 9px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 1;
}

.tab-indicator.right {
  left: 50%;
}

/* ====== FORM HEADERS ====== */
.form-container-relative {
  position: relative;
  width: 100%;
}

.auth-form {
  position: relative;
  z-index: 1;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.6rem;
  font-weight: 750;
  font-family: 'Outfit', sans-serif;
  letter-spacing: -0.01em;
  color: #fff;
  margin-bottom: 0.4rem;
}

.form-subtitle {
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.88rem;
  line-height: 1.4;
}

/* ====== FUTURISTIC INPUTS & FLOATING LABELS ====== */
.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1.1rem;
  color: rgba(255, 255, 255, 0.3);
  pointer-events: none;
  display: flex;
  align-items: center;
  transition: color 0.25s ease;
}

.form-input {
  width: 100%;
  padding: 1.1rem 3.2rem 1.1rem 2.8rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  color: #fff;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.035);
  border-color: rgba(0, 240, 255, 0.3);
  box-shadow: 
    0 0 0 3px rgba(0, 240, 255, 0.08),
    0 4px 20px rgba(0, 0, 0, 0.2);
}

/* Icon focus styling */
.form-input:focus ~ .input-icon,
.form-input:focus ~ label ~ .input-icon,
.input-wrapper:focus-within .input-icon {
  color: #00f0ff;
}

/* Floating Label Animation */
.floating-label {
  position: absolute;
  left: 2.8rem;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.95rem;
  pointer-events: none;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  transform-origin: 0 0;
  user-select: none;
}

/* Shift label upwards when focused or containing content */
.form-group.has-content .floating-label,
.form-input:focus ~ .floating-label {
  transform: translateY(-24px) scale(0.8);
  color: #00f0ff;
  left: 1.1rem;
}

/* Push input text slightly down when label is active */
.form-group.has-content .form-input,
.form-input:focus {
  padding-top: 1.4rem;
  padding-bottom: 0.8rem;
}

/* Error States */
.has-error .form-input {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.02);
}

.has-error .form-input:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.has-error .floating-label {
  color: #f87171 !important;
}

.field-error {
  display: block;
  margin-top: 0.4rem;
  font-size: 0.78rem;
  color: #f87171;
  padding-left: 0.4rem;
  animation: slide-up 0.25s ease;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ====== EYE BUTTON FOR PASSWORD ====== */
.eye-btn {
  position: absolute;
  right: 1.1rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
  z-index: 2;
}

.eye-btn:hover {
  color: #00f0ff;
}

/* ====== PASSWORD STRENGTH METER ====== */
.password-strength {
  margin-top: -0.9rem;
  margin-bottom: 1.4rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0 0.2rem;
}

.strength-bars {
  display: flex;
  gap: 0.35rem;
  flex: 1;
}

.bar {
  flex: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
  transition: background 0.35s ease;
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
  transition: color 0.35s ease;
  min-width: 44px;
  text-align: right;
}

/* ====== SHINY SUBMIT BUTTON ====== */
.submit-btn {
  width: 100%;
  margin-top: 0.6rem;
  padding: 1.05rem;
  background: linear-gradient(135deg, #00f0ff 0%, #4f46e5 50%, #9d4edd 100%);
  background-size: 200% 200%;
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 0.98rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.25);
  animation: gradient-shift 6s ease infinite;
}

@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 30px rgba(79, 70, 229, 0.4),
    0 0 15px rgba(0, 240, 255, 0.2);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  position: relative;
  z-index: 2;
}

.btn-arrow {
  font-size: 1.15rem;
  transition: transform 0.25s ease;
}

.submit-btn:hover:not(:disabled) .btn-arrow {
  transform: translateX(4px);
}

/* Button Swipe Shine Overlay */
.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.15) 30%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0.15) 70%,
    transparent 100%
  );
  transition: none;
  z-index: 1;
}

.submit-btn:hover:not(:disabled) .btn-shine {
  animation: shine-swipe 1.4s infinite ease-in-out;
}

@keyframes shine-swipe {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Loading Spinner inside Button */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  position: relative;
  z-index: 2;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ====== ERROR & SUCCESS MESSAGES ====== */
.error-message,
.success-message {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1.1rem;
  border-radius: 12px;
  margin-top: 1.4rem;
  font-size: 0.88rem;
  line-height: 1.4;
  animation: alert-slide 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 550;
}

.error-message {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.success-message {
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #34d399;
}

@keyframes alert-slide {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ====== BUTTER SMOOTH TRANSITIONS ====== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1), transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px) scale(0.98);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px) scale(0.98);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ====== ACCESSIBILITY & REDUCED MOTION ====== */
@media (prefers-reduced-motion: reduce) {
  .glow-orb,
  .particle,
  .submit-btn,
  .logo-pulse-core,
  .logo-radar-ring {
    animation: none !important;
  }

  .submit-btn,
  .tab-indicator,
  .form-input,
  .bar,
  .strength-text,
  .floating-label,
  .input-icon,
  .brand-header {
    transition: none !important;
  }

  .submit-btn:hover:not(:disabled) {
    transform: none !important;
  }
}

/* ====== ACCESSIBILITY KEYBOARD OUTLINES ====== */
.form-input:focus-visible,
.submit-btn:focus-visible,
.tab-btn:focus-visible,
.eye-btn:focus-visible {
  outline: 2px solid #00f0ff;
  outline-offset: 3px;
}
</style>
