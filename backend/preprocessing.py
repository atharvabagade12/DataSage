import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder 
import json

class DataPreprocessor:
    """
    Professional data preprocessing using scikit-learn
    """
    
    
    def __init__(self, df, column_metadata=None):
        print(f"DEBUG: DataPreprocessor.__init__ called")
        print(f"   DataFrame shape: {df.shape}")
        
        # ✅ FIX: Normalize missing values - convert empty strings and other representations to NaN
        print(f"   Normalizing missing values...")
        # ... (rest of normalization logic)
        df = df.replace(['', ' ', '  ', 'null', 'NULL', 'None', 'NA', 'N/A', 'n/a', 'NaN'], np.nan)
        df = df.replace({None: np.nan})
        
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)
        
        self.df = df.copy()
        self.original_df = df.copy()
        self.preprocessing_log = []
        
        # Use provided semantic types or auto-detect
        self.semantic_types = {}
        if column_metadata:
            for col in df.columns:
                if col in column_metadata:
                    self.semantic_types[col] = column_metadata[col].get('semantic_type')
        
        # ✅ Fallback: Ensure every column has a semantic type based on pandas dtype
        for col in df.columns:
            if col not in self.semantic_types or not self.semantic_types[col]:
                if pd.api.types.is_numeric_dtype(df[col]):
                    self.semantic_types[col] = 'numeric'
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    self.semantic_types[col] = 'datetime'
                else:
                    self.semantic_types[col] = 'categorical'
            
        # Backward compatibility for existing logic that uses self.column_types
        self.column_types = self._detect_column_types()
        
    def _detect_column_types(self):
        """Map semantic types to internal numerical/categorical labels for standard preprocessing"""
        column_types = {}
        for col in self.df.columns:
            # If we have a semantic type, use it to decide the processing pipe
            s_type = self.semantic_types.get(col)
            
            if s_type == 'numeric':
                column_types[col] = 'numerical'
            elif s_type in ['categorical', 'boolean', 'datetime']:
                column_types[col] = 'categorical'
            elif s_type == 'identifier':
                column_types[col] = 'identifier' # New type to handle exclusion
            else:
                # Fallback to basic detection
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
        print(f"\nDEBUG: handle_missing_values called")
        print(f"   Strategies received: {strategies}")
        
        df_processed = self.df.copy()
        rows_before = len(df_processed)
        
        # Group columns by strategy for efficient processing
        strategy_groups = {}
        for col, strategy in strategies.items():
            if col not in df_processed.columns:
                print(f"   Column '{col}' not found in dataframe, skipping")
                continue
                
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(col)
        
        print(f"   Strategy groups: {strategy_groups}")
        
        # Process each strategy group
        for strategy, cols in strategy_groups.items():
            print(f"\n   Processing strategy '{strategy}' for columns: {cols}")
            
            if strategy == 'droprows':
                # Drop rows with missing values in these columns
                df_processed = df_processed.dropna(subset=cols)
                self.preprocessing_log.append({
                    'action': 'drop_rows',
                    'columns': cols,
                    'rows_removed': rows_before - len(df_processed)
                })
                print(f"   Dropped rows with missing values")
                
            elif strategy == 'keep':
                # Do nothing - keep missing values
                self.preprocessing_log.append({
                    'action': 'keep_missing',
                    'columns': cols
                })
                print(f"   Kept missing values as-is")
                
            else:
                # Use SimpleImputer for fill strategies
                # ✅ ENFORCE SEMANTIC TYPES
                applied_numerical = []
                applied_categorical = []
                
                for col in cols:
                    s_type = self.semantic_types.get(col)
                    
                    # Rule 1: Identifier MUST be dropped (if not already in droprows group)
                    if s_type == 'identifier' and strategy != 'droprows':
                        print(f"   ⚠️ WARNING: Column '{col}' is an Identifier but strategy is '{strategy}'. Skipping filling.")
                        continue
                        
                    # Rule 2: Validate strategy against semantic type
                    allowed = False
                    if s_type == 'numeric':
                        if strategy in ['fillmean', 'fillmedian', 'fillzero', 'fillmode']:
                            allowed = True
                            applied_numerical.append(col)
                    elif s_type in ['categorical', 'boolean', 'datetime']:
                        if strategy in ['fillmode', 'fillunknown', 'fillzero']:
                            allowed = True
                            applied_categorical.append(col)
                    
                    if not allowed:
                        print(f"   ⚠️ WARNING: Strategy '{strategy}' not allowed for semantic type '{s_type}' on column '{col}'. Skipping.")

                print(f"   Validated Numerical columns: {applied_numerical}")
                print(f"   Validated Categorical columns: {applied_categorical}")
                
                # Handle numerical columns
                if applied_numerical:
                    if strategy == 'fillmean':
                        imputer = SimpleImputer(strategy='mean')
                        print(f"   Using SimpleImputer(strategy='mean') for numerical columns")
                    elif strategy == 'fillmedian':
                        imputer = SimpleImputer(strategy='median')
                        print(f"   Using SimpleImputer(strategy='median') for numerical columns")
                    elif strategy == 'fillzero':
                        imputer = SimpleImputer(strategy='constant', fill_value=0)
                        print(f"   Using SimpleImputer(strategy='constant', fill_value=0) for numerical columns")
                    elif strategy == 'fillmode':
                        imputer = SimpleImputer(strategy='most_frequent')
                        print(f"   Using SimpleImputer(strategy='most_frequent') for numerical columns (fillmode)")
                    else:
                        imputer = SimpleImputer(strategy='most_frequent')
                        print(f"   Using SimpleImputer(strategy='most_frequent') for numerical columns (default)")
                    
                    try:
                        df_processed[applied_numerical] = imputer.fit_transform(df_processed[applied_numerical])
                        print(f"   Successfully imputed numerical columns")
                    except Exception as e:
                        print(f"   Error imputing numerical columns: {e}")
                        raise
                    
                    self.preprocessing_log.append({
                        'action': f'impute_{strategy}',
                        'columns': applied_numerical,
                        'type': 'numerical',
                        'method': 'SimpleImputer'
                    })
                
                # Handle categorical columns
                if applied_categorical:
                    # Log missing counts BEFORE imputation
                    print(f"   Missing values BEFORE imputation:")
                    for col in applied_categorical:
                        missing_before = df_processed[col].isnull().sum()
                        print(f"      {col}: {missing_before} missing values")
                    
                    if strategy == 'fillmode':
                        imputer = SimpleImputer(strategy='most_frequent')
                        print(f"   Using SimpleImputer(strategy='most_frequent') for categorical columns (fillmode)")
                    elif strategy == 'fillunknown':
                        imputer = SimpleImputer(strategy='constant', fill_value='Unknown')
                        print(f"   Using SimpleImputer(strategy='constant', fill_value='Unknown') for categorical columns")
                    else:
                        imputer = SimpleImputer(strategy='most_frequent')
                        print(f"   Using SimpleImputer(strategy='most_frequent') for categorical columns (default)")
                    
                    try:
                        df_processed[applied_categorical] = imputer.fit_transform(df_processed[applied_categorical])
                        
                        # Log missing counts AFTER imputation
                        print(f"   Missing values AFTER imputation:")
                        for col in applied_categorical:
                            missing_after = df_processed[col].isnull().sum()
                            print(f"      {col}: {missing_after} missing values")
                            
                            # Show sample of imputed values
                            sample_values = df_processed[col].value_counts().head(3)
                            print(f"      {col} top values: {sample_values.to_dict()}")
                        
                        print(f"   Successfully imputed categorical columns")
                    except Exception as e:
                        print(f"   Error imputing categorical columns: {e}")
                        raise
                    
                    self.preprocessing_log.append({
                        'action': f'impute_{strategy}',
                        'columns': applied_categorical,
                        'type': 'categorical',
                        'method': 'SimpleImputer'
                    })
        
        print(f"\nhandle_missing_values completed successfully\n")
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
            # ✅ ENFORCE SEMANTIC TYPES: Only allow outliers for numeric columns
            if self.semantic_types.get(col) != 'numeric':
                print(f"   ⚠️ Skipping outlier handling for '{col}' (Type: {self.semantic_types.get(col)})")
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
    
    def encode_categorical(self, column, method='label'):
        """Encode categorical variables - FIXED with proper dtype"""
        
        if column not in self.df.columns:
            print(f"Column {column} not found in dataframe")
            return self.df
        
        # ✅ ENFORCE SEMANTIC TYPES: Only allow encoding for categorical columns
        if self.semantic_types.get(column) != 'categorical':
            print(f"   ⚠️ Skipping encoding for '{column}' (Type: {self.semantic_types.get(column)})")
            return self.df

        try:
            if method == 'label':
                print(f"Label encoding {column}...")
                le = LabelEncoder()
                
                # ✅ Handle NaN values
                col_data = self.df[column].astype(str)
                col_data = col_data.replace('nan', 'Unknown')
                
                # ✅ Fit and transform
                self.df[column] = le.fit_transform(col_data)
                
                print(f"Label encoded {column}: {le.classes_.tolist()}")
                self.preprocessinglog.append({
                    'action': 'label_encode',
                    'column': column,
                    'classes': le.classes_.tolist()
                })
            
            elif method == 'onehot':
                print(f"One-hot encoding {column}...")
                
                col_data = self.df[column].astype(str)
                col_data = col_data.replace('nan', 'Unknown')
                
                # ✅ CRITICAL: Create dummies AND convert to int (1/0, not True/False)
                dummies = pd.get_dummies(col_data, prefix=column, drop_first=True).astype(int)
                
                # ✅ Concatenate and drop original column
                self.df = pd.concat([self.df.drop(columns=[column]), dummies], axis=1)
                
                print(f"✅ One-hot encoded {column}: created {len(dummies.columns)} columns")
                print(f"   Values: 1 (True), 0 (False)")
                self.preprocessinglog.append({
                    'action': 'onehot_encode',
                    'column': column,
                    'new_columns': dummies.columns.tolist(),
                    'dtype': 'int (1/0)'  # ✅ Document dtype
                })
            
            elif method == 'ordinal':
                print(f"Ordinal encoding {column}...")
                
                col_data = self.df[column].astype(str)
                col_data = col_data.replace('nan', 'Unknown')
                
                oe = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
                
                # ✅ Convert to int
                self.df[column] = oe.fit_transform(col_data.values.reshape(-1, 1)).astype(int)
                
                print(f"Ordinal encoded {column}: {oe.categories_[0].tolist()}")
                self.preprocessinglog.append({
                    'action': 'ordinal_encode',
                    'column': column,
                    'categories': oe.categories_[0].tolist(),
                    'dtype': 'int'  # ✅ Document dtype
                })
            
            return self.df
        
        except Exception as e:
            print(f"Error encoding {column}: {e}")
            import traceback
            traceback.print_exc()
            return self.df


    
    def scale_features(self, columns, method='standard'):
        """Scale numerical features"""
        from sklearn.preprocessing import MinMaxScaler
        
        # ✅ ENFORCE SEMANTIC TYPES: Only allow scaling for numeric columns
        valid_cols = [col for col in columns if self.semantic_types.get(col) == 'numeric']
        
        if not valid_cols:
            print("   ⚠️ No valid numeric columns found for scaling")
            return self.df
            
        print(f"   Scaling columns: {valid_cols}")
        scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
        
        self.df[valid_cols] = scaler.fit_transform(self.df[valid_cols])
        
        self.preprocessing_log.append({
            'action': f'{method}_scaling',
            'columns': columns,
            'scaler': type(scaler).__name__
        })
        
        return self.df
    
    def handle_datetime_features(self, columns, features, cyclic_encoding=False, drop_original=True):
        """
        Extract features from datetime columns and optionally apply cyclic encoding.
        
        Args:
            columns (list): Datetime columns to process
            features (list): List of features to extract ('year', 'month', 'day', 'dayofweek', 'hour', 'minute', 'second', 'is_weekend', 'timestamp')
            cyclic_encoding (bool): Whether to apply sin/cos transformations to cyclic features
            drop_original (bool): Whether to drop the original datetime columns
        """
        for col in columns:
            if col not in self.df.columns:
                print(f"⚠️ Column {col} not found, skipping...")
                continue
                
            print(f"Processing datetime column: {col}")
            
            # Ensure it's datetime (with robust error handling for out-of-bounds dates)
            try:
                # errors='coerce' will turn out-of-bounds or invalid dates into NaT
                # format='mixed' handles multiple date formats automatically
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce', format='mixed')
            except Exception as e:
                print(f"❌ Critical error converting {col} to datetime: {e}")
                continue
                
            # Extract requested features
            for feature in features:
                new_col = f"{col}_{feature}"
                
                if feature == 'year':
                    self.df[new_col] = self.df[col].dt.year
                elif feature == 'month':
                    self.df[new_col] = self.df[col].dt.month
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 12)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 12)
                elif feature == 'day':
                    self.df[new_col] = self.df[col].dt.day
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 31)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 31)
                elif feature == 'dayofweek':
                    self.df[new_col] = self.df[col].dt.dayofweek
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 7)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 7)
                elif feature == 'hour':
                    self.df[new_col] = self.df[col].dt.hour
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 24)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 24)
                elif feature == 'minute':
                    self.df[new_col] = self.df[col].dt.minute
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 60)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 60)
                elif feature == 'second':
                    self.df[new_col] = self.df[col].dt.second
                    if cyclic_encoding:
                        val = self.df[new_col]
                        self.df[f"{new_col}_sin"] = np.sin(2 * np.pi * val / 60)
                        self.df[f"{new_col}_cos"] = np.cos(2 * np.pi * val / 60)
                elif feature == 'is_weekend':
                    # dayofweek is 0-6 (0=Mon, 6=Sun)
                    dayofweek = self.df[col].dt.dayofweek
                    self.df[new_col] = dayofweek.isin([5, 6]).astype(float)
                    # Restore NaNs if original was NaT
                    self.df.loc[dayofweek.isna(), new_col] = np.nan
                elif feature == 'timestamp':
                    # Safe timestamp extraction (returns NaN for NaT)
                    self.df[new_col] = self.df[col].apply(lambda x: x.timestamp() if pd.notnull(x) else np.nan)
                
                # Update semantic types if applicable
                self.semantic_types[new_col] = 'numeric'
                    
            if drop_original:
                self.df = self.df.drop(columns=[col])
                self.preprocessing_log.append({
                    'action': 'datetime_extraction',
                    'column': col,
                    'features': features,
                    'cyclic': cyclic_encoding,
                    'dropped_original': True
                })
            else:
                self.preprocessing_log.append({
                    'action': 'datetime_extraction',
                    'column': col,
                    'features': features,
                    'cyclic': cyclic_encoding,
                    'dropped_original': False
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

class TargetEncoder:
    """
    Custom Target Encoder with mandatory smoothing
    Formula: (n * category_mean + k * global_mean) / (n + k)
    """
    def __init__(self, smoothing=10):
        self.smoothing = smoothing
        self.mappings = {}
        self.global_mean = None
        self.problem_type = None

    def fit(self, X, y, column, problem_type='regression'):
        """
        Fit the encoder using training data
        """
        self.problem_type = problem_type
        
        # ✅ FIX: Handle string targets correctly for classification
        if problem_type == 'classification':
            # Use LabelEncoder to convert strings (e.g. 'Yes'/'No') to 0/1 integers
            le = LabelEncoder()
            # Handle potential NaNs in target by converting to string first
            y_clean = y.fillna('Unknown').astype(str)
            y_numeric = le.fit_transform(y_clean)
            
            # If binary, ensures we are predicting the "positive" class (usually 1)
            # but for target encoding, mean(0,1) is sufficient proxy for probability
        else:
            # Regression: safely coerce to numeric
            y_numeric = pd.to_numeric(y, errors='coerce')

        self.global_mean = np.mean(y_numeric)
        
        # ✅ Fallback if global_mean is NaN (should not happen with valid data)
        if pd.isna(self.global_mean):
            self.global_mean = 0.0
            
        print(f"   Fitting TargetEncoder for {column}. Global Mean: {self.global_mean}")
            
        # Combine X and y for easier calculation
        data = pd.DataFrame({column: X[column], 'target': y_numeric})
        
        # ✅ Drop NaNs in X for fitting to prevent NaN keys in mappings
        data = data.dropna(subset=[column])
        
        if problem_type == 'classification' and y.nunique() > 2:
            # Multiclass encoding: one mapping per class
            self.mappings[column] = {}
            
            # Iterate over the numeric codes from LabelEncoder
            for cls_idx, cls_label in enumerate(le.classes_):
                # Calculate global mean for this specific class using numeric targets
                y_binary = (y_numeric == cls_idx).astype(int)
                cls_global_mean = np.mean(y_binary)
                if pd.isna(cls_global_mean): cls_global_mean = 0.0
                
                # Count occurrences of this class per category
                # data['target'] holds y_numeric (integers)
                stats = data.groupby(column)['target'].apply(lambda x: (x == cls_idx).sum()).reset_index()
                counts = data.groupby(column)['target'].count().reset_index()
                
                merged = stats.merge(counts, on=column)
                merged.columns = [column, 'sum', 'count']
                
                # Apply smoothing
                merged['encoded'] = (merged['sum'] + self.smoothing * cls_global_mean) / (merged['count'] + self.smoothing)
                
                # Store mapping
                self.mappings[column][cls_label] = dict(zip(merged[column], merged['encoded']))
                self.mappings[column][cls_label]['_global_mean'] = cls_global_mean
        else:
            # Binary classification or Regression
            stats = data.groupby(column)['target'].agg(['count', 'mean'])
            
            # Apply smoothing formula: (n * mean + k * global_mean) / (n + k)
            smoothed = (stats['count'] * stats['mean'] + self.smoothing * self.global_mean) / (stats['count'] + self.smoothing)
            
            # ✅ Convert to dict and handle any internal NaNs
            self.mappings[column] = smoothed.fillna(self.global_mean).to_dict()
            self.mappings[column]['_global_mean'] = self.global_mean

    def transform(self, X, column):
        """
        Apply the learned mapping to X. 
        CRITICAL: Never output NaN. Use global mean as fallback for unseen or NaN categories.
        """
        if column not in self.mappings:
            return X, []
            
        X_encoded = X.copy()
        mapping = self.mappings[column]
        
        # Determine global fallback
        global_fallback = mapping.get('_global_mean', self.global_mean)
        if pd.isna(global_fallback): global_fallback = 0.0
        
        if self.problem_type == 'classification' and isinstance(mapping, dict) and any(isinstance(v, dict) for k, v in mapping.items() if k != '_global_mean'):
            # Multiclass: create new columns
            new_cols = []
            for cls, cls_mapping in mapping.items():
                col_name = f"{column}_target_{cls}"
                cls_fallback = cls_mapping.get('_global_mean', global_fallback)
                
                # Apply mapping and strictly fill NaNs with class-specific global mean
                X_encoded[col_name] = X_encoded[column].map(cls_mapping).fillna(cls_fallback)
                new_cols.append(col_name)
            
            # Drop original column
            X_encoded = X_encoded.drop(columns=[column])
            return X_encoded, new_cols
        else:
            # Binary/Regression: replace original column
            # Apply mapping and strictly fill NaNs with global mean
            X_encoded[column] = X_encoded[column].map(mapping).fillna(global_fallback)
            return X_encoded, [column]
