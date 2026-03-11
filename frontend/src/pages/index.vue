<template>
    <div class="landing-container">
      <!-- Navigation Header -->
      <header class="navbar" :class="{ 'scrolled': isScrolled }">
        <nav class="nav-content">
          <div class="nav-brand" @click="scrollToTop">
            <div class="brand-logo">
              <img src="@/assets/logo.jpeg" alt="DataSage Logo" class="logo-img">
            </div>
            <h1 class="brand-title">DataSage</h1>
          </div>
  
          <div class="nav-links">
            <a class="nav-link" @click="scrollTo('features')">Features</a>
            <a class="nav-link" @click="scrollTo('how-it-works')">How It Works</a>
            <a class="nav-link" @click="scrollTo('about')">About</a>
            <a class="nav-link" @click="scrollTo('faq')">FAQ</a>
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
          <div class="hero-grid"></div>
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
            <div class="pipeline-preview">
              <div class="preview-window">
                <div class="window-header">
                  <div class="window-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <div class="window-title">DataSage — ML Pipeline</div>
                </div>
                <div class="window-content pipeline-flow">
                  <div class="pipeline-track">
                    <div 
                      class="pipeline-node" 
                      v-for="(node, idx) in pipelineNodes" 
                      :key="node.label"
                      :class="{ active: activePipelineStep >= idx }"
                    >
                      <div class="node-icon-wrapper">
                        <span class="node-icon">{{ node.icon }}</span>
                      </div>
                      <span class="node-label">{{ node.label }}</span>
                      <span class="node-desc">{{ node.desc }}</span>
                    </div>
                  </div>
                  <div class="pipeline-connector">
                    <div class="connector-line"></div>
                    <div class="connector-progress" :style="{ width: pipelineProgress + '%' }"></div>
                    <div class="connector-dot" :style="{ left: pipelineProgress + '%' }"></div>
                  </div>
                  <div class="pipeline-output">
                    <div class="output-badge">
                      <span class="output-pulse"></span>
                      <span>Ready to build your first model</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features-section reveal" id="features">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Everything You Need for Machine Learning</h2>
            <p class="section-subtitle">
              From data upload to model training - DataSage provides a complete ML pipeline 
              that's perfect for learning and real-world applications.
            </p>
          </div>
  
          <div class="features-grid">
            <div class="feature-card reveal" v-for="feature in features" :key="feature.id">
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
      <section class="how-it-works-section reveal" id="how-it-works">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">How DataSage Works</h2>
            <p class="section-subtitle">
              Four simple steps to turn your raw data into actionable insights
            </p>
          </div>
  
          <div class="steps-container">
            <div class="step-item reveal" v-for="(step, index) in steps" :key="step.id">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-icon">{{ step.icon }}</div>
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- About Section -->
      <section class="about-section reveal" id="about">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">About DataSage</h2>
            <p class="section-subtitle">
              A student-built open-source platform making machine learning accessible to everyone.
            </p>
          </div>

          <div class="about-content">
            <div class="about-card">
              <div class="about-icon">🎯</div>
              <h3>Our Mission</h3>
              <p>
                DataSage was created to bridge the gap between understanding ML theory and 
                applying it in practice. We believe everyone should be able to train, evaluate, 
                and compare machine learning models — without writing a single line of code.
              </p>
            </div>
            <div class="about-card">
              <div class="about-icon">🎓</div>
              <h3>Built by Students</h3>
              <p>
                Developed as a final-year academic project, DataSage is built with modern 
                technologies and real-world engineering practices. It's designed to grow with 
                the community's feedback and contributions.
              </p>
            </div>
            <div class="about-card">
              <div class="about-icon">🌍</div>
              <h3>Open &amp; Free</h3>
              <p>
                DataSage is 100% free and open source. No hidden fees, no premium tiers. 
                We're committed to keeping ML tools accessible for students, researchers, 
                and data enthusiasts everywhere.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ Section -->
      <section class="faq-section reveal" id="faq">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Frequently Asked Questions</h2>
            <p class="section-subtitle">
              Got questions? We've got answers.
            </p>
          </div>

          <div class="faq-list">
            <div 
              class="faq-item" 
              v-for="(item, index) in faqItems" 
              :key="index"
              :class="{ open: openFaqIndex === index }"
            >
              <button class="faq-question" @click="toggleFaq(index)">
                <span>{{ item.question }}</span>
                <span class="faq-chevron">▾</span>
              </button>
              <div class="faq-answer" v-show="openFaqIndex === index">
                <p>{{ item.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Final CTA Section -->
      <section class="cta-section reveal">
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
              <span>Free to Explore</span>
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
                <div class="brand-logo footer-brand-logo">
                  <img src="@/assets/logo.jpeg" alt="DataSage Logo" class="logo-img">
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
          <p>&copy; 2025–2026 DataSage. Built with ❤️ as a student project.</p>
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
const datasetsCount = ref(12450)
const activePipelineStep = ref(-1)
const pipelineProgress = ref(0)
const openFaqIndex = ref(null)

// Data
const features = ref([
  {
    id: 1,
    icon: '📊',
    title: 'Smart Data Processing',
    description: 'Upload CSV or Excel files and let DataSage automatically detect data types, identify missing values, and generate data quality reports.',
    highlights: ['Automatic type detection', 'Missing value handling', 'Feature scaling & encoding', 'Data quality overview']
  },
  {
    id: 2,
    icon: '🤖',
    title: 'Automated ML Pipeline',
    description: 'Train multiple classification and regression algorithms simultaneously with built-in hyperparameter tuning and cross-validation.',
    highlights: ['Random Forest, XGBoost, SVM & more', 'Hyperparameter tuning', 'Cross-validation support', 'Train-test splitting']
  },
  {
    id: 3,
    icon: '📈',
    title: 'Interactive Visualizations',
    description: 'Explore your data with dynamic distribution charts, correlation heatmaps, and feature analysis plots powered by Chart.js.',
    highlights: ['Distribution plots', 'Correlation heatmaps', 'Feature analysis charts', 'Model performance graphs']
  },
  {
    id: 4,
    icon: '⚙️',
    title: 'Advanced Preprocessing',
    description: 'Handle class imbalance with SMOTE, apply label & ordinal encoding, detect outliers, and scale features — all from an intuitive interface.',
    highlights: ['SMOTE oversampling', 'Label & ordinal encoding', 'Outlier detection', 'Standard & MinMax scaling']
  },
  {
    id: 5,
    icon: '🏆',
    title: 'Model Comparison',
    description: 'Compare trained models side-by-side with key performance metrics, confusion matrices, and classification reports.',
    highlights: ['Side-by-side metrics', 'Confusion matrices', 'Classification reports', 'Accuracy, Precision & Recall']
  },
  {
    id: 6,
    icon: '💾',
    title: 'Version Control',
    description: 'Save snapshots of your preprocessed dataset at any stage. Track changes, compare versions, and roll back when needed.',
    highlights: ['Save dataset versions', 'Preprocessing history', 'Version comparison', 'Rollback support']
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
    description: 'Our algorithms handle data cleaning, preprocessing, feature engineering, and prepare your data for machine learning.'
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

const pipelineNodes = ref([
  { icon: '📁', label: 'Upload', desc: 'CSV / Excel' },
  { icon: '⚙️', label: 'Process', desc: 'Clean & encode' },
  { icon: '🚀', label: 'Train', desc: 'ML algorithms' },
  { icon: '📊', label: 'Analyze', desc: 'Metrics & charts' }
])

const faqItems = ref([
  {
    question: 'Is DataSage completely free to use?',
    answer: 'Yes! DataSage is 100% free and open source. There are no hidden fees, premium tiers, or usage limits. It was built as a student project to make ML accessible to everyone.'
  },
  {
    question: 'Do I need coding or programming experience?',
    answer: 'Not at all. DataSage is designed as a no-code platform. You upload your data, configure options through an intuitive UI, and the platform handles all the code behind the scenes.'
  },
  {
    question: 'What file formats are supported for upload?',
    answer: 'Currently DataSage supports CSV and Excel (.xlsx) file formats. Simply drag and drop your file or use the upload button to get started.'
  },
  {
    question: 'Which machine learning algorithms are available?',
    answer: 'DataSage supports popular algorithms including Random Forest, XGBoost, Support Vector Machines (SVM), Logistic Regression, Decision Trees, K-Nearest Neighbors, and more — for both classification and regression tasks.'
  },
  {
    question: 'Can I use my own datasets?',
    answer: 'Absolutely. You can upload any structured dataset in CSV or Excel format. DataSage also provides sample datasets if you want to explore the platform first.'
  },
  {
    question: 'Is my data stored securely?',
    answer: 'Your data is stored locally on the server during your session. DataSage does not share your data with any third parties. As an open-source project, you can review the code to verify our data handling practices.'
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

const toggleFaq = (index) => {
  openFaqIndex.value = openFaqIndex.value === index ? null : index
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

// Stats counter animation
const startStatsAnimation = () => {
  if (!process.client) return null
  
  const interval = setInterval(() => {
    datasetsCount.value += Math.floor(Math.random() * 3) + 1
  }, 3000)
  
  return interval
}

// Pipeline hero animation
const startPipelineAnimation = () => {
  if (!process.client) return null

  const totalDuration = 4000 // full cycle in ms
  const steps = 4
  let elapsed = 0
  const tick = 50

  const interval = setInterval(() => {
    elapsed += tick
    const progress = (elapsed % totalDuration) / totalDuration
    pipelineProgress.value = Math.min(progress * 100, 100)
    activePipelineStep.value = Math.floor(progress * steps)

    if (elapsed % totalDuration === 0) {
      // brief pause at end then restart
      setTimeout(() => {
        activePipelineStep.value = -1
        pipelineProgress.value = 0
      }, 800)
    }
  }, tick)

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
let statsInterval = null
let pipelineInterval = null

onMounted(() => {
  if (process.client) {
    // Add scroll listener
    window.addEventListener('scroll', handleScroll)
    
    // Add click listener for mobile menu
    document.addEventListener('click', closeMobileMenuOnOutsideClick)
    
    // Start demo animation
    demoInterval = startDemoAnimation()
    
    // Start stats animation
    statsInterval = startStatsAnimation()
    
    // Start pipeline hero animation
    pipelineInterval = startPipelineAnimation()
    
    // Initialize reveal on scroll
    initScrollReveal()
    
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
    
    // Clear stats interval
    if (statsInterval) {
      clearInterval(statsInterval)
    }
    
    // Clear pipeline interval
    if (pipelineInterval) {
      clearInterval(pipelineInterval)
    }
  }
})

// Scroll Reveal Logic
function initScrollReveal() {
  if (!process.client) return

  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active')
        // Once revealed, we can stop observing this element
        observer.unobserve(entry.target)
      }
    })
  }, observerOptions)

  // Observe all elements with the 'reveal' class
  document.querySelectorAll('.reveal').forEach(el => {
    observer.observe(el)
  })
}

//Expose methods for template usage
defineExpose({
  goToDashboard,
  startFreeTrial,
  goToLogin,
  goToSignup,
  watchDemo,
  closeDemoModal,
  toggleMobileMenu,
  handleMobileMenuClick,
  toggleFaq,
  scrollTo,
  scrollToTop,
  initScrollReveal
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
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    overflow: hidden;
  }
  
  .logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .footer-brand-logo {
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
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
    background: radial-gradient(circle at 50% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 80%);
  }

  .hero-grid {
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(rgba(102, 126, 234, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(102, 126, 234, 0.05) 1px, transparent 1px);
    background-size: 50px 50px;
    mask-image: radial-gradient(circle at 50% 50%, black 30%, transparent 100%);
    opacity: 0.5;
    z-index: 0;
  }
  
  .gradient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    animation: float 10s ease-in-out infinite;
    z-index: 1;
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
    0%, 100% { transform: translate(0, 0); }
    33% { transform: translate(30px, -30px); }
    66% { transform: translate(-20px, 20px); }
  }

  /* Reveal Animations */
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    will-change: opacity, transform;
  }

  .reveal.active {
    opacity: 1;
    transform: translateY(0);
  }

  /* Staggered reveals for cards */
  .features-grid .reveal:nth-child(2) { transition-delay: 0.1s; }
  .features-grid .reveal:nth-child(3) { transition-delay: 0.2s; }
  .features-grid .reveal:nth-child(4) { transition-delay: 0.3s; }
  .features-grid .reveal:nth-child(5) { transition-delay: 0.4s; }
  .features-grid .reveal:nth-child(6) { transition-delay: 0.5s; }

  .steps-container .reveal:nth-child(2) { transition-delay: 0.15s; }
  .steps-container .reveal:nth-child(3) { transition-delay: 0.3s; }
  .steps-container .reveal:nth-child(4) { transition-delay: 0.45s; }
  
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
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
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
  
  .live-stats {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 12px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    margin-top: 2rem;
  }
  
  .stat-ticker {
    display: flex;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 500;
  }
  
  .ticker-label {
    color: rgba(255, 255, 255, 0.6);
  }
  
  .ticker-value {
    color: #4facfe;
    font-family: var(--font-mono);
  }
  
  .stat-pulse {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 10px #4ade80;
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
  }
  
  /* Hero Visual — Pipeline Flow */
  .hero-visual {
    position: relative;
    z-index: 1;
  }

  .pipeline-preview {
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

  .pipeline-flow {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .pipeline-track {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
  }

  .pipeline-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    text-align: center;
    opacity: 0.4;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    transform: scale(0.95);
  }

  .pipeline-node.active {
    opacity: 1;
    transform: scale(1);
  }

  .node-icon-wrapper {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.25);
    transition: all 0.5s ease;
  }

  .pipeline-node.active .node-icon-wrapper {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.25), rgba(118, 75, 162, 0.25));
    border-color: rgba(102, 126, 234, 0.5);
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  }

  .node-icon {
    font-size: 1.5rem;
  }

  .node-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
  }

  .node-desc {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.5);
  }

  .pipeline-connector {
    position: relative;
    height: 6px;
    margin: 0 2rem;
  }

  .connector-line {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  .connector-progress {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 3px;
    transition: width 0.1s linear;
  }

  .connector-dot {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 14px;
    height: 14px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(102, 126, 234, 0.8), 0 0 24px rgba(102, 126, 234, 0.4);
    transition: left 0.1s linear;
  }

  .pipeline-output {
    display: flex;
    justify-content: center;
  }

  .output-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 1.25rem;
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 20px;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.8);
  }

  .output-pulse {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
    animation: pulse 2s infinite;
  }
  
  /* Sections */
  .features-section,
  .how-it-works-section,
  .about-section,
  .faq-section,
  .cta-section {
    padding: 6rem 2rem;
    position: relative;
  }
  
  .features-section {
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
    position: relative;
    overflow: hidden;
  }

  .feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    opacity: 0;
    transition: opacity 0.4s ease;
  }

  .feature-card:hover::before {
    opacity: 1;
  }
  
  .feature-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.4);
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
    transition: all 0.3s ease;
  }
  
  .step-item:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(102, 126, 234, 0.3);
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

  
  .academic-content {
    text-align: center;
    padding: 4rem;
    background: radial-gradient(circle at center, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
    border-radius: 30px;
    border: 1px solid rgba(102, 126, 234, 0.1);
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
    gap: 1rem;
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

  /* About Section */
  .about-section {
    background: rgba(255, 255, 255, 0.02);
  }

  .about-content {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }

  .about-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
  }

  .about-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.3);
  }

  .about-icon {
    font-size: 2.5rem;
    margin-bottom: 1.25rem;
  }

  .about-card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .about-card p {
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.7;
    font-size: 0.95rem;
  }

  /* FAQ Section */
  .faq-section {
    background: linear-gradient(180deg, transparent, rgba(102, 126, 234, 0.03));
  }

  .faq-list {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .faq-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .faq-item:hover {
    border-color: rgba(102, 126, 234, 0.3);
  }

  .faq-item.open {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.4);
  }

  .faq-question {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    background: none;
    border: none;
    color: white;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    text-align: left;
    font-family: inherit;
    transition: color 0.3s ease;
  }

  .faq-question:hover {
    color: #a5b4fc;
  }

  .faq-chevron {
    font-size: 1.2rem;
    transition: transform 0.3s ease;
    color: rgba(255, 255, 255, 0.5);
  }

  .faq-item.open .faq-chevron {
    transform: rotate(180deg);
    color: #667eea;
  }

  .faq-answer {
    padding: 0 1.5rem 1.25rem;
  }

  .faq-answer p {
    color: rgba(255, 255, 255, 0.75);
    line-height: 1.7;
    font-size: 0.95rem;
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
    
    .features-grid {
      grid-template-columns: 1fr;
    }

    .about-content {
      grid-template-columns: 1fr;
    }

    .pipeline-track {
      grid-template-columns: repeat(2, 1fr);
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
    
    .footer-content {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
    
    .cta-assurance {
      flex-direction: column;
      gap: 1rem;
    }

    .pipeline-track {
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
    }

    .connector-line,
    .connector-progress,
    .connector-dot {
      display: none;
    }

    .faq-question {
      font-size: 0.95rem;
      padding: 1rem 1.25rem;
    }
  }
  </style>