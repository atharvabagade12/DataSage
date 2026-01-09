
import pandas as pd
import numpy as np
import re

def detect_semantic_type(series: pd.Series):
    """
    Detect the semantic data type of a pandas Series based on rules + statistics.
    
    Returns:
        dict: {
            "column": name,
            "raw_dtype": dtype,
            "semantic_type": type,
            "confidence": high|medium|low,
            "reason": string
        }
    """
    col_name = str(series.name)
    raw_dtype = str(series.dtype)
    n_unique = series.nunique()
    total_count = len(series)
    unique_ratio = n_unique / total_count if total_count > 0 else 0
    
    # 1. Datetime detection
    if pd.api.types.is_datetime64_any_dtype(series):
        return {
            "column": col_name,
            "raw_dtype": raw_dtype,
            "semantic_type": "datetime",
            "confidence": "high",
            "reason": "Native datetime dtype detected"
        }
    
    # Try parsing as date if object
    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        # Sample some values to check for date format
        sample = series.dropna().head(10).astype(str)
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}', r'^\d{2}/\d{2}/\d{4}', r'^\d{4}/\d{2}/\d{2}',
            r'^\d{2}-\d{2}-\d{4}'
        ]
        is_date = any(all(re.match(p, val) for val in sample) for p in date_patterns)
        if is_date:
            return {
                "column": col_name,
                "raw_dtype": raw_dtype,
                "semantic_type": "datetime",
                "confidence": "medium",
                "reason": "Matches common date string patterns"
            }

    # 2. Boolean detection
    unique_vals = set(series.dropna().unique())
    boolean_sets = [
        {0, 1}, {0.0, 1.0}, {'0', '1'},
        {'yes', 'no'}, {'Yes', 'No'}, {'YES', 'NO'},
        {'true', 'false'}, {'True', 'False'}, {'TRUE', 'FALSE'},
        {True, False}
    ]
    
    if any(unique_vals.issubset(b_set) for b_set in boolean_sets):
        return {
            "column": col_name,
            "raw_dtype": raw_dtype,
            "semantic_type": "boolean",
            "confidence": "high",
            "reason": f"Binary-like values detected: {list(unique_vals)}"
        }

    # 3. Identifier detection
    # UUID pattern
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    phone_pattern = r'^\+?1?\d{9,15}$'
    
    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        sample = series.dropna().head(10).astype(str)
        if all(re.match(uuid_pattern, str(v), re.I) for v in sample):
            return {"column": col_name, "raw_dtype": raw_dtype, "semantic_type": "identifier", "confidence": "high", "reason": "UUID pattern matched"}
        if all(re.match(email_pattern, str(v)) for v in sample):
            return {"column": col_name, "raw_dtype": raw_dtype, "semantic_type": "identifier", "confidence": "high", "reason": "Email pattern matched"}

    if unique_ratio > 0.9 and n_unique > 10:
        return {
            "column": col_name,
            "raw_dtype": raw_dtype,
            "semantic_type": "identifier",
            "confidence": "high" if unique_ratio == 1.0 else "medium",
            "reason": f"High unique ratio ({unique_ratio:.2f})"
        }
    
    # Monotonic increasing (IDs often are)
    if pd.api.types.is_numeric_dtype(series) and series.is_monotonic_increasing and unique_ratio > 0.5:
        return {
            "column": col_name,
            "raw_dtype": raw_dtype,
            "semantic_type": "identifier",
            "confidence": "medium",
            "reason": "Monotonic increasing values with high uniqueness"
        }

    # 4. Numeric detection
    if pd.api.types.is_numeric_dtype(series):
        # We already checked for boolean/binary above
        if unique_ratio > 0.05 or n_unique > 20:
             return {
                "column": col_name,
                "raw_dtype": raw_dtype,
                "semantic_type": "numeric",
                "confidence": "high",
                "reason": f"Numeric type with {n_unique} unique values (ratio: {unique_ratio:.2f})"
            }

    # 5. Categorical detection (fallback)
    return {
        "column": col_name,
        "raw_dtype": raw_dtype,
        "semantic_type": "categorical",
        "confidence": "high" if unique_ratio < 0.05 else "medium",
        "reason": f"Defaulted to categorical (unique ratio: {unique_ratio:.2f})"
    }
