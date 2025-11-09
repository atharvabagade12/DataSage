<template>
    <div class="preprocessing-container">
      <!-- Header -->
      <div class="preprocessing-header">
        <h2>🔧 Data Preprocessing</h2>
        <p>Clean and transform your data for optimal machine learning performance</p>
      </div>
  
      <div class="preprocessing-content">
        <!-- Preprocessing Steps Overview -->
        <div class="steps-overview">
          <h3>📋 Preprocessing Pipeline</h3>
          <div class="pipeline-flow">
            <div 
              v-for="(step, index) in preprocessingSteps" 
              :key="step.id"
              class="pipeline-step"
              :class="{ 
                active: step.enabled,
                processing: step.processing,
                completed: step.completed,
                error: step.error
              }"
              @click="toggleStep(step)"
            >
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-content">
                <h4>{{ step.name }}</h4>
                <p>{{ step.description }}</p>
                <div class="step-meta">
                  <span class="step-impact" :class="step.impact">{{ step.impact }} impact</span>
                  <span class="step-status">{{ getStepStatus(step) }}</span>
                </div>
              </div>
              <div class="step-toggle">
                <input 
                  type="checkbox" 
                  :checked="step.enabled" 
                  @click.stop
                  @change="toggleStep(step)"
                  class="step-checkbox"
                />
              </div>
            </div>
          </div>
        </div>
  
        <!-- Configuration Tabs -->
        <div class="config-tabs">
          <button 
            v-for="tab in configTabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="['tab-btn', { active: activeTab === tab.id }]"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>
  
        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Missing Values Tab -->
          <div v-if="activeTab === 'missing'" class="tab-panel">
            <div class="missing-values-config">
              <h4>❌ Handle Missing Values</h4>
              <p>Configure how to handle missing data in your dataset</p>
  
              <div class="missing-columns" v-if="columnsWithMissing.length > 0">
                <div v-for="column in columnsWithMissing" :key="column.name" class="column-config">
                  <div class="column-header">
                    <h5>{{ column.name }}</h5>
                    <div class="missing-stats">
                      <span class="missing-count">{{ column.missingCount }} missing</span>
                      <span class="missing-percent">({{ column.missingPercent }}%)</span>
                    </div>
                  </div>
                  
                  <div class="strategy-selector">
                    <label>Strategy:</label>
                    <select v-model="column.strategy" @change="updateMissingStrategy(column)">
                      <option value="drop">Drop rows</option>
                      <option value="mean" v-if="column.type === 'numeric'">Fill with mean</option>
                      <option value="median" v-if="column.type === 'numeric'">Fill with median</option>
                      <option value="mode">Fill with mode</option>
                      <option value="constant">Fill with constant</option>
                      <option value="forward">Forward fill</option>
                      <option value="backward">Backward fill</option>
                      <option value="interpolate" v-if="column.type === 'numeric'">Interpolate</option>
                    </select>
                    
                    <input 
                      v-if="column.strategy === 'constant'"
                      v-model="column.constantValue"
                      type="text"
                      placeholder="Enter constant value"
                      class="constant-input"
                    />
                  </div>
  
                  <div class="preview-impact">
                    <span class="impact-text">Impact: {{ getMissingImpact(column) }}</span>
                  </div>
                </div>
              </div>
  
              <div v-else class="no-missing">
                <div class="success-message">
                  <span class="success-icon">✅</span>
                  <span>Great! No missing values detected in your dataset.</span>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Outliers Tab -->
          <div v-if="activeTab === 'outliers'" class="tab-panel">
            <div class="outliers-config">
              <h4>📊 Detect & Handle Outliers</h4>
              <p>Identify and manage outliers in numeric columns</p>
  
              <div class="outlier-methods">
                <div class="method-selector">
                  <label>Detection Method:</label>
                  <select v-model="outlierMethod" @change="updateOutlierDetection">
                    <option value="iqr">IQR (Interquartile Range)</option>
                    <option value="zscore">Z-Score</option>
                    <option value="isolation">Isolation Forest</option>
                    <option value="lof">Local Outlier Factor</option>
                  </select>
                </div>
  
                <div class="threshold-config" v-if="outlierMethod === 'zscore'">
                  <label>Z-Score Threshold:</label>
                  <input 
                    v-model.number="zscoreThreshold" 
                    type="number" 
                    min="1" 
                    max="4" 
                    step="0.1"
                    @input="updateOutlierDetection"
                  />
                </div>
  
                <div class="threshold-config" v-if="outlierMethod === 'iqr'">
                  <label>IQR Multiplier:</label>
                  <input 
                    v-model.number="iqrMultiplier" 
                    type="number" 
                    min="1" 
                    max="3" 
                    step="0.1"
                    @input="updateOutlierDetection"
                  />
                </div>
              </div>
  
              <div class="outlier-columns" v-if="numericColumns.length > 0">
                <div v-for="column in outlierAnalysis" :key="column.name" class="outlier-column">
                  <div class="column-header">
                    <h5>{{ column.name }}</h5>
                    <div class="outlier-stats">
                      <span class="outlier-count">{{ column.outlierCount }} outliers</span>
                      <span class="outlier-percent">({{ column.outlierPercent }}%)</span>
                    </div>
                  </div>
  
                  <div class="outlier-visualization">
                    <div class="box-plot">
                      <div class="whisker-left" :style="{ left: '10%' }"></div>
                      <div class="box" :style="{ left: '25%', width: '50%' }"></div>
                      <div class="whisker-right" :style="{ left: '75%' }"></div>
                      <div 
                        v-for="(outlier, index) in column.outliers.slice(0, 10)" 
                        :key="index"
                        class="outlier-point" 
                        :style="{ left: `${outlier.position}%` }"
                        :title="`Value: ${outlier.value}`"
                      ></div>
                    </div>
                  </div>
  
                  <div class="outlier-strategy">
                    <label>Action:</label>
                    <select v-model="column.action" @change="updateOutlierStrategy(column)">
                      <option value="keep">Keep outliers</option>
                      <option value="remove">Remove outliers</option>
                      <option value="cap">Cap values</option>
                      <option value="transform">Log transform</option>
                      <option value="winsorize">Winsorize</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Encoding Tab -->
          <div v-if="activeTab === 'encoding'" class="tab-panel">
            <div class="encoding-config">
              <h4>🔢 Feature Encoding</h4>
              <p>Convert categorical variables into numeric format</p>
  
              <div class="categorical-columns" v-if="categoricalColumns.length > 0">
                <div v-for="column in encodingConfig" :key="column.name" class="encoding-column">
                  <div class="column-header">
                    <h5>{{ column.name }}</h5>
                    <div class="category-stats">
                      <span class="unique-count">{{ column.uniqueValues }} unique values</span>
                      <span class="cardinality" :class="column.cardinalityLevel">{{ column.cardinalityLevel }} cardinality</span>
                    </div>
                  </div>
  
                  <div class="encoding-method">
                    <label>Encoding Method:</label>
                    <select v-model="column.method" @change="updateEncodingMethod(column)">
                      <option value="onehot">One-Hot Encoding</option>
                      <option value="label">Label Encoding</option>
                      <option value="ordinal">Ordinal Encoding</option>
                      <option value="target" v-if="hasTargetColumn">Target Encoding</option>
                      <option value="binary">Binary Encoding</option>
                      <option value="frequency">Frequency Encoding</option>
                    </select>
                  </div>
  
                  <div v-if="column.method === 'ordinal'" class="ordinal-config">
                    <label>Define Order (drag to reorder):</label>
                    <div class="ordinal-values">
                      <div 
                        v-for="(value, index) in column.ordinalOrder" 
                        :key="value"
                        class="ordinal-item"
                        draggable="true"
                        @dragstart="startDrag(column, index)"
                        @dragover.prevent
                        @drop="onDrop(column, index)"
                      >
                        <span class="drag-handle">⋮⋮</span>
                        <span class="ordinal-value">{{ value }}</span>
                        <span class="ordinal-rank">{{ index + 1 }}</span>
                      </div>
                    </div>
                  </div>
  
                  <div class="encoding-preview">
                    <h6>Preview:</h6>
                    <div class="preview-samples">
                      <div v-for="sample in column.previewSamples" :key="sample.original" class="sample-item">
                        <span class="original">{{ sample.original }}</span>
                        <span class="arrow">→</span>
                        <span class="encoded">{{ sample.encoded }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
  
              <div v-else class="no-categorical">
                <div class="info-message">
                  <span class="info-icon">ℹ️</span>
                  <span>No categorical columns detected. Encoding step will be skipped.</span>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Scaling Tab -->
          <div v-if="activeTab === 'scaling'" class="tab-panel">
            <div class="scaling-config">
              <h4>📏 Feature Scaling</h4>
              <p>Normalize numeric features for better model performance</p>
  
              <div class="scaling-method">
                <label>Scaling Method:</label>
                <select v-model="scalingMethod" @change="updateScalingMethod">
                  <option value="standard">StandardScaler (Z-score normalization)</option>
                  <option value="minmax">MinMaxScaler (0-1 scaling)</option>
                  <option value="robust">RobustScaler (median-based)</option>
                  <option value="quantile">QuantileTransformer</option>
                  <option value="power">PowerTransformer (Yeo-Johnson)</option>
                  <option value="none">No scaling</option>
                </select>
              </div>
  
              <div class="scaling-info">
                <div class="method-description">
                  <h6>{{ getScalingDescription().title }}</h6>
                  <p>{{ getScalingDescription().description }}</p>
                  <div class="pros-cons">
                    <div class="pros">
                      <strong>Pros:</strong>
                      <ul>
                        <li v-for="pro in getScalingDescription().pros" :key="pro">{{ pro }}</li>
                      </ul>
                    </div>
                    <div class="cons">
                      <strong>Cons:</strong>
                      <ul>
                        <li v-for="con in getScalingDescription().cons" :key="con">{{ con }}</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
  
              <div class="scaling-columns" v-if="numericColumns.length > 0">
                <h5>Columns to Scale:</h5>
                <div class="column-checkboxes">
                  <div v-for="column in numericColumns" :key="column" class="column-checkbox">
                    <input 
                      type="checkbox" 
                      :id="`scale-${column}`"
                      v-model="scalingColumns"
                      :value="column"
                      @change="updateScalingColumns"
                    />
                    <label :for="`scale-${column}`">{{ column }}</label>
                  </div>
                </div>
              </div>
  
              <div class="scaling-preview" v-if="scalingPreview.length > 0">
                <h6>Scaling Preview:</h6>
                <div class="preview-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Column</th>
                        <th>Original Range</th>
                        <th>Scaled Range</th>
                        <th>Sample Before</th>
                        <th>Sample After</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="preview in scalingPreview" :key="preview.column">
                        <td>{{ preview.column }}</td>
                        <td>{{ preview.originalRange }}</td>
                        <td>{{ preview.scaledRange }}</td>
                        <td>{{ preview.sampleBefore }}</td>
                        <td>{{ preview.sampleAfter }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Processing Summary -->
        <div class="processing-summary">
          <h4>📄 Processing Summary</h4>
          <div class="summary-stats">
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-content">
                <h5>{{ enabledStepsCount }}</h5>
                <p>Steps Enabled</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">⏱️</div>
              <div class="stat-content">
                <h5>{{ estimatedTime }}</h5>
                <p>Est. Time</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">💾</div>
              <div class="stat-content">
                <h5>{{ estimatedDataSize }}</h5>
                <p>Result Size</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-content">
                <h5>{{ qualityScore }}%</h5>
                <p>Quality Score</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="preprocessing-actions">
          <button 
            @click="previewProcessing" 
            class="action-btn secondary"
            :disabled="enabledStepsCount === 0 || isProcessing"
          >
            👁️ Preview Changes
          </button>
          
          <button 
            @click="startProcessing" 
            class="action-btn primary"
            :disabled="enabledStepsCount === 0 || isProcessing"
          >
            🚀 Apply Processing
          </button>
          
          <button 
            @click="resetConfig" 
            class="action-btn tertiary"
            :disabled="isProcessing"
          >
            🔄 Reset Configuration
          </button>
        </div>
      </div>
  
      <!-- Processing Modal -->
      <div v-if="isProcessing" class="processing-modal">
        <div class="processing-content">
          <div class="processing-header">
            <h3>⚡ Processing Data</h3>
            <p>Applying {{ enabledStepsCount }} preprocessing steps...</p>
          </div>
  
          <div class="processing-steps">
            <div 
              v-for="(step, index) in enabledSteps" 
              :key="step.id"
              class="processing-step"
              :class="{ 
                current: currentProcessingStep === index,
                completed: currentProcessingStep > index,
                pending: currentProcessingStep < index 
              }"
            >
              <div class="step-indicator">
                <span v-if="currentProcessingStep > index">✅</span>
                <span v-else-if="currentProcessingStep === index" class="spinner-small">⏳</span>
                <span v-else>{{ index + 1 }}</span>
              </div>
              <div class="step-info">
                <h5>{{ step.name }}</h5>
                <p v-if="currentProcessingStep === index">{{ step.processingMessage }}</p>
              </div>
            </div>
          </div>
  
          <div class="overall-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${overallProgress}%` }"></div>
            </div>
            <div class="progress-text">{{ Math.round(overallProgress) }}% Complete</div>
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
  const activeTab = ref('missing')
  const isProcessing = ref(false)
  const currentProcessingStep = ref(-1)
  
  // Configuration state
  const outlierMethod = ref('iqr')
  const zscoreThreshold = ref(3)
  const iqrMultiplier = ref(1.5)
  const scalingMethod = ref('standard')
  const scalingColumns = ref([])
  
  // Data
  const columnsWithMissing = ref([])
  const outlierAnalysis = ref([])
  const encodingConfig = ref([])
  const scalingPreview = ref([])
  
  // Drag and drop state
  const draggedItem = ref(null)
  const draggedIndex = ref(-1)
  
  // Configuration tabs
  const configTabs = [
    { id: 'missing', name: 'Missing Values', icon: '❌' },
    { id: 'outliers', name: 'Outliers', icon: '📊' },
    { id: 'encoding', name: 'Encoding', icon: '🔢' },
    { id: 'scaling', name: 'Scaling', icon: '📏' }
  ]
  
  // Preprocessing steps configuration
  const preprocessingSteps = reactive([
    {
      id: 'missing',
      name: 'Handle Missing Values',
      description: 'Deal with null/empty values in dataset',
      enabled: false,
      completed: false,
      processing: false,
      error: false,
      impact: 'high',
      processingMessage: 'Handling missing values...'
    },
    {
      id: 'outliers',
      name: 'Detect Outliers',
      description: 'Identify and handle outlying data points',
      enabled: false,
      completed: false,
      processing: false,
      error: false,
      impact: 'medium',
      processingMessage: 'Detecting and handling outliers...'
    },
    {
      id: 'encoding',
      name: 'Encode Categories',
      description: 'Convert categorical variables to numeric',
      enabled: false,
      completed: false,
      processing: false,
      error: false,
      impact: 'high',
      processingMessage: 'Encoding categorical features...'
    },
    {
      id: 'scaling',
      name: 'Scale Features',
      description: 'Normalize numeric feature ranges',
      enabled: false,
      completed: false,
      processing: false,
      error: false,
      impact: 'medium',
      processingMessage: 'Scaling numeric features...'
    }
  ])
  
  // Computed properties
  const dataset = computed(() => props.pipelineState.dataset)
  const columnAnalysis = computed(() => props.pipelineState.columnAnalysis || [])
  
  const numericColumns = computed(() => {
    return columnAnalysis.value
      .filter(col => col.type === 'numeric')
      .map(col => col.name)
  })
  
  const categoricalColumns = computed(() => {
    return columnAnalysis.value
      .filter(col => col.type === 'categorical')
      .map(col => col.name)
  })
  
  const hasTargetColumn = computed(() => {
    return props.pipelineState.targetColumn !== null
  })
  
  const enabledSteps = computed(() => {
    return preprocessingSteps.filter(step => step.enabled)
  })
  
  const enabledStepsCount = computed(() => {
    return enabledSteps.value.length
  })
  
  const estimatedTime = computed(() => {
    const baseTime = enabledSteps.value.reduce((time, step) => {
      const stepTimes = {
        missing: 5,
        outliers: 10,
        encoding: 8,
        scaling: 3
      }
      return time + (stepTimes[step.id] || 5)
    }, 0)
    
    const datasetSize = dataset.value?.length || 0
    const sizeFactor = datasetSize > 10000 ? 2 : datasetSize > 1000 ? 1.5 : 1
    
    return `${Math.round(baseTime * sizeFactor)}s`
  })
  
  const hasActiveTools = computed(() => {
      return activeTools.value.length > 0
  })

  // 🔥 NEW: Dynamic computed properties that reflect current dataset state
const currentDataset = computed(() => {
  return hasCleanedData.value ? cleanedDataset.value : originalDataset.value;
});

const currentColumns = computed(() => {
  if (!hasCleanedData.value) {
    return columns.value;
  }
  // Return columns based on cleaned dataset
  if (cleanedDataset.value.length > 0) {
    const cleanedColNames = Object.keys(cleanedDataset.value[0]);
    return columns.value.filter(col => cleanedColNames.includes(col.name));
  }
  return columns.value;
});

const currentDataInfo = computed(() => ({
  rows: currentDataset.value.length,
  columns: currentColumns.value.length,
}));

const currentDataQuality = computed(() => {
  const dataset = currentDataset.value;
  const cols = currentColumns.value;
  
  if (!dataset.length || !cols.length) return { score: 0 };

  const totalCells = dataset.length * cols.length;
  let issues = 0;

  dataset.forEach((row) => {
    cols.forEach((col) => {
      const value = row[col.name];
      if (value === null || value === undefined || value === "" || value === "null") {
        issues++;
      }
    });
  });

  const score = Math.max(0, Math.round(((totalCells - issues) / totalCells) * 100));
  return { score };
});

// 🔥 Calculate missing values for CURRENT dataset
const currentMissingColumnsDetailed = computed(() => {
  const dataset = currentDataset.value;
  const cols = currentColumns.value;
  const missing = [];
  
  if (!dataset.length || !cols.length) return missing;
  
  cols.forEach(col => {
    let missingCount = 0;
    
    dataset.forEach(row => {
      const value = row[col.name];
      if (value === null || value === undefined || value === '' || value === 'null' || value === 'NaN') {
        missingCount++;
      }
    });
    
    if (missingCount > 0) {
      missing.push({
        name: col.name,
        type: col.type,
        count: missingCount,
        percentage: ((missingCount / dataset.length) * 100).toFixed(1),
        strategy: col.type === 'numerical' ? 'fillmedian' : 'fillmode'
      });
    }
  });
  
  return missing.sort((a, b) => b.count - a.count);
});

const currentMissingStats = computed(() => {
  return {
    count: currentMissingColumnsDetailed.value.length,
    totalMissing: currentMissingColumnsDetailed.value.reduce((sum, col) => sum + col.count, 0)
  }
});

// 🔥 Calculate duplicates for CURRENT dataset
const currentDuplicateStats = computed(() => {
  const dataset = currentDataset.value;
  const seen = new Set();
  let count = 0;

  dataset.forEach((row) => {
    const rowString = JSON.stringify(row);
    if (seen.has(rowString)) {
      count++;
    } else {
      seen.add(rowString);
    }
  });

  return { count };
});

// 🔥 Calculate outliers for CURRENT dataset
const currentOutlierStats = computed(() => {
  const dataset = currentDataset.value;
  const cols = currentColumns.value;
  let count = 0;
  
  cols.filter((col) => col.type === "numerical")
    .forEach((col) => {
      const values = dataset
        .map((row) => parseFloat(row[col.name]))
        .filter((val) => !isNaN(val));

      if (values.length > 0) {
        const sorted = [...values].sort((a, b) => a - b);
        const q1 = sorted[Math.floor(sorted.length * 0.25)];
        const q3 = sorted[Math.floor(sorted.length * 0.75)];
        const iqr = q3 - q1;
        const lowerBound = q1 - 1.5 * iqr;
        const upperBound = q3 + 1.5 * iqr;

        count += values.filter((val) => val < lowerBound || val > upperBound).length;
      }
    });

  return { count };
});

// 🔥 Get categorical columns from CURRENT dataset
const currentCategoricalColumns = computed(() => {
  return currentColumns.value.filter((col) => col.type === "categorical");
});

  const estimatedDataSize = computed(() => {
    let sizeFactor = 1
    
    // Encoding can significantly increase size
    if (enabledSteps.value.some(step => step.id === 'encoding')) {
      const avgCardinality = encodingConfig.value.reduce((sum, col) => {
        return sum + (col.method === 'onehot' ? col.uniqueValues : 1)
      }, 0) / (encodingConfig.value.length || 1)
      sizeFactor *= Math.max(1.2, avgCardinality / 5)
    }
    
    const originalSize = props.pipelineState.datasetInfo?.size || 0
    return formatFileSize(originalSize * sizeFactor)
  })
  
  const qualityScore = computed(() => {
    let score = 85 // Base score
    
    if (enabledSteps.value.some(step => step.id === 'missing')) score += 5
    if (enabledSteps.value.some(step => step.id === 'outliers')) score += 3
    if (enabledSteps.value.some(step => step.id === 'encoding')) score += 4
    if (enabledSteps.value.some(step => step.id === 'scaling')) score += 3
    
    return Math.min(100, score)
  })
  
  const overallProgress = computed(() => {
    if (!isProcessing.value) return 0
    if (currentProcessingStep.value < 0) return 0
    
    const stepProgress = (currentProcessingStep.value / enabledSteps.value.length) * 100
    const withinStepProgress = 100 / enabledSteps.value.length
    
    return Math.min(100, stepProgress + (withinStepProgress * 0.5))
  })
  
  // Methods
  const formatFileSize = (bytes) => {
    if (!bytes) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }
  
  const getStepStatus = (step) => {
    if (step.error) return 'Error'
    if (step.processing) return 'Processing...'
    if (step.completed) return 'Completed'
    if (step.enabled) return 'Ready'
    return 'Disabled'
  }
  
  const toggleStep = (step) => {
    if (isProcessing.value) return
    
    step.enabled = !step.enabled
    
    // Auto-enable dependent steps
    if (step.enabled && step.id === 'missing') {
      // If missing values step is enabled, update missing columns config
      initializeMissingConfig()
    }
    
    if (step.enabled && step.id === 'encoding') {
      // Initialize encoding config
      initializeEncodingConfig()
    }
  }

  const getColumnsToKeep = () => {
  return columns.value.filter(col => !col.remove)
}

const getColumnsToRemove = () => {
  return columns.value.filter(col => col.remove)
}

const selectNoColumns = () => {
  columns.value.forEach(col => col.remove = false)
}

const selectAllColumns = () => {
  if (confirm('Are you sure you want to remove ALL columns? This will make your dataset unusable.')) {
    columns.value.forEach(col => col.remove = true)
  }
}
  
  const initializeMissingConfig = () => {
    columnsWithMissing.value = columnAnalysis.value
      .filter(col => col.missingCount > 0)
      .map(col => ({
        name: col.name,
        type: col.type,
        missingCount: col.missingCount,
        missingPercent: Math.round((col.missingCount / (props.pipelineState.datasetInfo?.rows || 1)) * 100),
        strategy: col.type === 'numeric' ? 'mean' : 'mode',
        constantValue: ''
      }))
  }
  
  const initializeEncodingConfig = () => {
    encodingConfig.value = categoricalColumns.value.map(columnName => {
      const columnData = columnAnalysis.value.find(col => col.name === columnName)
      const uniqueValues = columnData?.unique || 0
      
      // Determine cardinality level
      let cardinalityLevel = 'low'
      if (uniqueValues > 50) cardinalityLevel = 'high'
      else if (uniqueValues > 10) cardinalityLevel = 'medium'
      
      // Get sample values from dataset
      const sampleValues = [...new Set(
        dataset.value?.slice(0, 100).map(row => row[columnName]).filter(v => v != null)
      )].slice(0, 10)
      
      return {
        name: columnName,
        uniqueValues,
        cardinalityLevel,
        method: uniqueValues > 10 ? 'label' : 'onehot',
        ordinalOrder: sampleValues,
        previewSamples: sampleValues.slice(0, 3).map((value, index) => ({
          original: value,
          encoded: getEncodingPreview(value, index, uniqueValues > 10 ? 'label' : 'onehot')
        }))
      }
    })
  }
  
  const getEncodingPreview = (value, index, method) => {
    switch (method) {
      case 'label':
        return index
      case 'onehot':
        return `[${Array(3).fill(0).map((_, i) => i === index ? 1 : 0).join(', ')}]`
      case 'ordinal':
        return index + 1
      default:
        return index
    }
  }
  
  const updateMissingStrategy = (column) => {
    // Update preview impact when strategy changes
    console.log(`Updated missing strategy for ${column.name}: ${column.strategy}`)
  }
  
  const getMissingImpact = (column) => {
    if (column.strategy === 'drop') {
      return `Remove ${column.missingCount} rows`
    }
    return `Fill ${column.missingCount} values`
  }
  
  const updateOutlierDetection = () => {
    // Simulate outlier detection
    setTimeout(() => {
      outlierAnalysis.value = numericColumns.value.map(columnName => {
        // Mock outlier detection results
        const outlierCount = Math.floor(Math.random() * 10)
        const totalRows = props.pipelineState.datasetInfo?.rows || 1000
        
        return {
          name: columnName,
          outlierCount,
          outlierPercent: Math.round((outlierCount / totalRows) * 100),
          outliers: Array(outlierCount).fill().map((_, i) => ({
            value: Math.random() * 1000,
            position: Math.random() * 80 + 10
          })),
          action: 'keep'
        }
      })
    }, 300)
  }
  
  const updateOutlierStrategy = (column) => {
    console.log(`Updated outlier strategy for ${column.name}: ${column.action}`)
  }
  
  const updateEncodingMethod = (column) => {
    // Update preview samples when encoding method changes
    column.previewSamples = column.previewSamples.map((sample, index) => ({
      original: sample.original,
      encoded: getEncodingPreview(sample.original, index, column.method)
    }))
  }
  
  const startDrag = (column, index) => {
    draggedItem.value = column
    draggedIndex.value = index
  }
  
  const onDrop = (column, dropIndex) => {
    if (draggedItem.value === column && draggedIndex.value !== dropIndex) {
      const item = column.ordinalOrder.splice(draggedIndex.value, 1)[0]
      column.ordinalOrder.splice(dropIndex, 0, item)
    }
    draggedItem.value = null
    draggedIndex.value = -1
  }
  
  const updateScalingMethod = () => {
    // Update scaling preview when method changes
    updateScalingPreview()
  }
  
  const updateScalingColumns = () => {
    updateScalingPreview()
  }
  
  const updateScalingPreview = () => {
    if (scalingColumns.value.length === 0) {
      scalingPreview.value = []
      return
    }
    
    scalingPreview.value = scalingColumns.value.map(columnName => {
      // Mock scaling preview data
      const originalMin = Math.random() * -100
      const originalMax = originalMin + Math.random() * 1000
      
      let scaledMin = originalMin
      let scaledMax = originalMax
      
      switch (scalingMethod.value) {
        case 'standard':
          scaledMin = -2.5
          scaledMax = 2.5
          break
        case 'minmax':
          scaledMin = 0
          scaledMax = 1
          break
        case 'robust':
          scaledMin = -1.5
          scaledMax = 1.5
          break
      }
      
      return {
        column: columnName,
        originalRange: `${originalMin.toFixed(2)} to ${originalMax.toFixed(2)}`,
        scaledRange: `${scaledMin.toFixed(2)} to ${scaledMax.toFixed(2)}`,
        sampleBefore: originalMin.toFixed(2),
        sampleAfter: scaledMin.toFixed(2)
      }
    })
  }
  
  const getScalingDescription = () => {
    const descriptions = {
      standard: {
        title: 'Standard Scaler (Z-score)',
        description: 'Standardizes features by removing the mean and scaling to unit variance.',
        pros: ['Preserves shape of distribution', 'Good for normally distributed data'],
        cons: ['Sensitive to outliers', 'May not bound values to specific range']
      },
      minmax: {
        title: 'Min-Max Scaler',
        description: 'Scales features to a fixed range, typically 0 to 1.',
        pros: ['Bounded values', 'Preserves relationships'],
        cons: ['Sensitive to outliers', 'May compress normal values']
      },
      robust: {
        title: 'Robust Scaler',
        description: 'Uses median and interquartile range, robust to outliers.',
        pros: ['Robust to outliers', 'Preserves relationships'],
        cons: ['May not normalize to standard range', 'Less common']
      },
      quantile: {
        title: 'Quantile Transformer',
        description: 'Maps features to uniform or normal distribution using quantiles.',
        pros: ['Reduces outlier impact', 'Can create uniform distribution'],
        cons: ['May lose original relationships', 'Complex interpretation']
      },
      power: {
        title: 'Power Transformer',
        description: 'Applies power transformation to make data more Gaussian.',
        pros: ['Makes data more normal', 'Good for skewed data'],
        cons: ['May not preserve relationships', 'Interpretation difficulty']
      },
      none: {
        title: 'No Scaling',
        description: 'Keep original feature scales unchanged.',
        pros: ['Preserves original meaning', 'Simple interpretation'],
        cons: ['May bias algorithms', 'Poor performance with distance-based methods']
      }
    }
    
    return descriptions[scalingMethod.value] || descriptions.none
  }
  
  const previewProcessing = () => {
    // Show preview of what will happen
    alert('Preview functionality coming soon! This will show you exactly what changes will be made.')
  }
  
  const startProcessing = async () => {
    if (enabledStepsCount.value === 0) return
    
    isProcessing.value = true
    currentProcessingStep.value = 0
    
    try {
      // Process each enabled step
      for (let i = 0; i < enabledSteps.value.length; i++) {
        currentProcessingStep.value = i
        const step = enabledSteps.value[i]
        
        step.processing = true
        
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Apply the step
        await applyProcessingStep(step)
        
        step.processing = false
        step.completed = true
      }
      
      // Mark preprocessing as complete
      emit('update:state', {
        preprocessingComplete: true,
        preprocessingSteps: preprocessingSteps.map(step => ({ ...step })),
        cleanedDataset: dataset.value // In real implementation, this would be the processed data
      })
      
      // Auto advance to next step
      setTimeout(() => {
        emit('next-step')
      }, 1000)
      
    } catch (error) {
      console.error('Preprocessing failed:', error)
      const currentStep = enabledSteps.value[currentProcessingStep.value]
      if (currentStep) {
        currentStep.error = true
        currentStep.processing = false
      }
    } finally {
      isProcessing.value = false
      currentProcessingStep.value = -1
    }
  }
  
  const applyProcessingStep = async (step) => {
    // This is where actual preprocessing would happen
    // For now, we'll just simulate the processing
    
    switch (step.id) {
      case 'missing':
        console.log('Processing missing values...')
        // Apply missing value strategies
        break
      case 'outliers':
        console.log('Processing outliers...')
        // Apply outlier handling
        break
      case 'encoding':
        console.log('Processing encoding...')
        // Apply categorical encoding
        break
      case 'scaling':
        console.log('Processing scaling...')
        // Apply feature scaling
        break
    }
  }
  
  const resetConfig = () => {
    if (confirm('Are you sure you want to reset all preprocessing configuration?')) {
      // Reset all steps
      preprocessingSteps.forEach(step => {
        step.enabled = false
        step.completed = false
        step.processing = false
        step.error = false
      })
      
      // Reset configurations
      columnsWithMissing.value = []
      outlierAnalysis.value = []
      encodingConfig.value = []
      scalingPreview.value = []
      scalingColumns.value = []
      
      console.log('Preprocessing configuration reset')
    }
  }
  
  // Watchers
  watch(outlierMethod, () => {
    updateOutlierDetection()
  })
  
  watch(numericColumns, () => {
    updateOutlierDetection()
    // Auto-select numeric columns for scaling
    scalingColumns.value = [...numericColumns.value]
    updateScalingPreview()
  }, { immediate: true })
  
  watch(categoricalColumns, () => {
    if (preprocessingSteps.find(s => s.id === 'encoding')?.enabled) {
      initializeEncodingConfig()
    }
  }, { immediate: true })
  
  // Lifecycle
  onMounted(() => {
    // Initialize configurations based on existing data
    if (columnAnalysis.value.length > 0) {
      initializeMissingConfig()
      updateOutlierDetection()
      
      // Auto-enable steps based on data characteristics
      if (columnsWithMissing.value.length > 0) {
        const missingStep = preprocessingSteps.find(s => s.id === 'missing')
        if (missingStep) missingStep.enabled = true
      }
      
      if (categoricalColumns.value.length > 0) {
        const encodingStep = preprocessingSteps.find(s => s.id === 'encoding')
        if (encodingStep) {
          encodingStep.enabled = true
          initializeEncodingConfig()
        }
      }
      
      if (numericColumns.value.length > 1) {
        const scalingStep = preprocessingSteps.find(s => s.id === 'scaling')
        if (scalingStep) scalingStep.enabled = true
      }
    }
  })
  </script>
  
  <style scoped>
  /* Use the same CSS variables and styling patterns from your dashboard */
  .preprocessing-container {
    padding: 2rem;
    height: 100%;
    overflow-y: auto;
    background: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .preprocessing-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .preprocessing-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: var(--primary-gradient);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--primary-color);
}

  
  .preprocessing-header p {
    color: var(--text-secondary);
    font-size: 1rem;
  }
  
  .steps-overview {
    margin-bottom: 2rem;
  }
  
  .steps-overview h3 {
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .pipeline-flow {
    display: grid;
    gap: 1rem;
  }
  
  .pipeline-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-normal);
  }
  
  .pipeline-step:hover {
    border-color: var(--border-medium);
    transform: translateY(-2px);
  }
  
  .pipeline-step.active {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
  }
  
  .pipeline-step.completed {
    border-color: var(--success-color);
    background: rgba(16, 185, 129, 0.1);
  }
  
  .pipeline-step.processing {
    border-color: var(--warning-color);
    background: rgba(245, 158, 11, 0.1);
    animation: pulse 2s infinite;
  }
  
  .pipeline-step.error {
    border-color: var(--error-color);
    background: rgba(239, 68, 68, 0.1);
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    background: var(--primary-gradient);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.1rem;
  }
  
  .pipeline-step.completed .step-number {
    background: var(--success-color);
  }
  
  .step-content {
    flex: 1;
  }
  
  .step-content h4 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .step-content p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }
  
  .step-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.75rem;
  }
  
  .step-impact {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-weight: 500;
  }
  
  .step-impact.high {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }
  
  .step-impact.medium {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }
  
  .step-impact.low {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .step-status {
    color: var(--text-tertiary);
  }
  
  .step-toggle {
    margin-left: auto;
  }
  
  .step-checkbox {
    width: 20px;
    height: 20px;
    cursor: pointer;
  }
  
  .config-tabs {
    display: flex;
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 0.5rem;
    margin-bottom: 2rem;
    border: 1px solid var(--border-light);
  }
  
  .tab-btn {
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
  
  .tab-btn:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
  }
  
  .tab-btn.active {
    background: var(--primary-gradient);
    color: white;
  }
  
  .tab-content {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    min-height: 500px;
  }
  
  .tab-panel {
    padding: 2rem;
  }
  
  .tab-panel h4 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .tab-panel p {
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }
  
  /* Missing Values Tab */
  .missing-columns {
    display: grid;
    gap: 1.5rem;
  }
  
  .column-config {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .column-header h5 {
    color: var(--text-primary);
  }
  
  .missing-stats {
    display: flex;
    gap: 0.5rem;
    font-size: 0.875rem;
  }
  
  .missing-count {
    color: var(--error-color);
    font-weight: 500;
  }
  
  .missing-percent {
    color: var(--text-tertiary);
  }
  
  .strategy-selector {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .strategy-selector label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .strategy-selector select,
  .constant-input {
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  .preview-impact {
    padding: 0.75rem;
    background: rgba(59, 130, 246, 0.1);
    border-radius: var(--radius-sm);
    border-left: 4px solid var(--info-color);
  }
  
  .impact-text {
    color: var(--info-color);
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .no-missing,
  .no-categorical {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
  }
  
  .success-message,
  .info-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    color: var(--text-secondary);
  }
  
  .success-icon {
    font-size: 1.5rem;
  }
  
  .info-icon {
    font-size: 1.5rem;
  }
  
  /* Outliers Tab */
  .outlier-methods {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
  }
  
  .method-selector,
  .threshold-config {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .method-selector label,
  .threshold-config label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .method-selector select,
  .threshold-config input {
    padding: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  .outlier-columns {
    display: grid;
    gap: 1.5rem;
  }
  
  .outlier-column {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .outlier-stats {
    display: flex;
    gap: 0.5rem;
    font-size: 0.875rem;
  }
  
  .outlier-count {
    color: var(--warning-color);
    font-weight: 500;
  }
  
  .outlier-percent {
    color: var(--text-tertiary);
  }
  
  .outlier-visualization {
    margin: 1rem 0;
  }
  
  .box-plot {
    position: relative;
    height: 40px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
    margin: 1rem 0;
  }
  
  .whisker-left,
  .whisker-right {
    position: absolute;
    top: 50%;
    width: 2px;
    height: 20px;
    background: var(--text-secondary);
    transform: translateY(-50%);
  }
  
  .box {
    position: absolute;
    top: 25%;
    height: 50%;
    background: var(--primary-color);
    opacity: 0.7;
    border-radius: 2px;
  }
  
  .outlier-point {
    position: absolute;
    top: 50%;
    width: 6px;
    height: 6px;
    background: var(--error-color);
    border-radius: 50%;
    transform: translateY(-50%);
    cursor: pointer;
  }
  
  .outlier-strategy {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .outlier-strategy label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .outlier-strategy select {
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  /* Encoding Tab */
  .categorical-columns {
    display: grid;
    gap: 1.5rem;
  }
  
  .encoding-column {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .category-stats {
    display: flex;
    gap: 0.5rem;
    font-size: 0.875rem;
  }
  
  .unique-count {
    color: var(--info-color);
    font-weight: 500;
  }
  
  .cardinality {
    padding: 0.125rem 0.375rem;
    border-radius: 12px;
    font-weight: 500;
    font-size: 0.75rem;
  }
  
  .cardinality.low {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .cardinality.medium {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
  }
  
  .cardinality.high {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }
  
  .encoding-method {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
  }
  
  .encoding-method label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .encoding-method select {
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
  }
  
  .ordinal-config {
    margin: 1rem 0;
  }
  
  .ordinal-config label {
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.5rem;
    display: block;
  }
  
  .ordinal-values {
    display: grid;
    gap: 0.5rem;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .ordinal-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    cursor: move;
  }
  
  .drag-handle {
    color: var(--text-tertiary);
    cursor: grab;
  }
  
  .drag-handle:active {
    cursor: grabbing;
  }
  
  .ordinal-value {
    flex: 1;
    color: var(--text-primary);
  }
  
  .ordinal-rank {
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.875rem;
  }
  
  .encoding-preview {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
  }
  
  .encoding-preview h6 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }
  
  .preview-samples {
    display: grid;
    gap: 0.5rem;
  }
  
  .sample-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
  }
  
  .original {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .arrow {
    color: var(--text-tertiary);
  }
  
  .encoded {
    color: var(--info-color);
    font-family: 'Monaco', 'Consolas', monospace;
  }
  
  /* Scaling Tab */
  .scaling-method {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .scaling-method label {
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .scaling-method select {
    padding: 0.75rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    min-width: 300px;
  }
  
  .scaling-info {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .method-description h6 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .method-description p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }
  
  .pros-cons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
  
  .pros,
  .cons {
    font-size: 0.875rem;
  }
  
  .pros strong,
  .cons strong {
    color: var(--text-primary);
  }
  
  .pros ul,
  .cons ul {
    margin-top: 0.5rem;
    padding-left: 1rem;
  }
  
  .pros li,
  .cons li {
    color: var(--text-secondary);
    margin-bottom: 0.25rem;
  }
  
  .scaling-columns {
    margin-bottom: 2rem;
  }
  
  .scaling-columns h5 {
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  .column-checkboxes {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
  }
  
  .column-checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .column-checkbox input {
    width: 16px;
    height: 16px;
  }
  
  .column-checkbox label {
    color: var(--text-primary);
    cursor: pointer;
  }
  
  .scaling-preview {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }
  
  .scaling-preview h6 {
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .preview-table {
    overflow-x: auto;
  }
  
  .preview-table table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }
  
  .preview-table th,
  .preview-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-light);
  }
  
  .preview-table th {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .preview-table td {
    color: var(--text-secondary);
  }
  
  /* Processing Summary */
  .processing-summary {
    margin: 2rem 0;
    padding: 1.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
  }
  
  .processing-summary h4 {
    margin-bottom: 1rem;
    color: var(--text-primary);
  }
  
  .summary-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }
  
  .stat-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }
  
  .stat-icon {
    font-size: 1.5rem;
  }
  
  .stat-content h5 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .stat-content p {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  /* Action Buttons */
  .preprocessing-actions {
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
  
  .action-btn.tertiary {
    background: none;
    color: var(--text-secondary);
    border: 1px solid var(--border-light);
  }
  
  .action-btn.tertiary:hover:not(:disabled) {
    color: var(--text-primary);
    border-color: var(--border-medium);
  }
  
  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }
  
  /* Processing Modal */
  .processing-modal {
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
  
  .processing-content {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 2rem;
    max-width: 500px;
    width: 90%;
  }
  
  .processing-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .processing-header h3 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }
  
  .processing-header p {
    color: var(--text-secondary);
  }
  
  .processing-steps {
    margin-bottom: 2rem;
  }
  
  .processing-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.5rem;
    transition: all var(--transition-normal);
  }
  
  .processing-step.current {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid var(--warning-color);
  }
  
  .processing-step.completed {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid var(--success-color);
  }
  
  .processing-step.pending {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    opacity: 0.6;
  }
  
  .step-indicator {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .processing-step.current .step-indicator {
    background: var(--warning-color);
    color: white;
  }
  
  .processing-step.completed .step-indicator {
    background: var(--success-color);
    color: white;
  }
  
  .processing-step.pending .step-indicator {
    background: var(--bg-tertiary);
    color: var(--text-tertiary);
  }
  
  .spinner-small {
    animation: spin 1s linear infinite;
  }
  
  .step-info h5 {
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  .step-info p {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  .overall-progress {
    text-align: center;
  }
  
  .progress-bar {
    height: 8px;
    background: var(--bg-tertiary);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }
  
  .progress-fill {
    height: 100%;
    background: var(--primary-gradient);
    transition: width 0.3s ease;
  }
  
  .progress-text {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  /* Animations */
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .preprocessing-container {
      padding: 1rem;
    }
    
    .config-tabs {
      flex-direction: column;
    }
    
    .tab-btn {
      text-align: left;
    }
    
    .pipeline-step {
      flex-direction: column;
      text-align: center;
    }
    
    .step-content {
      order: -1;
    }
    
    .outlier-methods,
    .method-selector {
      flex-direction: column;
      gap: 1rem;
    }
    
    .pros-cons {
      grid-template-columns: 1fr;
    }
    
    .summary-stats {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
    
    .preprocessing-actions {
      flex-direction: column;
    }
    
    .action-btn {
      width: 100%;
    }
  }
  </style>
  