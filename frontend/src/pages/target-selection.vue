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
        <!-- Selected Target Display (Left Side) -->
        <div class="selected-target-status" :class="{ active: selectedColumn, empty: !selectedColumn }">
          <template v-if="selectedColumn">
            <span class="status-label">Selected Target:</span>
            <div class="target-badge-container">
              <span class="target-name-badge">{{ selectedColumn.name }}</span>
              <span class="target-type-badge" :class="selectedColumn.originalType || selectedColumn.type">
                {{ selectedColumn.type }}
              </span>
              <span v-if="selectedColumn.recommended" class="target-rec-badge">⭐ Recommended</span>
              <span class="target-suitability-badge" :class="getScoreClass(selectedColumn.suitabilityScore)">
                {{ selectedColumn.suitabilityScore }}% Match
              </span>
            </div>
          </template>
          <template v-else>
            <span class="pulse-indicator-warning"></span>
            <span class="status-label">No target column selected</span>
          </template>
        </div>

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
    <PremiumLoadingOverlay 
      :show="isLoading" 
      message="Analyzing dataset structure..."
    />

    <!-- Target Change Confirmation Modal -->
    <div v-if="showConfirmationModal" class="premium-modal-overlay">
      <div class="premium-modal">
        <div class="modal-header">
          <span class="warning-icon">⚠️</span>
          <h3>Reset Preprocessing?</h3>
        </div>
        <div class="modal-body">
          <p>Changing the target variable from <strong class="old-target-name">{{ oldTargetDisplayName }}</strong> to <strong class="new-target-name">{{ selectedColumn?.name }}</strong> will invalidate your current preprocessing steps (split, scaling, encoding, etc.).</p>
          <p class="leakage-explanation">To prevent <strong>data leakage</strong> and pipeline errors, all advanced preprocessing changes will be reset. This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button @click="showConfirmationModal = false" class="modal-btn secondary">Cancel</button>
          <button @click="confirmTargetChange" class="modal-btn danger">Yes, Change & Reset</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>


import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, onBeforeRouteLeave } from 'vue-router';
import { storeToRefs } from 'pinia';
import PremiumLoadingOverlay from '../components/PremiumLoadingOverlay.vue';
import { useMLDataFlowStore } from '../stores/mlDataFlow';
import { useDataStore } from '../stores/data';
import { useExperimentStore } from '../stores/experiment';
import { useAuthenticatedFetch } from '../composables/useAuthenticatedFetch';
import { useToast } from '../composables/useToast';
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
const { authenticatedPost, authenticatedDelete } = useAuthenticatedFetch();
const { showError, showWarning, showSuccess } = useToast();
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
const showConfirmationModal = ref(false);

const hasPreprocessing = computed(() => {
  const p = experimentStore.preprocessing;
  return p && (p.isSplitApplied || p.isScalingApplied || p.isEncodingApplied || p.smote?.applied);
});

const oldTargetDisplayName = computed(() => {
  const oldTarget = experimentStore.targetColumn;
  if (!oldTarget) return '';
  return typeof oldTarget === 'object' ? oldTarget.name : oldTarget;
});

// Methods
const handleColumnSelect = (column) => {
  selectedColumn.value = column;
};



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

    // 3. Restore target column selection if it was already chosen
    if (experimentStore.targetColumn) {
        const targetName = typeof experimentStore.targetColumn === 'object'
            ? experimentStore.targetColumn.name
            : experimentStore.targetColumn;
        const found = availableColumns.value.find(col => col.name === targetName);
        if (found) {
            selectedColumn.value = found;
        }
    }
};

const saveDraft = () => {
    // Optional: could persist to experimentStore or just log
    console.log("Draft saving not fully implemented in verify-only mode");
};

const getScoreClass = (score) => {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "fair";
  return "poor";
};

const continueToAdvancedPreprocessing = async () => {
  if (!selectedColumn.value) return;

  // Check if target column is being changed while preprocessing is already applied
  const oldTarget = experimentStore.targetColumn;
  const oldTargetName = oldTarget ? (typeof oldTarget === 'object' ? oldTarget.name : oldTarget) : null;
  const newTargetName = selectedColumn.value.name;

  if (oldTargetName && oldTargetName !== newTargetName && hasPreprocessing.value) {
    // Show confirmation modal
    showConfirmationModal.value = true;
    return;
  }

  // Otherwise, proceed immediately
  await executeTargetSetupAndNavigation();
};

const confirmTargetChange = async () => {
  showConfirmationModal.value = false;
  isLoading.value = true;
  
  try {
    // 1. Reset frontend experiment store preprocessing
    experimentStore.resetPreprocessing();
    
    // 2. Sync to mlStore for context bar visibility
    mlStore.isSplit = false;
    mlStore.isScaled = false;
    mlStore.isEncoded = false;
    
    // 3. Clear split on backend
    try {
      await authenticatedDelete(`/api/datasets/${datasetId.value}/split`);
      showWarning('Preprocessing Reset', 'Preprocessing configurations reset due to target column change.');
    } catch (err) {
      console.warn("Backend split clear on target change failed", err);
    }

    // 4. Proceed with setup and navigation
    await executeTargetSetupAndNavigation();
  } catch (error) {
    console.error('Target change confirmation error:', error);
    showError('Target Change Failed', error.message);
  } finally {
    isLoading.value = false;
  }
};

const executeTargetSetupAndNavigation = async () => {
  try {
    // 1. Update Experiment Store
    experimentStore.setTargetColumn(selectedColumn.value);
    
    // 1.1 Sync to mlStore for context bar visibility
    mlStore.setTargetColumn(selectedColumn.value.name);
    
    // Set problem type based on column properties (simplistic detection)
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
    showError('Navigation Failed', error.message);
  }
};

// --- Watchers ---
// Sync local view when global semantic types from backend change
watch(semanticTypes, (newVal) => {
    if (!newVal) return; // Guard against null
    console.log("🔄 Semantic types updated in store, re-analyzing targets...");
    processAvailableColumns();
}, { immediate: false }); // Remove deep watch to prevent reactivity issues

// ── NAVIGATION GUARD: clear session on pipeline exit ───────────────────────
const PIPELINE_ROUTES = [
  'data-preview', 'target-selection', 'advanced-preprocessing',
  'algorithm-select', 'model-training', 'model-visualization'
];
onBeforeRouteLeave((to, _from, next) => {
  if (!PIPELINE_ROUTES.includes(to.name)) {
    experimentStore.clearAll();
    dataStore.clearData();
  }
  next();
});
// ─────────────────────────────────────────────────────────────────────────────

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
  width: 100%;
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

/* Premium Footer Styling */
.selected-target-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #b3b3d1;
  transition: all 0.3s ease;
  user-select: none;
}

.selected-target-status.empty {
  color: #a0aec0;
}

.pulse-indicator-warning {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f59e0b;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
  animation: pulse-warning 2s infinite;
}

@keyframes pulse-warning {
  0%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
    box-shadow: 0 0 12px rgba(245, 158, 11, 0.8);
  }
}

.status-label {
  font-weight: 500;
  color: #a0aec0;
}

.target-badge-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.2);
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.selected-target-status.active:hover .target-badge-container {
  border-color: rgba(102, 126, 234, 0.4);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
}

.target-name-badge {
  font-weight: 700;
  color: #ffffff;
  font-size: 0.9rem;
}

.target-type-badge {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
  font-weight: 600;
  text-transform: uppercase;
}

.target-type-badge.number, .target-type-badge.numeric {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.target-type-badge.string, .target-type-badge.categorical {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.target-type-badge.date, .target-type-badge.datetime {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.target-type-badge.boolean {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.target-rec-badge {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.3);
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
}

.target-suitability-badge {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
  font-weight: 600;
}

.target-suitability-badge.excellent {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.target-suitability-badge.good {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.target-suitability-badge.fair {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.target-suitability-badge.poor {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Premium Modal Styling */
.premium-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(10, 10, 22, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  animation: fadeIn 0.25s ease;
}

.premium-modal {
  background: linear-gradient(135deg, #18182e 0%, #10101d 100%);
  border: 1px solid rgba(102, 126, 234, 0.3);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  border-radius: 16px;
  width: 500px;
  max-width: 90vw;
  overflow: hidden;
  animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
  background: rgba(102, 126, 234, 0.03);
}

.warning-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
}

.modal-body {
  padding: 1.5rem;
  color: #b3b3d1;
  font-size: 0.92rem;
  line-height: 1.5;
}

.leakage-explanation {
  background: rgba(239, 68, 68, 0.08);
  border-left: 3px solid #ef4444;
  padding: 0.75rem;
  border-radius: 4px 8px 8px 4px;
  color: #f87171;
  font-size: 0.85rem;
  margin-top: 1rem;
}

.old-target-name {
  color: #ef4444;
  text-decoration: line-through;
}

.new-target-name {
  color: #10b981;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(102, 126, 234, 0.1);
  background: rgba(10, 10, 20, 0.4);
}

.modal-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.modal-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.modal-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
}

.modal-btn.danger {
  background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
  color: #ffffff;
}

.modal-btn.danger:hover {
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
