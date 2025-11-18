"""
DataSage ML Backend - Clean Production Version
Fixed: Redundant endpoints, proper dataset updates, single storage
"""

from fastapi import FastAPI, WebSocket, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json
import asyncio
import io
import sys
import os
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi.responses import StreamingResponse


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
    train_test_split, cross_val_score, StratifiedKFold, KFold
)
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder,
    PolynomialFeatures
)
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif, f_regression

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
from preprocessing import DataPreprocessor

# ===== DIRECTORIES =====
UPLOAD_DIR = "enterprise_datasets"
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB limit
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True)

# ===== FASTAPI APP INITIALIZATION =====
app = FastAPI(
    title="DataSage ML Backend - Production Edition",
    version="2.0.0",
    description="Production-ready ML backend with proper dataset management"
)

# ===== CORS CONFIGURATION =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://localhost:3002"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ IMPORT AUTH ROUTER
try:
    import auth
    app.include_router(auth.router)
    print("✅ Auth router loaded successfully")
except ImportError as e:
    print(f"⚠️ Auth router not available: {e}")

# ===== SINGLE SOURCE OF TRUTH: GLOBAL STORAGE =====
datasets: Dict[str, Dict[str, Any]] = {}  # { dataset_id: { 'dataframe': df, 'metadata': {...} } }
trained_models: Dict[str, Dict[str, Any]] = {}
scalers: Dict[str, Any] = {}
X_train_storage: Dict[str, Any] = {}
X_test_storage: Dict[str, Any] = {}
y_train_storage: Dict[str, Any] = {}
y_test_storage: Dict[str, Any] = {}
split_scalers: Dict[str, Any] = {}

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
    
    if algorithm_name in ALGORITHMS:
        return ALGORITHMS[algorithm_name]
    
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
        'Neural Network (MLP)': {
            'classification': MLPClassifier,
            'regression': MLPRegressor
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
    
    
    if algorithm_name in algorithm_mapping:
        return algorithm_mapping[algorithm_name][problem_type]
    
    return RandomForestClassifier if problem_type == 'classification' else RandomForestRegressor



def initialize_algorithm_with_params(algorithm_name: str, problem_type: str, hyperparameters: dict):
    """
    Initialize algorithm with special handling for variant-based algorithms
    Supports: Naive Bayes variants, SVR, Ridge, Lasso, and all existing algorithms
    """
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


def apply_feature_scaling(X_train: np.ndarray, X_test: np.ndarray, scaling_method: str, model_id: str):
    """Apply feature scaling and store scaler"""
    scaler = None
    
    if scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        return X_train, X_test, None
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    scalers[model_id] = scaler
    
    return X_train_scaled, X_test_scaled, scaler

def apply_feature_engineering(X_train: np.ndarray, X_test: np.ndarray, 
                            feature_engineering: Dict[str, bool], y_train: np.ndarray, 
                            problem_type: str, model_id: str):
    """Apply feature engineering techniques"""
    transformers = {}
    
    if feature_engineering.get('polynomial', False):
        poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
        X_train = poly.fit_transform(X_train)
        X_test = poly.transform(X_test)
        transformers['polynomial'] = poly
    
    if feature_engineering.get('pca', False):
        pca = PCA(n_components=0.95)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        transformers['pca'] = pca
    
    if feature_engineering.get('featureSelection', False):
        score_func = f_classif if problem_type == 'classification' else f_regression
        k = min(20, X_train.shape[1])
        selector = SelectKBest(score_func=score_func, k=k)
        X_train = selector.fit_transform(X_train, y_train)
        X_test = selector.transform(X_test)
        transformers['feature_selector'] = selector
    
    if transformers:
        scalers[f"{model_id}_transformers"] = transformers
    
    return X_train, X_test, transformers

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

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and analyze CSV dataset"""
    try:
        print(f"📤 Receiving file upload: {file.filename}")
        
        # Read CSV
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        print(f"✅ CSV parsed successfully: {df.shape}")
        print(f"   Columns: {df.columns.tolist()}")
        print(f"   First row: {df.iloc[0].to_dict() if len(df) > 0 else 'empty'}")
        
        dataset_id = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        #  CHECK DATASET SIZE LIMITS
        row_count = len(df)
        col_count = len(df.columns)
        size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

        print(f"📊 Dataset size check:")
        print(f"   Rows: {row_count:,}")
        print(f"   Columns: {col_count}")
        print(f"   Memory: {size_mb:.1f} MB")

        # REJECT IF TOO LARGE (500K rows limit for in-memory processing)
        if row_count > 500000:
            raise HTTPException(
                status_code=413,
                detail=f"Dataset too large: {row_count:,} rows. Maximum: 500,000 rows"
            )

        if size_mb > 1000:  # 1 GB limit
            raise HTTPException(
                status_code=413,
                detail=f"Dataset too large: {size_mb:.1f}MB. Maximum: 1000MB"
            )

        #  WARN IF LARGE
        warning = None
        if row_count > 100000:
            warning = f"⚠️ Large dataset ({row_count:,} rows). Preprocessing may take 30-60 seconds."
            print(f"⚠️ {warning}")

        #  STORE FULL DATASET IN MEMORY
        datasets[dataset_id] = {
            'dataframe': df.copy(),
            'filename': file.filename,
            'uploaded_at': datetime.now().isoformat(),
            'preprocessed': False,
            'original_shape': df.shape,
            'total_rows': row_count, 
            'size_mb': round(size_mb, 2),
            
            'is_split': False,
            'is_scaled': False,
            'split_info': None,
            'X_train': None,
            'X_test': None,
            'y_train': None,
            'y_test': None,
            'scaler': None,
            'scaling_method': None,
            'scaled_columns': []
        }


        print(f"✅ FULL dataset {dataset_id} stored in memory: {row_count:,} rows")
        
        
        sample_size = min(200, len(df))
        sample_df = df.head(sample_size)
        
        print(f"📦 Preparing {sample_size} sample rows for response...")
        
        sample_data = []
        for idx, row in sample_df.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32, np.int16, np.int8)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64, np.float32, np.float16)):
                    if np.isnan(value) or np.isinf(value):
                        row_dict[str(col)] = None
                    else:
                        row_dict[str(col)] = float(value)
                elif isinstance(value, (np.bool_, bool)):
                    row_dict[str(col)] = bool(value)
                else:
                    row_dict[str(col)] = str(value)
            
            sample_data.append(row_dict)
        
        print(f" Sample data prepared: {len(sample_data)} rows")
        
        # Statistics
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
        
        response_data = {
        'dataset_id': dataset_id,
        'filename': file.filename,
        'shape': [int(df.shape[0]), int(df.shape[1])],
        'columns': [str(col) for col in df.columns.tolist()],
        'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
        'sample_data': sample_data,  # ← Sample for display
        'statistics': statistics,
        'upload_time': datetime.now().isoformat(),
        'success': True,
        'total_rows': int(df.shape[0]),  # ← FULL row count
        'total_columns': int(df.shape[1]),
        'warning': warning  # ← NEW: Warning for large datasets
        }
        
        print(f"   Returning upload response:")
        print(f"   Dataset ID: {dataset_id}")
        print(f"   Sample data rows: {len(sample_data)}")
        print(f"   Total rows: {df.shape[0]}")
        
        return response_data
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")



@app.get("/api/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get specific dataset information with sample data"""
    try:
        print(f"📊 Fetching dataset info for: {dataset_id}")
        
        if dataset_id not in datasets:
            print(f"❌ Dataset {dataset_id} not found in memory")
            print(f"   Available datasets: {list(datasets.keys())}")
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        data = datasets[dataset_id]
        df = data['dataframe']
        
        print(f"✅ Dataset found: {df.shape}")
        
        #  PREPARE SAMPLE DATA (CRITICAL!)
        sample_size = min(200, len(df))
        sample_df = df.head(sample_size)
        
        print(f"📦 Preparing {sample_size} sample rows...")
        
        sample_data = []
        for idx, row in sample_df.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                
                # Handle different data types properly
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32, np.int16, np.int8)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64, np.float32, np.float16)):
                    if np.isnan(value) or np.isinf(value):
                        row_dict[str(col)] = None
                    else:
                        row_dict[str(col)] = float(value)
                elif isinstance(value, (np.bool_, bool)):
                    row_dict[str(col)] = bool(value)
                else:
                    row_dict[str(col)] = str(value)
            
            sample_data.append(row_dict)
        
        print(f"✅ Sample data prepared: {len(sample_data)} rows")
        print(f"   First row keys: {list(sample_data[0].keys()) if sample_data else 'empty'}")
        
        # Prepare response
        response_data = {
        'dataset_id': dataset_id,
        'filename': data.get('filename', 'unknown'),
        'shape': [int(df.shape[0]), int(df.shape[1])],
        'total_rows': int(df.shape[0]),  # ← NEW: Add explicit total_rows
        'columns': [str(col) for col in df.columns.tolist()],
        'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
        'preprocessed': data.get('preprocessed', False),
        'uploaded_at': data.get('uploaded_at'),
        'sample_data': sample_data,  # ← Sample for display (200 rows)
        'status': 'success',
        'is_split': data.get('is_split', False),
        'is_scaled': data.get('is_scaled', False),
        'split_info': data.get('split_info')
    }
        print(f"✅ Returning response:")
        print(f"   Total rows in backend: {df.shape[0]}")
        print(f"   Sample rows returned: {len(sample_data)}")
        print(f"✅ Returning response with {len(sample_data)} sample rows")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in get_dataset_info: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching dataset: {str(e)}")



@app.post("/api/preprocess")
async def preprocess(config: dict):
    """Apply preprocessing steps to dataset - Fully Refactored & Robust"""
    new_dataset_id = None  # Safe initialization

    try:
        dataset_id = config.get("dataset_id")
        steps = config.get("steps", [])

        print("=" * 80)
        print("🔧 PREPROCESSING REQUEST")
        print("=" * 80)
        print(f"Dataset ID: {dataset_id}")
        print(f"Steps: {len(steps)}")

        if dataset_id not in datasets:
            return {"success": False, "error": f"Dataset {dataset_id} not found"}

        # ✅ Reset split/scaling if preprocessing changes after split
        if datasets[dataset_id].get("is_split", False):
            print(f"⚠️ Dataset was split. Resetting split & scaling state...")
            for key in ["is_split", "is_scaled", "X_train", "X_test", "y_train", "y_test", "scaler", "scaling_method", "split_info"]:
                datasets[dataset_id][key] = None
            print("✅ Split & scaling state reset complete")

        # ✅ Get FULL dataset
        df_full = datasets[dataset_id]["dataframe"].copy()
        original_rows = len(df_full)
        print(f"Original shape: {df_full.shape}")
        print(f"Original rows from storage: {original_rows}")

        from preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor(df_full)

        categorical_encoded = False
        encoded_columns = []

        # Main preprocessing loop
        for i, step in enumerate(steps, 1):
            step_type = step.get("type")
            print(f"\nStep {i}/{len(steps)}: {step_type}")

            if step_type == "handle_missing":
                strategies = step.get("strategies", {})
                print(f"  Strategies: {strategies}")
                if strategies:
                    preprocessor.handle_missing_values(strategies)
                    print(f"  ✅ Handled missing values")

            elif step_type == 'remove_columns':  
                columns_to_remove = step.get('columns', [])
                print(f"📋 Removing {len(columns_to_remove)} columns: {columns_to_remove}")
                
                if columns_to_remove:
                    # Filter out columns that don't exist
                    existing_cols = [col for col in columns_to_remove if col in preprocessor.df.columns]
                    missing_cols = [col for col in columns_to_remove if col not in preprocessor.df.columns]
                    
                    if missing_cols:
                        print(f"⚠️ Columns not found (skipping): {missing_cols}")
                    
                    if existing_cols:
                        before_cols = len(preprocessor.df.columns)
                        preprocessor.df = preprocessor.df.drop(columns=existing_cols)
                        after_cols = len(preprocessor.df.columns)
                        
                        print(f"✅ Columns removed: {existing_cols}")
                        print(f"   Before: {before_cols} columns → After: {after_cols} columns")
                        print(f"   Remaining columns: {preprocessor.df.columns.tolist()}")
                    else:
                        print("❌ No valid columns to remove")



            elif step_type == "remove_duplicates":
                keep = step.get("keep", "first")
                print(f"  Keep: {keep}")
                before = len(preprocessor.df)
                preprocessor.remove_duplicates(strategy=keep)
                after = len(preprocessor.df)
                print(f"  ✅ Duplicates removed: {before - after} rows")

            elif step_type == "handle_outliers":
                method = step.get("method", "remove")
                print(f"  Method: {method}")
                numeric_cols = preprocessor.df.select_dtypes(include=np.number).columns.tolist()
                if numeric_cols:
                    before = len(preprocessor.df)
                    preprocessor.handle_outliers(numeric_cols, method="iqr", strategy=method)
                    after = len(preprocessor.df)
                    print(f"  ✅ Outliers handled: {before - after} rows")

            elif step_type == "encode_categorical":
                columns_to_encode = step.get("columns", [])
                methods = step.get("methods", {})
                print(f"  Encoding columns: {columns_to_encode}")
                if columns_to_encode:
                    for col in columns_to_encode:
                        if col in preprocessor.df.columns:
                            method = methods.get(col, "label")
                            print(f"    - {col} ({method})...")
                            try:
                                preprocessor.encode_categorical(col, method=method)
                                categorical_encoded = True
                                encoded_columns.append(col)
                                print(f"      ✅ Encoded!")
                            except Exception as e:
                                print(f"      ❌ Error: {e}")
                        else:
                            print(f"    ⚠️ Column {col} not found")

        # Get processed dataframe
        processed_df = preprocessor.get_processed_dataframe()
        processed_rows = len(processed_df)

        print(f"\n📊 PROCESSING COMPLETE:")
        print(f"  Input: {original_rows} rows")
        print(f"  Output: {processed_rows} rows")
        print(f"  Columns: {len(processed_df.columns)}")

        processed_df = processed_df.replace([np.inf, -np.inf], np.nan)

        # ✅ Generate NEW cleaned dataset ID
        new_dataset_id = f"{dataset_id}_cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # ✅ Store the processed dataset
        datasets[new_dataset_id] = {
            "dataframe": processed_df.copy(),
            "filename": f"{datasets[dataset_id]['filename']}_cleaned",
            "uploaded_at": datasets[dataset_id]["uploaded_at"],
            "preprocessed": True,
            "original_dataset_id": dataset_id,
            "processing_steps": steps,
            "target_column": None,
            "is_split": False,
            "is_scaled": False,
            "split_info": None,
            "X_train": None,
            "X_test": None,
            "y_train": None,
            "y_test": None,
            "scaler": None,
            "scaling_method": None,
            "scaled_columns": []
        }

        print(f"✅ Stored processed dataset: {new_dataset_id}")

        # Prepare preview for frontend
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

        print("\n" + "=" * 80)
        print(f"✅ SUCCESS!")
        print(f"  Original: {original_rows}")
        print(f"  Cleaned: {processed_rows}")
        print(f"  Removed: {original_rows - processed_rows}")
        print(f"  New Dataset ID: {new_dataset_id}")
        print("=" * 80)

        return {
            "success": True,
            "preview": preview_data,
            "original_rows": original_rows,
            "total_rows": processed_rows,
            "rows_removed": original_rows - processed_rows,
            "categorical_encoded": categorical_encoded,
            "encoded_columns": encoded_columns,
            "cleaned_dataset_id": new_dataset_id
        }

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        # Return cleaned_dataset_id only if assigned
        error_response = {"success": False, "error": str(e)}
        if new_dataset_id is not None:
            error_response["cleaned_dataset_id"] = new_dataset_id
        return error_response





@app.get("/api/export-dataset/{dataset_id}")
async def export_dataset(dataset_id: str):
    """Export full dataset as CSV - FIXED with streaming"""
    try:
        print("\n" + "=" * 80)
        print(f"📥 EXPORT REQUEST: {dataset_id}")
        print("=" * 80)
        
        if dataset_id not in datasets:
            print(f"❌ Dataset {dataset_id} not found!")
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        df = datasets[dataset_id]["dataframe"].copy()
        
        print(f"✅ Found dataset: {len(df)} rows, {len(df.columns)} columns")
        
        # ✅ CRITICAL: Generate filename
        filename = datasets[dataset_id].get("filename", "dataset.csv")
        filename = filename.replace(".csv", "") + "_exported.csv"
        
        print(f"📄 Filename: {filename}")
        
        # ✅ CORRECT: Use StringIO to generate CSV
        def iter_csv():
            """Stream CSV line by line"""
            buffer = io.StringIO()
            
            # Write header
            df.to_csv(buffer, index=False, mode='w', header=True)
            yield buffer.getvalue()
            
            # Write data in chunks
            chunk_size = 1000
            for i in range(0, len(df), chunk_size):
                buffer = io.StringIO()
                df.iloc[i:i+chunk_size].to_csv(buffer, index=False, header=False)
                yield buffer.getvalue()
        
        print(f"✅ Streaming {len(df)} rows...")
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





# ===== TARGET VARIABLE SELECTION =====
@app.post("/api/set-target")
async def set_target(request: dict):
    """
    Set target variable and detect problem type
    """
    try:
        dataset_id = request.get('dataset_id')
        target_column = request.get('target_column')
        datasets[dataset_id]['target_column'] = target_column
        
        print(f"🎯 Setting target for dataset {dataset_id}: {target_column}")
        
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
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
async def split_dataset(request: Dict[str, Any]):
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
        
        # Get the target column from dataset metadata
        dataset_info = datasets[dataset_id]
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
        
        train_preview = train_preview_df.to_dict('records')
        test_preview = test_preview_df.to_dict('records')
        
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

# Storage for encoders (similar to split_scalers)
categorical_encoders = {}

@app.post("/api/apply-categorical-encoding")
async def apply_categorical_encoding(request: CategoricalEncodingRequest):
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
                X_test[col_name] = encoder.transform(X_test[col_name].astype(str))
                encoders_used[col_name] = {'type': 'label', 'encoder': encoder}
                encoded_columns.append(col_name)
                
            elif method == 'onehot':
                # One-Hot Encoding: Creates new columns
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                
                # Fit on train
                train_encoded = encoder.fit_transform(X_train[[col_name]])
                test_encoded = encoder.transform(X_test[[col_name]])
                
                # Create new column names
                feature_names = [f"{col_name}_{cat}" for cat in encoder.categories_[0]]
                
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
                
            elif method == 'ordinal':
                # Ordinal Encoding: Preserves order
                encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
                X_train[col_name] = encoder.fit_transform(X_train[[col_name]])
                X_test[col_name] = encoder.transform(X_test[[col_name]])
                encoders_used[col_name] = {'type': 'ordinal', 'encoder': encoder}
                encoded_columns.append(col_name)
            
            else:
                print(f"⚠️  Unknown encoding method: {method}")
        
        # Update storage
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        categorical_encoders[dataset_id] = encoders_used
        
        # Update dataset metadata
        datasets[dataset_id]['is_encoded'] = True
        datasets[dataset_id]['encoded_columns'] = encoded_columns
        datasets[dataset_id]['encoders'] = list(encoders_used.keys())
        
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
        
        return {
            "success": True,
            "message": f"Successfully encoded {len(encoded_columns)} columns",
            "train_shape": list(X_train.shape),
            "test_shape": list(X_test.shape),
            "encoded_columns": encoded_columns,
            "train_preview": train_preview,
            "test_preview": test_preview,
            "columns": list(X_train.columns)
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

class ScalingRequest(BaseModel):
    dataset_id: str
    method: str = 'standard'
    columns: Optional[List[str]] = None

@app.post("/api/datasets/apply-scaling")
async def apply_scaling(request: ScalingRequest):
    """Apply feature scaling to numerical columns"""
    global X_train_storage, X_test_storage, split_scalers
    
    try:
        dataset_id = request.dataset_id
        scaling_method = request.method
        columns = request.columns
        
        print(f"Scaling request for dataset: {dataset_id}")
        print(f"Method: {scaling_method}")
        
        if dataset_id not in X_train_storage or dataset_id not in X_test_storage:
            raise HTTPException(status_code=400, detail="Dataset not split yet. Please split first.")
        
        X_train = X_train_storage[dataset_id].copy()
        X_test = X_test_storage[dataset_id].copy()
        
        # If no columns specified, scale all numerical columns
        if not columns:
            columns = X_train.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            raise HTTPException(status_code=400, detail="No numerical columns found for scaling")
        
        print(f"Scaling columns: {columns}")
        
        # Select scaler
        if scaling_method == 'standard':
            scaler = StandardScaler()
        elif scaling_method == 'minmax':
            scaler = MinMaxScaler()
        elif scaling_method == 'robust':
            scaler = RobustScaler()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown scaling method: {scaling_method}")
        
        # Apply scaling
        X_train[columns] = scaler.fit_transform(X_train[columns])
        X_test[columns] = scaler.transform(X_test[columns])
        
        # Update storage
        X_train_storage[dataset_id] = X_train
        X_test_storage[dataset_id] = X_test
        split_scalers[dataset_id] = {
            'scaler': scaler,
            'columns': columns,
            'method': scaling_method
        }
        
        # Update dataset metadata
        datasets[dataset_id]['is_scaled'] = True
        datasets[dataset_id]['scaling_method'] = scaling_method
        datasets[dataset_id]['scaled_columns'] = columns
        
        # Create preview data for frontend
        y_train = y_train_storage.get(dataset_id)
        y_test = y_test_storage.get(dataset_id)
        
        train_preview_df = pd.concat([X_train.head(200), y_train.head(200)], axis=1)
        test_preview_df = pd.concat([X_test.head(200), y_test.head(200)], axis=1)
        
        train_preview = train_preview_df.to_dict('records')
        test_preview = test_preview_df.to_dict('records')
        
        print(f"✅ Scaling complete: {len(columns)} columns scaled")
        
        return {
            "success": True,
            "message": f"Scaling applied using {scaling_method} scaler",
            "columns_scaled": len(columns),
            "scaled_columns": columns,
            "scaler_type": scaling_method,
            "scaled_train_preview": train_preview,
            "scaled_test_preview": test_preview
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
async def list_datasets():
    """List all available datasets"""
    try:
        dataset_list = []
        for dataset_id, data in datasets.items():
            df = data['dataframe']
            dataset_list.append({
                'dataset_id': dataset_id,
                'filename': data.get('filename', 'unknown'),
                'shape': list(df.shape),
                'columns': df.columns.tolist(),
                'preprocessed': data.get('preprocessed', False),
                'uploaded_at': data.get('uploaded_at')
            })
        
        return {
            'datasets': dataset_list,
            'total_datasets': len(datasets),
            'status': 'success'
        }
    except Exception as e:
        return {
            'datasets': [],
            'total_datasets': 0,
            'status': 'error',
            'error': str(e)
        }


    
    
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
        algorithm_name = config['algorithm']
        test_size = config.get('test_size', 0.2)
        scaling_method = config.get('scaling', 'none')
        feature_engineering = config.get('featureEngineering', {})
        validation_method = config.get('validation_method', 'train_test_split')
        cv_folds = config.get('cv_folds', 5)
        hyperparameters = config.get('hyperparameters', {})
        
        print(f"🚀 Starting training with algorithm: {algorithm_name}")
        print(f"📊 Hyperparameters: {hyperparameters}")
    
        # ===== VALIDATE DATASET =====
        if dataset_id not in datasets:
            print(f"❌ [Training] Dataset {dataset_id} not found in memory")
            print(f"   Available datasets: {list(datasets.keys())}")
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': '❌ Dataset not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # Get preprocessed dataframe
        df = datasets[dataset_id]['dataframe'].copy()
        
        # 🔍 ADD THESE LINES TO VERIFY FULL DATASET
        print("="*80)
        print(f"🔍 TRAINING DATA VERIFICATION")
        print(f"Dataset ID: {dataset_id}")
        print(f"Full Dataset Shape: {df.shape}")
        print(f"Total Rows Being Used: {len(df)}")
        print(f"Total Columns: {len(df.columns)}")
        print("="*80)
        
        await websocket.send_text(json.dumps({
            'status': 'started',
            'message': f'🚀 Starting {algorithm_name} training...',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== VALIDATE TARGET COLUMN =====
        if target_column not in df.columns:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'❌ Target column "{target_column}" not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ===== DATA PREPARATION =====
        await websocket.send_text(json.dumps({
            'status': 'preprocessing',
            'message': '🔧 Preparing data for training...',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Handle categorical variables (exclude target)
        categorical_columns = df.select_dtypes(include=['object']).columns
        label_encoders = {}
        
        for col in categorical_columns:
            if col != target_column:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                label_encoders[col] = le
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        print("="*80)
        print(f"🎯 FEATURE PREPARATION VERIFICATION")
        print(f"Features Shape: {X.shape}")
        print(f"Target Shape: {y.shape}")
        print(f"Feature Columns: {list(X.columns)}")
        print("="*80)
        
        # ===== DETECT PROBLEM TYPE =====
        problem_type = detect_problem_type(y)
        
        await websocket.send_text(json.dumps({
            'status': 'analyzing',
            'message': f'🔍 Detected: {problem_type.upper()}',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Encode target if categorical (for classification)
        target_encoder = None
        if problem_type == 'classification' and pd.api.types.is_object_dtype(y):
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y)
            await websocket.send_text(json.dumps({
                'status': 'preprocessing',
                'message': f'🏷️ Encoded {len(target_encoder.classes_)} target classes',
                'timestamp': datetime.now().timestamp()
            }))
        
        # ===== TRAIN/TEST SPLIT =====
        print("="*80)
        print(f"📊 TRAIN/TEST SPLIT VERIFICATION")
        print(f"Test Size: {test_size}")
        print(f"Using Stratification: {problem_type == 'classification' and len(np.unique(y)) > 1}")
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=test_size, 
                random_state=42,
                stratify=y if problem_type == 'classification' and len(np.unique(y)) > 1 else None
            )
            print(f"Train Set Size: {len(X_train)} samples")
            print(f"Test Set Size: {len(X_test)} samples")
            print(f"Features in Train Set: {X_train.shape[1]}")
            print(f"Verification - Total Size: {len(X_train) + len(X_test)} (matches original: {len(X_train) + len(X_test) == len(X)})")
            print("="*80)
        except ValueError as e:
            # Handle case where stratify fails (e.g., too few samples per class)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        await websocket.send_text(json.dumps({
            'status': 'splitting',
            'message': f'🔪 Split: {len(X_train)} train, {len(X_test)} test samples',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== FEATURE SCALING =====
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        scaler = None
        
        if scaling_method != 'none':
            X_train, X_test, scaler = apply_feature_scaling(
                X_train.values, X_test.values, scaling_method, model_id
            )
            await websocket.send_text(json.dumps({
                'status': 'preprocessing',
                'message': f'⚖️ Applied {scaling_method} scaling',
                'timestamp': datetime.now().timestamp()
            }))
        else:
            X_train, X_test = X_train.values, X_test.values
        
        # ===== FEATURE ENGINEERING =====
        transformers = None
        if any(feature_engineering.values()):
            X_train, X_test, transformers = apply_feature_engineering(
                X_train, X_test, feature_engineering, y_train, problem_type, model_id
            )
            
            feature_names = []
            if feature_engineering.get('polynomial'):
                feature_names.append('Polynomial Features')
            if feature_engineering.get('pca'):
                feature_names.append('PCA')
            if feature_engineering.get('featureSelection'):
                feature_names.append('Feature Selection')
            
            await websocket.send_text(json.dumps({
                'status': 'feature_engineering',
                'message': f'🔧 Applied: {", ".join(feature_names)}',
                'timestamp': datetime.now().timestamp()
            }))
        
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
            
        except Exception as e:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'❌ Model initialization failed: {str(e)}',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ===== TRAINING =====
        await websocket.send_text(json.dumps({
            'status': 'training',
            'message': f'🎯 Training {model_class_name}...',
            'timestamp': datetime.now().timestamp()
        }))
        
        try:
            model.fit(X_train, y_train)
            
            await websocket.send_text(json.dumps({
                'status': 'training_complete',
                'message': f'✅ Model trained successfully',
                'timestamp': datetime.now().timestamp()
            }))
            
        except Exception as e:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'❌ Training failed: {str(e)}',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ===== PREDICTIONS & EVALUATION =====
        await websocket.send_text(json.dumps({
            'status': 'evaluating',
            'message': '📊 Evaluating model performance...',
            'timestamp': datetime.now().timestamp()
        }))
        
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        # Calculate metrics based on problem type
        if problem_type == 'classification':
            final_metrics = {
                'train_accuracy': float(accuracy_score(y_train, train_pred)),
                'test_accuracy': float(accuracy_score(y_test, test_pred)),
                'train_f1': float(f1_score(y_train, train_pred, average='weighted')),
                'test_f1': float(f1_score(y_test, test_pred, average='weighted')),
                'problem_type': problem_type,
                'n_classes': int(len(np.unique(y)))
            }
            
            # Add precision and recall
            try:
                final_metrics['train_precision'] = float(precision_score(y_train, train_pred, average='weighted'))
                final_metrics['test_precision'] = float(precision_score(y_test, test_pred, average='weighted'))
                final_metrics['train_recall'] = float(recall_score(y_train, train_pred, average='weighted'))
                final_metrics['test_recall'] = float(recall_score(y_test, test_pred, average='weighted'))
            except:
                pass
            
            main_metric = f"Test Accuracy: {final_metrics['test_accuracy']*100:.2f}%"
            
        else:  # regression
            final_metrics = {
                'train_r2': float(r2_score(y_train, train_pred)),
                'test_r2': float(r2_score(y_test, test_pred)),
                'train_mse': float(mean_squared_error(y_train, train_pred)),
                'test_mse': float(mean_squared_error(y_test, test_pred)),
                'train_rmse': float(np.sqrt(mean_squared_error(y_train, train_pred))),
                'test_rmse': float(np.sqrt(mean_squared_error(y_test, test_pred))),
                'train_mae': float(mean_absolute_error(y_train, train_pred)),
                'test_mae': float(mean_absolute_error(y_test, test_pred)),
                'problem_type': problem_type
            }
            main_metric = f"Test R²: {final_metrics['test_r2']:.4f}"
        
        # ===== SAVE MODEL =====
        model_path = f"models/{model_id}.joblib"
        joblib.dump(model, model_path)
        
        await websocket.send_text(json.dumps({
            'status': 'saving',
            'message': f'💾 Saving model to {model_path}...',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== STORE MODEL INFO =====
        model_info = {
            'model_id': model_id,
            'model_path': model_path,
            'algorithm': algorithm_name,
            'model_class': model_class_name,
            'problem_type': problem_type,
            'target_column': target_column,
            'feature_columns': list(X.columns) if hasattr(X, 'columns') else list(range(X.shape[1])),
            'n_features': int(X_train.shape[1]),
            'n_samples_train': int(len(X_train)),
            'n_samples_test': int(len(X_test)),
            'label_encoders': {k: list(v.classes_) for k, v in label_encoders.items()},
            'target_encoder': list(target_encoder.classes_) if target_encoder else None,
            'scaler_type': scaling_method,
            'feature_engineering': feature_engineering,
            'hyperparameters': hyperparameters,
            'final_metrics': final_metrics,
            'dataset_id': dataset_id,
            'trained_at': datetime.now().isoformat(),
            'test_size': test_size,
            'validation_method': validation_method
        }
        
        trained_models[model_id] = model_info
        
        print(f"✅ Model {model_id} saved successfully")
        print(f"📊 {main_metric}")
        
        # ===== SEND COMPLETION =====
        await websocket.send_text(json.dumps({
            'status': 'completed',
            'model_id': model_id,
            'final_metrics': final_metrics,
            'message': f'🎉 Training completed! {main_metric}',
            'timestamp': datetime.now().timestamp()
        }))
        
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
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DataSage ML Backend...")
    print("✅ Features: Upload, Preprocess (SimpleImputer), Train, Predict")
    uvicorn.run(app, host="127.0.0.1", port=8000)
