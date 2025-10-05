<template>
    <div class="model-training-container">
      <!-- Header -->
      <div class="training-header">
        <h2>🚀 Model Training</h2>
        <p>{{ getTrainingDescription() }}</p>
      </div>
  
      <div class="training-content">
        <!-- Pre-Training Summary -->
        <div v-if="trainingPhase === 'ready'" class="pre-training-summary">
          <h3>📋 Training Configuration</h3>
          
          <div class="config-overview">
            <div class="overview-cards">
              <div class="overview-card">
                <div class="card-icon">🧠</div>
                <div class="card-content">
                  <h4>Algorithm</h4>
                  <p>{{ algorithmName }}</p>
                  <span class="accuracy-badge">{{ expectedAccuracy }}% expected</span>
                </div>
              </div>
              
              <div class="overview-card">
                <div class="card-icon">📊</div>
                <div class="card-content">
                  <h4>Dataset</h4>
                  <p>{{ datasetRows }} rows, {{ datasetColumns }} features</p>
                  <span class="target-badge">Target: {{ targetColumn }}</span>
                </div>
              </div>
              
              <div class="overview-card">
                <div class="card-icon">⚙️</div>
                <div class="card-content">
                  <h4>Validation</h4>
                  <p>{{ validationStrategy }}</p>
                  <span class="time-badge">Est. {{ trainingTimeEstimate }}</span>
                </div>
              </div>
              
              <div class="overview-card">
                <div class="card-icon">🔧</div>
                <div class="card-content">
                  <h4>Configuration</h4>
                  <p>{{ configurationMode }}</p>
                  <span class="param-badge">{{ hyperparameterCount }} parameters</span>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Hyperparameters Preview -->
          <div class="hyperparams-preview">
            <h4>🎛️ Hyperparameters</h4>
            <div class="params-grid">
              <div 
                v-for="(value, param) in hyperparameters" 
                :key="param"
                class="param-item"
              >
                <span class="param-name">{{ formatParamName(param) }}:</span>
                <span class="param-value">{{ formatParamValue(value) }}</span>
              </div>
            </div>
          </div>
  
          <!-- Action Buttons -->
          <div class="pre-training-actions">
            <button @click="goBack" class="action-btn secondary">
              ← Back to Configuration
            </button>
            <button @click="startTraining" class="action-btn primary">
              🚀 Start Training
            </button>
          </div>
        </div>
  
        <!-- Training Progress -->
        <div v-if="trainingPhase === 'training'" class="training-progress">
          <div class="progress-header">
            <h3>⚡ Training in Progress</h3>
            <div class="training-status" :class="currentStatus.type">
              <span class="status-dot"></span>
              {{ currentStatus.message }}
            </div>
          </div>
  
          <!-- Overall Progress -->
          <div class="overall-progress">
            <div class="progress-info">
              <span class="progress-label">Overall Progress</span>
              <span class="progress-percentage">{{ Math.round(overallProgress) }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${overallProgress}%` }"
              ></div>
            </div>
            <div class="time-info">
              <span>Elapsed: {{ formatTime(elapsedTime) }}</span>
              <span>ETA: {{ formatTime(estimatedRemaining) }}</span>
            </div>
          </div>
  
          <!-- Training Steps -->
          <div class="training-steps">
            <div 
              v-for="(step, index) in trainingSteps" 
              :key="step.id"
              class="training-step"
              :class="{ 
                active: currentStepIndex === index,
                completed: currentStepIndex > index,
                pending: currentStepIndex < index 
              }"
            >
              <div class="step-indicator">
                <div class="step-number">
                  <span v-if="currentStepIndex > index">✓</span>
                  <span v-else-if="currentStepIndex === index">{{ index + 1 }}</span>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="step-progress-bar" v-if="currentStepIndex === index">
                  <div 
                    class="step-progress-fill" 
                    :style="{ width: `${currentStepProgress}%` }"
                  ></div>
                </div>
              </div>
              
              <div class="step-content">
                <h4>{{ step.name }}</h4>
                <p>{{ step.description }}</p>
                <div v-if="currentStepIndex === index && step.details" class="step-details">
                  {{ step.details }}
                </div>
              </div>
              
              <div class="step-timing">
                <div v-if="currentStepIndex > index" class="completed-time">
                  ✓ {{ formatTime(step.duration) }}
                </div>
                <div v-else-if="currentStepIndex === index" class="current-time">
                  {{ formatTime(step.elapsedTime || 0) }} / {{ formatTime(step.estimatedTime) }}
                </div>
                <div v-else class="estimated-time">
                  Est. {{ formatTime(step.estimatedTime) }}
                </div>
              </div>
            </div>
          </div>
  
          <!-- Live Metrics (if available) -->
          <div v-if="liveMetrics.length > 0" class="live-metrics">
            <h4>📈 Live Training Metrics</h4>
            <div class="metrics-grid">
              <div v-for="metric in liveMetrics" :key="metric.name" class="metric-card">
                <h5>{{ metric.name }}</h5>
                <div class="metric-value">{{ metric.value }}</div>
                <div class="metric-trend" :class="metric.trend">
                  {{ getTrendIcon(metric.trend) }} {{ metric.change }}
                </div>
                <div class="mini-chart">
                  <div 
                    v-for="(point, index) in metric.history" 
                    :key="index"
                    class="chart-point"
                    :style="{ 
                      height: `${(point / Math.max(...metric.history)) * 100}%`,
                      left: `${(index / (metric.history.length - 1)) * 100}%` 
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Training Logs -->
          <div class="training-logs">
            <h4>📝 Training Logs</h4>
            <div class="logs-container">
              <div 
                v-for="(log, index) in trainingLogs" 
                :key="index"
                class="log-entry"
                :class="log.type"
              >
                <span class="log-timestamp">{{ formatTimestamp(log.timestamp) }}</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
            </div>
          </div>
  
          <!-- Emergency Actions -->
          <div class="emergency-actions">
            <button @click="pauseTraining" class="action-btn warning" :disabled="isPaused">
              ⏸️ Pause Training
            </button>
            <button @click="resumeTraining" class="action-btn success" :disabled="!isPaused">
              ▶️ Resume Training
            </button>
            <button @click="stopTraining" class="action-btn danger">
              ⏹️ Stop Training
            </button>
          </div>
        </div>
  
        <!-- Training Complete -->
        <div v-if="trainingPhase === 'completed'" class="training-completed">
          <div class="completion-header">
            <div class="completion-icon">🎉</div>
            <h3>Training Completed Successfully!</h3>
            <p>Your {{ algorithmName }} model has been trained and is ready for evaluation.</p>
          </div>
  
          <!-- Training Summary -->
          <div class="training-summary">
            <h4>📊 Training Summary</h4>
            <div class="summary-grid">
              <div class="summary-card">
                <h5>Training Duration</h5>
                <div class="summary-value">{{ formatTime(totalTrainingTime) }}</div>
                <div class="summary-note">{{ getFinalPerformanceNote() }}</div>
              </div>
              
              <div class="summary-card">
                <h5>Final Metrics</h5>
                <div class="summary-metrics">
                  <div v-for="metric in finalMetrics" :key="metric.name" class="final-metric">
                    <span class="metric-name">{{ metric.name }}:</span>
                    <span class="metric-value">{{ metric.value }}</span>
                  </div>
                </div>
              </div>
              
              <div class="summary-card">
                <h5>Model Performance</h5>
                <div class="performance-score" :class="getPerformanceClass(modelPerformance.score)">
                  {{ modelPerformance.score }}%
                </div>
                <div class="performance-rating">{{ modelPerformance.rating }}</div>
              </div>
              
              <div class="summary-card">
                <h5>Model Size</h5>
                <div class="summary-value">{{ modelSize }}</div>
                <div class="summary-note">Ready for deployment</div>
              </div>
            </div>
          </div>
  
          <!-- Model Artifacts -->
          <div class="model-artifacts">
            <h4>📦 Model Artifacts</h4>
            <div class="artifacts-list">
              <div v-for="artifact in modelArtifacts" :key="artifact.name" class="artifact-item">
                <div class="artifact-icon">{{ artifact.icon }}</div>
                <div class="artifact-info">
                  <h5>{{ artifact.name }}</h5>
                  <p>{{ artifact.description }}</p>
                  <div class="artifact-meta">
                    <span class="artifact-size">{{ artifact.size }}</span>
                    <span class="artifact-format">{{ artifact.format }}</span>
                  </div>
                </div>
                <div class="artifact-actions">
                  <button @click="downloadArtifact(artifact)" class="download-btn">
                    📥 Download
                  </button>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Next Steps -->
          <div class="next-steps">
            <h4>🎯 What's Next?</h4>
            <div class="steps-grid">
              <div @click="viewPerformance" class="next-step-card">
                <div class="step-icon">📈</div>
                <h5>View Performance</h5>
                <p>Analyze detailed metrics and visualizations</p>
              </div>
              
              <div @click="testModel" class="next-step-card">
                <div class="step-icon">🧪</div>
                <h5>Test Model</h5>
                <p>Make predictions on new data</p>
              </div>
              
              <div @click="deployModel" class="next-step-card">
                <div class="step-icon">🚀</div>
                <h5>Deploy Model</h5>
                <p>Put your model into production</p>
              </div>
              
              <div @click="improveModel" class="next-step-card">
                <div class="step-icon">⚡</div>
                <h5>Improve Model</h5>
                <p>Try different algorithms or tune parameters</p>
              </div>
            </div>
          </div>
  
          <!-- Continue Button -->
          <div class="completion-actions">
            <button @click="continueToPerformance" class="action-btn primary large">
              📈 View Performance Metrics
            </button>
          </div>
        </div>
  
        <!-- Training Failed -->
        <div v-if="trainingPhase === 'failed'" class="training-failed">
          <div class="failure-header">
            <div class="failure-icon">❌</div>
            <h3>Training Failed</h3>
            <p>{{ failureReason }}</p>
          </div>
  
          <!-- Error Details -->
          <div class="error-details">
            <h4>🔍 Error Details</h4>
            <div class="error-message">{{ errorMessage }}</div>
            <div class="error-suggestions">
              <h5>💡 Suggested Solutions:</h5>
              <ul>
                <li v-for="suggestion in errorSuggestions" :key="suggestion">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
  
          <!-- Retry Options -->
          <div class="retry-options">
            <button @click="retryTraining" class="action-btn primary">
              🔄 Retry Training
            </button>
            <button @click="goBack" class="action-btn secondary">
              ← Modify Configuration
            </button>
            <button @click="resetPipeline" class="action-btn tertiary">
              🔄 Start Over
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
  
  // Props
  const props = defineProps({
    pipelineState: {
      type: Object,
      required: true
    }
  })
  
  // Emits
  const emit = defineEmits(['update:state', 'next-step', 'go-back'])
  
  // State
  const trainingPhase = ref('ready') // 'ready', 'training', 'completed', 'failed'
  const currentStepIndex = ref(0)
  const currentStepProgress = ref(0)
  const overallProgress = ref(0)
  const elapsedTime = ref(0)
  const totalTrainingTime = ref(0)
  const isPaused = ref(false)
  
  // Training intervals
  let trainingInterval = null
  let progressInterval = null
  
  // Data
  const trainingSteps = ref([])
  const trainingLogs = ref([])
  const liveMetrics = ref([])
  const finalMetrics = ref([])
  const modelArtifacts = ref([])
  
  // Status
  const currentStatus = reactive({
    type: 'info',
    message: 'Preparing to train...'
  })
  
  const modelPerformance = reactive({
    score: 0,
    rating: 'Unknown'
  })
  
  const failureReason = ref('')
  const errorMessage = ref('')
  const errorSuggestions = ref([])
  
  // Computed
  const algorithmName = computed(() => {
    const algoMap = {
      'random_forest_clf': 'Random Forest Classifier',
      'xgboost_clf': 'XGBoost Classifier',
      'logistic_regression': 'Logistic Regression',
      'random_forest_reg': 'Random Forest Regressor',
      'linear_regression': 'Linear Regression'
    }
    return algoMap[props.pipelineState.selectedAlgorithm] || 'Machine Learning Model'
  })
  
  const expectedAccuracy = computed(() => {
    return props.pipelineState.expectedAccuracy || 85
  })
  
  const datasetRows = computed(() => {
    return props.pipelineState.datasetInfo?.rows || 0
  })
  
  const datasetColumns = computed(() => {
    return props.pipelineState.datasetInfo?.columns || 0
  })
  
  const targetColumn = computed(() => {
    return props.pipelineState.targetColumn || 'target'
  })
  
  const validationStrategy = computed(() => {
    const strategyMap = {
      'cross_validation': `${props.pipelineState.validationConfig?.cv_folds || 5}-Fold Cross Validation`,
      'train_test_split': `${props.pipelineState.validationConfig?.test_size || 20}% Test Split`,
      'stratified_split': 'Stratified Split'
    }
    return strategyMap[props.pipelineState.validationStrategy] || 'Standard Validation'
  })
  
  const trainingTimeEstimate = computed(() => {
    return props.pipelineState.trainingTimeEstimate || '5 minutes'
  })
  
  const configurationMode = computed(() => {
    const modeMap = {
      'simple': 'Simple Mode',
      'advanced': 'Advanced Mode',
      'auto': 'Auto-Tune Mode'
    }
    return modeMap[props.pipelineState.configurationMode] || 'Standard Mode'
  })
  
  const hyperparameters = computed(() => {
    return props.pipelineState.hyperparameters || {}
  })
  
  const hyperparameterCount = computed(() => {
    return Object.keys(hyperparameters.value).length
  })
  
  const estimatedRemaining = computed(() => {
    if (overallProgress.value === 0) return 0
    const estimated = (elapsedTime.value / overallProgress.value) * (100 - overallProgress.value)
    return Math.max(0, estimated)
  })
  
  const modelSize = computed(() => {
    // Simulate model size calculation
    const baseSize = Math.random() * 50 + 10 // 10-60 MB
    return formatFileSize(baseSize * 1024 * 1024)
  })
  
  // Methods
  const getTrainingDescription = () => {
    if (trainingPhase.value === 'ready') {
      return 'Review your configuration and start training your machine learning model'
    } else if (trainingPhase.value === 'training') {
      return 'Your model is currently being trained. Monitor the progress below.'
    } else if (trainingPhase.value === 'completed') {
      return 'Training completed successfully! Review the results and continue to performance analysis.'
    } else if (trainingPhase.value === 'failed') {
      return 'Training encountered an error. Review the details and try again.'
    }
    return 'Machine learning model training'
  }
  
  const formatParamName = (param) => {
    return param.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }
  
  const formatParamValue = (value) => {
    if (typeof value === 'boolean') return value ? 'Yes' : 'No'
    if (typeof value === 'number') return value.toString()
    return String(value)
  }
  
  const formatTime = (seconds) => {
    if (seconds < 60) return `${Math.round(seconds)}s`
    if (seconds < 3600) return `${Math.round(seconds / 60)}m ${Math.round(seconds % 60)}s`
    return `${Math.round(seconds / 3600)}h ${Math.round((seconds % 3600) / 60)}m`
  }
  
  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString()
  }
  
  const formatFileSize = (bytes) => {
    const sizes = ['B', 'KB', 'MB', 'GB']
    if (bytes === 0) return '0 B'
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
  }
  
  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return '📈'
      case 'down': return '📉'
      default: return '➡️'
    }
  }
  
  const getPerformanceClass = (score) => {
    if (score >= 90) return 'excellent'
    if (score >= 80) return 'good'
    if (score >= 70) return 'fair'
    return 'poor'
  }
  
  const getFinalPerformanceNote = () => {
    const score = modelPerformance.score
    if (score >= 90) return 'Exceptional performance!'
    if (score >= 80) return 'Good performance achieved'
    if (score >= 70) return 'Acceptable performance'
    return 'Consider tuning parameters'
  }
  
  const goBack = () => {
    emit('go-back')
  }
  

  
  const initializeTrainingSteps = () => {
    const steps = [
      {
        id: 'data_preparation',
        name: 'Data Preparation',
        description: 'Loading and preparing dataset for training',
        estimatedTime: 30,
        elapsedTime: 0
      },
      {
        id: 'preprocessing',
        name: 'Data Preprocessing',
        description: 'Applying preprocessing transformations',
        estimatedTime: 45,
        elapsedTime: 0
      },
      {
        id: 'feature_engineering',
        name: 'Feature Engineering',
        description: 'Creating and selecting optimal features',
        estimatedTime: 60,
        elapsedTime: 0
      },
      {
        id: 'model_initialization',
        name: 'Model Initialization',
        description: 'Setting up model with hyperparameters',
        estimatedTime: 15,
        elapsedTime: 0
      },
      {
        id: 'training',
        name: 'Model Training',
        description: 'Training the machine learning model',
        estimatedTime: 180,
        elapsedTime: 0
      },
      {
        id: 'validation',
        name: 'Model Validation',
        description: 'Validating model performance',
        estimatedTime: 60,
        elapsedTime: 0
      },
      {
        id: 'finalization',
        name: 'Model Finalization',
        description: 'Saving model and generating artifacts',
        estimatedTime: 30,
        elapsedTime: 0
      }
    ]
  
    // Adjust based on configuration
    if (props.pipelineState.configurationMode === 'auto') {
      steps.push({
        id: 'hyperparameter_tuning',
        name: 'Hyperparameter Tuning',
        description: 'Automatically optimizing hyperparameters',
        estimatedTime: 300,
        elapsedTime: 0
      })
    }
  
    trainingSteps.value = steps
  }
  
  const simulateTraining = async () => {
    let totalElapsed = 0
    
    for (let stepIndex = 0; stepIndex < trainingSteps.value.length; stepIndex++) {
      currentStepIndex.value = stepIndex
      const step = trainingSteps.value[stepIndex]
      
      // Update status
      currentStatus.type = 'processing'
      currentStatus.message = `${step.name}...`
      
      // Add log entry
      addLog('info', `Starting ${step.name}`)
      
      // Simulate step progress
      await simulateStepProgress(step, stepIndex)
      
      // Mark step as completed
      step.duration = step.elapsedTime
      totalElapsed += step.duration
      
      addLog('success', `${step.name} completed in ${formatTime(step.duration)}`)
      
      // Update overall progress
      overallProgress.value = ((stepIndex + 1) / trainingSteps.value.length) * 100
      
      // Add some live metrics during training step
      if (step.id === 'training') {
        updateLiveMetrics()
      }
    }
    
    // Training completed
    totalTrainingTime.value = totalElapsed
    await completeTraining()
  }
  
  const simulateStepProgress = (step, stepIndex) => {
    return new Promise((resolve) => {
      const stepInterval = setInterval(() => {
        if (isPaused.value) return
        
        step.elapsedTime += 2
        currentStepProgress.value = (step.elapsedTime / step.estimatedTime) * 100
        elapsedTime.value += 2
        
        // Add some randomness to make it realistic
        if (Math.random() < 0.3) {
          step.details = getStepDetails(step.id, step.elapsedTime)
        }
        
        if (step.elapsedTime >= step.estimatedTime) {
          clearInterval(stepInterval)
          currentStepProgress.value = 100
          resolve()
        }
      }, 100) // Update every 100ms for smooth progress
    })
  }
  
  const getStepDetails = (stepId, elapsed) => {
    const details = {
      'data_preparation': [
        'Loading dataset from memory...',
        'Validating data integrity...',
        'Creating data splits...',
        'Preparing feature matrix...'
      ],
      'preprocessing': [
        'Handling missing values...',
        'Encoding categorical variables...',
        'Scaling numerical features...',
        'Removing outliers...'
      ],
      'feature_engineering': [
        'Analyzing feature importance...',
        'Creating interaction features...',
        'Selecting optimal features...',
        'Validating feature quality...'
      ],
      'model_initialization': [
        'Setting up model architecture...',
        'Configuring hyperparameters...',
        'Initializing model weights...'
      ],
      'training': [
        'Epoch 1/50 - Loss: 0.543',
        'Epoch 15/50 - Loss: 0.321',
        'Epoch 30/50 - Loss: 0.198',
        'Epoch 45/50 - Loss: 0.156',
        'Training convergence achieved'
      ],
      'validation': [
        'Cross-validation fold 1/5...',
        'Cross-validation fold 3/5...',
        'Cross-validation fold 5/5...',
        'Computing validation metrics...'
      ],
      'finalization': [
        'Serializing trained model...',
        'Generating model artifacts...',
        'Creating performance report...'
      ]
    }
    
    const stepDetails = details[stepId] || []
    const index = Math.min(Math.floor(elapsed / 10), stepDetails.length - 1)
    return stepDetails[index] || ''
  }
  
  const updateLiveMetrics = () => {
    liveMetrics.value = [
      {
        name: 'Training Loss',
        value: (0.8 - Math.random() * 0.6).toFixed(4),
        change: '-12.3%',
        trend: 'down',
        history: Array(10).fill().map(() => Math.random() * 0.8)
      },
      {
        name: 'Validation Accuracy',
        value: (0.75 + Math.random() * 0.2).toFixed(3),
        change: '+5.2%',
        trend: 'up',
        history: Array(10).fill().map(() => 0.7 + Math.random() * 0.25)
      },
      {
        name: 'Learning Rate',
        value: (0.001 + Math.random() * 0.01).toFixed(4),
        change: '0.0%',
        trend: 'stable',
        history: Array(10).fill().map(() => 0.001 + Math.random() * 0.01)
      }
    ]
  }
  
  const addLog = (type, message) => {
    trainingLogs.value.push({
      timestamp: Date.now(),
      type,
      message
    })
    
    // Keep only last 50 logs
    if (trainingLogs.value.length > 50) {
      trainingLogs.value = trainingLogs.value.slice(-50)
    }
  }
  
  const completeTraining = async () => {
    currentStatus.type = 'success'
    currentStatus.message = 'Training completed successfully!'
    
    // Generate final metrics
    finalMetrics.value = [
      { name: 'Accuracy', value: (85 + Math.random() * 10).toFixed(2) + '%' },
      { name: 'Precision', value: (82 + Math.random() * 12).toFixed(2) + '%' },
      { name: 'Recall', value: (80 + Math.random() * 15).toFixed(2) + '%' },
      { name: 'F1-Score', value: (83 + Math.random() * 10).toFixed(2) + '%' }
    ]
    
    // Set model performance
    modelPerformance.score = 85 + Math.random() * 10
    if (modelPerformance.score >= 90) modelPerformance.rating = 'Excellent'
    else if (modelPerformance.score >= 80) modelPerformance.rating = 'Good'
    else if (modelPerformance.score >= 70) modelPerformance.rating = 'Fair'
    else modelPerformance.rating = 'Needs Improvement'
    
    // Generate model artifacts
    modelArtifacts.value = [
      {
        name: 'Trained Model',
        description: 'Serialized machine learning model ready for deployment',
        size: '15.2 MB',
        format: 'PKL',
        icon: '🧠'
      },
      {
        name: 'Feature Scaler',
        description: 'Preprocessing scaler for input features',
        size: '2.1 KB',
        format: 'PKL',
        icon: '📏'
      },
      {
        name: 'Training Report',
        description: 'Detailed training metrics and performance analysis',
        size: '850 KB',
        format: 'PDF',
        icon: '📄'
      },
      {
        name: 'Model Config',
        description: 'Model configuration and hyperparameters',
        size: '1.2 KB',
        format: 'JSON',
        icon: '⚙️'
      }
    ]
    
    trainingPhase.value = 'completed'
    
    // Update pipeline state
    emit('update:state', {
      modelTrained: true,
      trainingResults: {
        algorithm: props.pipelineState.selectedAlgorithm,
        trainingTime: totalTrainingTime.value,
        finalMetrics: finalMetrics.value,
        modelPerformance: { ...modelPerformance },
        artifacts: modelArtifacts.value
      }
    })
  }
  
  const pauseTraining = () => {
    isPaused.value = true
    currentStatus.type = 'warning'
    currentStatus.message = 'Training paused'
    addLog('warning', 'Training paused by user')
  }
  
  const resumeTraining = () => {
    isPaused.value = false
    currentStatus.type = 'processing'
    currentStatus.message = 'Training resumed'
    addLog('info', 'Training resumed')
  }
  
  const stopTraining = () => {
    if (confirm('Are you sure you want to stop training? This will lose all progress.')) {
      trainingPhase.value = 'failed'
      failureReason.value = 'Training stopped by user'
      errorMessage.value = 'Training was manually stopped before completion.'
      errorSuggestions.value = [
        'Click "Retry Training" to start over',
        'Modify configuration if needed',
        'Ensure sufficient time for training completion'
      ]
    }
  }
  
  const retryTraining = () => {
    // Reset all training state
    trainingPhase.value = 'ready'
    currentStepIndex.value = 0
    currentStepProgress.value = 0
    overallProgress.value = 0
    elapsedTime.value = 0
    totalTrainingTime.value = 0
    isPaused.value = false
    trainingLogs.value = []
    liveMetrics.value = []
    finalMetrics.value = []
    modelArtifacts.value = []
  }
  
  const resetPipeline = () => {
    if (confirm('This will reset the entire pipeline. Are you sure?')) {
      // Emit reset event to parent
      emit('reset-pipeline')
    }
  }
  
  const viewPerformance = () => {
    // Navigate to performance view
    emit('next-step')
  }
  
  const testModel = () => {
    // Navigate to model testing
    console.log('Navigate to model testing')
  }
  
  const deployModel = () => {
    // Navigate to model deployment
    console.log('Navigate to model deployment')
  }
  
  const improveModel = () => {
    // Go back to algorithm configuration
    emit('go-back')
  }
  
  const downloadArtifact = (artifact) => {
    // Simulate artifact download
    console.log(`Downloading ${artifact.name}`)
    // In a real implementation, this would trigger a file download
  }
  
  const continueToPerformance = () => {
    emit('next-step')
  }
  
  // Lifecycle
  onMounted(() => {
    // Start with ready phase
    trainingPhase.value = 'ready'
  })
  
  onUnmounted(() => {
    // Clean up intervals
    if (trainingInterval) clearInterval(trainingInterval)
    if (progressInterval) clearInterval(progressInterval)
  })
  </script>
  
  <style scoped>
  .model-training-container {
    padding: 2rem;
    height: 100%;
    overflow-y: auto;
    background: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .training-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .training-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: var(--primary-gradient);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--primary-color);
}

  
  .training-header p {
    color: var(--text-secondary);
    font-size: 1rem;
  }
  
  /* Pre-Training Summary */
  .pre-training-summary {
    max-width: 1000px;
    margin: 0 auto;
  }
  
  .pre-training-summary h3 {
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    text-align: center;
  }
  
  .overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .overview-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .card-icon {
    font-size: 2rem;
    opacity: 0.8;
  }
  
  .card-content h4 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .card-content p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .accuracy-badge,
  .target-badge,
  .time-badge,
  .param-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .accuracy-badge {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
  }
  
  .target-badge {
    background: rgba(102, 126, 234, 0.1);
    color: var(--primary-color);
  }
  
  .time-badge {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
  }
  
  .param-badge {
    background: rgba(139, 92, 246, 0.1);
    color: #a78bfa;
  }
  
  .hyperparams-preview {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .hyperparams-preview h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .params-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .param-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .param-name {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .param-value {
    color: var(--text-primary);
    font-weight: 600;
    font-family: 'Monaco', 'Consolas', monospace;
  }
  
  .pre-training-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  /* Training Progress */
  .training-progress {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
  }
  
  .progress-header h3 {
    color: var(--text-primary);
  }
  
  .training-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
    font-weight: 500;
  }
  
  .training-status.info {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info-color);
  }
  
  .training-status.processing {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
  }
  
  .training-status.success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
  }
  
  .training-status.warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
  }
  
  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  
  .overall-progress {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .progress-label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .progress-percentage {
    color: var(--text-primary);
    font-weight: 700;
    font-size: 1.25rem;
  }
  
  .progress-bar {
    height: 12px;
    background: var(--border-light);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1rem;
  }
  
  .progress-fill {
    height: 100%;
    background: var(--primary-gradient);
    border-radius: 6px;
    transition: width 0.5s ease;
  }
  
  .time-info {
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .training-steps {
    display: grid;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .training-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    transition: all var(--transition-normal);
  }
  
  .training-step.active {
    border-color: var(--warning-color);
    background: rgba(245, 158, 11, 0.05);
  }
  
  .training-step.completed {
    border-color: var(--success-color);
    background: rgba(16, 185, 129, 0.05);
  }
  
  .training-step.pending {
    opacity: 0.6;
  }
  
  .step-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  
  .training-step.pending .step-number {
    background: var(--bg-secondary);
    color: var(--text-tertiary);
  }
  
  .training-step.active .step-number {
    background: var(--warning-color);
    color: white;
  }
  
  .training-step.completed .step-number {
    background: var(--success-color);
    color: white;
  }
  
  .step-progress-bar {
    width: 40px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    overflow: hidden;
  }
  
  .step-progress-fill {
    height: 100%;
    background: var(--warning-color);
    border-radius: 2px;
    transition: width 0.3s ease;
  }
  
  .step-content {
    flex: 1;
  }
  
  .step-content h4 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .step-content p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .step-details {
    color: var(--text-tertiary);
    font-size: 0.8125rem;
    font-style: italic;
  }
  
  .step-timing {
    text-align: right;
    min-width: 100px;
    font-size: 0.8125rem;
  }
  
  .completed-time {
    color: var(--success-color);
    font-weight: 500;
  }
  
  .current-time {
    color: var(--warning-color);
    font-weight: 500;
  }
  
  .estimated-time {
    color: var(--text-tertiary);
  }
  
  /* Live Metrics */
  .live-metrics {
    margin-bottom: 2rem;
  }
  
  .live-metrics h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    position: relative;
  }
  
  .metric-card h5 {
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }
  
  .metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .metric-trend {
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
  }
  
  .metric-trend.up {
    color: var(--success-color);
  }
  
  .metric-trend.down {
    color: var(--error-color);
  }
  
  .metric-trend.stable {
    color: var(--text-secondary);
  }
  
  .mini-chart {
    height: 30px;
    position: relative;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    overflow: hidden;
  }
  
  .chart-point {
    position: absolute;
    bottom: 0;
    width: 2px;
    background: var(--primary-color);
    transition: all 0.3s ease;
  }
  
  /* Training Logs */
  .training-logs {
    margin-bottom: 2rem;
  }
  
  .training-logs h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .logs-container {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    max-height: 200px;
    overflow-y: auto;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.8125rem;
  }
  
  .log-entry {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.25rem;
    padding: 0.25rem 0;
  }
  
  .log-timestamp {
    color: var(--text-tertiary);
    min-width: 80px;
  }
  
  .log-message {
    flex: 1;
  }
  
  .log-entry.info .log-message {
    color: var(--text-secondary);
  }
  
  .log-entry.success .log-message {
    color: var(--success-color);
  }
  
  .log-entry.warning .log-message {
    color: var(--warning-color);
  }
  
  .log-entry.error .log-message {
    color: var(--error-color);
  }
  
  /* Emergency Actions */
  .emergency-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
  }
  
  /* Training Completed */
  .training-completed {
    max-width: 1000px;
    margin: 0 auto;
    text-align: center;
  }
  
  .completion-header {
    margin-bottom: 3rem;
  }
  
  .completion-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }
  
  .completion-header h3 {
    font-size: 2rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .completion-header p {
    font-size: 1.1rem;
    color: var(--text-secondary);
  }
  
  .training-summary {
    margin-bottom: 3rem;
  }
  
  .training-summary h4 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
  
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .summary-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .summary-card h5 {
    color: var(--text-secondary);
    margin-bottom: 1rem;
    font-size: 0.875rem;
  }
  
  .summary-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .summary-note {
    color: var(--text-tertiary);
    font-size: 0.8125rem;
  }
  
  .summary-metrics {
    display: grid;
    gap: 0.5rem;
  }
  
  .final-metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .metric-name {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  .metric-value {
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .performance-score {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }
  
  .performance-score.excellent {
    color: var(--success-color);
  }
  
  .performance-score.good {
    color: var(--info-color);
  }
  
  .performance-score.fair {
    color: var(--warning-color);
  }
  
  .performance-score.poor {
    color: var(--error-color);
  }
  
  .performance-rating {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  /* Model Artifacts */
  .model-artifacts {
    margin-bottom: 3rem;
    text-align: left;
  }
  
  .model-artifacts h4 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .artifacts-list {
    display: grid;
    gap: 1rem;
  }
  
  .artifact-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
  }
  
  .artifact-icon {
    font-size: 2rem;
  }
  
  .artifact-info {
    flex: 1;
  }
  
  .artifact-info h5 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .artifact-info p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .artifact-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.8125rem;
    color: var(--text-tertiary);
  }
  
  .download-btn {
    padding: 0.5rem 1rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .download-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }
  
  /* Next Steps */
  .next-steps {
    margin-bottom: 3rem;
  }
  
  .next-steps h4 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
  
  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .next-step-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    cursor: pointer;
    transition: all var(--transition-normal);
    text-align: center;
  }
  
  .next-step-card:hover {
    border-color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .step-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }
  
  .next-step-card h5 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .next-step-card p {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  /* Training Failed */
  .training-failed {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
  }
  
  .failure-header {
    margin-bottom: 2rem;
  }
  
  .failure-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }
  
  .failure-header h3 {
    font-size: 1.5rem;
    color: var(--error-color);
    margin-bottom: 0.5rem;
  }
  
  .failure-header p {
    color: var(--text-secondary);
  }
  
  .error-details {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    margin-bottom: 2rem;
    text-align: left;
  }
  
  .error-details h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .error-message {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: var(--error-color);
    padding: 1rem;
    border-radius: var(--radius-sm);
    margin-bottom: 1rem;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.875rem;
  }
  
  .error-suggestions h5 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .error-suggestions ul {
    color: var(--text-secondary);
    padding-left: 1rem;
  }
  
  .error-suggestions li {
    margin-bottom: 0.25rem;
  }
  
  .retry-options {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  /* Action Buttons */
  .action-btn {
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-normal);
    min-width: 160px;
  }
  
  .action-btn.primary {
    background: var(--primary-gradient);
    color: white;
    border: none;
  }
  
  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .action-btn.tertiary {
    background: none;
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .action-btn.warning {
    background: var(--warning-color);
    color: white;
    border: none;
  }
  
  .action-btn.success {
    background: var(--success-color);
    color: white;
    border: none;
  }
  
  .action-btn.danger {
    background: var(--error-color);
    color: white;
    border: none;
  }
  
  .action-btn.large {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    min-width: 250px;
  }
  
  .action-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .model-training-container {
      padding: 1rem;
    }
    
    .overview-cards,
    .params-grid,
    .metrics-grid,
    .summary-grid,
    .steps-grid {
      grid-template-columns: 1fr;
    }
    
    .progress-header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    
    .training-step {
      flex-direction: column;
      text-align: center;
    }
    
    .time-info {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .pre-training-actions,
    .emergency-actions,
    .retry-options {
      flex-direction: column;
    }
    
    .action-btn {
      width: 100%;
    }
    
    .completion-header h3 {
      font-size: 1.5rem;
    }
    
    .completion-icon {
      font-size: 3rem;
    }
  }
  </style>
  