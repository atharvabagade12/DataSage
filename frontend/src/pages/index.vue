<template>
    <div class="landing-container">
      <!-- Navigation Header -->
      <header class="navbar" :class="{ 'scrolled': isScrolled }">
        <nav class="nav-content">
          <div class="nav-brand" @click="scrollToTop">
            <div class="brand-logo">
              <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" class="logo-svg">
                <defs>
                  <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                  </linearGradient>
                  <linearGradient id="logoAccent" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
                  </linearGradient>
                </defs>
                <!-- Neural network nodes -->
                <circle cx="20" cy="25" r="3" fill="url(#logoGradient)" opacity="0.9"/>
                <circle cx="20" cy="40" r="3" fill="url(#logoGradient)" opacity="0.9"/>
                <circle cx="20" cy="55" r="3" fill="url(#logoGradient)" opacity="0.9"/>
                
                <!-- Hidden layer -->
                <circle cx="40" cy="20" r="4" fill="url(#logoGradient)"/>
                <circle cx="40" cy="35" r="4" fill="url(#logoGradient)"/>
                <circle cx="40" cy="50" r="4" fill="url(#logoGradient)"/>
                <circle cx="40" cy="65" r="4" fill="url(#logoGradient)"/>
                
                <!-- Output layer -->
                <circle cx="60" cy="30" r="4.5" fill="url(#logoAccent)"/>
                <circle cx="60" cy="50" r="4.5" fill="url(#logoAccent)"/>
                
                <!-- Connections -->
                <line x1="23" y1="25" x2="36" y2="20" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.6"/>
                <line x1="23" y1="25" x2="36" y2="35" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.4"/>
                <line x1="23" y1="40" x2="36" y2="35" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.6"/>
                <line x1="23" y1="40" x2="36" y2="50" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.6"/>
                <line x1="23" y1="55" x2="36" y2="50" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.6"/>
                <line x1="23" y1="55" x2="36" y2="65" stroke="url(#logoGradient)" stroke-width="1.5" opacity="0.4"/>
                
                <line x1="44" y1="20" x2="56" y2="30" stroke="url(#logoAccent)" stroke-width="2" opacity="0.7"/>
                <line x1="44" y1="35" x2="56" y2="30" stroke="url(#logoAccent)" stroke-width="2" opacity="0.5"/>
                <line x1="44" y1="35" x2="56" y2="50" stroke="url(#logoAccent)" stroke-width="2" opacity="0.7"/>
                <line x1="44" y1="50" x2="56" y2="50" stroke="url(#logoAccent)" stroke-width="2" opacity="0.8"/>
                <line x1="44" y1="65" x2="56" y2="50" stroke="url(#logoAccent)" stroke-width="2" opacity="0.5"/>
              </svg>
            </div>
            <h1 class="brand-title">DataSage</h1>
          </div>
  
          <div class="nav-links">
            <a class="nav-link" @click="scrollTo('features')">Features</a>
            <a class="nav-link" @click="scrollTo('how-it-works')">How It Works</a>
            <a class="nav-link" @click="scrollTo('demo')">Demo</a>
            <a class="nav-link" @click="scrollTo('about')">About</a>
          </div>
  
          <div class="nav-actions">
            <button @click="goToLogin" class="nav-btn secondary">Sign In</button>
            <button @click="goToSignup" class="nav-btn primary">Get Started</button>
          </div>
  
          <button @click="toggleMobileMenu" class="mobile-menu-btn">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </nav>
      </header>
  
      <!-- Hero Section -->
      <section class="hero-section" id="home">
        <div class="hero-background">
          <div class="gradient-orb orb-1"></div>
          <div class="gradient-orb orb-2"></div>
          <div class="gradient-orb orb-3"></div>
        </div>
  
        <div class="hero-content-wrapper">
          <div class="hero-content">
            
  
            <h1 class="hero-title">
              Transform Your Data Into
              <span class="gradient-text">Intelligent Insights</span>
            </h1>
  
            <p class="hero-subtitle">
              Complete machine learning platform designed for students, researchers, and data enthusiasts. 
              Build powerful ML models without coding - perfect for learning and real projects.
            </p>
  
            <div class="hero-actions">
              <button @click="goToSignup" class="cta-button primary">
                <span>🚀</span>
                <span>Get Started Free</span>
              </button>
              <button @click="watchDemo" class="cta-button secondary">
                <span>🎬</span>
                <span>Watch Demo</span>
              </button>
            </div>
  
            <div class="trust-indicators">
              <div class="trust-badge">
                <span>✅</span>
                <span>100% Free</span>
              </div>
              <div class="trust-badge">
                <span>🎓</span>
                <span>Student-Built</span>
              </div>
              <div class="trust-badge">
                <span>⚡</span>
                <span>No Coding</span>
              </div>
              <div class="trust-badge">
                <span>🔓</span>
                <span>Open Source</span>
              </div>
            </div>
          </div>
  
          <div class="hero-visual">
            <div class="dashboard-preview">
              <div class="preview-window">
                <div class="window-header">
                  <div class="window-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <div class="window-title">DataSage Dashboard</div>
                </div>
                <div class="window-content">
                  <div class="demo-upload">
                    <div class="upload-icon">📊</div>
                    <div class="upload-text">Drop your dataset here</div>
                  </div>
                  <div class="demo-charts">
                    <div class="chart-item">
                      <div class="chart-bar" style="height: 60%"></div>
                    </div>
                    <div class="chart-item">
                      <div class="chart-bar" style="height: 80%"></div>
                    </div>
                    <div class="chart-item">
                      <div class="chart-bar" style="height: 45%"></div>
                    </div>
                    <div class="chart-item">
                      <div class="chart-bar" style="height: 75%"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features-section" id="features">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Everything You Need for Machine Learning</h2>
            <p class="section-subtitle">
              From data upload to model deployment - DataSage provides a complete ML pipeline 
              that's perfect for learning and real-world applications.
            </p>
          </div>
  
          <div class="features-grid">
            <div class="feature-card" v-for="feature in features" :key="feature.id">
              <div class="feature-icon">
                <span>{{ feature.icon }}</span>
              </div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
              <div class="feature-highlights">
                <div class="highlight" v-for="highlight in feature.highlights" :key="highlight">
                  <span class="highlight-icon">✓</span>
                  <span class="highlight-text">{{ highlight }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- How It Works Section -->
      <section class="how-it-works-section" id="how-it-works">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">How DataSage Works</h2>
            <p class="section-subtitle">
              Four simple steps to turn your raw data into actionable insights
            </p>
          </div>
  
          <div class="steps-container">
            <div class="step-item" v-for="(step, index) in steps" :key="step.id">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-icon">{{ step.icon }}</div>
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Platform Demo Section -->
      <section class="demo-section" id="demo">
        <div class="section-container">
          <div class="demo-content">
            <div class="demo-info">
              <h2 class="demo-title">See DataSage in Action</h2>
              <p class="demo-subtitle">
                Watch how easy it is to build machine learning models with DataSage's 
                intuitive interface and powerful automation.
              </p>
              
              <div class="demo-features">
                <div class="demo-feature">
                  <span class="demo-feature-icon">⚡</span>
                  <span class="demo-feature-text">Instant data processing</span>
                </div>
                <div class="demo-feature">
                  <span class="demo-feature-icon">🤖</span>
                  <span class="demo-feature-text">Automated model training</span>
                </div>
                <div class="demo-feature">
                  <span class="demo-feature-icon">📊</span>
                  <span class="demo-feature-text">Interactive visualizations</span>
                </div>
                <div class="demo-feature">
                  <span class="demo-feature-icon">📈</span>
                  <span class="demo-feature-text">Real-time insights</span>
                </div>
              </div>
  
              <button @click="goToSignup" class="demo-cta">
                <span>🚀</span>
                <span>Try It Yourself</span>
              </button>
            </div>
  
            <div class="demo-visual">
              <div class="demo-window">
                <div class="demo-header">
                  <div class="demo-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <div class="demo-title-bar">DataSage Platform</div>
                </div>
                
                <div class="demo-screen">
                  <div class="demo-step" :class="{ active: currentDemoStep === 0 }">
                    <div class="upload-simulation">
                      <div style="font-size: 2rem; margin-bottom: 1rem;">📁</div>
                      <div>Upload Complete</div>
                    </div>
                  </div>
                  
                  <div class="demo-step" :class="{ active: currentDemoStep === 1 }">
                    <div class="processing-simulation">
                      <div class="processing-bar">
                        <div class="progress" :style="{ width: processingProgress + '%' }"></div>
                      </div>
                      <div class="processing-text">Processing Data...</div>
                    </div>
                  </div>
                  
                  <div class="demo-step" :class="{ active: currentDemoStep === 2 }">
                    <div class="results-simulation">
                      <div class="chart-bars">
                        <div class="bar" style="height: 70px;"></div>
                        <div class="bar" style="height: 90px;"></div>
                        <div class="bar" style="height: 60px;"></div>
                      </div>
                      <div class="accuracy-display">
                        <div class="accuracy-label">Model Accuracy</div>
                        <div class="accuracy-value">{{ modelAccuracy.toFixed(1) }}%</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Academic Project Section -->
      <section class="academic-section" id="about">
        <div class="section-container">
          <div class="academic-content">
            <div class="academic-badge">
              <span>🎓</span>
              <span>Academic Excellence</span>
            </div>
            
            <h2 class="academic-title">Built as a Final Year Project</h2>
            <p class="academic-subtitle">
              DataSage represents the culmination of computer science education, 
              combining theoretical knowledge with practical application to create 
              a real-world machine learning platform.
            </p>
  
            <div class="academic-stats">
              <div class="stat-item">
                <div class="stat-number">2025</div>
                <div class="stat-label">Final Year Project</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">Student Built</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">Open</div>
                <div class="stat-label">Source Code</div>
              </div>
            </div>
  
            <div class="tech-stack">
              <div class="tech-item" v-for="tech in techStack" :key="tech.name">
                <div class="tech-icon">{{ tech.icon }}</div>
                <div class="tech-name">{{ tech.name }}</div>
                <div class="tech-desc">{{ tech.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Final CTA Section -->
      <section class="cta-section">
        <div class="section-container">
          <h2 class="cta-title">Ready to Start Your ML Journey?</h2>
          <p class="cta-subtitle">
            Join DataSage today and transform your data into powerful insights. 
            Perfect for students, researchers, and data enthusiasts.
          </p>
          
          <button @click="goToSignup" class="cta-button primary large">
            <span>🚀</span>
            <span>Get Started Free</span>
          </button>
  
          <div class="cta-assurance">
            <div class="assurance-item">
              <span>✅</span>
              <span>Free Forever</span>
            </div>
            <div class="assurance-item">
              <span>⚡</span>
              <span>No Setup Required</span>
            </div>
            <div class="assurance-item">
              <span>🎓</span>
              <span>Perfect for Learning</span>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="footer">
        <div class="footer-content">
          <div class="footer-section">
            <div class="footer-brand">
              <div class="footer-logo">
                <div class="brand-logo">
                  <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" class="logo-svg">
                    <defs>
                      <linearGradient id="footerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                      </linearGradient>
                      <linearGradient id="footerAccent" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
                      </linearGradient>
                    </defs>
                    <!-- Neural network representation -->
                    <circle cx="20" cy="30" r="2.5" fill="url(#footerGradient)" opacity="0.9"/>
                    <circle cx="20" cy="40" r="2.5" fill="url(#footerGradient)" opacity="0.9"/>
                    <circle cx="20" cy="50" r="2.5" fill="url(#footerGradient)" opacity="0.9"/>
                    
                    <circle cx="40" cy="25" r="3" fill="url(#footerGradient)"/>
                    <circle cx="40" cy="35" r="3" fill="url(#footerGradient)"/>
                    <circle cx="40" cy="45" r="3" fill="url(#footerGradient)"/>
                    <circle cx="40" cy="55" r="3" fill="url(#footerGradient)"/>
                    
                    <circle cx="60" cy="35" r="3.5" fill="url(#footerAccent)"/>
                    <circle cx="60" cy="45" r="3.5" fill="url(#footerAccent)"/>
                    
                    <!-- Simplified connections -->
                    <line x1="23" y1="35" x2="37" y2="30" stroke="url(#footerGradient)" stroke-width="1" opacity="0.6"/>
                    <line x1="23" y1="40" x2="37" y2="40" stroke="url(#footerGradient)" stroke-width="1" opacity="0.6"/>
                    <line x1="23" y1="45" x2="37" y2="50" stroke="url(#footerGradient)" stroke-width="1" opacity="0.6"/>
                    
                    <line x1="43" y1="30" x2="57" y2="35" stroke="url(#footerAccent)" stroke-width="1.5" opacity="0.7"/>
                    <line x1="43" y1="40" x2="57" y2="40" stroke="url(#footerAccent)" stroke-width="1.5" opacity="0.8"/>
                    <line x1="43" y1="50" x2="57" y2="45" stroke="url(#footerAccent)" stroke-width="1.5" opacity="0.7"/>
                  </svg>
                </div>
                <h3 class="footer-title">DataSage</h3>
              </div>
              <p class="footer-desc">
                Transform raw data into actionable intelligence with our 
                complete machine learning platform.
              </p>
            </div>
          </div>
  
          <div class="footer-section">
            <h4 class="footer-heading">Platform</h4>
            <div class="footer-links">
              <a @click="scrollTo('features')">Features</a>
              <a @click="scrollTo('how-it-works')">How It Works</a>
              <a @click="scrollTo('demo')">Demo</a>
              <a href="/login">Get Started</a>
            </div>
          </div>
  
          <div class="footer-section">
            <h4 class="footer-heading">Academic</h4>
            <div class="footer-links">
              <a @click="scrollTo('about')">About Project</a>
              <a href="#">Documentation</a>
              <a href="#">GitHub Repository</a>
              <a href="#">Research Paper</a>
            </div>
          </div>
  
          <div class="footer-section">
            <h4 class="footer-heading">Connect</h4>
            <div class="footer-links">
              <a href="mailto:contact@datasage.com">Contact</a>
              <a href="#">LinkedIn</a>
              <a href="#">GitHub</a>
              <a href="#">Support</a>
            </div>
          </div>
        </div>
  
        <div class="footer-bottom">
          <p>&copy; 2025 DataSage. Final Year Information Technology Project.</p>
        </div>
      </footer>
  
      <!-- Demo Modal -->
      <div v-if="showDemoModal" class="demo-modal" @click="closeDemoModal">
        <div class="demo-modal-content" @click.stop>
          <button @click="closeDemoModal" class="demo-modal-close">&times;</button>
          <h3 style="margin-bottom: 1rem; font-size: 1.5rem;">DataSage Platform Demo</h3>
          <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 0.5rem;">Interactive demo coming soon!</p>
            <p style="color: rgba(255,255,255,0.7);">For now, sign up to explore the full platform.</p>
          </div>
          <button @click="goToSignup" class="modal-cta">Try DataSage Now</button>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Page meta
useHead({
  title: 'DataSage - Machine Learning Platform for Students | Final Year Project 2025',
  meta: [
    { name: 'description', content: 'Complete machine learning platform built for students and researchers. Transform your data into insights with no coding required. Free forever, perfect for learning ML concepts.' },
    { name: 'keywords', content: 'machine learning, data science, student project, ML platform, no code ML, final year project, Vue.js, FastAPI' },
    { property: 'og:title', content: 'DataSage - ML Platform for Students' },
    { property: 'og:description', content: 'Free machine learning platform perfect for students and researchers. No coding required.' },
    { property: 'og:type', content: 'website' }
  ]
})

// Reactive state
const isScrolled = ref(false)
const showMobileMenu = ref(false)
const showDemoModal = ref(false)
const currentDemoStep = ref(0)
const processingProgress = ref(0)
const modelAccuracy = ref(94.2)

// Data
const features = ref([
  {
    id: 1,
    icon: '📊',
    title: 'Smart Data Processing',
    description: 'Upload CSV, Excel, or JSON files and let AI handle the cleaning, preprocessing, and feature engineering automatically.',
    highlights: ['Automatic data cleaning', 'Missing value handling', 'Feature scaling & encoding', 'Data quality reports']
  },
  {
    id: 2,
    icon: '🤖',
    title: 'Automated ML Pipeline',
    description: 'Train multiple algorithms simultaneously with hyperparameter tuning and cross-validation for optimal results.',
    highlights: ['Multiple algorithms', 'Auto hyperparameter tuning', 'Cross-validation', 'Model comparison']
  },
  {
    id: 3,
    icon: '📈',
    title: 'Interactive Visualizations',
    description: 'Create beautiful, interactive charts and dashboards to understand your data and model performance.',
    highlights: ['Dynamic charts', 'Custom dashboards', 'Real-time updates', 'Export capabilities']
  },
  {
    id: 4,
    icon: '☁️',
    title: 'Easy Model Deployment',
    description: 'Deploy your trained models with one click and integrate them into your applications via REST API.',
    highlights: ['One-click deployment', 'REST API endpoints', 'Model versioning', 'Performance monitoring']
  },
  {
    id: 5,
    icon: '🔍',
    title: 'Deep Analytics',
    description: 'Get detailed insights into your models with feature importance, prediction explanations, and performance metrics.',
    highlights: ['Feature importance', 'SHAP explanations', 'Performance metrics', 'Error analysis']
  },
  {
    id: 6,
    icon: '🎓',
    title: 'Learning Resources',
    description: 'Built-in tutorials, explanations, and best practices to help you understand ML concepts while building models.',
    highlights: ['Step-by-step tutorials', 'ML concept explanations', 'Best practices guide', 'Academic references']
  }
])

const steps = ref([
  {
    id: 1,
    icon: '📁',
    title: 'Upload Your Dataset',
    description: 'Drag and drop your CSV, Excel, or JSON file. DataSage automatically detects the structure and data types.'
  },
  {
    id: 2,
    icon: '⚙️',
    title: 'Automated Processing',
    description: 'AI handles data cleaning, preprocessing, feature engineering, and prepares your data for machine learning.'
  },
  {
    id: 3,
    icon: '🚀',
    title: 'Train ML Models',
    description: 'Multiple algorithms are trained simultaneously with automated hyperparameter tuning and cross-validation.'
  },
  {
    id: 4,
    icon: '📊',
    title: 'Get Insights',
    description: 'View interactive visualizations, model performance metrics, and deploy your best model with one click.'
  }
])

const techStack = ref([
  {
    icon: '⚡',
    name: 'Vue.js',
    desc: 'Frontend Framework'
  },
  {
    icon: '🚀',
    name: 'FastAPI',
    desc: 'Backend API'
  },
  {
    icon: '🤖',
    name: 'Scikit-Learn',
    desc: 'ML Library'
  },
  {
    icon: '📊',
    name: 'Chart.js',
    desc: 'Visualizations'
  }
])

// Methods
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollTo = (elementId) => {
  const element = document.getElementById(elementId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

// 🚀 FIXED NAVIGATION METHODS FOR NUXT 3
const goToLogin = async () => {
  try {
    await navigateTo('/login')
  } catch (error) {
    console.error('Navigation error:', error)
    // Fallback for client-side navigation
    if (process.client) {
      window.location.href = '/login'
    }
  }
}

const goToSignup = async () => {
  try {
    await navigateTo('/login#signup')
  } catch (error) {
    console.error('Navigation error:', error)
    // Fallback for client-side navigation
    if (process.client) {
      window.location.href = '/login#signup'
    }
  }
}

// 🎯 NEW: Navigate to Dashboard (Main Entry Point)
const goToDashboard = async () => {
  try {
    await navigateTo('/dashboard')
  } catch (error) {
    console.error('Navigation error:', error)
    // Fallback for client-side navigation
    if (process.client) {
      window.location.href = '/dashboard'
    }
  }
}

// 🚀 NEW: Start Free Trial (Direct to Dashboard)
const startFreeTrial = async () => {
  try {
    // Clear any existing session data
    if (process.client) {
      sessionStorage.clear()
      localStorage.clear()
    }
    
    // Navigate to dashboard to start fresh
    await navigateTo('/dashboard')
  } catch (error) {
    console.error('Navigation error:', error)
    if (process.client) {
      window.location.href = '/dashboard'
    }
  }
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const watchDemo = () => {
  showDemoModal.value = true
}

const closeDemoModal = () => {
  showDemoModal.value = false
  currentDemoStep.value = 0
  processingProgress.value = 0
  modelAccuracy.value = 94.2
}

const handleScroll = () => {
  if (process.client) {
    isScrolled.value = window.scrollY > 50
  }
}

// Demo animation
const startDemoAnimation = () => {
  if (!process.client) return null
  
  const interval = setInterval(() => {
    currentDemoStep.value = (currentDemoStep.value + 1) % 3
    
    if (currentDemoStep.value === 1) {
      processingProgress.value = 0
      const progressInterval = setInterval(() => {
        processingProgress.value += 2
        if (processingProgress.value >= 100) {
          clearInterval(progressInterval)
        }
      }, 30)
    }
    
    if (currentDemoStep.value === 2) {
      let currentAccuracy = 0
      const accuracyInterval = setInterval(() => {
        currentAccuracy += 1.5
        modelAccuracy.value = Math.min(currentAccuracy, 94.2)
        if (currentAccuracy >= 94.2) {
          clearInterval(accuracyInterval)
        }
      }, 30)
    }
  }, 4000)
  
  return interval
}

// ✨ NEW: Handle mobile menu clicks
const handleMobileMenuClick = async (action) => {
  showMobileMenu.value = false // Close mobile menu first
  
  switch (action) {
    case 'dashboard':
      await goToDashboard()
      break
    case 'login':
      await goToLogin()
      break
    case 'signup':
      await goToSignup()
      break
    case 'demo':
      watchDemo()
      break
    default:
      console.log('Unknown mobile menu action:', action)
  }
}

// ✨ NEW: Close mobile menu when clicking outside
const closeMobileMenuOnOutsideClick = (event) => {
  if (process.client && showMobileMenu.value) {
    const mobileMenu = document.getElementById('mobile-menu')
    const menuButton = document.getElementById('mobile-menu-button')
    
    if (mobileMenu && menuButton) {
      if (!mobileMenu.contains(event.target) && !menuButton.contains(event.target)) {
        showMobileMenu.value = false
      }
    }
  }
}

// Lifecycle
let demoInterval = null

onMounted(() => {
  if (process.client) {
    // Add scroll listener
    window.addEventListener('scroll', handleScroll)
    
    // Add click listener for mobile menu
    document.addEventListener('click', closeMobileMenuOnOutsideClick)
    
    // Start demo animation
    demoInterval = startDemoAnimation()
    
    console.log('🏠 Index page loaded successfully')
  }
})

onUnmounted(() => {
  if (process.client) {
    // Remove event listeners
    window.removeEventListener('scroll', handleScroll)
    document.removeEventListener('click', closeMobileMenuOnOutsideClick)
    
    // Clear demo interval
    if (demoInterval) {
      clearInterval(demoInterval)
    }
  }
})

// ✨ NEW: Expose methods for template usage
defineExpose({
  goToDashboard,
  startFreeTrial,
  goToLogin,
  goToSignup,
  watchDemo,
  closeDemoModal,
  toggleMobileMenu,
  handleMobileMenuClick,
  scrollTo,
  scrollToTop
})
</script>

  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .landing-container {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e);
    color: white;
    overflow-x: hidden;
    min-height: 100vh;
  }
  
  /* Navigation */
  .navbar {
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
    background: rgba(15, 15, 35, 0.9);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .navbar.scrolled {
    padding: 0.5rem 0;
    background: rgba(15, 15, 35, 0.95);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  }
  
  .nav-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
  }
  
  .nav-brand {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  
  .brand-logo {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  }
  
  .logo-svg {
    width: 28px;
    height: 28px;
  }
  
  .brand-title {
    margin-left: 1rem;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .nav-links {
    display: flex;
    gap: 2rem;
  }
  
  .nav-link {
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.3s ease;
  }
  
  .nav-link:hover {
    color: white;
  }
  
  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
  }
  
  .nav-link:hover::after {
    width: 100%;
  }
  
  .nav-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  
  .nav-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
  }
  
  .nav-btn.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  }
  
  .nav-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
  }
  
  .nav-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  .nav-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
  }
  
  .mobile-menu-btn {
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 8px;
  }
  
  .mobile-menu-btn span {
    width: 24px;
    height: 3px;
    background: white;
    border-radius: 2px;
    transition: all 0.3s ease;
  }
  
  /* Hero Section */
  .hero-section {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 8rem 2rem 4rem;
  }
  
  .hero-background {
    position: absolute;
    inset: 0;
    overflow: hidden;
    z-index: 0;
  }
  
  .gradient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    animation: float 6s ease-in-out infinite;
  }
  
  .orb-1 {
    width: 600px;
    height: 600px;
    background: linear-gradient(45deg, #667eea, #764ba2);
    top: -200px;
    left: -200px;
    opacity: 0.3;
  }
  
  .orb-2 {
    width: 500px;
    height: 500px;
    background: linear-gradient(45deg, #764ba2, #f093fb);
    bottom: -200px;
    right: -200px;
    opacity: 0.25;
    animation-delay: 2s;
  }
  
  .orb-3 {
    width: 400px;
    height: 400px;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.2;
    animation-delay: 4s;
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
  }
  
  .hero-content-wrapper {
    position: relative;
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    z-index: 1;
  }
  
  .hero-content {
    z-index: 1;
  }
  
  .academic-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    background: rgba(102, 126, 234, 0.15);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
  }
  
  .hero-title {
    font-size: 3.8rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 1.5rem;
  }
  
  .gradient-text {
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.7;
    margin-bottom: 2.5rem;
    max-width: 600px;
  }
  
  .hero-actions {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
  }
  
  .cta-button {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.25rem 2.5rem;
    border-radius: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    font-size: 1rem;
  }
  
  .cta-button.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  }
  
  .cta-button.primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
  }
  
  .cta-button.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
  }
  
  .cta-button.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }
  
  .cta-button.large {
    font-size: 1.2rem;
    padding: 1.5rem 3rem;
  }
  
  .trust-indicators {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .trust-badge {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(255, 255, 255, 0.08);
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
  }
  
  /* Hero Visual */
  .hero-visual {
    position: relative;
    z-index: 1;
  }
  
  .dashboard-preview {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .preview-window {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
  }
  
  .window-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .window-dots {
    display: flex;
    gap: 6px;
  }
  
  .window-dots span {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #ff5f56;
  }
  
  .window-dots span:nth-child(2) {
    background: #ffbd2e;
  }
  
  .window-dots span:nth-child(3) {
    background: #27ca3f;
  }
  
  .window-title {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
    font-weight: 500;
  }
  
  .window-content {
    padding: 2rem;
  }
  
  .demo-upload {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 2rem;
    border: 2px dashed rgba(102, 126, 234, 0.4);
    border-radius: 12px;
    background: linear-gradient(45deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
    margin-bottom: 2rem;
  }
  
  .upload-icon {
    font-size: 2.5rem;
    animation: bounce 2s infinite;
  }
  
  @keyframes bounce {
    0%, 20%, 53%, 80%, 100% {
      transform: translate3d(0, 0, 0);
    }
    40%, 43% {
      transform: translate3d(0, -8px, 0);
    }
    70% {
      transform: translate3d(0, -4px, 0);
    }
    90% {
      transform: translate3d(0, -2px, 0);
    }
  }
  
  .upload-text {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
  }
  
  .demo-charts {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
  }
  
  .chart-item {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 1rem 0.5rem;
    display: flex;
    align-items: flex-end;
    min-height: 80px;
  }
  
  .chart-bar {
    width: 100%;
    background: linear-gradient(to top, #667eea, #764ba2);
    border-radius: 4px;
    transition: all 0.8s ease;
  }
  
  /* Sections */
  .features-section,
  .how-it-works-section,
  .demo-section,
  .academic-section,
  .cta-section {
    padding: 6rem 2rem;
    position: relative;
  }
  
  .features-section {
    background: rgba(255, 255, 255, 0.02);
  }
  
  .demo-section {
    background: rgba(255, 255, 255, 0.02);
  }
  
  .cta-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    text-align: center;
  }
  
  .section-container {
    max-width: 1400px;
    margin: 0 auto;
  }
  
  .section-header {
    text-align: center;
    margin-bottom: 4rem;
  }
  
  .section-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .section-subtitle {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.8);
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }
  
  .feature-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    transition: all 0.4s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
  }
  
  .feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
    background: rgba(255, 255, 255, 0.08);
  }
  
  .feature-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    display: inline-block;
    padding: 1rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border-radius: 16px;
    border: 1px solid rgba(102, 126, 234, 0.3);
  }
  
  .feature-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }
  
  .feature-description {
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }
  
  .feature-highlights {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    text-align: left;
  }
  
  .highlight {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }
  
  .highlight-icon {
    color: #4ade80;
    font-weight: bold;
  }
  
  .highlight-text {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
  }
  
  .steps-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
  }
  
  .step-item {
    text-align: center;
    position: relative;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .step-number {
    position: absolute;
    top: -15px;
    right: -15px;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 700;
    color: white;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }
  
  .step-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
  }
  
  .step-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }
  
  .step-description {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }
  
  .demo-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
  }
  
  .demo-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .demo-subtitle {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 2rem;
    line-height: 1.6;
    font-size: 1.1rem;
  }
  
  .demo-features {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .demo-feature {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .demo-cta {
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .demo-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  }
  
  .demo-window {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .demo-header {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .demo-dots {
    display: flex;
    gap: 6px;
  }
  
  .demo-dots span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: white;
    opacity: 0.6;
  }
  
  .demo-title-bar {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
    margin-left: 1rem;
  }
  
  .demo-screen {
    padding: 2rem;
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .demo-step {
    width: 100%;
    opacity: 0;
    transition: all 0.5s ease;
  }
  
  .demo-step.active {
    opacity: 1;
  }
  
  .processing-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1rem;
  }
  
  .progress {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
  }
  
  .processing-text {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .chart-bars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .bar {
    background: linear-gradient(to top, #667eea, #764ba2);
    border-radius: 4px;
    transition: all 0.8s ease;
  }
  
  .accuracy-display {
    text-align: center;
  }
  
  .accuracy-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }
  
  .accuracy-value {
    font-size: 2rem;
    font-weight: 800;
    color: #4ade80;
  }
  
  .academic-content {
    text-align: center;
  }
  
  .academic-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .academic-subtitle {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 3rem;
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .academic-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
    margin-bottom: 4rem;
  }
  
  .stat-item {
    text-align: center;
  }
  
  .stat-number {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
  }
  
  .stat-label {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .tech-stack {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
  }
  
  .tech-item {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem 1rem;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
  }
  
  .tech-item:hover {
    transform: translateY(-4px);
    background: rgba(255, 255, 255, 0.08);
  }
  
  .tech-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .tech-name {
    font-weight: 700;
    margin-bottom: 0.5rem;
  }
  
  .tech-desc {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }
  
  .cta-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .cta-subtitle {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 3rem;
    font-size: 1.2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .cta-assurance {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .assurance-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .footer {
    background: rgba(15, 15, 35, 0.9);
    padding: 4rem 2rem 2rem;
  }
  
  .footer-content {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 3rem;
    max-width: 1400px;
    margin: 0 auto;
    margin-bottom: 2rem;
  }
  
  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .footer-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .footer-title {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .footer-desc {
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.6;
  }
  
  .footer-heading {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }
  
  .footer-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .footer-links a {
    color: rgba(255, 255, 255, 0.7);
    text-decoration: none;
    transition: color 0.3s ease;
    cursor: pointer;
  }
  
  .footer-links a:hover {
    color: #667eea;
  }
  
  .footer-bottom {
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 2rem;
    color: rgba(255, 255, 255, 0.6);
  }
  
  .demo-modal {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }
  
  .demo-modal-content {
    background: rgba(15, 15, 35, 0.95);
    border-radius: 16px;
    padding: 2rem;
    max-width: 500px;
    width: 90%;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .demo-modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s ease;
  }
  
  .demo-modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }
  
  .modal-cta {
    width: 100%;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .modal-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  }
  
  /* Responsive */
  @media (max-width: 1024px) {
    .hero-content-wrapper {
      grid-template-columns: 1fr;
      text-align: center;
    }
    
    .hero-title {
      font-size: 3rem;
    }
    
    .nav-links {
      display: none;
    }
    
    .mobile-menu-btn {
      display: flex;
    }
    
    .demo-content {
      grid-template-columns: 1fr;
      text-align: center;
    }
    
    .features-grid {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 768px) {
    .hero-title {
      font-size: 2.5rem;
    }
    
    .section-title {
      font-size: 2.5rem;
    }
    
    .cta-button {
      width: 100%;
      justify-content: center;
    }
    
    .hero-actions {
      flex-direction: column;
    }
    
    .trust-indicators {
      grid-template-columns: 1fr;
    }
    
    .academic-stats {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
    
    .footer-content {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
    
    .cta-assurance {
      flex-direction: column;
      gap: 1rem;
    }
  }
  </style>