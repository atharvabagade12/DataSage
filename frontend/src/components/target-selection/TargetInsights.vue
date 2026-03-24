<template>
  <aside class="insights-panel">
    <h3>Target Analysis</h3>

    <div v-if="!selectedColumn" class="no-selection">
      <div class="empty-icon">🤖</div>
      <p>Select a column to see AI analysis & statistics</p>
    </div>

    <div v-else class="target-insights">
      
      <!-- 1. Suitability Header -->
      <div class="hero-suitability" :class="getScoreClass(selectedColumn.suitabilityScore)">
        <div class="score-ring">
           <svg viewBox="0 0 36 36" class="circular-chart" :class="getScoreClass(selectedColumn.suitabilityScore)">
            <path class="circle-bg"
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path class="circle"
              :stroke-dasharray="`${selectedColumn.suitabilityScore}, 100`"
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <text x="18" y="20.35" class="percentage">{{ selectedColumn.suitabilityScore }}</text>
          </svg>
        </div>
        <div class="suitability-text">
          <h4 class="suitability-title">ML Suitability</h4>
          <p class="suitability-desc">{{ getSuitabilityDescription(selectedColumn.suitabilityScore) }}</p>
        </div>
      </div>

       <!-- Suitability Factors -->
       <div class="factors-container">
          <div v-for="(factor, idx) in getSuitabilityFactors()" :key="idx" class="factor-badge" :class="factor.status">
             <span class="icon">{{ factor.icon }}</span>
             <span class="text">{{ factor.text }}</span>
          </div>
       </div>

      <!-- 2. Data Quality (Completeness & Health) -->
      <div class="insight-section">
        <h4 class="section-title"><span class="icon">🛡️</span> Data Quality</h4>
        <div class="quality-card">
           <div class="quality-metric">
              <div class="metric-header">
                 <span>Completeness</span>
                 <span class="metric-value">{{ getCompletenessPercentage() }}%</span>
              </div>
              <div class="progress-bar-bg">
                 <div class="progress-bar-fill" :style="{ width: `${getCompletenessPercentage()}%` }" :class="getCompletenessClass()"></div>
              </div>
              <span class="metric-sub">{{ selectedColumn.missingPercent.toFixed(1) }}% missing data</span>
           </div>
           
           <div class="quality-split">
               <div class="mini-stat">
                  <span class="label">Outliers</span>
                  <span class="value">{{ getOutlierCount() }}</span>
               </div>
               <div class="mini-stat">
                  <span class="label">Original Type</span>
                  <span class="value capitalize">{{ selectedColumn.originalType }}</span>
               </div>
           </div>
        </div>
      </div>

      <!-- 3. Distribution & Statistics -->
      <div class="insight-section">
        <h4 class="section-title"><span class="icon">📊</span> Distribution Summary</h4>
        
        <!-- Numerical Stats -->
        <div v-if="isNumeric" class="modern-grid-stats">
          <div class="stat-box box-primary">
            <span class="lbl">Mean</span>
            <span class="val">{{ formatNumber(getMetric('mean')) }}</span>
          </div>
          <div class="stat-box box-primary">
            <span class="lbl">Median</span>
            <span class="val">{{ formatNumber(getMetric('median')) }}</span>
          </div>
          <div class="stat-box box-secondary full-width">
            <span class="lbl">Range (Min - Max)</span>
            <span class="val">{{ formatNumber(getMetric('min')) }} <span style="font-size: 0.8rem; color: #64748b;">to</span> {{ formatNumber(getMetric('max')) }}</span>
          </div>
          <div class="stat-box">
            <span class="lbl">Std Dev</span>
            <span class="val">{{ formatNumber(getMetric('std')) }}</span>
          </div>
          <div class="stat-box">
            <span class="lbl">Skewness</span>
            <span class="val" :title="getSkewnessText()">{{ formatNumber(getMetric('skewness')) }}</span>
          </div>
        </div>

        <!-- Categorical Stats -->
        <div v-else class="modern-grid-stats">
          <div class="stat-box box-primary full-width">
            <span class="lbl">Unique Classes</span>
            <span class="val">{{ selectedColumn.uniqueValues }} <span class="sub-val">cardinality</span></span>
          </div>
          
          <template v-if="selectedColumn.metrics">
             <div class="stat-box full-width warning-border" v-if="selectedColumn.metrics.imbalance_ratio">
                <div class="flex-between">
                    <span class="lbl">Imbalance Ratio</span>
                    <span class="val" :class="getImbalanceClass(selectedColumn.metrics.imbalance_ratio)">
                        {{ formatImbalance(selectedColumn.metrics.imbalance_ratio) }}
                    </span>
                </div>
                <p class="stat-desc">{{ getImbalanceTooltip(selectedColumn.metrics.imbalance_ratio) }}</p>
             </div>
             
             <div class="stat-box" v-if="selectedColumn.metrics.majority_class">
               <span class="lbl">Majority Class</span>
               <span class="val truncate" :title="selectedColumn.metrics.majority_class.name">{{ getTruncatedName(selectedColumn.metrics.majority_class.name) }}</span>
               <span class="sub-val margin-top">{{ selectedColumn.metrics.majority_class.percent }}%</span>
             </div>
             <div class="stat-box" v-if="selectedColumn.metrics.minority_class">
               <span class="lbl">Minority Class</span>
               <span class="val truncate" :title="selectedColumn.metrics.minority_class.name">{{ getTruncatedName(selectedColumn.metrics.minority_class.name) }}</span>
               <span class="sub-val margin-top">{{ selectedColumn.metrics.minority_class.percent }}%</span>
             </div>
          </template>
        </div>
      </div>

      <!-- 4. Sample Values -->
      <div class="insight-section">
        <h4 class="section-title"><span class="icon">🔍</span> Sample Values</h4>
        <div class="sample-pills">
          <span v-for="(val, idx) in getSampleValues()" :key="idx" class="sample-pill">
            {{ formatSampleValue(val) }}
          </span>
        </div>
      </div>

      <!-- 5. Recommendations List -->
      <div class="insight-section">
        <h4 class="section-title"><span class="icon">🎯</span> Suggested Tasks</h4>
        <div class="recommendations">
          <div v-for="rec in getTargetRecommendations()" :key="rec.title" class="rec-card">
            <div class="rec-icon-bg">{{ rec.icon }}</div>
            <div class="rec-info">
              <h5>{{ rec.title }}</h5>
              <p>{{ rec.description }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  selectedColumn: {
    type: Object,
    default: null
  },
  dataset: {
    type: Array,
    default: () => []
  }
});

const isNumeric = computed(() => {
    return props.selectedColumn && (props.selectedColumn.originalType === 'number' || props.selectedColumn.originalType === 'numerical');
});

const getScoreClass = (score) => {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "fair";
  return "poor";
};

const getSuitabilityDescription = (score) => {
  if (score >= 80) return "Excellent target variable";
  if (score >= 60) return "Good target variable";
  if (score >= 40) return "Fair target variable";
  return "Poor target variable";
};

const getSuitabilityFactors = () => {
  if (!props.selectedColumn) return [];

  const factors = [];
  if (props.selectedColumn.missingPercent < 5) {
    factors.push({ icon: "✅", text: "Low missing data", status: "good" });
  } else {
    factors.push({ icon: "⚠️", text: `${props.selectedColumn.missingPercent.toFixed(1)}% missing data`, status: "warning" });
  }

  const uniqueRatio = props.selectedColumn.uniqueValues / props.dataset.length;
  if (!isNumeric.value && uniqueRatio < 0.5) {
    factors.push({ icon: "✅", text: "Good cardinality for classification", status: "good" });
  } else if (isNumeric.value) {
    factors.push({ icon: "✅", text: "Numeric data suitable for ML", status: "good" });
  }

  if (props.selectedColumn.hasEncoding) {
    factors.push({ icon: "🔄", text: `${props.selectedColumn.encoding} encoding detected`, status: "info" });
  }

  return factors;
};

// Data Quality Methods
const getCompletenessPercentage = () => {
    return props.selectedColumn ? Math.round(100 - props.selectedColumn.missingPercent) : 0;
};
const getCompletenessClass = () => {
    const p = getCompletenessPercentage();
    if (p >= 95) return 'bg-success';
    if (p >= 80) return 'bg-warning';
    return 'bg-error';
};
const getOutlierCount = () => {
    if (!props.selectedColumn || !isNumeric.value) return "N/A";
    return props.selectedColumn.outliers || 0;
};

// Stats Methods
const getMetric = (name) => {
    if (!props.selectedColumn) return null;
    if (props.selectedColumn.statistics && props.selectedColumn.statistics[name] !== undefined) {
        return props.selectedColumn.statistics[name];
    }
    if (props.selectedColumn.metrics && props.selectedColumn.metrics[name] !== undefined) {
        return props.selectedColumn.metrics[name];
    }
    return null;
};
const formatNumber = (val) => {
    if (val === null || val === undefined) return 'N/A';
    if (typeof val === 'number') return Number.isInteger(val) ? val.toString() : val.toFixed(2);
    return val;
};
const getSkewnessText = () => {
    const skew = getMetric('skewness');
    const mean = getMetric('mean');
    const median = getMetric('median');
    if (skew === null) return "N/A";
    if (Math.abs(mean - median) < 0.1 || Math.abs(skew) < 0.5) return "Approximately Normal";
    return mean > median ? "Right Skewed" : "Left Skewed";
};
const getTruncatedName = (name) => {
    if (!name) return "";
    return String(name).length > 20 ? String(name).substring(0, 17) + "..." : String(name);
};
const formatImbalance = (ratio) => {
  if (!ratio || ratio === Infinity) return "N/A";
  return `${Number(ratio).toFixed(1)}:1`; // Slightly more precise than 0 decimals
};
const getImbalanceTooltip = (ratio) => {
  if (!ratio) return "";
  const r = Number(ratio);
  if (r < 1.5) return "Balanced distribution. Excellent for classification.";
  if (r < 3.0) return "Mild imbalance. Consider stratification.";
  return "Severe imbalance. Requires special handling Techniques (SMOTE/Class Weights).";
};
const getImbalanceClass = (ratio) => {
  if (!ratio) return "";
  if (ratio <= 1.5) return "text-success"; 
  if (ratio <= 3.0) return "text-warning";
  return "text-error";
};


// Formatting Data Fields
const getSampleValues = () => {
  if (!props.selectedColumn || !props.selectedColumn.sampleValues) return [];
  return props.selectedColumn.sampleValues.slice(0, 6); // Reduce to fit pills better
};
const formatSampleValue = (value) => {
  if (value === null || value === undefined) return "N/A";
  if (typeof value === "number") return value.toLocaleString();
  if (typeof value === "string" && value.length > 25) return value.substring(0, 22) + "...";
  return String(value);
};


// Recommendations
const getTargetRecommendations = () => {
  if (!props.selectedColumn) return [];

  try {
    const column = props.selectedColumn;
    const recommendations = [];

    // Binary Classification
    if (column.uniqueValues === 2) {
      recommendations.push({
        icon: "🎯",
        title: "Binary Classification",
        description: "Perfect for yes/no or true/false predictions",
      });
    }

    // Multi-class Classification
    if (column.uniqueValues >= 3 && column.uniqueValues <= 20) {
      recommendations.push({
        icon: "🎨",
        title: "Multi-class Classification",
        description: `Predicting ${column.uniqueValues} distinct categories`,
      });
    }

    // Regression
    if (isNumeric.value && column.uniqueValues > 20) {
      recommendations.push({
        icon: "📈",
        title: "Regression Analysis",
        description: "Predict continuous numerical values",
      });
    }

    // Time Series
    if (column.originalType === "date" || /date|time|timestamp/i.test(column.name)) {
      recommendations.push({
        icon: "⏰",
        title: "Time Series Forecasting",
        description: "Predict future values based on temporal patterns",
      });
    }

    // General fallback
    if (recommendations.length === 0) {
      recommendations.push({
        icon: "🤖",
        title: "Custom ML Task",
        description: "Flexible for various advanced forecasting models",
      });
    }

    return recommendations.slice(0, 2); // Show only top 2
  } catch (error) {
    console.error("Error generating recommendations:", error);
    return [];
  }
};
</script>

<style scoped>
.insights-panel {
  background: rgba(26, 26, 46, 0.6);  /* (15, 23, 42, 0.6)*/
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 180px);
  overflow-y: auto;
  color: #f8fafc;
}

.insights-panel h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding-bottom: 0.75rem;
}

.no-selection {
  text-align: center;
  padding: 3rem 1rem;
  color: #94a3b8;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.target-insights {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Base Sections */
.insight-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.section-title {
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title .icon {
    font-size: 1.1rem;
}

/* 1. Hero Suitability */
.hero-suitability {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.hero-suitability.excellent { border-left: 4px solid #10b981; }
.hero-suitability.good { border-left: 4px solid #3b82f6; }
.hero-suitability.fair { border-left: 4px solid #f59e0b; }
.hero-suitability.poor { border-left: 4px solid #ef4444; }

.score-ring { width: 70px; height: 70px; }
.circular-chart { display: block; margin: 0 auto; max-width: 100%; max-height: 250px; }
.circle-bg { fill: none; stroke: rgba(255, 255, 255, 0.1); stroke-width: 3.8; }
.circle { fill: none; stroke-width: 2.8; stroke-linecap: round; animation: progress 1s ease-out forwards; }
.percentage { fill: #fff; font-family: sans-serif; font-size: 0.5em; text-anchor: middle; font-weight: bold; }

@keyframes progress { 0% { stroke-dasharray: 0 100; } }

.circular-chart.excellent .circle { stroke: #10b981; }
.circular-chart.good .circle { stroke: #3b82f6; }
.circular-chart.fair .circle { stroke: #f59e0b; }
.circular-chart.poor .circle { stroke: #ef4444; }

.suitability-title { margin: 0 0 0.25rem 0; font-size: 1.1rem; color: #fff; }
.suitability-desc { margin: 0; font-size: 0.85rem; color: #94a3b8; }

.factors-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.factor-badge {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.4rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    color: #cbd5e1;
    border: 1px solid transparent;
}
.factor-badge.good { border-color: rgba(16, 185, 129, 0.3); color: #34d399; }
.factor-badge.warning { border-color: rgba(245, 158, 11, 0.3); color: #fbbf24; }
.factor-badge.info { border-color: rgba(99, 102, 241, 0.3); color: #818cf8; }

/* 2. Quality Card */
.quality-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.metric-header { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600;}
.progress-bar-bg { width: 100%; height: 6px; background: rgba(255, 255, 255, 0.1); border-radius: 3px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.metric-sub { font-size: 0.75rem; color: #64748b; margin-top: 0.4rem; display: block; }

.bg-success { background: #10b981; }
.bg-warning { background: #f59e0b; }
.bg-error { background: #ef4444; }

.quality-split { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1rem; }
.mini-stat { display: flex; flex-direction: column; }
.mini-stat .label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.mini-stat .value { font-size: 1rem; font-weight: 600; color: #f8fafc; margin-top: 0.25rem; }

/* 3. Grid Stats */
.modern-grid-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
}

.stat-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.full-width { grid-column: span 2; }
.box-primary { background: rgba(99, 102, 241, 0.08); border-color: rgba(99, 102, 241, 0.2); }
.box-secondary { background: rgba(16, 185, 129, 0.05); border-color: rgba(16, 185, 129, 0.15); }
.warning-border { border-left: 3px solid #f59e0b; }

.stat-box .lbl { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;}
.stat-box .val { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; }
.stat-box .sub-val { font-size: 0.7rem; color: #64748b; font-weight: 400; }
.stat-box .desc { font-size: 0.75rem; color: #10b981; font-weight: 600; margin-top: 0.2rem;}
.stat-desc { font-size: 0.75rem; color: #94a3b8; margin: 0.25rem 0 0 0; line-height: 1.3;}
.margin-top { margin-top: 0.25rem; }

/* Flex rules */
.flex-between { display: flex; justify-content: space-between; align-items: center; }

/* Text rules */
.text-success { color: #10b981 !important; }
.text-warning { color: #f59e0b !important; }
.text-error { color: #ef4444 !important; }
.capitalize { text-transform: capitalize; }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; display: block; }

/* 4. Sample Pills */
.sample-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.sample-pill {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    color: #e2e8f0;
}

/* 5. Recommended Tasks */
.recommendations {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.rec-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 0.85rem;
    border-radius: 10px;
    transition: transform 0.2s, background 0.2s;
}

.rec-card:hover {
    background: rgba(255, 255, 255, 0.04);
    transform: translateX(4px);
}

.rec-icon-bg {
    background: rgba(99, 102, 241, 0.15);
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
}

.rec-info h5 {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    color: #f1f5f9;
}

.rec-info p {
    margin: 0;
    font-size: 0.75rem;
    color: #94a3b8;
    line-height: 1.3;
}

/* Scrollbar styling */
.insights-panel::-webkit-scrollbar { width: 6px; }
.insights-panel::-webkit-scrollbar-track { background: transparent; }
.insights-panel::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.2); border-radius: 3px; }
.insights-panel::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.4); }

</style>
