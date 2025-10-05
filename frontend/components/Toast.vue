<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast" tag="div">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast-${toast.type}`]"
          @click="removeToast(toast.id)"
        >
          <div class="toast-icon">
            <span v-if="toast.type === 'success'">✅</span>
            <span v-else-if="toast.type === 'error'">❌</span>
            <span v-else-if="toast.type === 'warning'">⚠️</span>
            <span v-else-if="toast.type === 'info'">ℹ️</span>
          </div>
          <div class="toast-message">{{ toast.message }}</div>
          <button class="toast-close" @click.stop="removeToast(toast.id)">
            ✕
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
const { toasts, removeToast } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  cursor: pointer;
  pointer-events: auto;
  min-width: 300px;
  max-width: 500px;
}

.toast-success {
  background: rgba(16, 185, 129, 0.9);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: white;
}

.toast-error {
  background: rgba(239, 68, 68, 0.9);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: white;
}

.toast-warning {
  background: rgba(245, 158, 11, 0.9);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: white;
}

.toast-info {
  background: rgba(59, 130, 246, 0.9);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: white;
}

.toast-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1.1rem;
  opacity: 0.7;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  opacity: 1;
}

/* Toast animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
