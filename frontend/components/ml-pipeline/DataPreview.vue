<template>
  <div class="data-preview">
    <!-- Navigation Header -->
    <nav class="preview-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
          </svg>
          Back to Dashboard
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
          </svg>
          <span>Data Preview</span>
        </div>
      </div>
      
      <div class="nav-right">
        <button @click="startMLPipeline" class="next-btn">
          <span>Start Building Model</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
          </svg>
        </button>
      </div>
    </nav>

    <!-- File Summary Hero Card -->
    <div class="hero-card">
      <div class="hero-content">
        <div class="file-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
          </svg>
        </div>
        <div class="file-info">
          <h1>{{ fileData.name }}</h1>
          <div class="file-stats">
            <span>{{ fileData.rows?.toLocaleString() }} rows</span>
            <span>•</span>
            <span>{{ fileData.columns }} columns</span>
            <span>•</span>
            <span>{{ formatFileSize(fileData.size) }}</span>
          </div>
          <div class="upload-time">Uploaded {{ timeAgo }}</div>
        </div>
        <div class="health-badge">
          <div class="health-score" :class="getHealthClass(dataHealth)">
            <span class="score">{{ dataHealth }}%</span>
            <span class="label">Health</span>
          </div>
          <div class="status-indicator">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>
            Upload Complete
          </div>
        </div>
      </div>
      
      <div class="hero-actions">
        <button @click="replaceFile" class="action-btn secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"/>
          </svg>
          Replace File
        </button>
        <button @click="configureData" class="action-btn secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
          </svg>
          Configure
        </button>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="main-content">
      <!-- Left Panel - Insights -->
      <aside class="insights-panel">
        <!-- Data Health Card -->
        <div class="insight-card health-card">
          <div class="card-header">
            <h3>🎯 Data Health</h3>
          </div>
          <div class="card-body">
            <div class="health-donut">
              <svg class="donut-chart" viewBox="0 0 120 120">
                <circle 
                  cx="60" 
                  cy="60" 
                  r="40" 
                  fill="none" 
                  stroke="rgba(102,126,234,0.2)" 
                  stroke-width="12"
                />
                <circle 
                  cx="60" 
                  cy="60" 
                  r="40" 
                  fill="none" 
                  :stroke="getHealthColor(dataHealth)"
                  stroke-width="12" 
                  stroke-linecap="round"
                  :stroke-dasharray="251"
                  :stroke-dashoffset="251 - (dataHealth / 100) * 251"
                  transform="rotate(-90 60 60)"
                />
                <text x="60" y="60" class="donut-text" text-anchor="middle" dominant-baseline="middle">
                  {{ dataHealth }}%
                </text>
              </svg>
            </div>
            <div class="health-label">Overall Quality</div>
          </div>
        </div>

        <!-- Missing Data Heatmap -->
        <div class="insight-card missing-card">
          <div class="card-header">
            <h3>⚠️ Missing Values</h3>
          </div>
          <div class="card-body">
            <div class="missing-heatmap">
              <div 
                v-for="column in columnAnalysis" 
                :key="column.name"
                class="missing-row"
              >
                <span class="column-name">{{ column.name }}</span>
                <div class="missing-bar">
                  <div 
                    class="missing-fill" 
                    :style="{ width: `${100 - column.missingPercent}%` }"
                  ></div>
                </div>
                <span class="missing-percent">{{ column.missingPercent }}%</span>
              </div>
            </div>
            <div class="missing-summary">
              {{ missingColumnCount }} columns affected
            </div>
          </div>
        </div>

        <!-- ML Opportunities -->
        <div class="insight-card ml-card">
          <div class="card-header">
            <h3>🤖 ML Opportunities</h3>
          </div>
          <div class="card-body">
            <div class="ml-suggestions">
              <div v-for="suggestion in mlSuggestions" :key="suggestion.type" class="ml-suggestion">
                <div class="suggestion-header">
                  <span class="suggestion-icon">{{ suggestion.icon }}</span>
                  <span class="suggestion-name">{{ suggestion.type }}</span>
                  <span class="confidence">{{ suggestion.confidence }}%</span>
                </div>
                <div class="confidence-bar">
                  <div 
                    class="confidence-fill" 
                    :style="{ width: `${suggestion.confidence}%` }"
                  ></div>
                </div>
                <div class="suggestion-description">{{ suggestion.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Center Panel - Data Table -->
      <main class="data-panel">
        <div class="table-header">
          <h2>Dataset Preview</h2>
          <div class="table-controls">
            <div class="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
              </svg>
              <input 
                v-model="searchQuery" 
                placeholder="Search data..." 
                class="search-input"
              />
            </div>
            <select v-model="rowsPerPage" class="rows-select">
              <option value="25">25 rows</option>
              <option value="50">50 rows</option>
              <option value="100">100 rows</option>
            </select>
            <button @click="exportData" class="export-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
              Export
            </button>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th 
                  v-for="column in tableHeaders" 
                  :key="column.name"
                  @click="sortBy(column.name)"
                  class="table-header-cell"
                >
                  <div class="header-content">
                    <span class="column-name">{{ column.name }}</span>
                    <span class="type-badge" :class="column.type">
                      {{ getTypeIcon(column.type) }} {{ column.type }}
                    </span>
                    <svg 
                      v-if="sortColumn === column.name" 
                      width="12" 
                      height="12" 
                      viewBox="0 0 24 24" 
                      fill="currentColor"
                      :class="{ 'rotate-180': sortDirection === 'desc' }"
                    >
                      <path d="M7 14l5-5 5 5z"/>
                    </svg>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in paginatedData" :key="index" class="table-row">
                <td v-for="(value, key) in row" :key="key" class="table-cell">
                  <span class="cell-value">{{ formatCellValue(value, key) }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="table-footer">
          <div class="pagination-info">
            Showing {{ (currentPage - 1) * rowsPerPage + 1 }}-{{ Math.min(currentPage * rowsPerPage, filteredData.length) }} 
            of {{ filteredData.length }} rows
          </div>
          <div class="pagination-controls">
            <button 
              @click="prevPage" 
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              Previous
            </button>
            <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
            <button 
              @click="nextPage" 
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              Next
            </button>
          </div>
        </div>
      </main>

      <!-- Right Panel - Column Analytics -->
      <aside class="analytics-panel">
        <h3>Column Analytics</h3>
        <div class="column-cards">
          <div 
            v-for="column in columnAnalysis" 
            :key="column.name"
            class="column-card"
          >
            <div class="column-header">
              <h4>{{ getColumnIcon(column.type) }} {{ column.name }}</h4>
              <span class="column-type">{{ column.type }}</span>
            </div>
            
            <div class="column-stats">
              <!-- Missing Data Bar -->
              <div class="stat-row">
                <span class="stat-label">Missing:</span>
                <div class="stat-bar">
                  <div 
                    class="stat-fill missing" 
                    :style="{ width: `${column.missingPercent}%` }"
                  ></div>
                </div>
                <span class="stat-value">{{ column.missingPercent }}%</span>
              </div>

              <!-- Unique Values -->
              <div class="stat-row">
                <span class="stat-label">Unique:</span>
                <span class="stat-value">{{ column.uniqueValues }} values</span>
              </div>

              <!-- Distribution Visualization -->
              <div v-if="column.type === 'number'" class="distribution">
                <div class="distribution-label">Distribution:</div>
                <svg class="histogram" viewBox="0 0 100 30">
                  <rect 
                    v-for="(bar, i) in column.histogram" 
                    :key="i"
                    :x="i * 10" 
                    :width="8"
                    :height="bar.height" 
                    :y="30 - bar.height"
                    fill="url(#columnGradient)"
                  />
                  <defs>
                    <linearGradient id="columnGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#667eea"/>
                      <stop offset="100%" stop-color="#764ba2"/>
                    </linearGradient>
                  </defs>
                </svg>
                <div class="range-labels">
                  <span>{{ column.min }}</span>
                  <span>{{ column.max }}</span>
                </div>
              </div>

              <!-- Top Values for Categorical -->
              <div v-if="column.type === 'string'" class="top-values">
                <div class="distribution-label">Top Values:</div>
                <div 
                  v-for="value in column.topValues" 
                  :key="value.name"
                  class="value-bar"
                >
                  <span class="value-name">{{ value.name }}</span>
                  <div class="value-bar-container">
                    <div 
                      class="value-bar-fill" 
                      :style="{ width: `${(value.count / column.maxCount) * 100}%` }"
                    ></div>
                  </div>
                  <span class="value-count">{{ value.count }}</span>
                </div>
              </div>

              <!-- Outliers Warning -->
              <div v-if="column.outliers > 0" class="outliers-warning">
                ⚠️ {{ column.outliers }} outliers detected
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Action Footer -->
    <div class="action-footer">
      <div class="footer-content">
        <button @click="goBack" class="footer-btn secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
          </svg>
          Back to Dashboard
        </button>
        
        <div class="ready-indicator">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
          </svg>
          <span>Data looks great for ML!</span>
        </div>

        <button @click="startMLPipeline" class="footer-btn primary">
          <span>🚀 Start Building ML Model</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

// Page Meta
useHead({
  title: 'Data Preview - DataSage ML Platform',
  meta: [
    { name: 'description', content: 'Explore and analyze your dataset before building ML models' }
  ]
})

// Reactive Data
const fileData = ref({})
const tableData = ref([])
const tableHeaders = ref([])
const columnAnalysis = ref([])
const dataHealth = ref(87)
const timeAgo = ref('2 minutes ago')
const searchQuery = ref('')
const sortColumn = ref('')
const sortDirection = ref('asc')
const currentPage = ref(1)
const rowsPerPage = ref(50)

// ML Suggestions
const mlSuggestions = reactive([
  {
    type: 'Classification',
    icon: '🎯',
    confidence: 92,
    description: 'Predict categories based on features'
  },
  {
    type: 'Regression',
    icon: '📈',
    confidence: 78,
    description: 'Predict continuous numerical values'
  },
  {
    type: 'Clustering',
    icon: '🔍',
    confidence: 65,
    description: 'Find hidden patterns in data'
  }
])

// Computed Properties
const missingColumnCount = computed(() => {
  return columnAnalysis.value.filter(col => col.missingPercent > 0).length
})

const filteredData = computed(() => {
  if (!searchQuery.value) return tableData.value
  
  return tableData.value.filter(row => {
    return Object.values(row).some(value => 
      String(value).toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

const totalPages = computed(() => {
  return Math.ceil(filteredData.value.length / rowsPerPage.value)
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value
  const end = start + parseInt(rowsPerPage.value)
  return filteredData.value.slice(start, end)
})

// Methods
const loadDataFromSession = () => {
  try {
    const storedData = sessionStorage.getItem('uploadedDataset')
    if (storedData) {
      fileData.value = JSON.parse(storedData)
      generateMockData()
    } else {
      // Redirect back to dashboard if no data
      navigateTo('/dashboard')
    }
  } catch (error) {
    console.error('Error loading dataset:', error)
    navigateTo('/dashboard')
  }
}

const generateMockData = () => {
  // Generate realistic table data based on file info
  const rows = Math.min(fileData.value.rows || 100, 100) // Show first 100 rows
  const columns = fileData.value.columns || 8
  
  // Create headers with realistic names and types
  const headerNames = [
    'customer_id', 'age', 'salary', 'region', 'purchase_score', 
    'signup_date', 'is_premium', 'last_activity'
  ].slice(0, columns)
  
  tableHeaders.value = headerNames.map(name => ({
    name,
    type: detectColumnType(name)
  }))
  
  // Generate sample data
  tableData.value = Array.from({ length: rows }, (_, i) => {
    const row = {}
    headerNames.forEach(header => {
      row[header] = generateSampleValue(header, i)
    })
    return row
  })
  
  // Generate column analysis
  columnAnalysis.value = headerNames.map(name => ({
    name,
    type: detectColumnType(name),
    missingPercent: Math.random() * 15, // 0-15% missing
    uniqueValues: Math.floor(Math.random() * rows * 0.8),
    histogram: generateHistogram(),
    topValues: generateTopValues(name),
    maxCount: 50,
    outliers: Math.floor(Math.random() * 5),
    min: 0,
    max: 100
  }))
}

const detectColumnType = (name) => {
  if (name.includes('id')) return 'string'
  if (name.includes('age') || name.includes('score') || name.includes('salary')) return 'number'
  if (name.includes('date') || name.includes('time')) return 'date'
  if (name.includes('is_') || name.includes('has_')) return 'boolean'
  return 'string'
}

const generateSampleValue = (header, index) => {
  const type = detectColumnType(header)
  
  switch (type) {
    case 'number':
      if (header.includes('age')) return 18 + Math.floor(Math.random() * 50)
      if (header.includes('salary')) return 30000 + Math.floor(Math.random() * 100000)
      if (header.includes('score')) return (Math.random() * 10).toFixed(1)
      return Math.floor(Math.random() * 1000)
    case 'date':
      return new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    case 'boolean':
      return Math.random() > 0.5
    case 'string':
      if (header.includes('region')) return ['North', 'South', 'East', 'West'][Math.floor(Math.random() * 4)]
      if (header.includes('id')) return `C${String(index + 1).padStart(4, '0')}`
      return `Value_${index + 1}`
  }
}

const generateHistogram = () => {
  return Array.from({ length: 10 }, () => ({
    height: Math.random() * 25 + 5
  }))
}

const generateTopValues = (name) => {
  if (detectColumnType(name) !== 'string') return []
  
  return [
    { name: 'Value A', count: 45 },
    { name: 'Value B', count: 32 },
    { name: 'Value C', count: 28 },
    { name: 'Value D', count: 15 }
  ]
}

const formatCellValue = (value, key) => {
  const type = detectColumnType(key)
  
  if (value === null || value === undefined) return '—'
  
  switch (type) {
    case 'number':
      if (key.includes('salary')) return `$${Number(value).toLocaleString()}`
      return Number(value).toLocaleString()
    case 'boolean':
      return value ? '✓' : '✗'
    case 'date':
      return new Date(value).toLocaleDateString()
    default:
      return String(value)
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getHealthClass = (score) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

const getHealthColor = (score) => {
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#f59e0b'
  if (score >= 40) return '#ef4444'
  return '#dc2626'
}

const getTypeIcon = (type) => {
  const icons = {
    number: '📊',
    string: '📝',
    date: '📅',
    boolean: '✓'
  }
  return icons[type] || '📄'
}

const getColumnIcon = (type) => {
  const icons = {
    number: '📊',
    string: '🗺️',
    date: '📅',
    boolean: '✅'
  }
  return icons[type] || '📄'
}

const sortBy = (column) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
  
  tableData.value.sort((a, b) => {
    const aVal = a[column]
    const bVal = b[column]
    
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
}

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const goBack = () => {
  navigateTo('/dashboard')
}

const startMLPipeline = () => {
  // Store current dataset info and redirect to ML pipeline
  sessionStorage.setItem('previewedDataset', JSON.stringify({
    ...fileData.value,
    analysis: columnAnalysis.value,
    health: dataHealth.value,
    mlSuggestions: mlSuggestions
  }))
  navigateTo('/ml-pipeline')
}

const replaceFile = () => {
  sessionStorage.removeItem('uploadedDataset')
  navigateTo('/dashboard')
}

const configureData = () => {
  console.log('Configure data settings')
}

const exportData = () => {
  console.log('Export data')
}

// Lifecycle
onMounted(() => {
  loadDataFromSession()
  console.log('📊 Data Preview loaded!')
})
</script>

<style scoped>
/* Base Styles */
.data-preview {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Navigation Header */
.preview-header {
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
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #b3b3d1;
  font-size: 0.875rem;
}

.next-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

/* Hero Card */
.hero-card {
  margin: 2rem;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.hero-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px 16px 0 0;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.file-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.file-info h1 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.file-stats {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #b3b3d1;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.upload-time {
  color: #667eea;
  font-size: 0.875rem;
}

.health-badge {
  margin-left: auto;
  text-align: right;
}

.health-score {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 0.5rem;
}

.health-score.excellent { background: rgba(16, 185, 129, 0.2); }
.health-score.good { background: rgba(245, 158, 11, 0.2); }
.health-score.fair { background: rgba(239, 68, 68, 0.2); }
.health-score.poor { background: rgba(220, 38, 38, 0.2); }

.health-score .score {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
}

.health-score .label {
  font-size: 0.75rem;
  color: #b3b3d1;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #10b981;
  font-size: 0.875rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.action-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.action-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Main Content Grid */
.main-content {
  display: grid;
  grid-template-columns: 320px 1fr 320px;
  gap: 2rem;
  padding: 0 2rem 2rem;
  min-height: calc(100vh - 300px);
}

/* Insights Panel */
.insights-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
}

.card-header {
  margin-bottom: 1rem;
}

.card-header h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.health-donut {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.donut-chart {
  width: 120px;
  height: 120px;
}

.donut-text {
  font-size: 18px;
  font-weight: 700;
  fill: #ffffff;
}

.health-label {
  text-align: center;
  color: #b3b3d1;
  font-size: 0.875rem;
}

/* Missing Data Heatmap */
.missing-heatmap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.missing-row {
  display: grid;
  grid-template-columns: 1fr 60px 40px;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.column-name {
  color: #ffffff;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.missing-bar {
  height: 8px;
  background: rgba(239, 68, 68, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.missing-fill {
  height: 100%;
  background: #10b981;
  transition: width 0.3s ease;
}

.missing-percent {
  color: #b3b3d1;
  text-align: right;
}

.missing-summary {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  color: #b3b3d1;
  font-size: 0.875rem;
  text-align: center;
}

/* ML Suggestions */
.ml-suggestions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ml-suggestion {
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
}

.suggestion-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.suggestion-icon {
  font-size: 1.25rem;
}

.suggestion-name {
  font-weight: 600;
  color: #ffffff;
  flex: 1;
  margin-left: 0.5rem;
}

.confidence {
  color: #667eea;
  font-weight: 600;
  font-size: 0.875rem;
}

.confidence-bar {
  height: 6px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.suggestion-description {
  color: #b3b3d1;
  font-size: 0.75rem;
}

/* Data Table Panel */
.data-panel {
  display: flex;
  flex-direction: column;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.table-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.table-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #b3b3d1;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem 0.5rem 2.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.875rem;
}

.search-input::placeholder {
  color: #b3b3d1;
}

.rows-select, .export-btn {
  padding: 0.5rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.875rem;
  cursor: pointer;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.table-container {
  flex: 1;
  overflow: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header-cell {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  cursor: pointer;
  user-select: none;
}

.table-header-cell:hover {
  background: rgba(102, 126, 234, 0.1);
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.column-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.875rem;
}

.type-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
  width: fit-content;
}

.type-badge.number { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.type-badge.string { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.type-badge.date { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.type-badge.boolean { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }

.table-row:hover {
  background: rgba(102, 126, 234, 0.05);
}

.table-cell {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  font-size: 0.875rem;
}

.cell-value {
  color: #b3b3d1;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  background: rgba(26, 26, 46, 0.4);
}

.pagination-info {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #b3b3d1;
  font-size: 0.875rem;
}

/* Analytics Panel */
.analytics-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.analytics-panel h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.column-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: calc(100vh - 400px);
  overflow-y: auto;
}

.column-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.column-header h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.column-type {
  font-size: 0.75rem;
  color: #b3b3d1;
  text-transform: uppercase;
  font-weight: 500;
}

.column-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.stat-label {
  color: #b3b3d1;
  min-width: 50px;
}

.stat-bar {
  flex: 1;
  height: 6px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.stat-fill.missing {
  background: #ef4444;
}

.stat-value {
  color: #ffffff;
  font-weight: 500;
  min-width: 40px;
  text-align: right;
}

.distribution {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.distribution-label {
  font-size: 0.75rem;
  color: #b3b3d1;
  font-weight: 500;
}

.histogram {
  width: 100%;
  height: 30px;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.625rem;
  color: #b3b3d1;
}

.top-values {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.value-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.value-name {
  color: #ffffff;
  font-weight: 500;
  min-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.value-bar-container {
  flex: 1;
  height: 4px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.value-bar-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.value-count {
  color: #b3b3d1;
  font-weight: 500;
  min-width: 30px;
  text-align: right;
}

.outliers-warning {
  padding: 0.5rem;
  background: rgba(245, 158, 11, 0.2);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 6px;
  color: #fbbf24;
  font-size: 0.75rem;
  text-align: center;
}

/* Action Footer */
.action-footer {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  padding: 1.5rem 2rem;
  position: sticky;
  bottom: 0;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.footer-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.footer-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.footer-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  animation: pulse 2s infinite;
}

.footer-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
}

@keyframes pulse {
  0% { box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4); }
  50% { box-shadow: 0 8px 32px rgba(102, 126, 234, 0.6); }
  100% { box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4); }
}

.ready-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #10b981;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 280px 1fr 280px;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .hero-content {
    flex-direction: column;
    text-align: center;
  }
  
  .health-badge {
    margin-left: 0;
    text-align: center;
  }
  
  .table-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .ready-indicator {
    order: -1;
  }
}

/* Utility Classes */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
