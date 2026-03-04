import pytest
import pandas as pd
import numpy as np
from preprocessing import DataPreprocessor

def test_missing_values_normalization(sample_df):
    # Add some messy strings that should be normalized to NaN
    sample_df.loc[0, 'numeric'] = ''
    sample_df.loc[1, 'categorical'] = 'null'
    
    preprocessor = DataPreprocessor(sample_df)
    assert pd.isna(preprocessor.df.loc[0, 'numeric'])
    assert pd.isna(preprocessor.df.loc[1, 'categorical'])

def test_handle_missing_values_numeric(sample_df):
    preprocessor = DataPreprocessor(sample_df)
    strategies = {'missing': 'fillmedian'}
    # numeric: [1, 2, 3, 4, 5], missing: [1, NaN, 3, NaN, 5]
    # Median of [1, 3, 5] is 3
    df_processed = preprocessor.handle_missing_values(strategies)
    assert df_processed['missing'].iloc[1] == 3
    assert df_processed['missing'].iloc[3] == 3
    assert df_processed['missing'].isnull().sum() == 0

def test_handle_missing_values_categorical(sample_df):
    # categorical: ['A', 'B', 'A', 'B', 'C'] -> Mode is 'A' and 'B' (alphabetical 'A')
    sample_df.loc[0, 'categorical'] = np.nan
    preprocessor = DataPreprocessor(sample_df)
    strategies = {'categorical': 'fillmode'}
    df_processed = preprocessor.handle_missing_values(strategies)
    assert df_processed['categorical'].iloc[0] in ['A', 'B'] 
    assert df_processed['categorical'].isnull().sum() == 0

def test_handle_outliers_iqr(sample_df):
    # Add an outlier
    sample_df.loc[0, 'numeric'] = 100
    preprocessor = DataPreprocessor(sample_df)
    # [100, 2, 3, 4, 5] -> Q1=2.5, Q3=51.5? No, let's use a clearer case
    sample_df['numeric'] = [1, 2, 3, 4, 100]
    preprocessor = DataPreprocessor(sample_df)
    # Q1=2, Q3=4, IQR=2. Upper bound = 4 + 1.5*2 = 7
    df_processed = preprocessor.handle_outliers(['numeric'], method='iqr', strategy='cap')
    assert df_processed['numeric'].max() <= 7
    assert df_processed['numeric'].max() > 4

def test_encode_categorical_label(sample_df):
    preprocessor = DataPreprocessor(sample_df)
    # Ensure it's marked as categorical (DataPreprocessor should do this automatically)
    preprocessor.encode_categorical('categorical', method='label')
    assert pd.api.types.is_numeric_dtype(preprocessor.df['categorical'])
    # Labels should be 0, 1, 2 for A, B, C
    assert set(preprocessor.df['categorical'].unique()).issubset({0, 1, 2})

def test_encode_categorical_onehot(sample_df):
    preprocessor = DataPreprocessor(sample_df)
    preprocessor.encode_categorical('categorical', method='onehot')
    # Original 'categorical' column should be gone
    assert 'categorical' not in preprocessor.df.columns
    # New columns like 'categorical_B', 'categorical_C' should exist (drop_first=True)
    assert any(col.startswith('categorical_') for col in preprocessor.df.columns)
