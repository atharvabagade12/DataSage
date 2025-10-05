<template>
    <div class="algorithm-config-container">
      <!-- Header -->
      <div class="config-header">
        <h2>🧠 Algorithm Configuration</h2>
        <p>Select and configure machine learning algorithms for your {{ problemTypeLabel }} problem</p>
      </div>
  
      <div class="config-content">
        <!-- Algorithm Selection -->
        <div class="algorithm-selection">
          <h3>🎯 Available Algorithms</h3>
          <p>Choose algorithms based on your problem type and data characteristics</p>
          
          <div class="algorithms-grid">
            <div 
              v-for="algorithm in availableAlgorithms" 
              :key="algorithm.id"
              @click="selectAlgorithm(algorithm)"
              class="algorithm-card"
              :class="{ 
                selected: selectedAlgorithm?.id === algorithm.id,
                recommended: algorithm.recommended 
              }"
            >
              <div class="algorithm-header">
                <div class="algorithm-icon">{{ algorithm.icon }}</div>
                <div class="algorithm-info">
                  <h4>{{ algorithm.name }}</h4>
                  <p>{{ algorithm.description }}</p>
                </div>
                <div class="algorithm-metrics">
                  <div class="metric-badge expected-accuracy" :class="getAccuracyClass(algorithm.expectedAccuracy)">
                    {{ algorithm.expectedAccuracy }}%
                  </div>
                  <div v-if="algorithm.recommended" class="recommended-badge">
                    ⭐ Recommended
                  </div>
                </div>
              </div>
  
              <div class="algorithm-details">
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Complexity:</span>
                    <div class="complexity-bar">
                      <div 
                        class="complexity-fill" 
                        :style="{ width: `${algorithm.complexity * 20}%` }"
                      ></div>
                    </div>
                    <span class="detail-value">{{ getComplexityLabel(algorithm.complexity) }}</span>
                  </div>
                  
                  <div class="detail-item">
                    <span class="detail-label">Training Time:</span>
                    <span class="detail-value">{{ algorithm.trainingTime }}</span>
                  </div>
                  
                  <div class="detail-item">
                    <span class="detail-label">Interpretability:</span>
                    <div class="interpretability-dots">
                      <div 
                        v-for="i in 5" 
                        :key="i"
                        class="dot"
                        :class="{ filled: i <= algorithm.interpretability }"
                      ></div>
                    </div>
                  </div>
                  
                  <div class="detail-item">
                    <span class="detail-label">Memory Usage:</span>
                    <span class="detail-value">{{ algorithm.memoryUsage }}</span>
                  </div>
                </div>
  
                <div class="pros-cons">
                  <div class="pros">
                    <h6>✅ Strengths</h6>
                    <ul>
                      <li v-for="pro in algorithm.pros" :key="pro">{{ pro }}</li>
                    </ul>
                  </div>
                  <div class="cons">
                    <h6>⚠️ Considerations</h6>
                    <ul>
                      <li v-for="con in algorithm.cons" :key="con">{{ con }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Hyperparameter Configuration -->
        <div v-if="selectedAlgorithm" class="hyperparameter-config">
          <h3>⚙️ Hyperparameter Configuration</h3>
          <p>Fine-tune your {{ selectedAlgorithm.name }} algorithm for optimal performance</p>
  
          <!-- Configuration Mode Toggle -->
          <div class="config-mode-toggle">
            <button 
              @click="configMode = 'simple'"
              :class="['mode-btn', { active: configMode === 'simple' }]"
            >
              🎯 Simple Mode
            </button>
            <button 
              @click="configMode = 'advanced'"
              :class="['mode-btn', { active: configMode === 'advanced' }]"
            >
              🔧 Advanced Mode
            </button>
            <button 
              @click="configMode = 'auto'"
              :class="['mode-btn', { active: configMode === 'auto' }]"
            >
              🤖 Auto-Tune
            </button>
          </div>
  
          <!-- Simple Mode -->
          <div v-if="configMode === 'simple'" class="simple-config">
            <div class="config-cards">
              <div 
                v-for="param in selectedAlgorithm.simpleParams" 
                :key="param.name"
                class="param-card"
              >
                <div class="param-header">
                  <h5>{{ param.displayName }}</h5>
                  <div class="param-tooltip" :title="param.tooltip">
                    <span class="help-icon">❓</span>
                  </div>
                </div>
                <p class="param-description">{{ param.description }}</p>
                
                <!-- Range Slider -->
                <div v-if="param.type === 'range'" class="param-control">
                  <div class="range-control">
                    <input 
                      v-model.number="hyperparameters[param.name]"
                      type="range" 
                      :min="param.min" 
                      :max="param.max" 
                      :step="param.step"
                      class="param-slider"
                      @input="updateHyperparameter(param.name, $event.target.value)"
                    />
                    <div class="range-labels">
                      <span>{{ param.min }}</span>
                      <span class="current-value">{{ hyperparameters[param.name] }}</span>
                      <span>{{ param.max }}</span>
                    </div>
                  </div>
                  <div class="param-impact" :class="getParamImpact(param.name, hyperparameters[param.name])">
                    {{ getParamImpactText(param.name, hyperparameters[param.name]) }}
                  </div>
                </div>
                
                <!-- Select Dropdown -->
                <div v-if="param.type === 'select'" class="param-control">
                  <select 
                    v-model="hyperparameters[param.name]"
                    @change="updateHyperparameter(param.name, $event.target.value)"
                    class="param-select"
                  >
                    <option v-for="option in param.options" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                  <div class="param-impact" :class="getParamImpact(param.name, hyperparameters[param.name])">
                    {{ getParamImpactText(param.name, hyperparameters[param.name]) }}
                  </div>
                </div>
                
                <!-- Boolean Toggle -->
                <div v-if="param.type === 'boolean'" class="param-control">
                  <div class="toggle-control">
                    <input 
                      v-model="hyperparameters[param.name]"
                      type="checkbox" 
                      :id="`param-${param.name}`"
                      @change="updateHyperparameter(param.name, $event.target.checked)"
                      class="param-toggle"
                    />
                    <label :for="`param-${param.name}`" class="toggle-label">
                      {{ hyperparameters[param.name] ? param.trueLabel : param.falseLabel }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Advanced Mode -->
          <div v-if="configMode === 'advanced'" class="advanced-config">
            <div class="advanced-grid">
              <div 
                v-for="param in selectedAlgorithm.advancedParams" 
                :key="param.name"
                class="advanced-param"
              >
                <label class="param-label">
                  {{ param.displayName }}
                  <span class="param-tooltip" :title="param.tooltip">❓</span>
                </label>
                
                <input 
                  v-if="param.type === 'number'"
                  v-model.number="hyperparameters[param.name]"
                  type="number" 
                  :min="param.min" 
                  :max="param.max" 
                  :step="param.step"
                  class="param-input"
                  @input="updateHyperparameter(param.name, $event.target.value)"
                />
                
                <select 
                  v-if="param.type === 'select'"
                  v-model="hyperparameters[param.name]"
                  @change="updateHyperparameter(param.name, $event.target.value)"
                  class="param-select"
                >
                  <option v-for="option in param.options" :key="option" :value="option">
                    {{ option }}
                  </option>
                </select>
                
                <div class="param-hint">{{ param.hint }}</div>
              </div>
            </div>
          </div>
  
          <!-- Auto-Tune Mode -->
          <div v-if="configMode === 'auto'" class="auto-tune-config">
            <div class="auto-tune-options">
              <h4>🤖 Automatic Hyperparameter Tuning</h4>
              <p>Let our system find the optimal hyperparameters for your dataset</p>
              
              <div class="tuning-strategy">
                <label>Tuning Strategy:</label>
                <select v-model="autoTuneStrategy" class="strategy-select">
                  <option value="grid_search">Grid Search (Exhaustive)</option>
                  <option value="random_search">Random Search (Efficient)</option>
                  <option value="bayesian">Bayesian Optimization (Smart)</option>
                  <option value="hyperband">Hyperband (Fast)</option>
                </select>
              </div>
              
              <div class="tuning-budget">
                <label>Time Budget:</label>
                <select v-model="tuneBudget" class="budget-select">
                  <option value="5">5 minutes (Quick)</option>
                  <option value="15">15 minutes (Balanced)</option>
                  <option value="30">30 minutes (Thorough)</option>
                  <option value="60">1 hour (Extensive)</option>
                </select>
              </div>
              
              <div class="auto-tune-preview">
                <h5>What will be tuned:</h5>
                <div class="tune-params">
                  <span 
                    v-for="param in selectedAlgorithm.tuneableParams" 
                    :key="param"
                    class="tune-param-tag"
                  >
                    {{ param }}
                  </span>
                </div>
                <div class="tune-estimate">
                  <span class="estimate-label">Expected Performance Improvement:</span>
                  <span class="estimate-value">+{{ getExpectedImprovement() }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Algorithm Comparison -->
        <div v-if="selectedAlgorithms.length > 1" class="algorithm-comparison">
          <h3>⚖️ Algorithm Comparison</h3>
          <p>Compare different algorithms side by side</p>
          
          <div class="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Algorithm</th>
                  <th>Expected Accuracy</th>
                  <th>Training Time</th>
                  <th>Memory Usage</th>
                  <th>Interpretability</th>
                  <th>Complexity</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="algo in selectedAlgorithms" :key="algo.id">
                  <td class="algo-name">
                    <span class="algo-icon">{{ algo.icon }}</span>
                    {{ algo.name }}
                  </td>
                  <td class="accuracy-cell">
                    <div class="accuracy-bar">
                      <div 
                        class="accuracy-fill"
                        :style="{ width: `${algo.expectedAccuracy}%` }"
                      ></div>
                    </div>
                    <span>{{ algo.expectedAccuracy }}%</span>
                  </td>
                  <td>{{ algo.trainingTime }}</td>
                  <td>{{ algo.memoryUsage }}</td>
                  <td>
                    <div class="interpretability-dots">
                      <div 
                        v-for="i in 5" 
                        :key="i"
                        class="dot"
                        :class="{ filled: i <= algo.interpretability }"
                      ></div>
                    </div>
                  </td>
                  <td>{{ getComplexityLabel(algo.complexity) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
  
        <!-- Validation Strategy -->
        <div class="validation-strategy">
          <h3>✅ Model Validation Strategy</h3>
          <p>Configure how your model will be trained and validated</p>
          
          <div class="validation-options">
            <div class="validation-method">
              <h4>Validation Method</h4>
              <div class="method-cards">
                <div 
                  v-for="method in validationMethods" 
                  :key="method.id"
                  @click="selectedValidation = method"
                  class="method-card"
                  :class="{ selected: selectedValidation?.id === method.id }"
                >
                  <div class="method-header">
                    <span class="method-icon">{{ method.icon }}</span>
                    <h5>{{ method.name }}</h5>
                  </div>
                  <p>{{ method.description }}</p>
                  <div class="method-pros">
                    <strong>Best for:</strong> {{ method.bestFor }}
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="selectedValidation" class="validation-params">
              <h4>{{ selectedValidation.name }} Configuration</h4>
              <div class="validation-controls">
                <div v-if="selectedValidation.id === 'cross_validation'" class="cv-config">
                  <label>Number of Folds:</label>
                  <select v-model.number="validationConfig.cv_folds">
                    <option value="3">3-Fold (Fast)</option>
                    <option value="5">5-Fold (Balanced)</option>
                    <option value="10">10-Fold (Thorough)</option>
                  </select>
                </div>
                
                <div v-if="selectedValidation.id === 'train_test_split'" class="split-config">
                  <label>Test Set Size:</label>
                  <input 
                    v-model.number="validationConfig.test_size" 
                    type="range" 
                    min="10" 
                    max="40" 
                    step="5"
                  />
                  <span>{{ validationConfig.test_size }}%</span>
                </div>
                
                <div class="random-seed">
                  <label>Random Seed (for reproducibility):</label>
                  <input v-model.number="validationConfig.random_seed" type="number" min="0" max="9999" />
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Configuration Summary -->
        <div class="config-summary">
          <h3>📋 Configuration Summary</h3>
          <div class="summary-cards">
            <div class="summary-card">
              <h4>Selected Algorithm</h4>
              <div class="summary-content">
                <span class="algo-icon">{{ selectedAlgorithm?.icon }}</span>
                <div class="algo-details">
                  <strong>{{ selectedAlgorithm?.name }}</strong>
                  <p>Expected Accuracy: {{ selectedAlgorithm?.expectedAccuracy }}%</p>
                </div>
              </div>
            </div>
            
            <div class="summary-card">
              <h4>Configuration Mode</h4>
              <div class="summary-content">
                <span class="mode-icon">{{ getModeIcon(configMode) }}</span>
                <div class="mode-details">
                  <strong>{{ getModeLabel(configMode) }}</strong>
                  <p>{{ getModeDescription(configMode) }}</p>
                </div>
              </div>
            </div>
            
            <div class="summary-card">
              <h4>Validation Strategy</h4>
              <div class="summary-content">
                <span class="validation-icon">{{ selectedValidation?.icon }}</span>
                <div class="validation-details">
                  <strong>{{ selectedValidation?.name }}</strong>
                  <p>{{ getValidationSummary() }}</p>
                </div>
              </div>
            </div>
            
            <div class="summary-card">
              <h4>Training Estimate</h4>
              <div class="summary-content">
                <span class="time-icon">⏱️</span>
                <div class="time-details">
                  <strong>{{ getTrainingTimeEstimate() }}</strong>
                  <p>Memory: {{ selectedAlgorithm?.memoryUsage }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="config-actions">
          <button 
            @click="resetToDefaults" 
            class="action-btn secondary"
            :disabled="!selectedAlgorithm"
          >
            🔄 Reset to Defaults
          </button>
          
          <button 
            @click="compareAlgorithms" 
            class="action-btn secondary"
            :disabled="selectedAlgorithms.length < 2"
          >
            ⚖️ Compare Selected
          </button>
          
          <button 
            @click="previewTraining" 
            class="action-btn secondary"
            :disabled="!selectedAlgorithm"
          >
            👁️ Preview Training
          </button>
          
          <button 
            @click="confirmConfiguration" 
            class="action-btn primary"
            :disabled="!selectedAlgorithm || !selectedValidation"
          >
            🚀 Start Training
          </button>
        </div>
      </div>
  
      <!-- Training Preview Modal -->
      <div v-if="showPreview" class="preview-modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>🔍 Training Preview</h3>
            <button @click="showPreview = false" class="close-btn">×</button>
          </div>
          
          <div class="preview-details">
            <div class="preview-section">
              <h4>Configuration Details</h4>
              <div class="config-details">
                <pre>{{ JSON.stringify({ 
                  algorithm: selectedAlgorithm?.name,
                  hyperparameters: hyperparameters,
                  validation: selectedValidation?.name,
                  validationConfig: validationConfig
                }, null, 2) }}</pre>
              </div>
            </div>
            
            <div class="preview-section">
              <h4>Expected Outcomes</h4>
              <div class="outcomes-grid">
                <div class="outcome-item">
                  <span class="outcome-label">Accuracy:</span>
                  <span class="outcome-value">{{ selectedAlgorithm?.expectedAccuracy }}%</span>
                </div>
                <div class="outcome-item">
                  <span class="outcome-label">Training Time:</span>
                  <span class="outcome-value">{{ getTrainingTimeEstimate() }}</span>
                </div>
                <div class="outcome-item">
                  <span class="outcome-label">Model Size:</span>
                  <span class="outcome-value">{{ selectedAlgorithm?.memoryUsage }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="showPreview = false" class="modal-btn secondary">
              Cancel
            </button>
            <button @click="confirmFromPreview" class="modal-btn primary">
              Looks Good - Start Training
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, reactive, onMounted, watch } from 'vue'
  
  // Props
  const props = defineProps({
    pipelineState: {
      type: Object,
      required: true
    }
  })
  
  // Emits
  const emit = defineEmits(['update:state', 'next-step'])
  
  // State
  const selectedAlgorithm = ref(null)
  const selectedAlgorithms = ref([])
  const configMode = ref('simple')
  const autoTuneStrategy = ref('bayesian')
  const tuneBudget = ref('15')
  const selectedValidation = ref(null)
  const showPreview = ref(false)
  
  // Configuration
  const hyperparameters = reactive({})
  const validationConfig = reactive({
    cv_folds: 5,
    test_size: 20,
    random_seed: 42
  })
  
  // Data
  const availableAlgorithms = ref([])
  const validationMethods = ref([
    {
      id: 'cross_validation',
      name: 'Cross Validation',
      icon: '🔄',
      description: 'Split data into k-folds for robust validation',
      bestFor: 'Small to medium datasets, robust evaluation'
    },
    {
      id: 'train_test_split',
      name: 'Train-Test Split',
      icon: '✂️',
      description: 'Simple split into training and testing sets',
      bestFor: 'Large datasets, faster training'
    },
    {
      id: 'stratified_split',
      name: 'Stratified Split',
      icon: '📊',
      description: 'Maintains class distribution in splits',
      bestFor: 'Imbalanced datasets, classification problems'
    }
  ])
  
  // Computed
  const problemType = computed(() => props.pipelineState.problemType)
  const targetColumn = computed(() => props.pipelineState.targetColumn)
  
  const problemTypeLabel = computed(() => {
    const typeMap = {
      'classification': 'Classification',
      'regression': 'Regression',
      'binary_classification': 'Binary Classification',
      'time_series': 'Time Series'
    }
    return typeMap[problemType.value] || 'Machine Learning'
  })
  
  // Methods
  const getAccuracyClass = (accuracy) => {
    if (accuracy >= 90) return 'excellent'
    if (accuracy >= 80) return 'good'
    if (accuracy >= 70) return 'fair'
    return 'poor'
  }
  
  const getComplexityLabel = (complexity) => {
    const labels = ['Very Simple', 'Simple', 'Medium', 'Complex', 'Very Complex']
    return labels[complexity - 1] || 'Medium'
  }
  
  const selectAlgorithm = (algorithm) => {
    selectedAlgorithm.value = algorithm
    
    // Add to selected algorithms if not already there
    if (!selectedAlgorithms.value.find(a => a.id === algorithm.id)) {
      selectedAlgorithms.value.push(algorithm)
    }
    
    // Initialize hyperparameters with defaults
    initializeHyperparameters(algorithm)
    
    console.log('Selected algorithm:', algorithm.name)
  }
  
  const initializeHyperparameters = (algorithm) => {
    // Clear existing hyperparameters
    Object.keys(hyperparameters).forEach(key => delete hyperparameters[key])
    
    // Set defaults from algorithm definition
    if (algorithm.defaultParams) {
      Object.assign(hyperparameters, algorithm.defaultParams)
    }
  }
  
  const updateHyperparameter = (name, value) => {
    hyperparameters[name] = value
    console.log(`Updated ${name} to ${value}`)
  }
  
  const getParamImpact = (paramName, value) => {
    // Simplified impact assessment
    const impacts = {
      'learning_rate': value > 0.3 ? 'high' : value > 0.1 ? 'medium' : 'low',
      'n_estimators': value > 200 ? 'high' : value > 100 ? 'medium' : 'low',
      'max_depth': value > 10 ? 'high' : value > 5 ? 'medium' : 'low'
    }
    return impacts[paramName] || 'medium'
  }
  
  const getParamImpactText = (paramName, value) => {
    const texts = {
      'learning_rate': {
        high: 'Fast learning, may overfit',
        medium: 'Balanced learning rate',
        low: 'Slow but stable learning'
      },
      'n_estimators': {
        high: 'More trees, better accuracy',
        medium: 'Good balance',
        low: 'Fewer trees, faster training'
      },
      'max_depth': {
        high: 'Deep trees, may overfit',
        medium: 'Balanced depth',
        low: 'Shallow trees, prevents overfitting'
      }
    }
    const impact = getParamImpact(paramName, value)
    return texts[paramName]?.[impact] || 'Parameter configured'
  }
  
  const getModeIcon = (mode) => {
    const icons = {
      simple: '🎯',
      advanced: '🔧',
      auto: '🤖'
    }
    return icons[mode] || '⚙️'
  }
  
  const getModeLabel = (mode) => {
    const labels = {
      simple: 'Simple Mode',
      advanced: 'Advanced Mode',
      auto: 'Auto-Tune Mode'
    }
    return labels[mode] || 'Configuration Mode'
  }
  
  const getModeDescription = (mode) => {
    const descriptions = {
      simple: 'Easy sliders and dropdowns',
      advanced: 'Full parameter control',
      auto: 'Automatic optimization'
    }
    return descriptions[mode] || 'Parameter configuration'
  }
  
  const getValidationSummary = () => {
    if (!selectedValidation.value) return 'Not configured'
    
    if (selectedValidation.value.id === 'cross_validation') {
      return `${validationConfig.cv_folds}-fold CV`
    } else if (selectedValidation.value.id === 'train_test_split') {
      return `${validationConfig.test_size}% test split`
    }
    return selectedValidation.value.name
  }
  
  const getTrainingTimeEstimate = () => {
    if (!selectedAlgorithm.value) return 'Unknown'
    
    let baseTime = selectedAlgorithm.value.baseTrainingTime || 60 // seconds
    
    // Adjust based on validation method
    if (selectedValidation.value?.id === 'cross_validation') {
      baseTime *= validationConfig.cv_folds
    }
    
    // Adjust based on hyperparameters
    if (hyperparameters.n_estimators) {
      baseTime *= (hyperparameters.n_estimators / 100)
    }
    
    if (baseTime < 60) return `${Math.round(baseTime)}s`
    if (baseTime < 3600) return `${Math.round(baseTime / 60)}m`
    return `${Math.round(baseTime / 3600)}h`
  }
  
  const getExpectedImprovement = () => {
    const strategies = {
      'grid_search': 8,
      'random_search': 6,
      'bayesian': 12,
      'hyperband': 10
    }
    return strategies[autoTuneStrategy.value] || 5
  }
  
  const resetToDefaults = () => {
    if (selectedAlgorithm.value) {
      initializeHyperparameters(selectedAlgorithm.value)
    }
  }
  
  const compareAlgorithms = () => {
    // This would show a detailed comparison
    alert('Algorithm comparison feature activated!')
  }
  
  const previewTraining = () => {
    showPreview.value = true
  }
  
  const confirmConfiguration = () => {
    confirmFromPreview()
  }
  
  const confirmFromPreview = () => {
    showPreview.value = false
    
    // Update pipeline state
    emit('update:state', {
      selectedAlgorithm: selectedAlgorithm.value.id,
      hyperparameters: { ...hyperparameters },
      validationStrategy: selectedValidation.value.id,
      validationConfig: { ...validationConfig },
      configurationMode: configMode.value,
      autoTuneStrategy: configMode.value === 'auto' ? autoTuneStrategy.value : null,
      expectedAccuracy: selectedAlgorithm.value.expectedAccuracy,
      trainingTimeEstimate: getTrainingTimeEstimate()
    })
    
    // Advance to training step
    emit('next-step')
    
    console.log('Algorithm configuration confirmed:', {
      algorithm: selectedAlgorithm.value.name,
      mode: configMode.value,
      validation: selectedValidation.value.name
    })
  }
  
  // Initialize available algorithms based on problem type
  const initializeAlgorithms = () => {
    const algorithmDB = {
      classification: [
        {
          id: 'random_forest_clf',
          name: 'Random Forest',
          icon: '🌳',
          description: 'Ensemble of decision trees with voting',
          expectedAccuracy: 87,
          complexity: 3,
          trainingTime: '2-5 min',
          memoryUsage: 'Medium',
          interpretability: 4,
          recommended: true,
          baseTrainingTime: 180,
          pros: [
            'Handles missing values well',
            'Reduces overfitting',
            'Good feature importance',
            'Works with mixed data types'
          ],
          cons: [
            'Can be slow on large datasets',
            'Less interpretable than single trees',
            'Memory intensive'
          ],
          defaultParams: {
            n_estimators: 100,
            max_depth: 10,
            min_samples_split: 2,
            bootstrap: true
          },
          simpleParams: [
            {
              name: 'n_estimators',
              displayName: 'Number of Trees',
              description: 'More trees usually mean better accuracy but slower training',
              type: 'range',
              min: 50,
              max: 300,
              step: 10,
              tooltip: 'Number of decision trees in the forest'
            },
            {
              name: 'max_depth',
              displayName: 'Tree Depth',
              description: 'Deeper trees can capture more patterns but may overfit',
              type: 'range',
              min: 3,
              max: 20,
              step: 1,
              tooltip: 'Maximum depth of individual trees'
            }
          ],
          advancedParams: [
            {
              name: 'min_samples_split',
              displayName: 'Min Samples Split',
              type: 'number',
              min: 2,
              max: 20,
              step: 1,
              tooltip: 'Minimum samples required to split a node',
              hint: 'Higher values prevent overfitting'
            },
            {
              name: 'min_samples_leaf',
              displayName: 'Min Samples Leaf',
              type: 'number',
              min: 1,
              max: 10,
              step: 1,
              tooltip: 'Minimum samples required at leaf node'
            }
          ],
          tuneableParams: ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf']
        },
        {
          id: 'xgboost_clf',
          name: 'XGBoost',
          icon: '⚡',
          description: 'Gradient boosting with extreme optimization',
          expectedAccuracy: 91,
          complexity: 4,
          trainingTime: '3-8 min',
          memoryUsage: 'High',
          interpretability: 3,
          recommended: true,
          baseTrainingTime: 240,
          pros: [
            'State-of-the-art accuracy',
            'Handles missing values',
            'Built-in regularization',
            'Fast training with GPU'
          ],
          cons: [
            'Many hyperparameters',
            'Can easily overfit',
            'Requires careful tuning'
          ],
          defaultParams: {
            learning_rate: 0.1,
            n_estimators: 100,
            max_depth: 6,
            subsample: 0.8
          },
          simpleParams: [
            {
              name: 'learning_rate',
              displayName: 'Learning Rate',
              description: 'How quickly the model learns from mistakes',
              type: 'range',
              min: 0.01,
              max: 0.3,
              step: 0.01,
              tooltip: 'Lower values need more trees but are more stable'
            },
            {
              name: 'n_estimators',
              displayName: 'Number of Boosting Rounds',
              description: 'Number of sequential improvements',
              type: 'range',
              min: 50,
              max: 500,
              step: 25,
              tooltip: 'More rounds can improve accuracy'
            }
          ],
          advancedParams: [
            {
              name: 'max_depth',
              displayName: 'Max Depth',
              type: 'number',
              min: 3,
              max: 15,
              step: 1,
              tooltip: 'Maximum depth of trees'
            },
            {
              name: 'subsample',
              displayName: 'Subsample',
              type: 'number',
              min: 0.5,
              max: 1.0,
              step: 0.1,
              tooltip: 'Fraction of samples used for training each tree'
            }
          ],
          tuneableParams: ['learning_rate', 'n_estimators', 'max_depth', 'subsample', 'colsample_bytree']
        },
        {
          id: 'logistic_regression',
          name: 'Logistic Regression',
          icon: '📈',
          description: 'Linear model for binary and multiclass classification',
          expectedAccuracy: 78,
          complexity: 1,
          trainingTime: '30s-2min',
          memoryUsage: 'Low',
          interpretability: 5,
          recommended: false,
          baseTrainingTime: 60,
          pros: [
            'Fast training and prediction',
            'Highly interpretable',
            'No hyperparameter tuning needed',
            'Probabilistic output'
          ],
          cons: [
            'Assumes linear relationships',
            'Sensitive to outliers',
            'May underfit complex data'
          ],
          defaultParams: {
            C: 1.0,
            max_iter: 1000,
            solver: 'liblinear'
          },
          simpleParams: [
            {
              name: 'C',
              displayName: 'Regularization Strength',
              description: 'Higher values allow more complex models',
              type: 'range',
              min: 0.1,
              max: 10.0,
              step: 0.1,
              tooltip: 'Lower values = more regularization'
            }
          ],
          advancedParams: [
            {
              name: 'solver',
              displayName: 'Solver',
              type: 'select',
              options: ['liblinear', 'lbfgs', 'newton-cg', 'sag', 'saga'],
              tooltip: 'Algorithm for optimization'
            }
          ],
          tuneableParams: ['C', 'solver']
        }
      ],
      regression: [
        {
          id: 'random_forest_reg',
          name: 'Random Forest',
          icon: '🌳',
          description: 'Ensemble of decision trees for regression',
          expectedAccuracy: 85,
          complexity: 3,
          trainingTime: '2-5 min',
          memoryUsage: 'Medium',
          interpretability: 4,
          recommended: true,
          baseTrainingTime: 180,
          pros: [
            'Handles non-linear relationships',
            'Robust to outliers',
            'Feature importance available',
            'Handles missing values'
          ],
          cons: [
            'Can overfit with small datasets',
            'Less interpretable than linear models',
            'Memory intensive'
          ],
          defaultParams: {
            n_estimators: 100,
            max_depth: 15,
            min_samples_split: 5
          },
          simpleParams: [
            {
              name: 'n_estimators',
              displayName: 'Number of Trees',
              description: 'More trees usually mean better accuracy',
              type: 'range',
              min: 50,
              max: 300,
              step: 10,
              tooltip: 'Number of decision trees in the forest'
            }
          ],
          advancedParams: [
            {
              name: 'max_depth',
              displayName: 'Max Depth',
              type: 'number',
              min: 5,
              max: 25,
              step: 1,
              tooltip: 'Maximum depth of trees'
            }
          ],
          tuneableParams: ['n_estimators', 'max_depth', 'min_samples_split']
        },
        {
          id: 'linear_regression',
          name: 'Linear Regression',
          icon: '📏',
          description: 'Simple linear relationship modeling',
          expectedAccuracy: 72,
          complexity: 1,
          trainingTime: '10-30s',
          memoryUsage: 'Very Low',
          interpretability: 5,
          recommended: false,
          baseTrainingTime: 20,
          pros: [
            'Extremely fast',
            'Highly interpretable',
            'No hyperparameters',
            'Good baseline model'
          ],
          cons: [
            'Assumes linear relationships',
            'Sensitive to outliers',
            'Limited complexity'
          ],
          defaultParams: {},
          simpleParams: [],
          advancedParams: [],
          tuneableParams: []
        }
      ]
    }
  
    // Get algorithms for current problem type
    const algorithms = algorithmDB[problemType.value] || algorithmDB.classification
    availableAlgorithms.value = algorithms
  
    // Auto-select recommended algorithm
    const recommended = algorithms.find(a => a.recommended)
    if (recommended) {
      selectAlgorithm(recommended)
    }
  
    // Set default validation method
    selectedValidation.value = validationMethods.value[0]
  }
  
  // Watchers
  watch(() => props.pipelineState.problemType, (newType) => {
    if (newType) {
      initializeAlgorithms()
    }
  }, { immediate: true })
  
  // Lifecycle
  onMounted(() => {
    initializeAlgorithms()
    
    // Restore previous configuration if available
    if (props.pipelineState.selectedAlgorithm) {
      const savedAlgo = availableAlgorithms.value.find(a => a.id === props.pipelineState.selectedAlgorithm)
      if (savedAlgo) {
        selectAlgorithm(savedAlgo)
        
        if (props.pipelineState.hyperparameters) {
          Object.assign(hyperparameters, props.pipelineState.hyperparameters)
        }
      }
    }
  })
  </script>
  
  <style scoped>
  /* Use the same CSS variables and design patterns */
  .algorithm-config-container {
    padding: 2rem;
    height: 100%;
    overflow-y: auto;
    background: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .config-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .config-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: var(--primary-gradient);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--primary-color);
}

  
  .config-header p {
    color: var(--text-secondary);
    font-size: 1rem;
  }
  
  .algorithm-selection {
    margin-bottom: 3rem;
  }
  
  .algorithm-selection h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .algorithm-selection p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  .algorithms-grid {
    display: grid;
    gap: 1.5rem;
  }
  
  .algorithm-card {
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .algorithm-card:hover {
    border-color: var(--border-medium);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .algorithm-card.selected {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
    box-shadow: var(--shadow-glow);
  }
  
  .algorithm-card.recommended {
    border-color: var(--success-color);
  }
  
  .algorithm-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .algorithm-icon {
    font-size: 2rem;
  }
  
  .algorithm-info {
    flex: 1;
  }
  
  .algorithm-info h4 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .algorithm-info p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0;
  }
  
  .algorithm-metrics {
    text-align: center;
  }
  
  .expected-accuracy {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
  }
  
  .expected-accuracy.excellent {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
  }
  
  .expected-accuracy.good {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info-color);
  }
  
  .expected-accuracy.fair {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
  }
  
  .expected-accuracy.poor {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error-color);
  }
  
  .recommended-badge {
    font-size: 0.75rem;
    color: var(--success-color);
    font-weight: 500;
  }
  
  .algorithm-details {
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
  }
  
  .detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: 0.875rem;
  }
  
  .detail-label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .detail-value {
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .complexity-bar {
    height: 6px;
    background: var(--border-light);
    border-radius: 3px;
    overflow: hidden;
    margin: 0.25rem 0;
  }
  
  .complexity-fill {
    height: 100%;
    background: var(--primary-gradient);
    border-radius: 3px;
    transition: width var(--transition-normal);
  }
  
  .interpretability-dots {
    display: flex;
    gap: 0.25rem;
  }
  
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border-light);
    transition: background var(--transition-fast);
  }
  
  .dot.filled {
    background: var(--primary-color);
  }
  
  .pros-cons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 1rem;
  }
  
  .pros,
  .cons {
    font-size: 0.8125rem;
  }
  
  .pros h6,
  .cons h6 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .pros ul,
  .cons ul {
    margin: 0;
    padding-left: 1rem;
    color: var(--text-secondary);
  }
  
  .pros li,
  .cons li {
    margin-bottom: 0.25rem;
  }
  
  .hyperparameter-config {
    margin-bottom: 3rem;
  }
  
  .hyperparameter-config h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .hyperparameter-config p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  .config-mode-toggle {
    display: flex;
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 0.5rem;
    margin-bottom: 2rem;
    border: 1px solid var(--border-light);
  }
  
  .mode-btn {
    flex: 1;
    padding: 0.75rem 1rem;
    background: none;
    border: none;
    color: var(--text-secondary);
    font-weight: 500;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .mode-btn:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
  }
  
  .mode-btn.active {
    background: var(--primary-gradient);
    color: white;
  }
  
  .config-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
  }
  
  .param-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .param-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  
  .param-header h5 {
    color: var(--text-primary);
    margin: 0;
  }
  
  .param-tooltip {
    cursor: help;
  }
  
  .help-icon {
    font-size: 0.875rem;
    color: var(--text-tertiary);
  }
  
  .param-description {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .param-control {
    margin-bottom: 1rem;
  }
  
  .range-control {
    margin-bottom: 0.5rem;
  }
  
  .param-slider {
    width: 100%;
    height: 6px;
    background: var(--border-light);
    border-radius: 3px;
    outline: none;
    margin-bottom: 0.5rem;
  }
  
  .param-slider::-webkit-slider-thumb {
    appearance: none;
    width: 18px;
    height: 18px;
    background: var(--primary-color);
    border-radius: 50%;
    cursor: pointer;
  }
  
  .range-labels {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }
  
  .current-value {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .param-select {
    width: 100%;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .param-impact {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
    border-radius: 12px;
    font-weight: 500;
  }
  
  .param-impact.low {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
  }
  
  .param-impact.medium {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
  }
  
  .param-impact.high {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error-color);
  }
  
  .advanced-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .advanced-param {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    padding: 1rem;
  }
  
  .param-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }
  
  .param-input,
  .param-select {
    width: 100%;
    padding: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .param-hint {
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }
  
  .auto-tune-config {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 2rem;
  }
  
  .auto-tune-options h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .auto-tune-options p {
    color: var(--text-secondary);
    margin-bottom: 2rem;
  }
  
  .tuning-strategy,
  .tuning-budget {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .tuning-strategy label,
  .tuning-budget label {
    color: var(--text-secondary);
    font-weight: 500;
    min-width: 120px;
  }
  
  .strategy-select,
  .budget-select {
    padding: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  .auto-tune-preview {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
  }
  
  .auto-tune-preview h5 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .tune-params {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .tune-param-tag {
    padding: 0.25rem 0.5rem;
    background: rgba(102, 126, 234, 0.1);
    color: var(--primary-color);
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .tune-estimate {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .estimate-label {
    color: var(--text-secondary);
  }
  
  .estimate-value {
    color: var(--success-color);
    font-weight: 700;
    font-size: 1.1rem;
  }
  
  .validation-strategy {
    margin-bottom: 3rem;
  }
  
  .validation-strategy h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .validation-strategy p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  .validation-method h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .method-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .method-card {
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .method-card:hover {
    border-color: var(--border-medium);
  }
  
  .method-card.selected {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
  }
  
  .method-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .method-icon {
    font-size: 1.25rem;
  }
  
  .method-header h5 {
    color: var(--text-primary);
    margin: 0;
  }
  
  .method-card p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .method-pros {
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }
  
  .validation-params {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .validation-params h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .validation-controls {
    display: grid;
    gap: 1rem;
  }
  
  .cv-config,
  .split-config,
  .random-seed {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .cv-config label,
  .split-config label,
  .random-seed label {
    color: var(--text-secondary);
    font-weight: 500;
    min-width: 150px;
  }
  
  .cv-config select,
  .random-seed input {
    padding: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  .split-config input {
    flex: 1;
  }
  
  .config-summary {
    margin-bottom: 3rem;
  }
  
  .config-summary h3 {
    margin-bottom: 1.5rem;
    color: var(--text-primary);
  }
  
  .summary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .summary-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1rem;
  }
  
  .summary-card h4 {
    color: var(--text-primary);
    font-size: 0.875rem;
    margin-bottom: 0.75rem;
  }
  
  .summary-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .algo-icon,
  .mode-icon,
  .validation-icon,
  .time-icon {
    font-size: 1.5rem;
  }
  
  .algo-details strong,
  .mode-details strong,
  .validation-details strong,
  .time-details strong {
    color: var(--text-primary);
    display: block;
    margin-bottom: 0.25rem;
  }
  
  .algo-details p,
  .mode-details p,
  .validation-details p,
  .time-details p {
    color: var(--text-secondary);
    font-size: 0.8125rem;
    margin: 0;
  }
  
  .config-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border-light);
  }
  
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
  
  .action-btn.primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .action-btn.secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    color: var(--text-primary);
  }
  
  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }
  
  .preview-modal {
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
  }
  
  .modal-content {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 2rem;
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .modal-header h3 {
    color: var(--text-primary);
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all var(--transition-fast);
  }
  
  .close-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
  }
  
  .preview-section {
    margin-bottom: 1.5rem;
  }
  
  .preview-section h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .config-details pre {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    padding: 1rem;
    font-size: 0.8125rem;
    color: var(--text-secondary);
    overflow-x: auto;
  }
  
  .outcomes-grid {
    display: grid;
    gap: 0.75rem;
  }
  
  .outcome-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .outcome-label {
    color: var(--text-secondary);
  }
  
  .outcome-value {
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
  }
  
  .modal-btn {
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .modal-btn.primary {
    background: var(--primary-gradient);
    color: white;
    border: none;
  }
  
  .modal-btn.secondary {
    background: none;
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .modal-btn:hover {
    transform: translateY(-1px);
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .algorithm-config-container {
      padding: 1rem;
    }
    
    .algorithms-grid {
      grid-template-columns: 1fr;
    }
    
    .config-cards {
      grid-template-columns: 1fr;
    }
    
    .pros-cons {
      grid-template-columns: 1fr;
    }
    
    .method-cards {
      grid-template-columns: 1fr;
    }
    
    .summary-cards {
      grid-template-columns: 1fr;
    }
    
    .config-actions {
      flex-direction: column;
    }
    
    .action-btn {
      width: 100%;
    }
    
    .config-mode-toggle {
      flex-direction: column;
    }
    
    .tuning-strategy,
    .tuning-budget,
    .cv-config,
    .split-config,
    .random-seed {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  </style>
  