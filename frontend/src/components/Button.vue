<template>
  <button
    class="btn"
    :class="[
      `btn-${variant}`,
      `btn-${size}`,
      { 'btn-loading': loading, 'btn-disabled': disabled || loading }
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <LoadingSpinner
      v-if="loading"
      size="sm"
      :variant="variant === 'primary' || variant === 'secondary' ? 'white' : 'primary'"
    />
    <slot v-else></slot>
  </button>
</template>

<script setup>
import LoadingSpinner from './LoadingSpinner.vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'ghost', 'outline'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font-primary);
  font-weight: var(--font-weight-semibold, 600);
  border-radius: var(--radius-lg, 12px);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast, 150ms);
  white-space: nowrap;
  user-select: none;
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
}

/* Sizes */
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: var(--font-size-sm, 0.875rem);
  min-height: 32px;
}

.btn-md {
  padding: 0.75rem 1.5rem;
  font-size: var(--font-size-base, 1rem);
  min-height: 40px;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: var(--font-size-lg, 1.125rem);
  min-height: 48px;
}

/* Primary Variant */
.btn-primary {
  background: var(--gradient-primary);
  color: var(--color-text-primary, #ffffff);
  box-shadow: var(--shadow-md);
}

.btn-primary:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), var(--shadow-glow-primary);
}

.btn-primary:active:not(.btn-disabled) {
  transform: translateY(0);
}

/* Secondary Variant */
.btn-secondary {
  background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-dark));
  color: var(--color-text-primary, #ffffff);
  box-shadow: var(--shadow-md);
}

.btn-secondary:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Success Variant */
.btn-success {
  background: var(--gradient-success);
  color: var(--color-text-primary, #ffffff);
  box-shadow: var(--shadow-md);
}

.btn-success:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), var(--shadow-glow-success);
}

/* Danger Variant */
.btn-danger {
  background: var(--gradient-error);
  color: var(--color-text-primary, #ffffff);
  box-shadow: var(--shadow-md);
}

.btn-danger:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), var(--shadow-glow-error);
}

/* Warning Variant */
.btn-warning {
  background: var(--gradient-warning);
  color: var(--color-text-primary, #ffffff);
  box-shadow: var(--shadow-md);
}

.btn-warning:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Ghost Variant */
.btn-ghost {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary, #ffffff);
  border-color: rgba(255, 255, 255, 0.1);
}

.btn-ghost:hover:not(.btn-disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

/* Outline Variant */
.btn-outline {
  background: transparent;
  color: var(--color-primary, #667eea);
  border-color: var(--color-primary, #667eea);
}

.btn-outline:hover:not(.btn-disabled) {
  background: rgba(102, 126, 234, 0.1);
  border-color: var(--color-primary-light, #818cf8);
}

/* Disabled State */
.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* Loading State */
.btn-loading {
  cursor: wait;
  position: relative;
}
</style>
