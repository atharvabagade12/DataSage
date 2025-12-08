<template>
  <div class="target-selection">
    <!-- Navigation Header -->
    <header class="selection-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Back to Data-Preprocessing
        </button>
        <div class="breadcrumb">
          <span>Data Preview</span>
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M9 18l6-6-6-6" />
          </svg>
          <span class="current">Target Selection</span>
        </div>
      </div>

      <div class="backend-status">
        <div
          class="status-indicator"
          :class="{ connected: mlStore.backendConnected }"
        >
          <div class="status-dot"></div>
          <span class="status-text">{{
            mlStore.backendConnected ? "Backend Connected" : "Backend Offline"
          }}</span>
        </div>
        <span v-if="datasetId" class="dataset-id">ID: {{ datasetId }}</span>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <!-- Centered Header -->
        <div class="hero-header-centered">
          <h1 class="gradient-text">Target Variable Selection</h1>
          <p class="hero-subtitle">
            Choose the column you want to predict. Our algorithm analyzes each column's
            suitability for machine learning tasks.
          </p>
        </div>
      </div>
    </section>

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
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useMLDataFlowStore } from '../stores/mlDataFlow';
import { useAuthenticatedFetch } from '../composables/useAuthenticatedFetch';
import { useTargetAnalysis } from '../composables/useTargetAnalysis';

// Components
import ColumnSelector from '../components/target-selection/ColumnSelector.vue';
import DataPreviewChart from '../components/target-selection/DataPreviewChart.vue';
import TargetInsights from '../components/target-selection/TargetInsights.vue';

const router = useRouter();
const mlStore = useMLDataFlowStore();
const { authenticatedPost, authenticatedGet } = useAuthenticatedFetch();
const { processColumns } = useTargetAnalysis();

// State
const isLoading = ref(true);
const dataset = ref([]);
const columns = ref([]);
const availableColumns = ref([]);
const selectedColumn = ref(null);
const datasetId = ref(null);
const fileName = ref("");
const datasetInfo = ref({ rowCount: 0, columnCount: 0 });

// Methods
const handleColumnSelect = (column) => {
  selectedColumn.value = column;
};

const detectColumnType = (data) => {
  const nonNullData = data.filter(
    (val) => val !== null && val !== undefined && val !== ""
  );
  if (nonNullData.length === 0) return "string";

  const isNumber = nonNullData.every((val) => !isNaN(parseFloat(val)) && isFinite(val));
  if (isNumber) return "number";

  const isDate = nonNullData.every((val) => !isNaN(Date.parse(val)));
  if (isDate) return "date";

  return "string";
};

const loadPreviousData = async () => {
  try {
    isLoading.value = true;

    // Priority 1: mlStore
    if (mlStore.dataset && mlStore.dataset.length > 0) {
      console.log("✅ Using mlStore data");
      dataset.value = mlStore.dataset;
      datasetId.value = mlStore.datasetId;
      fileName.value = mlStore.fileName;
      setupColumnsFromDataset();
      return;
    }

    // Priority 2: localStorage
    const processedDataStr = localStorage.getItem("processedData");
    if (processedDataStr) {
      const processedData = JSON.parse(processedDataStr);
      if (processedData.data && processedData.data.length > 0) {
        console.log("✅ Using localStorage data");
        dataset.value = processedData.data;
        datasetId.value = processedData.datasetId;
        fileName.value = processedData.fileName;
        setupColumnsFromDataset();
        return;
      }
    }

    // Priority 3: Backend
    console.log("⚠️ Fetching from backend...");
    let idToFetch = mlStore.datasetId;
    if (!idToFetch && processedDataStr) {
      idToFetch = JSON.parse(processedDataStr).datasetId;
    }

    if (!idToFetch) {
      throw new Error("No dataset ID found.");
    }

    const response = await fetch(`http://localhost:8000/api/datasets/${idToFetch}/preview`);
    if (!response.ok) throw new Error("Failed to fetch dataset");
    
    const data = await response.json();
    dataset.value = data.data || [];
    datasetId.value = idToFetch;
    fileName.value = data.filename || "Unknown";
    setupColumnsFromDataset();

  } catch (error) {
    console.error("Error loading data:", error);
    alert("Failed to load dataset. Redirecting to preview.");
    router.push("/data-preview");
  } finally {
    isLoading.value = false;
  }
};

const setupColumnsFromDataset = () => {
  if (dataset.value.length > 0) {
    columns.value = Object.keys(dataset.value[0]).map((colName) => ({
      name: colName,
      type: detectColumnType(dataset.value.map((row) => row[colName])),
      originalType: detectColumnType(dataset.value.map((row) => row[colName])),
      unique: 0,
      missing: 0,
    }));

    datasetInfo.value = {
      rowCount: dataset.value.length,
      columnCount: columns.value.length,
    };

    // Use composable to process columns
    availableColumns.value = processColumns(dataset.value, columns.value);
  }
};

const goBack = () => router.push("/data-preview");

const saveDraft = () => {
  if (selectedColumn.value) {
    const draftState = {
      selectedTarget: selectedColumn.value.name,
      targetColumn: selectedColumn.value,
      savedAt: Date.now(),
    };
    localStorage.setItem("mlAppDraft", JSON.stringify(draftState));
    console.log("💾 Draft saved");
    alert("Draft saved successfully!");
  }
};

const continueToAdvancedPreprocessing = async () => {
  if (!selectedColumn.value) return;

  try {
    const processedData = JSON.parse(localStorage.getItem('processedData'));
    const backendDatasetId = processedData?.backendDatasetId || processedData?.datasetId; // Fallback

    const targetData = {
      name: selectedColumn.value.name,
      type: selectedColumn.value.type,
      originalType: selectedColumn.value.originalType || selectedColumn.value.type,
      uniqueValues: selectedColumn.value.uniqueValues,
      suitabilityScore: selectedColumn.value.suitabilityScore,
      statistics: selectedColumn.value.statistics,
      missingPercent: selectedColumn.value.missingPercent || 0,
      backendDatasetId: backendDatasetId,
      datasetId: datasetId.value,
    };

    // Store target data
    localStorage.setItem('selectedTarget', JSON.stringify(targetData));

    // Update global state
    const currentState = JSON.parse(localStorage.getItem('mlAppState')) || {};
    currentState.selectedTarget = selectedColumn.value.name;
    currentState.targetColumn = selectedColumn.value;
    currentState.backendDatasetId = backendDatasetId;
    currentState.datasetId = datasetId.value;
    currentState.updatedAt = Date.now();
    localStorage.setItem('mlAppState', JSON.stringify(currentState));

    console.log('\n' + '='.repeat(80));
    console.log('🎯 TARGET VARIABLE SELECTED');
    console.log('='.repeat(80));
    console.log('   Target Column:', selectedColumn.value.name);
    console.log('   Target Type:', selectedColumn.value.type);
    console.log('   Suitability Score:', selectedColumn.value.suitabilityScore);
    console.log('   Dataset ID:', datasetId.value);
    console.log('   Stored in: localStorage.mlAppState');
    console.log('='.repeat(80) + '\n');

    // Also notify backend
    try {
        await authenticatedPost('http://localhost:8000/api/set-target', {
            dataset_id: datasetId.value,
            target_column: selectedColumn.value.name
        });
        console.log('✅ Backend notified of target selection');
    } catch (e) {
        console.warn("⚠️ Backend notification failed, but proceeding locally:", e);
    }

    router.push('/advanced-preprocessing');
  } catch (error) {
    console.error('❌ Navigation error:', error);
    alert('Failed to proceed: ' + error.message);
  }
};

const fetchCompleteStatistics = async () => {
  if (!datasetId.value) return;

  try {
    console.log("🔄 Fetching complete statistics...");
    const response = await authenticatedGet(`http://localhost:8000/api/datasets/${datasetId.value}/statistics`);
    
    if (!response.ok) {
      console.warn("⚠️ Failed to fetch statistics");
      return;
    }

    const stats = await response.json();

    if (stats.column_stats) {
      // Update columns with backend statistics
      stats.column_stats.forEach(stat => {
        const col = columns.value.find(c => c.name === stat.name);
        if (col) {
          col.unique = stat.unique;
          col.missing = stat.missing;
          col.distribution = stat.distribution; // Store backend distribution data
          col.metrics = stat.detailed_metrics; // Store enhanced metrics
          // Use top values for preview if available (better than first 10 rows)
          if (stat.top_values && stat.top_values.length > 0) {
            col.hasBackendPreview = true;
            col.backendPreview = stat.top_values;
          }
        }
      });

      // Re-process columns with new data
      availableColumns.value = processColumns(dataset.value, columns.value);
      
      // Refresh selectedColumn if it exists to ensure it has the new stats
      if (selectedColumn.value) {
        const updatedCol = availableColumns.value.find(c => c.name === selectedColumn.value.name);
        if (updatedCol) {
          console.log("🔄 Refreshing selected column with full stats");
          selectedColumn.value = updatedCol;
        }
      }
      
      console.log("✅ Updated columns with full dataset statistics");
    }
  } catch (error) {
    console.warn("⚠️ Error updating statistics:", error);
  }
};

onMounted(async () => {
  await mlStore.checkBackendConnection();
  await loadPreviousData();
  // Fetch full stats after loading data
  await fetchCompleteStatistics();
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
