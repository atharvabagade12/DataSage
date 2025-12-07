<template>
  <aside class="column-selector">
    <div class="selector-header">
      <h3>Choose Target Column</h3>
      <p class="selector-subtitle">
        Select the column you want to predict or analyze
      </p>

      <!-- AI Disclaimer -->
      <div class="disclaimer-compact" :class="{ expanded: showDisclaimer }">
        <button
          @click="showDisclaimer = !showDisclaimer"
          class="disclaimer-toggle"
        >
          <span class="disclaimer-icon">⚠️</span>
          <span class="disclaimer-title">Target Analysis</span>
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
            Our algorithm analyzes data patterns to identify suitable target columns
            and filter out poor choices (IDs, dates, text fields). Please review
            recommendations and select the best target for your use case.
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
        <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
      <input
        v-model="searchQuery"
        placeholder="Search columns..."
        class="search-input"
      />
    </div>

    <div class="column-list-container">
      <!-- No Columns State -->
      <div v-if="filteredColumns.length === 0" class="no-columns">
        <div class="no-columns-icon">🔍</div>
        <p>No columns match your search</p>
        <button
          @click="clearFilters"
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
          @click="$emit('select', column)"
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
              {{ getColumnPreview(column) }}
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
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  columns: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedColumn: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['select']);

const searchQuery = ref("");
const activeFilter = ref("all");
const showDisclaimer = ref(false);

const columnFilters = [
  { type: "all", label: "All", icon: "📊" },
  { type: "number", label: "Numeric", icon: "🔢" },
  { type: "string", label: "Text", icon: "📝" },
  { type: "date", label: "Date", icon: "📅" },
  { type: "recommended", label: "Recommended", icon: "⭐" },
];

const filteredColumns = computed(() => {
  let columnsToFilter = props.columns;

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

const clearFilters = () => {
  searchQuery.value = '';
  activeFilter.value = 'all';
};

const getColumnTypeIcon = (type) => {
  const icons = { number: "🔢", string: "📝", date: "📅", boolean: "✅" };
  return icons[type] || "📄";
};

const getColumnPreview = (column) => {
  if (!column.sampleValues || column.sampleValues.length === 0) return "No data";

  const preview = column.sampleValues
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
</script>

<style scoped>
.column-selector {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 180px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.selector-header {
  flex-shrink: 0;
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
  margin-bottom: 0.27rem;
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

.search-box {
  position: relative;
  margin-bottom: 0.75rem;
  flex-shrink: 0;
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

.column-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: visible;
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
  max-height: calc(100vh - 480px);
  padding-bottom: 20px;
}

.column-item {
  padding: 0.8rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  flex-shrink: 0;
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
  font-size: 0.6rem;
  padding: 0.1rem 0.4rem;
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

.selection-helper {
  margin-top: 1rem;
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
  width: 10px;
}

.column-list::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 5px;
  margin: 8px 0 50px 0;
}

.column-list::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.5);
  border-radius: 5px;
  border: 1px solid rgba(26, 26, 46, 0.2);
}

.column-list::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.7);
}

.column-list::-webkit-scrollbar-thumb:active {
  background: rgba(102, 126, 234, 0.9);
}

.column-list {
  scrollbar-width: thin;
  scrollbar-color: rgba(102, 126, 234, 0.4) rgba(102, 126, 234, 0.1);
}

/* Disclaimer Styles */
.disclaimer-compact {
  margin: 10px 0 12px 0;
  background: linear-gradient(135deg, #fff3cd 0%, #fff8e1 100%);
  border-left: 3px solid #ffc107;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.disclaimer-compact.expanded {
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.15);
}

.disclaimer-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  color: #856404;
  transition: all 0.2s ease;
  text-align: left;
}

.disclaimer-toggle:hover {
  background: rgba(255, 193, 7, 0.1);
}

.disclaimer-icon {
  font-size: 0.9rem;
  flex-shrink: 0;
  line-height: 1;
}

.disclaimer-title {
  flex: 1;
  text-align: left;
  font-weight: 600;
}

.disclaimer-toggle svg {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
  flex-shrink: 0;
  fill: currentColor;
}

.disclaimer-toggle svg.rotated {
  transform: rotate(180deg);
}

.disclaimer-content {
  padding: 0 12px 10px 12px;
  animation: slideDown 0.3s ease;
  overflow: hidden;
}

.disclaimer-content p {
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.5;
  color: #856404;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 200px;
  }
}
</style>
