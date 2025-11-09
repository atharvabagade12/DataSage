<template>
  <div class="target-selection">
    <!-- Navigation Header -->
    <nav class="selection-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
            />
          </svg>
          Back to Data Preview
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span>Data Preview</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Target Selection</span>
        </div>
      </div>

      <!-- Backend Status -->
      <div class="backend-status" v-if="backendConnected !== null">
        <div
          class="status-indicator"
          :class="{
            connected: backendConnected,
            disconnected: !backendConnected,
          }"
        >
          <div class="status-dot"></div>
          <span class="status-text">
            {{ backendConnected ? "ML Backend Ready" : "Frontend Mode" }}
          </span>
          <span class="dataset-id" v-if="backendConnected && datasetId">
            ID: {{ datasetId.substring(0, 8) }}...
          </span>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🎯</div>
        <h1>Select Your Target Variable</h1>
        <p>
          Choose the column you want to predict or analyze. We'll help you
          explore its characteristics and suitability for machine learning.
        </p>

        <div class="dataset-summary">
          <span class="summary-item"
            ><strong>{{ fileData?.name || "Dataset" }}</strong></span
          >
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ dataset.length }} rows</span>
          <span class="summary-divider">•</span>
          <span class="summary-item"
            >{{ availableColumns.length }} columns available</span
          >
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="main-content">
      <!-- Left Panel: Column Selector -->
      <aside class="column-selector">
        <div class="selector-header">
          <h3>Choose Target Column</h3>
          <p class="selector-subtitle">
            Select the column you want to predict or analyze
          </p>

          <!-- ✅ COMPACT COLLAPSIBLE DISCLAIMER -->
          <div class="disclaimer-compact" :class="{ expanded: showDisclaimer }">
            <button
              @click="showDisclaimer = !showDisclaimer"
              class="disclaimer-toggle"
            >
              <span class="disclaimer-icon">⚠️</span>
              <span class="disclaimer-title">AI Recommendations</span>
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
                :class="{ rotated: showDisclaimer }"
              >
                <path d="M7 10l5 5 5-5z" />
              </svg>
            </button>

            <div v-if="showDisclaimer" class="disclaimer-content">
              <p>
                Column recommendations are AI-powered suggestions based on data
                patterns. Please review carefully and select the most
                appropriate target for your specific use case.
              </p>
            </div>
          </div>

          <div class="column-filters">
            <button
              v-for="filter in columnFilters"
              :key="filter.type"
              @click="activeFilter = filter.type"
              :class="['filter-btn', { active: activeFilter === filter.type }]"
            >
              {{ filter.icon }} {{ filter.label }}
            </button>
          </div>
        </div>

        <div class="search-box">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
            />
          </svg>
          <input
            v-model="searchQuery"
            placeholder="Search columns..."
            class="search-input"
          />
        </div>

        <!-- ✅ EXPANDED COLUMN LIST CONTAINER -->
        <div class="column-list-container">
          <!-- No Columns State -->
          <div v-if="filteredColumns.length === 0" class="no-columns">
            <div class="no-columns-icon">🔍</div>
            <p>No columns match your search</p>
            <button
              @click="
                searchQuery = '';
                activeFilter = 'all';
              "
              class="clear-filters-btn"
            >
              Clear filters
            </button>
          </div>

          <!-- Column List -->
          <div v-else class="column-list">
            <div
              v-for="(column, index) in filteredColumns"
              :key="column.name"
              @click="selectColumn(column)"
              :class="[
                'column-item',
                {
                  selected: selectedColumn?.name === column.name,
                  recommended: column.recommended,
                  'last-item': index === filteredColumns.length - 1,
                },
              ]"
            >
              <div class="column-info">
                <!-- Column Header -->
                <div class="column-header">
                  <span class="column-name">{{ column.name }}</span>
                  <span v-if="column.recommended" class="recommendation-badge">
                    ⭐ Best
                  </span>
                </div>

                <!-- Column Meta Information -->
                <div class="column-meta">
                  <span class="type-badge" :class="column.type">
                    {{ getColumnTypeIcon(column.type) }}
                    {{ column.type.toUpperCase() }}
                  </span>
                  <span class="unique-count"
                    >{{ column.uniqueValues }} unique</span
                  >
                  <span
                    v-if="column.missingPercent > 0"
                    class="missing-percent"
                  >
                    {{ column.missingPercent.toFixed(1) }}% missing
                  </span>
                </div>

                <!-- Column Preview -->
                <div class="column-preview">
                  {{ getColumnPreview(column.name) }}
                </div>

                <!-- Suitability Score -->
                <div v-if="column.suitabilityScore" class="suitability-score">
                  <div class="score-bar">
                    <div
                      class="score-fill"
                      :style="{ width: `${column.suitabilityScore}%` }"
                      :class="getScoreClass(column.suitabilityScore)"
                    ></div>
                  </div>
                  <span class="score-text"
                    >{{ column.suitabilityScore }}% suitable</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Selection Helper -->
        <div class="selection-helper">
          <div v-if="!selectedColumn" class="helper-message">
            <span class="helper-icon">👆</span>
            <span class="helper-text"
              >Click a column above to start exploring</span
            >
          </div>
          <div v-else class="helper-selected">
            <span class="helper-icon">✅</span>
            <span class="helper-text">{{ selectedColumn.name }} selected</span>
          </div>
        </div>
      </aside>

      <!-- Center Panel: Live Preview -->
      <main class="preview-panel">
        <div class="preview-header">
          <h3>
            {{
              selectedColumn
                ? `Exploring: ${selectedColumn.name}`
                : "Select a column to preview"
            }}
          </h3>
          <div v-if="selectedColumn" class="chart-controls">
            <select
              v-model="chartType"
              @change="onChartTypeChange"
              class="chart-selector"
            >
              <!-- NUMERIC COLUMN CHARTS -->
              <template v-if="selectedColumn.type === 'number'">
                <option value="histogram">📊 Histogram</option>
                <option value="box">📦 Box Plot</option>
                <option value="line">📈 Distribution Curve</option>
                <option value="scatter">🔵 Scatter Plot</option>
                <option value="violin">🎻 Violin Plot</option>
              </template>

              <!-- STRING COLUMN CHARTS -->
              <template v-else-if="selectedColumn.type === 'string'">
                <option value="doughnut">🍩 Value Distribution</option>
                <option value="bar">📊 Bar Chart</option>
                <option value="pie">🥧 Pie Chart</option>
                <option value="treemap">🗂️ Treemap View</option>
              </template>

              <!-- BOOLEAN/DATE COLUMN CHARTS -->
              <template v-else>
                <option value="bar">📊 Bar Chart</option>
                <option value="pie">🥧 Pie Chart</option>
              </template>
            </select>

            <!-- ENCODING INDICATOR -->
            <div
              v-if="encodingInfo && encodingInfo.encoding !== 'none'"
              class="encoding-badge"
            >
              🔄 {{ encodingInfo.encoding }} encoded
            </div>
          </div>
        </div>

        <!-- Chart Container Section -->
        <div class="chart-container">
          <div v-if="!selectedColumn" class="empty-state">
            <div class="empty-icon">📊</div>
            <h4>Choose a Target Column</h4>
            <p>
              Select a column from the left panel to see its distribution and
              characteristics.
            </p>
          </div>

          <div v-else class="interactive-chart">
            <!-- Loading State -->
            <div v-if="isLoadingChart" class="loading-overlay">
              <div class="chart-skeleton">
                <div class="skeleton-bar" v-for="i in 5" :key="i"></div>
              </div>
              <p>Generating {{ getChartTypeName() }} visualization...</p>
            </div>

            <!-- Chart Container -->
            <div class="chart-placeholder" :class="{ loading: isLoadingChart }">
              <canvas
                ref="chartCanvas"
                :key="`chart-${selectedColumn?.name}-${chartType}`"
                style="width: 100%; height: 400px"
              ></canvas>
            </div>

            <!-- ENHANCED CHART INSIGHTS -->
            <div v-if="!isLoadingChart" class="chart-insights">
              <div class="insight-cards">
                <div class="insight-card">
                  <span class="insight-label">Distribution</span>
                  <span class="insight-value">{{ getDistributionType() }}</span>
                </div>
                <div class="insight-card">
                  <span class="insight-label">Outliers</span>
                  <span class="insight-value">{{ getOutlierCount() }}</span>
                </div>
                <div class="insight-card">
                  <span class="insight-label">Skewness</span>
                  <span class="insight-value">{{ getSkewness() }}</span>
                </div>
                <div class="insight-card">
                  <span class="insight-label">Completeness</span>
                  <span class="insight-value"
                    >{{ getCompletenessPercentage() }}%</span
                  >
                </div>
              </div>

              <!-- ENCODING INFORMATION -->
              <div
                v-if="encodingInfo && encodingInfo.encoding !== 'none'"
                class="encoding-info"
              >
                <h4>🔄 Data Encoding Applied</h4>
                <div class="encoding-details">
                  <p>
                    <strong>Type:</strong>
                    {{ encodingInfo.encoding | capitalize }}
                  </p>
                  <p><strong>Note:</strong> {{ encodingInfo.note }}</p>
                  <div
                    v-if="
                      encodingInfo.mapping &&
                      Object.keys(encodingInfo.mapping).length <= 10
                    "
                    class="encoding-mapping"
                  >
                    <h5>Value Mapping:</h5>
                    <div class="mapping-grid">
                      <div
                        v-for="[original, encoded] in Object.entries(
                          encodingInfo.mapping
                        ).slice(0, 8)"
                        :key="original"
                        class="mapping-item"
                      >
                        <span class="original">{{ original }}</span>
                        <span class="arrow">→</span>
                        <span class="encoded">{{ encoded }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- Right Panel: Target Insights -->
      <aside class="insights-panel">
        <h3>Target Analysis</h3>

        <div v-if="!selectedColumn" class="no-selection">
          <div class="no-selection-icon">📋</div>
          <p>Select a column to see detailed analysis</p>
        </div>

        <div v-else class="target-insights">
          <!-- Column Statistics -->
          <div class="insight-section">
            <h4>📊 Statistics</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-label">Type</span>
                <span class="stat-value">{{ selectedColumn.type }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Unique Values</span>
                <span class="stat-value">{{
                  selectedColumn.uniqueValues.toLocaleString()
                }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Missing Data</span>
                <span class="stat-value"
                  >{{ selectedColumn.missingPercent.toFixed(1) }}%</span
                >
              </div>
              <div v-if="selectedColumn.type === 'number'" class="stat-item">
                <span class="stat-label">Range</span>
                <span class="stat-value"
                  >{{ selectedColumn.min }} - {{ selectedColumn.max }}</span
                >
              </div>
            </div>
          </div>

          <!-- ML Suitability -->
          <div class="insight-section">
            <h4>🤖 ML Suitability</h4>

            <!-- ✅ ENHANCED: Better No Data State -->
            <div v-if="!selectedColumn.suitabilityScore" class="no-data-state">
              <div class="no-data-icon">⏳</div>
              <p>Analyzing column suitability...</p>
            </div>

            <div v-else class="suitability-analysis">
              <div class="suitability-score-large">
                <div
                  class="score-circle"
                  :class="getScoreClass(selectedColumn.suitabilityScore)"
                >
                  {{ selectedColumn.suitabilityScore }}%
                </div>
                <div class="score-description">
                  {{
                    getSuitabilityDescription(selectedColumn.suitabilityScore)
                  }}
                </div>
              </div>

              <div class="suitability-factors">
                <div
                  v-for="factor in getSuitabilityFactors()"
                  :key="factor.name"
                  class="factor-item"
                >
                  <span class="factor-icon" :class="factor.status">{{
                    factor.icon
                  }}</span>
                  <span class="factor-text">{{ factor.text }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Sample Values -->
          <div class="insight-section">
            <h4>👀 Sample Values</h4>

            <!-- ✅ FIXED: Better handling of sample values -->
            <div
              v-if="
                !selectedColumn.sampleValues ||
                selectedColumn.sampleValues.length === 0
              "
              class="no-data-state"
            >
              <div class="no-data-icon">📭</div>
              <p>No sample values available</p>
            </div>

            <div v-else class="sample-values">
              <div
                v-for="(value, index) in selectedColumn.sampleValues.slice(
                  0,
                  8
                )"
                :key="index"
                class="sample-item"
              >
                {{ formatSampleValue(value) }}
              </div>
            </div>
          </div>

          <!-- ML Recommendations -->
          <div class="insight-section">
            <h4>💡 ML Recommendations</h4>

            <!-- ✅ FIXED: Better recommendations display -->
            <div v-if="!selectedColumn" class="no-data-state">
              <div class="no-data-icon">💭</div>
              <p>Select a column to see recommendations</p>
            </div>

            <div
              v-else-if="getTargetRecommendations().length === 0"
              class="no-data-state"
            >
              <div class="no-data-icon">🤔</div>
              <p>Generating recommendations...</p>
            </div>

            <div v-else class="recommendations">
              <div
                v-for="rec in getTargetRecommendations()"
                :key="rec.taskType || rec.title"
                class="recommendation-item"
              >
                <span class="rec-icon">{{ rec.icon }}</span>
                <div class="rec-content">
                  <div class="rec-title">{{ rec.title }}</div>
                  <div class="rec-description">{{ rec.description }}</div>
                  <div v-if="rec.confidence" class="rec-confidence">
                    <div class="confidence-bar">
                      <div
                        class="confidence-fill"
                        :style="{ width: `${rec.confidence}%` }"
                      ></div>
                    </div>
                    <span class="confidence-text"
                      >{{ rec.confidence }}% confidence</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Action Footer -->
    <div class="action-footer">
      <div class="footer-content">
        <button @click="goBack" class="footer-btn secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
            />
          </svg>
          Back to Preview
        </button>

        <div class="selection-summary">
          <span v-if="selectedColumn" class="selected-target">
            🎯 Target: <strong>{{ selectedColumn.name }}</strong>
          </span>
          <span v-else class="no-target">No target selected</span>
        </div>

        <div class="footer-actions">
          <button @click="saveDraft" class="footer-btn secondary">
            💾 Save Draft
          </button>
          <button
            @click="continueToModelSelection"
            :disabled="!selectedColumn"
            class="footer-btn primary"
          >
            <span>Continue to Algorithm Selection</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted,
  watch,
  nextTick,
  onBeforeUnmount,
} from "vue";

// ✅ CORRECT IMPORT AND USAGE:
import { useMLDataFlowStore } from "~/stores/mlDataFlow";

// ✅ INITIALIZE THE STORE:
const mlStore = useMLDataFlowStore();

const chartInstance = ref(null);
const chartCanvas = ref(null);
// ============= REACTIVE VARIABLES =============
const fileData = ref({});
const dataset = ref([]);
const columns = ref([]);
const datasetInfo = ref({ rowCount: 0, columnCount: 0 });
const availableColumns = ref([]);
const selectedColumn = ref(null);
const searchQuery = ref("");
const activeFilter = ref("all");
const chartType = ref("histogram");
const isLoadingChart = ref(false);
const fileName = ref("");
const isLoading = ref(true);
const selectedTarget = ref("");
const encodingInfo = ref(null);
const backendConnected = ref(null);
const datasetId = ref(null);
const showDisclaimer = ref(false); 

// Import Chart.js composable
const { loadChart } = useChart();

// Page Meta
useHead({
  title: "Target Selection - DataSage ML Platform",
  meta: [
    {
      name: "description",
      content: "Select your target variable for machine learning analysis",
    },
  ],
});

import { useRouter } from "vue-router";
const router = useRouter();

// Column Filters
const columnFilters = [
  { type: "all", label: "All", icon: "📊" },
  { type: "number", label: "Numeric", icon: "🔢" },
  { type: "string", label: "Text", icon: "📝" },
  { type: "date", label: "Date", icon: "📅" },
  { type: "recommended", label: "Recommended", icon: "⭐" },
];

// ============= COMPUTED PROPERTIES =============
const filteredColumns = computed(() => {
  let columnsToFilter = availableColumns.value;

  if (activeFilter.value !== "all") {
    if (activeFilter.value === "recommended") {
      columnsToFilter = columnsToFilter.filter((col) => col.recommended);
    } else {
      columnsToFilter = columnsToFilter.filter(
        (col) => col.originalType === activeFilter.value
      );
    }
  }

  if (searchQuery.value) {
    columnsToFilter = columnsToFilter.filter((col) =>
      col.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  return columnsToFilter;
});

const checkBackendConnection = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/health", {
      timeout: 3000,
    });
    if (response.ok) {
      backendConnected.value = true;
      console.log("✅ Backend connected");

      // Load dataset ID from previous step
      // Prefer the pipeline state sessionId saved by useMLPipeline
      const pipelineState = JSON.parse(
        localStorage.getItem("datasage_pipeline_state") || "{}"
      );
      if (pipelineState && pipelineState.sessionId) {
        datasetId.value = pipelineState.sessionId;
        console.log(
          "📊 Backend dataset ID (from pipeline state):",
          datasetId.value
        );
      } else {
        const storedDatasetId = localStorage.getItem("datasetId");
        if (storedDatasetId) {
          datasetId.value = storedDatasetId;
          console.log(
            "📊 Backend dataset ID (fallback localStorage):",
            storedDatasetId
          );
        } else if (mlStore?.datasetId) {
          datasetId.value = mlStore.datasetId;
          console.log(
            "📊 Backend dataset ID (fallback store):",
            mlStore.datasetId
          );
        }
      }
    } else {
      backendConnected.value = false;
    }
  } catch (error) {
    backendConnected.value = false;
    console.log("❌ Backend not available");
  }
};

// Get dataset info from backend
const getBackendDatasetInfo = async () => {
  if (!backendConnected.value || !datasetId.value) return null;

  try {
    const response = await fetch(
      `http://localhost:8000/api/datasets/${datasetId.value}`
    );
    if (response.ok) {
      const datasetInfo = await response.json();
      console.log("📊 Backend dataset info:", datasetInfo);
      return datasetInfo;
    }
  } catch (error) {
    console.error("❌ Failed to get backend dataset info:", error);
  }
  return null;
};

const detectColumnType = (values) => {
  if (!values || values.length === 0) return "categorical";

  // Filter out null/empty values
  const cleanValues = values.filter(
    (v) => v !== null && v !== undefined && v !== "" && v !== "null"
  );

  if (cleanValues.length === 0) return "categorical";

  // Count how many values are numbers
  let numericCount = 0;
  for (const val of cleanValues) {
    // Check if it's already a number
    if (typeof val === "number" && !isNaN(val)) {
      numericCount++;
      continue;
    }
    // Check if string can be converted to number
    if (typeof val === "string") {
      const num = Number(val);
      if (!isNaN(num) && isFinite(num)) {
        numericCount++;
      }
    }
  }

  // If more than 80% are numeric, it's a numerical column
  const numericRatio = numericCount / cleanValues.length;
  return numericRatio > 0.8 ? "numerical" : "categorical";
};

const detectProblemTypeWithBackend = async (column) => {
  // Use your existing logic but with backend awareness
  const targetData = dataset.value.map((row) => row[column.name]);
  const cleanData = targetData.filter(
    (val) => val != null && val !== undefined && val !== "" && val !== "null"
  );
  const uniqueValues = new Set(cleanData).size;

  // Your existing detection logic
  if (column.type === "number") {
    if (uniqueValues === 2) return "binary_classification";
    if (uniqueValues <= 10) return "classification";
    return "regression";
  } else {
    if (uniqueValues === 2) return "binary_classification";
    if (uniqueValues <= 20) return "classification";
    return "text_analysis";
  }
};

const loadPreviousData = async () => {
  try {
    console.log("🔄 Loading dataset for target selection...");
    isLoading.value = true;

    // STEP 1: Try mlStore first (fastest)
    if (mlStore.dataset && mlStore.dataset.length > 0) {
      console.log(
        "✅ Found dataset in mlStore:",
        mlStore.dataset.length,
        "rows"
      );
      dataset.value = mlStore.dataset;
      datasetId.value = mlStore.datasetId;
      fileName.value = mlStore.fileName;

      // Extract columns from mlStore data
      if (dataset.value.length > 0) {
        columns.value = Object.keys(dataset.value[0]).map((colName) => ({
          name: colName,
          type: detectColumnType(dataset.value.map((row) => row[colName])),
          originalType: detectColumnType(
            dataset.value.map((row) => row[colName])
          ),
          unique: 0,
          missing: 0,
        }));

        datasetInfo.value = {
          rowCount: dataset.value.length,
          columnCount: columns.value.length,
        };

        console.log("✅ Columns extracted from mlStore:", columns.value.length);
        processColumnsForTargetSelection();
        isLoading.value = false;
        return;
      }
    }

    // STEP 2: Try localStorage
    const processedDataStr = localStorage.getItem("processedData");
    if (processedDataStr) {
      console.log("🔍 Found processedData in localStorage");
      const processedData = JSON.parse(processedDataStr);

      if (processedData.data && processedData.data.length > 0) {
        console.log(
          "✅ Using localStorage data:",
          processedData.data.length,
          "rows"
        );
        dataset.value = processedData.data;
        datasetId.value =
          processedData.backendDatasetId || processedData.datasetId;
        fileName.value = processedData.fileName;

        // Extract columns from localStorage data
        columns.value = Object.keys(dataset.value[0]).map((colName) => ({
          name: colName,
          type: detectColumnType(dataset.value.map((row) => row[colName])),
          originalType: detectColumnType(
            dataset.value.map((row) => row[colName])
          ),
          unique: 0,
          missing: 0,
        }));

        datasetInfo.value = {
          rowCount: dataset.value.length,
          columnCount: columns.value.length,
        };

        console.log("✅ Dataset loaded from localStorage");
        console.log("   - Rows:", dataset.value.length);
        console.log("   - Columns:", columns.value.length);
        console.log("   - Dataset ID:", datasetId.value);

        processColumnsForTargetSelection();
        isLoading.value = false;
        return;
      }
    }

    // STEP 3: Try backend (if available)
    if (mlStore.backendConnected && datasetId.value) {
      console.log("🌐 Attempting to load from backend...");
      const response = await fetch(
        `http://localhost:8000/api/datasets/${datasetId.value}`
      );

      if (response.ok) {
        const backendData = await response.json();
        console.log("✅ Backend data received");

        if (backendData.sampledata && backendData.sampledata.length > 0) {
          dataset.value = backendData.sampledata;

          columns.value = backendData.columns.map((colName) => ({
            name: colName,
            type:
              backendData.dtypes?.[colName]?.includes("int") ||
              backendData.dtypes?.[colName]?.includes("float")
                ? "numerical"
                : "categorical",
            originalType:
              backendData.dtypes?.[colName]?.includes("int") ||
              backendData.dtypes?.[colName]?.includes("float")
                ? "numerical"
                : "categorical",
            unique: 0,
            missing: 0,
          }));

          datasetInfo.value = {
            rowCount: backendData.shape?.[0] || dataset.value.length,
            columnCount: backendData.shape?.[1] || columns.value.length,
          };

          console.log("✅ Dataset loaded from backend");
          processColumnsForTargetSelection();
          isLoading.value = false;
          return;
        }
      }
    }

    // STEP 4: No data found anywhere!
    throw new Error("Dataset not found in mlStore, localStorage, or backend");
  } catch (error) {
    console.error("❌ Error loading dataset:", error);
    alert(
      "Failed to load dataset. Please go back to Data Preview and try again."
    );
    router.push("/data-preview");
  } finally {
    isLoading.value = false;
  }
};

// SIMPLIFIED: processColumnsForTargetSelection

const processColumnsForTargetSelection = () => {
  console.log("🔄 Processing columns for target selection...");

  if (
    !dataset.value ||
    dataset.value.length === 0 ||
    !columns.value ||
    columns.value.length === 0
  ) {
    console.warn("⚠️ No data or columns available for processing");
    availableColumns.value = [];
    return;
  }

  availableColumns.value = columns.value.map((column) => {
    const columnName = column.name;
    const rawData = dataset.value.map((row) => row[columnName]);
    const cleanData = rawData.filter(
      (val) => val !== null && val !== undefined && val !== "" && val !== "null"
    );

    const missingCount = dataset.value.length - cleanData.length;
    const missingPercent = (missingCount / dataset.value.length) * 100;
    const uniqueValues = new Set(cleanData).size;

    // ✅ PROPER TYPE DETECTION
    let currentType = column.type || "categorical";
    let originalType = column.originalType || column.type || "categorical";

    // ✅ BETTER ENCODED COLUMN DETECTION
    const isEncodedColumn = Boolean(
      column.isEncoded ||
        column.encoding ||
        (columnName.includes("_") &&
          uniqueValues <= 2 &&
          cleanData.every((val) => [0, 1, "0", "1"].includes(val)))
    );

    let analysis = {
      name: columnName,
      originalType: originalType,
      type: currentType,
      missingPercent,
      missingValues: missingCount,
      totalRows: dataset.value.length,
      uniqueValues,
      sampleValues: cleanData.slice(0, 10),
      outliers: 0,
      statistics: null,

      // ✅ ENCODING INFO
      encoding: column.encoding || "none",
      isEncoded: isEncodedColumn,
      hasEncoding: isEncodedColumn,
    };

    // ✅ CALCULATE STATISTICS FOR NUMERIC COLUMNS
    if (currentType === "numerical" || currentType === "number") {
      const numbers = cleanData
        .map((val) => parseFloat(String(val).replace(/,/g, "")))
        .filter((n) => !isNaN(n) && isFinite(n));

      if (numbers.length > 0) {
        const mean = numbers.reduce((sum, n) => sum + n, 0) / numbers.length;
        const sorted = [...numbers].sort((a, b) => a - b);
        const median =
          numbers.length % 2 === 0
            ? (sorted[numbers.length / 2 - 1] + sorted[numbers.length / 2]) / 2
            : sorted[Math.floor(numbers.length / 2)];
        const std = Math.sqrt(
          numbers.reduce((sum, n) => sum + Math.pow(n - mean, 2), 0) /
            numbers.length
        );

        analysis.statistics = {
          min: Math.min(...numbers),
          max: Math.max(...numbers),
          mean,
          median,
          std,
        };
        analysis.outliers = detectOutliers(numbers).length;
      }
    }

    // ✅ CALCULATE TARGET SUITABILITY SCORE
    analysis.suitabilityScore = calculateTargetSuitability(analysis);
    analysis.recommended =
      analysis.suitabilityScore >= 70 && !analysis.isEncoded;

    return analysis;
  });

  // ✅ SORT BY SUITABILITY SCORE
  availableColumns.value.sort((a, b) => {
    if (a.recommended !== b.recommended) {
      return b.recommended - a.recommended;
    }
    return b.suitabilityScore - a.suitabilityScore;
  });

  console.log("✅ Columns processed for target selection:", {
    total: availableColumns.value.length,
    recommended: availableColumns.value.filter((col) => col.recommended).length,
    encoded: availableColumns.value.filter((col) => col.isEncoded).length,
  });
};

// ============= TARGET SUITABILITY SCORING =============

const calculateTargetSuitability = (analysis) => {
  let score = 50; // Base score

  console.log(`🎯 Calculating suitability for ${analysis.name}:`, {
    type: analysis.type,
    originalType: analysis.originalType,
    isEncoded: analysis.isEncoded,
    encoding: analysis.encoding,
    uniqueValues: analysis.uniqueValues,
    missingPercent: analysis.missingPercent,
  });

  // ❌ MAJOR PENALTIES: Encoded columns should NOT be targets
  if (analysis.isEncoded) {
    if (analysis.encoding === "onehot") {
      console.log(`❌ One-hot encoded column ${analysis.name} - MAJOR PENALTY`);
      score -= 70; // Massive penalty - these are feature indicators (0/1), not targets
    } else if (analysis.encoding === "label") {
      console.log(`❌ Label encoded column ${analysis.name} - penalty`);
      score -= 40; // Heavy penalty - artificial numeric labels
    } else if (analysis.encoding === "binary") {
      console.log(`❌ Binary encoded column ${analysis.name} - penalty`);
      score -= 35; // Heavy penalty for binary encoding
    } else if (analysis.encoding === "ordinal") {
      console.log(`⚠️ Ordinal encoded column ${analysis.name} - light penalty`);
      score -= 15; // Light penalty - ordinal can sometimes be okay as target
    } else {
      console.log(`⚠️ Unknown encoded column ${analysis.name} - penalty`);
      score -= 30; // General encoded column penalty
    }
  }

  // ❌ PENALTY: Columns with "_" (likely one-hot encoded features)
  if (analysis.name.includes("_") && !analysis.isEncoded) {
    console.log(
      `❌ Column with underscore ${analysis.name} - likely encoded feature`
    );
    score -= 40;
  }

  // ❌ MAJOR PENALTY: ID/Index columns (never good targets)
  if (isIDColumn(analysis)) {
    console.log(`❌ ID/Index column ${analysis.name} - MAJOR PENALTY`);
    score -= 60;
  }

  // ❌ PENALTY: High missing data
  if (analysis.missingPercent > 10) {
    const penalty = Math.min(analysis.missingPercent * 1.2, 40); // Max 40 point penalty
    console.log(
      `⚠️ High missing data ${analysis.name}: ${analysis.missingPercent}% - penalty: ${penalty}`
    );
    score -= penalty;
  }

  // ✅ BONUSES: Only for ORIGINAL (non-encoded) columns
  if (!analysis.isEncoded) {
    // Type bonuses for original data
    if (analysis.originalType === "numerical" || analysis.type === "number") {
      score += 25; // Great for regression
      console.log(`✅ Original numerical column ${analysis.name} - bonus +25`);
    }

    if (analysis.originalType === "categorical" || analysis.type === "string") {
      score += 20; // Great for classification
      console.log(
        `✅ Original categorical column ${analysis.name} - bonus +20`
      );
    }

    // Perfect binary classification (2 classes)
    if (analysis.uniqueValues === 2) {
      score += 30;
      console.log(`✅ Binary classification ${analysis.name} - bonus +30`);
    }

    // Good multi-class classification (3-20 classes)
    else if (analysis.uniqueValues >= 3 && analysis.uniqueValues <= 20) {
      score += 15;
      console.log(
        `✅ Good cardinality ${analysis.name}: ${analysis.uniqueValues} classes - bonus +15`
      );
    }

    // Regression-friendly (many unique values)
    else if (
      analysis.uniqueValues > 20 &&
      (analysis.type === "number" || analysis.originalType === "numerical")
    ) {
      score += 20;
      console.log(
        `✅ Regression-friendly ${analysis.name}: ${analysis.uniqueValues} unique values - bonus +20`
      );
    }

    // Target-like names (strong indicator)
    const targetKeywords = [
      "target",
      "label",
      "class",
      "outcome",
      "result",
      "success",
      "fail",
      "status",
      "category",
      "type",
      "grade",
      "score",
      "rating",
      "price",
      "amount",
      "value",
      "predict",
      "forecast",
      "response",
      "dependent",
      "output",
      "y",
      "salary",
      "income",
      "cost",
      "revenue",
      "profit",
    ];

    if (
      targetKeywords.some((keyword) =>
        analysis.name.toLowerCase().includes(keyword)
      )
    ) {
      score += 35;
      console.log(`✅ Target-like name ${analysis.name} - bonus +35`);
    }

    // Business/Domain relevant terms
    const businessKeywords = [
      "churn",
      "fraud",
      "default",
      "approved",
      "rejected",
      "conversion",
      "retention",
      "satisfaction",
      "quality",
      "performance",
      "efficiency",
    ];

    if (
      businessKeywords.some((keyword) =>
        analysis.name.toLowerCase().includes(keyword)
      )
    ) {
      score += 25;
      console.log(`✅ Business-relevant ${analysis.name} - bonus +25`);
    }
  }

  // ❌ PENALTY: Too many unique values for classification (unless numeric)
  if (analysis.type !== "number" && analysis.originalType !== "numerical") {
    const uniqueRatio = analysis.uniqueValues / analysis.totalRows;
    if (uniqueRatio > 0.8) {
      // More than 80% unique values
      score -= 25;
      console.log(
        `⚠️ Too many unique values ${analysis.name}: ${uniqueRatio.toFixed(
          2
        )} ratio - penalty -25`
      );
    }
  }

  // ❌ PENALTY: Likely feature engineering artifacts
  const featurePatterns = [
    "_mean",
    "_sum",
    "_count",
    "_std",
    "_min",
    "_max",
    "_encoded",
    "_transformed",
  ];
  if (
    featurePatterns.some((pattern) =>
      analysis.name.toLowerCase().includes(pattern)
    )
  ) {
    score -= 30;
    console.log(
      `❌ Feature engineering artifact ${analysis.name} - penalty -30`
    );
  }

  // ✅ BONUS: Good statistical distribution (for numeric)
  if (
    analysis.type === "number" &&
    analysis.statistics &&
    !analysis.isEncoded
  ) {
    const { mean, median, std } = analysis.statistics;

    // Well-distributed data (mean ≈ median)
    if (std > 0 && Math.abs(mean - median) < std * 0.5) {
      score += 10;
      console.log(`✅ Well-distributed numerical ${analysis.name} - bonus +10`);
    }

    // Reasonable variance (not constant)
    if (std / Math.abs(mean) > 0.1) {
      score += 5;
      console.log(`✅ Good variance ${analysis.name} - bonus +5`);
    }
  }

  // Final score with bounds
  const finalScore = Math.max(0, Math.min(100, Math.round(score)));

  console.log(
    `📊 Final suitability score for ${analysis.name}: ${finalScore}`,
    {
      isEncoded: analysis.isEncoded,
      encoding: analysis.encoding,
      recommended: finalScore > 70 && !analysis.isEncoded,
    }
  );

  return finalScore;
};

// =====TARGET RECOMMENDATIONS =====
const getTargetRecommendations = () => {
  if (!selectedColumn.value) return [];

  try {
    const column = selectedColumn.value;
    const recommendations = [];

    // Binary Classification
    if (column.uniqueValues === 2) {
      recommendations.push({
        icon: "🎯",
        title: "Binary Classification",
        description: "Perfect for yes/no or true/false predictions",
        confidence: Math.min(95, column.suitabilityScore),
        taskType: "binary",
      });
    }

    // Multi-class Classification
    if (column.uniqueValues >= 3 && column.uniqueValues <= 20) {
      recommendations.push({
        icon: "🎨",
        title: "Multi-class Classification",
        description: `Categorize data into ${column.uniqueValues} different classes`,
        confidence: Math.min(90, column.suitabilityScore - 5),
        taskType: "multiclass",
      });
    }

    // Regression
    if (column.type === "number" && column.uniqueValues > 20) {
      recommendations.push({
        icon: "📈",
        title: "Regression Analysis",
        description: "Predict continuous numerical values",
        confidence: Math.min(85, column.suitabilityScore),
        taskType: "regression",
      });
    }

    // Time Series (if applicable)
    if (column.type === "date" || /date|time|timestamp/i.test(column.name)) {
      recommendations.push({
        icon: "⏰",
        title: "Time Series Forecasting",
        description: "Predict future values based on temporal patterns",
        confidence: 75,
        taskType: "timeseries",
      });
    }

    // If no specific recommendations, add general one
    if (recommendations.length === 0) {
      recommendations.push({
        icon: "🤖",
        title: "Custom ML Task",
        description:
          "This column can be used for custom machine learning tasks",
        confidence: Math.max(50, column.suitabilityScore - 10),
        taskType: "custom",
      });
    }

    return recommendations.slice(0, 3);
  } catch (error) {
    console.error("Error generating recommendations:", error);
    return [];
  }
};

// ============= CHART GENERATION =============

const generateChart = async () => {
  if (!selectedColumn.value || !chartCanvas.value) return;

  isLoadingChart.value = true;

  try {
    // ✅ CRITICAL: DESTROY EXISTING CHART FIRST
    if (chartInstance.value) {
      console.log("🗑️ Destroying existing chart:", chartInstance.value.id);
      chartInstance.value.destroy();
      chartInstance.value = null;
    }

    // ✅ SMALL DELAY TO ENSURE CLEANUP
    await new Promise((resolve) => setTimeout(resolve, 100));

    // Get canvas context
    const ctx = chartCanvas.value.getContext("2d");

    // Clear the canvas manually
    ctx.clearRect(0, 0, chartCanvas.value.width, chartCanvas.value.height);

    // Use data as-is (already processed in preprocessing step)
    const rawData = dataset.value.map((row) => row[selectedColumn.value.name]);
    const cleanData = rawData.filter(
      (val) => val !== null && val !== undefined && val !== "" && val !== "null"
    );

    // ✅ DYNAMIC IMPORT Chart.js
    const { Chart, registerables } = await import("chart.js");
    Chart.register(...registerables);

    // Generate chart based on type
    if (
      selectedColumn.value.type === "numerical" ||
      selectedColumn.value.type === "number"
    ) {
      const numbers = cleanData
        .map((val) => parseFloat(val))
        .filter((n) => !isNaN(n) && isFinite(n));
      await generateNumericChart(Chart, ctx, numbers);
    } else {
      await generateCategoricalChart(Chart, ctx, cleanData);
    }
  } catch (error) {
    console.error("Chart error:", error);
  } finally {
    isLoadingChart.value = false;
  }
};

const generateNumericChart = async (Chart, ctx, data) => {
  switch (chartType.value) {
    case "histogram":
      await createHistogramChart(Chart, ctx, data);
      break;
    case "box":
      await createBoxPlotChart(Chart, ctx, data);
      break;
    default:
      await createHistogramChart(Chart, ctx, data);
  }
};

const generateCategoricalChart = async (Chart, ctx, data) => {
  const counts = {};
  data.forEach((val) => {
    counts[val] = (counts[val] || 0) + 1;
  });
  const entries = Object.entries(counts)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 15);

  switch (chartType.value) {
    case "doughnut":
      await createDoughnutChart(Chart, ctx, entries);
      break;
    case "bar":
      await createBarChart(Chart, ctx, entries);
      break;
    default:
      await createDoughnutChart(Chart, ctx, entries);
  }
};

// ============= CHART CREATORS =============
const createHistogramChart = async (Chart, ctx, data) => {
  const bins = generateHistogramBins(
    data,
    Math.min(15, Math.max(5, Math.floor(Math.sqrt(data.length))))
  );

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: bins.map((bin) => `${bin.min.toFixed(1)}-${bin.max.toFixed(1)}`),
      datasets: [
        {
          label: "Count",
          data: bins.map((bin) => bin.count),
          backgroundColor: "rgba(102, 126, 234, 0.7)",
          borderColor: "rgba(102, 126, 234, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: getChartOptions("Distribution"),
  });

  console.log("✅ Histogram chart created with ID:", chartInstance.value.id);
};

const createBoxPlotChart = async (Chart, ctx, data) => {
  const sorted = [...data].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)];
  const median = sorted[Math.floor(sorted.length * 0.5)];
  const q3 = sorted[Math.floor(sorted.length * 0.75)];

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Min", "Q1", "Median", "Q3", "Max"],
      datasets: [
        {
          label: "Statistics",
          data: [sorted[0], q1, median, q3, sorted[sorted.length - 1]],
          backgroundColor: [
            "rgba(239, 68, 68, 0.7)",
            "rgba(245, 158, 11, 0.7)",
            "rgba(16, 185, 129, 0.7)",
            "rgba(59, 130, 246, 0.7)",
            "rgba(139, 92, 246, 0.7)",
          ],
        },
      ],
    },
    options: getChartOptions("Box Plot"),
  });

  console.log("✅ Box plot chart created with ID:", chartInstance.value.id);
};

const createDoughnutChart = async (Chart, ctx, entries) => {
  chartInstance.value = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: entries.map(([name]) =>
        name.length > 20 ? name.substring(0, 20) + "..." : name
      ),
      datasets: [
        {
          data: entries.map(([, count]) => count),
          backgroundColor: generateColors(entries.length),
          borderWidth: 2,
          cutout: "60%",
        },
      ],
    },
    options: getPieChartOptions("Value Distribution"),
  });

  console.log("✅ Doughnut chart created with ID:", chartInstance.value.id);
};

const createBarChart = async (Chart, ctx, entries) => {
  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: entries.map(([name]) =>
        name.length > 15 ? name.substring(0, 15) + "..." : name
      ),
      datasets: [
        {
          label: "Count",
          data: entries.map(([, count]) => count),
          backgroundColor: "rgba(102, 126, 234, 0.7)",
          borderColor: "rgba(102, 126, 234, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: getChartOptions("Category Counts"),
  });

  console.log("✅ Bar chart created with ID:", chartInstance.value.id);
};

// ============= CHART HELPERS =============
const getChartOptions = (title) => ({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: "rgba(255, 255, 255, 0.1)" },
      ticks: { color: "rgba(255, 255, 255, 0.8)" },
    },
    x: {
      grid: { color: "rgba(255, 255, 255, 0.1)" },
      ticks: { color: "rgba(255, 255, 255, 0.8)" },
    },
  },
  plugins: {
    legend: { labels: { color: "rgba(255, 255, 255, 0.8)" } },
    title: { display: true, text: title, color: "rgba(255, 255, 255, 0.9)" },
  },
});

const getPieChartOptions = (title) => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "right",
      labels: {
        color: "rgba(255, 255, 255, 0.8)",
        padding: 15,
        usePointStyle: true,
      },
    },
    title: { display: true, text: title, color: "rgba(255, 255, 255, 0.9)" },
  },
});

const generateColors = (count) => {
  const colors = [
    "rgba(102, 126, 234, 0.8)",
    "rgba(118, 75, 162, 0.8)",
    "rgba(16, 185, 129, 0.8)",
    "rgba(245, 158, 11, 0.8)",
    "rgba(239, 68, 68, 0.8)",
    "rgba(139, 92, 246, 0.8)",
  ];
  return Array(count)
    .fill()
    .map((_, i) => colors[i % colors.length]);
};

const generateHistogramBins = (numbers, binCount) => {
  const min = Math.min(...numbers);
  const max = Math.max(...numbers);
  const binSize = (max - min) / binCount;

  if (binSize === 0) return [{ min, max, count: numbers.length }];

  const bins = Array(binCount)
    .fill()
    .map((_, i) => ({
      min: min + i * binSize,
      max: min + (i + 1) * binSize,
      count: 0,
    }));

  numbers.forEach((num) => {
    const binIndex = Math.min(Math.floor((num - min) / binSize), binCount - 1);
    bins[binIndex].count++;
  });

  return bins;
};

// ============= UTILITY FUNCTIONS =============
const detectOutliers = (numbers) => {
  if (numbers.length < 4) return [];
  const sorted = [...numbers].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)];
  const q3 = sorted[Math.floor(sorted.length * 0.75)];
  const iqr = q3 - q1;
  if (iqr === 0) return [];
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;
  return numbers.filter((n) => n < lowerBound || n > upperBound);
};

const isIDColumn = (column) => {
  const namePattern = /^(id|ID|.*_id|.*_ID|key|.*_key)$/i;
  const uniqueRatio = column.uniqueValues / column.totalRows;
  return namePattern.test(column.name) || uniqueRatio > 0.95;
};

// ============= ✅ MISSING UI HELPER FUNCTIONS =============
const getColumnTypeIcon = (type) => {
  const icons = { number: "🔢", string: "📝", date: "📅", boolean: "✅" };
  return icons[type] || "📄";
};

const getColumnPreview = (columnName) => {
  if (!dataset.value || dataset.value.length === 0) return "No data";

  const columnData = dataset.value.slice(0, 5).map((row) => row[columnName]);
  const preview = columnData
    .filter((val) => val !== null && val !== undefined && val !== "")
    .map((val) =>
      String(val).length > 15
        ? String(val).substring(0, 15) + "..."
        : String(val)
    )
    .join(", ");

  return preview || "No preview available";
};

const getScoreClass = (score) => {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "fair";
  return "poor";
};

const getDistributionType = () => {
  if (!selectedColumn.value) return "Unknown";

  if (selectedColumn.value.type === "number") {
    if (selectedColumn.value.encoding === "binary") return "Binary";
    if (selectedColumn.value.encoding === "ordinal") return "Ordinal";
    const uniqueRatio =
      selectedColumn.value.uniqueValues / dataset.value.length;
    return uniqueRatio > 0.8 ? "Continuous" : "Discrete";
  }

  const count = selectedColumn.value.uniqueValues;
  if (count <= 2) return "Binary";
  if (count <= 10) return "Categorical";
  return "High Cardinality";
};

const getOutlierCount = () => {
  if (!selectedColumn.value || selectedColumn.value.type !== "number")
    return "N/A";
  return selectedColumn.value.outliers || 0;
};

const getSkewness = () => {
  if (!selectedColumn.value?.statistics) return "N/A";
  const { mean, median } = selectedColumn.value.statistics;
  if (Math.abs(mean - median) < 0.1) return "Normal";
  return mean > median ? "Right Skewed" : "Left Skewed";
};

const getCompletenessPercentage = () => {
  return selectedColumn.value
    ? Math.round(100 - selectedColumn.value.missingPercent)
    : 0;
};

const getSuitabilityDescription = (score) => {
  if (score >= 80) return "Excellent target variable";
  if (score >= 60) return "Good target variable";
  if (score >= 40) return "Fair target variable";
  return "Poor target variable";
};

const getSuitabilityFactors = () => {
  if (!selectedColumn.value) return [];

  const factors = [];

  // Missing data check
  if (selectedColumn.value.missingPercent < 5) {
    factors.push({ icon: "✅", text: "Low missing data", status: "good" });
  } else {
    factors.push({
      icon: "⚠️",
      text: `${selectedColumn.value.missingPercent.toFixed(1)}% missing data`,
      status: "warning",
    });
  }

  // Unique values check
  const uniqueRatio = selectedColumn.value.uniqueValues / dataset.value.length;
  if (selectedColumn.value.type === "string" && uniqueRatio < 0.5) {
    factors.push({
      icon: "✅",
      text: "Good cardinality for classification",
      status: "good",
    });
  } else if (selectedColumn.value.type === "number") {
    factors.push({
      icon: "✅",
      text: "Numeric data suitable for ML",
      status: "good",
    });
  }

  // Encoding bonus
  if (selectedColumn.value.hasEncoding) {
    factors.push({
      icon: "🔄",
      text: `${selectedColumn.value.encoding} encoding detected`,
      status: "good",
    });
  }

  return factors;
};

const getSampleValues = () => {
  if (!selectedColumn.value || !selectedColumn.value.sampleValues) {
    return [];
  }
  return selectedColumn.value.sampleValues.slice(0, 8);
};

const formatSampleValue = (value) => {
  if (value === null || value === undefined) return "N/A";
  if (typeof value === "number") return value.toLocaleString();
  if (typeof value === "string" && value.length > 50) {
    return value.substring(0, 47) + "...";
  }
  return String(value);
};

// ============= UI INTERACTIONS =============
// ✅ UPDATE YOUR EXISTING selectColumn FUNCTION

// ✅ UPDATE your selectColumn function:
const selectColumn = async (column) => {
  console.log("Selected column:", column.name);
  selectedColumn.value = column;
  selectedTarget.value = column.name;

  // Set chart type based on column type
  if (column.type === "number" || column.type === "numerical") {
    chartType.value = "histogram";
  } else {
    chartType.value = "doughnut";
  }

  // ✅ GENERATE CHART WITH PROPER DELAY
  await nextTick();
  await generateChart();

  console.log("Target selected:", column.name, "with analysis");
};

const onChartTypeChange = async () => {
  if (selectedColumn.value) {
    await nextTick();
    await generateChart();
  }
};

const getChartTypeName = () => {
  const chartNames = {
    histogram: "Histogram",
    box: "Box Plot",
    doughnut: "Doughnut Chart",
    bar: "Bar Chart",
    pie: "Pie Chart",
  };
  return chartNames[chartType.value] || "Chart";
};

// ============= NAVIGATION =============
const goBack = () => navigateTo("/data-preview");

const saveDraft = () => {
  if (selectedColumn.value) {
    const draftState = {
      selectedTarget: selectedColumn.value.name,
      targetColumn: selectedColumn.value,
      savedAt: Date.now(),
    };
    localStorage.setItem("mlAppDraft", JSON.stringify(draftState));
    console.log("💾 Draft saved");
  }
};

// FIXED: In target-selection.vue
// ✅ UPDATE YOUR EXISTING continueToModelSelection FUNCTION

// ✅ UPDATE target-selection.vue continueToModelSelection

const continueToModelSelection = async () => {
  if (!selectedColumn.value) {
    alert("Please select a target column first");
    return;
  }

  try {
    // Get backend dataset ID from stored data
    const processedData = JSON.parse(
      localStorage.getItem("processedData") || "{}"
    );
    const backendDatasetId = processedData.backendDatasetId;

    // ✅ STORE TARGET WITH REAL BACKEND DATASET ID
    const targetData = {
      name: selectedColumn.value.name,
      type: selectedColumn.value.type,
      originalType:
        selectedColumn.value.originalType || selectedColumn.value.type,
      uniqueValues: selectedColumn.value.uniqueValues,
      suitabilityScore: selectedColumn.value.suitabilityScore,
      statistics: selectedColumn.value.statistics,
      missingPercent: selectedColumn.value.missingPercent || 0,

      // ✅ CRITICAL: Include backend dataset ID
      backendDatasetId: backendDatasetId,
      datasetId: processedData.datasetId,
    };
    localStorage.setItem("selectedTarget", JSON.stringify(targetData));

    // ✅ UPDATE ML APP STATE WITH BACKEND INFO
    const currentState = JSON.parse(localStorage.getItem("mlAppState") || "{}");
    currentState.selectedTarget = selectedColumn.value.name;
    currentState.targetColumn = selectedColumn.value;
    currentState.backendDatasetId = backendDatasetId;
    currentState.datasetId = processedData.datasetId;
    currentState.updatedAt = Date.now();
    localStorage.setItem("mlAppState", JSON.stringify(currentState));

    console.log("✅ Target selected with backend info:", {
      target: selectedColumn.value.name,
      backendDatasetId: backendDatasetId,
      datasetId: processedData.datasetId,
    });

    router.push("/algorithm-select");
  } catch (error) {
    console.error("Error in navigation:", error);
    alert(`Navigation failed: ${error.message}`);
  }
};

// ============= WATCHERS =============
watch(chartType, async () => {
  if (selectedColumn.value) {
    await nextTick();
    await generateChart();
  }
});

watch(
  selectedColumn,
  async (newColumn) => {
    if (newColumn) {
      if (newColumn.type === "number" || newColumn.type === "numerical") {
        chartType.value = "histogram";
      } else {
        chartType.value = "doughnut";
      }
    }
  },
  { immediate: false }
);

const debugStorageData = () => {
  console.log("=== STORAGE DEBUG ===");
  console.log("processedData:", localStorage.getItem("processedData"));
  console.log("mlAppState:", localStorage.getItem("mlAppState"));
  console.log("uploadedData:", localStorage.getItem("uploadedData"));
  console.log("====================");
};

// ============= LIFECYCLE =============
onBeforeUnmount(() => {
  if (chartInstance.value) {
    console.log(
      "💀 Component unmounting - destroying chart:",
      chartInstance.value.id
    );
    chartInstance.value.destroy();
    chartInstance.value = null;
  }
});

onMounted(async () => {
  try {
    console.log("🎯 Initializing Target Selection with ML Store...");

    // Initialize ML store first
    await mlStore.checkBackendConnection();

    // Load processed data
    await loadPreviousData();

    // ✅ VERIFY COLUMNS WERE LOADED
    if (availableColumns.value.length === 0) {
      console.error("❌ No columns available after loading");
      // Try to process columns again
      if (columns.value.length > 0) {
        processColumnsForTargetSelection();
      }
    }

    console.log("✅ Target Selection initialized:", {
      backendConnected: mlStore.backendConnected,
      datasetRows: dataset.value.length,
      totalColumns: columns.value.length,
      availableColumns: availableColumns.value.length,
      recommendedColumns: availableColumns.value.filter(
        (col) => col.recommended
      ).length,
    });
  } catch (error) {
    console.error("❌ Target Selection initialization failed:", error);
    alert("Failed to load target selection. Please go back and try again.");
  }
});
</script>

<style scoped lang="css">
/* Base Styles */
.target-selection {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

/* Navigation Header */
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
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
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

/* Hero Section */
.hero-section {
  padding: 1rem 2rem;
  text-align: center;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.hero-section h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-section p {
  font-size: 1.125rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.dataset-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 0.875rem;
}

.summary-item {
  color: #ffffff;
}

.summary-divider {
  color: #667eea;
}

/* Main Content Grid - Enhanced for Better Column Selector */
.main-content {
  display: grid;
  grid-template-columns: 480px 1fr 360px; /* Increased column selector width */
  gap: 2rem;
  padding: 2rem;
  min-height: calc(100vh - 300px);
}

.column-selector {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 180px); /* Even more space - was 200px */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Column Selector Header */
.selector-header {
  flex-shrink: 0; /* Prevent header from shrinking */
  margin-bottom: 0.75rem;
}

.selector-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #ffffff;
}

.selector-subtitle {
  font-size: 0.875rem;
  color: #b3b3d1;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.column-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.27rem; /* Reduced margin */
}

.filter-btn {
  padding: 0.4rem 0.6rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #b3b3d1;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  white-space: nowrap;
}

.filter-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  color: #ffffff;
  transform: translateY(-1px);
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Search Box */
.search-box {
  position: relative;
  margin-bottom: 0.75rem;
  flex-shrink: 0; /* Prevent search box from shrinking */
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #b3b3d1;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 0.6rem 0.6rem 0.6rem 2.2rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.15);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-input::placeholder {
  color: #b3b3d1;
}

/* Column List Container - KEY FIX for Scrolling */
.column-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  margin-bottom: 1rem;
}

.column-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding-right: 8px;
  margin-right: -4px;
  min-height: 400px;
  padding-bottom: 50px;
  scroll-padding-bottom: 50px;
}

.column-item.last-item {
  margin-bottom: 40px; /* Extra space for the very last item */
}

.scroll-spacer {
  height: 50px; /* Increased from 20px to 50px */
  flex-shrink: 0;
  pointer-events: none;
}

/* Column Items */
.column-item {
  padding: 0.8rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  flex-shrink: 0; /* Prevent items from shrinking */
  min-height: 120px;
}

.column-item:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.column-item.selected {
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.2),
    rgba(118, 75, 162, 0.2)
  );
  border-color: #667eea;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
}

.column-item.selected::before {
  content: "✓";
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  color: #10b981;
  font-weight: 700;
  font-size: 1rem;
}

.column-item.recommended {
  border-color: #fbbf24;
  background: rgba(251, 191, 36, 0.1);
}

.column-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.column-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.85rem;
}

.recommendation-badge {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.625rem;
  font-weight: 500;
}

.column-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.type-badge {
  font-size: 0.6rem; /* Smaller */
  padding: 0.1rem 0.4rem; /* Reduced padding */
  border-radius: 4px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.type-badge.number {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}
.type-badge.string {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}
.type-badge.date {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}
.type-badge.boolean {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.unique-count,
.missing-percent {
  font-size: 0.6rem;
  color: #b3b3d1;
}

.missing-percent {
  color: #f87171;
}

.column-preview {
  font-size: 0.6rem;
  color: #9ca3af;
  font-style: italic;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.suitability-score {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.score-bar {
  flex: 1;
  height: 4px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.score-fill.excellent {
  background: #10b981;
}
.score-fill.good {
  background: #3b82f6;
}
.score-fill.fair {
  background: #f59e0b;
}
.score-fill.poor {
  background: #ef4444;
}

.score-text {
  font-size: 0.6rem;
  color: #b3b3d1;
  font-weight: 500;
  min-width: 55px;
  text-align: right;
}

/* No Columns State */
.no-columns {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  text-align: center;
  flex: 1;
}

.no-columns-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-columns p {
  color: #b3b3d1;
  margin: 0 0 1rem 0;
}

.clear-filters-btn {
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-1px);
}

/* Selection Helper */
.selection-helper {
  margin-top: 1rem; /* Increased from 0.75rem */
  padding: 0.6rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  flex-shrink: 0;
}

.helper-message,
.helper-selected {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.helper-icon {
  font-size: 1rem;
}

.helper-text {
  font-size: 0.8rem;
  color: #b3b3d1;
}

.helper-selected .helper-text {
  color: #10b981;
  font-weight: 500;
}

.column-list::-webkit-scrollbar {
  width: 10px; /* Wider scrollbar */
}

.column-list::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 5px;
  margin: 8px 0 50px 0;
}

.column-list::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.5); /* More visible */
  border-radius: 5px;
  border: 1px solid rgba(26, 26, 46, 0.2);
}

.column-list::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.7);
}

.column-list::-webkit-scrollbar-thumb:active {
  background: rgba(102, 126, 234, 0.9);
}

/* Firefox Scrollbar */
.column-list {
  scrollbar-width: thin;
  scrollbar-color: rgba(102, 126, 234, 0.4) rgba(102, 126, 234, 0.1);
}

/* Preview Panel */
.preview-panel {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.preview-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

.chart-controls {
  display: flex;
  gap: 1rem;
}

.chart-selector {
  padding: 0.5rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.875rem;
  cursor: pointer;
}

.chart-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h4 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.empty-state p {
  color: #b3b3d1;
  margin: 0;
}

.loading-chart {
  text-align: center;
  padding: 2rem;
}

.chart-skeleton {
  width: 100%;
  height: 300px;
  background: linear-gradient(
    90deg,
    rgba(102, 126, 234, 0.1) 0%,
    rgba(102, 126, 234, 0.2) 50%,
    rgba(102, 126, 234, 0.1) 100%
  );
  border-radius: 8px;
  animation: shimmer 2s infinite;
  margin-bottom: 1rem;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.interactive-chart {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-placeholder {
  flex: 1;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  margin-bottom: 1rem;
  padding: 1rem;
  position: relative;
}

.chart-placeholder.loading {
  opacity: 0.5;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 26, 46, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  border-radius: 8px;
}

.chart-placeholder canvas {
  max-width: 100%;
  max-height: 100%;
}

.chart-insights {
  margin-top: auto;
}

.insight-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.insight-card {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.insight-label {
  display: block;
  font-size: 0.75rem;
  color: #b3b3d1;
  margin-bottom: 0.25rem;
}

.insight-value {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

/* Right Panel - Insights */
.insights-panel {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 400px);
  overflow-y: auto;
}

.insights-panel h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
}

.no-selection {
  text-align: center;
  padding: 2rem 1rem;
  color: #b3b3d1;
}

.target-insights {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.insight-section h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 6px;
}

.stat-label {
  font-size: 0.875rem;
  color: #b3b3d1;
}

.stat-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
}

.suitability-analysis {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suitability-score-large {
  text-align: center;
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 auto 0.5rem;
  position: relative;
}

.score-circle.excellent {
  background: conic-gradient(#10b981 0% 80%, rgba(102, 126, 234, 0.2) 80% 100%);
}

.score-circle.good {
  background: conic-gradient(#3b82f6 0% 60%, rgba(102, 126, 234, 0.2) 60% 100%);
}

.score-circle.fair {
  background: conic-gradient(#f59e0b 0% 40%, rgba(102, 126, 234, 0.2) 40% 100%);
}

.score-circle.poor {
  background: conic-gradient(#ef4444 0% 20%, rgba(102, 126, 234, 0.2) 20% 100%);
}

.score-description {
  font-size: 0.875rem;
  color: #b3b3d1;
}

.suitability-factors {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.factor-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 6px;
}

.factor-icon {
  font-size: 1rem;
}

.factor-icon.good {
  color: #10b981;
}
.factor-icon.warning {
  color: #f59e0b;
}
.factor-icon.error {
  color: #ef4444;
}

.factor-text {
  font-size: 0.75rem;
  color: #b3b3d1;
}

.sample-values {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sample-item {
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 4px;
  font-size: 0.75rem;
  font-family: "Monaco", "Menlo", monospace;
  color: #ffffff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.rec-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.rec-content {
  flex: 1;
}

.rec-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.rec-description {
  font-size: 0.75rem;
  color: #b3b3d1;
  line-height: 1.4;
}

/* Footer */
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

@keyframes pulse {
  0% {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  }
  50% {
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.6);
  }
  100% {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  }
}

/* ✅ AI Disclaimer Styling */
.ai-disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  background: linear-gradient(135deg, #fff3cd 0%, #fff8e1 100%);
  border-left: 3px solid #ffc107;
  border-radius: 8px;
  margin: 16px 0;
  font-size: 0.85rem;
  line-height: 1.5;
}

.disclaimer-compact {
  margin: 10px 0 12px 0;  /* Tight margins */
  background: linear-gradient(135deg, #fff3cd 0%, #fff8e1 100%);
  border-left: 3px solid #ffc107;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  flex-shrink: 0;  /* Prevent shrinking in flex layout */
}

/* Optional: Add subtle shadow when expanded */
.disclaimer-compact.expanded {
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.15);
}

/* Toggle Button */
.disclaimer-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;  /* Tight gap between elements */
  padding: 8px 12px;  /* Compact padding */
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;  /* Small font size */
  font-weight: 600;
  color: #856404;  /* Dark amber color */
  transition: all 0.2s ease;
  text-align: left;
}

/* Hover Effect */
.disclaimer-toggle:hover {
  background: rgba(255, 193, 7, 0.1);
}

/* Focus State (for accessibility) */
.disclaimer-toggle:focus {
  outline: 2px solid rgba(255, 193, 7, 0.4);
  outline-offset: -2px;
}

/* Warning Icon */
.disclaimer-icon {
  font-size: 0.9rem;  /* Smaller icon */
  flex-shrink: 0;
  line-height: 1;
}

/* Title Text */
.disclaimer-title {
  flex: 1;
  text-align: left;
  font-weight: 600;
}

/* Arrow Icon */
.disclaimer-toggle svg {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
  flex-shrink: 0;
  fill: currentColor;
}

/* Arrow Rotation When Expanded */
.disclaimer-toggle svg.rotated {
  transform: rotate(180deg);
}

/* Expandable Content */
.disclaimer-content {
  padding: 0 12px 10px 12px;  /* Compact padding (no top padding) */
  animation: slideDown 0.3s ease;
  overflow: hidden;
}

/* Content Text */
.disclaimer-content p {
  margin: 0;
  font-size: 0.75rem;  /* Smaller text */
  line-height: 1.5;
  color: #856404;  /* Dark amber */
}

/* Slide Down Animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 200px;  /* Adjust based on content */
  }
}

/* Optional: Slide Up Animation (when closing) */
@keyframes slideUp {
  from {
    opacity: 1;
    transform: translateY(0);
    max-height: 200px;
  }
  to {
    opacity: 0;
    transform: translateY(-8px);
    max-height: 0;
  }
}

.selection-summary {
  text-align: center;
  font-size: 0.875rem;
}

.selected-target {
  color: #10b981;
}

.no-target {
  color: #9ca3af;
}

.footer-actions {
  display: flex;
  gap: 1rem;
}

/* Responsive Design */
@media (max-width: 1400px) {
  .main-content {
    grid-template-columns: 400px 1fr 350px;
  }
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 350px 1fr 320px;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .column-list {
    padding-bottom: 40px; /* More padding on mobile */
  }

  .column-selector {
    max-height: 500px;
  }
}
</style>
