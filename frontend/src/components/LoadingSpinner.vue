<template>
  <div class="loading-spinner" :class="[`spinner-${size}`, `spinner-${variant}`]">
    <div class="spinner">
      <div class="spinner-circle"></div>
      <div class="spinner-circle"></div>
      <div class="spinner-circle"></div>
    </div>
    <div v-if="message" class="spinner-message">{{ message }}</div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'white'].includes(value)
  },
  message: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.spinner {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.spinner-circle {
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.spinner-circle:nth-child(1) {
  animation-delay: -0.32s;
}

.spinner-circle:nth-child(2) {
  animation-delay: -0.16s;
}

/* Sizes */
.spinner-sm .spinner-circle {
  width: 8px;
  height: 8px;
}

.spinner-md .spinner-circle {
  width: 12px;
  height: 12px;
}

.spinner-lg .spinner-circle {
  width: 16px;
  height: 16px;
}

.spinner-xl .spinner-circle {
  width: 20px;
  height: 20px;
}

/* Variants */
.spinner-primary .spinner-circle {
  background: var(--color-primary, #667eea);
}

.spinner-secondary .spinner-circle {
  background: var(--color-secondary, #764ba2);
}

.spinner-white .spinner-circle {
  background: var(--color-text-primary, #ffffff);
}

/* Message */
.spinner-message {
  font-size: var(--font-size-sm, 0.875rem);
  color: var(--color-text-secondary, #b3b3d1);
  font-weight: var(--font-weight-medium, 500);
  text-align: center;
}

/* Animation */
@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Overlay variant (for full-screen loading) */
.loading-spinner.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 15, 35, 0.8);
  backdrop-filter: blur(4px);
  z-index: var(--z-modal, 1050);
}
</style>
