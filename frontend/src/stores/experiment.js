import { defineStore } from 'pinia';

export const useExperimentStore = defineStore('experiment', {
  state: () => ({
    // Dataset Reference
    datasetId: null,
    datasetName: null,
    datasetSize: { rows: 0, columns: 0 },
    datasetMetadata: null, // { name: '', rows: 0, columns: 0, etc. }
    
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
      droppedColumns: [],
      
      // Data Cleaning & Feature Engineering (from Preview)
      isMissingValuesApplied: false,
      isOutliersApplied: false, 
      isDuplicatesApplied: false,
      isDateTimeApplied: false
    },
    
    // Model Configuration (Flattened for easier reactivity in components)
    selectedAlgorithm: null, // Algorithm object/ID
    hyperparameters: {},
    validationStrategy: 'kfold',
    folds: 5,
    testSize: 0.2
  }),
  
  actions: {
    // Dataset Actions
    setDataset(id, name, size) {
      // Clear experiment state to ensure fresh start
      this.targetColumn = null;
      this.problemType = null;
      this.resetPreprocessing(); // Use existing reset action
      this.selectedAlgorithm = null;
      this.hyperparameters = {};
      this.validationStrategy = 'kfold';

      this.datasetId = id;
      this.datasetName = name;
      const cleanSize = size || { rows: 0, columns: 0 };
      this.datasetSize = cleanSize;
      
      // Keep datasetMetadata in sync for components expecting it
      this.datasetMetadata = {
        id: id,
        name: name,
        totalRows: cleanSize.rows || 0,
        columns: cleanSize.columns || 0
      };
    },

    setDatasetId(id) {
      this.datasetId = id;
      if (this.datasetMetadata) {
        this.datasetMetadata.id = id;
      } else {
        this.datasetMetadata = { id: id };
      }
    },

    updateDatasetMetadata(metadata) {
      if (metadata.id) this.datasetId = metadata.id;
      if (metadata.name) this.datasetName = metadata.name;
      if (metadata.size) this.datasetSize = metadata.size;
      
      this.datasetMetadata = {
        ...this.datasetMetadata,
        ...metadata,
        // Ensure standard keys exist for components
        totalRows: metadata.totalRows || metadata.size?.rows || this.datasetMetadata?.totalRows || 0,
        columns: metadata.columns || metadata.size?.columns || this.datasetMetadata?.columns || 0
      };
    },
    
    // Target Actions
    setTarget(column, typeInfo) {
      this.targetColumn = column;
      this.problemType = typeInfo;
    },

    setTargetColumn(column) {
      this.targetColumn = column;
    },

    setProblemType(type) {
      this.problemType = type;
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
    
    setScalingApplied(status) {
      this.preprocessing.isScalingApplied = status;
    },

    setEncodingApplied(status) {
      this.preprocessing.isEncodingApplied = status;
    },

    setSmoteApplied(status, config) {
      this.preprocessing.smote.applied = status;
      if (config) {
        this.preprocessing.smote = { ...this.preprocessing.smote, ...config };
      }
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

    setMissingValuesApplied(status) {
      this.preprocessing.isMissingValuesApplied = status;
    },

    setOutliersApplied(status) {
      this.preprocessing.isOutliersApplied = status;
    },

    setDuplicatesApplied(status) {
      this.preprocessing.isDuplicatesApplied = status;
    },

    setDateTimeApplied(status) {
      this.preprocessing.isDateTimeApplied = status;
    },

    setDroppedColumns(columns) {
      this.preprocessing.droppedColumns = columns;
    },
    
    // Model Actions
    setAlgorithm(algo) {
      this.selectedAlgorithm = algo;
    },

    setSelectedAlgorithm(algo) {
      this.selectedAlgorithm = algo;
    },

    setHyperparameters(params) {
      this.hyperparameters = params;
    },

    setValidationConfig(strategy, config = {}) {
      this.validationStrategy = strategy;
      if (config.folds) this.folds = config.folds;
      if (config.testSize) this.testSize = config.testSize;
    },

    resetPreprocessing() {
      this.preprocessing = {
        splitRatio: 0.8,
        splitStrategy: 'random',
        randomSeed: 42,
        isSplitApplied: false,
        scalingMethod: 'standard',
        isScalingApplied: false,
        scaledColumns: [],
        encodingMethod: 'onehot',
        isEncodingApplied: false,
        encodedColumns: [],
        smote: {
          applied: false,
          strategy: 'auto',
          kNeighbors: 5
        },
        selectedFeatures: [],
        droppedColumns: [],
        isMissingValuesApplied: false,
        isOutliersApplied: false,
        isDuplicatesApplied: false,
        isDateTimeApplied: false
      };
    },
    
    // Reset Experiment (Keep dataset, clear configs)
    resetExperiment() {
      const currentId = this.datasetId;
      const currentName = this.datasetName;
      const currentSize = this.datasetSize;
      const currentMetadata = this.datasetMetadata;
      
      this.$reset();
      
      // Restore dataset link
      this.datasetId = currentId;
      this.datasetName = currentName;
      this.datasetSize = currentSize;
      this.datasetMetadata = currentMetadata;
    },
    
    // Full Reset
    clearAll() {
      this.$reset();
    }
  },
  
  persist: true,
});
