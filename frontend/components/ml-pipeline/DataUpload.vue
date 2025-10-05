<template>
    <div class="data-upload-container">
      <!-- Header Section -->
      <div class="upload-header">
        <div class="step-indicator">
          <div class="step-badge">Step 1</div>
          <div class="step-title">Upload Your Dataset</div>
        </div>
        <div class="step-description">
          Upload your dataset to start the machine learning pipeline. We support CSV, Excel, and JSON formats.
        </div>
      </div>
  
      <!-- Main Upload Area -->
      <div class="upload-main">
        <!-- Upload Zone -->
        <div 
          class="upload-zone"
          :class="{ 
            'drag-active': isDragActive,
            'has-file': selectedFile,
            'uploading': isUploading
          }"
          @drop="handleDrop"
          @dragover="handleDragOver"
          @dragenter="handleDragEnter"
          @dragleave="handleDragLeave"
          @click="triggerFileInput"
        >
          <!-- File Input (Hidden) -->
          <input
            ref="fileInput"
            type="file"
            accept=".csv,.xlsx,.xls,.json"
            @change="handleFileSelect"
            class="file-input"
            :disabled="isUploading"
          />
  
          <!-- Upload Content -->
          <div v-if="!selectedFile" class="upload-content">
            <div class="upload-icon">
              <svg v-if="!isDragActive" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10,9 9,9 8,9"></polyline>
              </svg>
              <svg v-else width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7,10 12,15 17,10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </div>
            
            <div class="upload-text">
              <h3 v-if="!isDragActive">Drop your dataset here</h3>
              <h3 v-else>Release to upload</h3>
              <p v-if="!isDragActive">or click to browse files</p>
              <p v-else>Drop your file now</p>
            </div>
            
            <div class="upload-formats">
              <div class="format-item">
                <span class="format-icon">📊</span>
                <span class="format-text">CSV</span>
              </div>
              <div class="format-item">
                <span class="format-icon">📈</span>
                <span class="format-text">Excel</span>
              </div>
              <div class="format-item">
                <span class="format-icon">📋</span>
                <span class="format-text">JSON</span>
              </div>
            </div>
          </div>
  
          <!-- File Preview -->
          <div v-else class="file-preview">
            <div class="file-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
              </svg>
            </div>
            
            <div class="file-details">
              <div class="file-name">{{ selectedFile.name }}</div>
              <div class="file-meta">
                <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
                <span class="file-type">{{ getFileType(selectedFile.name) }}</span>
              </div>
            </div>
            
            <button 
              v-if="!isUploading" 
              @click.stop="removeFile" 
              class="remove-file-btn"
              :disabled="isUploading"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
  
          <!-- Upload Progress -->
          <div v-if="isUploading" class="upload-progress">
            <div class="progress-circle">
              <svg class="progress-ring" width="60" height="60">
                <circle
                  class="progress-ring-circle"
                  stroke="currentColor"
                  stroke-width="4"
                  fill="transparent"
                  r="26"
                  cx="30"
                  cy="30"
                  :stroke-dasharray="circumference"
                  :stroke-dashoffset="progressOffset"
                />
              </svg>
              <span class="progress-text">{{ uploadProgress }}%</span>
            </div>
            <div class="progress-message">{{ uploadMessage }}</div>
          </div>
        </div>
  
        <!-- Upload Actions -->
        <div v-if="selectedFile && !isUploading" class="upload-actions">
          <button @click="removeFile" class="action-btn secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3,6 5,6 21,6"></polyline>
              <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
            </svg>
            Remove File
          </button>
          
          <button @click="uploadFile" class="action-btn primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17,8 12,3 7,8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            Upload Dataset
          </button>
        </div>
      </div>
  
      <!-- Sample Datasets Section -->
      <div class="sample-datasets">
        <div class="section-header">
          <h3>Or try our sample datasets</h3>
          <p>Perfect for testing and learning machine learning concepts</p>
        </div>
        
        <div class="samples-grid">
          <div 
            v-for="sample in sampleDatasets" 
            :key="sample.id"
            class="sample-card"
            @click="loadSampleDataset(sample)"
            :class="{ loading: sample.loading }"
          >
            <div class="sample-icon">{{ sample.icon }}</div>
            <div class="sample-info">
              <h4 class="sample-title">{{ sample.name }}</h4>
              <p class="sample-description">{{ sample.description }}</p>
              <div class="sample-meta">
                <span class="sample-rows">{{ sample.rows }} rows</span>
                <span class="sample-cols">{{ sample.cols }} columns</span>
                <span class="sample-type">{{ sample.type }}</span>
              </div>
            </div>
            <div v-if="sample.loading" class="sample-loading">
              <div class="spinner-small"></div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Upload Tips -->
      <div class="upload-tips">
        <div class="tips-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="m9,12 2,2 4,-4"></path>
          </svg>
          <h4>Upload Tips</h4>
        </div>
        
        <div class="tips-grid">
          <div class="tip-item">
            <div class="tip-icon">📊</div>
            <div class="tip-content">
              <h5>Data Format</h5>
              <p>Ensure your data has column headers and is properly structured</p>
            </div>
          </div>
          
          <div class="tip-item">
            <div class="tip-icon">🔢</div>
            <div class="tip-content">
              <h5>File Size</h5>
              <p>Maximum file size is 100MB. Larger files may take longer to process</p>
            </div>
          </div>
          
          <div class="tip-item">
            <div class="tip-icon">🎯</div>
            <div class="tip-content">
              <h5>Target Variable</h5>
              <p>Include the column you want to predict in your dataset</p>
            </div>
          </div>
          
          <div class="tip-item">
            <div class="tip-icon">✨</div>
            <div class="tip-content">
              <h5>Data Quality</h5>
              <p>Clean data leads to better models. We'll help you handle missing values</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Success Modal -->
      <div v-if="showSuccessModal" class="success-modal" @click="closeSuccessModal">
        <div class="modal-content" @click.stop>
          <div class="success-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m9,12 2,2 4,-4"></path>
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
          </div>
          
          <h3>Dataset Uploaded Successfully!</h3>
          <p>Your dataset has been processed and is ready for exploration.</p>
          
          <div class="dataset-summary" v-if="datasetSummary">
            <div class="summary-item">
              <span class="summary-label">Rows:</span>
              <span class="summary-value">{{ datasetSummary.rows }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Columns:</span>
              <span class="summary-value">{{ datasetSummary.columns }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Size:</span>
              <span class="summary-value">{{ datasetSummary.size }}</span>
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="closeSuccessModal" class="modal-btn secondary">
              Stay Here
            </button>
            <button @click="proceedToPreview" class="modal-btn primary">
              Preview Data
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
  import { useMLPipeline } from '~/composables/useMLPipeline'
  
  // Props
  const props = defineProps({
    pipelineState: {
      type: Object,
      required: true
    }
  })
  
  // Emits
  const emit = defineEmits(['update:state', 'next-step'])
  
  // ML Pipeline
  const { uploadDataset, getDatasetSummary } = useMLPipeline()
  
  // Refs
  const fileInput = ref(null)
  
  // State
  const selectedFile = ref(null)
  const isUploading = ref(false)
  const uploadProgress = ref(0)
  const uploadMessage = ref('')
  const isDragActive = ref(false)
  const showSuccessModal = ref(false)
  const datasetSummary = ref(null)
  
  // Drag and Drop
  let dragCounter = 0
  
  // Sample Datasets
  const sampleDatasets = reactive([
    {
      id: 'housing',
      name: 'House Prices',
      description: 'Predict house prices based on features like size, location, and amenities',
      icon: '🏠',
      rows: '1460',
      cols: '81',
      type: 'Regression',
      loading: false,
      url: '/api/samples/housing.csv'
    },
    {
      id: 'iris',
      name: 'Iris Flowers',
      description: 'Classic dataset for flower species classification based on measurements',
      icon: '🌸',
      rows: '150',
      cols: '5',
      type: 'Classification',
      loading: false,
      url: '/api/samples/iris.csv'
    },
    {
      id: 'titanic',
      name: 'Titanic Survival',
      description: 'Predict passenger survival on the Titanic based on demographics',
      icon: '🚢',
      rows: '891',
      cols: '12',
      type: 'Classification',
      loading: false,
      url: '/api/samples/titanic.csv'
    },
    {
      id: 'wine',
      name: 'Wine Quality',
      description: 'Predict wine quality based on chemical properties and characteristics',
      icon: '🍷',
      rows: '1599',
      cols: '12',
      type: 'Regression',
      loading: false,
      url: '/api/samples/wine.csv'
    }
  ])
  
  // Computed
  const circumference = computed(() => 2 * Math.PI * 26)
  const progressOffset = computed(() => {
    return circumference.value - (uploadProgress.value / 100) * circumference.value
  })
  
  // Methods
  const triggerFileInput = () => {
    if (!isUploading.value) {
      fileInput.value?.click()
    }
  }
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      validateAndSetFile(file)
    }
  }
  
  const validateAndSetFile = (file) => {
    // File size validation (100MB limit)
    const maxSize = 100 * 1024 * 1024 // 100MB in bytes
    if (file.size > maxSize) {
      showError('File size exceeds 100MB limit. Please choose a smaller file.')
      return
    }
  
    // File type validation
    const allowedTypes = ['.csv', '.xlsx', '.xls', '.json']
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    if (!allowedTypes.includes(fileExtension)) {
      showError('Unsupported file format. Please upload CSV, Excel, or JSON files.')
      return
    }
  
    selectedFile.value = file
    console.log('📁 File selected:', file.name, formatFileSize(file.size))
  }
  
  const removeFile = () => {
    selectedFile.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    console.log('🗑️ File removed')
  }
  
  const uploadFile = async () => {
    if (!selectedFile.value || isUploading.value) return
  
    isUploading.value = true
    uploadProgress.value = 0
    uploadMessage.value = 'Preparing upload...'
  
    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        if (uploadProgress.value < 95) {
          uploadProgress.value += Math.random() * 10
          
          if (uploadProgress.value < 30) {
            uploadMessage.value = 'Uploading file...'
          } else if (uploadProgress.value < 70) {
            uploadMessage.value = 'Processing dataset...'
          } else {
            uploadMessage.value = 'Analyzing data structure...'
          }
        }
      }, 200)
  
      // Actual upload
      const result = await uploadDataset(selectedFile.value)
  
      clearInterval(progressInterval)
      uploadProgress.value = 100
      uploadMessage.value = 'Upload complete!'
  
      // Update pipeline state
      emit('update:state', {
        dataset: result.data,
        datasetInfo: result.info,
        datasetName: selectedFile.value.name,
        datasetSize: selectedFile.value.size,
        datasetColumns: result.columns || [],
        datasetShape: result.shape || { rows: 0, columns: 0 },
        dataTypes: result.dtypes || {},
        missingValues: result.missingValues || {},
        duplicateRows: result.duplicateRows || 0
      })
  
      // Get dataset summary
      datasetSummary.value = {
        rows: result.shape?.rows || 0,
        columns: result.shape?.columns || 0,
        size: formatFileSize(selectedFile.value.size)
      }
  
      // Show success modal after a brief delay
      setTimeout(() => {
        isUploading.value = false
        showSuccessModal.value = true
      }, 500)
  
      console.log('✅ Dataset uploaded successfully:', result)
  
    } catch (error) {
      clearInterval(progressInterval)
      isUploading.value = false
      uploadProgress.value = 0
      
      showError(error.message || 'Failed to upload dataset. Please try again.')
      console.error('❌ Upload failed:', error)
    }
  }
  
  const loadSampleDataset = async (sample) => {
    if (sample.loading || isUploading.value) return
  
    sample.loading = true
    
    try {
      uploadMessage.value = `Loading ${sample.name}...`
      
      const response = await $fetch(sample.url)
      
      // Create a virtual file object
      const blob = new Blob([response], { type: 'text/csv' })
      const file = new File([blob], `${sample.id}.csv`, { type: 'text/csv' })
      
      selectedFile.value = file
      
      // Auto-upload sample dataset
      await uploadFile()
      
      console.log('📊 Sample dataset loaded:', sample.name)
      
    } catch (error) {
      showError(`Failed to load ${sample.name}. Please try again.`)
      console.error('❌ Sample dataset loading failed:', error)
    } finally {
      sample.loading = false
    }
  }
  
  // Drag and Drop Handlers
  const handleDragEnter = (e) => {
    e.preventDefault()
    dragCounter++
    isDragActive.value = true
  }
  
  const handleDragLeave = (e) => {
    e.preventDefault()
    dragCounter--
    if (dragCounter === 0) {
      isDragActive.value = false
    }
  }
  
  const handleDragOver = (e) => {
    e.preventDefault()
  }
  
  const handleDrop = (e) => {
    e.preventDefault()
    dragCounter = 0
    isDragActive.value = false
  
    const files = e.dataTransfer.files
    if (files.length > 0) {
      validateAndSetFile(files[0])
    }
  }
  
  // Modal Methods
  const closeSuccessModal = () => {
    showSuccessModal.value = false
  }
  
  const proceedToPreview = () => {
    showSuccessModal.value = false
    emit('next-step')
  }
  
  // Utility Methods
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }
  
  const getFileType = (filename) => {
    const extension = filename.split('.').pop().toUpperCase()
    return extension
  }
  
  const showError = (message) => {
    // This would typically emit to parent or use a toast system
    alert(message) // Temporary - replace with proper error handling
  }
  
  // Prevent default drag behaviors on window
  const preventDefaults = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }
  
  // Lifecycle
  onMounted(() => {
    // Prevent default drag behaviors
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      window.addEventListener(eventName, preventDefaults, false)
    })
    
    console.log('📤 DataUpload component mounted')
  })
  
  onUnmounted(() => {
    // Clean up event listeners
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      window.removeEventListener(eventName, preventDefaults, false)
    })
  })
  </script>
  
  <style scoped>
  .data-upload-container {
    padding: 2rem;
    max-height: 100vh;
    overflow-y: auto;
  }
  
  /* ===== HEADER ===== */
  .upload-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .step-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .step-badge {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .step-title {
    font-size: 1.875rem;
    font-weight: 800;
    background: var(--primary-gradient, linear-gradient(135deg, #667eea, #764ba2));
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--primary-color, #667eea);
}

@supports not (background-clip: text) {
    .step-title {
        background: none;
        color: var(--primary-color, #667eea);
    }
}

  .step-description {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
  }
  
  /* ===== MAIN UPLOAD AREA ===== */
  .upload-main {
    margin-bottom: 3rem;
  }
  
  .upload-zone {
    border: 2px dashed rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.02);
    position: relative;
    min-height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .upload-zone:hover {
    border-color: rgba(102, 126, 234, 0.5);
    background: rgba(102, 126, 234, 0.05);
  }
  
  .upload-zone.drag-active {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
    transform: scale(1.02);
  }
  
  .upload-zone.has-file {
    border-color: rgba(16, 185, 129, 0.5);
    background: rgba(16, 185, 129, 0.05);
  }
  
  .upload-zone.uploading {
    cursor: not-allowed;
    border-color: rgba(102, 126, 234, 0.5);
  }
  
  .file-input {
    display: none;
  }
  
  .upload-content {
    width: 100%;
  }
  
  .upload-icon {
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 1.5rem;
  }
  
  .upload-icon svg {
    transition: transform 0.3s ease;
  }
  
  .upload-zone:hover .upload-icon svg {
    transform: scale(1.1);
  }
  
  .upload-text h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .upload-text p {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 2rem;
  }
  
  .upload-formats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
  }
  
  .format-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    min-width: 80px;
  }
  
  .format-icon {
    font-size: 1.5rem;
  }
  
  .format-text {
    font-size: 0.875rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
  }
  
  /* ===== FILE PREVIEW ===== */
  .file-preview {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    width: 100%;
    max-width: 400px;
  }
  
  .file-icon {
    color: #667eea;
    flex-shrink: 0;
  }
  
  .file-details {
    flex: 1;
  }
  
  .file-name {
    font-weight: 600;
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.25rem;
    word-break: break-word;
  }
  
  .file-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
  }
  
  .remove-file-btn {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    padding: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    flex-shrink: 0;
  }
  
  .remove-file-btn:hover {
    background: rgba(239, 68, 68, 0.2);
  }
  
  /* ===== UPLOAD PROGRESS ===== */
  .upload-progress {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .progress-circle {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .progress-ring {
    transform: rotate(-90deg);
    color: rgba(255, 255, 255, 0.2);
  }
  
  .progress-ring-circle {
    transition: stroke-dashoffset 0.3s ease;
    stroke: #667eea;
  }
  
  .progress-text {
    position: absolute;
    font-weight: 700;
    font-size: 1rem;
    color: #667eea;
  }
  
  .progress-message {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
  }
  
  /* ===== UPLOAD ACTIONS ===== */
  .upload-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .action-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .action-btn.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
  }
  
  .action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  }
  
  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
  }
  
  /* ===== SAMPLE DATASETS ===== */
  .sample-datasets {
    margin-bottom: 3rem;
  }
  
  .section-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .section-header h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .section-header p {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .samples-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .sample-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
  }
  
  .sample-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
  }
  
  .sample-card.loading {
    cursor: not-allowed;
    opacity: 0.7;
  }
  
  .sample-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .sample-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .sample-description {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
    margin-bottom: 1rem;
  }
  
  .sample-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    font-size: 0.75rem;
  }
  
  .sample-meta span {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .sample-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .spinner-small {
    width: 24px;
    height: 24px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-left: 2px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  /* ===== UPLOAD TIPS ===== */
  .upload-tips {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .tips-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    color: #10b981;
  }
  
  .tips-header h4 {
    font-size: 1.125rem;
    font-weight: 600;
  }
  
  .tips-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .tip-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .tip-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }
  
  .tip-content h5 {
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .tip-content p {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.4;
  }
  
  /* ===== SUCCESS MODAL ===== */
  .success-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(10px);
  }
  
  .modal-content {
    background: rgba(15, 15, 35, 0.95);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    max-width: 400px;
    width: 90%;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .success-icon {
    color: #10b981;
    margin-bottom: 1rem;
  }
  
  .modal-content h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .modal-content p {
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 1.5rem;
  }
  
  .dataset-summary {
    display: flex;
    justify-content: space-around;
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
  }
  
  .summary-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }
  
  .summary-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
  }
  
  .summary-value {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }
  
  .modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  .modal-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .modal-btn.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
  }
  
  .modal-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  .modal-btn:hover {
    transform: translateY(-1px);
  }
  
  /* ===== ANIMATIONS ===== */
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* ===== RESPONSIVE ===== */
  @media (max-width: 768px) {
    .data-upload-container {
      padding: 1rem;
    }
    
    .upload-zone {
      padding: 2rem 1rem;
      min-height: 280px;
    }
    
    .upload-formats {
      gap: 1rem;
    }
    
    .format-item {
      min-width: 60px;
      padding: 0.75rem;
    }
    
    .upload-actions {
      flex-direction: column;
    }
    
    .samples-grid {
      grid-template-columns: 1fr;
    }
    
    .tips-grid {
      grid-template-columns: 1fr;
    }
    
    .file-preview {
      max-width: none;
    }
    
    .step-indicator {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .step-title {
      font-size: 1.5rem;
    }
  }
  
  @media (max-width: 480px) {
    .upload-zone {
      padding: 1.5rem 1rem;
      min-height: 240px;
    }
    
    .upload-text h3 {
      font-size: 1.25rem;
    }
    
    .format-item {
      min-width: 50px;
      padding: 0.5rem;
    }
    
    .format-text {
      font-size: 0.75rem;
    }
    
    .modal-content {
      padding: 1.5rem;
    }
    
    .dataset-summary {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .summary-item {
      flex-direction: row;
      justify-content: space-between;
    }
  }
  </style>
  