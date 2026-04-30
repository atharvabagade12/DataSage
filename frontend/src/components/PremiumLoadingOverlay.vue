<template>
  <Transition name="fade">
    <div v-if="show" class="premium-loading-overlay" :class="{ 'solid-bg': solidBg }">
      <div class="spinner-content">
        <div class="premium-spinner"></div>
        <h2 v-if="title" class="loading-title">{{ title }}</h2>
        <p v-if="message" class="loading-text">{{ message }}</p>
        
        <div v-if="showProgress" class="initialization-progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <p v-if="showProgress" class="progress-pct">{{ Math.round(progress) }}%</p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: 'Synchronizing intelligence...'
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: 0
  },
  solidBg: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.premium-loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 15, 35, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.premium-loading-overlay.solid-bg {
  background: #0f0f23;
  backdrop-filter: none;
}

.spinner-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

.premium-spinner {
  width: 64px;
  height: 64px;
  border: 3px solid rgba(102, 126, 234, 0.1);
  border-radius: 50%;
  border-top-color: #667eea;
  border-right-color: #764ba2;
  animation: spin 1s cubic-bezier(0.55, 0.055, 0.675, 0.19) infinite;
  box-shadow: 0 0 30px rgba(102, 126, 234, 0.15);
  margin-bottom: 1rem;
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.loading-text {
  font-size: 1rem;
  color: #b3b3d1;
  font-weight: 500;
  margin-bottom: 1rem;
}

.initialization-progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.initialization-progress-bar .progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

.progress-pct {
  font-size: 0.875rem;
  color: #667eea;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
