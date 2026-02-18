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
    isTypesVerified: false,
    lastFetchedId: null
  }),
  
  actions: {
    // Sync with backend using ID from Experiment Store
    async loadData(datasetId, force = false) {
      if (!datasetId) return;
      if (!force && this.isLoaded && this.lastFetchedId === datasetId) return;
      
      const { authenticatedGet } = useAuthenticatedFetch();
      
      try {
        console.log('🔄 DataStore: Fetching data for', datasetId);
        
        // Parallel Fetch using central utility
        const [previewRes, typesRes, statsRes] = await Promise.all([
          authenticatedGet(`/api/datasets/${datasetId}?limit=200`),
          authenticatedGet(`/api/datasets/${datasetId}/semantic-types`),
          authenticatedGet(`/api/datasets/${datasetId}/statistics`)
        ]);

        if (previewRes.ok) {
          const data = await previewRes.json();
          console.log("🛠️ DataStore: Preview Response Data:", data); // DEBUG LOG
          
          if (Array.isArray(data)) {
               this.rawPreview = data;
          } else {
               // Handle object response with sample_data and split previews
               if (Array.isArray(data.sample_data)) {
                   this.rawPreview = data.sample_data;
               } else if (Array.isArray(data.data)) {
                   this.rawPreview = data.data;
               }

               // Load split previews if they exist
               if (Array.isArray(data.train_preview)) {
                   this.trainPreview = data.train_preview;
                   console.log(`✅ DataStore: Loaded train_preview (${data.train_preview.length} rows)`);
               }
               if (Array.isArray(data.test_preview)) {
                   this.testPreview = data.test_preview;
                   console.log(`✅ DataStore: Loaded test_preview (${data.test_preview.length} rows)`);
               }
          }
          console.log("STATS: Loaded manual raw rows:", this.rawPreview.length);
        } else {
             console.error("Preview fetch failed", previewRes.status, await previewRes.text());
        }
        
        if (typesRes.ok) {
           const types = await typesRes.json();
           this.semanticTypes = types.column_types || [];
           this.isTypesVerified = types.is_verified || false;
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
    
    // Save user-verified semantic types to backend
    async saveSemanticTypes(datasetId, overrides) {
      if (!datasetId || !overrides || overrides.length === 0) return;
      
      const { authenticatedPost } = useAuthenticatedFetch();
      
      try {
        console.log('📤 DataStore: Saving semantic type overrides for', datasetId);
        
        const response = await authenticatedPost(`/api/datasets/${datasetId}/semantic-types/override`, overrides);

        if (!response.ok) {
          throw new Error(`Failed to save semantic types: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('✅ DataStore: Semantic types saved', result);
        
        this.isTypesVerified = true;
        
        // Refresh semantic types from backend if needed, or update locally
        // Updating locally for immediate feedback
        this.semanticTypes = this.semanticTypes.map(st => {
          const override = overrides.find(o => o.column === st.column);
          return override ? { ...st, ...override, is_override: true } : st;
        });

        return { success: true };
      } catch (error) {
        console.error('❌ DataStore: Save semantic types failed', error);
        throw error;
      }
    },
    
    clearData() {
      this.$reset();
    }
  }
});
