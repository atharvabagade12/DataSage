import { createRouter, createWebHistory } from "vue-router";

// Import components from pages directory
import Dashboard from "@/pages/dashboard.vue";
import DataPreview from "@/pages/data-preview.vue";
import TargetSelection from "@/pages/target-selection.vue";
import AlgorithmSelection from "@/pages/algorithm-select.vue";
import ModelTraining from "@/pages/model-training.vue";
import Results from "@/pages/results.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
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
    path: "/results",
    name: "Results",
    component: Results,
    meta: {
      title: "Results",
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

// Navigation guards for data flow validation
router.beforeEach((to, from, next) => {
  // Get pipeline state from localStorage (kept by useMLPipeline)
  const appState = JSON.parse(
    localStorage.getItem("datasage_pipeline_state") || "{}"
  );

  console.log(`Navigating from ${from.path} to ${to.path}`, appState);

  // Check if user is trying to access a page without required data
  if (to.meta.requiresData && !appState.dataset) {
    console.log("Redirecting to dashboard - no dataset");
    next("/dashboard");
    return;
  }

  if (to.meta.requiresTarget && !appState.targetColumn) {
    console.log("Redirecting to target selection - no target");
    next("/target-selection");
    return;
  }

  if (to.meta.requiresAlgorithm && !appState.selectedAlgorithm) {
    console.log("Redirecting to algorithm selection - no algorithm");
    next("/algorithm-selection");
    return;
  }

  if (to.meta.requiresModel && !appState.trainedModel) {
    console.log("Redirecting to model training - no model");
    next("/model-training");
    return;
  }

  // Update page title
  if (to.meta.title) {
    document.title = `${to.meta.title} - ML Platform`;
  }

  next();
});

export default router;
