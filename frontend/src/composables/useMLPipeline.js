import { reactive, ref, computed, watch } from 'vue'

// ===== ML PIPELINE STATE MANAGEMENT =====
export const useMLPipeline = () => {
  
  // ===== CORE PIPELINE STATE =====
  const pipelineState = reactive({
    // === Dataset Management ===
    dataset: null,
    datasetInfo: null,
    datasetName: '',
    datasetSize: 0,
    datasetColumns: [],
    datasetShape: { rows: 0, columns: 0 },
    dataTypes: {},
    
    // === Data Quality ===
    missingValues: {},
    duplicateRows: 0,
    outliers: {},
    dataQualityScore: 0,
    
    // === Step Completion Flags ===
    dataPreviewComplete: false,
    preprocessingComplete: false,
    targetSelectionComplete: false,
    algorithmConfigComplete: false,
    modelTrained: false,
    
    // === Preprocessing Configuration ===
    preprocessingConfig: {
      missingValueStrategy: {},
      duplicateHandling: 'remove_all',
      outlierHandling: {},
      categoricalEncoding: {},
      featureScaling: {
        method: null,
        required: false,
        recommended: false,
        applied: false
      }
    },
    
    // === Target Variable & Problem Type ===
    targetColumn: null,
    targetColumnType: null,
    problemType: null, // 'classification' | 'regression'
    features: [],
    trainTestSplit: 0.8,
    randomState: 42,
    
    // === Algorithm Configuration ===
    selectedAlgorithm: null,
    algorithmCategory: null, // 'classification' | 'regression'
    availableAlgorithms: {},
    hyperparameters: {},
    crossValidation: {
      enabled: true,
      folds: 5,
      scoring: null
    },
    
    // === Model Training ===
    modelTrainingStatus: 'idle', // 'idle' | 'training' | 'completed' | 'failed'
    trainingProgress: 0,
    trainingLogs: [],
    trainedModel: null,
    modelMetadata: {},
    
    // === Model Performance ===
    modelResults: {
      metrics: {},
      confusionMatrix: null,
      featureImportance: [],
      rocCurve: null,
      predictions: [],
      actualVsPredicted: []
    },
    
    // === Processing States ===
    isProcessing: false,
    processingMessage: '',
    processingSubtext: '',
    processingProgress: 0,
    currentOperation: null,
    
    // === Error Handling ===
    errors: [],
    warnings: [],
    
    // === Session Management ===
    sessionId: null,
    lastSaved: null,
    autoSaveEnabled: true
  })
  
  // ===== ALGORITHM CONFIGURATIONS =====
  const algorithmConfigs = reactive({
    classification: {
      'Random Forest': {
        name: 'Random Forest',
        description: 'Ensemble method using multiple decision trees',
        scalingRequired: false,
        scalingRecommended: false,
        parameters: {
          n_estimators: { type: 'slider', min: 10, max: 500, default: 100, step: 10 },
          max_depth: { type: 'slider', min: 1, max: 20, default: 10, step: 1 },
          min_samples_split: { type: 'slider', min: 2, max: 20, default: 2, step: 1 },
          min_samples_leaf: { type: 'slider', min: 1, max: 20, default: 1, step: 1 },
          criterion: { type: 'select', options: ['gini', 'entropy'], default: 'gini' },
          max_features: { type: 'select', options: ['sqrt', 'log2', 'auto'], default: 'sqrt' }
        }
      },
      'Decision Tree': {
        name: 'Decision Tree',
        description: 'Single decision tree for classification',
        scalingRequired: false,
        scalingRecommended: false,
        parameters: {
          max_depth: { type: 'slider', min: 1, max: 20, default: 5, step: 1 },
          criterion: { type: 'select', options: ['gini', 'entropy'], default: 'gini' },
          splitter: { type: 'select', options: ['best', 'random'], default: 'best' },
          min_samples_split: { type: 'slider', min: 2, max: 20, default: 2, step: 1 },
          min_samples_leaf: { type: 'slider', min: 1, max: 20, default: 1, step: 1 }
        }
      },
      'SVM': {
        name: 'Support Vector Machine',
        description: 'Powerful classifier using support vectors',
        scalingRequired: true,
        scalingRecommended: true,
        parameters: {
          C: { type: 'slider', min: 0.01, max: 10.0, default: 1.0, step: 0.01 },
          kernel: { type: 'select', options: ['linear', 'poly', 'rbf', 'sigmoid'], default: 'rbf' },
          gamma: { type: 'select', options: ['scale', 'auto'], default: 'scale' },
          degree: { type: 'slider', min: 1, max: 10, default: 3, step: 1 } // Only for poly kernel
        }
      },
      'Logistic Regression': {
        name: 'Logistic Regression',
        description: 'Linear model for binary and multiclass classification',
        scalingRequired: false,
        scalingRecommended: true,
        parameters: {
          C: { type: 'slider', min: 0.01, max: 10.0, default: 1.0, step: 0.01 },
          penalty: { type: 'select', options: ['l1', 'l2', 'elasticnet'], default: 'l2' },
          solver: { type: 'select', options: ['lbfgs', 'liblinear', 'saga'], default: 'lbfgs' },
          max_iter: { type: 'slider', min: 100, max: 1000, default: 100, step: 50 }
        }
      },
      'K-Nearest Neighbors': {
        name: 'K-Nearest Neighbors',
        description: 'Instance-based learning algorithm',
        scalingRequired: true,
        scalingRecommended: true,
        parameters: {
          n_neighbors: { type: 'slider', min: 3, max: 20, default: 5, step: 1 },
          weights: { type: 'select', options: ['uniform', 'distance'], default: 'uniform' },
          algorithm: { type: 'select', options: ['auto', 'ball_tree', 'kd_tree', 'brute'], default: 'auto' },
          metric: { type: 'select', options: ['euclidean', 'manhattan', 'chebyshev'], default: 'euclidean' }
        }
      },
      'Naive Bayes': {
        name: 'Naive Bayes',
        description: 'Probabilistic classifier based on Bayes theorem',
        scalingRequired: false,
        scalingRecommended: false,
        parameters: {
          alpha: { type: 'slider', min: 0.1, max: 2.0, default: 1.0, step: 0.1 },
          fit_prior: { type: 'boolean', default: true }
        }
      }
    },
    
    regression: {
      'Linear Regression': {
        name: 'Linear Regression',
        description: 'Simple linear relationship modeling',
        scalingRequired: false,
        scalingRecommended: true,
        parameters: {
          fit_intercept: { type: 'boolean', default: true },
          normalize: { type: 'boolean', default: false }
        }
      },
      'Random Forest': {
        name: 'Random Forest Regressor',
        description: 'Ensemble method for regression',
        scalingRequired: false,
        scalingRecommended: false,
        parameters: {
          n_estimators: { type: 'slider', min: 10, max: 500, default: 100, step: 10 },
          max_depth: { type: 'slider', min: 1, max: 20, default: 10, step: 1 },
          min_samples_split: { type: 'slider', min: 2, max: 20, default: 2, step: 1 },
          min_samples_leaf: { type: 'slider', min: 1, max: 20, default: 1, step: 1 },
          max_features: { type: 'select', options: ['sqrt', 'log2', 'auto'], default: 'auto' }
        }
      },
      'Decision Tree': {
        name: 'Decision Tree Regressor',
        description: 'Single decision tree for regression',
        scalingRequired: false,
        scalingRecommended: false,
        parameters: {
          max_depth: { type: 'slider', min: 1, max: 20, default: 5, step: 1 },
          criterion: { type: 'select', options: ['squared_error', 'friedman_mse', 'absolute_error'], default: 'squared_error' },
          splitter: { type: 'select', options: ['best', 'random'], default: 'best' },
          min_samples_split: { type: 'slider', min: 2, max: 20, default: 2, step: 1 },
          min_samples_leaf: { type: 'slider', min: 1, max: 20, default: 1, step: 1 }
        }
      },
      'SVR': {
        name: 'Support Vector Regression',
        description: 'Support Vector Machine for regression',
        scalingRequired: true,
        scalingRecommended: true,
        parameters: {
          C: { type: 'slider', min: 0.01, max: 10.0, default: 1.0, step: 0.01 },
          kernel: { type: 'select', options: ['linear', 'poly', 'rbf', 'sigmoid'], default: 'rbf' },
          gamma: { type: 'select', options: ['scale', 'auto'], default: 'scale' },
          epsilon: { type: 'slider', min: 0.01, max: 1.0, default: 0.1, step: 0.01 }
        }
      },
      'Ridge Regression': {
        name: 'Ridge Regression',
        description: 'Linear regression with L2 regularization',
        scalingRequired: false,
        scalingRecommended: true,
        parameters: {
          alpha: { type: 'slider', min: 0.1, max: 10.0, default: 1.0, step: 0.1 },
          fit_intercept: { type: 'boolean', default: true },
          normalize: { type: 'boolean', default: false }
        }
      },
      'Lasso Regression': {
        name: 'Lasso Regression',
        description: 'Linear regression with L1 regularization',
        scalingRequired: false,
        scalingRecommended: true,
        parameters: {
          alpha: { type: 'slider', min: 0.1, max: 10.0, default: 1.0, step: 0.1 },
          fit_intercept: { type: 'boolean', default: true },
          normalize: { type: 'boolean', default: false },
          max_iter: { type: 'slider', min: 100, max: 2000, default: 1000, step: 100 }
        }
      }
    }
  })
  
  // ===== COMPUTED PROPERTIES =====
  const availableAlgorithmsForProblem = computed(() => {
    if (!pipelineState.problemType) return {}
    return algorithmConfigs[pipelineState.problemType] || {}
  })
  
  const selectedAlgorithmConfig = computed(() => {
    if (!pipelineState.selectedAlgorithm || !pipelineState.problemType) return null
    return algorithmConfigs[pipelineState.problemType]?.[pipelineState.selectedAlgorithm] || null
  })
  
  const isScalingRequired = computed(() => {
    const config = selectedAlgorithmConfig.value
    return config?.scalingRequired || false
  })
  
  const isScalingRecommended = computed(() => {
    const config = selectedAlgorithmConfig.value
    return config?.scalingRecommended || false
  })
  
  const pipelineProgress = computed(() => {
    let progress = 0
    if (pipelineState.dataset) progress += 15
    if (pipelineState.dataPreviewComplete) progress += 15
    if (pipelineState.preprocessingComplete) progress += 20
    if (pipelineState.targetColumn) progress += 15
    if (pipelineState.selectedAlgorithm) progress += 15
    if (pipelineState.modelTrained) progress += 20
    return Math.min(progress, 100)
  })
  
  const canStartTraining = computed(() => {
    return !!(
      pipelineState.dataset &&
      pipelineState.preprocessingComplete &&
      pipelineState.targetColumn &&
      pipelineState.selectedAlgorithm &&
      pipelineState.hyperparameters &&
      !pipelineState.isProcessing
    )
  })
  
  // ===== STATE MANAGEMENT METHODS =====
  const updateState = (updates) => {
    Object.assign(pipelineState, updates)
    
    // Automatic validations and updates
    if (updates.selectedAlgorithm && pipelineState.problemType) {
      updateScalingRecommendations()
      initializeDefaultHyperparameters()
    }
    
    if (updates.targetColumn) {
      detectProblemType()
    }
    
    // Auto-save if enabled
    if (pipelineState.autoSaveEnabled) {
      debouncedSave()
    }
    
    console.log('📊 Pipeline state updated:', updates)
  }
  
  const resetPipeline = () => {
    // Reset all state except session info
    const sessionId = pipelineState.sessionId
    Object.assign(pipelineState, {
      dataset: null,
      datasetInfo: null,
      datasetName: '',
      datasetSize: 0,
      datasetColumns: [],
      datasetShape: { rows: 0, columns: 0 },
      dataTypes: {},
      missingValues: {},
      duplicateRows: 0,
      outliers: {},
      dataQualityScore: 0,
      dataPreviewComplete: false,
      preprocessingComplete: false,
      targetSelectionComplete: false,
      algorithmConfigComplete: false,
      modelTrained: false,
      preprocessingConfig: {
        missingValueStrategy: {},
        duplicateHandling: 'remove_all',
        outlierHandling: {},
        categoricalEncoding: {},
        featureScaling: {
          method: null,
          required: false,
          recommended: false,
          applied: false
        }
      },
      targetColumn: null,
      targetColumnType: null,
      problemType: null,
      features: [],
      trainTestSplit: 0.8,
      randomState: 42,
      selectedAlgorithm: null,
      algorithmCategory: null,
      availableAlgorithms: {},
      hyperparameters: {},
      crossValidation: {
        enabled: true,
        folds: 5,
        scoring: null
      },
      modelTrainingStatus: 'idle',
      trainingProgress: 0,
      trainingLogs: [],
      trainedModel: null,
      modelMetadata: {},
      modelResults: {
        metrics: {},
        confusionMatrix: null,
        featureImportance: [],
        rocCurve: null,
        predictions: [],
        actualVsPredicted: []
      },
      isProcessing: false,
      processingMessage: '',
      processingSubtext: '',
      processingProgress: 0,
      currentOperation: null,
      errors: [],
      warnings: [],
      sessionId
    })
    
    console.log('🔄 Pipeline reset complete')
  }
  
  // ===== HELPER METHODS =====
  const updateScalingRecommendations = () => {
    const config = selectedAlgorithmConfig.value
    if (config) {
      pipelineState.preprocessingConfig.featureScaling = {
        ...pipelineState.preprocessingConfig.featureScaling,
        required: config.scalingRequired,
        recommended: config.scalingRecommended
      }
    }
  }
  
  const initializeDefaultHyperparameters = () => {
    const config = selectedAlgorithmConfig.value
    if (config && config.parameters) {
      const defaultParams = {}
      Object.entries(config.parameters).forEach(([key, paramConfig]) => {
        defaultParams[key] = paramConfig.default
      })
      pipelineState.hyperparameters = defaultParams
    }
  }
  
  const detectProblemType = async () => {
    if (!pipelineState.targetColumn || !pipelineState.dataset) return
    
    try {
      // This would typically be a backend call
      const response = await $fetch('/api/ml/detect-problem-type', {
        method: 'POST',
        body: {
          sessionId: pipelineState.sessionId,
          targetColumn: pipelineState.targetColumn
        }
      })
      
      pipelineState.problemType = response.problemType
      pipelineState.targetColumnType = response.targetType
      
      console.log('🎯 Problem type detected:', response.problemType)
    } catch (error) {
      console.error('❌ Problem type detection failed:', error)
      addError('Failed to detect problem type automatically')
    }
  }
  
  // ===== PROCESSING METHODS =====
  const startProcessing = (message, subtext = '', operation = null) => {
    pipelineState.isProcessing = true
    pipelineState.processingMessage = message
    pipelineState.processingSubtext = subtext
    pipelineState.processingProgress = 0
    pipelineState.currentOperation = operation
  }
  
  const updateProcessing = (progress, message = null, subtext = null) => {
    pipelineState.processingProgress = Math.min(Math.max(progress, 0), 100)
    if (message) pipelineState.processingMessage = message
    if (subtext) pipelineState.processingSubtext = subtext
  }
  
  const stopProcessing = () => {
    pipelineState.isProcessing = false
    pipelineState.processingMessage = ''
    pipelineState.processingSubtext = ''
    pipelineState.processingProgress = 0
    pipelineState.currentOperation = null
  }
  
  // ===== ERROR HANDLING =====
  const addError = (message, details = null) => {
    pipelineState.errors.push({
      id: Date.now(),
      message,
      details,
      timestamp: new Date().toISOString()
    })
    console.error('❌ Pipeline Error:', message, details)
  }
  
  const addWarning = (message, details = null) => {
    pipelineState.warnings.push({
      id: Date.now(),
      message,
      details,
      timestamp: new Date().toISOString()
    })
    console.warn('⚠️ Pipeline Warning:', message, details)
  }
  
  const clearErrors = () => {
    pipelineState.errors = []
  }
  
  const clearWarnings = () => {
    pipelineState.warnings = []
  }
  
  // ===== PERSISTENCE METHODS =====
  const STORAGE_KEY = 'datasage_pipeline_state'
  
  const saveState = () => {
    try {
      const stateToSave = {
        ...pipelineState,
        lastSaved: new Date().toISOString()
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stateToSave))
      pipelineState.lastSaved = stateToSave.lastSaved
      console.log('💾 Pipeline state saved to localStorage')
    } catch (error) {
      console.error('❌ Failed to save pipeline state:', error)
    }
  }
  
  const loadState = () => {
    try {
      const savedState = localStorage.getItem(STORAGE_KEY)
      if (savedState) {
        const parsedState = JSON.parse(savedState)
        Object.assign(pipelineState, parsedState)
        console.log('📂 Pipeline state loaded from localStorage')
        return true
      }
    } catch (error) {
      console.error('❌ Failed to load pipeline state:', error)
    }
    return false
  }
  
  const clearSavedState = () => {
    try {
      localStorage.removeItem(STORAGE_KEY)
      console.log('🗑️ Saved pipeline state cleared')
    } catch (error) {
      console.error('❌ Failed to clear saved state:', error)
    }
  }
  
  // Debounced save for performance
  let saveTimeout = null
  const debouncedSave = () => {
    if (saveTimeout) clearTimeout(saveTimeout)
    saveTimeout = setTimeout(saveState, 2000) // Save after 2 seconds of inactivity
  }
  
  // ===== API METHODS =====
  const uploadDataset = async (file) => {
    startProcessing('Uploading dataset...', 'Please wait while we process your file')
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('sessionId', pipelineState.sessionId || generateSessionId())
      
      updateProcessing(25, 'Uploading file...')
      
      const response = await $fetch('/api/ml/upload-dataset', {
        method: 'POST',
        body: formData
      })
      
      updateProcessing(75, 'Processing dataset...')
      
      // Update pipeline state with dataset info
      updateState({
        dataset: response.data,
        datasetInfo: response.info,
        datasetName: file.name,
        datasetSize: file.size,
        datasetColumns: response.columns,
        datasetShape: response.shape,
        dataTypes: response.dtypes,
        missingValues: response.missingValues,
        duplicateRows: response.duplicateRows,
        sessionId: response.sessionId
      })
      
      updateProcessing(100, 'Dataset uploaded successfully!')
      
      setTimeout(stopProcessing, 1000)
      
      return response
    } catch (error) {
      stopProcessing()
      addError('Failed to upload dataset', error.message)
      throw error
    }
  }
  
  const preprocessData = async (config) => {
    startProcessing('Preprocessing data...', 'Applying data cleaning and transformations')
    
    try {
      updateProcessing(20, 'Handling missing values...')
      
      const response = await $fetch('/api/ml/preprocess-data', {
        method: 'POST',
        body: {
          sessionId: pipelineState.sessionId,
          config: config
        }
      })
      
      updateProcessing(80, 'Finalizing preprocessing...')
      
      updateState({
        preprocessingComplete: true,
        preprocessingConfig: config,
        dataset: response.processedData,
        datasetInfo: response.info
      })
      
      updateProcessing(100, 'Preprocessing completed!')
      setTimeout(stopProcessing, 1000)
      
      return response
    } catch (error) {
      stopProcessing()
      addError('Preprocessing failed', error.message)
      throw error
    }
  }
  
  const trainModel = async () => {
    if (!canStartTraining.value) {
      addError('Cannot start training - missing required configuration')
      return
    }
    
    startProcessing('Training model...', 'This may take a few minutes depending on your data size')
    pipelineState.modelTrainingStatus = 'training'
    
    try {
      updateProcessing(10, 'Preparing training data...')
      
      const response = await $fetch('/api/ml/train-model', {
        method: 'POST',
        body: {
          sessionId: pipelineState.sessionId,
          algorithm: pipelineState.selectedAlgorithm,
          hyperparameters: pipelineState.hyperparameters,
          targetColumn: pipelineState.targetColumn,
          trainTestSplit: pipelineState.trainTestSplit,
          crossValidation: pipelineState.crossValidation,
          scalingConfig: pipelineState.preprocessingConfig.featureScaling
        }
      })
      
      updateProcessing(90, 'Evaluating model performance...')
      
      updateState({
        modelTrained: true,
        modelTrainingStatus: 'completed',
        trainedModel: response.model,
        modelMetadata: response.metadata,
        modelResults: response.results
      })
      
      updateProcessing(100, 'Model training completed!')
      setTimeout(stopProcessing, 1000)
      
      return response
    } catch (error) {
      stopProcessing()
      pipelineState.modelTrainingStatus = 'failed'
      addError('Model training failed', error.message)
      throw error
    }
  }
  
  // ===== UTILITY METHODS =====
  const generateSessionId = () => {
    return 'ds_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
  }
  
  const getDatasetSummary = () => {
    if (!pipelineState.dataset || !pipelineState.datasetInfo) return null
    
    return {
      name: pipelineState.datasetName,
      shape: pipelineState.datasetShape,
      size: formatFileSize(pipelineState.datasetSize),
      columns: pipelineState.datasetColumns.length,
      missingValues: Object.values(pipelineState.missingValues).reduce((a, b) => a + b, 0),
      duplicates: pipelineState.duplicateRows,
      qualityScore: pipelineState.dataQualityScore
    }
  }
  
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }
  
  // ===== INITIALIZE =====
  const initialize = () => {
    // Generate session ID if not exists
    if (!pipelineState.sessionId) {
      pipelineState.sessionId = generateSessionId()
    }
    
    // Try to load saved state
    loadState()
    
    console.log('🚀 ML Pipeline initialized with session:', pipelineState.sessionId)
  }
  
  // Initialize on first use
  initialize()
  
  // ===== RETURN PUBLIC API =====
  return {
    // State
    pipelineState: readonly(pipelineState),
    algorithmConfigs: readonly(algorithmConfigs),
    
    // Computed
    availableAlgorithmsForProblem,
    selectedAlgorithmConfig,
    isScalingRequired,
    isScalingRecommended,
    pipelineProgress,
    canStartTraining,
    
    // Methods
    updateState,
    resetPipeline,
    
    // Processing
    startProcessing,
    updateProcessing,
    stopProcessing,
    
    // Error Handling
    addError,
    addWarning,
    clearErrors,
    clearWarnings,
    
    // Persistence
    saveState,
    loadState,
    clearSavedState,
    
    // API Methods
    uploadDataset,
    preprocessData,
    trainModel,
    
    // Utilities
    getDatasetSummary,
    generateSessionId,
    initialize
  }
}
