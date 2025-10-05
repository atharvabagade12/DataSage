"""
DataSage ML Backend - Complete Production-Ready Version
Advanced Features: Feature Scaling, Engineering, Cross-Validation, Stratified Validation
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
from datetime import datetime
from typing import Dict, Any, Optional
import tempfile
import auth 

# ===== SKLEARN IMPORTS =====
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor

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


UPLOAD_DIR = "enterprise_datasets"
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB limit
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== FASTAPI APP INITIALIZATION =====
app = FastAPI(
    title="DataSage ML Backend - Advanced Edition",
    version="2.0.0",
    description="Production-ready ML backend with feature scaling, engineering, and advanced validation"
)

# ===== CORS CONFIGURATION =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ IMPORT AND INCLUDE AUTH ROUTER
try:
    # If auth.py is in backend/ folder (same level as main.py)
    import auth
    app.include_router(auth.router)
    print("✅ Auth router loaded from backend/auth.py")
except ImportError:
    try:
        # If auth.py is in backend/routers/ folder
        from routers import auth
        app.include_router(auth.router)
        print("✅ Auth router loaded from backend/routers/auth.py")
    except ImportError as e:
        print(f"⚠️ Auth router not available: {e}")
        print("   Create auth.py in backend/ folder")
    

# ===== GLOBAL STORAGE =====
datasets: Dict[str, pd.DataFrame] = {}
trained_models: Dict[str, Dict[str, Any]] = {}
scalers: Dict[str, Any] = {}

app.include_router(auth.router)

# ===== ALGORITHM MAPPING =====
CLASSIFICATION_ALGORITHMS = {
    'Random Forest': RandomForestClassifier,
    'Logistic Regression': LogisticRegression,
    'Decision Tree': DecisionTreeClassifier,
    'XGBoost': xgb.XGBClassifier,
    'Support Vector Machine': SVC,
    'K-Nearest Neighbors': KNeighborsClassifier,
    'Neural Network (MLP)': MLPClassifier
}

REGRESSION_ALGORITHMS = {
    'Random Forest Regressor': RandomForestRegressor,
    'Linear Regression': LinearRegression,
    'Decision Tree Regressor': DecisionTreeRegressor,
    'XGBoost Regressor': xgb.XGBRegressor,
    'Support Vector Regressor (SVR)': SVR,
    'K-Nearest Neighbors Regressor': KNeighborsRegressor,
    'Neural Network Regressor (MLP)': MLPRegressor
}

ALGORITHMS = {**CLASSIFICATION_ALGORITHMS, **REGRESSION_ALGORITHMS}

# ===== UTILITY FUNCTIONS =====
def detect_problem_type(y: pd.Series) -> str:
    """Automatically detect if it's classification or regression"""
    unique_values = len(np.unique(y))
    total_values = len(y)
    
    # If target is string/object, it's classification
    if pd.api.types.is_string_dtype(y) or pd.api.types.is_object_dtype(y):
        return 'classification'
    
    # If less than 20 unique values and they're integers, likely classification
    if unique_values < 20 and pd.api.types.is_integer_dtype(y):
        return 'classification'
    
    # If unique values are more than 50% of total, it's regression
    if unique_values / total_values > 0.5:
        return 'regression'
    
    # Default to classification for discrete values
    return 'classification' if unique_values < 50 else 'regression'

def get_algorithm_for_problem_type(algorithm_name: str, problem_type: str):
    """Get the correct algorithm based on problem type"""
    
    # If algorithm name already specifies type, use it directly
    if algorithm_name in ALGORITHMS:
        return ALGORITHMS[algorithm_name]
    
    # Map generic names to specific algorithms
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
        }
    }
    
    if algorithm_name in algorithm_mapping:
        return algorithm_mapping[algorithm_name][problem_type]
    
    # Fallback
    return RandomForestClassifier if problem_type == 'classification' else RandomForestRegressor

def apply_feature_scaling(X_train: np.ndarray, X_test: np.ndarray, scaling_method: str, model_id: str):
    """Apply feature scaling and store scaler for later use"""
    scaler = None
    
    if scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        return X_train, X_test, None
    
    # Fit and transform
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Store scaler for predictions
    scalers[model_id] = scaler
    
    return X_train_scaled, X_test_scaled, scaler

def apply_feature_engineering(X_train: np.ndarray, X_test: np.ndarray, 
                            feature_engineering: Dict[str, bool], y_train: np.ndarray, 
                            problem_type: str, model_id: str):
    """Apply feature engineering techniques"""
    transformers = {}
    
    # Polynomial Features
    if feature_engineering.get('polynomial', False):
        poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
        X_train = poly.fit_transform(X_train)
        X_test = poly.transform(X_test)
        transformers['polynomial'] = poly
    
    # PCA
    if feature_engineering.get('pca', False):
        # Keep 95% of variance
        pca = PCA(n_components=0.95)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        transformers['pca'] = pca
    
    # Feature Selection
    if feature_engineering.get('featureSelection', False):
        score_func = f_classif if problem_type == 'classification' else f_regression
        k = min(20, X_train.shape[1])  # Select top features, but not more than available
        selector = SelectKBest(score_func=score_func, k=k)
        X_train = selector.fit_transform(X_train, y_train)
        X_test = selector.transform(X_test)
        transformers['feature_selector'] = selector
    
    # Store transformers for predictions
    if transformers:
        scalers[f"{model_id}_transformers"] = transformers
    
    return X_train, X_test, transformers

# ===== API ENDPOINTS =====

@app.get("/api/health")
async def health_check():
    """Enhanced health check with detailed status"""
    try:
        import sklearn
        
        return {
            "status": "healthy",
            "message": "DataSage Advanced ML Backend Running",
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
                "data_processing": "pandas + numpy",
                "model_persistence": "joblib",
                "cors_enabled": True,
                "websocket_support": True
            },
            "stats": {
                "datasets_loaded": len(datasets),
                "trained_models": len(trained_models),
                "active_scalers": len(scalers),
                "available_datasets": list(datasets.keys())
            },
            "endpoints": {
                "upload": "/api/upload-dataset",
                "datasets": "/api/datasets",
                "training": "/ws/train-model",
                "prediction": "/api/predict/{model_id}"
            },
            "timestamp": datetime.now().isoformat(),
            "server_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and analyze CSV dataset with bulletproof error handling"""
    try:
        print(f"📤 Receiving file upload: {file.filename}")
        
        # Read CSV with pandas
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        print(f"✅ CSV parsed successfully: {df.shape}")
        
        # Generate dataset ID
        dataset_id = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store dataset
        datasets[dataset_id] = df
        print(f"✅ Dataset {dataset_id} stored successfully")
        
        # ✅ BULLETPROOF RESPONSE CONSTRUCTION
        try:
            # Safe sample data (limit to 200 rows, handle NaN values)
            sample_size = min(200, len(df))
            sample_df = df.head(sample_size).fillna('')  # Replace NaN with empty string
            sample_data = []
            
            for _, row in sample_df.iterrows():
                row_dict = {}
                for col in df.columns:
                    value = row[col]
                    # Convert numpy types to Python types
                    if pd.isna(value):
                        row_dict[str(col)] = None
                    elif isinstance(value, (np.integer, np.int64, np.int32)):
                        row_dict[str(col)] = int(value)
                    elif isinstance(value, (np.floating, np.float64, np.float32)):
                        row_dict[str(col)] = float(value)
                    else:
                        row_dict[str(col)] = str(value)
                sample_data.append(row_dict)
            
            # Safe statistics
            statistics = {}
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                try:
                    stats_df = df[numeric_cols].describe()
                    for col in numeric_cols:
                        col_stats = {}
                        for stat in stats_df.index:
                            val = stats_df.loc[stat, col]
                            col_stats[str(stat)] = float(val) if pd.notna(val) else 0.0
                        statistics[str(col)] = col_stats
                except:
                    statistics = {}
            
            # Construct safe response
            response_data = {
                'dataset_id': str(dataset_id),
                'filename': str(file.filename) if file.filename else 'unknown.csv',
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': [str(col) for col in df.columns.tolist()],
                'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
                'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
                'sample_data': sample_data,
                'statistics': statistics,
                'upload_time': datetime.now().isoformat(),
                'success': True,
                'total_rows': int(df.shape[0]),
                'total_columns': int(df.shape[1]),
                'is_large_dataset': bool(df.shape[0] > 10000 or df.shape[1] > 50)
            }
            
            print(f"✅ Response prepared for {dataset_id}")
            return response_data
            
        except Exception as response_error:
            print(f"❌ Error preparing response: {str(response_error)}")
            # Minimal safe response
            return {
                'dataset_id': str(dataset_id),
                'filename': str(file.filename) if file.filename else 'unknown.csv',
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': [str(col) for col in df.columns],
                'total_rows': int(df.shape[0]),
                'total_columns': int(df.shape[1]),
                'success': True,
                'upload_time': datetime.now().isoformat(),
                'sample_data': [],
                'statistics': {},
                'dtypes': {},
                'missing_values': {},
                'is_large_dataset': bool(df.shape[0] > 10000)
            }
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


    
    
@app.post("/api/upload-large-dataset")
async def upload_large_dataset(file: UploadFile = File(...)):
    """Upload large datasets (up to 1GB) with streaming"""
    try:
        print(f"📤 Receiving large file upload: {file.filename}")
        
        # Stream file in chunks to avoid memory issues
        file_size = 0
        temp_content = []
        
        while True:
            chunk = await file.read(CHUNK_SIZE)
            if not chunk:
                break
            
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB")
            
            temp_content.append(chunk)
        
        # Process large CSV
        full_content = b''.join(temp_content)
        df = pd.read_csv(io.StringIO(full_content.decode('utf-8')))
        
        # Generate unique dataset ID
        dataset_id = f"large_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        datasets[dataset_id] = df
        
        # Save to disk for persistence
        file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}.parquet")
        df.to_parquet(file_path, compression='snappy')
        
        # Return analysis with sample data only
        return {
            'dataset_id': dataset_id,
            'filename': file.filename,
            'shape': list(df.shape),
            'columns': df.columns.tolist(),
            'sample_data': df.head(200).to_dict('records'),  # Only 200 rows
            'is_large_dataset': df.shape[0] > 10000,
            'total_rows': int(df.shape[0]),
            'file_size_mb': round(file_size / (1024*1024), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Large file processing error: {str(e)}")

@app.get("/api/datasets/{dataset_id}/page")
async def get_dataset_page(
    dataset_id: str, 
    page: int = 1, 
    page_size: int = 200
):
    """Get paginated data from datasets for UI preview"""
    try:
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        df = datasets[dataset_id]
        
        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get page data
        page_data = df.iloc[start_idx:end_idx]
        
        # Convert to safe dict format
        safe_data = []
        for _, row in page_data.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                # Convert to safe types
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64, np.float32)):
                    row_dict[str(col)] = float(value)
                else:
                    row_dict[str(col)] = str(value)
            safe_data.append(row_dict)
        
        return {
            'data': safe_data,
            'page': page,
            'page_size': page_size,
            'total_rows': int(len(df)),
            'total_pages': int((len(df) + page_size - 1) // page_size),
            'has_next': end_idx < len(df),
            'has_prev': page > 1,
            'dataset_id': dataset_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Pagination error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get page: {str(e)}")


@app.get("/api/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get dataset information without loading data"""
    try:
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        df = datasets[dataset_id]
        
        return {
            'dataset_id': dataset_id,
            'shape': [int(df.shape[0]), int(df.shape[1])],
            'columns': [str(col) for col in df.columns.tolist()],
            'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            'success': True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Dataset info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get dataset info: {str(e)}")


@app.get("/api/datasets")
async def list_datasets():
    """List all available datasets"""
    try:
        dataset_list = []
        for dataset_id, df in datasets.items():
            dataset_list.append({
                'dataset_id': dataset_id,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'upload_time': datetime.now().isoformat()
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

@app.get("/api/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get specific dataset information"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    
    df = datasets[dataset_id]
    return {
        'dataset_id': dataset_id,
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'sample_data': df.head(5).to_dict('records'),
        'statistics': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
        'status': 'success'
    }

@app.websocket("/ws/train-model")
async def train_model_websocket(websocket: WebSocket):
    """Advanced ML training with feature scaling, engineering, and validation"""
    await websocket.accept()
    
    try:
        # Receive configuration
        config_data = await websocket.receive_text()
        config = json.loads(config_data)
        
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
        
        print(f"🚀 Starting advanced training with config: {config}")
        
        # Validate dataset
        if dataset_id not in datasets:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': 'Dataset not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        df = datasets[dataset_id].copy()
        
        await websocket.send_text(json.dumps({
            'status': 'started',
            'message': f'🚀 Starting ADVANCED {algorithm_name} training with sklearn...',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Validate target column
        if target_column not in df.columns:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': f'Target column {target_column} not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ===== DATA PREPARATION =====
        await websocket.send_text(json.dumps({
            'status': 'preprocessing',
            'message': '🔧 Starting data preprocessing...',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Handle categorical variables
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
        
        # Detect problem type
        problem_type = detect_problem_type(y)
        
        await websocket.send_text(json.dumps({
            'status': 'analyzing',
            'message': f'🔍 Detected problem type: {problem_type.upper()}',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Encode target if categorical
        target_encoder = None
        if problem_type == 'classification' and pd.api.types.is_object_dtype(y):
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y)
        
        # ===== FEATURE SCALING AND ENGINEERING =====
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Split data first
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, 
            random_state=42,
            stratify=y if problem_type == 'classification' and len(np.unique(y)) > 1 else None
        )
        
        await websocket.send_text(json.dumps({
            'status': 'splitting',
            'message': f'🔪 Data split: {len(X_train)} train, {len(X_test)} test samples',
            'timestamp': datetime.now().timestamp()
        }))
        
        # Apply feature scaling
        if scaling_method != 'none':
            X_train, X_test, scaler = apply_feature_scaling(
                X_train.values, X_test.values, scaling_method, model_id
            )
            await websocket.send_text(json.dumps({
                'status': 'preprocessing',
                'message': f'🔧 Applied {scaling_method} scaling',
                'timestamp': datetime.now().timestamp()
            }))
        else:
            X_train, X_test = X_train.values, X_test.values
            scaler = None
        
        # Apply feature engineering
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
        
        # ===== MODEL INITIALIZATION =====
        model_class = get_algorithm_for_problem_type(algorithm_name, problem_type)
        
        # Apply hyperparameters
        model_params = {'random_state': 42}
        if hyperparameters:
            model_params.update(hyperparameters)
        
        try:
            model = model_class(**model_params)
        except:
            model = model_class()
        
        await websocket.send_text(json.dumps({
            'status': 'model_init',
            'message': f'🤖 Initialized {model_class.__name__} for {problem_type}',
            'timestamp': datetime.now().timestamp()
        }))
        
        # ===== ADVANCED VALIDATION =====
        final_metrics = {}
        
        if validation_method == 'cross_validation':
            await websocket.send_text(json.dumps({
                'status': 'validation',
                'message': f'🔄 Starting {cv_folds}-fold cross validation...',
                'timestamp': datetime.now().timestamp()
            }))
            
            # Combine for CV
            X_full = np.vstack([X_train, X_test])
            y_full = np.hstack([y_train, y_test])
            
            scoring = 'accuracy' if problem_type == 'classification' else 'r2'
            cv_scores = cross_val_score(model, X_full, y_full, cv=cv_folds, scoring=scoring)
            
            # Also train final model
            model.fit(X_train, y_train)
            final_pred = model.predict(X_test)
            
            if problem_type == 'classification':
                test_accuracy = accuracy_score(y_test, final_pred)
                final_metrics = {
                    'cv_mean': float(cv_scores.mean()),
                    'cv_std': float(cv_scores.std()),
                    'cv_scores': cv_scores.tolist(),
                    'test_accuracy': float(test_accuracy),
                    'test_f1': float(f1_score(y_test, final_pred, average='weighted')),
                    'validation_method': 'cross_validation',
                    'cv_folds': cv_folds,
                    'problem_type': problem_type
                }
                main_metric = f"CV Accuracy: {cv_scores.mean()*100:.1f}% (±{cv_scores.std()*100:.1f}%)"
            else:
                test_r2 = r2_score(y_test, final_pred)
                final_metrics = {
                    'cv_mean': float(cv_scores.mean()),
                    'cv_std': float(cv_scores.std()),
                    'cv_scores': cv_scores.tolist(),
                    'test_r2': float(test_r2),
                    'test_mse': float(mean_squared_error(y_test, final_pred)),
                    'validation_method': 'cross_validation',
                    'cv_folds': cv_folds,
                    'problem_type': problem_type
                }
                main_metric = f"CV R²: {cv_scores.mean()*100:.1f}% (±{cv_scores.std()*100:.1f}%)"
                
        elif validation_method == 'stratified' and problem_type == 'classification':
            await websocket.send_text(json.dumps({
                'status': 'validation',
                'message': f'🎯 Starting stratified {cv_folds}-fold validation...',
                'timestamp': datetime.now().timestamp()
            }))
            
            X_full = np.vstack([X_train, X_test])
            y_full = np.hstack([y_train, y_test])
            
            skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
            cv_scores = cross_val_score(model, X_full, y_full, cv=skf, scoring='accuracy')
            
            # Train final model
            model.fit(X_train, y_train)
            final_pred = model.predict(X_test)
            
            final_metrics = {
                'cv_mean': float(cv_scores.mean()),
                'cv_std': float(cv_scores.std()),
                'cv_scores': cv_scores.tolist(),
                'test_accuracy': float(accuracy_score(y_test, final_pred)),
                'test_f1': float(f1_score(y_test, final_pred, average='weighted')),
                'validation_method': 'stratified',
                'cv_folds': cv_folds,
                'problem_type': problem_type
            }
            main_metric = f"Stratified Accuracy: {cv_scores.mean()*100:.1f}% (±{cv_scores.std()*100:.1f}%)"
            
        else:
            # Standard train/test split
            await websocket.send_text(json.dumps({
                'status': 'training',
                'message': f'🎯 Training {model_class.__name__}...',
                'timestamp': datetime.now().timestamp()
            }))
            
            model.fit(X_train, y_train)
            
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            if problem_type == 'classification':
                final_metrics = {
                    'train_accuracy': float(accuracy_score(y_train, train_pred)),
                    'test_accuracy': float(accuracy_score(y_test, test_pred)),
                    'train_f1': float(f1_score(y_train, train_pred, average='weighted')),
                    'test_f1': float(f1_score(y_test, test_pred, average='weighted')),
                    'train_precision': float(precision_score(y_train, train_pred, average='weighted')),
                    'test_precision': float(precision_score(y_test, test_pred, average='weighted')),
                    'validation_method': 'train_test_split',
                    'problem_type': problem_type
                }
                main_metric = f"Test Accuracy: {final_metrics['test_accuracy']*100:.1f}%"
            else:
                final_metrics = {
                    'train_r2': float(r2_score(y_train, train_pred)),
                    'test_r2': float(r2_score(y_test, test_pred)),
                    'train_mse': float(mean_squared_error(y_train, train_pred)),
                    'test_mse': float(mean_squared_error(y_test, test_pred)),
                    'train_mae': float(mean_absolute_error(y_train, train_pred)),
                    'test_mae': float(mean_absolute_error(y_test, test_pred)),
                    'validation_method': 'train_test_split',
                    'problem_type': problem_type
                }
                main_metric = f"Test R²: {final_metrics['test_r2']*100:.1f}%"
        
        # ===== SAVE MODEL =====
        model_path = f"models/{model_id}.joblib"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, model_path)
        
        # Store model info
        model_info = {
            'model_id': model_id,
            'model_path': model_path,
            'algorithm': algorithm_name,
            'model_class': model_class.__name__,
            'problem_type': problem_type,
            'target_column': target_column,
            'feature_columns': list(X.columns) if hasattr(X, 'columns') else list(range(X.shape[1])),
            'label_encoders': {k: list(v.classes_) for k, v in label_encoders.items()},
            'target_encoder': list(target_encoder.classes_) if target_encoder else None,
            'scaler_type': scaling_method,
            'feature_engineering': feature_engineering,
            'validation_method': validation_method,
            'final_metrics': final_metrics,
            'hyperparameters': model_params,
            'dataset_shape': df.shape,
            'trained_at': datetime.now().isoformat()
        }
        
        trained_models[model_id] = model_info
        
        # Send completion message
        final_message = f'🎉 ADVANCED {model_class.__name__} training completed! {main_metric}'
        
        await websocket.send_text(json.dumps({
            'status': 'completed',
            'model_id': model_id,
            'final_metrics': final_metrics,
            'message': final_message,
            'timestamp': datetime.now().timestamp()
        }))
        
    except Exception as e:
        print(f"❌ Training error: {str(e)}")
        await websocket.send_text(json.dumps({
            'status': 'failed',
            'message': f'❌ Training failed: {str(e)}',
            'timestamp': datetime.now().timestamp()
        }))

@app.get("/api/models/{model_id}")
async def get_model_info(model_id: str):
    """Get detailed model information"""
    if model_id not in trained_models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return trained_models[model_id]

@app.post("/api/predict/{model_id}")
async def make_prediction(model_id: str, data: dict):
    """Make predictions with preprocessing pipeline"""
    if model_id not in trained_models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        model_info = trained_models[model_id]
        
        # Load model
        model = joblib.load(model_info['model_path'])
        
        # Prepare input data
        input_df = pd.DataFrame([data])
        
        # Apply same preprocessing as training
        for col, encoder_classes in model_info['label_encoders'].items():
            if col in input_df.columns:
                encoder = LabelEncoder()
                encoder.classes_ = np.array(encoder_classes)
                input_df[col] = encoder.transform(input_df[col])
        
        # Convert to numpy
        X_input = input_df.values
        
        # Apply scaling if used
        if model_id in scalers:
            scaler = scalers[model_id]
            X_input = scaler.transform(X_input)
        
        # Apply feature engineering if used
        if f"{model_id}_transformers" in scalers:
            transformers = scalers[f"{model_id}_transformers"]
            if 'polynomial' in transformers:
                X_input = transformers['polynomial'].transform(X_input)
            if 'pca' in transformers:
                X_input = transformers['pca'].transform(X_input)
            if 'feature_selector' in transformers:
                X_input = transformers['feature_selector'].transform(X_input)
        
        # Make prediction
        prediction = model.predict(X_input)
        
        # Get probabilities if available
        probabilities = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X_input).tolist()
        
        # Decode prediction if target was encoded
        if model_info['target_encoder']:
            target_encoder = LabelEncoder()
            target_encoder.classes_ = np.array(model_info['target_encoder'])
            prediction = target_encoder.inverse_transform(prediction)
        
        return {
            'model_id': model_id,
            'prediction': prediction.tolist(),
            'probabilities': probabilities,
            'preprocessing_applied': {
                'scaling': model_info.get('scaler_type', 'none'),
                'feature_engineering': model_info.get('feature_engineering', {}),
                'label_encoding': len(model_info['label_encoders']) > 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# ===== DEMO DATA =====
def create_demo_dataset():
    """Create demo datasets for testing"""
    np.random.seed(42)
    
    # Classification dataset (Iris-like)
    n_samples = 1000
    
    sepal_length = np.random.normal(5.8, 0.8, n_samples)
    sepal_width = np.random.normal(3.1, 0.4, n_samples)
    petal_length = np.random.normal(3.7, 1.8, n_samples)
    petal_width = np.random.normal(1.2, 0.8, n_samples)
    
    target = []
    for i in range(n_samples):
        if petal_length[i] < 2.5:
            target.append('setosa')
        elif petal_width[i] < 1.7:
            target.append('versicolor')
        else:
            target.append('virginica')
    
    df_demo = pd.DataFrame({
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width,
        'species': target
    })
    
    datasets['demo_dataset'] = df_demo
    print("✅ Demo classification dataset created")

@app.on_event("startup")
async def startup_event():
    """Initialize demo data on startup"""
    create_demo_dataset()
    print("🚀 DataSage Advanced ML Backend initialized")

# ===== DEBUG ENDPOINT =====
@app.get("/api/debug")
async def debug_info():
    """Debug information"""
    return {
        "datasets_in_memory": len(datasets),
        "dataset_ids": list(datasets.keys()),
        "trained_models": len(trained_models),
        "active_scalers": len(scalers),
        "model_details": {
            model_id: {
                "algorithm": info.get('algorithm'),
                "problem_type": info.get('problem_type'),
                "validation_method": info.get('validation_method'),
                "scaling": info.get('scaler_type', 'none'),
                "feature_engineering": info.get('feature_engineering', {})
            }
            for model_id, info in trained_models.items()
        }
    }

# ===== RUN SERVER =====
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DataSage Advanced ML Backend...")
    print("📊 Features: Training, Scaling, Engineering, Cross-Validation, Stratified Validation")
    print("🎯 All ML libraries loaded successfully!")
    uvicorn.run(app, host="127.0.0.1", port=8000)
