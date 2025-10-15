import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()
        self.feature_columns = []
    
    def load_data(self):
        """Load and preprocess the dataset"""
        df = pd.read_csv('data/processed/dataset.csv')
        
        # Feature engineering
        df = self.create_features(df)
        
        # Select final features
        self.feature_columns = ['file_size', 'entropy', 'is_text_file', 
                               'high_entropy', 'recent_events_5min', 'hour']
        
        X = df[self.feature_columns]
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def create_features(self, df):
        """Create additional features"""
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['hour'] = df['timestamp'].dt.hour
        df['is_text_file'] = df['file_extension'].isin(['.txt', '.log', '.csv'])
        df['high_entropy'] = (df['entropy'] > 7.0).astype(int)
        return df
    
def load_and_prepare_data():
    """Load and prepare data for training"""
    # Load dataset
    df = pd.read_csv('data/processed/dataset.csv')
    
    # Prepare features
    exclude_columns = ['timestamp', 'file_path', 'file_name', 'event_type', 'file_extension', 'label']
    feature_columns = [col for col in df.columns if col not in exclude_columns]
    
    X = df[feature_columns].fillna(0)
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_columns