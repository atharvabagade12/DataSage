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
    <section class="hero-section">
      <div class="hero-content">
        <!-- Centered Header -->
        <div class="hero-header-centered">
          <h1 class="gradient-text">Advanced Preprocessing</h1>
          <p class="hero-subtitle">Split, scale, and engineer features for optimal model training</p>
        </div>
        
        <!-- Stats Grid -->
        <div class="dataset-summary">
          <div class="summary-stat">
            <svg class="stat-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Dataset</span>
              <span class="stat-value" :title="fileName">{{ fileName }}</span>
            </div>
          </div>
          
          <div class="summary-stat">
            <svg class="stat-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M3,3H21V21H3V3M5,5V19H19V5H5M7,7H17V9H7V7M7,11H17V13H7V11M7,15H17V17H7V15Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Rows</span>
              <span class="stat-value" v-if="!splitApplied">{{ totalRows.toLocaleString() }}</span>
              <span class="stat-value" v-else>
                {{ (trainRows + testRows).toLocaleString() }}
                <span v-if="smoteApplied" style="color: #10b981; font-size: 0.85em;"> (+{{ (trainRows - Math.floor(totalRows * splitRatio)).toLocaleString() }})</span>
              </span>
            </div>
          </div>
          
          <div class="summary-stat">
            <svg class="stat-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2,2H8V4H16V2H22V8H20V16H22V22H16V20H8V22H2V16H4V8H2V2M16,8V6H8V8H6V16H8V18H16V16H18V8H16M4,4V6H6V4H4M18,4V6H20V4H18M4,18V20H6V18H4M18,18V20H20V18H18Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Columns</span>
              <span class="stat-value">{{ totalColumns }}</span>
            </div>
          </div>
          
          <div class="summary-stat">
            <svg class="stat-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Target Variable</span>
              <span class="stat-value">{{ selectedTarget || 'Not Set' }}</span>
            </div>
          </div>
          
          
        </div>
      </div>
    </section>

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
              <span class="stat">{{ totalColumns }} columns</span>
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
                        v-if="scaledColumns.has(column)"
                        class="encoded-badge"
                        >Scaled</span
                      >
                      <span
                        v-if="targetEncodedColumns.has(column)"
                        class="encoded-badge"
                        style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; border-color: rgba(139, 92, 246, 0.2);"
                        >Target Encoded</span
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
          <Card class="preprocessing-tool-card" hover>
            <div class="tool-header">
              <div class="tool-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>Dataset Splitting</h3>
                <p>Split your dataset into train and test sets to prevent data leakage</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': splitApplied }">
                {{ splitApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button variant="primary" @click="showSplitModal = true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                Configure Split
              </Button>
            </div>
          </Card>
          
          <!-- Dataset Splitting Modal -->
          <Modal v-model="showSplitModal" title="Dataset Splitting Configuration" size="xl">
            <div class="modal-section">
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
                  <div class="ratio-card train">
                    <span class="ratio-value">{{ (splitRatio * 100).toFixed(0) }}%</span>
                    <span class="ratio-label">Train Set</span>
                    <span class="ratio-rows">{{ Math.round(totalRows * splitRatio).toLocaleString() }} rows</span>
                  </div>
                  
                  <div class="ratio-visual">
                    <div class="ratio-bar">
                      <div class="ratio-fill train" :style="{ width: (splitRatio * 100) + '%' }"></div>
                      <div class="ratio-fill test" :style="{ width: ((1 - splitRatio) * 100) + '%' }"></div>
                    </div>
                  </div>

                  <div class="ratio-card test">
                    <span class="ratio-value">{{ ((1 - splitRatio) * 100).toFixed(0) }}%</span>
                    <span class="ratio-label">Test Set</span>
                    <span class="ratio-rows">{{ Math.round(totalRows * (1 - splitRatio)).toLocaleString() }} rows</span>
                  </div>
                </div>

                <div class="slider-container">
                  <div class="slider-labels">
                    <span>50%</span>
                    <span>95%</span>
                  </div>
                  <input
                    type="range"
                    min="0.5"
                    max="0.95"
                    step="0.05"
                    v-model.number="splitRatio"
                    :disabled="splitApplied"
                    class="split-slider"
                  />
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
            
            
          </Modal>


          <!-- ========== CARD 2: CATEGORICAL ENCODING ========== -->
          <Card class="preprocessing-tool-card" hover :class="{ disabled: !splitApplied }">
            <div class="tool-header">
              <div class="tool-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>
                  Categorical Encoding
                  <span v-if="!splitApplied" class="requires-split-inline">⚠️ Requires Split</span>
                </h3>
                <p>Convert categorical features to numerical representations for ML algorithms</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': encodingApplied }">
                {{ encodingApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button variant="primary" @click="showEncodingModal = true" :disabled="!splitApplied">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                Configure Encoding
              </Button>
            </div>
          </Card>
          
          <!-- Categorical Encoding Modal -->
          <Modal v-model="showEncodingModal" title="Categorical Encoding Configuration" size="xl">
            <div class="modal-section">
              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                  </svg>
                  Select Columns to Encode
                </label>
                
                <div class="selection-controls">
                  <button @click="selectAllCategoricalColumns" class="btn-secondary small">
                    Select All
                  </button>
                  <button @click="selectRecommendedCategoricalColumns" class="btn-secondary small">
                    Select Recommended
                  </button>
                  <button @click="deselectAllCategoricalColumns" class="btn-secondary small">
                    Deselect All
                  </button>
                </div>

                <div class="encoding-list">
                  <div
                    v-for="column in categoricalColumns.filter(c => c.name !== selectedTarget && !targetEncodedColumns.has(c.name))"
                    :key="column.name"
                    class="encoding-row"
                    :class="{ active: column.encode }"
                  >
                    <div class="col-main-info">
                      <label class="checkbox-label" :class="{ disabled: getEncodingRecommendation(column).method === 'target' }">
                        <input
                          type="checkbox"
                          v-model="column.encode"
                          @change="toggleColumnEncoding(column)"
                          :disabled="getEncodingRecommendation(column).method === 'target'"
                        />
                        <span class="checkbox-custom"></span>
                        <span class="col-name">
                          {{ column.name }}
                          <span class="category-count">({{ column.unique }} categories)</span>
                        </span>
                      </label>

                      <!-- Recommendation Badge -->
                      <div class="recommendation-info">
                        <span 
                          class="rec-badge" 
                          :class="getEncodingRecommendation(column).method"
                        >
                          {{ 
                            getEncodingRecommendation(column).method === 'onehot' ? 'One-Hot' : 
                            getEncodingRecommendation(column).method === 'label' ? 'Label' : 
                            getEncodingRecommendation(column).method === 'target' ? 'Target' : 'Ordinal' 
                          }}
                        </span>
                        <span class="rec-reason">{{ getEncodingRecommendation(column).reason }}</span>
                        <p v-if="getEncodingRecommendation(column).note" class="rec-note" style="color: #8b5cf6; font-weight: 600;">{{ getEncodingRecommendation(column).note }}</p>
                      </div>
                    </div>
                    
                    <div class="encoding-select-wrapper" v-if="column.encode">
                      <select
                        v-model="column.encoding"
                        @change="setEncodingMethod(column.name, column.encoding)"
                        class="encoding-select"
                      >
                        <option value="onehot">One-Hot Encoding</option>
                        <option value="label">Label Encoding</option>
                        <option value="ordinal">Ordinal Encoding</option>
                      </select>
                    </div>
                  </div>
                  
                  <div v-if="categoricalColumns.filter(c => c.name !== selectedTarget && !targetEncodedColumns.has(c.name)).length === 0" class="empty-state">
                    No categorical columns found available for encoding.
                  </div>
                </div>
              </div>

            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showEncodingModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                :loading="isProcessing"
                @click="applyCategoricalEncoding"
                :disabled="categoricalColumns.filter(c => c.name !== selectedTarget && !targetEncodedColumns.has(c.name) && c.encode).length === 0"
              >
                Apply Encoding
              </Button>
            </template>
          </Modal>
          
          <!-- ========== CARD 2.5: TARGET ENCODING (ADVANCED) ========== -->
          <Card class="preprocessing-tool-card" hover :class="{ disabled: !splitApplied || !selectedTarget }">
            <div class="tool-header">
              <div class="tool-icon" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>
                  Target Encoding
                  <span v-if="!splitApplied" class="requires-split-inline">⚠️ Requires Split</span>
                  <span v-else-if="!selectedTarget" class="requires-split-inline">⚠️ Requires Target</span>
                </h3>
                <p>Encode high-cardinality features using target statistics with smoothing</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': targetEncodingApplied }">
                {{ targetEncodingApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button variant="primary" @click="showTargetEncodingModal = true" :disabled="!splitApplied || !selectedTarget">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                Configure Target Encoding
              </Button>
            </div>
          </Card>

          <!-- Target Encoding Modal -->
          <Modal v-model="showTargetEncodingModal" title="Target Encoding Configuration" size="xl">
            <div class="modal-section">
              <div class="info-alert">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                </svg>
                <div>
                  <strong>What is Target Encoding?</strong>
                  <p>Target encoding replaces each category with the average target value for that category. It is highly effective for columns with many unique categories where One-Hot encoding would create too many columns.</p>
                </div>
              </div>

              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z"/>
                  </svg>
                  Select Columns for Target Encoding
                  <span class="help-icon" title="Recommended for columns with >10 unique categories.">ⓘ</span>
                </label>

                <div class="selection-controls">
                  <button @click="selectAllTargetEncoding" class="btn-secondary small">
                    Select All
                  </button>
                  <button @click="selectRecommendedTargetEncoding" class="btn-secondary small">
                    Select Recommended
                  </button>
                  <button @click="deselectAllTargetEncoding" class="btn-secondary small">
                    Deselect All
                  </button>
                </div>
                
                <div class="encoding-list">
                  <div
                    v-for="column in categoricalColumns.filter(c => c.name !== selectedTarget && !targetEncodedColumns.has(c.name))"
                    :key="column.name"
                    class="encoding-row"
                    :class="{ active: column.targetEncode }"
                  >
                    <label class="checkbox-label">
                      <input
                        type="checkbox"
                        v-model="column.targetEncode"
                      />
                      <span class="checkbox-custom"></span>
                      <span class="col-name">
                        {{ column.name }}
                        <span class="category-count">({{ column.unique }} categories)</span>
                      </span>
                    </label>
                    
                    <div class="recommendation-badge" v-if="column.unique > 30">
                      <span class="strongly-rec" title="High cardinality detected. Target encoding is strongly recommended over One-Hot.">🔥 Strongly Recommended</span>
                    </div>
                    <div class="recommendation-badge" v-else-if="column.unique >= 10">
                      <span class="recommended" title="Medium cardinality detected. Target encoding helps prevent overfitting compared to One-Hot.">👍 Recommended</span>
                    </div>
                    <div class="recommendation-badge" v-else-if="column.unique <= 8">
                      <span class="not-recommended" title="Low cardinality detected. One-Hot encoding is generally better for very few categories.">ℹ️ One-Hot may be better</span>
                    </div>
                  </div>

                  <div v-if="categoricalColumns.filter(c => c.name !== selectedTarget && !targetEncodedColumns.has(c.name)).length === 0" class="empty-state">
                    No categorical columns found available for target encoding.
                  </div>
                </div>
              </div>

              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,3L2,12h3v8h14v-8h3L12,3z M12,7.7c1.4,0,2.5,1.1,2.5,2.5S13.4,12.7,12,12.7s-2.5-1.1-2.5-2.5S10.6,7.7,12,7.7z"/>
                  </svg>
                  Smoothing Factor (k)
                  <span class="config-value-badge">{{ targetEncodingSmoothing }}</span>
                </label>
                <div class="slider-container">
                  <input
                    type="range"
                    min="1"
                    max="50"
                    step="1"
                    v-model.number="targetEncodingSmoothing"
                    class="split-slider"
                  />
                  <div class="slider-labels">
                    <span>Low Smoothing (1)</span>
                    <span>High Smoothing (50)</span>
                  </div>
                </div>
                <p class="config-help">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10S17.52,2,12,2zm1,15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                  Higher smoothing pushes rare categories closer to the global average, which prevents overfitting.
                </p>
              </div>

              <div class="leakage-warning">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 16h2v2h-2zm0-6h2v4h-2z"/>
                </svg>
                <span><strong>Anti-Leakage Protection:</strong> Statistics are calculated only on the Training Set and then mapped to the Test Set.</span>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showTargetEncodingModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                :loading="isProcessing"
                @click="applyTargetEncoding"
                :disabled="!categoricalColumns.some(c => c.targetEncode)"
              >
                Apply Target Encoding
              </Button>
            </template>
          </Modal>

          <!-- ========== CARD 3: FEATURE SCALING ========== -->
          <Card class="preprocessing-tool-card" hover :class="{ disabled: !splitApplied }">
            <div class="tool-header">
              <div class="tool-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>
                  Feature Scaling
                  <span v-if="!splitApplied" class="requires-split-inline">⚠️ Requires Split</span>
                </h3>
                <p>Normalize numerical features for better model performance</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': scalingApplied }">
                {{ scalingApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button variant="primary" @click="showScalingModal = true" :disabled="!splitApplied">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                Configure Scaling
              </Button>
            </div>
          </Card>
          
          <!-- Feature Scaling Modal -->
          <Modal v-model="showScalingModal" title="Feature Scaling Configuration" size="xl">
            <div class="modal-section">
              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                  </svg>
                  Select Columns to Scale
                </label>
                
                <div class="selection-controls">
                  <button @click="selectAllNumericalColumns" class="btn-secondary small">
                    Select All
                  </button>
                  <button @click="deselectAllNumericalColumns" class="btn-secondary small">
                    Deselect All
                  </button>
                </div>

                <div class="encoding-list">
                  <div
                    v-for="col in numericalColumns"
                    :key="col.name"
                    class="encoding-row"
                    :class="{ active: col.scale }"
                  >
                    <label class="checkbox-label">
                      <input
                        type="checkbox"
                        v-model="col.scale"
                        @change="toggleColumnScaling(col)"
                      />
                      <span class="checkbox-custom"></span>
                      <span class="col-name">
                        {{ col.name }}
                        <span v-if="col.isAlreadyScaled" class="requires-split-inline" style="margin-left: 8px; font-size: 0.7rem;">Scaled</span>
                      </span>
                    </label>

                    <div class="recommendation-info scaling-rec">
                      <span 
                        class="rec-badge" 
                        :class="getScalingRecommendation(col).method"
                      >
                        {{ 
                          getScalingRecommendation(col).method === 'standard' ? 'Standard' : 
                          getScalingRecommendation(col).method === 'robust' ? 'Robust' : 
                          getScalingRecommendation(col).method === 'minmax' ? 'MinMax' : 'MaxAbs' 
                        }}
                      </span>
                      <span class="rec-reason">{{ getScalingRecommendation(col).reason }}</span>
                    </div>
                    
                    <div class="encoding-select-wrapper" v-if="col.scale">
                      <select
                        v-model="col.scalingMethod"
                        class="encoding-select"
                      >
                        <option value="standard">StandardScaler</option>
                        <option value="minmax">MinMaxScaler</option>
                        <option value="robust">RobustScaler</option>
                        <option value="maxabs">MaxAbsScaler</option>
                      </select>
                    </div>
                  </div>
                  
                  <div v-if="numericalColumns.length === 0" class="empty-state">
                    No numerical columns available for scaling.
                  </div>
                </div>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showScalingModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                :loading="isProcessing"
                @click="applyScaling"
                :disabled="!splitApplied || !numericalColumns.some(col => col.scale)"
              >
                Apply Scaling
              </Button>
            </template>
          </Modal>

          <!-- ========== CARD 4: SMOTE ANALYSIS ========== -->
          <Card 
            class="preprocessing-tool-card" 
            hover 
            :class="{ disabled: !splitApplied || (!hasClassImbalance && !smoteApplied) }"
            v-if="problemType === 'classification'"
          >
            <div class="tool-header">
              <div class="tool-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>
                  SMOTE Analysis
                  <span v-if="!splitApplied" class="requires-split-inline">⚠️ Requires Split</span>
                  <span v-else-if="smoteApplied && !hasClassImbalance" class="balanced-badge">✓ Applied & Balanced</span>
                  <span v-else-if="!hasClassImbalance && splitApplied" class="balanced-badge">✓ Balanced (IR < 3.0)</span>
                  <span v-else-if="hasClassImbalance && imbalanceSeverity === 'mild'" class="imbalance-badge-mild">
                    ⚠️ Mild Imbalance: {{ imbalanceRatio.toFixed(2) }}x
                  </span>
                  <span v-else-if="hasClassImbalance && imbalanceSeverity === 'severe'" class="imbalance-badge-severe">
                    ⚠️ Severe Imbalance: {{ imbalanceRatio.toFixed(2) }}x
                  </span>
                </h3>
                <p>Balance class distribution using synthetic minority oversampling</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': smoteApplied }">
                {{ smoteApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button 
                variant="primary" 
                @click="showSmoteModal = true" 
                :disabled="!splitApplied || (!hasClassImbalance && !smoteApplied)"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                {{ smoteApplied ? 'View SMOTE Details' : 'Configure SMOTE' }}
              </Button>
            </div>
          </Card>
          
          <!-- SMOTE Configuration Modal -->
          <Modal v-model="showSmoteModal" title="SMOTE Configuration" size="xl">
            <div class="modal-section">
              <!-- Class Distribution Display -->
              <div class="config-group" v-if="classDistribution && Object.keys(classDistribution).length > 0">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                  </svg>
                  Current Class Distribution
                </label>
                
                <!-- SMOTE Validation Warning -->
                <div v-if="!smoteValidation.valid" class="leakage-warning" style="margin-bottom: 1.5rem; background: rgba(239, 68, 68, 0.05); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z"/>
                  </svg>
                  <div>
                    <strong>Numerical Data Required</strong>
                    <p style="margin: 4px 0 0 0; font-size: 0.85rem; opacity: 0.9;">{{ smoteValidation.message }}</p>
                  </div>
                </div>

                <!-- SMOTE Educational Note -->
                <div class="info-alert" style="margin-bottom: 1.5rem; background: rgba(59, 130, 246, 0.05);">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                  </svg>
                  <div>
                    <p style="margin: 0; font-size: 0.9rem; color: #b3b3d1;">
                      <strong>Note:</strong> SMOTE increases training data size by generating synthetic samples. The test set remains unchanged to ensure fair evaluation on real data.
                    </p>
                  </div>
                </div>
                
                <div class="class-distribution-grid">
                  <div 
                    v-for="(info, className) in classDistribution" 
                    :key="className"
                    class="class-item"
                  >
                    <div class="class-name">{{ className }}</div>
                    <div class="class-stats">
                      <span class="class-count">{{ info.count }} samples</span>
                      <span class="class-percentage">{{ info.percentage }}%</span>
                    </div>
                    <div class="class-bar">
                      <div 
                        class="class-bar-fill" 
                        :style="{ width: info.percentage + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
                
                <div class="imbalance-info" v-if="imbalanceRatio >= 3" :class="'imbalance-' + imbalanceSeverity">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                  </svg>
                  <span>
                    Imbalance Ratio: <strong>{{ imbalanceRatio.toFixed(2) }}x</strong>
                    <span v-if="imbalanceSeverity === 'severe'" class="severity-label"> (Severe - SMOTE Strongly Recommended)</span>
                    <span v-else-if="imbalanceSeverity === 'mild'" class="severity-label"> (Mild - SMOTE Optional)</span>
                  </span>
                </div>
              </div>

              <!-- Sampling Strategy -->
              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                  </svg>
                  Sampling Strategy
                </label>
                <select v-model="smoteStrategy" class="config-select">
                  <option value="auto">Auto (Balance all classes)</option>
                  <option value="minority">Minority (Oversample minority only)</option>
                  <option value="not minority">Not Minority (Oversample all except majority)</option>
                </select>
                <p class="config-help">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                  </svg>
                  {{ 
                    smoteStrategy === 'auto' 
                      ? 'Automatically balance all classes to have equal samples' 
                      : smoteStrategy === 'minority'
                      ? 'Only oversample the minority class to match the majority'
                      : 'Oversample all classes except the majority class'
                  }}
                </p>
              </div>

              <!-- K-Neighbors Parameter -->
              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                  </svg>
                  K-Neighbors
                  <span class="config-value-badge">{{ smoteKNeighbors }}</span>
                </label>
                
                <div class="slider-container">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    step="1"
                    v-model.number="smoteKNeighbors"
                    class="split-slider"
                  />
                  <div class="slider-labels">
                    <span>1</span>
                    <span>10</span>
                  </div>
                </div>
                
                <p class="config-help">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                  </svg>
                  Number of nearest neighbors used to generate synthetic samples. Default: 5
                </p>
              </div>

              <!-- Random Seed -->
              <div class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                  Random Seed
                  <span class="optional-tag">Optional</span>
                </label>
                <input
                  type="number"
                  v-model.number="smoteRandomSeed"
                  placeholder="Enter seed for reproducibility (e.g., 42)"
                  class="config-input"
                />
                <p class="config-help">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                  </svg>
                  Set a seed value for reproducible results. Leave empty for random generation.
                </p>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showSmoteModal = false">
                Cancel
              </Button>
              <Button 
                v-if="smoteApplied"
                variant="primary"
                @click="resetSmote"
                style="background: #ef4444; border-color: #ef4444;"
              >
                Reset SMOTE
              </Button>
              <Button 
                variant="primary" 
                :loading="isProcessing"
                @click="applySmote"
                :disabled="isProcessing || !smoteValidation.valid || smoteApplied"
              >
                Apply SMOTE
              </Button>
            </template>
          </Modal>

          <!-- ========== CARD 5: TF-IDF VECTORIZATION ========== -->
          <Card 
            class="preprocessing-tool-card" 
            hover 
            :class="{ disabled: !splitApplied }"
          >
            <div class="tool-header">
              <div class="tool-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 3h18v2H3V3zm0 4h18v2H3V7zm0 4h18v2H3v-2zm0 4h18v2H3v-2zm0 4h18v2H3v-2z"/>
                </svg>
              </div>
              <div class="tool-info">
                <h3>
                  TF-IDF Vectorization
                  <span v-if="!splitApplied" class="requires-split-inline">⚠️ Requires Split</span>
                </h3>
                <p>Convert text columns (reviews, descriptions) to numerical features</p>
              </div>
              <div class="tool-badge" :class="{ 'success-badge': tfidfApplied }">
                {{ tfidfApplied ? "✓ Applied" : "Not Applied" }}
              </div>
            </div>
            
            <div class="tool-footer">
              <Button variant="primary" @click="detectAndConfigureTfidf" :disabled="!splitApplied">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                </svg>
                Configure TF-IDF
              </Button>
            </div>
          </Card>

          <!-- TF-IDF Configuration Modal -->
          <Modal v-model="showTfidfModal" title="TF-IDF Vectorization Configuration" size="xl">
            <div class="modal-section">
              <!-- Info Alert -->
              <div class="info-alert">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                </svg>
                <div>
                  <strong>What is TF-IDF?</strong>
                  <p>TF-IDF (Term Frequency-Inverse Document Frequency) converts text into numerical features by measuring word importance. Ideal for reviews, descriptions, and other text data.</p>
                </div>
              </div>

              <!-- No Text Columns Detected -->
              <div v-if="textColumns.length === 0" class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.3;">
                  <path d="M3 3h18v2H3V3zm0 4h18v2H3V7zm0 4h18v2H3v-2zm0 4h18v2H3v-2zm0 4h18v2H3v-2z"/>
                </svg>
                <p>No text columns detected in your dataset.</p>
                <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">Text columns must have average length ≥ 30 characters.</p>
              </div>

              <!-- Detected Text Columns -->
              <div v-else class="config-group">
                <label class="config-label">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 3h18v2H3V3zm0 4h18v2H3V7zm0 4h18v2H3v-2zm0 4h18v2H3v-2zm0 4h18v2H3v-2z"/>
                  </svg>
                  Detected Text Columns ({{ textColumns.length }})
                </label>
                
                <div class="encoding-list">
                  <div
                    v-for="column in textColumns"
                    :key="column.name"
                    class="encoding-row"
                    :class="{ active: column.selected }"
                  >
                    <label class="checkbox-label">
                      <input
                        type="checkbox"
                        v-model="column.selected"
                      />
                      <span class="checkbox-custom"></span>
                      <span class="col-name">
                        {{ column.name }}
                        <span class="category-count" style="color: #3b82f6; font-weight: 600;">
                          Score: {{ column.score }}/10
                        </span>
                      </span>
                    </label>

                    <!-- Column Metrics -->
                    <div class="recommendation-info" style="margin-top: 0.5rem; flex-wrap: wrap;">
                      <span class="rec-badge" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                        {{ column.avg_length }} chars avg
                      </span>
                      <span class="rec-badge" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                        {{ column.median_words }} words median
                      </span>
                      <span class="rec-badge" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                        {{ column.vocabulary_size }} vocab
                      </span>
                      <span class="rec-badge" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                        entropy: {{ column.entropy }}
                      </span>
                    </div>

                    <!-- Reasoning (expandable) -->
                    <div v-if="column.reasoning && column.reasoning.length > 0" style="margin-top: 0.5rem;">
                      <details style="cursor: pointer;">
                        <summary style="color: #94a3b8; font-size: 0.85rem; user-select: none;">
                          📊 View detection reasoning ({{ column.reasoning.length }} signals)
                        </summary>
                        <ul style="margin: 0.5rem 0 0 1.5rem; padding: 0; color: #b3b3d1; font-size: 0.85rem; line-height: 1.6;">
                          <li v-for="(reason, idx) in column.reasoning" :key="idx">
                            {{ reason }}
                          </li>
                        </ul>
                      </details>
                    </div>

                    <!-- Configuration Display -->
                    <div v-if="column.selected && column.config" class="recommendation-info" style="margin-top: 0.75rem; border-top: 1px solid rgba(102, 126, 234, 0.2); padding-top: 0.75rem;">
                      <span class="rec-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">
                        max_features: {{ column.config.max_features }}
                      </span>
                      <span class="rec-badge" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">
                        ngram: {{ column.config.ngram_range[0] }}-{{ column.config.ngram_range[1] }}
                      </span>
                      <span class="rec-reason">Dataset tier: {{ tfidfConfig.base_params?.tier || 'auto' }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Warnings -->
              <div v-if="tfidfWarnings.length > 0" class="leakage-warning" style="margin-top: 1.5rem;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 16h2v2h-2zm0-6h2v4h-2z"/>
                </svg>
                <div>
                  <strong>Safety Adjustments:</strong>
                  <ul style="margin: 0.5rem 0 0 1.5rem; padding: 0;">
                    <li v-for="warning in tfidfWarnings" :key="warning.type">
                      {{ warning.message }}
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Model Compatibility -->
              <div v-if="tfidfConfig.recommended_models" class="info-alert" style="background: rgba(59, 130, 246, 0.05); margin-top: 1.5rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                </svg>
                <div>
                  <strong>Recommended Models:</strong>
                  <p style="margin: 0.5rem 0 0 0;">Linear models (Ridge, ElasticNet) or boosting models (LightGBM, XGBoost, CatBoost) work best with TF-IDF features.</p>
                </div>
              </div>

              <!-- Anti-Leakage Protection -->
              <div class="leakage-warning" style="margin-top: 1.5rem;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 16h2v2h-2zm0-6h2v4h-2z"/>
                </svg>
                <span><strong>Anti-Leakage Protection:</strong> TF-IDF will be fit on Training Set only and then applied to Test Set.</span>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showTfidfModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                :loading="isProcessing"
                @click="applyTfidf"
                :disabled="!textColumns.some(c => c.selected)"
              >
                Apply TF-IDF
              </Button>
            </template>
          </Modal>

          <!-- Reset Confirmation Modal -->
          <Modal v-model="showResetConfirmModal" title="Reset All Transformations?" size="md">
            <div class="modal-section">
              <div class="config-group">
                <p style="margin-bottom: 1rem; color: #e0e7ef; line-height: 1.6;">
                  Are you sure you want to reset all transformations?
                </p>
                <p style="margin-bottom: 1rem; color: #94a3b8; line-height: 1.6;">
                  This will:
                </p>
                <ul style="color: #94a3b8; margin-left: 1.5rem; line-height: 1.8;">
                  <li>Clear the dataset split</li>
                  <li>Remove all categorical encoding</li>
                  <li>Remove all feature scaling</li>
                  <li>Return dataset to its original state</li>
                </ul>
                <p style="margin-top: 1rem; color: #fbbf24; line-height: 1.6;">
                  ⚠️ This action cannot be undone.
                </p>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showResetConfirmModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                @click="confirmResetAll"
                style="background: #ef4444; border-color: #ef4444;"
              >
                Reset All
              </Button>
            </template>
          </Modal>

          <!-- Reset Split Confirmation Modal -->
          <Modal v-model="showResetSplitModal" title="Reset Dataset Split?" size="md">
            <div class="modal-section">
              <div class="config-group">
                <p style="margin-bottom: 1rem; color: #e0e7ef; line-height: 1.6;">
                  Are you sure you want to reset the dataset split?
                </p>
                <p style="margin-bottom: 1rem; color: #94a3b8; line-height: 1.6;">
                  This will also clear:
                </p>
                <ul style="color: #94a3b8; margin-left: 1.5rem; line-height: 1.8;">
                  <li>All categorical encoding</li>
                  <li>All feature scaling</li>
                </ul>
              </div>
            </div>
            
            <template #footer>
              <Button variant="ghost" @click="showResetSplitModal = false">
                Cancel
              </Button>
              <Button 
                variant="primary" 
                @click="confirmResetSplit"
                style="background: #ef4444; border-color: #ef4444;"
              >
                Reset Split
              </Button>
            </template>
          </Modal>

         
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
            @click="proceedToAlgorithmSelection"
            class="footer-btn continue-btn primary"
            :disabled="!splitApplied"
          >
            <span>Proceed to Algorithm Selection</span>
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
import { useAuthenticatedFetch } from '~/composables/useAuthenticatedFetch'
import { useToast } from '~/composables/useToast'
import { addPreprocessingStep } from '@/utils/preprocessingTracker';


const { authenticatedPost, authenticatedGet } = useAuthenticatedFetch()
const { showSuccess, showError, showWarning, showInfo } = useToast()

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

console.log('\n' + '='.repeat(80));
console.log('🎯 ADVANCED PREPROCESSING - Target Variable');
console.log('='.repeat(80));
console.log('   Selected Target:', selectedTarget.value || 'Not set');
console.log('   Full State:', mlAppState);
console.log('='.repeat(80) + '\n'); 


// ==================== SPLIT & SCALE CONFIG ====================
const splitApplied = ref(false);
const scalingApplied = ref(false);
const encodingApplied = ref(false);
const targetEncodingApplied = ref(false);
const currentSplitView = ref("full"); // 'full', 'train', 'test'
const splitRatio = ref(0.8);
const splitStrategy = ref("random"); // 'random' or 'stratified'
const randomSeed = ref(null);
const scalingMethod = ref("standard"); // 'standard', 'minmax', 'robust', 'maxabs', 'none'
const scaledColumns = ref(new Set()); // Track scaled columns
const targetEncodedColumns = ref(new Set()); // Track target encoded columns

watch(scaledColumns, (newSet) => {
  columns.value.forEach(col => {
    col.isAlreadyScaled = newSet.has(col.name);
  });
}, { deep: true });

// Watch for split applied to check class imbalance
watch(splitApplied, async (newValue) => {
  if (newValue && selectedTarget.value && problemType.value === 'classification') {
    // Wait a bit for the split to complete
    await nextTick();
    await checkClassImbalance();
  }
});

// ==================== TOOLKIT STATE ====================
const enabledTools = ref([]);
const openDropdowns = ref([]);

// ==================== MODAL STATE ====================
const showSplitModal = ref(false);
const showEncodingModal = ref(false);
const showScalingModal = ref(false);
const showResetConfirmModal = ref(false);
const showResetSplitModal = ref(false);
const showSmoteModal = ref(false);
const showTargetEncodingModal = ref(false);

// ==================== SMOTE STATE ====================
const smoteApplied = ref(false);
const smoteStrategy = ref('auto'); // 'auto', 'minority', 'not minority'
const smoteKNeighbors = ref(5);
const smoteRandomSeed = ref(null);
const targetEncodingSmoothing = ref(10);
const hasClassImbalance = ref(false);
const imbalanceRatio = ref(1.0);
const imbalanceSeverity = ref('balanced'); // 'balanced', 'mild', 'severe'
const classDistribution = ref({});

// Load correct problemType from mlAppState
const problemType = ref(mlAppState.problemType || 'classification');

// ==================== TF-IDF STATE ====================
const showTfidfModal = ref(false);
const tfidfApplied = ref(false);
const textColumns = ref([]);  // Detected text columns with metadata
const tfidfConfig = ref({});  // Recommended configuration
const tfidfWarnings = ref([]);  // Safety warnings
const selectedTextColumns = ref([]);  // User-selected columns for TF-IDF

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

const numericalColumns = computed(() =>
  columns.value.filter(col => col.type === 'numerical' && col.name !== selectedTarget.value && !scaledColumns.value.has(col.name))
);

const smoteValidation = computed(() => {
  const cats = columns.value.filter(col => col.type === 'categorical' && col.name !== selectedTarget.value);
  if (cats.length > 0) {
    return {
      valid: false,
      message: `SMOTE requires all feature columns to be numerical. Please encode the following categorical columns first: ${cats.map(c => c.name).join(', ')}.`
    };
  }
  return { valid: true };
});

// For per-column encoding selection state (update as needed for your structure)
categoricalColumns.value.forEach(col => {
  col.encode = col.encode ?? false;       // Whether to encode
  col.encoding = col.encoding ?? 'onehot';// Encoding method: onehot, label, ordinal
});

// For per-column scaling selection state
numericalColumns.value.forEach(col => {
  col.scale = col.scale ?? false;         // Whether to scale
  // Ensure scalingMethod is initialized to standard if null/undefined
  if (col.scalingMethod === undefined || col.scalingMethod === null || col.scalingMethod === '') {
    col.scalingMethod = 'standard';
  }
  // Mark as already scaled
  col.isAlreadyScaled = scaledColumns.value.has(col.name);
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
  // If column is selected but has no encoding method, default to the recommendation
  if (column.encode && !column.encoding) {
    column.encoding = getEncodingRecommendation(column).method;
  }
}

// Toggle scaling for a column
function toggleColumnScaling(column) {
  // Use recommendation when selected if no method set
  if (column.scale && !column.scalingMethod) {
    column.scalingMethod = getScalingRecommendation(column).method;
  }
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
    if (baseCol) {
      baseCol.encode = true;
      if (!baseCol.encoding) {
        baseCol.encoding = getEncodingRecommendation(col).method;
      }
    }
  });
}

function deselectAllCategoricalColumns() {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) baseCol.encode = false;
  });
}

// Select recommended columns for categorical encoding (exclude high cardinality)
function selectRecommendedCategoricalColumns() {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) {
       const rec = getEncodingRecommendation(col);
       if (rec.method !== 'target' && col.name !== selectedTarget.value) {
         baseCol.encode = true;
         baseCol.encoding = rec.method;
       } else {
         baseCol.encode = false;
       }
    }
  });
}

// Smart auto-select (exclude target column by name)
function autoSelectForEncoding(targetName) {
  categoricalColumns.value.forEach(col => {
    const baseCol = columns.value.find(c => c.name === col.name);
    if (baseCol) {
      baseCol.encode = (col.name !== targetName && col.unique > 1);
      if (baseCol.encode && !baseCol.encoding) {
        baseCol.encoding = getEncodingRecommendation(col).method;
      }
    }
  });
}

// Select recommended columns for target encoding (high cardinality)
function selectRecommendedTargetEncoding() {
  categoricalColumns.value.forEach(col => {
    if (col.name !== selectedTarget.value && !targetEncodedColumns.value.has(col.name)) {
      if (col.unique >= 10) {
        col.targetEncode = true;
      }
    }
  });
}

function selectAllTargetEncoding() {
  categoricalColumns.value.forEach(col => {
    if (col.name !== selectedTarget.value && !targetEncodedColumns.value.has(col.name)) {
      col.targetEncode = true;
    }
  });
}

function deselectAllTargetEncoding() {
  categoricalColumns.value.forEach(col => {
    col.targetEncode = false;
  });
}

// Categorical Encoding Recommendation Rules
const getEncodingRecommendation = (column) => {
  if (!column) return { method: 'onehot', reason: 'Defaulting to One-Hot' };

  const name = (column.name || '').toLowerCase();
  const uniqueCount = column.unique || 0;

  // 1. Ordinal Exclusion List (Columns that should NOT be ordinal)
  const nominalOnlyKeywords = [
    'occupation', 'city', 'country', 'department', 'relationship', 
    'gender', 'product', 'id', 'name', 'zip', 'email', 'phone'
  ];
  const isNominalOnly = nominalOnlyKeywords.some(k => name.includes(k));

  // 2. Ordinal Detection (Name-based)
  const ordinalNameKeywords = [
    'level', 'rating', 'rank', 'priority', 'severity', 'stage', 
    'size', 'satisfaction', 'education', 'experience', 'performance', 'grade'
  ];
  const hasOrdinalName = ordinalNameKeywords.some(k => name.includes(k));

  // 3. Ordinal Detection (Value-based - check sample values)
  const ordinalValueTerms = ['low', 'medium', 'high', 'small', 'large', 'poor', 'average', 'good', 'excellent', 'beginner', 'intermediate', 'expert', 'bronze', 'silver', 'gold'];
  const ordinalValuePatterns = [/level_\d+/i, /grade_\d+/i, /rank_\d+/i, /stage_\d+/i, /priority_\d+/i];
  
  // Get samples from originalDataset
  const samples = originalDataset.value
    .slice(0, 10)
    .map(row => String(row[column.name] || '').toLowerCase());
  
  const hasOrdinalValue = samples.some(s => 
    ordinalValueTerms.some(term => s.includes(term)) || 
    ordinalValuePatterns.some(pattern => pattern.test(s))
  );

  // Recommend Ordinal if confident (and not on exclusion list)
  if (!isNominalOnly && (hasOrdinalName || hasOrdinalValue)) {
    return {
      method: 'ordinal',
      reason: `Natural order detected based on ${hasOrdinalName ? 'column name' : 'category values'}.`,
      isOrdinal: true
    };
  }

  // 4. Cardinality-based Rules (Fallbacks)
  if (uniqueCount <= 10) {
    return {
      method: 'onehot',
      reason: 'Low cardinality detected; One-Hot is efficient and safe.'
    };
  } else if (uniqueCount <= 50) {
    return {
      method: 'label',
      reason: 'Moderate cardinality; Label Encoding is recommended for Tree-based models.'
    };
  } else {
    return {
      method: 'target',
      reason: 'High cardinality detected. One-Hot or Label Encoding may lead to poor performance.',
      note: '🚨 Recommend: Use Target Encoding tool for this column.'
    };
  }
};

// Feature Scaling Recommendation Rules
const getScalingRecommendation = (column) => {
  if (!column || !column.backendMetrics) return { method: 'standard', reason: 'Defaulting to Standard Scaling' };

  const m = column.backendMetrics;
  const skew = Math.abs(m.skewness || 0);
  const hasOutliers = (m.outliers_count || 0) > 0;
  
  // Bounded range detection (Rule 3)
  const isBounded = (m.min >= 0 && (m.max <= 1 || m.max === 100 || m.max === 10 || m.max === 5));
  
  // Rule 4: MaxAbsScaler (Sparsity)
  if ((m.zeros_pct || 0) > 30 || (Math.abs(m.mean || 0) < 0.1 && m.std > 0)) {
     return {
       method: 'maxabs',
       reason: 'MaxAbsScaler preserves sparsity and scales by maximum absolute value.'
     };
  }

  // Rule 1: RobustScaler (Outliers/Skewness)
  if (hasOutliers || skew > 1.5) {
    return {
      method: 'robust',
      reason: 'RobustScaler is resistant to outliers and skewed distributions.'
    };
  }

  // Rule 3: MinMaxScaler (Bounded Range)
  if (isBounded) {
    return {
      method: 'minmax',
      reason: 'MinMaxScaler preserves relative distances within a fixed range.'
    };
  }

  // Rule 2: StandardScaler (Normal/Symmetric)
  if (skew < 1 && !hasOutliers) {
    return {
      method: 'standard',
      reason: 'StandardScaler works best for normally distributed data.'
    };
  }

  // Default Fallback
  return {
    method: 'standard',
    reason: 'StandardScaler is recommended for this distribution.'
  };
};


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
    const response = await authenticatedGet(`http://localhost:8000/api/datasets/${datasetId}`)
    
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

const fetchCompleteStatistics = async () => {
  if (!datasetId.value) return;

  try {
    console.log("🔄 Fetching complete statistics for accurate category counts...");
    const response = await authenticatedGet(`http://localhost:8000/api/datasets/${datasetId.value}/statistics`);
    
    if (!response.ok) {
      console.warn("⚠️ Failed to fetch statistics from backend");
      return;
    }

    const stats = await response.json();

    if (stats.column_stats) {
      console.log("✅ Received full statistics, updating column metadata");
      // Update columns with backend statistics
      stats.column_stats.forEach(stat => {
        const col = columns.value.find(c => c.name === stat.name);
        if (col) {
          col.unique = stat.unique;
          col.missing = stat.missing;
          // Store additional metrics if needed for future use
          col.backendMetrics = stat.detailed_metrics; 
        }
      });
      console.log("✅ Updated unique category counts from full dataset");
    }
  } catch (error) {
    console.warn("⚠️ Error updating statistics:", error);
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

    // Step 6: Fetch complete statistics after initial analysis (Accurate category counts)
    if (mlStore.backendConnected && datasetId.value) {
      await fetchCompleteStatistics();
    }

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

  console.log('Sending split request for dataset ID:', datasetId.value);

  if (!selectedTarget.value) {
    alert("⚠️ No target column selected. Please go back to Target Selection.");
    isProcessing.value = false;
    return;
  }

  if (!datasetId.value) {
    alert("⚠️ No dataset ID found. Please refresh the page or go back to upload a dataset.");
    isProcessing.value = false;
    return;
  }

  try {
    const payload = {
      datasetid: datasetId.value,
      test_size: 1 - splitRatio.value,
      stratify: splitStrategy.value === 'stratified',
      random_state: randomSeed.value || 42,
      target_column: selectedTarget.value
    };

    console.log('🔍 Split Request Debug:');
    console.log('  Dataset ID:', payload.datasetid);
    console.log('  Target Column:', payload.target_column);
    console.log('  Full Payload:', payload);

    const response = await authenticatedPost('http://localhost:8000/api/split-dataset', payload)

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

      showSuccess(
        'Dataset Split Applied!',
        `Train: ${data.train_size.toLocaleString()} rows | Test: ${data.test_size.toLocaleString()} rows`
      );

      addPreprocessingStep('Train/Test Split');

      // CRITICAL: Save the dataset ID immediately after successful split
      // This ensures that even if the user navigates via sidebar (skipping proceedToAlgorithmSelection),
      // the correct dataset ID is available for training.
      if (datasetId.value) {
        localStorage.setItem('backendDatasetId', datasetId.value);
        localStorage.setItem('datasetId', datasetId.value);
        console.log('✅ Saved processed dataset ID to localStorage (on split success):', datasetId.value);
      }

      // Close the modal
      showSplitModal.value = false;
    } else {
      throw new Error(data.message || "Split failed");
    }
  } catch (error) {
    console.error("❌ Split error:", error);
    showError('Split Failed', error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = "";
  }
};


const resetSplit = () => {
  showResetSplitModal.value = true;
};

const confirmResetSplit = () => {
  splitApplied.value = false;
  scalingApplied.value = false;
  encodingApplied.value = false;
  scaledColumns.value.clear();
  trainData.value = [];
  testData.value = [];
  trainRows.value = 0;
  testRows.value = 0;
  currentSplitView.value = "full";

  mlStore.isSplit = false;
  mlStore.isScaled = false;
  mlStore.isEncoded = false;

  // Clear Target Encoding State
  targetEncodingApplied.value = false;
  targetEncodedColumns.value.clear();

  showResetSplitModal.value = false;
  console.log("🔄 Split reset");
  showSuccess('Split Reset', 'All transformations have been cleared');
};

// Reset all transformations
const resetAllTransformations = () => {
  showResetConfirmModal.value = true;
};

const confirmResetAll = async () => {
  try {
    isProcessing.value = true;
    showResetConfirmModal.value = false;
    
    // Reload the original dataset from backend
    await loadInitialData();
    
    // Reset all state
    splitApplied.value = false;
    scalingApplied.value = false;
    encodingApplied.value = false;
    scaledColumns.value.clear();
    trainData.value = [];
    testData.value = [];
    trainRows.value = 0;
    testRows.value = 0;
    currentSplitView.value = "full";
    
    mlStore.isSplit = false;
    mlStore.isScaled = false;
    mlStore.isEncoded = false;

    // Clear Target Encoding State
    targetEncodingApplied.value = false;
    targetEncodedColumns.value.clear();
    
    console.log("🔄 All transformations reset");
    showSuccess('Reset Complete', 'Dataset returned to original state');
  } catch (error) {
    console.error('❌ Reset error:', error);
    showError('Reset Failed', error.message);
  } finally {
    isProcessing.value = false;
  }
};

// ==================== SMOTE OPERATIONS ====================

// Re-check class imbalance on the backend
const checkClassImbalance = async () => {
  // 🛑 GUARD: SMOTE and imbalance checks only apply to classification
  if (problemType.value !== 'classification') {
    console.log("⏭️ Skipping imbalance check: Problem type is", problemType.value);
    return;
  }

  if (!splitApplied.value || !selectedTarget.value) return;

  try {
    const response = await authenticatedGet(
      `http://localhost:8000/api/datasets/${datasetId.value}/check-imbalance?target_column=${selectedTarget.value}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      hasClassImbalance.value = data.has_imbalance;
      imbalanceRatio.value = data.imbalance_ratio;
      imbalanceSeverity.value = data.severity;
      classDistribution.value = data.class_distribution;

      console.log('📊 Class Imbalance Check:');
      console.log('  Has Imbalance:', data.has_imbalance);
      console.log('  Ratio:', data.imbalance_ratio);
      console.log('  Severity:', data.severity);
      console.log('  Recommendation:', data.recommendation);
    }
  } catch (error) {
    console.error('❌ Error checking class imbalance:', error);
    // Don't show error to user, just log it
  }
};

// Apply SMOTE
const applySmote = async () => {
  if (!splitApplied.value || !hasClassImbalance.value) {
    showWarning('SMOTE Not Available', 'Dataset must be split and have class imbalance');
    return;
  }

  console.log("\n" + "=".repeat(80));
  console.log("⚖️ APPLYING SMOTE");
  console.log("=".repeat(80));

  isProcessing.value = true;
  processingMessage.value = "Applying SMOTE...";

  try {
    const payload = {
      sampling_strategy: smoteStrategy.value,
      k_neighbors: smoteKNeighbors.value,
      random_state: smoteRandomSeed.value
    };

    console.log('🔍 SMOTE Request Debug:');
    console.log('  Dataset ID:', datasetId.value);
    console.log('  Configuration:', payload);

    const response = await authenticatedPost(
      `http://localhost:8000/api/datasets/${datasetId.value}/apply-smote`,
      payload
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      console.log("✅ SMOTE applied successfully");
      console.log(`  Original samples: ${data.original_samples}`);
      console.log(`  New samples: ${data.new_samples}`);
      console.log(`  Samples added: ${data.samples_added}`);

      smoteApplied.value = true;
      trainRows.value = data.new_samples;

      // Update class distribution
      classDistribution.value = data.class_distribution_after;

      // Update mlStore with new training row count
      mlStore.splitInfo = {
        ...mlStore.splitInfo,
        trainRows: data.new_samples,
        smoteApplied: true,
        samplesAdded: data.samples_added
      };

      console.log("=".repeat(80) + "\n");

      showSuccess(
        'SMOTE Applied Successfully!',
        `Added ${data.samples_added} synthetic samples to balance the training set. New training size: ${data.new_samples.toLocaleString()} rows`
      );

      addPreprocessingStep('SMOTE Analysis');

      // Re-check class imbalance to update the UI with new balanced distribution
      await checkClassImbalance();

      // ✅ CRITICAL: Update processedData in localStorage immediately
      // This ensures algorithm-select page sees the updated row counts
      const existingProcessedData = JSON.parse(localStorage.getItem('processedData') || '{}');
      existingProcessedData.splitInfo = mlStore.splitInfo; // Update with SMOTE-modified split info
      localStorage.setItem('processedData', JSON.stringify(existingProcessedData));
      console.log('✅ Updated processedData in localStorage with SMOTE-modified splitInfo');

      // Close the modal
      showSmoteModal.value = false;
    } else {
      throw new Error(data.detail || "SMOTE application failed");
    }
  } catch (error) {
    console.error("❌ SMOTE error:", error);
    showError('SMOTE Failed', error.message || 'Failed to apply SMOTE');
  } finally {
    isProcessing.value = false;
  }
};

// Reset SMOTE
const resetSmote = async () => {
  if (!smoteApplied.value) {
    return;
  }

  try {
    const response = await authenticatedPost(
      `http://localhost:8000/api/datasets/${datasetId.value}/reset-smote`,
      {}
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      smoteApplied.value = false;
      
      showInfo(
        'SMOTE Reset',
        data.message || 'SMOTE has been reset. Please re-split the dataset to restore original training data.'
      );

      // Close modal
      showSmoteModal.value = false;

      // If requires resplit, suggest it
      if (data.requires_resplit) {
        showWarning(
          'Re-split Required',
          'Please reset and re-apply the dataset split to restore original training data and row counts'
        );
      }
    }
  } catch (error) {
    console.error('❌ Error resetting SMOTE:', error);
    showError('Reset Failed', error.message);
  }
};


// ==================== SCALING OPERATIONS ====================

const applyScaling = async () => {
  if (!splitApplied.value || isProcessing.value) {
    alert("Please apply split first");
    return;
  }

  // Get columns to scale
  const columnsToScale = numericalColumns.value
    .filter(col => col.scale)
    .map(col => ({
      name: col.name,
      method: col.scalingMethod || 'standard'
    }));

  if (columnsToScale.length === 0) {
    alert('Please select at least one numerical column for scaling.');
    return;
  }

  console.log("\n" + "=".repeat(80));
  console.log("📊 APPLYING FEATURE SCALING");
  console.log("=".repeat(80));

  isProcessing.value = true;
  processingMessage.value = "Scaling features...";

  if (!datasetId.value) {
    alert("⚠️ No dataset ID found. Please refresh the page.");
    isProcessing.value = false;
    return;
  }

  try {
    const payload = {
      dataset_id: datasetId.value,
      columns: columnsToScale
    };

    console.log('🔍 Scaling Request Debug:');
    console.log('  Dataset ID:', payload.dataset_id);
    console.log('  Columns to scale:', columnsToScale);

    const response = await authenticatedPost('http://localhost:8000/api/datasets/apply-scaling', payload)

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
      mlStore.isScaled = true;
      mlStore.scalingMethod = scalingMethod.value;
      
      // Track scaled columns (Force reactive update)
      const newScaledSet = new Set(scaledColumns.value);
      columnsToScale.forEach(col => newScaledSet.add(col.name));
      scaledColumns.value = newScaledSet;

      console.log("=".repeat(80) + "\n");

      const scaledCount = columnsToScale.length;
      const scaledList = columnsToScale.slice(0, 3).map(c => c.name).join(', ');
      const moreText = scaledCount > 3 ? ` and ${scaledCount - 3} more` : '';
      
      showSuccess(
        'Feature Scaling Applied!',
        `Scaled ${scaledCount} column${scaledCount !== 1 ? 's' : ''}: ${scaledList}${moreText}`
      );

      addPreprocessingStep('Feature Scaling');

      // Close the modal
      showScalingModal.value = false;
    } else {
      throw new Error(data.error || "Scaling failed");
    }
  } catch (error) {
    console.error("❌ Scaling error:", error);
    showError('Scaling Failed', error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = "";
  }
};



const selectAllNumericalColumns = () => {
  numericalColumns.value.forEach(col => {
    col.scale = true;
    if (!col.scalingMethod) {
      col.scalingMethod = getScalingRecommendation(col).method;
    }
  });
};

const deselectAllNumericalColumns = () => {
  numericalColumns.value.forEach(col => col.scale = false);
};



const resetScaling = async () => {
  if (
    confirm(
      "Are you sure you want to reset scaling? This will reload the split data without scaling."
    )
  ) {
    scalingApplied.value = false;
    mlStore.isScaled = false;
    scaledColumns.value.clear();

    await applySplit();

    console.log("🔄 Scaling reset");
  }
};

// ==================== EXPORT FUNCTION ====================

const exportData = async () => {
  console.log("🔄 Starting data export...");

  try {
    let response;
    let filename = "";

    if (currentSplitView.value === "train" && splitApplied.value) {
      // Export full training dataset from backend
      console.log("📥 Exporting full training dataset from backend...");
      response = await authenticatedGet(`http://localhost:8000/api/export-train/${datasetId.value}`);
      filename = `${fileName.value.replace(".csv", "")}_train.csv`;
      
    } else if (currentSplitView.value === "test" && splitApplied.value) {
      // Export full test dataset from backend
      console.log("📥 Exporting full test dataset from backend...");
      response = await authenticatedGet(`http://localhost:8000/api/export-test/${datasetId.value}`);
      filename = `${fileName.value.replace(".csv", "")}_test.csv`;
      
    } else {
      // Export full original dataset from backend
      console.log("📥 Exporting full original dataset from backend...");
      response = await authenticatedGet(`http://localhost:8000/api/export-dataset/${datasetId.value}`);
      filename = fileName.value;
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Export failed with status ${response.status}`);
    }

    // Download the file
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);

    console.log(`✅ Exported full dataset to ${filename}`);
    showSuccess('Export Complete', `Downloaded ${filename}`);
    
  } catch (error) {
    console.error("❌ Export failed:", error);
    showError('Export Failed', error.message);
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

  if (!datasetId.value) {
    alert("⚠️ No dataset ID found. Please refresh the page.");
    return;
  }

  isProcessing.value = true;

  try {
    // POST to backend - adapt this to your splitting/scaling pipeline as needed
    const payload = {
      dataset_id: datasetId.value,
      columns: columnsToEncode
    };

    console.log('🔍 Encoding Request Debug:');
    console.log('  Dataset ID:', payload.dataset_id);
    console.log('  Columns to encode:', columnsToEncode);

  const response = await authenticatedPost('http://localhost:8000/api/apply-categorical-encoding', payload)

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(`HTTP ${response.status}: ${errorBody.detail || errorBody.message || 'Unknown error'}`);
  }

  const data = await response.json();
  if (data.success) {
    console.log('🔍 Encoding Response:', data);
    console.log('  Train preview rows:', data.train_preview?.length);
    console.log('  Test preview rows:', data.test_preview?.length);
    console.log('  Encoded columns:', data.encoded_columns);
    console.log('  New columns:', data.columns);
    
    trainData.value = data.train_preview || [];
    testData.value = data.test_preview || [];
    encodingApplied.value = true;
    
    // Update columns list with new encoded column names
    if (data.columns && data.columns.length > 0) {
      console.log('  Updating columns from:', columns.value.map(c => c.name));
      console.log('  To:', data.columns);
      
      // Rebuild columns array with new column names
      columns.value = data.columns.map(colName => {
        // Check if this is an encoded column (new column from one-hot encoding)
        const isEncodedColumn = data.encoded_columns?.includes(colName);
        
        // Try to find existing column info
        const existingCol = columns.value.find(c => c.name === colName);
        
        if (existingCol) {
          if (isEncodedColumn) existingCol.type = 'numerical';
          return existingCol;
        } else {
          // New column (from one-hot encoding)
          return {
            name: colName,
            type: isEncodedColumn ? 'numerical' : 'categorical',
            unique: 0,
            missing: 0,
            remove: false,
            encode: false,
            encoding: 'onehot'
          };
        }
      });
      
      console.log('  Updated columns:', columns.value.map(c => c.name));
    }
    
    // Switch to train view to show encoded data
    currentSplitView.value = 'train';
    
    console.log('✅ Categorical encoding applied successfully');
    console.log('  Current view:', currentSplitView.value);
    console.log('  Train data rows:', trainData.value.length);
    
    const encodedCount = data.encoded_columns?.length || 0;
    const encodedList = data.encoded_columns?.slice(0, 3).join(', ') || '';
    const moreText = encodedCount > 3 ? ` and ${encodedCount - 3} more` : '';
    
    showSuccess(
      'Categorical Encoding Applied!',
      `Encoded ${encodedCount} column${encodedCount !== 1 ? 's' : ''}: ${encodedList}${moreText}`
    );
    
    addPreprocessingStep('Categorical Encoding');

    // Close the modal
    showEncodingModal.value = false;
    // Refresh table, preview, columns, etc. here as needed
  } else {
    throw new Error(data.detail || data.message || 'Encoding failed');
  }
  } catch (error) {
    console.error('❌ Encoding error:', error);
    showError('Encoding Failed', error.message);
  } finally {
    isProcessing.value = false;
  }
}


// ===== TF-IDF METHODS =====

async function detectAndConfigureTfidf() {
  try {
    if (!datasetId.value) {
      showError('Error', 'No dataset ID found');
      return;
    }

    isProcessing.value = true;
    processingMessage.value = 'Detecting text columns...';

    // Step 1: Detect text columns
    const detectResponse = await authenticatedPost('http://localhost:8000/api/detect-text-columns', {
      dataset_id: datasetId.value
    });

    const detectData = await detectResponse.json();

    if (!detectData.success) {
      throw new Error('Text column detection failed');
    }

    console.log('📝 Detected text columns:', detectData.text_columns);

    // Step 2: Configure TF-IDF parameters
    if (detectData.text_columns.length > 0) {
      processingMessage.value = 'Configuring TF-IDF parameters...';

      const configResponse = await authenticatedPost('http://localhost:8000/api/configure-tfidf', {
        dataset_id: datasetId.value,
        text_columns: detectData.text_columns
      });

      const configData = await configResponse.json();

      if (!configData.success) {
        throw new Error('TF-IDF configuration failed');
      }

      console.log('⚙️ TF-IDF configuration:', configData);

      // Store configuration
      tfidfConfig.value = configData;
      tfidfWarnings.value = configData.warnings || [];

      // Prepare text columns with configuration
      textColumns.value = detectData.text_columns.map(col => ({
        ...col,
        selected: false,
        config: configData.column_configs.find(c => c.name === col.name)
      }));

      showSuccess('Text Columns Detected', `Found ${detectData.text_columns.length} text column(s)`);
    } else {
      textColumns.value = [];
      showInfo('No Text Columns', 'No text columns detected in your dataset');
    }

    // Show modal
    showTfidfModal.value = true;

  } catch (error) {
    console.error('❌ TF-IDF detection error:', error);
    showError('Detection Failed', error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = '';
  }
}

async function applyTfidf() {
  try {
    const selectedColumns = textColumns.value.filter(c => c.selected);

    if (selectedColumns.length === 0) {
      showWarning('No Selection', 'Please select at least one text column');
      return;
    }

    if (!datasetId.value) {
      showError('Error', 'No dataset ID found');
      return;
    }

    isProcessing.value = true;
    processingMessage.value = `Applying TF-IDF to ${selectedColumns.length} column(s)...`;

    // Prepare request payload
    const columnsConfig = selectedColumns.map(col => ({
      name: col.name,
      max_features: col.config.max_features,
      min_df: col.config.min_df,
      max_df: col.config.max_df,
      ngram_range: col.config.ngram_range
    }));

    console.log('🔤 Applying TF-IDF with config:', columnsConfig);

    const response = await authenticatedPost('http://localhost:8000/api/apply-tfidf', {
      dataset_id: datasetId.value,
      columns: columnsConfig
    });

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.detail || 'TF-IDF application failed');
    }

    console.log('✅ TF-IDF applied successfully:', data);

    // Update preview data
    trainData.value = data.train_preview || [];
    testData.value = data.test_preview || [];
    columns.value = data.columns.map(col => ({ name: col }));

    // Update state
    tfidfApplied.value = true;
    showTfidfModal.value = false;

    // Show success message with details
    showSuccess(
      'TF-IDF Applied',
      `Added ${data.tfidf_features_added} TF-IDF features. Total features: ${data.final_feature_count}`
    );

    // Add preprocessing step
    addPreprocessingStep({
      type: 'tfidf',
      description: `Applied TF-IDF to ${selectedColumns.length} text column(s)`,
      details: {
        columns: selectedColumns.map(c => c.name),
        total_features_added: data.tfidf_features_added,
        final_feature_count: data.final_feature_count
      }
    });

  } catch (error) {
    console.error('❌ TF-IDF application error:', error);
    showError('TF-IDF Failed', error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = '';
  }
}




async function applyTargetEncoding() {
  const columnsToEncode = categoricalColumns.value
    .filter(col => col.targetEncode)
    .map(col => ({
      name: col.name,
      smoothing: targetEncodingSmoothing.value
    }));

  if (columnsToEncode.length === 0) {
    alert('Please select at least one categorical column for target encoding.');
    return;
  }

  if (!datasetId.value) {
    alert("⚠️ No dataset ID found. Please refresh the page.");
    return;
  }

  isProcessing.value = true;
  processingMessage.value = "Applying Target Encoding...";

  try {
    const payload = {
      dataset_id: datasetId.value,
      columns: columnsToEncode
    };

    console.log('🔍 Target Encoding Request:', payload);

    const response = await authenticatedPost('http://localhost:8000/api/apply-target-encoding', payload)

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${errorBody.detail || errorBody.message || 'Unknown error'}`);
    }

    const data = await response.json();
    if (data.success) {
      console.log('✅ Target encoding successful');
      
      trainData.value = data.train_preview || [];
      testData.value = data.test_preview || [];
      targetEncodingApplied.value = true;
      
      // Track which columns were encoded (Force reactive update)
      const newEncodedSet = new Set(targetEncodedColumns.value);
      columnsToEncode.forEach(col => newEncodedSet.add(col.name));
      targetEncodedColumns.value = newEncodedSet;
      
      // Update columns list if new columns were added (multiclass)
      if (data.columns && data.columns.length > 0) {
        // Rebuild columns array
        columns.value = data.columns.map(colName => {
          const isNewEncodedCol = data.encoded_columns?.includes(colName);
          const existingCol = columns.value.find(c => c.name === colName);
          
          if (existingCol) {
            // Update type to numerical if it was target encoded
            if (isNewEncodedCol) existingCol.type = 'numerical';
            return existingCol;
          }
          
          return {
            name: colName,
            type: 'numerical',
            unique: 0,
            missing: 0,
            remove: false,
            encode: false,
            encoding: 'onehot'
          };
        });
      }
      
      currentSplitView.value = 'train';
      
      const encodedCount = columnsToEncode.length;
      showSuccess(
        'Target Encoding Applied!',
        `Encoded ${encodedCount} column${encodedCount !== 1 ? 's' : ''} using category means with smoothing (k=${targetEncodingSmoothing.value}).`
      );
      
      addPreprocessingStep('Target Encoding');
      showTargetEncodingModal.value = false;
    } else {
      throw new Error(data.detail || 'Target encoding failed');
    }
  } catch (error) {
    console.error('❌ Target encoding error:', error);
    showError('Target Encoding Failed', error.message);
  } finally {
    isProcessing.value = false;
    processingMessage.value = "";
  }
}




// ==================== NAVIGATION ====================

const goBack = () => {
  router.push("/target-selection");
};

const proceedToAlgorithmSelection = () => {
  console.log('🔵 proceedToAlgorithmSelection called!', { splitApplied: splitApplied.value });
  
  if (!splitApplied.value) {
    showWarning('Split Required', 'Please apply dataset splitting before proceeding');
    return;
  }

  // Save preprocessing state
  localStorage.setItem(
    "advancedPreprocessing",
    JSON.stringify({
      splitApplied: splitApplied.value,
      scalingApplied: scalingApplied.value,
      encodingApplied: encodingApplied.value,
      splitRatio: splitRatio.value,
      scalingMethod: scalingMethod.value,
      trainRows: trainRows.value,
      testRows: testRows.value,
      processedDatasetId: datasetId.value // CRITICAL: Save ID here too for model-training.vue
    })
  );

  // CRITICAL: Save the processed dataset ID (this is the dataset with split/encode/scale applied)
  if (datasetId.value) {
    console.log('🔍 DEBUG: Current datasetId.value:', datasetId.value);
    console.log('🔍 DEBUG: mlStore.cleanedDatasetId:', mlStore.cleanedDatasetId);
    console.log('🔍 DEBUG: mlStore.datasetId:', mlStore.datasetId);
    
    localStorage.setItem('backendDatasetId', datasetId.value);
    localStorage.setItem('datasetId', datasetId.value);
    console.log('✅ Saved processed dataset ID to localStorage:', datasetId.value);
  } else {
    console.error('❌ WARNING: datasetId.value is empty! Cannot save to localStorage');
  }

  // CRITICAL FIX: Save the current processed data preview to localStorage
  // This ensures algorithm-select.vue displays the preprocessed (scaled/encoded) data
  const currentDataPreview = splitApplied.value 
    ? (trainData.value.length > 0 ? trainData.value : originalDataset.value)
    : originalDataset.value;

  const processedDataPayload = {
    data: currentDataPreview.slice(0, 200), // Save preview (first 200 rows)
    fileName: fileName.value,
    backendDatasetId: datasetId.value,
    datasetId: datasetId.value,
    totalRowsInBackend: totalRowsInBackend.value,
    rowCount: totalRowsInBackend.value || currentDataPreview.length,
    columnCount: columns.value.length,
    columns: columns.value.map(col => col.name || col),
    backendAvailable: mlStore.backendConnected,
    splitInfo: mlStore.splitInfo, // ✅ Include split info with SMOTE-updated training rows
    preprocessingApplied: {
      split: splitApplied.value,
      scaling: scalingApplied.value,
      encoding: encodingApplied.value,
      scaledColumns: Array.from(scaledColumns.value)
    },
    processingSteps: JSON.parse(localStorage.getItem('processedData') || '{}').processingSteps || []
  };

  localStorage.setItem('processedData', JSON.stringify(processedDataPayload));
  console.log('✅ Saved processed data preview to localStorage:', {
    rows: processedDataPayload.data.length,
    columns: processedDataPayload.columnCount,
    scaled: scalingApplied.value,
    scaledColumns: processedDataPayload.preprocessingApplied.scaledColumns
  });

  // Ensure pipeline state has targetColumn for navigation guard
  const pipelineState = JSON.parse(
    localStorage.getItem("datasage_pipeline_state") || "{}"
  );
  
  if (!pipelineState.targetColumn) {
    // Get target from mlStore
    pipelineState.targetColumn = mlStore.targetColumn || selectedTarget.value;
    pipelineState.dataset = mlStore.dataset;
    localStorage.setItem("datasage_pipeline_state", JSON.stringify(pipelineState));
  }

  console.log('Navigating to algorithm selection with state:', pipelineState);
  router.push("/algorithm-select");
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
  appearance: none;
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
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.stat-label {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.stat-value {
  display: block;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.col-name {
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
}

.category-count {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 4px;
}

.col-main-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.recommendation-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-left: 2rem;
}

.rec-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  width: fit-content;
}

.rec-badge.onehot {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.rec-badge.label {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.rec-badge.ordinal {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.rec-badge.target {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.rec-badge.standard {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.rec-badge.minmax {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.rec-badge.robust {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.rec-badge.maxabs {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.scaling-rec {
  margin-top: 4px;
}

.rec-reason {
  font-size: 0.75rem;
  color: #94a3b8;
  font-style: italic;
}

.rec-note {
  font-size: 0.7rem;
  color: #6366f1;
  margin: 0;
  font-weight: 500;
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
  appearance: none;
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

.continue-btn {
  animation: none !important
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

/* Hero Section - Glassmorphism Effect */
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
  max-width: 1200px;
  margin: 0 auto;
}

.hero-header-centered {
  text-align: center;
  margin-bottom: 2rem;
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

.dataset-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.summary-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.summary-stat:hover {
  background: rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.stat-icon {
  color: #667eea;
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
  flex: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: #b3b3d1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.quality-indicator {
  width: 100%;
}

.quality-score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.quality-score.excellent {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.quality-score.good {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.quality-score.fair {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.quality-score.poor {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.quality-icon {
  flex-shrink: 0;
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
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #764ba2, #667eea);
}

/* ========== NEW UI ELEMENTS ========== */

/* Ratio Display */
.ratio-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 16px;
}

.ratio-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
}

.ratio-card.train .ratio-value {
  color: #667eea;
}

.ratio-card.test .ratio-value {
  color: #ef4444;
}

.ratio-value {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.ratio-label {
  font-size: 0.75rem;
  color: #b3b3d1;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.ratio-rows {
  font-size: 0.85rem;
  color: #94a3b8;
}

.ratio-visual {
  flex: 1;
  padding: 0 1rem;
}

.ratio-bar {
  height: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
}

.ratio-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.ratio-fill.train {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.ratio-fill.test {
  background: linear-gradient(90deg, #ef4444, #b91c1c);
}

/* Slider Labels */
.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 500;
}

/* Categorical Encoding Selection */
.selection-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.btn-secondary.small {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.encoding-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.encoding-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.encoding-row.active {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  flex: 1;
}

.checkbox-label.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checkbox-label.disabled .checkbox-custom {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.checkbox-label input {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(102, 126, 234, 0.4);
  border-radius: 6px;
  position: relative;
  transition: all 0.2s ease;
}

.checkbox-custom::after {
  content: "✓";
  color: white;
  font-size: 14px;
  display: none;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.checkbox-label input:checked + .checkbox-custom {
  background: #667eea;
  border-color: #667eea;
}

.checkbox-label input:checked + .checkbox-custom::after {
  display: block;
}

.col-name {
  font-size: 1rem;
  color: #e0e7ef;
  font-weight: 500;
}

.encoding-select-wrapper {
  position: relative;
  min-width: 180px;
}

.encoding-select {
  width: 100%;
  padding: 0.5rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #e0e7ef;
  font-size: 0.9rem;
  outline: none;
  cursor: pointer;
}

.encoding-select:focus {
  border-color: #667eea;
}

.encoding-select.placeholder-active {
  color: #94a3b8;
  font-style: italic;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
  font-style: italic;
  background: rgba(26, 26, 46, 0.4);
  border-radius: 8px;
}

/* ==================== PREPROCESSING TOOL CARD STYLES ==================== */
.preprocessing-tool-card {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.preprocessing-tool-card:hover {
  border-color: rgba(102, 126, 234, 0.4);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
}

.preprocessing-tool-card.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1rem;
}

.tool-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.requires-split-inline {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.tool-info p {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.5;
}

.tool-badges-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex-shrink: 0;
}

.tool-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(71, 85, 105, 0.5);
  color: #cbd5e1;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

/* ==================== IMPROVED COLUMN LIST STYLES ==================== */

.select-all-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.selection-count {
  font-size: 0.85rem;
  color: #94a3b8;
}

.column-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom Scrollbar */
.column-list::-webkit-scrollbar {
  width: 6px;
}

.column-list::-webkit-scrollbar-track {
  background: rgba(30, 41, 59, 0.3);
  border-radius: 3px;
}

.column-list::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 3px;
}

.column-item {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
}

.column-item:hover {
  background: rgba(30, 41, 59, 0.6);
  border-color: rgba(102, 126, 234, 0.3);
}

.column-item.selected {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.4);
}

.column-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.column-actions {
  flex-shrink: 0;
}

.mini-select {
  padding: 0.35rem 0.75rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #e2e8f0;
  font-size: 0.85rem;
  outline: none;
  cursor: pointer;
  min-width: 160px;
}

.mini-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.method-description {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #94a3b8;
  padding-left: 2rem; /* Align with text, past checkbox */
}

.col-name {
  font-size: 0.95rem;
  color: #f1f5f9; /* Brighter white */
  font-weight: 500;
}

.tool-badge.success-badge {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border-color: rgba(34, 197, 94, 0.3);
}

.order-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.order-badge.order-1 {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.order-badge.order-2 {
  background: rgba(168, 85, 247, 0.2);
  color: #d8b4fe;
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.order-badge.order-3 {
  background: rgba(236, 72, 153, 0.2);
  color: #f9a8d4;
  border: 1px solid rgba(236, 72, 153, 0.3);
}

.order-badge.order-warning {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.tool-footer {
  padding: 0 1.25rem 1rem 1.25rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* ==================== MODAL SECTION STYLES ==================== */
.modal-section {
  padding: 1rem 0;
}

/* ==================== DISABLED BUTTON STYLES ==================== */
.footer-btn:disabled,
.footer-btn.continue-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
  background: rgba(71, 85, 105, 0.5) !important;
  border-color: rgba(71, 85, 105, 0.3) !important;
  color: rgba(148, 163, 184, 0.7) !important;
}

.footer-btn:disabled:hover {
  transform: none;
  box-shadow: none;
}

/* ==================== SMOTE STYLES ==================== */

/* SMOTE Badges */
.balanced-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  margin-left: 8px;
}

.imbalance-badge-mild {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
  margin-left: 8px;
}

.imbalance-badge-severe {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  margin-left: 8px;
  font-weight: 600;
}

/* Class Distribution Grid */
.class-distribution-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(25, 27, 44, 0.5);
  border-radius: 8px;
}

.class-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.class-name {
  font-weight: 600;
  color: #e0e7ef;
  font-size: 0.95rem;
}

.class-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.class-count {
  color: #94a3b8;
}

.class-percentage {
  color: #667eea;
  font-weight: 600;
}

.class-bar {
  height: 8px;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.class-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Imbalance Info */
.imbalance-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.imbalance-info.imbalance-mild {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.imbalance-info.imbalance-severe {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.imbalance-info svg {
  flex-shrink: 0;
}

.imbalance-info strong {
  color: inherit;
  font-weight: 700;
}

.imbalance-info .severity-label {
  font-size: 0.85rem;
  opacity: 0.9;
}

/* Config Value Badge */
.config-value-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  margin-left: 8px;
  font-weight: 600;
}


.category-count {
  font-size: 0.85rem;
  opacity: 0.6;
  margin-left: 4px;
}

.recommendation-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.strongly-rec {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.recommended {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.not-recommended {
  background: rgba(107, 114, 128, 0.1);
  color: #6b7280;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid rgba(107, 114, 128, 0.2);
}

.leakage-warning {
  background: rgba(245, 158, 11, 0.05);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #d97706;
  font-size: 0.9rem;
  margin-top: 16px;
}

.leakage-warning svg {
  flex-shrink: 0;
}

.info-alert {
  background: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  color: #1e40af;
}

.info-alert strong {
  display: block;
  margin-bottom: 4px;
}

.info-alert p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  opacity: 0.8;
}


</style>
