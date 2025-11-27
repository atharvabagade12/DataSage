<template>
  <div class="input-wrapper" :class="{ 'input-error': error, 'input-disabled': disabled }">
    <label v-if="label" class="input-label" :for="inputId">
      {{ label }}
      <span v-if="required" class="input-required">*</span>
    </label>
    
    <div class="input-container">
      <!-- Prefix Icon/Text -->
      <div v-if="$slots.prefix || prefix" class="input-prefix">
        <slot name="prefix">{{ prefix }}</slot>
      </div>
      
      <!-- Input Field -->
      <input
        :id="inputId"
        ref="inputRef"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        class="input-field"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
      
      <!-- Suffix Icon/Text -->
      <div v-if="$slots.suffix || suffix" class="input-suffix">
        <slot name="suffix">{{ suffix }}</slot>
      </div>
      
      <!-- Clear Button -->
      <button
        v-if="clearable && modelValue && !disabled"
        class="input-clear"
        @click="handleClear"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
        </svg>
      </button>
    </div>
    
    <!-- Helper Text or Error Message -->
    <div v-if="helperText || error" class="input-message">
      <span v-if="error" class="input-error-message">{{ error }}</span>
      <span v-else class="input-helper-text">{{ helperText }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'tel', 'url', 'search'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: false
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  },
  min: {
    type: [String, Number],
    default: undefined
  },
  max: {
    type: [String, Number],
    default: undefined
  },
  step: {
    type: [String, Number],
    default: undefined
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'clear'])

const inputRef = ref(null)
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleClear = () => {
  emit('update:modelValue', '')
  emit('clear')
  inputRef.value?.focus()
}

// Expose focus method
defineExpose({
  focus: () => inputRef.value?.focus()
})
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: var(--font-size-sm, 0.875rem);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-primary, #ffffff);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.input-required {
  color: var(--color-error, #ef4444);
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-lg, 12px);
  transition: all var(--transition-fast, 150ms);
}

.input-container:focus-within {
  border-color: var(--color-primary, #667eea);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  background: rgba(255, 255, 255, 0.08);
}

.input-error .input-container {
  border-color: var(--color-error, #ef4444);
}

.input-error .input-container:focus-within {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

.input-disabled .input-container {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-field {
  flex: 1;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  outline: none;
  color: var(--color-text-primary, #ffffff);
  font-size: var(--font-size-base, 1rem);
  font-family: var(--font-primary);
}

.input-field::placeholder {
  color: var(--color-text-tertiary, #8b8ba7);
}

.input-field:disabled {
  cursor: not-allowed;
}

.input-prefix,
.input-suffix {
  display: flex;
  align-items: center;
  padding: 0 0.75rem;
  color: var(--color-text-secondary, #b3b3d1);
  font-size: var(--font-size-sm, 0.875rem);
}

.input-clear {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: none;
  border: none;
  color: var(--color-text-tertiary, #8b8ba7);
  cursor: pointer;
  transition: color var(--transition-fast, 150ms);
}

.input-clear:hover {
  color: var(--color-text-primary, #ffffff);
}

.input-message {
  font-size: var(--font-size-xs, 0.75rem);
  padding-left: 0.25rem;
}

.input-helper-text {
  color: var(--color-text-tertiary, #8b8ba7);
}

.input-error-message {
  color: var(--color-error, #ef4444);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.input-error-message::before {
  content: '⚠';
}
</style>
