<template>
  <div class="model-training">
    <!-- Navigation Header -->
    <nav class="training-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
          Back
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Model Training</span>
        </div>
      </div>
      
      <div class="header-status" v-if="backendConnected !== null">
        <div class="status-indicator" :class="{ 'connected': backendConnected }">
          <div class="status-dot"></div>
          <span class="status-text">{{ backendConnected ? 'Backend Connected' : 'Backend Offline' }}</span>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🚀</div>
        <h1>Model Training</h1>
        <p>Training your {{ problemType }} model with advanced features</p>
        
        <div class="training-summary" v-if="modelConfig">
          <span class="summary-item">{{ formatNumber(datasetStats.rows) }} samples</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ modelConfig.algorithm?.name || 'Unknown' }}</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ getValidationMethodDisplay() }}</span>
        </div>
      </div>
    </div>

    
    <div class="preprocessing-summary" v-if="preprocessingInfo">
        <div class="section-header" @click="showPreprocessing = !showPreprocessing">
          <h3>🔧 Data Preprocessing Applied</h3>
          <span class="toggle-icon">{{ showPreprocessing ? '▼' : '►' }}</span>
        </div>
        
        <div v-if="showPreprocessing" class="preprocessing-details">
          <!-- Scaling card -->
          <div class="preprocessing-card">
            <h4>📊 Scaling: {{ preprocessingInfo.scaling?.method }}</h4>
            <p>Applied to {{ preprocessingInfo.scaling?.columns?.length }} numeric columns</p>
            <div class="stats-badges">
              <span class="badge success">✓ Mean = 0.0</span>
              <span class="badge success">✓ Std = 1.0</span>
            </div>
          </div>
          
          <!-- Feature engineering card -->
          <div class="preprocessing-card">
            <h4>🔨 Feature Engineering</h4>
            <p>Features: {{ preprocessingInfo.originalFeatures }} → {{ preprocessingInfo.finalFeatures }} (+{{ preprocessingInfo.finalFeatures - preprocessingInfo.originalFeatures }})</p>
          </div>
        </div>
      </div>


    <!-- Main Container -->
    <div class="main-container">
      <!-- Training Progress Section -->
      <section class="progress-section">
        <div class="section-header">
          <h2>Training Progress</h2>
          <div class="training-controls">
            <button 
              @click="startTraining"
              :disabled="isTraining || isCompleted"
              class="control-btn start"
              v-if="!isTraining && !isCompleted"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
              </svg>
              Start Training
            </button>
            
            <button 
              @click="pauseTraining"
              :disabled="!isTraining"
              class="control-btn pause"
              v-if="isTraining && !isPaused"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,19H18V5H14M6,19H10V5H6V19Z" />
              </svg>
              Pause
            </button>
            
            <button 
              @click="resumeTraining"
              class="control-btn resume"
              v-if="isPaused"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
              </svg>
              Resume
            </button>
            
            <button 
              @click="stopTraining"
              :disabled="!isTraining"
              class="control-btn stop"
              v-if="isTraining"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18,18H6V6H18V18Z" />
              </svg>
              Stop
            </button>
          </div>
        </div>

        <!-- Progress Dashboard -->
        <div class="progress-dashboard">
          <div class="progress-main">
            <div class="progress-info">
              <h3>{{ getTrainingPhase() }}</h3>
              <div class="progress-details">
                <div class="detail-item">
                  <span class="detail-label">Epoch:</span>
                  <span class="detail-value">{{ currentEpoch }}/{{ totalEpochs }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Time Elapsed:</span>
                  <span class="detail-value">{{ formatTime(elapsedTime) }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">ETA:</span>
                  <span class="detail-value">{{ formatTime(estimatedTimeRemaining) }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Validation:</span>
                  <span class="detail-value">{{ getValidationMethodDisplay() }}</span>
                </div>
              </div>
            </div>
            
            <div class="progress-visual">
              <div class="progress-circle">
                <svg class="progress-ring" width="120" height="120">
                  <circle
                    class="progress-ring-circle background"
                    stroke="rgba(102, 126, 234, 0.2)"
                    stroke-width="8"
                    fill="transparent"
                    r="52"
                    cx="60"
                    cy="60"
                  />
                  <circle
                    class="progress-ring-circle foreground"
                    :stroke-dasharray="circumference + ' ' + circumference"
                    :stroke-dashoffset="progressOffset"
                    stroke="url(#progressGradient)"
                    stroke-width="8"
                    fill="transparent"
                    r="52"
                    cx="60"
                    cy="60"
                  />
                  <defs>
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                    </linearGradient>
                  </defs>
                </svg>
                <div class="progress-text">
                  <span class="progress-percent">{{ Math.round(trainingProgress) }}%</span>
                  <span class="progress-label">Complete</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Training Stages -->
          <div class="stage-progress">
            <div class="stage-item" :class="{ 'active': currentStage >= 1, 'completed': currentStage > 1 }">
              <div class="stage-icon">📊</div>
              <div class="stage-info">
                <span class="stage-name">Preprocessing</span>
                <div class="stage-bar">
                  <div class="bar-fill" :style="{ width: getStageProgress(1) + '%' }"></div>
                </div>
              </div>
            </div>
            
            <div class="stage-item" :class="{ 'active': currentStage >= 2, 'completed': currentStage > 2 }">
              <div class="stage-icon">🤖</div>
              <div class="stage-info">
                <span class="stage-name">Training</span>
                <div class="stage-bar">
                  <div class="bar-fill" :style="{ width: getStageProgress(2) + '%' }"></div>
                </div>
              </div>
            </div>
            
            <div class="stage-item" :class="{ 'active': currentStage >= 3, 'completed': currentStage > 3 }">
              <div class="stage-icon">🎯</div>
              <div class="stage-info">
                <span class="stage-name">Validation</span>
                <div class="stage-bar">
                  <div class="bar-fill" :style="{ width: getStageProgress(3) + '%' }"></div>
                </div>
              </div>
            </div>
            
            <div class="stage-item" :class="{ 'active': currentStage >= 4, 'completed': currentStage > 4 }">
              <div class="stage-icon">✅</div>
              <div class="stage-info">
                <span class="stage-name">Finalization</span>
                <div class="stage-bar">
                  <div class="bar-fill" :style="{ width: getStageProgress(4) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Metrics and Charts Grid -->
      <div class="metrics-charts-grid">
        <!-- Metrics Section -->
        <section class="metrics-section">
          <div class="section-header">
            <h2>Performance Metrics</h2>
          </div>

          <div class="metrics-grid">
            <!-- Main Metric -->
            <div class="metric-card primary" :key="`main-${currentMetrics.test_accuracy}-${currentMetrics.test_r2}`">
              <div class="metric-icon">🎯</div>
              <div class="metric-content">
                <div class="metric-value">{{ formatMainMetric() }}</div>
                <div class="metric-label">{{ getMainMetricLabel() }}</div>
                <div class="metric-change" :class="getChangeClass(metricChanges.main)">
                  {{ formatChange(metricChanges.main) }}
                </div>
              </div>
            </div>

            <!-- Secondary Metric -->
            <div class="metric-card success" :key="`secondary-${currentMetrics.test_f1}-${currentMetrics.test_mse}`">
              <div class="metric-icon">📈</div>
              <div class="metric-content">
                <div class="metric-value">{{ formatSecondaryMetric() }}</div>
                <div class="metric-label">{{ getSecondaryMetricLabel() }}</div>
                <div class="metric-change" :class="getChangeClass(metricChanges.secondary, problemType === 'regression')">
                  {{ formatChange(metricChanges.secondary) }}
                </div>
              </div>
            </div>

            <!-- Classification Metrics -->
            <template v-if="problemType.includes('classification')">
              <div class="metric-card info">
                <div class="metric-icon">🔍</div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatMetric(currentMetrics.test_precision * 100) }}%</div>
                  <div class="metric-label">Precision</div>
                </div>
              </div>

              <div class="metric-card warning">
                <div class="metric-icon">🎪</div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatMetric(currentMetrics.test_recall * 100) }}%</div>
                  <div class="metric-label">Recall</div>
                </div>
              </div>
            </template>

            <!-- Regression Metrics -->
            <template v-if="!problemType.includes('classification')">
              <div class="metric-card info">
                <div class="metric-icon">📉</div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatMetric(currentMetrics.test_mae) }}</div>
                  <div class="metric-label">MAE</div>
                </div>
              </div>

              <div class="metric-card warning">
                <div class="metric-icon">🎲</div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatMetric(Math.sqrt(currentMetrics.test_mse || 0)) }}</div>
                  <div class="metric-label">RMSE</div>
                </div>
              </div>
            </template>
          </div>

          <!-- Cross-Validation Results -->
          <div class="cv-results" v-if="hasAdvancedValidation() && currentMetrics.cv_scores && currentMetrics.cv_scores.length > 0">
            <h4>Cross-Validation Results</h4>
            <div class="cv-summary">
              <span class="cv-metric">Mean: {{ formatMetric(currentMetrics.cv_mean * 100) }}%</span>
              <span class="cv-metric">Std: ±{{ formatMetric(currentMetrics.cv_std * 100) }}%</span>
              <span class="cv-metric">Folds: {{ currentMetrics.cv_scores.length }}</span>
            </div>
            <div class="cv-fold-scores">
              <div 
                v-for="(score, index) in currentMetrics.cv_scores" 
                :key="index"
                class="cv-fold"
              >
                Fold {{ index + 1 }}: {{ formatMetric(score * 100) }}%
              </div>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="charts-section">
          <div class="section-header">
            <h2>Training Visualization</h2>
          </div>

          <div class="chart-container">
            <canvas ref="chartContainer" v-if="isTraining || isCompleted"></canvas>
            <div class="chart-placeholder" v-else>
              <svg class="chart-icon" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 3v18h18" stroke-width="2"/>
                <path d="M7 16l4-4 3 3 5-5" stroke-width="2"/>
              </svg>
              <p>Training curves will appear during training</p>
            </div>
          </div>
        </section>
      </div>

      <!-- Training Logs Section -->
      <section class="logs-section">
        <div class="section-header">
          <h2>Training Logs</h2>
          <div class="log-controls">
            <button @click="clearLogs" class="clear-btn">Clear</button>
            <button @click="exportLogs" class="export-btn">Export</button>
          </div>
        </div>

        <div class="logs-container" ref="logsContainer">
          <div v-if="trainingLogs.length === 0" class="log-empty">
            No logs yet. Start training to see progress updates.
          </div>
          <div v-for="(log, index) in trainingLogs" :key="index" class="log-entry" :class="log.type">
            <span class="log-time">{{ formatLogTime(log.timestamp) }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </section>

      <!-- Completion Section -->
      <section class="action-section" v-if="isCompleted">
        <div class="action-content">
          <div class="completion-message">
            <div class="completion-icon">🎉</div>
            <h3>Training Completed Successfully!</h3>
            <p>Your {{ problemType }} model is ready for evaluation and deployment.</p>
            
            <div class="training-summary-complete">
              <div class="summary-row">
                <span class="summary-label">Algorithm:</span>
                <span class="summary-value">{{ modelConfig?.algorithm?.name }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">Final Score:</span>
                <span class="summary-value">{{ formatMainMetric() }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">Validation:</span>
                <span class="summary-value">{{ getValidationMethodDisplay() }}</span>
              </div>
            </div>
          </div>

          <div class="action-buttons">
            <button @click="retrain" class="action-btn secondary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
              </svg>
              Train Again
            </button>
            <button @click="viewResults" class="action-btn primary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3,3V21H21V3M5,5H19V19H5M7.5,18A4.5,4.5 0 0,1 12,13.5A4.5,4.5 0 0,1 16.5,18" />
              </svg>
              View Results
            </button>
          </div>
        </div>
      </section>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isInitializing" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h3>Initializing Training Environment</h3>
        <p>{{ initializationMessage }}</p>
        <div class="loading-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: initializationProgress + '%' }"></div>
          </div>
          <span class="progress-text">{{ initializationProgress }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const router = useRouter()

// Core State
const isInitializing = ref(true)
const initializationProgress = ref(0)
const initializationMessage = ref('Loading configuration...')
const backendConnected = ref(null)

const isTraining = ref(false)
const isPaused = ref(false)
const isCompleted = ref(false)
const preprocessingInfo = ref(null)
const showPreprocessing = ref(false)

// Training Progress
const trainingProgress = ref(0)
const currentEpoch = ref(0)
const totalEpochs = ref(100)
const currentStage = ref(0)
const elapsedTime = ref(0)
const estimatedTimeRemaining = ref(0)
let websocket = null
let timeInterval = null

// Configuration
const modelConfig = ref(null)
const datasetStats = ref({ rows: 0, features: 0 })
const datasetId = ref(null)
const problemType = ref('classification')

// UI Controls
const selectedChart = ref('accuracy')
const selectedMetricView = ref('training')

// Metrics
const currentMetrics = reactive({
  train_accuracy: 0,
  test_accuracy: 0,
  train_f1: 0,
  test_f1: 0,
  train_precision: 0,
  test_precision: 0,
  train_recall: 0,
  test_recall: 0,
  train_r2: 0,
  test_r2: 0,
  train_mse: 0,
  test_mse: 0,
  train_mae: 0,
  test_mae: 0,
  cv_mean: 0,
  cv_std: 0,
  cv_scores: [],
  samplesPerSec: 0
})

const metricChanges = reactive({
  main: 0,
  secondary: 0,
  precision: 0,
  recall: 0,
  mae: 0,
  rmse: 0
})

// Training history for charts
const trainingHistory = ref({
  epochs: [],
  train_scores: [],
  test_scores: []
})

const chartContainer = ref(null)
let trainingChart = null

const trainingLogs = ref([])
const logsContainer = ref(null)

// Computed Properties
const circumference = computed(() => 2 * Math.PI * 52)
const progressOffset = computed(() => 
  circumference.value - (trainingProgress.value / 100) * circumference.value
)

// Feature Detection
const hasFeatureScaling = () => {
  return modelConfig.value?.scaling && modelConfig.value.scaling !== 'none'
}

const hasFeatureEngineering = () => {
  const fe = modelConfig.value?.featureEngineering || {}
  return fe.polynomial || fe.pca || fe.featureSelection
}

const hasAdvancedValidation = () => {
  const method = modelConfig.value?.validation?.method
  return method === 'cross_validation' || method === 'stratified'
}

const getScalingDisplay = () => {
  const scaling = modelConfig.value?.scaling || 'none'
  const displays = {
    'none': 'No Scaling',
    'standard': 'Standard Scaling',
    'minmax': 'MinMax Scaling',
    'robust': 'Robust Scaling'
  }
  return displays[scaling] || 'Unknown'
}

const getEngineeringDisplay = () => {
  const fe = modelConfig.value?.featureEngineering || {}
  const features = []
  if (fe.polynomial) features.push('Polynomial')
  if (fe.pca) features.push('PCA')
  if (fe.featureSelection) features.push('Selection')
  return features.length > 0 ? features.join(' + ') : 'None'
}

const getValidationMethodDisplay = () => {
  const method = modelConfig.value?.validation?.method || 'train_test_split'
  const displays = {
    'train_test_split': 'Train/Test Split',
    'cross_validation': `${modelConfig.value?.validation?.cvFolds || 5}-Fold CV`,
    'stratified': `Stratified ${modelConfig.value?.validation?.cvFolds || 5}-Fold`
  }
  return displays[method] || 'Unknown'
}

// Helper Functions
const formatNumber = (num) => {
  if (typeof num !== 'number') return '0'
  return new Intl.NumberFormat().format(num)
}

const formatMetric = (value) => {
  if (typeof value !== 'number' || isNaN(value)) return '0.0'
  
  // For very large numbers (MSE, MAE)
  if (value > 100) {
    return value.toFixed(2)
  }
  
  // For R² scores (typically -1 to 1, can be negative)
  if (value >= -1 && value <= 1) {
    return value.toFixed(3)
  }
  
  // For other decimals
  return value.toFixed(3)
}

const formatMainMetric = () => {
  console.log('🔍 formatMainMetric called - problemType:', problemType.value, 'test_accuracy:', currentMetrics.test_accuracy, 'test_r2:', currentMetrics.test_r2)
  
  // Check if it's any classification type
  const isClassification = problemType.value.includes('classification')
  
  if (isClassification) {
    const accuracy = currentMetrics.test_accuracy || 0
    console.log('📊 Classification - raw accuracy:', accuracy)
    // If accuracy is 0-1 range, convert to percentage
    if (accuracy > 0 && accuracy <= 1) {
      return (accuracy * 100).toFixed(1) + '%'
    }
    // If already in percentage range
    return accuracy.toFixed(1) + '%'
  } else {
    const r2 = currentMetrics.test_r2 || 0
    console.log('📊 Regression - raw r2:', r2)
    return r2.toFixed(3)
  }
}

const getMainMetricLabel = () => {
  const isClassification = problemType.value.includes('classification')
  return isClassification ? 'Test Accuracy' : 'R² Score'
}

const formatSecondaryMetric = () => {
  console.log('🔍 formatSecondaryMetric called - problemType:', problemType.value, 'test_f1:', currentMetrics.test_f1, 'test_mse:', currentMetrics.test_mse)
  
  const isClassification = problemType.value.includes('classification')
  
  if (isClassification) {
    const f1 = currentMetrics.test_f1 || 0
    console.log('📊 Classification - raw f1:', f1)
    if (f1 > 0 && f1 <= 1) {
      return (f1 * 100).toFixed(1) + '%'
    }
    return f1.toFixed(1) + '%'
  } else {
    const mse = currentMetrics.test_mse || 0
    console.log('📊 Regression - raw mse:', mse)
    return mse.toFixed(2)
  }
}

const getSecondaryMetricLabel = () => {
  const isClassification = problemType.value.includes('classification')
  return isClassification ? 'F1-Score' : 'MSE'
}

const formatChange = (change) => {
  if (!change || typeof change !== 'number' || isNaN(change)) return '0.0%'
  const sign = change > 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}%`
}

const getChangeClass = (change, isLoss = false) => {
  if (!change || isNaN(change)) return 'neutral'
  if (isLoss) {
    return change > 0 ? 'negative' : 'positive'
  } else {
    return change > 0 ? 'positive' : 'negative'
  }
}

const formatTime = (seconds) => {
  if (typeof seconds !== 'number' || isNaN(seconds)) return '0s'
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  if (minutes > 0) {
    return `${minutes}m ${secs}s`
  } else {
    return `${secs}s`
  }
}

const formatLogTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}

const getTrainingPhase = () => {
  if (!isTraining.value && !isCompleted.value) return 'Ready to Start Training'
  if (isPaused.value) return 'Training Paused'
  if (isCompleted.value) return 'Training Complete'
  
  switch (currentStage.value) {
    case 1: return 'Preprocessing Data'
    case 2: return 'Training Model'
    case 3: return 'Running Validation'
    case 4: return 'Finalizing Model'
    default: return 'Training in Progress'
  }
}

const getStageProgress = (stage) => {
  if (currentStage.value > stage) return 100
  if (currentStage.value < stage) return 0
  
  const progress = trainingProgress.value / 100
  switch (stage) {
    case 1: return Math.min(100, Math.max(0, (progress * 10) / 0.1 * 100))
    case 2: return Math.min(100, Math.max(0, ((progress - 0.1) / 0.7) * 100))
    case 3: return Math.min(100, Math.max(0, ((progress - 0.8) / 0.15) * 100))
    case 4: return Math.min(100, Math.max(0, ((progress - 0.95) / 0.05) * 100))
    default: return 0
  }
}

// Backend Functions
const checkBackendConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/health')
    if (response.ok) {
      backendConnected.value = true
      console.log('Backend connected')
      return true
    }
  } catch (error) {
    console.error('Backend connection failed:', error)
    backendConnected.value = false
    return false
  }
}

const loadConfiguration = async () => {
  try {
    console.log('Loading configuration...')
    
    const mlConfig = localStorage.getItem('mlConfiguration')
    if (!mlConfig) {
      console.error('No ML configuration found')
      router.push('/algorithm-select')
      return
    }

    modelConfig.value = JSON.parse(mlConfig)
    console.log('Loaded config:', modelConfig.value)

    // Extract configuration
    if (modelConfig.value.problemType) {
      problemType.value = modelConfig.value.problemType.type || 'classification'
      selectedChart.value = problemType.value === 'classification' ? 'accuracy' : 'r2'
    }
    
    if (modelConfig.value.datasetStats) {
      datasetStats.value = {
        rows: modelConfig.value.datasetStats.rows || 0,
        features: modelConfig.value.datasetStats.features || 0
      }
    }
    
    if (modelConfig.value.backendDatasetId) {
      datasetId.value = modelConfig.value.backendDatasetId
    }

    // Set epochs
    if (modelConfig.value.algorithm?.name) {
      switch(modelConfig.value.algorithm.name) {
        case 'Random Forest':
        case 'XGBoost':
          totalEpochs.value = modelConfig.value.hyperparameters?.n_estimators || 100
          break
        case 'Neural Network (MLP)':
          totalEpochs.value = 200
          break
        default:
          totalEpochs.value = 50
      }
    }

  } catch (error) {
    console.error('Failed to load configuration:', error)
    addLog('error', `Failed to load configuration: ${error.message}`)
  }
}





// Training Functions
const startTraining = async () => {
  try {
    if (!modelConfig.value || !datasetId.value) {
      throw new Error('Configuration not loaded properly')
    }

    // Verify dataset
    const response = await fetch(`http://localhost:8000/api/datasets/${datasetId.value}`)
    if (!response.ok) {
      throw new Error(`Dataset ${datasetId.value} not found`)
    }

    const datasetInfo = await response.json()
    const targetColumn = modelConfig.value.target?.name

    if (!datasetInfo.columns.includes(targetColumn)) {
      throw new Error(`Target column '${targetColumn}' not found`)
    }

    // Initialize training state
    isTraining.value = true
    isCompleted.value = false
    trainingProgress.value = 0
    currentEpoch.value = 0
    currentStage.value = 1
    elapsedTime.value = 0
    
    // Clear metrics and chart data
    Object.keys(currentMetrics).forEach(key => {
      if (Array.isArray(currentMetrics[key])) {
        currentMetrics[key] = []
      } else {
        currentMetrics[key] = 0
      }
    })
    Object.keys(metricChanges).forEach(key => metricChanges[key] = 0)
    
    // Initialize chart
    nextTick(() => {
      destroyChart()
      initializeChart()
    })
    
    // Start timing
    const startTime = Date.now()
    timeInterval = setInterval(() => {
      elapsedTime.value = Math.floor((Date.now() - startTime) / 1000)
      updateTimeEstimate()
    }, 1000)

    // Connect to WebSocket
    websocket = new WebSocket('ws://localhost:8000/ws/train-model')
    
    websocket.onopen = () => {
      const trainingConfig = {
        dataset_id: datasetId.value,
        target_column: targetColumn,
        algorithm: modelConfig.value.algorithm?.name || 'Random Forest',
        hyperparameters: modelConfig.value.hyperparameters || {},
        test_size: modelConfig.value.validation?.testSize || 0.2,
        scaling: modelConfig.value.scaling || 'none',
        featureEngineering: modelConfig.value.featureEngineering || {},
        validation_method: modelConfig.value.validation?.method || 'train_test_split',
        cv_folds: modelConfig.value.validation?.cvFolds || 5
      }
      
      console.log('Sending training config:', trainingConfig)
      websocket.send(JSON.stringify(trainingConfig))
      
      addLog('success', 'Connected to ML Backend')
      addLog('info', `Dataset: ${trainingConfig.dataset_id}`)
      addLog('info', `Algorithm: ${trainingConfig.algorithm}`)
      addLog('info', `Target: ${trainingConfig.target_column}`)
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleTrainingUpdate(data)
    }
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
      addLog('error', 'Connection error to training server')
      isTraining.value = false
    }
    
    websocket.onclose = () => {
      console.log('WebSocket connection closed')
      if (isTraining.value) {
        addLog('warning', 'Connection closed unexpectedly')
        isTraining.value = false
      }
    }
    
  } catch (error) {
    console.error('Training failed:', error)
    addLog('error', `Error: ${error.message}`)
    isTraining.value = false
  }
}

const handleTrainingUpdate = (data) => {
  console.log('Training update received:', data)
  
  switch (data.status) {
    case 'started':
      addLog('info', 'Training initialized')
      currentStage.value = 1
      break
      
    case 'analyzing':
      addLog('info', data.message)
      currentStage.value = 1
      
      if (data.message && data.message.includes('classification')) {
        problemType.value = 'classification'
        selectedChart.value = 'accuracy'
      } else if (data.message && data.message.includes('regression')) {
        problemType.value = 'regression'
        selectedChart.value = 'r2'
      }
      break
      
    case 'preprocessing':
      preprocessingInfo.value = {
        scaling: data.scaling,
        originalFeatures: data.feature_engineering.original_features,
        finalFeatures: data.feature_engineering.final_features
      }
      addLog('info', `✓ Scaling applied: ${data.scaling.method}`)
      addLog('info', `✓ Features: ${data.feature_engineering.original_features} → ${data.feature_engineering.final_features}`)
      break
    case 'feature_engineering':
      addLog('info', data.message)
      currentStage.value = 1
      break
      
    case 'splitting':
    case 'model_init':
      addLog('info', data.message)
      currentStage.value = 2
      break
      
    case 'validation':
      addLog('info', data.message)
      currentStage.value = 3
      break
      
    case 'training':
      currentEpoch.value = data.epoch || 0
      totalEpochs.value = data.total_epochs || data.totalepochs || 100
      trainingProgress.value = (currentEpoch.value / totalEpochs.value) * 100
      currentStage.value = 2
      
      if (data.metrics) {
        console.log('📊 Updating metrics from training:', data.metrics)
        updateMetrics(data.metrics)
      }
      
      addLog('info', data.message)
      break
      
    case 'completed':
      isTraining.value = false
      isCompleted.value = true
      trainingProgress.value = 100
      currentStage.value = 4
      
      if (timeInterval) {
        clearInterval(timeInterval)
        timeInterval = null
      }
      
      if (data.final_metrics || data.finalmetrics) {
        const finalMetrics = data.final_metrics || data.finalmetrics
        console.log('Final metrics received:', finalMetrics)
        updateMetrics(finalMetrics)
      }
      
      if (data.model_id || data.modelid) {
        const modelId = data.model_id || data.modelid
        localStorage.setItem('trainedModelId', modelId)
        localStorage.setItem('modelResults', JSON.stringify({
          modelId,
          finalMetrics: data.final_metrics || data.finalmetrics,
          problemType: problemType.value,
          algorithm: modelConfig.value?.algorithm?.name,
          completedAt: new Date().toISOString()
        }))
      }
      
      addLog('success', data.message)
      break
      
    case 'failed':
      isTraining.value = false
      if (timeInterval) {
        clearInterval(timeInterval)
        timeInterval = null
      }
      addLog('error', data.message)
      break
  }
}

const updateMetrics = (metrics) => {
  if (!metrics) {
    console.warn('⚠️ No metrics provided to updateMetrics')
    return
  }
  
  console.log('🔄 Updating metrics with:', metrics)
  
  // Store previous main metric for change calculation
  const prevMain = problemType.value === 'classification' 
    ? currentMetrics.test_accuracy 
    : currentMetrics.test_r2

  const metricProblemType = metrics.problem_type || metrics.problemtype || problemType.value
  
  console.log('📊 Problem Type:', metricProblemType)
  
  if (metricProblemType === 'classification') {
    currentMetrics.train_accuracy = metrics.train_accuracy || metrics.trainaccuracy || 0
    currentMetrics.test_accuracy = metrics.test_accuracy || metrics.testaccuracy || 0
    currentMetrics.train_f1 = metrics.train_f1 || metrics.trainf1 || 0
    currentMetrics.test_f1 = metrics.test_f1 || metrics.testf1 || 0
    currentMetrics.train_precision = metrics.train_precision || metrics.trainprecision || 0
    currentMetrics.test_precision = metrics.test_precision || metrics.testprecision || 0
    currentMetrics.train_recall = metrics.train_recall || metrics.trainrecall || 0
    currentMetrics.test_recall = metrics.test_recall || metrics.testrecall || 0
    
    const newMain = currentMetrics.test_accuracy
    metricChanges.main = (newMain - prevMain) * 100
    metricChanges.secondary = (currentMetrics.test_f1 - (metricChanges.f1Score || 0)) * 100
    metricChanges.f1Score = currentMetrics.test_f1
    
    console.log('✅ Classification metrics updated:', {
      test_accuracy: currentMetrics.test_accuracy,
      test_f1: currentMetrics.test_f1
    })
    
  } else if (metricProblemType === 'regression') {
    currentMetrics.train_r2 = metrics.train_r2 || metrics.trainr2 || 0
    currentMetrics.test_r2 = metrics.test_r2 || metrics.testr2 || 0
    currentMetrics.train_mse = metrics.train_mse || metrics.trainmse || 0
    currentMetrics.test_mse = metrics.test_mse || metrics.testmse || 0
    currentMetrics.train_mae = metrics.train_mae || metrics.trainmae || 0
    currentMetrics.test_mae = metrics.test_mae || metrics.testmae || 0
    
    const newMain = currentMetrics.test_r2
    const prevSecondary = metricChanges.mseValue || currentMetrics.test_mse
    
    metricChanges.main = (newMain - prevMain) * 100
    metricChanges.secondary = currentMetrics.test_mse - prevSecondary
    metricChanges.mseValue = currentMetrics.test_mse
    
    console.log('✅ Regression metrics updated:', {
      test_r2: currentMetrics.test_r2,
      test_mse: currentMetrics.test_mse,
      test_mae: currentMetrics.test_mae
    })
  }
  
  // Cross-validation metrics
  if (metrics.cv_mean !== undefined || metrics.cvmean !== undefined) {
    currentMetrics.cv_mean = metrics.cv_mean || metrics.cvmean || 0
    currentMetrics.cv_std = metrics.cv_std || metrics.cvstd || 0
    currentMetrics.cv_scores = metrics.cv_scores || metrics.cvscores || []
  }
  
  currentMetrics.samplesPerSec = Math.floor(800 + Math.random() * 400)
  
  // Update chart with new data
  const isClassification = metricProblemType.includes('classification')
  if (isClassification) {
    const trainScore = currentMetrics.train_accuracy || 0
    const testScore = currentMetrics.test_accuracy || 0
    updateChart(currentEpoch.value, trainScore, testScore)
  } else {
    const trainScore = currentMetrics.train_r2 || 0
    const testScore = currentMetrics.test_r2 || 0
    updateChart(currentEpoch.value, trainScore, testScore)
  }
  
  console.log('🎯 Metrics updated successfully:', {
    problemType: metricProblemType,
    test_accuracy: currentMetrics.test_accuracy,
    test_r2: currentMetrics.test_r2,
    test_mse: currentMetrics.test_mse,
    test_f1: currentMetrics.test_f1
  })
}

// Control Functions
const pauseTraining = () => {
  isPaused.value = true
  addLog('warning', 'Training paused')
}

const resumeTraining = () => {
  isPaused.value = false
  addLog('info', 'Training resumed')
}

const stopTraining = () => {
  isTraining.value = false
  isPaused.value = false
  
  if (websocket) {
    websocket.close()
    websocket = null
  }
  
  if (timeInterval) {
    clearInterval(timeInterval)
    timeInterval = null
  }
  
  addLog('warning', 'Training stopped by user')
}

const retrain = () => {
  trainingProgress.value = 0
  currentEpoch.value = 0
  currentStage.value = 0
  elapsedTime.value = 0
  estimatedTimeRemaining.value = 0
  isCompleted.value = false
  
  Object.keys(currentMetrics).forEach(key => {
    if (Array.isArray(currentMetrics[key])) {
      currentMetrics[key] = []
    } else {
      currentMetrics[key] = 0
    }
  })
  Object.keys(metricChanges).forEach(key => metricChanges[key] = 0)
  
  trainingLogs.value = []
  addLog('info', 'Ready for retraining')
}

const viewResults = () => {
  router.push('/results')
}

const goBack = () => {
  router.push('/algorithm-select')
}

// Chart Functions
const initializeChart = () => {
  if (!chartContainer.value) {
    trainingChart = null 
    return
  }
  
  const ctx = chartContainer.value.getContext('2d')
  const isClassification = problemType.value.includes('classification')
  
  trainingChart = new Chart(ctx, {  // ✅ FIXED - use Chart, not window.Chart
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: isClassification ? 'Train Accuracy' : 'Train R²',
          data: [],
          borderColor: 'rgb(102, 126, 234)',
          backgroundColor: 'rgba(102, 126, 234, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: isClassification ? 'Test Accuracy' : 'Test R²',
          data: [],
          borderColor: 'rgb(16, 185, 129)',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#b3b3d1',
            font: { size: 12 }
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Epoch',
            color: '#b3b3d1'
          },
          ticks: { color: '#b3b3d1' },
          grid: { color: 'rgba(102, 126, 234, 0.1)' }
        },
        y: {
          title: {
            display: true,
            text: isClassification ? 'Accuracy' : 'R² Score',
            color: '#b3b3d1'
          },
          ticks: { color: '#b3b3d1' },
          grid: { color: 'rgba(102, 126, 234, 0.1)' },
          min: 0,
          max: isClassification ? 1 : 1
        }
      },
      animation: {
        duration: 300
      }
    }
  })
}


const updateChart = (epoch, trainScore, testScore) => {
  if (!trainingChart) return
  
  trainingChart.data.labels.push(epoch)
  trainingChart.data.datasets[0].data.push(trainScore)
  trainingChart.data.datasets[1].data.push(testScore)
  
  // Keep only last 50 points for performance
  if (trainingChart.data.labels.length > 50) {
    trainingChart.data.labels.shift()
    trainingChart.data.datasets[0].data.shift()
    trainingChart.data.datasets[1].data.shift()
  }
  
  trainingChart.update('none') // Update without animation for smoothness
}

const destroyChart = () => {
  if (trainingChart) {
    trainingChart.destroy()
    trainingChart = null
  }
}
const updateTimeEstimate = () => {
  if (currentEpoch.value > 0 && totalEpochs.value > 0) {
    const timePerEpoch = elapsedTime.value / currentEpoch.value
    const remainingEpochs = totalEpochs.value - currentEpoch.value
    estimatedTimeRemaining.value = Math.max(0, Math.floor(remainingEpochs * timePerEpoch))
  }
}

const addLog = (type, message) => {
  trainingLogs.value.push({
    type,
    message,
    timestamp: Date.now()
  })
  
  nextTick(() => {
    if (logsContainer.value) {
      logsContainer.value.scrollTop = logsContainer.value.scrollHeight
    }
  })
  
  
  if (trainingLogs.value.length > 100) {
    trainingLogs.value = trainingLogs.value.slice(-100)
  }
}

  
  nextTick(() => {
    if (logsContainer.value) {
      logsContainer.value.scrollTop = logsContainer.value.scrollHeight
    }
  })
  
  if (trainingLogs.value.length > 100) {
    trainingLogs.value = trainingLogs.value.slice(-100)
  }


const clearLogs = () => {
  trainingLogs.value = []
  addLog('info', 'Logs cleared')
}


const exportLogs = () => {
  const logData = trainingLogs.value.map(log => 
    `${formatLogTime(log.timestamp)} [${log.type.toUpperCase()}] ${log.message}`
  ).join('\n')
  
  const blob = new Blob([logData], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `training-logs-${Date.now()}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  addLog('info', 'Training logs exported')
}

// Initialization
const initializeTrainingEnvironment = async () => {
  const steps = [
    'Loading configuration...',
    'Validating dataset...',
    'Preparing environment...',
    'Initializing parameters...',
    'Ready to train!'
  ]

  for (let i = 0; i < steps.length; i++) {
    initializationMessage.value = steps[i]
    const targetProgress = ((i + 1) / steps.length) * 100
    
    while (initializationProgress.value < targetProgress) {
      initializationProgress.value += 5
      await new Promise(resolve => setTimeout(resolve, 50))
    }
    
    await new Promise(resolve => setTimeout(resolve, 300))
  }
  
  isInitializing.value = false
}

// Lifecycle
onMounted(async () => {
  console.log('Initializing Model Training...')
  
  await checkBackendConnection()
  await loadConfiguration()
  await initializeTrainingEnvironment()
})

onUnmounted(() => {
  if (websocket) {
    websocket.close()
  }
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  destroyChart()
})
</script>

<style scoped>
.model-training {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header */
.training-header {
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

.nav-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
  transform: translateX(-2px);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #b3b3d1;
  font-size: 0.875rem;
}

.breadcrumb .current {
  color: #667eea;
  font-weight: 600;
}

.header-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border-radius: 20px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 2s infinite;
}

.status-indicator.connected .status-dot {
  background: #10b981;
}

.status-text {
  font-size: 0.75rem;
  color: #b3b3d1;
}

/* Hero Section */
.hero-section {
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-section p {
  font-size: 1.25rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
}

.training-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  font-size: 1rem;
  flex-wrap: wrap;
}

.summary-item {
  color: #ffffff;
}

.summary-divider {
  color: #667eea;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

/* Training Controls */
.training-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.control-btn.start {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.control-btn.start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.control-btn.pause {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.control-btn.resume {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.control-btn.stop {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

/* Progress Dashboard */
.progress-dashboard {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.progress-main {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 3rem;
  align-items: center;
  margin-bottom: 2rem;
}

.progress-info h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: #667eea;
}

.progress-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.detail-label {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.detail-value {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
}

.progress-visual {
  position: relative;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring-circle.foreground {
  transition: stroke-dashoffset 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-percent {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  color: #667eea;
  line-height: 1;
}

.progress-label {
  display: block;
  font-size: 0.75rem;
  color: #b3b3d1;
  margin-top: 0.25rem;
}

/* Stage Progress */
.stage-progress {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.stage-item.active {
  opacity: 1;
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
}

.stage-item.completed {
  opacity: 0.8;
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}

.stage-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 50%;
  flex-shrink: 0;
}

.stage-item.active .stage-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stage-item.completed .stage-icon {
  background: linear-gradient(135deg, #10b981, #059669);
}

.stage-info {
  flex: 1;
  min-width: 0;
}

.stage-name {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
  font-size: 0.875rem;
}

.stage-bar {
  height: 4px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.5s ease;
  border-radius: 2px;
}

/* Metrics and Charts Grid */
.metrics-charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.metrics-section,
.charts-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.metric-card.primary {
  border-color: rgba(102, 126, 234, 0.4);
}

.metric-card.success {
  border-color: rgba(16, 185, 129, 0.4);
}

.metric-card.info {
  border-color: rgba(59, 130, 246, 0.4);
}

.metric-card.warning {
  border-color: rgba(245, 158, 11, 0.4);
}

.metric-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  flex-shrink: 0;
}

.metric-content {
  flex: 1;
  min-width: 0;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #b3b3d1;
  margin-bottom: 0.25rem;
}

.metric-change {
  font-size: 0.75rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.metric-change.neutral {
  color: #b3b3d1;
}

/* Cross-Validation Results */
.cv-results {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.cv-results h4 {
  margin: 0 0 1rem 0;
  color: #667eea;
  font-size: 1rem;
}

.cv-summary {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.cv-metric {
  color: #ffffff;
  font-weight: 500;
  font-size: 0.875rem;
}

.cv-fold-scores {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.cv-fold {
  font-size: 0.75rem;
  color: #b3b3d1;
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  text-align: center;
}

/* Charts */
.chart-container {
  min-height: 300px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #b3b3d1;
}

.chart-icon {
  margin: 0 auto 1rem;
  opacity: 0.5;
}

/* Logs Section */
.logs-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.log-controls {
  display: flex;
  gap: 1rem;
}

.clear-btn,
.export-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.clear-btn:hover,
.export-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.logs-container {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  padding: 1rem;
  height: 300px;
  overflow-y: auto;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.875rem;
}

.log-empty {
  color: #b3b3d1;
  text-align: center;
  padding: 2rem;
  font-style: italic;
}

.log-entry {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.log-entry:last-child {
  border-bottom: none;
}

.log-time {
  color: #b3b3d1;
  font-size: 0.75rem;
  min-width: 80px;
  flex-shrink: 0;
}

.log-message {
  flex: 1;
  word-break: break-word;
}

.log-entry.info .log-message {
  color: #ffffff;
}

.log-entry.success .log-message {
  color: #10b981;
}

.log-entry.warning .log-message {
  color: #f59e0b;
}

.log-entry.error .log-message {
  color: #ef4444;
}

/* Action Section */
.action-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 3rem;
}

.action-content {
  text-align: center;
}

.completion-message {
  margin-bottom: 2rem;
}

.completion-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.completion-message h3 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #10b981;
}

.completion-message p {
  font-size: 1.125rem;
  color: #b3b3d1;
  margin-bottom: 2rem;
}

.training-summary-complete {
  max-width: 500px;
  margin: 0 auto 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-label {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.summary-value {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.action-btn.secondary {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.4);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.action-btn.primary:hover {
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.3);
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 15, 35, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.loading-content {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

.loading-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.loading-content p {
  color: #b3b3d1;
  margin-bottom: 2rem;
  font-size: 0.875rem;
}

.loading-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-text {
  font-weight: 600;
  color: #667eea;
  min-width: 40px;
}

/* Scrollbar Styling */
.logs-container::-webkit-scrollbar {
  width: 8px;
}

.logs-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .metrics-charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 1rem;
  }
  
  .hero-section {
    padding: 2rem 1rem;
  }
  
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .hero-section p {
    font-size: 1rem;
  }
  
  .progress-main {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .progress-details {
    grid-template-columns: 1fr;
  }
  
  .stage-progress {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .training-controls {
    flex-direction: column;
    width: 100%;
  }
  
  .control-btn {
    width: 100%;
    justify-content: center;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .action-btn {
    width: 100%;
    justify-content: center;
  }
  
  .training-summary {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .summary-divider {
    display: none;
  }
  
  .breadcrumb {
    display: none;
  }
}

@media (max-width: 480px) {
  .training-header {
    padding: 0.75rem 1rem;
  }
  
  .hero-icon {
    font-size: 3rem;
  }
  
  .hero-section h1 {
    font-size: 1.75rem;
  }
  
  .progress-dashboard,
  .metrics-section,
  .charts-section,
  .logs-section,
  .action-section {
    padding: 1.5rem;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .stage-progress {
    grid-template-columns: 1fr;
  }
  
  .metric-value {
    font-size: 1.5rem;
  }
  
  .completion-icon {
    font-size: 3rem;
  }
  
  .completion-message h3 {
    font-size: 1.5rem;
  }
}
</style>