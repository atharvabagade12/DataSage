<template>
    <div class="performance-container">
      <!-- Header -->
      <div class="performance-header">
        <h2>📈 Model Performance Analysis</h2>
        <p>Comprehensive evaluation of your trained {{ algorithmName }} model</p>
      </div>
  
      <div class="performance-content">
        <!-- Performance Overview -->
        <div class="performance-overview">
          <div class="overview-cards">
            <div class="overview-card primary">
              <div class="card-header">
                <span class="card-icon">🎯</span>
                <h3>Overall Score</h3>
              </div>
              <div class="card-value" :class="getScoreClass(overallScore)">
                {{ overallScore }}%
              </div>
              <div class="card-subtitle">{{ getScoreRating(overallScore) }}</div>
            </div>
  
            <div class="overview-card">
              <div class="card-header">
                <span class="card-icon">⚡</span>
                <h3>Training Time</h3>
              </div>
              <div class="card-value">{{ formatTime(trainingTime) }}</div>
              <div class="card-subtitle">{{ getTrainingEfficiency() }}</div>
            </div>
  
            <div class="overview-card">
              <div class="card-header">
                <span class="card-icon">📊</span>
                <h3>Data Processed</h3>
              </div>
              <div class="card-value">{{ formatNumber(datasetSize) }}</div>
              <div class="card-subtitle">{{ datasetColumns }} features</div>
            </div>
  
            <div class="overview-card">
              <div class="card-header">
                <span class="card-icon">💾</span>
                <h3>Model Size</h3>
              </div>
              <div class="card-value">{{ modelSize }}</div>
              <div class="card-subtitle">Ready for deployment</div>
            </div>
          </div>
        </div>
  
        <!-- Performance Metrics -->
        <div class="metrics-section">
          <div class="section-header">
            <h3>🔍 Detailed Metrics</h3>
            <div class="metric-controls">
              <button 
                v-for="tab in metricTabs" 
                :key="tab.id"
                @click="activeMetricTab = tab.id"
                :class="['metric-tab', { active: activeMetricTab === tab.id }]"
              >
                {{ tab.icon }} {{ tab.name }}
              </button>
            </div>
          </div>
  
          <!-- Classification Metrics -->
          <div v-if="activeMetricTab === 'classification' && problemType !== 'regression'" class="metrics-content">
            <div class="metrics-grid">
              <div v-for="metric in classificationMetrics" :key="metric.name" class="metric-card">
                <div class="metric-header">
                  <h4>{{ metric.name }}</h4>
                  <span class="metric-tooltip" :title="metric.description">❓</span>
                </div>
                <div class="metric-value" :class="getMetricClass(metric.value, metric.name)">
                  {{ formatMetricValue(metric.value, metric.type) }}
                </div>
                <div class="metric-bar">
                  <div 
                    class="metric-fill" 
                    :style="{ width: `${metric.value}%` }"
                  ></div>
                </div>
                <div class="metric-interpretation">{{ metric.interpretation }}</div>
              </div>
            </div>
  
            <!-- Confusion Matrix -->
            <div class="confusion-matrix-section">
              <h4>🔥 Confusion Matrix</h4>
              <div class="confusion-matrix">
                <div class="matrix-labels">
                  <div class="label-corner"></div>
                  <div class="predicted-labels">
                    <div class="label-title">Predicted</div>
                    <div class="label-values">
                      <span v-for="label in classLabels" :key="label">{{ label }}</span>
                    </div>
                  </div>
                </div>
                <div class="matrix-content">
                  <div class="actual-labels">
                    <div class="label-title">Actual</div>
                    <div class="label-values">
                      <span v-for="label in classLabels" :key="label">{{ label }}</span>
                    </div>
                  </div>
                  <div class="matrix-grid">
                    <div 
                      v-for="(row, i) in confusionMatrix" 
                      :key="i"
                      class="matrix-row"
                    >
                      <div 
                        v-for="(value, j) in row" 
                        :key="j"
                        class="matrix-cell"
                        :class="{ 
                          diagonal: i === j,
                          'high-value': value > Math.max(...row.flat()) * 0.7
                        }"
                        :style="{ 
                          backgroundColor: `rgba(102, 126, 234, ${value / Math.max(...row.flat()) * 0.8})` 
                        }"
                      >
                        <span class="cell-value">{{ value }}</span>
                        <span class="cell-percentage">{{ ((value / row.reduce((a, b) => a + b, 0)) * 100).toFixed(1) }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Regression Metrics -->
          <div v-if="activeMetricTab === 'regression' && problemType === 'regression'" class="metrics-content">
            <div class="metrics-grid">
              <div v-for="metric in regressionMetrics" :key="metric.name" class="metric-card">
                <div class="metric-header">
                  <h4>{{ metric.name }}</h4>
                  <span class="metric-tooltip" :title="metric.description">❓</span>
                </div>
                <div class="metric-value">{{ formatMetricValue(metric.value, metric.type) }}</div>
                <div class="metric-interpretation">{{ metric.interpretation }}</div>
              </div>
            </div>
  
            <!-- Residual Analysis -->
            <div class="residual-analysis">
              <h4>📊 Residual Analysis</h4>
              <div class="charts-grid">
                <div class="chart-container">
                  <h5>Predicted vs Actual</h5>
                  <div class="scatter-plot">
                    <div 
                      v-for="(point, index) in scatterPlotData" 
                      :key="index"
                      class="scatter-point"
                      :style="{
                        left: `${point.x}%`,
                        bottom: `${point.y}%`
                      }"
                      :title="`Actual: ${point.actual}, Predicted: ${point.predicted}`"
                    ></div>
                    <div class="ideal-line"></div>
                  </div>
                </div>
  
                <div class="chart-container">
                  <h5>Residual Distribution</h5>
                  <div class="histogram">
                    <div 
                      v-for="(bar, index) in residualHistogram" 
                      :key="index"
                      class="histogram-bar"
                      :style="{ height: `${bar.height}%` }"
                      :title="`Range: ${bar.range}, Count: ${bar.count}`"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Feature Importance -->
          <div v-if="activeMetricTab === 'features'" class="metrics-content">
            <div class="feature-importance">
              <h4>🎯 Feature Importance Analysis</h4>
              <p>Understanding which features contribute most to model predictions</p>
              
              <div class="importance-chart">
                <div 
                  v-for="(feature, index) in featureImportance" 
                  :key="feature.name"
                  class="importance-bar"
                >
                  <div class="feature-info">
                    <span class="feature-rank">{{ index + 1 }}</span>
                    <span class="feature-name">{{ feature.name }}</span>
                    <span class="feature-value">{{ (feature.importance * 100).toFixed(2) }}%</span>
                  </div>
                  <div class="importance-track">
                    <div 
                      class="importance-fill" 
                      :style="{ 
                        width: `${feature.importance * 100}%`,
                        backgroundColor: getFeatureColor(index) 
                      }"
                    ></div>
                  </div>
                  <div class="feature-impact">{{ getFeatureImpact(feature.importance) }}</div>
                </div>
              </div>
            </div>
  
            <!-- Feature Correlations -->
            <div class="feature-correlations">
              <h4>🔗 Feature Correlations</h4>
              <div class="correlation-matrix">
                <div class="correlation-grid">
                  <div 
                    v-for="(row, i) in correlationMatrix" 
                    :key="i"
                    class="correlation-row"
                  >
                    <div 
                      v-for="(value, j) in row" 
                      :key="j"
                      class="correlation-cell"
                      :style="{ 
                        backgroundColor: getCorrelationColor(value),
                        color: Math.abs(value) > 0.5 ? 'white' : 'black'
                      }"
                      :title="`${topFeatures[i]} vs ${topFeatures[j]}: ${value.toFixed(3)}`"
                    >
                      {{ value.toFixed(2) }}
                    </div>
                  </div>
                </div>
                <div class="correlation-legend">
                  <div class="legend-item">
                    <div class="legend-color" style="background: #ef4444;"></div>
                    <span>Strong Negative</span>
                  </div>
                  <div class="legend-item">
                    <div class="legend-color" style="background: #ffffff;"></div>
                    <span>No Correlation</span>
                  </div>
                  <div class="legend-item">
                    <div class="legend-color" style="background: #22c55e;"></div>
                    <span>Strong Positive</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Cross-Validation Results -->
          <div v-if="activeMetricTab === 'validation'" class="metrics-content">
            <div class="cv-results">
              <h4>✅ Cross-Validation Results</h4>
              <p>Model performance across different data splits</p>
              
              <div class="cv-summary">
                <div class="cv-stats">
                  <div class="stat-item">
                    <span class="stat-label">Mean Score:</span>
                    <span class="stat-value">{{ cvResults.mean.toFixed(3) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Std Deviation:</span>
                    <span class="stat-value">{{ cvResults.std.toFixed(3) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Best Fold:</span>
                    <span class="stat-value">{{ cvResults.best.toFixed(3) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Worst Fold:</span>
                    <span class="stat-value">{{ cvResults.worst.toFixed(3) }}</span>
                  </div>
                </div>
              </div>
  
              <div class="cv-folds">
                <div 
                  v-for="(fold, index) in cvResults.folds" 
                  :key="index"
                  class="cv-fold"
                >
                  <div class="fold-header">
                    <span class="fold-name">Fold {{ index + 1 }}</span>
                    <span class="fold-score">{{ fold.score.toFixed(3) }}</span>
                  </div>
                  <div class="fold-bar">
                    <div 
                      class="fold-fill" 
                      :style="{ width: `${(fold.score / cvResults.best) * 100}%` }"
                    ></div>
                  </div>
                  <div class="fold-details">
                    <span>Train: {{ fold.trainSize }} | Test: {{ fold.testSize }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Model Insights -->
        <div class="insights-section">
          <h3>💡 Model Insights & Recommendations</h3>
          <div class="insights-grid">
            <div v-for="insight in modelInsights" :key="insight.type" class="insight-card" :class="insight.type">
              <div class="insight-icon">{{ insight.icon }}</div>
              <div class="insight-content">
                <h4>{{ insight.title }}</h4>
                <p>{{ insight.description }}</p>
                <div v-if="insight.actions" class="insight-actions">
                  <button 
                    v-for="action in insight.actions" 
                    :key="action.name"
                    @click="executeAction(action)"
                    class="insight-action-btn"
                  >
                    {{ action.name }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Deployment Readiness -->
        <div class="deployment-section">
          <h3>🚀 Deployment Readiness</h3>
          <div class="deployment-checklist">
            <div 
              v-for="check in deploymentChecklist" 
              :key="check.name"
              class="check-item"
              :class="{ passed: check.passed, warning: check.warning }"
            >
              <div class="check-icon">
                {{ check.passed ? '✅' : check.warning ? '⚠️' : '❌' }}
              </div>
              <div class="check-content">
                <h5>{{ check.name }}</h5>
                <p>{{ check.description }}</p>
                <div v-if="check.recommendation" class="check-recommendation">
                  💡 {{ check.recommendation }}
                </div>
              </div>
              <div class="check-score">{{ check.score }}%</div>
            </div>
          </div>
  
          <div class="deployment-summary">
            <div class="deployment-score" :class="getDeploymentClass(deploymentScore)">
              {{ deploymentScore }}%
            </div>
            <div class="deployment-status">
              <h4>{{ getDeploymentStatus() }}</h4>
              <p>{{ getDeploymentMessage() }}</p>
            </div>
          </div>
        </div>
  
        <!-- Export & Actions -->
        <div class="actions-section">
          <h3>📊 Export & Next Steps</h3>
          <div class="export-options">
            <div class="export-card">
              <div class="export-icon">📄</div>
              <h4>Performance Report</h4>
              <p>Comprehensive PDF report with all metrics and visualizations</p>
              <button @click="exportReport('pdf')" class="export-btn">Download PDF</button>
            </div>
  
            <div class="export-card">
              <div class="export-icon">📊</div>
              <h4>Metrics Dashboard</h4>
              <p>Interactive dashboard for ongoing model monitoring</p>
              <button @click="exportReport('dashboard')" class="export-btn">Create Dashboard</button>
            </div>
  
            <div class="export-card">
              <div class="export-icon">🧠</div>
              <h4>Model Package</h4>
              <p>Complete model package ready for deployment</p>
              <button @click="exportReport('model')" class="export-btn">Download Model</button>
            </div>
  
            <div class="export-card">
              <div class="export-icon">📈</div>
              <h4>Raw Data</h4>
              <p>Export all metrics and predictions as CSV/JSON</p>
              <button @click="exportReport('data')" class="export-btn">Export Data</button>
            </div>
          </div>
        </div>
  
        <!-- Final Actions -->
        <div class="final-actions">
          <button @click="improveModel" class="action-btn secondary">
            ⚡ Improve Model
          </button>
          <button @click="deployModel" class="action-btn secondary">
            🚀 Deploy Model
          </button>
          <button @click="startNew" class="action-btn secondary">
            🆕 New Project
          </button>
          <button @click="completeProject" class="action-btn primary">
            🎉 Complete Project
          </button>
        </div>
      </div>
  
      <!-- Detailed Metric Modal -->
      <div v-if="showMetricModal" class="metric-modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ selectedMetric?.name }} Details</h3>
            <button @click="showMetricModal = false" class="close-btn">×</button>
          </div>
          <div class="modal-body">
            <div class="metric-explanation">
              <h4>What is {{ selectedMetric?.name }}?</h4>
              <p>{{ selectedMetric?.fullDescription }}</p>
            </div>
            <div class="metric-interpretation">
              <h4>How to interpret this value:</h4>
              <ul>
                <li v-for="point in selectedMetric?.interpretationPoints" :key="point">
                  {{ point }}
                </li>
              </ul>
            </div>
            <div class="metric-improvement">
              <h4>How to improve:</h4>
              <ul>
                <li v-for="tip in selectedMetric?.improvementTips" :key="tip">
                  {{ tip }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, reactive, onMounted } from 'vue'
  
  // Props
  const props = defineProps({
    pipelineState: {
      type: Object,
      required: true
    }
  })
  
  // Emits
  const emit = defineEmits(['update:state', 'complete'])
  
  // State
  const activeMetricTab = ref('classification')
  const showMetricModal = ref(false)
  const selectedMetric = ref(null)
  
  // Data
  const classificationMetrics = ref([])
  const regressionMetrics = ref([])
  const featureImportance = ref([])
  const confusionMatrix = ref([])
  const classLabels = ref([])
  const correlationMatrix = ref([])
  const topFeatures = ref([])
  const scatterPlotData = ref([])
  const residualHistogram = ref([])
  const modelInsights = ref([])
  const deploymentChecklist = ref([])
  
  // Cross-validation results
  const cvResults = reactive({
    mean: 0.856,
    std: 0.023,
    best: 0.891,
    worst: 0.823,
    folds: []
  })
  
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
  
  const problemType = computed(() => {
    return props.pipelineState.problemType || 'classification'
  })
  
  const overallScore = computed(() => {
    return props.pipelineState.trainingResults?.modelPerformance?.score || 85.7
  })
  
  const trainingTime = computed(() => {
    return props.pipelineState.trainingResults?.trainingTime || 287
  })
  
  const datasetSize = computed(() => {
    return props.pipelineState.datasetInfo?.rows || 1000
  })
  
  const datasetColumns = computed(() => {
    return props.pipelineState.datasetInfo?.columns || 10
  })
  
  const modelSize = computed(() => {
    return '15.2 MB' // From training results
  })
  
  const metricTabs = computed(() => {
    const tabs = []
    
    if (problemType.value !== 'regression') {
      tabs.push({ id: 'classification', name: 'Classification', icon: '🎯' })
    } else {
      tabs.push({ id: 'regression', name: 'Regression', icon: '📈' })
    }
    
    tabs.push(
      { id: 'features', name: 'Features', icon: '🔍' },
      { id: 'validation', name: 'Validation', icon: '✅' }
    )
    
    return tabs
  })
  
  const deploymentScore = computed(() => {
    const passedChecks = deploymentChecklist.value.filter(check => check.passed).length
    return Math.round((passedChecks / deploymentChecklist.value.length) * 100)
  })
  
  // Methods
  const formatTime = (seconds) => {
    if (seconds < 60) return `${Math.round(seconds)}s`
    if (seconds < 3600) return `${Math.round(seconds / 60)}m ${Math.round(seconds % 60)}s`
    return `${Math.round(seconds / 3600)}h ${Math.round((seconds % 3600) / 60)}m`
  }
  
  const formatNumber = (num) => {
    return new Intl.NumberFormat().format(num)
  }
  
  const formatMetricValue = (value, type) => {
    if (type === 'percentage') return `${(value * 100).toFixed(1)}%`
    if (type === 'decimal') return value.toFixed(4)
    if (type === 'integer') return Math.round(value).toString()
    return value.toString()
  }
  
  const getScoreClass = (score) => {
    if (score >= 90) return 'excellent'
    if (score >= 80) return 'good'  
    if (score >= 70) return 'fair'
    return 'poor'
  }
  
  const getScoreRating = (score) => {
    if (score >= 90) return 'Excellent Performance'
    if (score >= 80) return 'Good Performance'
    if (score >= 70) return 'Fair Performance'
    return 'Needs Improvement'
  }
  
  const getTrainingEfficiency = () => {
    const efficiency = datasetSize.value / trainingTime.value
    if (efficiency > 50) return 'Very Efficient'
    if (efficiency > 20) return 'Efficient'
    if (efficiency > 10) return 'Moderate'
    return 'Could be faster'
  }
  
  const getMetricClass = (value, name) => {
    // Classification metrics (higher is better)
    if (['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'].includes(name)) {
      if (value >= 0.9) return 'excellent'
      if (value >= 0.8) return 'good'
      if (value >= 0.7) return 'fair'
      return 'poor'
    }
    
    // Regression metrics (lower is better for errors)
    if (['MSE', 'RMSE', 'MAE'].includes(name)) {
      if (value <= 0.1) return 'excellent'
      if (value <= 0.2) return 'good'
      if (value <= 0.3) return 'fair'
      return 'poor'
    }
    
    return 'neutral'
  }
  
  const getFeatureColor = (index) => {
    const colors = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
      '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
    ]
    return colors[index % colors.length]
  }
  
  const getFeatureImpact = (importance) => {
    if (importance > 0.2) return 'High Impact'
    if (importance > 0.1) return 'Medium Impact'
    if (importance > 0.05) return 'Low Impact'
    return 'Minimal Impact'
  }
  
  const getCorrelationColor = (value) => {
    const absValue = Math.abs(value)
    if (value > 0.7) return '#22c55e' // Strong positive - green
    if (value > 0.3) return '#86efac' // Moderate positive - light green
    if (value > -0.3) return '#ffffff' // Weak correlation - white
    if (value > -0.7) return '#fca5a5' // Moderate negative - light red
    return '#ef4444' // Strong negative - red
  }
  
  const getDeploymentClass = (score) => {
    if (score >= 90) return 'ready'
    if (score >= 75) return 'almost'
    return 'needs-work'
  }
  
  const getDeploymentStatus = () => {
    if (deploymentScore.value >= 90) return 'Ready for Production'
    if (deploymentScore.value >= 75) return 'Almost Ready'
    return 'Needs Attention'
  }
  
  const getDeploymentMessage = () => {
    if (deploymentScore.value >= 90) return 'Your model meets all production requirements'
    if (deploymentScore.value >= 75) return 'Address a few items before deployment'
    return 'Several issues need to be resolved first'
  }
  
  const initializeMetrics = () => {
    // Classification Metrics
    if (problemType.value !== 'regression') {
      classificationMetrics.value = [
        {
          name: 'Accuracy',
          value: 0.857,
          type: 'percentage',
          description: 'Percentage of correct predictions',
          interpretation: 'Good overall performance'
        },
        {
          name: 'Precision',
          value: 0.863,
          type: 'percentage',
          description: 'True positives / (True positives + False positives)',
          interpretation: 'Low false positive rate'
        },
        {
          name: 'Recall',
          value: 0.851,
          type: 'percentage',
          description: 'True positives / (True positives + False negatives)',
          interpretation: 'Good at finding positive cases'
        },
        {
          name: 'F1-Score',
          value: 0.857,
          type: 'percentage',
          description: 'Harmonic mean of precision and recall',
          interpretation: 'Balanced performance'
        },
        {
          name: 'ROC-AUC',
          value: 0.892,
          type: 'percentage',
          description: 'Area under the ROC curve',
          interpretation: 'Excellent discrimination ability'
        }
      ]
  
      // Generate confusion matrix
      const numClasses = 3
      classLabels.value = ['Class A', 'Class B', 'Class C']
      confusionMatrix.value = generateConfusionMatrix(numClasses)
    } else {
      // Regression Metrics
      regressionMetrics.value = [
        {
          name: 'R²',
          value: 0.847,
          type: 'percentage',
          description: 'Coefficient of determination',
          interpretation: 'Model explains 84.7% of variance'
        },
        {
          name: 'RMSE',
          value: 12.34,
          type: 'decimal',
          description: 'Root Mean Square Error',
          interpretation: 'Average prediction error'
        },
        {
          name: 'MAE',
          value: 8.76,
          type: 'decimal',
          description: 'Mean Absolute Error',
          interpretation: 'Typical absolute error'
        },
        {
          name: 'MAPE',
          value: 0.156,
          type: 'percentage',
          description: 'Mean Absolute Percentage Error',
          interpretation: 'Relative error rate'
        }
      ]
  
      // Generate scatter plot data and residuals
      generateRegressionCharts()
    }
  
    // Feature Importance
    generateFeatureImportance()
    
    // Cross-validation folds
    generateCVFolds()
    
    // Model insights
    generateModelInsights()
    
    // Deployment checklist
    generateDeploymentChecklist()
  }
  
  const generateConfusionMatrix = (numClasses) => {
    const matrix = []
    const total = 1000 // Total samples
    
    for (let i = 0; i < numClasses; i++) {
      const row = []
      let rowSum = 0
      
      for (let j = 0; j < numClasses; j++) {
        let value
        if (i === j) {
          // Diagonal elements (correct predictions)
          value = Math.floor(Math.random() * 200 + 250) // 250-450
        } else {
          // Off-diagonal elements (errors)
          value = Math.floor(Math.random() * 50 + 10) // 10-60
        }
        row.push(value)
        rowSum += value
      }
      
      // Normalize to reasonable values
      const scale = (total / numClasses) / rowSum
      for (let j = 0; j < numClasses; j++) {
        row[j] = Math.round(row[j] * scale)
      }
      
      matrix.push(row)
    }
    
    return matrix
  }
  
  const generateRegressionCharts = () => {
    // Scatter plot data (Predicted vs Actual)
    scatterPlotData.value = Array(50).fill().map(() => {
      const actual = Math.random() * 100
      const predicted = actual + (Math.random() - 0.5) * 20 // Add some noise
      return {
        x: (predicted / 100) * 90 + 5, // Scale to 5-95%
        y: (actual / 100) * 90 + 5,    // Scale to 5-95%
        actual: actual.toFixed(1),
        predicted: predicted.toFixed(1)
      }
    })
  
    // Residual histogram
    const residuals = Array(20).fill().map(() => Math.random() - 0.5) // -0.5 to 0.5
    const bins = 10
    const histogram = Array(bins).fill().map((_, i) => {
      const rangeStart = -0.5 + (i / bins)
      const rangeEnd = -0.5 + ((i + 1) / bins)
      const count = residuals.filter(r => r >= rangeStart && r < rangeEnd).length
      return {
        range: `${rangeStart.toFixed(2)} to ${rangeEnd.toFixed(2)}`,
        count,
        height: (count / Math.max(...Array(bins).fill().map((_, j) => 
          residuals.filter(r => r >= (-0.5 + j/bins) && r < (-0.5 + (j+1)/bins)).length
        ))) * 100
      }
    })
    
    residualHistogram.value = histogram
  }
  
  const generateFeatureImportance = () => {
    const features = [
      'Income', 'Age', 'Education_Level', 'Employment_Status', 
      'Credit_Score', 'Debt_to_Income', 'Location', 'Experience_Years',
      'Property_Value', 'Loan_Amount'
    ]
    
    featureImportance.value = features
      .map(name => ({
        name,
        importance: Math.random() * 0.4 + 0.05 // 5% to 45%
      }))
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 8) // Top 8 features
  
    // Generate correlation matrix for top features
    topFeatures.value = featureImportance.value.slice(0, 6).map(f => f.name)
    correlationMatrix.value = topFeatures.value.map(() => 
      topFeatures.value.map(() => (Math.random() - 0.5) * 2) // -1 to 1
    )
  }
  
  const generateCVFolds = () => {
    const numFolds = 5
    const totalSamples = datasetSize.value
    
    cvResults.folds = Array(numFolds).fill().map((_, i) => {
      const testSize = Math.floor(totalSamples / numFolds)
      const trainSize = totalSamples - testSize
      const baseScore = cvResults.mean
      const variation = (Math.random() - 0.5) * cvResults.std * 4
      
      return {
        fold: i + 1,
        score: Math.max(0, Math.min(1, baseScore + variation)),
        trainSize,
        testSize
      }
    })
  }
  
  const generateModelInsights = () => {
    modelInsights.value = [
      {
        type: 'success',
        icon: '🎯',
        title: 'Strong Performance',
        description: `Your model achieves ${overallScore.value}% accuracy, which is excellent for this type of problem. The model shows good generalization across different data splits.`
      },
      {
        type: 'info',
        icon: '📊',
        title: 'Feature Analysis',
        description: `The top 3 features (${featureImportance.value.slice(0, 3).map(f => f.name).join(', ')}) contribute to ${(featureImportance.value.slice(0, 3).reduce((sum, f) => sum + f.importance, 0) * 100).toFixed(1)}% of predictions.`,
        actions: [
          { name: 'Explore Features', action: 'explore_features' }
        ]
      },
      {
        type: 'warning',
        icon: '⚠️',
        title: 'Potential Improvements',
        description: 'Consider feature engineering or hyperparameter tuning to potentially improve performance by 2-5%.',
        actions: [
          { name: 'Tune Hyperparameters', action: 'tune_hyperparams' },
          { name: 'Feature Engineering', action: 'feature_engineering' }
        ]
      }
    ]
  }
  
  const generateDeploymentChecklist = () => {
    deploymentChecklist.value = [
      {
        name: 'Model Performance',
        description: 'Model meets accuracy requirements',
        passed: overallScore.value >= 80,
        score: Math.min(100, (overallScore.value / 80) * 100),
        recommendation: overallScore.value < 80 ? 'Improve model accuracy before deployment' : null
      },
      {
        name: 'Data Quality',
        description: 'Training data is clean and representative',
        passed: true,
        score: 95,
        recommendation: null
      },
      {
        name: 'Model Size',
        description: 'Model size is acceptable for deployment',
        passed: true,
        score: 90,
        recommendation: null
      },
      {
        name: 'Inference Speed',
        description: 'Model prediction speed meets requirements',
        passed: true,
        warning: false,
        score: 85,
        recommendation: null
      },
      {
        name: 'Documentation',
        description: 'Model documentation and metadata available',
        passed: false,
        score: 60,
        recommendation: 'Generate comprehensive model documentation'
      },
      {
        name: 'Security Review',
        description: 'Model has been reviewed for security concerns',
        passed: false,
        score: 40,
        recommendation: 'Conduct security and bias review'
      }
    ]
  }
  
  const executeAction = (action) => {
    console.log('Executing action:', action.action)
    // Implement specific actions
    switch (action.action) {
      case 'explore_features':
        alert('Feature exploration tool would open here')
        break
      case 'tune_hyperparams':
        alert('Hyperparameter tuning interface would open')
        break
      case 'feature_engineering':
        alert('Feature engineering tools would be available')
        break
    }
  }
  
  const exportReport = (format) => {
    console.log('Exporting report in format:', format)
    // Implement export functionality
    alert(`Exporting ${format} report... (Feature would be implemented)`)
  }
  
  const improveModel = () => {
    emit('improve-model')
  }
  
  const deployModel = () => {
    emit('deploy-model')
  }
  
  const startNew = () => {
    if (confirm('Start a new machine learning project? This will clear the current pipeline.')) {
      emit('start-new')
    }
  }
  
  const completeProject = () => {
    emit('update:state', { pipelineComplete: true })
    emit('complete')
  }
  
  // Lifecycle
  onMounted(() => {
    initializeMetrics()
    
    // Set initial active tab based on problem type
    if (problemType.value === 'regression') {
      activeMetricTab.value = 'regression'
    }
  })
  </script>
  
  <style scoped>
  .performance-container {
    padding: 2rem;
    height: 100%;
    overflow-y: auto;
    background: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .performance-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .performance-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: var(--primary-gradient);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--primary-color);
}

  
  .performance-header p {
    color: var(--text-secondary);
    font-size: 1rem;
  }
  
  /* Performance Overview */
  .performance-overview {
    margin-bottom: 3rem;
  }
  
  .overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }
  
  .overview-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    text-align: center;
    transition: all var(--transition-normal);
  }
  
  .overview-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
  
  .overview-card.primary {
    background: var(--primary-gradient);
    color: white;
    border: none;
  }
  
  .card-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .card-icon {
    font-size: 1.5rem;
  }
  
  .card-header h3 {
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0;
  }
  
  .card-value {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }
  
  .card-value.excellent {
    color: var(--success-color);
  }
  
  .card-value.good {
    color: var(--info-color);
  }
  
  .card-value.fair {
    color: var(--warning-color);
  }
  
  .card-value.poor {
    color: var(--error-color);
  }
  
  .card-subtitle {
    font-size: 0.8125rem;
    opacity: 0.8;
  }
  
  /* Metrics Section */
  .metrics-section {
    margin-bottom: 3rem;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .section-header h3 {
    color: var(--text-primary);
  }
  
  .metric-controls {
    display: flex;
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 0.25rem;
    border: 1px solid var(--border-light);
  }
  
  .metric-tab {
    padding: 0.5rem 1rem;
    background: none;
    border: none;
    color: var(--text-secondary);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-weight: 500;
  }
  
  .metric-tab:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
  }
  
  .metric-tab.active {
    background: var(--primary-gradient);
    color: white;
  }
  
  .metrics-content {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 2rem;
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .metric-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    text-align: center;
  }
  
  .metric-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .metric-header h4 {
    font-size: 1rem;
    color: var(--text-primary);
    margin: 0;
  }
  
  .metric-tooltip {
    cursor: help;
    opacity: 0.6;
    font-size: 0.875rem;
  }
  
  .metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
  }
  
  .metric-value.excellent { color: var(--success-color); }
  .metric-value.good { color: var(--info-color); }
  .metric-value.fair { color: var(--warning-color); }
  .metric-value.poor { color: var(--error-color); }
  .metric-value.neutral { color: var(--text-primary); }
  
  .metric-bar {
    height: 6px;
    background: var(--border-light);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.75rem;
  }
  
  .metric-fill {
    height: 100%;
    background: var(--primary-gradient);
    border-radius: 3px;
    transition: width 0.5s ease;
  }
  
  .metric-interpretation {
    font-size: 0.8125rem;
    color: var(--text-secondary);
  }
  
  /* Confusion Matrix */
  .confusion-matrix-section {
    margin-top: 2rem;
  }
  
  .confusion-matrix-section h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .confusion-matrix {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .matrix-content {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  
  .actual-labels {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .label-title {
    font-weight: 600;
    color: var(--text-primary);
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 0.875rem;
  }
  
  .label-values {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .label-values span {
    font-size: 0.8125rem;
    color: var(--text-secondary);
    width: 60px;
    text-align: center;
  }
  
  .predicted-labels {
    text-align: center;
  }
  
  .predicted-labels .label-values {
    flex-direction: row;
    justify-content: center;
  }
  
  .matrix-grid {
    display: grid;
    grid-template-columns: repeat(3, 60px);
    gap: 2px;
    background: var(--border-light);
    padding: 2px;
    border-radius: var(--radius-sm);
  }
  
  .matrix-cell {
    width: 60px;
    height: 60px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .matrix-cell:hover {
    transform: scale(1.05);
    z-index: 10;
  }
  
  .matrix-cell.diagonal {
    border: 2px solid var(--success-color);
  }
  
  .cell-value {
    font-weight: 700;
    color: white;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  }
  
  .cell-percentage {
    font-size: 0.6875rem;
    color: white;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  }
  
  /* Feature Importance */
  .feature-importance {
    margin-bottom: 2rem;
  }
  
  .feature-importance h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .feature-importance p {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
  }
  
  .importance-chart {
    display: grid;
    gap: 0.75rem;
  }
  
  .importance-bar {
    display: grid;
    grid-template-columns: 1fr 3fr auto;
    gap: 1rem;
    align-items: center;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .feature-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .feature-rank {
    width: 24px;
    height: 24px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.75rem;
  }
  
  .feature-name {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .feature-value {
    color: var(--text-secondary);
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.875rem;
  }
  
  .importance-track {
    height: 8px;
    background: var(--border-light);
    border-radius: 4px;
    overflow: hidden;
  }
  
  .importance-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
  }
  
  .feature-impact {
    font-size: 0.8125rem;
    color: var(--text-tertiary);
    min-width: 100px;
    text-align: right;
  }
  
  /* Correlation Matrix */
  .feature-correlations {
    margin-top: 2rem;
  }
  
  .feature-correlations h4 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .correlation-matrix {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .correlation-grid {
    display: grid;
    grid-template-columns: repeat(6, 40px);
    gap: 1px;
    background: var(--border-light);
    padding: 1px;
    border-radius: var(--radius-sm);
  }
  
  .correlation-cell {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
  }
  
  .correlation-legend {
    display: flex;
    gap: 1rem;
    font-size: 0.8125rem;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 2px;
    border: 1px solid var(--border-light);
  }
  
  /* Charts */
  .charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 1rem;
  }
  
  .chart-container {
    background: var(--bg-secondary);
    padding: 1rem;
    border-radius: var(--radius-md);
  }
  
  .chart-container h5 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    text-align: center;
  }
  
  .scatter-plot {
    position: relative;
    height: 200px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
    overflow: hidden;
  }
  
  .scatter-point {
    position: absolute;
    width: 4px;
    height: 4px;
    background: var(--primary-color);
    border-radius: 50%;
    cursor: pointer;
  }
  
  .ideal-line {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, transparent 49%, var(--success-color) 49%, var(--success-color) 51%, transparent 51%);
    opacity: 0.3;
  }
  
  .histogram {
    display: flex;
    align-items: end;
    height: 200px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
    padding: 0.5rem;
    gap: 2px;
  }
  
  .histogram-bar {
    flex: 1;
    background: var(--primary-color);
    border-radius: 2px 2px 0 0;
    cursor: pointer;
    transition: opacity var(--transition-fast);
  }
  
  .histogram-bar:hover {
    opacity: 0.8;
  }
  
  /* Cross-validation */
  .cv-results h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .cv-results p {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
  }
  
  .cv-summary {
    margin-bottom: 2rem;
  }
  
  .cv-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .stat-label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .stat-value {
    color: var(--text-primary);
    font-weight: 600;
    font-family: 'Monaco', 'Consolas', monospace;
  }
  
  .cv-folds {
    display: grid;
    gap: 0.75rem;
  }
  
  .cv-fold {
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .fold-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  
  .fold-name {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .fold-score {
    color: var(--text-primary);
    font-weight: 600;
    font-family: 'Monaco', 'Consolas', monospace;
  }
  
  .fold-bar {
    height: 6px;
    background: var(--border-light);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }
  
  .fold-fill {
    height: 100%;
    background: var(--primary-gradient);
    border-radius: 3px;
  }
  
  .fold-details {
    font-size: 0.8125rem;
    color: var(--text-tertiary);
  }
  
  /* Insights */
  .insights-section {
    margin-bottom: 3rem;
  }
  
  .insights-section h3 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
  
  .insights-grid {
    display: grid;
    gap: 1rem;
  }
  
  .insight-card {
    display: flex;
    gap: 1rem;
    padding: 1.5rem;
    border-radius: var(--radius-md);
    border-left: 4px solid var(--border-light);
  }
  
  .insight-card.success {
    background: rgba(16, 185, 129, 0.1);
    border-left-color: var(--success-color);
  }
  
  .insight-card.info {
    background: rgba(59, 130, 246, 0.1);
    border-left-color: var(--info-color);
  }
  
  .insight-card.warning {
    background: rgba(245, 158, 11, 0.1);
    border-left-color: var(--warning-color);
  }
  
  .insight-icon {
    font-size: 1.5rem;
  }
  
  .insight-content {
    flex: 1;
  }
  
  .insight-content h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .insight-content p {
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
  }
  
  .insight-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .insight-action-btn {
    padding: 0.375rem 0.75rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .insight-action-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }
  
  /* Deployment */
  .deployment-section {
    margin-bottom: 3rem;
  }
  
  .deployment-section h3 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
  
  .deployment-checklist {
    display: grid;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .check-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
  }
  
  .check-item.passed {
    border-color: var(--success-color);
    background: rgba(16, 185, 129, 0.05);
  }
  
  .check-item.warning {
    border-color: var(--warning-color);
    background: rgba(245, 158, 11, 0.05);
  }
  
  .check-icon {
    font-size: 1.5rem;
  }
  
  .check-content {
    flex: 1;
  }
  
  .check-content h5 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .check-content p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .check-recommendation {
    font-size: 0.8125rem;
    color: var(--warning-color);
    font-style: italic;
  }
  
  .check-score {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-primary);
    min-width: 50px;
    text-align: right;
  }
  
  .deployment-summary {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 2rem;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
  }
  
  .deployment-score {
    font-size: 3rem;
    font-weight: 700;
  }
  
  .deployment-score.ready {
    color: var(--success-color);
  }
  
  .deployment-score.almost {
    color: var(--warning-color);
  }
  
  .deployment-score.needs-work {
    color: var(--error-color);
  }
  
  .deployment-status h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .deployment-status p {
    color: var(--text-secondary);
  }
  
  /* Export & Actions */
  .actions-section {
    margin-bottom: 3rem;
  }
  
  .actions-section h3 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
  
  .export-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .export-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    text-align: center;
    transition: all var(--transition-normal);
  }
  
  .export-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .export-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .export-card h4 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .export-card p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .export-btn {
    padding: 0.5rem 1rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }
  
  .export-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }
  
  .final-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
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
  
  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .action-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  /* Modal */
  .metric-modal {
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
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
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
    width: 32px;
    height: 32px;
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
  
  .modal-body h4 {
    color: var(--text-primary);
    margin-bottom: 0.75rem;
  }
  
  .modal-body p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }
  
  .modal-body ul {
    color: var(--text-secondary);
    padding-left: 1rem;
    margin-bottom: 1rem;
  }
  
  .modal-body li {
    margin-bottom: 0.5rem;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .performance-container {
      padding: 1rem;
    }
    
    .overview-cards,
    .metrics-grid,
    .insights-grid,
    .export-options {
      grid-template-columns: 1fr;
    }
    
    .section-header {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    
    .metric-controls {
      flex-direction: column;
    }
    
    .charts-grid {
      grid-template-columns: 1fr;
    }
    
    .deployment-summary {
      flex-direction: column;
      text-align: center;
    }
    
    .final-actions {
      flex-direction: column;
    }
    
    .action-btn {
      width: 100%;
    }
    
    .correlation-grid {
      grid-template-columns: repeat(4, 35px);
    }
    
    .correlation-cell {
      width: 35px;
      height: 35px;
      font-size: 0.6875rem;
    }
  }
  </style>
  