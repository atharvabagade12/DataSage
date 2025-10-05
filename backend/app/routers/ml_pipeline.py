from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import json
from pathlib import Path
import tempfile
import os

router = APIRouter(prefix="/ml", tags=["Machine Learning Pipeline"])

# In-memory storage for demo (use Redis or database in production)
user_sessions = {}

@router.post("/upload-dataset")
async def upload_dataset(
    file: UploadFile = File(...),
    session_id: Optional[str] = None
):
    """Upload and analyze dataset"""
    try:
        # Validate file type
        allowed_extensions = ['.csv', '.xlsx', '.xls', '.json']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {allowed_extensions}"
            )
        
        # Read file content
        content = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Load dataset based on file type
            if file_extension == '.csv':
                df = pd.read_csv(tmp_file_path)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(tmp_file_path)
            elif file_extension == '.json':
                df = pd.read_json(tmp_file_path)
            
            # Generate session ID if not provided
            if not session_id:
                import uuid
                session_id = f"ds_{uuid.uuid4().hex[:12]}"
            
            # Analyze dataset
            analysis = analyze_dataset(df)
            
            # Store in session (use proper storage in production)
            user_sessions[session_id] = {
                'original_data': df,
                'current_data': df.copy(),
                'analysis': analysis,
                'filename': file.filename,
                'preprocessing_steps': []
            }
            
            return {
                "success": True,
                "message": "Dataset uploaded successfully",
                "sessionId": session_id,
                "filename": file.filename,
                "shape": {"rows": len(df), "columns": len(df.columns)},
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "analysis": analysis,
                "preview": df.head().to_dict('records')
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")

@router.get("/dataset-info/{session_id}")
async def get_dataset_info(session_id: str):
    """Get dataset information"""
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = user_sessions[session_id]
    df = session_data['current_data']
    
    return {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "analysis": session_data['analysis'],
        "preview": df.head().to_dict('records'),
        "preprocessing_steps": session_data['preprocessing_steps']
    }

@router.post("/detect-problem-type")
async def detect_problem_type(request: Dict[str, Any]):
    """Detect if problem is classification or regression"""
    session_id = request.get('sessionId')
    target_column = request.get('targetColumn')
    
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    df = user_sessions[session_id]['current_data']
    
    if target_column not in df.columns:
        raise HTTPException(status_code=400, detail="Target column not found")
    
    # Analyze target column
    target_series = df[target_column]
    target_type = str(target_series.dtype)
    unique_values = target_series.nunique()
    total_values = len(target_series)
    unique_ratio = unique_values / total_values
    
    # Problem type detection logic
    if target_type in ['object', 'category', 'bool']:
        problem_type = 'classification'
    elif target_type in ['int64', 'int32', 'float64', 'float32']:
        if unique_ratio < 0.05 or unique_values <= 20:
            problem_type = 'classification'
        else:
            problem_type = 'regression'
    else:
        problem_type = 'regression'  # Default
    
    return {
        "problemType": problem_type,
        "targetType": target_type,
        "uniqueValues": unique_values,
        "uniqueRatio": unique_ratio,
        "reasoning": get_problem_type_reasoning(problem_type, target_type, unique_values, unique_ratio)
    }

@router.post("/preprocess-data")
async def preprocess_data(request: Dict[str, Any]):
    """Apply preprocessing steps to dataset"""
    session_id = request.get('sessionId')
    config = request.get('config', {})
    
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get current data
    df = user_sessions[session_id]['current_data'].copy()
    preprocessing_steps = []
    
    try:
        # Handle missing values
        missing_config = config.get('missingValueStrategy', {})
        for column, strategy in missing_config.items():
            if column in df.columns and df[column].isnull().any():
                if strategy == 'drop':
                    df = df.dropna(subset=[column])
                    preprocessing_steps.append(f"Dropped rows with missing {column}")
                elif strategy == 'mean' and df[column].dtype in ['float64', 'int64']:
                    df[column].fillna(df[column].mean(), inplace=True)
                    preprocessing_steps.append(f"Filled {column} missing values with mean")
                elif strategy == 'median' and df[column].dtype in ['float64', 'int64']:
                    df[column].fillna(df[column].median(), inplace=True)
                    preprocessing_steps.append(f"Filled {column} missing values with median")
                elif strategy == 'mode':
                    df[column].fillna(df[column].mode()[0], inplace=True)
                    preprocessing_steps.append(f"Filled {column} missing values with mode")
        
        # Handle duplicates
        if config.get('duplicateHandling') == 'remove_all':
            initial_len = len(df)
            df = df.drop_duplicates()
            removed = initial_len - len(df)
            if removed > 0:
                preprocessing_steps.append(f"Removed {removed} duplicate rows")
        
        # Categorical encoding
        encoding_config = config.get('categoricalEncoding', {})
        for column, encoding_type in encoding_config.items():
            if column in df.columns and df[column].dtype == 'object':
                if encoding_type == 'onehot':
                    # One-hot encoding
                    dummies = pd.get_dummies(df[column], prefix=column)
                    df = pd.concat([df, dummies], axis=1)
                    df.drop(column, axis=1, inplace=True)
                    preprocessing_steps.append(f"Applied one-hot encoding to {column}")
                elif encoding_type == 'label':
                    # Label encoding
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    df[column] = le.fit_transform(df[column].astype(str))
                    preprocessing_steps.append(f"Applied label encoding to {column}")
        
        # Update session data
        user_sessions[session_id]['current_data'] = df
        user_sessions[session_id]['preprocessing_steps'].extend(preprocessing_steps)
        user_sessions[session_id]['analysis'] = analyze_dataset(df)
        
        return {
            "success": True,
            "message": "Preprocessing completed",
            "steps": preprocessing_steps,
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "analysis": analyze_dataset(df),
            "preview": df.head().to_dict('records')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")

# Helper functions
def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze dataset and return statistics"""
    try:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        analysis = {
            "basic_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "numeric_columns": len(numeric_columns),
                "categorical_columns": len(categorical_columns)
            },
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        # Add statistics for numeric columns
        if numeric_columns:
            analysis["numeric_stats"] = df[numeric_columns].describe().to_dict()
        
        # Add info for categorical columns
        if categorical_columns:
            analysis["categorical_info"] = {}
            for col in categorical_columns:
                analysis["categorical_info"][col] = {
                    "unique_values": df[col].nunique(),
                    "most_frequent": df[col].mode().iloc[0] if not df[col].empty else None,
                    "frequency": df[col].value_counts().head().to_dict()
                }
        
        return analysis
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def get_problem_type_reasoning(problem_type: str, target_type: str, unique_values: int, unique_ratio: float) -> str:
    """Explain why a problem type was detected"""
    if problem_type == 'classification':
        if target_type in ['object', 'category', 'bool']:
            return f"Target variable is {target_type} type, indicating classification problem"
        else:
            return f"Target has {unique_values} unique values ({unique_ratio:.1%} of total), suggesting discrete classes"
    else:
        return f"Target has {unique_values} unique values ({unique_ratio:.1%} of total), indicating continuous regression target"
