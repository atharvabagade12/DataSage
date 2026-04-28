<template>
  <div class="dashboard">
    <!-- Main Content -->
    <div v-if="isLoading" class="loader-container">
        <div class="premium-loader"></div>
        <p>Intelligence gathering in progress...</p>
    </div>

    <div v-else class="dashboard-content">
      <!-- ===== DASHBOARD TAB ===== -->
      <transition name="fade-slide">
        <div v-if="activeDashboardTab === 'dashboard'" class="tab-view dashboard-view">
          

          <div class="kpi-grid">
            <div class="kpi-card premium project" @click="activeDashboardTab = 'projects'">
              <div class="kpi-icon-circle blue">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <div class="kpi-info">
                <div class="kpi-label">My Projects</div>
                <div class="kpi-value">{{ dashboardStats.projects }}</div>
                <div class="kpi-sub">Active Datasets</div>
              </div>
            </div>

            <div class="kpi-card premium dataset">
              <div class="kpi-icon-circle purple">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"></path>
                </svg>
              </div>
              <div class="kpi-info">
                <div class="kpi-label">Latest Upload</div>
                <div class="latest-entry" v-if="allDatasets.length">
                  <div class="entry-name">{{ sortedDatasets[0].name }}</div>
                  <div class="entry-meta">{{ sortedDatasets[0].rows?.toLocaleString() }} rows</div>
                </div>
                <div v-else class="latest-entry empty">No data yet</div>
              </div>
            </div>

            <div class="kpi-card premium health" @click="activeDashboardTab = 'analytics'">
              <div class="kpi-icon-circle emerald">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                </svg>
              </div>
              <div class="kpi-content-row">
                <div class="kpi-info">
                  <div class="kpi-label">Data Health</div>
                  <div class="health-percentage">{{ dashboardStats.dataHealth }}%</div>
                  <div class="kpi-sub">Quality Score</div>
                </div>
                <div class="health-donut-mini">
                  <svg viewBox="0 0 36 36" class="circular-chart">
                    <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    <path class="circle" :stroke-dasharray="`${dashboardStats.dataHealth}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  </svg>
                </div>
              </div>
            </div>

            <div class="kpi-card premium training" @click="activeDashboardTab = 'models'">
              <div class="kpi-icon-circle indigo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                </svg>
              </div>
              <div class="kpi-info">
                <div class="kpi-label">Models Trained</div>
                <div class="kpi-value">{{ dashboardStats.models }}</div>
                <div class="kpi-sub">Total Experiments</div>
              </div>
            </div>
          </div>

          <!--------------------Quick Actions ---------------------->
          <div class="quick-actions-section">
            <h2 class="section-title">Quick Actions</h2>
            <div class="quick-actions-grid">
              <div class="action-card" @click="useSampleData">
                <div class="action-icon sample">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2H2v10h10V2zM22 12h-10v10h10V12zM12 12H2v10h10V12zM22 2h-10v10h10V2z"/>
                  </svg>
                </div>
                <div class="action-text">
                  <h3>Sample Data</h3>
                  <p>Quick start with curated data</p>
                </div>
              </div>

              <div class="action-card" @click="resumeLastSession" :class="{ 'disabled-action': !sortedDatasets.length }">
                <div class="action-icon resume">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                  </svg>
                </div>
                <div class="action-text">
                  <h3>Resume Last Session</h3>
                  <p v-if="sortedDatasets.length">Continue with <strong>{{ sortedDatasets[0].name }}</strong></p>
                  <p v-else>No previous sessions found</p>
                </div>
              </div>

              <div class="action-card" @click="showGuideModal = true">
                <div class="action-icon guide">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                  </svg>
                </div>
                <div class="action-text">
                  <h3>Ecosystem Guide</h3>
                  <p>Master the DataSage flow</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Shrunken Center Upload Section -->
          <div class="upload-immersive-section">
            <div class="upload-compact-container glass">
              <div class="upload-header-compact">
                <h2>Import Intelligence</h2>
                <p>Support for CSV, JSON, Parquet & Excel (Max 1GB)</p>
              </div>
              
              <div ref="uploadSection" class="upload-compact-zone"
                   :class="{ 'drag-over': dragOver, 'uploading': isUploading, 'success': uploadSuccess }"
                   @dragover.prevent="dragOver = true"
                   @dragleave.prevent="dragOver = false"
                   @drop.prevent="handleDrop"
                   @click="triggerFileInput">
                
                <input type="file" ref="fileInput" class="hidden-input" @change="handleFileSelect" accept=".csv,.json,.parquet,.xlsx,.xls">
                
                <div v-if="!isUploading && !uploadSuccess" class="upload-prompt-compact">
                  <div class="prompt-icon-mini">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="1.5">
                      <path d="M12 3v12M17 8l-5-5-5 5M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    </svg>
                  </div>
                  <h3>Drop file to analyze</h3>
                  <p>or click to browse</p>
                  <div class="format-badges">
                    <span class="fmt-csv">CSV</span>
                    <span class="fmt-json">JSON</span>
                    <span class="fmt-excel">Excel</span>
                    <span class="fmt-parquet">Parquet</span>
                  </div>
                </div>

                <div v-if="isUploading" class="upload-progress-compact">
                  <div class="premium-spinner"></div>
                  <h3>Uploading Data...</h3>
                  <div class="mini-progress-bar">
                    <div class="fill" :style="{ width: uploadProgress + '%' }"></div>
                  </div>
                  <p>{{ uploadMessage }}</p>
                </div>

                <transition name="scale">
                  <div v-if="uploadSuccess" class="upload-success-compact">
                    <h3>{{ uploadedFile?.filename }} is Ready</h3>
                    <button @click.stop="goToPreview" class="launch-btn-premium">Launch Data Lab</button>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- ===== PROJECTS TAB ===== -->
      <transition name="fade-slide">
        <div v-if="activeDashboardTab === 'projects'" class="tab-view inventory-view">
          <div class="view-header">
            <div class="header-main">
              <h2>Project Inventory</h2>
              <div class="inventory-header-stats">
                <p>Manage all your uploaded datasets and historical progress</p>
                <div class="dataset-limit-pill" :class="{ 'warning': allDatasets.length >= 25, 'danger': allDatasets.length >= 30 }">
                  <span class="count">{{ allDatasets.length }}</span>
                  <span class="limit">/ 30 Datasets</span>
                </div>
              </div>
            </div>
            
          </div>

          <div class="inventory-section glass">
            <div class="table-container">
              <table v-if="allDatasets.length">
                <thead>
                  <tr>
                    <th>Dataset Name</th>
                    <th>Records</th>
                    <th>Size</th>
                    <th>State</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ds in sortedDatasets" :key="ds.id" class="table-row-hover">
                    <td class="file-name-cell">
                      <div class="file-icon-mini">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                          <polyline points="14 2 14 8 20 8"></polyline>
                        </svg>
                      </div>
                      {{ ds.name }}
                    </td>
                    <td>{{ ds.rows?.toLocaleString() }}</td>
                    <td>{{ formatFileSize(ds.size_bytes || ds.size) }}</td>
                    <td>
                      <span class="status-pill" :class="{ processed: ds.is_processed || ds.isProcessed }">
                        {{ (ds.is_processed || ds.isProcessed) ? 'Refined' : 'Initial' }}
                      </span>
                    </td>
                    <td>
                      <div class="action-group-mini">
                        <button @click="analyzeDataset(ds)" class="btn-table-action">Explore</button>
                        <button @click="downloadDataset(ds)" class="btn-table-action secondary" title="Download CSV">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                          </svg>
                        </button>
                        <button @click="deleteDataset(ds)" class="btn-table-action danger" title="Delete Dataset">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else class="empty-state-view">
                <div class="empty-illustration">📂</div>
                <h3>No datasets uploaded</h3>
                <p>Start by importing your first data project.</p>
                <button @click="triggerFileInput" class="btn-outline">Upload Now</button>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- ===== ANALYTICS TAB ===== -->
      <transition name="fade-slide">
        <div v-if="activeDashboardTab === 'analytics'" class="tab-view analytics-view">
          <div class="view-header">
            <div class="header-main">
              <h2>Data Intelligence Analytics</h2>
              <p>Explore performance trends and recent system actions</p>
            </div>
          </div>

          <div class="analytics-grid">
            <div class="chart-container-premium glass">
              <div class="container-header">
                <h3>Evolution of Accuracy</h3>
                <span class="status-indicator">Live</span> 
              </div>
              <div class="chart-wrapper">
                <canvas ref="performanceChartCanvas"></canvas>
              </div>
            </div>

            <div class="activity-container-premium glass">
              <div class="container-header">
                <h3>Activity Chronicle</h3>
                <span class="count-badge">Last {{ recentActivity.length }} Events</span>
              </div>
              <div class="activity-feed custom-scrollbar">
                <div v-for="act in recentActivity" :key="act.id" class="activity-item-premium">
                  <div class="item-icon-wrapper" :class="act.action_type">
                    <div class="icon-inner" v-html="getActionIcon(act.action_type)"></div>
                  </div>
                  <div class="item-content">
                    <div class="item-header">
                      <div class="item-title">{{ formatActionTitle(act) }}</div>
                      <div class="item-timestamp" :title="new Date(act.created_at).toLocaleString()">
                        {{ getRelativeTime(act.created_at) }}
                      </div>
                    </div>
                    <div class="item-subtext" v-if="act.details?.filename">Targeting {{ act.details.filename }}</div>
                  </div>
                </div>
                <div v-if="recentActivity.length === 0" class="empty-activity">
                    <p>System log is currently empty.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- ===== MODELS TAB ===== -->
      <transition name="fade-slide">
        <div v-if="activeDashboardTab === 'models'" class="tab-view models-view">
          <div class="view-header">
            <div class="header-main">
              <h2>Model Leaderboard</h2>
              <p>Performance comparison of all trained intelligence units</p>
            </div>
          </div>

          <div class="inventory-section glass">
            <div class="table-container">
              <table v-if="allModels.length">
                <thead>
                  <tr>
                    <th>Model Strategy</th>
                    <th>Algorithm</th>
                    <th>Performance Indicators</th>
                    <th>Configuration</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="model in allModels" :key="model.id" class="table-row-hover">
                    <td class="model-name-cell">
                      <div class="model-icon-mini">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        </svg>
                      </div>
                      <div class="model-info-stack">
                        <span class="model-name-text">{{ model.name }}</span>
                        <span class="model-date-mini">{{ getRelativeTime(model.createdAt) }}</span>
                      </div>
                    </td>
                    <td><span class="algo-badge">{{ model.algorithm }}</span></td>
                    <td>
                      <div class="metrics-pill-group">
                        <div v-for="(val, key) in getBriefMetrics(model)" :key="key" class="metric-pill" :class="getMetricClass(key)">
                          <span class="metric-label">{{ formatMetricKey(key) }}</span>
                          <span class="metric-value">{{ formatMetricValue(val) }}</span>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="config-badges">
                        <div v-for="(val, key) in getBriefConfig(model)" :key="key" class="config-badge" :title="`${key}: ${val}`">
                          {{ key }}: {{ val }}
                        </div>
                        <div v-if="Object.keys(model.hyperparameters || {}).length > 3" class="config-badge more">
                          +{{ Object.keys(model.hyperparameters).length - 3 }} more
                          <div class="config-tooltip">
                            <div v-for="(val, key) in getHiddenConfig(model)" :key="key" class="tooltip-item">
                              <span class="t-key">{{ key }}</span>
                              <span class="t-val">{{ formatHyperparam(val) }}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="action-group-mini">
                        <button @click="downloadModel(model)" class="btn-table-action secondary" title="Download Model (.joblib)">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else class="empty-state-view">
                <div class="empty-illustration">🧠</div>
                <h3>Brain empty</h3>
                <p>Train your first model in the Laboratory to see results here.</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- ===== CUSTOM DELETE MODAL ===== -->
    <transition name="modal-fade">
      <div v-if="showDeleteModal" class="modal-overlay" @click.self="cancelDelete">
        <div class="modal-container glass">
          <div class="modal-header">
            <div class="warning-icon-animate">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01"></path>
              </svg>
            </div>
            <h2>Destroy Intelligence?</h2>
          </div>
          
          <div class="modal-body">
            <p>You are about to permanently purge <span class="highlight-name">{{ datasetToDelete?.name }}</span> from the ecosystem.</p>
            <div class="warning-box">
              <p>This action will also incinerate all associated trained models and processed versions. This cannot be undone.</p>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="cancelDelete" class="btn-modal secondary" :disabled="isDeleting">Abort Mission</button>
            <button @click="confirmDelete" class="btn-modal danger" :disabled="isDeleting">
              <span v-if="!isDeleting">Confirm Purge</span>
              <span v-else class="spinner-mini"></span>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- ===== LIMIT EXCEEDED MODAL ===== -->
    <transition name="modal-fade">
      <div v-if="showLimitModal" class="modal-overlay" @click.self="showLimitModal = false">
        <div class="modal-container glass">
          <div class="modal-header">
            <div class="warning-icon-animate">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2">
                <path d="M12 9v4M12 17h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              </svg>
            </div>
            <h2>Limit Reached</h2>
          </div>
          
          <div class="modal-body">
            <p>You have reached the dataset upload limit of 30.</p>
            <div class="warning-box" style="background: rgba(245, 158, 11, 0.05); border-color: rgba(245, 158, 11, 0.1);">
              <p style="color: #f59e0b;">Please delete some of the previous datasets to continue uploading.</p>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="showLimitModal = false" class="btn-modal secondary">Understood</button>
            <button @click="activeDashboardTab = 'projects'; showLimitModal = false" class="btn-modal" style="background: linear-gradient(135deg, #667eea, #764ba2); border: none; color: white;">Manage Datasets</button>
          </div>
        </div>
      </div>
    </transition>
  </div>

  <!-- Sample Data Modal -->
  <SampleDataModal :show="showSampleModal" @close="showSampleModal = false" />
  
  <!-- Ecosystem Guide Modal -->
  <EcosystemGuideModal :show="showGuideModal" @close="showGuideModal = false" />

</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMLDataFlowStore } from '../stores/mlDataFlow'
import { useExperimentStore } from '../stores/experiment'
import { useToast } from '@/composables/useToast'
import axios from 'axios'
import Chart from 'chart.js/auto'
import SampleDataModal from '@/components/SampleDataModal.vue'
import EcosystemGuideModal from '@/components/EcosystemGuideModal.vue'

const router = useRouter()
const route = useRoute()
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()
const { showError, showSuccess } = useToast()

// Navigation & View State
// Use URL query 'tab' as the source of truth for the active tab
const activeDashboardTab = computed({
  get: () => route.query.tab || 'dashboard',
  set: (val) => router.push({ query: { ...route.query, tab: val } })
})
const isLoading = ref(true)

// Upload State
const dragOver = ref(false)
const isUploading = ref(false)
const uploadSuccess = ref(false)
const uploadProgress = ref(0)
const uploadMessage = ref('')
const uploadedFile = ref(null)

// Refs
const fileInput = ref(null)
const uploadSection = ref(null)
const performanceChartCanvas = ref(null)
let performanceChart = null

// Modal States
const showDeleteModal = ref(false)
const showLimitModal = ref(false)
const showSampleModal = ref(false)
const showGuideModal = ref(false)
const datasetToDelete = ref(null)
const isDeleting = ref(false)

// Computed User Data
const userName = computed(() => {
  try {
    const userString = sessionStorage.getItem('user') || localStorage.getItem('user')
    const user = JSON.parse(userString || '{}')
    return user.username || user.name || 'Data Scientist'
  } catch {
    return 'Data Scientist'
  }
})

const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'DS'
})

// Mapped Stats from Stores
const dashboardStats = computed(() => mlStore.dashboardStats)
const recentActivity = computed(() => mlStore.recentActivity)
const allDatasets = computed(() => mlStore.allUserDatasets)
const allModels = computed(() => mlStore.allUserModels)

const sortedDatasets = computed(() => {
  if (!allDatasets.value) return []
  return [...allDatasets.value].sort((a, b) => {
    return new Date(b.upload_time) - new Date(a.upload_time)
  })
})

// Data Fetching
const fetchData = async (isSilent = false) => {
  if (!isSilent) isLoading.value = true
  try {
    await Promise.all([
      mlStore.fetchDashboardStats(),
      mlStore.fetchRecentActivity(),
      mlStore.fetchAllDatasets(),
      mlStore.fetchAllModels()
    ])
    if (activeDashboardTab.value === 'analytics') {
      nextTick(() => initCharts())
    }
  } catch (error) {
    console.error("Dashboard Sync Error:", error)
  } finally {
    if (!isSilent) isLoading.value = false
  }
}

// Chart Logic
const initCharts = () => {
  if (!performanceChartCanvas.value) return
  if (performanceChart) performanceChart.destroy()
  
  const ctx = performanceChartCanvas.value.getContext('2d')
  
  const gradient = ctx.createLinearGradient(0, 0, 0, 300)
  gradient.addColorStop(0, 'rgba(102, 126, 234, 0.4)')
  gradient.addColorStop(1, 'rgba(102, 126, 234, 0)')

  const sortedModels = [...allModels.value].sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt)).slice(-7)
  
  if (!sortedModels.length) {
    // Show empty state if no models
    performanceChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['No Data'],
        datasets: [{
          label: 'Accuracy',
          data: [0],
          borderColor: 'rgba(106, 106, 138, 0.2)',
          backgroundColor: 'transparent',
          fill: true,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { display: false } },
          x: { grid: { display: false }, ticks: { color: '#6a6a8a' } }
        }
      }
    })
    return
  }
  
  // Helper: resolve the best accuracy-equivalent metric across all validation methods
  // train_test_split   -> accuracy / r2
  // kfold_cv           -> cv_mean  / test_accuracy / test_r2
  // grid_search        -> best_score / cv_mean / test_accuracy / test_r2
  // randomized_search  -> best_score / cv_mean / test_accuracy / test_r2
  const resolveAccuracy = (metrics) => {
    if (!metrics) return 0
    return metrics.accuracy
      ?? metrics.cv_mean
      ?? metrics.best_score
      ?? metrics.test_accuracy
      ?? metrics.r2
      ?? metrics.test_r2
      ?? 0
  }

  const labels = sortedModels.map(m => m.name.split(' ')[0])
  const data = sortedModels.map(m => {
    const acc = resolveAccuracy(m.metrics)
    return acc <= 1 ? acc * 100 : acc
  })

  performanceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Accuracy',
        data,
        borderColor: '#667eea',
        backgroundColor: gradient,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 15, 35, 0.9)',
          padding: 12,
          displayColors: false
        }
      },
      scales: {
        y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#6a6a8a' } },
        x: { grid: { display: false }, ticks: { color: '#6a6a8a' } }
      }
    }
  })
}

// Upload Handling
const triggerFileInput = () => {
    if (allDatasets.value.length >= 30) {
      showLimitModal.value = true
      return
    }
    if (!isUploading.value && !uploadSuccess.value) fileInput.value?.click()
}

const handleFileSelect = (e) => {
    const file = e.target.files?.[0]
    if (file) processFile(file)
}

const handleDrop = (e) => {
    dragOver.value = false
    const file = e.dataTransfer.files?.[0]
    if (file) processFile(file)
}

const processFile = async (file) => {
  if (allDatasets.value.length >= 30) {
    showLimitModal.value = true
    return
  }
  const { resolveUrl } = useAuthenticatedFetch()
  isUploading.value = true
  uploadSuccess.value = false
  uploadProgress.value = 0
  uploadMessage.value = 'Preparing upload...'
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    // Get JWT token from storage consistently with useAuthenticatedFetch
    const token = sessionStorage.getItem('token') || 
                  sessionStorage.getItem('authToken') || 
                  localStorage.getItem('token') || 
                  localStorage.getItem('authToken')
    
    const finalUrl = resolveUrl(`/api/upload-dataset`)
    
    const response = await axios.post(finalUrl, formData, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'ngrok-skip-browser-warning': 'true'
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadProgress.value = percentCompleted
          
          if (percentCompleted < 100) {
            const uploadedKB = Math.round(progressEvent.loaded / 1024)
            const totalKB = Math.round(progressEvent.total / 1024)
            uploadMessage.value = `Uploading stream... (${uploadedKB} KB / ${totalKB} KB)`
          } else {
            uploadMessage.value = 'Gathering Intelligence... (Analyzing data structure)'
          }
        } else {
          uploadMessage.value = 'Uploading stream...'
        }
      }
    })
    
    const result = response.data
    uploadProgress.value = 100
    uploadSuccess.value = true
    isUploading.value = false 
    uploadedFile.value = result
    
    mlStore.setCurrentDataset(result.dataset_id, [], result.filename, result.columns || [])
    experimentStore.setDataset(result.dataset_id, result.filename)
    
    fetchData(true)
  } catch (error) {
    console.error('Core Upload Error:', error)
    const errorMsg = error.response?.data?.detail || error.message || 'Network intelligence failure'
    showError('Upload Failed', errorMsg)
    isUploading.value = false
  }
}

// UI Helpers
const getActionIcon = (type) => {
  const icons = { 
    upload: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>`, 
    train: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`, 
    cleaning: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`, 
    preprocess: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>` 
  }
  return icons[type] || `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`
}

const formatActionTitle = (act) => {
  if (act.action_type === 'upload') return `Uploaded ${act.details?.filename}`
  if (act.action_type === 'train') return `Trained ${act.details?.algorithm}`
  return `Applied ${act.action_type}`
}

const resolveModelAccuracy = (metrics) => {
  if (!metrics) return 0
  return metrics.accuracy
    ?? metrics.cv_mean
    ?? metrics.best_score
    ?? metrics.test_accuracy
    ?? metrics.r2
    ?? metrics.test_r2
    ?? 0
}

const formatAccuracy = (m) => {
  const acc = resolveModelAccuracy(m.metrics)
  return (acc <= 1 ? acc * 100 : acc).toFixed(1)
}

const getRelativeTime = (dateStr) => {
  if (!dateStr) return '-'
  const now = new Date()
  const past = new Date(dateStr)
  const diff = Math.floor((now - past) / 1000)
  
  if (diff < 5) return 'Just now'
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const formatFileSize = (bytes) => {
  if (!bytes || isNaN(bytes)) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Navigation
const navigateTo = (path) => router.push(path)
const logout = () => { sessionStorage.clear(); localStorage.clear(); navigateTo('/login') }
const useSampleData = () => { showSampleModal.value = true }
const resumeLastSession = () => {
  const latest = sortedDatasets.value[0]
  if (!latest) return
  analyzeDataset(latest)
}
const analyzeDataset = (ds) => {
  mlStore.setCurrentDataset(ds.id, [], ds.name, [])
  experimentStore.setDataset(ds.id, ds.name)
  navigateTo('/data-preview')
}

const deleteDataset = (ds) => {
  datasetToDelete.value = ds
  showDeleteModal.value = true
}

const cancelDelete = () => {
  if (isDeleting.value) return
  showDeleteModal.value = false
  datasetToDelete.value = null
}

const confirmDelete = async () => {
  if (!datasetToDelete.value || isDeleting.value) return
  
  isDeleting.value = true
  try {
    const { authenticatedDelete } = useAuthenticatedFetch()
    const response = await authenticatedDelete(`/api/datasets/${datasetToDelete.value.id}`)
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Purge failed')
    }
    
    // Refresh data
    await fetchData(true)
    showDeleteModal.value = false
    datasetToDelete.value = null
    // alert('Intelligence purged successfully') // Optional: already visible in feed
  } catch (error) {
    console.error('Purge Error:', error)
    showError('Purge Failed', error.message)
  } finally {
    isDeleting.value = false
  }
}

const downloadDataset = async (ds) => {
  try {
    const { authenticatedGet } = useAuthenticatedFetch()
    const response = await authenticatedGet(`/api/export-dataset/${ds.id}`)
    
    if (!response.ok) throw new Error('Download failed')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${ds.name.replace('.csv', '')}_download.csv`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('Download Error:', error)
    showError('Download Failed', error.message)
  }
}

const downloadModel = async (model) => {
  try {
    const { authenticatedGet } = useAuthenticatedFetch()
    const response = await authenticatedGet(`/api/models/${model.id}/download`)
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Download failed')
    }
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${model.name.replace(/\s+/g, '_')}.joblib`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('Model Download Error:', error)
    showError('Model Download Failed', error.message)
  }
}

const getBriefMetrics = (model) => {
  if (!model.metrics) return {}
  const m = model.metrics
  
  // Common classification metrics — include cv_mean / best_score for KFold/Grid/Randomized methods
  const acc = m.accuracy ?? m.cv_mean ?? m.best_score ?? m.test_accuracy ?? m.val_accuracy
  const f1 = m.f1 ?? m.test_f1 ?? m.val_f1 ?? m.weighted_f1 ?? m.macro_f1
  
  // Common regression metrics
  const r2 = m.r2 ?? m.test_r2 ?? m.cv_mean ?? m.val_r2
  const mae = m.mae ?? m.test_mae ?? m.val_mae
  
  // Choose relevant pair based on availability
  if (acc !== undefined) return { acc, f1 }
  if (r2 !== undefined) return { r2, mae }
  
  // Fallback to first two keys
  const keys = Object.keys(model.metrics).filter(k => k !== 'validation_method').slice(0, 2)
  const result = {}
  keys.forEach(k => result[k] = model.metrics[k])
  return result
}

const getBriefConfig = (model) => {
  if (!model.hyperparameters) return {}
  const important = ['n_estimators', 'max_depth', 'learning_rate', 'C', 'alpha', 'n_neighbors']
  const result = {}
  let count = 0
  
  for (const key of important) {
    if (model.hyperparameters[key] !== undefined) {
      result[key] = model.hyperparameters[key]
      count++
      if (count >= 3) break
    }
  }
  
  // Fallback if none of the important ones found
  if (count < 3) {
    for (const key in model.hyperparameters) {
      if (!result.hasOwnProperty(key)) {
        result[key] = model.hyperparameters[key]
        count++
        if (count >= 3) break
      }
    }
  }
  
  return result
}

const getHiddenConfig = (model) => {
  if (!model.hyperparameters) return {}
  const shown = Object.keys(getBriefConfig(model))
  const hidden = {}
  Object.keys(model.hyperparameters).forEach(k => {
    if (!shown.includes(k)) hidden[k] = model.hyperparameters[k]
  })
  return hidden
}

const formatHyperparam = (val) => {
  if (typeof val === 'number') return val % 1 === 0 ? val : val.toFixed(4)
  return val
}

const formatMetricKey = (key) => {
  const map = { 'acc': 'ACC', 'f1': 'F1', 'r2': 'R²', 'mae': 'MAE', 'mse': 'MSE', 'rmse': 'RMSE' }
  return map[key] || key.substring(0, 3).toUpperCase()
}

const formatMetricValue = (val) => {
  if (val === undefined || val === null) return '-'
  return typeof val === 'number' ? (val < 1 ? val.toFixed(3) : val.toFixed(1)) : val
}

const getMetricClass = (key) => {
  if (['acc', 'f1', 'r2'].includes(key)) return 'positive'
  if (['mae', 'mse', 'rmse'].includes(key)) return 'neutral'
  return ''
}

const viewTraining = (model) => {
  // Logic to navigate to training results/visualization
  mlStore.selectedModelId = model.id
  navigateTo('/model-visualization')
}
const goToPreview = () => {
  // Set the dataset context synchronously so data-preview knows what to load
  if (uploadedFile.value) {
    mlStore.setCurrentDataset(
      uploadedFile.value.dataset_id,
      [],
      uploadedFile.value.filename,
      uploadedFile.value.columns || []
    )
    experimentStore.setDataset(uploadedFile.value.dataset_id, uploadedFile.value.filename)
  }
  // Navigate immediately — data-preview's own spinner handles the rest
  router.push('/data-preview')
}

// Watchers
watch(activeDashboardTab, (newVal) => {
  if (newVal === 'analytics') nextTick(() => initCharts())
})

// Lifecycle
onMounted(() => fetchData())
onUnmounted(() => performanceChart?.destroy())

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

.dashboard {
  min-height: 100vh;
  background: #0b0b1a;
  background-image: 
    radial-gradient(circle at 0% 0%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(118, 75, 162, 0.05) 0%, transparent 50%);
  color: #ffffff;
  font-family: 'Outfit', sans-serif;
}

/* Glass & Premium Cards */
.glass {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
}

/* Dashboard Content */
.dashboard-content { padding: 4rem; max-width: 1400px; margin: 0 auto; }

/* Welcome Section */
.welcome-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; }
.welcome-text h1 { font-size: 2.75rem; font-weight: 900; letter-spacing: -1.5px; margin: 0; }
.gradient-text { background: linear-gradient(135deg, #667eea, #a88beb); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.welcome-text p { color: #6a6a8a; font-size: 1.1rem; margin-top: 0.5rem; }
.refresh-btn-mini { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #4a4a6a; padding: 10px; border-radius: 50%; cursor: pointer; transition: all 0.3s; }
.refresh-btn-mini:hover { color: #667eea; border-color: #667eea; transform: rotate(180deg); }

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 4rem; }
.kpi-card { padding: 1.75rem; border-radius: 28px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.05); transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); cursor: pointer; position: relative; overflow: hidden; }
.kpi-card:hover { transform: translateY(-10px); background: rgba(255,255,255,0.04); border-color: rgba(102, 126, 234, 0.3); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }

.kpi-icon-circle { width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem; transition: transform 0.3s; }
.kpi-card:hover .kpi-icon-circle { transform: scale(1.1) rotate(-5deg); }
.kpi-icon-circle.blue { background: rgba(102, 126, 234, 0.1); color: #667eea; }
.kpi-icon-circle.purple { background: rgba(168, 139, 235, 0.1); color: #a88beb; }
.kpi-icon-circle.emerald { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.kpi-icon-circle.indigo { background: rgba(129, 140, 248, 0.1); color: #818cf8; }

.kpi-label { color: #6a6a8a; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { font-size: 2.25rem; font-weight: 800; margin: 0.5rem 0; letter-spacing: -1px; }
.kpi-sub { font-size: 0.8rem; color: #4a4a6a; }
.latest-entry { margin-top: 0.5rem; }
.entry-name { font-weight: 600; font-size: 0.9rem; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.entry-meta { font-size: 0.75rem; color: #6a6a8a; }

.kpi-content-row { display: flex; justify-content: space-between; align-items: flex-end; }
.health-percentage { font-size: 2.25rem; font-weight: 800; color: #10b981; margin: 0.5rem 0; }
.health-donut-mini { width: 40px; height: 40px; }
.circular-chart { display: block; margin: 0; max-width: 100%; max-height: 100%; }
.circle-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 3.8; }
.circle { fill: none; stroke: #10b981; stroke-width: 3.8; stroke-linecap: round; transition: stroke-dasharray 1s ease; }

/* Quick Actions */
.section-title { font-size: 1.25rem; font-weight: 800; margin-bottom: 1.5rem; color: #b3b3d1; }
.quick-actions-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 4rem; }
.action-card { display: flex; gap: 1.25rem; padding: 1.5rem; border-radius: 24px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); cursor: pointer; transition: all 0.3s; }
.action-card:hover { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); transform: scale(1.02); }

.action-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.action-icon.upload { background: rgba(102, 126, 234, 0.1); color: #667eea; }
.action-icon.sample { background: rgba(168, 139, 235, 0.1); color: #a88beb; }
.action-icon.resume { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.action-icon.guide { background: rgba(129, 140, 248, 0.1); color: #818cf8; }

.action-text h3 { margin: 0; font-size: 1.1rem; font-weight: 700; }
.action-text p { margin: 4px 0 0; font-size: 0.85rem; color: #6a6a8a; }
.action-text p strong { color: #a88beb; font-weight: 600; }

.disabled-action { opacity: 0.45; cursor: not-allowed; pointer-events: none; }

/* Immersive Upload Section */
.upload-immersive-section { display: flex; justify-content: center; margin-top: 2rem; }
.upload-compact-container { width: 100%; max-width: 800px; padding: 1.5rem 2.5rem; text-align: center; }
.upload-header-compact h2 { font-size: 1.5rem; font-weight: 800; margin: 0; }
.upload-header-compact p { color: #6a6a8a; font-size: 0.9rem; margin-top: 8px; }

.upload-compact-zone { margin-top: 1.5rem; border: 2px dashed rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 2rem; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; background: rgba(102, 126, 234, 0.02); }
.upload-compact-zone:hover { border-color: #667eea; background: rgba(102, 126, 234, 0.05); }
.upload-compact-zone.drag-over { border-color: #10b981; background: rgba(16, 185, 129, 0.05); transform: scale(1.02); }

.prompt-icon-mini { margin-bottom: 1.5rem; color: #667eea; }
.upload-prompt-compact h3 { font-size: 1.25rem; font-weight: 700; margin: 0; }
.upload-prompt-compact p { color: #5a5a7a; font-size: 0.9rem; margin-top: 4px; }
.format-badges { display: flex; justify-content: center; gap: 8px; margin-top: 1.5rem; }
.format-badges span { font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 6px; transition: all 0.3s; }
.format-badges span.fmt-csv { background: rgba(102, 126, 234, 0.1); color: #667eea; border: 1px solid rgba(102, 126, 234, 0.2); }
.format-badges span.fmt-json { background: rgba(168, 139, 235, 0.1); color: #a88beb; border: 1px solid rgba(168, 139, 235, 0.2); }
.format-badges span.fmt-excel { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
.format-badges span.fmt-parquet { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }

.premium-spinner { width: 40px; height: 40px; border: 3px solid rgba(102, 126, 234, 0.1); border-top-color: #667eea; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1.5rem; }
.mini-progress-bar { width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; margin: 1.5rem 0; overflow: hidden; }
.mini-progress-bar .fill { height: 100%; background: linear-gradient(to right, #667eea, #a88beb); transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }

.success-icon-wrap { width: 60px; height: 60px; background: rgba(16, 185, 129, 0.1); color: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin: 0 auto 1.5rem; border: 1px solid rgba(16, 185, 129, 0.2); }
.launch-btn-premium { background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 12px 32px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: all 0.3s; margin-top: 1rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }
.launch-btn-premium:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4); }

/* Tab Views Common */
.tab-view { width: 100%; }
.view-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5rem; }
.header-main h2 { font-size: 2.25rem; font-weight: 900; margin: 0; letter-spacing: -1px; }
.header-main p { color: #6a6a8a; margin-top: 6px; }

/* Table Styling */
.table-container { padding: 1.5rem; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 1.25rem 1rem; color: #4a4a6a; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 800; border-bottom: 1px solid rgba(255,255,255,0.03); }
td { padding: 1.5rem 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.02); color: #b3b3d1; font-size: 0.95rem; }
.table-row-hover:hover { background: rgba(255, 255, 255, 0.01); }

.file-name-cell, .model-name-cell { display: flex; align-items: center; gap: 12px; font-weight: 600; color: #ffffff; }
.file-icon-mini, .model-icon-mini { width: 28px; height: 28px; background: rgba(255,255,255,0.03); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #667eea; }

.status-pill { font-size: 0.7rem; font-weight: 800; padding: 4px 12px; border-radius: 30px; background: rgba(255,255,255,0.03); color: #4a4a6a; text-transform: uppercase; }
.status-pill.processed { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.1); }

.model-info-stack { display: flex; flex-direction: column; gap: 2px; }
.model-name-text { font-weight: 600; color: #ffffff; }
.model-date-mini { font-size: 0.75rem; color: #6a6a8a; }

.metrics-pill-group { display: flex; gap: 8px; flex-wrap: wrap; }
.metric-pill { display: flex; align-items: center; border-radius: 8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); overflow: hidden; font-size: 0.75rem; }
.metric-pill.positive { border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.05); }
.metric-pill.neutral { border-color: rgba(102, 126, 234, 0.3); background: rgba(102, 126, 234, 0.05); }
.metric-label { padding: 4px 8px; background: rgba(255,255,255,0.02); color: #6a6a8a; font-weight: 800; border-right: 1px solid rgba(255,255,255,0.05); }
.metric-value { padding: 4px 10px; color: #ffffff; font-weight: 700; }
.metric-pill.positive .metric-value { color: #10b981; }

.config-badges { display: flex; gap: 6px; flex-wrap: wrap; }
.config-badge { font-size: 0.7rem; font-weight: 600; padding: 4px 10px; border-radius: 6px; background: rgba(168, 139, 235, 0.05); color: #a88beb; border: 1px solid rgba(168, 139, 235, 0.1); position: relative; }
.config-badge.more { background: rgba(255,255,255,0.03); color: #6a6a8a; border-style: dashed; cursor: help; }

.config-tooltip {
  position: absolute;
  bottom: 140%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 15, 30, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(168, 139, 235, 0.3);
  padding: 12px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  display: none;
  z-index: 100;
  min-width: 180px;
}
.config-badge.more:hover .config-tooltip { display: block; }
.tooltip-item { display: flex; justify-content: space-between; gap: 15px; margin-bottom: 6px; white-space: nowrap; align-items: center; }
.tooltip-item:last-child { margin-bottom: 0; }
.t-key { color: #6a6a8a; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.t-val { color: #ffffff; font-weight: 700; font-size: 0.75rem; background: rgba(168, 139, 235, 0.1); padding: 2px 6px; border-radius: 4px; }

.algo-badge { background: rgba(168, 139, 235, 0.1); color: #a88beb; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
.accuracy-cell-premium { font-weight: 800; color: #10b981; font-size: 1.1rem; }

.btn-table-action { background: none; border: 1px solid rgba(102, 126, 234, 0.3); color: #667eea; padding: 8px 16px; border-radius: 80px; font-size: 0.8rem; font-weight: 700; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }
.btn-table-action:hover { background: #667eea; color: white; transform: scale(1.05); }
.btn-table-action.secondary { border-color: rgba(255, 255, 255, 0.1); color: #6a6a8a; padding: 8px; }
.btn-table-action.secondary:hover { border-color: #667eea; color: #667eea; background: rgba(102, 126, 234, 0.1); }
.btn-table-action.danger { border-color: rgba(239, 68, 68, 0.1); color: #4a4a6a; padding: 8px; }
.btn-table-action.danger:hover { border-color: #ef4444; color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.inventory-header-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: 8px;
  gap: 1rem;
}

.dataset-limit-pill {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.dataset-limit-pill.warning {
  border-color: rgba(244, 158, 11, 0.3);
  background: rgba(244, 158, 11, 0.05);
}

.dataset-limit-pill.danger {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
  animation: pulse-border 2s infinite;
}

.dataset-limit-pill .count {
  color: #667eea;
}

.dataset-limit-pill.warning .count { color: #f59e0b; }
.dataset-limit-pill.danger .count { color: #ef4444; }

.dataset-limit-pill .limit {
  color: #6a6a8a;
  font-size: 0.75rem;
}

@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
  70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* Custom Delete Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(5, 5, 15, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.5rem;
}

.modal-container {
  width: 100%;
  max-width: 480px;
  background: rgba(15, 15, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  text-align: center;
}

.modal-header {
  margin-bottom: 2rem;
}

.warning-icon-animate {
  width: 64px;
  height: 64px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  animation: shake 2s infinite ease-in-out;
}

.modal-header h2 {
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff, #ef4444);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.modal-body {
  margin-bottom: 2.5rem;
  color: #b3b3d1;
  line-height: 1.6;
}

.highlight-name {
  color: #ffffff;
  font-weight: 700;
  font-family: monospace;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.warning-box {
  background: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.1);
  border-radius: 16px;
  padding: 1.25rem;
  margin-top: 1.5rem;
}

.warning-box p {
  color: #ef4444;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.btn-modal {
  flex: 1;
  padding: 14px 24px;
  border-radius: 16px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-modal.secondary {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #b3b3d1;
}

.btn-modal.secondary:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.btn-modal.danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  color: #ffffff;
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.25);
}

.btn-modal.danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(239, 68, 68, 0.35);
}

.btn-modal:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.spinner-mini {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* Animations */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container {
  animation: modal-pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes modal-pop {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes shake {
  0%, 100% { transform: translateY(0); }
  25% { transform: translateY(-4px) rotate(-1deg); }
  75% { transform: translateY(2px) rotate(1deg); }
}

.action-group-mini { display: flex; gap: 8px; align-items: center; }

/* Analytics Grid */
.analytics-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 2rem; }
.chart-container-premium { padding: 0; }
.chart-wrapper { height: 400px; margin-top: 1.5rem; padding: 0 2rem 2rem; }

.activity-container-premium { display: flex; flex-direction: column; overflow: hidden; }
.activity-feed { padding: 1.5rem; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; }

.container-header {
  padding: 1.5rem 2rem 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.container-header h3 {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.5px;
}

.count-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.activity-item-premium { 
  display: flex; 
  gap: 1.25rem; 
  padding: 1.25rem; 
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 20px; 
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.activity-item-premium:hover { 
  background: rgba(255, 255, 255, 0.05); 
  border-color: rgba(102, 126, 234, 0.3);
  transform: translateX(4px);
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

.activity-item-premium::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: #667eea;
  transition: height 0.3s ease;
  border-radius: 0 4px 4px 0;
}

.activity-item-premium:hover::before {
  height: 60%;
}

.item-icon-wrapper { 
  width: 48px; 
  height: 48px; 
  border-radius: 16px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  background: rgba(255, 255, 255, 0.03); 
  border: 1px solid rgba(255, 255, 255, 0.05); 
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.activity-item-premium:hover .item-icon-wrapper {
  transform: scale(1.1) rotate(-5deg);
}

.item-icon-wrapper.upload { color: #667eea; background: rgba(102, 126, 234, 0.1); border-color: rgba(102, 126, 234, 0.2); }
.item-icon-wrapper.train { color: #10b981; background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.2); }
.item-icon-wrapper.cleaning { color: #f59e0b; background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.2); }
.item-icon-wrapper.preprocess { color: #8b5cf6; background: rgba(139, 92, 246, 0.1); border-color: rgba(139, 92, 246, 0.2); }

.item-content { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.item-header { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; }
.item-title { font-weight: 700; font-size: 0.95rem; color: #ffffff; letter-spacing: -0.01em; }
.item-timestamp { font-size: 0.75rem; color: #6a6a8a; font-weight: 500; }
.item-subtext { font-size: 0.8rem; color: #4a4a6a; margin-top: 4px; }

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.01); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(102, 126, 234, 0.2); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05); }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(102, 126, 234, 0.4); }

/* Empty States */
.empty-state-view { text-align: center; padding: 6rem 1rem; }
.empty-illustration { font-size: 4rem; opacity: 0.2; margin-bottom: 1.5rem; }
.empty-state-view h3 { font-size: 1.5rem; margin: 0; }
.empty-state-view p { color: #5a5a7a; margin: 8px 0 2rem; }
.btn-outline { background: none; border: 1px solid #667eea; color: #667eea; padding: 12px 28px; border-radius: 12px; font-weight: 800; cursor: pointer; }

/* Misc */
.loader-container p { color: #b3b3d1; font-weight: 500; }
.hidden-input { display: none; }
.text-capitalize { text-transform: capitalize; }

/* Transitions */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.fade-slide-enter-from { opacity: 0; transform: translateY(20px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 1200px) {
  .kpi-grid, .quick-actions-grid { grid-template-columns: repeat(2, 1fr); }
  .analytics-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .dashboard-header { padding: 1rem 2rem; }
  .nav-links { display: none; }
  .kpi-grid, .quick-actions-grid { grid-template-columns: 1fr; }
  .dashboard-content { padding: 2rem; }
}
</style>
