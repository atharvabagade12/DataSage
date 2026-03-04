<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="show" class="sdm-overlay" @click.self="$emit('close')">
        <div class="sdm-modal">
          <!-- Header -->
          <div class="sdm-header">
            <div class="sdm-header-left">
              <div class="sdm-header-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2H2v10h10V2zM22 12h-10v10h10V12zM12 12H2v10h10V12zM22 2h-10v10h10V2z"/>
                </svg>
              </div>
              <div>
                <h2>Sample Datasets</h2>
                <p>Pick a curated dataset to start your ML journey</p>
              </div>
            </div>
            <button class="sdm-close" @click="$emit('close')">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Gallery View -->
          <Transition name="slide-fade" mode="out-in">
            <div v-if="!selectedDataset" key="gallery" class="sdm-body">
              <div class="sdm-grid">
                <div
                  v-for="ds in datasets"
                  :key="ds.id"
                  class="sdm-card"
                  @click="selectedDataset = ds"
                >
                  <div class="sdm-card-top">
                    <div class="sdm-card-icon" :style="{ background: ds.iconBg, color: ds.iconColor }">
                      <span v-html="ds.icon"></span>
                    </div>
                    <span class="sdm-badge" :class="ds.badgeClass">{{ ds.type }}</span>
                  </div>
                  <div class="sdm-card-body">
                    <h3>{{ ds.name }}</h3>
                    <p>{{ ds.tagline }}</p>
                    <div class="sdm-card-meta">
                      <span>{{ ds.rows.toLocaleString() }} rows</span>
                      <span>·</span>
                      <span>{{ ds.cols }} features</span>
                    </div>
                  </div>
                  <div class="sdm-card-footer">
                    <span class="sdm-target-hint">🎯 Target: <strong>{{ ds.target }}</strong></span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="9 18 15 12 9 6"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Detail View -->
            <div v-else key="detail" class="sdm-body">
              <button class="sdm-back" @click="selectedDataset = null">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="15 18 9 12 15 6"/>
                </svg>
                Back to gallery
              </button>

              <div class="sdm-detail">
                <div class="sdm-detail-header">
                  <div class="sdm-card-icon lg" :style="{ background: selectedDataset.iconBg, color: selectedDataset.iconColor }">
                    <span v-html="selectedDataset.icon"></span>
                  </div>
                  <div>
                    <div class="sdm-detail-title-row">
                      <h3>{{ selectedDataset.name }}</h3>
                      <span class="sdm-badge" :class="selectedDataset.badgeClass">{{ selectedDataset.type }}</span>
                    </div>
                    <div class="sdm-card-meta">
                      <span>{{ selectedDataset.rows.toLocaleString() }} rows</span>
                      <span>·</span>
                      <span>{{ selectedDataset.cols }} features</span>
                      <span>·</span>
                      <span>CSV format</span>
                    </div>
                  </div>
                </div>

                <p class="sdm-description">{{ selectedDataset.description }}</p>

                <div class="sdm-columns-section">
                  <h4>Columns</h4>
                  <div class="sdm-columns">
                    <span
                      v-for="col in selectedDataset.columns"
                      :key="col"
                      class="sdm-col-chip"
                      :class="{ 'sdm-col-target': col === selectedDataset.target }"
                    >
                      {{ col === selectedDataset.target ? '🎯 ' : '' }}{{ col }}
                    </span>
                  </div>
                </div>

                <div class="sdm-target-box">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
                  </svg>
                  <span>Suggested Target: <strong>{{ selectedDataset.target }}</strong></span>
                </div>
              </div>

              <!-- Loading state -->
              <div v-if="isLoading" class="sdm-loading">
                <div class="sdm-spinner"></div>
                <p>{{ loadingMessage }}</p>
              </div>
            </div>
          </Transition>

          <!-- Footer -->
          <div class="sdm-footer">
            <button class="sdm-btn-cancel" @click="$emit('close')" :disabled="isLoading">Cancel</button>
            <button
              v-if="selectedDataset"
              class="sdm-btn-use"
              @click="useDataset"
              :disabled="isLoading"
            >
              <svg v-if="!isLoading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
              <span>{{ isLoading ? loadingMessage : 'Use This Dataset' }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMLDataFlowStore } from '@/stores/mlDataFlow'
import { useExperimentStore } from '@/stores/experiment'
import { useAuthenticatedFetch } from '@/composables/useAuthenticatedFetch'
import axios from 'axios'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close'])

const router = useRouter()
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()

const selectedDataset = ref(null)
const isLoading = ref(false)
const loadingMessage = ref('')

const datasets = [
  {
    id: 'churn',
    name: 'Churn Modelling',
    file: '/sample-datasets/churn.csv',
    type: 'Binary Classification',
    badgeClass: 'badge-binary',
    tagline: 'Predict which bank customers will leave',
    description: 'A classic binary classification dataset containing 10,000 bank customer records. Features include credit score, geography, gender, age, tenure, balance, and more. The goal is to predict whether a customer will churn (leave the bank).',
    rows: 10000,
    cols: 14,
    target: 'Exited',
    columns: ['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited'],
    icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    iconBg: 'rgba(102, 126, 234, 0.12)',
    iconColor: '#667eea'
  },
  {
    id: 'iris',
    name: 'Iris Flowers',
    file: '/sample-datasets/iris.csv',
    type: 'Multi-Class Classification',
    badgeClass: 'badge-multi',
    tagline: 'Classify 3 species of iris flowers',
    description: 'The legendary Iris dataset — perfect for getting started with multi-class classification. Contains 150 samples across 3 iris species (setosa, versicolor, virginica), described by sepal and petal measurements.',
    rows: 150,
    cols: 6,
    target: 'Species',
    columns: ['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'],
    icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    iconBg: 'rgba(168, 139, 235, 0.12)',
    iconColor: '#a88beb'
  },
  {
    id: 'california',
    name: 'California Housing',
    file: '/sample-datasets/california.csv',
    type: 'Regression',
    badgeClass: 'badge-regression',
    tagline: 'Predict house prices across California',
    description: 'Real real-estate data from the 1990 California census. Each row represents a block group with aggregate statistics. Predict the median house value for California districts based on features like median income, housing age, and ocean proximity.',
    rows: 20640,
    cols: 10,
    target: 'median_house_value',
    columns: ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity'],
    icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    iconBg: 'rgba(16, 185, 129, 0.12)',
    iconColor: '#10b981'
  },
  {
    id: 'aqi',
    name: 'AQI Prediction',
    file: '/sample-datasets/aqi.csv',
    type: 'Regression',
    badgeClass: 'badge-regression',
    tagline: 'Forecast air quality index from pollutants',
    description: 'Daily Air Quality Index (AQI) data spanning 2021–2023. Features include PM2.5, PM10, NO2, SO2, CO, and Ozone readings. Predict the overall AQI score — a real-world environmental regression problem.',
    rows: 1097,
    cols: 12,
    target: 'AQI',
    columns: ['Date', 'Month', 'Year', 'Holidays_Count', 'Days', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'Ozone', 'AQI'],
    icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    iconBg: 'rgba(245, 158, 11, 0.12)',
    iconColor: '#f59e0b'
  }
]

const useDataset = async () => {
  if (!selectedDataset.value || isLoading.value) return
  isLoading.value = true
  loadingMessage.value = 'Fetching dataset...'

  try {
    // Fetch the CSV from /public
    const response = await fetch(selectedDataset.value.file)
    if (!response.ok) throw new Error('Failed to fetch sample CSV')
    const blob = await response.blob()
    const file = new File([blob], `${selectedDataset.value.id}.csv`, { type: 'text/csv' })

    loadingMessage.value = 'Uploading to your workspace...'

    const { resolveUrl } = useAuthenticatedFetch()
    const token = sessionStorage.getItem('token') ||
                  sessionStorage.getItem('authToken') ||
                  localStorage.getItem('token') ||
                  localStorage.getItem('authToken')

    const formData = new FormData()
    formData.append('file', file)

    const uploadResponse = await axios.post(resolveUrl('/api/upload-dataset'), formData, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'ngrok-skip-browser-warning': 'true'
      }
    })

    const result = uploadResponse.data
    loadingMessage.value = 'Loading pipeline...'

    mlStore.setCurrentDataset(result.dataset_id, [], result.filename, result.columns || [])
    experimentStore.setDataset(result.dataset_id, result.filename)

    emit('close')
    router.push('/data-preview')
  } catch (err) {
    console.error('Sample upload failed:', err)
    alert('Failed to load sample dataset: ' + (err.response?.data?.detail || err.message))
    isLoading.value = false
    loadingMessage.value = ''
  }
}
</script>

<style scoped>
/* ── Overlay ── */
.sdm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

/* ── Modal container ── */
.sdm-modal {
  background: #0f0f1a;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  width: 100%;
  max-width: 680px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 32px 80px rgba(0,0,0,0.6);
}

/* ── Header ── */
.sdm-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.75rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.sdm-header-left {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.sdm-header-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(168,139,235,0.12);
  color: #a88beb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sdm-header h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.sdm-header p {
  margin: 2px 0 0;
  font-size: 0.8rem;
  color: #6a6a8a;
}

.sdm-close {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  color: #888;
  border-radius: 10px;
  width: 34px;
  height: 34px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.sdm-close:hover { background: rgba(255,255,255,0.1); color: #fff; }

/* ── Body ── */
.sdm-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 1.75rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.1) transparent;
}

/* ── Dataset Grid ── */
.sdm-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.sdm-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 18px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.sdm-card:hover {
  background: rgba(255,255,255,0.06);
  border-color: rgba(168,139,235,0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.sdm-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.sdm-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sdm-card-icon.lg {
  width: 52px;
  height: 52px;
  border-radius: 16px;
}
.sdm-card-icon svg { display: block; }

/* ── Badges ── */
.sdm-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 20px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  white-space: nowrap;
}
.badge-binary { background: rgba(102,126,234,0.15); color: #667eea; border: 1px solid rgba(102,126,234,0.25); }
.badge-multi  { background: rgba(168,139,235,0.15); color: #a88beb; border: 1px solid rgba(168,139,235,0.25); }
.badge-regression { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.25); }

/* ── Card body/footer ── */
.sdm-card-body h3 { margin: 0; font-size: 0.95rem; font-weight: 700; color: #fff; }
.sdm-card-body p  { margin: 4px 0 0; font-size: 0.8rem; color: #6a6a8a; line-height: 1.4; }

.sdm-card-meta {
  display: flex;
  gap: 6px;
  font-size: 0.75rem;
  color: #555;
  margin-top: 4px;
}

.sdm-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255,255,255,0.05);
  color: #555;
}
.sdm-target-hint { font-size: 0.75rem; }
.sdm-target-hint strong { color: #8888cc; }

/* ── Detail view ── */
.sdm-back {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #6a6a8a;
  font-size: 0.82rem;
  cursor: pointer;
  margin-bottom: 1.25rem;
  padding: 0;
  transition: color 0.2s;
}
.sdm-back:hover { color: #a88beb; }

.sdm-detail { display: flex; flex-direction: column; gap: 1.25rem; }

.sdm-detail-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}
.sdm-detail-title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 4px;
}
.sdm-detail-title-row h3 { margin: 0; font-size: 1.15rem; font-weight: 700; color: #fff; }

.sdm-description {
  font-size: 0.875rem;
  color: #8888aa;
  line-height: 1.65;
  margin: 0;
  padding: 1rem;
  background: rgba(255,255,255,0.02);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.05);
}

.sdm-columns-section h4 {
  margin: 0 0 0.6rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #6a6a8a;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.sdm-columns {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.sdm-col-chip {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  color: #888;
}
.sdm-col-target {
  background: rgba(168,139,235,0.12);
  border-color: rgba(168,139,235,0.3);
  color: #a88beb;
  font-weight: 600;
}

.sdm-target-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.75rem 1rem;
  background: rgba(16,185,129,0.06);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 12px;
  color: #10b981;
  font-size: 0.85rem;
}
.sdm-target-box strong { font-weight: 700; }

/* ── Loading ── */
.sdm-loading {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  color: #a88beb;
  font-size: 0.85rem;
}
.sdm-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(168,139,235,0.3);
  border-top-color: #a88beb;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Footer ── */
.sdm-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.75rem 1.25rem;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.sdm-btn-cancel {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  color: #888;
  padding: 0.6rem 1.25rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}
.sdm-btn-cancel:hover:not(:disabled) { background: rgba(255,255,255,0.1); color: #fff; }
.sdm-btn-cancel:disabled { opacity: 0.4; cursor: not-allowed; }

.sdm-btn-use {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #a88beb, #667eea);
  color: #fff;
  border: none;
  padding: 0.65rem 1.4rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s;
}
.sdm-btn-use:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(168,139,235,0.35); }
.sdm-btn-use:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

/* ── Transitions ── */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.slide-fade-enter-active { transition: all 0.2s ease; }
.slide-fade-leave-active { transition: all 0.15s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateX(12px); }
.slide-fade-leave-to   { opacity: 0; transform: translateX(-12px); }

/* ── Responsive ── */
@media (max-width: 560px) {
  .sdm-grid { grid-template-columns: 1fr; }
  .sdm-modal { border-radius: 16px; }
}
</style>
