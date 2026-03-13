
from fastapi import FastAPI, WebSocket, HTTPException, UploadFile, File, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

import json
import asyncio
import io
import sys
import os
import traceback 
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Union
from fastapi.responses import StreamingResponse, FileResponse
import multiprocessing
import queue
import time
from datetime import datetime


# ===== SKLEARN IMPORTS =====
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.linear_model import Ridge, Lasso  
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

# ===== PREPROCESSING IMPORTS =====
from sklearn.model_selection import (
    train_test_split, cross_val_score, cross_validate, StratifiedKFold, KFold,
    GridSearchCV, RandomizedSearchCV
)
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, LabelEncoder,
    PolynomialFeatures
)
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, issparse, csr_matrix

# ===== IMBALANCED-LEARN (SMOTE) =====
try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False
    print("⚠️ Warning: imbalanced-learn not installed. SMOTE functionality will be disabled.")


# ===== METRICS IMPORTS =====
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, mean_absolute_error
)

# ===== XGBOOST =====
import xgboost as xgb

# ===== MODEL PERSISTENCE =====
import joblib

# ===== PREPROCESSING MODULE =====
from preprocessing import DataPreprocessor, TargetEncoder
from semantic_type_utils import detect_semantic_type, get_effective_semantic_types
from missing_value_markers import MISSING_VALUE_MARKERS



# ===== DATABASE & STORAGE =====
from database import get_db, engine
from models import Dataset as DatasetModel, Model as ModelModel
from services.file_service import FileService
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from fastapi import Depends

file_service = FileService()

# ===== FASTAPI APP INITIALIZATION =====
app = FastAPI(
    title="DataSage ML Backend - Production Edition",
    version="2.0.0",
    description="Production-ready ML backend with proper dataset management"
)

from fastapi import Response
import os

# 1. Define allowed origins clearly
env_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://0.0.0.0:3000",
    "http://[::1]:3000",
    "https://datasage-ui.vercel.app"
]
# Add origins from environment if provided
if env_origins:
    ALLOWED_ORIGINS.extend([o.strip() for o in env_origins if o.strip()])

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(frontend_url)
 
@app.middleware("http")
async def manual_cors_middleware(request, call_next):
    origin = request.headers.get("origin")
    
    # Handle preflight (OPTIONS) requests manually
    if request.method == "OPTIONS":
        print(f"🛠️ MANUAL CORS: Handling OPTIONS for {request.url.path} from {origin}")
        response = Response(status_code=204)
        # Always return the origin that requested it if it's in our allowed list or ends with .vercel.app
        if origin and (origin in ALLOWED_ORIGINS or origin.endswith(".vercel.app") or "localhost" in origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
            
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, ngrok-skip-browser-warning, X-Requested-With"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    # Handle actual requests
    response = await call_next(request)
    
    # Inject CORS headers into every response
    if origin:
        if origin in ALLOWED_ORIGINS or origin.endswith(".vercel.app") or "localhost" in origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
            
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, ngrok-skip-browser-warning, X-Requested-With"
    
    return response


# IMPORT AUTH ROUTER
try:
    import auth
    app.include_router(auth.router)
    print("Auth router loaded successfully")
except ImportError as e:
    print(f"Auth router not available: {e}")

# ===== SINGLE SOURCE OF TRUTH: GLOBAL STORAGE =====
datasets: Dict[str, Dict[str, Any]] = {}  # { dataset_id: { 'dataframe': df, 'metadata': {...} } }
trained_models: Dict[str, Dict[str, Any]] = {}
scalers: Dict[str, Any] = {}
X_train_storage: Dict[str, Any] = {}
X_test_storage: Dict[str, Any] = {}
y_train_storage: Dict[str, Any] = {}
y_test_storage: Dict[str, Any] = {}
split_scalers: Dict[str, Any] = {}


categorical_encoders: Dict[str, Dict[str, Any]] = {}  # dataset_id -> {col_name: encoder_info}
target_encoders: Dict[str, Dict[str, Any]] = {}  # dataset_id -> {col_name: TargetEncoder}

# Visualization data storage
visualization_data: Dict[str, Dict[str, Any]] = {}  # model_id -> {predictions, actuals, probabilities, metadata}

# Feature Metadata Registry: dataset_id -> { feature_name: { original_col, type, transformation, ... } }
feature_metadata: Dict[str, Dict[str, Any]] = {}

# Global tracker for active training processes to allow interruption
# Format: { websocket_id: multiprocessing.Process }
active_training_processes: Dict[str, multiprocessing.Process] = {}

# ===== ALGORITHM MAPPING =====
CLASSIFICATION_ALGORITHMS = {
    'Random Forest': RandomForestClassifier,
    'Logistic Regression': LogisticRegression,
    'Decision Tree': DecisionTreeClassifier,
    'XGBoost': xgb.XGBClassifier,
    'Support Vector Machine': SVC,
    'K-Nearest Neighbors': KNeighborsClassifier,
    'Neural Network (MLP)': MLPClassifier,
    'Naive Bayes': GaussianNB,
}

REGRESSION_ALGORITHMS = {
    'Random Forest Regressor': RandomForestRegressor,
    'Linear Regression': LinearRegression,
    'Decision Tree Regressor': DecisionTreeRegressor,
    'XGBoost Regressor': xgb.XGBRegressor,
    'Support Vector Regressor (SVR)': SVR,
    'K-Nearest Neighbors Regressor': KNeighborsRegressor,
    'Neural Network Regressor (MLP)': MLPRegressor,
    'Support Vector Regression': SVR,  
    'Ridge Regression': Ridge,  
    'Lasso Regression': Lasso,  
}

ALGORITHMS = {**CLASSIFICATION_ALGORITHMS, **REGRESSION_ALGORITHMS}

# ===== USER ACTION LOGGING =====

def log_user_action(db: Session, user_id: int, action_type: str, details: dict = None, resource_id: int = None, resource_type: str = None):
    """Log a user action to the database"""
    try:
        from models import UserAction
        action = UserAction(
            user_id=user_id,
            action_type=action_type,
            action_details=details,
            resource_id=resource_id,
            resource_type=resource_type
        )
        db.add(action)
        db.commit()
    except Exception as e:
        print(f"⚠️ Failed to log user action: {e}")
        db.rollback()

# ===== QUALITY SCORING HELPER =====
## healthscore in data-preview page
def calculate_quality_score(df: pd.DataFrame, stats: dict) -> dict:
    """
    Calculate a robust quality score (0-100) based on various data quality metrics.
    
    Returns:
        score: The overall quality score
        breakdown: Detailed scores for each dimension
    """
    base_score = 100.0
    
    if df is None or df.empty:
        return {"score": 0, "breakdown": {}}

    total_cells = len(df) * len(df.columns)
    if total_cells == 0:
        return {"score": 0, "breakdown": {}}

    # 1. Missing Values Penalty (Max -40 points)
    # 1% missing = -1.5 points
    total_missing = sum(stats.get('missing_values', {}).values())
    missing_pct = (total_missing / total_cells) * 100
    missing_penalty = min(40.0, missing_pct * 1.5)
    
    # 2. Duplicate Rows Penalty (Max -20 points)
    # 1% duplicates = -2 points
    total_rows = len(df)
    duplicates = stats.get('duplicates', 0)
    duplicate_pct = (duplicates / total_rows) * 100 if total_rows > 0 else 0
    duplicate_penalty = min(20.0, duplicate_pct * 2.0)
    
    # 3. Outlier Penalty (Max -15 points)
    # 1% outliers = -0.5 points
    total_outliers = stats.get('outliers', 0)
    outlier_pct = (total_outliers / total_cells) * 100
    outlier_penalty = min(15.0, outlier_pct * 0.5)
    
    # 4. Constant Columns Penalty (Max -25 points)
    # Each constant column = -5 points
    constant_cols = 0
    for col_stat in stats.get('column_stats', []):
        if col_stat.get('unique') <= 1:
            constant_cols += 1
    constant_penalty = min(25.0, constant_cols * 5.0)

    # Calculate final score
    final_score = max(0, base_score - missing_penalty - duplicate_penalty - outlier_penalty - constant_penalty)
    
    return {
        "score": round(final_score),
        "breakdown": {
            "missing_values": {
                "score": round(100 - (missing_penalty / 40.0 * 100) if 40.0 > 0 else 100),
                "penalty": round(missing_penalty, 1),
                "pct": round(missing_pct, 2)
            },
            "duplicates": {
                "score": round(100 - (duplicate_penalty / 20.0 * 100) if 20.0 > 0 else 100),
                "penalty": round(duplicate_penalty, 1),
                "pct": round(duplicate_pct, 2)
            },
            "outliers": {
                "score": round(100 - (outlier_penalty / 15.0 * 100) if 15.0 > 0 else 100),
                "penalty": round(outlier_penalty, 1),
                "pct": round(outlier_pct, 2)
            },
            "cardinality": {
                "score": round(100 - (constant_penalty / 25.0 * 100) if 25.0 > 0 else 100),
                "penalty": round(constant_penalty, 1),
                "constant_columns": constant_cols
            }
        }
    }

# ===== UTILITY FUNCTIONS =====
def detect_problem_type(y: pd.Series) -> str:
    """Automatically detect if it's classification or regression"""
    unique_values = len(np.unique(y))
    total_values = len(y)
    
    if pd.api.types.is_string_dtype(y) or pd.api.types.is_object_dtype(y):
        return 'classification'
    
    if unique_values < 20 and pd.api.types.is_integer_dtype(y):
        return 'classification'
    
    if unique_values / total_values > 0.5:
        return 'regression'
    
    return 'classification' if unique_values < 50 else 'regression'

def get_algorithm_for_problem_type(algorithm_name: str, problem_type: str):
    """Get the correct algorithm based on problem type"""
    
    # Normalize problem type
    if problem_type and 'classification' in problem_type:
        problem_type = 'classification'
    elif problem_type and 'regression' in problem_type:
        problem_type = 'regression'
    
    # Define mapping for algorithms with both classifier and regressor variants
    algorithm_mapping = {
        'Random Forest': {
            'classification': RandomForestClassifier,
            'regression': RandomForestRegressor
        },
        'Decision Tree': {
            'classification': DecisionTreeClassifier,
            'regression': DecisionTreeRegressor
        },
        'XGBoost': {
            'classification': xgb.XGBClassifier,
            'regression': xgb.XGBRegressor
        },
        'Support Vector Machine': {
            'classification': SVC,
            'regression': SVR
        },
        'K-Nearest Neighbors': {
            'classification': KNeighborsClassifier,
            'regression': KNeighborsRegressor
        },

        'Linear Regression': {
            'classification': LogisticRegression,
            'regression': LinearRegression
        },
        'Naive Bayes': {
            'classification': GaussianNB,
            'regression': GaussianNB
        },
        'Support Vector Regression': {
            'classification': SVC,
            'regression': SVR
        },
        'Ridge Regression': {
            'classification': LogisticRegression,  
            'regression': Ridge
        },
        'Lasso Regression': {
            'classification': LogisticRegression, 
            'regression': Lasso 
        },
    }
    
    # PRIORITY 1: Check algorithm_mapping first (for algorithms with variants)
    if algorithm_name in algorithm_mapping:
        return algorithm_mapping[algorithm_name][problem_type]
    
    # PRIORITY 2: Check ALGORITHMS dict (for single-variant algorithms)
    if algorithm_name in ALGORITHMS:
        return ALGORITHMS[algorithm_name]
    
    # PRIORITY 3: Default fallback
    return RandomForestClassifier if problem_type == 'classification' else RandomForestRegressor



def initialize_algorithm_with_params(algorithm_name: str, problem_type: str, hyperparameters: dict):
    """
    Initialize algorithm with special handling for variant-based algorithms
    Supports: Naive Bayes variants, SVR, Ridge, Lasso, and all existing algorithms
    """
    # Normalize problem type
    if problem_type and 'classification' in problem_type:
        problem_type = 'classification'
    elif problem_type and 'regression' in problem_type:
        problem_type = 'regression'
        
    # Get base model class
    model_class = get_algorithm_for_problem_type(algorithm_name, problem_type)
    
    # ===== SPECIAL HANDLING FOR NAIVE BAYES =====
    if algorithm_name == 'Naive Bayes':
        variant = hyperparameters.get('variant', 'gaussian')
        
        if variant == 'gaussian':
            model_class = GaussianNB
            params = {
                'var_smoothing': float(hyperparameters.get('var_smoothing', 1e-9))
            }
        elif variant == 'multinomial':
            model_class = MultinomialNB
            params = {
                'alpha': float(hyperparameters.get('alpha', 1.0)),
                'fit_prior': bool(hyperparameters.get('fit_prior', True))
            }
        elif variant == 'bernoulli':
            model_class = BernoulliNB
            params = {
                'alpha': float(hyperparameters.get('alpha', 1.0)),
                'fit_prior': bool(hyperparameters.get('fit_prior', True))
            }
        else:
            params = {}
        
        print(f"🎯 Initializing {variant.capitalize()} Naive Bayes with params: {params}")
        return model_class(**params)

    # ===== DEFAULT INITIALIZATION FOR ALL OTHER ALGORITHMS =====
    model_params = {}
    
    # Add random_state for reproducibility (where applicable)
    if hasattr(model_class, '__init__') and 'random_state' in model_class.__init__.__code__.co_varnames:
        model_params['random_state'] = 42
    
    # Add hyperparameters
    if hyperparameters:
        # Filter out None values and special keys
        filtered_params = {
            k: v for k, v in hyperparameters.items() 
            if v is not None and k not in ['variant']
        }
        model_params.update(filtered_params)
    
    try:
        print(f"🤖 Initializing {model_class.__name__} with params: {model_params}")
        return model_class(**model_params)
    except Exception as e:
        print(f"⚠️ Failed to initialize with params, using defaults: {e}")
        return model_class()


def training_worker(config, X_train, X_test, y_train, y_test, result_queue, feature_names=None, feature_registry=None, target_classes=None):
    """
    Worker function to run training in a separate process.
    Sends progress and results back via a multiprocessing.Queue.
    """
    try:
        algorithm_name = config['algorithm_name']
        problem_type = config.get('problem_type', 'classification')
        
        # Normalize problem type
        if problem_type and 'classification' in problem_type:
            problem_type = 'classification'
        elif problem_type and 'regression' in problem_type:
            problem_type = 'regression'
            
        hyperparameters = config.get('hyperparameters', {})
        validation_method = config.get('validation_method', 'train_test_split')
        cv_folds = config.get('cv_folds', 5)
        
        # Robust target handling (belt and suspenders)
        target_column = config.get('target_column', 'target')
        if isinstance(target_column, str) and target_column.startswith('{'):
            try:
                import json
                target_json = json.loads(target_column)
                target_column = target_json.get('name', target_column)
                print(f"🎯 Worker: Parsed target_column from JSON: {target_column}")
            except:
                pass

        print(f"👷 Worker started for {algorithm_name} ({problem_type})")
        
        # Initialize model
        model = initialize_algorithm_with_params(algorithm_name, problem_type, hyperparameters)
        start_time = time.time()
        
        # Combine data for CV methods
        if validation_method in ['kfold_cv', 'grid_search', 'randomized_search']:
            if isinstance(X_train, np.ndarray):
                X_full = np.concatenate((X_train, X_test), axis=0)
                y_full = np.concatenate((y_train, y_test), axis=0)
            else:
                X_full = pd.concat([pd.DataFrame(X_train), pd.DataFrame(X_test)], axis=0).values
                y_full = pd.concat([pd.Series(y_train), pd.Series(y_test)], axis=0).values

        # Initialize metrics to avoid UnboundLocalError
        metrics = {}
        
        if validation_method in ['train_test_split', 'simple']:
            result_queue.put({'status': 'training', 'message': f'⏳ Training {algorithm_name}...'})
            print(f"⏳ Fitting model on training data...")
            model.fit(X_train, y_train)
            
            # Predict on both sets
            print(f"🔮 Making predictions...")
            y_pred_test = model.predict(X_test)
            y_pred_train = model.predict(X_train)
            
            if problem_type == 'classification':
                # Test metrics
                test_accuracy = accuracy_score(y_test, y_pred_test)
                test_precision = precision_score(y_test, y_pred_test, average='weighted', zero_division=0)
                test_recall = recall_score(y_test, y_pred_test, average='weighted', zero_division=0)
                test_f1 = f1_score(y_test, y_pred_test, average='weighted', zero_division=0)
                
                # Train metrics
                train_accuracy = accuracy_score(y_train, y_pred_train)
                train_precision = precision_score(y_train, y_pred_train, average='weighted', zero_division=0)
                train_recall = recall_score(y_train, y_pred_train, average='weighted', zero_division=0)
                train_f1 = f1_score(y_train, y_pred_train, average='weighted', zero_division=0)
                
                metrics = {
                    'validation_method': 'train_test_split',
                    'accuracy': float(test_accuracy),
                    'test_accuracy': float(test_accuracy),
                    'test_precision': float(test_precision),
                    'test_recall': float(test_recall),
                    'test_f1': float(test_f1),
                    'train_accuracy': float(train_accuracy),
                    'train_precision': float(train_precision),
                    'train_recall': float(train_recall),
                    'train_f1': float(train_f1),
                    'n_classes': int(len(np.unique(y_test))),
                    'problem_type': problem_type
                }
            else:
                # Test metrics
                test_r2 = r2_score(y_test, y_pred_test)
                test_mse = mean_squared_error(y_test, y_pred_test)
                test_mae = mean_absolute_error(y_test, y_pred_test)
                
                # Train metrics
                train_r2 = r2_score(y_train, y_pred_train)
                train_mse = mean_squared_error(y_train, y_pred_train)
                train_mae = mean_absolute_error(y_train, y_pred_train)
                
                metrics = {
                    'validation_method': 'train_test_split',
                    'r2': float(test_r2),
                    'test_r2': float(test_r2),
                    'test_mse': float(test_mse),
                    'test_mae': float(test_mae),
                    'test_rmse': float(np.sqrt(test_mse)),
                    'train_r2': float(train_r2),
                    'train_mse': float(train_mse),
                    'train_mae': float(train_mae),
                    'problem_type': problem_type
                }
                
            
        elif validation_method == 'kfold_cv':
            result_queue.put({'status': 'training', 'message': f'🔄 Running {cv_folds}-fold CV...'})
            
            if problem_type == 'classification':
                cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
                scoring = ['accuracy', 'f1_weighted', 'precision_weighted', 'recall_weighted']
            else:
                scoring = ['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error']
            
            # IMPORTANT: For multiprocessing environments on Windows, n_jobs=1 is safer inside worker processes
            print(f"🔄 Running {cv_folds}-fold CV (n_jobs=1)...")
            cv_results = cross_validate(model, X_full, y_full, cv=cv, scoring=scoring, return_train_score=True, n_jobs=1)
            print(f"✅ CV completed")
            
            if problem_type == 'classification':
                metrics = {
                    'validation_method': 'kfold_cv',
                    'cv_mean': float(cv_results['test_accuracy'].mean()),
                    'cv_std': float(cv_results['test_accuracy'].std()),
                    'cv_scores': cv_results['test_accuracy'].tolist(),
                    'test_accuracy': float(cv_results['test_accuracy'].mean()),
                    'test_f1': float(cv_results['test_f1_weighted'].mean()),
                    'test_precision': float(cv_results['test_precision_weighted'].mean()),
                    'test_recall': float(cv_results['test_recall_weighted'].mean()),
                    'train_accuracy': float(cv_results['train_accuracy'].mean()),
                    'train_f1': float(cv_results['train_f1_weighted'].mean()),
                    'train_precision': float(cv_results['train_precision_weighted'].mean()),
                    'train_recall': float(cv_results['train_recall_weighted'].mean()),
                    'problem_type': problem_type
                }
            else:
                metrics = {
                    'validation_method': 'kfold_cv',
                    'cv_mean': float(cv_results['test_r2'].mean()),
                    'cv_std': float(cv_results['test_r2'].std()),
                    'cv_scores': cv_results['test_r2'].tolist(),
                    'test_r2': float(cv_results['test_r2'].mean()),
                    'test_mse': float(-cv_results['test_neg_mean_squared_error'].mean()),
                    'test_mae': float(-cv_results['test_neg_mean_absolute_error'].mean()),
                    'train_r2': float(cv_results['train_r2'].mean()),
                    'train_mse': float(-cv_results['train_neg_mean_squared_error'].mean()),
                    'train_mae': float(-cv_results['train_neg_mean_absolute_error'].mean()),
                    'problem_type': problem_type
                }
            
            model.fit(X_full, y_full)
            

        elif validation_method in ['grid_search', 'randomized_search']:
            is_grid = (validation_method == 'grid_search')
            folds = config.get('grid_search_cv_folds' if is_grid else 'random_search_cv_folds', 5)
            
            result_queue.put({'status': 'training', 'message': f'🔍 Starting {"Grid" if is_grid else "Randomized"} Search...'})
            
            density = config.get('grid_density', 'normal')
            param_grid = get_param_grid_for_algorithm(algorithm_name, problem_type, density if is_grid else 'fine')
            
            if problem_type == 'classification':
                cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
                scoring = 'accuracy'
            else:
                cv = KFold(n_splits=folds, shuffle=True, random_state=42)
                scoring = 'r2'
            
            base_model = initialize_algorithm_with_params(algorithm_name, problem_type, {})
            
            # IMPORTANT: n_jobs=1 to avoid deadlocks on Windows sub-processes
            if is_grid:
                print(f"🔍 Starting GridSearchCV (n_jobs=1)...")
                search = GridSearchCV(base_model, param_grid, cv=cv, scoring=scoring, n_jobs=1)
            else:
                n_iter = config.get('random_search_iterations', 20)
                print(f"🎲 Starting RandomizedSearchCV (n_iter={n_iter}, n_jobs=1)...")
                search = RandomizedSearchCV(base_model, param_grid, n_iter=n_iter, cv=cv, scoring=scoring, n_jobs=1, random_state=42)
            
            search.fit(X_full, y_full)
            print(f"✅ Search completed. Best params: {search.best_params_}")
            
            model = search.best_estimator_
            
            # Extract detailed CV results for the best estimator
            best_idx = search.best_index_
            cv_mean = search.cv_results_['mean_test_score'][best_idx]
            cv_std = search.cv_results_['std_test_score'][best_idx]
            
            # Extract individual fold scores
            cv_scores = []
            for i in range(folds):
                key = f'split{i}_test_score'
                if key in search.cv_results_:
                    cv_scores.append(float(search.cv_results_[key][best_idx]))

            # Ensure best_params are native types
            clean_best_params = {}
            for k, v in search.best_params_.items():
                if hasattr(v, 'item'): 
                    clean_best_params[k] = v.item()
                else:
                    clean_best_params[k] = v
            
            # Calculate metrics on the full dataset (which was used for final fit)
            y_pred_full = model.predict(X_full)
            if problem_type == 'classification':
                train_acc = accuracy_score(y_full, y_pred_full)
                train_f1 = f1_score(y_full, y_pred_full, average='weighted', zero_division=0)
            else:
                train_acc = r2_score(y_full, y_pred_full)
                train_f1 = mean_squared_error(y_full, y_pred_full)

            metrics = {
                'validation_method': validation_method,
                'best_params': clean_best_params,
                'best_score': float(search.best_score_),
                'cv_mean': float(cv_mean),
                'cv_std': float(cv_std),
                'cv_scores': cv_scores,
                'n_iterations': len(search.cv_results_['params']),
                'test_accuracy' if problem_type == 'classification' else 'test_r2': float(search.best_score_),
                'train_accuracy' if problem_type == 'classification' else 'train_r2': float(train_acc),
                'train_f1' if problem_type == 'classification' else 'train_mse': float(train_f1),
                'problem_type': problem_type
            }
            
        # ===== CAPTURE VISUALIZATION DATA =====
        # Store predictions and actual values for visualization
        viz_data = {
            'problem_type': problem_type,
            'validation_method': validation_method,
            'algorithm_name': algorithm_name,
            'feature_names': feature_names,
            'feature_metadata': feature_registry
        }
        
        # For simple train/test split, store predictions on test set
        if validation_method in ['train_test_split', 'simple']:
            viz_data['y_train_actual'] = y_train.tolist() if hasattr(y_train, 'tolist') else list(y_train)
            viz_data['y_test_actual'] = y_test.tolist() if hasattr(y_test, 'tolist') else list(y_test)
            viz_data['y_train_pred'] = y_pred_train.tolist() if hasattr(y_pred_train, 'tolist') else list(y_pred_train)
            viz_data['y_test_pred'] = y_pred_test.tolist() if hasattr(y_pred_test, 'tolist') else list(y_pred_test)
            
            # For classification, try to get probability predictions
            if problem_type == 'classification':
                # Always try to get classes
                if target_classes:
                     viz_data['classes'] = target_classes
                     
                     # DECODE TARGETS BACK TO ORIGINAL LABELS
                     # This ensures frontend matches 'classes' (strings) with y values (now strings)
                     try:
                         viz_data['y_train_actual'] = [target_classes[int(val)] for val in viz_data['y_train_actual']]
                         viz_data['y_test_actual'] = [target_classes[int(val)] for val in viz_data['y_test_actual']]
                         viz_data['y_train_pred'] = [target_classes[int(val)] for val in viz_data['y_train_pred']]
                         viz_data['y_test_pred'] = [target_classes[int(val)] for val in viz_data['y_test_pred']]
                     except Exception as e:
                         print(f"⚠️ Failed to decode target labels: {e}")

                elif hasattr(model, 'classes_'):
                     viz_data['classes'] = model.classes_.tolist()
                else:
                     # Fallback
                     viz_data['classes'] = np.unique(y_train).tolist()

                if hasattr(model, 'predict_proba'):
                    try:
                        y_test_proba = model.predict_proba(X_test)
                        viz_data['y_test_proba'] = y_test_proba.tolist()
                    except:
                        viz_data['y_test_proba'] = None
            
            # For regression, calculate residuals
            if problem_type == 'regression':
                residuals_train = np.array(y_train) - np.array(y_pred_train)
                residuals_test = np.array(y_test) - np.array(y_pred_test)
                viz_data['residuals_train'] = residuals_train.tolist()
                viz_data['residuals_test'] = residuals_test.tolist()
        
        # For CV methods, make final predictions on the full dataset
        elif validation_method in ['kfold_cv', 'grid_search', 'randomized_search']:
            y_full_pred = model.predict(X_full)
            viz_data['y_full_actual'] = y_full.tolist() if hasattr(y_full, 'tolist') else list(y_full)
            viz_data['y_full_pred'] = y_full_pred.tolist() if hasattr(y_full_pred, 'tolist') else list(y_full_pred)
            
            if problem_type == 'classification':
                 # Always try to get classes
                if target_classes:
                     viz_data['classes'] = target_classes
                     
                     # DECODE TARGETS BACK TO ORIGINAL LABELS
                     try:
                         viz_data['y_full_actual'] = [target_classes[int(val)] for val in viz_data['y_full_actual']]
                         viz_data['y_full_pred'] = [target_classes[int(val)] for val in viz_data['y_full_pred']]
                     except Exception as e:
                         print(f"⚠️ Failed to decode target labels (CV): {e}")

                elif hasattr(model, 'classes_'):
                     viz_data['classes'] = model.classes_.tolist()
                else:
                     viz_data['classes'] = np.unique(y_full).tolist()

                if hasattr(model, 'predict_proba'):
                    try:
                        y_full_proba = model.predict_proba(X_full)
                        viz_data['y_full_proba'] = y_full_proba.tolist()
                    except:
                        viz_data['y_full_proba'] = None
            
            if problem_type == 'regression':
                residuals_full = np.array(y_full) - np.array(y_full_pred)
                viz_data['residuals_full'] = residuals_full.tolist()
        
        # Extract feature importance if available
        if hasattr(model, 'feature_importances_'):
            viz_data['feature_importance'] = model.feature_importances_.tolist()
        elif hasattr(model, 'coef_'):
            # For linear models, use absolute coefficients as importance
            coef = model.coef_
            if len(coef.shape) > 1:  # Multi-class
                viz_data['feature_importance'] = np.abs(coef).mean(axis=0).tolist()
            else:
                viz_data['feature_importance'] = np.abs(coef).tolist()
        else:
            # FALLBACK: Permutation Importance
            # This works for any model (SVM, KNN, etc.)
            try:
                from sklearn.inspection import permutation_importance
                
                # Use a subset for speed if dataset is huge
                X_val_perm = X_test if len(X_test) < 2000 else X_test[:2000]
                y_val_perm = y_test if len(y_test) < 2000 else y_test[:2000]
                
                print(f"🔄 Calculating permutation importance for {algorithm_name}...")
                perm_result = permutation_importance(
                    model, X_val_perm, y_val_perm, 
                    n_repeats=5, 
                    random_state=42, 
                    n_jobs=1
                )
                viz_data['feature_importance'] = perm_result.importances_mean.tolist()
            except Exception as e:
                print(f"⚠️ Permutation importance failed: {e}")
                viz_data['feature_importance'] = None

        # Ensure feature names are present for visualization
        if feature_names and viz_data.get('feature_importance'):
             viz_data['feature_names'] = feature_names
            
        # ===== FINALIZE & SAVE =====
        from datetime import datetime
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import os
        os.makedirs('models', exist_ok=True)
        model_path = f"models/{model_id}.joblib"
        import joblib
        joblib.dump(model, model_path)
        
        # ===== LOG ACTION =====
        # Note: training_worker runs in a separate process, so it doesn't have access to the DB dependency directly.
        # However, it can return a 'log_action' request in its final result.
        # Alternatively, we can log the action in the endpoint that handles the training result.
        
        model_info = {
            'model_id': model_id,
            'model_path': model_path,
            'algorithm': algorithm_name,
            'model_class': model.__class__.__name__,
            'problem_type': problem_type,
            'n_features': int(X_train.shape[1]),
            'n_samples_train': int(len(X_train)),
            'n_samples_test': int(len(X_test)),
            'hyperparameters': hyperparameters,
            'final_metrics': metrics,
            'trained_at': datetime.now().isoformat(),
            'validation_method': validation_method,
            'visualization_data': viz_data  # Include visualization data
        }
        
        result_queue.put({
            'status': 'success',
            'metrics': metrics,
            'model_info': model_info,
            'visualization_data': viz_data,  # Also send separately for easy access
            'message': f'✅ Training completed in {time.time() - start_time:.2f}s'
        })

    except Exception as e:
        import traceback
        result_queue.put({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        })
    






def get_param_grid_for_algorithm(algorithm_name: str, problem_type: str, grid_density: str = 'normal'):
    """
    Generate parameter grid for GridSearchCV or RandomizedSearchCV
    
    Args:
        algorithm_name: Name of the algorithm
        problem_type: 'classification' or 'regression'
        grid_density: 'coarse', 'normal', or 'fine' - controls number of parameter values
    
    Returns:
        dict: Parameter grid for the algorithm
    """
    from scipy.stats import uniform, randint
    
    # Define grids based on density
    if grid_density == 'coarse':
        n_estimators_range = [50, 100, 200]
        max_depth_range = [5, 10, 20]
        learning_rate_range = [0.01, 0.1, 0.3]
        C_range = [0.1, 1.0, 10.0]
        n_neighbors_range = [3, 5, 10]
    elif grid_density == 'fine':
        n_estimators_range = [50, 100, 150, 200, 300, 500]
        max_depth_range = [3, 5, 7, 10, 15, 20, 30]
        learning_rate_range = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3]
        C_range = [0.01, 0.1, 1.0, 10.0, 100.0]
        n_neighbors_range = [3, 5, 7, 10, 15, 20]
    else:  # normal
        n_estimators_range = [50, 100, 200, 300]
        max_depth_range = [5, 10, 15, 20]
        learning_rate_range = [0.01, 0.05, 0.1, 0.2]
        C_range = [0.1, 1.0, 10.0, 50.0]
        n_neighbors_range = [3, 5, 7, 10, 15]
    
    param_grids = {
        "Random Forest": {
            'n_estimators': n_estimators_range,
            'max_depth': max_depth_range + [None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        },
        
        "XGBoost": {
            'n_estimators': n_estimators_range,
            'max_depth': [3, 5, 7, 10],
            'learning_rate': learning_rate_range,
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0]
        },
        
        "Logistic Regression": {
            'C': C_range,
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'saga'],
            'max_iter': [100, 200, 500]
        },
        
        "Support Vector Machine": {
            'C': C_range,
            'kernel': ['linear', 'rbf', 'poly'],
            'gamma': ['scale', 'auto']
        },
        
        "Support Vector Regression": {
            'C': C_range,
            'kernel': ['linear', 'rbf', 'poly'],
            'gamma': ['scale', 'auto'],
            'epsilon': [0.01, 0.1, 0.5]
        },
        
        "K-Nearest Neighbors": {
            'n_neighbors': n_neighbors_range,
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        },
        
        "Decision Tree": {
            'max_depth': max_depth_range + [None],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 2, 4, 8],
            'criterion': ['gini', 'entropy'] if problem_type == 'classification' else ['squared_error', 'friedman_mse']
        },
        
        "Ridge Regression": {
            'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr']
        },
        
        "Lasso Regression": {
            'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
            'selection': ['cyclic', 'random']
        },
        
        "Naive Bayes": {
            'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6] if problem_type == 'classification' else []
        }
    }
    
    # Return the grid for the specified algorithm
    return param_grids.get(algorithm_name, {})


# ===== INSIGHT GENERATION HELPERS =====

def generate_regression_insights(viz_data):
    insights = []
    
    # Analyze R2 if available (usually in final_metrics)
    # But here we analyze the plot data
    y_actual = np.array(viz_data.get('y_test_actual', viz_data.get('y_full_actual', [])))
    y_pred = np.array(viz_data.get('y_test_pred', viz_data.get('y_full_pred', [])))
    
    if len(y_actual) > 0 and len(y_pred) > 0:
        r2 = r2_score(y_actual, y_pred)
        
        # Actual vs Predicted Plot Insights
        if r2 > 0.8:
            insights.append({
                "plot": "actual_vs_predicted",
                "text": "Predictions follow the diagonal closely, indicating strong accuracy.",
                "verdict": "good"
            })
        elif r2 > 0.5:
            insights.append({
                "plot": "actual_vs_predicted",
                "text": "Predictions show moderate accuracy with some scatter.",
                "verdict": "moderate"
            })
        else:
            insights.append({
                "plot": "actual_vs_predicted",
                "text": "Wide scatter suggests the model struggles to predict these values accurately.",
                "verdict": "poor"
            })
            
        # Residual Plot Insights
        residuals = y_actual - y_pred
        std_resid = np.std(residuals)
        
        # Simple check for bias
        mean_resid = np.mean(residuals)
        if abs(mean_resid) > 0.1 * np.std(y_actual):
            insights.append({
                "plot": "residuals",
                "text": f"Average error is {mean_resid:.2f}, suggesting systematic {'under' if mean_resid > 0 else 'over'}-prediction.",
                "verdict": "warning"
            })
        else:
            insights.append({
                "plot": "residuals",
                "text": "Residuals are centered around zero, which is desirable.",
                "verdict": "good"
            })
            
        # check for funnel shape (heteroscedasticity) - very simple heuristic
        # Split predictions into two halves and check variance ratio
        mid = len(y_pred) // 2
        sorted_indices = np.argsort(y_pred)
        first_half_resid = residuals[sorted_indices[:mid]]
        second_half_resid = residuals[sorted_indices[mid:]]
        var_ratio = np.var(second_half_resid) / np.var(first_half_resid) if np.var(first_half_resid) > 0 else 1
        
        if var_ratio > 2.0 or var_ratio < 0.5:
            insights.append({
                "plot": "residuals",
                "text": "Error variance changes with predicted values, suggesting unreliable predictions at some scales.",
                "verdict": "warning"
            })
            
    return insights

def generate_classification_insights(viz_data):
    insights = []
    
    y_actual = np.array(viz_data.get('y_test_actual', viz_data.get('y_full_actual', [])))
    y_pred = np.array(viz_data.get('y_test_pred', viz_data.get('y_full_pred', [])))
    
    if len(y_actual) > 0 and len(y_pred) > 0:
        acc = accuracy_score(y_actual, y_pred)
        
        # Confusion Matrix Insights
        if acc > 0.85:
            insights.append({
                "plot": "confusion_matrix",
                "text": "Model correctly classifies most cases across all classes.",
                "verdict": "good"
            })
        elif acc > 0.6:
            insights.append({
                "plot": "confusion_matrix",
                "text": "Model shows reasonable performance but has noticeable misclassifications.",
                "verdict": "moderate"
            })
        else:
            insights.append({
                "plot": "confusion_matrix",
                "text": "Model struggles significantly with class separation.",
                "verdict": "poor"
            })
            
        # ROC Insights (Binary only implied by y_proba presence)
        if 'y_test_proba' in viz_data and viz_data['y_test_proba'] is not None:
            # We don't calculate AUC here to keep it fast, but we can comment on separation
            insights.append({
                "plot": "roc_curve",
                "text": "Smooth curve indicates consistent trade-off between sensitivity and specificity.",
                "verdict": "good"
            })
            
    return insights


# ===== VISUALIZATION DATA ENDPOINT =====

@app.get("/api/get-visualization-data/{model_id}")
async def get_visualization_data(model_id: str):
    """
    Retrieve all data needed for model performance visualization
    """
    if model_id not in trained_models:
        raise HTTPException(status_code=404, detail="Model not found")
        
    m_info = trained_models[model_id]
    v_data = visualization_data.get(model_id, {})
    
    if not v_data:
        # Fallback for older models or failed captures
        return {
            "success": False,
            "message": "No visualization data available for this model",
            "model_summary": m_info
        }
        
    # Generate insights on the fly or retrieve stored ones
    problem_type = v_data.get('problem_type', 'classification')
    if problem_type == 'regression':
        insights = generate_regression_insights(v_data)
    else:
        insights = generate_classification_insights(v_data)
        
    return {
        "success": True,
        "model_summary": {
            "model_id": model_id,
            "algorithm": m_info.get('algorithm'),
            "problem_type": problem_type,
            "samples_train": m_info.get('n_samples_train'),
            "samples_test": m_info.get('n_samples_test'),
            "dataset_id": m_info.get('dataset_id'),
            "validation_method": m_info.get('validation_method'),
            "final_metrics": m_info.get('final_metrics')
        },
        "plot_data": v_data,
        "insights": insights
    }


# ===== API ENDPOINTS =====


@app.get("/api/health")
async def health_check():
    """Health check with detailed status"""
    try:
        import sklearn
        
        return {
            "status": "healthy",
            "message": "DataSage ML Backend Running",
            "versions": {
                "sklearn": sklearn.__version__,
                "pandas": pd.__version__,
                "numpy": np.__version__,
                "xgboost": xgb.__version__,
                "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            },
            "capabilities": {
                "real_training": True,
                "feature_scaling": ["standard", "minmax", "robust"],
                "feature_engineering": ["polynomial", "pca", "feature_selection"],
                "validation_methods": ["train_test_split", "cross_validation", "stratified"],
                "sklearn_algorithms": list(ALGORITHMS.keys()),
                "preprocessing": "SimpleImputer + scikit-learn",
                "model_persistence": "joblib"
            },
            "stats": {
                "datasets_loaded": len(datasets),
                "trained_models": len(trained_models),
                "active_scalers": len(scalers)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# ===== DASHBOARD ENDPOINTS =====

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Aggregate dashboard statistics for the current user"""
    print(f"📊 Dashboard Stats requested by user: {current_user.get('username')}")
    try:
        user_id = current_user['id']
        from models import Dataset as DatasetModel, Model as ModelModel, UserAction
        
        dataset_count = db.query(DatasetModel).filter(DatasetModel.user_id == user_id).count()
        model_count = db.query(ModelModel).filter(ModelModel.user_id == user_id).count()
        
        # Calculate average health score
        total_quality = 0
        calculated_datasets = 0
        recent_datasets = db.query(DatasetModel).filter(DatasetModel.user_id == user_id).order_by(DatasetModel.upload_date.desc()).limit(5).all()
        
        for ds in recent_datasets:
            if ds.column_metadata and 'quality_score' in ds.column_metadata:
                total_quality += ds.column_metadata['quality_score']
                calculated_datasets += 1
                
        avg_quality = int(total_quality / calculated_datasets) if calculated_datasets > 0 else 0
        
        # Get latest model accuracy
        latest_model = db.query(ModelModel).filter(ModelModel.user_id == user_id).order_by(ModelModel.created_at.desc()).first()
        best_accuracy = 0
        if latest_model and latest_model.metrics:
            # Check for various accuracy metric names
            best_accuracy = latest_model.metrics.get('accuracy', latest_model.metrics.get('r2', 0))
            
        return {
            "projects": dataset_count,
            "models": model_count,
            "dataHealth": avg_quality,
            "bestAccuracy": round(best_accuracy * 100, 1) if best_accuracy <= 1 else round(best_accuracy, 1),
            "recentActivityCount": db.query(UserAction).filter(UserAction.user_id == user_id).count()
        }
    except Exception as e:
        print(f"❌ Dashboard Stats Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/dashboard/activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Get recent user actions"""
    print(f"📡 Recent Activity requested by user: {current_user.get('username')}")
    try:
        user_id = current_user['id']
        from models import UserAction
        
        actions = db.query(UserAction).filter(UserAction.user_id == user_id).order_by(UserAction.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": a.id,
                "action_type": a.action_type,
                "details": a.action_details,
                "resource_id": a.resource_id,
                "resource_type": a.resource_type,
                "created_at": a.created_at.isoformat() + "Z" if a.created_at.isoformat().endswith('Z') == False else a.created_at.isoformat()
            }
            for a in actions
        ]
    except Exception as e:
        print(f"❌ Recent Activity Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def list_models(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """List all models trained by user"""
    user_id = current_user['id']
    from models import Model as ModelModel
    
    models_db = db.query(ModelModel).filter(ModelModel.user_id == user_id).order_by(ModelModel.created_at.desc()).all()
    
    return [
        {
            "id": m.id,
            "name": m.name,
            "algorithm": m.algorithm,
            "metrics": m.metrics,
            "hyperparameters": m.hyperparameters,
            "createdAt": m.created_at.isoformat() + "Z",
            "dataset_id": m.dataset_id
        }
        for m in models_db
    ]

@app.post("/api/upload-dataset")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Upload and analyze CSV dataset - Persisted with 15-dataset limit"""
    try:
        user_id = current_user['id']
        
        # 0. Check dataset limit (30 max)
        dataset_count = db.query(DatasetModel).filter(DatasetModel.user_id == user_id).count()
        if dataset_count >= 30:
            print(f"⚠️ User {user_id} reached dataset limit (30). Blocked upload.")
            raise HTTPException(
                status_code=400, 
                detail="Dataset limit reached (30 max). Please delete old datasets to upload new ones."
            )

        print(f"Receiving file upload: {file.filename}")
        
        # 1. Save file to disk
        file_path = await file_service.save_dataset(file, user_id)
        
        # 2. Read DataFrame for analysis based on file extension
        ext = file.filename.lower()
        try:
            if ext.endswith('.csv'):
                df = pd.read_csv(file_path, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
            elif ext.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            elif ext.endswith('.json'):
                df = pd.read_json(file_path)
            elif ext.endswith('.xlsx') or ext.endswith('.xls'):
                df = pd.read_excel(file_path, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
            else:
                # Fallback to CSV if extension is unknown but might be a text file
                df = pd.read_csv(file_path, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
        except Exception as e:
            # Clean up file if reading fails
            if os.path.exists(file_path):
                os.remove(file_path)
            print(f"❌ Failed to parse uploaded file {file.filename}: {e}")
            raise HTTPException(status_code=400, detail=f"Failed to parse as {ext.split('.')[-1].upper()}: {str(e)}")
            
        # 3. Create DB Record
        dataset = DatasetModel(
            user_id=user_id,
            name=file.filename,
            storage_path=file_path,
            row_count=len(df),
            column_count=len(df.columns),
            size_bytes=os.path.getsize(file_path),
            is_processed=False
        )
        
        # 3.1 Calculate Quality Score for Dashboard
        try:
            # Quick partial stats for quality score
            missing_values = {str(col): int(df[col].isnull().sum()) for col in df.columns}
            duplicates = int(df.duplicated().sum())
            
            # Simple Column Stats for quality calculation
            col_stats = []
            for col in df.columns:
                unique_count = int(df[col].nunique())
                col_stats.append({"name": str(col), "unique": unique_count})
            
            # Outlier count (Quick IQR)
            outliers = 0
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                v = df[col].dropna()
                if len(v) > 0:
                    q1, q3 = v.quantile([0.25, 0.75])
                    iqr = q3 - q1
                    outliers += int(((v < (q1 - 1.5 * iqr)) | (v > (q3 + 1.5 * iqr))).sum())
            
            partial_stats = {
                "missing_values": missing_values,
                "duplicates": duplicates,
                "outliers": outliers,
                "column_stats": col_stats
            }
            
            quality_info = calculate_quality_score(df, partial_stats)
            dataset.column_metadata = {"quality_score": quality_info["score"]}
            print(f"✅ Initial Quality Score calculated: {quality_info['score']}")
        except Exception as q_err:
            print(f"⚠️ Could not calculate initial quality score: {q_err}")
            dataset.column_metadata = {"quality_score": 0} # Default

        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        dataset_id = str(dataset.id)
        
        # 3.2 Log Action
        log_user_action(db, user_id, "upload", {"filename": file.filename, "rows": len(df)}, resource_id=dataset.id, resource_type="dataset")

        # 3.5 Populate Global Storage
        datasets[dataset_id] = {
            'dataframe': df,
            'filename': file.filename,
            'upload_time': datetime.now(),
            'is_processed': False,
            'user_id': user_id
        }

        # 4. Prepare Response
        sample_size = min(200, len(df))
        sample_df = df.head(sample_size)
        
        sample_data = []
        for idx, row in sample_df.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    if np.isnan(value) or np.isinf(value):
                        row_dict[str(col)] = None
                    else:
                        row_dict[str(col)] = float(value)
                elif isinstance(value, (np.bool_, bool)):
                    row_dict[str(col)] = bool(value)
                else:
                    row_dict[str(col)] = str(value)
            sample_data.append(row_dict)
            
        statistics = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats_df = df[numeric_cols].describe()
            for col in numeric_cols:
                col_stats = {}
                for stat in stats_df.index:
                    val = stats_df.loc[stat, col]
                    col_stats[str(stat)] = float(val) if pd.notna(val) else 0.0
                statistics[str(col)] = col_stats

        return {
            'dataset_id': dataset_id,
            'filename': dataset.name,
            'shape': [dataset.row_count, dataset.column_count],
            'columns': [str(col) for col in df.columns.tolist()],
            'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
            'sample_data': sample_data,
            'statistics': statistics,
            'upload_time': dataset.upload_date.isoformat() + "Z",
            'success': True,
            'total_rows': dataset.row_count,
            'total_columns': dataset.column_count,
            'warning': None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/export-dataset/{dataset_id}")
async def export_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Export full dataset as CSV"""
    try:
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        if dataset.user_id != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # PRIORITIZE IN-MEMORY DATA (This includes unsaved preprocessing steps)
        if str(dataset_id) in datasets:
            print(f"Using in-memory dataframe for export (Dataset {dataset_id})")
            df = datasets[str(dataset_id)]['dataframe']
        else:
            print(f"Loading dataframe from disk for export (Dataset {dataset_id})")
            df = file_service.load_dataframe(dataset.storage_path)
        
        filename = dataset.name.replace(".csv", "") + "_exported.csv"
        
        def iter_csv():
            chunk_size = 5000
            for i in range(0, len(df), chunk_size):
                buffer = io.StringIO()
                # Write header only for the first chunk
                header = (i == 0)
                df.iloc[i:i+chunk_size].to_csv(buffer, index=False, header=header)
                yield buffer.getvalue()
        
        return StreamingResponse(
            iter_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Export error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export-train/{dataset_id}")
async def export_train_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Export full training dataset as CSV (with all transformations applied)"""
    global X_train_storage, y_train_storage
    
    try:
        print(f"\n{'='*80}")
        print(f"📥 EXPORT TRAIN DATASET: {dataset_id}")
        print(f"{'='*80}")
        
        # Check if dataset exists
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Check if dataset is split
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset not split yet. Please split first.")
        
        # Check if split data exists
        if dataset_id not in X_train_storage or dataset_id not in y_train_storage:
            raise HTTPException(status_code=400, detail="Training data not found in storage")
        
        # Get train data
        X_train = X_train_storage[dataset_id]
        y_train = y_train_storage[dataset_id]
        
        # Combine features and target
        train_df = pd.concat([X_train, y_train], axis=1)
        
        print(f"✅ Exporting training dataset: {len(train_df)} rows, {len(train_df.columns)} columns")
        
        # Generate filename
        original_filename = datasets[dataset_id].get("filename", "dataset.csv")
        filename = original_filename.replace(".csv", "") + "_train.csv"
        
        print(f"📄 Filename: {filename}")
        
        # Stream CSV
        def iter_csv():
            chunk_size = 5000
            for i in range(0, len(train_df), chunk_size):
                buffer = io.StringIO()
                header = (i == 0)
                train_df.iloc[i:i+chunk_size].to_csv(buffer, index=False, header=header)
                yield buffer.getvalue()
        
        print(f"✅ Streaming {len(train_df)} rows...")
        print(f"{'='*80}\n")
        
        return StreamingResponse(
            iter_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Export train error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export-test/{dataset_id}")
async def export_test_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Export full test dataset as CSV (with all transformations applied)"""
    global X_test_storage, y_test_storage
    
    try:
        print(f"\n{'='*80}")
        print(f"📥 EXPORT TEST DATASET: {dataset_id}")
        print(f"{'='*80}")
        
        # Check if dataset exists
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Check if dataset is split
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset not split yet. Please split first.")
        
        # Check if split data exists
        if dataset_id not in X_test_storage or dataset_id not in y_test_storage:
            raise HTTPException(status_code=400, detail="Test data not found in storage")
        
        # Get test data
        X_test = X_test_storage[dataset_id]
        y_test = y_test_storage[dataset_id]
        
        # Combine features and target
        test_df = pd.concat([X_test, y_test], axis=1)
        
        print(f"✅ Exporting test dataset: {len(test_df)} rows, {len(test_df.columns)} columns")
        
        # Generate filename
        original_filename = datasets[dataset_id].get("filename", "dataset.csv")
        filename = original_filename.replace(".csv", "") + "_test.csv"
        
        print(f"📄 Filename: {filename}")
        
        # Stream CSV
        def iter_csv():
            chunk_size = 5000
            for i in range(0, len(test_df), chunk_size):
                buffer = io.StringIO()
                header = (i == 0)
                test_df.iloc[i:i+chunk_size].to_csv(buffer, index=False, header=header)
                yield buffer.getvalue()
        
        print(f"✅ Streaming {len(test_df)} rows...")
        print(f"{'='*80}\n")
        
        return StreamingResponse(
            iter_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Export test error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ===== RE-HYDRATION HELPERS =====

async def ensure_dataset_in_memory(dataset_id: str, db: Session):
    """Ensure dataset is loaded into the global memory storage"""
    global datasets
    
    if dataset_id in datasets:
        return datasets[dataset_id]
        
    try:
        print(f"🔄 Attempting to re-hydrate dataset {dataset_id}...")
        try:
            db_id = int(dataset_id)
        except ValueError:
            print(f"⚠️ Invalid dataset ID format: {dataset_id}")
            return None
            
        dataset = db.query(DatasetModel).filter(DatasetModel.id == db_id).first()
        
        if not dataset:
            print(f"❌ Re-hydration failed: Dataset {dataset_id} not found in DB")
            return None
            
        # Load from disk
        df = file_service.load_dataframe(dataset.storage_path)
        
        datasets[dataset_id] = {
            'dataframe': df,
            'filename': dataset.name,
            'upload_time': dataset.upload_date,
            'is_processed': dataset.is_processed,
            'user_id': dataset.user_id
        }
        
        print(f"✅ Re-hydrated dataset {dataset_id} ({len(df)} rows)")
        return datasets[dataset_id]
        
    except Exception as e:
        print(f"❌ Re-hydration error for {dataset_id}: {str(e)}")
        return None


@app.get("/api/datasets/{dataset_id}")
async def get_dataset_info(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Get specific dataset information with sample data - Persisted"""
    try:
        # 1. Fetch from DB
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        # Check ownership
        if dataset.user_id != current_user['id']:
             raise HTTPException(status_code=403, detail="Not authorized to access this dataset")

        # 2. Load Dataframe (Memory First)
        if dataset_id in datasets:
            df = datasets[dataset_id]['dataframe']
            print(f"✅ Using in-memory dataset {dataset_id}")
        else:
            try:
                df = file_service.load_dataframe(dataset.storage_path)
                
                # 2.5 Populate Global Storage if missing
                print(f"🔄 Restoring dataset {dataset_id} to memory")
                datasets[dataset_id] = {
                    'dataframe': df,
                    'filename': dataset.name,
                    'upload_time': dataset.upload_date,
                    'is_processed': dataset.is_processed,
                }
                    
            except FileNotFoundError:
                 raise HTTPException(status_code=404, detail="Dataset file not found on disk")

        # 3. Prepare Sample
        sample_size = min(200, len(df))
        sample_df = df.head(sample_size)
        
        sample_data = []
        for idx, row in sample_df.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    if np.isnan(value) or np.isinf(value):
                        row_dict[str(col)] = None
                    else:
                        row_dict[str(col)] = float(value)
                elif isinstance(value, (np.bool_, bool)):
                    row_dict[str(col)] = bool(value)
                else:
                    row_dict[str(col)] = str(value)
            sample_data.append(row_dict)

        # 4. Check for Split/Scaling state in memory
        is_split = False
        is_scaled = False
        split_info = None
        train_preview = []
        test_preview = []
        
        if dataset_id in datasets:
            meta = datasets[dataset_id]
            is_split = meta.get('is_split', False)
            is_scaled = meta.get('is_scaled', False)
            split_info = meta.get('split_info')
            
            # If split, get previews from in-memory globals first
            if is_split and dataset_id in X_train_storage and dataset_id in y_train_storage:
                X_tr = X_train_storage[dataset_id]
                y_tr = y_train_storage[dataset_id]
                train_preview = pd.concat([X_tr.head(200), y_tr.head(200)], axis=1).to_dict('records')
                
                if dataset_id in X_test_storage and dataset_id in y_test_storage:
                    X_te = X_test_storage[dataset_id]
                    y_te = y_test_storage[dataset_id]
                    test_preview = pd.concat([X_te.head(200), y_te.head(200)], axis=1).to_dict('records')

        # ── PERSISTENCE FIX ──────────────────────────────────────────────────
        # If in-memory previews are empty (e.g. after backend restart), fall
        # back to the previews we persisted in column_metadata at split time.
        db_meta = dataset.column_metadata or {}
        cached_previews = db_meta.get("_split_previews", {})
        if cached_previews:
            # We have DB-persisted split state — trust it.
            if not is_split:
                is_split = True
                split_info = split_info or {
                    "train_size": cached_previews.get("train_size"),
                    "test_size": cached_previews.get("test_size"),
                }
            if not train_preview:
                train_preview = cached_previews.get("train", [])
                print(f"✅ Restored train preview from DB ({len(train_preview)} rows)")
            if not test_preview:
                test_preview = cached_previews.get("test", [])
                print(f"✅ Restored test preview from DB ({len(test_preview)} rows)")
        # ─────────────────────────────────────────────────────────────────────

        return {
            'dataset_id': str(dataset.id),
            'filename': dataset.name,
            'shape': [dataset.row_count, dataset.column_count],
            'total_rows': dataset.row_count,
            'columns': [str(col) for col in df.columns.tolist()],
            'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
            'preprocessed': dataset.is_processed,
            'uploaded_at': dataset.upload_date.isoformat() + "Z",
            'sample_data': sample_data,
            'status': 'success',
            'is_split': is_split, 
            'is_scaled': is_scaled,
            'split_info': split_info,
            'train_preview': train_preview,
            'test_preview': test_preview
        } 
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_dataset_info: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching dataset: {str(e)}")


@app.get("/api/datasets/{dataset_id}/statistics")
async def get_dataset_statistics(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Get complete dataset statistics calculated on ALL rows (not just preview)"""
    try:
        # 1. Fetch from DB
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        # Check ownership
        if dataset.user_id != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized to access this dataset")

        # Load semantic metadata if available
        column_metadata = dataset.column_metadata or {}

        # 2. Load COMPLETE Dataframe (Memory First)
        if dataset_id in datasets:
            df = datasets[dataset_id]['dataframe']
        else:
            try:
                df = file_service.load_dataframe(dataset.storage_path)
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Dataset file not found on disk")

        print(f"\n📊 DEBUG: get_dataset_statistics called")
        print(f"   Dataset ID: {dataset_id}")
        print(f"   Dataset name: {dataset.name}")
        print(f"   Storage path: {dataset.storage_path}")
        print(f"   Is processed: {dataset.is_processed}")
        print(f"   Calculating statistics on COMPLETE dataset: {len(df)} rows")

        # 3. Calculate Missing Values and Column Stats
        missing_values = {}
        missing_info = []
        column_stats = []
        
        for col in df.columns:
            missing_count = int(df[col].isnull().sum())
            unique_count = int(df[col].nunique())
            
            # Detect column type
            col_type = "categorical"
            if pd.api.types.is_numeric_dtype(df[col]):
                col_type = "numerical"
            
            # ✅ Determine semantic type (from metadata override or auto-detect)
            semantic_info = None
            if str(col) in column_metadata:
                semantic_info = column_metadata[str(col)]
                sem_type = semantic_info.get("semantic_type", "unknown")
            else:
                semantic_info = detect_semantic_type(df[col])
                sem_type = semantic_info.get("semantic_type", "unknown")
            
            # Normalize naming: "numerical" -> "numeric" for frontend consistency
            if sem_type == "numerical":
                sem_type = "numeric"
            
            # [Fix] Force col_type to categorical if semantic type is boolean
            # This ensures we get value_counts instead of histogram for binary columns
            if sem_type == "boolean":
                col_type = "categorical"
            
            # Base stats
            stat_entry = {
                "name": str(col),
                "type": col_type,
                "semanticType": sem_type,  # For frontend compatibility
                "semantic_type": sem_type, # For backend consistency
                "unique": unique_count,
                "missing": missing_count,
                "top_values": [],
                "distribution": None,
                "detailed_metrics": None
            }

            try:
                if col_type == "numerical":
                    # Calculate histogram and box plot stats for numerical columns
                    clean_series = df[col].dropna()
                    if not clean_series.empty:
                        # Histogram
                        counts, bin_edges = np.histogram(clean_series, bins='auto')
                        # Box plot
                        quantiles = clean_series.quantile([0, 0.25, 0.5, 0.75, 1]).tolist()
                        
                        stat_entry["distribution"] = {
                            "type": "numerical",
                            "histogram": {
                                "counts": counts.tolist(),
                                "bin_edges": bin_edges.tolist()
                            },
                            "box_plot": {
                                "min": quantiles[0],
                                "q1": quantiles[1],
                                "median": quantiles[2],
                                "q3": quantiles[3],
                                "max": quantiles[4]
                            }
                        }
                        
                        # Detailed Metrics for Numerical
                        iqr = float(quantiles[3] - quantiles[1])
                        outliers_mask = (clean_series < (quantiles[1] - 1.5 * iqr)) | (clean_series > (quantiles[3] + 1.5 * iqr))
                        
                        stat_entry["detailed_metrics"] = {
                            "mean": float(clean_series.mean()),
                            "std": float(clean_series.std()) if len(clean_series) > 1 else 0,
                            "median": float(clean_series.median()),
                            "min": float(clean_series.min()),
                            "max": float(clean_series.max()),
                            "range": float(clean_series.max() - clean_series.min()),
                            "skewness": float(clean_series.skew()) if len(clean_series) > 1 else 0,
                            "iqr": iqr,
                            "outliers_count": int(outliers_mask.sum()),
                            "zeros_pct": float((clean_series == 0).sum() / len(clean_series) * 100) if not clean_series.empty else 0
                        }
                else: 
                    # Calculate value counts for categorical columns
                    top_vals_series = df[col].value_counts()
                    top_15_series = top_vals_series.head(15) 
                    
                    top_vals = top_15_series.index.tolist()
                    stat_entry["top_values"] = [str(v) for v in top_vals] 
                    
                    stat_entry["distribution"] = {
                        "type": "categorical",
                        "value_counts": {str(k): int(v) for k, v in top_15_series.items()}
                    }
                    
                    # Detailed Metrics for Categorical
                    if not top_vals_series.empty:
                        majority_class = top_vals_series.index[0]
                        majority_count = top_vals_series.iloc[0]
                        minority_class = top_vals_series.index[-1]
                        minority_count = top_vals_series.iloc[-1]
                        total_count = top_vals_series.sum()
                        
                        stat_entry["detailed_metrics"] = {
                            "class_count": len(top_vals_series),
                            "majority_class": {
                                "name": str(majority_class),
                                "percent": round((majority_count / total_count) * 100, 1) if total_count > 0 else 0
                            },
                            "minority_class": {
                                "name": str(minority_class),
                                "percent": round((minority_count / total_count) * 100, 1) if total_count > 0 else 0
                            },
                            "imbalance_ratio": round(majority_count / minority_count, 2) if minority_count > 0 else float('inf')
                        }
            except Exception as e:
                print(f"Error calculating distribution/metrics for {col}: {e}")

            column_stats.append(stat_entry)

            if missing_count > 0:
                missing_values[str(col)] = missing_count
                
                missing_info.append({
                    "name": str(col),
                    "type": col_type,
                    "semanticType": sem_type,  # Added
                    "semantic_type": sem_type, # Added
                    "count": missing_count,
                    "percentage": f"{(missing_count / len(df) * 100):.1f}",
                    "strategy": "fillmedian" if col_type == "numerical" else "fillmode"
                })

        # 4. Calculate Duplicates
        duplicates = int(df.duplicated().sum())

        # 5. Calculate Outliers (for numerical columns only)
        outliers = 0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            values = df[col].dropna()
            if len(values) > 0:
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers += int(((values < lower_bound) | (values > upper_bound)).sum())

        print(f"✅ Statistics calculated:")
        print(f"   Total Rows: {len(df)}")
        print(f"   Missing Columns: {len(missing_info)}")
        print(f"   Duplicates: {duplicates}")
        print(f"   Outliers: {outliers}")

        # 6. Calculate Quality Score
        partial_stats = {
            "missing_values": missing_values,
            "duplicates": duplicates,
            "outliers": outliers,
            "column_stats": column_stats
        }
        quality_info = calculate_quality_score(df, partial_stats)

        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": missing_values,
            "missing_info": missing_info,
            "column_stats": column_stats,
            "duplicates": duplicates,
            "outliers": outliers,
            "quality_score": quality_info["score"],
            "quality_breakdown": quality_info["breakdown"],
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")


# ===== SEMANTIC DATA TYPE DETECTION & CONVERSION =====

@app.get("/api/datasets/{dataset_id}/semantic-types")
async def get_semantic_types(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Detect and return semantic data types for each column"""
    try:
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Load data to detect types (Memory First)
        if dataset_id in datasets:
            df = datasets[dataset_id]['dataframe']
        else:
            df = file_service.load_dataframe(dataset.storage_path)
        
        # Get existing metadata for overrides
        existing_metadata = dataset.column_metadata or {}
        
        results = []
        is_auto_verified = True
        
        for col in df.columns:
            # Check if we have an override
            if col in existing_metadata and existing_metadata[col].get("is_override"):
                results.append(existing_metadata[col])
            else:
                # Auto-detect
                detection = detect_semantic_type(df[col])
                results.append(detection)
                # Auto-verification criteria: all detections must be high confidence
                if detection.get("confidence") != "high":
                    is_auto_verified = False
                
        return {
            "dataset_id": dataset_id,
            "column_types": results,
            "is_verified": dataset.column_metadata.get("_is_verified", False) if dataset.column_metadata else False,
            "is_auto_verified": is_auto_verified,
            "status": "success"
        }
    except Exception as e:
        print(f"Error detecting semantic types: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/datasets/{dataset_id}/columns/{column_name}/insights")
async def get_column_insights(
    dataset_id: str,
    column_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Fetch detailed diagnostic insights for a specific column"""
    try:
        # 1. Fetch dataset and verify
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        if dataset.user_id != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized")

        # 2. Load Dataframe
        if dataset_id in datasets:
            df = datasets[dataset_id]['dataframe']
        else:
            df = file_service.load_dataframe(dataset.storage_path)
            datasets[dataset_id] = {
                'dataframe': df,
                'filename': dataset.name,
                'upload_time': dataset.upload_date,
                'is_processed': dataset.is_processed,
            }

        if column_name not in df.columns:
            raise HTTPException(status_code=404, detail=f"Column '{column_name}' not found")

        col_data = df[column_name]
        clean_data = col_data.dropna()
        total_rows = len(df)
        missing_count = int(col_data.isnull().sum())
        missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows > 0 else 0
        unique_count = int(col_data.nunique())

        # Semantic type detection (Check overrides first)
        column_metadata = dataset.column_metadata or {}
        if str(column_name) in column_metadata:
            semantic_type = column_metadata[str(column_name)].get("semantic_type", "unknown")
        else:
            semantic_type = detect_semantic_type(col_data).get("semantic_type", "unknown")

        # Determine processing path
        # 1. DateTime takes priority
        is_datetime = semantic_type.lower() in ["datetime", "date", "timestamp", "time"]
        
        # 2. Categorical takes priority over Numeric if explicitly set
        # This list covers all common non-numeric semantic types
        is_categorical = semantic_type in [
            "categorical", "boolean", "identifier", "email", "url", "phone",
            "gender", "country", "state", "city", "address", "zipcode",
            "department", "occupation", "company", "color"
        ]
        
        # 3. Numeric if it's either explicitly numeric OR it's numeric data and not categorical/datetime
        is_numeric = (semantic_type == "numeric") or (
            pd.api.types.is_numeric_dtype(col_data) and not is_categorical and not is_datetime
        )
        
        # Final decision: Categorical if it's not datetime and not numeric (or explicitly categorical)
        if not is_datetime and not is_numeric:
            is_categorical = True

        insights = {
            "column_name": column_name,
            "semantic_type": semantic_type,
            "missing_pct": missing_pct,
            "unique_count": unique_count,
            "suggested_actions": []
        }

        if is_datetime:
            # Handle DateTime Columns
            temp_dt = pd.to_datetime(clean_data, errors='coerce')
            valid_dt = temp_dt.dropna()
            
            invalid_count = len(clean_data) - len(valid_dt)
            
            # Initialize with basic datetime info
            insights.update({
                "type": "datetime",
                "invalid_count": invalid_count,
                "min_date": None,
                "max_date": None,
                "date_range": "N/A",
                "granularity": "N/A",
                "distribution": {"time_frequency": {}}
            })

            if not valid_dt.empty:
                min_date = valid_dt.min()
                max_date = valid_dt.max()
                date_range = str(max_date - min_date)
                
                # Granularity estimation
                diffs = valid_dt.sort_values().diff().dropna()
                if not diffs.empty:
                    median_diff = diffs.median()
                    granularity = str(median_diff)
                else:
                    granularity = "Single value"

                # Frequency distribution (by day or month based on range)
                days_span = (max_date - min_date).days
                if days_span < 30:
                    freq = 'D'
                elif days_span < 365 * 2:
                    freq = 'M'
                else:
                    freq = 'Y'
                
                freq_counts = valid_dt.value_counts().resample(freq).sum().tail(50)
                
                insights.update({
                    "min_date": min_date.isoformat(),
                    "max_date": max_date.isoformat(),
                    "date_range": date_range,
                    "granularity": granularity,
                    "distribution": {
                        "time_frequency": {str(k.date()): int(v) for k, v in freq_counts.items()}
                    }
                })
            
            # Suggested Actions for DateTime
            if invalid_count > 0:
                insights["suggested_actions"].append(f"Found {invalid_count} invalid date formats. Consider careful cleaning.")
            insights["suggested_actions"].append("Extract features like Year, Month, Day, or Hour using Date/Time Handling tool.")

        elif is_numeric:
            # Handle Numeric Columns - Robust Decision System
            n_obs = len(clean_data)
            if n_obs > 0:
                # Step 1: Core Statistics
                q1 = float(clean_data.quantile(0.25))
                q3 = float(clean_data.quantile(0.75))
                median = float(clean_data.median())
                mean_val = float(clean_data.mean())
                std_val = float(clean_data.std()) if n_obs > 1 else 0
                col_min = float(clean_data.min())
                col_max = float(clean_data.max())
                col_range = col_max - col_min
                iqr = q3 - q1

                # ── FIX #1: Zero-variance / near-constant guard ──────────────────
                is_near_constant = std_val == 0 or col_range == 0 or iqr == 0

                # Bounds & Outlier Counts (only meaningful when not near-constant)
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                extreme_lower = q1 - 3 * iqr
                extreme_upper = q3 + 3 * iqr

                outliers_mask = (clean_data < lower_bound) | (clean_data > upper_bound)
                extreme_outliers_mask = (clean_data < extreme_lower) | (clean_data > extreme_upper)

                outlier_count = int(outliers_mask.sum())
                extreme_outlier_count = int(extreme_outliers_mask.sum())
                outlier_ratio = (outlier_count / n_obs) if (n_obs > 0 and not is_near_constant) else 0
                outlier_pct = round(outlier_ratio * 100, 2)

                # Skewness
                raw_skewness = float(clean_data.skew()) if n_obs > 1 else 0
                # Robust/Bowley skewness = (Q3 + Q1 − 2×Median) / IQR  (IQR=0 → 0)
                robust_skewness = (q3 + q1 - 2 * median) / iqr if iqr != 0 else 0
                skewness_gap = abs(abs(raw_skewness) - abs(robust_skewness))

                # Zero-inflated indicator
                zeros_pct = float((clean_data == 0).sum() / n_obs * 100) if n_obs > 0 else 0

                # ── FIX #2: Lowered gap threshold from 1 → 0.7 for better distortion detection ──
                # Skewness Distorted  = outliers are pulling raw_skewness high;
                #                       robust_skewness stays low → safe core distribution
                skewness_distorted = (
                    skewness_gap > 0.7
                    and abs(raw_skewness) > 1
                    and abs(robust_skewness) < 0.5
                )

                # ── FIX #3: Use true_skewness (guard with skewness_gap) for Cases C & D ──
                # true_skewness = robust but skewness_gap is tight
                # (i.e. outliers aren't inflating the raw metric)
                true_skewness = abs(robust_skewness) > 0.7 and skewness_gap < 0.7

                # Skewness Interpretation (Reporting only)
                if abs(raw_skewness) < 0.5:
                    skew_desc = "Symmetric"
                elif 0.5 <= raw_skewness < 1:
                    skew_desc = "Slightly Right-Skewed"
                elif raw_skewness >= 1:
                    skew_desc = "Right-Skewed"
                elif -1 < raw_skewness <= -0.5:
                    skew_desc = "Slightly Left-Skewed"
                else:
                    skew_desc = "Left-Skewed"

                # ── Transform recommendation helper (Box-Cox requires min > 0) ──
                # Used in multiple cases below
                def _transform_advice(include_log=True):
                    if col_min > 0:
                        return "Box-Cox (preferred, all values positive), Yeo-Johnson, or Log" if include_log else "Box-Cox or Yeo-Johnson"
                    elif col_min == 0 and include_log:
                        return "Yeo-Johnson (handles zeros), Log1p"
                    else:
                        return "Yeo-Johnson (handles zeros and negatives)"

                # Histogram computation (once)
                hist_counts, hist_edges = np.histogram(clean_data, bins='auto')

                insights.update({
                    "type": "numeric",
                    "mean": mean_val,
                    "median": median,
                    "std": std_val,
                    "min": col_min,
                    "max": col_max,
                    "iqr": iqr,
                    "zeros_pct": zeros_pct,
                    "raw_skewness": raw_skewness,
                    "robust_skewness": robust_skewness,
                    "skewness_gap": skewness_gap,
                    "skewness_interpretation": skew_desc,
                    "outlier_pct": outlier_pct,
                    "outlier_count": outlier_count,
                    "extreme_outlier_count": extreme_outlier_count,
                    "outlier_ratio": outlier_ratio,
                    "distribution": {
                        "histogram": {
                            "counts": hist_counts.tolist(),
                            "bin_edges": hist_edges.tolist()
                        },
                        "box_plot": {
                            "min": col_min, "q1": q1, "median": median, "q3": q3, "max": col_max
                        }
                    }
                })

                # ── Step 4: Decision Logic  ──────────────────────────────────────
                if n_obs < 30:
                    insights["suggested_actions"].append(
                        "⚠️ Statistical recommendations are unreliable due to small sample size "
                        "(N < 30). Manual review is recommended before applying transformations."
                    )

                # ── FIX #6: Degenerate / near-constant column  ───────────────────
                elif is_near_constant:
                    unique_vals = int(clean_data.nunique())
                    if unique_vals <= 1:
                        insights["suggested_actions"].append(
                            "⚠️ Column is constant (single unique value). "
                            "It carries no information and should be dropped before modelling."
                        )
                    else:
                        insights["suggested_actions"].append(
                            "⚠️ Column has zero or near-zero variance (IQR = 0). "
                            "All values fall within a very tight range. "
                            "Consider dropping or flagging — this column may offer little predictive value."
                        )

                else:
                    has_moderate_outliers = outlier_ratio >= 0.02
                    has_extreme_outliers  = extreme_outlier_count > 0

                    # ── FIX #4 & #5: Reorder — heavy-tail / zero-inflated BEFORE distorted-skew ──
                    # Case A-1: Zero-inflated heavy-tail (>15% outliers AND >30% zeros)
                    if outlier_ratio > 0.15 and zeros_pct > 30:
                        insights["suggested_actions"].append(
                            f"⚠️ Zero-inflated distribution detected ({zeros_pct:.1f}% zeros) "
                            "with a heavy tail. IQR-based outlier flagging is overcounting — "
                            "this is a structural property of the data. "
                            "Consider a two-part/hurdle model, sqrt transform, or domain-specific binning."
                        )

                    # Case A-2: Heavy-tailed (>15% flagged, NOT zero-inflated)
                    elif outlier_ratio > 0.15:
                        insights["suggested_actions"].append(
                            "High proportion of values flagged as outliers (>15%). "
                            "This likely indicates a naturally heavy-tailed distribution, "
                            "not isolated anomalies. Avoid aggressive capping. "
                            f"Consider {_transform_advice()} transformation or domain review."
                        )

                    # Case B: Skewness distorted by extreme outliers
                    elif skewness_distorted:
                        insights["suggested_actions"].append(
                            "Recommend handling extreme outliers first — high raw skewness is "
                            "likely an outlier-driven distortion (core distribution is roughly symmetric)."
                        )

                    # Case C: True extreme outliers, low overall outlier ratio
                    elif has_extreme_outliers and outlier_ratio < 0.05:
                        insights["suggested_actions"].append(
                            "Recommend outlier capping. A small number of extreme anomalies "
                            "are distorting statistics."
                        )
                        # ── FIX #3: use true_skewness (not bare robust check) ──
                        if true_skewness:
                            insights["suggested_actions"].append(
                                f"After capping, recommend {_transform_advice()} transformation "
                                "to address genuine distributional skewness."
                            )

                    # Case D: High robust skewness, low outlier ratio  (natural skew)
                    elif true_skewness and outlier_ratio < 0.02:
                        insights["suggested_actions"].append(
                            f"Recommend {_transform_advice()} transformation. "
                            "Distribution is genuinely skewed with few outliers."
                        )

                    # Case E: High robust skewness AND moderate/high outliers
                    elif true_skewness and has_moderate_outliers:
                        insights["suggested_actions"].append(
                            f"Suggest handling outliers first, then apply {_transform_advice()} "
                            "transformation. Both genuine skewness and outlier contamination are present."
                        )

                    # Case F: Outliers present, but core distribution is symmetric
                    elif outlier_ratio > 0.01 and abs(robust_skewness) < 0.3:
                        insights["suggested_actions"].append(
                            "Optional outlier capping. Core distribution is symmetric; "
                            "outliers appear to be isolated noise."
                        )

                    # Case G: No significant issues
                    else:
                        if outlier_ratio < 0.01 and abs(robust_skewness) < 0.3:
                            if missing_pct == 0:
                                insights["suggested_actions"].append(
                                    "No outlier handling or transformation required. Distribution is stable."
                                )
                        elif true_skewness:
                            insights["suggested_actions"].append(
                                f"Recommend {_transform_advice()} transformation."
                            )
                        elif has_moderate_outliers:
                            insights["suggested_actions"].append(
                                "Recommend handling outliers (capping or review)."
                            )

                # Add missing value recommendations (Common across all numeric)
                if missing_pct > 20:
                    insights["suggested_actions"].append(
                        "High missing values. Consider dropping column or using advanced imputation."
                    )
                elif missing_pct > 0:
                    insights["suggested_actions"].append(
                        "Handle missing values using Median/Mean/Mode imputation."
                    )

        else:
            # Handle Categorical Columns
            value_counts = col_data.value_counts()
            most_frequent = str(value_counts.index[0]) if not value_counts.empty else None
            least_frequent = str(value_counts.index[-1]) if not value_counts.empty else None
            
            # Imbalance ratio
            imbalance_ratio = round(value_counts.iloc[0] / value_counts.iloc[-1], 2) if not value_counts.empty and value_counts.iloc[-1] > 0 else 1
            
            # Rare categories (< 1% frequency)
            rare_count = int((value_counts / total_rows < 0.01).sum())

            insights.update({
                "type": "categorical",
                "most_frequent": most_frequent,
                "least_frequent": least_frequent,
                "imbalance_ratio": imbalance_ratio,
                "rare_category_count": rare_count,
                "distribution": {
                    "bar_chart": {str(k): int(v) for k, v in value_counts.head(15).items()}
                }
            })

            # Suggested Actions
            if unique_count > (total_rows * 0.5) and semantic_type != "identifier":
                insights["suggested_actions"].append("High cardinality detected. This may cause overfitting or high memory usage.")
            
            if imbalance_ratio > 4:
                insights["suggested_actions"].append("Significant class imbalance. Consider SMOTE or oversampling.")
                
            if rare_count > 0:
                insights["suggested_actions"].append(f"Found {rare_count} rare categories. Consider grouping them into 'Other'.")

        return insights

    except Exception as e:
        print(f"Error in get_column_insights: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/datasets/{dataset_id}/semantic-types/override")
async def override_semantic_types(
    dataset_id: str,
    overrides: List[Dict[str, Any]],
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Save user overrides for semantic data types"""
    try:
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        # Create a new dict object to ensure SQLAlchemy detects the change (mutation tracking)
        current_metadata = dict(dataset.column_metadata or {})
        
        for item in overrides:
            col = item.get("column")
            if col:
                current_metadata[col] = {
                    **item,
                    "is_override": True,
                    "updated_at": datetime.now().isoformat()
                }
        
        # Set verification flag
        current_metadata["_is_verified"] = True
        
        # Explicitly assign to trigger SQLAlchemy's setter
        dataset.column_metadata = current_metadata
        db.commit()
        
        return {
            "message": "Semantic types updated successfully",
            "status": "success"
        }
    except Exception as e:
        print(f"Error overriding semantic types: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/datasets/{dataset_id}/reset")
async def reset_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Reset dataset to original state by clearing in-memory transformations and reverting metadata"""
    try:
        # 1. Fetch from DB
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Check ownership
        if dataset.user_id != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized")

        # 2. Clear In-Memory Cache
        if dataset_id in datasets:
            del datasets[dataset_id]
            print(f"🗑️ Cleared in-memory cache for Dataset {dataset_id}")

        # 3. Revert Database Metadata
        dataset.column_metadata = None
        dataset.is_processed = False
        db.commit()

        return {
            "message": "Dataset successfully reset to original state",
            "status": "success"
        }
    except Exception as e:
        print(f"Error resetting dataset: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/preprocess")
async def preprocess(
    config: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Apply preprocessing steps to dataset - Persisted"""
    try:
        dataset_id = config.get("dataset_id")
        steps = config.get("steps", [])

        print(f"Preprocessing request for Dataset {dataset_id}")

        # 1. Fetch Source Dataset
        dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset:
             raise HTTPException(status_code=404, detail="Dataset not found")
        
        if dataset.user_id != current_user['id']:
             raise HTTPException(status_code=403, detail="Not authorized")

        # 2. Load Dataframe
        df = file_service.load_dataframe(dataset.storage_path)
        original_rows = len(df)
        
        # 3. Apply Preprocessing
        # 3. Process
        # ✅ Load semantic metadata if available
        column_metadata = dataset.column_metadata or {}
        preprocessor = DataPreprocessor(df, column_metadata=column_metadata)
        
        categorical_encoded = False
        encoded_columns = []
        
        # ✅ Identify target column to exclude it from bulk processing
        target_column = None
        if dataset_id in datasets and 'target_column' in datasets[dataset_id]:
             target_column = datasets[dataset_id]['target_column']
        elif 'target_column' in config:
             target_column = config['target_column']
             # Handle JSON target
             if isinstance(target_column, str) and target_column.startswith('{'):
                 try:
                     import json
                     target_json = json.loads(target_column)
                     target_column = target_json.get('name')
                 except: pass

        for i, step in enumerate(steps, 1):
            step_type = step.get("type")
            print(f"  Step {i}: {step_type}")

            if step_type == "handle_missing":
                strategies = step.get("strategies", {})
                if strategies:
                    preprocessor.handle_missing_values(strategies)

            elif step_type == 'remove_columns':  
                columns_to_remove = step.get('columns', [])
                if columns_to_remove:
                    existing_cols = [col for col in columns_to_remove if col in preprocessor.df.columns]
                    if existing_cols:
                        preprocessor.df = preprocessor.df.drop(columns=existing_cols)

            elif step_type == "remove_duplicates":
                keep = step.get("keep", "first")
                preprocessor.remove_duplicates(strategy=keep)

            elif step_type == "handle_outliers":
                method = step.get("method", "remove")
                numeric_cols = preprocessor.df.select_dtypes(include=np.number).columns.tolist()
                
                # ✅ CRITICAL: Exclude target column from outlier handling
                if target_column and target_column in numeric_cols:
                    print(f"  Skipping outlier handling for target column: {target_column}")
                    numeric_cols.remove(target_column)
                    
                if numeric_cols:
                    preprocessor.handle_outliers(numeric_cols, method="iqr", strategy=method)

            elif step_type == "encode_categorical":
                columns_to_encode = step.get("columns", [])
                methods = step.get("methods", {})
                if columns_to_encode:
                    for col in columns_to_encode:
                        if col in preprocessor.df.columns:
                            method = methods.get(col, "label")
                            preprocessor.encode_categorical(col, method=method)
                            categorical_encoded = True
                            encoded_columns.append(col)

        # 4. Update in-memory storage (Managed Versioning)
        processed_df = preprocessor.get_processed_dataframe()
        processed_rows = len(processed_df)
        
        # Update core global storage
        datasets[dataset_id]['dataframe'] = processed_df
        datasets[dataset_id]['is_processed'] = True
        
        # 5. Log Action (Ephemeral)
        log_user_action(db, current_user['id'], "cleaning_draft", {
            "dataset_id": dataset_id,
            "original_rows": original_rows,
            "processed_rows": processed_rows
        })

        # 6. Prepare Preview
        sample_size = min(200, len(processed_df))
        sample_df = processed_df.head(sample_size)
        preview_data = []
        for idx, row in sample_df.iterrows():
            row_dict = {}
            for col in processed_df.columns:
                value = row[col]
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    if np.isnan(value) or np.isinf(value):
                        row_dict[str(col)] = None
                    else:
                        row_dict[str(col)] = float(value)
                elif isinstance(value, (np.bool_, bool)):
                    row_dict[str(col)] = bool(value)
                else:
                    row_dict[str(col)] = str(value)
            preview_data.append(row_dict)

        return {
            "success": True,
            "preview": preview_data,
            "original_rows": original_rows,
            "total_rows": processed_rows,
            "rows_removed": original_rows - processed_rows,
            "categorical_encoded": categorical_encoded,
            "encoded_columns": encoded_columns,
            "cleaned_dataset_id": dataset_id
        }

    except Exception as e:
        print(f"Preprocessing Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export-cleaned/{dataset_id}")
async def export_cleaned_dataset(dataset_id: str):
    """Export cleaned/preprocessed dataset as CSV"""
    try:
        print("\n" + "=" * 80)
        print(f"📥 EXPORT CLEANED: {dataset_id}")
        print("=" * 80)
        
        if dataset_id not in datasets:
            print(f"❌ Dataset {dataset_id} not found!")
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        df = datasets[dataset_id]["dataframe"].copy()
        
        print(f"✅ Exporting cleaned dataset: {len(df)} rows, {len(df.columns)} columns")
        
        # ✅ Generate filename
        filename = datasets[dataset_id].get("filename", "dataset.csv")
        filename = filename.replace(".csv", "") + "_cleaned_exported.csv"
        
        print(f"📄 Filename: {filename}")
        
        # ✅ CORRECT: Use StringIO to generate CSV
        def iter_csv():
            """Stream CSV line by line"""
            buffer = io.StringIO()
            
            # Write header
            df.to_csv(buffer, index=False, mode='w', header=True)
            yield buffer.getvalue()
            
            # Write data in chunks (1000 rows at a time)
            chunk_size = 1000
            for i in range(0, len(df), chunk_size):
                buffer = io.StringIO()
                df.iloc[i:i+chunk_size].to_csv(buffer, index=False, header=False)
                yield buffer.getvalue()
        
        print(f"✅ Streaming {len(df)} rows in chunks...")
        print("=" * 80)
        
        return StreamingResponse(
            iter_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Export error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    
    



@app.get("/api/get-engineering-preview/{dataset_id}")
async def get_engineering_preview(dataset_id: str):
    """Get preview of scaled/engineered data"""
    try:
        if dataset_id not in datasets:
            raise HTTPException(status_code=404)
        
        df = datasets[dataset_id]["dataframe"]
        split_info = datasets[dataset_id].get("split_info", {})
        
        # Show first 5 rows of each
        train_sample = df.iloc[:5].to_dict('records')
        
        return {
            "success": True,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "train_rows": len(split_info.get("train_indices", [])),
            "test_rows": len(split_info.get("test_indices", [])),
            "sample_data": train_sample,
            "scaling_method": datasets[dataset_id].get("scaling_method", "None"),
            "pca_applied": "pca" in datasets[dataset_id]
        }
    
    except Exception as e:
        raise HTTPException(500, str(e))


# ===== SMOTE (CLASS IMBALANCE HANDLING) =====

@app.get("/api/datasets/{dataset_id}/check-imbalance")
async def check_imbalance(
    dataset_id: str,
    target_column: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Check if the training set has class imbalance.
    Returns imbalance ratio and recommendation for SMOTE.
    Respects manual semantic type overrides.
    """
    global y_train_storage
    
    try:
        print(f"\n{'='*80}")
        print(f"🔍 CHECKING CLASS IMBALANCE: Dataset {dataset_id}, Target: {target_column}")
        print(f"{'='*80}")
        
        # 1. Fetch Dataset and Overrides from DB
        dataset_record = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset_record:
            raise HTTPException(status_code=404, detail="Dataset not found in database")
            
        column_metadata = dataset_record.column_metadata or {}
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found in memory")
        
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset must be split first")
        
        # Determine problem type from effective semantic types
        df_full = datasets[dataset_id]['dataframe']
        # Use simple check for target column
        target_meta = column_metadata.get(target_column, {})
        if target_meta.get("is_override"):
            target_type = target_meta.get("semantic_type")
        else:
            target_type = detect_semantic_type(df_full[target_column]).get("semantic_type", "unknown")

        is_classification = target_type in ['categorical', 'boolean', 'identifier', 'text']
        # Also check raw type if unknown
        if target_type == 'unknown' or target_type == 'numeric':
             # If numeric but unique values are low, it might be classified as categorical by some logic,
             # but here we follow the dataset record if available.
             is_classification = datasets[dataset_id].get('problem_type') == 'classification'

        if not is_classification:
             return {
                "success": True,
                "has_imbalance": False,
                "imbalance_ratio": 1.0,
                "severity": "balanced",
                "recommendation": "SMOTE is not applicable for regression tasks (numeric targets).",
                "message": "Regression problem detected. Skipping class imbalance check."
            }
        
        # Get training target data
        if dataset_id not in y_train_storage:
            raise HTTPException(status_code=400, detail="Training data not found")
        
        y_train = y_train_storage[dataset_id]
        
        # Calculate class distribution
        class_counts = y_train.value_counts().to_dict()
        total_samples = len(y_train)
        
        # Calculate imbalance ratio (max / min)
        max_count = max(class_counts.values())
        min_count = min(class_counts.values())
        imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
        
        # Determine if imbalance exists with updated thresholds
        # IR < 1.5: Balanced (SMOTE disabled)
        # 1.5 ≤ IR < 3.0: Mild imbalance (SMOTE optional)
        # IR ≥ 3.0: Severe imbalance (SMOTE strongly recommended)
        threshold = 1.5
        has_imbalance = imbalance_ratio >= threshold
        
        # Generate recommendation
        if imbalance_ratio < 1.5:
            recommendation = "Balanced dataset - SMOTE not recommended"
            severity = "balanced"
        elif imbalance_ratio < 3.0:
            recommendation = "Mild imbalance detected - SMOTE optional but may improve model performance"
            severity = "mild"
        else:
            recommendation = "Severe imbalance detected - SMOTE strongly recommended"
            severity = "severe"
        
        # Calculate percentages
        class_distribution = {
            str(k): {
                "count": int(v),
                "percentage": round((v / total_samples) * 100, 2)
            }
            for k, v in class_counts.items()
        }
        
        print(f"✅ Class Distribution:")
        for cls, info in class_distribution.items():
            print(f"   {cls}: {info['count']} ({info['percentage']}%)")
        print(f"📊 Imbalance Ratio: {imbalance_ratio:.2f}")
        print(f"🎯 Recommendation: {recommendation}")
        print(f"{'='*80}\n")
        
        return {
            "success": True,
            "has_imbalance": has_imbalance,
            "imbalance_ratio": round(imbalance_ratio, 2),
            "threshold": threshold,
            "severity": severity,
            "recommendation": recommendation,
            "class_distribution": class_distribution,
            "total_samples": total_samples,
            "num_classes": len(class_counts)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error checking imbalance: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/datasets/{dataset_id}/apply-smote")
async def apply_smote(
    dataset_id: str,
    config: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Apply SMOTE to balance class distribution in training data.
    Respects manual semantic type overrides.
    """
    global X_train_storage, y_train_storage, datasets
    
    try:
        print(f"\n{'='*80}")
        print(f"⚖️ APPLYING SMOTE: Dataset {dataset_id}")
        print(f"{'='*80}")
        
        # 1. Fetch Dataset and Overrides from DB
        dataset_record = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if not dataset_record:
            raise HTTPException(status_code=404, detail="Dataset not found in database")
            
        column_metadata = dataset_record.column_metadata or {}
        
        # Check if SMOTE is available
        if not SMOTE_AVAILABLE:
            raise HTTPException(
                status_code=500, 
                detail="SMOTE not available. Please install imbalanced-learn: pip install imbalanced-learn"
            )
        
        # Validate dataset exists and is split
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset must be split first")
        
        if dataset_id not in X_train_storage or dataset_id not in y_train_storage:
            raise HTTPException(status_code=400, detail="Training data not found")
        
        # Check problem type (SMOTE is for classification only)
        if datasets[dataset_id].get('problem_type') != 'classification':
            raise HTTPException(
                status_code=400,
                detail="SMOTE can only be applied to classification problems with categorical or discrete targets. Regression tasks are not supported."
            )
        
        # Get configuration
        sampling_strategy = config.get('sampling_strategy', 'auto')
        k_neighbors = config.get('k_neighbors', 5)
        random_state = config.get('random_state', None)
        
        print(f"📋 Configuration:")
        print(f"   Sampling Strategy: {sampling_strategy}")
        print(f"   K-Neighbors: {k_neighbors}")
        print(f"   Random State: {random_state}")
        
        # Get training data
        X_train = X_train_storage[dataset_id]
        y_train = y_train_storage[dataset_id]
        
        # Check for non-numeric columns (SMOTE requirement)
        # 1. Get effective types to respect overrides
        effective_types = get_effective_semantic_types(X_train, column_metadata)
        
        # 2. Identify non-numeric columns based on effective type or raw dtype
        # We consider 'numeric', 'numerical' and 'boolean' as valid for SMOTE
        non_numeric_cols = []
        for col in X_train.columns:
            eff_type = (effective_types.get(col) or "").lower()
            # If overridden to something other than numeric/boolean, it's non-numeric
            if eff_type and eff_type not in ['numeric', 'numerical', 'boolean', 'integer', 'float']:
                non_numeric_cols.append(col)
            # If not overridden, fall back to pandas dtype
            elif not eff_type and not pd.api.types.is_numeric_dtype(X_train[col]):
                non_numeric_cols.append(col)
        
        if non_numeric_cols:
            raise HTTPException(
                status_code=400,
                detail=f"SMOTE requires all features to be numerical. Found non-numeric columns based on semantic types: {', '.join(non_numeric_cols)}. Please encode them first."
            )
        
        # Store original distribution
        original_distribution = y_train.value_counts().to_dict()
        original_total = len(y_train)
        
        print(f"\n📊 Original Distribution:")
        for cls, count in original_distribution.items():
            print(f"   {cls}: {count} ({(count/original_total)*100:.2f}%)")
        
        # Apply SMOTE
        try:
            smote = SMOTE(
                sampling_strategy=sampling_strategy,
                k_neighbors=k_neighbors,
                random_state=random_state if random_state is not None else 42
            )
            
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
            
            # Convert back to DataFrame/Series with proper column names
            X_train_resampled = pd.DataFrame(X_train_resampled, columns=X_train.columns)
            y_train_resampled = pd.Series(y_train_resampled, name=y_train.name)
            
        except ValueError as e:
            # Handle cases where SMOTE cannot be applied (e.g., too few samples)
            raise HTTPException(
                status_code=400,
                detail=f"SMOTE cannot be applied: {str(e)}. Ensure you have enough samples per class (at least k_neighbors + 1)."
            )
        
        # Calculate new distribution
        new_distribution = y_train_resampled.value_counts().to_dict()
        new_total = len(y_train_resampled)
        samples_added = new_total - original_total
        
        print(f"\n📊 New Distribution (After SMOTE):")
        for cls, count in new_distribution.items():
            print(f"   {cls}: {count} ({(count/new_total)*100:.2f}%)")
        print(f"\n✅ Samples Added: {samples_added}")
        print(f"✅ New Total: {new_total}")
        
        # Update storage with resampled data
        X_train_storage[dataset_id] = X_train_resampled
        y_train_storage[dataset_id] = y_train_resampled
        
        # ── SYNC BASE DATAFRAME ──────────────────────────────────────────────
        # Reconstruct the full dataset so Data Preview sees the SMOTE distribution
        try:
            X_test_sync = X_test_storage.get(dataset_id)
            y_test_sync = y_test_storage.get(dataset_id)
            
            if X_test_sync is not None and y_test_sync is not None:
                full_X = pd.concat([X_train_resampled, X_test_sync], axis=0).reset_index(drop=True)
                full_y = pd.concat([y_train_resampled, y_test_sync], axis=0).reset_index(drop=True)
                full_df = pd.concat([full_X, full_y], axis=1)
            else:
                full_df = pd.concat([X_train_resampled, y_train_resampled], axis=1)
                
            datasets[dataset_id]['dataframe'] = full_df
            print(f"✅ Base dataframe synced after SMOTE. Shape: {full_df.shape}")
        except Exception as sync_err:
            print(f"⚠️  Could not sync base dataframe after SMOTE: {sync_err}")
        # ─────────────────────────────────────────────────────────────────────
        
        # Mark SMOTE as applied in dataset metadata
        datasets[dataset_id]['smote_applied'] = True
        datasets[dataset_id]['smote_config'] = config
        
        # Prepare response
        class_distribution_before = {
            str(k): {
                "count": int(v),
                "percentage": round((v / original_total) * 100, 2)
            }
            for k, v in original_distribution.items()
        }
        
        class_distribution_after = {
            str(k): {
                "count": int(v),
                "percentage": round((v / new_total) * 100, 2)
            }
            for k, v in new_distribution.items()
        }
        
        print(f"{'='*80}\n")
        
        # Prepare preview (limit to 100 rows for performance)
        preview_df = X_train_resampled.copy()
        preview_df[y_train_resampled.name] = y_train_resampled
        train_preview = preview_df.head(100).replace({np.nan: None}).to_dict(orient='records')

        return {
            "success": True,
            "message": "SMOTE applied successfully",
            "original_samples": original_total,
            "new_samples": new_total,
            "samples_added": samples_added,
            "class_distribution_before": class_distribution_before,
            "class_distribution_after": class_distribution_after,
            "train_preview": train_preview,
            "config": {
                "sampling_strategy": sampling_strategy,
                "k_neighbors": k_neighbors,
                "random_state": random_state
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error applying SMOTE: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/datasets/{dataset_id}/reset-smote")
async def reset_smote(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Reset SMOTE transformation and restore original training data
    """
    global datasets
    
    try:
        print(f"\n{'='*80}")
        print(f"🔄 RESETTING SMOTE: Dataset {dataset_id}")
        print(f"{'='*80}")
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        if not datasets[dataset_id].get('smote_applied', False):
            return {
                "success": True,
                "message": "SMOTE was not applied, nothing to reset"
            }
        
        # Note: To properly reset, we would need to store the original training data
        # For now, we'll require re-splitting the dataset
        datasets[dataset_id]['smote_applied'] = False
        datasets[dataset_id].pop('smote_config', None)
        
        print(f"✅ SMOTE reset. Please re-split the dataset to restore original data.")
        print(f"{'='*80}\n")
        
        return {
            "success": True,
            "message": "SMOTE reset. Please re-split the dataset to restore original training data.",
            "requires_resplit": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error resetting SMOTE: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ===== TARGET VARIABLE SELECTION =====
@app.post("/api/set-target")
async def set_target(
    request: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Set target variable and detect problem type
    """
    try:
        dataset_id = request.get('dataset_id')
        target_column = request.get('target_column')
        
        print(f"🎯 Setting target for dataset {dataset_id}: {target_column}")
        
        # Check if dataset exists in memory
        if dataset_id not in datasets:
            print(f"⚠️ Dataset {dataset_id} not in memory, attempting restoration...")
            
            # Try to restore from DB
            dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
            
            if not dataset:
                print(f"❌ Dataset {dataset_id} not found in DB")
                raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
                
            # Check ownership
            if dataset.user_id != current_user['id']:
                raise HTTPException(status_code=403, detail="Not authorized")
                
            # Restore to memory
            try:
                df = file_service.load_dataframe(dataset.storage_path)
                datasets[dataset_id] = {
                    'dataframe': df,
                    'filename': dataset.name,
                    'upload_time': dataset.upload_date,
                    'is_processed': dataset.is_processed
                }
                print(f"✅ Dataset {dataset_id} restored to memory")
            except Exception as e:
                print(f"❌ Failed to restore dataset: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to restore dataset: {str(e)}")

        # Proceed with target setting
        if dataset_id not in datasets:
             raise HTTPException(status_code=404, detail="Dataset not found even after restoration attempt")
             
        df = datasets[dataset_id]['dataframe']
        
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{target_column}' not found in dataset")
        
        # Detect problem type
        unique_values = df[target_column].nunique()
        problem_type = "classification" if unique_values < 20 else "regression"
        
        # If numerical but few unique values, check if they're continuous
        if pd.api.types.is_numeric_dtype(df[target_column]):
            if unique_values > 20:
                problem_type = "regression"
            else:
                # Check if values are integers (likely classification)
                if df[target_column].dtype in ['int64', 'int32']:
                    problem_type = "classification"
                else:
                    problem_type = "regression"
        
        # Store target info in dataset
        datasets[dataset_id]['target_column'] = target_column
        datasets[dataset_id]['problem_type'] = problem_type
        
        # Get feature information
        feature_columns = [col for col in df.columns if col != target_column]
        categorical_features = df[feature_columns].select_dtypes(include=['object', 'category']).columns.tolist()
        numerical_features = df[feature_columns].select_dtypes(include=np.number).columns.tolist()
        
        print(f"✅ Target set: {target_column} | Type: {problem_type}")
        
        return {
            'success': True,
            'target_column': target_column,
            'problem_type': problem_type,
            'target_unique_values': int(unique_values),
            'total_features': len(feature_columns),
            'categorical_features': categorical_features,
            'numerical_features': numerical_features
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error setting target: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
# ===== NEW: SPLIT & SCALING ENDPOINTS =====

@app.post("/api/split-dataset")
async def split_dataset(
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Split dataset into train/test sets"""
    global X_train_storage, X_test_storage, y_train_storage, y_test_storage
    
    try:
        dataset_id = request.get('datasetid')
        test_size = request.get('test_size', 0.2)
        stratify_enabled = request.get('stratify', True)
        random_state = request.get('random_state', 42)
        
        print(f"Split request for dataset: {dataset_id}")
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Get the target column from dataset metadata OR request
        dataset_info = datasets[dataset_id]
        
        # Allow passing target_column in request if not set in metadata
        if 'target_column' in request:
            dataset_info['target_column'] = request['target_column']
            
        if 'target_column' not in dataset_info:
            raise HTTPException(status_code=400, detail="No target selected. Please select target first.")
        
        target_column = dataset_info['target_column']
        df = dataset_info['dataframe'].copy()
        
        print(f"Target column: {target_column}")
        print(f"Dataset shape: {df.shape}")
        
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{target_column}' not found")
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Determine if stratification is possible
        stratify_param = None
        if stratify_enabled:
            # Check if target is categorical/classification
            if y.dtype == 'object' or y.nunique() < 20:
                try:
                    stratify_param = y
                except:
                    print("Stratification failed, proceeding without stratification")
                    stratify_param = None
        
        # Perform split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size,
            random_state=random_state,
            stratify=stratify_param
        )
        
        # Store split data
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        y_train_storage[dataset_id] = y_train
        y_test_storage[dataset_id] = y_test
        
        # Update dataset metadata
        datasets[dataset_id]['is_split'] = True
        datasets[dataset_id]['split_info'] = {
            'train_size': len(X_train),
            'test_size': len(X_test),
            'test_size_ratio': test_size,
            'stratified': stratify_param is not None
        }
        
        # Get numerical columns for scaling
        numerical_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        
        train_preview_df = pd.concat([X_train.head(200), y_train.head(200)], axis=1)
        test_preview_df = pd.concat([X_test.head(200), y_test.head(200)], axis=1)
        
        # Sanitize NaN/Inf before serializing to JSON
        def sanitize_preview(df):
            return df.replace({float('inf'): None, float('-inf'): None}).where(df.notna(), None).to_dict('records')

        train_preview = sanitize_preview(train_preview_df)
        test_preview  = sanitize_preview(test_preview_df)
        
        # ── PERSISTENCE FIX ──────────────────────────────────────────────────
        # Save previews to the DB so they survive backend restarts.
        # We embed them inside column_metadata (already a JSON column) using a
        # private key "_split_previews" that the GET endpoint can read back.
        try:
            db_dataset = db.query(DatasetModel).filter(
                DatasetModel.id == int(dataset_id)
            ).first()
            if db_dataset:
                existing_meta = db_dataset.column_metadata or {}
                existing_meta["_split_previews"] = {
                    "train": train_preview,
                    "test": test_preview,
                    "train_size": len(X_train),
                    "test_size": len(X_test),
                }
                db_dataset.column_metadata = existing_meta
                flag_modified(db_dataset, "column_metadata")  # Required for PostgreSQL JSON tracking
                db.commit()
                print(f"✅ Split previews persisted to DB for dataset {dataset_id}")
        except Exception as persist_err:
            print(f"⚠️ Could not persist split previews to DB: {persist_err}")
        # ─────────────────────────────────────────────────────────────────────

        print(f"Split complete: {len(X_train)} train, {len(X_test)} test")
        print(f"Numerical columns: {numerical_cols}")
        
        return {
            "status": "success",
            "message": "Dataset split successfully",
            "train_size": len(X_train),
            "test_size": len(X_test),
            "train_preview": train_preview,
            "test_preview": test_preview,
            "numerical_columns": numerical_cols,
            "stratified": stratify_param is not None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Split error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))





@app.delete("/api/datasets/{dataset_id}/split")
async def reset_split(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Clear split state and cached previews so the dataset returns to its full/unsplit form."""
    global X_train_storage, X_test_storage, y_train_storage, y_test_storage, datasets

    try:
        # 1. Verify dataset ownership
        db_dataset = db.query(DatasetModel).filter(
            DatasetModel.id == int(dataset_id)
        ).first()
        if not db_dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        if db_dataset.user_id != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized")

        # 2. Remove in-memory split globals
        for store in [X_train_storage, X_test_storage, y_train_storage, y_test_storage]:
            store.pop(dataset_id, None)

        # 3. Clear in-memory split flags
        if dataset_id in datasets:
            datasets[dataset_id]['is_split'] = False
            datasets[dataset_id].pop('split_info', None)
            datasets[dataset_id].pop('smote_applied', None)
            datasets[dataset_id].pop('smote_config', None)

        # 4. Clear cached previews from DB
        existing_meta = db_dataset.column_metadata or {}
        existing_meta.pop("_split_previews", None)
        db_dataset.column_metadata = existing_meta
        flag_modified(db_dataset, "column_metadata")  # Required for PostgreSQL JSON tracking
        db.commit()

        print(f"✅ Split reset for dataset {dataset_id}")
        return {"success": True, "message": "Split reset successfully"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error resetting split: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import numpy as np

# Pydantic model for request
class ColumnEncoding(BaseModel):
    name: str
    method: str  # 'onehot', 'label', 'ordinal'

class CategoricalEncodingRequest(BaseModel):
    dataset_id: str
    columns: List[ColumnEncoding]

class TargetEncodingColumn(BaseModel):
    name: str
    smoothing: Optional[int] = 10

class TargetEncodingRequest(BaseModel):
    dataset_id: str
    columns: List[TargetEncodingColumn]

# Storage for encoders (similar to split_scalers)
categorical_encoders = {}
target_encoders = {}

@app.post("/api/apply-target-encoding")
async def apply_target_encoding(
    request: TargetEncodingRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Apply smoothed target encoding to specified categorical columns.
    Must be called AFTER dataset is split.
    """
    global X_train_storage, X_test_storage, y_train_storage, y_test_storage, target_encoders
    
    try:
        dataset_id = request.dataset_id
        columns_to_encode = request.columns
        
        print("\n" + "=" * 80)
        print(f"📊 TARGET ENCODING REQUEST: Dataset {dataset_id}")
        print(f"   Columns: {[c.name for c in columns_to_encode]}")
        print("=" * 80)
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset must be split before target encoding")
        
        X_train = X_train_storage[dataset_id].copy()
        X_test = X_test_storage[dataset_id].copy()
        y_train = y_train_storage[dataset_id]
        
        # Detect problem type if not already known
        problem_type = datasets[dataset_id].get('problem_type', 'regression')
        
        encoders_used = {}
        new_encoded_cols = []
        
        for col_info in columns_to_encode:
            col_name = col_info.name
            smoothing = col_info.smoothing if col_info.smoothing is not None else 10
            
            if col_name not in X_train.columns:
                print(f"⚠️ Column {col_name} not found, skipping...")
                continue
                
            print(f"Encoding {col_name} (smoothing={smoothing})...")
            
            encoder = TargetEncoder(smoothing=smoothing)
            encoder.fit(X_train, y_train, col_name, problem_type=problem_type)
            
            X_train, cols_added = encoder.transform(X_train, col_name)
            X_test, _ = encoder.transform(X_test, col_name)
            
            encoders_used[col_name] = encoder
            new_encoded_cols.extend(cols_added)
            
            # Update Registry
            if dataset_id not in feature_metadata: feature_metadata[dataset_id] = {}
            for ec in cols_added:
                feature_metadata[dataset_id][ec] = {
                    'original_column': col_name,
                    'type': 'target_encoded',
                    'transformation': 'smoothing_target_mean',
                    'smoothing': smoothing
                }
            
        # Update storage
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        target_encoders[dataset_id] = encoders_used
        
        # ── SYNC BASE DATAFRAME ──────────────────────────────────────────────
        try:
            full_X = pd.concat([X_train, X_test], axis=0).reset_index(drop=True)
            y_train_sync = y_train_storage.get(dataset_id)
            y_test_sync = y_test_storage.get(dataset_id)
            
            if y_train_sync is not None and y_test_sync is not None:
                full_y = pd.concat([y_train_sync, y_test_sync], axis=0).reset_index(drop=True)
                full_df = pd.concat([full_X, full_y], axis=1)
            else:
                full_df = full_X
                
            datasets[dataset_id]['dataframe'] = full_df
            print(f"✅ Base dataframe synced after target encoding. Shape: {full_df.shape}")
        except Exception as sync_err:
            print(f"⚠️  Could not sync base dataframe after target encoding: {sync_err}")
        # ─────────────────────────────────────────────────────────────────────
        
        # Update metadata
        datasets[dataset_id]['target_encoded'] = True
        datasets[dataset_id]['target_encoded_columns'] = list(encoders_used.keys())
        
        # Update Database Metadata to reflect new numeric status
        dataset_record = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if dataset_record:
            meta = dict(dataset_record.column_metadata or {})

            # 🔧 FIX: Mark BOTH the original column names AND the new encoded column names as numeric.
            # The original column may still be in the DB with semantic_type='categorical' (possibly with
            # is_override=True), which causes get_effective_semantic_types() to return 'categorical',
            # blocking SMOTE validation even after encoding has replaced the data with numeric values.
            encoded_original_names = [col_info.name for col_info in columns_to_encode]
            for original_col in encoded_original_names:
                meta[original_col] = {
                    "column": original_col,
                    "semantic_type": "numeric",
                    "is_override": True,  # Force this to take priority in get_effective_semantic_types
                    "reason": "Column was target encoded — values are now numeric means"
                }

            # Also update the new encoded column names (could differ from original for multiclass)
            for ec in new_encoded_cols:
                meta[ec] = {
                    "column": ec,
                    "semantic_type": "numeric",
                    "is_override": True,
                    "reason": "Target encoded (smoothed mean)"
                }

            dataset_record.column_metadata = meta
            db.commit()
            print(f"✅ Updated DB metadata: {len(encoded_original_names)} original + {len(new_encoded_cols)} new encoded columns → numeric")
        
        # Preview data
        y_test = y_test_storage[dataset_id]
        train_preview = pd.concat([X_train.head(200), y_train.head(200)], axis=1).to_dict('records')
        test_preview = pd.concat([X_test.head(200), y_test.head(200)], axis=1).to_dict('records')
        
        print(f"✅ Target encoding complete. Added {len(new_encoded_cols)} columns.")
        print("=" * 80 + "\n")
        
        target_col_name = y_train.name if hasattr(y_train, 'name') else 'target'
        all_columns = list(X_train.columns) + [target_col_name]
        
        return {
            "success": True,
            "message": f"Successfully applied target encoding to {len(encoders_used)} original columns",
            "train_preview": train_preview,
            "test_preview": test_preview,
            "columns": all_columns,
            "encoded_columns": new_encoded_cols
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Target encoding error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apply-categorical-encoding")
async def apply_categorical_encoding(
    request: CategoricalEncodingRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Apply categorical encoding to specified columns in train and test splits.
    Must be called AFTER dataset is split.
    """
    global X_train_storage, X_test_storage, y_train_storage, y_test_storage, categorical_encoders
    
    try:
        dataset_id = request.dataset_id
        columns_to_encode = request.columns
        
        print("\n" + "=" * 80)
        print(f"📊 CATEGORICAL ENCODING REQUEST")
        print(f"   Dataset ID: {dataset_id}")
        print(f"   Columns to encode: {len(columns_to_encode)}")
        print("=" * 80)
        
        # Validate dataset exists and is split
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        if not datasets[dataset_id].get('is_split', False):
            raise HTTPException(status_code=400, detail="Dataset must be split before encoding")
        
        if dataset_id not in X_train_storage or dataset_id not in X_test_storage:
            raise HTTPException(status_code=400, detail="Split data not found")
        
        X_train = X_train_storage[dataset_id].copy()
        X_test = X_test_storage[dataset_id].copy()
        y_train = y_train_storage[dataset_id]
        y_test = y_test_storage[dataset_id]
        
        encoders_used = {}
        encoded_columns = []
        onehot_columns = []  # Added to track only OH dummies
        
        for col_info in columns_to_encode:
            col_name = col_info.name
            method = col_info.method.lower()
            
            if col_name not in X_train.columns:
                print(f"⚠️  Column {col_name} not found, skipping...")
                continue
            
            print(f"Encoding {col_name} using {method}...")
            
            if method == 'label':
                # Label Encoding: Fit on train, transform both
                encoder = LabelEncoder()
                X_train[col_name] = encoder.fit_transform(X_train[col_name].astype(str))
                
                # Handle unseen categories in test set
                test_values = X_test[col_name].astype(str)
                # Map unseen categories to -1
                test_encoded = test_values.map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)
                X_test[col_name] = test_encoded
                
                encoders_used[col_name] = {'type': 'label', 'encoder': encoder}
                encoded_columns.append(col_name)
                
            elif method == 'onehot':
                # One-Hot Encoding: Creates new columns
                # Using drop='first' to avoid dummy variable trap (multicollinearity)
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first')
                
                # Fit on train
                train_encoded = encoder.fit_transform(X_train[[col_name]])
                test_encoded = encoder.transform(X_test[[col_name]])
                
                # Get feature names from encoder (this handles drop='first' correctly)
                feature_names = encoder.get_feature_names_out([col_name]).tolist()
                
                # Create DataFrames for encoded columns
                train_encoded_df = pd.DataFrame(train_encoded, columns=feature_names, index=X_train.index)
                test_encoded_df = pd.DataFrame(test_encoded, columns=feature_names, index=X_test.index)
                
                # Drop original column and concat encoded columns
                X_train = X_train.drop(columns=[col_name])
                X_test = X_test.drop(columns=[col_name])
                X_train = pd.concat([X_train, train_encoded_df], axis=1)
                X_test = pd.concat([X_test, test_encoded_df], axis=1)
                
                encoders_used[col_name] = {'type': 'onehot', 'encoder': encoder, 'feature_names': feature_names}
                encoded_columns.extend(feature_names)
                onehot_columns.extend(feature_names) # Track as OH dummies
                
                # Update Registry
                if dataset_id not in feature_metadata: feature_metadata[dataset_id] = {}
                for fn in feature_names:
                    feature_metadata[dataset_id][fn] = {
                        'original_column': col_name,
                        'type': 'categorical',
                        'transformation': 'one-hot',
                        'parent_count': len(feature_names)
                    }
            elif method == 'ordinal':
                # Ordinal Encoding: Preserves order
                encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
                X_train[col_name] = encoder.fit_transform(X_train[[col_name]]).ravel()
                X_test[col_name] = encoder.transform(X_test[[col_name]]).ravel()
                encoders_used[col_name] = {'type': 'ordinal', 'encoder': encoder}
                encoded_columns.append(col_name)
                
                # Update Registry
                if dataset_id not in feature_metadata: feature_metadata[dataset_id] = {}
                feature_metadata[dataset_id][col_name] = {
                    'original_column': col_name,
                    'type': 'categorical',
                    'transformation': 'ordinal'
                }
            
            else:
                print(f"⚠️  Unknown encoding method: {method}")
        
        # Update storage
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        categorical_encoders[dataset_id] = encoders_used
        
        # ── SYNC BASE DATAFRAME ──────────────────────────────────────────────
        # Reconstruct the full dataset from train + test so that
        # GET /api/datasets/{id} (used by data-preview page) always reflects
        # the latest encoded state. Without this, data-preview shows stale
        # pre-encoding data because it reads from datasets[id]['dataframe'].
        try:
            full_X = pd.concat([X_train, X_test], axis=0).reset_index(drop=True)
            full_y = pd.concat([y_train_storage[dataset_id], y_test_storage[dataset_id]], axis=0).reset_index(drop=True)
            full_df = pd.concat([full_X, full_y], axis=1)
            datasets[dataset_id]['dataframe'] = full_df
            print(f"✅ Base dataframe synced after encoding. Shape: {full_df.shape}")
        except Exception as sync_err:
            print(f"⚠️  Could not sync base dataframe after encoding: {sync_err}")
        # ─────────────────────────────────────────────────────────────────────

        # Update dataset metadata
        datasets[dataset_id]['is_encoded'] = True
        datasets[dataset_id]['encoded_columns'] = encoded_columns
        datasets[dataset_id]['encoders'] = list(encoders_used.keys())
        
        # Ensure in-memory metadata is updated for immediate visibility (e.g., in /statistics)
        if 'column_metadata' not in datasets[dataset_id]:
            datasets[dataset_id]['column_metadata'] = {}
            
        for ec in encoded_columns:
            datasets[dataset_id]['column_metadata'][ec] = {
                "column": ec,
                "semantic_type": "numeric",
                "is_override": True,
                "reason": "Categorically encoded",
                "updated_at": datetime.now().isoformat()
            }
        
        # Update Database Metadata
        dataset_record = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
        if dataset_record:
            meta = dataset_record.column_metadata or {}
            for ec in encoded_columns:
                meta[ec] = datasets[dataset_id]['column_metadata'][ec]
            
            # Use flag_modified to ensure SQLAlchemy tracks the JSON change
            dataset_record.column_metadata = meta
            flag_modified(dataset_record, "column_metadata")
            db.commit()
            print(f"✅ Updated DB metadata for {len(encoded_columns)} columns and flagged as modified")
        
        # Create preview data with encoded columns
        train_preview_df = pd.concat([X_train.head(200), y_train.head(200)], axis=1)
        test_preview_df = pd.concat([X_test.head(200), y_test.head(200)], axis=1)
        
        train_preview = train_preview_df.to_dict('records')
        test_preview = test_preview_df.to_dict('records')
        
        print(f"✅ Encoding complete!")
        print(f"   Train shape: {X_train.shape}")
        print(f"   Test shape: {X_test.shape}")
        print(f"   Encoded columns: {encoded_columns}")
        print("=" * 80 + "\n")
        
        # Include target column in the columns list
        target_col_name = y_train.name if hasattr(y_train, 'name') else 'target'
        all_columns = list(X_train.columns) + [target_col_name]
        
        return {
            "success": True,
            "message": f"Successfully encoded {len(encoded_columns)} columns",
            "train_shape": list(X_train.shape),
            "test_shape": list(X_test.shape),
            "encoded_columns": encoded_columns,
            "onehot_columns": onehot_columns, # Added
            "train_preview": train_preview,
            "test_preview": test_preview,
            "columns": all_columns
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Encoding error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Encoding error: {str(e)}")





from pydantic import BaseModel 
from typing import List, Optional

class ColumnScaling(BaseModel):
    name: str
    method: str = 'standard'

class ScalingRequest(BaseModel):
    dataset_id: str
    columns: List[ColumnScaling]



class DateTimeRequest(BaseModel):
    dataset_id: str
    columns: List[str]
    features: List[str]
    cyclic: bool = False
    drop_original: bool = True
    target_column: Union[str, Dict, None] = None

@app.post("/api/datasets/apply-scaling")
@app.post("/api/datasets/apply-scaling")
async def apply_scaling(request: ScalingRequest):
    """Apply feature scaling to specified numerical columns"""
    global X_train_storage, X_test_storage, split_scalers
    
    try:
        dataset_id = request.dataset_id
        columns_to_scale = request.columns
        
        print(f"Scaling request for dataset: {dataset_id}")
        print(f"Columns to scale: {len(columns_to_scale)}")
        
        if dataset_id not in X_train_storage or dataset_id not in X_test_storage:
            raise HTTPException(status_code=400, detail="Dataset not split yet. Please split first.")
        
        X_train = X_train_storage[dataset_id].copy()
        X_test = X_test_storage[dataset_id].copy()
        
        if not columns_to_scale:
            raise HTTPException(status_code=400, detail="No columns specified for scaling")
            
        scalers_used = {}
        scaled_columns = []
        
        for col_info in columns_to_scale:
            col_name = col_info.name
            method = col_info.method.lower()
            
            if col_name not in X_train.columns:
                print(f"⚠️ Column {col_name} not found, skipping...")
                continue
                
            print(f"Scaling {col_name} using {method}...")
            
            # Select scaler
            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            elif method == 'robust':
                scaler = RobustScaler()
            elif method == 'maxabs':
                scaler = MaxAbsScaler()
            else:
                print(f"⚠️ Unknown scaling method: {method}")
                continue
                
            # Apply scaling
            # Reshape for single column scaling
            X_train[[col_name]] = scaler.fit_transform(X_train[[col_name]])
            X_test[[col_name]] = scaler.transform(X_test[[col_name]])
            
            scalers_used[col_name] = {
                'scaler': scaler,
                'method': method
            }
            scaled_columns.append(col_name)
        
        # Update storage
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        split_scalers[dataset_id] = scalers_used
        
        # ── SYNC BASE DATAFRAME ──────────────────────────────────────────────
        # Reconstruct the full dataset from train + test so that
        # GET /api/datasets/{id} (used by data-preview page) always reflects
        # the latest scaled state. Without this, data-preview shows stale
        # pre-scaling data because it reads from datasets[id]['dataframe'].
        try:
            full_X = pd.concat([X_train, X_test], axis=0).reset_index(drop=True)
            y_train_sync = y_train_storage.get(dataset_id)
            y_test_sync = y_test_storage.get(dataset_id)
            
            if y_train_sync is not None and y_test_sync is not None:
                full_y = pd.concat([y_train_sync, y_test_sync], axis=0).reset_index(drop=True)
                full_df = pd.concat([full_X, full_y], axis=1)
            else:
                full_df = full_X
                
            datasets[dataset_id]['dataframe'] = full_df
            print(f"✅ Base dataframe synced after scaling. Shape: {full_df.shape}")
        except Exception as sync_err:
            print(f"⚠️  Could not sync base dataframe after scaling: {sync_err}")
        # ─────────────────────────────────────────────────────────────────────
        
        # Update dataset metadata
        datasets[dataset_id]['is_scaled'] = True
        datasets[dataset_id]['scaled_columns'] = scaled_columns
        datasets[dataset_id]['scalers'] = list(scalers_used.keys())
        
        # Create preview data for frontend
        y_train = y_train_storage.get(dataset_id)
        y_test = y_test_storage.get(dataset_id)
        
        # Ensure y_train/y_test are DataFrames/Series with correct index
        if y_train is not None and y_test is not None:
             train_preview_df = pd.concat([X_train.head(200), y_train.head(200)], axis=1)
             test_preview_df = pd.concat([X_test.head(200), y_test.head(200)], axis=1)
        else:
             train_preview_df = X_train.head(200)
             test_preview_df = X_test.head(200)
        
        train_preview = train_preview_df.to_dict('records')
        test_preview = test_preview_df.to_dict('records')
        
        print(f"✅ Scaling complete: {len(scaled_columns)} columns scaled")
        
        # Include target column in the columns list if it exists
        all_columns = list(X_train.columns)
        if y_train is not None:
             target_col_name = y_train.name if hasattr(y_train, 'name') else 'target'
             all_columns.append(target_col_name)

        return {
            "success": True,
            "message": f"Successfully scaled {len(scaled_columns)} columns",
            "columns_scaled": len(scaled_columns),
            "scaled_columns": scaled_columns,
            "scaled_train_preview": train_preview,
            "scaled_test_preview": test_preview,
            "columns": all_columns
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Scaling error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/detect-problem-type")
async def detect_problem_type_endpoint(request: Dict[str, Any]):
    """Detect if the target is classification or regression for a given dataset_id and target_column"""
    try:
        dataset_id = request.get('dataset_id')
        target_column = request.get('target_column')

        if not dataset_id or not target_column:
            raise HTTPException(status_code=400, detail="dataset_id and target_column are required")

        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")

        df = datasets[dataset_id]['dataframe']
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail="Target column not found")

        target_series = df[target_column]
        target_type = str(target_series.dtype)
        unique_values = int(target_series.nunique(dropna=True))
        total_values = int(len(target_series))
        unique_ratio = float(unique_values / total_values) if total_values else 0.0

        # Determine problem type (align with app router logic)
        if target_type in ['object', 'category', 'bool']:
            problem_type = 'classification'
        elif target_type in ['int64', 'int32', 'float64', 'float32']:
            if unique_ratio < 0.05 or unique_values <= 20:
                problem_type = 'classification'
            else:
                problem_type = 'regression'
        else:
            problem_type = 'regression'

        def _reason(pt: str, tt: str, uv: int, ur: float) -> str:
            if pt == 'classification':
                if tt in ['object', 'category', 'bool']:
                    return f"Target variable is {tt} type, indicating classification problem"
                return f"Target has {uv} unique values ({ur:.1%} of total), suggesting discrete classes"
            return f"Target has {uv} unique values ({ur:.1%} of total), indicating continuous regression target"

        return {
            "problemType": problem_type,
            "targetType": target_type,
            "uniqueValues": unique_values,
            "uniqueRatio": unique_ratio,
            "reasoning": _reason(problem_type, target_type, unique_values, unique_ratio)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")

        

@app.get("/api/datasets")
async def get_datasets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """List all datasets for current user - Persisted"""
    try:
        datasets = db.query(DatasetModel).filter(DatasetModel.user_id == current_user['id']).order_by(DatasetModel.upload_date.desc()).all()
        return [
            {
                "id": str(d.id),
                "name": d.name,          # Frontend expected name
                "filename": d.name,      # Backward compatibility
                "upload_time": d.upload_date.isoformat(),
                "size_bytes": d.size_bytes,
                "rows": d.row_count,      # Frontend expected rows
                "row_count": d.row_count, # Backward compatibility
                "column_count": d.column_count,
                "is_processed": d.is_processed
            }
            for d in datasets
        ]
    except Exception as e:
        print(f"Error listing datasets: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Delete a dataset and its associated file, models, and versions"""
    try:
        user_id = current_user['id']
        dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id, DatasetModel.user_id == user_id).first()
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # 1. Delete associated models (physical files first)
        models_to_delete = db.query(ModelModel).filter(ModelModel.dataset_id == dataset_id).all()
        for model in models_to_delete:
            if model.storage_path and os.path.exists(model.storage_path):
                try:
                    os.remove(model.storage_path)
                except Exception as me:
                    print(f"⚠️ Error removing model file {model.storage_path}: {me}")
            db.delete(model)
        
        # 2. Delete child versions (recursive cleanup)
        child_versions = db.query(DatasetModel).filter(DatasetModel.parent_dataset_id == dataset_id).all()
        for version in child_versions:
            # We recursively call or just handle one level if that's the limit
            if version.storage_path and os.path.exists(version.storage_path):
                try:
                    os.remove(version.storage_path)
                except Exception as ve:
                    print(f"⚠️ Error removing version file {version.storage_path}: {ve}")
            db.delete(version)
            
        # 3. Delete physical file of the dataset itself
        if dataset.storage_path and os.path.exists(dataset.storage_path):
            try:
                os.remove(dataset.storage_path)
            except Exception as fe:
                print(f"⚠️ Error removing file {dataset.storage_path}: {fe}")
        
        # 4. Cleanup in-memory cache
        ds_id_str = str(dataset_id)
        if ds_id_str in datasets:
            del datasets[ds_id_str]
            
        # 5. Log the action
        log_user_action(db, user_id, "delete", {"filename": dataset.name}, resource_id=dataset_id, resource_type="dataset")
        
        # 6. Delete from database
        db.delete(dataset)
        db.commit()
        
        return {"success": True, "message": "Dataset and all associated data deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting dataset: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/missing-values/{dataset_id}")
async def get_missing_values(dataset_id: str):
    """Get missing values information for a dataset"""
    try:
        print(f"\n📊 Fetching missing values for dataset: {dataset_id}")
        
        
        print(f"   Available datasets: {list(datasets.keys())}")
        print(f"   Looking for: {dataset_id}")
        print(f"   Dataset exists: {dataset_id in datasets}")
        print(f"   Available dataset IDs: {list(datasets.keys())}")
        print(f"   Total datasets in memory: {len(datasets)}")
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = datasets[dataset_id]['dataframe']
        
        print(f"   Dataset shape: {df.shape}")
        print(f"   Total missing values: {df.isnull().sum().sum()}")
        
        # Calculate missing values per column
        missing_values = []
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            
            if missing_count > 0:
                # Detect column type
                if pd.api.types.is_numeric_dtype(df[col]):
                    col_type = 'numerical'
                else:
                    col_type = 'categorical'
                
                missing_values.append({
                    'column': col,
                    'type': col_type,
                    'count': int(missing_count),
                    'percentage': round((missing_count / len(df)) * 100, 1)
                })
        
        print(f"   Columns with missing values: {len(missing_values)}")
        
        return {
            "dataset_id": dataset_id,
            "missing_values": missing_values,
            "total_missing": int(df.isnull().sum().sum()),
            "total_rows": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching missing values: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/train-model")
async def train_model_websocket(websocket: WebSocket):
    """Advanced ML training with feature scaling and engineering - REFACTORED"""
    await websocket.accept()
    
    try:
        # ===== RECEIVE CONFIGURATION =====
        config_data = await websocket.receive_text()
        config = json.loads(config_data)
        
        print(f"🔍 [Training] Received training request with config: {config}")
        
        # Extract configuration
        dataset_id = config['dataset_id']
        target_column = config['target_column']
        # Parse target_column if it's a JSON string
        if isinstance(target_column, str) and target_column.startswith('{'):
            try:
                target_json = json.loads(target_column)
                target_column = target_json.get('name', target_column)
                print(f"🎯 [Training] Parsed target_column from JSON: {target_column}")
            except:
                pass
        algorithm_name = config['algorithm_name']
        test_size = config.get('test_size', 0.2)

        validation_method = config.get('validation_method', 'train_test_split')
        cv_folds = config.get('cv_folds', 5)
        hyperparameters = config.get('hyperparameters', {})
        problem_type_from_config = config.get('problem_type')
        
        print(f"🚀 Starting training with algorithm: {algorithm_name}")
        print(f"📊 Hyperparameters: {hyperparameters}")
    
        # ===== VALIDATE DATASET =====
        # Try to re-hydrate if missing
        db = next(get_db())
        dataset_info = await ensure_dataset_in_memory(dataset_id, db)
        
        if not dataset_info:
            print(f"❌ [Training] Dataset {dataset_id} not found even after re-hydration attempt")
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': '❌ Dataset not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        await websocket.send_text(json.dumps({
            'status': 'started',
            'message': f'🚀 Starting {algorithm_name} training...',
        # Check if preprocessed data exists (validate all 4 storage dicts)
        }))
        if (dataset_id not in X_train_storage or dataset_id not in X_test_storage or
            dataset_id not in y_train_storage or dataset_id not in y_test_storage):
            
            print(f"🔄 [Training] Preprocessed data not found for {dataset_id}. Attempting auto-split...")
            try:
                # We need the dataframe to split
                if dataset_id not in datasets:
                    # Should have been re-hydrated above, but double check
                    await ensure_dataset_in_memory(dataset_id, db)
                
                if dataset_id not in datasets:
                    raise Exception("Dataset not found in memory or DB")
                
                df = datasets[dataset_id]['dataframe']
                if target_column not in df.columns:
                    raise Exception(f"Target column '{target_column}' not found")
                
                # Perform split
                X = df.drop(columns=[target_column])
                y = df[target_column]
                
                from sklearn.model_selection import train_test_split
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
                
                # Store in memory
                X_train_storage[dataset_id] = X_train
                X_test_storage[dataset_id] = X_test
                y_train_storage[dataset_id] = y_train
                y_test_storage[dataset_id] = y_test
                
                print(f"✅ [Training] Auto-split successful for {dataset_id}")
            except Exception as e:
                error_msg = f"❌ Preprocessed data not found and auto-split failed: {str(e)}"
                print(error_msg)
                await websocket.send_text(json.dumps({
                    'status': 'failed',
                    'message': error_msg,
                    'timestamp': datetime.now().timestamp()
                }))
                return
        
        # Retrieve preprocessed data and make copies to avoid mutation
        X_train = X_train_storage[dataset_id].copy()
        X_test = X_test_storage[dataset_id].copy()
        y_train = y_train_storage[dataset_id].copy()
        y_test = y_test_storage[dataset_id].copy()
        
        print(f"✅ Retrieved preprocessed data:")
        print(f"   X_train shape: {X_train.shape}")
        print(f"   X_test shape: {X_test.shape}")
        print(f"   y_train shape: {y_train.shape}")
        print(f"   y_test shape: {y_test.shape}")
        print("="*80)
        await websocket.send_text(json.dumps({
            'status': 'data_loaded',
            'message': f'✅ Loaded preprocessed data: {len(X_train)} train, {len(X_test)} test samples',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== CAPTURE FEATURE NAMES BEFORE CONVERSION =====
        current_feature_names = []
        if isinstance(X_train, pd.DataFrame):
            current_feature_names = X_train.columns.tolist()
        elif hasattr(X_train, 'columns'):
            current_feature_names = list(X_train.columns)
        
        # Get specific registry for this dataset
        dataset_feature_registry = feature_metadata.get(dataset_id, {})
        
        # ===== ENCODE CATEGORICAL FEATURES =====
        # Check if data is DataFrame and has categorical columns
        label_encoders = {}
        if hasattr(X_train, 'select_dtypes'):
            categorical_columns = X_train.select_dtypes(include=['object', 'category']).columns
            
            if len(categorical_columns) > 0:
                await websocket.send_text(json.dumps({
                    'status': 'preprocessing',
                    'message': f'🔤 Encoding {len(categorical_columns)} categorical features...',
                    'timestamp': datetime.now().timestamp()
                }))
                
                for col in categorical_columns:
                    le = LabelEncoder()
                    # Fit on combined train+test to ensure consistent encoding
                    combined_values = pd.concat([X_train[col], X_test[col]]).astype(str)
                    le.fit(combined_values)
                    
                    X_train[col] = le.transform(X_train[col].astype(str))
                    X_test[col] = le.transform(X_test[col].astype(str))
                    label_encoders[col] = le
                
                print(f"✅ Encoded {len(categorical_columns)} categorical columns: {list(categorical_columns)}")

                
        
        # ===== DETECT PROBLEM TYPE FROM PREPROCESSED DATA =====
        problem_type = problem_type_from_config or detect_problem_type(y_train)
        
        # ✅ Normalize problem type for internal logic consistency
        if problem_type and 'classification' in problem_type.lower():
            problem_type = 'classification'
        elif problem_type and 'regression' in problem_type.lower():
            problem_type = 'regression'
            
        await websocket.send_text(json.dumps({
            'status': 'analyzing',
            'message': f'🔍 Detected: {problem_type.upper()}',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== ENCODE TARGET IF CATEGORICAL =====
        target_encoder = None
        # Robust handling for classification: Ensure labels are discrete
        if problem_type == 'classification':
            if hasattr(y_train, 'dtype') and pd.api.types.is_object_dtype(y_train):
                target_encoder = LabelEncoder()
                y_train = target_encoder.fit_transform(y_train.astype(str))
                y_test = target_encoder.transform(y_test.astype(str))
                
                await websocket.send_text(json.dumps({
                    'status': 'preprocessing',
                    'message': f'🏷️ Encoded target: {len(target_encoder.classes_)} classes',
                    'timestamp': datetime.now().timestamp()
                }))
            elif pd.api.types.is_numeric_dtype(y_train):
                # Force numeric labels to integers to avoid "continuous" errors from float noise
                print("   🎯 [Training] Casting numeric classification target to int to ensure discrete labels")
                # Handle potential NaNs or infs before casting to avoid errors
                if hasattr(y_train, 'replace'):
                    y_train = y_train.replace([np.inf, -np.inf], 0).fillna(0).astype(int)
                    y_test = y_test.replace([np.inf, -np.inf], 0).fillna(0).astype(int)
                else:
                    y_train = y_train.astype(int)
                    y_test = y_test.astype(int)
        
        # ===== CONVERT TO NUMPY IF NEEDED =====
        # Ensure data is in numpy array format for sklearn
        if hasattr(X_train, 'values'):
            X_train = X_train.values
        if hasattr(X_test, 'values'):
            X_test = X_test.values
        if hasattr(y_train, 'values'):
            y_train = y_train.values
        if hasattr(y_test, 'values'):
            y_test = y_test.values
        
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # ===== MODEL INITIALIZATION (REFACTORED) =====
        await websocket.send_text(json.dumps({
            'status': 'model_init',
            'message': f'🤖 Initializing {algorithm_name}...',
            'timestamp': datetime.now().timestamp()
        }))
        
        try:
            # ✅ USE NEW INITIALIZATION FUNCTION
            model = initialize_algorithm_with_params(
                algorithm_name, 
                problem_type, 
                hyperparameters
            )
            
            model_class_name = model.__class__.__name__
            
            await websocket.send_text(json.dumps({
                'status': 'model_ready',
                'message': f'✅ {model_class_name} initialized for {problem_type}',
                'timestamp': datetime.now().timestamp()
            }))
            
            # ===== VALIDATE DATA FOR MULTINOMIALNB =====
            if algorithm_name == 'MultinomialNB' or model_class_name == 'MultinomialNB':
                # Check for negative values
                has_negative = False
                if hasattr(X_train, 'min'):
                    has_negative = (X_train.min() < 0)
                else:
                    has_negative = (np.min(X_train) < 0)
                
                if has_negative:
                    await websocket.send_text(json.dumps({
                        'status': 'failed',
                        'message': (
                            '❌ MultinomialNB requires non-negative features, but your data contains negative values. '
                            'Solutions: (1) Use GaussianNB instead, or (2) Apply Min-Max scaling in preprocessing step.'
                        ),
                        'timestamp': datetime.now().timestamp()
                    }))
                    return
            
        except Exception as e:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'❌ Model initialization failed: {str(e)}',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ===== TRAINING & VALIDATION (MULTIPROCESSING REFACTOR) =====
        import uuid
        ws_id = str(uuid.uuid4())
        result_queue = multiprocessing.Queue()
        
        # Prepare worker config
        worker_config = {
            'algorithm_name': algorithm_name,
            'problem_type': problem_type,
            'hyperparameters': hyperparameters,
            'validation_method': validation_method,
            'cv_folds': cv_folds,
            'grid_density': config.get('grid_density', 'normal'),
            'grid_search_cv_folds': config.get('grid_search_cv_folds', 5),
            'random_search_iterations': config.get('random_search_iterations', 20),
            'random_search_cv_folds': config.get('random_search_cv_folds', 5)
        }
        
        # Prepare target classes for worker
        target_classes = None
        if target_encoder:
            target_classes = target_encoder.classes_.tolist()
        
        # Start training process
        p = multiprocessing.Process(
            target=training_worker, 
            args=(worker_config, X_train, X_test, y_train, y_test, result_queue, current_feature_names, dataset_feature_registry, target_classes)
        )
        active_training_processes[ws_id] = p
        p.start()
        
        print(f"🚀 [Training] Started worker process {p.pid} for WS {ws_id}")
        
        try:
            while p.is_alive() or not result_queue.empty():
                # 1. Listen for "stop" message from client (with timeout)
                try:
                    # We use a non-blocking wait to check for messages
                    raw_msg = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                    msg = json.loads(raw_msg)
                    if msg.get('action') == 'stop':
                        print(f"🛑 [Training] Stop signal received for {ws_id}")
                        p.terminate()
                        p.join()
                        await websocket.send_text(json.dumps({
                            'status': 'stopped',
                            'message': '⏹️ Training stopped by user',
                            'timestamp': datetime.now().timestamp()
                        }))
                        return
                except asyncio.TimeoutError:
                    pass # No message received, continue
                except Exception as e:
                    # Handle disconnection or other WS errors
                    if not str(e).strip(): # Happens on close
                        print(f"🔌 [Training] WebSocket closed during training for {ws_id}")
                    else:
                        print(f"⚠️ [Training] WS error: {e}")
                    p.terminate()
                    break
                
                # 2. Check for updates from worker
                try:
                    update = result_queue.get_nowait()
                    if update['status'] == 'success':
                        # Store in global dictionary
                        model_info = update.get('model_info')
                        if model_info:
                            # Add missing context
                            model_id = model_info['model_id']
                            model_info['dataset_id'] = dataset_id
                            model_info['target_column'] = target_column
                            trained_models[model_id] = model_info
                            
                            # Store visualization data if present
                            if 'visualization_data' in update:
                                visualization_data[model_id] = update['visualization_data']
                            
                            # Store in DB for persistence
                            try:
                                from models import Model as ModelModel
                                new_model_record = ModelModel(
                                    user_id=dataset_info.get('user_id') if isinstance(dataset_info, dict) else (dataset_info.user_id if hasattr(dataset_info, 'user_id') else 1),
                                    dataset_id=int(dataset_id),
                                    name=f"{algorithm_name} Model",
                                    algorithm=algorithm_name,
                                    storage_path=model_info['model_path'],
                                    metrics=model_info['final_metrics'],
                                    hyperparameters=model_info['hyperparameters']
                                )
                                db.add(new_model_record)
                                db.commit()
                                db.refresh(new_model_record)
                                
                                # Log Action
                                log_user_action(db, new_model_record.user_id, "train", {
                                    "algorithm": algorithm_name, 
                                    "accuracy": model_info['final_metrics'].get('accuracy', model_info['final_metrics'].get('r2', 0))
                                }, resource_id=new_model_record.id, resource_type="model")
                                
                            except Exception as e:
                                print(f"⚠️ Failed to save model to DB: {e}")
                                db.rollback()
                            
                            await websocket.send_text(json.dumps({
                                'status': 'completed',
                                'model_id': model_id,
                                'final_metrics': model_info['final_metrics'],
                                'message': f"🎉 Training completed! {update['message']}",
                                'timestamp': datetime.now().timestamp()
                            }))
                        break
                    elif update['status'] == 'error':
                        await websocket.send_text(json.dumps({
                            'status': 'failed',
                            'message': f"❌ Error: {update['message']}",
                            'timestamp': datetime.now().timestamp()
                        }))
                        break
                    else:
                        # Forward progress messages
                        await websocket.send_text(json.dumps({
                            'status': update['status'],
                            'message': update['message'],
                            'timestamp': datetime.now().timestamp()
                        }))
                except queue.Empty:
                    await asyncio.sleep(0.5) # Wait before next check
                    
            p.join()
            
        finally:
            if ws_id in active_training_processes:
                del active_training_processes[ws_id]
                
    except Exception as e:
        print(f"❌ [Training] Global error: {e}")
        traceback.print_exc()
        try:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f"❌ Training failed: {str(e)}",
                'timestamp': datetime.now().timestamp()
            }))
        except:
            pass
        
    except WebSocketDisconnect:
        print("⚠️ WebSocket disconnected during training")
        
    except Exception as e:
        print(f"❌ Training error: {str(e)}")
        traceback.print_exc()
        
        try:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'❌ Training failed: {str(e)}',
                'error_details': traceback.format_exc(),
                'timestamp': datetime.now().timestamp()
            }))
        except:
            pass





@app.get("/api/models/{model_id}")
async def get_model_info(model_id: str):
    """Get detailed model information"""
    if model_id not in trained_models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return trained_models[model_id]

@app.get("/api/models/{model_id}/download")
async def download_model(
    model_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Download the trained model file"""
    model_path = None
    model_name = "model"
    
    # 1. Check in-memory storage (most recent)
    if model_id in trained_models:
        model_info = trained_models[model_id]
        model_path = model_info.get('model_path')
    
    # 2. Check Database if not in memory
    if not model_path:
        model_db = db.query(ModelModel).filter(
            ModelModel.id == model_id,
            ModelModel.user_id == current_user['id']
        ).first()
        
        if not model_db:
            # Try UUID string match if ID is string (compatibility)
            model_db = db.query(ModelModel).filter(
                ModelModel.user_id == current_user['id']
            ).all()
            model_db = next((m for m in model_db if str(m.id) == model_id), None)
            
        if model_db:
            model_path = model_db.storage_path
            model_name = model_db.name.replace(" ", "_")
        
    if not model_path or not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found on server")
    
    filename = f"{model_name}.joblib"
    return FileResponse(
        path=model_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/api/debug")
async def debug_info():
    """Debug information"""
    return {
        "datasets_in_memory": len(datasets),
        "dataset_ids": list(datasets.keys()),
        "dataset_details": {
            ds_id: {
                "shape": list(data['dataframe'].shape),
                "preprocessed": data.get('preprocessed', False),
                "uploaded_at": data.get('uploaded_at')
            }
            for ds_id, data in datasets.items()
        },
        "trained_models": len(trained_models),
        "active_scalers": len(scalers)
    }

# ===== RUN SERVER =====

# ============================================
# PREPROCESSING ENDPOINTS
# ============================================


class DropColumnsRequest(BaseModel):
    columns: List[str]

class MissingValueRequest(BaseModel):
    strategy: str  # 'droprows', 'fillmean', etc.
    columns: List[str]
    target_column: Union[str, Dict, None] = None

class OutlierRequest(BaseModel):
    method: str  # 'cap', 'remove'
    target_column: Union[str, Dict, None] = None

class DuplicateRequest(BaseModel):
    keep: str  # 'first', 'last', 'all'

class SaveVersionRequest(BaseModel):
    version_name: str

# Helper to save dataset state
def save_dataset_state(dataset_id: str, df: pd.DataFrame, log_entry: dict = None):
    datasets[dataset_id]['dataframe'] = df
    datasets[dataset_id]['preprocessed'] = True
    
    # Update shape in metadata
    if 'metadata' not in datasets[dataset_id]:
        datasets[dataset_id]['metadata'] = {}
    
    datasets[dataset_id]['metadata']['rows'] = df.shape[0]
    datasets[dataset_id]['metadata']['columns'] = df.shape[1]
    
    # Add to log
    if 'processing_log' not in datasets[dataset_id]:
        datasets[dataset_id]['processing_log'] = []
    
    if log_entry:
        datasets[dataset_id]['processing_log'].append(log_entry)

@app.post("/api/datasets/{dataset_id}/save-version")
async def save_dataset_version(
    dataset_id: str,
    request: SaveVersionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    """Persist the current in-memory state of a dataset as a new version"""
    if dataset_id not in datasets:
        # Try to re-hydrate if missing
        await ensure_dataset_in_memory(dataset_id, db)
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found in memory or DB")
        
    try:
        # Reconstruct transformed dataframe if split exists (capture preprocessed state)
        if (str(dataset_id) in X_train_storage and str(dataset_id) in X_test_storage and 
            str(dataset_id) in y_train_storage and str(dataset_id) in y_test_storage):
            
            print(f"🔄 Reconstructing transformed dataset for saving (Dataset {dataset_id})")
            X_train = X_train_storage[str(dataset_id)]
            X_test = X_test_storage[str(dataset_id)]
            y_train = y_train_storage[str(dataset_id)]
            y_test = y_test_storage[str(dataset_id)]
            
            # Reconstruct transformed train set
            train_df = X_train.copy()
            target_name = y_train.name if hasattr(y_train, 'name') else 'target'
            train_df[target_name] = y_train
            
            # Reconstruct transformed test set
            test_df = X_test.copy()
            test_df[target_name] = y_test
            
            # Concatenate
            df = pd.concat([train_df, test_df], axis=0)
            
            # Convert to dense if sparse columns are present (to avoid Parquet issues with multi-type sparse stores)
            if hasattr(df, 'sparse'):
                df = df.sparse.to_dense()
                
            print(f"✅ Reconstructed transformed dataset: {len(df)} rows, {len(df.columns)} columns")
        else:
            df = datasets[dataset_id]['dataframe']

        user_id = current_user['id']
        version_name = request.version_name
        
        # 1. Save to disk
        file_path = file_service.save_dataframe(df, user_id, version_name, is_processed=True)
        
        # 2. Fetch parent ID
        try:
            parent_id = int(dataset_id)
        except:
            parent_id = None
        
        # 3. Create DB Record
        new_dataset = DatasetModel(
            user_id=user_id,
            name=version_name,
            storage_path=file_path,
            row_count=len(df),
            column_count=len(df.columns),
            size_bytes=os.path.getsize(file_path),
            is_processed=True,
            parent_dataset_id=parent_id
        )
        
        # 3.1 Calculate Quality Score
        try:
            missing_values = {str(col): int(df[col].isnull().sum()) for col in df.columns}
            duplicates = int(df.duplicated().sum())
            col_stats = [{"name": str(col), "unique": int(df[col].nunique())} for col in df.columns]
            
            outliers = 0
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                v = df[col].dropna()
                if len(v) > 0:
                    q1, q3 = v.quantile([0.25, 0.75])
                    iqr = q3 - q1
                    outliers += int(((v < (q1 - 1.5 * iqr)) | (v > (q3 + 1.5 * iqr))).sum())
            
            partial_stats = {
                "missing_values": missing_values, "duplicates": duplicates,
                "outliers": outliers, "column_stats": col_stats
            }
            quality_info = calculate_quality_score(df, partial_stats)
            
            # Inherit column metadata from parent
            parent_ds = db.query(DatasetModel).filter(DatasetModel.id == parent_id).first()
            if parent_ds and parent_ds.column_metadata:
                # Merge: Quality score from new, rest from parent
                new_metadata = parent_ds.column_metadata.copy()
                new_metadata["quality_score"] = quality_info["score"]
                new_dataset.column_metadata = new_metadata
            else:
                new_dataset.column_metadata = {"quality_score": quality_info["score"]}
        except Exception as q_err:
            print(f"⚠️ Could not calculate version quality score: {q_err}")

        db.add(new_dataset)
        db.commit()
        db.refresh(new_dataset)
        
        # 4. Log Action
        log_user_action(db, user_id, "save_version", {
            "version_name": version_name,
            "parent_id": parent_id,
            "rows": len(df)
        }, resource_id=new_dataset.id, resource_type="dataset")
        
        return {
            "success": True,
            "dataset_id": str(new_dataset.id),
            "name": new_dataset.name,
            "message": f"Successfully saved version '{version_name}'"
        }
        
    except Exception as e:
        print(f"Error saving dataset version: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/datasets/{dataset_id}/preprocessing/drop-columns")
async def drop_columns(dataset_id: str, request: DropColumnsRequest, current_user: dict = Depends(auth.get_current_user)):
    """Drop specified columns"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = datasets[dataset_id]['dataframe']
        # Load semantic types if available
        metadata = datasets[dataset_id].get('column_metadata', {})
        processor = DataPreprocessor(df, column_metadata=metadata)
        
        df_new = processor.remove_columns(request.columns)
        
        save_dataset_state(dataset_id, df_new, {
            'action': 'drop_columns',
            'columns': request.columns,
            'timestamp': datetime.now().isoformat()
        })
        
        # Log Action
        log_user_action(db, current_user['id'], "cleaning", {
            "sub_action": "drop_columns",
            "columns": request.columns
        }, resource_id=int(dataset_id), resource_type="dataset")
        
        return {
            "success": True, 
            "message": f"Dropped {len(request.columns)} columns",
            "current_shape": list(df_new.shape)
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/datasets/{dataset_id}/preprocessing/missing-values")
async def handle_missing_values_route(dataset_id: str, request: MissingValueRequest, current_user: dict = Depends(auth.get_current_user)):
    """Handle missing values"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = datasets[dataset_id]['dataframe']
        metadata = datasets[dataset_id].get('column_metadata', {})
        processor = DataPreprocessor(df, column_metadata=metadata)
        
        # Convert request to expected format {col: strategy}
        strategies = {col: request.strategy for col in request.columns}
        
        # ✅ Identify and exclude target column
        target_column = request.target_column
        if not target_column and dataset_id in datasets:
             target_column = datasets[dataset_id].get('target_column')
             
        if isinstance(target_column, str) and target_column.startswith('{'):
             try:
                 import json
                 target_json = json.loads(target_column)
                 target_column = target_json.get('name')
             except: pass
             
        if target_column and target_column in strategies:
            print(f"   Skipping target column '{target_column}' during missing value handling")
            del strategies[target_column]
        
        print(f"Applying missing value strategy: {request.strategy} for {len(strategies)} columns")
        
        df_new = processor.handle_missing_values(strategies)
        
        save_dataset_state(dataset_id, df_new, {
            'action': 'missing_values',
            'strategy': request.strategy,
            'columns': request.columns,
            'timestamp': datetime.now().isoformat()
        })
        
        # Log Action
        log_user_action(db, current_user['id'], "cleaning", {
            "sub_action": "handle_missing",
            "strategy": request.strategy,
            "columns": request.columns
        }, resource_id=int(dataset_id), resource_type="dataset")
        
        return {
            "success": True,
            "message": "Missing values processed",
            "current_shape": list(df_new.shape)
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/datasets/{dataset_id}/preprocessing/outliers")
async def handle_outliers_route(dataset_id: str, request: OutlierRequest, current_user: dict = Depends(auth.get_current_user)):
    """Handle outliers"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = datasets[dataset_id]['dataframe']
        metadata = datasets[dataset_id].get('column_metadata', {})
        processor = DataPreprocessor(df, column_metadata=metadata)
        
        # Detect numeric columns for outlier handling
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Check semantic types to verify they are actually numeric
        if metadata:
            numeric_cols = [c for c in numeric_cols if metadata.get(c, {}).get('semantic_type') == 'numeric']
            
        # ✅ Identify and exclude target column
        target_column = request.target_column
        if not target_column and dataset_id in datasets:
             target_column = datasets[dataset_id].get('target_column')
             
        if isinstance(target_column, str) and target_column.startswith('{'):
             try:
                 import json
                 target_json = json.loads(target_column)
                 target_column = target_json.get('name')
             except: pass
             
        if target_column and target_column in numeric_cols:
            print(f"   Skipping target column '{target_column}' during outlier handling")
            numeric_cols.remove(target_column)
        
        print(f"Checking outliers in {len(numeric_cols)} numeric columns using {request.method} method")
        
        # Mapping: Frontend sends 'cap'/'remove' as 'method' (via OutlierRequest match to data-preview)
        # But backend processor takes 'method' (iqr/zscore) and 'strategy' (cap/remove)
        # The frontend seems to send { method: outlierStrategy.value } where value is 'cap' or 'remove'
        # We'll use 'iqr' as default detection method
        
        strategy = request.method # 'cap' or 'remove'
        detection_method = 'iqr'
        
        df_new = processor.handle_outliers(numeric_cols, method=detection_method, strategy=strategy)
        
        save_dataset_state(dataset_id, df_new, {
            'action': 'outliers',
            'strategy': strategy,
            'method': detection_method,
            'timestamp': datetime.now().isoformat()
        })
        
        # Log Action
        log_user_action(db, current_user['id'], "cleaning", {
            "sub_action": "handle_outliers",
            "strategy": strategy,
            "method": detection_method
        }, resource_id=int(dataset_id), resource_type="dataset")
        
        return {
            "success": True,
            "message": "Outliers processed",
            "current_shape": list(df_new.shape)
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/datasets/{dataset_id}/preprocessing/remove-duplicates")
async def handle_duplicates_route(dataset_id: str, request: DuplicateRequest, current_user: dict = Depends(auth.get_current_user)):
    """Remove duplicates"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = datasets[dataset_id]['dataframe']
        processor = DataPreprocessor(df)
        
        df_new = processor.remove_duplicates(strategy=request.keep)
        
        save_dataset_state(dataset_id, df_new, {
            'action': 'remove_duplicates',
            'strategy': request.keep,
            'timestamp': datetime.now().isoformat()
        })
        
        # Log Action
        log_user_action(db, current_user['id'], "cleaning", {
            "sub_action": "remove_duplicates",
            "strategy": request.keep
        }, resource_id=int(dataset_id), resource_type="dataset")
        
        return {
            "success": True,
            "message": "Duplicates removed",
            "current_shape": list(df_new.shape)
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/datasets/{dataset_id}/preprocessing/datetime")
async def handle_datetime_route(dataset_id: str, request: DateTimeRequest, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    """Handle datetime feature extraction"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = datasets[dataset_id]['dataframe']
        metadata = datasets[dataset_id].get('column_metadata', {})
        processor = DataPreprocessor(df, column_metadata=metadata)
        
        print(f"Extracting features from {len(request.columns)} datetime columns")
        
        # ✅ Identify and exclude target column
        process_columns = list(request.columns)
        target_column = request.target_column
        if not target_column and dataset_id in datasets:
             target_column = datasets[dataset_id].get('target_column')
             
        if isinstance(target_column, str) and target_column.startswith('{'):
             try:
                 import json
                 target_json = json.loads(target_column)
                 target_column = target_json.get('name')
             except: pass
             
        if target_column and target_column in process_columns:
            print(f"   Skipping target column '{target_column}' during datetime extraction")
            process_columns.remove(target_column)

        if not process_columns:
             return {"success": True, "message": "No columns to process (target excluded)", "current_shape": list(df.shape)}

        df_new = processor.handle_datetime_features(
            columns=process_columns,
            features=request.features,
            cyclic_encoding=request.cyclic,
            drop_original=request.drop_original
        )
        
        save_dataset_state(dataset_id, df_new, {
            'action': 'datetime_preprocessing',
            'columns': request.columns,
            'features': request.features,
            'cyclic': request.cyclic,
            'drop_original': request.drop_original,
            'timestamp': datetime.now().isoformat()
        })
        
        # Persist semantic types for new columns
        new_columns = [c for c in df_new.columns if c not in df.columns]
        if new_columns:
            # 1. Update In-Memory Metadata
            if 'column_metadata' not in datasets[dataset_id]:
                datasets[dataset_id]['column_metadata'] = {}
            
            for col in new_columns:
                if col in processor.semantic_types:
                    datasets[dataset_id]['column_metadata'][col] = {
                        "column": col,
                        "semantic_type": processor.semantic_types[col],
                        "is_override": True,
                        "reason": "Feature extraction component",
                        "updated_at": datetime.now().isoformat()
                    }
            
            # 2. Update Database Metadata
            dataset = db.query(DatasetModel).filter(DatasetModel.id == int(dataset_id)).first()
            if dataset:
                dataset_metadata = dataset.column_metadata or {}
                # Merge new overrides
                for col in new_columns:
                    if col in processor.semantic_types:
                        dataset_metadata[col] = datasets[dataset_id]['column_metadata'][col]
                
                dataset.column_metadata = dataset_metadata
                db.commit()
                dataset.column_metadata = dataset_metadata
                db.commit()
        
        return {
            "success": True,
            "message": "DateTime features processed",
            "current_shape": list(df_new.shape)
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("Starting DataSage ML Backend...")
    print("Features: Upload, Preprocess (SimpleImputer), Train, Predict")
    uvicorn.run(app, host="127.0.0.1", port=8000)
