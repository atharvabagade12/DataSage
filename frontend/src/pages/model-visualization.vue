<template>
  <div class="model-visualization">
      <PageHeader 
      title="Model Visualization" 
      description="Visualize the performance of your model with interactive charts and insights."
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


    <div class="main-container" v-if="loading">
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Generating visualizations...</p>
      </div>
    </div>

    <div class="main-container" v-else-if="error">
      <div class="error-state">
        <span class="error-icon">⚠️</span>
        <h3>Visualization Failed</h3>
        <p>{{ error }}</p>
        <button @click="fetchVisualizationData" class="retry-btn">Retry Analysis</button>
      </div>
    </div>

    <div class="main-container" v-else>
      <!-- Summary Dashboard -->
      <div class="summary-dashboard">
        <div class="summary-card main-info">
          <div class="card-header">
            <h3>Model Summary</h3>
            <span class="algo-badge">{{ modelSummary.algorithm }}</span>
          </div>
          <div class="summary-grid">
            <div class="summary-item">
              <label>Problem Type</label>
              <span>{{ capitalize(modelSummary.problem_type) }}</span>
            </div>
            <div class="summary-item">
              <label>Validation</label>
              <span>{{ formatValidation(modelSummary.validation_method) }}</span>
            </div>
            <div class="summary-item">
              <label>Features</label>
              <span>{{ plotData.feature_importance?.length || 'N/A' }} Used</span>
            </div>
            <div class="summary-item">
              <label>Dataset Size</label>
              <span>{{ modelSummary.samples_train + modelSummary.samples_test }} Rows</span>
            </div>
          </div>
        </div>

        <!-- Metrics Overview -->
        <div class="summary-card metrics-card">
          <h3>Key Performance Metrics</h3>
          <div class="metrics-grid">
            <template v-if="modelSummary.problem_type === 'classification'">
              <div class="mini-metric">
                <span class="m-val">{{ (modelSummary.final_metrics.test_accuracy * 100).toFixed(1) }}%</span>
                <label>Accuracy</label>
              </div>
              <div class="mini-metric">
                <span class="m-val">{{ (modelSummary.final_metrics.test_f1 * 100).toFixed(1) }}%</span>
                <label>F1-Score</label>
              </div>
            </template>
            <template v-else>
              <div class="mini-metric">
                <span class="m-val">{{ modelSummary.final_metrics.test_r2.toFixed(3) }}</span>
                <label>R² Score</label>
              </div>
              <div class="mini-metric">
                <span class="m-val">{{ formatNumber(modelSummary.final_metrics.test_rmse.toFixed(2)) }}</span>
                <label>RMSE</label>
              </div>
            </template>
          </div>
        </div>

        <!-- Auto Insights Card -->
        <div class="summary-card insights-card">
          <div class="card-header">
            <h3>Automated Insights</h3>
            <span class="ai-badge">AI Generated</span>
          </div>
          <div class="insights-list">
            <div v-for="(insight, i) in insights" :key="i" class="insight-item" :class="insight.verdict">
              <div class="insight-status"></div>
              <p>{{ insight.text }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Visualization Sections -->
      <div class="visuals-grid">
        <!-- REGRESSION PLOTS -->
        <template v-if="modelSummary.problem_type === 'regression'">
          <!-- Actual vs Predicted -->
          <div class="vis-section full-width">
            <div class="section-info">
              <div class="header-with-metric">
                <h3>Actual vs. Predicted Values</h3>
                <div v-if="modelSummary.final_metrics?.test_r2" class="metric-chip">
                  R² Score: <strong>{{ modelSummary.final_metrics.test_r2.toFixed(3) }}</strong>
                </div>
              </div>
              <p class="description">How closely the model's predictions align with ground truth.</p>
              <div class="instructional-box">
                <p class="howto"><strong>How to read:</strong> Points closer to the diagonal indicate better predictions. Vertical distance from the line represents prediction error.</p>
                <ul class="reg-insights">
                  <li>✨ <strong>Tight clustering along diagonal</strong> → Strong model performance</li>
                  <li>⚠️ <strong>Systematic offset</strong> → Model bias (over or under prediction)</li>
                  <li>🌪️ <strong>Fan-shaped spread</strong> → Variance changes with scale (Heteroscedasticity)</li>
                </ul>
              </div>
            </div>
            <div class="chart-wrapper large">
              <canvas id="actualVsPredictedChart"></canvas>
            </div>
          </div>

          <!-- Residuals Plot -->
          <div class="vis-section">
            <div class="section-info">
              <h3>Residuals vs. Predicted</h3>
              <p class="description">Visualizes error distribution across prediction scales.</p>
              <div class="instructional-box">
                <p class="howto">Residuals should be randomly scattered around zero with no visible pattern.</p>
                <div class="pattern-detect">
                  <strong>Pattern Detection:</strong>
                  <ul>
                    <li>📐 <strong>Funnel shape</strong> → Error variance increases with magnitude</li>
                    <li>🌊 <strong>Curved pattern</strong> → Non-linear relationship not captured</li>
                    <li>🍱 <strong>Clusters</strong> → Potential missing categorical interactions</li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="chart-wrapper">
              <canvas id="residualsChart"></canvas>
            </div>
          </div>

          <!-- Error Distribution -->
          <div class="vis-section">
            <div class="section-info">
              <h3>Error Distribution</h3>
              <p class="description">Frequency and magnitude of prediction errors.</p>
              <div class="instructional-box">
                <p class="howto">A bell-shaped distribution centered at zero indicates unbiased errors.</p>
                <div class="pattern-detect">
                  <strong>Shape Insights:</strong>
                  <ul>
                    <li>⚖️ <strong>Skewed</strong> → Systematic over or under prediction</li>
                    <li>🐘 <strong>Heavy tails</strong> → Frequent outliers or large errors</li>
                    <li>⛰️ <strong>Multi-modal</strong> → Hidden sub-groups/patterns in data</li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="chart-wrapper">
              <canvas id="errorDistChart"></canvas>
            </div>
          </div>
        </template>

       
        <!-- CLASSIFICATION PLOTS -->
        
        <template v-else>
          <!-- Confusion Matrix with Insight Panel -->
          <div class="vis-section full-width cm-insight-section">
            <div class="cm-layout-container">
              <!-- Left: The Visual Heatmap -->
              <div class="cm-visual-side">
                <div class="section-info">
                  <h3>Confusion Matrix</h3>
                  <p class="description">Detailed breakdown of correct and incorrect classifications.</p>
                  <div class="educational-note">
                    <strong>Diagonal mastery:</strong> The diagonal cells (top-left to bottom-right) represent correct classifications. Higher numbers here are better.
                  </div>
                </div>
                <div class="matrix-container">
                  <div class="cm-grid" :style="{ gridTemplateColumns: `auto repeat(${classes.length}, 1fr)` }">
                    <div class="cm-corner">Actual \ Pred</div>
                    <div v-for="cls in classes" :key="'h-'+cls" class="cm-header">{{ cls }}</div>
                    
                    <template v-for="(row, i) in confusionMatrix" :key="'row-'+i">
                      <div class="cm-row-label">{{ classes[i] }}</div>
                      <div v-for="(val, j) in row" :key="'cell-'+i+'-'+j" 
                           class="cm-cell" 
                           :style="{ backgroundColor: getCMAlpha(val) }">
                        {{ val }}
                      </div>
                    </template>
                  </div>
                </div>
              </div>

              <!-- Right: Interpretation Panel -->
              <div class="cm-analysis-side" v-if="cmMetrics">
                <div class="panel-header">
                  <div class="title-wrap">
                    <h2>Classification Breakdown</h2>
                    <p class="subtitle">Key insights derived from the confusion matrix</p>
                  </div>
                </div>

                <!-- Derived Metrics Block (Binary) -->
                <div class="analysis-section" v-if="cmMetrics.binary">
                  <h4 class="mini-title">Derived Metrics <span class="pos-context">(Positive Class: {{ cmMetrics.posLabel || '1' }})</span></h4>
                  <div class="raw-counts-grid">
                    <div class="count-item"><strong>TP:</strong> {{ cmMetrics.tp }}</div>
                    <div class="count-item"><strong>FP:</strong> {{ cmMetrics.fp }}</div>
                    <div class="count-item"><strong>FN:</strong> {{ cmMetrics.fn }}</div>
                    <div class="count-item"><strong>TN:</strong> {{ cmMetrics.tn }}</div>
                  </div>
                  
                  <div class="derived-grid">
                    <div class="derived-card">
                      <label>Recall</label>
                      <span class="d-val">{{ (cmMetrics.recall * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="derived-card">
                      <label>Precision</label>
                      <span class="d-val">{{ (cmMetrics.precision * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="derived-card">
                      <label>False Positive Rate</label>
                      <span class="d-val">{{ (cmMetrics.fpr * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="derived-card">
                      <label>False Negative Rate</label>
                      <span class="d-val">{{ (cmMetrics.fnr * 100).toFixed(1) }}%</span>
                    </div>
                  </div>
                </div>

                <!-- Multiclass breakdown -->
                <div class="analysis-section" v-else>
                  <h4 class="mini-title">Per-Class Performance</h4>
                  <div class="class-recall-list">
                    <div v-for="c in cmMetrics.perClassRecall" :key="c.label" class="recall-row">
                      <span class="r-label">{{ c.label }}</span>
                      <div class="r-progress-bg">
                        <div class="r-progress-fill" :style="{ width: (c.recall * 100) + '%' }"></div>
                      </div>
                      <span class="r-value">{{ (c.recall * 100).toFixed(0) }}%</span>
                    </div>
                  </div>
                </div>

                <!-- Interpretation -->
                <div class="analysis-section highlight">
                  <div class="interpretation-content">
                    <p class="plain-talk">{{ cmInsights.interpretation }}</p>
                    <div class="insight-badges">
                      <span v-for="b in cmInsights.badges" :key="b.text" :class="['i-badge', b.type]">
                        {{ b.text }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Implication -->
                <div class="analysis-section">
                  <h4 class="mini-title">Why This Matters</h4>
                  <p class="summary-text">{{ cmInsights.whyMatters }}</p>
                </div>

                <!-- Suggestions -->
                <div class="analysis-section">
                  <h4 class="mini-title">Actionable Suggestions</h4>
                  <ul class="suggestion-list">
                    <li v-for="s in cmInsights.suggestions" :key="s">{{ s }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- ROC Curve -->
          <div class="vis-section" v-if="canShowROC">
            <div class="section-info">
              <h3>ROC Curve</h3>
              <p class="description">Trade-off between True Positive and False Positive rates.</p>
              <div class="educational-note">
                <strong>The Goal:</strong> The closer the curve is to the top-left corner, the better the model is at discriminating between classes.
              </div>
            </div>
            <div class="chart-wrapper">
              <canvas id="rocChart"></canvas>
            </div>
          </div>

          <!-- Precision-Recall Curve -->
          <div class="vis-section" v-if="canShowROC">
            <div class="section-info">
              <h3>Precision-Recall Curve</h3>
              <p class="description">Performance specifically regarding the positive class.</p>
              <div class="educational-note">
                <strong>Use Case:</strong> Especially useful for imbalanced datasets where the positive class is rare.
              </div>
            </div>
            <div class="chart-wrapper">
              <canvas id="prChart"></canvas>
            </div>
          </div>
        </template>
        
        <!-- Feature Importance -->
        <div class="vis-section full-width" v-if="plotData.feature_importance">
          <div class="section-info">
            <h3>Feature Significance</h3>
            <p class="description">Which data points influenced the model's decisions the most.</p>
            <div class="educational-note">
              <strong>Understanding Impact:</strong> This shows the relative weight the algorithm placed on each column. Higher bars mean that feature was more critical for predictions.
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas id="importanceChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router';
import { useAuthenticatedFetch } from '@/composables/useAuthenticatedFetch';
import { useExperimentStore } from '@/stores/experiment';
import Chart from 'chart.js/auto';

const route = useRoute();
const router = useRouter();
const experimentStore = useExperimentStore();

const loading = ref(true);
const error = ref(null);
const modelSummary = ref({});
const plotData = ref({});
const insights = ref([]);
const classes = ref([]);
const confusionMatrix = ref([]);

// Chart instances
let actualVsPredChart = null;
let residualsChart = null;
let errorDistChart = null;
let rocChart = null;
let prChart = null;
let importanceChart = null;

const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const formatNumber = (num) => new Intl.NumberFormat().format(num);

const formatValidation = (v) => {
  const map = {
    'simple': 'Train/Test Split',
    'train_test_split': 'Train/Test Split',
    'kfold_cv': 'K-Fold CV',
    'grid_search': 'Grid Search CV',
    'randomized_search': 'Randomized Search'
  };
  return map[v] || v;
};

const canShowROC = computed(() => {
  return modelSummary.value.problem_type === 'classification' && 
         plotData.value.classes?.length === 2 && 
         plotData.value.y_test_proba;
});

const fetchVisualizationData = async () => {
  loading.value = true;
  error.value = null;
  
  const modelId = route.params.modelId || localStorage.getItem('last_model_id');
  
  if (!modelId) {
    error.value = "No model ID provided for analysis.";
    loading.value = false;
    return;
  }
  
  try {
    const { authenticatedGet } = useAuthenticatedFetch();
    const response = await authenticatedGet(`/api/get-visualization-data/${modelId}`);
    const data = await response.json();
    
    if (data.success) {
      modelSummary.value = data.model_summary;
      plotData.value = data.plot_data;
      insights.value = data.insights;
      
      if (modelSummary.value.problem_type === 'classification') {
        processClassificationData();
      }
      
      loading.value = false;
      
      // Allow DOM to update before initializing charts
      await nextTick();
      initCharts();
    } else {
      error.value = data.message || "Failed to load visualization data.";
      loading.value = false;
    }
  } catch (err) {
    console.error("Fetch error:", err);
    error.value = "Connection error. Please ensure the backend is running.";
    loading.value = false;
  }
};

const processClassificationData = () => {
  classes.value = plotData.value.classes || [];
  const yTrue = plotData.value.y_test_actual || plotData.value.y_full_actual || [];
  const yPred = plotData.value.y_test_pred || plotData.value.y_full_pred || [];
  
  if (classes.value.length > 0 && yTrue.length > 0) {
    // Basic Confusion Matrix calculation
    const n = classes.value.length;
    const matrix = Array(n).fill(0).map(() => Array(n).fill(0));
    const classMap = {};
    classes.value.forEach((c, i) => classMap[c] = i);
    
    for (let i = 0; i < yTrue.length; i++) {
       const trueIdx = classMap[yTrue[i]];
       const predIdx = classMap[yPred[i]];
       if (trueIdx !== undefined && predIdx !== undefined) {
         matrix[trueIdx][predIdx]++;
       }
    }
    confusionMatrix.value = matrix;
  }
};

const getCMAlpha = (val) => {
  if (confusionMatrix.value.length === 0) return 'rgba(102, 126, 234, 0.1)';
  // Get max in row or matrix
  const max = Math.max(...confusionMatrix.value.flat());
  const alpha = 0.1 + (val / max) * 0.7;
  return `rgba(102, 126, 234, ${alpha})`;
};

const initCharts = () => {
  const type = modelSummary.value.problem_type;
  
  if (type === 'regression') {
    initRegressionCharts();
  } else {
    initClassificationCharts();
  }
  
  if (plotData.value.feature_importance) {
    initImportanceChart();
  }
};

const initRegressionCharts = () => {
  const yTrue = plotData.value.y_test_actual || plotData.value.y_full_actual;
  const yPred = plotData.value.y_test_pred || plotData.value.y_full_pred;
  const residuals = plotData.value.residuals_test || plotData.value.residuals_full;

  if (!yTrue || !yPred || !residuals) return;

  // 1. Actual vs Predicted
  const ctxAvP = document.getElementById('actualVsPredictedChart')?.getContext('2d');
  if (ctxAvP) {
    if (actualVsPredChart) actualVsPredChart.destroy();

    const min = Math.min(...yTrue, ...yPred);
    const max = Math.max(...yTrue, ...yPred);

    // Color points by error magnitude
    const errors = yTrue.map((v, i) => Math.abs(v - yPred[i]));
    const maxErr = Math.max(...errors) || 1;
    
    // Indigo (99, 102, 241) to Red (239, 68, 68)
    const pointColors = errors.map(err => {
      const ratio = err / maxErr;
      const r = Math.round(99 + (239 - 99) * ratio);
      const g = Math.round(102 + (68 - 102) * ratio);
      const b = Math.round(241 + (68 - 241) * ratio);
      return `rgba(${r}, ${g}, ${b}, 0.7)`;
    });

    actualVsPredChart = new Chart(ctxAvP, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Predictions',
            data: yTrue.map((v, i) => ({ x: v, y: yPred[i] })),
            backgroundColor: pointColors,
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 6
          },
          {
            label: 'Ideal Fit',
            data: [{ x: min, y: min }, { x: max, y: max }],
            type: 'line',
            borderColor: 'rgba(255, 255, 255, 0.4)',
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => {
                const idx = context.dataIndex;
                const err = Math.abs(yTrue[idx] - yPred[idx]);
                return [
                  `Actual: ${yTrue[idx].toFixed(2)}`,
                  `Predicted: ${yPred[idx].toFixed(2)}`,
                  `Error: ${err.toFixed(4)}`
                ];
              }
            }
          }
        },
        scales: {
          x: { title: { display: true, text: 'Actual Value', color: '#b3b3d1' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#b3b3d1' } },
          y: { title: { display: true, text: 'Predicted Value', color: '#b3b3d1' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#b3b3d1' } }
        }
      }
    });
  }

  // 2. Residuals
  const ctxRes = document.getElementById('residualsChart')?.getContext('2d');
  if (ctxRes) {
    if (residualsChart) residualsChart.destroy();

    // Calculate Residual Std Dev for the "Acceptable Band"
    const meanRes = residuals.reduce((a, b) => a + b, 0) / residuals.length;
    const stdRes = Math.sqrt(residuals.reduce((s, r) => s + Math.pow(r - meanRes, 2), 0) / residuals.length);
    
    const xMin = Math.min(...yPred);
    const xMax = Math.max(...yPred);

    residualsChart = new Chart(ctxRes, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Residuals',
            data: yPred.map((v, i) => ({ x: v, y: residuals[i] })),
            backgroundColor: 'rgba(139, 92, 246, 0.5)',
            borderColor: 'rgba(139, 92, 246, 0.8)',
            pointRadius: 3
          },
          {
            label: 'No Error',
            data: [{ x: xMin, y: 0 }, { x: xMax, y: 0 }],
            type: 'line',
            borderColor: '#10b981',
            borderWidth: 2,
            pointRadius: 0,
            fill: false
          },
          {
            label: '±1 Std Dev Band',
            data: [
              { x: xMin, y: stdRes }, { x: xMax, y: stdRes },
              { x: xMax, y: -stdRes }, { x: xMin, y: -stdRes }
            ],
            type: 'line',
            backgroundColor: 'rgba(16, 185, 129, 0.05)',
            borderColor: 'transparent',
            pointRadius: 0,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { title: { display: true, text: 'Predicted Value', color: '#b3b3d1' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#b3b3d1' } },
          y: { title: { display: true, text: 'Residual (Error)', color: '#b3b3d1' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#b3b3d1' } }
        }
      }
    });
  }

  // 3. Error Distribution (Residual Histogram)
  const ctxErr = document.getElementById('errorDistChart')?.getContext('2d');
  if (ctxErr) {
    if (errorDistChart) errorDistChart.destroy();

    const bins = 20;
    const minErr = Math.min(...residuals);
    const maxErr = Math.max(...residuals);
    const step = (maxErr - minErr) / bins;
    const counts = Array(bins).fill(0);
    const binLabels = Array(bins).fill(0);
    
    residuals.forEach(r => {
      let b = Math.floor((r - minErr) / step);
      if (b === bins) b = bins - 1;
      counts[b]++;
    });
    binLabels.forEach((_, i) => binLabels[i] = (minErr + i * step + step/2).toFixed(2));

    // Calculate Normal Distribution Overlay
    const mean = residuals.reduce((a,b) => a+b,0) / residuals.length;
    const std = Math.sqrt(residuals.reduce((s,r) => s + Math.pow(r-mean,2), 0) / residuals.length) || 1;
    const n = residuals.length;
    
    // Points for the curve
    const curvePoints = [];
    const curveStep = (maxErr - minErr) / 50;
    for (let x = minErr; x <= maxErr; x += curveStep) {
      // Normal PDF scaled by bin width and sample size
      const y = (1 / (std * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * Math.pow((x - mean) / std, 2));
      curvePoints.push({ x: x.toFixed(2), y: y * n * step });
    }

    errorDistChart = new Chart(ctxErr, {
      type: 'bar',
      data: {
        labels: binLabels,
        datasets: [
          {
            label: 'Error Frequency',
            data: counts,
            backgroundColor: 'rgba(16, 185, 129, 0.3)',
            borderColor: '#10b981',
            borderWidth: 1,
            order: 2
          },
          {
            label: 'Ideal Normal Distrib.',
            data: curvePoints.map(p => p.y),
            type: 'line',
            borderColor: 'rgba(255,255,255,0.5)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4,
            fill: false,
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { 
            grid: { display: false }, 
            ticks: { color: '#b3b3d1', maxRotation: 45 },
            title: { display: true, text: 'Residual Value', color: '#b3b3d1' }
          },
          y: { 
            beginAtZero: true, 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' },
            title: { display: true, text: 'Frequency', color: '#b3b3d1' }
          }
        }
      }
    });
  }
};

const initClassificationCharts = () => {
  if (!canShowROC.value) return;
  
  // ROC and PR require y_proba which is a nested list [samples, classes]
  // We assume binary for now (class 1 is positive)
  const yTrue = plotData.value.y_test_actual || plotData.value.y_full_actual;
  const yProba = plotData.value.y_test_proba || plotData.value.y_full_proba;
  const scores = yProba.map(p => p[1]);
  // 1. Prepare data for O(N log N) scan
  // We sort by score descending to calculate thresholds efficiently
  const samples = scores.map((s, i) => ({
    score: s,
    actual: String(yTrue[i]) === String(classes.value[1]) ? 1 : 0
  })).sort((a,b) => b.score - a.score);

  const totalPos = samples.reduce((acc, curr) => acc + curr.actual, 0);
  const totalNeg = samples.length - totalPos;

  const rocPoints = [{ x: 0, y: 0 }];
  const prPoints = [];

  if (totalPos > 0 && totalNeg > 0) {
    let tp = 0;
    let fp = 0;

    for (let i = 0; i < samples.length; i++) {
      if (samples[i].actual) tp++;
      else fp++;

      // Only add a point if current score is different from next or it's the last sample
      if (i === samples.length - 1 || samples[i+1].score !== samples[i].score) {
        rocPoints.push({ x: fp / totalNeg, y: tp / totalPos });
        prPoints.push({ x: tp / totalPos, y: tp / (tp + fp) });
      }
    }
  } else {
    // Edge case: entire dataset has only one class
    rocPoints.push({ x: 1, y: 1 });
    prPoints.push({ x: 0, y: 0 }, { x: 1, y: 0 });
  }
  
  // Ensure ROC reaches (1,1)
  if (rocPoints[rocPoints.length - 1].x < 1) {
    rocPoints.push({ x: 1, y: 1 });
  }
  
  // PR Curve typically starts at (Recall=0, Precision=1) or (0, Precision_at_highest_threshold)
  if (prPoints.length > 0 && prPoints[0].x > 0) {
    prPoints.unshift({ x: 0, y: prPoints[0].y });
  }

  // Initialize ROC Chart
  const ctxROC = document.getElementById('rocChart')?.getContext('2d');
  if (ctxROC) {
    rocChart = new Chart(ctxROC, {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'ROC Curve',
            data: rocPoints,
            borderColor: '#6366f1',
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            tension: 0
          },
          {
            label: 'Random',
            data: [{x:0, y:0}, {x:1, y:1}],
            borderColor: 'rgba(255,255,255,0.2)',
            borderDash: [5,5],
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
          legend: { labels: { color: '#fff' } },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { 
            type: 'linear',
            position: 'bottom',
            min: 0, max: 1,
            title: { display: true, text: 'False Positive Rate', color: '#b3b3d1' }, 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' } 
          },
          y: { 
            min: 0, max: 1,
            title: { display: true, text: 'True Positive Rate', color: '#b3b3d1' }, 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' } 
          }
        }
      }
    });
  }

  // Initialize PR Chart
  const ctxPR = document.getElementById('prChart')?.getContext('2d');
  if (ctxPR) {
    prChart = new Chart(ctxPR, {
      type: 'line',
      data: {
        datasets: [{
          label: 'PR Curve',
          data: prPoints,
          borderColor: '#10b981',
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
          legend: { labels: { color: '#fff' } },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { 
            type: 'linear',
            position: 'bottom',
            min: 0, max: 1,
            title: { display: true, text: 'Recall', color: '#b3b3d1' }, 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' } 
          },
          y: { 
            min: 0, max: 1,
            title: { display: true, text: 'Precision', color: '#b3b3d1' }, 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' } 
          }
        }
      }
    });
  }
};

const initImportanceChart = () => {
  const importances = plotData.value.feature_importance;
  if (!importances) return;

  const rawNames = plotData.value.feature_names || Array.from({length: importances.length}, (_, i) => `Feature ${i+1}`);
  const registry = plotData.value.feature_metadata || {};

  // Aggregate storage: { originalName: { totalImpact, subFeatures: [], meta: {} } }
  const aggregated = {};

  importances.forEach((val, idx) => {
    const fName = rawNames[idx];
    const meta = registry[fName] || { original_column: fName, type: 'unknown' };
    const originalName = meta.original_column;

    if (!aggregated[originalName]) {
      aggregated[originalName] = {
        value: 0,
        subFeatures: [],
        meta: meta
      };
    }

    aggregated[originalName].value += val;
    aggregated[originalName].subFeatures.push({ name: fName, impact: val });
  });

  // Convert to array and sort
  const dataList = Object.keys(aggregated).map(name => ({
    name: name,
    value: aggregated[name].value,
    subFeatures: aggregated[name].subFeatures,
    meta: aggregated[name].meta
  })).sort((a,b) => b.value - a.value).slice(0, 15);

  const ctxImp = document.getElementById('importanceChart')?.getContext('2d');
  if (ctxImp) {
    if (importanceChart) importanceChart.destroy();
    
    importanceChart = new Chart(ctxImp, {
      type: 'bar',
      data: {
        labels: dataList.map(d => d.name),
        datasets: [{
          label: 'Relative Significance',
          data: dataList.map(d => d.value),
          backgroundColor: dataList.map((_, i) => 
            `rgba(102, 126, 234, ${1 - (i * 0.05)})`
          ),
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => {
                const item = dataList[context.dataIndex];
                const parts = [`Significance Score: ${item.value.toFixed(4)}`];
                
                if (item.meta.type === 'categorical') {
                  const method = item.meta.transformation || 'standard';
                  parts.push(`Type: Categorical (${method})`);
                  if (item.subFeatures.length > 1) {
                    parts.push(`Includes ${item.subFeatures.length} encoded categories`);
                  }
                } else if (item.meta.type === 'target_encoded') {
                   parts.push(`Type: Target Encoded (smoothing=${item.meta.smoothing})`);
                } else if (item.meta.type === 'text') {
                   parts.push(`Type: Text (TF-IDF)`);
                }
                
                return parts;
              }
            }
          }
        },
        scales: {
          x: { 
            grid: { color: 'rgba(255,255,255,0.05)' }, 
            ticks: { color: '#b3b3d1' },
            title: { display: true, text: 'Total Relative Impact', color: '#b3b3d1' }
          },
          y: { 
            grid: { display: false }, 
            ticks: { color: '#fff', font: { weight: 'bold' } } 
          }
        }
      }
    });
  }
};

const cmMetrics = computed(() => {
  if (!confusionMatrix.value || confusionMatrix.value.length === 0 || classes.value.length === 0) return null;
  const cm = confusionMatrix.value;
  const cls = classes.value;
  
  if (cls.length === 2 && cm.length === 2) {
    const tn = cm[0][0];
    const fp = cm[0][1];
    const fn = cm[1][0];
    const tp = cm[1][1];
    
    // Imbalance Ratio: max(class_count) / min(class_count)
    const count0 = tn + fp;
    const count1 = fn + tp;
    const imbalanceRatio = count0 > 0 && count1 > 0 ? Math.max(count0, count1) / Math.min(count0, count1) : 1;
    
    return {
      binary: true,
      tp, fp, fn, tn,
      recall: (tp + fn) > 0 ? tp / (tp + fn) : 0,
      precision: (tp + fp) > 0 ? tp / (tp + fp) : 0,
      fpr: (fp + tn) > 0 ? fp / (fp + tn) : 0,
      fnr: (fn + tp) > 0 ? fn / (fn + tp) : 0,
      imbalanceRatio,
      posLabel: cls[1]
    };
  } else if (cls.length > 2) {
    // Multiclass imbalance and recall
    const rowSums = cls.map((_, i) => cm[i]?.reduce((a, b) => a + b, 0) || 0);
    const validRowSums = rowSums.filter(s => s > 0);
    const imbalanceRatio = validRowSums.length > 0 ? Math.max(...rowSums) / Math.min(...validRowSums) : 1;

    const perClassRecall = cls.map((label, i) => {
      const rowSum = rowSums[i];
      return { label, recall: rowSum > 0 ? cm[i][i] / rowSum : 0 };
    });
    
    const lowestRecallClass = perClassRecall.reduce((prev, curr) => (prev.recall < curr.recall) ? prev : curr);

    let maxConf = -1;
    let mostConfused = null;
    for(let i=0; i < cm.length; i++) {
      for(let j=0; j < cm[i].length; j++) {
        if (i !== j && cm[i][j] > maxConf) {
          maxConf = cm[i][j];
          mostConfused = { trueLabel: cls[i], predLabel: cls[j], count: maxConf };
        }
      }
    }
    return { binary: false, perClassRecall, mostConfused, lowestRecallClass, imbalanceRatio };
  }
  return null;
});

const cmInsights = computed(() => {
  const m = cmMetrics.value;
  if (!m) return null;
  
  let interpretation = "";
  let badges = [];
  let whyMatters = "";
  let suggestions = [];
  
  if (m.binary) {
    // 1. Detection Logic for Interpretation (Prioritize PR tradeoff and high error rates)
    if (m.recall > 0.8 && m.precision < 0.6) {
      interpretation = "The model correctly identifies most positive cases, but also produces many false alarms.";
    } else if (m.fpr > 0.25) {
      interpretation = "The model results in a high number of false alarms, frequently misclassifying negative cases as positive.";
    } else if (m.fnr > 0.25) {
      interpretation = "The model fails to detect a significant portion of positive cases, resulting in frequent misses.";
    } else if (m.imbalanceRatio > 3.0) {
      interpretation = "Severe class imbalance is causing the model to lean heavily towards the majority class, making standard metrics less reliable.";
    } else {
      interpretation = "The model demonstrates a stable classification pattern with balanced error rates across both classes.";
    }

    // 2. Badges (Max 2)
    if (m.imbalanceRatio > 3.0) badges.push({ text: "Severe Class Imbalance", type: "danger" });
    else if (m.imbalanceRatio > 1.5) badges.push({ text: "Accuracy May Be Misleading", type: "warning" });

    if (badges.length < 2) {
      if (m.recall > 0.8 && m.precision < 0.6) badges.push({ text: "Precision–Recall Tradeoff", type: "warning" });
      else if (m.fpr > 0.25) badges.push({ text: "High False Positive Rate", type: "warning" });
      else if (m.fnr > 0.25) badges.push({ text: "High False Negative Rate", type: "danger" });
    }
    
    if (badges.length < 2 && m.recall > 0.9 && m.precision > 0.9) {
       badges.push({ text: "Strong Predictive Power", type: "success" });
    }

    // 3. Why it Matters
    if (m.imbalanceRatio > 1.5) {
      whyMatters = "In imbalanced scenarios, accuracy can be artificially inflated by the majority class. This masks poor performance on the rarer, often more critical, cases.";
    } else if (m.recall > 0.8 && m.precision < 0.6) {
      whyMatters = "This behavior ensures high coverage of positive events but at the cost of operational noise. It is ideal for screening where missing a case is worse than a false alarm.";
    } else if (m.fnr > 0.25) {
      whyMatters = "High false negative rates are risky in scenarios where missing a positive outcome has severe consequences, like in fraud detection or medical diagnosis.";
    } else {
      whyMatters = "Balanced error rates indicate the model has successfully identified distinguishing features that apply equally to both outcomes.";
    }

    // 4. Suggestions (Max 2)
    if (m.imbalanceRatio > 1.5) {
      suggestions.push("Use class weighting or SMOTE sampling to help the model learn the underrepresented class.");
    } else if (m.recall > 0.8 && m.precision < 0.6) {
      suggestions.push("Adjust the classification threshold to find a better balance between detection and noise.");
    }
    
    if (suggestions.length < 2) {
       if (m.fpr > 0.25 || m.fnr > 0.25) {
         suggestions.push("Investigate features that might be causing confusion between these specific outcomes.");
       } else {
         suggestions.push("The model is performing well; consider verifying its robustness on a completely unseen longitudinal dataset.");
       }
    }
  } else {
    // Multiclass Logic
    interpretation = `The model shows the most difficulty with ${m.lowestRecallClass.label} Category (recall: ${(m.lowestRecallClass.recall * 100).toFixed(0)}%) and frequently confuses ${m.mostConfused.trueLabel} with ${m.mostConfused.predLabel}.`;
    
    if (m.imbalanceRatio > 3.0) badges.push({ text: "Severe Imbalance Detected", type: "danger" });
    if (m.lowestRecallClass.recall < 0.5 && badges.length < 2) badges.push({ text: `Weak Recall: ${m.lowestRecallClass.label}`, type: "warning" });
    
    whyMatters = "Multiclass imbalances or feature overlaps cause the model to systematically collapse certain categories into more frequent ones.";
    
    if (m.imbalanceRatio > 1.5) {
      suggestions.push("Apply class weights to penalize errors on majority classes more heavily during training.");
    }
    if (suggestions.length < 2) {
      suggestions.push(`Focus on collecting more distinct examples for ${m.lowestRecallClass.label} to improve its separation from ${m.mostConfused.predLabel}.`);
    }
  }
  
  return { 
    interpretation, 
    badges: badges.slice(0, 2), 
    whyMatters, 
    suggestions: suggestions.slice(0, 2) 
  };
});

const goBack = () => {
  const query = {};
  if (modelSummary.value.dataset_id) {
    query.datasetId = modelSummary.value.dataset_id;
  }
  router.push({ path: '/model-training', query });
};

// ── NAVIGATION GUARD: clear session on pipeline exit ───────────────────────
const PIPELINE_ROUTES = [
  'data-preview', 'target-selection', 'advanced-preprocessing',
  'algorithm-select', 'model-training', 'model-visualization'
];
onBeforeRouteLeave((to, _from, next) => {
  if (!PIPELINE_ROUTES.includes(to.name)) {
    // All pipeline work is done at visualization — clear session to allow fresh start
    experimentStore.clearAll();
  }
  next();
});
// ─────────────────────────────────────────────────────────────────────────────

onMounted(() => {
  fetchVisualizationData();
});

onUnmounted(() => {
  [actualVsPredChart, residualsChart, errorDistChart, rocChart, prChart, importanceChart].forEach(chart => {
    if (chart) chart.destroy();
  });
});
</script>

<style scoped>
.model-visualization {
  background-color: #0f0f23;
  color: #ffffff;
  padding-bottom: 5rem;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.vis-header {
  padding: 1rem 2rem;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
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
  border: 1px solid rgba(102, 126, 234, 0.4);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #b3b3d1;
}

.breadcrumb .current {
  color: #667eea;
  font-weight: 600;
}

.hero-section {
  padding: 3rem 2rem;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  text-align: center;
  margin-bottom: 4rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.hero-section p {
  font-size: 1.25rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
}


.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2.5rem;
}

.summary-dashboard {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1.5fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.summary-card {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.algo-badge {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.summary-item label {
  display: block;
  font-size: 0.75rem;
  color: #b3b3d1;
  margin-bottom: 0.25rem;
}

.summary-item span {
  font-weight: 600;
  color: #fff;
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  height: 100%;
  align-items: center;
}

.mini-metric {
  text-align: center;
}

.m-val {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #667eea;
}

.mini-metric label {
  font-size: 0.75rem;
  color: #b3b3d1;
}

.ai-badge {
  font-size: 0.65rem;
  color: #10b981;
  border: 1px solid #10b981;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.insight-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  font-size: 0.875rem;
}

.insight-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.insight-item.good .insight-status { background: #10b981; }
.insight-item.moderate .insight-status { background: #f59e0b; }
.insight-item.warning .insight-status { background: #ef4444; }

/* Visuals Grid */
.visuals-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.vis-section {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.vis-section.full-width {
  grid-column: span 2;
}

.section-info {
  margin-bottom: 2rem;
  max-width: 800px;
}

.header-with-metric {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.metric-chip {
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  border: 1px solid rgba(99, 102, 241, 0.3);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.1);
}

.metric-chip strong {
  color: #fff;
  margin-left: 0.3rem;
}

.instructional-box {
  background: rgba(255, 255, 255, 0.03);
  border-left: 3px solid #667eea;
  padding: 1.25rem;
  border-radius: 4px 8px 8px 4px;
  margin-top: 1rem;
}

.howto {
  font-size: 0.95rem;
  color: #fff;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.reg-insights, .pattern-detect ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.reg-insights li, .pattern-detect li {
  font-size: 0.85rem;
  color: #b3b3d1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pattern-detect strong {
  display: block;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #667eea;
  margin-bottom: 0.75rem;
}

.chart-wrapper.large {
  height: 500px;
}

.section-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.description {
  color: #b3b3d1;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.educational-note {
  background: rgba(99, 102, 241, 0.1);
  border-left: 3px solid #6366f1;
  padding: 1rem;
  color: #a5b4fc;
  font-size: 0.875rem;
  line-height: 1.5;
}

.chart-wrapper {
  height: 400px;
  position: relative;
}

/* Confusion Matrix Custom UI */
.matrix-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.cm-grid {
  display: grid;
  gap: 4px;
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 12px;
}

.cm-corner {
  font-size: 0.75rem;
  color: #b3b3d1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.cm-header, .cm-row-label {
  font-weight: 700;
  font-size: 0.875rem;
  padding: 1rem;
  text-align: center;
  color: #b3b3d1;
}

.cm-cell {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: white;
  border-radius: 4px;
}

/* Loading/Error States */
.loading-state, .error-state {
  height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(102, 126, 234, 0.3);
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.error-icon { font-size: 3rem; margin-bottom: 1.5rem; }
.retry-btn {
  margin-top: 2rem;
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .summary-dashboard { grid-template-columns: 1fr; }
  .visuals-grid { grid-template-columns: 1fr; }
  .vis-section.full-width { grid-column: span 1; }
}
/* Confusion Matrix Split Layout */
.cm-insight-section {
  padding: 0 !important;
  overflow: hidden;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.cm-layout-container {
  display: flex;
  min-height: 500px;
}

.cm-visual-side {
  flex: 1.3;
  padding: 2rem;
  border-right: 1px solid rgba(102, 126, 234, 0.1);
  background: rgba(26, 26, 46, 0.2);
}

.cm-analysis-side {
  flex: 1;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.02);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.title-wrap h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 0.875rem;
  color: #b3b3d1;
}

.analysis-section {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.analysis-section:last-child {
  border-bottom: none;
}

.analysis-section.highlight {
  background: rgba(102, 126, 234, 0.05);
  margin: 0 -2rem;
  padding: 1.5rem 2rem;
}

.mini-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #667eea;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pos-context {
  text-transform: none;
  font-weight: 400;
  color: #b3b3d1;
  letter-spacing: 0;
}

.raw-counts-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.count-item {
  font-size: 0.8rem;
  color: #b3b3d1;
}

.derived-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.derived-card {
  background: rgba(26, 26, 46, 0.6);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.derived-card label {
  display: block;
  font-size: 0.7rem;
  color: #b3b3d1;
  margin-bottom: 0.2rem;
}

.d-val {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
}

.class-recall-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recall-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.r-label {
  width: 80px;
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.r-progress-bg {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.r-progress-fill {
  height: 100%;
  background: #667eea;
  border-radius: 3px;
}

.r-value {
  font-family: monospace;
  font-weight: 700;
  color: #10b981;
}

.plain-talk {
  font-size: 1rem;
  line-height: 1.5;
  color: #fff;
  margin-bottom: 1rem;
}

.insight-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.i-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.i-badge.success { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
.i-badge.warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
.i-badge.danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }

.summary-text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #b3b3d1;
}

.suggestion-list {
  padding-left: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.suggestion-list li {
  font-size: 0.875rem;
  color: #a5b4fc;
}

@media (max-width: 1200px) {
  .cm-layout-container {
    flex-direction: column;
  }
  .cm-visual-side {
    border-right: none;
    border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  }
}
</style>
