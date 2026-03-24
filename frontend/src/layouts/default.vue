<template>
  <div class="main-layout">
    <GlobalNavbar v-if="showGlobalNavbar" />
    <DatasetContextBar v-if="showContextBar" @save-version="openSaveModal" />
    
    <main class="content-area"> 
      <slot />
    </main>

    <!-- Internal Save Modal for Context Bar -->
    <div v-if="showSaveModal" class="save-modal-overlay" @click.self="showSaveModal = false">
      <div class="save-modal" @click.stop>
        <h3>Save Dataset Version</h3>
        <p>Save the current state of your dataset as a new version in your inventory.</p>
        <label class="version-label">Version Name</label>
        <input 
          v-model="versionName" 
          type="text" 
          placeholder="e.g., v2 REFINED" 
          class="version-input"
          @keyup.enter="saveVersion"
        />
        <div class="modal-actions">
          <button @click="showSaveModal = false" class="btn-cancel">Cancel</button>
          <button @click="saveVersion" class="btn-confirm" :disabled="!versionName">Save Version</button>
        </div>
      </div>
    </div>

    <!-- Save Success Toast -->
    <transition name="toast-slide">
      <div v-if="saveToast.visible" class="save-toast">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="toast-icon">
          <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
        </svg>
        <span>{{ saveToast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMLDataFlowStore } from '~/stores/mlDataFlow'
import { useExperimentStore } from '~/stores/experiment'
import GlobalNavbar from '~/components/GlobalNavbar.vue'
import DatasetContextBar from '~/components/DatasetContextBar.vue'

const route = useRoute()
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()

const showSaveModal = ref(false)
const versionName = ref('')

// Toast state
const saveToast = ref({ visible: false, message: '' })
let toastTimer = null

const showSaveSuccessToast = (datasetName) => {
  if (toastTimer) clearTimeout(toastTimer)
  saveToast.value = {
    visible: true,
    message: `"${datasetName}" was saved successfully in inventory`
  }
  toastTimer = setTimeout(() => {
    saveToast.value.visible = false
  }, 3500)
}

// Pipeline routes — used to control context bar visibility only
const PIPELINE_ROUTES = [
  'data-preview',
  'target-selection',
  'advanced-preprocessing',
  'algorithm-select',
  'model-training',
  'model-visualization'
]

// Only show context bar on pipeline pages
const showContextBar = computed(() => PIPELINE_ROUTES.includes(route.name))

// Hide global navbar on landing and login pages
const showGlobalNavbar = computed(() => {
  return !['index', 'login'].includes(route.name)
})

// Context-bar "Save Dataset Version" button handler
const openSaveModal = () => {
  // Prefill with a suggested name
  versionName.value = mlStore.getNextVersionName()
  showSaveModal.value = true
}

// Resolve dataset ID from the active pipeline context
const resolveDatasetId = () =>
  mlStore.datasetId || mlStore.currentDataset || experimentStore.datasetId || null

const saveVersion = async () => {
  if (!versionName.value) return

  const savedName = versionName.value
  const datasetId = resolveDatasetId()

  if (!datasetId) {
    saveToast.value = { visible: true, message: 'No active dataset — please re-open your dataset first.' }
    setTimeout(() => { saveToast.value.visible = false }, 4000)
    return
  }

  try {
    await mlStore.saveDatasetVersion(datasetId, savedName)
    showSaveModal.value = false
    versionName.value = ''
    showSaveSuccessToast(savedName)
  } catch (err) {
    saveToast.value = { visible: true, message: `Save failed: ${err.message}` }
    setTimeout(() => { saveToast.value.visible = false }, 4000)
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #0b0b1a;
  color: #ffffff;
}

.content-area {
  flex: 1;
  overflow-y: auto;
}

.save-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
}

.save-modal {
  background: #1a1a2e;
  padding: 24px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.save-modal h3 { margin-bottom: 8px; }
.save-modal p { color: #b3b3d1; font-size: 0.9rem; margin-bottom: 12px; }

.version-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #b3b3d1;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.version-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px;
  border-radius: 8px;
  color: white;
  margin-bottom: 24px;
  font-size: 1rem;
}

.modal-actions { display: flex; justify-content: flex-end; align-items: center; gap: 12px; }

.btn-cancel { background: transparent; border: none; color: #b3b3d1; cursor: pointer; padding: 8px 16px; }
.btn-confirm { 
    background: linear-gradient(135deg, #667eea, #764ba2); 
    color: white; 
    border: none; 
    padding: 8px 16px; 
    border-radius: 6px; 
    cursor: pointer;
    font-weight: 600;
}
.btn-confirm:disabled { opacity: 0.5; cursor: not-allowed; }

/* Save Success Toast */
.save-toast {
  position: fixed;
  bottom: 28px;
  right: 28px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #1a2a1a 0%, #1a2e1a 100%);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #10b981;
  padding: 12px 18px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  z-index: 20000;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(16, 185, 129, 0.1);
  backdrop-filter: blur(8px);
  max-width: 400px;
}

.toast-icon {
  flex-shrink: 0;
  color: #10b981;
}

/* Toast transition */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-slide-enter-from,
.toast-slide-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.96);
}
</style>
