<template>
  <div class="algorithm-selection">
    <!-- Navigation Header -->
    <nav class="selection-header">
      <div class="nav-left">
        <button @click="goBack" class="back-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
            />
          </svg>
          Back to Target Selection
        </button>
        <div class="breadcrumb">
          <span>DataSage</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span>Target Selection</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
          <span class="current">Algorithm Selection</span>
        </div>
      </div>

      <!-- ✅ ADD THIS: Backend Status -->
      <div class="backend-status" v-if="backendConnected !== null">
        <div
          class="status-indicator"
          :class="{
            connected: backendConnected,
            disconnected: !backendConnected,
          }"
        >
          <div class="status-dot"></div>
          <span class="status-text">
            {{ backendConnected ? "ML Backend Ready" : "Frontend Mode" }}
          </span>
          <span class="dataset-id" v-if="backendConnected && datasetId">
            ID: {{ datasetId.substring(0, 8) }}...
          </span>
        </div>
      </div>
      <div class="target-summary" v-if="selectedTarget">
        <span class="target-info">
          🎯 Target: <strong>{{ selectedTarget.name }}</strong>
          <span class="problem-type">{{
            formatProblemType(problemType.type)
          }}</span>
        </span>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🤖</div>
        <h1>Choose Your ML Algorithm</h1>
        <p>
          We'll recommend the best machine learning algorithms based on your
          data and target variable
        </p>
        <div class="dataset-summary" v-if="datasetStats.rows">
          <span class="summary-item"
            >📊 {{ formatNumber(datasetStats.rows) }} rows</span
          >
          <span class="summary-divider">•</span>
          <span class="summary-item"
            >📋 {{ datasetStats.features }} features</span
          >
          <span class="summary-divider">•</span>
          <span class="summary-item"
            >🎯 {{ formatProblemType(problemType.type) }}</span
          >
          <div class="confidence-indicator">
            <div
              class="confidence-score"
              :class="getConfidenceLevel(problemType.confidence)"
            >
              {{ Math.round(problemType.confidence * 100) }}% Confidence
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Analyzing your data and generating algorithm recommendations...</p>
    </div>

    <!-- Main Content -->
    <div v-else class="main-container">
      <!-- Problem Analysis Section -->
      <section class="analysis-section">
        <div class="section-header">
          <h2>Problem Analysis</h2>
          <p class="section-description">
            Understanding your machine learning task
          </p>
        </div>

        <div class="analysis-grid">
          <div class="analysis-card">
            <div class="card-icon">🎯</div>
            <h3>Problem Type</h3>
            <div class="problem-info">
              <span class="problem-label">{{
                formatProblemType(problemType.type)
              }}</span>
              <div class="problem-details">
                <p>{{ getProblemDescription(problemType.type) }}</p>
                <div class="problem-metrics">
                  <span class="metric">
                    <span class="metric-label">Target Variable:</span>
                    <span class="metric-value"
                      >{{ selectedTarget.name }} ({{
                        selectedTarget.type
                      }})</span
                    >
                  </span>
                  <span class="metric" v-if="selectedTarget.uniqueValues">
                    <span class="metric-label">Unique Values:</span>
                    <span class="metric-value">{{
                      selectedTarget.uniqueValues
                    }}</span>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="analysis-card">
            <div class="card-icon">📊</div>
            <h3>Dataset Profile</h3>
            <div class="dataset-profile">
              <div class="profile-metric">
                <span class="profile-label">Size Category</span>
                <span class="profile-value">{{
                  getDatasetSizeCategory()
                }}</span>
              </div>
              <div class="profile-metric">
                <span class="profile-label">Complexity</span>
                <span class="profile-value">{{ getDatasetComplexity() }}</span>
              </div>
              <div class="profile-metric">
                <span class="profile-label">Recommended Focus</span>
                <span class="profile-value">{{ getRecommendedFocus() }}</span>
              </div>
            </div>
          </div>

          <div class="analysis-card">
            <div class="card-icon">⚙️</div>
            <h3>Preprocessing Applied</h3>
            <div class="preprocessing-summary">
              <div
                v-if="preprocessingSteps.length === 0"
                class="no-preprocessing"
              >
                <p>No preprocessing was applied</p>
                <span class="warning-note"
                  >⚠️ Consider going back to apply data cleaning</span
                >
              </div>
              <div v-else class="preprocessing-list">
                <div
                  v-for="step in preprocessingSteps"
                  :key="step"
                  class="preprocessing-step"
                >
                  <span class="step-icon">✓</span>
                  <span class="step-name">{{
                    formatPreprocessingStep(step)
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Algorithm Recommendations -->
      <section class="recommendations-section">
        <div class="section-header">
          <h2>Algorithm Recommendations</h2>
          <div class="recommendation-controls">
            <button
              @click="showComparison = !showComparison"
              class="compare-btn"
              :class="{ active: showComparison }"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M3,3H21V5H3V3M3,7H21V9H3V7M3,11H21V13H3V11M3,15H21V17H3V15M3,19H21V21H3V19Z"
                />
              </svg>
              {{ showComparison ? "Hide Comparison" : "Compare Algorithms" }}
            </button>
            <button @click="resetSelection" class="reset-btn">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"
                />
              </svg>
              Reset Selection
            </button>
          </div>
        </div>

        <!-- Comparison Table -->
        <div v-if="showComparison" class="comparison-table-container">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>Algorithm</th>
                <th>Accuracy</th>
                <th>Speed</th>
                <th>Interpretability</th>
                <th>Complexity</th>
                <th>Score</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="algo in recommendedAlgorithms"
                :key="algo.name"
                :class="{
                  selected: selectedAlgorithm?.name === algo.name,
                  recommended: algo.recommended,
                }"
              >
                <td class="algorithm-cell">
                  <span class="algo-icon">{{ algo.icon }}</span>
                  <span class="algo-name">{{ algo.name }}</span>
                  <span v-if="algo.recommended" class="recommended-badge"
                    >Recommended</span
                  >
                </td>
                <td>
                  <div
                    class="score-bar"
                    :style="{ width: algo.accuracy * 100 + '%' }"
                  >
                    {{ (algo.accuracy * 100).toFixed(0) }}%
                  </div>
                </td>
                <td>
                  <div
                    class="score-bar"
                    :style="{ width: algo.speed * 100 + '%' }"
                  >
                    {{ (algo.speed * 100).toFixed(0) }}%
                  </div>
                </td>
                <td>
                  <span
                    class="complexity-badge"
                    :class="algo.complexity.toLowerCase()"
                    >{{ algo.complexity }}</span
                  >
                </td>
                <td>
                  <span
                    class="complexity-badge"
                    :class="algo.complexity.toLowerCase()"
                    >{{ algo.complexity }}</span
                  >
                </td>
                <td>
                  <div class="overall-score">
                    {{ (algo.score * 100).toFixed(0) }}%
                  </div>
                </td>
                <td>
                  <button
                    @click="selectAlgorithm(algo)"
                    class="select-btn"
                    :class="{ selected: selectedAlgorithm?.name === algo.name }"
                  >
                    {{
                      selectedAlgorithm?.name === algo.name
                        ? "Selected"
                        : "Select"
                    }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Algorithm Cards -->
        <div v-if="!showComparison" class="algorithms-grid">
          <div
            v-for="algorithm in recommendedAlgorithms"
            :key="algorithm.name"
            class="algorithm-card"
            :class="{
              selected: selectedAlgorithm?.name === algorithm.name,
              recommended: algorithm.recommended,
            }"
            @click="selectAlgorithm(algorithm)"
          >
            <div class="card-header">
              <div class="algorithm-info">
                <span class="algorithm-icon">{{ algorithm.icon }}</span>
                <div class="algorithm-title">
                  <h3>{{ algorithm.name }}</h3>
                  <div class="algorithm-badges">
                    <span v-if="algorithm.recommended" class="badge recommended"
                      >🏆 Recommended</span
                    >
                    <span
                      class="badge complexity"
                      :class="algorithm.complexity.toLowerCase()"
                      >{{ algorithm.complexity }}</span
                    >
                    <span v-if="algorithm.needsScaling" class="badge scaling"
                      >Needs Scaling</span
                    >
                  </div>
                </div>
              </div>
              <div class="algorithm-score">
                <div
                  class="score-circle"
                  :class="getScoreLevel(algorithm.score)"
                >
                  {{ Math.round(algorithm.score * 100) }}
                </div>
                <span class="score-label">Match Score</span>
              </div>
            </div>

            <div class="algorithm-metrics">
              <div class="metric">
                <span class="metric-label">Accuracy</span>
                <div class="metric-bar">
                  <div
                    class="bar-fill accuracy"
                    :style="{ width: algorithm.accuracy * 100 + '%' }"
                  ></div>
                  <span class="metric-value"
                    >{{ (algorithm.accuracy * 100).toFixed(0) }}%</span
                  >
                </div>
              </div>
              <div class="metric">
                <span class="metric-label">Training Speed</span>
                <div class="metric-bar">
                  <div
                    class="bar-fill speed"
                    :style="{ width: algorithm.speed * 100 + '%' }"
                  ></div>
                  <span class="metric-value"
                    >{{ (algorithm.speed * 100).toFixed(0) }}%</span
                  >
                </div>
              </div>
            </div>

            <div class="algorithm-strengths">
              <h4>Best for:</h4>
              <ul class="strengths-list">
                <li
                  v-for="strength in algorithm.strongWith.slice(0, 3)"
                  :key="strength"
                >
                  {{ strength }}
                </li>
              </ul>
            </div>

            <div class="card-footer">
              <button
                class="select-algorithm-btn"
                :class="{
                  selected: selectedAlgorithm?.name === algorithm.name,
                }"
              >
                <svg
                  v-if="selectedAlgorithm?.name === algorithm.name"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"
                  />
                </svg>
                {{
                  selectedAlgorithm?.name === algorithm.name
                    ? "Selected"
                    : "Select Algorithm"
                }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Configuration Section -->
      <section v-if="selectedAlgorithm" class="configuration-section">
        <div class="section-header">
          <h2>Configure {{ selectedAlgorithm.name }}</h2>
          <p class="section-description">
            Fine-tune hyperparameters and preprocessing options
          </p>
        </div>

        <div class="config-grid">
          <!-- Hyperparameters -->
          <div class="config-panel">
            <div class="panel-header">
              <h3>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"
                  />
                </svg>
                Hyperparameters
              </h3>
              <div class="panel-actions">
                <button @click="resetHyperparameters" class="reset-params-btn">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"
                    />
                  </svg>
                  Reset to Defaults
                </button>
                <button @click="useOptimalParams" class="optimal-btn">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M12,2A3,3 0 0,1 15,5A3,3 0 0,1 12,8A3,3 0 0,1 9,5A3,3 0 0,1 12,2M21,9V7H15L13.5,7.5C13.14,7.19 12.79,6.89 12.4,6.62L13.5,6H21V9M21,16V14H13.91C13.65,14.76 13.34,15.5 13,16H21M21,23V21H13C13,21.34 13,21.67 13,22C13,22.35 13,22.67 13,23H21M9,10H12L13.5,15L15,10H18V8H9V10Z"
                    />
                  </svg>
                  Use Optimal Settings
                </button>
              </div>
            </div>

            <div class="hyperparameters-container">
              <div
                v-for="paramGroup in getKeyParameters(selectedAlgorithm.name)"
                :key="paramGroup.name"
                class="param-group"
              >
                <div class="param-group-header">
                  <span class="group-icon">{{ paramGroup.icon }}</span>
                  <h4>{{ paramGroup.name }}</h4>
                </div>

                <div class="params-list">
                  <div
                    v-for="param in paramGroup.params"
                    :key="param.name"
                    class="param-item"
                  >
                    <div class="param-header">
                      <label class="param-label">{{ param.label }}</label>
                      <span class="param-impact" :class="param.impact"
                        >{{ param.impact }} impact</span
                      >
                    </div>

                    <!-- Slider Parameter -->
                    <div v-if="param.type === 'slider'" class="param-control">
                      <div class="slider-container">
                        <input
                          type="range"
                          :min="param.min"
                          :max="param.max"
                          :step="param.step"
                          v-model="hyperparameters[param.name]"
                          class="param-slider"
                        />
                        <div class="slider-value">
                          {{
                            formatParameterValue(
                              param.name,
                              hyperparameters[param.name]
                            )
                          }}
                        </div>
                      </div>
                    </div>

                    <!-- Select Parameter -->
                    <div
                      v-else-if="param.type === 'select'"
                      class="param-control"
                    >
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

                    <p class="param-description">{{ param.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Preprocessing Options -->
          <div class="config-panel">
            <div class="panel-header">
              <h3>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M6,2A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2H6Z"
                  />
                </svg>
                Feature Scaling & Engineering
              </h3>
            </div>

            <div class="preprocessing-options">
              <!-- Feature Scaling -->
              <div class="option-group">
                <h4>Feature Scaling</h4>
                <div class="scaling-options">
                  <label
                    class="option-card"
                    :class="{ selected: selectedScaling === 'none' }"
                  >
                    <input
                      type="radio"
                      v-model="selectedScaling"
                      value="none"
                    />
                    <div class="option-content">
                      <div class="option-icon">🚫</div>
                      <span class="option-title">No Scaling</span>
                      <p class="option-desc">
                        Use raw features (good for tree-based algorithms)
                      </p>
                    </div>
                  </label>

                  <label
                    class="option-card"
                    :class="{ selected: selectedScaling === 'standard' }"
                  >
                    <input
                      type="radio"
                      v-model="selectedScaling"
                      value="standard"
                    />
                    <div class="option-content">
                      <div class="option-icon">📊</div>
                      <span class="option-title">Standard Scaling</span>
                      <p class="option-desc">
                        Zero mean, unit variance (recommended for most
                        algorithms)
                      </p>
                    </div>
                  </label>

                  <label
                    class="option-card"
                    :class="{ selected: selectedScaling === 'minmax' }"
                  >
                    <input
                      type="radio"
                      v-model="selectedScaling"
                      value="minmax"
                    />
                    <div class="option-content">
                      <div class="option-icon">📏</div>
                      <span class="option-title">MinMax Scaling</span>
                      <p class="option-desc">
                        Scale to [0,1] range (good for neural networks)
                      </p>
                    </div>
                  </label>

                  <label
                    class="option-card"
                    :class="{ selected: selectedScaling === 'robust' }"
                  >
                    <input
                      type="radio"
                      v-model="selectedScaling"
                      value="robust"
                    />
                    <div class="option-content">
                      <div class="option-icon">🛡️</div>
                      <span class="option-title">Robust Scaling</span>
                      <p class="option-desc">
                        Median and IQR-based (resistant to outliers)
                      </p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Feature Engineering -->
              <div class="option-group">
                <h4>Feature Engineering</h4>
                <div class="engineering-options">
                  <label class="checkbox-option">
                    <input
                      type="checkbox"
                      v-model="featureEngineering.polynomial"
                    />
                    <span class="checkbox-custom"></span>
                    <div class="option-content">
                      <span class="option-title">Polynomial Features</span>
                      <p class="option-desc">
                        Create interaction and polynomial terms
                      </p>
                    </div>
                  </label>

                  <label class="checkbox-option">
                    <input type="checkbox" v-model="featureEngineering.pca" />
                    <span class="checkbox-custom"></span>
                    <div class="option-content">
                      <span class="option-title"
                        >Principal Component Analysis</span
                      >
                      <p class="option-desc">
                        Reduce dimensionality while preserving variance
                      </p>
                    </div>
                  </label>

                  <label class="checkbox-option">
                    <input
                      type="checkbox"
                      v-model="featureEngineering.featureSelection"
                    />
                    <span class="checkbox-custom"></span>
                    <div class="option-content">
                      <span class="option-title">Feature Selection</span>
                      <p class="option-desc">
                        Select most important features automatically
                      </p>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Training Configuration -->
      <section v-if="selectedAlgorithm" class="training-section">
        <div class="section-header">
          <h2>Training Configuration</h2>
          <p class="section-description">
            Set up model validation and training parameters
          </p>
        </div>

        <div class="training-config">
          <div class="config-row">
            <div class="config-item">
              <label class="config-label">Validation Method</label>
              <select v-model="validationMethod" class="config-select">
                <option value="train_test_split">Train/Test Split</option>
                <option value="cross_validation">Cross Validation</option>
                <option value="stratified">Stratified Validation</option>
              </select>
            </div>

            <div
              class="config-item"
              v-if="validationMethod === 'train_test_split'"
            >
              <label class="config-label">Test Size</label>
              <div class="slider-input">
                <input
                  type="range"
                  min="0.1"
                  max="0.5"
                  step="0.05"
                  v-model="testSize"
                  class="config-slider"
                />
                <span class="slider-value"
                  >{{ Math.round(testSize * 100) }}%</span
                >
              </div>
            </div>

            <div
              class="config-item"
              v-if="validationMethod === 'cross_validation'"
            >
              <label class="config-label">CV Folds</label>
              <select v-model="cvFolds" class="config-select">
                <option :value="3">3-Fold</option>
                <option :value="5">5-Fold</option>
                <option :value="10">10-Fold</option>
              </select>
            </div>
          </div>

          <div class="config-row">
            <div class="config-item">
              <label class="config-label">Random State</label>
              <input
                type="number"
                v-model="randomState"
                class="config-input"
                min="0"
                max="999"
              />
            </div>

            <div class="config-item">
              <label class="config-label">Metric to Optimize</label>
              <select v-model="optimizationMetric" class="config-select">
                <option
                  v-for="metric in getAvailableMetrics()"
                  :key="metric.value"
                  :value="metric.value"
                >
                  {{ metric.label }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <!-- Action Section -->
      <section v-if="selectedAlgorithm" class="action-section">
        <div class="action-content">
          <!-- ✅ ENHANCE your configuration summary section -->
        <div class="configuration-summary">
          <h3>Advanced Configuration Summary</h3>
          <div class="summary-grid">
            <div class="summary-item">
              <span class="summary-label">Algorithm</span>
              <span class="summary-value">{{ selectedAlgorithm.name }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Problem Type</span>
              <span class="summary-value">{{ formatProblemType(problemType.type) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Feature Scaling</span>
              <span class="summary-value">{{ formatScalingMethod(selectedScaling) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Validation Method</span>
              <span class="summary-value">{{ formatValidationMethod(validationMethod) }}</span>
            </div>
            <!-- ✅ ADD THESE NEW ITEMS -->
            <div class="summary-item" v-if="hasFeatureEngineering()">
              <span class="summary-label">Feature Engineering</span>
              <span class="summary-value">{{ getFeatureEngineeringSummary() }}</span>
            </div>
            <div class="summary-item" v-if="validationMethod === 'cross_validation' || validationMethod === 'stratified'">
              <span class="summary-label">CV Folds</span>
              <span class="summary-value">{{ cvFolds }}-Fold</span>
            </div>
          </div>
        </div>


          <div class="action-buttons">
            <button @click="exportConfiguration" class="export-config-btn">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
                />
              </svg>
              Export Configuration
            </button>

            <button @click="startTraining" class="start-training-btn" :disabled="isTraining">
              <svg v-if="isTraining" width="16" height="16" class="spinner" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z" />
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
              </svg>
              {{ isTraining ? 'Initializing Advanced Training...' : 'Start Advanced Training' }}
              <!-- ✅ ADD FEATURE COUNT INDICATOR -->
              <span v-if="!isTraining && getAdvancedFeaturesCount() > 0" class="feature-count">
                +{{ getAdvancedFeaturesCount() }} Advanced Features
              </span>
            </button>
          </div>
        </div>
      </section>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isTraining" class="training-overlay">
      <div class="training-content">
        <div class="training-spinner"></div>
        <h3>Training {{ selectedAlgorithm.name }}</h3>
        <p>{{ trainingMessage }}</p>
        <div class="training-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: trainingProgress + '%' }"
            ></div>
          </div>
          <span class="progress-text">{{ trainingProgress }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Core Data
const isLoading = ref(true);
const selectedTarget = ref(null);
const problemType = ref({ type: "binary_classification", confidence: 0.8 });
const datasetStats = ref({ rows: 0, features: 0 });
const preprocessingSteps = ref([]);
const recommendedAlgorithms = ref([]);
const selectedAlgorithm = ref(null);
const backendConnected = ref(null);
const datasetId = ref(null);

// UI State
const showComparison = ref(false);
const isTraining = ref(false);
const trainingProgress = ref(0);
const trainingMessage = ref("");

// Configuration
const hyperparameters = reactive({});
const selectedScaling = ref("standard");
const featureEngineering = reactive({
  polynomial: false,
  pca: false,
  featureSelection: true,
});

// Training Config
const validationMethod = ref("train_test_split");
const testSize = ref(0.2);
const cvFolds = ref(5);
const randomState = ref(42);
const optimizationMetric = ref("accuracy");


// ✅ STANDARDIZED BACKEND CONNECTION CHECK
const checkBackendConnection = async () => {
  try {
    console.log('🔌 Checking backend connection...')
    
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
    
    const response = await fetch('http://localhost:8000/api/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    
    if (response.ok) {
      const data = await response.json()
      backendConnected.value = true
      console.log('✅ Backend connected:', data.message)
      return true
    } else {
      throw new Error(`Backend returned ${response.status}`)
    }
  } catch (error) {
    console.error('❌ Backend connection failed:', error.message)
    backendConnected.value = false
    return false
  }
}


// Methods
const loadDataFromPreviousSteps = () => {
  try {
    console.log("Loading data from previous steps...");

    // Load target selection data
    const targetData = localStorage.getItem("selectedTarget");
    const processedData = localStorage.getItem("processedData");

    if (targetData) {
      const target = JSON.parse(targetData);
      selectedTarget.value = target;
      problemType.value = detectProblemType(target);
      console.log("Loaded target:", target);
    }

    if (processedData) {
      const data = JSON.parse(processedData);
      datasetStats.value = {
        rows: data.finalRows || data.data?.length || 0,
        features: data.finalColumns || data.columns?.length || 0,
      };
      preprocessingSteps.value = data.processingSteps || [];
      console.log("Loaded dataset stats:", datasetStats.value);
    }

    if (!targetData || !processedData) {
      console.warn("Missing required data, redirecting...");
      router.push("/target-selection");
      return false;
    }

    return true;
  } catch (error) {
    console.error("Error loading data:", error);
    router.push("/target-selection");
    return false;
  }
};

const selectAlgorithmWithBackend = (algorithm) => {
  // Your existing selectAlgorithm logic
  selectedAlgorithm.value = algorithm

  // Set default scaling based on algorithm requirements
  if (algorithm.needsScaling) {
    selectedScaling.value = 'standard'
  } else {
    selectedScaling.value = 'none'
  }

  // Initialize hyperparameters with defaults
  resetHyperparameters()

  console.log(`✅ Algorithm selected: ${algorithm.name} with ${backendConnected.value ? 'BACKEND' : 'FRONTEND'} integration`)
}

const detectProblemType = (target) => {
  let problemType = "binary_classification";
  let confidence = 0.8;

  if (target.type === "numerical" || target.originalType === "numerical") {
    problemType = "regression";
    confidence = 0.95;
  } else if (
    target.type === "categorical" ||
    target.originalType === "categorical"
  ) {
    if (target.uniqueValues === 2) {
      problemType = "binary_classification";
      confidence = 0.95;
    } else if (target.uniqueValues > 2 && target.uniqueValues <= 20) {
      problemType = "multiclass_classification";
      confidence = 0.9;
    } else if (target.uniqueValues > 20) {
      problemType = "regression";
      confidence = 0.6;
    }
  }

  return { type: problemType, confidence };
};

const initializeRecommendations = () => {
  const algorithms = getAllAvailableAlgorithms();

  recommendedAlgorithms.value = algorithms
    .map((algo) => ({
      ...algo,
      score: calculateAlgorithmScore(algo),
      rank: 0,
    }))
    .sort((a, b) => b.score - a.score)
    .map((algo, index) => ({
      ...algo,
      rank: index + 1,
      recommended: index < 3,
    }));

  // Auto-select the top recommendation
  if (recommendedAlgorithms.value.length > 0) {
    selectAlgorithm(recommendedAlgorithms.value[0]);
  }
};

const calculateAlgorithmScore = (algorithm) => {
  let score = 0.5;

  // Dataset size considerations
  if (datasetStats.value.rows < 1000) {
    if (
      ["Logistic Regression", "Support Vector Machine"].includes(algorithm.name)
    )
      score += 0.2;
    if (algorithm.name === "XGBoost") score -= 0.1;
  } else if (datasetStats.value.rows > 10000) {
    if (algorithm.name === "Random Forest") score += 0.2;
    if (algorithm.name === "XGBoost") score += 0.3;
  }

  // Problem type considerations
  if (problemType.value.type === "binary_classification") {
    if (algorithm.name === "Logistic Regression") score += 0.2;
    if (algorithm.name === "Support Vector Machine") score += 0.15;
  } else if (problemType.value.type === "multiclass_classification") {
    if (["Random Forest", "XGBoost"].includes(algorithm.name)) score += 0.2;
  } else if (problemType.value.type === "regression") {
    if (
      ["Random Forest", "XGBoost", "Linear Regression"].includes(algorithm.name)
    )
      score += 0.2;
  }

  // Feature count considerations
  if (datasetStats.value.features > 50) {
    if (algorithm.name === "Random Forest") score += 0.1;
    if (algorithm.name === "XGBoost") score += 0.15;
  }

  // Preprocessing considerations
  if (preprocessingSteps.value.includes("categoricalEncoding")) {
    if (["Random Forest", "XGBoost"].includes(algorithm.name)) score += 0.1;
  }

  return Math.min(1.0, Math.max(0.0, score));
};

const getAllAvailableAlgorithms = () => {
  const allAlgorithms = [
    {
      name: "Random Forest",
      icon: "🌲",
      complexity: "Medium",
      needsScaling: false,
      speed: 0.7,
      accuracy: 0.85,
      strongWith: [
        "Mixed features",
        "Outliers",
        "Non-linear patterns",
        "Feature importance",
      ],
      weakWith: ["High dimensionality", "Linear relationships"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
    {
      name: "XGBoost",
      icon: "🚀",
      complexity: "High",
      needsScaling: false,
      speed: 0.6,
      accuracy: 0.92,
      strongWith: [
        "Complex patterns",
        "Competition performance",
        "Tabular data",
      ],
      weakWith: ["Interpretability", "Overfitting with small data"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
    {
      name: "Logistic Regression",
      icon: "📈",
      complexity: "Low",
      needsScaling: true,
      speed: 0.95,
      accuracy: 0.78,
      strongWith: [
        "Linear relationships",
        "Baseline model",
        "Interpretability",
        "Small datasets",
      ],
      weakWith: ["Non-linear patterns", "Feature interactions"],
      problemTypes: ["binary_classification", "multiclass_classification"],
    },
    {
      name: "Linear Regression",
      icon: "📊",
      complexity: "Low",
      needsScaling: true,
      speed: 0.98,
      accuracy: 0.72,
      strongWith: ["Linear relationships", "Simple baseline", "Fast training"],
      weakWith: ["Non-linear patterns", "Outliers"],
      problemTypes: ["regression"],
    },
    {
      name: "Support Vector Machine",
      icon: "🎪",
      complexity: "High",
      needsScaling: true,
      speed: 0.5,
      accuracy: 0.84,
      strongWith: ["High dimensions", "Kernel trick", "Small datasets"],
      weakWith: ["Large datasets", "Interpretability"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
    {
      name: "K-Nearest Neighbors",
      icon: "🎯",
      complexity: "Low",
      needsScaling: true,
      speed: 0.4,
      accuracy: 0.76,
      strongWith: ["Local patterns", "Non-parametric", "Simple implementation"],
      weakWith: ["High dimensions", "Large datasets", "Memory usage"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
    {
      name: "Decision Tree",
      icon: "🌳",
      complexity: "Low",
      needsScaling: false,
      speed: 0.9,
      accuracy: 0.75,
      strongWith: [
        "Interpretability",
        "Categorical features",
        "Non-linear patterns",
      ],
      weakWith: ["Overfitting", "Unstable predictions"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
    {
      name: "Neural Network (MLP)",
      icon: "🧠",
      complexity: "High",
      needsScaling: true,
      speed: 0.6,
      accuracy: 0.86,
      strongWith: ["Complex patterns", "Large datasets", "Feature learning"],
      weakWith: ["Interpretability", "Hyperparameter tuning", "Small datasets"],
      problemTypes: [
        "binary_classification",
        "multiclass_classification",
        "regression",
      ],
    },
  ];

  return allAlgorithms.filter((algo) =>
    algo.problemTypes.includes(problemType.value.type)
  );
};

const getKeyParameters = (algorithmName) => {
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
            description:
              "More trees generally improve performance but increase training time.",
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
            description:
              "Controls tree complexity. Deeper trees can capture more patterns but may overfit.",
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
        ],
      },
    ],
    XGBoost: [
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
        ],
      },
    ],
    "Logistic Regression": [
      {
        name: "Regularization",
        icon: "⚖️",
        params: [
          {
            name: "C",
            label: "Regularization Strength",
            type: "slider",
            min: 0.001,
            max: 100,
            step: 0.001,
            default: 1.0,
            impact: "high",
            description: "Inverse of regularization strength.",
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
        ],
      },
    ],
    "Support Vector Machine": [
      {
        name: "SVM Configuration",
        icon: "🎪",
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
            description:
              "Regularization parameter. Higher values mean less regularization.",
          },
          {
            name: "kernel",
            label: "Kernel Type",
            type: "select",
            options: [
              { value: "rbf", label: "RBF (Gaussian)" },
              { value: "linear", label: "Linear" },
              { value: "poly", label: "Polynomial" },
            ],
            default: "rbf",
            impact: "high",
            description: "Kernel function to use.",
          },
        ],
      },
    ],
  };

  return parameterSets[algorithmName] || [];
};

const selectAlgorithm = (algorithm) => {
  selectAlgorithmWithBackend(algorithm)
}

const resetHyperparameters = () => {
  const params = getKeyParameters(selectedAlgorithm.value.name);
  params.forEach((group) => {
    group.params.forEach((param) => {
      hyperparameters[param.name] = param.default;
    });
  });
};

const useOptimalParams = () => {
  // Set optimal parameters based on dataset characteristics
  if (selectedAlgorithm.value.name === "Random Forest") {
    hyperparameters.n_estimators = datasetStats.value.rows < 1000 ? 100 : 200;
    hyperparameters.max_depth = datasetStats.value.features > 50 ? 15 : 10;
  } else if (selectedAlgorithm.value.name === "XGBoost") {
    hyperparameters.n_estimators = 100;
    hyperparameters.learning_rate = 0.1;
    hyperparameters.max_depth = 6;
  }
};

const resetSelection = () => {
  selectedAlgorithm.value = null;
  Object.keys(hyperparameters).forEach((key) => delete hyperparameters[key]);
  selectedScaling.value = "standard";
  featureEngineering.polynomial = false;
  featureEngineering.pca = false;
  featureEngineering.featureSelection = true;
};

const getAvailableMetrics = () => {
  if (problemType.value.type === "regression") {
    return [
      { value: "r2", label: "R² Score" },
      { value: "mse", label: "Mean Squared Error" },
      { value: "mae", label: "Mean Absolute Error" },
    ];
  } else {
    return [
      { value: "accuracy", label: "Accuracy" },
      { value: "f1", label: "F1 Score" },
      { value: "precision", label: "Precision" },
      { value: "recall", label: "Recall" },
      { value: "roc_auc", label: "ROC AUC" },
    ];
  }
};

const hasFeatureEngineering = () => {
  return featureEngineering.polynomial || featureEngineering.pca || featureEngineering.featureSelection
}

const getFeatureEngineeringSummary = () => {
  const features = []
  if (featureEngineering.polynomial) features.push('Polynomial')
  if (featureEngineering.pca) features.push('PCA')
  if (featureEngineering.featureSelection) features.push('Selection')
  return features.length > 0 ? features.join(', ') : 'None'
}

const getAdvancedFeaturesCount = () => {
  let count = 0
  if (selectedScaling.value !== 'none') count++
  if (hasFeatureEngineering()) count++
  if (validationMethod.value !== 'train_test_split') count++
  return count
}



const startTraining = async () => {
  if (!selectedAlgorithm.value) {
    alert('Please select an algorithm first')
    return
  }

  try {
    // GET REAL BACKEND DATASET ID
    const processedData = JSON.parse(localStorage.getItem('processedData') || '{}')
    const selectedTargetData = JSON.parse(localStorage.getItem('selectedTarget') || '{}')
    
    if (!processedData.backendDatasetId) {
      throw new Error('No backend dataset ID found. Please ensure dataset was uploaded to backend.')
    }
    
    // CREATE COMPLETE CONFIGURATION WITH BACKEND DATASET
    const finalConfig = {
      // ALGORITHM INFO
      algorithm: {
        name: selectedAlgorithm.value.name,
        icon: selectedAlgorithm.value.icon,
        complexity: selectedAlgorithm.value.complexity
      },
      
      // HYPERPARAMETERS
      hyperparameters: {...hyperparameters},
      
      // ADVANCED PREPROCESSING (CRITICAL - WAS MISSING)
      scaling: selectedScaling.value,
      featureEngineering: {...featureEngineering},
      
      // ADVANCED VALIDATION CONFIG (CRITICAL - WAS MISSING)
      validation: {
        method: validationMethod.value,
        testSize: testSize.value,
        cvFolds: cvFolds.value,
        randomState: randomState.value,
        metric: optimizationMetric.value
      },
      
      // PROBLEM TYPE
      problemType: {
        type: problemType.value.type,
        confidence: problemType.value.confidence
      },
      
      // TARGET INFO
      target: {
        name: selectedTargetData.name || selectedTarget.value?.name,
        type: selectedTargetData.type || selectedTarget.value?.type
      },
      
      // CRITICAL: BACKEND DATASET INTEGRATION
      backendDatasetId: processedData.backendDatasetId,
      datasetId: processedData.datasetId,
      backendAvailable: processedData.backendAvailable,
      
      // METADATA
      timestamp: new Date().toISOString(),
      sessionId: `session_${Date.now()}`
    }

    localStorage.setItem('mlConfiguration', JSON.stringify(finalConfig))

    console.log('✅ Advanced ML Configuration with backend integration:', {
      algorithm: finalConfig.algorithm.name,
      backendDatasetId: finalConfig.backendDatasetId,
      scaling: finalConfig.scaling,
      featureEngineering: finalConfig.featureEngineering,
      validationMethod: finalConfig.validation.method
    })

    router.push('/model-training')
    
  } catch (error) {
    console.error('Error:', error)
    alert('Error: ' + error.message)
  }
}





const exportConfiguration = () => {
  const config = {
    algorithm: selectedAlgorithm.value.name,
    hyperparameters: { ...hyperparameters },
    scaling: selectedScaling.value,
    featureEngineering: { ...featureEngineering },
    validation: {
      method: validationMethod.value,
      testSize: testSize.value,
      cvFolds: cvFolds.value,
      randomState: randomState.value,
      metric: optimizationMetric.value,
    },
  };

  const blob = new Blob([JSON.stringify(config, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "ml_configuration.json";
  a.click();
  URL.revokeObjectURL(url);
};

const goBack = () => {
  router.push("/target-selection");
};

// Utility functions
const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num);
};

const formatProblemType = (type) => {
  const types = {
    binary_classification: "Binary Classification",
    multiclass_classification: "Multi-class Classification",
    regression: "Regression",
  };
  return types[type] || type;
};

const formatScalingMethod = (method) => {
  const methods = {
    none: "No Scaling",
    standard: "Standard Scaling",
    minmax: "MinMax Scaling",
    robust: "Robust Scaling",
  };
  return methods[method] || method;
};

const formatValidationMethod = (method) => {
  const methods = {
    train_test_split: "Train/Test Split",
    cross_validation: "Cross Validation",
    stratified: "Stratified Validation",
  };
  return methods[method] || method;
};

const formatPreprocessingStep = (step) => {
  const steps = {
    columnSelection: "Column Selection",
    missingValues: "Missing Value Handling",
    duplicateRemoval: "Duplicate Removal",
    outlierHandling: "Outlier Handling",
    categoricalEncoding: "Categorical Encoding",
  };
  return steps[step] || step;
};

const formatParameterValue = (paramName, value) => {
  if (paramName === "learning_rate" || paramName === "C") {
    return parseFloat(value).toFixed(3);
  }
  return value;
};

const getConfidenceLevel = (confidence) => {
  if (confidence >= 0.9) return "high";
  if (confidence >= 0.7) return "medium";
  return "low";
};

const getScoreLevel = (score) => {
  if (score >= 0.8) return "high";
  if (score >= 0.6) return "medium";
  return "low";
};

const getDatasetSizeCategory = () => {
  const rows = datasetStats.value.rows;
  if (rows < 1000) return "Small";
  if (rows < 10000) return "Medium";
  if (rows < 100000) return "Large";
  return "Very Large";
};

const getDatasetComplexity = () => {
  const features = datasetStats.value.features;
  if (features < 10) return "Simple";
  if (features < 50) return "Moderate";
  if (features < 200) return "Complex";
  return "High-dimensional";
};

const getRecommendedFocus = () => {
  const rows = datasetStats.value.rows;
  const features = datasetStats.value.features;

  if (rows < 1000) return "Avoid Overfitting";
  if (features > 100) return "Feature Selection";
  if (problemType.value.type.includes("classification")) return "Class Balance";
  return "Model Tuning";
};

const getProblemDescription = (type) => {
  const descriptions = {
    binary_classification:
      "Predict one of two possible outcomes (Yes/No, True/False, etc.)",
    multiclass_classification: "Predict one of multiple categories or classes",
    regression: "Predict a continuous numerical value",
  };
  return descriptions[type] || "";
};

// Lifecycle
onMounted(async () => {
  if (loadDataFromPreviousSteps()) {
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate loading
    initializeRecommendations()
    isLoading.value = false
  }

  // ✅ ADD THIS: Check backend connection
  await checkBackendConnection()
})
</script>

<style scoped>
/* Base Styles */
.algorithm-selection {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
}

/* Navigation */
.selection-header {
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

.target-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.target-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  font-size: 0.875rem;
}

.problem-type {
  padding: 0.25rem 0.75rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
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
  display: block;
}

.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-section p {
  font-size: 1.25rem;
  color: #b3b3d1;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.dataset-summary {
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

.confidence-indicator {
  margin-left: 1rem;
}

.confidence-score {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
}

.confidence-score.high {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.confidence-score.medium {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.confidence-score.low {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 2rem;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* Section Headers */
.section-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

.section-description {
  font-size: 1rem;
  color: #b3b3d1;
  margin: 0;
  line-height: 1.6;
}

.recommendation-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.compare-btn,
.reset-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.compare-btn:hover,
.reset-btn:hover,
.compare-btn.active {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

/* Analysis Section */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.analysis-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.analysis-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
}

.problem-info {
  text-align: left;
}

.problem-label {
  font-size: 1.25rem;
  font-weight: 600;
  color: #667eea;
  display: block;
  margin-bottom: 0.75rem;
}

.problem-details p {
  color: #b3b3d1;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.problem-metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.metric-value {
  color: #ffffff;
  font-weight: 500;
}

.dataset-profile,
.preprocessing-summary {
  text-align: left;
}

.profile-metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.profile-metric:last-child {
  border-bottom: none;
}

.profile-label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.profile-value {
  color: #ffffff;
  font-weight: 500;
}

.no-preprocessing {
  text-align: center;
  padding: 1rem;
}

.warning-note {
  font-size: 0.875rem;
  color: #f59e0b;
  display: block;
  margin-top: 0.5rem;
}

.preprocessing-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.preprocessing-step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.step-icon {
  color: #10b981;
  font-weight: bold;
}

.step-name {
  color: #b3b3d1;
}


.backend-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.dataset-id {
  font-size: 0.7rem;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 8px;
  font-family: monospace;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Comparison Table */
.comparison-table-container {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  overflow-x: auto;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-table th,
.comparison-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.comparison-table th {
  background: rgba(102, 126, 234, 0.1);
  color: #ffffff;
  font-weight: 600;
  position: sticky;
  top: 0;
}

.comparison-table tr.recommended {
  background: rgba(16, 185, 129, 0.05);
  border-left: 3px solid #10b981;
}

.comparison-table tr.selected {
  background: rgba(102, 126, 234, 0.1);
  border-left: 3px solid #667eea;
}

.algorithm-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.algo-icon {
  font-size: 1.5rem;
}

.algo-name {
  font-weight: 500;
  color: #ffffff;
}

.recommended-badge {
  padding: 0.25rem 0.5rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.score-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.complexity-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.complexity-badge.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.complexity-badge.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.complexity-badge.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.overall-score {
  font-size: 1.25rem;
  font-weight: 700;
  color: #667eea;
}

.select-btn {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.select-btn:hover,
.select-btn.selected {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

/* Algorithm Cards */
.algorithms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.algorithm-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.algorithm-card:hover {
  background: rgba(26, 26, 46, 0.8);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
}

.algorithm-card.recommended {
  border-color: #10b981;
  background: linear-gradient(
    135deg,
    rgba(16, 185, 129, 0.1),
    rgba(26, 26, 46, 0.8)
  );
}

.algorithm-card.recommended::before {
  content: "🏆";
  position: absolute;
  top: -10px;
  right: -10px;
  background: linear-gradient(135deg, #10b981, #059669);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.algorithm-card.selected {
  border-color: #667eea;
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.15),
    rgba(26, 26, 46, 0.8)
  );
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.algorithm-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.algorithm-icon {
  font-size: 2.5rem;
}

.algorithm-title h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #ffffff;
}

.algorithm-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.recommended {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.badge.scaling {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.algorithm-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.score-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  border: 3px solid;
}

.score-circle.high {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-color: #10b981;
}

.score-circle.medium {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border-color: #f59e0b;
}

.score-circle.low {
  background: linear-gradient(135deg, #6b7280, #4b5563);
  color: white;
  border-color: #6b7280;
}

.score-label {
  font-size: 0.75rem;
  color: #9ca3af;
  text-align: center;
}

.algorithm-metrics {
  margin-bottom: 1.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.metric:last-child {
  margin-bottom: 0;
}

.metric-label {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-bottom: 0.5rem;
}

.metric-bar {
  position: relative;
  height: 8px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  overflow: hidden;
  flex: 1;
  margin: 0 1rem;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.bar-fill.accuracy {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.bar-fill.speed {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.metric-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #ffffff;
  min-width: 40px;
  text-align: right;
}

.algorithm-strengths {
  margin-bottom: 2rem;
}

.algorithm-strengths h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.strengths-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.strengths-list li {
  padding: 0.5rem 0;
  color: #b3b3d1;
  font-size: 0.875rem;
  position: relative;
  padding-left: 1.5rem;
}

.strengths-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

.card-footer {
  margin-top: auto;
}

.select-algorithm-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
}

.select-algorithm-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.select-algorithm-btn.selected {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: #667eea;
}

/* Configuration Section */
.config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.config-panel {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

.panel-header h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.panel-actions {
  display: flex;
  gap: 0.75rem;
}

.reset-params-btn,
.optimal-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.reset-params-btn:hover,
.optimal-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.param-group {
  margin-bottom: 2rem;
}

.param-group:last-child {
  margin-bottom: 0;
}

.param-group-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.group-icon {
  font-size: 1.5rem;
}

.param-group-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.param-item {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
}

.param-item:last-child {
  margin-bottom: 0;
}

.param-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.param-label {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

.param-impact {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.param-impact.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.param-impact.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.param-impact.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.param-control {
  margin-bottom: 1rem;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.param-slider {
  flex: 1;
  height: 8px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 4px;
  outline: none;
  /* -webkit-appearance: none; */
}

.param-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.param-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

.slider-value {
  min-width: 60px;
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
  color: #ffffff;
}

.feature-count {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-left: 0.5rem;
}

.param-select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.875rem;
}

.param-select:focus {
  outline: none;
  border-color: #667eea;
}

.param-description {
  color: #b3b3d1;
  font-size: 0.875rem;
  line-height: 1.4;
  margin: 0;
}

/* Preprocessing Options */
.option-group {
  margin-bottom: 2rem;
}

.option-group:last-child {
  margin-bottom: 0;
}

.option-group h4 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
}

.scaling-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.option-card {
  display: block;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-card input[type="radio"] {
  display: none;
}

.option-content {
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  text-align: center;
  transition: all 0.2s ease;
}

.option-card:hover .option-content {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.4);
}

.option-card.selected .option-content {
  background: rgba(102, 126, 234, 0.15);
  border-color: #667eea;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.option-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: block;
}

.option-title {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  display: block;
  margin-bottom: 0.5rem;
}

.option-desc {
  font-size: 0.875rem;
  color: #b3b3d1;
  line-height: 1.4;
  margin: 0;
}

.engineering-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-option {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-option:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.4);
}

.checkbox-option input[type="checkbox"] {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 4px;
  position: relative;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.checkbox-option input[type="checkbox"]:checked + .checkbox-custom {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
}

.checkbox-option input[type="checkbox"]:checked + .checkbox-custom::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
}

/* Training Section */
.training-config {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.config-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.config-row:last-child {
  margin-bottom: 0;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.config-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
}

.config-select,
.config-input {
  padding: 0.75rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.875rem;
}

.config-select:focus,
.config-input:focus {
  outline: none;
  border-color: #667eea;
}

.slider-input {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.config-slider {
  flex: 1;
  height: 6px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 3px;
  outline: none;
  /* -webkit-appearance: none; */
}

.config-slider::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.config-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

/* Action Section */
.action-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.action-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.configuration-summary h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.summary-label {
  color: #9ca3af;
  font-size: 0.875rem;
}

.summary-value {
  color: #ffffff;
  font-weight: 500;
  font-size: 0.875rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.export-config-btn,
.start-training-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-config-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.export-config-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.start-training-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  min-width: 180px;
  justify-content: center;
}

.start-training-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.start-training-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Training Overlay */
.training-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.training-content {
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.training-spinner {
  width: 80px;
  height: 80px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

.training-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.training-content p {
  color: #b3b3d1;
  margin-bottom: 2rem;
}

.training-progress {
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
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-text {
  font-weight: 600;
  color: #667eea;
  min-width: 40px;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .config-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
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

  .algorithms-grid {
    grid-template-columns: 1fr;
  }

  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .action-content {
    flex-direction: column;
    text-align: center;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    width: 100%;
    justify-content: center;
  }

  .scaling-options {
    grid-template-columns: 1fr;
  }

  .config-row {
    grid-template-columns: 1fr;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
