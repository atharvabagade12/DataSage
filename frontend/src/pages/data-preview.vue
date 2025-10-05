<template>
  <div class="data-preview">
    <!-- Navigation Header -->
    <nav class="preview-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
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

      <!-- ✅ MOVED OUTSIDE nav-left, INSIDE nav -->
      <div class="backend-status" v-if="backendConnected !== null">
        <div class="status-indicator" :class="{ connected: backendConnected, disconnected: !backendConnected }">
          <div class="status-dot"></div>
          <span class="status-text">
            {{ backendConnected ? 'ML Backend Ready' : 'Frontend Mode' }}
          </span>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🛠️</div>
        <h1>Data Preprocessing</h1>
        <p>Clean and prepare your dataset for machine learning</p>
        <div class="dataset-summary">
          <span class="summary-item"><strong>{{ fileName }}</strong> Dataset</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ formatNumber(dataInfo.rows) }} rows</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ dataInfo.columns }} columns</span>
          <div class="quality-indicator">
            <div class="quality-score" :class="getHealthLevel(dataQuality.score)">
              {{ dataQuality.score }}% Quality
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Container -->
    <div class="main-container">
      <!-- Data Table Preview Section -->
      <section class="table-preview-section">
        <div class="section-header">
          <h2>Data Preview</h2>
          <div class="preview-controls">
            <button @click="showOriginal = true" :class="{ active: showOriginal }" class="preview-toggle">
              Original Data
            </button>
            <button @click="showOriginal = false" :class="{ active: !showOriginal }" class="preview-toggle" :disabled="!hasCleanedData">
              Cleaned Data
            </button>
            <div v-if="hasCleanedData" class="data-stats">
              <span class="stat">{{ cleanedDataset.length }} rows</span>
              <span class="stat">{{ getCleanedColumns().length }} columns</span>
              <span class="stat">{{ finalQuality }}% quality</span>
            </div>
          </div>
        </div>

        <!-- Table Container -->
        <div class="table-container">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <span class="table-info">
                Showing {{ startRow }} to {{ endRow }} of {{ filteredRows.length }} rows
              </span>
            </div>
            <div class="toolbar-right">
              <div class="search-box">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
                <input v-model="searchQuery" type="text" placeholder="Search data..." class="search-input" />
              </div>
              <button @click="exportData" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
                </svg>
                Export CSV
              </button>
            </div>
          </div>

          <div class="data-table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th v-for="column in visibleColumns" :key="column" class="table-header-cell">
                    <div class="header-content">
                      <span>{{ column }}</span>
                      <button @click="sortByColumn(column)" class="sort-button">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M7,15L12,10L17,15H7Z" />
                        </svg>
                      </button>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in paginatedRows" :key="index" class="table-row">
                  <td v-for="column in visibleColumns" :key="column" class="table-cell">
                    <div class="cell-content">
                      {{ formatCellValue(row[column]) }}
                      <span v-if="isEncodedColumn(column)" class="encoded-badge">Encoded</span>
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
              <button @click="currentPage = Math.max(1, currentPage - 1)" :disabled="currentPage === 1" class="page-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z" />
                </svg>
                Previous
              </button>

              <div class="page-numbers">
                <button v-for="page in visiblePageNumbers" :key="page" @click="currentPage = page" :class="{ active: currentPage === page }" class="page-number">
                  {{ page }}
                </button>
              </div>

              <button @click="currentPage = Math.min(totalPages, currentPage + 1)" :disabled="currentPage === totalPages" class="page-btn">
                Next
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" />
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
          <p class="section-description">Select and configure preprocessing steps to clean your data</p>
        </div>

        <div class="preprocessing-grid">

          <!-- Column Selection Tool - FIXED WITH DROPDOWN STATE MANAGEMENT -->
          <div class="preprocessing-tool" :class="{ 
            active: isToolEnabled('columnSelection'),
            expanded: isDropdownOpen('columnSelection')
          }">
            <div class="tool-header">
              <div class="tool-info">
                <h3>Column Selection</h3>
                <p>Remove irrelevant columns (IDs, names, URLs) that don't help in learning</p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge">{{ columns.length }} columns</span>
                
                <!-- ✅ NEW: Separate Configure/Close button -->
                <button 
                  @click="toggleDropdown('columnSelection')" 
                  class="config-btn"
                  :class="{ active: isDropdownOpen('columnSelection') }"
                  v-if="isToolEnabled('columnSelection')"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path v-if="!isDropdownOpen('columnSelection')" d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"/>
                    <path v-else d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"/>
                  </svg>
                  {{ isDropdownOpen('columnSelection') ? 'Close' : 'Configure' }}
                </button>
                
                
                <button 
                  @click="isToolEnabled('columnSelection') ? disableTool('columnSelection') : enableTool('columnSelection')" 
                  class="tool-btn"
                  :class="{ active: isToolEnabled('columnSelection') }"
                >
                  {{ isToolEnabled('columnSelection') ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>

           
            <div v-if="isDropdownOpen('columnSelection')" class="tool-config">
              <div class="config-header">
                <h4>Select columns to REMOVE from dataset:</h4>
                <div class="config-actions">
                  <button @click="selectNoColumns" class="action-link">Remove None</button>
                  <button @click="selectIrrelevantColumns" class="action-btn small">Auto-select Irrelevant</button>
                  <button @click="selectAllColumns" class="action-link danger">Remove All</button>
                  
                 
                  <button @click="resetToolSettingsColumnSelection('columnSelection')" class="reset-btn small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"/>
                    </svg>
                    Reset
                  </button>
                </div>
              </div>

              <div class="columns-grid">
                <label v-for="column in columns" :key="column.name" class="column-card" :class="{ 'to-remove': column.remove }">
                  <input type="checkbox" v-model="column.remove" :value="column.name" />
                  <div class="column-content">
                    <div class="column-header">
                      <span class="column-name">{{ column.name }}</span>
                      <span class="column-type" :class="column.type">{{ column.type }}</span>
                      <span v-if="column.remove" class="remove-badge">Will Remove</span>
                    </div>
                    <div class="column-stats">
                      <span class="stat-item">{{ column.unique }} unique</span>
                      <span v-if="column.missing > 0" class="stat-item missing">{{ column.missing }} missing</span>
                    </div>
                    <div class="column-sample">
                      <span class="sample-label">Sample:</span>
                      <span class="sample-text">{{ getColumnSample(column) }}</span>
                    </div>
                  </div>
                </label>
              </div>

             
              <div class="selection-summary">
                <div class="summary-stats">
                  <span class="summary-stat keep">{{ getColumnsToKeep().length }} columns to keep</span>
                  <span class="summary-stat remove">{{ getColumnsToRemove().length }} columns to remove</span>
                </div>
                <div v-if="getColumnsToRemove().length > 0" class="removal-list">
                  <span class="removal-label">Will remove:</span>
                  <div class="removal-tags">
                    <span v-for="col in getColumnsToRemove()" :key="col.name" class="removal-tag">
                      {{ col.name }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- ✅ NEW: Dropdown footer with actions -->
              <div class="dropdown-footer">
                <button @click="toggleDropdown('columnSelection')" class="close-dropdown-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>

          
          <!-- Missing Values Tool - ENHANCED PER-COLUMN STRATEGY -->
          <div 
            class="preprocessing-tool" 
            :class="{ 
              'active': isToolEnabled('missingValues'), 
              'expanded': isDropdownOpen('missingValues') 
            }"
          >
            <div class="tool-header">
              <div class="tool-info">
                <h3>Handle Missing Values</h3>
                <p>Choose strategy for each column with missing values</p>
              </div>
              
              <div class="tool-actions">
                <span v-if="missingStats.count > 0" class="tool-badge">
                  {{ missingStats.count }} columns affected
                </span>
                
                <button 
                  @click="toggleDropdown('missingValues')" 
                  class="config-btn"
                  :class="{ 'active': isDropdownOpen('missingValues') }"
                  v-if="isToolEnabled('missingValues')"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path v-if="!isDropdownOpen('missingValues')" d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z" />
                    <path v-else d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z" />
                  </svg>
                  {{ isDropdownOpen('missingValues') ? 'Close' : 'Configure' }}
                </button>
                
                <button 
                  @click="isToolEnabled('missingValues') ? disableTool('missingValues') : enableTool('missingValues')"
                  class="tool-btn"
                  :class="{ 'active': isToolEnabled('missingValues') }"
                >
                  {{ isToolEnabled('missingValues') ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>
            
            <!-- Configuration Dropdown -->
            <div v-if="isDropdownOpen('missingValues')" class="tool-config">
              <!-- Missing Columns List -->
              <div v-if="missingColumnsDetailed.length > 0" class="missing-columns-config">
                <div class="config-header">
                  <h4>Select strategy for each column</h4>
                  <div class="config-actions">
                    <button @click="applyGlobalMissingStrategy" class="action-btn small">
                      Apply "{{ getStrategyName(globalMissingStrategy) }}" to All
                    </button>
                    <button @click="autoSelectMissingStrategies" class="action-btn small">
                      Auto-select Strategies
                    </button>
                    <button @click="resetToolSettingsMissingValues('missingValues')" class="reset-btn small">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
                      </svg>
                      Reset
                    </button>
                  </div>
                </div>
                
                <!-- Global Strategy Selector -->
                <div class="global-strategy-selector">
                  <label class="global-strategy-label">
                    <span>Global Strategy (apply to all):</span>
                    <select v-model="globalMissingStrategy" class="strategy-select">
                      <option value="droprows">Drop Rows with Missing Values</option>
                      <option value="fillmean">Fill with Mean (numerical only)</option>
                      <option value="fillmedian">Fill with Median (numerical only)</option>
                      <option value="fillmode">Fill with Most Frequent Value</option>
                      <option value="fillzero">Fill with Zero</option>
                      <option value="fillunknown">Fill with "Unknown"</option>
                    </select>
                  </label>
                </div>
                
                <!-- Individual Column Strategies -->
                <div class="missing-columns-list">
                  <div 
                    v-for="col in missingColumnsDetailed" 
                    :key="col.name" 
                    class="missing-column-row"
                  >
                    <!-- Column Info -->
                    <div class="column-info-section">
                      <div class="column-header">
                        <span class="column-name">{{ col.name }}</span>
                        <span class="column-type" :class="col.type">{{ col.type }}</span>
                      </div>
                      <div class="missing-stats">
                        <span class="stat-badge missing">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
                          </svg>
                          {{ col.count }} missing ({{ col.percentage }}%)
                        </span>
                      </div>
                    </div>
                    
                    <!-- Strategy Selector -->
                    <div class="strategy-selector-section">
                      <select 
                        v-model="col.strategy" 
                        @change="updateMissingStrategy(col.name, col.strategy)"
                        class="column-strategy-select"
                        :class="getStrategyClass(col.strategy)"
                      >
                        <option value="droprows">❌ Drop Rows</option>
                        <option value="fillmean" :disabled="col.type !== 'numerical'">
                          📊 Fill with Mean {{ col.type !== 'numerical' ? '(numerical only)' : '' }}
                        </option>
                        <option value="fillmedian" :disabled="col.type !== 'numerical'">
                          📈 Fill with Median {{ col.type !== 'numerical' ? '(numerical only)' : '' }}
                        </option>
                        <option value="fillmode">🔢 Fill with Mode (most frequent)</option>
                        <option value="fillzero">0️⃣ Fill with Zero</option>
                        <option value="fillunknown">❓ Fill with "Unknown"</option>
                        <option value="keep">⚠️ Keep Missing (not recommended)</option>
                      </select>
                      
                      <!-- Strategy Description -->
                      <span class="strategy-hint">{{ getStrategyDescription(col.strategy, col.type) }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Summary -->
                <div class="missing-summary">
                  <div class="summary-stats">
                    <span class="summary-stat">
                      <strong>{{ missingColumnsDetailed.length }}</strong> columns with missing values
                    </span>
                    <span class="summary-divider">•</span>
                    <span class="summary-stat">
                      <strong>{{ missingStats.totalMissing }}</strong> total missing cells
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- No Missing Values -->
              <div v-else class="no-missing-values">
                <div class="no-missing-icon">✅</div>
                <h4>No Missing Values Found!</h4>
                <p>Your dataset doesn't have any missing values. You can skip this step.</p>
              </div>
              
              <!-- Dropdown Footer -->
              <div class="dropdown-footer">
                <button @click="toggleDropdown('missingValues')" class="close-dropdown-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>


          <!-- Duplicate Removal Tool - SAME PATTERN -->
          <div class="preprocessing-tool" :class="{ 
            active: isToolEnabled('duplicateRemoval'),
            expanded: isDropdownOpen('duplicateRemoval')
          }">
            <div class="tool-header">
              <div class="tool-info">
                <h3>Remove Duplicates</h3>
                <p>Remove duplicate rows from your dataset</p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge" v-if="duplicateStats.count > 0">{{ duplicateStats.count }} duplicates found</span>
                
                <button 
                  @click="toggleDropdown('duplicateRemoval')" 
                  class="config-btn"
                  :class="{ active: isDropdownOpen('duplicateRemoval') }"
                  v-if="isToolEnabled('duplicateRemoval')"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path v-if="!isDropdownOpen('duplicateRemoval')" d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"/>
                    <path v-else d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"/>
                  </svg>
                  {{ isDropdownOpen('duplicateRemoval') ? 'Close' : 'Configure' }}
                </button>
                
                <button 
                  @click="isToolEnabled('duplicateRemoval') ? disableTool('duplicateRemoval') : enableTool('duplicateRemoval')" 
                  class="tool-btn"
                  :class="{ active: isToolEnabled('duplicateRemoval') }"
                >
                  {{ isToolEnabled('duplicateRemoval') ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>

            <div v-if="isDropdownOpen('duplicateRemoval')" class="tool-config">
              <div class="strategy-selector">
                <h4>Choose duplicate handling strategy:</h4>
                <div class="strategy-grid">
                  <label class="strategy-card" :class="{ selected: duplicateStrategy === 'keep_first' }">
                    <input type="radio" v-model="duplicateStrategy" value="keep_first" />
                    <div class="strategy-content">
                      <div class="strategy-icon">⬆️</div>
                      <h5>Keep First</h5>
                      <p>Keep the first occurrence of duplicate rows</p>
                    </div>
                  </label>

                  <label class="strategy-card" :class="{ selected: duplicateStrategy === 'keep_last' }">
                    <input type="radio" v-model="duplicateStrategy" value="keep_last" />
                    <div class="strategy-content">
                      <div class="strategy-icon">⬇️</div>
                      <h5>Keep Last</h5>
                      <p>Keep the last occurrence of duplicate rows</p>
                    </div>
                  </label>
                </div>
              </div>

              <div class="dropdown-footer">
                <button @click="toggleDropdown('duplicateRemoval')" class="close-dropdown-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>

          <!-- Outlier Handling Tool - SAME PATTERN -->
          <div class="preprocessing-tool" :class="{ 
            active: isToolEnabled('outlierHandling'),
            expanded: isDropdownOpen('outlierHandling')
          }">
            <div class="tool-header">
              <div class="tool-info">
                <h3>Handle Outliers</h3>
                <p>Detect and handle extreme values in numerical columns</p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge" v-if="outlierStats.count > 0">{{ outlierStats.count }} outliers detected</span>
                
                <button 
                  @click="toggleDropdown('outlierHandling')" 
                  class="config-btn"
                  :class="{ active: isDropdownOpen('outlierHandling') }"
                  v-if="isToolEnabled('outlierHandling')"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path v-if="!isDropdownOpen('outlierHandling')" d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"/>
                    <path v-else d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"/>
                  </svg>
                  {{ isDropdownOpen('outlierHandling') ? 'Close' : 'Configure' }}
                </button>
                
                <button 
                  @click="isToolEnabled('outlierHandling') ? disableTool('outlierHandling') : enableTool('outlierHandling')" 
                  class="tool-btn"
                  :class="{ active: isToolEnabled('outlierHandling') }"
                >
                  {{ isToolEnabled('outlierHandling') ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>

            <div v-if="isDropdownOpen('outlierHandling')" class="tool-config">
              <div class="strategy-selector">
                <h4>Select outlier handling method:</h4>
                <div class="strategy-grid">
                  <label class="strategy-card" :class="{ selected: outlierStrategy === 'remove' }">
                    <input type="radio" v-model="outlierStrategy" value="remove" />
                    <div class="strategy-content">
                      <div class="strategy-icon">❌</div>
                      <h5>Remove Outliers</h5>
                      <p>Remove rows containing outlier values</p>
                    </div>
                  </label>

                  <label class="strategy-card" :class="{ selected: outlierStrategy === 'cap' }">
                    <input type="radio" v-model="outlierStrategy" value="cap" />
                    <div class="strategy-content">
                      <div class="strategy-icon">📏</div>
                      <h5>Cap Outliers</h5>
                      <p>Limit outliers to reasonable bounds</p>
                    </div>
                  </label>

                  <label class="strategy-card" :class="{ selected: outlierStrategy === 'keep' }">
                    <input type="radio" v-model="outlierStrategy" value="keep" />
                    <div class="strategy-content">
                      <div class="strategy-icon">✅</div>
                      <h5>Keep Outliers</h5>
                      <p>Keep all values, just flag them</p>
                    </div>
                  </label>
                </div>
              </div>

              <div class="dropdown-footer">
                <button @click="toggleDropdown('outlierHandling')" class="close-dropdown-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>

          <!-- Categorical Encoding Tool - ENHANCED -->
          <div class="preprocessing-tool" :class="{ 
            active: isToolEnabled('categoricalEncoding'),
            expanded: isDropdownOpen('categoricalEncoding')
          }">
            <div class="tool-header">
              <div class="tool-info">
                <h3>Encode Categorical Data</h3>
                <p>Convert categorical text data to numbers for machine learning</p>
              </div>
              <div class="tool-actions">
                <span class="tool-badge">{{ categoricalColumns.length }} categorical columns</span>
                
                <button 
                  @click="toggleDropdown('categoricalEncoding')" 
                  class="config-btn"
                  :class="{ active: isDropdownOpen('categoricalEncoding') }"
                  v-if="isToolEnabled('categoricalEncoding')"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path v-if="!isDropdownOpen('categoricalEncoding')" d="M12,18.17L8.83,15L7.42,16.41L12,21L16.58,16.41L15.17,15M12,5.83L15.17,9L16.58,7.59L12,3L7.42,7.59L8.83,9L12,5.83Z"/>
                    <path v-else d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"/>
                  </svg>
                  {{ isDropdownOpen('categoricalEncoding') ? 'Close' : 'Configure' }}
                </button>
                
                <button 
                  @click="isToolEnabled('categoricalEncoding') ? disableTool('categoricalEncoding') : enableTool('categoricalEncoding')" 
                  class="tool-btn"
                  :class="{ active: isToolEnabled('categoricalEncoding') }"
                >
                  {{ isToolEnabled('categoricalEncoding') ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>

            <div v-if="isDropdownOpen('categoricalEncoding')" class="tool-config">
              <div class="encoding-config">
                <h4>Choose which categorical columns to encode:</h4>
                <div class="encoding-list">
                  <div v-for="column in categoricalColumns" :key="column.name" class="encoding-row">
                    
                    <!-- ✅ FIXED: Checkbox to enable/disable encoding for this column -->
                    <label class="encoding-checkbox">
                      <input type="checkbox" v-model="column.encode" />
                      <div class="column-details">
                        <span class="column-name">{{ column.name }}</span>
                        <span class="column-info">{{ column.unique }} unique values</span>
                        <div class="sample-values">
                          <span class="sample-label">Sample:</span>
                          <span class="sample-text">{{ getColumnSample(column) }}</span>
                        </div>
                      </div>
                    </label>

                    <!-- Only show encoding selector if column is selected for encoding -->
                    <div v-if="column.encode" class="encoding-selector">
                      <select v-model="column.encoding" class="encoding-select">
                        <option value="onehot">One-Hot Encoding</option>
                        <option value="label">Label Encoding</option>
                        <option value="ordinal">Ordinal Encoding</option>
                      </select>
                    </div>
                    <div v-else class="not-encoded">
                      <span class="not-encoded-text">Will keep original values</span>
                    </div>
                  </div>
                </div>

                <!-- ✅ Quick selection buttons -->
                <div class="encoding-actions">
                  <button @click="selectAllCategoricalColumns" class="action-btn small">Select All</button>
                  <button @click="deselectAllCategoricalColumns" class="action-btn small">Select None</button>
                  <button @click="autoSelectForEncoding" class="action-btn small">Auto-select (exclude likely targets)</button>
                </div>
              </div>

              <div class="dropdown-footer">
                <button @click="toggleDropdown('categoricalEncoding')" class="close-dropdown-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                  </svg>
                  Close Configuration
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- Skip Preprocessing Section -->
        <div class="skip-section" v-if="!hasActiveTools">
          <div class="skip-content">
            <h3>Skip Preprocessing</h3>
            <p>Your data looks good as-is? You can skip preprocessing and use the original dataset for machine learning.</p>
            <button @click="proceedToTargetSelection" class="skip-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z" />
              </svg>
              Skip to Target Selection
            </button>
          </div>
        </div>

        <!-- Apply Changes Section - ENHANCED -->
        <div class="apply-section" v-if="hasActiveTools">
          <div class="apply-summary">
            <h3>Ready to Apply {{ activeTools.length }} Change{{ activeTools.length > 1 ? 's' : '' }}</h3>
            <div class="changes-preview">
              <div v-for="tool in activeTools" :key="tool" class="change-item">
                <span class="change-icon">✓</span>
                <span class="change-text">{{ getToolName(tool) }}</span>
                <span class="change-config">{{ getToolConfig(tool) }}</span>
                
                <!-- ✅ NEW: Individual tool controls -->
                <div class="change-actions">
                  <button @click="toggleDropdown(tool)" class="change-edit-btn" :title="`Configure ${getToolName(tool)}`">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"/>
                    </svg>
                  </button>
                  <button @click="disableTool(tool)" class="change-remove-btn" :title="`Remove ${getToolName(tool)}`">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="apply-buttons">
            <button @click="resetAllChanges" class="reset-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z" />
              </svg>
              Reset All
            </button>
            <button @click="applyChanges" class="apply-btn primary" :disabled="isProcessing || !hasActiveTools" :class="{ loading: isProcessing }">
              <span v-if="isProcessing">
                <div class="btn-spinner"></div>
                Processing...
              </span>
              <span v-else>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                </svg>
                Apply {{ activeTools.length }} Change{{ activeTools.length > 1 ? 's' : '' }}
              </span>
            </button>
          </div>
        </div>

      </section>
    </div>

    <!-- Action Footer -->
    <div class="action-footer">
      <div class="footer-content">
        <!-- Processing Status -->
        <div class="processing-status">
          <div v-if="hasCleanedData" class="processing-complete">
            <div class="success-icon">✅</div>
            <div class="success-text">
              <h3>Dataset Successfully Cleaned!</h3>
              <p>Your data is now ready for machine learning model training</p>
            </div>
          </div>

          <div v-else class="processing-original">
            <div class="original-icon">📊</div>
            <div class="original-text">
              <h3>Original Dataset Ready</h3>
              <p>You can proceed with the original data or apply preprocessing steps first</p>
            </div>
          </div>
        </div>

        <!-- Dataset Stats -->
        <div class="final-stats">
          <div class="stat-item">
            <span class="stat-value">{{ hasCleanedData ? cleanedDataset.length : originalDataset.length }}</span>
            <span class="stat-label">{{ hasCleanedData ? 'Final' : 'Original' }} Rows</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ hasCleanedData ? getCleanedColumns().length : columns.length }}</span>
            <span class="stat-label">{{ hasCleanedData ? 'Final' : 'Original' }} Columns</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ hasCleanedData ? finalQuality : dataQuality.score }}%</span>
            <span class="stat-label">Data Quality</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="footer-actions">
          <button v-if="hasCleanedData" @click="resetAllChanges" class="footer-btn secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z" />
            </svg>
            Reset Changes
          </button>

          <!-- Always show the Continue button -->
          <button @click="proceedToTargetSelection" class="footer-btn primary">
            <span>{{ hasCleanedData ? 'Continue with Cleaned Data' : 'Continue with Original Data' }}</span>
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
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useMLDataFlowStore } from '~/stores/mlDataFlow'
const mlStore = useMLDataFlowStore()

const router = useRouter();

const backendConnected = computed(() => mlStore.backendConnected)

// ===== DATA STATE =====
const isProcessing = ref(false);
const isApplyingPreprocessing = ref(false); // NEW
const processingMessage = ref("");
const fileName = ref("");
const fileSize = ref(0);
const originalDataset = ref([]);
const cleanedDataset = ref([]);
const columns = ref([]);
const showOriginal = ref(true);
const searchQuery = ref("");
const currentPage = ref(1);
const pageSize = ref(25);
const sortColumn = ref("");
const sortDirection = ref("asc");
const datasetId = ref(""); 
const originalDatasetBackup = ref([])

// ===== PREPROCESSING CONFIG =====
const missingValuesConfig = ref({}) 
const missingColumnsDetailed = ref([]) // NOW A REF (populated from backend)
const globalMissingStrategy = ref('fillmean')

const activeTools = ref([]);
const openDropdowns = ref([])
const missingStrategy = ref("fill_mean");
const duplicateStrategy = ref("keep_first");
const outlierStrategy = ref("cap");

// ===== COMPUTED PROPERTIES =====
const dataInfo = computed(() => ({
  rows: originalDataset.value.length,
  columns: columns.value.length,
}));

const dataQuality = computed(() => {
  if (!originalDataset.value.length || !columns.value.length)
    return { score: 0 };

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

const categoricalColumns = computed(() => {
  return columns.value.filter((col) => col.type === "categorical");
});

const duplicateStats = computed(() => {
  const seen = new Set();
  let count = 0;

  originalDataset.value.forEach((row) => {
    const rowString = JSON.stringify(row);
    if (seen.has(rowString)) {
      count++;
    } else {
      seen.add(rowString);
    }
  });

  return { count };
});

const missingStats = computed(() => {
  return {
    count: missingColumnsDetailed.value.length,
    totalMissing: missingColumnsDetailed.value.reduce((sum, col) => sum + col.count, 0)
  }
})

const outlierStats = computed(() => {
  let count = 0;
  columns.value
    .filter((col) => col.type === "numerical")
    .forEach((col) => {
      const values = originalDataset.value
        .map((row) => parseFloat(row[col.name]))
        .filter((val) => !isNaN(val));

      if (values.length > 0) {
        const q1 = values.sort()[Math.floor(values.length * 0.25)];
        const q3 = values[Math.floor(values.length * 0.75)];
        const iqr = q3 - q1;
        const lowerBound = q1 - 1.5 * iqr;
        const upperBound = q3 + 1.5 * iqr;

        count += values.filter(
          (val) => val < lowerBound || val > upperBound
        ).length;
      }
    });

  return { count };
});

const hasCleanedData = computed(() => {
  return cleanedDataset.value && cleanedDataset.value.length > 0
})

const finalQuality = computed(() => {
  if (!hasCleanedData.value) return dataQuality.value.score;

  const cleanedColumns = getCleanedColumns();
  const totalCells = cleanedDataset.value.length * cleanedColumns.length;
  let issues = 0;

  cleanedDataset.value.forEach((row) => {
    cleanedColumns.forEach((colName) => {
      const value = row[colName];
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

  return Math.max(0, Math.round(((totalCells - issues) / totalCells) * 100));
});

const currentDataset = computed(() => {
  return showOriginal.value ? originalDataset.value : cleanedDataset.value;
});

const currentColumns = computed(() => {
  if (showOriginal.value) {
    return columns.value;
  }
  return getCleanedColumns();
});

const visibleColumns = computed(() => {
  if (showOriginal.value) {
    return columns.value.map((col) => col.name);
  } else {
    return getCleanedColumns();
  }
});

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
    rows.sort((a, b) => {
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

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredRows.value.slice(start, start + pageSize.value);
});

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

const hasActiveTools = computed(() => {
  return activeTools.value.length > 0
})


// ===== ADD THESE MISSING HELPER FUNCTIONS =====

const getToolName = (toolId) => {
  const toolNames = {
    'columnSelection': 'Column Selection',
    'missingValues': 'Handle Missing Values',
    'duplicateRemoval': 'Remove Duplicates',
    'outlierHandling': 'Handle Outliers',
    'categoricalEncoding': 'Encode Categories'
  }
  return toolNames[toolId] || toolId
}

const getToolIcon = (toolId) => {
  const icons = {
    'columnSelection': '🗂️',
    'missingValues': '🔧',
    'duplicateRemoval': '🔄',
    'outlierHandling': '📊',
    'categoricalEncoding': '🏷️'
  }
  return icons[toolId] || '⚙️'
}

const getToolDescription = (toolId) => {
  const descriptions = {
    'columnSelection': 'Select which columns to keep or remove',
    'missingValues': 'Handle missing values with various strategies',
    'duplicateRemoval': 'Remove duplicate rows from your dataset',
    'outlierHandling': 'Detect and handle statistical outliers',
    'categoricalEncoding': 'Convert categorical variables to numbers'
  }
  return descriptions[toolId] || 'Configure this tool'
}

const isEncodedColumn = (columnName) => {
  const col = columns.value.find(c => c.name === columnName)
  return col?.encode || false
}

const getEncodingMethod = (columnName) => {
  const col = columns.value.find(c => c.name === columnName)
  return col?.encoding || 'onehot'
}

const toggleColumnEncoding = (columnName) => {
  const col = columns.value.find(c => c.name === columnName)
  if (col) {
    col.encode = !col.encode
  }
}

const setEncodingMethod = (columnName, method) => {
  const col = columns.value.find(c => c.name === columnName)
  if (col) {
    col.encoding = method
  }
}

const calculateMissingValuesFrontend = () => {
  const missing = []
  
  columns.value.forEach(col => {
    const missingCount = originalDataset.value.filter(row => {
      const value = row[col.name]
      return value === null || value === undefined || value === '' || value === 'null'
    }).length
    
    if (missingCount > 0) {
      missing.push({
        name: col.name,
        type: col.type,
        count: missingCount,
        percentage: ((missingCount / originalDataset.value.length) * 100).toFixed(1),
        strategy: col.type === 'numerical' ? 'fillmedian' : 'fillmode'
      })
    }
  })
  
  missingColumnsDetailed.value = missing.sort((a, b) => b.count - a.count)
  console.log('✅ Calculated missing values in frontend:', missingColumnsDetailed.value)
}

// ===== NEW: BACKEND API FUNCTIONS =====

// Fetch missing values info from backend
const fetchMissingValuesInfo = async () => {
  if (!backendConnected.value || !datasetId.value) {
    console.log('Backend not connected or no dataset ID, skipping fetch')
    return
  }
  
  try {
    console.log('📊 Fetching missing values info from backend...')
    
    const response = await fetch('http://localhost:8000/api/preprocess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_id: datasetId.value,
        get_missing_info: true  
      })
    })
    
    if (!response.ok) throw new Error('Failed to fetch missing info')
    
    const data = await response.json()
    
    // Update missingColumnsDetailed with backend data
    missingColumnsDetailed.value = data.missing_info.map(col => ({
      ...col,
      strategy: col.strategy || 'fillmean'
    }))
    
    console.log('✅ Fetched missing info from backend:', missingColumnsDetailed.value)
    
  } catch (error) {
    console.error('❌ Error fetching missing info:', error)
  }
}

// Apply preprocessing via backend
const applyPreprocessing = async () => {
  if (!backendConnected.value || !datasetId.value) {
    console.warn('Backend not connected - using frontend fallback')
    applyPreprocessingFrontend()
    return
  }
  
  isApplyingPreprocessing.value = true
  
  try {
    // ✅ Build preprocessing config
    const preprocessingConfig = {
      dataset_id: datasetId.value
    }
    
    // ✅ 1. COLUMN REMOVAL (if enabled)
    if (isToolEnabled('columnSelection')) {
      const columnsToRemove = columns.value
        .filter(col => col.remove)
        .map(col => col.name)
      
      if (columnsToRemove.length > 0) {
        preprocessingConfig.remove_columns = columnsToRemove
        console.log('📋 Columns to remove:', columnsToRemove)
      }
    }
    
    // ✅ 2. MISSING VALUES (if enabled)
    if (isToolEnabled('missingValues') && missingColumnsDetailed.value.length > 0) {
      preprocessingConfig.missing_values = {}
      missingColumnsDetailed.value.forEach(col => {
        preprocessingConfig.missing_values[col.name] = col.strategy
      })
      console.log('🔧 Missing values strategies:', preprocessingConfig.missing_values)
    }
    
    // ✅ 3. DUPLICATE REMOVAL (if enabled)
    if (isToolEnabled('duplicateRemoval')) {
      preprocessingConfig.remove_duplicates = duplicateStrategy.value === 'keep_first' ? 'first' : 'last'
      console.log('🔄 Duplicate strategy:', preprocessingConfig.remove_duplicates)
    }
    
    // ✅ 4. OUTLIER HANDLING (if enabled)
    if (isToolEnabled('outlierHandling')) {
      const outlierColumns = columns.value
        .filter(col => col.type === 'numerical' && !col.remove)
        .map(col => col.name)
      
      if (outlierColumns.length > 0) {
        preprocessingConfig.outliers = {
          columns: outlierColumns,
          method: 'iqr',
          strategy: outlierStrategy.value
        }
        console.log('📊 Outlier config:', preprocessingConfig.outliers)
      }
    }
    
    // ✅ 5. CATEGORICAL ENCODING (if enabled)
    if (isToolEnabled('categoricalEncoding')) {
      const columnsToEncode = columns.value
        .filter(col => col.encode && col.type === 'categorical')
        .map(col => ({
          name: col.name,
          method: col.encoding || 'onehot'
        }))
      
      if (columnsToEncode.length > 0) {
        preprocessingConfig.encoding = {
          columns: columnsToEncode.map(c => c.name),
          method: 'label' // or 'onehot' based on selection
        }
        console.log('🏷️ Encoding config:', preprocessingConfig.encoding)
      }
    }
    
    console.log('📤 Sending preprocessing config to backend:', preprocessingConfig)
    
    processingMessage.value = 'Preprocessing dataset with scikit-learn...'
    isProcessing.value = true
    
    // ✅ SEND TO BACKEND
    const response = await fetch('http://localhost:8000/api/preprocess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preprocessingConfig)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Preprocessing failed')
    }
    
    const result = await response.json()
    
    console.log('✅ Preprocessing completed:', result)
    console.log('   Original shape:', result.summary.original_shape)
    console.log('   Final shape:', result.summary.final_shape)
    console.log('   Rows removed:', result.summary.rows_removed)
    
    // ✅ UPDATE DATASET WITH PREPROCESSED DATA
    if (result.preview && result.preview.length > 0) {
      cleanedDataset.value = result.preview
      originalDataset.value = result.preview // Update original too
      
      // Update columns from new data
      updateColumnsFromData(result.preview)
      
      // ✅ UPDATE MLSTORE
      mlStore.updateDataset(result.preview)
      mlStore.setPreprocessingSteps(result.summary.preprocessing_steps)
      
      // ✅ UPDATE LOCALSTORAGE
      localStorage.setItem('processedData', JSON.stringify({
        data: result.preview,
        fileName: fileName.value,
        datasetId: datasetId.value,
        backendDatasetId: datasetId.value,
        uploadTime: new Date().toISOString(),
        preprocessed: true
      }))
      
      processingMessage.value = `✅ Preprocessing completed! ${result.summary.rows_removed} rows removed`
      
      // Show summary
      console.log('📊 Preprocessing Summary:', result.summary)
      
      // Mark as preprocessed
      showOriginal.value = false
    }
    
    await new Promise(resolve => setTimeout(resolve, 1500))
    
  } catch (error) {
    console.error('❌ Preprocessing error:', error)
    processingMessage.value = `❌ Preprocessing failed: ${error.message}`
    alert(`Preprocessing failed: ${error.message}`)
  } finally {
    isApplyingPreprocessing.value = false
    isProcessing.value = false
  }
}


// Fallback: Frontend preprocessing (if backend unavailable)
const applyPreprocessingFrontend = async () => {
  isProcessing.value = true;
  processingMessage.value = "Starting data preprocessing (frontend mode)...";

  try {
    let processedData = [...originalDataset.value];

    if (activeTools.value.includes("columnSelection")) {
      processingMessage.value = "Removing selected columns...";
      const columnsToKeep = getColumnsToKeep().map((col) => col.name);

      if (columnsToKeep.length === 0) {
        throw new Error(
          "Cannot remove all columns. At least one column must remain."
        );
      }

      processedData = processedData.map((row) => {
        const newRow = {};
        columnsToKeep.forEach((colName) => {
          if (row.hasOwnProperty(colName)) {
            newRow[colName] = row[colName];
          }
        });
        return newRow;
      });

      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    if (activeTools.value.includes("missingValues")) {
      processingMessage.value = "Handling missing values...";
      processedData = handleMissingValues(processedData);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    if (activeTools.value.includes("duplicateRemoval")) {
      processingMessage.value = "Removing duplicates...";
      processedData = removeDuplicates(processedData);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    if (activeTools.value.includes("outlierHandling")) {
      processingMessage.value = "Handling outliers...";
      processedData = handleOutliers(processedData);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    cleanedDataset.value = processedData;
    showOriginal.value = false;
    processingMessage.value = "Processing completed successfully (frontend mode)!";

    await new Promise((resolve) => setTimeout(resolve, 1000));
  } catch (error) {
    console.error("Error processing data:", error);
    alert("Error processing dataset: " + error.message);
  } finally {
    isProcessing.value = false;
  }
}

// Helper: Update columns from new data
const updateColumnsFromData = (data) => {
  if (!data || data.length === 0) return
  
  const newColumns = Object.keys(data[0]).map(colName => {
    const existingCol = columns.value.find(c => c.name === colName)
    const type = detectColumnType(data.map(row => row[colName]))
    
    return {
      name: colName,
      type: type,
      remove: existingCol?.remove || false,
      unique: 0,
      missing: 0,
      encoding: type === 'categorical' ? 'onehot' : null,
      encode: false
    }
  })
  
  columns.value = newColumns
}

// Helper: Detect column type
const detectColumnType = (values) => {
  const nonNull = values.filter(v => v !== null && v !== undefined && v !== '')
  if (nonNull.length === 0) return 'categorical'
  
  const numericCount = nonNull.filter(v => !isNaN(parseFloat(v))).length
  return numericCount / nonNull.length > 0.8 ? 'numerical' : 'categorical'
}

// ===== MISSING VALUES STRATEGY HELPERS =====

const updateMissingStrategy = (columnName, strategy) => {
  const col = missingColumnsDetailed.value.find(c => c.name === columnName)
  if (col) {
    col.strategy = strategy
  }
  console.log(`Updated ${columnName}: ${strategy}`)
}

const applyGlobalMissingStrategy = () => {
  missingColumnsDetailed.value.forEach(col => {
    if ((globalMissingStrategy.value === 'fillmean' || globalMissingStrategy.value === 'fillmedian') && col.type !== 'numerical') {
      col.strategy = 'fillmode'
    } else {
      col.strategy = globalMissingStrategy.value
    }
    updateMissingStrategy(col.name, col.strategy)
  })
  console.log('Applied global strategy to all columns')
}

const autoSelectMissingStrategies = () => {
  missingColumnsDetailed.value.forEach(col => {
    let bestStrategy
    
    if (col.type === 'numerical') {
      bestStrategy = parseFloat(col.percentage) < 10 ? 'fillmedian' : 'droprows'
    } else {
      bestStrategy = parseFloat(col.percentage) < 15 ? 'fillmode' : 'droprows'
    }
    
    col.strategy = bestStrategy
    updateMissingStrategy(col.name, bestStrategy)
  })
  console.log('Auto-selected strategies based on data types')
}

const getStrategyName = (strategy) => {
  const names = {
    droprows: 'Drop Rows',
    fillmean: 'Fill Mean',
    fillmedian: 'Fill Median',
    fillmode: 'Fill Mode',
    fillzero: 'Fill Zero',
    fillunknown: 'Fill Unknown',
    keep: 'Keep Missing'
  }
  return names[strategy] || strategy
}

const getStrategyDescription = (strategy, type) => {
  const descriptions = {
    droprows: 'Removes entire rows with missing values',
    fillmean: type === 'numerical' ? 'Replace with average value' : 'Not applicable for text data',
    fillmedian: type === 'numerical' ? 'Replace with middle value' : 'Not applicable for text data',
    fillmode: 'Replace with most common value',
    fillzero: 'Replace with 0',
    fillunknown: 'Replace with "Unknown" placeholder',
    keep: 'Leave as missing (may cause errors)'
  }
  return descriptions[strategy] || ''
}

const getStrategyClass = (strategy) => {
  const classes = {
    droprows: 'strategy-drop',
    fillmean: 'strategy-fill',
    fillmedian: 'strategy-fill',
    fillmode: 'strategy-fill',
    fillzero: 'strategy-fill',
    fillunknown: 'strategy-fill',
    keep: 'strategy-keep'
  }
  return classes[strategy] || ''
}

// ===== FRONTEND PREPROCESSING HELPERS (FALLBACK) =====

const handleMissingValues = (data) => {
  // Your existing frontend logic (keep as fallback)
  let processedData = [...data];
  const rowsToDelete = new Set()
  
  missingColumnsDetailed.value.forEach(col => {
    const colName = col.name
    const strategy = col.strategy
    
    if (strategy === 'droprows') {
      processedData.forEach((row, index) => {
        const value = row[colName]
        if (value === null || value === undefined || value === '' || value === 'null') {
          rowsToDelete.add(index)
        }
      })
    } else if (strategy === 'keep') {
      console.log(`Keeping missing values in ${colName}`)
    } else {
      const values = processedData
        .map(row => row[colName])
        .filter(val => val !== null && val !== undefined && val !== '' && val !== 'null')
      
      if (values.length === 0) return
      
      let fillValue
      
      if (strategy === 'fillmean' && col.type === 'numerical') {
        const numbers = values.map(val => parseFloat(val)).filter(val => !isNaN(val))
        fillValue = numbers.reduce((a, b) => a + b) / numbers.length
      } else if (strategy === 'fillmedian' && col.type === 'numerical') {
        const numbers = values.map(val => parseFloat(val)).filter(val => !isNaN(val))
        numbers.sort((a, b) => a - b)
        fillValue = numbers[Math.floor(numbers.length / 2)]
      } else if (strategy === 'fillmode') {
        const frequency = {}
        values.forEach(val => {
          frequency[val] = (frequency[val] || 0) + 1
        })
        fillValue = Object.keys(frequency).reduce((a, b) => 
          frequency[a] > frequency[b] ? a : b
        )
      } else if (strategy === 'fillzero') {
        fillValue = 0
      } else if (strategy === 'fillunknown') {
        fillValue = 'Unknown'
      }
      
      if (fillValue !== undefined) {
        processedData.forEach(row => {
          const value = row[colName]
          if (value === null || value === undefined || value === '' || value === 'null') {
            row[colName] = fillValue
          }
        })
      }
    }
  })
  
  if (rowsToDelete.size > 0) {
    processedData = processedData.filter((_, index) => !rowsToDelete.has(index))
    console.log(`Removed ${rowsToDelete.size} rows with missing values`)
  }
  
  return processedData;
};

const removeDuplicates = (data) => {
  const seen = new Set();
  const result = [];

  data.forEach((row) => {
    const rowString = JSON.stringify(row);
    if (!seen.has(rowString)) {
      seen.add(rowString);
      result.push(row);
    } else if (duplicateStrategy.value === "keep_last") {
      const prevIndex = result.findIndex(
        (r) => JSON.stringify(r) === rowString
      );
      if (prevIndex !== -1) {
        result.splice(prevIndex, 1);
      }
      result.push(row);
    }
  });

  return result;
};

const handleOutliers = (data) => {
  if (outlierStrategy.value === "keep") return data;

  let processedData = [...data];
  const numericalCols = columns.value.filter(col => col.type === "numerical");

  numericalCols.forEach((col) => {
    const colName = col.name;
    const values = processedData
      .map((row) => parseFloat(row[colName]))
      .filter((val) => !isNaN(val) && isFinite(val));

    if (values.length === 0) return;

    values.sort((a, b) => a - b);
    const q1 = values[Math.floor(values.length * 0.25)];
    const q3 = values[Math.floor(values.length * 0.75)];
    const iqr = q3 - q1;
    const lowerBound = q1 - 1.5 * iqr;
    const upperBound = q3 + 1.5 * iqr;

    if (outlierStrategy.value === "remove") {
      processedData = processedData.filter((row) => {
        const value = parseFloat(row[colName]);
        return (
          isNaN(value) ||
          !isFinite(value) ||
          (value >= lowerBound && value <= upperBound)
        );
      });
    } else if (outlierStrategy.value === "cap") {
      processedData.forEach((row) => {
        const value = parseFloat(row[colName]);
        if (!isNaN(value) && isFinite(value)) {
          if (value < lowerBound) row[colName] = lowerBound;
          if (value > upperBound) row[colName] = upperBound;
        }
      });
    }
  });

  return processedData;
};

// ===== TOOL MANAGEMENT =====

const toggleTool = (toolName) => {
  const index = activeTools.value.indexOf(toolName);
  if (index > -1) {
    activeTools.value.splice(index, 1);
  } else {
    activeTools.value.push(toolName);
  }
};

const toggleDropdown = (toolName) => {
  const index = openDropdowns.value.indexOf(toolName)
  if (index > -1) {
    openDropdowns.value.splice(index, 1)
  } else {
    openDropdowns.value.push(toolName)
  }
}

const enableTool = (toolName) => {
  if (!activeTools.value.includes(toolName)) {
    activeTools.value.push(toolName)
  }
  if (!openDropdowns.value.includes(toolName)) {
    openDropdowns.value.push(toolName)
  }
}

const disableTool = (toolName) => {
  const index = activeTools.value.indexOf(toolName)
  if (index > -1) {
    activeTools.value.splice(index, 1)
  }
  const dropdownIndex = openDropdowns.value.indexOf(toolName)
  if (dropdownIndex > -1) {
    openDropdowns.value.splice(dropdownIndex, 1)
  }
}


// ===== ADD THESE 4 MISSING HELPER FUNCTIONS =====

// 1. Get tool configuration summary (used in Apply Changes section)
const getToolConfig = (toolId) => {
  const configs = {
    'columnSelection': `${getColumnsToRemove().length} column(s) to remove`,
    'missingValues': `${missingStats.value.count} column(s) affected`,
    'duplicateRemoval': `Keep ${duplicateStrategy.value === 'keep_first' ? 'first' : 'last'} occurrence`,
    'outlierHandling': `${outlierStrategy.value.charAt(0).toUpperCase() + outlierStrategy.value.slice(1)} strategy`,
    'categoricalEncoding': `${columns.value.filter(c => c.encode).length} column(s) to encode`
  }
  
  return configs[toolId] || 'Not configured'
}

// 2. Select all categorical columns for encoding
const selectAllCategoricalColumns = () => {
  categoricalColumns.value.forEach(col => {
    const column = columns.value.find(c => c.name === col.name)
    if (column) column.encode = true
  })
  console.log('✅ Selected all categorical columns for encoding')
}

// 3. Deselect all categorical columns
const deselectAllCategoricalColumns = () => {
  categoricalColumns.value.forEach(col => {
    const column = columns.value.find(c => c.name === col.name)
    if (column) column.encode = false
  })
  console.log('❌ Deselected all categorical columns')
}

// 4. Auto-select categorical columns (smart selection)
const autoSelectForEncoding = () => {
  categoricalColumns.value.forEach(col => {
    const column = columns.value.find(c => c.name === col.name)
    if (!column) return
    
    const uniqueCount = column.unique || 0
    const isLikelyTarget = uniqueCount <= 10 
    
    // Encode if it's not a likely target and has more than 2 unique values
    column.encode = !isLikelyTarget && uniqueCount > 2
  })
  console.log('🤖 Auto-selected columns for encoding (excluded likely targets)')
}

// 5. Reset all changes
const resetAllChanges = () => {
  console.log('🔄 Starting reset...')
  
  // 1. Reset UI state
  activeTools.value = []
  openDropdowns.value = []
  showOriginal.value = true
  isProcessing.value = false
  isApplyingPreprocessing.value = false
  
  // 2. Clear cleaned dataset
  cleanedDataset.value = []
  processingMessage.value = ''
  
  // 3. Reset all tool settings
  columns.value.forEach(col => {
    col.remove = false
    col.encode = false
  })
  
  missingColumnsDetailed.value.forEach(col => {
    col.strategy = col.type === 'numerical' ? 'fillmedian' : 'fillmode'
  })
  
  duplicateStrategy.value = 'keep_first'
  outlierStrategy.value = 'cap'
  globalMissingStrategy.value = 'fillmean'
  
  // 4. ✅ RESTORE ORIGINAL DATASET FROM BACKUP
  if (originalDatasetBackup.value && originalDatasetBackup.value.length > 0) {
    // Deep copy from backup to prevent any mutation
    originalDataset.value = JSON.parse(JSON.stringify(originalDatasetBackup.value))
    console.log('✅ Restored original dataset from backup:', originalDataset.value.length, 'rows')
  } else {
    console.warn('⚠️ No backup found, trying to reload from localStorage...')
    
    // Fallback: reload from localStorage
    const processedDataStr = localStorage.getItem('processedData')
    if (processedDataStr) {
      try {
        const processedData = JSON.parse(processedDataStr)
        if (processedData.data && processedData.data.length > 0) {
          originalDataset.value = processedData.data.slice(0, 200)
          // Recreate backup
          originalDatasetBackup.value = JSON.parse(JSON.stringify(originalDataset.value))
          console.log('✅ Restored from localStorage:', originalDataset.value.length, 'rows')
          console.log('   Backup recreated:', originalDatasetBackup.value.length, 'rows')
        }
      } catch (error) {
        console.error('❌ Error restoring from localStorage:', error)
      }
    }
  }
  
  // 5. Re-analyze columns from original data
  if (originalDataset.value.length > 0) {
    analyzeColumns()
    console.log('✅ Columns re-analyzed')
  }
  
  // 6. Recalculate statistics
  if (backendConnected.value && datasetId.value) {
    fetchMissingValuesInfo()
    console.log('📊 Fetching fresh missing values info from backend...')
  } else {
    calculateMissingValuesFrontend()
    console.log('📊 Recalculated missing values in frontend')
  }
  
  // 7. Reset pagination
  currentPage.value = 1
  
  console.log('✅ Reset complete!')
  console.log('   Active tools:', activeTools.value.length)
  console.log('   Original dataset:', originalDataset.value.length, 'rows')
  console.log('   Cleaned dataset:', cleanedDataset.value.length, 'rows')
  console.log('   Backup available:', originalDatasetBackup.value.length, 'rows')
}



// 6. Reset tool-specific settings (helper functions)
const resetToolSettingsColumnSelection = () => {
  columns.value.forEach(col => col.remove = false)
  console.log('🔄 Reset column selection')
}

const resetToolSettingsMissingValues = () => {
  missingColumnsDetailed.value.forEach(col => {
    col.strategy = col.type === 'numerical' ? 'fillmedian' : 'fillmode'
  })
  globalMissingStrategy.value = 'fillmean'
  console.log('🔄 Reset missing values strategies')
}

// 7. Apply changes wrapper
const applyChanges = async () => {
  await applyPreprocessing()
}

// 8. Export data function
const exportData = () => {
  const dataToExport = hasCleanedData.value ? cleanedDataset.value : originalDataset.value
  
  if (!dataToExport || dataToExport.length === 0) {
    alert('No data to export')
    return
  }
  
  const cols = hasCleanedData.value ? getCleanedColumns() : visibleColumns.value
  const csv = [
    cols.join(','),
    ...dataToExport.map(row => 
      cols.map(col => {
        const value = row[col]
        if (value === null || value === undefined) return ''
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`
        }
        return value
      }).join(',')
    )
  ].join('\n')
  
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${fileName.value.replace('.csv', '')}_${hasCleanedData.value ? 'cleaned' : 'original'}_${new Date().getTime()}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  console.log('📥 Exported data to CSV')
}


const resetToolSettings = (toolName) => {
  switch(toolName) {
    case 'columnSelection':
      columns.value.forEach(col => col.remove = false)
      break
    case 'missingValues':
      missingValuesConfig.value = {}
      globalMissingStrategy.value = 'fillmean'
      missingColumnsDetailed.value.forEach(col => {
        col.strategy = 'fillmean'
      })
      break
    case 'duplicateRemoval':
      duplicateStrategy.value = 'keep_first'
      break
    case 'outlierHandling':
      outlierStrategy.value = 'cap'
      break
  }
}

const isDropdownOpen = (toolName) => {
  return openDropdowns.value.includes(toolName)
}

const isToolEnabled = (toolName) => {
  return activeTools.value.includes(toolName)
}

// ===== COLUMN HELPERS =====

const getColumnsToKeep = () => {
  return columns.value.filter((col) => !col.remove);
};

const getColumnsToRemove = () => {
  return columns.value.filter((col) => col.remove);
};

const getCleanedColumns = () => {
  if (cleanedDataset.value.length === 0) return [];
  return Object.keys(cleanedDataset.value[0]);
};

const selectNoColumns = () => {
  columns.value.forEach((col) => (col.remove = false));
};

const selectAllColumns = () => {
  if (
    confirm(
      "Are you sure you want to remove ALL columns? This will make your dataset unusable."
    )
  ) {
    columns.value.forEach((col) => (col.remove = true));
  }
};

const selectIrrelevantColumns = () => {
  columns.value.forEach((col) => {
    col.remove = checkIfIrrelevant(
      col.name,
      originalDataset.value.map((row) => row[col.name])
    );
  });
};

const checkIfIrrelevant = (columnName, values) => {
  const name = columnName.toLowerCase();

  const irrelevantPatterns = [
    "id", "uuid", "key", "index", "_id", "name", "email", "phone", 
    "address", "url", "link", "path", "image", "created", "updated", "timestamp",
  ];

  const matchesPattern = irrelevantPatterns.some((pattern) =>
    name.includes(pattern)
  );

  const uniqueValues = new Set(
    values.filter(
      (v) => v !== null && v !== undefined && v !== "" && v !== "null"
    )
  ).size;
  const nonNullValues = values.filter(
    (v) => v !== null && v !== undefined && v !== "" && v !== "null"
  );
  const isAllUnique =
    uniqueValues === nonNullValues.length &&
    uniqueValues > nonNullValues.length * 0.9;

  return matchesPattern || isAllUnique;
};

const getColumnSample = (column) => {
  const values = originalDataset.value
    .map((row) => row[column.name])
    .filter(
      (val) => val !== null && val !== undefined && val !== "" && val !== "null"
    )
    .slice(0, 3);

  return values.length > 0 ? values.join(", ") : "No data";
};

// ===== UTILITY FUNCTIONS =====

const analyzeColumns = () => {
  if (originalDataset.value.length === 0) return;

  const firstRow = originalDataset.value[0];
  const analyzedColumns = [];

  Object.keys(firstRow).forEach((colName) => {
    const values = originalDataset.value.map((row) => row[colName]);
    const nonNullValues = values.filter(
      (val) => val !== null && val !== undefined && val !== "" && val !== "null"
    );

    let type = "categorical";
    if (nonNullValues.length > 0) {
      const numericCount = nonNullValues.filter(
        (val) => !isNaN(parseFloat(val)) && isFinite(val)
      ).length;
      if (numericCount > nonNullValues.length * 0.8) {
        type = "numerical";
      }
    }

    analyzedColumns.push({
      name: colName,
      type,
      remove: false,
      unique: new Set(nonNullValues).size,
      missing: values.length - nonNullValues.length,
      encoding: type === "categorical" ? "onehot" : null,
      encode: false,
    });
  });

  columns.value = analyzedColumns;
};

const loadDataFromStorage = async () => {
  try {
    console.log('📊 Loading data from storage...')
    
    // ===== PRIORITY 1: Try mlStore =====
    if (mlStore.dataset && mlStore.dataset.length > 0 && mlStore.datasetId) {
      datasetId.value = mlStore.datasetId
      fileName.value = mlStore.fileName || 'Dataset'
      originalDataset.value = mlStore.dataset.slice(0, 200)
      
      // ✅ CREATE BACKUP (deep copy to prevent mutation)
      originalDatasetBackup.value = JSON.parse(JSON.stringify(originalDataset.value))
      
      console.log('✅ Data loaded from mlStore')
      console.log('   Dataset ID:', datasetId.value)
      console.log('   Rows:', originalDataset.value.length)
      console.log('   File:', fileName.value)
      console.log('   Backup created:', originalDatasetBackup.value.length, 'rows')
      
      analyzeColumns()
      
      if (backendConnected.value && datasetId.value) {
        await fetchMissingValuesInfo()
      }
      
      return
    }
    
    // ===== PRIORITY 2: Try localStorage =====
    const processedDataStr = localStorage.getItem('processedData')
    if (processedDataStr) {
      console.log('📦 Found data in localStorage, parsing...')
      
      const processedData = JSON.parse(processedDataStr)
      
      console.log('📋 localStorage data:', {
        hasData: !!processedData.data,
        dataLength: processedData.data?.length || 0,
        fileName: processedData.fileName,
        datasetId: processedData.datasetId
      })
      
      datasetId.value = processedData.backendDatasetId || processedData.datasetId || ''
      fileName.value = processedData.fileName || 'Dataset'
      originalDataset.value = (processedData.data || []).slice(0, 200)
      
      console.log('✅ Data loaded from localStorage')
      console.log('   Dataset ID:', datasetId.value)
      console.log('   Rows:', originalDataset.value.length)
      console.log('   Columns:', originalDataset.value[0] ? Object.keys(originalDataset.value[0]).length : 0)
      
      if (originalDataset.value.length > 0) {
        // ✅ CREATE BACKUP (deep copy)
        originalDatasetBackup.value = JSON.parse(JSON.stringify(originalDataset.value))
        console.log('   Backup created:', originalDatasetBackup.value.length, 'rows')
        
        analyzeColumns()
        
        if (backendConnected.value && datasetId.value) {
          await fetchMissingValuesInfo()
        }
      } else {
        console.warn('⚠️ No rows in dataset, trying to fetch from backend...')
        
        // ===== PRIORITY 3: Try backend =====
        if (backendConnected.value && datasetId.value) {
          await fetchDatasetFromBackend(datasetId.value)
        }
      }
    } else {
      console.warn('⚠️ No data found in storage')
    }
  } catch (error) {
    console.error('❌ Error loading data:', error)
  }
}

// ✅ UPDATE fetchDatasetFromBackend to also create backup
const fetchDatasetFromBackend = async (datasetId) => {
  try {
    console.log('📥 Fetching dataset from backend:', datasetId)
    
    const response = await fetch(`http://localhost:8000/api/datasets/${datasetId}`)
    
    if (response.ok) {
      const data = await response.json()
      
      console.log('✅ Dataset fetched from backend:', {
        dataset_id: data.dataset_id,
        filename: data.filename,
        shape: data.shape,
        hasSampleData: !!data.sample_data,
        sampleDataLength: data.sample_data?.length || 0,
        columns: data.columns?.length || 0
      })
      
      console.log('📋 Sample data preview:', data.sample_data?.slice(0, 2))
      
      // Store in localStorage
      localStorage.setItem('processedData', JSON.stringify({
        data: data.sample_data || [],
        fileName: data.filename,
        datasetId: data.dataset_id,
        backendDatasetId: data.dataset_id,
        uploadTime: data.uploaded_at
      }))
      
      // Load into component
      originalDataset.value = (data.sample_data || []).slice(0, 200)
      fileName.value = data.filename
      
      // ✅ CREATE BACKUP
      if (originalDataset.value.length > 0) {
        originalDatasetBackup.value = JSON.parse(JSON.stringify(originalDataset.value))
        console.log('   Backup created:', originalDatasetBackup.value.length, 'rows')
      }
      
      analyzeColumns()
      
      console.log('✅ Dataset loaded from backend:', originalDataset.value.length, 'rows')
    } else {
      console.error('❌ Failed to fetch dataset from backend')
    }
  } catch (error) {
    console.error('❌ Error fetching from backend:', error)
  }
}



// In dashboard.vue - handleFileUploadBackend function

const handleFileUploadBackend = async (file) => {
  try {
    console.log('🚀 Processing file with DIRECT-TO-BACKEND approach:', file.name)
    
    const formData = new FormData()
    formData.append('file', file)
    
    const uploadUrl = 'http://localhost:8000/api/upload-dataset'
    console.log(`📤 Uploading ${file.name} (${(file.size / 1024 / 1024).toFixed(1)}MB) to ${uploadUrl}`)
    
    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Upload failed')
    }
    
    const result = await response.json()
    
    console.log('✅ File uploaded successfully:', result.dataset_id)
    console.log('   Shape:', result.shape)
    console.log('   Columns:', result.columns.length)
    console.log('   Sample data rows:', result.sample_data?.length || 0)
    
    
    
    // 1. Register in mlStore
    const mlStore = useMLDataFlowStore()
    
    await mlStore.registerDataset({
      dataset_id: result.dataset_id,
      filename: result.filename,
      shape: result.shape,
      columns: result.columns,
      dtypes: result.dtypes,
      upload_time: result.upload_time
    })
    
    // 2. Set dataset data in mlStore
    mlStore.setDataset(
      result.sample_data || [],  // Actual data
      result.filename,
      result.dataset_id
    )
    
    // 3. ✅ FIXED: Store in localStorage with actual data
    localStorage.setItem('processedData', JSON.stringify({
      data: result.sample_data || [],  // ← CRITICAL: Must have actual data
      fileName: result.filename,
      datasetId: result.dataset_id,
      backendDatasetId: result.dataset_id,
      uploadTime: result.upload_time || new Date().toISOString(),
      shape: result.shape,
      columns: result.columns
    }))
    
    console.log('🎉 Upload completed successfully with backend integration!')
    console.log('   Data stored:', {
      mlStore: mlStore.dataset.length,
      localStorage: result.sample_data?.length || 0
    })
    
    // Verify backend has the dataset
    const verified = await mlStore.verifyDatasetInBackend(result.dataset_id)
    if (verified) {
      console.log('✅ Dataset verified in backend')
    } else {
      console.warn('⚠️ Dataset not found in backend')
    }
    
    // Navigate to data preview
    console.log('✅ Navigating to data preview with backend dataset:', result.dataset_id)
    router.push('/data-preview')
    
  } catch (error) {
    console.error('❌ Backend upload failed:', error)
    alert(`Upload failed: ${error.message}`)
  }
}



const sortByColumn = (columnName) => {
  if (sortColumn.value === columnName) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortColumn.value = columnName;
    sortDirection.value = "asc";
  }
};

const formatCellValue = (value) => {
  if (value === null || value === undefined || value === "null") return "-";
  if (typeof value === "number") {
    if (Number.isInteger(value)) return value.toString();
    return Number.isFinite(value) ? value.toFixed(2) : "-";
  }
  if (typeof value === "string" && value.length > 30)
    return value.substring(0, 30) + "...";
  return String(value);
};

const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num);
};

const getHealthLevel = (score) => {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "fair";
  return "poor";
};

const goBack = () => {
  router.push("/dashboard");
};

const proceedToTargetSelection = async () => {
  try {
    isProcessing.value = true
    processingMessage.value = "Preparing for target selection..."
    
    // Apply preprocessing if tools are enabled
    if (hasActiveTools.value && !hasCleanedData.value) {
      await applyPreprocessing()
    }
    
    await new Promise(resolve => setTimeout(resolve, 500))
    router.push("/target-selection")
    
  } catch (error) {
    console.error("❌ Navigation failed:", error)
    alert(`Error: ${error.message}`)
  } finally {
    isProcessing.value = false
  }
}




// ===== WATCHERS =====

watch(pageSize, () => {
  currentPage.value = 1;
});

watch(searchQuery, () => {
  currentPage.value = 1;
});

// ===== LIFECYCLE =====

onMounted(async () => {
  console.log('🚀 Initializing Data Preview...')
  
  await mlStore.checkBackendConnection()
  await loadDataFromStorage()
  
  console.log('✅ Data Preview initialized')
})

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
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
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
  white-space: nowrap;
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

/* ✅ ADD THESE STYLES TO YOUR EXISTING CSS */

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
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
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
</style>
