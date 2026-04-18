<template>
  <div class="main-layout">
    <GlobalNavbar v-if="showGlobalNavbar" />
    <DatasetContextBar v-if="showContextBar" @save-version="openSaveModal" />
    
    <main class="content-area"> 
      <slot />
    </main>

    <!-- Save Version Modal (Context Bar) -->
    <Modal v-model="showSaveModal" title="Save Dataset Version" size="md">
      <div class="modal-section" style="padding: 1.5rem;">
        <p class="modal-intro" style="margin-bottom: 1.5rem; color: #b3b3d1; font-size: 0.95rem;">Save the current state of your dataset as a new version in your inventory.</p>
        <div class="input-group" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <label for="layoutVersionName" style="font-weight: 600; color: #e2e8f0; font-size: 0.9rem;">Version Name</label>
          <input 
            id="layoutVersionName"
            v-model="versionName" 
            type="text" 
            :placeholder="versionNamePlaceholder"
            class="native-input"
            @keyup.enter="saveVersion"
            style="background: rgba(13, 17, 23, 0.6); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 8px; padding: 0.75rem 1rem; color: white; width: 100%; font-size: 0.95rem; outline: none; transition: border-color 0.2s;"
          />
        </div>
      </div>
      <template #footer>
        <div style="display: flex; gap: 0.75rem; flex-shrink: 0;">
          <Button
            variant="primary"
            :loading="isSaving"
            @click="saveVersion"
            :disabled="!versionName"
            style="padding: 0.5rem 1.25rem; font-weight: 600;"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 6px;">
              <path d="M17,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3M19,19H5V5H16.17L19,7.83V19M12,12A3,3 0 0,0 9,15A3,3 0 0,0 12,18A3,3 0 0,0 15,15A3,3 0 0,0 12,12M6,6H15V10H6V6Z"/>
            </svg>
            Save Version
          </Button>
          <Button variant="ghost" @click="showSaveModal = false" style="padding: 0.5rem 1.25rem;">Cancel</Button>
        </div>
      </template>
    </Modal>

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
import Modal from '~/components/Modal.vue'
import Button from '~/components/Button.vue'

const route = useRoute()
const mlStore = useMLDataFlowStore()
const experimentStore = useExperimentStore()

const showSaveModal = ref(false)
const versionName = ref('')
const isSaving = ref(false)

// Placeholder hint for naming convention
const versionNamePlaceholder = computed(() => {
  const base = (mlStore.fileName || 'dataset').split('.')[0]
  return `e.g., ${base}_v1`
})

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
  // Prefill with naming convention: <filename>_v<HHmm>
  const now = new Date()
  const ts = `${now.getHours()}${String(now.getMinutes()).padStart(2, '0')}`
  const base = (mlStore.fileName || 'dataset').split('.')[0]
  versionName.value = `${base}_v${ts}`
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
    isSaving.value = true
    await mlStore.saveDatasetVersion(datasetId, savedName)
    mlStore.isDirty = false
    showSaveModal.value = false
    versionName.value = ''
    showSaveSuccessToast(savedName)
  } catch (err) {
    saveToast.value = { visible: true, message: `Save failed: ${err.message}` }
    setTimeout(() => { saveToast.value.visible = false }, 4000)
  } finally {
    isSaving.value = false
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

.native-input {
  background: rgba(13, 17, 23, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: white;
  width: 100%;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}
.native-input:focus {
  border-color: rgba(102, 126, 234, 0.7);
}

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
