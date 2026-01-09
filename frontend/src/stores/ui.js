import { defineStore } from 'pinia';

export const useUIStore = defineStore('ui', {
  state: () => ({
    isLoading: false,
    processingMessage: '',
    
    // Global UI Elements
    activeModal: null, // 'split', 'encode', 'scale', etc.
    showBackendWarning: false,
    
    // Toast / Notifications
    notifications: []
  }),
  
  actions: {
    startProcessing(message = 'Processing...') {
      this.isLoading = true;
      this.processingMessage = message;
    },
    
    stopProcessing() {
      this.isLoading = false;
      this.processingMessage = '';
    },
    
    openModal(modalName) {
      this.activeModal = modalName;
    },
    
    closeModal() {
      this.activeModal = null;
    },
    
    showToast(type, title, message) {
      const id = Date.now();
      this.notifications.push({ id, type, title, message });
      setTimeout(() => {
        this.notifications = this.notifications.filter(n => n.id !== id);
      }, 5000);
    }
  }
});
