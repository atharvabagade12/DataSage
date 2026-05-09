<template>
  <transition name="modal-fade">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-container comparison-modal glass custom-scrollbar">
        <div class="modal-header sticky-header">
          <div class="header-content">
            <div class="header-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
              </svg>
            </div>
            <div class="header-text">
              <h2>Intelligence Comparison</h2>
              <p>Deep-dive analysis of {{ models.length }} selected models</p>
            </div>
          </div>
          <button class="close-btn" @click="$emit('close')">&times;</button>
        </div>

        <div class="modal-body">
          <div v-if="datasetMismatch" class="mismatch-warning">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01"></path>
            </svg>
            <span>Warning: Models are trained on different datasets. Metrics may not be directly comparable.</span>
          </div>

          <!-- Metrics Comparison Table -->
          <div class="comparison-section">
            <div class="section-title">
              <h3>Performance Metrics</h3>
              <div class="title-line"></div>
            </div>
            
            <div class="table-responsive">
              <table class="comparison-table">
                <thead>
                  <tr>
                    <th class="metric-name-col">Metric</th>
                    <th v-for="model in models" :key="model.id" class="model-col">
                      <div class="model-header-stack">
                        <span class="algo-pill">{{ model.algorithm }}</span>
                        <span class="model-name-text">{{ model.name }}</span>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="metric in allAvailableMetrics" :key="metric.key">
                    <td class="metric-label-cell">
                      {{ metric.label }}
                      <span class="metric-key">{{ metric.key }}</span>
                    </td>
                    <td v-for="model in models" :key="model.id" 
                        :class="{ 'best-value': isBestMetric(model, metric.key) }">
                      {{ formatMetricValue(model.metrics?.[metric.key]) }}
                      <div v-if="isBestMetric(model, metric.key)" class="best-badge">BEST</div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Hyperparameters Comparison -->
          <div class="comparison-section">
            <div class="section-title">
              <h3>Hyperparameters</h3>
              <div class="title-line"></div>
            </div>
            
            <div class="table-responsive">
              <table class="comparison-table params-table">
                <thead>
                  <tr>
                    <th class="metric-name-col">Parameter</th>
                    <th v-for="model in models" :key="model.id" class="model-col">
                      <div class="model-name-mini">{{ model.name }}</div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="param in allAvailableParams" :key="param" :class="{ 'diff-row': hasParamDifference(param) }">
                    <td class="metric-label-cell">
                      {{ param }}
                    </td>
                    <td v-for="model in models" :key="model.id">
                      {{ formatParamValue(model.hyperparameters?.[param]) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Training Info -->
          <div class="comparison-section">
            <div class="section-title">
              <h3>Run Details</h3>
              <div class="title-line"></div>
            </div>
            <div class="table-responsive">
              <table class="comparison-table details-table">
                <tbody>
                  <tr>
                    <td class="metric-label-cell">Dataset</td>
                    <td v-for="model in models" :key="model.id">{{ getDatasetName(model.dataset_id) }}</td>
                  </tr>
                  <tr>
                    <td class="metric-label-cell">Validation</td>
                    <td v-for="model in models" :key="model.id">{{ model.metrics?.validation_method || 'simple' }}</td>
                  </tr>
                  <tr>
                    <td class="metric-label-cell">Trained</td>
                    <td v-for="model in models" :key="model.id">{{ getRelativeTime(model.createdAt) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-primary" @click="$emit('close')">Close Analysis</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: Boolean,
  models: {
    type: Array,
    default: () => []
  },
  datasets: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close'])

const datasetMismatch = computed(() => {
  if (props.models.length < 2) return false
  const firstId = props.models[0].dataset_id
  return props.models.some(m => m.dataset_id !== firstId)
})

const allAvailableMetrics = computed(() => {
  const keys = new Set()
  props.models.forEach(m => {
    if (m.metrics) {
      Object.keys(m.metrics).forEach(k => {
        if (k !== 'validation_method' && typeof m.metrics[k] === 'number') {
          keys.add(k)
        }
      })
    }
  })
  
  const metricLabels = {
    accuracy: 'Accuracy',
    test_accuracy: 'Test Accuracy',
    f1: 'F1 Score',
    test_f1: 'Test F1',
    precision: 'Precision',
    test_precision: 'Test Precision',
    recall: 'Recall',
    test_recall: 'Test Recall',
    r2: 'R² Score',
    test_r2: 'Test R²',
    mae: 'MAE',
    test_mae: 'Test MAE',
    rmse: 'RMSE',
    test_rmse: 'Test RMSE',
    mse: 'MSE',
    test_mse: 'Test MSE',
    cv_mean: 'CV Mean',
    best_score: 'Best Score'
  }

  return Array.from(keys).map(k => ({
    key: k,
    label: metricLabels[k] || k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  })).sort((a, b) => {
    // Sort to keep accuracy/r2 at top
    const top = ['accuracy', 'test_accuracy', 'r2', 'test_r2']
    const aIdx = top.indexOf(a.key)
    const bIdx = top.indexOf(b.key)
    if (aIdx !== -1 && bIdx !== -1) return aIdx - bIdx
    if (aIdx !== -1) return -1
    if (bIdx !== -1) return 1
    return a.label.localeCompare(b.label)
  })
})

const allAvailableParams = computed(() => {
  const keys = new Set()
  props.models.forEach(m => {
    if (m.hyperparameters) {
      Object.keys(m.hyperparameters).forEach(k => keys.add(k))
    }
  })
  return Array.from(keys).sort()
})

const isBestMetric = (model, key) => {
  if (props.models.length < 2) return false
  const val = model.metrics?.[key]
  if (val === undefined || val === null) return false
  
  const lowerIsBetter = ['mae', 'mse', 'rmse', 'test_mae', 'test_mse', 'test_rmse'].includes(key)
  
  let bestVal = val
  let isBest = true
  
  props.models.forEach(m => {
    const otherVal = m.metrics?.[key]
    if (otherVal === undefined || otherVal === null) return
    if (lowerIsBetter) {
      if (otherVal < bestVal) isBest = false
    } else {
      if (otherVal > bestVal) isBest = false
    }
  })
  
  // Check if it's the uniquely best or tied for best
  // For simplicity, we mark all tied bests
  return isBest
}

const hasParamDifference = (param) => {
  if (props.models.length < 2) return false
  const firstVal = JSON.stringify(props.models[0].hyperparameters?.[param])
  return props.models.some(m => JSON.stringify(m.hyperparameters?.[param]) !== firstVal)
}

const formatMetricValue = (val) => {
  if (val === undefined || val === null) return '-'
  if (typeof val !== 'number') return val
  return val < 1 ? val.toFixed(4) : val.toFixed(2)
}

const formatParamValue = (val) => {
  if (val === undefined || val === null) return '-'
  if (typeof val === 'boolean') return val ? 'True' : 'False'
  if (typeof val === 'object') return JSON.stringify(val)
  return val
}

const getDatasetName = (id) => {
  const ds = props.datasets.find(d => String(d.id) === String(id))
  return ds ? ds.name : `ID: ${id}`
}

const getRelativeTime = (dateStr) => {
  if (!dateStr) return '-'
  const now = new Date()
  const past = new Date(dateStr)
  const diff = Math.floor((now - past) / 1000)
  
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(5, 5, 15, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
}

.modal-container {
  width: 100%;
  max-width: 1100px;
  max-height: 90vh;
  background: rgba(15, 15, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);
}

.sticky-header {
  position: sticky;
  top: 0;
  background: rgba(15, 15, 30, 0.98);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.header-icon {
  width: 44px;
  height: 44px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
}

.header-text h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0;
  color: #ffffff;
}

.header-text p {
  font-size: 0.9rem;
  color: #6a6a8a;
  margin: 4px 0 0;
}

.close-btn {
  background: none;
  border: none;
  color: #6a6a8a;
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover { color: #ffffff; }

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.mismatch-warning {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.comparison-section {
  margin-bottom: 3rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-title h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #a88beb;
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}

.title-line {
  height: 1px;
  background: linear-gradient(to right, rgba(168, 139, 235, 0.2), transparent);
  flex: 1;
}

.table-responsive {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(255, 255, 255, 0.01);
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.comparison-table th, .comparison-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.metric-name-col { width: 250px; }
.model-col { min-width: 200px; }

.model-header-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.algo-pill {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  width: fit-content;
}

.model-name-text {
  font-weight: 700;
  color: #ffffff;
}

.metric-label-cell {
  font-weight: 600;
  color: #b3b3d1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-key {
  font-size: 0.65rem;
  color: #4a4a6a;
  font-family: monospace;
}

.best-value {
  color: #10b981;
  font-weight: 800;
  position: relative;
}

.best-badge {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  font-size: 0.6rem;
  padding: 2px 6px;
  background: #10b981;
  color: #ffffff;
  border-radius: 4px;
  letter-spacing: 0.5px;
}

.params-table td {
  font-family: monospace;
  font-size: 0.85rem;
}

.model-name-mini {
  font-size: 0.85rem;
  font-weight: 700;
  color: #6a6a8a;
}

.diff-row {
  background: rgba(168, 139, 235, 0.03);
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.custom-scrollbar::-webkit-scrollbar { width: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }
</style>
