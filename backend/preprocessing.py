import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json

class DataPreprocessor:
    """
    Professional data preprocessing using scikit-learn
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
        self.preprocessing_log = []
        self.column_types = self._detect_column_types()
        
    def _detect_column_types(self):
        """Detect numerical vs categorical columns"""
        column_types = {}
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                column_types[col] = 'numerical'
            else:
                column_types[col] = 'categorical'
        return column_types
    
    def get_missing_info(self):
        """
        Get detailed information about missing values
        Returns dict with column-wise missing stats
        """
        missing_info = []
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_info.append({
                    'name': col,
                    'type': self.column_types[col],
                    'count': int(missing_count),
                    'percentage': round((missing_count / len(self.df)) * 100, 2),
                    'strategy': 'fillmedian' if self.column_types[col] == 'numerical' else 'fillmode'
                })
        
        return sorted(missing_info, key=lambda x: x['count'], reverse=True)
    
    def remove_columns(self, columns_to_remove):
        """Remove specified columns"""
        for col in columns_to_remove:
            if col in self.df.columns:
                self.df = self.df.drop(columns=[col])
                self.preprocessing_log.append({
                    'action': 'remove_column',
                    'column': col
                })
        
        return self.df
    
    def handle_missing_values(self, strategies):
        """
        Handle missing values using scikit-learn SimpleImputer
        
        Args:
            strategies (dict): { 'column_name': 'strategy' }
                Strategies: 'fillmean', 'fillmedian', 'fillmode', 'fillzero', 
                           'fillunknown', 'droprows', 'keep'
        
        Returns:
            DataFrame: Preprocessed dataframe
        """
        df_processed = self.df.copy()
        rows_before = len(df_processed)
        
        # Group columns by strategy for efficient processing
        strategy_groups = {}
        for col, strategy in strategies.items():
            if col not in df_processed.columns:
                continue
                
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(col)
        
        # Process each strategy group
        for strategy, cols in strategy_groups.items():
            
            if strategy == 'droprows':
                # Drop rows with missing values in these columns
                df_processed = df_processed.dropna(subset=cols)
                self.preprocessing_log.append({
                    'action': 'drop_rows',
                    'columns': cols,
                    'rows_removed': rows_before - len(df_processed)
                })
                
            elif strategy == 'keep':
                # Do nothing - keep missing values
                self.preprocessing_log.append({
                    'action': 'keep_missing',
                    'columns': cols
                })
                
            else:
                # Use SimpleImputer for fill strategies
                numerical_cols = [c for c in cols if self.column_types.get(c) == 'numerical']
                categorical_cols = [c for c in cols if self.column_types.get(c) == 'categorical']
                
                # Handle numerical columns
                if numerical_cols:
                    if strategy == 'fillmean':
                        imputer = SimpleImputer(strategy='mean')
                    elif strategy == 'fillmedian':
                        imputer = SimpleImputer(strategy='median')
                    elif strategy == 'fillzero':
                        imputer = SimpleImputer(strategy='constant', fill_value=0)
                    else:
                        imputer = SimpleImputer(strategy='most_frequent')
                    
                    df_processed[numerical_cols] = imputer.fit_transform(df_processed[numerical_cols])
                    
                    self.preprocessing_log.append({
                        'action': f'impute_{strategy}',
                        'columns': numerical_cols,
                        'type': 'numerical',
                        'method': 'SimpleImputer'
                    })
                
                # Handle categorical columns
                if categorical_cols:
                    if strategy == 'fillmode':
                        imputer = SimpleImputer(strategy='most_frequent')
                    elif strategy == 'fillunknown':
                        imputer = SimpleImputer(strategy='constant', fill_value='Unknown')
                    else:
                        imputer = SimpleImputer(strategy='most_frequent')
                    
                    df_processed[categorical_cols] = imputer.fit_transform(df_processed[categorical_cols])
                    
                    self.preprocessing_log.append({
                        'action': f'impute_{strategy}',
                        'columns': categorical_cols,
                        'type': 'categorical',
                        'method': 'SimpleImputer'
                    })
        
        self.df = df_processed
        return df_processed
    
    def remove_duplicates(self, strategy='first'):
        """Remove duplicate rows using pandas"""
        rows_before = len(self.df)
        
        if strategy == 'first':
            self.df = self.df.drop_duplicates(keep='first')
        elif strategy == 'last':
            self.df = self.df.drop_duplicates(keep='last')
        elif strategy == 'all':
            self.df = self.df.drop_duplicates(keep=False)
        
        rows_removed = rows_before - len(self.df)
        
        self.preprocessing_log.append({
            'action': 'remove_duplicates',
            'strategy': strategy,
            'rows_removed': rows_removed
        })
        
        return self.df
    
    def handle_outliers(self, columns, method='iqr', strategy='cap'):
        """
        Handle outliers using IQR or Z-score methods
        
        Args:
            columns (list): Columns to check for outliers
            method (str): 'iqr' or 'zscore'
            strategy (str): 'cap' (winsorize) or 'remove'
        """
        for col in columns:
            if self.column_types.get(col) != 'numerical':
                continue
            
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
            else:  # zscore
                mean = self.df[col].mean()
                std = self.df[col].std()
                lower_bound = mean - 3 * std
                upper_bound = mean + 3 * std
            
            outliers_count = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            
            if strategy == 'cap':
                # Winsorization - cap outliers at bounds
                self.df[col] = np.clip(self.df[col], lower_bound, upper_bound)
                action = 'capped'
            else:  # remove
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                action = 'removed'
            
            self.preprocessing_log.append({
                'action': f'outlier_{action}',
                'column': col,
                'method': method,
                'outliers_affected': int(outliers_count),
                'bounds': [float(lower_bound), float(upper_bound)]
            })
        
        return self.df
    
    def encode_categorical(self, columns, method='label'):
        """
        Encode categorical variables
        
        Args:
            columns (list): Columns to encode
            method (str): 'label' or 'onehot'
        """
        for col in columns:
            if col not in self.df.columns:
                continue
            
            if method == 'label':
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col].astype(str))
                
                self.preprocessing_log.append({
                    'action': 'label_encode',
                    'column': col,
                    'classes': le.classes_.tolist()
                })
            
            elif method == 'onehot':
                # One-hot encoding
                dummies = pd.get_dummies(self.df[col], prefix=col)
                self.df = pd.concat([self.df.drop(col, axis=1), dummies], axis=1)
                
                self.preprocessing_log.append({
                    'action': 'onehot_encode',
                    'column': col,
                    'new_columns': dummies.columns.tolist()
                })
        
        return self.df
    
    def scale_features(self, columns, method='standard'):
        """
        Scale numerical features
        
        Args:
            columns (list): Columns to scale
            method (str): 'standard' or 'minmax'
        """
        from sklearn.preprocessing import MinMaxScaler
        
        scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
        
        self.df[columns] = scaler.fit_transform(self.df[columns])
        
        self.preprocessing_log.append({
            'action': f'{method}_scaling',
            'columns': columns,
            'scaler': type(scaler).__name__
        })
        
        return self.df
    
    def get_preprocessing_summary(self):
        """Get summary of all preprocessing steps"""
        return {
            'original_shape': self.original_df.shape,
            'final_shape': self.df.shape,
            'rows_removed': len(self.original_df) - len(self.df),
            'columns_added': len(self.df.columns) - len(self.original_df.columns),
            'preprocessing_steps': self.preprocessing_log
        }
    
    def get_processed_dataframe(self):
        """Return the processed dataframe"""
        return self.df
