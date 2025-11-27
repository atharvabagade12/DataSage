<template>
  <div class="select-wrapper" :class="{ 'select-error': error, 'select-disabled': disabled }">
    <label v-if="label" class="select-label" :for="selectId">
      {{ label }}
      <span v-if="required" class="select-required">*</span>
    </label>
    
    <div class="select-container" @click="toggleDropdown">
      <!-- Selected Value Display -->
      <div class="select-display">
        <span v-if="selectedOption" class="select-value">
          {{ selectedOption.label }}
        </span>
        <span v-else class="select-placeholder">
          {{ placeholder }}
        </span>
      </div>
      
      <!-- Dropdown Arrow -->
      <svg
        class="select-arrow"
        :class="{ 'select-arrow-open': isOpen }"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M7 10l5 5 5-5z"/>
      </svg>
      
      <!-- Dropdown Menu -->
      <Transition name="dropdown">
        <div v-if="isOpen" class="select-dropdown">
          <div
            v-for="option in options"
            :key="option.value"
            class="select-option"
            :class="{ 'select-option-selected': option.value === modelValue }"
            @click.stop="selectOption(option)"
          >
            <span>{{ option.label }}</span>
            <svg
              v-if="option.value === modelValue"
              class="select-check"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>
          </div>
          
          <div v-if="options.length === 0" class="select-empty">
            No options available
          </div>
        </div>
      </Transition>
    </div>
    
    <!-- Helper Text or Error Message -->
    <div v-if="helperText || error" class="select-message">
      <span v-if="error" class="select-error-message">{{ error }}</span>
      <span v-else class="select-helper-text">{{ helperText }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: null
  },
  options: {
    type: Array,
    required: true,
    // Array of { value, label } objects
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an option'
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
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOpen = ref(false)
const selectId = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

const selectedOption = computed(() => {
  return props.options.find(opt => opt.value === props.modelValue)
})

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value
  }
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  emit('change', option.value)
  isOpen.value = false
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const selectElement = event.target.closest('.select-wrapper')
  if (!selectElement && isOpen.value) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.select-label {
  font-size: var(--font-size-sm, 0.875rem);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-primary, #ffffff);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.select-required {
  color: var(--color-error, #ef4444);
}

.select-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-lg, 12px);
  cursor: pointer;
  transition: all var(--transition-fast, 150ms);
  user-select: none;
}

.select-container:hover:not(.select-disabled .select-container) {
  border-color: var(--color-primary, #667eea);
  background: rgba(255, 255, 255, 0.08);
}

.select-error .select-container {
  border-color: var(--color-error, #ef4444);
}

.select-disabled .select-container {
  opacity: 0.5;
  cursor: not-allowed;
}

.select-display {
  flex: 1;
  min-width: 0;
}

.select-value {
  color: var(--color-text-primary, #ffffff);
  font-size: var(--font-size-base, 1rem);
}

.select-placeholder {
  color: var(--color-text-tertiary, #8b8ba7);
  font-size: var(--font-size-base, 1rem);
}

.select-arrow {
  flex-shrink: 0;
  color: var(--color-text-secondary, #b3b3d1);
  transition: transform var(--transition-fast, 150ms);
}

.select-arrow-open {
  transform: rotate(180deg);
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  max-height: 300px;
  overflow-y: auto;
  background: var(--glass-background, rgba(26, 26, 46, 0.95));
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border, rgba(102, 126, 234, 0.2));
  border-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-xl);
  z-index: var(--z-dropdown, 1000);
}

/* Custom scrollbar */
.select-dropdown::-webkit-scrollbar {
  width: 8px;
}

.select-dropdown::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.select-dropdown::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

.select-dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

.select-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  color: var(--color-text-secondary, #b3b3d1);
  font-size: var(--font-size-sm, 0.875rem);
  cursor: pointer;
  transition: all var(--transition-fast, 150ms);
}

.select-option:hover {
  background: rgba(102, 126, 234, 0.1);
  color: var(--color-text-primary, #ffffff);
}

.select-option-selected {
  background: rgba(102, 126, 234, 0.15);
  color: var(--color-primary, #667eea);
  font-weight: var(--font-weight-medium, 500);
}

.select-check {
  color: var(--color-primary, #667eea);
}

.select-empty {
  padding: 1.5rem 1rem;
  text-align: center;
  color: var(--color-text-tertiary, #8b8ba7);
  font-size: var(--font-size-sm, 0.875rem);
}

.select-message {
  font-size: var(--font-size-xs, 0.75rem);
  padding-left: 0.25rem;
}

.select-helper-text {
  color: var(--color-text-tertiary, #8b8ba7);
}

.select-error-message {
  color: var(--color-error, #ef4444);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.select-error-message::before {
  content: '⚠';
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--transition-fast, 150ms);
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
