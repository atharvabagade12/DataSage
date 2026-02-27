<template>
  <div class="page-header-container">
    <!-- Background decorative blobs -->
    <div class="bg-blob blob-left"></div>
    <div class="bg-blob blob-right"></div>

    <!-- Grid overlay -->
    <div class="grid-overlay"></div>

    <div class="page-header-inner">
      <!-- Icon -->
      <div class="page-header-icon" v-if="icon">
        <slot name="icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="3" y1="9" x2="21" y2="9"></line>
            <line x1="9" y1="21" x2="9" y2="9"></line>
          </svg>
        </slot>
      </div>

      <!-- Text (centered) -->
      <div class="page-header-text">
        <h1 class="page-title">{{ title }}</h1>
        <p class="page-description" v-if="description">{{ description }}</p>
      </div>

      <!-- Optional actions slot -->
      <div class="page-header-actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.page-header-container {
  position: relative;
  padding: 2.5rem 2rem;
  margin-bottom: 2rem;
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg,
    rgba(20, 14, 40, 0.95) 0%,
    rgba(18, 18, 38, 0.95) 40%,
    rgba(14, 20, 45, 0.95) 100%
  );
  border: 1px solid rgba(139, 92, 246, 0.15);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.03),
    0 8px 40px rgba(0, 0, 0, 0.35),
    0 0 80px rgba(99, 102, 241, 0.06);
}

/* Grid pattern overlay */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(139, 92, 246, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

/* Ambient glow blobs */
.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
  opacity: 0.35;
}

.blob-left {
  width: 300px;
  height: 200px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%);
  top: -60px;
  left: -60px;
}

.blob-right {
  width: 250px;
  height: 180px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.35) 0%, transparent 70%);
  bottom: -50px;
  right: -40px;
}

/* Top shimmer line */
.page-header-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 15%;
  right: 15%;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    rgba(167, 139, 250, 0.6),
    rgba(99, 102, 241, 0.8),
    rgba(167, 139, 250, 0.6),
    transparent
  );
}

/* Bottom faint line */
.page-header-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 30%;
  right: 30%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.2), transparent);
}

.page-header-inner {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
}

/* Icon */
.page-header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
  color: #a78bfa;
  border: 1px solid rgba(167, 139, 250, 0.25);
  box-shadow:
    0 0 0 4px rgba(139, 92, 246, 0.06),
    0 8px 24px rgba(99, 102, 241, 0.2);
  backdrop-filter: blur(8px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.page-header-icon:hover {
  transform: translateY(-2px);
  box-shadow:
    0 0 0 4px rgba(139, 92, 246, 0.1),
    0 12px 32px rgba(99, 102, 241, 0.3);
}

.page-header-icon :deep(svg) {
  width: 28px;
  height: 28px;
}

/* Text */
.page-header-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.page-title {
  font-size: 1.9rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.025em;
  line-height: 1.2;
  background: linear-gradient(135deg, #f0eaff 0%, #c4b5fd 40%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 24px rgba(167, 139, 250, 0.25));
}

.page-description {
  margin: 0;
  font-size: 0.97rem;
  color: #94a3b8;
  max-width: 560px;
  line-height: 1.6;
  letter-spacing: 0.01em;
}

/* Actions */
.page-header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .page-header-container {
    padding: 2rem 1.25rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-description {
    font-size: 0.9rem;
  }
}
</style>
