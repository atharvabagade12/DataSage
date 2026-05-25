<template>
  <div class="landing-container">
    <!-- Ambient Glow Orbs -->
    <div class="ambient-glow">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
    </div>

    <!-- Navigation Header -->
    <header class="navbar" :class="{ scrolled: isScrolled }">
      <nav class="nav-content">
        <div class="nav-brand" @click="scrollToTop">
          <div class="brand-logo">
            <img
              src="@/assets/logo.jpeg"
              alt="DataSage Logo"
              class="logo-img"
            />
          </div>
          <h1 class="brand-title">DataSage</h1>
        </div>

        <div class="nav-links">
          <a class="nav-link" @click="scrollTo('features')">Features</a>
          <a class="nav-link" @click="scrollTo('how-it-works')">How It Works</a>
          <a class="nav-link" @click="scrollTo('about')">About</a>
          <a class="nav-link" @click="scrollTo('faq')">FAQ</a>
        </div>

        <div class="nav-actions">
          <button @click="goToLogin" class="nav-btn secondary">Sign In</button>
          <button @click="goToSignup" class="nav-btn primary">
            Get Started
          </button>
        </div>

        <button
          @click="toggleMobileMenu"
          class="mobile-menu-btn"
          :class="{ active: showMobileMenu }"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </nav>

      <!-- Mobile Navigation Drawer -->
      <transition name="fade">
        <div v-if="showMobileMenu" class="mobile-drawer" id="mobile-menu">
          <div class="drawer-links">
            <a class="drawer-link" @click="handleMobileMenuClick('features')"
              >Features</a
            >
            <a
              class="drawer-link"
              @click="handleMobileMenuClick('how-it-works')"
              >How It Works</a
            >
            <a class="drawer-link" @click="handleMobileMenuClick('about')"
              >About</a
            >
            <a class="drawer-link" @click="handleMobileMenuClick('faq')">FAQ</a>
            <div class="drawer-actions">
              <button @click="goToLogin" class="nav-btn secondary full-width">
                Sign In
              </button>
              <button @click="goToSignup" class="nav-btn primary full-width">
                Get Started Free
              </button>
            </div>
          </div>
        </div>
      </transition>
    </header>

    <!-- Hero Section -->
    <section class="hero-section" id="home">
      <div class="hero-grid-overlay"></div>

      <div class="hero-content-wrapper">
        <div class="hero-text-block">
          <div class="hero-badge animate-pulse">
            <span class="badge-dot"></span>
            <span class="badge-text"
              >Academic Research & No-Code ML Platform</span
            >
          </div>

          <h1 class="hero-title">
            The Unified <br />
            <span class="gradient-text">No-Code ML</span> Platform
          </h1>

          <p class="hero-subtitle">
            Empowering students, researchers, and data enthusiasts to transform
            raw datasets into high-performing machine learning models with zero
            coding required.
          </p>

          <div class="hero-actions">
            <button @click="goToSignup" class="cta-button primary">
              <span>🚀</span>
              <span>Build A Pipeline Free</span>
            </button>
            <button @click="watchDemo" class="cta-button secondary">
              <span>🎬</span>
              <span>Watch Platform Demo</span>
            </button>
          </div>

          <div class="trust-indicators">
            <div class="trust-badge">
              <span class="trust-icon">✓</span>
              <span>Zero Setup Required</span>
            </div>
            <div class="trust-badge">
              <span class="trust-icon">🎓</span>
              <span>Student & Researcher Friendly</span>
            </div>
            <div class="trust-badge">
              <span class="trust-icon">⚡</span>
              <span>Instant Local Training</span>
            </div>
          </div>
        </div>

        <!-- High-fidelity interactive pipeline preview -->
        <div class="hero-visual">
          <div class="glass-mockup">
            <div class="mockup-header">
              <div class="mockup-dots">
                <span class="dot-red"></span>
                <span class="dot-yellow"></span>
                <span class="dot-green"></span>
              </div>
              <div class="mockup-tab">
                <span class="tab-icon">⚙️</span>
                <span class="tab-title">datasage-pipeline</span>
              </div>
            </div>

            <div class="mockup-body">
              <div class="pipeline-horizontal">
                <!-- Node 1: Upload -->
                <div
                  class="horizontal-node"
                  :class="{ active: activePipelineStep >= 0 }"
                >
                  <div class="horizontal-icon-container">
                    <span class="node-emoji">📁</span>
                  </div>
                  <span class="node-name">Upload</span>
                  <span class="node-meta">CSV, Excel</span>
                </div>

                <div class="horizontal-connector">
                  <div
                    class="connector-fill"
                    :style="{ width: getConnectorProgress(0) + '%' }"
                  ></div>
                </div>

                <!-- Node 2: Clean -->
                <div
                  class="horizontal-node"
                  :class="{ active: activePipelineStep >= 1 }"
                >
                  <div class="horizontal-icon-container">
                    <span class="node-emoji">⚙️</span>
                  </div>
                  <span class="node-name">Preprocess</span>
                  <span class="node-meta">Encode & Scale</span>
                </div>

                <div class="horizontal-connector">
                  <div
                    class="connector-fill"
                    :style="{ width: getConnectorProgress(1) + '%' }"
                  ></div>
                </div>

                <!-- Node 3: Train -->
                <div
                  class="horizontal-node"
                  :class="{ active: activePipelineStep >= 2 }"
                >
                  <div class="horizontal-icon-container">
                    <span class="node-emoji">🚀</span>
                  </div>
                  <span class="node-name">Train</span>
                  <span class="node-meta">Multi-Algorithm</span>
                </div>

                <div class="horizontal-connector">
                  <div
                    class="connector-fill"
                    :style="{ width: getConnectorProgress(2) + '%' }"
                  ></div>
                </div>

                <!-- Node 4: Analyze -->
                <div
                  class="horizontal-node"
                  :class="{ active: activePipelineStep >= 3 }"
                >
                  <div class="horizontal-icon-container">
                    <span class="node-emoji">📈</span>
                  </div>
                  <span class="node-name">Visualize</span>
                  <span class="node-meta">Metrics & Plots</span>
                </div>
              </div>

              <!-- Interactive Demo Animation Area -->
              <div class="live-console">
                <div class="console-header">
                  <span
                    class="console-indicator"
                    :class="getConsoleIndicatorClass()"
                  ></span>
                  <span class="console-status-text">{{
                    getConsoleStatusText()
                  }}</span>
                </div>
                <div class="console-body">
                  <transition name="fade" mode="out-in">
                    <div :key="activePipelineStep" class="console-content">
                      <p
                        v-if="activePipelineStep === -1"
                        class="console-line text-muted"
                      >
                        Ready to initialize machine learning execution. Click
                        "Build A Pipeline" to begin.
                      </p>

                      <div
                        v-else-if="activePipelineStep === 0"
                        class="console-upload-state"
                      >
                        <p class="console-line text-cyan">
                          > Importing dataset: customer_churn.csv
                        </p>
                        <p class="console-line text-success">
                          > Loaded 1,245 rows successfully
                        </p>
                        <p class="console-line">
                          > Schema detected: 14 numerical, 4 categorical columns
                        </p>
                      </div>

                      <div
                        v-else-if="activePipelineStep === 1"
                        class="console-preprocess-state"
                      >
                        <p class="console-line text-purple">
                          > Starting data transformations...
                        </p>
                        <p class="console-line">
                          > Handle Missing Values: 122 missing values handled
                          using mean imputation
                        </p>
                        <p class="console-line text-success">
                          > Label encoded categorical fields & scaled features
                          using StandardScaler
                        </p>
                      </div>

                      <div
                        v-else-if="activePipelineStep === 2"
                        class="console-train-state"
                      >
                        <p class="console-line text-cyan">
                          > Initializing concurrent model fitting...
                        </p>
                        <div class="training-algorithms-preview">
                          <div class="algo-row">
                            <span>Random Forest:</span>
                            <div class="algo-bar">
                              <div
                                class="algo-bar-fill"
                                :style="{ width: modelAccuracyRF + '%' }"
                              ></div>
                            </div>
                            <span class="algo-acc"
                              >{{ modelAccuracyRF.toFixed(1) }}% Acc</span
                            >
                          </div>
                          <div class="algo-row">
                            <span>XGBoost Classifier:</span>
                            <div class="algo-bar">
                              <div
                                class="algo-bar-fill purple"
                                :style="{ width: modelAccuracyXGB + '%' }"
                              ></div>
                            </div>
                            <span class="algo-acc"
                              >{{ modelAccuracyXGB.toFixed(1) }}% Acc</span
                            >
                          </div>
                        </div>
                      </div>

                      <div
                        v-else-if="activePipelineStep === 3"
                        class="console-analyze-state"
                      >
                        <p class="console-line text-success">
                          > Execution complete! Exported joblib models.
                        </p>
                        <div class="metrics-visual-grid">
                          <div class="metric-mini-card">
                            <span class="m-val"
                              >{{ modelAccuracy.toFixed(1) }}%</span
                            >
                            <span class="m-label">Best Accuracy</span>
                          </div>
                          <div class="metric-mini-card">
                            <span class="m-val text-purple">0.96</span>
                            <span class="m-label">ROC AUC Score</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Bento Grid Features Section -->
    <section class="features-section reveal" id="features">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Everything You Need for End-to-End ML</h2>
          <p class="section-subtitle">
            DataSage packs the full data science lifecycle into a highly visual,
            fully automated web pipeline. Perfect for classrooms, researchers,
            and quick exploratory modeling.
          </p>
        </div>

        <div class="bento-grid">
          <!-- Card 1: Large (Preprocessing) -->
          <div class="bento-card large glass-panel reveal">
            <div class="card-glow"></div>
            <div class="bento-icon-wrapper">
              <svg
                class="bento-svg-icon"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4 19H20"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
                <path
                  d="M7 15V11"
                  stroke="url(#cyan-gradient)"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
                <path
                  d="M12 15V6"
                  stroke="url(#purple-gradient)"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
                <path
                  d="M17 15V9"
                  stroke="url(#cyan-gradient)"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
                <defs>
                  <linearGradient
                    id="cyan-gradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="0%" stop-color="#00F0FF" />
                    <stop offset="100%" stop-color="#3B82F6" />
                  </linearGradient>
                  <linearGradient
                    id="purple-gradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="0%" stop-color="#9D4EDD" />
                    <stop offset="100%" stop-color="#8A2BE2" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div class="bento-content">
              <h3 class="bento-title">Smart Data Processing</h3>
              <p class="bento-desc">
                Drag and drop your raw files. DataSage instantly performs
                intelligent data profiling, auto-detects structural schemas,
                flags null imbalances, and builds a comprehensive data-quality
                summary in real-time.
              </p>
              <div class="bento-preview-box prep-preview">
                <div class="quality-score-radial">
                  <span class="radial-num">98%</span>
                  <span class="radial-lbl">Data Health Score</span>
                </div>
                <div class="issues-list">
                  <div class="issue-item">
                    <span class="bullet red"></span
                    ><span>24 missing age values auto-imputed</span>
                  </div>
                  <div class="issue-item">
                    <span class="bullet green"></span
                    ><span>4 categorical fields standard encoded</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 2: Medium (Automated Training) -->
          <div class="bento-card medium glass-panel reveal">
            <div class="card-glow"></div>
            <div class="bento-icon-wrapper">
              <svg
                class="bento-svg-icon"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  x="3"
                  y="11"
                  width="18"
                  height="10"
                  rx="3"
                  stroke="url(#purple-gradient)"
                  stroke-width="2"
                />
                <path
                  d="M12 2V5"
                  stroke="#00F0FF"
                  stroke-width="2"
                  stroke-linecap="round"
                />
                <circle cx="12" cy="2" r="1.5" fill="#00F0FF" />
                <path
                  d="M8 15H8.01"
                  stroke="#00F0FF"
                  stroke-width="3"
                  stroke-linecap="round"
                />
                <path
                  d="M16 15H16.01"
                  stroke="#00F0FF"
                  stroke-width="3"
                  stroke-linecap="round"
                />
                <path
                  d="M9 18H15"
                  stroke="url(#purple-gradient)"
                  stroke-width="2"
                  stroke-linecap="round"
                />
                <path
                  d="M3 15H2"
                  stroke="url(#purple-gradient)"
                  stroke-width="2"
                  stroke-linecap="round"
                />
                <path
                  d="M22 15H21"
                  stroke="url(#purple-gradient)"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <div class="bento-content">
              <h3 class="bento-title">Automated ML Pipeline</h3>
              <p class="bento-desc">
                Deploy diverse algorithms concurrently. We run Random Forest,
                SVMs, Decision Trees, K-Neighbors, and XGBoost with automated
                grid hyperparameter validation.
              </p>
              <div class="bento-preview-box train-preview">
                <div class="mini-chart-row">
                  <span class="c-title">SVM</span>
                  <span class="c-value">91.4% Acc</span>
                </div>
                <div class="mini-chart-row highlight-cyan">
                  <span class="c-title">Random Forest</span>
                  <span class="c-value">95.2% Acc</span>
                </div>
                <div class="mini-chart-row">
                  <span class="c-title">XGBoost</span>
                  <span class="c-value">94.8% Acc</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 3: Medium (Imbalance & Scale) -->
          <div class="bento-card medium glass-panel reveal">
            <div class="card-glow"></div>
            <div class="bento-icon-wrapper">
              <svg
                class="bento-svg-icon"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                  stroke="url(#cyan-gradient)"
                  stroke-width="2"
                />
                <path
                  d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"
                  stroke="url(#cyan-gradient)"
                  stroke-width="2"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <div class="bento-content">
              <h3 class="bento-title">Advanced Feature Engineering</h3>
              <p class="bento-desc">
                Resolve real-world data issues directly. Handle class imbalances
                with synthetic SMOTE oversampling, apply robust label/one-hot
                encoding, clean extreme outliers, and normalize columns with
                different scalers.
              </p>
              <div class="bento-preview-box spec-preview">
                <div class="pill-group">
                  <span class="glow-pill cyan">SMOTE Oversampling</span>
                  <span class="glow-pill purple">Standard Scaler</span>
                  <span class="glow-pill">One-Hot Encoding</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 4: Large (Visualizations) -->
          <div class="bento-card large glass-panel reveal">
            <div class="card-glow"></div>
            <div class="bento-icon-wrapper">
              <svg
                class="bento-svg-icon"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M3 3V21H21"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M18.5 7.5L13.5 12.5L9.5 8.5L4.5 13.5"
                  stroke="url(#cyan-gradient)"
                  stroke-width="2.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <circle
                  cx="18.5"
                  cy="7.5"
                  r="2"
                  fill="#9D4EDD"
                  stroke="#ffffff"
                  stroke-width="1"
                />
                <circle
                  cx="13.5"
                  cy="12.5"
                  r="2"
                  fill="#00F0FF"
                  stroke="#ffffff"
                  stroke-width="1"
                />
                <circle
                  cx="9.5"
                  cy="8.5"
                  r="2"
                  fill="#9D4EDD"
                  stroke="#ffffff"
                  stroke-width="1"
                />
              </svg>
            </div>
            <div class="bento-content">
              <h3 class="bento-title">Interactive Visualizations</h3>
              <p class="bento-desc">
                Experience crystal clear model transparency. Interactively study
                Pearson feature correlation heatmaps, plot classification
                margins, evaluate model matrices, and track training residuals
                with Chart.js dashboards.
              </p>
              <div class="bento-preview-box chart-preview">
                <div class="heatmap-mock">
                  <div class="heat-cell h-high"></div>
                  <div class="heat-cell h-med"></div>
                  <div class="heat-cell h-low"></div>
                  <div class="heat-cell h-med"></div>
                  <div class="heat-cell h-high"></div>
                  <div class="heat-cell h-low"></div>
                  <div class="heat-cell h-low"></div>
                  <div class="heat-cell h-med"></div>
                  <div class="heat-cell h-high"></div>
                </div>
                <div class="heatmap-legend">
                  <span>-1.0</span>
                  <span class="grad-bar"></span>
                  <span>+1.0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section (Interactive Workflow Canvas Redesign) -->
    <section class="how-it-works-section reveal" id="how-it-works">
      <div class="canvas-grid-overlay"></div>

      <!-- Faint neural background line graphics -->
      <div class="neural-bg-graphics">
        <svg
          class="neural-bg-svg"
          viewBox="0 0 1000 800"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M100 100 L300 200 L500 150 L450 460 L800 600 L900 400"
            stroke="rgba(255, 255, 255, 0.01)"
            stroke-width="1.5"
          />
          <path
            d="M200 650 L350 460 L150 200"
            stroke="rgba(255, 255, 255, 0.01)"
            stroke-width="1.5"
          />
          <path
            d="M850 700 L450 460 L700 200"
            stroke="rgba(255, 255, 255, 0.01)"
            stroke-width="1.5"
          />
        </svg>
      </div>

      <div class="canvas-ambient-glow orb-cyan"></div>
      <div class="canvas-ambient-glow orb-purple"></div>

      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">From Raw Data to Intelligent Models</h2>
          <p class="section-subtitle">
            An intelligent end-to-end machine learning workflow designed to
            simplify preprocessing, training, and diagnostics through a visual
            AI-powered pipeline.
          </p>
        </div>

        <!-- Workflow Canvas Container -->
        <div class="workflow-canvas">
          <!-- Central Simple Single Vertical Connection Path -->
          <div class="canvas-spine-container">
            <svg
              class="canvas-spine-svg"
              viewBox="0 0 100 800"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <!-- Static subtle path -->
              <path
                d="M50 0 V800"
                stroke="rgba(255, 255, 255, 0.05)"
                stroke-width="2"
                stroke-linecap="round"
              />
              <!-- Glowing neon pulse path -->
              <path
                class="pulse-line"
                d="M50 0 V800"
                stroke="url(#spine-pulse-gradient)"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-dasharray="25 180"
              />
              <defs>
                <linearGradient
                  id="spine-pulse-gradient"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
                  <stop offset="50%" stop-color="#3B82F6" stop-opacity="1" />
                  <stop offset="100%" stop-color="#9D4EDD" stop-opacity="0" />
                </linearGradient>
              </defs>
            </svg>
            <!-- Flowing neon particles -->
            <div class="flowing-particle pt-1"></div>
            <div class="flowing-particle pt-2"></div>
          </div>

          <!-- Nodes container -->
          <div class="canvas-nodes">
            <!-- Node 1: Upload Dataset -->
            <div class="canvas-node glass-panel reveal" id="node-upload">
              <!-- Infrastructure Telemetry Ribbon -->
              <div class="node-telemetry">
                <span class="tel-item"
                  ><span class="tel-dot green"></span> NODE_01 //
                  INGESTION</span
                >
                <span class="tel-item">SYS_STATUS: ONLINE</span>
                <span class="tel-item">LATENCY: 14ms</span>
                <span class="tel-item">SPEED: 4.2 MB/s</span>
              </div>

              <div class="node-header">
                <div class="node-icon-box">
                  <svg
                    class="node-svg-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M12 15V3M12 3L8 7M12 3L16 7"
                      stroke="#00F0FF"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M20 17V18.5C20 19.8807 18.8807 21 17.5 21H6.5C5.11929 21 4 19.8807 4 18.5V17"
                      stroke="#00F0FF"
                      stroke-width="2"
                      stroke-linecap="round"
                    />
                  </svg>
                </div>
                <div class="node-meta-info">
                  <span class="node-number">STEP 01</span>
                  <h3 class="node-title">Upload Dataset</h3>
                </div>
              </div>
              <p class="node-desc">
                Simply drag and drop your raw files. Instantly parse schemas,
                map columns, and ingest rows to the server.
              </p>

              <!-- Mini visualizer for Upload -->
              <div class="node-visualizer upload-visualizer">
                <div class="upload-progress-ring">
                  <span class="file-icon">📁</span>
                  <span class="upload-badge">1.2k rows</span>
                </div>
                <div class="visual-table-rows">
                  <!-- Shimmer overlay -->
                  <div class="scan-shimmer"></div>
                  <div class="table-row-stream tr-1">
                    <span>120</span><span>"customer_churn"</span
                    ><span>0.98</span><span>True</span>
                  </div>
                  <div class="table-row-stream tr-2">
                    <span>121</span><span>"customer_churn"</span
                    ><span>0.34</span><span>False</span>
                  </div>
                  <div class="table-row-stream tr-3">
                    <span>122</span><span>"customer_churn"</span
                    ><span>0.56</span><span>True</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Node 2: Interactive Cleanse -->
            <div class="canvas-node glass-panel reveal" id="node-cleanse">
              <!-- Infrastructure Telemetry Ribbon -->
              <div class="node-telemetry">
                <span class="tel-item"
                  ><span class="tel-dot green"></span> NODE_02 // CLEANSE</span
                >
                <span class="tel-item">SYS_STATUS: SYNCED</span>
                <span class="tel-item">LATENCY: 28ms</span>
                <span class="tel-item">SCAN_RATE: 99.8%</span>
              </div>

              <div class="node-header">
                <div class="node-icon-box orange-glow">
                  <svg
                    class="node-svg-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M19.5 10.5C21.3787 12.3787 21.3787 15.4213 19.5 17.3M17 8C18.5 9.5 18.5 11.5 17 13M12.5 15C13.5 16 13.5 17.5 12.5 18.5M10.5 4L4 10.5M15.5 9L9 15.5"
                      stroke="#f59e0b"
                      stroke-width="2"
                      stroke-linecap="round"
                    />
                  </svg>
                </div>
                <div class="node-meta-info">
                  <span class="node-number">STEP 02</span>
                  <h3 class="node-title">Interactive Cleanse</h3>
                </div>
              </div>
              <p class="node-desc">
                Clean null items, remove duplicates, handle outliers, and scale
                numeric rows dynamically.
              </p>

              <!-- Mini visualizer for Cleanse -->
              <div class="node-visualizer cleanse-visualizer">
                <div class="null-grid-simulator">
                  <!-- Laser scanning sweep bar -->
                  <div class="sweeper-laser-beam"></div>
                  <span class="grid-cell filled"></span>
                  <span class="grid-cell filled"></span>
                  <span class="grid-cell imputed pulsing-green">NaN</span>
                  <span class="grid-cell filled"></span>
                  <span class="grid-cell filled"></span>
                  <span class="grid-cell filled"></span>
                  <span class="grid-cell imputed pulsing-green">NaN</span>
                  <span class="grid-cell filled"></span>
                </div>
                <div class="smote-ratio-bar">
                  <span class="ratio-label">SMOTE balance ratio: 1:1</span>
                  <div class="ratio-progress">
                    <div class="progress-fill green-gradient"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Node 3: Automated Training -->
            <div class="canvas-node glass-panel reveal" id="node-train">
              <!-- Infrastructure Telemetry Ribbon -->
              <div class="node-telemetry">
                <span class="tel-item"
                  ><span class="tel-dot green"></span> NODE_03 // AUTO_ML</span
                >
                <span class="tel-item">SYS_STATUS: TRAINING</span>
                <span class="tel-item">LATENCY: 42ms</span>
                <span class="tel-item">GPU_LOAD: 88%</span>
              </div>

              <div class="node-header">
                <div class="node-icon-box purple-glow">
                  <svg
                    class="node-svg-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M12 2L2 22H22L12 2Z"
                      stroke="#9D4EDD"
                      stroke-width="2"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M12 6L16 18H8L12 6Z"
                      stroke="#00F0FF"
                      stroke-width="1.5"
                      stroke-linejoin="round"
                    />
                  </svg>
                </div>
                <div class="node-meta-info">
                  <span class="node-number">STEP 03</span>
                  <h3 class="node-title">Automated Training</h3>
                </div>
              </div>
              <p class="node-desc">
                Deploy diverse classifiers concurrently. Monitor weights and
                parameter updates with real-time feedback loops.
              </p>

              <!-- Mini visualizer for Training -->
              <div
                class="node-visualizer train-visualizer active-visualizer-bg"
              >
                <div class="neural-activity-visualizer">
                  <div class="algo-chip cyan">
                    RF: <span class="live-acc">95.2%</span>
                  </div>
                  <div class="algo-chip purple">
                    SVM: <span class="live-acc">91.4%</span>
                  </div>
                  <div class="algo-chip active-chip-glowing">
                    XGB: <span class="live-acc-pulsing">94.8%</span>
                  </div>
                </div>
                <!-- Mini fitting line chart -->
                <div class="training-line-chart">
                  <svg class="fitting-line-svg" viewBox="0 0 100 40">
                    <path
                      class="fitting-line-path"
                      d="M0 38 Q 20 20, 40 15 T 80 5 T 100 2"
                      fill="none"
                      stroke="#00F0FF"
                      stroke-width="2"
                    />
                    <circle
                      cx="100"
                      cy="2"
                      r="3"
                      fill="#00F0FF"
                      class="pulsing-endpoint"
                    />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Node 4: Model Diagnostics -->
            <div class="canvas-node glass-panel reveal" id="node-diagnose">
              <!-- Infrastructure Telemetry Ribbon -->
              <div class="node-telemetry">
                <span class="tel-item"
                  ><span class="tel-dot green"></span> NODE_04 //
                  DIAGNOSTICS</span
                >
                <span class="tel-item">SYS_STATUS: COMPLETE</span>
                <span class="tel-item">LATENCY: 8ms</span>
                <span class="tel-item">EXPORT: JOBLIB</span>
              </div>

              <div class="node-header">
                <div class="node-icon-box pink-glow">
                  <svg
                    class="node-svg-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M3 12H7L10 19L14 5L17 12H21"
                      stroke="#ec4899"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </div>
                <div class="node-meta-info">
                  <span class="node-number">STEP 04</span>
                  <h3 class="node-title">Model Diagnostics</h3>
                </div>
              </div>
              <p class="node-desc">
                Examine ROC curves, study detailed confusion matrices, evaluate
                metrics, and export finished joblib pipelines.
              </p>

              <!-- Mini visualizer for Diagnostics -->
              <div class="node-visualizer diagnose-visualizer">
                <div class="mini-confusion-matrix">
                  <div class="matrix-cell tp">
                    TP<span class="val">84</span>
                  </div>
                  <div class="matrix-cell fp">FP<span class="val">4</span></div>
                  <div class="matrix-cell fn">FN<span class="val">2</span></div>
                  <div class="matrix-cell tn">
                    TN<span class="val">78</span>
                  </div>
                </div>
                <div class="diagnose-download-badge">
                  <span class="download-icon-pulse">📥</span>
                  <span class="download-lbl"
                    >Download model.joblib
                    <span class="blinking-cursor">_</span></span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="about-section reveal" id="about">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">About The Platform</h2>
          <p class="section-subtitle">
            An open-source, student-built research tool created to break down
            barriers to data science literacy.
          </p>
        </div>

        <div class="about-cards-grid">
          <div class="about-card-premium glass-panel reveal">
            <div class="about-glow color-cyan"></div>
            <div class="about-premium-icon">🎯</div>
            <h3 class="about-premium-title">The Academic Mission</h3>
            <p class="about-premium-desc">
              DataSage bridges the gap between machine learning formulas and
              practical application. We engineered an accessible interface
              enabling you to upload data, scale parameters, compile algorithms,
              and critique models without standard programming friction.
            </p>
          </div>

          <div class="about-card-premium glass-panel reveal">
            <div class="about-glow color-purple"></div>
            <div class="about-premium-icon">🎓</div>
            <h3 class="about-premium-title">Built with True Engineering</h3>
            <p class="about-premium-desc">
              Designed and implemented entirely from scratch as a final-year
              project. We avoided generic quick-fix templates, constructing a
              highly resilient pipeline using Nuxt 3, custom CSS variables, and
              powerful backend libraries.
            </p>
          </div>

          <div class="about-card-premium glass-panel reveal">
            <div class="about-glow color-blue"></div>
            <div class="about-premium-icon">🌍</div>
            <h3 class="about-premium-title">100% Free & Open Source</h3>
            <p class="about-premium-desc">
              Committed to keeping learning open to everyone. No hidden monthly
              limits, no high premium subscription lockouts. You can research
              freely, study core ML workflows, and inspect the open-source
              pipeline integrity anytime.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section reveal" id="faq">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="section-subtitle">
            Answers to common questions regarding technical features, security,
            and open-source availability.
          </p>
        </div>

        <div class="faq-accordion-list">
          <div
            class="faq-accordion-card glass-panel"
            v-for="(item, index) in faqItems"
            :key="index"
            :class="{ expanded: openFaqIndex === index }"
          >
            <button class="faq-trigger" @click="toggleFaq(index)">
              <span class="faq-question-text">{{ item.question }}</span>
              <span class="faq-indicator-icon"></span>
            </button>
            <transition name="slide-fade">
              <div class="faq-content-pane" v-show="openFaqIndex === index">
                <p class="faq-answer-text">{{ item.answer }}</p>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </section>

    <!-- Final Call to Action Section -->
    <section class="cta-section reveal">
      <div class="cta-backdrop-glow"></div>
      <div class="section-container">
        <h2 class="cta-header-title">Ready to Experience Data Sage?</h2>
        <p class="cta-header-subtitle">
          Accelerate your data science journey or classroom assignments today.
          No installation, no setup, pure machine learning instantly.
        </p>

        <div class="cta-action-holder">
          <button @click="goToSignup" class="cta-button primary large glow">
            <span>🚀</span>
            <span>Get Started For Free</span>
          </button>
        </div>

        <div class="cta-support-badges">
          <div class="support-badge">
            <span class="badge-check">✓</span><span>Free Dataset Previews</span>
          </div>
          <div class="support-badge">
            <span class="badge-check">✓</span
            ><span>Cross-Validation Support</span>
          </div>
          <div class="support-badge">
            <span class="badge-check">✓</span
            ><span>Full Confusion Matrices</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col brand-col">
          <div class="footer-logo-wrap">
            <div class="brand-logo">
              <img
                src="@/assets/logo.jpeg"
                alt="DataSage Logo"
                class="logo-img"
              />
            </div>
            <h3 class="footer-brand-title">DataSage</h3>
          </div>
          <p class="footer-brand-desc">
            Transform raw structured data into production-ready insights using
            our state-of-the-art visual ML platform.
          </p>
          <div class="footer-socials">
            <a
              href="https://www.linkedin.com/in/atharva-bagade-85813528b/"
              target="_blank"
              rel="noopener noreferrer"
              class="social-icon"
              >LN</a
            >
            <a class="social-icon">GH</a>
          </div>
        </div>

        <div class="footer-col">
          <h4 class="footer-col-title">Platform</h4>
          <ul class="footer-links-list">
            <li><a @click="scrollTo('features')">Features</a></li>
            <li><a @click="scrollTo('how-it-works')">How It Works</a></li>
            <li><a @click="goToLogin">Get Started</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4 class="footer-col-title">Academic</h4>
          <ul class="footer-links-list">
            <li><a @click="scrollTo('about')">About Project</a></li>
            <li><a>GitHub Repository</a></li>
            <li>
              <a
                href="https://www.irjet.net/archives/V12/i11/IRJET-V12I1139.pdf"
                target="_blank"
                rel="noopener noreferrer"
                >Research Paper</a
              >
            </li>
          </ul>
        </div>

        <div class="footer-col">
          <h4 class="footer-col-title">Support</h4>
          <ul class="footer-links-list">
            <li><a href="mailto:[EMAIL_ADDRESS]">Contact Team</a></li>
            <li><a @click="scrollTo('faq')">FAQs</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-credits">
        <p>
          &copy; 2025–2026 DataSage. Built with ❤️ for educational and research
          excellence.
        </p>
      </div>
    </footer>

    <!-- Demo Modal -->
    <transition name="fade">
      <div v-if="showDemoModal" class="demo-modal" @click="closeDemoModal">
        <div class="demo-modal-content glass-panel" @click.stop>
          <button @click="closeDemoModal" class="demo-modal-close-btn">
            &times;
          </button>
          <h3 class="modal-title-text">DataSage Platform Demo</h3>
          <div class="modal-body-content">
            <div class="modal-demo-icon">🎬</div>
            <p class="modal-text-lead">Interactive visual demo coming soon!</p>
            <p class="modal-text-sub">
              We are working on bringing a guided tutorial experience here. In
              the meantime, you can sign up or log in to explore the live
              workspace instantly.
            </p>
          </div>
          <button @click="goToSignup" class="modal-action-btn">
            Launch Platform Workspace
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

// Nuxt SEO and Meta Optimization
useHead({
  title:
    "DataSage - Premium No-Code Machine Learning Platform | Final Year Project",
  meta: [
    {
      name: "description",
      content:
        "Explore DataSage, the state-of-the-art unified no-code machine learning platform designed for students, educators, and researchers. Clean datasets, train algorithms, and visualize performance interactively.",
    },
    {
      name: "keywords",
      content:
        "machine learning, data science, student project, no-code, ML pipeline, hyperparameter tuning, data cleaning, SMOTE, VueJS, Nuxt 3",
    },
    { property: "og:title", content: "DataSage - No-Code ML Platform" },
    {
      property: "og:description",
      content:
        "Interactive, student-built machine learning pipeline. Free for classroom and research work.",
    },
    { property: "og:type", content: "website" },
  ],
});

// Navigation & Interactive UI States
const isScrolled = ref(false);
const showMobileMenu = ref(false);
const showDemoModal = ref(false);
const openFaqIndex = ref(null);

// Pipeline Animation States
const activePipelineStep = ref(-1);
const pipelineProgress = ref(0);
const modelAccuracy = ref(94.2);
const modelAccuracyRF = ref(70);
const modelAccuracyXGB = ref(60);

// Predefined Data Assets
const features = ref([
  {
    id: 1,
    icon: "📊",
    title: "Smart Data Processing",
    description:
      "Upload raw CSV or Excel sheets. Our profile analyser structures schemas, handles data quality profiling, and suggests scaling steps.",
    highlights: [],
  },
  {
    id: 2,
    icon: "🤖",
    title: "Automated ML Pipeline",
    description:
      "Train classification or regression models concurrently. Includes automated hyperparameter grids and validation partitioning.",
    highlights: [],
  },
]);

const steps = ref([
  {
    id: 1,
    icon: "📁",
    title: "Upload Dataset",
    description:
      "Simply drag and drop your structured CSV or Excel dataset. The platform immediately auto-detects rows, columns, data types, and quality defects.",
  },
  {
    id: 2,
    icon: "⚙️",
    title: "Interactive Cleanse",
    description:
      "Apply scale normalization, fix imbalanced labels via SMOTE oversampling, resolve empty rows, and encode categories with simple visual settings.",
  },
  {
    id: 3,
    icon: "🚀",
    title: "Automated Training",
    description:
      "Run Random Forest, SVM, XGBoost, Decision Trees, and K-Neighbors simultaneously. View live training metrics as hyperparameter weights tune.",
  },
  {
    id: 4,
    icon: "📈",
    title: "Model Diagnostics",
    description:
      "Compare algorithms with detailed metrics. Study interactive confusion matrices, precision/recall curves, and download completed joblib files.",
  },
]);

const faqItems = ref([
  {
    question: "Is DataSage completely free to use?",
    answer:
      "Yes, 100%! DataSage was created as an educational final-year engineering project. It is fully open-source and free from hidden tiers, commercial subscription limits, or feature locking.",
  },

  {
    question: "Do I need any programming experience?",
    answer:
      "None whatsoever. The interface is meticulously designed to abstract Python libraries like scikit-learn, category_encoders, and imblearn, letting you control full ML execution with intuitive visual controls.",
  },

  {
    question: "Can I use my own datasets?",
    answer:
      "Absolutely. You can upload any structured dataset in CSV or Excel format. DataSage also provides sample datasets if you want to explore the platform first. ",
  },

  {
    question: "What dataset formats are supported?",
    answer:
      "DataSage currently supports structured tabular data in CSV (.csv) and Excel (.xlsx) file formats. You can drag and drop your datasets directly into the dashboard upload zone.",
  },

  {
    question: "Which machine learning models are available?",
    answer:
      "We support standard supervised algorithms: Random Forest, Support Vector Machines (SVM), Extreme Gradient Boosting (XGBoost), K-Nearest Neighbors (KNN), Decision Trees, and Logistic/Linear Regression.",
  },

  {
    question: "How is data security handled?",
    answer:
      "Data Sage executes processing files securely inside active database/session memories. Your local CSV data remains private and is never distributed or sold to third-party networks.",
  },
]);

// Navigation Methods
const scrollToTop = () => {
  if (process.client) window.scrollTo({ top: 0, behavior: "smooth" });
};

const scrollTo = (elementId) => {
  if (process.client) {
    const el = document.getElementById(elementId);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  }
};

const goToLogin = async () => {
  try {
    await navigateTo("/login");
  } catch (err) {
    if (process.client) window.location.href = "/login";
  }
};

const goToSignup = async () => {
  try {
    await navigateTo("/login#signup");
  } catch (err) {
    if (process.client) window.location.href = "/login#signup";
  }
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

const handleMobileMenuClick = async (section) => {
  showMobileMenu.value = false;
  scrollTo(section);
};

// Modal Control
const watchDemo = () => {
  showDemoModal.value = true;
};
const closeDemoModal = () => {
  showDemoModal.value = false;
};

// FAQ Accordion Control
const toggleFaq = (index) => {
  openFaqIndex.value = openFaqIndex.value === index ? null : index;
};

// Scroll detection helper
const handleScroll = () => {
  if (process.client) {
    isScrolled.value = window.scrollY > 40;
  }
};

// Helper calculation for interactive horizontal pipeline connector fill
const getConnectorProgress = (connectorIndex) => {
  if (activePipelineStep.value < connectorIndex) return 0;
  if (activePipelineStep.value > connectorIndex) return 100;
  return pipelineProgress.value;
};

// Live interactive console states
const getConsoleStatusText = () => {
  if (activePipelineStep.value === -1) return "System Status: Idle";
  if (activePipelineStep.value === 0)
    return "System Status: Parsing customer_churn.csv";
  if (activePipelineStep.value === 1)
    return "System Status: Running balancing algorithms";
  if (activePipelineStep.value === 2)
    return "System Status: Training parallel estimators";
  if (activePipelineStep.value === 3)
    return "System Status: Compiling precision matrix";
  return "System Status: Idle";
};

const getConsoleIndicatorClass = () => {
  if (activePipelineStep.value === -1) return "idle";
  if (activePipelineStep.value === 3) return "success";
  return "busy";
};

// High-fidelity pipeline simulator lifecycle
let pipelineCycleInterval = null;

const initPipelineSimulator = () => {
  if (!process.client) return;

  const nodesCount = 4;
  const nodeDuration = 3500; // duration spent per node in ms
  let elapsed = 0;
  const tick = 100;
  let isIdlePause = false;

  pipelineCycleInterval = setInterval(() => {
    if (isIdlePause) return;

    elapsed += tick;
    const totalCycleTime = nodesCount * nodeDuration;

    if (elapsed >= totalCycleTime) {
      // Completed full pipeline iteration, pause on the final validation visual, then reset
      activePipelineStep.value = 3;
      pipelineProgress.value = 100;
      isIdlePause = true;

      setTimeout(() => {
        activePipelineStep.value = -1;
        pipelineProgress.value = 0;
        modelAccuracyRF.value = 70;
        modelAccuracyXGB.value = 60;
        elapsed = 0;
        isIdlePause = false;
      }, 2500);
      return;
    }

    const currentProgressPercentage =
      ((elapsed % nodeDuration) / nodeDuration) * 100;
    const currentNodeIdx = Math.floor(elapsed / nodeDuration);

    activePipelineStep.value = currentNodeIdx;
    pipelineProgress.value = currentProgressPercentage;

    // Micro bar animation inside model training simulation
    if (currentNodeIdx === 2) {
      modelAccuracyRF.value = Math.min(
        70 + (currentProgressPercentage / 100) * 25.2,
        95.2,
      );
      modelAccuracyXGB.value = Math.min(
        60 + (currentProgressPercentage / 100) * 34.8,
        94.8,
      );
    }
  }, tick);
};

// Scroll reveal observer API
let scrollRevealObserver = null;
let nodeScrollObserver = null;

const initScrollReveal = () => {
  if (!process.client) return;

  const options = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  scrollRevealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("active");
        scrollRevealObserver.unobserve(entry.target);
      }
    });
  }, options);

  document.querySelectorAll(".reveal").forEach((el) => {
    scrollRevealObserver.observe(el);
  });

  // Guided storytelling observer for canvas workflow nodes
  const nodeOptions = {
    threshold: 0.25,
    rootMargin: "0px 0px -15% 0px",
  };

  nodeScrollObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("node-active-glowing");
      } else {
        entry.target.classList.remove("node-active-glowing");
      }
    });
  }, nodeOptions);

  document.querySelectorAll(".canvas-node").forEach((node) => {
    nodeScrollObserver.observe(node);
  });
};

// LifeCycle hooks
onMounted(() => {
  if (process.client) {
    window.addEventListener("scroll", handleScroll);
    initPipelineSimulator();
    setTimeout(() => {
      initScrollReveal();
    }, 200);
    console.log("💎 Premium DataSage landing-new loaded.");
  }
});

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener("scroll", handleScroll);
    if (pipelineCycleInterval) clearInterval(pipelineCycleInterval);
    if (scrollRevealObserver) scrollRevealObserver.disconnect();
    if (nodeScrollObserver) nodeScrollObserver.disconnect();
  }
});

// Expose states to Vue template
defineExpose({
  isScrolled,
  showMobileMenu,
  showDemoModal,
  openFaqIndex,
  activePipelineStep,
  pipelineProgress,
  modelAccuracyRF,
  modelAccuracyXGB,
  modelAccuracy,
  steps,
  faqItems,
  toggleMobileMenu,
  handleMobileMenuClick,
  goToLogin,
  goToSignup,
  watchDemo,
  closeDemoModal,
  toggleFaq,
  scrollTo,
  scrollToTop,
  getConnectorProgress,
  getConsoleStatusText,
  getConsoleIndicatorClass,
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&display=swap");

/* Global resets for index-new scope */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.landing-container {
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Helvetica,
    Arial,
    sans-serif;
  background-color: #030307;
  color: #ffffff;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  position: relative;
}

/* Ambient glow system */
.ambient-glow {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(140px);
  opacity: 0.15;
  mix-blend-mode: screen;
  animation: float 25s ease-in-out infinite alternate;
}

.orb-1 {
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, #00f0ff 0%, rgba(0, 240, 255, 0) 70%);
  top: -10%;
  left: -10%;
}

.orb-2 {
  width: 60vw;
  height: 60vw;
  background: radial-gradient(circle, #9d4edd 0%, rgba(157, 78, 221, 0) 75%);
  bottom: 10%;
  right: -15%;
  animation-delay: -5s;
}

.orb-3 {
  width: 45vw;
  height: 45vw;
  background: radial-gradient(circle, #3b82f6 0%, rgba(59, 130, 246, 0) 80%);
  top: 40%;
  left: 30%;
  animation-delay: -10s;
}

@keyframes float {
  0% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(5%, -5%) scale(1.05);
  }
  100% {
    transform: translate(-5%, 5%) scale(0.95);
  }
}

/* Glass panel global layout token */
.glass-panel {
  background: rgba(12, 12, 24, 0.45);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Premium Navigation */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.navbar.scrolled {
  background: rgba(3, 3, 7, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0.25rem 0;
}

.nav-content {
  max-width: 1300px;
  margin: 0 auto;
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  z-index: 10;
}

.brand-logo {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: #ffffff;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.brand-title {
  font-family: "Outfit", sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2.25rem;
}

.nav-link {
  font-size: 0.95rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: color 0.2s ease;
  position: relative;
  padding: 0.25rem 0;
}

.nav-link:hover {
  color: #ffffff;
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: #00f0ff;
  transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.nav-link:hover::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-btn {
  padding: 0.7rem 1.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  border: none;
}

.nav-btn.primary {
  background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 50%, #9d4edd 100%);
  color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 240, 255, 0.25);
  background-size: 200% 200%;
  animation: shineGradient 6s ease infinite;
}

.nav-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 240, 255, 0.4);
}

.nav-btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.nav-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.15);
}

/* Mobile Navigation Hamburger */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 22px;
  height: 16px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 11;
}

.mobile-menu-btn span {
  width: 100%;
  height: 2px;
  background-color: #ffffff;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.mobile-menu-btn.active span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-menu-btn.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.mobile-drawer {
  position: fixed;
  inset: 0;
  background: rgba(3, 3, 7, 0.95);
  backdrop-filter: blur(20px);
  z-index: 9;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.drawer-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  width: 100%;
  max-width: 320px;
}

.drawer-link {
  font-family: "Outfit", sans-serif;
  font-size: 1.8rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease;
}

.drawer-link:hover {
  color: #00f0ff;
}

.drawer-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  margin-top: 1.5rem;
}

.full-width {
  width: 100%;
}

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 8.5rem 2rem 4.5rem;
  z-index: 1;
}

.hero-grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(
    circle at center,
    black 40%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 0;
}

.hero-content-wrapper {
  max-width: 1300px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 4.5rem;
  align-items: center;
  width: 100%;
  position: relative;
  z-index: 1;
}

.hero-text-block {
  text-align: left;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 240, 255, 0.07);
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 50px;
  margin-bottom: 1.75rem;
  backdrop-filter: blur(10px);
}

.badge-dot {
  width: 6px;
  height: 6px;
  background-color: #00f0ff;
  border-radius: 50%;
  box-shadow: 0 0 8px #00f0ff;
}

.badge-text {
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #00f0ff;
}

.hero-title {
  font-family: "Outfit", sans-serif;
  font-size: 3.8rem;
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -1.5px;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 50%, #9d4edd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.15rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2.75rem;
  max-width: 580px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  margin-bottom: 3.5rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.15rem 2.25rem;
  border-radius: 16px;
  font-family: "Outfit", sans-serif;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  border: none;
}

.cta-button.primary {
  background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 50%, #9d4edd 100%);
  color: #ffffff;
  box-shadow: 0 10px 25px rgba(0, 240, 255, 0.25);
  background-size: 200% 200%;
  animation: shineGradient 6s ease infinite;
}

.cta-button.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(0, 240, 255, 0.45);
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.04);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.cta-button.large {
  font-size: 1.1rem;
  padding: 1.35rem 2.75rem;
}

.cta-button.glow {
  box-shadow: 0 10px 30px rgba(0, 240, 255, 0.3);
}

.cta-button.glow:hover {
  box-shadow: 0 12px 40px rgba(0, 240, 255, 0.5);
}

.trust-indicators {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.trust-icon {
  color: #00f0ff;
  font-weight: bold;
}

/* High Fidelity Interactive Glass Mockup styling */
.hero-visual {
  width: 100%;
  perspective: 1000px;
}

.glass-mockup {
  background: rgba(12, 12, 28, 0.55);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow:
    0 30px 70px rgba(0, 0, 0, 0.6),
    0 0 100px rgba(0, 240, 255, 0.05);
  transform: rotateY(-3deg) rotateX(2deg);
  transition: transform 0.5s ease;
}

.glass-mockup:hover {
  transform: rotateY(0deg) rotateX(0deg) translateY(-5px);
}

.mockup-header {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.mockup-dots {
  display: flex;
  gap: 6px;
  margin-right: 1.5rem;
}

.mockup-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: block;
}

.dot-red {
  background: #ef4444;
}
.dot-yellow {
  background: #f59e0b;
}
.dot-green {
  background: #10b981;
}

.mockup-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.9rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
}

.tab-icon {
  font-size: 0.8rem;
}

.tab-title {
  font-size: 0.78rem;
  font-family: monospace;
  color: rgba(255, 255, 255, 0.8);
}

.mockup-body {
  padding: 2.25rem 2rem;
}

/* Horizontal connected pipeline layout */
.pipeline-horizontal {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.25rem;
  position: relative;
}

.horizontal-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  z-index: 2;
  opacity: 0.35;
  transform: scale(0.95);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.horizontal-node.active {
  opacity: 1;
  transform: scale(1.05);
}

.horizontal-icon-container {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  margin-bottom: 0.6rem;
  transition: all 0.4s ease;
}

.horizontal-node.active .horizontal-icon-container {
  background: linear-gradient(
    135deg,
    rgba(0, 240, 255, 0.15) 0%,
    rgba(157, 78, 221, 0.15) 100%
  );
  border-color: rgba(0, 240, 255, 0.4);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
}

.node-emoji {
  font-size: 1.25rem;
}

.node-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.15rem;
}

.node-meta {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.4);
}

.horizontal-connector {
  flex-grow: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.06);
  margin: 0 0.5rem;
  margin-bottom: 1.75rem;
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  z-index: 1;
}

.connector-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #00f0ff, #9d4edd);
  width: 0;
  transition: width 0.1s linear;
}

/* Console details simulator */
.live-console {
  background: rgba(3, 3, 8, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 1.25rem;
  font-family: monospace;
}

.console-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  padding-bottom: 0.6rem;
  margin-bottom: 0.75rem;
}

.console-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.console-indicator.idle {
  background-color: #ef4444;
  box-shadow: 0 0 8px #ef4444;
}

.console-indicator.busy {
  background-color: #f59e0b;
  box-shadow: 0 0 8px #f59e0b;
  animation: pulse 1s infinite alternate;
}

.console-indicator.success {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.console-status-text {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.55);
}

.console-body {
  min-height: 88px;
}

.console-line {
  font-size: 0.78rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
}

.text-muted {
  color: rgba(255, 255, 255, 0.4);
}
.text-cyan {
  color: #00f0ff;
}
.text-success {
  color: #10b981;
}
.text-purple {
  color: #d8b4fe;
}

.training-algorithms-preview {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 0.4rem;
}

.algo-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.75rem;
}

.algo-row span:first-child {
  width: 130px;
  color: rgba(255, 255, 255, 0.75);
}

.algo-bar {
  flex-grow: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
}

.algo-bar-fill {
  height: 100%;
  background-color: #00f0ff;
  border-radius: 10px;
  transition: width 0.1s linear;
}

.algo-bar-fill.purple {
  background-color: #9d4edd;
}

.algo-acc {
  width: 60px;
  text-align: right;
  font-weight: 700;
  color: #ffffff;
}

.metrics-visual-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 0.5rem;
}

.metric-mini-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 0.6rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.m-val {
  font-size: 1.1rem;
  font-weight: 700;
  color: #10b981;
}

.m-label {
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.15rem;
}

/* Bento Grid styling */
.features-section {
  padding: 7rem 2rem;
  position: relative;
}

.section-container {
  max-width: 1300px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 4.5rem;
}

.section-title {
  font-family: "Outfit", sans-serif;
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 1.25rem;
  background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-subtitle {
  font-size: 1.1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.65);
  max-width: 760px;
  margin: 0 auto;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.bento-card {
  height: 100%;
  padding: 2.25rem;
  display: flex;
  flex-direction: column;
}

.bento-card.large {
  grid-column: span 2;
}

.bento-card.medium {
  grid-column: span 1;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
    rgba(0, 240, 255, 0.08) 0%,
    transparent 60%
  );
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 1;
}

.glass-panel:hover .card-glow {
  opacity: 1;
}

.glass-panel:hover {
  transform: translateY(-6px);
  border-color: rgba(0, 240, 255, 0.25);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.4),
    0 0 50px rgba(0, 240, 255, 0.05);
}

.bento-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  margin-bottom: 1.5rem;
  z-index: 2;
  position: relative;
}

.glass-panel:hover .bento-icon-wrapper {
  background: rgba(0, 240, 255, 0.08);
  border-color: rgba(0, 240, 255, 0.3);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
}

.bento-emoji {
  font-size: 1.5rem;
}

.bento-content {
  z-index: 2;
  position: relative;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.bento-svg-icon {
  width: 24px;
  height: 24px;
  color: #00f0ff;
  display: block;
  transition: transform 0.3s ease;
}

.glass-panel:hover .bento-svg-icon {
  transform: scale(1.1);
}

.bento-title {
  font-family: "Outfit", sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #ffffff;
}

.bento-desc {
  font-size: 0.92rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.65);
  margin-bottom: 1.5rem;
}

/* Bento card preview structures */
.bento-preview-box {
  background: rgba(3, 3, 7, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  padding: 1.25rem;
  margin-top: auto;
}

.prep-preview {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.quality-score-radial {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid #10b981;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.radial-num {
  font-size: 1.2rem;
  font-weight: 800;
  color: #10b981;
}

.radial-lbl {
  font-size: 0.5rem;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  text-align: center;
  line-height: 1.1;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.issue-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.7);
}

.bullet {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.bullet.red {
  background-color: #ef4444;
}
.bullet.green {
  background-color: #10b981;
}

.train-preview {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mini-chart-row {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0.75rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.6);
}

.mini-chart-row.highlight-cyan {
  background: rgba(0, 240, 255, 0.05);
  border-color: rgba(0, 240, 255, 0.15);
  color: #00f0ff;
  font-weight: 700;
}

.spec-preview {
  display: flex;
  justify-content: center;
}

.pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.glow-pill {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 50px;
  color: rgba(255, 255, 255, 0.6);
}

.glow-pill.cyan {
  background: rgba(0, 240, 255, 0.05);
  border-color: rgba(0, 240, 255, 0.2);
  color: #00f0ff;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.1);
}

.glow-pill.purple {
  background: rgba(157, 78, 221, 0.05);
  border-color: rgba(157, 78, 221, 0.2);
  color: #d8b4fe;
  box-shadow: 0 0 10px rgba(157, 78, 221, 0.1);
}

.chart-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.heatmap-mock {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  background: rgba(255, 255, 255, 0.02);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.heat-cell {
  width: 24px;
  height: 24px;
  border-radius: 4px;
}

.heat-cell.h-high {
  background-color: rgba(0, 240, 255, 0.8);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
}

.heat-cell.h-med {
  background-color: rgba(0, 240, 255, 0.4);
}

.heat-cell.h-low {
  background-color: rgba(255, 255, 255, 0.05);
}

.heatmap-legend {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.45);
}

.grad-bar {
  width: 8px;
  height: 50px;
  background: linear-gradient(
    180deg,
    rgba(0, 240, 255, 0.8),
    rgba(255, 255, 255, 0.05)
  );
  border-radius: 20px;
}

/* How It Works (Vertical Interactive Workflow Canvas) */
.how-it-works-section {
  padding: 9rem 2rem;
  position: relative;
  background-color: #020205;
  overflow: hidden;
}

/* AI Blueprint/Grid Overlay */
.canvas-grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size:
    50px 50px,
    10px 10px;
  background-image:
    linear-gradient(to right, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
    radial-gradient(circle, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  pointer-events: none;
  z-index: 1;
}

/* Faint neural background vector line graphics */
.neural-bg-graphics {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  opacity: 0.45;
}

.neural-bg-svg {
  width: 100%;
  height: 100%;
}

/* Soft Ambient Glows behind canvas nodes */
.canvas-ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(160px);
  opacity: 0.09;
  pointer-events: none;
  z-index: 1;
}

.canvas-ambient-glow.orb-cyan {
  width: 600px;
  height: 600px;
  background-color: #00f0ff;
  top: 10%;
  left: 5%;
  animation: floatOrbOne 35s infinite alternate ease-in-out;
}

.canvas-ambient-glow.orb-purple {
  width: 700px;
  height: 700px;
  background-color: #9d4edd;
  bottom: 5%;
  right: 2%;
  animation: floatOrbTwo 40s infinite alternate ease-in-out;
}

@keyframes floatOrbOne {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(80px, 50px) scale(1.15);
  }
}

@keyframes floatOrbTwo {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(-60px, -90px) scale(1.1);
  }
}

/* Canvas Container */
.workflow-canvas {
  position: relative;
  max-width: 900px;
  margin: 5rem auto 0;
  z-index: 2;
}

/* Central spine line path canvas container */
.canvas-spine-container {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  pointer-events: none;
}

.canvas-spine-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* Simple single line pulse trail */
.pulse-line {
  animation: flowSingleSpine 8s linear infinite;
  filter: drop-shadow(0 0 5px #00f0ff);
}

@keyframes flowSingleSpine {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: -205;
  }
}

/* Orbiting data particles along central canvas vertical coordinate */
.flowing-particle {
  position: absolute;
  left: 50%;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transform: translateX(-50%);
  filter: drop-shadow(0 0 8px #00f0ff);
  pointer-events: none;
}

.flowing-particle.pt-1 {
  background-color: #00f0ff;
  animation: flowParticleDown1 10s infinite cubic-bezier(0.4, 0, 0.2, 1);
}

.flowing-particle.pt-2 {
  background-color: #9d4edd;
  filter: drop-shadow(0 0 8px #9d4edd);
  animation: flowParticleDown2 10s infinite cubic-bezier(0.4, 0, 0.2, 1);
  animation-delay: 5s;
}

@keyframes flowParticleDown1 {
  0% {
    top: 0%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    top: 100%;
    opacity: 0;
  }
}

@keyframes flowParticleDown2 {
  0% {
    top: 0%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    top: 100%;
    opacity: 0;
  }
}

/* Canvas Nodes */
.canvas-nodes {
  display: flex;
  flex-direction: column;
  gap: 7rem;
  position: relative;
  z-index: 2;
}

.canvas-node {
  width: 480px;
  padding: 2.25rem;
  position: relative;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: grab;
  opacity: 0.45;
  filter: grayscale(35%) blur(0.4px);
}

.canvas-node.node-active-glowing,
.canvas-node.primary-active-node {
  opacity: 1;
  filter: none;
}

.canvas-node:active {
  cursor: grabbing;
}

/* Staggered alternate node alignments */
.canvas-node:nth-child(odd) {
  align-self: flex-start;
}

.canvas-node:nth-child(even) {
  align-self: flex-end;
}

/* Hover dynamic elevation scale actions */
.canvas-node:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(0, 240, 255, 0.35);
  box-shadow:
    0 20px 45px rgba(0, 0, 0, 0.55),
    0 0 35px rgba(0, 240, 255, 0.08);
}

/* Infrastructure Telemetry Ribbons */
.node-telemetry {
  display: flex;
  justify-content: space-between;
  padding: 0.45rem 0.85rem;
  background: rgba(255, 255, 255, 0.015);
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  font-family: monospace;
  font-size: 0.62rem;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.4);
  margin: -2.25rem -2.25rem 1.5rem -2.25rem;
  border-top-left-radius: 14px;
  border-top-right-radius: 14px;
}

.tel-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.tel-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  display: inline-block;
}

.tel-dot.green {
  background-color: #10b981;
  box-shadow: 0 0 6px #10b981;
}

.cyan-highlight {
  color: #00f0ff !important;
  font-weight: 700;
  letter-spacing: 1px;
}

/* Headers & Containers */
.node-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.node-icon-box {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: rgba(0, 240, 255, 0.06);
  border: 1px solid rgba(0, 240, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.05);
}

.node-icon-box.orange-glow {
  background: rgba(245, 158, 11, 0.06);
  border-color: rgba(245, 158, 11, 0.15);
}

.node-icon-box.purple-glow {
  background: rgba(157, 78, 221, 0.06);
  border-color: rgba(157, 78, 221, 0.15);
}

.node-icon-box.pink-glow {
  background: rgba(236, 72, 153, 0.06);
  border-color: rgba(236, 72, 153, 0.15);
}

.active-icon-glow {
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
  border-color: rgba(0, 240, 255, 0.4) !important;
  background: rgba(0, 240, 255, 0.1) !important;
}

.node-svg-icon {
  width: 22px;
  height: 22px;
}

.node-meta-info {
  display: flex;
  flex-direction: column;
}

.node-number {
  font-family: monospace;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: rgba(255, 255, 255, 0.35);
}

.node-title {
  font-family: "Outfit", sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
}

.node-desc {
  font-size: 0.88rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.55);
  margin-bottom: 1.5rem;
}

/* Inside mini visualizers */
.node-visualizer {
  background: rgba(2, 2, 5, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 14px;
  padding: 1.25rem;
  overflow: hidden;
  position: relative;
}

.active-visualizer-bg {
  background: rgba(0, 240, 255, 0.015) !important;
  border-color: rgba(0, 240, 255, 0.1) !important;
}

/* 1. Upload visualizer */
.upload-visualizer {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.upload-progress-ring {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  border: 2px dashed rgba(0, 240, 255, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 240, 255, 0.02);
  flex-shrink: 0;
  animation: rotateDashedRing 20s linear infinite;
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.05);
}

@keyframes rotateDashedRing {
  100% {
    transform: rotate(360deg);
  }
}

.upload-progress-ring .file-icon,
.upload-progress-ring .upload-badge {
  transform: rotate(0deg);
}

.upload-progress-ring .file-icon {
  font-size: 1.25rem;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.2));
}

.upload-progress-ring .upload-badge {
  font-size: 0.52rem;
  font-weight: 700;
  color: #00f0ff;
  margin-top: 0.15rem;
  text-transform: uppercase;
}

.visual-table-rows {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  position: relative;
  max-height: 80px;
  overflow: hidden;
}

.scan-shimmer {
  position: absolute;
  top: 0;
  left: -150%;
  width: 150%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.04),
    transparent
  );
  transform: skewX(-20deg);
  animation: scanShimmerAnimation 6s ease-in-out infinite;
  pointer-events: none;
}

@keyframes scanShimmerAnimation {
  0% {
    left: -150%;
  }
  30% {
    left: 150%;
  }
  100% {
    left: 150%;
  }
}

.table-row-stream {
  display: flex;
  justify-content: space-between;
  padding: 0.35rem 0.6rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  font-size: 0.68rem;
  color: rgba(255, 255, 255, 0.5);
  font-family: monospace;
  animation: flowRowsUp 5s linear infinite;
}

.table-row-stream.tr-2 {
  animation-delay: 1.66s;
}
.table-row-stream.tr-3 {
  animation-delay: 3.33s;
}

@keyframes flowRowsUp {
  0% {
    transform: translateY(40px);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-40px);
    opacity: 0;
  }
}

/* 2. Cleanse visualizer */
.cleanse-visualizer {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.null-grid-simulator {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  position: relative;
}

/* Scanning vertical light beam sweep */
.sweeper-laser-beam {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f59e0b, transparent);
  box-shadow: 0 0 10px #f59e0b;
  animation: scanLaserSweep 3.5s ease-in-out infinite;
  pointer-events: none;
  z-index: 2;
}

@keyframes scanLaserSweep {
  0% {
    top: 0%;
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    top: 100%;
    opacity: 0;
  }
}

.grid-cell {
  height: 20px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.grid-cell.filled {
  background: rgba(255, 255, 255, 0.07);
}

.grid-cell.imputed {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: monospace;
  font-size: 0.58rem;
  font-weight: 700;
  color: #10b981;
}

.grid-cell.pulsing-green {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
  animation: greenPulseImpute 2s infinite alternate;
}

@keyframes greenPulseImpute {
  0% {
    background-color: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.25);
    color: #ef4444;
  }
  40% {
    background-color: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.25);
    color: #ef4444;
  }
  60% {
    background-color: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.25);
    color: #10b981;
  }
  100% {
    background-color: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.25);
    color: #10b981;
  }
}

.smote-ratio-bar {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.ratio-label {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.45);
}

.ratio-progress {
  height: 5px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 10px;
  overflow: hidden;
}

.ratio-progress .progress-fill {
  height: 100%;
  width: 50%;
  animation: fillProgressPulse 3s infinite alternate
    cubic-bezier(0.4, 0, 0.2, 1);
}

.ratio-progress .progress-fill.green-gradient {
  background: linear-gradient(90deg, #f59e0b, #10b981);
}

@keyframes fillProgressPulse {
  0% {
    width: 35%;
  }
  100% {
    width: 100%;
  }
}

/* 3. Train visualizer */
.train-visualizer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.neural-activity-visualizer {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex-shrink: 0;
}

.algo-chip {
  font-size: 0.68rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.55);
  font-weight: 700;
  display: flex;
  justify-content: space-between;
  width: 105px;
  transition: all 0.3s ease;
}

.algo-chip.cyan {
  background: rgba(0, 240, 255, 0.02);
  border-color: rgba(0, 240, 255, 0.1);
  color: rgba(0, 240, 255, 0.8);
}

.algo-chip.purple {
  background: rgba(157, 78, 221, 0.02);
  border-color: rgba(157, 78, 221, 0.1);
  color: #c084fc;
}

.algo-chip.active-chip-glowing {
  background: rgba(0, 240, 255, 0.07) !important;
  border-color: rgba(0, 240, 255, 0.35) !important;
  color: #00f0ff !important;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.15);
}

.live-acc {
  font-family: monospace;
}

.live-acc-pulsing {
  font-family: monospace;
  animation: accMetricPulse 1s infinite alternate;
}

@keyframes accMetricPulse {
  0% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

.training-line-chart {
  flex-grow: 1;
  height: 48px;
  position: relative;
  background: rgba(255, 255, 255, 0.015);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 4px;
}

.fitting-line-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.fitting-line-path {
  stroke-dasharray: 200;
  stroke-dashoffset: 200;
  animation: drawFittingLine 4s infinite alternate ease-in-out;
}

@keyframes drawFittingLine {
  0% {
    stroke-dashoffset: 200;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.pulsing-endpoint {
  animation: endpointPulseOpacity 1.5s infinite alternate;
}

@keyframes endpointPulseOpacity {
  0% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1.3);
  }
}

/* 4. Diagnose visualizer */
.diagnose-visualizer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.mini-confusion-matrix {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  flex-shrink: 0;
}

.matrix-cell {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.58rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.015);
  border: 1px solid rgba(255, 255, 255, 0.03);
}

.matrix-cell .val {
  font-family: monospace;
  font-size: 0.65rem;
  color: #ffffff;
}

.matrix-cell.tp {
  background: rgba(16, 185, 129, 0.07);
  border-color: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.matrix-cell.tn {
  background: rgba(16, 185, 129, 0.07);
  border-color: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.diagnose-download-badge {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.015);
  border: 1px dashed rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  animation: downloadBadgePulse 2.5s infinite alternate;
}

@keyframes downloadBadgePulse {
  0% {
    border-color: rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.015);
  }
  100% {
    border-color: rgba(0, 240, 255, 0.2);
    background: rgba(0, 240, 255, 0.02);
    color: #00f0ff;
  }
}

.download-icon-pulse {
  animation: coreWavePulse 2s infinite alternate ease-in-out;
  display: inline-block;
}

.blinking-cursor {
  font-weight: 700;
  color: #00f0ff;
  animation: textCursorBlink 0.9s steps(2, start) infinite;
}

@keyframes textCursorBlink {
  to {
    visibility: hidden;
  }
}

/* Responsive adjustments for canvas layout */
@media (max-width: 992px) {
  .canvas-spine-container {
    left: 20px;
    transform: none;
    width: 20px;
  }

  .ai-core-hub {
    display: none; /* Hide center core on small screens */
  }

  .canvas-spine-svg {
    display: none; /* Hide complex overlapping SVGs on mobile/tablet */
  }

  .canvas-node {
    width: 100%;
    align-self: flex-start !important;
    padding-left: 3rem;
  }

  .canvas-node::after {
    left: 20px !important;
    width: 20px !important;
  }

  .canvas-node .port-in,
  .canvas-node .port-out {
    left: 16px !important;
  }

  .flowing-particle {
    left: 20px !important;
  }
}

/* About premium styling */
.about-section {
  padding: 7rem 2rem;
}

.about-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.25rem;
}

.about-card-premium {
  padding: 3rem 2.25rem;
  height: 100%;
}

.about-glow {
  position: absolute;
  top: -40%;
  left: -40%;
  width: 80%;
  height: 80%;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.05;
  pointer-events: none;
}

.about-glow.color-cyan {
  background-color: #00f0ff;
}
.about-glow.color-purple {
  background-color: #9d4edd;
}
.about-glow.color-blue {
  background-color: #3b82f6;
}

.about-premium-icon {
  font-size: 2.5rem;
  margin-bottom: 1.75rem;
}

.about-premium-title {
  font-family: "Outfit", sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #ffffff;
}

.about-premium-desc {
  font-size: 0.92rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.65);
}

/* FAQ Accordion Styling */
.faq-section {
  padding: 7rem 2rem;
}

.faq-accordion-list {
  max-width: 820px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.faq-accordion-card {
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.faq-accordion-card.expanded {
  background: rgba(12, 12, 28, 0.65);
  border-color: rgba(0, 240, 255, 0.3);
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.4),
    0 0 25px rgba(0, 240, 255, 0.03);
}

.faq-trigger {
  width: 100%;
  background: none;
  border: none;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
}

.faq-question-text {
  font-family: "Outfit", sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  transition: color 0.25s ease;
}

.faq-trigger:hover .faq-question-text {
  color: #00f0ff;
}

.faq-indicator-icon {
  width: 18px;
  height: 18px;
  position: relative;
  flex-shrink: 0;
}

.faq-indicator-icon::before,
.faq-indicator-icon::after {
  content: "";
  position: absolute;
  background-color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Horizontal line */
.faq-indicator-icon::before {
  top: 8px;
  left: 0;
  width: 100%;
  height: 2px;
}

/* Vertical line */
.faq-indicator-icon::after {
  top: 0;
  left: 8px;
  width: 2px;
  height: 100%;
}

.faq-accordion-card.expanded .faq-indicator-icon::after {
  transform: rotate(90deg);
  opacity: 0;
}

.faq-accordion-card.expanded .faq-indicator-icon::before {
  background-color: #00f0ff;
}

.faq-content-pane {
  padding: 0 2rem 1.75rem;
}

.faq-answer-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.65);
}

/* Final Call To Action Section */
.cta-section {
  padding: 8rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-backdrop-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60vw;
  height: 60vw;
  background: radial-gradient(
    circle,
    rgba(0, 240, 255, 0.08) 0%,
    rgba(157, 78, 221, 0.04) 50%,
    transparent 70%
  );
  pointer-events: none;
}

.cta-header-title {
  font-family: "Outfit", sans-serif;
  font-size: 3.2rem;
  font-weight: 800;
  letter-spacing: -1.5px;
  margin-bottom: 1.25rem;
  background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-header-subtitle {
  font-size: 1.2rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  max-width: 620px;
  margin: 0 auto 3rem;
}

.cta-action-holder {
  margin-bottom: 3.5rem;
}

.cta-support-badges {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.support-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.badge-check {
  color: #10b981;
  font-weight: bold;
}

/* Footer Section */
.footer {
  background-color: #020204;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
  padding: 5.5rem 2rem 2.5rem;
}

.footer-inner {
  max-width: 1300px;
  margin: 0 auto 4rem;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 4rem;
}

.brand-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.footer-logo-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-brand-title {
  font-family: "Outfit", sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  color: #ffffff;
}

.footer-brand-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.55);
}

.footer-socials {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.social-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.25s ease;
  text-decoration: none;
}

.social-icon:hover {
  background: rgba(0, 240, 255, 0.08);
  border-color: rgba(0, 240, 255, 0.3);
  color: #00f0ff;
}

.footer-col-title {
  font-family: "Outfit", sans-serif;
  font-size: 0.98rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1.5rem;
}

.footer-links-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-links-list a {
  font-size: 0.92rem;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease;
}

.footer-links-list a:hover {
  color: #00f0ff;
}

.footer-credits {
  max-width: 1300px;
  margin: 0 auto;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
  text-align: center;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.45);
}

/* Modal Windows styling */
.demo-modal {
  position: fixed;
  inset: 0;
  background: rgba(3, 3, 7, 0.8);
  backdrop-filter: blur(15px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.demo-modal-content {
  max-width: 500px;
  width: 100%;
  padding: 3rem 2.5rem;
  position: relative;
  text-align: center;
}

.demo-modal-close-btn {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 2rem;
  cursor: pointer;
  line-height: 0.5;
  transition: color 0.2s ease;
}

.demo-modal-close-btn:hover {
  color: #ffffff;
}

.modal-title-text {
  font-family: "Outfit", sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.modal-demo-icon {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
}

.modal-text-lead {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.modal-text-sub {
  font-size: 0.9rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.65);
  margin-bottom: 2.25rem;
}

.modal-action-btn {
  width: 100%;
  padding: 1.1rem 2rem;
  border-radius: 14px;
  background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 100%);
  border: none;
  color: #ffffff;
  font-family: "Outfit", sans-serif;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px rgba(0, 240, 255, 0.25);
}

.modal-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(0, 240, 255, 0.45);
}

/* Animations declarations */
@keyframes shineGradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.15);
    opacity: 1;
  }
}

/* Vue Transitions classes */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-fade-leave-active {
  transition: all 0.25s cubic-bezier(0.82, 0.085, 0.395, 0.895);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Scroll reveal initial styling */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

.bento-grid .reveal:nth-child(1) {
  transition-delay: 0.05s;
}
.bento-grid .reveal:nth-child(2) {
  transition-delay: 0.15s;
}
.bento-grid .reveal:nth-child(3) {
  transition-delay: 0.25s;
}
.bento-grid .reveal:nth-child(4) {
  transition-delay: 0.35s;
}

.timeline-steps .reveal:nth-child(1) {
  transition-delay: 0.05s;
}
.timeline-steps .reveal:nth-child(2) {
  transition-delay: 0.15s;
}
.timeline-steps .reveal:nth-child(3) {
  transition-delay: 0.25s;
}
.timeline-steps .reveal:nth-child(4) {
  transition-delay: 0.35s;
}

.about-cards-grid .reveal:nth-child(1) {
  transition-delay: 0.05s;
}
.about-cards-grid .reveal:nth-child(2) {
  transition-delay: 0.15s;
}
.about-cards-grid .reveal:nth-child(3) {
  transition-delay: 0.25s;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .hero-title {
    font-size: 3.3rem;
  }
}

@media (max-width: 1024px) {
  .hero-content-wrapper {
    grid-template-columns: 1fr;
    gap: 3.5rem;
    text-align: center;
  }

  .hero-text-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }

  .hero-actions {
    justify-content: center;
  }

  .trust-indicators {
    justify-content: center;
  }

  .bento-grid {
    grid-template-columns: 1fr;
  }

  .bento-card.large,
  .bento-card.medium {
    grid-column: span 1;
  }

  .timeline-steps {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }

  .timeline-line {
    display: none;
  }

  .about-cards-grid {
    grid-template-columns: 1fr;
  }

  .footer-inner {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}

@media (max-width: 768px) {
  .nav-links,
  .nav-actions {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .hero-section {
    padding-top: 7rem;
  }

  .hero-title {
    font-size: 2.6rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .cta-header-title {
    font-size: 2.3rem;
  }

  .cta-header-subtitle {
    font-size: 1rem;
  }

  .timeline-steps {
    grid-template-columns: 1fr;
  }

  .footer-inner {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .mockup-body {
    padding: 1.5rem 1rem;
  }

  .pipeline-horizontal {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }

  .horizontal-connector {
    display: none;
  }

  .horizontal-node {
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    width: 100%;
    text-align: left;
  }

  .horizontal-icon-container {
    margin-bottom: 0;
  }

  .live-console {
    margin-top: 1rem;
  }

  .faq-trigger {
    padding: 1.25rem 1.5rem;
  }

  .faq-question-text {
    font-size: 0.98rem;
  }
}
</style>
