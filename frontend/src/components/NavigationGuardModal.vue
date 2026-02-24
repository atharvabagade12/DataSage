<template>
  <div v-if="modelValue" class="guard-overlay" @click="$emit('update:modelValue', false)">
    <div class="guard-modal" @click.stop>
      <div class="modal-header">
        <div class="warning-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z" />
          </svg>
        </div>
        <h3>Unsaved Changes</h3>
      </div>
      
      <div class="modal-body">
        <p>You have unsaved changes in your dataset session. What would you like to do?</p>
        <div class="warning-box">
          Navigating away without saving will discard your in-memory modifications.
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-stay" @click="$emit('update:modelValue', false)">Stay & Edit</button>
        <button class="btn btn-discard" @click="$emit('discard')">Dont Save Now</button>
        <button class="btn btn-save" @click="$emit('save')">Save & Continue</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: Boolean
})
defineEmits(['update:modelValue', 'save', 'discard'])
</script>

<style scoped>
.guard-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.guard-modal {
  background: #1a1a2e;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
  padding: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.warning-icon { color: #f59e0b; }
.modal-header h3 { font-size: 1.25rem; font-weight: 700; color: #ffffff; }

.modal-body p { color: #b3b3d1; line-height: 1.6; margin-bottom: 16px; }
.warning-box { 
    background: rgba(245, 158, 11, 0.1); 
    border-left: 4px solid #f59e0b; 
    padding: 12px; 
    font-size: 0.85rem; 
    color: #f59e0b; 
    border-radius: 4px;
}

.modal-footer { margin-top: 28px; display: flex; flex-direction: column; gap: 10px; }

.btn { 
    padding: 12px; 
    border-radius: 8px; 
    font-weight: 700; 
    cursor: pointer; 
    transition: all 0.2s; 
    border: none;
    font-size: 0.9rem;
}

.btn-save { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.btn-save:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3); }

.btn-discard { background: rgba(255, 87, 87, 0.1); color: #ff5757; border: 1px solid rgba(255, 87, 87, 0.2); }
.btn-discard:hover { background: rgba(255, 87, 87, 0.2); }

.btn-stay { background: transparent; color: #b3b3d1; }
.btn-stay:hover { color: #ffffff; background: rgba(255, 255, 255, 0.05); }

</style>
