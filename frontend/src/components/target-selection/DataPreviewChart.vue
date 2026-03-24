<template>
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
          class="chart-selector"
          :class="{ 'placeholder': !chartType }"
        >
          <template v-if="selectedColumn && (selectedColumn.originalType === 'number' || selectedColumn.originalType === 'numerical')">
            <option value="histogram">📊 Histogram</option>
            <option value="box">📦 Box Plot</option>
            <option value="scatter">🔵 Scatter Plot</option>
          </template>

          <template v-else-if="selectedColumn && (selectedColumn.originalType === 'string' || selectedColumn.originalType === 'categorical' || selectedColumn.originalType === 'boolean')">
            <option value="bar">📊 Bar Chart</option>
            <option value="pie">🥧 Pie Chart</option>
          </template>

          <template v-else>
            <option value="bar">📊 Bar Chart</option>
          </template>
        </select>

        <!-- ENCODING INDICATOR -->
        <div
          v-if="selectedColumn.encoding && selectedColumn.encoding !== 'none'"
          class="encoding-badge"
        >
          🔄 {{ selectedColumn.encoding }} encoded
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
            style="width: 100%; height: 400px"
          ></canvas>
        </div>

        <div v-show="false"></div> <!-- Placeholder to keep structure if needed, or just remove -->
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from 'vue';

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

const chartType = ref("");
const isLoadingChart = ref(false);
const chartCanvas = ref(null);
const chartInstance = ref(null);

watch(() => props.selectedColumn, async (newColumn, oldColumn) => {
  if (!newColumn) {
    // Clear chart when column is deselected
    if (chartInstance.value) {
      chartInstance.value.destroy();
      chartInstance.value = null;
    }
    return;
  }
  
  // Only update if column actually changed
  if (oldColumn && newColumn.name === oldColumn.name) return;
  
  if (newColumn.originalType === "number" || newColumn.originalType === "numerical") {
    chartType.value = "histogram";
  } else if (newColumn.originalType === "date") {
    chartType.value = "bar"; // Dates don't have a special chart in this component yet
  } else {
    chartType.value = "bar";
  }
  
  console.log("📊 Chart update triggered for:", newColumn.name);
  console.log("   Has backend distribution:", !!newColumn.distribution);

  await nextTick();
  await generateChart();
});

watch(chartType, async (newType, oldType) => {
  // Only regenerate if chart type actually changed and we have a column
  if (props.selectedColumn && newType !== oldType) {
    await nextTick();
    await generateChart();
  }
});

const getChartTypeName = () => {
  const chartNames = {
    histogram: "Histogram",
    box: "Box Plot",
    scatter: "Scatter Plot",
    bar: "Bar Chart",
    pie: "Pie Chart",
  };
  return chartNames[chartType.value] || "Chart";
};

const isFullDatasetChart = () => {
  if (!props.selectedColumn) return false;
  if (chartType.value === 'scatter') return false; 
  return !!props.selectedColumn.distribution;
};

const getTruncatedName = (name) => {
    if (!name) return "";
    return String(name).length > 20 ? String(name).substring(0, 20) + "..." : String(name);
};

// ============= CHART GENERATION =============

const generateChart = async () => {
  // Comprehensive null guards
  if (!props.selectedColumn || !chartCanvas.value) {
    isLoadingChart.value = false;
    return;
  }
  
  // Ensure dataset is valid
  if (!props.dataset || props.dataset.length === 0) {
    isLoadingChart.value = false;
    return;
  }

  isLoadingChart.value = true;

  try {
    // Safely destroy existing chart
    if (chartInstance.value) {
      try {
        chartInstance.value.destroy();
      } catch (e) {
        console.warn('Chart destroy error:', e);
      }
      chartInstance.value = null;
    }

    await new Promise((resolve) => setTimeout(resolve, 100));

    // Double-check canvas still exists after timeout
    if (!chartCanvas.value) {
      isLoadingChart.value = false;
      return;
    }

    const ctx = chartCanvas.value.getContext("2d");
    if (!ctx) {
      isLoadingChart.value = false;
      return;
    }
    
    ctx.clearRect(0, 0, chartCanvas.value.width, chartCanvas.value.height);

    const rawData = props.dataset.map((row) => row[props.selectedColumn.name]);
    const cleanData = rawData.filter(
      (val) => val !== null && val !== undefined && val !== "" && val !== "null"
    );

    const { Chart, registerables } = await import("chart.js");
    Chart.register(...registerables);

    if (
      props.selectedColumn.originalType === "numerical" ||
      props.selectedColumn.originalType === "number"
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
  const distribution = props.selectedColumn.distribution;
  const useBackend = distribution && distribution.type === "numerical";

  switch (chartType.value) {
    case "histogram":
      if (useBackend && distribution.histogram) {
        await createBackendHistogramChart(Chart, ctx, distribution.histogram);
      } else {
        await createHistogramChart(Chart, ctx, data);
      }
      break;
    case "box":
      if (useBackend && distribution.box_plot) {
        await createBackendBoxPlotChart(Chart, ctx, distribution.box_plot);
      } else {
        await createBoxPlotChart(Chart, ctx, data);
      }
      break;
    case "scatter":
      // Scatter plot still requires raw data points, so use sample
      await createScatterChart(Chart, ctx, data);
      break;
    default:
      if (useBackend && distribution.histogram) {
        await createBackendHistogramChart(Chart, ctx, distribution.histogram);
      } else {
        await createHistogramChart(Chart, ctx, data);
      }
  }
};

const generateCategoricalChart = async (Chart, ctx, data) => {
  let entries = [];
  const distribution = props.selectedColumn.distribution;

  if (distribution && distribution.type === "categorical" && distribution.value_counts) {
      // Use backend value counts
      entries = Object.entries(distribution.value_counts);
  } else {
      // Fallback to sample data counting
      const counts = {};
      data.forEach((val) => {
        counts[val] = (counts[val] || 0) + 1;
      });
      entries = Object.entries(counts)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 15);
  }

  switch (chartType.value) {
    case "bar":
      await createBarChart(Chart, ctx, entries);
      break;
    case "pie":
      await createPieChart(Chart, ctx, entries);
      break;
    default:
      await createBarChart(Chart, ctx, entries);
  }
};

const createBackendHistogramChart = async (Chart, ctx, histogram) => {
    // Histogram from backend: counts and bin_edges
    // bin_edges has N+1 elements, counts has N elements
    const labels = [];
    for (let i = 0; i < histogram.counts.length; i++) {
        const start = histogram.bin_edges[i];
        const end = histogram.bin_edges[i+1];
        labels.push(`${start.toFixed(1)}-${end.toFixed(1)}`);
    }

    chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Count (Full Dataset)",
          data: histogram.counts,
          backgroundColor: "rgba(102, 126, 234, 0.7)",
          borderColor: "rgba(102, 126, 234, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: getChartOptions(`Distribution (${isFullDatasetChart() ? "Full Dataset" : "Sampled"})`),
  });
};

const createBackendBoxPlotChart = async (Chart, ctx, boxPlot) => {
  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Min", "Q1", "Median", "Q3", "Max"],
      datasets: [
        {
          label: "Statistics (Full Dataset)",
          data: [boxPlot.min, boxPlot.q1, boxPlot.median, boxPlot.q3, boxPlot.max],
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
    options: getChartOptions(`Box Plot (${isFullDatasetChart() ? "Full Dataset" : "Sampled"})`),
  });
};

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
};

const createPieChart = async (Chart, ctx, entries) => {
  chartInstance.value = new Chart(ctx, {
    type: "pie",
    data: {
      labels: entries.map(([name]) =>
        String(name).length > 20 ? String(name).substring(0, 20) + "..." : String(name)
      ),
      datasets: [
        {
          data: entries.map(([, count]) => count),
          backgroundColor: generateColors(entries.length),
          borderWidth: 2,
        },
      ],
    },
    options: getPieChartOptions(`Value Distribution (${isFullDatasetChart() ? "Full Dataset" : "Sampled"})`),
  });
};

const createBarChart = async (Chart, ctx, entries) => {
  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: entries.map(([name]) =>
        String(name).length > 15 ? String(name).substring(0, 15) + "..." : String(name)
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
    options: getChartOptions(`Category Counts (${isFullDatasetChart() ? "Full Dataset" : "Sampled"})`),
  });
};

const createScatterChart = async (Chart, ctx, data) => {
  // Create scatter plot with index vs value
  const scatterData = data.map((value, index) => ({ x: index, y: value }));
  
  chartInstance.value = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Values",
          data: scatterData,
          backgroundColor: "rgba(102, 126, 234, 0.6)",
          borderColor: "rgba(102, 126, 234, 1)",
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      ...getChartOptions("Scatter Plot (Sampled)"),
      scales: {
        ...getChartOptions("Scatter Plot").scales,
        x: {
          ...getChartOptions("Scatter Plot").scales.x,
          title: {
            display: true,
            text: "Index",
            color: "rgba(255, 255, 255, 0.8)",
          },
        },
        y: {
          ...getChartOptions("Scatter Plot").scales.y,
          title: {
            display: true,
            text: "Value",
            color: "rgba(255, 255, 255, 0.8)",
          },
        },
      },
    },
  });
};

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

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
    chartInstance.value = null;
  }
});
</script>

<style scoped>
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

.chart-selector option {
  color: #000000;
  background: #ffffff;
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

.insight-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  margin-top: 4px;
  letter-spacing: 0.5px;
}

.insight-badge.full {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.insight-badge.sampled {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.2);
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

.encoding-badge {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
