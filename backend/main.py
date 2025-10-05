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
        "http://localhost:3001"
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
        }
    }
    
    if algorithm_name in algorithm_mapping:
        return algorithm_mapping[algorithm_name][problem_type]
    
    return RandomForestClassifier if problem_type == 'classification' else RandomForestRegressor

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
        
        # Generate dataset ID
        dataset_id = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # ✅ STORE DATASET IN MEMORY
        datasets[dataset_id] = {
            'dataframe': df.copy(),
            'filename': file.filename,
            'uploaded_at': datetime.now().isoformat(),
            'preprocessed': False,
            'original_shape': df.shape
        }
        
        print(f"✅ Dataset {dataset_id} stored in memory")
        
        # ✅ PREPARE SAMPLE DATA (CRITICAL!)
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
        
        print(f"✅ Sample data prepared: {len(sample_data)} rows")
        
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
            'sample_data': sample_data,  # ← MUST BE HERE
            'statistics': statistics,
            'upload_time': datetime.now().isoformat(),
            'success': True,
            'total_rows': int(df.shape[0]),
            'total_columns': int(df.shape[1])
        }
        
        print(f"✅ Returning upload response:")
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
        
        # ✅ PREPARE SAMPLE DATA (CRITICAL!)
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
            'columns': [str(col) for col in df.columns.tolist()],
            'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
            'preprocessed': data.get('preprocessed', False),
            'uploaded_at': data.get('uploaded_at'),
            'sample_data': sample_data,  
            'status': 'success'
        }
        
        print(f"✅ Returning response with {len(sample_data)} sample rows")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in get_dataset_info: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching dataset: {str(e)}")



@app.post("/api/preprocess")
async def preprocess_data(request: dict):
    """
    Preprocess dataset using scikit-learn SimpleImputer
    """
    try:
        dataset_id = request.get('dataset_id')
        
        # ✅ GET DATASET FROM SINGLE STORAGE
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = datasets[dataset_id]['dataframe'].copy()
        
        # Initialize preprocessor
        preprocessor = DataPreprocessor(df)
        
        # ✅ JUST GET MISSING INFO (for frontend display)
        if request.get('get_missing_info'):
            return {
                "missing_info": preprocessor.get_missing_info(),
                "column_types": preprocessor.column_types
            }
        
        # ✅ APPLY PREPROCESSING STEPS
        
        # 1. Remove columns (FIRST!)
        if 'remove_columns' in request:
            preprocessor.remove_columns(request['remove_columns'])
        
        # 2. Handle missing values
        if 'missing_values' in request:
            preprocessor.handle_missing_values(request['missing_values'])
        
        # 3. Remove duplicates
        if 'remove_duplicates' in request:
            preprocessor.remove_duplicates(request['remove_duplicates'])
        
        # 4. Handle outliers
        if 'outliers' in request:
            outlier_config = request['outliers']
            preprocessor.handle_outliers(
                columns=outlier_config.get('columns', []),
                method=outlier_config.get('method', 'iqr'),
                strategy=outlier_config.get('strategy', 'cap')
            )
        
        # 5. Encode categorical (LAST!)
        if 'encoding' in request:
            encoding_config = request['encoding']
            preprocessor.encode_categorical(
                columns=encoding_config.get('columns', []),
                method=encoding_config.get('method', 'label')
            )
        
        
        processed_df = preprocessor.get_processed_dataframe()
        
        
        datasets[dataset_id]['dataframe'] = processed_df
        datasets[dataset_id]['preprocessed'] = True
        datasets[dataset_id]['preprocessing_log'] = preprocessor.preprocessing_log
        
        print(f"✅ Dataset {dataset_id} updated after preprocessing")
        print(f"   Original shape: {df.shape} -> New shape: {processed_df.shape}")
        
        # Get summary
        summary = preprocessor.get_preprocessing_summary()
        
        # Prepare preview
        preview_data = []
        sample_size = min(200, len(processed_df))
        for _, row in processed_df.head(sample_size).iterrows():
            row_dict = {}
            for col in processed_df.columns:
                value = row[col]
                if pd.isna(value):
                    row_dict[str(col)] = None
                elif isinstance(value, (np.integer, np.int64, np.int32)):
                    row_dict[str(col)] = int(value)
                elif isinstance(value, (np.floating, np.float64, np.float32)):
                    row_dict[str(col)] = float(value)
                else:
                    row_dict[str(col)] = str(value)
            preview_data.append(row_dict)
        
        return {
            "success": True,
            "message": "Preprocessing completed successfully",
            "summary": summary,
            "shape": list(processed_df.shape),
            "preview": preview_data,
            "dataset_id": dataset_id
        }
        
    except Exception as e:
        print(f"❌ Preprocessing error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/api/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get specific dataset information"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    
    data = datasets[dataset_id]
    df = data['dataframe']
    
    return {
        'dataset_id': dataset_id,
        'filename': data.get('filename'),
        'shape': list(df.shape),
        'columns': df.columns.tolist(),
        'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': {str(col): int(df[col].isnull().sum()) for col in df.columns},
        'preprocessed': data.get('preprocessed', False),
        'uploaded_at': data.get('uploaded_at'),
        'status': 'success'
    }

@app.websocket("/ws/train-model")
async def train_model_websocket(websocket: WebSocket):
    """Advanced ML training with feature scaling and engineering"""
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
        
        print(f"🚀 Starting training with config: {config}")
        
        # ✅ GET DATASET FROM SINGLE STORAGE
        if dataset_id not in datasets:
            await websocket.send_text(json.dumps({
                'status': 'failed',
                'message': 'Dataset not found',
                'timestamp': datetime.now().timestamp()
            }))
            return
        
        # ✅ USE PREPROCESSED DATAFRAME
        df = datasets[dataset_id]['dataframe'].copy()
        
        await websocket.send_text(json.dumps({
            'status': 'started',
            'message': f'🚀 Starting {algorithm_name} training with sklearn...',
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
            'message': '🔧 Preparing data for training...',
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
        
        # Split data
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
        
        # ===== TRAINING =====
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
                'problem_type': problem_type
            }
            main_metric = f"Test Accuracy: {final_metrics['test_accuracy']*100:.1f}%"
        else:
            final_metrics = {
                'train_r2': float(r2_score(y_train, train_pred)),
                'test_r2': float(r2_score(y_test, test_pred)),
                'train_mse': float(mean_squared_error(y_train, train_pred)),
                'test_mse': float(mean_squared_error(y_test, test_pred)),
                'problem_type': problem_type
            }
            main_metric = f"Test R²: {final_metrics['test_r2']*100:.1f}%"
        
        # ===== SAVE MODEL =====
        model_path = f"models/{model_id}.joblib"
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
            'final_metrics': final_metrics,
            'dataset_id': dataset_id,
            'trained_at': datetime.now().isoformat()
        }
        
        trained_models[model_id] = model_info
        
        # Send completion
        await websocket.send_text(json.dumps({
            'status': 'completed',
            'model_id': model_id,
            'final_metrics': final_metrics,
            'message': f'🎉 {model_class.__name__} training completed! {main_metric}',
            'timestamp': datetime.now().timestamp()
        }))
        
    except Exception as e:
        print(f"❌ Training error: {str(e)}")
        traceback.print_exc()
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
