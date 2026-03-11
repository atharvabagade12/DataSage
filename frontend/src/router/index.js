import { createRouter, createWebHistory } from "vue-router";

// Import components from pages directory
import Login from "@/pages/login.vue";
import Dashboard from "@/pages/dashboard.vue";
import DataPreview from "@/pages/data-preview.vue";
import TargetSelection from "@/pages/target-selection.vue";
import AlgorithmSelection from "@/pages/algorithm-select.vue";
import ModelTraining from "@/pages/model-training.vue";
import ModelVisualization from "@/pages/model-visualization.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { title: "Sign In — DataSage", public: true },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      title: "ML Dashboard",
      step: 1,
    },
  },
  {
    path: "/data-preview",
    name: "DataPreview",
    component: DataPreview,
    meta: {
      title: "Data Preview",
      step: 2,
      requiresData: true,
    },
  },
  {
    path: "/target-selection",
    name: "TargetSelection",
    component: TargetSelection,
    meta: {
      title: "Target Selection",
      step: 3,
      requiresData: true,
    },
  },
  {
    path: "/algorithm-select",
    name: "AlgorithmSelection",
    component: AlgorithmSelection,
    meta: {
      title: "Algorithm Selection",
      step: 4,
      requiresTarget: true,
    },
  },
  {
    path: "/model-training",
    name: "ModelTraining",
    component: ModelTraining,
    meta: {
      title: "Model Training",
      step: 5,
      requiresAlgorithm: true,
    },
  },
  {
    path: "/model-visualization/:modelId?",
    name: "model-visualization",
    component: ModelVisualization,
    meta: {
      title: "Model Visualization",
      step: 6,
      requiresModel: true,
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/pages/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard — auth check first, then pipeline data-flow checks
router.beforeEach((to, from, next) => {
  const token =
    sessionStorage.getItem("token") ||
    sessionStorage.getItem("authToken") ||
    localStorage.getItem("token") ||
    localStorage.getItem("authToken");

  const isPublic = to.meta.public === true;

  // Redirect unauthenticated users to /login for protected routes
  if (!isPublic && !token) {
    next("/login");
    return;
  }

  // Redirect already-authenticated users away from /login
  if (to.name === "Login" && token) {
    next("/dashboard");
    return;
  }

  // Get pipeline state from localStorage (kept by useMLPipeline)
  const appState = JSON.parse(
    localStorage.getItem("datasage_pipeline_state") || "{}"
  );

  // Check if user is trying to access a page without required data
  if (to.meta.requiresData && !appState.dataset) {
    next("/dashboard");
    return;
  }

  if (to.meta.requiresTarget && !appState.targetColumn) {
    next("/target-selection");
    return;
  }

  if (to.meta.requiresAlgorithm && !appState.selectedAlgorithm) {
    next("/algorithm-select");
    return;
  }

  if (to.meta.requiresModel && !appState.trainedModel) {
    next("/model-training");
    return;
  }

  // Update page title
  if (to.meta.title) {
    document.title = `${to.meta.title} - DataSage`;
  }

  next();
});

export default router;
