<template>
  <div
    class="card"
    :class="[
      `card-${variant}`,
      { 'card-hover': hover, 'card-clickable': clickable }
    ]"
    @click="handleClick"
  >
    <!-- Header (optional) -->
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>

    <!-- Body -->
    <div class="card-body" :class="{ 'card-body-padded': padded }">
      <slot></slot>
    </div>

    <!-- Footer (optional) -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'error'].includes(value)
  },
  hover: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  padded: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.card {
  background: var(--glass-background, rgba(26, 26, 46, 0.6));
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-xl, 16px);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  transition: all var(--transition-base, 200ms);
}

/* Hover Effect */
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl), var(--shadow-glow-primary);
  border-color: rgba(102, 126, 234, 0.4);
}

/* Clickable */
.card-clickable {
  cursor: pointer;
}

/* Variants */
.card-primary {
  border-color: var(--color-primary, #667eea);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.05));
}

.card-success {
  border-color: var(--color-success, #10b981);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
}

.card-warning {
  border-color: var(--color-warning, #f59e0b);
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.05));
}

.card-error {
  border-color: var(--color-error, #ef4444);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
}

/* Header */
.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
}

.card-title {
  font-size: var(--font-size-lg, 1.125rem);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #ffffff);
  margin: 0;
}

/* Body */
.card-body {
  color: var(--color-text-secondary, #b3b3d1);
}

.card-body-padded {
  padding: 1.5rem;
}

/* Footer */
.card-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* Gradient Border Effect (optional) */
.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity var(--transition-base, 200ms);
}

.card-hover:hover::before {
  opacity: 1;
}
</style>
