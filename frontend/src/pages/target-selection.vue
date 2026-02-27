<template>
  <div class="target-selection">
    <PageHeader 
      title="Target Selection" 
      description="Choose the most relevant column to predict for your machine learning task."
    >
      <template #icon>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="22" y1="12" x2="18" y2="12"></line>
          <line x1="6" y1="12" x2="2" y2="12"></line>
          <line x1="12" y1="6" x2="12" y2="2"></line>
          <line x1="12" y1="22" x2="12" y2="18"></line>
        </svg>
      </template>
    </PageHeader>


    <!-- Main Content Grid -->
    <div class="main-content">
      <!-- Left Panel: Column Selector -->
      <ColumnSelector
        :columns="availableColumns"
        :selected-column="selectedColumn"
        @select="handleColumnSelect"
      />

      <!-- Center Panel: Data Preview & Chart -->
      <DataPreviewChart
        :selected-column="selectedColumn"
        :dataset="dataset"
      />

      <!-- Right Panel: Insights & Recommendations -->
      <TargetInsights
        :selected-column="selectedColumn"
        :dataset="dataset"
      />
    </div>

    <!-- Footer -->
    <footer class="action-footer">
      <div class="footer-content">
        <button @click="saveDraft" class="footer-btn secondary">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"
            />
            <polyline points="17 21 17 13 7 13 7 21" />
            <polyline points="7 3 7 8 15 8" />
          </svg>
          Save Draft
        </button>

        <button
          @click="continueToAdvancedPreprocessing"
          class="footer-btn continue-btn primary"
          :disabled="!selectedColumn"
        >
          Continue to Advanced Preprocessing
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </footer>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="global-loading">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>Analyzing dataset structure...</p>
      </div>
    </div>
  </div>
</template>

<script setup>


import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useMLDataFlowStore } from '../stores/mlDataFlow';
import { useDataStore } from '../stores/data';
import { useExperimentStore } from '../stores/experiment';
import { useAuthenticatedFetch } from '../composables/useAuthenticatedFetch';
import { useTargetAnalysis } from '../composables/useTargetAnalysis';
import PageHeader from '../components/PageHeader.vue';

// Components
import ColumnSelector from '../components/target-selection/ColumnSelector.vue';
import DataPreviewChart from '../components/target-selection/DataPreviewChart.vue';
import TargetInsights from '../components/target-selection/TargetInsights.vue';

const router = useRouter();
const mlStore = useMLDataFlowStore();
const dataStore = useDataStore();
const experimentStore = useExperimentStore();
const { authenticatedPost } = useAuthenticatedFetch();
const { processColumns } = useTargetAnalysis();

// Store Refs
const { backendConnected } = storeToRefs(mlStore);
const { rawPreview: dataset, statistics: dataStats, semanticTypes } = storeToRefs(dataStore);
const { datasetId } = storeToRefs(experimentStore);

// Local State
const isLoading = ref(true);
const selectedColumn = ref(null);
const availableColumns = ref([]);
const datasetInfo = ref({ rowCount: 0, columnCount: 0 });

// Methods
const handleColumnSelect = (column) => {
  selectedColumn.value = column;
};

const goBack = () => router.push("/data-preview");

const loadData = async () => {
  isLoading.value = true;
  try {
    // 1. Recovery Check
    if (!datasetId.value) {
       if (mlStore.datasetId) {
         experimentStore.setDataset(mlStore.datasetId, mlStore.fileName);
       } else {
         // Try legacy localStorage
         const stored = localStorage.getItem('processedData');
         if (stored) {
            const parsed = JSON.parse(stored);
            if (parsed.datasetId) {
               experimentStore.setDataset(parsed.datasetId, parsed.fileName || "Dataset");
            }
         }
       }
    }

    if (!datasetId.value) {
        router.push("/data-preview");
        return;
    }

    // 2. dataStore Load
    await dataStore.loadData(datasetId.value);
    
    // 3. Process Columns for UI
    processAvailableColumns();

  } catch (error) {
    console.error("Target Selection Load Error:", error);
  } finally {
    isLoading.value = false;
  }
};

const processAvailableColumns = () => {
    // Logic adapted from original setupColumnsFromDataset
    if (!dataset.value.length) return;

    datasetInfo.value = {
        rowCount: dataset.value.length,
        columnCount: Object.keys(dataset.value[0]).length
    };

    // 1. Prepare raw columns with backend metadata merged in
    const rawCols = Object.keys(dataset.value[0]).map(k => {
        const backendStat = dataStats.value?.column_stats?.find(s => s.name === k);
        const backendType = semanticTypes.value?.find(t => t.column === k)?.semantic_type;
        
        return { 
            name: k,
            unique: backendStat?.unique || 0,
            missing: backendStat?.missing || 0,
            semanticType: backendType || backendStat?.semanticType || backendStat?.semantic_type || 'unknown',
            distribution: backendStat?.distribution || null,
            metrics: backendStat?.detailed_metrics || backendStat?.metrics || null
        };
    });
    
    // 2. Process via composable (which now respects semanticType for UI mapping)
    availableColumns.value = processColumns(dataset.value, rawCols);
};

const saveDraft = () => {
    // Optional: could persist to experimentStore or just log
    console.log("Draft saving not fully implemented in verify-only mode");
};

const continueToAdvancedPreprocessing = async () => {
  if (!selectedColumn.value) return;

  try {
    // 1. Update Experiment Store
    experimentStore.setTargetColumn(selectedColumn.value);
    
    // Set problem type based on column properties (simplistic detection)
    // Real detection should happen on backend or via robust logic
    let probType = "classification";
    if (selectedColumn.value.type === 'number' && selectedColumn.value.uniqueValues > 20) {
        probType = "regression";
    }
    experimentStore.setProblemType(probType);

    // 2. Notify Backend
    try {
        await authenticatedPost(`/api/set-target`, {
            dataset_id: datasetId.value,
            target_column: selectedColumn.value.name,
            problem_type: probType
        });
    } catch (e) {
        console.warn("Backend target set failed", e);
    }

    router.push('/advanced-preprocessing');
  } catch (error) {
    console.error('Navigation error:', error);
    alert('Failed to proceed: ' + error.message);
  }
};

// --- Watchers ---
// Sync local view when global semantic types from backend change
watch(semanticTypes, (newVal) => {
    if (!newVal) return; // Guard against null
    console.log("🔄 Semantic types updated in store, re-analyzing targets...");
    processAvailableColumns();
}, { immediate: false }); // Remove deep watch to prevent reactivity issues

onMounted(async () => {
  await mlStore.checkBackendConnection();
  await loadData();
});
</script>

<style scoped>
.target-selection {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

.selection-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.backend-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border-radius: 20px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 2s infinite;
}

.status-indicator.connected .status-dot {
  background: #10b981;
}

.status-text {
  font-size: 0.75rem;
  color: #b3b3d1;
}

.dataset-id {
  font-size: 0.7rem;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 8px;
  font-family: monospace;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
  transform: translateX(-2px);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #b3b3d1;
  font-size: 0.875rem;
}

.breadcrumb .current {
  color: #667eea;
  font-weight: 600;
}

.hero-section {
  padding: 2rem;
  text-align: center;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  margin: 1.5rem 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-header-centered {
  text-align: center;
}

.gradient-text {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.6;
}

.main-content {
  display: grid;
  grid-template-columns: 480px 1fr 360px;
  gap: 2rem;
  padding: 2rem;
  min-height: calc(100vh - 300px);
}

.action-footer {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  padding: 1.5rem 2rem;
  position: sticky;
  bottom: 0;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.footer-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.footer-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.footer-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  animation: pulse 2s infinite;
}

.continue-btn {
  animation: none !important;
}

.footer-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
}

.footer-btn.primary:disabled {
  background: rgba(102, 126, 234, 0.3);
  color: rgba(255, 255, 255, 0.5);
  cursor: not-allowed;
  animation: none;
}

.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 15, 35, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-content {
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
