<template>
  <div v-if="modelValue" class="drawer-overlay" @click="$emit('update:modelValue', false)">
    <div class="drawer-content" @click.stop>
      <!-- Header -->
      <div class="drawer-header">
        <div class="header-main">
          <div class="column-info">
            <span class="column-type-icon" :class="insights?.type">
              <span v-if="insights?.type === 'numeric'">#</span>
              <span v-else-if="insights?.type === 'datetime'">📅</span>
              <span v-else>Abc</span>
            </span>
            <h2>{{ columnName }}</h2>
          </div>
          <button @click="$emit('update:modelValue', false)" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
            </svg>
          </button>
        </div>
        <div class="semantic-badge" v-if="insights?.semantic_type">
          {{ insights.semantic_type.toUpperCase() }}
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="drawer-body loading-state">
        <div class="spinner"></div>
        <p>Analyzing column diagnostics...</p>
      </div>

      <!-- Main Content -->
      <div v-else-if="insights" class="drawer-body">
        <!-- Key Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card">
            <span class="label">Missing %</span>
            <span class="value" :class="{ 'warning': insights.missing_pct > 0 }">{{ insights.missing_pct }}%</span>
          </div>
          <div class="stat-card">
            <span class="label">Cardinality</span>
            <span class="value">{{ insights.unique_count }}</span>
          </div>
          <template v-if="insights.type === 'numeric'">
            <div class="stat-card">
              <span class="label">Mean</span>
              <span class="value">{{ formatValue(insights.mean) }}</span>
            </div>
            <div class="stat-card">
              <span class="label">Median</span>
              <span class="value">{{ formatValue(insights.median) }}</span>
            </div>
            <div class="stat-card" :title="`Total Outliers: ${insights.outlier_count}\nExtreme Outliers: ${insights.extreme_outlier_count}`">
              <span class="label">Outlier Ratio</span>
              <span class="value" :class="{ 'warning': insights.outlier_pct > 5 }">
                {{ insights.outlier_pct }}%
                <small v-if="insights.extreme_outlier_count > 0" class="extreme-badge">!</small>
              </span>
            </div>
          </template>
          <template v-else-if="insights.type === 'datetime'">
            <div class="stat-card">
              <span class="label">Min Date</span>
              <span class="value date-value" :title="insights.min_date">{{ formatDate(insights.min_date) }}</span>
            </div>
            <div class="stat-card">
              <span class="label">Max Date</span>
              <span class="value date-value" :title="insights.max_date">{{ formatDate(insights.max_date) }}</span>
            </div>
          </template>
          <template v-else>
            <div class="stat-card">
              <span class="label">Most Frequent</span>
              <span class="value" :title="insights.most_frequent">{{ truncate(insights.most_frequent) }}</span>
            </div>
            <div class="stat-card">
              <span class="label">Imbalance</span>
              <span class="value">{{ insights.imbalance_ratio }}</span>
            </div>
          </template>
        </div>

        <!-- Suggestion Alert -->
        <div v-if="insights.suggested_actions?.length" class="suggestion-box">
          <div class="suggestion-header">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,2A10,10 0 1,0 22,12A10,10 0 0,0 12,2M11,17H13V15H11V17M11,13H13V7H11V13Z" />
            </svg>
            <strong>Suggested Actions</strong>
          </div>
          <ul class="suggestion-list">
            <li v-for="(action, idx) in insights.suggested_actions" :key="idx">
              {{ action }}
            </li>
          </ul>
          <div v-if="insights.type !== 'datetime'" class="prep-tip">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M11,9H13V7H11V9M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z" />
            </svg>
            <span>You can resolve these issues using our <strong>Advanced Prep toolkit</strong>.</span>
          </div>
        </div>

        <!-- Visualizations -->
        <div class="visuals-section">
          <div class="visuals-header">
            <h3>Data Distribution</h3>
            <div v-if="insights.type === 'numeric'" class="chart-toggle">
              <button 
                @click="activeChart = 'histogram'" 
                :class="{ active: activeChart === 'histogram' }"
              >Histogram</button>
              <button 
                @click="activeChart = 'boxplot'" 
                :class="{ active: activeChart === 'boxplot' }"
              >Boxplot</button>
            </div>
          </div>
          
          <div class="chart-container">
            <canvas ref="chartCanvas"></canvas>
          </div>
          
          <div v-if="insights.type === 'numeric'" class="detailed-metrics">
            <h4>Numeric Summary</h4>
            <div class="metrics-row">
              <span>Distribution Type:</span> <strong>{{ insights.skewness_interpretation }}</strong>
            </div>
            <div class="metrics-row">
              <span>Min / Max / Range:</span> <strong>{{ formatValue(insights.min) }} / {{ formatValue(insights.max) }} ({{ formatValue(insights.max - insights.min) }})</strong>
            </div>
            <div class="metrics-row">
              <span>Std Dev / IQR:</span> <strong>{{ formatValue(insights.std) }} / {{ formatValue(insights.iqr) }}</strong>
            </div>
            <div class="metrics-row divider"></div>
            <div class="metrics-row">
              <span>Raw Skewness:</span> <strong :class="{ 'warning': Math.abs(insights.raw_skewness) > 1 }">{{ formatValue(insights.raw_skewness) }}</strong>
            </div>
            <div class="metrics-row">
              <span>Robust Skewness:</span> <strong :class="{ 'warning': Math.abs(insights.robust_skewness) > 0.7 }">{{ formatValue(insights.robust_skewness) }}</strong>
            </div>
            <div class="metrics-row">
              <span>Skewness Gap:</span> <strong :title="Math.abs(insights.skewness_gap) > 1 ? 'Distortion likely' : 'Low distortion'">{{ formatValue(insights.skewness_gap) }}</strong>
            </div>
            <div class="metrics-row divider"></div>
            <div class="metrics-row">
              <span>Outlier / Extreme Counts:</span> <strong>{{ insights.outlier_count }} / {{ insights.extreme_outlier_count }}</strong>
            </div>
          </div>
          <div v-else-if="insights.type === 'datetime'" class="detailed-metrics">
            <h4>Temporal Summary</h4>
            <div class="metrics-row">
              <span>Date Range:</span> <strong :title="insights.date_range">{{ insights.date_range }}</strong>
            </div>
            <div class="metrics-row">
              <span>Granularity:</span> <strong>{{ insights.granularity }}</strong>
            </div>
            <div class="metrics-row" v-if="insights.invalid_count > 0">
              <span>Invalid Formats:</span> <strong class="warning">{{ insights.invalid_count }}</strong>
            </div>
          </div>
          <div v-else class="detailed-metrics">
            <h4>Categorical Summary</h4>
            <div class="metrics-row">
              <span>Least Frequent:</span> <strong :title="insights.least_frequent">{{ truncate(insights.least_frequent) }}</strong>
            </div>
            <div class="metrics-row">
              <span>Rare Categories (<1%):</span> <strong>{{ insights.rare_category_count }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { useAuthenticatedFetch } from '../composables/useAuthenticatedFetch';

const props = defineProps({
  modelValue: Boolean,
  datasetId: String,
  columnName: String,
  refreshKey: Number
});

const emit = defineEmits(['update:modelValue']);

const { authenticatedGet } = useAuthenticatedFetch();
const loading = ref(false);
const insights = ref(null);
const chartCanvas = ref(null);
const activeChart = ref('histogram');
let chartInstance = null;

const fetchInsights = async () => {
  if (!props.columnName || !props.datasetId) return;
  
  const { authenticatedGet } = useAuthenticatedFetch();
  loading.value = true;
  insights.value = null;
  
  try {
    const response = await authenticatedGet(`/api/datasets/${encodeURIComponent(props.datasetId)}/columns/${encodeURIComponent(props.columnName)}/insights`);
    if (response.ok) {
      insights.value = await response.json();
      nextTick(() => {
        renderChart();
      });
    }
  } catch (error) {
    console.error("Failed to fetch column insights:", error);
  } finally {
    loading.value = false;
  }
};

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  if (!chartCanvas.value || !insights.value) return;

  const ctx = chartCanvas.value.getContext('2d');
  const type = insights.value.type;
  
  let data = {};
  let chartType = 'bar';

  if ((type === 'numeric' && activeChart.value === 'histogram') || type === 'categorical') {
    if (type === 'numeric') {
      const { counts, bin_edges } = insights.value.distribution.histogram;
      const labels = bin_edges.slice(0, -1).map((edge, i) => {
        return `${formatValue(edge)} - ${formatValue(bin_edges[i+1])}`;
      });
      
      data = {
        labels: labels,
        datasets: [{
          label: 'Frequency',
          data: counts,
          backgroundColor: 'rgba(99, 102, 241, 0.6)',
          borderColor: 'rgb(99, 102, 241)',
          borderWidth: 1,
          barPercentage: 1,
          categoryPercentage: 1,
        }]
      };
    } else {
      const counts = insights.value.distribution.bar_chart;
      data = {
        labels: Object.keys(counts).map(l => truncate(l, 10)),
        datasets: [{
          label: 'Count',
          data: Object.values(counts),
          backgroundColor: 'rgba(16, 185, 129, 0.6)',
          borderColor: 'rgb(16, 185, 129)',
          borderWidth: 1
        }]
      };
    }

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: chartOptions
    });
  } else if (activeChart.value === 'boxplot' && type === 'numeric') {
    // Basic Boxplot using bar chart hacks or better just custom drawing
    // Chart.js doesn't have native boxplot without plugins, but we can simulate it or use a simple stats view
    // For now, let's just stick to Histogram as the primary visual since we have the stats below.
    // If I wanted real boxplot I'd need charjs-boxplot-plugin which might not be here.
    // Let's implement a "Stat labels" box instead or just a message.
    
    chartInstance = new Chart(ctx, {
      type: 'bar', // Fallback or placeholder
      data: {
        labels: ['Min', 'Q1', 'Median', 'Q3', 'Max'],
        datasets: [{
          label: 'Values',
          data: [
            insights.value.distribution.box_plot.min,
            insights.value.distribution.box_plot.q1,
            insights.value.distribution.box_plot.median,
            insights.value.distribution.box_plot.q3,
            insights.value.distribution.box_plot.max
          ],
          backgroundColor: 'rgba(99, 102, 241, 0.4)'
        }]
      },
      options: chartOptions
    });
  } else if (type === 'datetime') {
    const counts = insights.value.distribution.time_frequency;
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: Object.keys(counts),
        datasets: [{
          label: 'Frequency',
          data: Object.values(counts),
          borderColor: '#818cf8',
          backgroundColor: 'rgba(129, 140, 248, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        ...chartOptions,
        scales: {
          ...chartOptions.scales,
          y: { ...chartOptions.scales.y, beginAtZero: true }
        }
      }
    });
  }
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: {
      beginAtZero: false,
      grid: { color: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#94a3b8' }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94a3b8' }
    }
  }
};

const formatValue = (val) => {
  if (val === null || val === undefined) return '-';
  if (typeof val !== 'number') return val;
  if (Number.isInteger(val)) return val;
  return val.toFixed(2);
};

const truncate = (str, len = 20) => {
  if (!str) return '-';
  str = String(str);
  return str.length > len ? str.substring(0, len) + '...' : str;
};

const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  } catch (e) {
    return dateStr;
  }
};

watch(() => activeChart.value, () => {
  renderChart();
});

watch(() => props.refreshKey, () => {
  if (props.modelValue) {
    fetchInsights();
  }
});

watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    fetchInsights();
  } else if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
});

watch(() => props.columnName, () => {
  if (props.modelValue) {
    fetchInsights();
  }
});
</script>

<style scoped>
.drawer-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 2000;
  display: flex;
  justify-content: flex-end;
}

.drawer-content {
  width: 100%;
  max-width: 450px;
  background: #1a1a2e;
  height: 100vh;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.drawer-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.02);
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.column-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.column-type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
}

.column-type-icon.numeric {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
}

.column-type-icon.categorical {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.column-type-icon.datetime {
  background: rgba(129, 140, 248, 0.2);
  color: #818cf8;
}

h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #fff;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.semantic-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #94a3b8;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.loading-state {
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(99, 102, 241, 0.1);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-card .label {
  display: block;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 4px;
}

.stat-card .value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
}


.stat-card .value.date-value {
  font-size: 0.95rem;
  word-break: break-all;
}

.suggestion-box {
  background: rgba(251, 191, 36, 0.05);
  border: 1px solid rgba(251, 191, 36, 0.2);
  border-radius: 12px;
  padding: 16px;
}

.suggestion-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fbbf24;
  margin-bottom: 12px;
}

.suggestion-list {
  padding-left: 20px;
  margin: 0 0 16px 0;
  color: #d1d5db;
  font-size: 0.9rem;
}

.suggestion-list li {
  margin-bottom: 6px;
}

.prep-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(99, 102, 241, 0.1);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.prep-tip svg {
  color: #818cf8;
  flex-shrink: 0;
}

.prep-tip strong {
  color: #fff;
}

.visuals-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.visuals-header h3 {
  margin: 0;
}

.chart-toggle {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  padding: 4px;
  border-radius: 8px;
  gap: 4px;
}

.chart-toggle button {
  background: none;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
}

.chart-toggle button.active {
  background: #6366f1;
  color: #fff;
}

.chart-container {
  height: 250px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.detailed-metrics h4 {
  font-size: 0.9rem;
  color: #94a3b8;
  margin: 0 0 12px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metrics-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.95rem;
}

.metrics-row:last-child {
  border-bottom: none;
}

.metrics-row span {
  color: #94a3b8;
}

.metrics-row strong {
  color: #e2e8f0;
}

.metrics-row strong.warning {
  color: #f87171;
}

.metrics-row.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.05);
  margin: 4px 0;
  padding: 0;
}

.extreme-badge {
  font-size: 0.7rem;
  background: #ef4444;
  color: white;
  padding: 0 4px;
  border-radius: 4px;
  vertical-align: super;
  margin-left: 2px;
  font-weight: 800;
}
</style>
