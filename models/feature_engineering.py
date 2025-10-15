import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

class FeatureEngineer:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_columns = []
    
    def load_and_combine_data(self):
        """Load and combine normal and attack datasets"""
        try:
            # Load raw data
            normal_df = pd.read_csv("data/raw/normal_activity.csv")
            attack_df = pd.read_csv("data/raw/attack_activity.csv")
            
            # Combine datasets
            combined_df = pd.concat([normal_df, attack_df], ignore_index=True)
            print(f"Combined dataset: {len(combined_df)} records")
            print(f"Normal: {len(normal_df)}, Attack: {len(attack_df)}")
            
            return combined_df
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def engineer_features(self, df):
        """Create advanced features for ML model"""
        if df.empty:
            return df
        
        # Basic features
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        
        # File type features
        df['is_text_file'] = df['file_extension'].isin(['.txt', '.log', '.csv', '.json'])
        df['is_config_file'] = df['file_extension'].isin(['.cfg', '.conf', '.ini', '.xml'])
        df['is_binary_file'] = df['file_extension'].isin(['.bin', '.dat', '.encrypted'])
        
        # Entropy-based features
        df['high_entropy'] = (df['entropy'] > 7.0).astype(int)
        df['very_high_entropy'] = (df['entropy'] > 7.5).astype(int)
        
        # Size-based features
        df['file_size_mb'] = df['file_size'] / (1024 * 1024)
        df['large_file'] = (df['file_size'] > 1024 * 1024).astype(int)  # >1MB
        
        # Aggregation features (window-based)
        df = self.add_window_features(df)
        
        return df
    
    def add_window_features(self, df):
        """Add time-window aggregated features"""
        # Sort by timestamp
        df = df.sort_values('timestamp')
        
        # Calculate events in last 5 minutes window
        df['recent_events_5min'] = 0
        df['recent_entropy_avg_5min'] = 0.0
        
        window_seconds = 300  # 5 minutes
        
        for i, row in df.iterrows():
            window_start = row['timestamp'] - pd.Timedelta(seconds=window_seconds)
            window_data = df[(df['timestamp'] >= window_start) & (df['timestamp'] <= row['timestamp'])]
            
            df.at[i, 'recent_events_5min'] = len(window_data)
            df.at[i, 'recent_entropy_avg_5min'] = window_data['entropy'].mean()
        
        return df
    
    def prepare_training_data(self, df):
        """Prepare final features for training"""
        # Select features for model
        feature_columns = [
            'file_size', 'entropy', 'hour', 'minute',
            'is_text_file', 'is_config_file', 'is_binary_file',
            'high_entropy', 'very_high_entropy', 'file_size_mb', 'large_file',
            'recent_events_5min', 'recent_entropy_avg_5min'
        ]
        
        self.feature_columns = feature_columns
        
        X = df[feature_columns].fillna(0)
        y = df['label']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def save_processed_data(self, df, filename="data/processed/dataset.csv"):
        """Save processed dataset"""
        df.to_csv(filename, index=False)
        print(f"Saved processed dataset to {filename}")
    
    def save_preprocessor(self, filename="data/models/preprocessor.joblib"):
        """Save scaler and feature information"""
        preprocessor = {
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(preprocessor, filename)
        print(f"Saved preprocessor to {filename}")

# Main execution function
def create_dataset():
    """Complete dataset creation pipeline"""
    engineer = FeatureEngineer()
    
    # Load and combine data
    df = engineer.load_and_combine_data()
    if df.empty:
        print("No data to process!")
        return
    
    # Engineer features
    df = engineer.engineer_features(df)
    
    # Save processed data
    engineer.save_processed_data(df)
    
    # Prepare training data
    X, y = engineer.prepare_training_data(df)
    
    # Save preprocessor
    engineer.save_preprocessor()
    
    print(f"Dataset created with {X.shape[0]} samples and {X.shape[1]} features")
    print(f"Class distribution: {y.value_counts().to_dict()}")
    
    return X, y

if __name__ == "__main__":
    X, y = create_dataset()