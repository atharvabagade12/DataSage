<template>
  <div class="advanced-preprocessing">
    <!-- Navigation Header -->
    <nav class="preview-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
          Back to Target Selection
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Advanced Preprocessing</span>
        </div>
      </div>
      <div class="backend-status" v-if="backendConnected !== null">
        <div
          class="status-indicator"
          :class="{
            connected: backendConnected,
            disconnected: !backendConnected,
          }"
        ></div>
        <span>{{ backendConnected ? 'Connected' : 'Disconnected' }}</span>
      </div>
    </nav>

    <!-- Dataset Info -->
    <section class="dataset-info">
      <div>
        Dataset: <strong>{{ fileName }}</strong>
        <span>Rows (Train/Test): {{ trainData.length }} / {{ testData.length }}</span>
        <span>Columns: {{ columns.length }}</span>
      </div>
    </section>

    <!-- Split Toggle -->
    <div class="split-toggle">
      <button :class="{ active: selectedSplit === 'train' }" @click="selectedSplit = 'train'">
        Train Data
      </button>
      <button :class="{ active: selectedSplit === 'test' }" @click="selectedSplit = 'test'">
        Test Data
      </button>
    </div>

    <!-- Dataset Preview Table -->
    <section class="dataset-preview">
      <table>
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.name">{{ col.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in previewData.slice(pageStart, pageEnd)" :key="idx">
            <td v-for="col in columns" :key="col.name">{{ row[col.name] }}</td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">Previous</button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
      </div>
    </section>

    <!-- Advanced Preprocessing Toolkit -->
    <section class="advanced-toolkit">
      <!-- Dataset Splitting Card -->
      <div class="tool-card">
        <h3>Dataset Splitting</h3>
        <label>
          Train Ratio:
          <input type="range" min="0.5" max="0.95" step="0.05" v-model.number="splitRatio" />
          {{ (splitRatio * 100).toFixed(0) }}%
        </label>
        <label>
          Split Strategy:
          <select v-model="splitStrategy">
            <option value="random">Random</option>
            <option value="stratified">Stratified</option>
          </select>
        </label>
        <button @click="applySplit" :disabled="isProcessing">Apply Split</button>
      </div>

      <!-- Feature Scaling Card -->
      <div class="tool-card">
        <h3>Feature Scaling</h3>
        <label>
          Scaling Method:
          <select v-model="scalingMethod" :disabled="!splitApplied">
            <option value="standard">StandardScaler</option>
            <option value="minmax">MinMaxScaler</option>
            <option value="robust">RobustScaler</option>
          </select>
        </label>
        <button @click="applyScaling" :disabled="!splitApplied || isProcessing">Apply Scaling</button>
      </div>
    </section>

    <!-- Footer Navigation -->
    <footer>
      <button @click="goBack" :disabled="isProcessing">Back to Target Selection</button>
      <button @click="proceedToModelTraining" :disabled="!splitApplied || isProcessing">Next: Model Training</button>
    </footer>
  </div>
</template>


<script setup>
import { ref, reactive, computed } from 'vue';
import mlStore from '@/stores/mlDataFlow'; 
import { useRouter } from 'vue-router';

const router = useRouter();

const backendConnected = ref(false);
const fileName = ref('');
const columns = ref([]);

// Dataset splitting state
const splitRatio = ref(0.8);
const splitStrategy = ref('random');
const splitApplied = ref(false);
const trainData = ref([]);
const testData = ref([]);
const scalingMethod = ref('standard');

const isProcessing = ref(false);
const selectedSplit = ref('train'); // 'train' or 'test'

const previewData = computed(() =>
  selectedSplit.value === 'train' ? trainData.value : testData.value
);

// Pagination state
const currentPage = ref(1);
const rowsPerPage = ref(25);

const totalPages = computed(() =>
  Math.ceil(previewData.value.length / rowsPerPage.value)
);
const pageStart = computed(() => (currentPage.value - 1) * rowsPerPage.value);
const pageEnd = computed(() => pageStart.value + rowsPerPage.value);

// Load initial state from mlStore/backend
const loadInitialDataset = async () => {
  backendConnected.value = await mlStore.checkBackendConnection();
  if (backendConnected.value) {
    fileName.value = mlStore.fileName;
    columns.value = mlStore.columns || [];

    // For splitting, initialize trainData with full dataset sample
    trainData.value = mlStore.dataset || [];
    testData.value = [];

    splitApplied.value = false;
    selectedSplit.value = 'train';
  }
};

// Apply dataset split with backend API call
const applySplit = async () => {
  if (isProcessing.value) return;
  isProcessing.value = true;
  try {
    const response = await fetch('/api/datasets/split', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        datasetId: mlStore.datasetId,
        trainRatio: splitRatio.value,
        strategy: splitStrategy.value,
      }),
    });
    const data = await response.json();
    if (data.success) {
      trainData.value = data.trainDataPreview;
      testData.value = data.testDataPreview;

      splitApplied.value = true;
      selectedSplit.value = 'train';

      // Update mlStore with the full split data for later steps
      mlStore.setSplitData(data.trainData, data.testData);
    } else {
      alert('Dataset split failed: ' + data.message);
    }
  } catch (error) {
    console.error(error);
    alert('Error occurred during dataset split.');
  } finally {
    isProcessing.value = false;
  }
};

// Apply feature scaling via backend API
const applyScaling = async () => {
  if (isProcessing.value || !splitApplied.value) {
    alert('Please apply data split before scaling.');
    return;
  }
  isProcessing.value = true;
  try {
    const response = await fetch('/api/datasets/scale', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        trainData: trainData.value,
        testData: testData.value,
        method: scalingMethod.value,
      }),
    });
    const data = await response.json();
    if (data.success) {
      trainData.value = data.scaledTrainDataPreview;
      testData.value = data.scaledTestDataPreview;

      mlStore.setScaledData(data.scaledTrainData, data.scaledTestData);
    } else {
      alert('Feature scaling failed: ' + data.message);
    }
  } catch (error) {
    console.error(error);
    alert('Error occurred during feature scaling.');
  } finally {
    isProcessing.value = false;
  }
};

// Navigation controls
const goBack = () => {
  router.push('/target-selection');
};

const proceedToModelTraining = () => {
  if (!splitApplied.value) {
    alert('Please apply dataset split before proceeding.');
    return;
  }
  router.push('/model-training');
};

// Initialize state
loadInitialDataset();
</script>


<style scoped>
/* Navigation and header */
.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
  background-color: #1e293b;
  color: white;
  font-size: 14px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.back-btn svg {
  margin-right: 6px;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
}

.breadcrumb .current {
  font-weight: bold;
}

/* Backend status */
.backend-status {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.status-indicator.connected {
  width: 12px;
  height: 12px;
  background-color: #4ade80;
  border-radius: 50%;
}

.status-indicator.disconnected {
  width: 12px;
  height: 12px;
  background-color: #f87171;
  border-radius: 50%;
}

/* Dataset Info */
.dataset-info {
  font-size: 15px;
  color: #cbd5e1;
  margin-bottom: 20px;
}

/* Split toggle buttons */
.split-toggle {
  display: flex;
  margin: 10px 0 15px 0;
  gap: 15px;
}

.split-toggle button {
  padding: 8px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background-color: #2d3748;
  color: #cbd5e1;
  transition: background-color 0.3s ease;
}

.split-toggle button.active,
.split-toggle button:hover {
  background-color: #2563eb;
  color: white;
}

/* Dataset preview table */
.dataset-preview table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1e293b;
  color: white;
  font-size: 14px;
}

.dataset-preview th,
.dataset-preview td {
  padding: 10px 14px;
  border-bottom: 1px solid #334155;
  text-align: left;
}

.dataset-preview thead tr {
  border-bottom: 2px solid #3b82f6;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 10px 0;
  color: #cbd5e1;
}

.pagination button {
  background-color: #2d3748;
  border: none;
  padding: 6px 15px;
  color: #cbd5e1;
  border-radius: 5px;
  cursor: pointer;
}

/* Disable pagination buttons */
.pagination button[disabled] {
  background-color: #475569;
  cursor: not-allowed;
}

/* Advanced toolkit cards */
.advanced-toolkit {
  margin-top: 30px;
}

.tool-card {
  background-color: #1e293b;
  border-radius: 10px;
  padding: 16px 24px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(25, 50, 80, 0.4);
  color: #cbd5e1;
}

.tool-card h3 {
  margin-bottom: 15px;
  font-weight: 600;
  color: #3b82f6;
}

.tool-card label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
}

.tool-card input[type="range"] {
  width: 100%;
  margin: 8px 0 15px 0;
}

.tool-card select {
  width: 100%;
  padding: 6px 10px;
  background-color: #334155;
  border: none;
  border-radius: 6px;
  color: #cbd5e1;
  font-size: 14px;
  cursor: pointer;
}

.tool-card button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 12px 28px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.tool-card button:disabled {
  background-color: #475569;
  cursor: not-allowed;
}

.tool-card button:hover:not(:disabled) {
  background-color: #1d4ed8;
}

/* Footer */
footer {
  margin-top: 40px;
  display: flex;
  justify-content: space-between;
}

footer button {
  font-weight: 600;
  padding: 12px 28px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  background-color: #2563eb;
  color: white;
  transition: background-color 0.3s ease;
}

footer button:disabled {
  background-color: #475569;
  cursor: not-allowed;
}

footer button:hover:not(:disabled) {
  background-color: #1d4ed8;
}
</style>
