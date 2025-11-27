<template>
  <Teleport to="body">
    <Transition name="toast-container">
      <div v-if="toasts.length > 0" class="toast-container">
        <TransitionGroup name="toast">
          <div
            v-for="toast in toasts"
            :key="toast.id"
            class="toast"
            :class="`toast-${toast.type}`"
            @click="removeToast(toast.id)"
          >
            <div class="toast-icon">
              <!-- Success Icon -->
              <svg v-if="toast.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
              </svg>
              
              <!-- Error Icon -->
              <svg v-else-if="toast.type === 'error'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
              </svg>
              
              <!-- Warning Icon -->
              <svg v-else-if="toast.type === 'warning'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
              </svg>
              
              <!-- Info Icon -->
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
              </svg>
            </div>
            
            <div class="toast-content">
              <div class="toast-title">{{ toast.title }}</div>
              <div v-if="toast.message" class="toast-message">{{ toast.message }}</div>
            </div>
            
            <button class="toast-close" @click.stop="removeToast(toast.id)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
              </svg>
            </button>
          </div>
        </TransitionGroup>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { toastState } from '~/composables/useToast'

const { toasts, removeToast } = toastState()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: var(--z-tooltip, 1070);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: var(--glass-background, rgba(26, 26, 46, 0.95));
  backdrop-filter: blur(20px);
  border-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-xl), 0 0 30px rgba(0, 0, 0, 0.3);
  border: 1px solid;
  cursor: pointer;
  pointer-events: all;
  min-width: 300px;
  max-width: 400px;
  transition: all var(--transition-base, 200ms);
}

.toast:hover {
  transform: translateX(-4px);
  box-shadow: var(--shadow-2xl), 0 0 40px rgba(0, 0, 0, 0.4);
}

/* Toast Types */
.toast-success {
  border-color: var(--color-success, #10b981);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
}

.toast-success .toast-icon {
  color: var(--color-success, #10b981);
}

.toast-error {
  border-color: var(--color-error, #ef4444);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
}

.toast-error .toast-icon {
  color: var(--color-error, #ef4444);
}

.toast-warning {
  border-color: var(--color-warning, #f59e0b);
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.05));
}

.toast-warning .toast-icon {
  color: var(--color-warning, #f59e0b);
}

.toast-info {
  border-color: var(--color-info, #3b82f6);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.05));
}

.toast-info .toast-icon {
  color: var(--color-info, #3b82f6);
}

/* Toast Content */
.toast-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  margin-top: 2px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: var(--font-size-sm, 0.875rem);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #ffffff);
  margin-bottom: 0.25rem;
}

.toast-message {
  font-size: var(--font-size-xs, 0.75rem);
  color: var(--color-text-secondary, #b3b3d1);
  line-height: var(--line-height-normal, 1.5);
}

.toast-close {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  padding: 0;
  background: none;
  border: none;
  color: var(--color-text-tertiary, #8b8ba7);
  cursor: pointer;
  transition: color var(--transition-fast, 150ms);
  margin-top: 2px;
}

.toast-close:hover {
  color: var(--color-text-primary, #ffffff);
}

/* Animations */
.toast-container-enter-active,
.toast-container-leave-active {
  transition: opacity var(--transition-base, 200ms);
}

.toast-container-enter-from,
.toast-container-leave-to {
  opacity: 0;
}

.toast-enter-active {
  transition: all var(--transition-base, 200ms);
}

.toast-leave-active {
  transition: all var(--transition-fast, 150ms);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(50%) scale(0.8);
}

.toast-move {
  transition: transform var(--transition-base, 200ms);
}
</style>
