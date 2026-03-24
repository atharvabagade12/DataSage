<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="show" class="egm-overlay" @click.self="$emit('close')">
        <div class="egm-modal glass">
          <!-- Header -->
          <div class="egm-header">
            <div class="egm-header-left">
              <div class="egm-header-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
              </div>
              <div>
                <h2>Ecosystem Guide</h2>
                <p>Master the DataSage intelligence pipeline</p>
              </div>
            </div>
            <button class="egm-close" @click="$emit('close')">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- Body with Sidebar and Content -->
          <div class="egm-container">
            <div class="egm-sidebar">
              <div 
                v-for="(section, index) in sections" 
                :key="index"
                class="sidebar-item"
                :class="{ active: activeSection === index }"
                @click="activeSection = index"
              >
                <div class="item-icon" v-html="section.icon"></div>
                <span>{{ section.title }}</span>
              </div>
            </div>

            <div class="egm-content custom-scrollbar">
              <Transition name="slide-up" mode="out-in">
                <div :key="activeSection" class="section-view">
                  <div class="section-header">
                    <div class="section-icon-large" :style="{ background: sections[activeSection].bg, color: sections[activeSection].color }">
                      <span v-html="sections[activeSection].iconLarge"></span>
                    </div>
                    <div>
                      <h3>{{ sections[activeSection].title }}</h3>
                      <p class="section-tagline">{{ sections[activeSection].tagline }}</p>
                    </div>
                  </div>

                  <div class="section-body">
                    <div v-for="(item, i) in sections[activeSection].content" :key="i" class="info-block">
                      <h4>{{ item.label }}</h4>
                      <p>{{ item.text }}</p>
                    </div>

                    <div v-if="sections[activeSection].proTip" class="pro-tip-box">
                      <div class="pro-tip-header">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                          <path d="M9.663 17h4.674M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 1 1 7.072 0l-.548.7c-.413.528-.941 1.201-1.011 1.86H9.344c-.07-.659-.598-1.332-1.011-1.86l-.548-.7z"></path>
                        </svg>
                        <span>Expert Tip</span>
                      </div>
                      <p>{{ sections[activeSection].proTip }}</p>
                    </div>
                  </div>
                </div>
              </Transition>
            </div>
          </div>

          <!-- Footer -->
          <div class="egm-footer">
            <div class="step-indicator">
               {{ activeSection + 1 }} / {{ sections.length }}
            </div>
            <div class="footer-actions">
              <button class="btn-prev" @click="prevSection" :disabled="activeSection === 0">
                Back
              </button>
              <button class="btn-next" @click="nextSection">
                {{ activeSection === sections.length - 1 ? 'Finish' : 'Next Step' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close'])

const activeSection = ref(0)

const sections = [
  {
    title: 'Data Journey',
    tagline: 'From raw files to machine intelligence',
    bg: 'rgba(102, 126, 234, 0.1)',
    color: '#667eea',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>',
    iconLarge: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>',
    content: [
      { label: '1. Import', text: 'Upload your CSV, JSON, or Excel data. DataSage supports files up to 1GB for high-performance analysis.' },
      { label: '2. Exploration', text: 'Use the Data Preview to understand distributions, missing values, and potential outliers in your dataset.' },
      { label: '3. Intelligence', text: 'Pick an algorithm and train your model. DataSage automatically handles the heavy lifting of model training.' }
    ],
    proTip: 'Always check your data distributions before training. A skewed feature can significantly impact model performance.'
  },
  {
    title: 'Smart Refinement',
    tagline: 'Deep cleaning and feature engineering',
    bg: 'rgba(168, 139, 235, 0.1)',
    color: '#a88beb',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>',
    iconLarge: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>',
    content: [
      { label: 'Missing Values', text: 'DataSage can automatically fill gaps in your data using Mean, Median, or Mode imputation strategies.' },
      { label: 'Categorical Encoding', text: 'Convert text-based data into numerical formats that machine learning algorithms can understand.' },
      { label: 'Scaling & Normalization', text: 'Ensure all your features are on the same scale (e.g., 0 to 1) for more stable and faster training.' }
    ],
    proTip: 'Use Standard Scaling when your data follows a normal distribution, and Min-Max Scaling for others.'
  },
  {
    title: 'Intelligence Models',
    tagline: 'Choosing the right algorithm for the job',
    bg: 'rgba(129, 140, 248, 0.1)',
    color: '#818cf8',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>',
    iconLarge: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>',
    content: [
      { label: 'Classification', text: 'Predict a category or label. Examples: "Will this customer churn?", "Is this transaction fraudulent?"' },
      { label: 'Regression', text: 'Predict a continuous numerical value. Examples: "What will the stock price be?", "How much will this house sell for?"' },
      { label: 'Ensemble Learning', text: 'Combine multiple models (like Random Forest) to achieve higher accuracy and robustness than a single model.' }
    ],
    proTip: 'Start with simpler models like Logistic Regression or Linear Regression to establish a baseline before moving to complex ones.'
  },
  {
    title: 'Decoding Results',
    tagline: 'Understanding how your model performs',
    bg: 'rgba(16, 185, 129, 0.1)',
    color: '#10b981',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"></path></svg>',
    iconLarge: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"></path></svg>',
    content: [
      { label: 'Accuracy & R²', text: 'Accuracy tells you the % of correct predictions. R² (for regression) tells you how well your model explains the data.' },
      { label: 'Precision & Recall', text: 'Used for classification. Precision focus on "How many flagged items were actually correct?". Recall focus on "Did we find all items?"' },
      { label: 'Feature Importance', text: 'Identify which columns in your data actually drove the model\'s decisions. Great for business insights.' }
    ],
    proTip: 'In imbalanced datasets, Accuracy can be misleading. Always look at F1-Score or the Confusion Matrix for a complete picture.'
  }
]

const nextSection = () => {
  if (activeSection.value < sections.length - 1) {
    activeSection.value++
  } else {
    emit('close')
  }
}

const prevSection = () => {
  if (activeSection.value > 0) {
    activeSection.value--
  }
}
</script>

<style scoped>
/* Modal Structure */
.egm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.5rem;
}

.egm-modal {
  width: 100%;
  max-width: 850px;
  height: 600px;
  background: #0b0b1a;
  border-radius: 32px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.7);
}

.glass {
  background: rgba(11, 11, 26, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Header */
.egm-header {
  padding: 1.75rem 2.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.egm-header-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.egm-header-icon {
  width: 44px;
  height: 44px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.egm-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.egm-header p {
  margin: 4px 0 0;
  font-size: 0.85rem;
  color: #6a6a8a;
}

.egm-close {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: #6a6a8a;
  border-radius: 12px;
  width: 38px;
  height: 38px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.egm-close:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.2);
}

/* Container & Sidebar */
.egm-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.egm-sidebar {
  width: 240px;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.01);
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.25rem;
  border-radius: 14px;
  color: #6a6a8a;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 0.9rem;
}

.sidebar-item:hover {
  background: rgba(255, 255, 255, 0.03);
  color: #fff;
}

.sidebar-item.active {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Content */
.egm-content {
  flex: 1;
  padding: 2.5rem;
  overflow-y: auto;
}

.section-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.section-icon-large {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
}

.section-tagline {
  margin: 6px 0 0;
  color: #6a6a8a;
  font-size: 0.95rem;
}

.section-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-block h4 {
  margin: 0 0 0.5rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: #b3b3d1;
}

.info-block p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #6a6a8a;
}

.pro-tip-box {
  margin-top: 1rem;
  padding: 1.25rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 16px;
}

.pro-tip-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #667eea;
  font-weight: 800;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.75rem;
}

.pro-tip-box p {
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.5;
  color: #b3b3d1;
  font-style: italic;
}

/* Footer */
.egm-footer {
  padding: 1.5rem 2.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.step-indicator {
  font-size: 0.8rem;
  font-weight: 700;
  color: #4a4a6a;
}

.footer-actions {
  display: flex;
  gap: 1rem;
}

.btn-prev {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.05);
  color: #6a6a8a;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-prev:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.03);
  color: #fff;
}

.btn-prev:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn-next {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-next:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .egm-modal {
    height: auto;
    max-height: 90vh;
  }
  .egm-sidebar {
    display: none;
  }
}
</style>
