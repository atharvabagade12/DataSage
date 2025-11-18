<template>
  <div class="data-preview">
    <!-- Navigation Header -->
    <nav class="preview-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
            />
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
        >
          <div class="status-dot"></div>
          <span class="status-text">
            {{ backendConnected ? "ML Backend Ready" : "Frontend Mode" }}
          </span>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🔧</div>
        <h1>Advanced Preprocessing</h1>
        <p>Split, scale, and engineer features for optimal model training</p>
        <div class="dataset-summary">
          <span class="summary-item"
            >Dataset: <strong>{{ fileName }}</strong></span
          >
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ totalRows }} rows</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ totalColumns }} columns</span>
          <div class="quality-indicator">
          <div 
            class="quality-score"
            :class="{
              excellent: dataQuality.score >= 90,
              good: dataQuality.score >= 70 && dataQuality.score < 90,
              fair: dataQuality.score >= 50 && dataQuality.score < 70,
              poor: dataQuality.score < 50
            }"
          >
            {{ dataQuality.score }}% Quality
          </div>
        </div>
        </div>
      </div>
    </div>

    <div v-if="showBackendWarning" class="backend-warning">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" />
  </svg>
  <div>
    <strong>Backend Not Connected</strong>
    <p>Dataset splitting and scaling require backend connection. Please ensure the backend is running.</p>
  </div>
</div>

    <!-- Main Content Container -->
    <div class="main-container">
      <!-- Data Table Preview Section -->
      <section class="table-preview-section">
        <div class="section-header">
          <h2>Data Preview</h2>
          <div class="preview-controls">
            <button
              @click="currentSplitView = 'full'"
              :class="{ active: currentSplitView === 'full' }"
              class="preview-toggle"
              :disabled="splitApplied"
            >
              Full Dataset
            </button>
            <button
              @click="currentSplitView = 'train'"
              :class="{ active: currentSplitView === 'train' }"
              class="preview-toggle"
              :disabled="!splitApplied"
            >
              Train Data
            </button>
            <button
              @click="currentSplitView = 'test'"
              :class="{ active: currentSplitView === 'test' }"
              class="preview-toggle"
              :disabled="!splitApplied"
            >
              Test Data
            </button>
            <div v-if="splitApplied" class="data-stats">
              <span class="stat">
                {{
                  currentSplitView === "train"
                    ? trainRows
                    : currentSplitView === "test"
                    ? testRows
                    : totalRows
                }}
                rows
              </span>
              <span class="stat-value">{{ totalColumns }} columns</span>
            </div>
          </div>
        </div>

        <!-- Table Container -->
        <div class="table-container">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <span class="table-info">
                Showing {{ startRow }} to {{ endRow }} of
                {{ filteredRows.length }} rows
                <span v-if="splitApplied" class="split-badge">
                  {{
                    currentSplitView === "train"
                      ? "(Train Set)"
                      : currentSplitView === "test"
                      ? "(Test Set)"
                      : "(Full)"
                  }}
                </span>
              </span>
            </div>
            <div class="toolbar-right">
              <div class="search-box">
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
                  />
                </svg>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search data..."
                  class="search-input"
                />
              </div>
              <button @click="exportData" class="export-btn">
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
                  />
                </svg>
                Download
                {{
                  currentSplitView === "full"
                    ? "Full"
                    : (currentSplitView || "full").toUpperCase()
                }}
                CSV
              </button>
            </div>
          </div>

          <div class="data-table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th
                    v-for="column in visibleColumns"
                    :key="column"
                    class="table-header-cell"
                  >
                    <div class="header-content">
                      <span>{{ column }}</span>
                      <button @click="sortByColumn(column)" class="sort-button">
                        <svg
                          width="12"
                          height="12"
                          viewBox="0 0 24 24"
                          fill="currentColor"
                        >
                          <path d="M7,15L12,10L17,15H7Z" />
                        </svg>
                      </button>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in paginatedRows"
                  :key="index"
                  class="table-row"
                >
                  <td
                    v-for="column in visibleColumns"
                    :key="column"
                    class="table-cell"
                  >
                    <div class="cell-content">
                      {{ formatCellValue(row[column]) }}
                      <span
                        v-if="scalingApplied && isNumericalColumn(column)"
                        class="encoded-badge"
                        >Scaled</span
                      >
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="table-pagination">
            <div class="pagination-left">
              <select v-model="pageSize" class="page-size-select">
                <option :value="10">10 rows</option>
                <option :value="25">25 rows</option>
                <option :value="50">50 rows</option>
                <option :value="100">100 rows</option>
              </select>
            </div>
            <div class="pagination-controls">
              <button
                @click="currentPage = Math.max(1, currentPage - 1)"
                :disabled="currentPage === 1"
                class="page-btn"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"
                  />
                </svg>
                Previous
              </button>

              <div class="page-numbers">
                <button
                  v-for="page in visiblePageNumbers"
                  :key="page"
                  @click="currentPage = page"
                  :class="{ active: currentPage === page }"
                  class="page-number"
                >
                  {{ page }}
                </button>
              </div>

              <button
                @click="currentPage = Math.min(totalPages, currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="page-btn"
              >
                Next
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Advanced Preprocessing Toolkit Section -->
      <section class="preprocessing-section">
        <div class="section-header">
          <h2>Advanced Preprocessing Toolkit</h2>
          <p class="section-description">
            Configure dataset splitting and feature transformations for optimal
            model training
          </p>
        </div>

        <div class="preprocessing-grid">
          <!-- ========== CARD 1: DATASET SPLITTING ========== -->

          <!-- ========== CARD 1: DATASET SPLITTING (IMPROVED UI) ========== -->
          <div
            class="preprocessing-tool"
            :class="{
              active: isToolEnabled('datasetSplitting'),
              expanded: isDropdownOpen('datasetSplitting'),
            }"
          >
            <div class="tool-header">
              <div class="tool-info">
                <h3>
                  Dataset Splitting
                  <span class="required-badge">Required First Step</span>
                </h3>
                <p class="tool-description">
                  Split your dataset into train and test sets to prevent data
                  leakage
                </p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge" :class="{ success: splitApplied }">
                  {{ splitApplied ? "✓ Applied" : "Not Applied" }}
                </span>
                <button
                  @click="toggleDropdown('datasetSplitting')"
                  class="config-btn"
                  :class="{ active: isDropdownOpen('datasetSplitting') }"
                  v-if="isToolEnabled('datasetSplitting')"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      v-if="!isDropdownOpen('datasetSplitting')"
                      d="M7 10l5 5 5-5z"
                    />
                    <path v-else d="M7 14l5-5 5 5z" />
                  </svg>
                  {{
                    isDropdownOpen("datasetSplitting") ? "Close" : "Configure"
                  }}
                </button>
                <button
                  @click="
                    isToolEnabled('datasetSplitting')
                      ? disableTool('datasetSplitting')
                      : enableTool('datasetSplitting')
                  "
                  class="tool-btn"
                  :class="{ active: isToolEnabled('datasetSplitting') }"
                  :disabled="splitApplied"
                >
                  {{ isToolEnabled("datasetSplitting") ? "Disable" : "Enable" }}
                </button>
              </div>
            </div>

            <!-- ========== CARD CONTENT ========== -->
            <div
              class="tool-config"
              v-show="isDropdownOpen('datasetSplitting')"
            >
              <!-- Split Ratio Section -->
              <div class="config-group">
                <label class="config-label">
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"
                    />
                  </svg>
                  Train/Test Split Ratio
                </label>

                <div class="ratio-display">
                  <div class="ratio-badge-large train">
                    <span class="ratio-percentage"
                      >{{ (splitRatio * 100).toFixed(0) }}%</span
                    >
                    <span class="ratio-label">Train</span>
                  </div>
                  <div class="ratio-separator">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
                    </svg>
                  </div>
                  <div class="ratio-badge-large test">
                    <span class="ratio-percentage"
                      >{{ ((1 - splitRatio) * 100).toFixed(0) }}%</span
                    >
                    <span class="ratio-label">Test</span>
                  </div>
                </div>

                <div class="slider-container">
                  <input
                    type="range"
                    min="0.5"
                    max="0.95"
                    step="0.05"
                    v-model.number="splitRatio"
                    :disabled="splitApplied"
                    class="split-slider"
                  />
                  <div
                    class="slider-track-fill"
                    :style="{ width: splitRatio * 100 + '%' }"
                  ></div>
                </div>

                <div class="quick-ratios">
                  <button
                    v-for="ratio in [0.6, 0.7, 0.8, 0.9]"
                    :key="ratio"
                    @click="splitRatio = ratio"
                    :disabled="splitApplied"
                    class="quick-ratio-btn"
                    :class="{ active: splitRatio === ratio }"
                  >
                    {{ (ratio * 100).toFixed(0) }}/{{
                      ((1 - ratio) * 100).toFixed(0)
                    }}
                  </button>
                </div>
              </div>

              <!-- Split Strategy Section -->
              <div class="config-group">
                <label class="config-label">
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" />
                  </svg>
                  Split Strategy
                </label>
                <select
                  v-model="splitStrategy"
                  :disabled="splitApplied"
                  class="config-select"
                >
                  <option value="random">Random Split</option>
                  <option value="stratified">
                    Stratified Split (preserves class distribution)
                  </option>
                </select>
                <p class="config-help">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"
                    />
                  </svg>
                  {{
                    splitStrategy === "stratified"
                      ? "Maintains the same proportion of target classes in both train and test sets"
                      : "Randomly shuffles and splits the data"
                  }}
                </p>
              </div>

              <!-- Random Seed Section (Optional) -->
              <div class="config-group">
                <label class="config-label">
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                    />
                  </svg>
                  Random Seed
                  <span class="optional-tag">Optional</span>
                </label>
                <input
                  type="number"
                  v-model.number="randomSeed"
                  :disabled="splitApplied"
                  placeholder="Enter seed for reproducibility (e.g., 42)"
                  class="config-input"
                />
                <p class="config-help">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"
                    />
                  </svg>
                  Set a seed value for reproducible splits. Leave empty for
                  random splitting.
                </p>
              </div>

              <!-- Action Buttons -->
              <div class="config-actions">
                <button
                  @click="applySplit"
                  class="btn btn-apply"
                  :disabled="isProcessing || splitApplied"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
                    />
                  </svg>
                  {{ isProcessing ? "Splitting..." : "Apply Split" }}
                </button>
                <button
                  v-if="splitApplied"
                  @click="resetSplit"
                  class="btn btn-reset"
                  :disabled="isProcessing"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
                    />
                  </svg>
                  Reset Split
                </button>
              </div>

              <!-- Split Summary (shown after split) -->
              <div class="split-summary" v-if="splitApplied">
                <div class="summary-header">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
                    />
                  </svg>
                  <h4>Split Applied Successfully</h4>
                </div>
                <div class="summary-stats">
                  <div class="stat-box train">
                    <div class="stat-icon">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                      >
                        <path
                          d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7z"
                        />
                      </svg>
                    </div>
                    <div class="stat-content">
                      <span class="stat-value">{{
                        trainRows.toLocaleString()
                      }}</span>
                      <span class="stat-label">Train Rows</span>
                    </div>
                  </div>
                  <div class="stat-box test">
                    <div class="stat-icon">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                      >
                        <path
                          d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"
                        />
                      </svg>
                    </div>
                    <div class="stat-content">
                      <span class="stat-value">{{
                        testRows.toLocaleString()
                      }}</span>
                      <span class="stat-label">Test Rows</span>
                    </div>
                  </div>
                  <div class="stat-box total">
                    <div class="stat-icon">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                      >
                        <path
                          d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2z"
                        />
                      </svg>
                    </div>
                    <div class="stat-content">
                      <span class="stat-value">{{
                        totalRows.toLocaleString()
                      }}</span>
                      <span class="stat-label">Total Rows</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>


          <!-- ========== CARD:2 CATEGORICAL ENCODING ========== -->

<div
  class="preprocessing-tool"
  :class="{
    active: isToolEnabled('categoricalEncoding'),
    expanded: isDropdownOpen('categoricalEncoding'),
    disabled: !splitApplied,
  }"
>
  <div class="tool-header">
    <div class="tool-info">
      <h3>Categorical Encoding</h3>
      <p>
        Convert categorical features to numerical representations for ML algorithms.
      </p>
    </div>
    <div class="tool-actions">
      <span class="tool-badge" :class="{ success: encodingApplied }">
        {{ encodingApplied ? "✓ Applied" : "Not Applied" }}
      </span>
      <button
        @click="splitApplied && toggleDropdown('categoricalEncoding')"
        class="config-btn"
        :class="{ active: isDropdownOpen('categoricalEncoding') }"
        :disabled="!splitApplied"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path
            v-if="!isDropdownOpen('categoricalEncoding')"
            d="M7 10l5 5 5-5z"
          />
          <path v-else d="M7 14l5-5 5 5z" />
        </svg>
        {{ isDropdownOpen("categoricalEncoding") ? "Close" : "Configure" }}
      </button>
      <button
        @click="
          isToolEnabled('categoricalEncoding')
            ? disableTool('categoricalEncoding')
            : enableTool('categoricalEncoding')
        "
        class="tool-btn"
        :class="{ active: isToolEnabled('categoricalEncoding') }"
        :disabled="!splitApplied"
      >
        {{ isToolEnabled("categoricalEncoding") ? "Disable" : "Enable" }}
      </button>
    </div>
  </div>

  <!-- Dropdown Content -->
  <div class="tool-config" v-show="isDropdownOpen('categoricalEncoding')">
    <h4>Select Categorical Columns to Encode</h4>
    <div class="encoding-actions" style="margin-bottom: 1rem; display: flex; gap: 1rem;">
      <button @click="selectAllCategoricalColumns" class="btn small secondary">
        Select All
      </button>
      <button @click="deselectAllCategoricalColumns" class="btn small secondary">
        Deselect All
      </button>
      <!-- <button @click="autoSelectForEncoding(selectedTarget)" class="btn small secondary">
        Auto-select (Excludes Target)
      </button> -->
    </div>

    <div class="encoding-list">
      <div
        v-for="column in categoricalColumns.filter(c => c.name !== selectedTarget)"
        :key="column.name"
        class="encoding-row"
        style="margin-bottom:0.75rem"
      >
        <label style="font-size:1rem; display:flex; align-items:center;">
          <input
            type="checkbox"
            v-model="column.encode"
            @change="toggleColumnEncoding(column)"
            style="margin-right:0.5rem"
          />
          {{ column.name }}
        </label>
        <select
          v-if="column.encode"
          v-model="column.encoding"
          @change="setEncodingMethod(column.name, column.encoding)"
          style="margin-left:1rem; min-width: 160px;"
        >
          <option value="onehot">One-Hot Encoding</option>
          <option value="label">Label Encoding</option>
          <option value="ordinal">Ordinal Encoding</option>
        </select>
      </div>
    </div>

    <div style="text-align: center; margin-top: 2rem;">
      <button
        @click="applyCategoricalEncoding"
        class="btn btn-apply"
        style="padding: 0.75rem 2.5rem; font-size: 1.1rem;"
        :disabled="categoricalColumns.filter(c => c.name !== selectedTarget && c.encode).length === 0"
      >
        Apply Categorical Encoding
      </button>
    </div>
  </div>
</div>

          <!-- ========== CARD 3: FEATURE SCALING ========== -->
          <div
            class="preprocessing-tool"
            :class="{
              active: isToolEnabled('featureScaling'),
              expanded: isDropdownOpen('featureScaling'),
              disabled: !splitApplied,
            }"
          >
            <div class="tool-header">
              <div class="tool-info">
                <h3>Feature Scaling</h3>
                <p>Normalize numerical features for better model performance</p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge" :class="{ success: scalingApplied }">
                  {{ scalingApplied ? "✓ Applied" : "Not Applied" }}
                </span>

                <button
                  @click="splitApplied && toggleDropdown('featureScaling')"
                  class="config-btn"
                  :class="{ active: isDropdownOpen('featureScaling') }"
                  v-if="isToolEnabled('featureScaling')"
                  :disabled="!splitApplied"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      v-if="!isDropdownOpen('featureScaling')"
                      d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"
                    />
                    <path
                      v-else
                      d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"
                    />
                  </svg>
                  {{ isDropdownOpen("featureScaling") ? "Close" : "Configure" }}
                </button>

                <button
                  @click="
                    isToolEnabled('featureScaling')
                      ? disableTool('featureScaling')
                      : enableTool('featureScaling')
                  "
                  class="tool-btn"
                  :class="{ active: isToolEnabled('featureScaling') }"
                  :disabled="!splitApplied"
                >
                  {{ isToolEnabled("featureScaling") ? "Disable" : "Enable" }}
                </button>
              </div>
            </div>

            <!-- Dropdown Content -->
            <div class="tool-config" v-show="isDropdownOpen('featureScaling')">
              <!-- Warning if split not applied -->
              <div class="alert alert-warning" v-if="!splitApplied">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"
                  />
                </svg>
                <span
                  >Please apply dataset splitting first to prevent data
                  leakage</span
                >
              </div>

              <div class="config-section" :class="{ disabled: !splitApplied }">
                <!-- Scaling Method -->
                <div class="form-group">
                  <label class="form-label">
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z"
                      />
                    </svg>
                    Scaling Method
                  </label>
                  <select
                    v-model="scalingMethod"
                    :disabled="!splitApplied || scalingApplied"
                    class="form-select"
                  >
                    <option value="standard">
                      StandardScaler - Standardize features (mean=0, std=1)
                    </option>
                    <option value="minmax">
                      MinMaxScaler - Scale to range [0, 1]
                    </option>
                    <option value="robust">
                      RobustScaler - Scale using median and IQR (robust to
                      outliers)
                    </option>
                    <option value="maxabs">
                      MaxAbsScaler - Scale to [-1, 1] based on max absolute
                      value
                    </option>
                    <option value="none">No Scaling</option>
                  </select>
                  <p class="help-text">
                    {{
                      scalingMethod === "standard"
                        ? "Best for algorithms that assume normally distributed data (e.g., Logistic Regression, SVM)"
                        : scalingMethod === "minmax"
                        ? "Best for algorithms that require bounded features (e.g., Neural Networks)"
                        : scalingMethod === "robust"
                        ? "Best when data contains many outliers"
                        : scalingMethod === "maxabs"
                        ? "Best for data that is already centered at zero or sparse data"
                        : "Features will not be scaled"
                    }}
                  </p>
                </div>

                <!-- Action Buttons -->
                <div class="action-buttons">
                  <button
                    @click="applyScaling"
                    class="btn btn-apply"
                    :disabled="
                      !splitApplied ||
                      isProcessing ||
                      scalingApplied ||
                      scalingMethod === 'none'
                    "
                  >
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
                      />
                    </svg>
                    {{ isProcessing ? "Scaling..." : "Apply Scaling" }}
                  </button>
                  <button
                    v-if="scalingApplied"
                    @click="resetScaling"
                    class="btn btn-reset"
                    :disabled="isProcessing"
                  >
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
                      />
                    </svg>
                    Reset Scaling
                  </button>
                </div>

                <!-- Scaling Info -->
                <div class="info-panel success" v-if="scalingApplied">
                  <div class="info-header">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
                      />
                    </svg>
                    <h4>Scaling Applied</h4>
                  </div>
                  <p class="info-text">
                    <strong>{{ scalingMethod.toUpperCase() }}</strong> scaling
                    has been applied to numerical features in the training set.
                    The same transformation will be applied to the test set.
                  </p>
                </div>
              </div>

              <!-- Dropdown Footer -->
              <div class="dropdown-footer">
                <button
                  @click="toggleDropdown('featureScaling')"
                  class="close-dropdown-btn"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
                    />
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>

          <!-- CARD 3: Feature Engineering (Coming Soon) -->
          <div class="preprocessing-tool disabled">
            <div class="tool-header">
              <div class="tool-info">
                <h3>Feature Engineering</h3>
                <p>Apply advanced feature engineering techniques</p>
              </div>
              <div class="card-header-right">
                <span class="status-badge">Coming Soon</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Action Footer -->
    <div class="action-footer">
      <div class="footer-content">
        <!-- Processing Status -->
        <div class="processing-status">
          <div v-if="splitApplied" class="processing-complete">
            <div class="success-icon"></div>
            <div class="success-text">
              <h3>Dataset Split Successfully!</h3>
              <p>
                Your data has been split into train ({{ trainRows }} rows) and
                test ({{ testRows }} rows) sets
                <span v-if="scalingApplied">
                  with {{ scalingMethod }} scaling applied</span
                >
              </p>
            </div>
          </div>

          <div v-else class="processing-original">
            <div class="original-icon"></div>
            <div class="original-text">
              <h3>Ready for Advanced Preprocessing</h3>
              <p>
                Split your dataset first to enable feature scaling and
                engineering
              </p>
            </div>
          </div>
        </div>

        <!-- Dataset Stats -->
        <div class="final-stats">
          <div class="stat-item">
            <span class="stat-value">{{ totalRows }}</span>
            <span class="stat-label">Total Rows</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ totalColumns }}</span>
            <span class="stat-label">Columns</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ dataQuality.score }}%</span>
            <span class="stat-label">Quality Score</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="footer-actions">
          <button
            v-if="splitApplied"
            @click="resetAllTransformations"
            class="footer-btn secondary"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"
              />
            </svg>
            Reset All Transformations
          </button>

          <button
            @click="proceedToModelTraining"
            class="footer-btn primary"
            :disabled="!splitApplied"
          >
            <span>Proceed to Model Training</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isProcessing" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>{{ processingMessage }}</p>
      </div>
    </div>
  </div>
</template>



<script setup>

import { ref, reactive, computed, onMounted, watch, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useMLDataFlowStore } from "~/stores/mlDataFlow";


const router = useRouter();
const mlStore = useMLDataFlowStore();

// ==================== BACKEND & PROCESSING STATE ====================
const backendConnected = computed(() => mlStore.backendConnected);
const isProcessing = ref(false);
const processingMessage = ref("");

// ==================== DATASET STATE ====================
const fileName = ref("");
const datasetId = ref(null);
const originalDatasetId = ref(null);
const cleanedDatasetId = ref(null);
const totalRowsInBackend = ref(0);

// Original dataset (before split)
const originalDataset = ref([]);
const originalDatasetBackup = ref([]);

// Train/Test split data
const trainData = ref([]);
const testData = ref([]);
const trainRows = ref(0);
const testRows = ref(0);

// Columns
const columns = ref([]);

// Selected target variable
const mlAppState = JSON.parse(localStorage.getItem('mlAppState') || '{}');
const selectedTarget = ref(mlAppState.selectedTarget || ""); 


// ==================== SPLIT & SCALE CONFIG ====================
const splitApplied = ref(false);
const scalingApplied = ref(false);
const currentSplitView = ref("full"); // 'full', 'train', 'test'
const splitRatio = ref(0.8);
const splitStrategy = ref("random"); // 'random' or 'stratified'
const randomSeed = ref(null);
const scalingMethod = ref("standard"); // 'standard', 'minmax', 'robust', 'maxabs', 'none'

// ==================== TOOLKIT STATE ====================
const enabledTools = ref([]);
const openDropdowns = ref([]);

// ==================== TABLE STATE ====================
const searchQuery = ref("");
const currentPage = ref(1);
const pageSize = ref(25);
const sortColumn = ref("");
const sortDirection = ref("asc");

// ==================== COMPUTED PROPERTIES ====================

const totalRows = computed(
  () => totalRowsInBackend.value || originalDataset.value.length
);

console.log('Backend connected?', mlStore.backendConnected);

console.log("Original Dataset:", originalDataset.value.lenght);
console.log("Total rows: ", totalRowsInBackend.value); // 0

const totalColumns = computed(() => columns.value.length);

const dataQuality = computed(() => {
  if (!originalDataset.value.length || !columns.value.length)
    return { score: 100 };

  const totalCells = originalDataset.value.length * columns.value.length;
  let issues = 0;

  originalDataset.value.forEach((row) => {
    columns.value.forEach((col) => {
      const value = row[col.name];
      if (
        value === null ||
        value === undefined ||
        value === "" ||
        value === "null"
      ) {
        issues++;
      }
    });
  });

  const score = Math.max(
    0,
    Math.round(((totalCells - issues) / totalCells) * 100)
  );
  return { score };
});

const checkBackendConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/health');
    mlStore.backendConnected = response.ok;
    console.log('✅ Backend connected:', mlStore.backendConnected);
  } catch (e) {
    mlStore.backendConnected = false;
    console.error('❌ Backend connection failed:', e);
  }
};

const showBackendWarning = computed(() => {
  return !mlStore.backendConnected || !totalRowsInBackend.value;
});

// Current dataset based on split view
const currentDataset = computed(() => {
  if (!splitApplied.value) return originalDataset.value;
  if (currentSplitView.value === "train") return trainData.value;
  if (currentSplitView.value === "test") return testData.value;
  return originalDataset.value;
});

// Visible columns
const visibleColumns = computed(() => {
  return columns.value.map((col) => col.name || col);
});

// Display row count
const displayedRowCount = computed(() => {
  if (splitApplied.value) {
    if (currentSplitView.value === "train") return trainRows.value;
    if (currentSplitView.value === "test") return testRows.value;
  }
  return totalRows.value;
});

const categoricalColumns = computed(() =>
  columns.value.filter(col => col.type === 'categorical')
);
// For per-column encoding selection state (update as needed for your structure)
categoricalColumns.value.forEach(col => {
  col.encode = col.encode ?? false;       // Whether to encode
  col.encoding = col.encoding ?? 'onehot';// Encoding method: onehot, label, ordinal
});




const backendTotalRows = computed(() => {
  if (!mlStore.datasetId) return 'unknown3';
  const record = mlStore.registeredDatasets.get(mlStore.datasetId);
  if (!record || !record.shape) return 'unknown4';
  return record.shape[0] || 'unknown5';
});

console.log(`Backend dataset total rows: ${backendTotalRows.value || 'unknown'}`);
console.log(`Backend dataset total rows: ${backendTotalRows.value || 'unknown'}`);

// Filtered rows
const filteredRows = computed(() => {
  let rows = currentDataset.value;

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    rows = rows.filter((row) =>
      Object.values(row).some((value) =>
        String(value || "")
          .toLowerCase()
          .includes(query)
      )
    );
  }

  if (sortColumn.value) {
    rows = [...rows].sort((a, b) => {
      const aVal = a[sortColumn.value];
      const bVal = b[sortColumn.value];

      if (sortDirection.value === "asc") {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });
  }

  return rows;
});

// Paginated rows
const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredRows.value.slice(start, start + pageSize.value);
});

// Pagination helpers
const totalPages = computed(() => {
  return Math.ceil(filteredRows.value.length / pageSize.value);
});

const startRow = computed(() => {
  return (currentPage.value - 1) * pageSize.value + 1;
});

const endRow = computed(() => {
  return Math.min(
    currentPage.value * pageSize.value,
    filteredRows.value.length
  );
});

const visiblePageNumbers = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push("...");
      pages.push(total);
    } else if (current >= total - 3) {
      pages.push(1);
      pages.push("...");
      for (let i = total - 4; i <= total; i++) pages.push(i);
    } else {
      pages.push(1);
      pages.push("...");
      for (let i = current - 1; i <= current + 1; i++) pages.push(i);
      pages.push("...");
      pages.push(total);
    }
  }

  return pages;
});

const numericalColumns = computed(() => {
  if (!columns.value || columns.value.length === 0) return [];
  return columns.value
    .filter(col => col.type === 'number' || col.type === 'numerical')
    .map(col => col.name);
});

// ==================== UTILITY FUNCTIONS ====================

const formatCellValue = (value) => {
  if (value === null || value === undefined) return "-";
  if (typeof value === "number") {
    return value % 1 === 0 ? value : value.toFixed(2);
  }
  return String(value);
};

const isNumericalColumn = (columnName) => {
  const col = columns.value.find((c) => (c.name || c) === columnName);
  return col && (col.type === "numerical" || col.type === "numeric");
};

const getHealthLevel = (quality) => {
  if (quality >= 80) return "excellent";
  if (quality >= 60) return "good";
  if (quality >= 40) return "fair";
  return "poor";
};

const sortByColumn = (column) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortColumn.value = column;
    sortDirection.value = "asc";
  }
};

const getColumnSample = (column) => {
  if (!originalDataset.value || originalDataset.value.length === 0) return "";
  const sample = originalDataset.value
    .slice(0, 3)
    .map((row) => row[column.name || column])
    .filter((v) => v);
  return sample.join(", ");
};

// Toggle encoding for a column
function toggleColumnEncoding(column) {
  // If column is selected but has no encoding method, default to 'onehot'
  if (column.encode && !column.encoding) column.encoding = 'onehot';
}

// Set encoding method for a column
function setEncodingMethod(columnName, method) {
  const col = columns.value.find(c => c.name === columnName);
  if (col) col.encoding = method;
}

// Select/Deselect all categorical columns
function selectAllCategoricalColumns() {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) baseCol.encode = true;
  });
}

function deselectAllCategoricalColumns() {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) baseCol.encode = false;
  });
}

// Smart auto-select (exclude target column by name)
function autoSelectForEncoding(targetName) {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) baseCol.encode = (col.name !== targetName && col.unique > 2);
  });
}


// ==================== TOOLKIT FUNCTIONS ====================

const isToolEnabled = (toolName) => {
  return enabledTools.value.includes(toolName);
};

const isDropdownOpen = (toolName) => {
  return openDropdowns.value.includes(toolName);
};

const toggleDropdown = (toolName) => {
  const index = openDropdowns.value.indexOf(toolName);
  if (index > -1) {
    openDropdowns.value.splice(index, 1);
  } else {
    openDropdowns.value.push(toolName);
  }
};

const enableTool = (toolName) => {
  if (!enabledTools.value.includes(toolName)) {
    enabledTools.value.push(toolName);
  }
  // Auto-open the dropdown when enabling
  if (!openDropdowns.value.includes(toolName)) {
    openDropdowns.value.push(toolName);
  }
};

const disableTool = (toolName) => {
  const index = enabledTools.value.indexOf(toolName);
  if (index > -1) {
    enabledTools.value.splice(index, 1);
    const dropdownIndex = openDropdowns.value.indexOf(toolName);
    if (dropdownIndex > -1) {
      openDropdowns.value.splice(dropdownIndex, 1);
    }
  }
};



// ==================== FETCH BACKEND DATASET INFO ====================
const fetchBackendDatasetInfo = async (datasetId) => {
  if (!datasetId) {
    console.error('❌ No dataset ID provided');
    return null;
  }

  console.log(`📡 Fetching backend dataset info for ID: ${datasetId}`);

  try {
    const response = await fetch(`http://localhost:8000/api/datasets/${datasetId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Dataset not found in backend`);
    }

    const backendInfo = await response.json();
    console.log('✅ Backend dataset info:', backendInfo);

    // Update backend row count
    if (backendInfo.shape && Array.isArray(backendInfo.shape)) {
      totalRowsInBackend.value = backendInfo.shape[0];
    }

    return backendInfo;
  } catch (error) {
    console.error('❌ Failed to fetch backend dataset:', error);
    alert(`⚠️ Backend dataset not found. Please go back and re-process your data.`);
    return null;
  }
};


// ==================== DATA LOADING ====================

const loadInitialData = async () => {
  console.log("\n" + "=".repeat(80));
  console.log("📊 ADVANCED PREPROCESSING - Loading Dataset");
  console.log("=".repeat(80));

  try {
    // Step 1: Check backend connection
    await checkBackendConnection();

    if (!mlStore.backendConnected) {
      alert('⚠️ Backend is not connected. Some features may not work.');
    }

    // Step 2: Get dataset ID (prefer cleaned ID)
    datasetId.value = mlStore.cleanedDatasetId || mlStore.datasetId;
    
    if (!datasetId.value) {
      // Fallback to localStorage
      const processedData = localStorage.getItem("processedData");
      if (processedData) {
        const data = JSON.parse(processedData);
        datasetId.value = data.backendDatasetId || data.datasetId;
      }
    }

    console.log(`📋 Using dataset ID: ${datasetId.value}`);

    // Step 3: Fetch backend dataset info (CRITICAL!)
    if (mlStore.backendConnected && datasetId.value) {
      const backendInfo = await fetchBackendDatasetInfo(datasetId.value);
      
      if (!backendInfo) {
        throw new Error('Dataset not found in backend');
      }

      // Store backend total rows
      if (backendInfo.shape) {
        totalRowsInBackend.value = backendInfo.shape[0];
      }
    }

    // Step 4: Load preview data for UI
    if (mlStore.dataset && mlStore.dataset.length > 0) {
      console.log("✅ Loading preview from mlStore");
      originalDataset.value = mlStore.dataset.slice(0, 200);
      fileName.value = mlStore.fileName || "dataset.csv";
    } else {
      // Fallback to localStorage
      const processedData = localStorage.getItem("processedData");
      if (processedData) {
        const data = JSON.parse(processedData);
        originalDataset.value = (data.data || []).slice(0, 200);
        fileName.value = data.fileName || "dataset.csv";
      }
    }

    // Step 5: Analyze columns
    analyzeColumns();

    originalDatasetBackup.value = JSON.parse(JSON.stringify(originalDataset.value));

    console.log(`✅ Loaded ${originalDataset.value.length} preview rows`);
    console.log(`✅ Backend has ${totalRowsInBackend.value} total rows`);
    console.log("=" + "=".repeat(80) + "\n");

  } catch (error) {
    console.error("❌ Error loading data:", error);
    alert("Failed to load dataset. Please go back to Data Preview.");
  }
};


const analyzeColumns = () => {
  if (!originalDataset.value || originalDataset.value.length === 0) return;

  const firstRow = originalDataset.value[0];
  columns.value = Object.keys(firstRow).map((colName) => {
    const values = originalDataset.value
      .map((row) => row[colName])
      .filter((v) => v !== null && v !== undefined);
    const type = detectColumnType(values);

    return {
      name: colName,
      type: type,
      unique: new Set(values).size,
      missing: originalDataset.value.length - values.length,
      remove: false,
      encode: false,
      encoding: "onehot",
    };
  });

  console.log(`✅ Analyzed ${columns.value.length} columns`);
};

const detectColumnType = (values) => {
  if (values.length === 0) return "categorical";

  const numericCount = values.filter(
    (v) => !isNaN(parseFloat(v)) && isFinite(v)
  ).length;
  const numericRatio = numericCount / values.length;

  return numericRatio > 0.8 ? "numerical" : "categorical";
};

// ==================== SPLIT OPERATIONS ====================

const applySplit = async () => {
  if (isProcessing.value || splitApplied.value) return;

  isProcessing.value = true;
  processingMessage.value = "Splitting dataset...";

  console.log('Sending split request for dataset ID:', mlStore.cleanedDatasetId || mlStore.datasetId);


  try {
    const response = await fetch('http://localhost:8000/api/split-dataset', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      datasetid: datasetId.value,  // Use the verified backend dataset ID
      test_size: 1 - splitRatio.value,
      stratify: splitStrategy.value === 'stratified',
      random_state: randomSeed.value || 42,
    }),
  });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${errorBody.detail || errorBody.message || 'Unknown error'}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      console.log("✅ Split successful");
      console.log(`   Train rows: ${data.train_size}`);
      console.log(`   Test rows: ${data.test_size}`);

      trainRows.value = data.train_size;
      testRows.value = data.test_size;
      trainData.value = data.train_preview || [];
      testData.value = data.test_preview || [];
      splitApplied.value = true;
      currentSplitView.value = 'train';

      mlStore.isSplit = true;
      mlStore.splitInfo = {
        trainRows: data.train_size,
        testRows: data.test_size,
        trainRatio: splitRatio.value,
        testRatio: 1 - splitRatio.value,
      };

      alert(`✅ Dataset Split Applied!\n\nTrain: ${data.train_size.toLocaleString()} rows\nTest: ${data.test_size.toLocaleString()} rows`);
    } else {
      throw new Error(data.message || "Split failed");
    }
  } catch (error) {
    console.error("❌ Split error:", error);
    alert("Error applying split: " + error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = "";
  }
};


const resetSplit = () => {
  if (
    confirm(
      "Are you sure you want to reset the split? This will also reset any scaling applied."
    )
  ) {
    splitApplied.value = false;
    scalingApplied.value = false;
    trainData.value = [];
    testData.value = [];
    trainRows.value = 0;
    testRows.value = 0;
    currentSplitView.value = "full";

    mlStore.isSplit = false;
    mlStore.isScaled = false;

    console.log("🔄 Split reset");
  }
};

// ==================== SCALING OPERATIONS ====================

const applyScaling = async () => {
  if (!splitApplied.value || isProcessing.value || scalingApplied.value) {
    alert("Please apply split first");
    return;
  }

  console.log("\n" + "=".repeat(80));
  console.log("📊 APPLYING FEATURE SCALING");
  console.log("=".repeat(80));

  isProcessing.value = true;
  processingMessage.value = "Scaling features...";

  try {
    const response = await fetch("http://localhost:8000/api/datasets/apply-scaling", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dataset_id: datasetId.value,
        method: scalingMethod.value,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      console.log("✅ Scaling successful");

      trainData.value = data.scaled_train_preview || trainData.value;
      testData.value = data.scaled_test_preview || testData.value;
      scalingApplied.value = true;

      mlStore.isScaled = true;
      mlStore.scalingMethod = scalingMethod.value;

      console.log("=".repeat(80) + "\n");

      alert(
        `✅ Feature Scaling Applied!\n\nMethod: ${scalingMethod.value.toUpperCase()}`
      );
    } else {
      throw new Error(data.error || "Scaling failed");
    }
  } catch (error) {
    console.error("❌ Scaling error:", error);
    alert("Error applying scaling: " + error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = "";
  }
};

const resetScaling = async () => {
  if (
    confirm(
      "Are you sure you want to reset scaling? This will reload the split data without scaling."
    )
  ) {
    scalingApplied.value = false;
    mlStore.isScaled = false;

    await applySplit();

    console.log("🔄 Scaling reset");
  }
};

// ==================== EXPORT FUNCTION ====================

const exportData = async () => {
  console.log("🔄 Starting data export...");

  let dataToExport = [];
  let filename = "";

  if (currentSplitView.value === "train" && splitApplied.value) {
    dataToExport = trainData.value;
    filename = `${fileName.value.replace(".csv", "")}_train.csv`;
  } else if (currentSplitView.value === "test" && splitApplied.value) {
    dataToExport = testData.value;
    filename = `${fileName.value.replace(".csv", "")}_test.csv`;
  } else {
    dataToExport = originalDataset.value;
    filename = fileName.value;
  }

  if (dataToExport.length === 0) {
    alert("No data to export");
    return;
  }

  try {
    const headers = visibleColumns.value.join(",");
    const rows = dataToExport.map((row) =>
      visibleColumns.value
        .map((col) => JSON.stringify(row[col] ?? ""))
        .join(",")
    );
    const csv = [headers, ...rows].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);

    console.log(`✅ Exported ${dataToExport.length} rows to ${filename}`);
  } catch (error) {
    console.error("❌ Export failed:", error);
    alert(`Export failed: ${error.message}`);
  }
};


async function applyCategoricalEncoding() {
  const columnsToEncode = categoricalColumns.value
    .filter(col => col.encode)
    .map(col => ({
      name: col.name,
      method: col.encoding || 'onehot'
    }));

  if (columnsToEncode.length === 0) {
    alert('Please select at least one categorical column for encoding.');
    return;
  }

  // POST to backend - adapt this to your splitting/scaling pipeline as needed
  const response = await fetch('http://localhost:8000/api/apply-categorical-encoding', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    dataset_id: datasetId.value,
    columns: [
      { name: 'Category_B', method: 'onehot' },
      { name: 'Category_C', method: 'label' },
      { name: 'Category_D', method: 'ordinal' }
    ]
  })
});

  const data = await response.json();
  if (data.success) {
    trainData.value = data.train_preview;
    testData.value = data.test_preview;
    alert('Categorical encoding applied!');
    // Refresh table, preview, columns, etc. here as needed
  } else {
    alert('Encoding failed: ' + (data.detail || data.message));
  }
}




// ==================== NAVIGATION ====================

const goBack = () => {
  router.push("/target-selection");
};

const proceedToModelTraining = () => {
  if (!splitApplied.value) {
    alert("Please apply dataset splitting before proceeding");
    return;
  }

  localStorage.setItem(
    "advancedPreprocessing",
    JSON.stringify({
      splitApplied: splitApplied.value,
      scalingApplied: scalingApplied.value,
      splitRatio: splitRatio.value,
      scalingMethod: scalingMethod.value,
      trainRows: trainRows.value,
      testRows: testRows.value,
    })
  );

  router.push("/algo-selection");
};

const resetAllTransformations = () => {
  if (
    confirm(
      "Are you sure you want to reset all transformations? This will clear all splits and scaling."
    )
  ) {
    resetSplit();
    console.log("🔄 All transformations reset");
  }
};

// ==================== LIFECYCLE ====================

onMounted(async () => {
  await loadInitialData();

  console.log('✅ Advanced Preprocessing page initialized');
  console.log({
    backendConnected: mlStore.backendConnected,
    datasetId: datasetId.value,
    previewRows: originalDataset.value.length,
    backendTotalRows: totalRowsInBackend.value,
    columns: columns.value.length,
    targetName: selectedTarget.value,
  });
});


// ==================== WATCHERS ====================

watch(pageSize, () => {
  currentPage.value = 1;
});

watch(searchQuery, () => {
  currentPage.value = 1;
});

watch(currentSplitView, () => {
  currentPage.value = 1;
});
</script>




<style scoped>
/* Complete CSS*/

/* Base Styles - Dark Theme */
.data-preview {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

/* Navigation Header */
.preview-header {
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
  font-size: 0.875rem;
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
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-section p {
  font-size: 1.25rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.dataset-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  font-size: 1rem;
  flex-wrap: wrap;
}

.summary-item {
  color: #ffffff;
}

.summary-divider {
  color: #667eea;
}

.quality-indicator {
  margin-left: 1rem;
}

.quality-score {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
}

.quality-score.excellent {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.quality-score.good {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.quality-score.fair {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.quality-score.poor {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* Section Headers */
.section-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

.section-description {
  font-size: 1rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.6;
}

/* Table Preview Section */
.table-preview-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.preview-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.preview-toggle {
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #b3b3d1;
  font-weight: 500;
}

.preview-toggle.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

.preview-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.data-stats {
  display: flex;
  gap: 1rem;
  margin-left: auto;
}

.data-stats .stat {
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Table Container */
.table-container {
  margin-top: 1.5rem;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  flex-wrap: wrap;
  gap: 1rem;
}

.table-info {
  color: #b3b3d1;
  font-weight: 500;
  font-size: 0.875rem;
}

.toolbar-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box svg {
  position: absolute;
  left: 12px;
  color: #b3b3d1;
  z-index: 2;
}

.search-input {
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.875rem;
  width: 250px;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.15);
}

.search-input::placeholder {
  color: #b3b3d1;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.export-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Data Table */
.data-table-wrapper {
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  overflow: auto; /* Change from hidden to auto */
  max-height: 600px;
  width: 100%;
  /* Add horizontal scrolling */
  overflow-x: auto;
  overflow-y: auto;
}

.data-table {
  width: 100%;
  min-width: fit-content; /* Allow table to grow wider than container */
  border-collapse: collapse;
  font-size: 0.875rem;
}

.table-header-cell,
.table-cell {
  white-space: nowrap; /* Prevent text wrapping */
  padding: 0.75rem 1rem; /* Increased padding for better readability */
  min-width: 120px; /* Minimum column width */
}

.data-table-wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.data-table-wrapper::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
}

.data-table-wrapper::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

.data-table-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sort-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #b3b3d1;
  opacity: 0.7;
  transition: opacity 0.2s ease;
  padding: 0.25rem;
}

.sort-button:hover {
  opacity: 1;
}

.table-row {
  transition: background 0.2s ease;
}

.table-row:hover {
  background: rgba(102, 126, 234, 0.05);
}

.table-row:nth-child(even) {
  background: rgba(255, 255, 255, 0.02);
}

.table-row:nth-child(even):hover {
  background: rgba(102, 126, 234, 0.07);
}

.table-cell {
  padding: 0.75rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  color: #b3b3d1;
  max-width: 200px;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.encoded-badge {
  padding: 0.125rem 0.5rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Add this to your existing styles */
.backend-status {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(26, 26, 46, 0.9);
  border-radius: 20px;
  backdrop-filter: blur(10px);
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

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Table Pagination */
.table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  flex-wrap: wrap;
  gap: 1rem;
}

.page-size-select {
  padding: 0.5rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.875rem;
}

.pagination-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.page-btn:hover:not(:disabled) {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #b3b3d1;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.page-number:hover {
  background: rgba(102, 126, 234, 0.2);
  color: #ffffff;
}

.page-number.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

/* Preprocessing Section */
.preprocessing-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.preprocessing-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Preprocessing Tools */
.preprocessing-tool {
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.preprocessing-tool:hover {
  background: rgba(102, 126, 234, 0.08);
  border-color: rgba(102, 126, 234, 0.3);
}

.preprocessing-tool.active {
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.15),
    rgba(118, 75, 162, 0.15)
  );
  border-color: #667eea;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.tool-info {
  flex: 1;
}

.tool-info h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.tool-info p {
  font-size: 0.9rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.5;
}

.tool-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.tool-badge {
  padding: 0.375rem 0.75rem;
  background: rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 500;
}

.tool-btn {
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  min-width: 80px;
}

.tool-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.tool-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

/* Processing Status Styles */
.processing-status {
  flex: 1;
}

.processing-complete {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.processing-original {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.original-icon {
  font-size: 2rem;
}

.original-text h3 {
  margin: 0 0 0.25rem 0;
  color: #667eea;
  font-size: 1.25rem;
  font-weight: 600;
}

.original-text p {
  margin: 0;
  color: #b3b3d1;
  font-size: 0.9rem;
}

.success-text h3 {
  margin: 0 0 0.25rem 0;
  color: #10b981;
  font-size: 1.25rem;
  font-weight: 600;
}

.success-text p {
  margin: 0;
  color: #b3b3d1;
  font-size: 0.9rem;
}

.tool-config {
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  padding-top: 1.5rem;
  margin-top: 1.5rem;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.config-header h4 {
  margin: 0;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
}

.config-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.action-link {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.action-link:hover {
  color: #764ba2;
}

.action-link.danger {
  color: #ef4444;
}

.action-link.danger:hover {
  color: #dc2626;
}

.action-btn.small {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.action-btn.small:hover {
  background: rgba(102, 126, 234, 0.3);
  border-color: #667eea;
}

/* Missing Values Configuration */
.missing-columns-config {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.global-strategy-selector {
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.global-strategy-label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.global-strategy-label span {
  font-size: 0.875rem;
  color: #b3b3d1;
  font-weight: 500;
}

.strategy-select {
  padding: 0.75rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
}

.strategy-select:focus {
  outline: none;
  border-color: #667eea;
}

/* Missing Columns List */
.missing-columns-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 500px;
  overflow-y: auto;
  padding: 0.5rem;
}

.missing-column-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.25rem;
  background: rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.missing-column-row:hover {
  background: rgba(102, 126, 234, 0.12);
  border-color: rgba(102, 126, 234, 0.4);
}

/* Column Info Section */
.column-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.column-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.column-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 1rem;
}

.column-type {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.column-type.numerical {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.column-type.categorical {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.missing-stats {
  display: flex;
  gap: 0.5rem;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.stat-badge.missing {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

/* Strategy Selector Section */
.strategy-selector-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.column-strategy-select {
  padding: 0.75rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.column-strategy-select:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(26, 26, 46, 1);
}

.column-strategy-select.strategy-drop {
  border-color: rgba(239, 68, 68, 0.5);
}

.column-strategy-select.strategy-fill {
  border-color: rgba(16, 185, 129, 0.5);
}

.column-strategy-select.strategy-keep {
  border-color: rgba(245, 158, 11, 0.5);
}

.strategy-hint {
  font-size: 0.75rem;
  color: #9ca3af;
  font-style: italic;
}

/* Missing Summary */
.missing-summary {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.summary-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

.summary-stat {
  color: #b3b3d1;
  font-size: 0.9rem;
}

.summary-stat strong {
  color: #ffffff;
  font-weight: 700;
}

.summary-divider {
  color: #667eea;
}

/* No Missing Values */
.no-missing-values {
  text-align: center;
  padding: 3rem 2rem;
}

.no-missing-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-missing-values h4 {
  margin: 0 0 0.5rem 0;
  color: #10b981;
  font-size: 1.5rem;
  font-weight: 600;
}

.no-missing-values p {
  margin: 0;
  color: #b3b3d1;
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .missing-column-row {
    flex-direction: column;
    align-items: stretch;
  }

  .global-strategy-selector {
    padding: 0.75rem;
  }
}

/* Columns Grid */
.columns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem;
}

.column-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.column-card:hover {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.4);
}

.column-card.to-remove {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.column-card.to-remove:hover {
  background: rgba(239, 68, 68, 0.15);
}

.column-card input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #667eea;
  margin-top: 0.25rem;
}

.column-content {
  flex: 1;
}

.column-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.column-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.9rem;
}

/* Selected Column Card Styling */
.column-card.selected {
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.column-card.selected .column-name {
  color: #10b981;
  font-weight: 600;
}

.column-type {
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.column-type.numerical {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.column-type.categorical {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.remove-badge {
  padding: 0.125rem 0.5rem;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.column-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.stat-item {
  font-size: 0.75rem;
  color: #b3b3d1;
}

.stat-item.missing {
  color: #f59e0b;
}

.column-sample {
  margin-top: 0.5rem;
}

.sample-label {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-right: 0.5rem;
}

.sample-text {
  font-size: 0.75rem;
  color: #b3b3d1;
  font-style: italic;
}

.ratio-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  color: #e5e5e5;
}

.ratio-label strong {
  color: #667eea;
  font-size: 1.1rem;
}

.ratio-info {
  color: #b3b3d1;
}

.ratio-slider {
  width: 100%;
  height: 8px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 5px;
  outline: none;
  cursor: pointer;
}

.ratio-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.5);
}

.quick-ratios {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.quick-ratio-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #b3b3d1;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.quick-ratio-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.quick-ratio-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

.preview-box {
  flex: 1;
  padding: 1.5rem;
  border-radius: 12px;
  background: rgba(102, 126, 234, 0.05);
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.preview-box.train {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.3);
}

.preview-box.test {
  background: rgba(245, 158, 11, 0.05);
  border-color: rgba(245, 158, 11, 0.3);
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.preview-icon {
  font-size: 1.5rem;
}

.preview-label {
  font-weight: 600;
  color: #ffffff;
}

.preview-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preview-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.preview-box.train .preview-percentage {
  color: #10b981;
}

.preview-box.test .preview-percentage {
  color: #f59e0b;
}

.preview-rows {
  font-size: 0.9rem;
  color: #b3b3d1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left .section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.header-left .section-description {
  color: #6b7280;
  margin: 0;
  font-size: 0.95rem;
}

.badge-type.type-classification {
  background: #dbeafe;
  color: #1e40af;
}

.badge-type.type-regression {
  background: #fef3c7;
  color: #92400e;
}

/* Info Box */
.info-box {
  display: flex;
  gap: 12px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.info-box svg {
  flex-shrink: 0;
  color: #3b82f6;
}

.info-text strong {
  display: block;
  margin-bottom: 8px;
  color: #1e40af;
}

.info-text p {
  margin: 4px 0;
  color: #1e3a8a;
  font-size: 0.9rem;
}

.info-text ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.info-text li {
  color: #1e3a8a;
  margin: 4px 0;
}

/* Columns Grid */
.columns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.column-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.column-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.column-icon {
  display: flex;
  color: #6b7280;
}

.column-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.95rem;
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.column-type-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-numerical {
  background: #dbeafe;
  color: #1e40af;
}

.badge-categorical {
  background: #fce7f3;
  color: #9f1239;
}

.column-unique {
  font-size: 0.75rem;
  color: #9ca3af;
}

.selected-card {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 2px solid #86efac;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  gap: 20px;
  max-width: 600px;
  width: 100%;
}

.selected-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: #22c55e;
  border-radius: 50%;
  flex-shrink: 0;
}

.selected-icon svg {
  color: white;
}

.selected-info {
  flex: 1;
}

.selected-info h3 {
  margin: 0 0 12px 0;
  color: #166534;
  font-size: 1.1rem;
}

.selected-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.detail-item {
  display: flex;
  gap: 8px;
}

.detail-label {
  font-weight: 500;
  color: #15803d;
  font-size: 0.875rem;
}

.detail-value {
  color: #166534;
  font-weight: 600;
  font-size: 0.875rem;
}

.capitalize {
  text-transform: capitalize;
}

.selected-actions {
  display: flex;
  align-items: center;
}

.required-badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 12px;
  margin-left: 8px;
  font-weight: 600;
}

.toolkit-header {
  margin-bottom: 2rem;
}

.toolkit-description {
  font-size: 1rem;
  color: #b3b3d1;
  margin: 0.5rem 0 0 0;
  line-height: 1.6;
}

.preprocessing-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.preprocessing-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.tool-badge.success {
  background: rgba(16, 185, 129, 0.3);
  color: #10b981;
  font-weight: 600;
}

.range-input-wrapper {
  margin-top: 12px;
}

.range-slider {
  width: 100%;
  height: 6px;
  background: linear-gradient(to right, #e0e0e0 0%, #e0e0e0 100%);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #667eea;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.range-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #667eea;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: none;
}

.range-slider:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.range-values {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}

.value-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
}

.value-badge.train {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.value-badge.test {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: rgba(26, 26, 46, 0.8);
  color: #ffffff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
}

.form-input::placeholder {
  color: #b3b3d1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.train {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.test {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.total {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.85rem;
  color: #757575;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212121;
}

.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.alert-warning {
  background: #fff3cd;
  border: 1px solid #ffecb5;
  color: #856404;
}

.info-panel {
  margin-top: 20px;
  padding: 20px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.info-panel.success {
  background: rgba(16, 185, 129, 0.1);
  border-left-color: #10b981;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.info-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

.info-text {
  font-size: 0.95rem;
  color: #b3b3d1;
  line-height: 1.6;
}

.preprocessing-tool.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.config-section.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;
  margin-bottom: 0.75rem;
}

.form-select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.form-select:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(26, 26, 46, 1);
}

.form-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.help-text {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #9ca3af;
  line-height: 1.4;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 0.95rem;
}

.btn-apply {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  align-items: center;
}

.btn-apply:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.btn-apply:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reset {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.btn-reset:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.clean-section {
  margin-top: 28px;
  margin-bottom: 15px;
  padding-bottom: 6px;
  border-bottom: 1px solid #22223b4d;
}

.clean-label {
  font-size: 1rem;
  font-weight: 500;
  color: #e0e7ef;
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 5px;
}

.optional {
  color: #94a3b8;
  font-size: 13px;
  margin-left: 8px;
}

.split-slider-row {
  display: flex;
  align-items: center;
  gap: 18px;
  margin: 12px 0 6px 0;
}
.split-slider {
  flex: 1;
  accent-color: #3b82f6;
}
.slider-label {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  background: #1e40af;
  color: #b9e0ff;
  min-width: 80px;
  display: inline-block;
  text-align: center;
}
.slider-label.test {
  background: #be123c;
  color: #fff0f5;
}

.split-ratio-badges {
  display: flex;
  gap: 10px;
  margin-bottom: 0;
}
.ratio-badge {
  font-size: 13px;
  background: #22223b;
  color: #6ea8fe;
  border-radius: 7px;
  padding: 3px 14px;
}
.ratio-badge.train {
  background: #182c49;
  color: #85d2ff;
}
.ratio-badge.test {
  background: #4b1a29;
  color: #ff8fa3;
}

.clean-select,
.clean-input {
  width: 100%;
  background: #191b2c;
  color: #e0e7ef;
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  margin-top: 7px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s;
}
.clean-input:focus,
.clean-select:focus {
  border: 1px solid #3b82f6;
}
.split-help {
  margin: 6px 0 0 0;
  color: #88a2b7;
  font-size: 13px;
}
.split-action-row {
  display: flex;
  gap: 20px;
  margin: 18px 0 12px 0;
}

.range-input-wrapper {
  margin-top: 12px;
}

.range-slider {
  width: 100%;
  height: 6px;
  background: linear-gradient(to right, #e0e0e0 0%, #e0e0e0 100%);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #667eea;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.range-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #667eea;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: none;
}

.range-slider:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.range-values {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}

.value-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
}

.value-badge.train {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.value-badge.test {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.train {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.test {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.total {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.85rem;
  color: #757575;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212121;
}

.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.alert-warning {
  background: #fff3cd;
  border: 1px solid #ffecb5;
  color: #856404;
}

.info-panel {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.info-panel.success {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.info-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #212121;
}

.info-text {
  font-size: 0.95rem;
  color: #424242;
  line-height: 1.6;
}

.preprocessing-card.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.config-section.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.change-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #86efac;
  border-radius: 6px;
  color: #15803d;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.change-btn:hover {
  background: #f0fdf4;
  border-color: #22c55e;
}

.complete-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #10b981;
}

.complete-header h5 {
  margin: 0;
  font-size: 1.1rem;
}

.complete-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.stat-row span {
  color: #b3b3d1;
}

.stat-row strong {
  color: #ffffff;
}

.apply-scaling-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1.5rem;
}

.apply-scaling-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.apply-scaling-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.config-warning {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 8px;
  color: #f59e0b;
  margin-bottom: 1.5rem;
}

.preprocessing-tool.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.tool-badge.success {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.tool-badge.warning {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

/* ⚠️ WARNING MODAL STYLES */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: linear-gradient(135deg, #1a1a2e, #2d2d44);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.3s ease;
}

.modal-header {
  padding: 2rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-header.warning {
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.1),
    rgba(217, 119, 6, 0.1)
  );
}

.warning-icon {
  font-size: 2.5rem;
  line-height: 1;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #f59e0b;
}

.modal-body {
  padding: 2rem;
}

.warning-message {
  font-size: 1rem;
  line-height: 1.6;
  color: #e5e5e5;
  margin-bottom: 1.5rem;
}

.warning-message strong {
  color: #f59e0b;
}

.warning-details {
  background: rgba(245, 158, 11, 0.05);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.9rem;
}

.detail-item strong {
  color: #ffffff;
}

.detail-item span {
  color: #b3b3d1;
}

.warning-note {
  font-size: 0.875rem;
  color: #b3b3d1;
  background: rgba(102, 126, 234, 0.05);
  border-left: 3px solid #667eea;
  padding: 1rem;
  border-radius: 4px;
  margin: 0;
}

.warning-note strong {
  color: #667eea;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-warning {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
}

.btn-warning:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Selection Summary */
.selection-summary {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
}

.summary-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.summary-stat {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.summary-stat.keep {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.summary-stat.remove {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.removal-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.removal-label {
  font-size: 0.875rem;
  color: #b3b3d1;
  font-weight: 500;
}

.removal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.removal-tag {
  padding: 0.25rem 0.75rem;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Expanded state for tools */
.preprocessing-tool.expanded {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
  border-color: #667eea;
}

/* Configure button */
.config-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.config-btn:hover,
.config-btn.active {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Dropdown footer */
.dropdown-footer {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  justify-content: center;
}

.close-dropdown-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.close-dropdown-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Change item actions */
.change-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
}

.change-edit-btn,
.change-remove-btn {
  padding: 0.375rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.change-edit-btn {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.change-edit-btn:hover {
  background: rgba(102, 126, 234, 0.3);
}

.change-remove-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.change-remove-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.reset-btn.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

/* Strategy Selector */
.strategy-selector {
  margin-bottom: 1.5rem;
}

.strategy-selector h4 {
  margin: 0 0 1.5rem 0;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
}

.strategy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.strategy-card {
  display: block;
  cursor: pointer;
  transition: all 0.3s ease;
}

.strategy-card input[type="radio"] {
  display: none;
}

.strategy-content {
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}

.strategy-card:hover .strategy-content {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.strategy-card.selected .strategy-content {
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.3),
    rgba(118, 75, 162, 0.3)
  );
  border-color: #667eea;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.strategy-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: block;
}

.strategy-content h5 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.strategy-content p {
  font-size: 0.875rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.4;
}

/* ========== CONFIG GROUPS ========== */
.config-group {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
}

.config-group:last-of-type {
  border-bottom: none;
}

/* ========== LABELS ========== */
.config-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e0e7ef;
  margin-bottom: 1rem;
}

.config-label svg {
  color: #667eea;
  flex-shrink: 0;
}

.optional-tag {
  display: inline-block;
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: 0.5rem;
}

.backend-warning {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 8px;
  color: #f59e0b;
  margin: 1rem 2rem;
}

.backend-warning svg {
  flex-shrink: 0;
}

.backend-warning strong {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 1rem;
}

.backend-warning p {
  margin: 0;
  font-size: 0.875rem;
  color: #b3b3d1;
}


/* ========== RATIO DISPLAY ========== */
.ratio-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.ratio-badge-large {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem 1rem;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.1));
  border: 2px solid rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.ratio-badge-large.train {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.15));
  border-color: rgba(102, 126, 234, 0.4);
}

.ratio-badge-large.test {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.15));
  border-color: rgba(239, 68, 68, 0.4);
}

.ratio-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.ratio-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #b3b3d1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ratio-separator {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  opacity: 0.6;
}

/* ========== SLIDER ========== */
.slider-container {
  position: relative;
  margin-bottom: 1rem;
}

.split-slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 10px;
  outline: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.split-slider:hover:not(:disabled) {
  background: rgba(102, 126, 234, 0.3);
}

.split-slider:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.split-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.2s ease;
}

.split-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

.split-slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  border: none;
  transition: all 0.2s ease;
}

.split-slider::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

/* ========== QUICK RATIOS ========== */
.quick-ratios {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.quick-ratio-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #b3b3d1;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-ratio-btn:hover:not(:disabled) {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
  color: #ffffff;
  transform: translateY(-1px);
}

.quick-ratio-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.quick-ratio-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ========== SELECT & INPUT ========== */
.config-select,
.config-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 10px;
  color: #e0e7ef;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.2s ease;
}

.config-select:focus,
.config-input:focus {
  border-color: #667eea;
  background: rgba(26, 26, 46, 0.8);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.config-select:disabled,
.config-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.config-input::placeholder {
  color: #6b7280;
}

/* ========== HELP TEXT ========== */
.config-help {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.05);
  border-left: 3px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #94a3b8;
  font-size: 0.85rem;
  line-height: 1.5;
}

.config-help svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: #667eea;
}

/* ========== ACTION BUTTONS ========== */
.config-actions {
  display: flex;
  justify-content: center; /* Center when single button */
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(102, 126, 234, 0.15);
}

/* When multiple buttons, space them out */
.config-actions:has(.btn-reset) {
  justify-content: space-between;
}

/* ========== SPLIT SUMMARY ========== */
.split-summary {
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.summary-header svg {
  color: #10b981;
}

.summary-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #10b981;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  flex-shrink: 0;
}

.stat-box.train .stat-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-box.test .stat-icon {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.stat-box.total .stat-icon {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.stat-icon svg {
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #b3b3d1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ========== TOOL DESCRIPTION ========== */
.tool-description {
  font-size: 0.9rem;
  color: #94a3b8;
  margin: 0.25rem 0 0 0;
  line-height: 1.4;
}

/* Encoding Configuration */
.encoding-config h4 {
  margin: 0 0 1.5rem 0;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
}

.encoding-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.encoding-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  gap: 1rem;
}

.column-details {
  flex: 1;
}

.encoding-row .column-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 0.25rem;
}

.column-info {
  font-size: 0.75rem;
  color: #b3b3d1;
  margin-bottom: 0.5rem;
}

.encoding-row .sample-values {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.encoding-row .sample-label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.encoding-row .sample-text {
  font-size: 0.75rem;
  color: #b3b3d1;
  font-style: italic;
}

.encoding-selector {
  flex-shrink: 0;
}

.encoding-select {
  padding: 0.5rem 0.75rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.875rem;
  min-width: 160px;
}

.encoding-select:focus {
  outline: none;
  border-color: #667eea;
}

/* Apply Section */
.apply-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
}

.apply-summary {
  margin-bottom: 2rem;
}

.apply-summary h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.changes-preview {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.change-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
}

.change-icon {
  color: #10b981;
  font-weight: bold;
}

.change-text {
  color: #34d399;
  font-weight: 500;
  flex: 1;
}

.change-config {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.apply-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.reset-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.apply-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apply-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.apply-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.apply-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.apply-btn.loading {
  opacity: 0.8;
  cursor: wait;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Action Footer */
.action-footer {
  background: rgba(26, 26, 46, 0.9);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  padding: 2rem;
  position: sticky;
  bottom: 0;
  z-index: 50;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
}

.processing-complete {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.success-icon {
  font-size: 2rem;
}

.success-text h3 {
  margin: 0 0 0.25rem 0;
  color: #10b981;
  font-size: 1.25rem;
  font-weight: 600;
}

.success-text p {
  margin: 0;
  color: #b3b3d1;
  font-size: 0.9rem;
}

.final-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #b3b3d1;
}

.footer-actions {
  display: flex;
  gap: 1rem;
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

.footer-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  animation: pulse 2s infinite;
  min-width: 200px;
  justify-content: center;
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

.footer-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
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

.skip-section {
  margin-top: 2rem;
  padding: 2rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px dashed rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  text-align: center;
}

.skip-content h3 {
  margin: 0 0 1rem 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.skip-content p {
  margin: 0 0 1.5rem 0;
  color: #b3b3d1;
  font-size: 1rem;
  line-height: 1.5;
}

.skip-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.4);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.skip-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  border-color: #667eea;
  transform: translateY(-1px);
}

.reset-tool-btn {
  padding: 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-tool-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.encoding-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
  cursor: pointer;
}

.encoding-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 0.25rem;
}

.not-encoded {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 6px;
  flex-shrink: 0;
}

.not-encoded-text {
  font-size: 0.875rem;
  color: #b3b3d1;
  font-style: italic;
}

.encoding-actions {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
}

/* âœ… ADD THESE STYLES TO YOUR EXISTING CSS */

.backend-status {
  position: relative;
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

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  color: white;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-content p {
  font-size: 1.125rem;
  font-weight: 500;
  margin: 0;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .main-container {
    padding: 1.5rem;
  }

  .hero-section {
    padding: 2rem 1.5rem;
  }

  .hero-section h1 {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 1rem;
  }

  .hero-section {
    padding: 1.5rem 1rem;
  }

  .hero-section h1 {
    font-size: 2rem;
  }

  .dataset-summary {
    flex-direction: column;
    gap: 1rem;
  }

  .preview-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .data-stats {
    margin-left: 0;
    justify-content: center;
  }

  .table-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-right {
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }

  .tool-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .tool-actions {
    justify-content: space-between;
  }

  .config-header {
    flex-direction: column;
    align-items: stretch;
  }

  .config-actions {
    justify-content: center;
    align-items: center;
  }

  .columns-grid {
    grid-template-columns: 1fr;
  }

  .strategy-grid {
    grid-template-columns: 1fr;
  }

  .encoding-row {
    flex-direction: column;
    align-items: stretch;
  }

  .apply-buttons {
    flex-direction: column;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .final-stats {
    justify-content: center;
  }

  .footer-actions {
    justify-content: center;
  }

  .table-pagination {
    flex-direction: column;
    gap: 1rem;
  }

  .pagination-controls {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .hero-section h1 {
    font-size: 1.75rem;
  }

  .final-stats {
    flex-direction: column;
    gap: 1rem;
  }

  .page-numbers {
    flex-wrap: wrap;
    justify-content: center;
  }

  .preprocessing-tool {
    padding: 1rem;
  }

  .tool-config {
    padding-top: 1rem;
    margin-top: 1rem;
  }
}

/* Custom Scrollbars */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

/* Selection Styles */
::selection {
  background: rgba(102, 126, 234, 0.3);
  color: white;
}

::-moz-selection {
  background: rgba(102, 126, 234, 0.3);
  color: white;
}
</style>
