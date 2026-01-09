import { defineStore } from 'pinia';
import { useExperimentStore } from './experiment';

export const useDataStore = defineStore('data', {
  state: () => ({
    // Transient Data (Not Persisted)
    rawPreview: [], // Top 200 rows of original data
    trainPreview: [],
    testPreview: [],
    
    statistics: null, // Full column statistics
    semanticTypes: [], // Backend-detected types
    
    // Status
    isLoaded: false,
    lastFetchedId: null
  }),
  
  actions: {
    // Sync with backend using ID from Experiment Store
    async loadData(datasetId) {
      if (!datasetId) return;
      if (this.isLoaded && this.lastFetchedId === datasetId) return;
      
      try {
        console.log('🔄 DataStore: Fetching data for', datasetId);
        
        // Parallel Fetch
        const [previewRes, typesRes, statsRes] = await Promise.all([
          fetch(`http://localhost:8000/api/datasets/${datasetId}?limit=200`),
          fetch(`http://localhost:8000/api/datasets/${datasetId}/semantic-types`),
          fetch(`http://localhost:8000/api/datasets/${datasetId}/statistics`)
        ]);

        if (previewRes.ok) {
          const data = await previewRes.json();
          this.rawPreview = data.data || []; // Adjust based on actual API response structure
        }
        
        if (typesRes.ok) {
           const types = await typesRes.json();
           this.semanticTypes = types.column_types || [];
        }

        if (statsRes.ok) {
           const stats = await statsRes.json();
           this.statistics = stats;
        }

        this.lastFetchedId = datasetId;
        this.isLoaded = true;
        console.log('✅ DataStore: Loaded successfully');
        
      } catch (error) {
        console.error('❌ DataStore: Load failed', error);
        this.isLoaded = false;
      }
    },
    
    // Set split data manually (usually response from split API)
    setSplitData(train, test) {
      this.trainPreview = train;
      this.testPreview = test;
    },
    
    clearData() {
      this.$reset();
    }
  }
});
