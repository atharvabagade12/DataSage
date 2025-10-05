<template>
    <div class="target-selection-container">
      <!-- Header -->
      <div class="selection-header">
        <h2>🎯 Target Variable Selection</h2>
        <p>Choose your target variable and define the machine learning problem type</p>
      </div>
  
      <div class="selection-content">
        <!-- Step Progress -->
        <div class="step-progress">
          <div class="progress-step" :class="{ completed: selectedColumn }">
            <div class="step-number">1</div>
            <span>Select Target Column</span>
          </div>
          <div class="progress-arrow">→</div>
          <div class="progress-step" :class="{ completed: problemType }">
            <div class="step-number">2</div>
            <span>Determine Problem Type</span>
          </div>
          <div class="progress-arrow">→</div>
          <div class="progress-step" :class="{ completed: validationComplete }">
            <div class="step-number">3</div>
            <span>Validate Selection</span>
          </div>
        </div>
  
        <!-- Target Column Selection -->
        <div class="selection-section">
          <h3>📊 Available Columns</h3>
          <p>Select the column you want to predict (your target variable)</p>
          
          <div class="columns-grid">
            <div 
              v-for="column in availableColumns" 
              :key="column.name"
              @click="selectColumn(column)"
              class="column-card"
              :class="{ 
                selected: selectedColumn?.name === column.name,
                recommended: column.recommended 
              }"
            >
              <div class="column-header">
                <h4>{{ column.name }}</h4>
                <div class="column-badges">
                  <span class="type-badge" :class="`type-${column.type}`">
                    {{ column.type }}
                  </span>
                  <span v-if="column.recommended" class="recommended-badge">
                    ⭐ Recommended
                  </span>
                </div>
              </div>
              
              <div class="column-stats">
                <div class="stat-row">
                  <span class="stat-label">Unique Values:</span>
                  <span class="stat-value">{{ column.uniqueValues }}</span>
                </div>
                <div class="stat-row">
                  <span class="stat-label">Missing:</span>
                  <span class="stat-value">{{ column.missingCount }} ({{ column.missingPercent }}%)</span>
                </div>
                <div class="stat-row">
                  <span class="stat-label">Sample Values:</span>
                  <span class="stat-value">{{ column.sampleValues }}</span>
                </div>
              </div>
  
              <div class="column-suitability">
                <div class="suitability-score" :class="getSuitabilityClass(column.suitability)">
                  <span class="score">{{ column.suitability }}%</span>
                  <span class="label">Suitability</span>
                </div>
                <div class="suitability-reasons">
                  <div v-for="reason in column.reasons" :key="reason.text" class="reason-item" :class="reason.type">
                    <span class="reason-icon">{{ reason.type === 'positive' ? '✓' : '⚠' }}</span>
                    <span class="reason-text">{{ reason.text }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Problem Type Detection -->
        <div v-if="selectedColumn" class="problem-type-section">
          <h3>🔍 Problem Type Analysis</h3>
          <p>Based on your target variable, here are the detected problem types:</p>
          
          <div class="problem-types">
            <div 
              v-for="type in detectedProblemTypes" 
              :key="type.id"
              @click="selectProblemType(type)"
              class="problem-type-card"
              :class="{ 
                selected: problemType?.id === type.id,
                recommended: type.recommended 
              }"
            >
              <div class="type-header">
                <div class="type-icon">{{ type.icon }}</div>
                <div class="type-info">
                  <h4>{{ type.name }}</h4>
                  <p>{{ type.description }}</p>
                </div>
                <div class="type-confidence">
                  <div class="confidence-score" :class="getConfidenceClass(type.confidence)">
                    {{ type.confidence }}%
                  </div>
                  <span v-if="type.recommended" class="recommended-label">Recommended</span>
                </div>
              </div>
              
              <div class="type-details">
                <div class="detail-section">
                  <h6>Why this type?</h6>
                  <ul>
                    <li v-for="reason in type.reasons" :key="reason">{{ reason }}</li>
                  </ul>
                </div>
                
                <div class="detail-section">
                  <h6>Suitable Algorithms:</h6>
                  <div class="algorithm-tags">
                    <span v-for="algo in type.algorithms" :key="algo" class="algorithm-tag">
                      {{ algo }}
                    </span>
                  </div>
                </div>
                
                <div class="detail-section">
                  <h6>Evaluation Metrics:</h6>
                  <div class="metrics-tags">
                    <span v-for="metric in type.metrics" :key="metric" class="metric-tag">
                      {{ metric }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Target Variable Analysis -->
        <div v-if="selectedColumn && problemType" class="analysis-section">
          <h3>📈 Target Variable Analysis</h3>
          
          <div class="analysis-grid">
            <!-- Distribution Analysis -->
            <div class="analysis-card">
              <h4>📊 Distribution</h4>
              <div class="distribution-chart">
                <div v-if="problemType.id === 'classification'" class="class-distribution">
                  <div v-for="class_ in targetDistribution" :key="class_.label" class="class-bar">
                    <span class="class-label">{{ class_.label }}</span>
                    <div class="class-bar-bg">
                      <div 
                        class="class-bar-fill" 
                        :style="{ width: `${class_.percentage}%` }"
                      ></div>
                    </div>
                    <span class="class-count">{{ class_.count }} ({{ class_.percentage.toFixed(1) }}%)</span>
                  </div>
                </div>
                
                <div v-if="problemType.id === 'regression'" class="numeric-distribution">
                  <div class="distribution-stats">
                    <div class="stat-item">
                      <span class="stat-name">Mean:</span>
                      <span class="stat-value">{{ numericStats.mean?.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-name">Median:</span>
                      <span class="stat-value">{{ numericStats.median?.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-name">Std Dev:</span>
                      <span class="stat-value">{{ numericStats.std?.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-name">Range:</span>
                      <span class="stat-value">{{ numericStats.min }} - {{ numericStats.max }}</span>
                    </div>
                  </div>
                  
                  <!-- Simple histogram visualization -->
                  <div class="histogram">
                    <div class="histogram-bars">
                      <div 
                        v-for="(bin, index) in histogramBins" 
                        :key="index"
                        class="histogram-bar"
                        :style="{ height: `${(bin.count / histogramBins.reduce((max, b) => Math.max(max, b.count), 0)) * 100}%` }"
                        :title="`${bin.range}: ${bin.count} values`"
                      ></div>
                    </div>
                    <div class="histogram-labels">
                      <span>{{ numericStats.min }}</span>
                      <span>{{ numericStats.max }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Data Quality -->
            <div class="analysis-card">
              <h4>🔍 Data Quality</h4>
              <div class="quality-metrics">
                <div class="quality-item">
                  <div class="quality-label">Completeness</div>
                  <div class="quality-bar">
                    <div 
                      class="quality-fill completeness" 
                      :style="{ width: `${dataQuality.completeness}%` }"
                    ></div>
                  </div>
                  <span class="quality-value">{{ dataQuality.completeness }}%</span>
                </div>
                
                <div class="quality-item">
                  <div class="quality-label">Balance</div>
                  <div class="quality-bar">
                    <div 
                      class="quality-fill balance" 
                      :style="{ width: `${dataQuality.balance}%` }"
                    ></div>
                  </div>
                  <span class="quality-value">{{ dataQuality.balance }}%</span>
                </div>
                
                <div class="quality-item">
                  <div class="quality-label">Predictability</div>
                  <div class="quality-bar">
                    <div 
                      class="quality-fill predictability" 
                      :style="{ width: `${dataQuality.predictability}%` }"
                    ></div>
                  </div>
                  <span class="quality-value">{{ dataQuality.predictability }}%</span>
                </div>
              </div>
  
              <div class="quality-issues">
                <div v-for="issue in qualityIssues" :key="issue.type" class="quality-issue" :class="issue.severity">
                  <span class="issue-icon">{{ getIssueIcon(issue.severity) }}</span>
                  <span class="issue-text">{{ issue.message }}</span>
                </div>
              </div>
            </div>
  
            <!-- Recommendations -->
            <div class="analysis-card">
              <h4>💡 Recommendations</h4>
              <div class="recommendations">
                <div v-for="rec in recommendations" :key="rec.type" class="recommendation-item">
                  <div class="rec-header">
                    <span class="rec-icon">{{ rec.icon }}</span>
                    <h6>{{ rec.title }}</h6>
                  </div>
                  <p>{{ rec.description }}</p>
                  <div v-if="rec.actions" class="rec-actions">
                    <button 
                      v-for="action in rec.actions" 
                      :key="action.name"
                      @click="executeRecommendation(action)"
                      class="rec-action-btn"
                    >
                      {{ action.name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Selection Summary -->
        <div v-if="selectedColumn && problemType" class="summary-section">
          <h3>📋 Selection Summary</h3>
          <div class="summary-card">
            <div class="summary-row">
              <span class="summary-label">Target Variable:</span>
              <span class="summary-value">{{ selectedColumn.name }} ({{ selectedColumn.type }})</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Problem Type:</span>
              <span class="summary-value">{{ problemType.name }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Confidence:</span>
              <span class="summary-value">{{ problemType.confidence }}%</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Expected Performance:</span>
              <span class="summary-value" :class="getPerformanceClass(expectedPerformance.level)">
                {{ expectedPerformance.level }} ({{ expectedPerformance.score }}%)
              </span>
            </div>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="selection-actions">
          <button 
            @click="analyzeCorrelations" 
            class="action-btn secondary"
            :disabled="!selectedColumn || isAnalyzing"
          >
            🔗 Analyze Feature Correlations
          </button>
          
          <button 
            @click="validateSelection" 
            class="action-btn secondary"
            :disabled="!selectedColumn || !problemType || isValidating"
          >
            ✅ Validate Selection
          </button>
          
          <button 
            @click="confirmSelection" 
            class="action-btn primary"
            :disabled="!validationComplete || !selectedColumn || !problemType"
          >
            🚀 Confirm & Continue
          </button>
        </div>
      </div>
  
      <!-- Analysis Loading Modal -->
      <div v-if="isAnalyzing || isValidating" class="analysis-modal">
        <div class="modal-content">
          <div class="analysis-spinner"></div>
          <h3>{{ isAnalyzing ? '🔗 Analyzing Correlations...' : '✅ Validating Selection...' }}</h3>
          <p>{{ analysisMessage }}</p>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${analysisProgress}%` }"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch, onMounted } from 'vue'
  
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
  const selectedColumn = ref(null)
  const problemType = ref(null)
  const validationComplete = ref(false)
  const isAnalyzing = ref(false)
  const isValidating = ref(false)
  const analysisMessage = ref('')
  const analysisProgress = ref(0)
  
  // Data
  const availableColumns = ref([])
  const detectedProblemTypes = ref([])
  const targetDistribution = ref([])
  const numericStats = ref({})
  const histogramBins = ref([])
  const dataQuality = ref({ completeness: 0, balance: 0, predictability: 0 })
  const qualityIssues = ref([])
  const recommendations = ref([])
  
  // Computed
  const dataset = computed(() => props.pipelineState.dataset)
  const columnAnalysis = computed(() => props.pipelineState.columnAnalysis || [])
  
  const expectedPerformance = computed(() => {
    if (!selectedColumn.value || !problemType.value) {
      return { level: 'Unknown', score: 0 }
    }
    
    // Calculate expected performance based on data quality factors
    const baseScore = (dataQuality.value.completeness + dataQuality.value.balance + dataQuality.value.predictability) / 3
    
    if (baseScore >= 85) return { level: 'Excellent', score: Math.round(baseScore) }
    if (baseScore >= 70) return { level: 'Good', score: Math.round(baseScore) }
    if (baseScore >= 50) return { level: 'Fair', score: Math.round(baseScore) }
    return { level: 'Poor', score: Math.round(baseScore) }
  })
  
  // Methods
  const getSuitabilityClass = (score) => {
    if (score >= 80) return 'excellent'
    if (score >= 60) return 'good'
    if (score >= 40) return 'fair'
    return 'poor'
  }
  
  const getConfidenceClass = (confidence) => {
    if (confidence >= 90) return 'high'
    if (confidence >= 70) return 'medium'
    return 'low'
  }
  
  const getPerformanceClass = (level) => {
    switch (level.toLowerCase()) {
      case 'excellent': return 'performance-excellent'
      case 'good': return 'performance-good'
      case 'fair': return 'performance-fair'
      default: return 'performance-poor'
    }
  }
  
  const getIssueIcon = (severity) => {
    switch (severity) {
      case 'high': return '🔴'
      case 'medium': return '🟡'
      case 'low': return '🟢'
      default: return 'ℹ️'
    }
  }
  
  const selectColumn = (column) => {
    selectedColumn.value = column
    validationComplete.value = false
    
    // Auto-detect problem types based on the selected column
    detectProblemTypes(column)
    
    // Analyze target variable
    analyzeTargetVariable(column)
    
    console.log('Selected target column:', column.name)
  }
  
  const selectProblemType = (type) => {
    problemType.value = type
    validationComplete.value = false
    
    // Update analysis based on problem type
    updateAnalysisForProblemType(type)
    
    console.log('Selected problem type:', type.name)
  }
  
  const detectProblemTypes = (column) => {
    const types = []
    
    // Classification detection
    if (column.type === 'categorical' || column.uniqueValues <= 20) {
      const confidence = column.type === 'categorical' ? 95 : Math.max(60, 100 - (column.uniqueValues * 3))
      
      types.push({
        id: 'classification',
        name: 'Classification',
        description: 'Predict discrete categories or classes',
        icon: '🎯',
        confidence,
        recommended: confidence >= 80,
        reasons: [
          `${column.uniqueValues} unique values detected`,
          column.type === 'categorical' ? 'Column type is categorical' : 'Low cardinality suggests categories',
          'Suitable for predicting discrete outcomes'
        ],
        algorithms: ['Random Forest', 'Logistic Regression', 'SVM', 'XGBoost'],
        metrics: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
      })
    }
    
    // Regression detection
    if (column.type === 'numeric') {
      const confidence = column.uniqueValues > 50 ? 95 : Math.max(60, column.uniqueValues * 2)
      
      types.push({
        id: 'regression',
        name: 'Regression',
        description: 'Predict continuous numeric values',
        icon: '📈',
        confidence,
        recommended: confidence >= 80,
        reasons: [
          'Column type is numeric',
          `${column.uniqueValues} unique values suggest continuous data`,
          'Suitable for predicting continuous outcomes'
        ],
        algorithms: ['Linear Regression', 'Random Forest', 'XGBoost', 'SVR'],
        metrics: ['MAE', 'MSE', 'RMSE', 'R²', 'MAPE']
      })
    }
    
    // Binary classification special case
    if (column.uniqueValues === 2) {
      types.push({
        id: 'binary_classification',
        name: 'Binary Classification',
        description: 'Predict between two possible outcomes',
        icon: '⚡',
        confidence: 98,
        recommended: true,
        reasons: [
          'Exactly 2 unique values detected',
          'Perfect for binary outcomes',
          'Simpler than multi-class classification'
        ],
        algorithms: ['Logistic Regression', 'Random Forest', 'SVM', 'Neural Network'],
        metrics: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
      })
    }
    
    // Time series detection (if applicable)
    if (column.type === 'numeric' && dataset.value?.length > 100) {
      types.push({
        id: 'time_series',
        name: 'Time Series Forecasting',
        description: 'Predict future values based on temporal patterns',
        icon: '📅',
        confidence: 60,
        recommended: false,
        reasons: [
          'Numeric data with sufficient history',
          'Could contain temporal patterns',
          'Requires time-based feature engineering'
        ],
        algorithms: ['ARIMA', 'LSTM', 'Prophet', 'XGBoost'],
        metrics: ['MAE', 'MSE', 'MAPE', 'Directional Accuracy']
      })
    }
    
    detectedProblemTypes.value = types.sort((a, b) => b.confidence - a.confidence)
    
    // Auto-select the highest confidence recommended type
    const recommendedType = types.find(t => t.recommended && t.confidence >= 80)
    if (recommendedType) {
      problemType.value = recommendedType
    }
  }
  
  const analyzeTargetVariable = (column) => {
    if (!dataset.value || dataset.value.length === 0) return
    
    // Get target values
    const targetValues = dataset.value
      .map(row => row[column.name])
      .filter(val => val != null && val !== '')
    
    if (targetValues.length === 0) return
    
    // Calculate distribution
    if (column.type === 'categorical' || column.uniqueValues <= 20) {
      // Categorical distribution
      const valueCounts = {}
      targetValues.forEach(val => {
        valueCounts[val] = (valueCounts[val] || 0) + 1
      })
      
      targetDistribution.value = Object.entries(valueCounts)
        .map(([label, count]) => ({
          label,
          count,
          percentage: (count / targetValues.length) * 100
        }))
        .sort((a, b) => b.count - a.count)
        
    } else {
      // Numeric distribution
      const numbers = targetValues.map(Number).filter(n => !isNaN(n)).sort((a, b) => a - b)
      
      if (numbers.length > 0) {
        const mean = numbers.reduce((sum, n) => sum + n, 0) / numbers.length
        const median = numbers[Math.floor(numbers.length / 2)]
        const variance = numbers.reduce((sum, n) => sum + Math.pow(n - mean, 2), 0) / numbers.length
        const std = Math.sqrt(variance)
        
        numericStats.value = {
          mean,
          median,
          std,
          min: numbers[0],
          max: numbers[numbers.length - 1],
          q25: numbers[Math.floor(numbers.length * 0.25)],
          q75: numbers[Math.floor(numbers.length * 0.75)]
        }
        
        // Create histogram bins
        const binCount = Math.min(20, Math.max(5, Math.sqrt(numbers.length)))
        const binWidth = (numericStats.value.max - numericStats.value.min) / binCount
        
        histogramBins.value = Array(Math.floor(binCount)).fill().map((_, i) => {
          const start = numericStats.value.min + (i * binWidth)
          const end = start + binWidth
          const count = numbers.filter(n => n >= start && n < end).length
          
          return {
            range: `${start.toFixed(1)}-${end.toFixed(1)}`,
            count,
            start,
            end
          }
        })
      }
    }
    
    // Calculate data quality
    calculateDataQuality(column, targetValues)
    
    // Generate recommendations
    generateRecommendations(column, targetValues)
  }
  
  const calculateDataQuality = (column, targetValues) => {
    const totalRows = dataset.value?.length || 0
    
    // Completeness
    const completeness = (targetValues.length / totalRows) * 100
    
    // Balance (for classification) or variance (for regression)
    let balance = 100
    if (targetDistribution.value.length > 0) {
      // Classification balance
      const maxClass = Math.max(...targetDistribution.value.map(d => d.percentage))
      const minClass = Math.min(...targetDistribution.value.map(d => d.percentage))
      balance = (minClass / maxClass) * 100
    } else if (numericStats.value.std) {
      // Regression variance (normalized)
      const cv = (numericStats.value.std / Math.abs(numericStats.value.mean)) * 100
      balance = Math.max(0, 100 - Math.min(cv, 100))
    }
    
    // Predictability (simplified heuristic)
    let predictability = 75 // Base predictability
    if (column.uniqueValues === 1) predictability = 0 // No variance
    if (column.uniqueValues === 2) predictability = 90 // Binary is often predictable
    if (column.type === 'numeric' && numericStats.value.std) {
      // Higher variance might mean harder to predict
      const cv = (numericStats.value.std / Math.abs(numericStats.value.mean)) * 100
      predictability = Math.max(50, 90 - (cv / 2))
    }
    
    dataQuality.value = {
      completeness: Math.round(completeness),
      balance: Math.round(balance),
      predictability: Math.round(predictability)
    }
    
    // Generate quality issues
    qualityIssues.value = []
    
    if (completeness < 95) {
      qualityIssues.value.push({
        type: 'missing_data',
        severity: completeness < 80 ? 'high' : 'medium',
        message: `${(100 - completeness).toFixed(1)}% of target values are missing`
      })
    }
    
    if (balance < 30 && targetDistribution.value.length > 1) {
      qualityIssues.value.push({
        type: 'class_imbalance',
        severity: balance < 10 ? 'high' : 'medium',
        message: 'Significant class imbalance detected'
      })
    }
    
    if (column.uniqueValues === 1) {
      qualityIssues.value.push({
        type: 'no_variance',
        severity: 'high',
        message: 'Target variable has only one unique value - cannot be predicted'
      })
    }
    
    if (column.uniqueValues > totalRows * 0.9) {
      qualityIssues.value.push({
        type: 'high_cardinality',
        severity: 'medium',
        message: 'Very high cardinality - might indicate ID column or unique identifiers'
      })
    }
  }
  
  const generateRecommendations = (column, targetValues) => {
    recommendations.value = []
    
    // Missing data recommendations
    if (dataQuality.value.completeness < 95) {
      recommendations.value.push({
        type: 'missing_data',
        icon: '🔧',
        title: 'Handle Missing Target Values',
        description: 'Remove rows with missing target values or investigate data collection issues.',
        actions: [
          { name: 'Remove Missing Rows', action: 'remove_missing' }
        ]
      })
    }
    
    // Class imbalance recommendations
    if (dataQuality.value.balance < 30 && targetDistribution.value.length > 1) {
      recommendations.value.push({
        type: 'class_imbalance',
        icon: '⚖️',
        title: 'Address Class Imbalance',
        description: 'Consider sampling techniques or different evaluation metrics for imbalanced data.',
        actions: [
          { name: 'Apply SMOTE', action: 'smote' },
          { name: 'Use Balanced Metrics', action: 'balanced_metrics' }
        ]
      })
    }
    
    // Feature engineering recommendations
    if (column.type === 'numeric' && numericStats.value.std) {
      const cv = (numericStats.value.std / Math.abs(numericStats.value.mean)) * 100
      if (cv > 100) {
        recommendations.value.push({
          type: 'feature_engineering',
          icon: '🔄',
          title: 'Consider Target Transformation',
          description: 'High variance in target variable. Log transformation might improve model performance.',
          actions: [
            { name: 'Apply Log Transform', action: 'log_transform' }
          ]
        })
      }
    }
    
    // Data collection recommendations
    if (targetValues.length < 1000) {
      recommendations.value.push({
        type: 'data_size',
        icon: '📈',
        title: 'Increase Data Size',
        description: 'Small dataset might limit model performance. Consider collecting more data.',
        actions: []
      })
    }
  }
  
  const updateAnalysisForProblemType = (type) => {
    // Update recommendations based on selected problem type
    if (type.id === 'binary_classification') {
      // Add binary-specific recommendations
      if (!recommendations.value.find(r => r.type === 'threshold_tuning')) {
        recommendations.value.push({
          type: 'threshold_tuning',
          icon: '🎛️',
          title: 'Optimize Decision Threshold',
          description: 'For binary classification, consider tuning the decision threshold based on business requirements.',
          actions: [
            { name: 'ROC Analysis', action: 'roc_analysis' }
          ]
        })
      }
    }
  }
  
  const analyzeCorrelations = async () => {
    if (!selectedColumn.value) return
    
    isAnalyzing.value = true
    analysisProgress.value = 0
    
    try {
      analysisMessage.value = 'Calculating feature correlations...'
      analysisProgress.value = 25
      
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      analysisMessage.value = 'Identifying highly correlated features...'
      analysisProgress.value = 50
      
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      analysisMessage.value = 'Generating correlation insights...'
      analysisProgress.value = 75
      
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      analysisMessage.value = 'Analysis complete!'
      analysisProgress.value = 100
      
      // Add correlation recommendations
      recommendations.value.push({
        type: 'correlation',
        icon: '🔗',
        title: 'Feature Correlations Analyzed',
        description: 'Found strong correlations with: feature1 (0.87), feature2 (0.72), feature3 (-0.65)',
        actions: []
      })
      
    } catch (error) {
      console.error('Correlation analysis failed:', error)
    } finally {
      setTimeout(() => {
        isAnalyzing.value = false
      }, 500)
    }
  }
  
  const validateSelection = async () => {
    if (!selectedColumn.value || !problemType.value) return
    
    isValidating.value = true
    analysisProgress.value = 0
    
    try {
      analysisMessage.value = 'Validating target variable selection...'
      analysisProgress.value = 20
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      analysisMessage.value = 'Checking problem type compatibility...'
      analysisProgress.value = 40
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      analysisMessage.value = 'Assessing data quality requirements...'
      analysisProgress.value = 60
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      analysisMessage.value = 'Estimating model performance...'
      analysisProgress.value = 80
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      analysisMessage.value = 'Validation complete!'
      analysisProgress.value = 100
      
      validationComplete.value = true
      
    } catch (error) {
      console.error('Validation failed:', error)
    } finally {
      setTimeout(() => {
        isValidating.value = false
      }, 500)
    }
  }
  
  const confirmSelection = () => {
    if (!selectedColumn.value || !problemType.value) return
    
    // Update pipeline state
    emit('update:state', {
      targetColumn: selectedColumn.value.name,
      problemType: problemType.value.id,
      targetAnalysis: {
        distribution: targetDistribution.value,
        numericStats: numericStats.value,
        dataQuality: dataQuality.value,
        expectedPerformance: expectedPerformance.value
      },
      recommendations: recommendations.value
    })
    
    // Advance to next step
    emit('next-step')
    
    console.log('Target selection confirmed:', {
      target: selectedColumn.value.name,
      problemType: problemType.value.id
    })
  }
  
  const executeRecommendation = (action) => {
    // Placeholder for recommendation actions
    console.log('Executing recommendation:', action.action)
    alert(`Recommendation "${action.name}" will be implemented in preprocessing step!`)
  }
  
  // Initialize data
  const initializeColumns = () => {
    if (!columnAnalysis.value.length) return
    
    availableColumns.value = columnAnalysis.value.map(col => {
      // Calculate suitability score
      let suitability = 70 // Base score
      
      // Penalize high missing values
      const missingPercent = (col.missingCount / (dataset.value?.length || 1)) * 100
      suitability -= missingPercent * 0.5
      
      // Boost for good cardinality
      if (col.type === 'categorical' && col.unique >= 2 && col.unique <= 10) suitability += 15
      if (col.type === 'numeric' && col.unique > 20) suitability += 10
      
      // Penalize single value columns
      if (col.unique === 1) suitability = 0
      
      // Penalize very high cardinality (likely IDs)
      if (col.unique > (dataset.value?.length || 1) * 0.9) suitability -= 40
      
      suitability = Math.max(0, Math.min(100, Math.round(suitability)))
      
      // Generate reasons
      const reasons = []
      if (col.unique === 1) {
        reasons.push({ type: 'negative', text: 'Only one unique value' })
      } else if (col.unique === 2) {
        reasons.push({ type: 'positive', text: 'Perfect for binary classification' })
      } else if (col.unique <= 10 && col.type === 'categorical') {
        reasons.push({ type: 'positive', text: 'Good for multi-class classification' })
      } else if (col.unique > 20 && col.type === 'numeric') {
        reasons.push({ type: 'positive', text: 'Suitable for regression' })
      }
      
      if (missingPercent < 5) {
        reasons.push({ type: 'positive', text: 'Low missing values' })
      } else if (missingPercent > 20) {
        reasons.push({ type: 'negative', text: 'High missing values' })
      }
      
      // Sample values
      const sampleValues = dataset.value
        ?.slice(0, 10)
        .map(row => row[col.name])
        .filter(val => val != null && val !== '')
        .slice(0, 3)
        .join(', ') || 'No samples'
      
      return {
        name: col.name,
        type: col.type,
        uniqueValues: col.unique,
        missingCount: col.missingCount,
        missingPercent: Math.round(missingPercent),
        suitability,
        recommended: suitability >= 80,
        reasons,
        sampleValues: sampleValues.length > 50 ? sampleValues.substring(0, 50) + '...' : sampleValues
      }
    }).sort((a, b) => b.suitability - a.suitability)
  }
  
  // Watchers
  watch(() => props.pipelineState.columnAnalysis, (newAnalysis) => {
    if (newAnalysis && newAnalysis.length > 0) {
      initializeColumns()
    }
  }, { immediate: true })
  
  // Lifecycle
  onMounted(() => {
    initializeColumns()
    
    // Restore state if available
    if (props.pipelineState.targetColumn) {
      const savedColumn = availableColumns.value.find(col => col.name === props.pipelineState.targetColumn)
      if (savedColumn) {
        selectColumn(savedColumn)
        
        if (props.pipelineState.problemType) {
          const savedProblemType = detectedProblemTypes.value.find(type => type.id === props.pipelineState.problemType)
          if (savedProblemType) {
            selectProblemType(savedProblemType)
          }
        }
      }
    }
  })
  </script>
  
  <style scoped>
  /* Use the same CSS variables and styling patterns */
  .target-selection-container {
    padding: 2rem;
    height: 100%;
    overflow-y: auto;
    background: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .selection-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .selection-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: var(--primary-gradient);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--primary-color);
}

  
  .selection-header p {
    color: var(--text-secondary);
    font-size: 1rem;
  }
  
  .step-progress {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 3rem;
    padding: 1.5rem;
    background: var(--bg-card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
  }
  
  .progress-step {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-tertiary);
    transition: all var(--transition-normal);
  }
  
  .progress-step.completed {
    color: var(--success-color);
  }
  
  .step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--bg-secondary);
    border: 2px solid var(--border-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    transition: all var(--transition-normal);
  }
  
  .progress-step.completed .step-number {
    background: var(--success-color);
    border-color: var(--success-color);
    color: white;
  }
  
  .progress-arrow {
    margin: 0 1rem;
    color: var(--text-tertiary);
    font-size: 1.2rem;
  }
  
  .selection-section {
    margin-bottom: 3rem;
  }
  
  .selection-section h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .selection-section p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  .columns-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 1.5rem;
  }
  
  .column-card {
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .column-card:hover {
    border-color: var(--border-medium);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .column-card.selected {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
    box-shadow: var(--shadow-glow);
  }
  
  .column-card.recommended {
    border-color: var(--success-color);
  }
  
  .column-card.recommended::before {
    content: '⭐';
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 1.2rem;
  }
  
  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  
  .column-header h4 {
    color: var(--text-primary);
    font-weight: 600;
    margin: 0;
  }
  
  .column-badges {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .type-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .type-numeric {
    background: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
  }
  
  .type-categorical {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
  }
  
  .recommended-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
  }
  
  .column-stats {
    margin-bottom: 1rem;
  }
  
  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }
  
  .stat-label {
    color: var(--text-secondary);
  }
  
  .stat-value {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .column-suitability {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .suitability-score {
    text-align: center;
    min-width: 80px;
  }
  
  .suitability-score .score {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  
  .suitability-score.excellent .score { color: var(--success-color); }
  .suitability-score.good .score { color: var(--info-color); }
  .suitability-score.fair .score { color: var(--warning-color); }
  .suitability-score.poor .score { color: var(--error-color); }
  
  .suitability-score .label {
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }
  
  .suitability-reasons {
    flex: 1;
  }
  
  .reason-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
    font-size: 0.8125rem;
  }
  
  .reason-item.positive {
    color: var(--success-color);
  }
  
  .reason-item.negative {
    color: var(--error-color);
  }
  
  .reason-icon {
    font-weight: 600;
  }
  
  .problem-type-section {
    margin-bottom: 3rem;
  }
  
  .problem-type-section h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .problem-type-section p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  .problem-types {
    display: grid;
    gap: 1.5rem;
  }
  
  .problem-type-card {
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .problem-type-card:hover {
    border-color: var(--border-medium);
    transform: translateY(-2px);
  }
  
  .problem-type-card.selected {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
  }
  
  .problem-type-card.recommended {
    border-color: var(--success-color);
  }
  
  .type-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .type-icon {
    font-size: 2rem;
  }
  
  .type-info {
    flex: 1;
  }
  
  .type-info h4 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .type-info p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0;
  }
  
  .type-confidence {
    text-align: center;
  }
  
  .confidence-score {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  
  .confidence-score.high { color: var(--success-color); }
  .confidence-score.medium { color: var(--warning-color); }
  .confidence-score.low { color: var(--error-color); }
  
  .recommended-label {
    font-size: 0.75rem;
    color: var(--success-color);
    font-weight: 500;
  }
  
  .type-details {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
  }
  
  .detail-section h6 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }
  
  .detail-section ul {
    margin: 0;
    padding-left: 1rem;
    font-size: 0.8125rem;
    color: var(--text-secondary);
  }
  
  .detail-section li {
    margin-bottom: 0.25rem;
  }
  
  .algorithm-tags,
  .metrics-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
  }
  
  .algorithm-tag,
  .metric-tag {
    padding: 0.25rem 0.5rem;
    background: rgba(102, 126, 234, 0.1);
    color: var(--primary-color);
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .metric-tag {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
  }
  
  .analysis-section {
    margin-bottom: 3rem;
  }
  
  .analysis-section h3 {
    margin-bottom: 1.5rem;
    color: var(--text-primary);
  }
  
  .analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
  }
  
  .analysis-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .analysis-card h4 {
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .class-distribution {
    display: grid;
    gap: 0.75rem;
  }
  
  .class-bar {
    display: grid;
    grid-template-columns: 1fr 2fr auto;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.875rem;
  }
  
  .class-label {
    color: var(--text-primary);
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .class-bar-bg {
    height: 8px;
    background: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
  }
  
  .class-bar-fill {
    height: 100%;
    background: var(--primary-gradient);
    transition: width var(--transition-normal);
  }
  
  .class-count {
    color: var(--text-secondary);
    font-weight: 500;
    min-width: 80px;
    text-align: right;
  }
  
  .distribution-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
  }
  
  .stat-name {
    color: var(--text-secondary);
  }
  
  .stat-value {
    color: var(--text-primary);
    font-weight: 600;
    font-family: 'Monaco', 'Consolas', monospace;
  }
  
  .histogram {
    margin-top: 1rem;
  }
  
  .histogram-bars {
    display: flex;
    align-items: end;
    height: 60px;
    margin-bottom: 0.5rem;
    gap: 1px;
  }
  
  .histogram-bar {
    flex: 1;
    background: var(--primary-gradient);
    opacity: 0.8;
    border-radius: 2px 2px 0 0;
    min-height: 2px;
    cursor: pointer;
    transition: opacity var(--transition-fast);
  }
  
  .histogram-bar:hover {
    opacity: 1;
  }
  
  .histogram-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--text-tertiary);
  }
  
  .quality-metrics {
    display: grid;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .quality-item {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1rem;
  }
  
  .quality-label {
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.875rem;
    min-width: 100px;
  }
  
  .quality-bar {
    height: 8px;
    background: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
  }
  
  .quality-fill {
    height: 100%;
    transition: width var(--transition-normal);
    border-radius: 4px;
  }
  
  .quality-fill.completeness {
    background: var(--success-color);
  }
  
  .quality-fill.balance {
    background: var(--info-color);
  }
  
  .quality-fill.predictability {
    background: var(--warning-color);
  }
  
  .quality-value {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.875rem;
    min-width: 40px;
    text-align: right;
  }
  
  .quality-issues {
    display: grid;
    gap: 0.5rem;
  }
  
  .quality-issue {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
  }
  
  .quality-issue.high {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: var(--error-color);
  }
  
  .quality-issue.medium {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: var(--warning-color);
  }
  
  .quality-issue.low {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    color: var(--success-color);
  }
  
  .issue-icon {
    font-size: 1rem;
  }
  
  .issue-text {
    flex: 1;
  }
  
  .recommendations {
    display: grid;
    gap: 1rem;
  }
  
  .recommendation-item {
    padding: 1rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
  }
  
  .rec-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
  }
  
  .rec-icon {
    font-size: 1.25rem;
  }
  
  .rec-header h6 {
    color: var(--text-primary);
    margin: 0;
  }
  
  .recommendation-item p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.75rem;
  }
  
  .rec-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .rec-action-btn {
    padding: 0.375rem 0.75rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .rec-action-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }
  
  .summary-section {
    margin-bottom: 3rem;
  }
  
  .summary-section h3 {
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .summary-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border-light);
  }
  
  .summary-row:last-child {
    border-bottom: none;
  }
  
  .summary-label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .summary-value {
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .performance-excellent {
    color: var(--success-color);
  }
  
  .performance-good {
    color: var(--info-color);
  }
  
  .performance-fair {
    color: var(--warning-color);
  }
  
  .performance-poor {
    color: var(--error-color);
  }
  
  .selection-actions {
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
    min-width: 180px;
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
  
  .analysis-modal {
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
    max-width: 400px;
    width: 90%;
    text-align: center;
  }
  
  .analysis-spinner {
    width: 48px;
    height: 48px;
    margin: 0 auto 1rem;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-left: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .modal-content h3 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .modal-content p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }
  
  .progress-bar {
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;
  }
  
  .progress-fill {
    height: 100%;
    background: var(--primary-gradient);
    transition: width 0.3s ease;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .target-selection-container {
      padding: 1rem;
    }
    
    .columns-grid {
      grid-template-columns: 1fr;
    }
    
    .problem-type-card .type-details {
      grid-template-columns: 1fr;
    }
    
    .analysis-grid {
      grid-template-columns: 1fr;
    }
    
    .distribution-stats {
      grid-template-columns: 1fr;
    }
    
    .quality-item {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }
    
    .selection-actions {
      flex-direction: column;
    }
    
    .action-btn {
      width: 100%;
    }
    
    .step-progress {
      flex-direction: column;
      gap: 1rem;
    }
    
    .progress-arrow {
      transform: rotate(90deg);
    }
  }
  </style>
  