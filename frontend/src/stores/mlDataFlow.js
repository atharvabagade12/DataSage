// stores/mlDataFlow.js
import { defineStore } from 'pinia'

export const useMLDataFlowStore = defineStore('mlDataFlow', {
  state: () => ({
    // Backend Connection
    backendConnected: false,
    backendStatus: null,
    
    // Current Dataset
    currentDataset: null, // dataset_id
    datasetId: '', // Alias for easier access
    dataset: [], // Actual data rows
    fileName: '',
    
    // Dataset Registry (Map of all uploaded datasets)
    registeredDatasets: new Map(),
    
    // Preprocessing State
    preprocessed: false,
    preprocessingSteps: [],
    
    // ML Pipeline State
    targetColumn: null,
    selectedAlgorithm: null,
    trainedModel: null,
    
    // Columns Info
    columns: [],
    
    // Navigation State
    currentStep: 'upload' // upload, preview, target, algorithm, train, results
  }),
  
  getters: {
    // Check if dataset is loaded
    hasDataset: (state) => {
      return state.dataset && state.dataset.length > 0 && state.datasetId
    },
    
    // Get current dataset info
    currentDatasetInfo: (state) => {
      if (!state.currentDataset) return null
      return state.registeredDatasets.get(state.currentDataset)
    },
    
    // Get all datasets
    allDatasets: (state) => {
      return Array.from(state.registeredDatasets.values())
    }
  },
  
  actions: {
    // ===== BACKEND CONNECTION =====
    async checkBackendConnection() {
      try {
        console.log('🔌 Checking backend connection...')
        
        const response = await fetch('http://localhost:8000/api/health', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        
        if (response.ok) {
          this.backendStatus = await response.json()
          this.backendConnected = true
          console.log('✅ Backend connected:', this.backendStatus.message)
          return true
        } else {
          throw new Error(`Backend returned ${response.status}`)
        }
      } catch (error) {
        console.error('❌ Backend connection failed:', error.message)
        this.backendConnected = false
        this.backendStatus = null
        return false
      }
    },
    
    // ===== DATASET MANAGEMENT =====
    
    // Register dataset after upload
    async registerDataset(datasetInfo) {
      try {
        console.log('📝 Registering dataset:', datasetInfo.dataset_id)
        
        const datasetRecord = {
          id: datasetInfo.dataset_id,
          filename: datasetInfo.filename,
          shape: datasetInfo.shape,
          columns: datasetInfo.columns,
          dtypes: datasetInfo.dtypes,
          uploadTime: datasetInfo.upload_time,
          registered: new Date().toISOString(),
          preprocessed: false
        }
        
        this.registeredDatasets.set(datasetInfo.dataset_id, datasetRecord)
        this.currentDataset = datasetInfo.dataset_id
        this.datasetId = datasetInfo.dataset_id // Set alias
        
        console.log('✅ Dataset registered successfully')
        console.log('   ID:', datasetInfo.dataset_id)
        console.log('   File:', datasetInfo.filename)
        console.log('   Shape:', datasetInfo.shape)
        
      } catch (error) {
        console.error('❌ Failed to register dataset:', error)
      }
    },
    
    // Set dataset data (from upload response)
    setDataset(data, fileName, datasetId) {
      console.log('📊 Setting dataset in store...')
      
      this.dataset = data
      this.fileName = fileName
      this.datasetId = datasetId
      this.currentDataset = datasetId
      
      // Extract columns from data
      if (data && data.length > 0) {
        this.columns = Object.keys(data[0]).map(colName => ({
          name: colName,
          type: this.detectColumnType(data.map(row => row[colName]))
        }))
      }
      
      console.log('✅ Dataset set in store:', {
        rows: data.length,
        columns: this.columns.length,
        fileName,
        datasetId
      })
    },
    
    // Update dataset after preprocessing
    updateDataset(newData) {
      console.log('🔄 Updating dataset after preprocessing...')
      
      this.dataset = newData
      this.preprocessed = true
      
      // Update columns
      if (newData && newData.length > 0) {
        this.columns = Object.keys(newData[0]).map(colName => ({
          name: colName,
          type: this.detectColumnType(newData.map(row => row[colName]))
        }))
      }
      
      // Update registered dataset
      if (this.currentDataset && this.registeredDatasets.has(this.currentDataset)) {
        const dataset = this.registeredDatasets.get(this.currentDataset)
        dataset.preprocessed = true
        dataset.shape = [newData.length, this.columns.length]
      }
      
      console.log('✅ Dataset updated:', {
        rows: newData.length,
        columns: this.columns.length,
        preprocessed: true
      })
    },
    
    // Verify dataset exists in backend
    async verifyDatasetInBackend(datasetId = null) {
      if (!this.backendConnected) {
        console.warn('⚠️ Backend not connected')
        return false
      }
      
      const targetId = datasetId || this.currentDataset
      if (!targetId) {
        console.warn('⚠️ No dataset ID to verify')
        return false
      }
      
      try {
        console.log('🔍 Verifying dataset in backend:', targetId)
        
        const response = await fetch(`http://localhost:8000/api/datasets/${targetId}`)
        
        if (response.ok) {
          const data = await response.json()
          console.log('✅ Dataset verified in backend:', data)
          return true
        } else {
          console.warn('⚠️ Dataset not found in backend:', targetId)
          return false
        }
      } catch (error) {
        console.error('❌ Backend verification failed:', error)
        return false
      }
    },
    
    // ===== ML PIPELINE STATE =====
    
    setTargetColumn(columnName) {
      this.targetColumn = columnName
      console.log('🎯 Target column set:', columnName)
    },
    
    setAlgorithm(algorithmName) {
      this.selectedAlgorithm = algorithmName
      console.log('🤖 Algorithm selected:', algorithmName)
    },
    
    setTrainedModel(modelInfo) {
      this.trainedModel = modelInfo
      console.log('✅ Trained model saved:', modelInfo.model_id)
    },
    
    setPreprocessingSteps(steps) {
      this.preprocessingSteps = steps
      this.preprocessed = true
      console.log('🔧 Preprocessing steps recorded:', steps)
    },
    
    // ===== NAVIGATION =====
    
    setCurrentStep(step) {
      this.currentStep = step
      console.log('📍 Current step:', step)
    },
    
    // ===== UTILITIES =====
    
    detectColumnType(values) {
      const nonNull = values.filter(v => v !== null && v !== undefined && v !== '')
      if (nonNull.length === 0) return 'categorical'
      
      const numericCount = nonNull.filter(v => !isNaN(parseFloat(v))).length
      return numericCount / nonNull.length > 0.8 ? 'numerical' : 'categorical'
    },
    
    // Reset store
    reset() {
      this.currentDataset = null
      this.datasetId = ''
      this.dataset = []
      this.fileName = ''
      this.preprocessed = false
      this.preprocessingSteps = []
      this.targetColumn = null
      this.selectedAlgorithm = null
      this.trainedModel = null
      this.columns = []
      this.currentStep = 'upload'
      
      console.log('🔄 Store reset')
    },
    
    // Clear all datasets
    clearAllDatasets() {
      this.registeredDatasets.clear()
      this.reset()
      console.log('🗑️ All datasets cleared')
    }
  },
  
  // Persist to localStorage
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'mlDataFlow',
        storage: localStorage,
        paths: [
          'currentDataset',
          'datasetId',
          'fileName',
          'preprocessed',
          'targetColumn',
          'selectedAlgorithm',
          'currentStep'
        ]
      }
    ]
  }
})
