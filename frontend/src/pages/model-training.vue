<template>
  <div class="model-training">
    <!-- Navigation Header -->
    <nav class="training-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
            />
          </svg>
          Back to Algorithm Selection
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Model Training</span>
        </div>
      </div>

      <div class="header-status" v-if="backendConnected !== null">
        <div class="status-indicator" :class="{ connected: backendConnected }">
          <div class="status-dot"></div>
          <span class="status-text">{{
            backendConnected ? "Backend Connected" : "Backend Offline"
          }}</span>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        
        <h1>Model Training</h1>
        <p>Training your {{ problemType }} model with advanced features</p>

        <div class="training-summary" v-if="modelConfig">
          <span class="summary-item"
            >{{ formatNumber(datasetStats.rows) }} samples</span
          >
          <span class="summary-divider">•</span>
          <span class="summary-item">{{
            modelConfig.algorithm?.name || "Unknown"
          }}</span>
          <span class="summary-divider">•</span>
          <span class="summary-item">{{ getValidationMethodDisplay() }}</span>
        </div>
      </div>
    </div>

    
    <div class="preprocessing-summary" v-if="preprocessingInfo">
      <div
        class="section-header"
        @click="showPreprocessing = !showPreprocessing"
      >
        <h3>🔧 Data Preprocessing Applied</h3>
        <span class="toggle-icon">{{ showPreprocessing ? "▼" : "►" }}</span>
      </div>

      <div v-if="showPreprocessing" class="preprocessing-details">
        <!-- Scaling card -->
        <div class="preprocessing-card">
          <h4>📊 Scaling: {{ preprocessingInfo.scaling?.method }}</h4>
          <p>
            Applied to {{ preprocessingInfo.scaling?.columns?.length }} numeric
            columns
          </p>
          <div class="stats-badges">
            <span class="badge success">✓ Mean = 0.0</span>
            <span class="badge success">✓ Std = 1.0</span>
          </div>
        </div>

        <!-- Feature engineering card -->
        <div class="preprocessing-card">
          <h4>🔨 Feature Engineering</h4>
          <p>
            Features: {{ preprocessingInfo.originalFeatures }} →
            {{ preprocessingInfo.finalFeatures }} (+{{
              preprocessingInfo.finalFeatures -
              preprocessingInfo.originalFeatures
            }})
          </p>
        </div>
      </div>
    </div>

    <!-- ===== Configuration Section (Always Visible) ===== -->
    <div class="configuration-container">
      <section class="configuration-section">
        <div class="section-header">
          <h2>Configure {{ modelConfig?.algorithm?.name || 'Model' }}</h2>
          <p class="section-description">
            Set hyperparameters and validation strategy before training
          </p>
          <div v-if="isTraining" class="training-active-badge">
            🔄 Training in Progress - Configuration Locked
          </div>
          
          
        </div>

        <div class="config-grid">
          <!-- Hyperparameters Panel - Placeholder for Phase 2 -->
          <div class="config-panel">
            <div class="panel-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
                </svg>
                Hyperparameters
              </h3>
              <button 
                @click="resetHyperparametersToDefault" 
                class="reset-params-btn"
                :disabled="isTraining"
                title="Reset all hyperparameters to default values"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,4C14.1,4 16.1,4.8 17.6,6.3C20.7,9.4 20.7,14.5 17.6,17.6C15.8,19.5 13.3,20.2 10.9,19.9L11.4,17.9C13.1,18.1 14.9,17.5 16.2,16.2C18.5,13.9 18.5,10.1 16.2,7.7C15.1,6.6 13.5,6 12,6V10.6L7,5.6L12,0.6V4M6.3,17.6C3.7,15 3.3,11 5.1,7.9L6.6,9.4C5.5,11.6 5.9,14.4 7.8,16.2C8.3,16.7 8.9,17.1 9.6,17.4L9,19.4C8,19 7.1,18.4 6.3,17.6Z"/>
                </svg>
                Reset to Default
              </button>
            </div>
            <div class="hyperparameters-container">
              <div
                v-for="paramGroup in getKeyParameters(modelConfig?.algorithm?.name)"
                :key="paramGroup.name"
                class="param-group"
              >
                <div class="param-group-header">
                  <span class="group-icon">{{ paramGroup.icon }}</span>
                  <h4>{{ paramGroup.name }}</h4>
                </div>

                <div class="params-list">
                  <template v-for="param in paramGroup.params" :key="param.name">
                    <div
                      v-if="shouldShowParam(param)"
                      class="param-item"
                    >
                    <div class="param-header">
                      <label class="param-label">{{ param.label }}</label>
                      <span class="param-impact" :class="param.impact">
                        {{ param.impact }} impact
                      </span>
                    </div>

                    <!-- Slider Parameter -->
                    <div v-if="param.type === 'slider'" class="param-control">
                      <div class="slider-container">
                        <input
                          type="range"
                          v-model.number="hyperparameters[param.name]"
                          :min="param.min"
                          :max="param.max"
                          :step="param.step"
                          :disabled="isTraining"
                          class="param-slider"
                        />
                        <div class="slider-value">
                          {{ formatParameterValue(param.name, hyperparameters[param.name]) }}
                        </div>
                      </div>
                    </div>

                    <!-- Select Parameter -->
                    <div v-else-if="param.type === 'select'" class="param-control">
                      <select
                        v-model="hyperparameters[param.name]"
                        class="param-select"
                      >
                        <option
                          v-for="option in param.options"
                          :key="option.value"
                          :value="option.value"
                        >
                          {{ option.label }}
                        </option>
                      </select>
                    </div>

                    <!-- Checkbox Parameter -->
                    <div v-else-if="param.type === 'checkbox'" class="param-control">
                      <label class="checkbox-container">
                        <input
                          type="checkbox"
                          v-model="hyperparameters[param.name]"
                          class="param-checkbox"
                        />
                        <span class="checkbox-label">{{ param.label }}</span>
                      </label>
                    </div>

                    <p class="param-description">{{ param.description }}</p>
                  </div>
                </template>
              </div>
              </div>
            </div>
          </div>

          <!-- Validation Strategy Panel - Placeholder for Phase 3 -->
          <div class="config-panel">
            <div class="panel-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z"/>
                </svg>
                Validation Strategy
              </h3>
            </div>
            <div class="validation-strategies">
              <!-- Simple Validation (No CV) -->
              <div 
                class="strategy-card"
                :class="{ active: validationStrategy === 'simple', disabled: isTraining }"
                @click="!isTraining && (validationStrategy = 'simple')"
              >
                <div class="strategy-header">
                  <div class="strategy-icon">✓</div>
                  <h4>Simple Validation</h4>
                  <div class="strategy-badge recommended">Recommended</div>
                </div>
                <p class="strategy-description">
                  Use the train/test split from preprocessing. Fast and straightforward.
                </p>
              </div>

              <!-- K-Fold Cross-Validation -->
              <div 
                class="strategy-card"
                :class="{ active: validationStrategy === 'kfold_cv', disabled: isTraining }"
                @click="!isTraining && (validationStrategy = 'kfold_cv')"
              >
                <div class="strategy-header">
                  <div class="strategy-icon">🔄</div>
                  <h4>K-Fold Cross-Validation</h4>
                  <div class="strategy-badge">More Robust</div>
                </div>
                <p class="strategy-description">
                  Split training data into K folds for more reliable evaluation.
                </p>
                
                <!-- K-Fold Configuration -->
                <div v-if="validationStrategy === 'kfold_cv'" class="strategy-config">
                  <div class="config-item">
                    <label>Number of Folds: {{ cvFolds }}</label>
                    <input
                      type="range"
                      v-model.number="cvFolds"
                      min="2"
                      max="10"
                      step="1"
                      class="config-slider"
                    />
                    <p class="config-hint">{{ cvFolds }} training iterations on training set</p>
                  </div>
                  
                  <div class="config-item">
                    <label class="checkbox-container">
                      <input type="checkbox" v-model="stratifiedCV" class="param-checkbox" />
                      <span class="checkbox-label">Stratified K-Fold</span>
                    </label>
                    <p class="config-hint">Maintains class distribution in each fold</p>
                  </div>
                </div>
              </div>

              <!-- Randomized Search CV (Advanced) -->
              <div 
                class="strategy-card"
                :class="{ active: validationStrategy === 'randomized_search', disabled: isTraining }"
                @click="!isTraining && (validationStrategy = 'randomized_search')"
              >
                <div class="strategy-header">
                  <div class="strategy-icon">🎲</div>
                  <h4>Randomized Search CV</h4>
                  <div class="strategy-badge advanced">Advanced</div>
                </div>
                <p class="strategy-description">
                  Randomly sample hyperparameters. Faster than Grid Search.
                </p>
                
                <!-- Randomized Search Configuration -->
                <div v-if="validationStrategy === 'randomized_search'" class="strategy-config">
                  <div class="config-item">
                    <label>Iterations: {{ randomSearchIterations }}</label>
                    <input
                      type="range"
                      v-model.number="randomSearchIterations"
                      min="10"
                      max="100"
                      step="10"
                      class="config-slider"
                    />
                  </div>
                  
                  <div class="config-item">
                    <label>CV Folds: {{ randomSearchCVFolds }}</label>
                    <input
                      type="range"
                      v-model.number="randomSearchCVFolds"
                      min="2"
                      max="10"
                      step="1"
                      class="config-slider"
                    />
                  </div>
                </div>
              </div>

              <!-- Grid Search CV (Advanced) -->
              <div 
                class="strategy-card"
                :class="{ active: validationStrategy === 'grid_search', disabled: isTraining }"
                @click="!isTraining && (validationStrategy = 'grid_search')"
              >
                <div class="strategy-header">
                  <div class="strategy-icon">🔍</div>
                  <h4>Grid Search CV</h4>
                  <div class="strategy-badge expert">Expert</div>
                </div>
                <p class="strategy-description">
                  Exhaustively search best hyperparameters using cross-validation.
                </p>
                
                <!-- Grid Search Configuration -->
                <div v-if="validationStrategy === 'grid_search'" class="strategy-config">
                  <div class="config-item">
                    <label>CV Folds: {{ gridSearchCVFolds }}</label>
                    <input
                      type="range"
                      v-model.number="gridSearchCVFolds"
                      min="2"
                      max="10"
                      step="1"
                      class="config-slider"
                    />
                  </div>
                  
                  <div class="config-item">
                    <label>Grid Density</label>
                    <select v-model="gridDensity" class="param-select">
                      <option value="coarse">Coarse (Faster)</option>
                      <option value="normal">Normal</option>
                      <option value="fine">Fine (Slower)</option>
                    </select>
                  </div>
                  
                  <div class="warning-box">
                    ⚠️ Grid Search can be time-consuming for large parameter spaces
                  </div>
                </div>
              </div>

              
            </div>
          </div>
        </div>

        <!-- Start Training Button -->
        <div class="config-actions" v-if="trainingPhase === 'configuration' || isCompleted">
          <button @click="proceedToTraining" class="start-training-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8,5.14V19.14L19,12.14L8,5.14Z"/>
            </svg>
            {{ isCompleted ? 'Retrain Model' : 'Start Training' }}
          </button>
        </div>
      </section>
    </div>

    <!-- Main Container (Training & Results) - Shows Below Configuration -->
    <div v-if="trainingPhase === 'training'" id="training-section" class="main-container">
      <!-- Training Progress Section -->
      <section class="progress-section">
        <div class="section-header">
          <h2>Training Progress</h2>
          <div class="training-controls">
            <button
              @click="startTraining"
              :disabled="isTraining || isCompleted"
              class="control-btn start"
              v-if="!isTraining && !isCompleted"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
              </svg>
              Start Training
            </button>

            <button
              @click="stopTraining"
              :disabled="!isTraining"
              class="control-btn stop"
              v-if="isTraining"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M18,18H6V6H18V18Z" />
              </svg>
              Stop Training
            </button>
          </div>
        </div>

        <!-- Progress Dashboard -->
        <div class="progress-dashboard">
          <!-- Current Stage Banner -->
          <div class="current-stage-banner">
            <div class="stage-info-left">
              <span class="stage-icon-large">{{ getCurrentStageIcon() }}</span>
              <div class="stage-text">
                <div class="stage-title">{{ currentStageTitle }}</div>
                <div class="stage-subtitle">{{ currentStageMessage }}</div>
              </div>
            </div>
            <div class="stage-progress-right">
              <div class="progress-percentage-large">
                {{ Math.round(trainingProgress) }}%
              </div>
              <div class="progress-dots">
                <span
                  v-for="i in 5"
                  :key="i"
                  class="progress-dot"
                  :class="{ active: i <= Math.ceil(trainingProgress / 20) }"
                ></span>
              </div>
            </div>
          </div>

          
        </div>
      </section>

      <!-- Metrics and Charts Grid -->
      <div class="metrics-charts-grid">
        <!-- Metrics Section -->
        <section class="metrics-section">
          <div class="section-header">
            <h2>Performance Metrics</h2>
          </div>

          <div class="metrics-grid">
            <!-- ===== CLASSIFICATION METRICS ===== -->
            <template v-if="problemType.includes('classification')">
              <!-- Accuracy Card -->
              <div class="metric-card primary animated">
                <div class="metric-header">
                  <div class="metric-icon">🎯</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ (currentMetrics.test_accuracy * 100).toFixed(1) }}%</div>
                  <div class="metric-label">Accuracy</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ (currentMetrics.train_accuracy * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ (currentMetrics.test_accuracy * 100).toFixed(1) }}%</span>
                    </div>
                  </div>
                  
                </div>
              </div>

              <!-- F1-Score Card -->
              <div class="metric-card success animated">
                <div class="metric-header">
                  <div class="metric-icon">📊</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ (currentMetrics.test_f1 * 100).toFixed(1) }}%</div>
                  <div class="metric-label">F1-Score</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ (currentMetrics.train_f1 * 100).toFixed(1) }}%</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ (currentMetrics.test_f1 * 100).toFixed(1) }}%</span>
                      
                    </div>
                  </div>
                  
                </div>
              </div>

              <!-- Precision Card -->
              <div class="metric-card info animated">
                <div class="metric-header">
                  <div class="metric-icon">🎲</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ (currentMetrics.test_precision * 100).toFixed(1) }}%</div>
                  <div class="metric-label">Precision</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ (currentMetrics.train_precision * 100).toFixed(1) }}%</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ (currentMetrics.test_precision * 100).toFixed(1) }}%</span>
                      
                    </div>
                  </div>

                </div>
              </div>

              <!-- Recall Card -->
              <div class="metric-card warning animated">
                <div class="metric-header">
                  <div class="metric-icon">🔍</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ (currentMetrics.test_recall * 100).toFixed(1) }}%</div>
                  <div class="metric-label">Recall</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ (currentMetrics.train_recall * 100).toFixed(1) }}%</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ (currentMetrics.test_recall * 100).toFixed(1) }}%</span>
                      
                    </div>
                  </div>

                </div>
              </div>
            </template>

            <!-- ===== REGRESSION METRICS ===== -->
            <template v-else>
              <!-- R² Score Card -->
              <div class="metric-card primary animated">
                <div class="metric-header">
                  <div class="metric-icon">🎯</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ currentMetrics.test_r2.toFixed(2) }}</div>
                  <div class="metric-label">R² Score</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ currentMetrics.train_r2.toFixed(2) }}</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ currentMetrics.test_r2.toFixed(2) }}</span>
                      
                    </div>
                  </div>
                  
                </div>
              </div>

              <!-- MSE Card -->
              <div class="metric-card primary animated">
                <div class="metric-header">
                  <div class="metric-icon">📉</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatNumber(currentMetrics.test_mse.toFixed(0)) }}</div>
                  <div class="metric-label">MSE</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ formatNumber(currentMetrics.train_mse.toFixed(0)) }}</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ formatNumber(currentMetrics.test_mse.toFixed(0)) }}</span>
                      
                    </div>
                  </div>
                  
                </div>
              </div>

              <!-- MAE Card -->
              <div class="metric-card info animated">
                <div class="metric-header">
                  <div class="metric-icon">📊</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatNumber(currentMetrics.test_mae.toFixed(0)) }}</div>
                  <div class="metric-label">MAE</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ formatNumber(currentMetrics.train_mae.toFixed(0)) }}</span>
                     
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ formatNumber(currentMetrics.test_mae.toFixed(0)) }}</span>
                      
                    </div>
                  </div>

                </div>
              </div>

              <!-- RMSE Card -->
              <div class="metric-card warning animated">
                <div class="metric-header">
                  <div class="metric-icon">📐</div>
                  <span v-if="isTraining" class="live-indicator"></span>
                </div>
                <div class="metric-content">
                  <div class="metric-value">{{ formatNumber(calculateRMSE().toFixed(0)) }}</div>
                  <div class="metric-label">RMSE</div>
                  <div class="metric-split">
                    <div class="split-item">
                      <span class="split-label">Train</span>
                      <span class="split-value">{{ formatNumber(Math.sqrt(currentMetrics.train_mse).toFixed(0)) }}</span>
                      
                    </div>
                    <div class="split-item">
                      <span class="split-label">Test</span>
                      <span class="split-value">{{ formatNumber(calculateRMSE().toFixed(0)) }}</span>
                      
                    </div>
                  </div>

                </div>
              </div>
            </template>
          </div>

          <!-- Cross-Validation Results (NEW) -->
          <div v-if="currentMetrics.validation_method === 'kfold_cv'" class="cv-results-section">
            <h3>Cross-Validation Results</h3>
            <div class="cv-metrics-grid">
              <div class="metric-card highlight">
                <div class="metric-icon">🎯</div>
                <div class="metric-content">
                  <div class="metric-label">Mean CV Score</div>
                  <div class="metric-value">{{ (currentMetrics.cv_mean * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-content">
                  <div class="metric-label">Standard Deviation</div>
                  <div class="metric-value">± {{ (currentMetrics.cv_std * 100).toFixed(2) }}%</div>
                </div>
              </div>
            </div>
            
            <div class="fold-scores-list">
              <h4>Individual Fold Scores</h4>
              <div class="folds-grid">
                <div v-for="(score, idx) in currentMetrics.cv_scores" :key="idx" class="fold-item">
                  <span class="fold-label">Fold {{ idx + 1 }}</span>
                  <span class="fold-value"> {{ (score * 100).toFixed(2) }}%</span>
                  <div class="fold-bar" :style="{ width: (score * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Grid Search CV Results -->
          <div v-if="currentMetrics.validation_method === 'grid_search'" class="cv-results-section">
            <h3>🔍 Grid Search CV Results</h3>
            
            <!-- Best Score -->
            <div class="cv-metrics-grid">
              <div class="metric-card highlight">
                <div class="metric-icon">🏆</div>
                <div class="metric-content">
                  <div class="metric-label">Best Score</div>
                  <div class="metric-value">{{ (currentMetrics.best_score * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-content">
                  <div class="metric-label">Mean CV Score</div>
                  <div class="metric-value">{{ (currentMetrics.cv_mean * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-content">
                  <div class="metric-label">Std Deviation</div>
                  <div class="metric-value">± {{ (currentMetrics.cv_std * 100).toFixed(2) }}%</div>
                </div>
              </div>
            </div>
            
            <!-- Best Parameters -->
            <div class="best-params-section" v-if="currentMetrics.best_params">
              <h4>✨ Best Hyperparameters Found</h4>
              <div class="params-grid">
                <div v-for="(value, key) in currentMetrics.best_params" :key="key" class="param-badge">
                  <span class="param-name">{{ key }}</span>
                  <span class="param-value">{{ value }}</span>
                </div>
              </div>
            </div>
            
            <!-- Fold Scores -->
            <div class="fold-scores-list">
              <h4>Individual Fold Scores</h4>
              <div class="folds-grid">
                <div v-for="(score, idx) in currentMetrics.cv_scores" :key="idx" class="fold-item">
                  <span class="fold-label">Fold {{ idx + 1 }}</span>
                  <span class="fold-value">{{ (score * 100).toFixed(2) }}%</span>
                  <div class="fold-bar" :style="{ width: (score * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Randomized Search CV Results -->
          <div v-if="currentMetrics.validation_method === 'randomized_search'" class="cv-results-section">
            <h3>🎲 Randomized Search CV Results</h3>
            
            <!-- Best Score -->
            <div class="cv-metrics-grid">
              <div class="metric-card highlight">
                <div class="metric-icon">🏆</div>
                <div class="metric-content">
                  <div class="metric-label">Best Score</div>
                  <div class="metric-value">{{ (currentMetrics.best_score * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-content">
                  <div class="metric-label">Mean CV Score</div>
                  <div class="metric-value">{{ (currentMetrics.cv_mean * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-content">
                  <div class="metric-label">Std Deviation</div>
                  <div class="metric-value">± {{ (currentMetrics.cv_std * 100).toFixed(2) }}%</div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">🔢</div>
                <div class="metric-content">
                  <div class="metric-label">Iterations</div>
                  <div class="metric-value">{{ currentMetrics.n_iterations }}</div>
                </div>
              </div>
            </div>
            
            <!-- Best Parameters -->
            <div class="best-params-section" v-if="currentMetrics.best_params">
              <h4>✨ Best Hyperparameters Found</h4>
              <div class="params-grid">
                <div v-for="(value, key) in currentMetrics.best_params" :key="key" class="param-badge">
                  <span class="param-name">{{ key }}</span>
                  <span class="param-value">{{ value }}</span>
                </div>
              </div>
            </div>
            
            <!-- Fold Scores -->
            <div class="fold-scores-list">
              <h4>Individual Fold Scores</h4>
              <div class="folds-grid">
                <div v-for="(score, idx) in currentMetrics.cv_scores" :key="idx" class="fold-item">
                  <span class="fold-label">Fold {{ idx + 1 }}</span>
                  <span class="fold-value">{{ (score * 100).toFixed(2) }}%</span>
                  <div class="fold-bar" :style="{ width: (score * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="charts-section">
          <div class="section-header">
            <h2>Training Visualization</h2>
          </div>
          <div class="chart-container">
            <canvas ref="chartContainer" v-if="isTraining || isCompleted"></canvas>
            <div class="chart-placeholder" v-else>
              <p>Training curves will appear during training</p>
            </div>
          </div>
        </section>
      </div>

      <!-- Visualization and Download Actions (Final Location) -->
      <div v-if="isCompleted" class="final-actions-section">
          <button @click="viewDetailedResults" class="view-results-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M11,9H13V7H11M11,17H13V11H11M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
            </svg>
            <span class="btn-title">View Detailed Visualizations</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" class="arrow-icon">
              <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"/>
            </svg>
          </button>

          <button @click="downloadModel" class="download-model-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"/>
            </svg>
            <span class="btn-title">Download Trained Model</span>
          </button>
      </div>

      <!-- Logs Section -->
      <section class="logs-section">
        <div class="section-header">
          <h2>Training Logs</h2>
          <div class="log-controls">
            <button @click="clearLogs" class="clear-btn">Clear</button>
          </div>
        </div>
        <div class="logs-container" ref="logsContainer">
          <div v-for="(log, index) in trainingLogs" :key="index" class="log-entry" :class="log.type">
            <span class="log-time">{{ formatLogTime(log.timestamp) }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter, useRoute } from "vue-router";
import { Chart, registerables } from "chart.js";
import { storeToRefs } from "pinia";
import { useExperimentStore } from "@/stores/experiment";
import { useAuthenticatedFetch } from '~/composables/useAuthenticatedFetch';
Chart.register(...registerables);

const router = useRouter();
const route = useRoute();
const { authenticatedGet } = useAuthenticatedFetch();
const experimentStore = useExperimentStore();

const { 
  datasetId: storeDatasetId, 
  targetColumn: storeTargetColumn, 
  problemType: storeProblemType, 
  selectedAlgorithm: storeAlgorithm,
  datasetMetadata
} = storeToRefs(experimentStore);

// State
const isInitializing = ref(true);
const initializationProgress = ref(0);
const initializationMessage = ref("Loading configuration...");
const backendConnected = ref(null);
const currentStageTitle = ref('Ready to Start Training');
const currentStageMessage = ref('Click Start Training to begin');
const currentProcessingStep = ref('Initializing...');
const trainingPhase = ref('configuration');

// Config
const hyperparameters = reactive({});
const selectedScaling = ref('standard');
const featureEngineering = reactive({ polynomial: false, pca: false, featureSelection: true });
const validationStrategy = ref('simple');
const splitRatio = ref(0.8);
const stratifiedCV = ref(true);
const cvFolds = ref(5);
const gridSearchCVFolds = ref(5);
const gridDensity = ref('normal');
const randomSearchCVFolds = ref(5);
const randomSearchIterations = ref(20);

// Training State
const isTraining = ref(false);
const isPaused = ref(false);
const isCompleted = ref(false);
const lastTrainedModelId = ref(null);
const preprocessingInfo = ref(null);
const showPreprocessing = ref(false);
const trainingProgress = ref(0);
const currentEpoch = ref(0);
const totalEpochs = ref(100);
const currentStage = ref(0);
const elapsedTime = ref(0);
let websocket = null;
let timeInterval = null;
const modelConfig = ref(null);
const datasetStats = ref({ rows: 0, features: 0 });
const datasetId = ref(null);
const problemType = ref("classification");
const selectedChart = ref("accuracy");
const trainingLogs = ref([]);
const logsContainer = ref(null);
const chartContainer = ref(null);
let trainingChart = null;

// Progress simulation
let progressSimulator = null;
const targetProgress = ref(0);

const currentMetrics = reactive({
  train_accuracy: 0, test_accuracy: 0, train_f1: 0, test_f1: 0,
  train_precision: 0, test_precision: 0, train_recall: 0, test_recall: 0,
  train_r2: 0, test_r2: 0, train_mse: 0, test_mse: 0,
  train_mae: 0, test_mae: 0,
  cv_mean: 0, cv_std: 0, cv_scores: [],
  validation_method: 'simple',
  best_params: null,
  best_score: 0,
  n_iterations: 0
});

// Training History for comparison
const trainingHistory = ref([]);
const showHistory = ref(false);

const metricChanges = reactive({ main: 0, secondary: 0 });

const trainingStages = ref([
  { name: 'Preprocessing', status: 'pending' },
  { name: 'Training', status: 'pending' },
  { name: 'Validation', status: 'pending' },
  { name: 'Finalizing', status: 'pending' }
]);

// Computed
const testSize = computed({ get: () => 1 - splitRatio.value, set: (val) => { splitRatio.value = 1 - val; } });

// Functions
const formatNumber = (num) => new Intl.NumberFormat().format(num);
const formatMetric = (val) => (typeof val === 'number' ? val.toFixed(3) : '0.0');
const formatMainMetric = () => problemType.value.includes('classification') ? (currentMetrics.test_accuracy * 100).toFixed(1) + '%' : currentMetrics.test_r2.toFixed(3);
const getMainMetricLabel = () => problemType.value.includes('classification') ? 'Test Accuracy' : 'R² Score';
const formatSecondaryMetric = () => problemType.value.includes('classification') ? (currentMetrics.test_f1 * 100).toFixed(1) + '%' : currentMetrics.test_mse.toFixed(2);
const getSecondaryMetricLabel = () => problemType.value.includes('classification') ? 'F1-Score' : 'MSE';
const formatChange = (val) => `${val > 0 ? '+' : ''}${val.toFixed(2)}%`;
const getChangeClass = (val, isLoss) => isLoss ? (val > 0 ? 'negative' : 'positive') : (val > 0 ? 'positive' : 'negative');
const formatTime = (s) => `${Math.floor(s / 60)}m ${s % 60}s`;
const formatLogTime = (ts) => new Date(ts).toLocaleTimeString();
const getCurrentStageIcon = () => '🔄';
const getStageStatusClass = (i) => trainingStages.value[i]?.status || 'pending';
const getStageIconByStatus = (i) => trainingStages.value[i]?.status === 'completed' ? '✓' : '○';
const getValidationMethodDisplay = () => {
  const methodLabels = {
    'simple': 'Train/Test Split',
    'kfold_cv': 'K-Fold CV',
    'grid_search': 'Grid Search CV',
    'randomized_search': 'Randomized Search CV'
  };
  return methodLabels[validationStrategy.value] || validationStrategy.value;
};

// ===== NEW HELPER FUNCTIONS FOR ENHANCED METRICS =====




const calculateRMSE = () => {
  return Math.sqrt(currentMetrics.test_mse || 0);
};

// Format metric values for display
const formatMetricValue = (value, decimals = 2) => {
  if (typeof value !== 'number' || isNaN(value)) return '0.00';
  
  // For very large numbers (MSE), use compact notation
  if (Math.abs(value) >= 1000000) {
    return (value / 1000000).toFixed(2) + 'M';
  } else if (Math.abs(value) >= 1000) {
    return new Intl.NumberFormat('en-US', { 
      minimumFractionDigits: decimals, 
      maximumFractionDigits: decimals 
    }).format(value);
  }
  
  return value.toFixed(decimals);
};



const updateMetrics = (metrics) => {
  if (!metrics) {
    console.warn("⚠️ updateMetrics called with null/undefined metrics");
    return;
  }
  
  console.log("📊 updateMetrics called with:", metrics);
  
  const metricProblemType = metrics.problem_type || problemType.value;
  
  if (metricProblemType === "classification") {
    currentMetrics.train_accuracy = metrics.train_accuracy || 0;
    currentMetrics.test_accuracy = metrics.test_accuracy || 0;
    currentMetrics.train_f1 = metrics.train_f1 || 0;
    currentMetrics.test_f1 = metrics.test_f1 || 0;
    currentMetrics.train_precision = metrics.train_precision || 0;
    currentMetrics.test_precision = metrics.test_precision || 0;
    currentMetrics.train_recall = metrics.train_recall || 0;
    currentMetrics.test_recall = metrics.test_recall || 0;

    console.log("✅ Classification metrics assigned:", {
      train_accuracy: currentMetrics.train_accuracy,
      test_accuracy: currentMetrics.test_accuracy,
      train_f1: currentMetrics.train_f1,
      test_f1: currentMetrics.test_f1,
      train_precision: currentMetrics.train_precision,
      test_precision: currentMetrics.test_precision,
      train_recall: currentMetrics.train_recall,
      test_recall: currentMetrics.test_recall,
    });

    const newMain = currentMetrics.test_accuracy;
    metricChanges.main = (newMain - (metricChanges.prevMain || 0)) * 100;
    metricChanges.prevMain = newMain;
    
  } else if (metricProblemType === "regression") {
    currentMetrics.train_r2 = metrics.train_r2 || metrics.trainr2 || 0;
    currentMetrics.test_r2 = metrics.test_r2 || metrics.testr2 || 0;
    currentMetrics.train_mse = metrics.train_mse || metrics.trainmse || 0;
    currentMetrics.test_mse = metrics.test_mse || metrics.testmse || 0;
    currentMetrics.train_mae = metrics.train_mae || metrics.trainmae || 0;
    currentMetrics.test_mae = metrics.test_mae || metrics.testmae || 0;

    const newMain = currentMetrics.test_r2;
    const prevMain = metricChanges.prevMain || 0;
    const prevSecondary = metricChanges.mseValue || currentMetrics.test_mse;

    metricChanges.main = (newMain - prevMain) * 100;
    metricChanges.secondary = currentMetrics.test_mse - prevSecondary;
    metricChanges.prevMain = newMain;
    metricChanges.mseValue = currentMetrics.test_mse;

    console.log("✅ Regression metrics updated:", {
      test_r2: currentMetrics.test_r2,
      test_mse: currentMetrics.test_mse,
      test_mae: currentMetrics.test_mae,
    });
  }

  // Cross-validation metrics
  if (metrics.cv_mean !== undefined || metrics.cvmean !== undefined) {
    currentMetrics.cv_mean = metrics.cv_mean || metrics.cvmean || 0;
    currentMetrics.cv_std = metrics.cv_std || metrics.cvstd || 0;
    currentMetrics.cv_scores = metrics.cv_scores || metrics.cvscores || [];
  }
  
  // Grid Search / Randomized Search specific metrics
  if (metrics.best_params !== undefined) {
    currentMetrics.best_params = metrics.best_params;
  }
  if (metrics.best_score !== undefined) {
    currentMetrics.best_score = metrics.best_score;
  }
  if (metrics.n_iterations !== undefined) {
    currentMetrics.n_iterations = metrics.n_iterations;
  }
  
  // Update validation method
  if (metrics.validation_method !== undefined) {
    currentMetrics.validation_method = metrics.validation_method;
  } else {
    // Fallback: Use the strategy selected in the UI
    currentMetrics.validation_method = validationStrategy.value;
  }

  currentMetrics.samplesPerSec = Math.floor(800 + Math.random() * 400);

  // Update chart with new data
  const isClassification = metricProblemType.includes("classification");
  if (isClassification) {
    const trainScore = currentMetrics.train_accuracy || 0;
    const testScore = currentMetrics.test_accuracy || 0;
    updateChart(currentEpoch.value, trainScore, testScore);
  } else {
    const trainScore = currentMetrics.train_r2 || 0;
    const testScore = currentMetrics.test_r2 || 0;
    updateChart(currentEpoch.value, trainScore, testScore);
  }

  console.log("🎯 Metrics updated successfully:", {
    problemType: metricProblemType,
    test_accuracy: currentMetrics.test_accuracy,
    test_r2: currentMetrics.test_r2,
    test_mse: currentMetrics.test_mse,
    test_f1: currentMetrics.test_f1,
  });
};

// ===== PROGRESS SIMULATION FUNCTIONS =====

const simulateProgress = (target, speed = 1, onComplete = null) => {
  targetProgress.value = target;
  
  // Clear existing simulator
  if (progressSimulator) {
    clearInterval(progressSimulator);
  }
  
  // Don't simulate if already at or past target
  if (trainingProgress.value >= target) {
    trainingProgress.value = target;
    if (onComplete) onComplete();
    return;
  }
  
  // Gradually increment progress
  progressSimulator = setInterval(() => {
    if (trainingProgress.value < targetProgress.value) {
      // Slower increment as we approach target (more realistic)
      const remaining = targetProgress.value - trainingProgress.value;
      const increment = Math.max(0.3, Math.min(remaining / 10, 1.5)) * speed;
      
      trainingProgress.value = Math.min(
        trainingProgress.value + increment,
        targetProgress.value
      );
    } else {
      clearInterval(progressSimulator);
      progressSimulator = null;
      
      // Execute callback when animation completes
      if (onComplete) {
        onComplete();
      }
    }
  }, 150); // Update every 150ms for smooth animation
};

const getTrainingMessage = () => {
  return 'Training in progress...';
};

// ===== NEW: Configuration Phase Functions =====


// ===== NEW: Hyperparameter Configuration Functions =====
const getKeyParameters = (algorithmName) => {
  if (!algorithmName) return [];
  
  const parameterSets = {
    "Random Forest": [
      {
        name: "Tree Configuration",
        icon: "🌲",
        params: [
          {
            name: "n_estimators",
            label: "Number of Trees",
            type: "slider",
            min: 10,
            max: 500,
            step: 10,
            default: 100,
            impact: "high",
            description: "More trees generally improve performance but increase training time.",
          },
          {
            name: "max_depth",
            label: "Maximum Tree Depth",
            type: "slider",
            min: 1,
            max: 30,
            step: 1,
            default: 10,
            impact: "high",
            description: "Controls tree complexity. Deeper trees can capture more patterns but may overfit.",
          },
          {
            name: "max_features",
            label: "Max Features per Split",
            type: "select",
            options: [
              { value: "sqrt", label: "sqrt (recommended)" },
              { value: "log2", label: "log2" },
              { value: null, label: "All features" }
            ],
            default: "sqrt",
            impact: "high",
            description: "Number of features considered at each split."
          },
          {
            name: "min_samples_split",
            label: "Min Samples to Split",
            type: "slider",
            min: 2,
            max: 20,
            step: 1,
            default: 2,
            impact: "medium",
            description: "Minimum samples required to split an internal node.",
          },
          {
            name: "min_samples_leaf",
            label: "Min Samples per Leaf",
            type: "slider",
            min: 1,
            max: 10,
            step: 1,
            default: 1,
            impact: "medium",
            description: "Minimum samples required at leaf node.",
          },
          {
            name: "bootstrap",
            label: "Bootstrap Sampling",
            type: "checkbox",
            default: true,
            impact: "low",
            description: "Use bootstrap samples when building trees."
          },
        ],
      },
    ],

    "XGBoost": [
      {
        name: "Boosting Configuration",
        icon: "🚀",
        params: [
          {
            name: "n_estimators",
            label: "Number of Estimators",
            type: "slider",
            min: 50,
            max: 1000,
            step: 50,
            default: 100,
            impact: "high",
            description: "Number of boosting rounds.",
          },
          {
            name: "learning_rate",
            label: "Learning Rate",
            type: "slider",
            min: 0.01,
            max: 0.3,
            step: 0.01,
            default: 0.1,
            impact: "high",
            description: "Step size shrinkage used in updates.",
          },
          {
            name: "max_depth",
            label: "Maximum Tree Depth",
            type: "slider",
            min: 3,
            max: 15,
            step: 1,
            default: 6,
            impact: "high",
            description: "Maximum depth of trees.",
          },
          {
            name: "subsample",
            label: "Subsample Ratio",
            type: "slider",
            min: 0.5,
            max: 1.0,
            step: 0.1,
            default: 1.0,
            impact: "medium",
            description: "Subsample ratio of training instances.",
          },
          {
            name: "reg_lambda",
            label: "L2 Regularization (Lambda)",
            type: "slider",
            min: 0,
            max: 10,
            step: 0.1,
            default: 1.0,
            impact: "medium",
            description: "Controls model complexity using L2 regularization."
          },
          {
            name: "reg_alpha",
            label: "L1 Regularization (Alpha)",
            type: "slider",
            min: 0,
            max: 10,
            step: 0.1,
            default: 0.0,
            impact: "medium",
            description: "Encourages sparsity in features."
          }
        ],
      },
    ],

    "Logistic Regression": [
      {
        name: "Regularization",
        icon: "📈",
        params: [
          {
            name: "C",
            label: "Regularization Strength (Inverse)",
            type: "slider",
            min: 0.001,
            max: 100,
            step: 0.001,
            default: 1.0,
            impact: "high",
            description: "Inverse of regularization strength. Smaller values = stronger regularization.",
          },
          {
            name: "solver",
            label: "Optimization Solver",
            type: "select",
            options: [
              { value: "lbfgs", label: "LBFGS (default, fast)" },
              { value: "liblinear", label: "Liblinear (small datasets)" },
              { value: "saga", label: "SAGA (supports L1 & ElasticNet)" }
            ],
            default: "lbfgs",
            impact: "high",
            description: "Solver determines which penalties are supported and affects convergence speed."
          },
          {
            name: "penalty",
            label: "Penalty Type",
            type: "select",
            options: [
              { value: "l2", label: "L2 (Ridge)" },
              { value: "l1", label: "L1 (Lasso)" },
              { value: "elasticnet", label: "Elastic Net" },
            ],
            default: "l2",
            impact: "medium",
            description: "Type of penalty to apply.",
          },
          {
            name: "l1_ratio",
            label: "Elastic Net L1 Ratio",
            type: "slider",
            min: 0.0,
            max: 1.0,
            step: 0.01,
            default: 0.5,
            impact: "medium",
            description: "The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1.",
            condition: "penalty === 'elasticnet'"
          },
          {
            name: "max_iter",
            label: "Maximum Iterations",
            type: "slider",
            min: 100,
            max: 1000,
            step: 100,
            default: 100,
            impact: "low",
            description: "Maximum iterations for convergence.",
          },
        ],
      },
    ],

    "Linear Regression": [
      {
        name: "Basic Configuration",
        icon: "📉",
        params: [
          {
            name: "fit_intercept",
            label: "Fit Intercept",
            type: "checkbox",
            default: true,
            impact: "low",
            description: "Whether to calculate the intercept.",
          },
          {
            name: "positive",
            label: "Positive Coefficients Only",
            type: "checkbox",
            default: false,
            impact: "low",
            description: "Forces coefficients to be non-negative (useful in some domains)."
          },
        ],
      },
    ],

    "Support Vector Machine": [
      {
        name: "SVM Configuration",
        icon: "⚡",
        params: [
          {
            name: "C",
            label: "Regularization Parameter",
            type: "slider",
            min: 0.1,
            max: 100,
            step: 0.1,
            default: 1.0,
            impact: "high",
            description: "Regularization parameter. Higher values mean less regularization.",
          },
          {
            name: "kernel",
            label: "Kernel Type",
            type: "select",
            options: [
              { value: "rbf", label: "RBF (Gaussian)" },
              { value: "linear", label: "Linear" },
              { value: "poly", label: "Polynomial" },
              { value: "sigmoid", label: "Sigmoid" },
            ],
            default: "rbf",
            impact: "high",
            description: "Kernel function to use.",
          },
          {
            name: "degree",
            label: "Polynomial Degree",
            type: "slider",
            min: 1,
            max: 10,
            step: 1,
            default: 3,
            impact: "medium",
            description: "Degree of the polynomial kernel function ('poly').",
            condition: "kernel === 'poly'"
          },
          {
            name: "gamma",
            label: "Gamma (Kernel Coefficient)",
            type: "select",
            options: [
              { value: "scale", label: "Scale (1 / (n_features * X.var()))" },
              { value: "auto", label: "Auto (1 / n_features)" },
            ],
            default: "scale",
            impact: "medium",
            description: "Kernel coefficient for RBF, poly, and sigmoid.",
          },
        ],
      },
    ],

    "K-Nearest Neighbors": [
      {
        name: "KNN Configuration",
        icon: "🎲",
        params: [
          {
            name: "n_neighbors",
            label: "Number of Neighbors",
            type: "slider",
            min: 1,
            max: 50,
            step: 1,
            default: 5,
            impact: "high",
            description: "Number of neighbors to consider.",
          },
          {
            name: "weights",
            label: "Weight Function",
            type: "select",
            options: [
              { value: "uniform", label: "Uniform" },
              { value: "distance", label: "Distance" },
            ],
            default: "uniform",
            impact: "medium",
            description: "Weight function used in prediction.",
          },
          {
            name: "metric",
            label: "Distance Metric",
            type: "select",
            options: [
              { value: "euclidean", label: "Euclidean" },
              { value: "manhattan", label: "Manhattan" },
              { value: "minkowski", label: "Minkowski" },
            ],
            default: "euclidean",
            impact: "medium",
            description: "Distance metric for finding neighbors.",
          },
          {
            name: "algorithm",
            label: "Neighbor Search Algorithm",
            type: "select",
            options: [
              { value: "auto", label: "Auto" },
              { value: "ball_tree", label: "Ball Tree" },
              { value: "kd_tree", label: "KD Tree" },
              { value: "brute", label: "Brute Force" }
            ],
            default: "auto",
            impact: "low",
            description: "Algorithm used to compute nearest neighbors."
          }
        ],
      },
    ],

    "Decision Tree": [
      {
        name: "Tree Configuration",
        icon: "🌳",
        params: [
          {
            name: "max_depth",
            label: "Maximum Depth",
            type: "slider",
            min: 1,
            max: 30,
            step: 1,
            default: 10,
            impact: "high",
            description: "Maximum depth of the tree.",
          },
          {
            name: "min_samples_split",
            label: "Min Samples to Split",
            type: "slider",
            min: 2,
            max: 20,
            step: 1,
            default: 2,
            impact: "high",
            description: "Minimum samples required to split.",
          },
          {
            name: "criterion",
            label: "Split Criterion",
            type: "select",
            options: [
              { value: "gini", label: "Gini Impurity" },
              { value: "entropy", label: "Information Gain" },
            ],
            default: "gini",
            impact: "medium",
            description: "Function to measure split quality.",
          },
        ],
      },
    ],

    "Support Vector Regression": [
      {
        name: "SVR Configuration",
        icon: "📊",
        params: [
          {
            name: "kernel",
            label: "Kernel Type",
            type: "select",
            options: [
              { value: "rbf", label: "RBF (Radial Basis Function)" },
              { value: "linear", label: "Linear" },
              { value: "poly", label: "Polynomial" },
              { value: "sigmoid", label: "Sigmoid" },
            ],
            default: "rbf",
            impact: "high",
            description: "Kernel type for non-linear transformation.",
          },
          {
            name: "degree",
            label: "Polynomial Degree",
            type: "slider",
            min: 1,
            max: 10,
            step: 1,
            default: 3,
            impact: "medium",
            description: "Degree of the polynomial kernel function ('poly').",
            condition: "kernel === 'poly'"
          },
          {
            name: "C",
            label: "Regularization Parameter",
            type: "slider",
            min: 0.001,
            max: 100,
            step: 0.1,
            default: 1.0,
            impact: "high",
            description: "Trade-off between margin and training errors.",
          },
          {
            name: "epsilon",
            label: "Epsilon (ε-tube width)",
            type: "slider",
            min: 0.001,
            max: 1.0,
            step: 0.01,
            default: 0.1,
            impact: "medium",
            description: "Width of insensitive zone. No penalty for errors within this range.",
          },
          {
            name: "gamma",
            label: "Gamma (Kernel Coefficient)",
            type: "select",
            options: [
              { value: "scale", label: "Scale (1 / (n_features * X.var()))" },
              { value: "auto", label: "Auto (1 / n_features)" },
            ],
            default: "scale",
            impact: "medium",
            description: "Kernel coefficient for RBF, poly, and sigmoid.",
          },
        ],
      },
    ],

    "Naive Bayes": [
      {
        name: "Naive Bayes Configuration",
        icon: "🎯",
        params: [
          {
            name: "variant",
            label: "Naive Bayes Variant",
            type: "select",
            options: [
              { value: "gaussian", label: "Gaussian (Continuous features)" },
              { value: "bernoulli", label: "Bernoulli (Binary features)" },
            ],
            default: "gaussian",
            impact: "high",
            description: "Variant based on feature distribution.",
          },
          {
            name: "alpha",
            label: "Smoothing Parameter (α)",
            type: "slider",
            min: 0.0,
            max: 10.0,
            step: 0.1,
            default: 1.0,
            impact: "medium",
            description: "Laplace/Lidstone smoothing (0 = no smoothing). For multinomial/bernoulli only.",
            condition: "variant !== 'gaussian'"
          },
          {
            name: "var_smoothing",
            label: "Variance Smoothing",
            type: "slider",
            min: 1e-11,
            max: 1e-5,
            step: 1e-11,
            default: 1e-9,
            impact: "low",
            description: "Portion of largest variance added for stability. For Gaussian only.",
            condition: "variant === 'gaussian'"
          },
          {
            name: "fit_prior",
            label: "Learn Class Priors",
            type: "checkbox",
            default: true,
            impact: "low",
            description: "Learn class prior probabilities from data.",
          },
        ],
      },
    ],

    "Ridge Regression": [
      {
        name: "Ridge Configuration",
        icon: "📐",
        params: [
          {
            name: "alpha",
            label: "Regularization Strength (α)",
            type: "slider",
            min: 0.001,
            max: 100.0,
            step: 0.1,
            default: 1.0,
            impact: "high",
            description: "Higher values = more regularization (smaller coefficients).",
          },
          {
            name: "solver",
            label: "Optimization Solver",
            type: "select",
            options: [
              { value: "auto", label: "Auto (chooses best)" },
              { value: "svd", label: "SVD (Singular Value Decomposition)" },
              { value: "cholesky", label: "Cholesky (Fast)" },
              { value: "lsqr", label: "LSQR (Sparse data)" },
              { value: "saga", label: "SAGA (Large datasets)" },
            ],
            default: "auto",
            impact: "medium",
            description: "Algorithm for optimization.",
          },
          {
            name: "fit_intercept",
            label: "Fit Intercept",
            type: "checkbox",
            default: true,
            impact: "low",
            description: "Calculate intercept (recommended).",
          },
        ],
      },
    ],

    "Lasso Regression": [
      {
        name: "Lasso Configuration",
        icon: "🎯",
        params: [
          {
            name: "alpha",
            label: "Regularization Strength (α)",
            type: "slider",
            min: 0.001,
            max: 100.0,
            step: 0.1,
            default: 1.0,
            impact: "high",
            description: "Higher values = more feature elimination (stronger L1 penalty).",
          },
          {
            name: "selection",
            label: "Feature Selection Method",
            type: "select",
            options: [
              { value: "cyclic", label: "Cyclic (Default)" },
              { value: "random", label: "Random (Faster convergence)" },
            ],
            default: "cyclic",
            impact: "medium",
            description: "Method for coordinate descent updates.",
          },
          {
            name: "fit_intercept",
            label: "Fit Intercept",
            type: "checkbox",
            default: true,
            impact: "low",
            description: "Calculate intercept.",
          },
        ],
      },
    ],
  };

  return parameterSets[algorithmName] || [];
};

const shouldShowParam = (param) => {
  if (!param || !param.condition) return true;
  
  try {
    // Simple expression evaluator for conditions like "penalty === 'elasticnet'"
    const context = hyperparameters;
    
    // Support "key === 'value'" patterns
    const matchEq = param.condition.match(/(\w+)\s*===\s*'([^']+)'/);
    if (matchEq) {
      const [_, key, value] = matchEq;
      return context[key] === value;
    }

    // Support "key !== 'value'" patterns
    const matchNotEq = param.condition.match(/(\w+)\s*!==\s*'([^']+)'/);
    if (matchNotEq) {
      const [_, key, value] = matchNotEq;
      return context[key] !== value;
    }
    
    // Fallback or more complex logic if needed
    return true;
  } catch (e) {
    console.warn("Condition evaluation failed:", e);
    return true;
  }
};

const formatParameterValue = (paramName, value) => {
  if (paramName === "learning_rate" || paramName === "C") {
    return parseFloat(value).toFixed(3);
  }
  return value;
};

const initializeHyperparameters = () => {
  if (!modelConfig.value?.algorithm?.name) return;
  
  const params = getKeyParameters(modelConfig.value.algorithm.name);
  params.forEach((group) => {
    group.params.forEach((param) => {
      if (!hyperparameters[param.name]) {
        hyperparameters[param.name] = param.default;
      }
    });
  });
  
  console.log('✅ Hyperparameters initialized:', hyperparameters);
};

const resetHyperparametersToDefault = () => {
  if (!modelConfig.value?.algorithm?.name) {
    console.warn('⚠️ Cannot reset: No algorithm selected');
    return;
  }
  
  console.log('🔄 Resetting hyperparameters to default values...');
  
  const params = getKeyParameters(modelConfig.value.algorithm.name);
  params.forEach((group) => {
    group.params.forEach((param) => {
      hyperparameters[param.name] = param.default;
    });
  });
  
  addLog('info', `Hyperparameters reset to default values for ${modelConfig.value.algorithm.name}`);
  console.log('✅ Hyperparameters reset to defaults:', hyperparameters);
};

// Control Functions
const pauseTraining = () => {
  isPaused.value = true;
  addLog("warning", "Training paused");
};

const resumeTraining = () => {
  isPaused.value = false;
  addLog("info", "Training resumed");
};

const stopTraining = () => {
  if (!isTraining.value) return;

  console.log('🛑 Requesting training stop...');
  addLog("warning", "Requesting training stop...");

  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify({ action: "stop" }));
    console.log('📤 Sent stop signal');
  } else {
    // Fallback if socket is already closed/unstable
    isTraining.value = false;
    isPaused.value = false;
    if (timeInterval) {
      clearInterval(timeInterval);
      timeInterval = null;
    }
    trainingPhase.value = 'configuration';
    addLog("error", "WebSocket not available. Local state reset.");
  }
};

const viewDetailedResults = () => {
  if (!lastTrainedModelId.value) {
    addLog('error', '❌ Model ID not found. Please retrain or refresh.');
    return;
  }
  
  // Save necessary context for the visualization page
  localStorage.setItem('last_model_id', lastTrainedModelId.value);
  localStorage.setItem('last_dataset_id', datasetId.value);
  
  // Navigate to visualizer
  router.push({
    name: 'model-visualization',
    params: { modelId: lastTrainedModelId.value }
  });
};

const downloadModel = async () => {
  if (!lastTrainedModelId.value) {
    addLog('error', '❌ Model ID not found. Cannot download.');
    return;
  }

  addLog('info', '📂 Preparing model for download...');
  
  try {
    const response = await fetch(`http://localhost:8000/api/models/${lastTrainedModelId.value}/download`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Failed to download model: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${lastTrainedModelId.value}.joblib`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    addLog('success', '✅ Model downloaded successfully');
  } catch (error) {
    console.error('Download error:', error);
    addLog('error', `❌ Download failed: ${error.message}`);
  }
};

const scrollToConfiguration = () => {
  // Scroll to the top where configuration sections are located
  addLog("info", "Navigating to configuration sections...");
  
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
};

const unlockConfiguration = () => {
  // Return to configuration phase
  trainingPhase.value = 'configuration';
  
  // Reset all metrics to zero
  Object.keys(currentMetrics).forEach(key => {
    if (Array.isArray(currentMetrics[key])) {
      currentMetrics[key] = [];
    } else if (key === 'validation_method') {
      currentMetrics[key] = 'simple';
    } else if (key === 'best_params') {
      currentMetrics[key] = null;
    } else {
      currentMetrics[key] = 0;
    }
  });
  
  // Reset training state
  isCompleted.value = false;
  trainingProgress.value = 0;
  currentEpoch.value = 0;
  
  addLog("info", "Configuration unlocked. Metrics reset. Ready to retrain.");
  
  // Scroll to configuration section
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
};

const retrainModel = () => {
  // Save current training results to history
  if (isCompleted.value) {
    trainingHistory.value.push({
      timestamp: Date.now(),
      algorithm: modelConfig.value.algorithm.name,
      hyperparameters: { ...hyperparameters },
      validationStrategy: validationStrategy.value,
      metrics: { ...currentMetrics },
      trainingTime: elapsedTime.value
    });
  }

  // Reset training state but keep configuration
  isTraining.value = false;
  isPaused.value = false;
  isCompleted.value = false;
  trainingProgress.value = 0;
  currentEpoch.value = 0;
  trainingPhase.value = 'configuration';
  
  // Reset metrics
  Object.keys(currentMetrics).forEach(key => {
    if (Array.isArray(currentMetrics[key])) {
      currentMetrics[key] = [];
    } else if (key === 'validation_method') {
      currentMetrics[key] = 'simple';
    } else if (key === 'best_params') {
      currentMetrics[key] = null;
    } else {
      currentMetrics[key] = 0;
    }
  });

  // Clear chart
  destroyChart();
  
  // Close websocket if open
  if (websocket) {
    websocket.close();
    websocket = null;
  }

  if (timeInterval) {
    clearInterval(timeInterval);
    timeInterval = null;
  }

  addLog("info", "Ready to retrain with new configuration");
};

// ===== TRAINING FUNCTIONS =====

const proceedToTraining = async () => {
  console.log('🚀 Proceeding to training phase...');
  
  // Validate configuration
  if (!modelConfig.value?.algorithm) {
    addLog('error', 'No algorithm selected');
    return;
  }
  
  if (!datasetId.value) {
    addLog('error', 'No dataset ID found');
    return;
  }
  
  // Transition to training phase
  trainingPhase.value = 'training';
  
  // Scroll to training section
  await nextTick();
  const trainingSection = document.getElementById('training-section');
  if (trainingSection) {
    trainingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  
  addLog('info', 'Configuration locked. Ready to start training.');
  
  // Auto-start training after a brief delay
  setTimeout(() => {
    startTraining();
  }, 500);
};

const startTraining = async () => {
  if (isTraining.value) {
    console.warn('Training already in progress');
    return;
  }

  console.log('🎯 Starting training...');
  isTraining.value = true;
  isCompleted.value = false;
  trainingProgress.value = 0;
  currentEpoch.value = 0;
  elapsedTime.value = 0;

  // Reset training stages
  trainingStages.value.forEach(stage => {
    stage.status = 'pending';
  });

  addLog('info', `Starting ${modelConfig.value.algorithm.name} training...`);

  // Start elapsed time counter
  timeInterval = setInterval(() => {
    elapsedTime.value++;
  }, 1000);

  try {
    // Prepare training configuration
    const storedTarget = localStorage.getItem('selectedTarget');
    let targetName = "target";
    
    if (storedTarget) {
      try {
        const targetObj = JSON.parse(storedTarget);
        targetName = targetObj.name || targetObj; 
      } catch (e) {
        targetName = storedTarget; // Fallback if not JSON
      }
    }
    
    const trainingConfig = {
      dataset_id: datasetId.value,
      target_column: targetName,
      algorithm_name: modelConfig.value.algorithm.name,
      test_size: 1 - splitRatio.value,
      validation_method: validationStrategy.value,
      cv_folds: validationStrategy.value === 'kfold_cv' ? cvFolds.value : undefined,
      grid_search_cv_folds: validationStrategy.value === 'grid_search' ? gridSearchCVFolds.value : undefined,
      grid_density: validationStrategy.value === 'grid_search' ? gridDensity.value : undefined,
      random_search_cv_folds: validationStrategy.value === 'randomized_search' ? randomSearchCVFolds.value : undefined,
      random_search_iterations: validationStrategy.value === 'randomized_search' ? randomSearchIterations.value : undefined,
      hyperparameters: { ...hyperparameters }
    };

    console.log('📤 Training config:', trainingConfig);

    // Connect to WebSocket
    const wsUrl = `ws://localhost:8000/ws/train-model`;
    console.log('🔌 Connecting to:', wsUrl);

    websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('✅ WebSocket connected');
      addLog('success', 'Connected to training server');
      
      // Send training configuration
      websocket.send(JSON.stringify(trainingConfig));
      console.log('📤 Sent training configuration');
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📥 Received:', data);

        handleTrainingMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    websocket.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      addLog('error', 'Connection error occurred');
      isTraining.value = false;
      
      if (timeInterval) {
        clearInterval(timeInterval);
        timeInterval = null;
      }
    };

    websocket.onclose = () => {
      console.log('🔌 WebSocket closed');
      
      if (!isCompleted.value && isTraining.value) {
        addLog('warning', 'Connection closed unexpectedly');
        isTraining.value = false;
      }
      
      if (timeInterval) {
        clearInterval(timeInterval);
        timeInterval = null;
      }
    };

  } catch (error) {
    console.error('❌ Training error:', error);
    addLog('error', `Training failed: ${error.message}`);
    isTraining.value = false;
    
    if (timeInterval) {
      clearInterval(timeInterval);
      timeInterval = null;
    }
  }
};

const handleTrainingMessage = (data) => {
  const status = data.status;
  const message = data.message;

  // Update stage status based on message
  if (status === 'started' || status === 'data_loaded') {
    trainingStages.value[0].status = 'active';
    simulateProgress(15, 0.5); // Slow start to 15%
  } else if (status === 'preprocessing' || status === 'model_init' || status === 'model_ready') {
    trainingStages.value[0].status = 'active';
    simulateProgress(30, 0.8); // Gradually to 30%
  } else if (status === 'training') {
    trainingStages.value[0].status = 'completed';
    trainingStages.value[1].status = 'active';
    
    // Simulate progress based on validation strategy
    if (validationStrategy.value === 'kfold_cv') {
      simulateProgress(85, 0.6); // Slower for K-Fold (multiple folds)
    } else if (validationStrategy.value === 'grid_search') {
      simulateProgress(80, 0.4); // Even slower for Grid Search (many combinations)
    } else if (validationStrategy.value === 'randomized_search') {
      simulateProgress(82, 0.5); // Moderate for Randomized Search
    } else {
      simulateProgress(70, 1); // Moderate speed for simple validation
    }
    
    currentStageTitle.value = 'Training Model';
    currentStageMessage.value = getTrainingMessage(); // Dynamic message with fold info
  } else if (status === 'training_complete') {
    trainingStages.value[1].status = 'completed';
    simulateProgress(88, 1.2); // Quick jump to 88%
  } else if (status === 'evaluating') {
    trainingStages.value[2].status = 'active';
    simulateProgress(95, 1.5); // Faster near end
    currentStageTitle.value = 'Evaluating Performance';
    currentStageMessage.value = 'Calculating metrics...';
  } else if (status === 'saving') {
    trainingStages.value[2].status = 'completed';
    trainingStages.value[3].status = 'active';
    simulateProgress(98, 2); // Very fast to 98%
  } else if (status === 'completed') {
    console.log('🎉 Training completed! Full data received:', data);
    console.log('🔍 Checking final_metrics:', data.final_metrics);
    
    trainingStages.value[3].status = 'completed';
    
    // Animate to 100% first, then show completion state and metrics
    simulateProgress(100, 2.5, () => {
      // This callback runs AFTER animation reaches 100%
      isTraining.value = false;
      isCompleted.value = true;
      lastTrainedModelId.value = data.model_id; // Store model_id for visualization
      currentStageTitle.value = 'Training Complete!';
      currentStageMessage.value = 'Model trained successfully';

      // Note: Configuration inputs will auto-unlock because isTraining = false
      // We keep trainingPhase = 'training' to show the metrics section

      // Update metrics with final results AFTER animation completes
      if (data.final_metrics) {
        console.log('📊 Final metrics received:', data.final_metrics);
        updateMetrics(data.final_metrics);
        
        // Update global pipeline state for router guards
        const appState = JSON.parse(localStorage.getItem('datasage_pipeline_state') || '{}');
        appState.trainedModel = true;
        appState.modelTrained = true;
        localStorage.setItem('datasage_pipeline_state', JSON.stringify(appState));
      } else {
        console.error('❌ No final_metrics in completion data!');
      }
    });
    
    addLog('error', message || 'Training failed');
  } else if (status === 'stopped') {
    isTraining.value = false;
    isCompleted.value = false;
    
    if (timeInterval) {
      clearInterval(timeInterval);
      timeInterval = null;
    }
    
    if (progressSimulator) {
      clearInterval(progressSimulator);
      progressSimulator = null;
    }
    
    trainingPhase.value = 'configuration';
    addLog("info", message || "⏹️ Training stopped by user");
    
    // Scroll back to configuration section
    nextTick(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Add log message
  if (message) {
    const logType = status === 'failed' ? 'error' : 
                    status === 'completed' ? 'success' : 
                    status.includes('warning') ? 'warning' : 'info';
    addLog(logType, message);
  }
};

// ===== HELPER FUNCTIONS =====

const addLog = (type, message) => {
  trainingLogs.value.push({
    type,
    message,
    timestamp: Date.now()
  });
  
  // Auto-scroll logs to bottom
  nextTick(() => {
    if (logsContainer.value) {
      logsContainer.value.scrollTop = logsContainer.value.scrollHeight;
    }
  });
};

const clearLogs = () => {
  trainingLogs.value = [];
};

const updateChart = (epoch, trainScore, testScore) => {
  if (!chartContainer.value) return;
  
  // Initialize chart if not exists
  if (!trainingChart) {
    const ctx = chartContainer.value.getContext('2d');
    trainingChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Train R²',
            data: [],
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4
          },
          {
            label: 'Test R²',
            data: [],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#ffffff' }
          }
        },
        scales: {
          x: {
            ticks: { color: '#b3b3d1' },
            grid: { color: 'rgba(102, 126, 234, 0.1)' }
          },
          y: {
            ticks: { color: '#b3b3d1' },
            grid: { color: 'rgba(102, 126, 234, 0.1)' }
          }
        }
      }
    });
  }
  
  // Update chart data
  trainingChart.data.labels.push(epoch);
  trainingChart.data.datasets[0].data.push(trainScore);
  trainingChart.data.datasets[1].data.push(testScore);
  trainingChart.update();
};

const destroyChart = () => {
  if (trainingChart) {
    trainingChart.destroy();
    trainingChart = null;
  }
};

const goBack = () => {
  // Clean up before leaving
  if (websocket) {
    websocket.close();
    websocket = null;
  }
  
  if (timeInterval) {
    clearInterval(timeInterval);
    timeInterval = null;
  }
  
  router.push('/algorithm-select');
};



const loadConfiguration = async () => {
  try {
    // 1. Get Dataset ID (Priority: URL > Store > LocalStorage Legacy)
    const queryDatasetId = route.query.datasetId || route.query.backendDatasetId;
    
    if (queryDatasetId) {
      datasetId.value = queryDatasetId;
    } else if (storeDatasetId.value) {
      datasetId.value = storeDatasetId.value;
    } else {
      // Fallback
      datasetId.value = localStorage.getItem("datasetId") || localStorage.getItem("backendDatasetId");
    }

    if (!datasetId.value) {
      addLog("error", "No Dataset ID found. Please go back and select a dataset.");
    }

    // 2. Algorithm Configuration
    if (storeAlgorithm.value) {
      modelConfig.value = {
        algorithm: storeAlgorithm.value
      };
    } else {
      // Fallback
      const storedAlgo = localStorage.getItem("selectedAlgorithm");
      if (storedAlgo) {
         modelConfig.value = { algorithm: JSON.parse(storedAlgo) };
         // Sync back to store
         experimentStore.setAlgorithm(modelConfig.value.algorithm);
      } else {
         modelConfig.value = { algorithm: { name: "Random Forest", type: "ensemble" } }; // Default
      }
    }

    // 3. Problem Type
    if (storeProblemType.value && storeProblemType.value.type) {
      problemType.value = storeProblemType.value.type;
      modelConfig.value.problemType = storeProblemType.value;
    } else {
       const storedPT = localStorage.getItem("problemType");
       if (storedPT) {
         const pt = JSON.parse(storedPT);
         problemType.value = pt.type || "classification";
         modelConfig.value.problemType = pt;
       }
    }

    // 4. Target Column
    if (storeTargetColumn.value) {
       modelConfig.value.target = storeTargetColumn.value;
    } else {
       const storedTarget = localStorage.getItem("selectedTarget");
       if (storedTarget) {
          modelConfig.value.target = JSON.parse(storedTarget);
       }
    }
    
    // 5. Statistics
    if (datasetMetadata.value) {
      datasetStats.value = {
        rows: datasetMetadata.value.totalRows || 0,
        features: datasetMetadata.value.columns || 0
      };
      modelConfig.value.datasetStats = datasetStats.value;
    } else {
       const storedStats = localStorage.getItem("datasetStats");
       if (storedStats) {
         datasetStats.value = JSON.parse(storedStats);
         modelConfig.value.datasetStats = datasetStats.value;
       }
    }
    
    // Initialize hyperparameters after loading config
    initializeHyperparameters();

    // Update Store with any resolved values if they were missing
    if (!storeDatasetId.value && datasetId.value) experimentStore.setDatasetId(datasetId.value);

  } catch (error) {
    console.error("Failed to load configuration:", error);
    addLog("error", `Failed to load configuration: ${error.message}`);
  }
};



const exportLogs = () => {
  const logData = trainingLogs.value
    .map(
      (log) =>
        `${formatLogTime(log.timestamp)} [${log.type.toUpperCase()}] ${
          log.message
        }`
    )
    .join("\n");

  const blob = new Blob([logData], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `training-logs-${Date.now()}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  addLog("info", "Training logs exported");
};

// Initialization
const initializeTrainingEnvironment = async () => {
  const steps = [
    "Loading configuration...",
    "Validating dataset...",
    "Preparing environment...",
    "Initializing parameters...",
    "Ready to train!",
  ];

  for (let i = 0; i < steps.length; i++) {
    initializationMessage.value = steps[i];
    const targetProgress = ((i + 1) / steps.length) * 100;

    while (initializationProgress.value < targetProgress) {
      initializationProgress.value += 5;
      await new Promise((resolve) => setTimeout(resolve, 50));
    }

    await new Promise((resolve) => setTimeout(resolve, 300));
  }

  isInitializing.value = false;
};



// Lifecycle
onMounted(async () => {
  console.log("Initializing Model Training...");

  await loadConfiguration();  
  
  // Proactively validate dataset with backend to trigger re-hydration if needed
  if (datasetId.value) {
    try {
      console.log(`🔍 Proactively validating dataset ${datasetId.value}...`);
      const response = await authenticatedGet(`http://localhost:8000/api/datasets/${datasetId.value}`);
      if (response.ok) {
        console.log("✅ Dataset validated and hydrated in backend memory");
      } else {
        console.warn("⚠️ Dataset validation failed on backend");
      }
    } catch (err) {
      console.warn("⚠️ Error pinging backend for dataset validation:", err);
    }
  }

  await initializeTrainingEnvironment();
  
  // Initialize hyperparameters with defaults
  initializeHyperparameters();
});

onUnmounted(() => {
  if (websocket) {
    websocket.close();
  }
  if (timeInterval) {
    clearInterval(timeInterval);
  }
  if (progressSimulator) {
    clearInterval(progressSimulator);
  }
  destroyChart();
});


</script>

<style scoped>
.model-training {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

/* Header */
.training-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
  transform: translateX(-2px);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #b3b3d1;
  font-size: 0.875rem;
}

.breadcrumb .current {
  color: #667eea;
  font-weight: 600;
}

.header-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(26, 26, 46, 0.8);
  border-radius: 20px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 2s infinite;
}

.status-indicator.connected .status-dot {
  background: #10b981;
}

.status-text {
  font-size: 0.75rem;
  color: #b3b3d1;
}

/* Hero Section */
.hero-section {
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.1),
    rgba(118, 75, 162, 0.1)
  );
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-section p {
  font-size: 1.25rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
}

.training-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  font-size: 1rem;
  flex-wrap: wrap;
}

.summary-item {
  color: #ffffff;
}

.summary-divider {
  color: #667eea;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

/* Training Controls */
.training-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.control-btn.start {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.control-btn.start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.control-btn.pause {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.control-btn.resume {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.control-btn.stop {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.control-btn.modify {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.control-btn.modify:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Progress Dashboard */
.progress-dashboard {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.progress-main {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 3rem;
  align-items: center;
  margin-bottom: 2rem;
}

.progress-info h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: #667eea;
}

.progress-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.detail-label {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.detail-value {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
}

.progress-visual {
  position: relative;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring-circle.foreground {
  transition: stroke-dashoffset 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-percent {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  color: #667eea;
  line-height: 1;
}

.progress-label {
  display: block;
  font-size: 0.75rem;
  color: #b3b3d1;
  margin-top: 0.25rem;
}

/* Stage Progress */
.stage-progress {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.stage-item.active {
  opacity: 1;
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
}

.stage-item.completed {
  opacity: 0.8;
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}

.stage-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 50%;
  flex-shrink: 0;
}

.stage-item.active .stage-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stage-item.completed .stage-icon {
  background: linear-gradient(135deg, #10b981, #059669);
}

.stage-info {
  flex: 1;
  min-width: 0;
}

.stage-name {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
  font-size: 0.875rem;
}

.stage-bar {
  height: 4px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.5s ease;
  border-radius: 2px;
}

/* Metrics and Charts Grid */
.metrics-charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.metrics-section,
.charts-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.metric-card.primary {
  border-color: rgba(102, 126, 234, 0.4);
}

.metric-card.success {
  border-color: rgba(16, 185, 129, 0.4);
}

.metric-card.info {
  border-color: rgba(59, 130, 246, 0.4);
}

.metric-card.warning {
  border-color: rgba(245, 158, 11, 0.4);
}

.metric-icon {
  font-size: 1.75rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 10px;
  flex-shrink: 0;
}

.metric-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.1;
  margin-bottom: 0.25rem;
  text-align: left;
}

.metric-label {
  font-size: 0.85rem;
  color: #b3b3d1;
  margin-bottom: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  text-align: left;
}

.metric-change {
  font-size: 0.75rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.metric-change.neutral {
  color: #b3b3d1;
}

/* ===== ENHANCED METRIC CARD STYLES ===== */

/* Animated metric cards with glassmorphism */
.metric-card.animated {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(26, 26, 46, 0.6));
  backdrop-filter: blur(20px);
  border: 2px solid transparent;
  flex-direction: column;
  align-items: stretch;
  padding: 1.1rem;
  min-height: 210px;
  max-height: 240px;
  display: flex;
  justify-content: space-between;
}

.metric-card.animated::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 12px;
  padding: 2px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: borderGlow 3s ease-in-out infinite;
  pointer-events: none;
}

@keyframes borderGlow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.live-indicator {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
}

@keyframes pulse {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
  }
  50% { 
    opacity: 0.5; 
    transform: scale(1.3);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.8);
  }
}

/* Train/Test split bars */
.metric-split {
  display: flex;
  flex-direction: row;
  gap: 0.6rem;
  margin: 0.6rem 0 0.5rem 0;
  padding: 0.6rem 0.7rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.split-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  flex: 1;
  align-items: flex-start;
}

.split-label {
  font-size: 0.65rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-weight: 700;
  margin-bottom: 0.1rem;
}

.split-value {
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0;
  line-height: 1;
}



/* Metric trend indicators */
.metric-trend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.7rem;
  font-weight: 600;
  margin-top: auto;
  padding: 0.35rem 0.6rem;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.25);
  text-align: center;
}

.metric-trend.improving {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.metric-trend.improving::before {
  content: '↑';
  font-size: 1rem;
  font-weight: bold;
}

.metric-trend.degrading {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.metric-trend.degrading::before {
  content: '↓';
  font-size: 1rem;
  font-weight: bold;
}

.metric-trend.stable {
  color: #b3b3d1;
  background: rgba(179, 179, 209, 0.05);
}

.metric-trend.stable::before {
  content: '→';
  font-size: 1rem;
  font-weight: bold;
}

/* Responsive grid adjustments */
@media (max-width: 1400px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-charts-grid {
    grid-template-columns: 1fr;
  }
}

/* Cross-Validation Results */
.cv-results {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.cv-results h4 {
  margin: 0 0 1rem 0;
  color: #667eea;
  font-size: 1rem;
}

.cv-summary {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.cv-metric {
  color: #ffffff;
  font-weight: 500;
  font-size: 0.875rem;
}

.cv-fold-scores {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.cv-fold {
  font-size: 0.75rem;
  color: #b3b3d1;
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  text-align: center;
}

/* Charts */
.chart-container {
  min-height: 300px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #b3b3d1;
}

.chart-icon {
  margin: 0 auto 1rem;
  opacity: 0.5;
}

/* Logs Section */
.logs-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.log-controls {
  display: flex;
  gap: 1rem;
}

.clear-btn,
.export-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.clear-btn:hover,
.export-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.logs-container {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  padding: 1rem;
  height: 300px;
  overflow-y: auto;
  font-family: "Monaco", "Menlo", monospace;
  font-size: 0.875rem;
}

.log-empty {
  color: #b3b3d1;
  text-align: center;
  padding: 2rem;
  font-style: italic;
}

.log-entry {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.log-entry:last-child {
  border-bottom: none;
}

.log-time {
  color: #b3b3d1;
  font-size: 0.75rem;
  min-width: 80px;
  flex-shrink: 0;
}

.log-message {
  flex: 1;
  word-break: break-word;
}

.log-entry.info .log-message {
  color: #ffffff;
}

.log-entry.success .log-message {
  color: #10b981;
}

.log-entry.warning .log-message {
  color: #f59e0b;
}

.log-entry.error .log-message {
  color: #ef4444;
}

/* Action Section */
.action-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 3rem;
}

.action-content {
  text-align: center;
}

.completion-message {
  margin-bottom: 2rem;
}

.completion-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.completion-message h3 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #10b981;
}

.completion-message p {
  font-size: 1.125rem;
  color: #b3b3d1;
  margin-bottom: 2rem;
}

.training-summary-complete {
  max-width: 500px;
  margin: 0 auto 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-label {
  color: #b3b3d1;
  font-size: 0.875rem;
}

.summary-value {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.action-btn.secondary {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.4);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.action-btn.primary:hover {
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.3);
}

.view-results-btn {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.view-results-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
  border-color: rgba(102, 126, 234, 0.6);
}

.view-results-btn:active {
  transform: translateY(-1px);
}

.view-results-btn .btn-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.view-results-btn .btn-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #ffffff;
}

.view-results-btn .btn-subtitle {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

/* ✅ ADD ALL THESE NEW STYLES AT THE END */

.final-actions-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 0 2rem;
  flex-wrap: wrap;
}

.download-model-btn, .view-results-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.9375rem;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.view-results-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.download-model-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-color: rgba(102, 126, 234, 0.4);
}

.view-results-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.download-model-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
  transform: translateY(-2px);
}

.view-results-btn:active, .download-model-btn:active {
  transform: translateY(0);
}

.view-results-btn span, .download-model-btn span {
  white-space: nowrap;
}

/* Current Stage Banner */
.current-stage-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-radius: 16px;
  border-left: 4px solid #6366f1;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
}

.stage-info-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stage-icon-large {
  font-size: 2.5rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

.stage-text {
  .stage-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.25rem;
  }
  
  .stage-subtitle {
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.7);
  }
}

.stage-progress-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.progress-percentage-large {
  font-size: 2.5rem;
  font-weight: 800;
  color: #6366f1;
  text-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
}

.progress-dots {
  display: flex;
  gap: 0.6rem;
  
  .progress-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    transition: all 0.4s ease;
    
    &.active {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
    }
  }
}

/* Training Metrics Grid */
.training-metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
  }
  
  .metric-icon {
    font-size: 2rem;
  }
  
  .metric-content {
    flex: 1;
    
    .metric-label {
      font-size: 0.85rem;
      color: rgba(255, 255, 255, 0.6);
      margin-bottom: 0.25rem;
    }
    
    .metric-value {
      font-size: 1.1rem;
      font-weight: 600;
      color: #fff;
    }
  }
}

/* Training Stages Bar */
.training-stages-bar {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.stage-item-new {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 0.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  
  &.completed {
    background: rgba(34, 197, 94, 0.1);
    
    .stage-icon-wrapper {
      background: rgba(34, 197, 94, 0.2);
      color: #22c55e;
      box-shadow: 0 0 15px rgba(34, 197, 94, 0.3);
    }
    
    .stage-name-new {
      color: #22c55e;
    }
  }
  
  &.active {
    background: rgba(99, 102, 241, 0.15);
    
    .stage-icon-wrapper {
      background: rgba(99, 102, 241, 0.3);
      color: #6366f1;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
      animation: pulse 2s ease-in-out infinite;
    }
    
    .stage-name-new {
      color: #6366f1;
      font-weight: 600;
    }
  }
  
  &.pending {
    opacity: 0.5;
    
    .stage-icon-wrapper {
      background: rgba(255, 255, 255, 0.05);
      color: rgba(255, 255, 255, 0.4);
    }
  }
}

.stage-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.stage-icon-emoji {
  font-size: 1.5rem;
}

.stage-name-new {
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
}



/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 15, 35, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.loading-content {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

.loading-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.loading-content p {
  color: #b3b3d1;
  margin-bottom: 2rem;
  font-size: 0.875rem;
}

.loading-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-text {
  font-weight: 600;
  color: #667eea;
  min-width: 40px;
}

/* Scrollbar Styling */
.logs-container::-webkit-scrollbar {
  width: 8px;
}

.logs-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

/* Animations */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .metrics-charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 1rem;
  }

  .hero-section {
    padding: 2rem 1rem;
  }

  .hero-section h1 {
    font-size: 2rem;
  }

  .hero-section p {
    font-size: 1rem;
  }

  .progress-main {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .progress-details {
    grid-template-columns: 1fr;
  }

  .stage-progress {
    grid-template-columns: repeat(2, 1fr);
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .training-controls {
    flex-direction: column;
    width: 100%;
  }

  .control-btn {
    width: 100%;
    justify-content: center;
  }

  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .training-summary {
    flex-direction: column;
    gap: 0.5rem;
  }

  .summary-divider {
    display: none;
  }

  .breadcrumb {
    display: none;
  }
}

@media (max-width: 480px) {
  .training-header {
    padding: 0.75rem 1rem;
  }

  .hero-icon {
    font-size: 3rem;
  }

  .hero-section h1 {
    font-size: 1.75rem;
  }

  .progress-dashboard,
  .metrics-section,
  .charts-section,
  .logs-section,
  .action-section {
    padding: 1.5rem;
  }

  .section-header h2 {
    font-size: 1.5rem;
  }

  .stage-progress {
    grid-template-columns: 1fr;
  }

  .metric-value {
    font-size: 1.5rem;
  }

  .completion-icon {
    font-size: 3rem;
  }
  .completion-message h3 {
    font-size: 1.5rem;
  }
}

/* ===== NEW: Configuration Section Styles ===== */
.configuration-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.configuration-section {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(20px);
}

.configuration-section .section-header {
  text-align: center;
  margin-bottom: 2rem;
  border-bottom: none;
  padding-bottom: 0;
}

.configuration-section .section-header h2 {
  font-size: 2rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.section-description {
  color: #b3b3d1;
  font-size: 1rem;
  margin: 0;
}

.training-active-badge {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #667eea;
  font-weight: 600;
  text-align: center;
  font-size: 0.9375rem;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.config-panel {
  background: rgba(15, 15, 35, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.config-panel:hover {
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.panel-header h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.panel-header svg {
  color: #667eea;
}

.hyperparameters-placeholder,
.validation-placeholder {
  padding: 3rem 2rem;
  text-align: center;
  background: rgba(102, 126, 234, 0.05);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #b3b3d1;
  font-size: 1rem;
}

.config-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  flex-wrap: wrap;
}

.start-training-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 3rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.start-training-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.start-training-btn:active {
  transform: translateY(0);
}

@media (max-width: 1200px) {
  .config-grid {
    grid-template-columns: 1fr;
  }
}

/* Hyperparameter Controls Styles */
.hyperparameters-container {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.param-group {
  margin-bottom: 1.5rem;
}

.param-group-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.group-icon {
  font-size: 1.5rem;
}

.param-group-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.params-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.param-item {
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.15);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.param-item:hover {
  background: rgba(102, 126, 234, 0.08);
  border-color: rgba(102, 126, 234, 0.25);
}

.param-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.param-label {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
}

.param-impact {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.param-impact.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.param-impact.medium {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.param-impact.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.param-control {
  margin-bottom: 0.5rem;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.param-slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: rgba(102, 126, 234, 0.2);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.param-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.param-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.slider-value {
  min-width: 60px;
  text-align: right;
  font-weight: 600;
  color: #667eea;
  font-size: 0.9375rem;
}

.param-select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 15, 35, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.param-select:hover {
  border-color: rgba(102, 126, 234, 0.5);
}

.param-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.param-description {
  font-size: 0.8125rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.5;
}

.hyperparameters-container::-webkit-scrollbar {
  width: 6px;
}

.hyperparameters-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.hyperparameters-container::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.3);
  border-radius: 3px;
}

.hyperparameters-container::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.5);
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.param-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(102, 126, 234, 0.4);
  border-radius: 4px;
  background: rgba(15, 15, 35, 0.8);
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
}

.param-checkbox:checked {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
}

.param-checkbox:checked::after {
  content: '✓';
  display: block;
  text-align: center;
  color: white;
  font-size: 14px;
  font-weight: bold;
  line-height: 16px;
}

.param-checkbox:hover {
  border-color: #667eea;
}

.checkbox-label {
  font-size: 0.9375rem;
  color: #ffffff;
  user-select: none;
}

/* Validation Strategy Styles */
.validation-strategies {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.strategy-card {
  background: rgba(15, 15, 35, 0.6);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.strategy-card:hover {
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateX(4px);
}

.strategy-card.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
}

.strategy-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.strategy-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.strategy-icon {
  font-size: 1.5rem;
}

.strategy-header h4 {
  flex: 1;
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.strategy-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.strategy-badge.recommended {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.strategy-badge.advanced {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.strategy-badge.expert{
  background: rgba(231, 60, 37, 0.2);
  color: #e01b1b;
}

.strategy-description {
  color: #b3b3d1;
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.strategy-config {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-item label {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
}

.config-slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: rgba(102, 126, 234, 0.2);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.config-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.config-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.config-hint {
  font-size: 0.8125rem;
  color: #b3b3d1;
  margin: 0;
}

.split-preview {
  margin-top: 0.75rem;
}


.train-portion {
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  transition: width 0.3s ease;
}

.test-portion {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  transition: width 0.3s ease;
}

.warning-box {
  padding: 0.75rem 1rem;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 8px;
  color: #fbbf24;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Algorithm Warning Banner */
.algorithm-warning-banner {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.15));
  border: 1px solid rgba(245, 158, 11, 0.4);
  border-left: 4px solid #f59e0b;
  border-radius: 8px;
  margin-top: 1rem;
  animation: slideDown 0.3s ease;
}

.algorithm-warning-banner svg {
  color: #f59e0b;
  flex-shrink: 0;
  margin-top: 2px;
}

.algorithm-warning-banner .warning-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #fbbf24;
  font-size: 0.875rem;
  line-height: 1.5;
}

.algorithm-warning-banner .warning-content strong {
  color: #fbbf24;
  font-weight: 600;
}

.algorithm-warning-banner .warning-content span {
  color: #fcd34d;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Tweak Parameters Section */
.tweak-params-section {
  margin: 2rem 0;
  padding: 0 2rem;
}

.tweak-params-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.tweak-params-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
  transition: left 0.5s ease;
}

.tweak-params-btn:hover::before {
  left: 100%;
}
.tweak-params-btn .btn-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.tweak-params-btn .btn-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tweak-params-btn .btn-subtitle {
  font-size: 0.875rem;
  color: #b3b3d1;
  font-weight: 400;
}

.tweak-params-btn .arrow-icon {
  color: #667eea;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.tweak-params-btn:hover .arrow-icon {
  transform: translateX(5px);
}

/* Reset Hyperparameters Button */
.reset-params-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-params-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  transform: translateY(-1px);
}

.reset-params-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.reset-params-btn svg {
  flex-shrink: 0;
}

/* Best Parameters Section */
.best-params-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.best-params-section h4 {
  color: #e0e7ff;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.param-badge {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.param-badge:hover {
  background: rgba(15, 23, 42, 0.8);
  border-color: rgba(102, 126, 234, 0.5);
  transform: translateY(-2px);
}

.param-name {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.param-value {
  font-size: 1rem;
  color: #e0e7ff;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

/* ===== CV RESULTS SECTION STYLES ===== */
.cv-results-section {
  margin-top: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.03), rgba(118, 75, 162, 0.03));
  border-radius: 16px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.cv-results-section h3 {
  color: #e0e7ff;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cv-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.cv-metrics-grid .metric-card {
  padding: 1.25rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.cv-metrics-grid .metric-card:hover {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.cv-metrics-grid .metric-card.highlight {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
  border-color: rgba(102, 126, 234, 0.4);
}

.cv-metrics-grid .metric-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.cv-metrics-grid .metric-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cv-metrics-grid .metric-label {
  font-size: 0.875rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.cv-metrics-grid .metric-value {
  font-size: 1.75rem;
  color: #e0e7ff;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

/* ===== FOLD SCORES LIST STYLES ===== */
.fold-scores-list {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.fold-scores-list h4 {
  color: #e0e7ff;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.folds-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.fold-item {
  display: grid;
  grid-template-columns: 80px 100px 1fr;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.fold-item:hover {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(102, 126, 234, 0.3);
  transform: translateX(4px);
}

.fold-label {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.fold-value {
  font-size: 1rem;
  color: #e0e7ff;
  font-weight: 700;
  font-family: 'Courier New', monospace;
  text-align: right;
}

.fold-bar {
  height: 8px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.5s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

</style>


