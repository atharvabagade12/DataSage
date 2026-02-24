<template>
  <div class="algorithm-selection">
    <!-- Navigation Header - REMOVED (Handled by Global Layout) -->
    
    <!-- Hero Section - REMOVED (Context handled by Global Context Bar) -->


    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Analyzing your data and generating algorithm recommendations...</p>
    </div>

    <!-- Main Content -->
    <div v-else class="main-container">
      <!-- Understanding Your Machine Learning Task Section -->
      <section class="analysis-section">
        <div class="section-header">
          <h2>Understanding Your Machine Learning Task</h2>
          <p class="section-description">
            Review your problem setup and data characteristics
          </p>
        </div>

        <div class="analysis-grid">
          <!-- Card 1: Problem Type & Target Analysis -->
          <div class="analysis-card">
            <div class="card-header">
              <div class="card-icon">🎯</div>
              <h3>Problem Type & Target Analysis</h3>
            </div>
            
            <div class="card-content">
              <!-- Problem Type Badge -->
              <div class="info-section">
                <label class="info-label">Problem Type</label>
                <div class="problem-type-badge" :class="problemType.type">
                  {{ formatProblemType(problemType.type) }}
                </div>
              </div>

              <!-- Confidence Meter -->
              <div class="info-section">
                <label class="info-label">Detection Confidence</label>
                <div class="confidence-meter">
                  <div 
                    class="meter-fill" 
                    :class="getConfidenceLevel(problemType.confidence)"
                    :style="{ width: (problemType.confidence * 100) + '%' }"
                  ></div>
                </div>
                <span class="confidence-value">
                  {{ Math.round(problemType.confidence * 100) }}%
                </span>
              </div>

              <div class="card-divider"></div>

              <!-- Target Details -->
              <div class="target-details">
                <div class="detail-row">
                  <span class="detail-label">Target Variable:</span>
                  <span class="detail-value">{{ selectedTarget.name }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Data Type:</span>
                  <span class="detail-value">{{ selectedTarget.type }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Unique Values:</span>
                  <span class="detail-value">{{ selectedTarget.uniqueValues }}</span>
                </div>
              </div>

              <div class="card-divider"></div>

              <!-- Insight Box -->
              <div class="insight-box">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,17A1.5,1.5 0 0,1 10.5,15.5A1.5,1.5 0 0,1 12,14A1.5,1.5 0 0,1 13.5,15.5A1.5,1.5 0 0,1 12,17M13.5,13H10.5V7H13.5V13Z"/>
                </svg>
                <p>{{ getProblemDescription(problemType.type) }}</p>
              </div>
            </div>
          </div>

          <!-- Card 2: Dataset Profile -->
          <div class="analysis-card">
            <div class="card-header">
              <div class="card-icon">📊</div>
              <h3>Dataset Profile</h3>
            </div>
            
            <div class="card-content">
              <!-- Dataset Characteristics -->
              <div class="info-section">
                <label class="info-label">Dataset Characteristics</label>
                <div class="stats-grid">
                  <div class="stat-box">
                    <span class="stat-value">{{ formatNumber(datasetStats.rows) }}</span>
                    <span class="stat-label">Rows</span>
                  </div>
                  <div class="stat-box">
                    <span class="stat-value">{{ datasetStats.features }}</span>
                    <span class="stat-label">Features</span>
                  </div>
                  <div class="stat-box">
                    <span class="stat-value">{{ getDatasetSizeCategory() }}</span>
                    <span class="stat-label">Size</span>
                  </div>
                  <div class="stat-box">
                    <span class="stat-value">{{ getDatasetComplexity() }}</span>
                    <span class="stat-label">Complexity</span>
                  </div>
                </div>
              </div>

              <div class="card-divider"></div>

              <!-- Feature Breakdown -->
              <div class="info-section">
                <label class="info-label">Feature Breakdown</label>
                <div class="feature-breakdown">
                  <div class="breakdown-item">
                    <span class="breakdown-label">Total Features</span>
                    <span class="breakdown-value">{{ datasetStats.features }}</span>
                  </div>
                </div>
              </div>

              <div class="card-divider"></div>

              <!-- Recommendation -->
              <div class="insight-box">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,17A1.5,1.5 0 0,1 10.5,15.5A1.5,1.5 0 0,1 12,14A1.5,1.5 0 0,1 13.5,15.5A1.5,1.5 0 0,1 12,17M13.5,13H10.5V7H13.5V13Z"/>
                </svg>
                <p><strong>Recommendation:</strong> {{ getRecommendedFocus() }}</p>
              </div>
            </div>
          </div>

          <!-- Card 3: Preprocessing Applied -->
          <div class="analysis-card">
            <div class="card-header">
              <div class="card-icon">✅</div>
              <h3>Preprocessing Applied</h3>
              <span class="steps-badge" v-if="preprocessingSteps.length > 0">
                {{ preprocessingSteps.length }} Steps
              </span>
            </div>
            
            <div class="card-content">
              <div v-if="preprocessingSteps.length > 0" class="preprocessing-timeline">
                <div 
                  v-for="(step, index) in preprocessingSteps" 
                  :key="index"
                  class="timeline-item"
                >
                  <div class="timeline-marker">{{ index + 1 }}</div>
                  <div class="timeline-content">
                    <h4>{{ formatPreprocessingStep(step) }}</h4>
                  </div>
                </div>
              </div>
              
              <div v-else class="no-preprocessing">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor" opacity="0.3">
                  <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                </svg>
                <p>No preprocessing steps applied yet</p>
                <span class="warning-note">Data will be used as-is for training</span>
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
                      >Recommended</span
                    >
                    <!-- <span
                      class="badge complexity"
                      :class="algorithm.complexity.toLowerCase()"
                      >{{ algorithm.complexity}}<p>Complexity</p></span
                    > -->
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
              <!-- 🆕 ADD THIS: Two-button layout -->
              <div class="footer-buttons">
                <!-- Learn More Button -->
                <button
                  @click.stop="showAlgorithmDetails(algorithm)"
                  class="learn-more-btn"
                  title="Learn how this algorithm works"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"
                    />
                  </svg>
                  Learn More
                </button>

                <!-- Select Algorithm Button -->
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
        </div>
      </section>

      

      

      
      

      <!-- Action Section -->
      <section v-if="selectedAlgorithm" class="action-section">
        <div class="action-content">
          <!--  ENHANCE your configuration summary section -->
          <div class="configuration-summary">
            <h3>Configuration Summary</h3>
            <div class="summary-grid">
              <div class="summary-item">
                <span class="summary-label">Algorithm: </span>
                <span class="summary-value">{{ selectedAlgorithm.name }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Problem Type: </span>
                <span class="summary-value">{{formatProblemType(problemType.type)}}</span>
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

            <button
              @click="startTraining"
              class="start-training-btn"
              :disabled="isTraining"
            >
              <svg
                v-if="isTraining"
                width="16"
                height="16"
                class="spinner"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z" />
              </svg>
              <svg
                v-else
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
              </svg>
              {{
                isTraining
                  ? "Initializing Model Training..."
                  : "Start Model Training"
              }}
              <!-- ADD FEATURE COUNT INDICATOR -->
              
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

    <div
      v-if="selectedAlgorithmInfo"
      class="algorithm-info-modal"
      @click.self="closeAlgorithmInfo"
    >
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h2>
            <span class="algo-icon">{{ selectedAlgorithmInfo.icon }}</span>
            {{ selectedAlgorithmInfo.name }}
          </h2>
          <button @click="closeAlgorithmInfo" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
              />
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <!-- Overview Section -->
          <div class="info-section">
            <h3>📋 Overview</h3>
            <p class="description">
              {{ selectedAlgorithmInfo.detailedDescription }}
            </p>
          </div>

          <!-- How It Works -->
          <div class="info-section">
            <h3>⚙️ How It Works</h3>
            <p>{{ selectedAlgorithmInfo.howItWorks }}</p>
          </div>

          <!-- When to Use -->
          <div class="info-section">
            <h3>✅ When to Use</h3>
            <ul class="bullet-list">
              <li
                v-for="(use, index) in selectedAlgorithmInfo.whenToUse"
                :key="index"
              >
                {{ use }}
              </li>
            </ul>
          </div>

          <!-- When NOT to Use -->
          <div class="info-section warning">
            <h3>⚠️ When NOT to Use</h3>
            <ul class="bullet-list">
              <li
                v-for="(avoid, index) in selectedAlgorithmInfo.whenNotToUse"
                :key="index"
              >
                {{ avoid }}
              </li>
            </ul>
          </div>

          <!-- Real World Examples -->
          <div class="info-section">
            <h3>💼 Real-World Examples</h3>
            <div class="example-tags">
              <span
                v-for="(
                  example, index
                ) in selectedAlgorithmInfo.realWorldExamples"
                :key="index"
                class="example-tag"
              >
                {{ example }}
              </span>
            </div>
          </div>

          <!-- Complexity & Performance -->
          <div class="info-section">
            <h3>📊 Performance Characteristics</h3>
            <div class="metrics-grid">
              <div class="metric-item">
                <span class="metric-label">Complexity</span>
                <span class="metric-value">{{
                  selectedAlgorithmInfo.complexity
                }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Speed</span>
                <span class="metric-value">{{
                  selectedAlgorithmInfo.speed
                }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Interpretability</span>
                <span class="metric-value">{{
                  selectedAlgorithmInfo.interpretability || "Medium"
                }}</span>
              </div>
            </div>
          </div>

          <!-- Pros & Cons -->
          <div class="pros-cons-container">
            <div class="pros-section">
              <h3>👍 Strengths</h3>
              <ul class="bullet-list">
                <li
                  v-for="(pro, index) in selectedAlgorithmInfo.strongWith"
                  :key="index"
                >
                  {{ pro }}
                </li>
              </ul>
            </div>
            <div class="cons-section">
              <h3>👎 Weaknesses</h3>
              <ul class="bullet-list">
                <li
                  v-for="(con, index) in selectedAlgorithmInfo.weakWith"
                  :key="index"
                >
                  {{ con }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useExperimentStore } from "@/stores/experiment";
import { useDataStore } from "@/stores/data";
import { useAuthenticatedFetch } from "@/composables/useAuthenticatedFetch";

const router = useRouter();
const experimentStore = useExperimentStore();
const dataStore = useDataStore();
const { authenticatedGet } = useAuthenticatedFetch();

const { 
  datasetId, 
  targetColumn: storeTargetColumn, 
  problemType: storeProblemType,
  preprocessing: storePreprocessing,
  datasetMetadata
} = storeToRefs(experimentStore);

const { statistics } = storeToRefs(dataStore);

// Core Data
const isLoading = ref(true);
const selectedTarget = ref(null);
const problemType = ref({ type: "binary_classification", confidence: 0.8 });
const datasetStats = ref({ rows: 0, features: 0 });
const preprocessingSteps = ref([]);
const recommendedAlgorithms = ref([]);
const selectedAlgorithm = ref(null);
const backendConnected = ref(null);
const selectedAlgorithmInfo = ref(null);

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

// New Validation Strategy Config
const validationStrategy = ref("simple_train_test"); 
const splitRatio = ref(0.8);
const stratifiedCV = ref(true);

// GridSearchCV Config
const gridSearchCVFolds = ref(5);
const gridDensity = ref("normal"); 
const showGridPreview = ref(false);

// RandomizedSearchCV Config
const randomSearchCVFolds = ref(5);
const randomSearchIterations = ref(20);
const showDistributionsPreview = ref(false);

//  STANDARDIZED BACKEND CONNECTION CHECK
const checkBackendConnection = async () => {
  try {
    console.log(" Checking backend connection...");
    const response = await authenticatedGet(`/api/health`);

    if (response.ok) {
      const data = await response.json();
      backendConnected.value = true;
      console.log("Backend connected:", data.message);
      return true;
    } else {
      throw new Error(`Backend returned ${response.status}`);
    }
  } catch (error) {
    console.error("Backend connection failed:", error.message);
    backendConnected.value = false;
    return false;
  }
};

// Methods
const loadDataFromPreviousSteps = () => {
  try {
    console.log("🔄 Loading data from Experiment Store...");
    
    // Sync Reactives from Store
    if (storeTargetColumn.value) {
      selectedTarget.value = storeTargetColumn.value;
    }
    
    if (storeProblemType.value && storeProblemType.value.type) {
      problemType.value = storeProblemType.value;
    } else if (selectedTarget.value) {
      problemType.value = detectProblemType(selectedTarget.value);
    }
    
    // Dataset Stats
    if (datasetMetadata.value) {
       datasetStats.value = {
         rows: datasetMetadata.value.totalRows || 0,
         features: datasetMetadata.value.columns || 0
       };
    }
    
    // Preprocessing Steps Visualization
    const steps = [];
    if (storePreprocessing.value.droppedColumns?.length > 0) steps.push(`Dropped Columns (${storePreprocessing.value.droppedColumns.length})`);
    if (storePreprocessing.value.isMissingValuesApplied) steps.push("Missing Values Handled");
    if (storePreprocessing.value.isOutliersApplied) steps.push("Outliers Handled");
    if (storePreprocessing.value.isDuplicatesApplied) steps.push("Duplicates Removed");
    if (storePreprocessing.value.isDateTimeApplied) steps.push("DateTime Features Extracted");
    
    if (storePreprocessing.value.isSplitApplied) steps.push("Train/Test Split");
    if (storePreprocessing.value.isEncodingApplied) steps.push(`Categorical Encoding (${storePreprocessing.value.encodedColumns?.length || 0})`);
    if (storePreprocessing.value.isScalingApplied) steps.push(`Feature Scaling`);
    if (storePreprocessing.value.smote?.applied) steps.push(`SMOTE (${storePreprocessing.value.smote?.samples_added || 0} samples)`);
    
    preprocessingSteps.value = steps;

    if (storePreprocessing.value.splitInfo) {
      splitRatio.value = storePreprocessing.value.splitInfo.testRatio ? (1 - storePreprocessing.value.splitInfo.testRatio) : 0.8;
    }

    console.log("✅ Loaded from Store:", {
      target: selectedTarget.value,
      problem: problemType.value,
      stats: datasetStats.value,
      steps: steps
    });

    return true;
  } catch (error) {
    console.error("❌ Error loading data:", error);
    return false;
  }
};

const selectAlgorithmWithBackend = (algorithm) => {
  // Your existing selectAlgorithm logic
  selectedAlgorithm.value = algorithm;

  // Set default scaling based on algorithm requirements
  if (algorithm.needsScaling) {
    selectedScaling.value = "standard";
  } else {
    selectedScaling.value = "none";
  }

  // Initialize hyperparameters with defaults
  resetHyperparameters();

  console.log(
    `Algorithm selected: ${algorithm.name} with ${
      backendConnected.value ? "BACKEND" : "FRONTEND"
    } integration`
  );
};

const detectProblemType = (target) => {
  console.log("🔍 Detecting problem type for target:", target);
  
  let problemType = "binary_classification";
  let confidence = 0.8;

  // Check multiple possible property names for data type
  const rawType = target.type || 
                   target.dataType || 
                   target.dtype || 
                   target.originalType ||
                   target.columnType;
                   
  const dataType = String(rawType).toLowerCase();
  
  const uniqueValues = target.uniqueValues || 
                       target.unique_values || 
                       target.cardinality ||
                       0;
  
  console.log("📊 Extracted properties:", {
    dataType,
    uniqueValues,
    rawTarget: target
  });

  // ============================================================================
  // PRIORITY 1: Binary Classification (Explicit 2 values)
  // ============================================================================
  if (uniqueValues === 2) {
    problemType = "binary_classification";
    confidence = 0.95;
    console.log("✅ Detected as BINARY CLASSIFICATION (2 unique values)");
    return { type: problemType, confidence };
  }

  // ============================================================================
  // PRIORITY 2: Semantic Type Check (Most Reliable)
  // ============================================================================
  const isNumeric = ['numerical', 'numeric', 'int', 'integer', 'float', 'double', 'decimal', 'number'].includes(dataType);
  const isCategorical = ['categorical', 'category', 'string', 'object', 'text', 'bool', 'boolean'].includes(dataType);

  if (isNumeric) {
     // Default to Regression for numerical data
     // Exception: If user intends classification on numeric labels, they should override, 
     // but statistically/structurally it's a regression space.
     problemType = "regression";
     confidence = 0.9;
     
     // Lower confidence if cardinality is very low (could be ordinal/class labels)
     if (uniqueValues > 0 && uniqueValues <= 10) {
         confidence = 0.7;
         console.log(`⚠️ Detected as REGRESSION (Numerical type, low cardinality: ${uniqueValues})`);
     } else {
         console.log("✅ Detected as REGRESSION (Numerical type)");
     }
     
     return { type: problemType, confidence };
  }

  if (isCategorical) {
      // Must be Multiclass since we already checked uniqueValues === 2
      problemType = "multiclass_classification";
      confidence = 0.9;
      console.log("✅ Detected as MULTICLASS CLASSIFICATION (Categorical type)");
      return { type: problemType, confidence };
  }

  // ============================================================================
  // PRIORITY 3: Fallback Heuristics (Unknown Type)
  // ============================================================================
  
  if (uniqueValues > 20) {
    problemType = "regression";
    confidence = 0.6;
    console.log("⚠️ Fallback: Detected as REGRESSION (High cardinality, unknown type)");
    return { type: problemType, confidence };
  }
  
  if (uniqueValues > 2) {
      problemType = "multiclass_classification";
      confidence = 0.6;
      console.log("⚠️ Fallback: Detected as MULTICLASS CLASSIFICATION (Low cardinality, unknown type)");
      return { type: problemType, confidence };
  }

  // Final Catch-all
  console.log("⚠️ No clear indicators, defaulting to BINARY CLASSIFICATION");
  return { type: "binary_classification", confidence: 0.5 };
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
  // 1. Base Compatibility Check
  if (!algorithm.problemTypes.includes(problemType.value.type)) {
    return 0; // Not compatible
  }

  let score = 0.5; // Base score
  const rows = datasetStats.value.rows;
  const features = datasetStats.value.features;
  const isScaled = preprocessingSteps.value.some(step => 
    (typeof step === 'string' && step.includes('Scaling')) || 
    (step.name && step.name.includes('Scaling'))
  );
  const isEncoded = preprocessingSteps.value.some(step => 
    (typeof step === 'string' && step.includes('Encoding')) || 
    (step.name && step.name.includes('Encoding'))
  );

  // 2. Dataset Size Heuristics
  if (rows < 1000) {
    // Small dataset: Prefer simple, low-variance models
    if (algorithm.complexity === "Low") score += 0.25;
    if (["Logistic Regression", "Linear Regression", "Naive Bayes", "K-Nearest Neighbors"].includes(algorithm.name)) score += 0.15;
    
    
  } else if (rows >= 1000 && rows < 50000) {
    // Medium dataset: Sweet spot for many algorithms
    if (["Random Forest", "Support Vector Machine", "XGBoost"].includes(algorithm.name)) score += 0.2;
  } else {
    // Large dataset: Prefer efficient, scalable models
    if (["XGBoost", "LightGBM", "Linear Regression", "Logistic Regression"].includes(algorithm.name)) score += 0.25;
    if (["Support Vector Machine", "K-Nearest Neighbors"].includes(algorithm.name)) score -= 0.3; // Too slow O(n^2) or O(n) inference
  }

  // 3. Dimensionality (Features)
  if (features > 100) {
    // High dimensionality
    // User Preference: Reward Trees, SVM, Naive Bayes
    if (["Random Forest", "XGBoost", "Support Vector Machine", "Naive Bayes"].includes(algorithm.name)) score += 0.2;
    
    // Penalize algorithms that struggle with high dimensions without feature selection
    if (algorithm.name === "K-Nearest Neighbors") score -= 0.4; // Curse of dimensionality distance issues
  } else if (features < 20) {
    // Low dimensionality
    if (["Decision Tree", "K-Nearest Neighbors", "Logistic Regression"].includes(algorithm.name)) score += 0.1;
  }

  // 4. Preprocessing Context
  if (algorithm.needsScaling && !isScaled) {
    score -= 0.4; // Critical penalty: Distance/Gradient based algos fail without scaling
  }
  
  if (algorithm.needsScaling && isScaled) {
    score += 0.1; // Reward for meeting requirement
  }

  // 5. Algorithm Specific Boosts
  if (algorithm.name === "XGBoost" || algorithm.name === "Random Forest") {
    score += 0.1; // Generally strong performers (State of the Art for tabular)
  }

  // 6. Problem Type Specifics
  if (problemType.value.type === "binary_classification") {
    if (algorithm.name === "Logistic Regression") score += 0.1;
  }

  // Clamp score between 0 and 1
  return Math.min(1.0, Math.max(0.0, score));
};


// 🎯 COMPLETE REFACTORED getAllAvailableAlgorithms() FUNCTION

const getAllAvailableAlgorithms = () => {
  const allAlgorithms = [
    // ========== EXISTING ALGORITHMS ==========
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
      description:
        "Ensemble of decision trees that reduces overfitting through bagging. Excellent for mixed data types and provides feature importance.",
      category: "ensemble",
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
      description:
        "Gradient boosting algorithm optimized for speed and performance. Industry standard for tabular data competitions.",
      category: "boosting",
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
      description:
        "Linear model for classification with probabilistic outputs. Fast, interpretable, and excellent as a baseline.",
      category: "linear",
    },
    {
      name: "Linear Regression",
      icon: "📉",
      complexity: "Low",
      needsScaling: true,
      speed: 0.98,
      accuracy: 0.72,
      strongWith: ["Linear relationships", "Simple baseline", "Fast training"],
      weakWith: ["Non-linear patterns", "Outliers"],
      problemTypes: ["regression"],
      description:
        "Simple linear model for regression. Perfect for understanding linear relationships and as a baseline.",
      category: "linear",
    },
    {
      name: "Support Vector Machine",
      icon: "⚡",
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
      description:
        "Powerful classifier using kernel tricks for non-linear decision boundaries. Effective in high-dimensional spaces.",
      category: "kernel",
    },
    {
      name: "K-Nearest Neighbors",
      icon: "🎲",
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
      description:
        "Instance-based learning that classifies by majority vote of neighbors. Simple but memory-intensive.",
      category: "instance-based",
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
      description:
        "Tree-like model of decisions. Highly interpretable but prone to overfitting without constraints.",
      category: "tree",
    },
    
    {
      name: "Support Vector Regression",
      icon: "📊",
      complexity: "Medium",
      needsScaling: true,
      speed: 0.55,
      accuracy: 0.82,
      strongWith: [
        "Non-linear regression",
        "High dimensions",
        "Robust to outliers",
        "Small to medium datasets",
      ],
      weakWith: [
        "Large datasets (slow)",
        "Interpretability",
        "Kernel selection",
      ],
      problemTypes: ["regression"],
      description:
        "Extension of SVM for regression tasks. Uses kernel trick to model non-linear relationships with robust predictions.",
      category: "kernel",
    },
    
    {
      name: "Naive Bayes",
      icon: "🎯",
      complexity: "Low",
      needsScaling: false,
      speed: 0.98,
      accuracy: 0.8,
      strongWith: [
        "Text classification",
        "Categorical features",
        "Small datasets",
        "Real-time predictions",
        "Probabilistic output",
      ],
      weakWith: [
        "Feature independence assumption",
        "Correlated features",
        "Continuous features (without binning)",
      ],
      problemTypes: ["binary_classification", "multiclass_classification"],
      description:
        "Fast probabilistic classifier based on Bayes theorem. Excellent for text classification and categorical data.",
      category: "probabilistic",
    },
    {
      name: "Ridge Regression",
      icon: "📐",
      complexity: "Low",
      needsScaling: true,
      speed: 0.96,
      accuracy: 0.78,
      strongWith: [
        "Multicollinearity",
        "Many correlated features",
        "Regularization",
        "Interpretability",
      ],
      weakWith: [
        "Non-linear patterns",
        "No feature selection",
        "Requires scaled features",
      ],
      problemTypes: ["regression"],
      description:
        "Linear regression with L2 regularization. Handles multicollinearity and prevents overfitting by shrinking coefficients.",
      category: "linear",
    },
    {
      name: "Lasso Regression",
      icon: "🎯",
      complexity: "Low",
      needsScaling: true,
      speed: 0.94,
      accuracy: 0.77,
      strongWith: [
        "Feature selection",
        "High-dimensional data",
        "Sparse models",
        "Interpretability",
      ],
      weakWith: [
        "Non-linear patterns",
        "Correlated features (unstable)",
        "May eliminate useful features",
      ],
      problemTypes: ["regression"],
      description:
        "Linear regression with L1 regularization. Automatically performs feature selection by setting irrelevant coefficients to zero.",
      category: "linear",
    },
  ];

  // Filter by problem type
  return allAlgorithms.filter((algo) =>
    algo.problemTypes.includes(problemType.value.type)
  );
};

// 🔧 COMPLETE REFACTORED getKeyParameters() FUNCTION

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

const selectAlgorithm = (algorithm) => {
  selectAlgorithmWithBackend(algorithm);
};

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

const showAlgorithmDetails = (algo) => {
  selectedAlgorithmInfo.value = getAlgorithmEducationalContent(algo);
};

const closeAlgorithmInfo = () => {
  selectedAlgorithmInfo.value = null;
};

const getAlgorithmEducationalContent = (algo) => {
  const educationalContent = {
    "Random Forest": {
      ...algo,
      detailedDescription:
        "Random Forest is an ensemble learning method that constructs multiple decision trees during training and outputs the mode (classification) or mean (regression) of their predictions. Each tree is trained on a random subset of data and features.",
      howItWorks:
        "Creates many decision trees using bootstrap aggregating (bagging). Each tree votes for a classification or predicts a value, and the forest combines these results. Random feature selection at each split reduces correlation between trees, improving accuracy.",
      whenToUse: [
        "When you have mixed numerical and categorical features",
        "When you need feature importance rankings",
        "When dealing with non-linear relationships",
        "When you want good performance without extensive tuning",
        "When overfitting is a concern (more resistant than single trees)",
      ],
      whenNotToUse: [
        "When interpretability is critical (complex to explain)",
        "When you have extremely high-dimensional data (>10,000 features)",
        "When real-time predictions are required (slower than single models)",
        "When working with very small datasets (<100 samples)",
      ],
      realWorldExamples: [
        "🏦 Credit Card Fraud Detection",
        "🏥 Disease Diagnosis",
        "📧 Email Spam Filtering",
        "💰 Stock Price Prediction",
        "🎮 Game AI Behavior",
      ],
    },

    XGBoost: {
      ...algo,
      detailedDescription:
        "XGBoost (Extreme Gradient Boosting) is an optimized distributed gradient boosting library. It builds trees sequentially, where each new tree corrects errors made by previous trees, using gradient descent optimization.",
      howItWorks:
        "Builds trees one at a time, focusing on samples that previous trees got wrong. Uses second-order gradients (Newton method) for optimization, includes regularization to prevent overfitting, and supports parallel processing for speed.",
      whenToUse: [
        "When you need the best possible accuracy on tabular data",
        "When competing in ML competitions (Kaggle favorite)",
        "When you have medium to large datasets (1K+ rows)",
        "When you can invest time in hyperparameter tuning",
        "When feature engineering is already done",
      ],
      whenNotToUse: [
        "When you need easily interpretable results",
        "When working with very small datasets (<500 rows)",
        "When training time is critical",
        "When you lack computational resources",
        "When simple baseline is needed first",
      ],
      realWorldExamples: [
        "🏆 Kaggle Competition Winning Models",
        "🎯 Click-Through Rate Prediction",
        "🏪 Customer Churn Prediction",
        "📈 Sales Forecasting",
        "🔍 Search Ranking Algorithms",
      ],
    },

    "Logistic Regression": {
      ...algo,
      detailedDescription:
        "Logistic Regression is a linear model for binary and multiclass classification that uses the logistic (sigmoid) function to predict probabilities. Despite its name, it's a classification algorithm.",
      howItWorks:
        "Learns a linear combination of features and applies a sigmoid function to output probabilities between 0 and 1. Uses maximum likelihood estimation to find optimal coefficients. Very fast and provides probability scores.",
      whenToUse: [
        "When you need a quick baseline model",
        "When interpretability is crucial (clear coefficient weights)",
        "When relationships between features and target are roughly linear",
        "When you need probability predictions",
        "When working with small to medium datasets",
      ],
      whenNotToUse: [
        "When relationships are highly non-linear",
        "When features have complex interactions",
        "When you need to capture complex patterns",
        "When features are not scaled (highly sensitive)",
        "When you have multicollinearity issues",
      ],
      realWorldExamples: [
        "💳 Credit Approval Systems",
        "📧 Email Spam Detection",
        "🏥 Medical Diagnosis (binary outcomes)",
        "🎓 Student Admission Prediction",
        "📱 Customer Conversion Prediction",
      ],
    },

    "Linear Regression": {
      ...algo,
      detailedDescription:
        "Linear Regression models the relationship between a dependent variable and one or more independent variables using a linear equation. It's the foundation of regression analysis.",
      howItWorks:
        "Finds the best-fitting straight line (hyperplane in multiple dimensions) through data points by minimizing the sum of squared residuals. Uses ordinary least squares (OLS) or gradient descent to find optimal coefficients.",
      whenToUse: [
        "When the relationship is genuinely linear",
        "When you need a simple, interpretable baseline",
        "When predictions need to be explainable",
        "When you want to understand feature impacts",
        "For quick exploratory analysis",
      ],
      whenNotToUse: [
        "When relationships are non-linear",
        "When data has many outliers (very sensitive)",
        "When features are highly correlated (multicollinearity)",
        "When you need to capture complex interactions",
        "When assumptions (normality, homoscedasticity) are violated",
      ],
      realWorldExamples: [
        "🏠 House Price Prediction (with features)",
        "💰 Salary Estimation",
        "📊 Sales Forecasting",
        "🌡️ Temperature Prediction",
        "📈 Stock Return Modeling",
      ],
    },

    "Support Vector Machine": {
      ...algo,
      detailedDescription:
        "SVM finds the optimal hyperplane that maximally separates different classes in high-dimensional space. It uses the 'kernel trick' to handle non-linear decision boundaries.",
      howItWorks:
        "Identifies support vectors (data points closest to decision boundary) and maximizes the margin between classes. Kernel functions (RBF, polynomial) transform data into higher dimensions where linear separation becomes possible.",
      whenToUse: [
        "When you have high-dimensional data",
        "When classes are clearly separable",
        "When working with small to medium datasets",
        "When you need non-linear decision boundaries",
        "When margin of separation matters",
      ],
      whenNotToUse: [
        "When you have very large datasets (>10K rows)",
        "When training time is critical",
        "When features are not scaled",
        "When data is very noisy",
        "When you need probability estimates",
      ],
      realWorldExamples: [
        "✍️ Handwriting Recognition",
        "🖼️ Image Classification",
        "🧬 Protein Classification",
        "📄 Text Categorization",
        "👤 Face Detection",
      ],
    },

    "K-Nearest Neighbors": {
      ...algo,
      detailedDescription:
        "KNN is a simple, instance-based learning algorithm that classifies new data points based on the majority vote of their 'k' nearest neighbors in the feature space.",
      howItWorks:
        "Stores all training data in memory. For prediction, it calculates distance to all training points, finds k nearest neighbors, and predicts based on majority class (classification) or average (regression). No explicit training phase.",
      whenToUse: [
        "When you need a simple baseline",
        "When decision boundaries are irregular",
        "When you have small datasets",
        "When training time doesn't matter",
        "When data is well-distributed",
      ],
      whenNotToUse: [
        "When you have large datasets (very slow predictions)",
        "When features have different scales (must normalize)",
        "When you have high-dimensional data (curse of dimensionality)",
        "When memory is limited (stores all training data)",
        "When real-time predictions are needed",
      ],
      realWorldExamples: [
        "🎬 Movie Recommendation Systems",
        "🏥 Patient Similarity Matching",
        "📸 Image Recognition",
        "🗺️ Location-Based Services",
        "📚 Document Classification",
      ],
    },

    "Decision Tree": {
      ...algo,
      detailedDescription:
        "Decision Trees create a tree-like model of decisions and their consequences. Each internal node represents a feature test, branches represent outcomes, and leaves represent class labels or values.",
      howItWorks:
        "Recursively splits data based on feature values that best separate classes (using Gini impurity or entropy). Creates branches until reaching stopping criteria (max depth, min samples). Easy to visualize and interpret.",
      whenToUse: [
        "When interpretability is paramount",
        "When you need to explain decisions to non-technical stakeholders",
        "When working with categorical features",
        "When you need to capture non-linear relationships",
        "When you want feature importance",
      ],
      whenNotToUse: [
        "When you need high accuracy (tends to overfit)",
        "When data is noisy",
        "When you want stable predictions (small data changes cause big tree changes)",
        "When you need smooth decision boundaries",
        "As a final production model (use Random Forest instead)",
      ],
      realWorldExamples: [
        "🏥 Medical Diagnosis Decision Support",
        "💳 Credit Risk Assessment",
        "🎯 Customer Segmentation",
        "🏦 Loan Approval Systems",
        "🌐 Website Navigation Optimization",
      ],
    },

    "Support Vector Regression": {
      ...algo,
      detailedDescription:
        "SVR extends Support Vector Machines to regression problems. It fits a function within an epsilon-insensitive tube, ignoring errors within the tube while penalizing larger deviations.",
      howItWorks:
        "Creates an epsilon-tube around predictions. Points within the tube have no penalty, while points outside contribute to the loss. Uses kernel trick for non-linear regression. Robust to outliers due to epsilon-insensitivity.",
      whenToUse: [
        "When you need robust regression (outlier resistance)",
        "When relationships are non-linear",
        "When you have small to medium datasets",
        "When feature space is high-dimensional",
        "When you need flexibility with kernel functions",
      ],
      whenNotToUse: [
        "When you have very large datasets (computationally expensive)",
        "When you need highly interpretable predictions",
        "When linear relationships are sufficient",
        "When training time is critical",
        "When you need probability distributions",
      ],
      realWorldExamples: [
        "📈 Stock Price Forecasting",
        "🌡️ Weather Prediction",
        "⚡ Energy Demand Forecasting",
        "🏠 Real Estate Valuation",
        "📊 Time Series Prediction",
      ],
    },

    "Naive Bayes": {
      ...algo,
      detailedDescription:
        "Naive Bayes is a probabilistic classifier based on Bayes' theorem. It assumes features are conditionally independent given the class (the 'naive' assumption), making it simple yet surprisingly effective.",
      howItWorks:
        "Calculates probability of each class given the features using Bayes' theorem: P(class|features) ∝ P(features|class) × P(class). Assumes feature independence, which simplifies calculation and makes it very fast.",
      whenToUse: [
        "When you need extremely fast training and prediction",
        "When working with text classification (spam detection)",
        "When you have small datasets",
        "When features are truly independent (or mostly)",
        "When you need probabilistic predictions",
        "When baseline model is needed quickly",
      ],
      whenNotToUse: [
        "When features are highly correlated (violates independence assumption)",
        "When you need the best possible accuracy",
        "When feature interactions are important",
        "When relationships are complex and non-linear",
        "When continuous features have complex distributions",
      ],
      realWorldExamples: [
        "📧 Email Spam Detection",
        "📄 Document Classification",
        "💭 Sentiment Analysis",
        "🏥 Medical Diagnosis Screening",
        "🔍 Search Engine Result Filtering",
      ],
    },

    "Ridge Regression": {
      ...algo,
      detailedDescription:
        "Ridge Regression is Linear Regression with L2 regularization. It adds a penalty term proportional to the square of coefficients, preventing overfitting by shrinking coefficients toward zero.",
      howItWorks:
        "Minimizes sum of squared residuals PLUS alpha × sum of squared coefficients. The regularization term discourages large coefficients, handling multicollinearity and preventing overfitting. Alpha controls regularization strength.",
      whenToUse: [
        "When you have multicollinearity (correlated features)",
        "When you have more features than samples",
        "When you want to prevent overfitting",
        "When all features are potentially relevant (doesn't eliminate features)",
        "When interpretability with regularization is needed",
      ],
      whenNotToUse: [
        "When you need automatic feature selection (use Lasso instead)",
        "When relationships are non-linear",
        "When most features are irrelevant",
        "When you don't have multicollinearity issues",
        "When a sparse model is desired",
      ],
      realWorldExamples: [
        "🏠 House Price Prediction (many correlated features)",
        "💰 Financial Risk Modeling",
        "🏥 Medical Cost Prediction",
        "📊 Economic Forecasting",
        "🔬 Gene Expression Analysis",
      ],
    },

    "Lasso Regression": {
      ...algo,
      detailedDescription:
        "Lasso (Least Absolute Shrinkage and Selection Operator) is Linear Regression with L1 regularization. It can shrink coefficients to exactly zero, performing automatic feature selection.",
      howItWorks:
        "Minimizes sum of squared residuals PLUS alpha × sum of absolute values of coefficients. L1 penalty creates sparse models by forcing some coefficients to zero, effectively selecting most important features. Creates interpretable models.",
      whenToUse: [
        "When you need automatic feature selection",
        "When you have high-dimensional data with many irrelevant features",
        "When you want a sparse, interpretable model",
        "When you suspect only few features are truly important",
        "When you want to identify key predictors",
      ],
      whenNotToUse: [
        "When all features are important (Ridge is better)",
        "When features are highly correlated (arbitrarily picks one)",
        "When relationships are non-linear",
        "When you need stable feature selection (sensitive to data changes)",
        "When interpretability of all features matters",
      ],
      realWorldExamples: [
        "🧬 Genomics (selecting important genes)",
        "💊 Drug Discovery (identifying key molecular features)",
        "📊 Marketing Analytics (finding key conversion drivers)",
        "🌐 Web Analytics (identifying important metrics)",
        "📝 Text Analysis (selecting informative words)",
      ],
    },
  };

  return educationalContent[algo.name] || algo;
};

const getAvailableMetrics = () => {
  if (problemType.value.type === "regression") {
    return [
      { value: "r2", label: "RÂ² Score" },
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
  return (
    featureEngineering.polynomial ||
    featureEngineering.pca ||
    featureEngineering.featureSelection
  );
};

const getFeatureEngineeringSummary = () => {
  const features = [];
  if (featureEngineering.polynomial) features.push("Polynomial");
  if (featureEngineering.pca) features.push("PCA");
  if (featureEngineering.featureSelection) features.push("Selection");
  return features.length > 0 ? features.join(", ") : "None";
};

const getAdvancedFeaturesCount = () => {
  let count = 0;
  if (selectedScaling.value !== "none") count++;
  if (hasFeatureEngineering()) count++;
  if (validationMethod.value !== "train_test_split") count++;
  return count;
};

const startTraining = async () => {
  if (!selectedAlgorithm.value) {
    alert("Please select an algorithm first");
    return;
  }

  try {
    // Save selection to Experiment Store
    experimentStore.setAlgorithm({
      name: selectedAlgorithm.value.name,
      type: selectedAlgorithm.value.type || 'classification', 
      params: hyperparameters 
    });
    
    // Save the REFINDED/DETECTED Problem Type
    if (problemType.value) {
        experimentStore.setProblemType(problemType.value);
    }
    
    // Also save simple ref for convenience if model-training needs specific object
    experimentStore.selectedAlgorithm = selectedAlgorithm.value;

    console.log("✅ Algorithm selected, navigating to model-training:", {
      algorithm: selectedAlgorithm.value.name,
      datasetId: datasetId.value
    });

    router.push({
      path: "/model-training",
      query: {
        datasetId: datasetId.value
      }
    });
  } catch (error) {
    console.error("❌ Error navigating to training:", error);
    alert("Error: " + error.message);
  }
};

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
  router.push("/advanced-preprocessing");
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
  // Handle object format (from preprocessingTracker.js)
  if (step && typeof step === 'object' && step.name) {
    return step.name;
  }
  
  // Handle string format
  if (typeof step === 'string') {
    // Map old key-based names to display names
    const steps = {
      columnSelection: "Column Selection",
      missingValues: "Missing Value Handling",
      duplicateRemoval: "Duplicate Removal",
      outlierHandling: "Outlier Handling",
      categoricalEncoding: "Categorical Encoding",
    };
    return steps[step] || step;
  }
  
  return 'Unknown Step';
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

// Validation Strategy Helper Functions
const getTrainRows = () => {
  return Math.round(datasetStats.value.rows * splitRatio.value);
};

const getTestRows = () => {
  return Math.round(datasetStats.value.rows * (1 - splitRatio.value));
};

const estimateKFoldTime = () => {
  const baseTime = (datasetStats.value.rows * datasetStats.value.features) / 10000;
  return (baseTime * cvFolds.value / 60).toFixed(1);
};

const estimateGridCombinations = () => {
  const densityMap = {
    coarse: 3,
    normal: 4,
    fine: 6
  };
  const valuesPerParam = densityMap[gridDensity.value] || 4;
  
  // Estimate based on typical algorithm parameters
  const numParams = selectedAlgorithm.value ? 4 : 4; // Most algorithms have 4-6 key params
  return Math.pow(valuesPerParam, numParams);
};

const estimateGridRuns = () => {
  return estimateGridCombinations() * gridSearchCVFolds.value;
};

const estimateGridSearchTime = () => {
  const baseTime = (datasetStats.value.rows * datasetStats.value.features) / 10000;
  const totalRuns = estimateGridRuns();
  return (baseTime * totalRuns / 60).toFixed(0);
};

const estimateRandomSearchTime = () => {
  const baseTime = (datasetStats.value.rows * datasetStats.value.features) / 10000;
  const totalRuns = randomSearchIterations.value * randomSearchCVFolds.value;
  return (baseTime * totalRuns / 60).toFixed(1);
};

const formatGridPreview = () => {
  if (!selectedAlgorithm.value) return "No algorithm selected";
  
  const algoName = selectedAlgorithm.value.name;
  const densityMap = {
    coarse: { min: 0.5, max: 2, count: 3 },
    normal: { min: 0.5, max: 2, count: 4 },
    fine: { min: 0.3, max: 3, count: 6 }
  };
  
  const density = densityMap[gridDensity.value];
  
  // Generate example grid based on algorithm
  if (algoName === "Random Forest") {
    const nEstimators = Array.from({length: density.count}, (_, i) => 
      Math.round(50 + (200 * i / (density.count - 1)))
    );
    const maxDepth = [5, 10, 15, 20, null].slice(0, density.count);
    
    return `n_estimators: [${nEstimators.join(', ')}]\nmax_depth: [${maxDepth.join(', ')}]\nmin_samples_split: [2, 5, 10]\nmin_samples_leaf: [1, 2, 4]`;
  } else if (algoName === "XGBoost") {
    return `n_estimators: [50, 100, 200, 300]\nlearning_rate: [0.01, 0.05, 0.1, 0.3]\nmax_depth: [3, 5, 7, 9]\nsubsample: [0.6, 0.8, 1.0]`;
  } else {
    return `Auto-generated grid based on\nyour hyperparameter selections\nand dataset characteristics`;
  }
};

const formatDistributionsPreview = () => {
  if (!selectedAlgorithm.value) return "No algorithm selected";
  
  const algoName = selectedAlgorithm.value.name;
  
  if (algoName === "Random Forest") {
    return `n_estimators: uniform(50, 500)\nmax_depth: choice([5, 10, 15, 20, None])\nmin_samples_split: uniform(2, 20)\nmin_samples_leaf: uniform(1, 10)`;
  } else if (algoName === "XGBoost") {
    return `n_estimators: uniform(50, 500)\nlearning_rate: loguniform(0.01, 1.0)\nmax_depth: choice([3, 5, 7, 9, 11])\nsubsample: uniform(0.5, 1.0)`;
  } else {
    return `Auto-generated distributions\nbased on your hyperparameters\nand algorithm characteristics`;
  }
};

// Lifecycle
onMounted(async () => {

  
  if (loadDataFromPreviousSteps()) {
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate loading
    initializeRecommendations();
    isLoading.value = false;
    
    // Log final loaded values
    console.log("📊 Final loaded values:");
    console.log("- Dataset rows:", datasetStats.value.rows);
    console.log("- Dataset features:", datasetStats.value.features);
    console.log("- Split ratio:", splitRatio.value);
    console.log("- Train rows:", getTrainRows());
    console.log("- Test rows:", getTestRows());
  }

  // ADD THIS: Check backend connection
  await checkBackendConnection();
});


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
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

@media (max-width: 1400px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }
}

.analysis-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 0;
  transition: all 0.3s ease;
  overflow: hidden;
}

.analysis-card:hover {
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 2rem;
  background: rgba(102, 126, 234, 0.05);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.card-header .card-icon {
  font-size: 1.5rem;
  margin: 0;
}

.card-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
  flex: 1;
}

.steps-badge {
  padding: 0.25rem 0.75rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Card Content */
.card-content {
  padding: 2rem;
  text-align: left;
}

/* Info Sections */
.info-section {
  margin-bottom: 1.5rem;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Problem Type Badge */
.problem-type-badge {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
}

/* Confidence Meter */
.confidence-meter {
  position: relative;
  height: 8px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.meter-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.meter-fill.high {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.meter-fill.medium {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.meter-fill.low {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.confidence-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #667eea;
}

/* Card Divider */
.card-divider {
  height: 1px;
  background: rgba(102, 126, 234, 0.1);
  margin: 1.5rem 0;
}

/* Target Details */
.target-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 0.875rem;
  color: #9ca3af;
}

.detail-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
}

/* Insight Box */
.insight-box {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
}

.insight-box svg {
  flex-shrink: 0;
  color: #6366f1;
  margin-top: 0.125rem;
}

.insight-box p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.6;
  color: #b3b3d1;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Feature Breakdown */
.feature-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.breakdown-label {
  font-size: 0.875rem;
  color: #9ca3af;
}

.breakdown-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
}

/* Preprocessing Timeline */
.preprocessing-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.timeline-marker {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.875rem;
}

.timeline-content {
  flex: 1;
  padding-top: 0.25rem;
}

.timeline-content h4 {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #ffffff;
}

/* No Preprocessing State */
.no-preprocessing {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.no-preprocessing svg {
  margin-bottom: 1rem;
  color: #6b7280;
}

.no-preprocessing p {
  margin: 0 0 0.5rem 0;
  font-size: 0.9375rem;
  color: #9ca3af;
}

.warning-note {
  font-size: 0.8125rem;
  color: #f59e0b;
  display: block;
}

/* Legacy styles for compatibility */
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
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #6366f1;
  text-align: center;  
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
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
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
  content: "";
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
  content: "";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

.card-footer {
  margin-top: auto;
  padding-top: 1rem;
}

.footer-buttons {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

/* Learn More Button */
.learn-more-btn {
  flex: 0 0 auto;
  padding: 0.75rem 1rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  color: #6366f1;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
}

.learn-more-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: #6366f1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.learn-more-btn svg {
  flex-shrink: 0;
}

/* Select Algorithm Button - Updated */
.select-algorithm-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.select-algorithm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.select-algorithm-btn.selected {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.select-algorithm-btn svg {
  flex-shrink: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer-buttons {
    flex-direction: column;
  }

  .learn-more-btn {
    flex: 1;
  }
}

.learn-icon {
  font-size: 1.2rem;
}

/* Modal Overlay */
.algorithm-info-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Modal Content */
.modal-content {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 20px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from { 
    transform: translateY(50px);
    opacity: 0;
  }
  to { 
    transform: translateY(0);
    opacity: 1;
  }
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  z-index: 1;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #fff;
}

.algo-icon {
  font-size: 2rem;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
}

.close-btn:hover {
  background: rgba(255, 59, 48, 0.3);
  transform: rotate(90deg);
}

/* Modal Body */
.modal-body {
  padding: 2rem;
}

/* Info Sections */
.info-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.info-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: #6366f1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-section.warning h3 {
  color: #f59e0b;
}

.info-section p {
  margin: 0;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.8);
}

/* Bullet Lists */
.bullet-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bullet-list li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.bullet-list li::before {
  content: "▸";
  position: absolute;
  left: 0;
  color: #6366f1;
  font-weight: bold;
}

.warning .bullet-list li::before {
  color: #f59e0b;
}

/* Example Tags */
.example-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
}

.example-tag {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 20px;
  font-size: 0.9rem;
  color: #fff;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.metric-item {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.5rem;
  text-align: center; 
}

.metric-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #6366f1;
  text-align: center; 
}

/* Pros & Cons Container */
.pros-cons-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.pros-section,
.cons-section {
  padding: 1.5rem;
  border-radius: 12px;
}

.pros-section {
  background: rgba(34, 197, 94, 0.05);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.pros-section h3 {
  color: #22c55e;
}

.pros-section .bullet-list li::before {
  color: #22c55e;
}

.cons-section {
  background: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.cons-section h3 {
  color: #ef4444;
}

.cons-section .bullet-list li::before {
  color: #ef4444;
}

/* Responsive Design */
@media (max-width: 768px) {
  .pros-cons-container {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    max-height: 95vh;
  }
  
  .modal-header h2 {
    font-size: 1.4rem;
  }
}

/* Configuration Section */
.config-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.params-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
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
  content: "";
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
  
}

.summary-item {
  display: flex;
  
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

/* Validation Strategy Section */
.validation-section {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.strategy-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.strategy-card {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.strategy-card:hover {
  border-color: rgba(102, 126, 234, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
}

.strategy-card.selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.15);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.strategy-card .card-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.strategy-card h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  line-height: 1.3;
}

.strategy-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.strategy-badge.fastest {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.strategy-badge.recommended {
  background: rgba(99, 102, 241, 0.2);
  color: #6366f1;
}

.strategy-badge.thorough {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.strategy-badge.efficient {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
}

.run-count {
  font-size: 0.8125rem;
  color: #9ca3af;
}

/* Configuration Panel */
.strategy-config-panel {
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.config-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.config-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #10b981;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.config-header svg {
  flex-shrink: 0;
}

.config-description {
  color: #b3b3d1;
  font-size: 0.875rem;
  margin: 0;
}

.config-estimate {
  color: #667eea;
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0;
}

.config-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-group-inline {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.option-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  min-width: 80px;
}

.radio-group {
  display: flex;
  gap: 0.75rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.radio-option:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.4);
}

.radio-option input[type="radio"] {
  accent-color: #667eea;
}

.radio-option input[type="radio"]:checked + span {
  color: #667eea;
  font-weight: 600;
}

.checkbox-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  color: #b3b3d1;
}

.checkbox-inline input[type="checkbox"] {
  accent-color: #667eea;
  width: 18px;
  height: 18px;
}

.slider-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.iterations-slider {
  flex: 1;
  height: 6px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 3px;
  outline: none;
  appearance: none;
}

.iterations-slider::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.iterations-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.slider-value {
  min-width: 40px;
  padding: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 6px;
  text-align: center;
  font-weight: 600;
  color: #ffffff;
  font-size: 0.875rem;
}

.view-details-btn {
  align-self: flex-start;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8125rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-details-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.grid-preview {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.grid-preview pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 0.8125rem;
  color: #10b981;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* Common Settings */
.common-settings {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.setting-item label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
}

.setting-item input[type="number"],
.setting-item select {
  flex: 1;
  padding: 0.75rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.875rem;
}

.setting-item input[type="number"]:focus,
.setting-item select:focus {
  outline: none;
  border-color: #667eea;
}

/* Responsive */
@media (max-width: 1200px) {
  .strategy-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .strategy-cards {
    grid-template-columns: 1fr;
  }
  
  .common-settings {
    flex-direction: column;
  }
  
  .option-group-inline {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
