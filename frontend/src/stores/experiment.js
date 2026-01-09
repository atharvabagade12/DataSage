import { defineStore } from 'pinia';

export const useExperimentStore = defineStore('experiment', {
  state: () => ({
    // Dataset Reference (Metadata only)
    datasetId: null,
    datasetName: null,
    datasetSize: { rows: 0, columns: 0 },
    
    // Problem Definition
    targetColumn: null,
    problemType: null, // { type: 'classification', confidence: 0.9 }
    
    // Preprocessing Configuration
    preprocessing: {
      splitRatio: 0.8,
      splitStrategy: 'random', // 'random', 'stratified'
      randomSeed: 42,
      isSplitApplied: false,
      
      // Feature Engineering
      scalingMethod: 'standard', // 'standard', 'minmax', etc.
      isScalingApplied: false,
      scaledColumns: [], // List of column names
      
      encodingMethod: 'onehot',
      isEncodingApplied: false,
      encodedColumns: [], // List of { name, method }
      
      smote: {
        applied: false,
        strategy: 'auto',
        kNeighbors: 5
      },
      
      // Feature Selection
      selectedFeatures: [],
      droppedColumns: []
    },
    
    // Model Selection
    model: {
      selectedAlgorithm: null, // Algorithm ID/Name
      hyperparameters: {}, // { C: 1.0, kernel: 'rbf' }
      validationStrategy: 'kfold',
      folds: 5
    }
  }),
  
  actions: {
    // Dataset Actions
    setDataset(id, name, size) {
      this.datasetId = id;
      this.datasetName = name;
      this.datasetSize = size || { rows: 0, columns: 0 };
    },
    
    // Target Actions
    setTarget(column, typeInfo) {
      this.targetColumn = column;
      this.problemType = typeInfo;
    },
    
    // Preprocessing Actions
    updateSplitConfig(ratio, strategy, seed) {
      this.preprocessing.splitRatio = ratio;
      this.preprocessing.splitStrategy = strategy;
      this.preprocessing.randomSeed = seed;
    },
    
    setSplitApplied(status) {
      this.preprocessing.isSplitApplied = status;
    },
    
    updateScaling(method, columns, applied = true) {
      this.preprocessing.scalingMethod = method;
      this.preprocessing.scaledColumns = columns;
      this.preprocessing.isScalingApplied = applied;
    },
    
    updateEncoding(columns, applied = true) {
      this.preprocessing.encodedColumns = columns;
      this.preprocessing.isEncodingApplied = applied;
    },
    
    updateSmote(config) {
      this.preprocessing.smote = { ...this.preprocessing.smote, ...config };
    },
    
    // Model Actions
    setSelectedAlgorithm(algo) {
      this.model.selectedAlgorithm = algo;
    },
    
    // Reset Experiment (Keep dataset, clear configs)
    resetExperiment() {
      const currentId = this.datasetId;
      const currentName = this.datasetName;
      const currentSize = this.datasetSize;
      
      this.$reset();
      
      // Restore dataset link
      this.datasetId = currentId;
      this.datasetName = currentName;
      this.datasetSize = currentSize;
    },
    
    // Full Reset
    clearAll() {
      this.$reset();
    }
  },
  
  persist: true, // Auto-persist entire state using default storage (localStorage)
});
