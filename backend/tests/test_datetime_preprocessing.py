import pandas as pd
import numpy as np
import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing import DataPreprocessor

def test_datetime_handling():
    # Create dummy data with one out-of-bounds date
    data = {
        'date': ['2023-01-01 12:00:00', '2023-06-15 08:30:15', '5013-07-15 00:00:00'],
        'target': [1, 0, 1]
    }
    df = pd.DataFrame(data)
    
    print("Original DataFrame:")
    print(df)
    
    metadata = {'date': {'semantic_type': 'datetime'}}
    processor = DataPreprocessor(df, column_metadata=metadata)
    
    features = ['year', 'month', 'day', 'dayofweek', 'hour', 'minute', 'second', 'is_weekend', 'timestamp']
    
    print("\nApplying datetime extraction with cyclic encoding...")
    df_processed = processor.handle_datetime_features(
        columns=['date'],
        features=features,
        cyclic_encoding=True,
        drop_original=True
    )
    
    print("\nProcessed DataFrame Columns:")
    print(df_processed.columns.tolist())
    
    print("\nSample of Processed Data:")
    print(df_processed.head())
    
    # Assertions
    assert 'date_year' in df_processed.columns
    assert 'date_month_sin' in df_processed.columns
    assert 'date_timestamp' in df_processed.columns
    assert 'date' not in df_processed.columns
    
    print("\nDatetime handling test PASSED!")

if __name__ == "__main__":
    test_datetime_handling()
