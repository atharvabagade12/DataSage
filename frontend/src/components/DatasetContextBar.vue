<template>
  <div v-if="hasDataset" class="dataset-context-bar">
    <div class="context-left">
      <button @click="goBack" class="back-btn" title="Go to previous step">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z" />
        </svg>
      </button>
      
      <div class="separator"></div>
      
      <div class="active-item dataset-info">
        <!-- Table / dataset icon -->
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
          <path d="M5,4H19A2,2 0 0,1 21,6V18A2,2 0 0,1 19,20H5A2,2 0 0,1 3,18V6A2,2 0 0,1 5,4M5,8V12H11V8H5M13,8V12H19V8H13M5,14V18H11V14H5M13,14V18H19V14H13Z"/>
        </svg>
        <span class="file-name">{{ originalFileName }}</span>
      </div>
      
      <div class="separator"></div>
      
      <div class="active-item metadata">
        <div class="meta-pill">
          <strong>{{ rowCount.toLocaleString() }}</strong> rows
        </div>
      </div>

      <div v-if="targetColumn" class="separator"></div>

      <div v-if="targetColumn" class="active-item metadata">
        <div class="meta-pill target">
          Target: <strong>{{ targetColumn }}</strong>
        </div>
      </div>
    </div>
    
    <div v-if="showSaveControls" class="context-right">
      <div class="status-indicator" :class="{ 'is-dirty': isDirty }">
        <span class="status-dot"></span>
        <span class="status-text">{{ isDirty ? 'Status: Unsaved Changes' : 'Status: Saved ✓' }}</span>
      </div>
      
      <button 
        @click="onSaveVersion" 
        class="save-btn" 
        :disabled="!isDirty"
        :class="{ pulse: isDirty }"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M17,3H5C3.89,3 3,3.9 3,5V19C3,20.1 3.89,21 5,21H19C20.1,21 21,20.1 21,19V7L17,3M12,19A3,3 0 0,1 9,16A3,3 0 0,1 12,13A3,3 0 0,1 15,16A3,3 0 0,1 12,19M15,9H5V5H15V9Z" />
        </svg>
        Save Dataset Version
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMLDataFlowStore } from '~/stores/mlDataFlow'
import { useExperimentStore } from '~/stores/experiment'

const router = useRouter()
const route = useRoute()
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()

// Pages where the save controls (status + save button) should be hidden
const SAVE_HIDDEN_ROUTES = ['algorithm-select', 'model-training', 'model-visualization']

const hasDataset = computed(() => !!mlStore.datasetId)

// Always show the ORIGINAL uploaded file name, never the saved version name
const originalFileName = computed(() => {
  // mlStore.fileName holds the original upload filename and is NOT updated on save
  return mlStore.fileName
})

const isDirty = computed(() => mlStore.isDirty)

// Whether to show the status indicator and save button
const showSaveControls = computed(() => {
  return !SAVE_HIDDEN_ROUTES.includes(route.name)
})

const rowCount = computed(() => {
  // 1. If dataset is split, use trainRows + testRows (reflects SMOTE changes)
  if (mlStore.isSplit && mlStore.splitInfo) {
    const train = mlStore.splitInfo.trainRows || 0
    const test = mlStore.splitInfo.testRows || 0
    if (train + test > 0) return train + test
  }

  // 2. Fallback: in-memory dataset array length
  if (mlStore.dataset && mlStore.dataset.length > 0) return mlStore.dataset.length
  
  // 3. Fallback to registeredDatasets (if available)
  const registered = mlStore.registeredDatasets[mlStore.datasetId]
  if (registered?.shape?.[0]) return registered.shape[0]
  if (registered?.row_count) return registered.row_count
  
  // 4. Fallback to allUserDatasets (from dashboard view)
  const meta = mlStore.allUserDatasets?.find(d => d.id === mlStore.datasetId || d.dataset_id === mlStore.datasetId)
  if (meta) {
    return meta.row_count || meta.rows || meta.total_rows || (meta.shape?.[0]) || 0
  }
  
  return 0
})

const targetColumn = computed(() => {
  const fromExperiment = experimentStore.targetColumn;
  if (fromExperiment) {
    return typeof fromExperiment === 'object' ? (fromExperiment.name || fromExperiment.label) : fromExperiment;
  }
  return mlStore.targetColumn;
})

const emit = defineEmits(['save-version'])

const onSaveVersion = () => {
  emit('save-version')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.dataset-context-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(18, 18, 38, 0.7);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  height: 48px;
  backdrop-filter: blur(8px);
  z-index: 1000;
  position: relative;
}

.context-left { display: flex; align-items: center; gap: 16px; }

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #b3b3d1;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(-2px);
}

.active-item { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #b3b3d1; }
.active-item strong { color: #ffffff; }

.separator { width: 1px; height: 16px; background: rgba(255, 255, 255, 0.1); }

.version-badge { 
    background: rgba(102, 126, 234, 0.15); 
    color: #667eea; 
    padding: 2px 8px; 
    border-radius: 4px; 
    font-size: 0.75rem; 
    font-weight: 700; 
    border: 1px solid rgba(102, 126, 234, 0.2);
}

.meta-pill { 
    background: rgba(255, 255, 255, 0.04); 
    padding: 4px 10px; 
    border-radius: 100px; 
    font-size: 0.78rem; 
    border: 1px solid rgba(255, 255, 255, 0.03); 
}
.meta-pill.target { background: rgba(234, 179, 8, 0.05); color: #eab308; border-color: rgba(234, 179, 8, 0.1); }
.meta-pill.algorithm { background: rgba(139, 92, 246, 0.05); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.1); }

.context-right { display: flex; align-items: center; gap: 20px; }

.status-indicator { display: flex; align-items: center; gap: 8px; font-size: 0.78rem; font-weight: 600; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: #10b981; }
.status-text { color: #10b981; }

.status-indicator.is-dirty .status-dot { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
.status-indicator.is-dirty .status-text { color: #f59e0b; }

.save-btn { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border: none; 
    padding: 6px 14px; 
    border-radius: 7px; 
    display: flex; 
    align-items: center; 
    gap: 6px; 
    font-size: 0.8rem;
    font-weight: 700; 
    cursor: pointer; 
    transition: all 0.3s ease; 
    box-shadow: 0 4px 12px rgba(118, 75, 162, 0.3);
}

.save-btn:disabled { 
    background: #2a2a3a; 
    color: #5a5a7a; 
    box-shadow: none; 
    cursor: default; 
    opacity: 0.7;
}

.save-btn:not(:disabled):hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(118, 75, 162, 0.4); }

.pulse { animation: pulse-shadow 2s infinite; }
@keyframes pulse-shadow {
  0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
  100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}

@media (max-width: 992px) {
    .metadata { display: none; }
}
</style>
