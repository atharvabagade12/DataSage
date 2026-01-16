<template>
  <aside class="insights-panel">
    <h3>Target Analysis</h3>

    <div v-if="!selectedColumn" class="no-selection">
      <p>Select a column to see AI analysis</p>
    </div>

    <div v-else class="target-insights">
      <!-- Suitability Score -->
      <div class="insight-section">
        <h4>ML Suitability Score</h4>
        <div class="suitability-analysis">
          <div class="suitability-score-large">
            <div
              class="score-circle"
              :class="getScoreClass(selectedColumn.suitabilityScore)"
            >
              {{ selectedColumn.suitabilityScore }}
            </div>
            <span class="score-description">
              {{ getSuitabilityDescription(selectedColumn.suitabilityScore) }}
            </span>
          </div>

          <div class="suitability-factors">
            <div
              v-for="(factor, idx) in getSuitabilityFactors()"
              :key="idx"
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

      <!-- Statistics -->
      <div
        v-if="selectedColumn.statistics"
        class="insight-section"
      >
        <h4>Statistical Summary</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Mean</span>
            <span class="stat-value">{{
              selectedColumn.statistics.mean.toFixed(2)
            }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Median</span>
            <span class="stat-value">{{
              selectedColumn.statistics.median.toFixed(2)
            }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Std Dev</span>
            <span class="stat-value">{{
              selectedColumn.statistics.std.toFixed(2)
            }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Min/Max</span>
            <span class="stat-value"
              >{{ selectedColumn.statistics.min }} /
              {{ selectedColumn.statistics.max }}</span
            >
          </div>
        </div>
      </div>

      <!-- Sample Values -->
      <div class="insight-section">
        <h4>Sample Values</h4>
        <div class="sample-values">
          <div
            v-for="(val, idx) in getSampleValues()"
            :key="idx"
            class="sample-item"
          >
            {{ formatSampleValue(val) }}
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="insight-section">
        <h4>Recommended ML Tasks</h4>
        <div class="recommendations">
          <div
            v-for="rec in getTargetRecommendations()"
            :key="rec.title"
            class="recommendation-item"
          >
            <span class="rec-icon">{{ rec.icon }}</span>
            <div class="rec-content">
              <div class="rec-title">{{ rec.title }}</div>
              <div class="rec-description">{{ rec.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
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

  // Missing data check
  if (props.selectedColumn.missingPercent < 5) {
    factors.push({ icon: "✅", text: "Low missing data", status: "good" });
  } else {
    factors.push({
      icon: "⚠️",
      text: `${props.selectedColumn.missingPercent.toFixed(1)}% missing data`,
      status: "warning",
    });
  }

  // Unique values check
  const uniqueRatio = props.selectedColumn.uniqueValues / props.dataset.length;
  if (props.selectedColumn.originalType === "string" && uniqueRatio < 0.5) {
    factors.push({
      icon: "✅",
      text: "Good cardinality for classification",
      status: "good",
    });
  } else if (props.selectedColumn.originalType === "number") {
    factors.push({
      icon: "✅",
      text: "Numeric data suitable for ML",
      status: "good",
    });
  }

  // Encoding bonus
  if (props.selectedColumn.hasEncoding) {
    factors.push({
      icon: "🔄",
      text: `${props.selectedColumn.encoding} encoding detected`,
      status: "good",
    });
  }

  return factors;
};

const getSampleValues = () => {
  if (!props.selectedColumn || !props.selectedColumn.sampleValues) {
    return [];
  }
  return props.selectedColumn.sampleValues.slice(0, 8);
};

const formatSampleValue = (value) => {
  if (value === null || value === undefined) return "N/A";
  if (typeof value === "number") return value.toLocaleString();
  if (typeof value === "string" && value.length > 50) {
    return value.substring(0, 47) + "...";
  }
  return String(value);
};

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
    if (props.selectedColumn.originalType === "number" && column.uniqueValues > 20) {
      recommendations.push({
        icon: "📈",
        title: "Regression Analysis",
        description: "Predict continuous numerical values",
        confidence: Math.min(85, column.suitabilityScore),
        taskType: "regression",
      });
    }

    // Time Series (if applicable)
    if (props.selectedColumn.originalType === "date" || /date|time|timestamp/i.test(column.name)) {
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
</script>

<style scoped>
.insights-panel {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 180px);
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

/* Scrollbar */
.insights-panel::-webkit-scrollbar {
  width: 8px;
}

.insights-panel::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
}

.insights-panel::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

.insights-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}
</style>
