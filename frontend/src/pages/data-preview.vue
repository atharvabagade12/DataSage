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
          Back to Dashboard
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Data Preprocessing</span>
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
          <h1 class="gradient-text">Data Preprocessing</h1>
          <p class="hero-subtitle">Clean and prepare your dataset for machine learning</p>
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
              <path d="M3,3H21V21H3V3M5,5V19H19V5H5M7,7H9V9H7V7M11,7H13V9H11V7M15,7H17V9H15V7Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Rows</span>
              <span class="stat-value">{{ displayedRowCount.toLocaleString() }}</span>
            </div>
          </div>
          
          <div class="summary-stat">
            <svg class="stat-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2,2H8V4H16V2H22V8H20V16H22V22H16V20H8V22H2V16H4V8H2V2M16,8V6H8V8H6V16H8V18H16V16H18V8H16M4,4V6H6V4H4M18,4V6H20V4H18M4,18V20H6V18H4M18,18V20H20V18H18Z"/>
            </svg>
            <div class="stat-content">
              <span class="stat-label">Columns</span>
              <span class="stat-value">{{ dataInfo.columns }}</span>
            </div>
          </div>
          
          <div class="summary-stat">
            <div class="quality-indicator">
              <div class="quality-score" :class="getHealthLevel(dataQuality.score)">
                <svg class="quality-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,2L2,7V13.5C2,19.75 6.5,25.5 12,27C17.5,25.5 22,19.75 22,13.5V7L12,2M12,4.18L20,8.09V13.5C20,18.87 16.25,23.74 12,25.13C7.75,23.74 4,18.87 4,13.5V8.09L12,4.18Z"/>
                </svg>
                <span>{{ dataQuality.score }}% Quality</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content Container -->
    <div class="main-container">
      <!-- Data Table Preview Section -->
      <section class="table-preview-section">
        <div class="section-header">
          <h2>Data Preview</h2>
          <div class="preview-controls">
            <button
              @click="showOriginal = true"
              :class="{ active: showOriginal }"
              class="preview-toggle"
            >
              Original Data
            </button>
            <button
              @click="showOriginal = false"
              :class="{ active: !showOriginal }"
              class="preview-toggle"
              :disabled="!hasCleanedData"
            >
              Cleaned Data
            </button>
            
          </div>
        </div>

        <!-- Table Container -->
        <div class="table-container">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <span class="table-info">
                Showing {{ startRow }} to {{ endRow }} of
                {{ filteredRows.length }} rows
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
                Download CSV
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
                      <span v-if="isEncodedColumn(column)" class="encoded-badge"
                        >Encoded</span
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

      

        <!-- Data Preprocessing Toolkit Section -->
        <section class="preprocessing-section">
          <div class="section-header">
            <h2>Data Preprocessing Toolkit</h2>
            <p class="section-description">
              Select and configure preprocessing steps to clean your data
            </p>
          </div>

          <!-- Help Section: Why Order Matters -->
          <Card variant="info" class="preprocessing-help-section">
            <details class="help-details">
              <summary class="help-summary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" class="help-icon">
                  <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                </svg>
                <strong>Why does preprocessing order matter?</strong>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" class="chevron-icon">
                  <path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/>
                </svg>
              </summary>
              <div class="help-content">
                <p>Preprocessing steps can affect each other in unexpected ways:</p>
                <ul class="help-list">
                  <li>
                    <strong>Capping outliers</strong> may create new duplicates by setting multiple extreme values to the same threshold
                  </li>
                  <li>
                    <strong>Removing duplicates</strong> may change the data distribution, causing new values to become outliers
                  </li>
                </ul>
                <div class="recommended-order-box">
                  <p class="order-title"><strong>📋 Recommended Order:</strong></p>
                  <ol class="order-list">
                    <li><span class="order-number">1</span> Handle Missing Values</li>
                    <li><span class="order-number">2</span> Handle Outliers</li>
                    <li><span class="order-number">3</span> Remove Duplicates</li>
            
                  </ol>
                  <p class="order-note">
                    💡 Following this order ensures optimal results and prevents unexpected behavior.
                  </p>
                </div>
              </div>
            </details>
          </Card>

          <div class="preprocessing-grid">
            <!-- ========== CARD 0: DATA TYPE DETECTION & CONVERSION ========== -->
            <Card class="preprocessing-tool-card" hover>
              <div class="tool-header">
                <div class="tool-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10,10-4.48,10-10S17.52,2,12,2z M13,17h-2v-2h2v2z M13,13h-2V7h2V13z"/>
                  </svg>
                </div>
                <div class="tool-info">
                  <h3>
                    Type Detection & Conversion
                    <span class="step-badge">Source of Truth</span>
                  </h3>
                  <p>Verify and override semantic data types for all downstream tools</p>
                </div>
                <div class="tool-badge success-badge">
                  ✓ Active
                </div>
              </div>
              
              <div class="tool-footer">
                <Button variant="primary" @click="openTypeDetectionModal">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,9L10,9L10,11L12,11L12,13L14,13L14,11L16,11L16,9L14,9L14,7L12,7L12,9Z M7,9L9,9L9,11L7,11L7,9Z M21,3h-18c-1.1,0-2,0.9-2,2v14c0,1.1,0.9,2,2,2h18c1.1,0,2-0.9,2-2v-14c0-1.1-0.9-2-2-2z M21,19h-18v-14h18v14z"/>
                  </svg>
                  Manage Types
                </Button>
              </div>
            </Card>

            <!-- Column Selection Tool - REFACTORED WITH MODAL -->
            <Card class="preprocessing-tool-card" hover>
              <div class="tool-header">
                <div class="tool-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2,2H8V4H16V2H22V8H20V16H22V22H16V20H8V22H2V16H4V8H2V2M16,8V6H8V8H6V16H8V18H16V16H18V8H16M4,4V6H6V4H4M18,4V6H20V4H18M4,18V20H6V18H4M18,18V20H20V18H18Z"/>
                  </svg>
                </div>
                <div class="tool-info">
                  <h3>Column Selection</h3>
                  <p>Remove irrelevant columns that don't contribute to learning</p>
                </div>
                <div class="tool-badge">{{ columns.length }} columns</div>
              </div>
              
              <div class="tool-footer">
                <Button variant="primary" @click="showColumnModal = true">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19.4,13C19.8,13 20.1,13.3 20.1,13.7V19.4C20.1,19.8 19.8,20.1 19.4,20.1H13.7C13.3,20.1 13,19.8 13,19.4V13.7C13,13.3 13.3,13 13.7,13H19.4M19.4,3.9C19.8,3.9 20.1,4.2 20.1,4.6V10.3C20.1,10.7 19.8,11 19.4,11H13.7C13.3,11 13,10.7 13,10.3V4.6C13,4.2 13.3,3.9 13.7,3.9H19.4M10.3,13C10.7,13 11,13.3 11,13.7V19.4C11,19.8 10.7,20.1 10.3,20.1H4.6C4.2,20.1 3.9,19.8 3.9,19.4V13.7C3.9,13.3 4.2,13 4.6,13H10.3M10.3,3.9C10.7,3.9 11,4.2 11,4.6V10.3C11,10.7 10.7,11 10.3,11H4.6C4.2,11 3.9,10.7 3.9,10.3V4.6C3.9,4.2 4.2,3.9 4.6,3.9H10.3Z"/>
                  </svg>
                  Configure Columns
                </Button>
              </div>
            </Card>
            
            <!-- Column Selection Modal -->
            <Modal v-model="showColumnModal" title="Column Selection" size="xl">
              <div class="modal-section">
                <div class="modal-section-header">
                  <h4>Select columns to remove from dataset</h4>
                  <div class="quick-actions">
                    <Button variant="ghost" size="sm" @click="selectNoColumns">
                      Clear All
                    </Button>
                    <Button variant="outline" size="sm" @click="selectIrrelevantColumns">
                      Auto-Select Irrelevant
                    </Button>
                    <Button variant="ghost" size="sm" @click="selectAllColumns">
                      Select All
                    </Button>
                  </div>
                </div>
                
                <div class="columns-grid-modal">
                  <Card 
                    v-for="column in columns" 
                    :key="column.name"
                    class="column-card-modal"
                    :class="{ 'column-to-remove': column.remove }"
                  >
                    <div class="column-card-header">
                      <label class="column-checkbox-native">
                        <input 
                          type="checkbox"
                          v-model="column.remove"
                          class="checkbox-input"
                        />
                        <span class="checkbox-label">{{ column.name }}</span>
                      </label>
                      <span class="column-type-badge" :class="`type-${column.type}`">
                        {{ column.type }}
                      </span>
                      <span class="semantic-type-pill" :class="getColumnSemanticType(column.name)" style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1);">
                        {{ getColumnSemanticType(column.name).toUpperCase() }}
                      </span>
                    </div>
                    
                    <div class="column-card-body">
                      <div class="column-stats-row">
                        <span class="stat-chip">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                          </svg>
                          {{ column.unique }} unique
                        </span>
                        <span v-if="column.missing > 0" class="stat-chip missing">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                          </svg>
                          {{ column.missing }} missing
                        </span>
                      </div>
                      
                      <div class="column-sample">
                        <span class="sample-label">Sample:</span>
                        <span class="sample-value">{{ getColumnSample(column) }}</span>
                      </div>
                    </div>
                    
                    <div v-if="column.remove" class="column-remove-badge">
                      {{ getColumnSemanticType(column.name) === 'identifier' ? 'Identifier - Recommended Removal' : 'Will be removed' }}
                    </div>
                  </Card>
                </div>
                
                <div v-show="getColumnsToRemove().length > 0" class="selection-summary-modal">
                  <Card variant="warning">
                    <div class="summary-content">
                      <div class="summary-header">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                        </svg>
                        <strong>{{ getColumnsToRemove().length }} columns will be removed</strong>
                      </div>
                      <div class="removal-tags">
                        <span v-for="col in getColumnsToRemove()" :key="col.name" class="removal-tag">
                          {{ col.name }}
                        </span>
                      </div>
                    </div>
                  </Card>
                </div>
              </div>
              
              <template #footer>
                <Button variant="ghost" @click="showColumnModal = false">
                  Cancel
                </Button>
                <Button 
                  variant="primary" 
                  :loading="isProcessing"
                  @click="applyColumnChanges"
                  :disabled="getColumnsToRemove().length === 0"
                >
                  Apply Changes
                </Button>
              </template>
            </Modal>

            <!-- Missing Values Tool - REFACTORED WITH MODAL -->
            <Card class="preprocessing-tool-card" hover>
              <div class="tool-header">
                <div class="tool-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"/>
                  </svg>
                </div>
                <div class="tool-info">
                  <h3>Handle Missing Values</h3>
                  <p>Choose strategy for columns with missing data</p>
                </div>
                <div class="tool-badges-container">
                  <span class="order-badge order-1">1️⃣ First</span>
                  <div class="tool-badge" v-if="missingStats.count > 0">
                    {{ missingStats.count }} columns affected
                  </div>
                  <div class="tool-badge success-badge" v-else>
                    ✓ No missing values
                  </div>
                </div>
              </div>
              
              <div class="tool-footer">
                <Button variant="primary" @click="showMissingModal = true" :disabled="missingStats.count === 0">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                  </svg>
                  Configure Strategies
                </Button>
              </div>
            </Card>
            
            <!-- Missing Values Modal -->
            <Modal v-model="showMissingModal" title="Missing Values Strategy" size="xl">
              <div class="modal-section">
                <!-- Global Strategy Section -->
                <Card variant="primary" v-show="missingColumnsDetailed.length > 0">
                  <div class="global-strategy-section">
                    <h4>Quick Apply to All Columns</h4>
                    <div class="global-controls">
                      <select v-model="globalMissingStrategy" class="native-select-global">
                        <option value="droprows">Drop Rows with Missing Values</option>
                        <option value="fillmean">Fill with Mean (numerical only)</option>
                        <option value="fillmedian">Fill with Median (numerical only)</option>
                        <option value="fillmode">Fill with Most Frequent Value</option>
                        <option value="fillzero">Fill with Zero</option>
                        <option value="fillunknown">Fill with "Unknown"</option>
                      </select>
                      <Button variant="outline" size="sm" @click="applyGlobalMissingStrategy">
                        Apply to All
                      </Button>
                      <Button variant="ghost" size="sm" @click="autoSelectMissingStrategies">
                        Auto-Select
                      </Button>
                    </div>
                  </div>
                </Card>
                <!-- Per-Column Strategies -->
                <div class="columns-flex-modal" v-show="missingColumnsDetailed.length > 0">
                  <Card 
                    v-for="col in missingColumnsDetailed" 
                    :key="col.name"
                    class="column-card-modal missing-column-card"
                  >
                    <div class="column-card-header">
                      <span class="column-name-text">{{ col.name }}</span>
                      <span class="column-type-badge" :class="`type-${col.type}`">
                        {{ col.type }}
                      </span>
                    </div>
                    
                    <div class="missing-stats-row">
                      <span class="stat-chip missing">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"/>
                        </svg>
                        {{ col.count }} missing ({{ col.percentage }}%)
                      </span>
                      <span class="semantic-type-pill" :class="col.semanticType" style="font-size: 0.75rem; padding: 2px 8px; border-radius: 12px; background: rgba(255,255,255,0.1);">
                        {{ col.semanticType || 'unknown' }}
                      </span>
                    </div>
                    
                    <select 
                      v-model="col.strategy" 
                      @change="updateMissingStrategy(col.name, col.strategy)"
                      class="native-select-strategy"
                    >
                      <!-- Rule: Identifier MUST be dropped -->
                      <option v-if="col.semanticType === 'identifier'" value="droprows">Drop Rows (Mandatory for IDs)</option>
                      
                      <!-- Standard options for others -->
                      <template v-else>
                        <option value="droprows">Drop Rows</option>
                        <option value="fillmean" v-if="col.semanticType === 'numeric'">Fill with Mean</option>
                        <option value="fillmedian" v-if="col.semanticType === 'numeric'">Fill with Median</option>
                        <option value="fillmode" v-if="['categorical', 'boolean'].includes(col.semanticType)">Fill with Mode</option>
                        <option value="fillzero" v-if="['numeric', 'boolean'].includes(col.semanticType)">Fill with Zero</option>
                        <option value="fillunknown" v-if="['categorical', 'datetime'].includes(col.semanticType)">Fill with "Unknown"</option>
                      </template>
                      <option value="keep">Keep Missing (Not Recommended)</option>
                    </select>
                    
                    <p class="strategy-hint" style="font-size: 0.75rem; color: #b3b3d1; margin-top: 0.5rem;">
                      {{ getStrategyDescription(col.strategy, col.type) }}
                    </p>
                  </Card>
                </div>
                <Card v-show="missingColumnsDetailed.length === 0">
                  <div class="no-data-message">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor" style="color: var(--color-success)">
                      <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M11,16.5L6.5,12L7.91,10.59L11,13.67L16.59,8.09L18,9.5L11,16.5Z"/>
                    </svg>
                    <h4>No Missing Values Found!</h4>
                    <p>Your dataset doesn't have any missing values. You can skip this step.</p>
                  </div>
                </Card>
                
                <!-- Summary -->
                <Card variant="warning" v-show="missingColumnsDetailed.length > 0">
                  <div class="summary-content">
                    <div class="summary-header">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                      </svg>
                      <strong>{{ missingColumnsDetailed.length }} columns</strong> with 
                      <strong>{{ missingStats.totalMissing }} total missing cells</strong>
                    </div>
                  </div>
                </Card>
              </div>
              
              <template #footer>
                <Button variant="ghost" @click="showMissingModal = false">
                  Cancel
                </Button>
                <Button 
                  variant="primary" 
                  :loading="isProcessing"
                  @click="applyMissingStrategies"
                  :disabled="missingColumnsDetailed.length === 0"
                >
                  Apply Strategies
                </Button>
              </template>
            </Modal>



<!-- Outlier Handling Tool - SAME PATTERN -->
            <!-- Outlier Handling Tool - REFACTORED WITH MODAL -->
            <Card class="preprocessing-tool-card" hover>
              <div class="tool-header">
                <div class="tool-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M16,6L18.29,8.29L13.41,13.17L9.41,9.17L2,16.59L3.41,18L9.41,12L13.41,16L19.71,9.71L22,12V6H16Z" />
                  </svg>
                </div>
                <div class="tool-info">
                  <h3>Handle Outliers</h3>
                  <p>Detect and handle extreme values in numerical columns</p>
                </div>
                <div class="tool-badges-container">
                  <span class="order-badge order-2">2️⃣ Second</span>
                  <div class="tool-badge" v-if="outlierStats.count > 0">
                    {{ outlierStats.count }} outliers detected
                  </div>
                  <div class="tool-badge success-badge" v-else>
                    ✓ No outliers found
                  </div>
                </div>
              </div>
              
              <div class="tool-footer">
                <Button variant="primary" @click="showOutlierModal = true" :disabled="outlierStats.count === 0">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                  </svg>
                  Configure Handling
                </Button>
              </div>
            </Card>
            
            <!-- Outlier Handling Modal -->
            <Modal v-model="showOutlierModal" title="Outlier Handling" size="md">
              <div class="modal-section">
                <Card>
                  <div class="duplicate-info">
                    <div class="info-stat">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="color: var(--color-warning)">
                        <path d="M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z" />
                      </svg>
                      <div>
                        <strong>{{ outlierStats.count }} outliers detected</strong>
                        <p>Across {{ outlierStats.columns }} numerical columns</p>
                      </div>
                    </div>
                  </div>
                </Card>
                
                <div class="strategy-options">
                  <h4>Select Handling Strategy</h4>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="outlierStrategy" value="cap" class="native-radio" />
                    <div class="option-content">
                      <strong>Cap Outliers (Winsorization)</strong>
                      <p>Limit extreme values to the 5th and 95th percentiles</p>
                    </div>
                  </label>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="outlierStrategy" value="remove" class="native-radio" />
                    <div class="option-content">
                      <strong>Remove Rows</strong>
                      <p>Remove rows containing outlier values</p>
                    </div>
                  </label>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="outlierStrategy" value="keep" class="native-radio" />
                    <div class="option-content">
                      <strong>Keep (Do Nothing)</strong>
                      <p>Keep outliers as they are (for analysis)</p>
                    </div>
                  </label>
                </div>
              </div>
              
              <template #footer>
                <Button variant="ghost" @click="showOutlierModal = false">
                  Cancel
                </Button>
                <Button 
                  variant="primary" 
                  :loading="isProcessing"
                  @click="applyOutlierHandling"
                >
                  Apply Strategy
                </Button>
              </template>
            </Modal>



            <!-- Duplicate Removal Tool - REFACTORED WITH MODAL -->
            <Card class="preprocessing-tool-card" hover>
              <div class="tool-header">
                <div class="tool-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M16,9H21.5L16,3.5V9M7,2H17L23,8V18A2,2 0 0,1 21,20H7C5.89,20 5,19.1 5,18V4A2,2 0 0,1 7,2M3,6V22H21V24H3A2,2 0 0,1 1,22V6H3Z" />
                  </svg>
                </div>
                <div class="tool-info">
                  <h3>Remove Duplicates</h3>
                  <p>Remove duplicate rows from your dataset</p>
                </div>
                <div class="tool-badges-container">
                  <span class="order-badge order-3">3️⃣ Third</span>
                  <div class="tool-badge" v-if="duplicateStats.count > 0">
                    {{ duplicateStats.count }} duplicates found
                  </div>
                  <div class="tool-badge success-badge" v-else>
                    ✓ No duplicates found
                  </div>
                </div>
              </div>
              
              <div class="tool-footer">
                <Button variant="primary" @click="showDuplicateModal = true" :disabled="duplicateStats.count === 0">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
                  </svg>
                  Configure Removal
                </Button>
              </div>
            </Card>
            
            <!-- Duplicate Removal Modal -->
            <Modal v-model="showDuplicateModal" title="Duplicate Removal" size="md">
              <div class="modal-section">
                <Card>
                  <div class="duplicate-info">
                    <div class="info-stat">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="color: var(--color-info)">
                        <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z" />
                      </svg>
                      <div>
                        <strong>{{ duplicateStats.count }} duplicate rows</strong> found
                        <p v-if="totalRows > 0">{{ ((duplicateStats.count / totalRows) * 100).toFixed(1) }}% of total rows</p>
                      </div>
                    </div>
                  </div>
                </Card>
                
                <div class="strategy-options">
                  <h4>Select Duplicate Handling Strategy</h4>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="duplicateStrategy" value="keep_first" class="native-radio" />
                    <div class="option-content">
                      <strong>Keep First Occurrence</strong>
                      <p>Remove all duplicates except the first occurrence</p>
                    </div>
                  </label>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="duplicateStrategy" value="keep_last" class="native-radio" />
                    <div class="option-content">
                      <strong>Keep Last Occurrence</strong>
                      <p>Remove all duplicates except the last occurrence</p>
                    </div>
                  </label>
                  
                  <label class="radio-option">
                    <input type="radio" v-model="duplicateStrategy" value="remove_all" class="native-radio" />
                    <div class="option-content">
                      <strong>Remove All Duplicates</strong>
                      <p>Remove all duplicate rows (including originals)</p>
                    </div>
                  </label>
                </div>
                
                <Card variant="warning" v-show="duplicateStrategy === 'remove_all'">
                  <div class="warning-content">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16" />
                    </svg>
                    <div>
                      <strong>Warning:</strong> This will remove ALL duplicate rows, including the original occurrences.
                    </div>
                  </div>
                </Card>
              </div>
              
              <template #footer>
                <Button variant="ghost" @click="showDuplicateModal = false">
                  Cancel
                </Button>
                <Button 
                  variant="primary" 
                  :loading="isProcessing"
                  @click="applyDuplicateRemoval"
                >
                  Remove Duplicates
                </Button>
              </template>
            </Modal>

            <!-- Data Type Detection Modal -->
            <Modal v-model="showTypeDetectionModal" title="Data Type Detection & Verification" size="xl">
              <div class="modal-section">
                <div class="info-alert" style="margin-bottom: 1.5rem; display: flex; gap: 1rem; background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="#667eea" style="flex-shrink: 0;">
                    <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                  </svg>
                  <div>
                    <strong style="color: #e2e8f0; display: block; margin-bottom: 0.25rem;">Why verify data types?</strong>
                    <p style="color: #94a3b8; font-size: 0.875rem; margin: 0;">Incorrect data types lead to ML errors. Categorical data treated as numeric can skew scaling, and identifiers should never be used as features. Setting correct types here ensures all other tools (imputers, scalers, encoders) behave correctly.</p>
                  </div>
                </div>

                <div v-if="isDetectingTypes" class="loading-inline" style="display: flex; align-items: center; justify-content: center; padding: 3rem; gap: 1rem; color: #94a3b8;">
                  <div class="spinner-small" style="width: 24px; height: 24px; border: 2px solid rgba(102, 126, 234, 0.2); border-top: 2px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                  <span>Analyzing dataset columns...</span>
                </div>

                <div v-else class="type-detection-table-wrapper" style="overflow-x: auto; background: rgba(15, 23, 42, 0.4); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
                  <table class="type-detection-table" style="width: 100%; border-collapse: collapse; font-size: 0.9rem; color: #e2e8f0; text-align: left;">
                    <thead>
                      <tr style="background: rgba(102, 126, 234, 0.1);">
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Column</th>
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Raw Type</th>
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Detected Semantic Type</th>
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Confidence</th>
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Reasoning</th>
                        <th style="padding: 1rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem;">Action / Override</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="col in semanticTypes" :key="col.column" :class="{ 'is-overridden': col.is_override }" style="border-bottom: 1px solid rgba(102, 126, 234, 0.1);">
                        <td style="padding: 1rem; font-weight: 500;">{{ col.column }}</td>
                        <td style="padding: 1rem;"><code style="background: rgba(255,255,255,0.05); padding: 0.2rem 0.4rem; border-radius: 4px;">{{ col.raw_dtype }}</code></td>
                        <td style="padding: 1rem;">
                          <span :class="['type-pill', col.semantic_type]" style="padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.7rem; font-weight: 700; display: inline-block;">
                            {{ col.semantic_type.toUpperCase() }}
                          </span>
                        </td>
                        <td style="padding: 1rem;">
                          <span :class="['confidence-badge', col.confidence]" style="padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.7rem; font-weight: 600; text-transform: capitalize;">
                            {{ col.confidence }}
                          </span>
                        </td>
                        <td style="padding: 1rem; color: #94a3b8; font-size: 0.8rem; line-height: 1.4; max-width: 250px;">{{ col.reason }}</td>
                        <td style="padding: 1rem;">
                          <select v-model="col.semantic_type" @change="col.is_override = true" style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(102, 126, 234, 0.3); color: #e2e8f0; padding: 0.5rem; border-radius: 8px; font-size: 0.85rem; width: 100%;">
                            <option value="numeric">Numeric</option>
                            <option value="categorical">Categorical</option>
                            <option value="boolean">Boolean</option>
                            <option value="datetime">Datetime</option>
                            <option value="identifier">Identifier (Rule Out)</option>
                          </select>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <template #footer>
                <Button variant="ghost" @click="showTypeDetectionModal = false">Cancel</Button>
                <Button variant="primary" :loading="isProcessing" @click="saveSemanticOverrides">
                  Save & Apply Globally
                </Button>
              </template>
            </Modal>
            
            <!-- Reset Confirmation Modal -->
            <Modal v-model="showResetModal" title="Reset All Changes" size="md">
              <div class="modal-section">
                <Card variant="warning">
                  <div class="warning-content">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="color: var(--color-warning)">
                      <path d="M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16" />
                    </svg>
                    <div>
                      <strong>Warning:</strong> This action will reset all preprocessing changes.
                    </div>
                  </div>
                </Card>
                
                <div class="reset-info">
                  <h4>The following will be reset:</h4>
                  <ul class="reset-list">
                    <li>✓ All preprocessing operations will be discarded</li>
                    <li>✓ Original dataset will be restored</li>
                    <li>✓ All tool configurations will be reset to defaults</li>
                    <li>✓ Cleaned data will be removed</li>
                  </ul>
                  <p class="reset-note">
                    You will need to reapply any preprocessing steps if you want to use them again.
                  </p>
                </div>
              </div>
              
              <template #footer>
                <Button variant="ghost" @click="showResetModal = false">
                  Cancel
                </Button>
                <Button 
                  variant="danger" 
                  :loading="isProcessing"
                  @click="confirmReset"
                >
                  Reset All Changes
                </Button>
              </template>
            </Modal>
        </div>
          </section>

            

        
        <!-- Skip Preprocessing Section -->
        <div class="skip-section" v-if="!hasActiveTools">
          <div class="skip-content">
            <h3>Skip Preprocessing</h3>
            <p>
              Your data looks good as-is? You can skip preprocessing and use the
              original dataset for machine learning.
            </p>
            <button @click="proceedToTargetSelection" class="skip-btn">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"
                />
              </svg>
              Skip to Target Selection
            </button>
          </div>
        </div>

        <!-- Apply Changes Section - ENHANCED -->
        <div class="apply-section" v-if="hasActiveTools">
          <div class="apply-summary">
            <h3>
              Ready to Apply {{ activeTools.length }} Change{{
                activeTools.length > 1 ? "s" : ""
              }}
            </h3>
            <div class="changes-preview">
              <div v-for="tool in activeTools" :key="tool" class="change-item">
                <span class="change-icon"></span>
                <span class="change-text">{{ getToolName(tool) }}</span>
                <span class="change-config">{{ getToolConfig(tool) }}</span>

                <!-- NEW: Individual tool controls -->
                <div class="change-actions">
                  <button
                    @click="toggleDropdown(tool)"
                    class="change-edit-btn"
                    :title="`Configure ${getToolName(tool)}`"
                  >
                    <svg
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"
                      />
                    </svg>
                  </button>
                  <button
                    @click="disableTool(tool)"
                    class="change-remove-btn"
                    :title="`Remove ${getToolName(tool)}`"
                  >
                    <svg
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="apply-buttons">
            <button @click="resetAllChanges" class="reset-btn">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"
                />
              </svg>
              Reset All
            </button>
            <button
              @click="applyChanges"
              class="apply-btn primary"
              :disabled="isProcessing || !hasActiveTools"
              :class="{ loading: isProcessing }"
            >
              <span v-if="isProcessing">
                <div class="btn-spinner"></div>
                Processing...
              </span>
              <span v-else>
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"
                  />
                </svg>
                Apply {{ activeTools.length }} Change{{
                  activeTools.length > 1 ? "s" : ""
                }}
              </span>
            </button>
          </div>
        </div>
      
    </div>

    <!-- Action Footer -->
    <div class="action-footer">
      <div class="footer-content">
        <!-- Processing Status -->
        <div class="processing-status">
          <div v-if="hasCleanedData" class="processing-complete">
            <div class="success-icon"></div>
            <div class="success-text">
              <h3>Dataset Successfully Cleaned!</h3>
              <p>Your data is now ready for machine learning model training</p>
            </div>
          </div>

          <div v-else class="processing-original">
            <div class="original-icon"></div>
            <div class="original-text">
              <h3>Original Dataset Ready</h3>
              <p>
                You can proceed with the original data or apply preprocessing
                steps first
              </p>
            </div>
          </div>
        </div>

        

        <!-- Action Buttons -->
        <div class="footer-actions">
          <button
            v-if="hasCleanedData"
            @click="showResetModal = true"
            class="footer-btn secondary"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"
              />
            </svg>
            Reset All Changes
          </button>

          <!-- Always show the Continue button -->
          <button @click="proceedToTargetSelection" class="footer-btn continue-btn primary">
            <span>{{
              hasCleanedData
                ? "Continue with Cleaned Data"
                : "Continue with Original Data"
            }}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Reset All Changes Confirmation Modal -->
    <Modal v-model="showResetModal" title="Reset All Changes?" size="md">
      <div class="modal-section">
        <div class="config-group">
          <p style="margin-bottom: 1rem; color: #e0e7ef; line-height: 1.6;">
            Are you sure you want to reset all preprocessing changes?
          </p>
          <p style="margin-bottom: 1rem; color: #94a3b8; line-height: 1.6;">
            This will:
          </p>
          <ul style="color: #94a3b8; margin-left: 1.5rem; line-height: 1.8;">
            <li>Reload the original dataset</li>
            <li>Remove all preprocessing transformations</li>
            <li>Clear missing value handling</li>
            <li>Clear duplicate removal</li>
            <li>Clear outlier handling</li>
            
          </ul>
          <p style="margin-top: 1rem; color: #fbbf24; line-height: 1.6;">
            ⚠️ This action cannot be undone.
          </p>
        </div>
      </div>
      
      <template #footer>
        <Button variant="ghost" @click="showResetModal = false">
          Cancel
        </Button>
        <Button 
          variant="primary" 
          @click="confirmResetAllChanges"
          style="background: #ef4444; border-color: #ef4444;"
        >
          Reset All Changes
        </Button>
      </template>
    </Modal>

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
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useMLDataFlowStore } from "../stores/mlDataFlow";
import { useDataStore } from "../stores/data";
import { useExperimentStore } from "../stores/experiment";
import { useAuthenticatedFetch } from "../composables/useAuthenticatedFetch";
import { useToast } from '~/composables/useToast';

// Components
import Card from "../components/Card.vue";
import Button from "../components/Button.vue";
import Modal from "../components/Modal.vue";

const router = useRouter();
const mlStore = useMLDataFlowStore();
const dataStore = useDataStore();
const experimentStore = useExperimentStore();
const { showSuccess, showError, showInfo, showWarning } = useToast();
const { authenticatedPost } = useAuthenticatedFetch();

// Store Refs
const { backendConnected } = storeToRefs(mlStore);
const { rawPreview: dataset, statistics: dataStats, semanticTypes } = storeToRefs(dataStore);
const { datasetId } = storeToRefs(experimentStore);

// State
const isLoading = ref(true);
const isProcessing = ref(false);
const processingMessage = ref("Processing..."); // Added missing ref
const fileName = ref(""); // Get from store if possible, or keep local if transient

// --- Table State ---
const searchQuery = ref("");
const currentPage = ref(1);
const pageSize = ref(10);
const sortColumn = ref("");
const sortDirection = ref("asc");
const showOriginal = ref(true); // Added missing ref
const showResetModal = ref(false); // Added missing ref

// --- Preprocessing History & Tools ---
const activeTools = ref([]); // Added missing ref (used in template)
const preprocessingHistory = ref([]); // Added missing ref
const preprocessingComplete = ref(true); // Added missing ref

const hasActiveTools = computed(() => activeTools.value.length > 0); // Added missing computed


// --- Preprocessing State ---
const showColumnModal = ref(false);
const showMissingModal = ref(false);
const showOutlierModal = ref(false);
const showDuplicateModal = ref(false);
const showTypeDetectionModal = ref(false); // Added for type detection tool
const isDetectingTypes = ref(false); 
const semanticOverrides = ref({});

// Column State
const columns = ref([]);
const availableColumns = ref([]); 


const missingStats = ref({ count: 0, totalMissing: 0 });
const missingColumnsDetailed = ref([]);
const globalMissingStrategy = ref("droprows");

// Outliers
const outlierStats = ref({ count: 0, columns: 0 });
const outlierStrategy = ref("cap");

// Duplicates
const duplicateStats = ref({ count: 0 });
const duplicateStrategy = ref("keep_first");


// ==================== COMPUTED PROPERTIES ====================

const displayedRowCount = computed(() => {
  // If we have stats from backend, use that for total count, otherwise preview length
  return dataStats.value?.total_rows || dataset.value.length;
});

const dataInfo = computed(() => ({
  columns: columns.value.length,
}));

// Basic Quality Score (Placeholder logic - can be improved with store stats)
const dataQuality = computed(() => {
  if (!dataset.value.length || !columns.value.length) return { score: 100 };
  
  // Use backend stats if available for better accuracy
  if (dataStats.value?.quality_score) {
    return { score: dataStats.value.quality_score };
  }

  // Fallback to simple check on preview data
  const totalCells = dataset.value.length * columns.value.length;
  let issues = 0;
  // Simple check on preview
  return { score: 100 }; // Default for now
});


// Filtered Rows
const filteredRows = computed(() => {
  let rows = dataset.value;

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
      /* eslint-disable eqeqeq */
      if (aVal == bVal) return 0;
      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;
      
      const result = aVal > bVal ? 1 : -1;
      return sortDirection.value === "asc" ? result : -result;
      /* eslint-enable eqeqeq */
    });
  }

  return rows;
});

const totalPages = computed(() => Math.ceil(filteredRows.value.length / pageSize.value));

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredRows.value.slice(start, start + pageSize.value);
});

const startRow = computed(() => (currentPage.value - 1) * pageSize.value + 1);
const endRow = computed(() => Math.min(currentPage.value * pageSize.value, filteredRows.value.length));

const visiblePageNumbers = computed(() => {
    // Simple pagination logic
    const total = totalPages.value;
    const current = currentPage.value;
    const delta = 2;
    const range = [];
    for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
        range.push(i);
    }
    if (current - delta > 2) range.unshift("...");
    if (current + delta < total - 1) range.push("...");
    range.unshift(1);
    if (total > 1) range.push(total);
    return range; 
});

const visibleColumns = computed(() => {
    // Filter out removed columns if we want to hide them, or just show all
    return columns.value.filter(c => !c.remove).map(c => c.name);
});

const hasCleanedData = computed(() => {
    // Check if we have evidence of cleaning
    // dataStore doesn't separate cleaned/original preview yet, just one 'rawPreview'
    // but we can check if preprocessing steps exist in experiment store
    return false; // For now disable toggle till we have diff views
});

// ==================== METHODS ====================

const initializeData = async () => {
  isLoading.value = true;
  try {
    // 1. Check if we have a dataset ID in Experiment Store
    if (!datasetId.value) {
       // Fallback: Check mlStore or localStorage for legacy support
       if (mlStore.datasetId) {
         experimentStore.setDataset(mlStore.datasetId, mlStore.fileName);
       } else {
         const stored = localStorage.getItem('processedData');
         if (stored) {
            const parsed = JSON.parse(stored);
            if (parsed.datasetId) {
                experimentStore.setDataset(parsed.datasetId, parsed.fileName || "Recovered Dataset");
            }
         }
       }
    }

    if (!datasetId.value) {
        // No data found, redirect
        router.push("/"); 
        return;
    }

    // 2. Load Data via DataStore
    await dataStore.loadData(datasetId.value);
    
    // 3. Set Local Metadata
    fileName.value = experimentStore.datasetName || "Dataset";
    processColumns();
    analyzeDataQuality();

  } catch (error) {
    console.error("Initialization error:", error);
    // alert("Failed to load data");
  } finally {
    isLoading.value = false;
  }
};

const processColumns = () => {
  if (!dataset.value.length) return;

  // Use DataStore statistics/types if available
  const stats = dataStats.value?.column_stats || {};
  const types = semanticTypes.value || [];

  const firstRow = dataset.value[0];
  columns.value = Object.keys(firstRow).map(key => {
    // Find backend info
    const stat = Array.isArray(stats) ? stats.find(s => s.name === key) : null;
    const typeInfo = Array.isArray(types) ? types.find(t => t.column === key) : null;

    return {
        name: key,
        type: stat?.type || detectType(dataset.value.map(r => r[key])),
        unique: stat?.unique || 0,
        missing: stat?.missing || 0,
        remove: false, // UI state
        // Add other metadata needed for tools
        semanticType: typeInfo?.semantic_type || (stat?.type === 'numerical' ? 'numeric' : 'categorical')
    };
  });
};

const detectType = (values) => {
    // fast client-side detection fallback
    const nonNull = values.filter(v => v !== null && v !== undefined && v !== "");
    if (!nonNull.length) return "string";
    const isNum = nonNull.every(v => !isNaN(parseFloat(v)) && isFinite(v));
    return isNum ? "number" : "string";
};

const analyzeDataQuality = () => {
    // Calculate stats for tool badges
    // Missing
    let totalMiss = 0;
    let colsWithMiss = 0;
    
    // Outliers (if we have backend metrics)
    let outlierCount = 0;
    
    columns.value.forEach(c => {
        if (c.missing > 0) {
            totalMiss += c.missing;
            colsWithMiss++;
        }
        // Use backend stats from detailed_metrics
        if (dataStats.value?.column_stats) {
            const stat = dataStats.value.column_stats.find(s => s.name === c.name);
            if (stat?.detailed_metrics?.outliers_count) outlierCount += stat.detailed_metrics.outliers_count;
        }
    });

    missingStats.value = { count: colsWithMiss, totalMissing: totalMiss };
    outlierStats.value.count = outlierCount;
    
    // Duplicates from backend stats
    if (dataStats.value?.duplicates !== undefined) {
        duplicateStats.value.count = dataStats.value.duplicates;
    }
    
    // Populate missingColumnsDetailed for modal
    missingColumnsDetailed.value = columns.value
        .filter(c => c.missing > 0)
        .map(c => {
            const currentSType = getColumnSemanticType(c.name);
            return {
                ...c,
                percentage: ((c.missing / displayedRowCount.value) * 100).toFixed(1),
                semanticType: currentSType,
                strategy: currentSType === 'identifier' ? 'droprows' : (currentSType === 'numeric' ? 'fillmean' : 'fillmode')
            };
        });
};

// --- Actions ---

const goBack = () => router.push("dashboard"); // Dashboard
const proceedToTargetSelection = () => router.push("target-selection");

const exportData = () => {
    // Simple CSV export of current visual data
    if (!dataset.value.length) return;
    const headers = visibleColumns.value.join(",");
    const rows = filteredRows.value.map(row => 
        visibleColumns.value.map(col => {
            const val = row[col];
            return val === null ? "" : `"${val}"`;
        }).join(",")
    ).join("\n");
    
    const csvContent = "data:text/csv;charset=utf-8," + headers + "\n" + rows;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${fileName.value}_preview.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};


// --- Modal Actions (Placeholders connecting to backend) ---

// COLUMN SELECTION
const selectNoColumns = () => columns.value.forEach(c => c.remove = false);
const selectAllColumns = () => columns.value.forEach(c => c.remove = true);
const selectIrrelevantColumns = () => {
    // Auto-select ID columns or high cardinality string columns
    columns.value.forEach(c => {
        if (c.semanticType === 'identifier' || (c.unique === displayedRowCount.value && c.type !== 'number')) {
            c.remove = true;
        }
    });
};
const getColumnsToRemove = () => columns.value.filter(c => c.remove);

const applyColumnChanges = async () => {
    isProcessing.value = true;
    try {
        const toDrop = getColumnsToRemove().map(c => c.name);
        if (toDrop.length > 0) {
            await authenticatedPost(`http://localhost:8000/api/datasets/${datasetId.value}/preprocessing/drop-columns`, {
                columns: toDrop
            });
            // Reload data
            await dataStore.loadData(datasetId.value, true);
            // Refresh local columns
            processColumns();
            analyzeDataQuality();
            showSuccess("Columns Dropped", `Removed ${toDrop.length} columns successfully.`);
        }
        showColumnModal.value = false;
    } catch (e) {
        console.error("Drop columns failed", e);
        showError("Drop Failed", "Could not remove selected columns.");
    } finally {
        isProcessing.value = false;
    }
};

const confirmResetAllChanges = async () => {
    isProcessing.value = true;
    try {
        // Find original dataset ID (usually saved in store or part of metadata)
        // For now, if we have an originalDatasetId or similar logic
        // This is a placeholder for actual reset logic
        showResetModal.value = false;
        // Reload data
        await dataStore.loadData(datasetId.value, true);
        showSuccess("Reset Complete", "Dataset reverted to original state.");
    } catch(e) {
        console.error("Reset failed", e);
        showError("Reset Failed", "Could not revert changes.");
    } finally {
        isProcessing.value = false;
    }
};

// MISSING VALUES
const applyGlobalMissingStrategy = () => {
    missingColumnsDetailed.value.forEach(c => {
        // Don't override mandatory ID drops
        if (c.semanticType !== 'identifier') {
            c.strategy = globalMissingStrategy.value;
        }
    });
};
const autoSelectMissingStrategies = () => {
    missingColumnsDetailed.value.forEach(c => {
        if (c.semanticType === 'identifier') c.strategy = 'droprows';
        else if (c.semanticType === 'numeric') c.strategy = 'fillmean';
        else c.strategy = 'fillmode';
    });
};
const applyMissingStrategies = async () => {
    isProcessing.value = true;
    try {
        // Group by strategy
        const strategies = {};
        missingColumnsDetailed.value.forEach(c => {
            if (!strategies[c.strategy]) strategies[c.strategy] = [];
            strategies[c.strategy].push(c.name);
        });

        // Execute API calls sequantially or parallel
        for (const [strategy, cols] of Object.entries(strategies)) {
            // Need specific endpoints or a bulk one. 
            // Assuming generic 'handle-missing' endpoint
            await authenticatedPost(`http://localhost:8000/api/datasets/${datasetId.value}/preprocessing/missing-values`, {
                strategy: strategy, // e.g., 'drop' (rows), 'mean', etc. Map frontend strategy to backend
                columns: cols
            });
        }
        
        await dataStore.loadData(datasetId.value, true);
        processColumns();
        analyzeDataQuality();
        showMissingModal.value = false;
        showSuccess("Missing Values Handled", "Strategies applied successfully.");
    } catch (e) {
        console.error("Missing handling failed", e);
        showError("Processing Failed", "Failed to handle missing values.");
    } finally {
        isProcessing.value = false;
    }
};

// OUTLIERS
const applyOutlierHandling = async () => {
    // If 'keep', just close modal (do nothing)
    if (outlierStrategy.value === 'keep') {
        showOutlierModal.value = false;
        return;
    }

    isProcessing.value = true;
    try {
        await authenticatedPost(`http://localhost:8000/api/datasets/${datasetId.value}/preprocessing/outliers`, {
             method: outlierStrategy.value // 'cap', 'remove'
        });
        await dataStore.loadData(datasetId.value, true);
        // Refresh local columns
        processColumns();
        analyzeDataQuality();
        showOutlierModal.value = false;
        showSuccess("Outliers Processed", `Outliers handled using ${outlierStrategy.value} method.`);
    } catch (e) {
         console.error("Outlier handling failed", e);
         showError("Processing Failed", "Failed to handle outliers.");
    } finally {
        isProcessing.value = false;
    }
};

// DUPLICATES
const applyDuplicateRemoval = async () => {
    isProcessing.value = true;
     try {
        let keepStrategy = 'first';
        if (duplicateStrategy.value === 'keep_last') keepStrategy = 'last';
        else if (duplicateStrategy.value === 'remove_all') keepStrategy = 'all';

        await authenticatedPost(`http://localhost:8000/api/datasets/${datasetId.value}/preprocessing/remove-duplicates`, {
             keep: keepStrategy
        });
        await dataStore.loadData(datasetId.value, true);
        processColumns();
        analyzeDataQuality();
        showDuplicateModal.value = false;
        showSuccess("Duplicates Removed", "Duplicate removal complete.");
    } catch (e) {
         console.error("Duplicate removal failed", e);
         showError("Processing Failed", "Failed to remove duplicates.");
    } finally {
        isProcessing.value = false;
    }
};

// UTILS
const formatCellValue = (val) => {
    if (val === null || val === undefined) return "-";
    if (typeof val === 'number') return val % 1 === 0 ? val : val.toFixed(4);
    return val;
};
const isEncodedColumn = (col) => false; // Placeholder
const getHealthLevel = (score) => {
    if (score > 80) return "good";
    if (score > 50) return "medium";
    return "poor";
};
const sortByColumn = (col) => {
    if (sortColumn.value === col) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn.value = col;
        sortDirection.value = 'asc';
    }
};
const getColumnSample = (col) => {
    return dataset.value.slice(0,3).map(r => r[col.name]).join(", ");
};
const openTypeDetectionModal = () => {
    showTypeDetectionModal.value = true;
};
const getStrategyDescription = (strategy, type) => {
    // Simple helper for hint text
    if (strategy === 'droprows') return "Removes entire row if value missing";
    if (strategy === 'fillmean') return "Fills with average value";
    return "";
};

const getColumnSemanticType = (name) => {
    const col = columns.value.find(c => c.name === name);
    return col?.semanticType || 'unknown';
};

// function removed (duplicate)

const confirmRemoveColumns = async () => {
    // const columnsToRemove = columns.value.filter(c => c.remove).map(c => c.name);
    const columnsToRemove = getColumnsToRemove().map(c => c.name);
    
    if (columnsToRemove.length === 0) return;
    
    // Call API usually, but here we might just simulate or update store
    console.log("Removing columns:", columnsToRemove);
    
    // Update local dataset immediately for preview
    const newDataset = dataset.value.map(row => {
        const newRow = { ...row };
        columnsToRemove.forEach(col => delete newRow[col]);
        return newRow;
    });
    
    // Update store
    dataStore.updateDataset(newDataset);
    
    // Update columns list
    columns.value = columns.value.filter(c => !columnsToRemove.includes(c.name));
    
    // Close modal
    showColumnModal.value = false;
    
    // Record step
    preprocessingHistory.value.push({
        id: Date.now(),
        type: 'feature_selection',
        description: `Removed ${columnsToRemove.length} columns: ${columnsToRemove.join(', ')}`,
        timestamp: new Date()
    });
};

const saveSemanticOverrides = async () => {
    const overrides = semanticTypes.value.filter(st => st.is_override);
    
    if (overrides.length === 0) {
        showInfo("No Changes", "No semantic type overrides were made.");
        showTypeDetectionModal.value = false;
        return;
    }

    isDetectingTypes.value = true;
    try {
        await dataStore.saveSemanticTypes(datasetId.value, overrides);
        
        // Update local columns view to match new semantic types
        processColumns();
        // Refresh quality analysis (recommendations change)
        analyzeDataQuality();
        
        showSuccess("Types Saved", `Updated semantic types for ${overrides.length} columns.`);
        showTypeDetectionModal.value = false;
    } catch (e) {
        console.error("Failed to save types", e);
        showError("Save Failed", "Could not persist semantic type overrides.");
    } finally {
        isDetectingTypes.value = false;
    }
};

const updateMissingStrategy = (name, strategy) => {
    const col = missingColumnsDetailed.value.find(c => c.name === name);
    if(col) col.strategy = strategy;
};

// --- Watchers ---
watch(pageSize, () => {
    currentPage.value = 1;
});

watch(searchQuery, () => {
    currentPage.value = 1;
});

// Sync local view when global semantic types from backend change
watch(semanticTypes, () => {
    console.log("🔄 Semantic types updated in store, re-processing columns...");
    processColumns();
    analyzeDataQuality();
}, { deep: true });

onMounted(() => {
    mlStore.checkBackendConnection();
    initializeData();
});
</script>

<style scoped>
/* Complete CSS - Same as previously provided with additional fixes */

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

/* ============================================
   NEW HERO CARD STYLES
   ============================================ */

.hero-card {
  margin: 2rem 0;
  position: relative;
  overflow: visible;
}

.hero-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.hero-content {
  padding: 2rem;
}

.hero-header-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.hero-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  background: var(--gradient-primary);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-glow-primary);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.hero-icon {
  color: var(--color-text-primary);
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
}

.gradient-text {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 0.5rem 0;
  background: var(--gradient-primary);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.dataset-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.summary-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all var(--transition-fast);
}

.summary-stat:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
}

.stat-icon {
  color: var(--color-primary);
  flex-shrink: 0;
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

.quality-indicator {
  width: 100%;
}

.quality-score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

.quality-icon {
  flex-shrink: 0;
}

.quality-score.excellent {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
  color: var(--color-success);
  border: 1px solid var(--color-success);
}

.quality-score.good {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.1));
  color: var(--color-info);
  border: 1px solid var(--color-info);
}

.quality-score.fair {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.1));
  color: var(--color-warning);
  border: 1px solid var(--color-warning);
}

.quality-score.poor {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.1));
  color: var(--color-error);
  border: 1px solid var(--color-error);
}

@media (max-width: 768px) {
  .hero-header-centered {
    gap: 1.5rem;
  }
  
  .hero-icon-wrapper {
    width: 80px;
    height: 80px;
  }
  
  .gradient-text {
    font-size: var(--font-size-2xl);
  }
  
  .dataset-summary {
    grid-template-columns: 1fr;
  }
}

/* ============================================
   PREPROCESSING TOOL CARDS (REFACTORED)
   ============================================ */

.preprocessing-tool-card {
  transition: all var(--transition-base);
}

.preprocessing-tool-card .tool-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.preprocessing-tool-card .tool-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: var(--gradient-primary);
  border-radius: var(--radius-lg);
  flex-shrink: 0;
}

.preprocessing-tool-card .tool-icon svg {
  color: var(--color-text-primary);
}

.preprocessing-tool-card .tool-info {
  flex: 1;
  min-width: 0;
}

.preprocessing-tool-card .tool-info h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 0.25rem 0;
}

.preprocessing-tool-card .tool-info p {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.preprocessing-tool-card .tool-badge {
  padding: 0.375rem 0.75rem;
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  white-space: nowrap;
}

.preprocessing-tool-card .tool-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

/* ============================================
   COLUMN SELECTION MODAL STYLES
   ============================================ */

.modal-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0;
  width: 100%;
  overflow: hidden;
}

.modal-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.modal-section-header h4 {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin: 0;
}

.quick-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.columns-grid-modal {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  max-height: 60vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem;
  min-width: 0;
  width: 100%;
}

/* Responsive: 3 columns on desktop */
@media (min-width: 1201px) {
  .columns-grid-modal .column-card-modal {
    width: calc(33.333% - 0.67rem);
    flex-shrink: 0;
    flex-grow: 0;
  }
}

/* Responsive: 2 columns on medium screens */
@media (min-width: 769px) and (max-width: 1200px) {
  .columns-grid-modal .column-card-modal {
    width: calc(50% - 0.5rem);
    flex-shrink: 0;
    flex-grow: 0;
  }
}

/* Responsive: 1 column on small screens */
@media (max-width: 768px) {
  .columns-grid-modal .column-card-modal {
    width: 100%;
    flex-shrink: 0;
    flex-grow: 0;
  }
}

.columns-grid-modal * {
  box-sizing: border-box;
}

.column-card-modal {
  position: relative;
  transition: all var(--transition-fast);
  box-sizing: border-box;
}

/* Force Card component to maintain width */
.column-card-modal :deep(.card) {
  width: 100% !important;
  min-width: 0 !important;
  max-width: 100% !important;
  flex-shrink: 0 !important;
}

.column-card-modal :deep(.card-body) {
  width: 100% !important;
  min-width: 0 !important;
}

.column-card-modal.column-to-remove {
  opacity: 0.6;
  border-color: var(--color-error);
}

.column-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.column-checkbox-native {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.checkbox-input {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  cursor: pointer;
  accent-color: var(--color-primary, #667eea);
}

.checkbox-label {
  flex: 1;
  min-width: 0;
  font-size: var(--font-size-base, 1rem);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-primary, #ffffff);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.column-type-badge {
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  white-space: nowrap;
}

.column-type-badge.type-numeric,
.column-type-badge.type-int64,
.column-type-badge.type-float64 {
  background: rgba(59, 130, 246, 0.2);
  color: var(--color-info);
  border: 1px solid var(--color-info);
}

.column-type-badge.type-object,
.column-type-badge.type-string {
  background: rgba(245, 158, 11, 0.2);
  color: var(--color-warning);
  border: 1px solid var(--color-warning);
}

.column-type-badge.type-bool,
.column-type-badge.type-boolean {
  background: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}

.column-card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 0;
  width: 100%;
}

.column-stats-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.stat-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.stat-chip svg {
  flex-shrink: 0;
}

.stat-chip.missing {
  background: rgba(239, 68, 68, 0.1);
  color: var(--color-error);
}

.column-sample {
  display: flex;
  gap: 0.5rem;
  font-size: var(--font-size-xs);
}

.sample-label {
  color: var(--color-text-tertiary);
  font-weight: var(--font-weight-medium);
}

.sample-value {
  color: var(--color-text-secondary);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.column-rename-input-native {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-md, 8px);
  color: var(--color-text-primary, #ffffff);
  font-size: var(--font-size-sm, 0.875rem);
  font-family: var(--font-primary);
  transition: all var(--transition-fast, 150ms);
  outline: none;
  box-sizing: border-box;
}

.column-rename-input-native::placeholder {
  color: var(--color-text-tertiary, #8b8ba7);
}

.column-rename-input-native:focus {
  border-color: var(--color-primary, #667eea);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.column-remove-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: var(--color-error);
  color: var(--color-text-primary);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  z-index: 1;
}

.selection-summary-modal {
  margin-top: 1rem;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-warning);
}

.removal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.removal-tag {
  padding: 0.375rem 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--color-error);
}

/* ============================================
   MISSING VALUES MODAL STYLES
   ============================================ */

/* Flexbox Grid Pattern (Prevents Shrinking) */
.columns-flex-modal {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  max-height: 60vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem;
  min-width: 0;
  width: 100%;
}

/* Responsive: 3 columns on desktop */
@media (min-width: 1201px) {
  .columns-flex-modal .column-card-modal {
    width: calc(33.333% - 0.67rem);
    flex-shrink: 0;
    flex-grow: 0;
  }
}

/* Responsive: 2 columns on medium screens */
@media (min-width: 769px) and (max-width: 1200px) {
  .columns-flex-modal .column-card-modal {
    width: calc(50% - 0.5rem);
    flex-shrink: 0;
    flex-grow: 0;
  }
}

/* Responsive: 1 column on small screens */
@media (max-width: 768px) {
  .columns-flex-modal .column-card-modal {
    width: 100%;
    flex-shrink: 0;
    flex-grow: 0;
  }
}

.columns-flex-modal * {
  box-sizing: border-box;
}

/* Force Card component to maintain width in flex grid */
.columns-flex-modal :deep(.card) {
  width: 100% !important;
  min-width: 0 !important;
  max-width: 100% !important;
  flex-shrink: 0 !important;
}

.columns-flex-modal :deep(.card-body) {
  width: 100% !important;
  min-width: 0 !important;
}

/* Global Strategy Section */
.global-strategy-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.global-controls {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

/* Native Select Styling */
.native-select-global,
.native-select-strategy {
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-md, 8px);
  color: var(--color-text-primary, #ffffff);
  font-size: var(--font-size-sm, 0.875rem);
  font-family: var(--font-primary);
  transition: all var(--transition-fast, 150ms);
  outline: none;
  cursor: pointer;
}

.native-select-global {
  flex: 1;
  min-width: 200px;
}

.native-select-strategy {
  width: 100%;
  margin-top: 0.5rem;
}

.native-select-global:focus,
.native-select-strategy:focus {
  border-color: var(--color-primary, #667eea);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.native-select-global option,
.native-select-strategy option {
  background: #1a1a2e; /* Fallback dark background */
  color: #ffffff;
}

/* Missing Column Card Specifics */
.missing-column-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.column-name-text {
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.missing-stats-row {
  display: flex;
  gap: 0.5rem;
}

.strategy-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-top: 0.25rem;
  min-height: 1.2em; /* Prevent layout shift */
}

.no-data-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  gap: 1rem;
}

.no-data-message h4 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin: 0;
}

.no-data-message p {
  color: var(--color-text-secondary);
  margin: 0;
}

/* ============================================
   DUPLICATES MODAL STYLES
   ============================================ */

.duplicate-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-stat strong {
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
}

.info-stat p {
  margin: 0;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
}

.strategy-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.strategy-options h4 {
  margin: 0 0 0.5rem 0;
  font-size: var(--font-size-md);
  color: var(--color-text-primary);
}

.radio-option {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.radio-option:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--color-primary-light);
}

.radio-option:has(input:checked) {
  background: rgba(102, 126, 234, 0.1);
  border-color: var(--color-primary);
}

.native-radio {
  margin-top: 0.25rem;
  accent-color: var(--color-primary);
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.option-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.option-content strong {
  color: var(--color-text-primary);
  font-size: var(--font-size-md);
}

.option-content p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.warning-content {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  color: #fbbf24; /* Warning color */
}

.warning-content strong {
  color: #f59e0b;
}

/* Reset Modal Styles */
.reset-info {
  margin-top: 1.5rem;
}

.reset-info h4 {
  margin: 0 0 1rem 0;
  color: var(--color-text-primary);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
}

.reset-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reset-list li {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  padding-left: 0.5rem;
}

.reset-note {
  margin: 1rem 0 0 0;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border-left: 3px solid var(--color-error);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

/* Preprocessing Order Guidance Styles */
.preprocessing-help-section {
  margin-bottom: 2rem;
}

.help-details {
  cursor: pointer;
}

.help-summary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  list-style: none;
  cursor: pointer;
  user-select: none;
}

.help-summary::-webkit-details-marker {
  display: none;
}

.help-icon {
  color: var(--color-info);
  flex-shrink: 0;
}

.chevron-icon {
  margin-left: auto;
  color: var(--color-text-tertiary);
  transition: transform var(--transition-normal);
  flex-shrink: 0;
}

.help-details[open] .chevron-icon {
  transform: rotate(180deg);
}

.help-content {
  padding: 1rem 0 0.5rem 0;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.help-list {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.help-list li {
  margin-bottom: 0.75rem;
}

.recommended-order-box {
  background: rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  margin-top: 1.5rem;
}

.order-title {
  margin: 0 0 1rem 0;
  color: var(--color-text-primary);
}

.order-list {
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
  list-style: none;
  counter-reset: order-counter;
}

.order-list li {
  counter-increment: order-counter;
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

.order-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
  font-size: 0.875rem;
  font-weight: 600;
  margin-right: 0.75rem;
}

.order-note {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

/* Order Badges on Tool Cards */
.tool-badges-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.order-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.order-badge.order-1 {
  background: linear-gradient(135deg, #10b981, #059669);
}

.order-badge.order-2 {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.order-badge.order-3 {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

/* Success Badge for No Issues Found */
.success-badge {
  background: rgba(16, 185, 129, 0.1) !important;
  color: #10b981 !important;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.continue-btn {
  animation: none !important;
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

/* Compact Hero Overrides */
.hero-header-centered {
  margin-bottom: 1.5rem !important;
  gap: 0.5rem !important;
}

.hero-content {
  padding: 1.5rem !important;
}


/* ==================== TYPE DETECTION UI ==================== */
.type-pill.numeric { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.type-pill.categorical { background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }
.type-pill.boolean { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
.type-pill.datetime { background: rgba(244, 63, 185, 0.15); color: #f472b6; border: 1px solid rgba(244, 63, 185, 0.3); }
.type-pill.identifier { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

.confidence-badge.high { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.confidence-badge.medium { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.confidence-badge.low { background: rgba(239, 68, 68, 0.2); color: #f87171; }

.tr.is-overridden {
  background: rgba(16, 185, 129, 0.05);
}

.step-badge {
  font-size: 0.65rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  margin-left: 0.5rem;
  vertical-align: middle;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

</style>
