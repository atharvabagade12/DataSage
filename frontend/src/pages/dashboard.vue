<template>
  <div class="dashboard">
    <!-- Top Navigation -->
    <nav class="dashboard-header">
      <div class="nav-left">
        <div class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="12" fill="url(#gradient)" opacity="0.8"/>
              <circle cx="16" cy="16" r="6" fill="white" opacity="0.9"/>
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#667eea"/>
                  <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="brand-text">DataSage</div>
        </div>
      </div>
      
      <div class="nav-center">
        <div class="nav-links">
          <a href="#" class="nav-link active">Dashboard</a>
          <a href="#" class="nav-link">Projects</a>
          <a href="#" class="nav-link">Analytics</a>
          <a href="#" class="nav-link">Models</a>
        </div>
      </div>
      
      <div class="nav-right">
        <div class="user-section">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            
          </div>
          <button @click="logout" class="logout-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.59L17 17l5-5-5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
            </svg>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <div class="welcome-section">
        <h1>Welcome back, {{ userName }}!</h1>
        <p>Ready to build some amazing ML models? Let's get started.</p>
      </div>

      <!-- Summary Cards Grid -->
      <div class="cards-grid">
        <!-- My Projects Card -->
        <div class="dashboard-card projects-card">
          <div class="card-header">
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2h-8l-2-2z"/>
              </svg>
            </div>
            <h3>My Projects</h3>
          </div>
          <div class="card-body">
            <div class="metric-value">{{ stats.projects }}</div>
            <div class="metric-label">Active Projects</div>
            <button @click="createNewProject" class="primary-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
              </svg>
              New Project
            </button>
          </div>
        </div>

        <!-- Recent Datasets Card -->
        <div class="dashboard-card datasets-card">
          <div class="card-header">
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <h3>Recent Datasets</h3>
          </div>
          <div class="card-body">
            <div v-if="recentDataset" class="dataset-info">
              <div class="dataset-name">{{ recentDataset.name }}</div>
              <div class="dataset-meta">
                {{ recentDataset.rows.toLocaleString() }} rows • {{ recentDataset.columns }} cols
              </div>
              <div class="dataset-date">{{ formatDate(recentDataset.uploadedAt) }}</div>
            </div>
            <div v-else class="no-data">
              <div class="empty-state">No datasets uploaded yet</div>
              <button @click="scrollToUpload" class="secondary-btn">Upload Below</button>
            </div>
          </div>
        </div>

        <!-- Data Health Card -->
        <div class="dashboard-card health-card">
          <div class="card-header">
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M7.07,18.28C7.5,17.38 8.12,16.5 8.91,15.77C9.71,15.04 10.69,14.5 11.71,14.21C9.04,13.3 7,10.79 7,8A5,5 0 0,1 12,3A5,5 0 0,1 17,8C17,10.79 14.96,13.3 12.29,14.21C13.31,14.5 14.29,15.04 15.09,15.77C15.88,16.5 16.5,17.38 16.93,18.28C15.39,19.36 13.72,20 12,20C10.28,20 8.61,19.36 7.07,18.28Z"/>
              </svg>
            </div>
            <h3>Data Health</h3>
          </div>
          <div class="card-body">
            <div class="health-gauge">
              <svg class="gauge" viewBox="0 0 100 100">
                <circle class="gauge-bg" cx="50" cy="50" r="40" fill="none" stroke-width="8"/>
                <circle 
                  class="gauge-fill" 
                  cx="50" 
                  cy="50" 
                  r="40" 
                  fill="none" 
                  stroke-width="8"
                  :stroke-dasharray="251"
                  :stroke-dashoffset="251 - (dataHealth / 100) * 251"
                  transform="rotate(-90 50 50)"
                />
                <text x="50" y="50" class="gauge-text" text-anchor="middle" dominant-baseline="middle">
                  {{ dataHealth }}%
                </text>
              </svg>
            </div>
            <div class="health-label">Overall Quality</div>
          </div>
        </div>

        <!-- Models Trained Card -->
        <div class="dashboard-card models-card">
          <div class="card-header">
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9,5A4,4 0 0,1 13,9A4,4 0 0,1 9,13A4,4 0 0,1 5,9A4,4 0 0,1 9,5M9,15C11.67,15 17,16.34 17,19V21H1V19C1,16.34 6.33,15 9,15M16.76,5.36C18.78,7.56 18.78,10.61 16.76,12.63L15.08,10.94C15.92,9.76 15.92,8.23 15.08,7.05L16.76,5.36M20.07,2C24,6.05 23.97,12.11 20.07,16.07L18.44,14.44C21.21,11.19 21.21,6.65 18.44,3.63L20.07,2Z"/>
              </svg>
            </div>
            <h3>Models Trained</h3>
          </div>
          <div class="card-body">
            <div class="metric-value">{{ stats.models }}</div>
            <div class="metric-label">Total Models</div>
            <div class="sparkline">
              <svg width="100%" height="30" viewBox="0 0 100 30">
                <polyline 
                  :points="sparklinePoints" 
                  fill="none" 
                  stroke="url(#sparklineGradient)" 
                  stroke-width="2"
                />
                <defs>
                  <linearGradient id="sparklineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <button @click="trainModel" class="secondary-btn">Train New Model</button>
          </div>
        </div>
      </div>

      <!-- Quick Actions Section -->
      <div class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="actions-grid">
          <button @click="scrollToUpload" class="action-card">
            <div class="action-icon upload">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <h3>Upload Dataset</h3>
            <p>Start your ML journey by uploading your data</p>
          </button>

          <button @click="useSampleData" class="action-card">
            <div class="action-icon sample">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M19,19H5V5H19V19Z"/>
              </svg>
            </div>
            <h3>Sample Datasets</h3>
            <p>Try DataSage with pre-loaded sample data</p>
          </button>

          <button @click="viewTutorials" class="action-card">
            <div class="action-icon tutorial">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19,3A2,2 0 0,1 21,5V19A2,2 0 0,1 19,21H5A2,2 0 0,1 3,19V5A2,2 0 0,1 5,3H19M12,17L17,12L15.59,10.59L12,14.17L8.41,10.59L7,12L12,17Z"/>
              </svg>
            </div>
            <h3>Learn DataSage</h3>
            <p>Master ML workflows with guided tutorials</p>
          </button>
        </div>
      </div>

      <!-- Inline Upload Section -->
      <div ref="uploadSection" class="upload-section">
        <h2>Ready to Start? Upload Your Dataset</h2>
        <p class="upload-subtitle">Drop your file below and we'll automatically take you to the data preview</p>
        
        <div 
          class="inline-uploader"
          :class="{ 
            'drag-over': dragOver, 
            'uploading': isUploading,
            'success': uploadSuccess
          }"
          @dragover.prevent="dragOver = true"
          @dragleave="dragOver = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <input 
            ref="fileInput" 
            type="file" 
            accept=".csv,.xlsx,.xls,.json" 
            @change="handleFileSelect" 
            style="display: none;"
          />

          <!-- Initial State -->
          <div v-if="!isUploading && !uploadSuccess" class="upload-initial">
            <div class="upload-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <h3>Drop your dataset here</h3>
            <p>Or click to browse your files</p>
            <div class="supported-formats">
              <span class="format-badge">CSV</span>
              <span class="format-badge">Excel</span>
              <span class="format-badge">JSON</span>
            </div>
          </div>

          <!-- Uploading State -->
          <div v-if="isUploading" class="upload-processing">
            <div class="processing-spinner">
              <svg viewBox="0 0 50 50">
                <circle 
                  cx="25" 
                  cy="25" 
                  r="20" 
                  fill="none" 
                  stroke="#667eea" 
                  stroke-width="4" 
                  stroke-linecap="round"
                  stroke-dasharray="31.416" 
                  stroke-dashoffset="31.416"
                >
                  <animate 
                    attributeName="stroke-array" 
                    dur="2s" 
                    values="0 31.416;15.708 15.708;0 31.416;15.708 15.708;0 31.416"
                    repeatCount="indefinite"
                  />
                  <animate 
                    attributeName="stroke-dashoffset" 
                    dur="2s" 
                    values="0;-15.708;-31.416;-47.124;-62.832" 
                    repeatCount="indefinite"
                  />
                  <animateTransform 
                    attributeName="transform" 
                    type="rotate"
                    dur="2s" 
                    values="0 25 25;360 25 25" 
                    repeatCount="indefinite"
                  />
                </circle>
              </svg>
            </div>
            <h3>{{ uploadProgress }}% uploading...</h3>
            <p>{{ uploadMessage }}</p>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${uploadProgress}%` }"></div>
            </div>
          </div>

          <!-- Success State -->
          <div v-if="uploadSuccess" class="upload-success">
            <div class="success-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
              </svg>
            </div>
            <h3>Upload successful!</h3>
            <p>{{ uploadedFile.name }} • {{ uploadedFile.rows.toLocaleString() }} rows</p>
            <button @click="goToPreview" class="continue-btn">
              <span>Continue to Preview</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useMLDataFlowStore } from '../stores/mlDataFlow'
import { useExperimentStore } from '../stores/experiment'

const backendConnected = ref(false)
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()

// Page Meta
useHead({
  title: 'DataSage Dashboard - AI-Powered ML Platform',
  meta: [
    { name: 'description', content: 'Your personal machine learning dashboard for building AI models without coding' }
  ]
})

// Refs
const fileInput = ref(null)
const uploadSection = ref(null)

// User Data
const userName = computed(() => {
  try {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}')
    return user.username || user.name || 'Data Scientist'
  } catch {
    return 'Data Scientist'
  }
})

const userInitials = computed(() => {
  try {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}')
    // Use username instead of name for initials
    const displayName = user.username || user.name || 'Data Scientist'
    return displayName.split(' ').map(n => n[0]).join('').toUpperCase() || 'DS'
  } catch {
    return 'DS'
  }
})



// Dashboard Stats
const stats = reactive({
  projects: 3,
  models: 8,
  datasets: 5
})

const dataHealth = ref(87)

// Recent Dataset
const recentDataset = ref({
  name: 'customer_analytics.csv',
  rows: 15420,
  columns: 18,
  uploadedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) // 2 days ago
})

// Upload State
const dragOver = ref(false)
const isUploading = ref(false)
const uploadSuccess = ref(false)
const uploadProgress = ref(0)
const uploadMessage = ref('')
const uploadedFile = ref(null)

// Sparkline Data for Models Chart
const sparklinePoints = computed(() => {
  const data = [2, 3, 1, 4, 3, 6, 4, 8, 5, 8] // Sample trend data
  const width = 100
  const height = 30
  const maxVal = Math.max(...data)
  const points = data.map((val, i) => {
    const x = (i / (data.length - 1)) * width
    const y = height - (val / maxVal) * height
    return `${x},${y}`
  }).join(' ')
  return points
})

// Methods
const createNewProject = () => {
  navigateTo('/ml-pipeline')
}

const useSampleData = () => {
  navigateTo('/ml-pipeline?sample=true')
}

const viewTutorials = () => {
  console.log('Navigate to tutorials')
}

const trainModel = () => {
  navigateTo('/ml-pipeline')
}

const logout = () => {
  sessionStorage.clear()
  navigateTo('/login')
}

const formatDate = (date) => {
  return new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
    Math.ceil((date - new Date()) / (1000 * 60 * 60 * 24)), 
    'day'
  )
}

// Upload Methods
const scrollToUpload = () => {
  uploadSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const triggerFileInput = () => {
  if (!isUploading.value && !uploadSuccess.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (e) => {
  const file = e.target.files?.[0]
  if (file) processFile(file)
}

const handleDrop = (e) => {
  dragOver.value = false
  const file = e.dataTransfer.files?.[0]
  if (file) processFile(file)
}

const checkBackendConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/health')
    backendConnected.value = response.ok
    if (backendConnected.value) {
      console.log('✅ Backend connected and ready')
    }
  } catch (error) {
    backendConnected.value = false
    console.warn('⚠️ Backend not available - uploads will not work')
  }
}

const processFile = async (file) => {
  console.log('🚀 Processing file with DIRECT-TO-BACKEND approach:', file.name)
  
  // File validation
  const allowedTypes = ['text/csv', 'application/json', 'text/plain']
  const maxSize = 1024 * 1024 * 1024 // 1GB for large datasets

  if (!allowedTypes.some(type => file.type === type) && 
      !file.name.toLowerCase().endsWith('.csv') && 
      !file.name.toLowerCase().endsWith('.json')) {
    alert('Please upload a CSV or JSON file')
    return
  }

  if (file.size > maxSize) {
    alert(`File size must be less than ${Math.round(maxSize / (1024 * 1024))}MB`)
    return
  }
  
  isUploading.value = true
  uploadSuccess.value = false
  uploadProgress.value = 0
  
  try {
    uploadMessage.value = 'Uploading directly to ML backend...'
    
    const formData = new FormData()
    formData.append('file', file)
    
    // ✅ USE THE WORKING ENDPOINT FOR NOW
    const fileSizeMB = file.size / (1024 * 1024)
    const endpoint = 'http://localhost:8000/api/upload-dataset' // Always use regular endpoint
    
    console.log(`📤 Uploading ${file.name} (${fileSizeMB.toFixed(1)}MB) to ${endpoint}`)
    
    // Progress simulation
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 5
        uploadMessage.value = `Uploading... ${uploadProgress.value}%`
      }
    }, 200)
    
    // Upload to backend with better error handling
    // Get JWT token from sessionStorage or localStorage
    const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken')
    
    console.log('🔑 Auth token found:', token ? 'Yes' : 'No')
    
    const headers = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: headers,
      body: formData
    })
    
    clearInterval(progressInterval)
    
    if (!response.ok) {
      // Get detailed error message
      let errorDetail = `HTTP ${response.status}`
      try {
        const errorData = await response.json()
        errorDetail = errorData.detail || errorDetail
      } catch {
        const errorText = await response.text()
        errorDetail = errorText || errorDetail
      }
      throw new Error(`Upload failed: ${errorDetail}`)
    }
    
    const result = await response.json()
    console.log('✅ File uploaded successfully:', result.dataset_id)
    
    uploadProgress.value = 100
    uploadMessage.value = 'Upload complete!'
    
    // ✅ SAFE DATA EXTRACTION WITH FALLBACKS
    const lightweightData = {
      backendDatasetId: result.dataset_id,
      datasetId: result.dataset_id,
      fileName: result.filename || file.name,
      fileSize: file.size,
      totalRows: result.total_rows || result.shape?.[0] || 0,
      totalColumns: result.total_columns || result.shape?.[1] || 0,
      columns: result.columns || [],
      isLargeDataset: result.is_large_dataset || false,
      backendAvailable: true,
      uploadedAt: new Date().toISOString(),
      processingSteps: [] // Initialize empty steps array
    }
    
    // Store metadata
    localStorage.setItem('processedData', JSON.stringify(lightweightData))
    localStorage.setItem('backendDatasetId', result.dataset_id)
    localStorage.removeItem('uploadedData') // Clean up old data

    // ✅ UPDATE STORES TO PREVENT STALE DATA
    mlStore.setCurrentDataset(
      result.dataset_id, 
      [], // No data yet, will be fetched
      result.filename || file.name,
      result.columns || []
    );
    experimentStore.setDataset(
        result.dataset_id,
        result.filename || file.name,
        { rows: result.total_rows, columns: result.total_columns }
    );
    
    // Update UI
    uploadedFile.value = {
      name: result.filename || file.name,
      rows: result.total_rows || result.shape?.[0] || 0,
      columns: result.total_columns || result.shape?.[1] || 0,
      size: file.size,
      backendDatasetId: result.dataset_id
    }
    
    isUploading.value = false
    uploadSuccess.value = true
    console.log('🎉 Upload completed successfully with backend integration!')
    
  } catch (error) {
    console.error('❌ Upload failed:', error)
    isUploading.value = false
    uploadSuccess.value = false
    uploadProgress.value = 0
    
    let errorMessage = 'Upload failed: ' + error.message
    if (error.message.includes('quota') || error.message.includes('storage')) {
      errorMessage = 'File too large for browser storage. Please try a smaller file or contact support.'
    }
    
    alert(errorMessage)
  }
}






const getFileType = (filename) => {
  const extension = filename.split('.').pop().toLowerCase()
  switch (extension) {
    case 'csv': return 'CSV'
    case 'json': return 'JSON'
    case 'xlsx': 
    case 'xls': return 'XLSX'
    default: return 'CSV'
  }
}


const goToPreview = () => {
  if (!uploadedFile.value) {
    alert('No file uploaded. Please upload a dataset first.')
    return
  }
  
  // Check if we have backend dataset ID
  const processedData = localStorage.getItem('processedData')
  if (!processedData) {
    alert('Dataset information not found. Please upload again.')
    return
  }
  
  try {
    const data = JSON.parse(processedData)
    if (!data.backendDatasetId) {
      alert('Dataset not properly uploaded to backend. Please try uploading again.')
      return
    }
    
    console.log('✅ Navigating to data preview with backend dataset:', data.backendDatasetId)
    navigateTo('/data-preview')
  } catch (error) {
    console.error('Error checking dataset info:', error)
    alert('Error accessing dataset information. Please upload again.')
  }
}



// Lifecycle
onMounted(async () => {
  await checkBackendConnection()
  console.log('🔍 Debug sessionStorage:')
  console.log('sessionStorage user:', sessionStorage.getItem('user'))
  console.log('localStorage user:', localStorage.getItem('user'))
  console.log('sessionStorage keys:', Object.keys(sessionStorage))
  console.log('localStorage keys:', Object.keys(localStorage))
});

</script>

<style scoped>
/* Base Dashboard Styles (keeping existing styles) */
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left .logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 32px;
  height: 32px;
}

.brand-text {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: #b3b3d1;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  color: #ffffff;
  border-bottom-color: #667eea;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  color: white;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
}



.logout-btn {
  background: none;
  border: 1px solid rgba(255, 87, 87, 0.3);
  color: #ff5757;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(255, 87, 87, 0.1);
  border-color: #ff5757;
}

.dashboard-content {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Welcome Section */
.welcome-section {
  margin-bottom: 3rem;
}

.welcome-section h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-section p {
  color: #b3b3d1;
  font-size: 1.125rem;
}

/* Cards Grid - keeping existing card styles */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.dashboard-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px 16px 0 0;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1;
}

.metric-label {
  color: #b3b3d1;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Dataset Card */
.dataset-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dataset-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
}

.dataset-meta {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.dataset-date {
  color: #667eea;
  font-size: 0.75rem;
  font-weight: 500;
}

.no-data {
  text-align: center;
  padding: 1rem;
}

.empty-state {
  color: #b3b3d1;
  margin-bottom: 1rem;
}

/* Health Gauge */
.health-gauge {
  width: 120px;
  height: 120px;
  margin: 0 auto 1rem;
}

.gauge {
  width: 100%;
  height: 100%;
}

.gauge-bg {
  stroke: rgba(102, 126, 234, 0.2);
}

.gauge-fill {
  stroke: url(#gradient);
  stroke-linecap: round;
  transition: stroke-dashoffset 1s ease;
}

.gauge-text {
  fill: #ffffff;
  font-size: 16px;
  font-weight: 700;
}

.health-label {
  text-align: center;
  color: #b3b3d1;
  font-size: 0.875rem;
}

/* Sparkline */
.sparkline {
  height: 30px;
  margin: 0.5rem 0;
}

/* Buttons */
.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.secondary-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 3rem;
}

.quick-actions h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: rgba(26, 26, 46, 0.4);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.action-card:hover {
  background: rgba(26, 26, 46, 0.6);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.action-icon.upload {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.action-icon.sample {
  background: linear-gradient(135deg, #00d4aa, #01a3a4);
}

.action-icon.tutorial {
  background: linear-gradient(135deg, #ff9500, #ff5722);
}

.action-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.action-card p {
  color: #b3b3d1;
  font-size: 0.875rem;
  margin: 0;
}

/* NEW: Inline Upload Section */
.upload-section {
  margin-top: 4rem;
  text-align: center;
}

.upload-section h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.upload-subtitle {
  color: #b3b3d1;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.inline-uploader {
  max-width: 600px;
  margin: 0 auto;
  padding: 3rem 2rem;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.inline-uploader:hover {
  border-color: rgba(102, 126, 234, 0.6);
  background: rgba(26, 26, 46, 0.8);
}

.inline-uploader.drag-over {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  transform: scale(1.02);
}

.inline-uploader.uploading,
.inline-uploader.success {
  cursor: default;
  border-style: solid;
}

/* Upload States */
.upload-initial {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  color: #667eea;
  margin-bottom: 1rem;
}

.upload-initial h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.upload-initial p {
  color: #b3b3d1;
  margin: 0;
}

.supported-formats {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin-top: 1rem;
}

.format-badge {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.upload-processing {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.processing-spinner {
  width: 50px;
  height: 50px;
  margin-bottom: 1rem;
}

.upload-processing h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.upload-processing p {
  color: #b3b3d1;
  margin: 0;
}

.progress-bar {
  width: 100%;
  max-width: 300px;
  height: 8px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.upload-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.success-icon {
  color: #00d4aa;
  margin-bottom: 1rem;
}

.upload-success h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.upload-success p {
  color: #b3b3d1;
  margin: 0;
}

.continue-btn {
  background: linear-gradient(135deg, #00d4aa, #01a3a4);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  margin-top: 1rem;
}

.continue-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 212, 170, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-center {
    order: -1;
  }

  .nav-links {
    gap: 1rem;
  }

  .dashboard-content {
    padding: 1rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .user-info {
    display: none;
  }

  .inline-uploader {
    padding: 2rem 1rem;
  }

  .supported-formats {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
}
</style>
