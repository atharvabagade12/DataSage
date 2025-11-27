<template>
  <label class="checkbox-wrapper" :class="{ 'checkbox-disabled': disabled }">
    <input
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      :indeterminate.prop="indeterminate"
      class="checkbox-input"
      @change="handleChange"
    />
    
    <span class="checkbox-box">
      <!-- Checkmark -->
      <svg v-if="!indeterminate" class="checkbox-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      
      <!-- Indeterminate -->
      <svg v-else class="checkbox-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
    </span>
    
    <span v-if="label || $slots.default" class="checkbox-label">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  indeterminate: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const handleChange = (event) => {
  const checked = event.target.checked
  emit('update:modelValue', checked)
  emit('change', checked)
}
</script>

<style scoped>
.checkbox-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
  transition: opacity var(--transition-fast, 150ms);
}

.checkbox-wrapper:hover:not(.checkbox-disabled) .checkbox-box {
  border-color: var(--color-primary, #667eea);
  background: rgba(102, 126, 234, 0.1);
}

.checkbox-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-box {
  position: relative;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid var(--color-border, rgba(102, 126, 234, 0.3));
  border-radius: var(--radius-sm, 6px);
  transition: all var(--transition-fast, 150ms);
}

.checkbox-input:checked + .checkbox-box {
  background: var(--gradient-primary);
  border-color: var(--color-primary, #667eea);
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
}

.checkbox-input:indeterminate + .checkbox-box {
  background: var(--gradient-primary);
  border-color: var(--color-primary, #667eea);
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
}

.checkbox-input:focus + .checkbox-box {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.checkbox-icon {
  opacity: 0;
  transform: scale(0.5);
  transition: all var(--transition-fast, 150ms);
  color: var(--color-text-primary, #ffffff);
}

.checkbox-input:checked + .checkbox-box .checkbox-icon,
.checkbox-input:indeterminate + .checkbox-box .checkbox-icon {
  opacity: 1;
  transform: scale(1);
}

.checkbox-label {
  font-size: var(--font-size-sm, 0.875rem);
  color: var(--color-text-secondary, #b3b3d1);
  line-height: var(--line-height-normal, 1.5);
}

.checkbox-wrapper:hover:not(.checkbox-disabled) .checkbox-label {
  color: var(--color-text-primary, #ffffff);
}
</style>
