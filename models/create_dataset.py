import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

class DatasetCreator:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
    
    def load_raw_data(self):
        """Load and combine normal and attack datasets"""
        print("📊 Loading raw data...")
        
        try:
            # Load normal activity data
            normal_df = pd.read_csv('data/raw/normal_activity.csv')
            print(f"✅ Loaded normal data: {len(normal_df)} records")
            
            # Load attack activity data  
            attack_df = pd.read_csv('data/raw/attack_activity.csv')
            print(f"✅ Loaded attack data: {len(attack_df)} records")
            
            # Combine datasets
            combined_df = pd.concat([normal_df, attack_df], ignore_index=True)
            print(f"📈 Combined dataset: {len(combined_df)} records")
            print(f"   - Normal: {len(normal_df)} records")
            print(f"   - Attack: {len(attack_df)} records")
            
            return combined_df
            
        except FileNotFoundError as e:
            print(f"❌ Error loading raw data: {e}")
            print("Please run data generation scripts first!")
            return None
    
    def clean_data(self, df):
        """Clean and preprocess the data"""
        print("🧹 Cleaning data...")
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        print(f"   Removed {initial_count - len(df)} duplicate records")
        
        # Handle missing values
        df = df.fillna(0)
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        return df
    
    def engineer_features(self, df):
        """Create features for machine learning"""
        print("⚙️ Engineering features...")
        
        # Basic file features
        df['file_size_kb'] = df['file_size'] / 1024
        
        # Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        
        # File type features
        df['is_text_file'] = df['file_extension'].isin(['.txt', '.log', '.csv', '.json', '.cfg'])
        df['is_binary_file'] = df['file_extension'].isin(['.dat', '.encrypted', '.locked'])
        
        # Entropy-based features
        df['high_entropy'] = (df['entropy'] > 7.0).astype(int)
        df['very_high_entropy'] = (df['entropy'] > 7.5).astype(int)
        
        # Behavioral features (simplified)
        df['large_file'] = (df['file_size'] > 1024 * 1024).astype(int)  # >1MB
        
        print(f"   Created {len([col for col in df.columns if col not in ['timestamp', 'file_path', 'event_type', 'file_extension']])} features")
        
        return df
    
    def prepare_training_data(self, df):
        """Prepare final dataset for training"""
        print("🎯 Preparing training data...")
        
        # Select features for model
        feature_columns = [
            'file_size', 'entropy', 'file_size_kb', 'hour', 'minute',
            'is_text_file', 'is_binary_file', 'high_entropy', 
            'very_high_entropy', 'large_file'
        ]
        
        # Ensure all columns exist
        available_features = [col for col in feature_columns if col in df.columns]
        print(f"   Using features: {available_features}")
        
        X = df[available_features]
        y = df['label']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y, available_features
    
    def save_dataset(self, df, filename="data/processed/dataset.csv"):
        """Save processed dataset"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"💾 Saved processed dataset to {filename}")
    
    def save_preprocessor(self, filename="data/models/preprocessor.joblib"):
        """Save scaler for later use"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        preprocessor = {
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(preprocessor, filename)
        print(f"💾 Saved preprocessor to {filename}")
    
    def create_dataset(self):
        """Complete dataset creation pipeline"""
        print("🚀 Starting Dataset Creation Pipeline")
        print("=" * 50)
        
        # Load raw data
        df = self.load_raw_data()
        if df is None:
            return None, None, None
        
        # Clean data
        df = self.clean_data(df)
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Save processed dataset
        self.save_dataset(df)
        
        # Prepare training data
        X, y, self.feature_columns = self.prepare_training_data(df)
        
        # Save preprocessor
        self.save_preprocessor()
        
        print(f"✅ Dataset creation completed!")
        print(f"📊 Final dataset: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"🎯 Class distribution: {y.value_counts().to_dict()}")
        
        return X, y, self.feature_columns

def main():
    creator = DatasetCreator()
    X, y, features = creator.create_dataset()
    
    if X is not None:
        print(f"\n🎉 Success! You can now run the training script.")
        print("Next command: python models/train_model.py")

if __name__ == "__main__":
    main()