import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def train_random_forest():
    """Train a Random Forest classifier for ransomware detection"""
    print("🌲 Training Random Forest Classifier")
    print("=" * 40)
    
    try:
        # Load the processed dataset
        df = pd.read_csv('data/processed/dataset.csv')
        print(f"✅ Dataset loaded: {len(df)} records")
        
    except FileNotFoundError:
        print("❌ Dataset not found! Please run data processing first.")
        print("💡 Run: python models/create_dataset.py")
        return None
    
    # Prepare features (adjust based on your actual columns)
    exclude_columns = ['timestamp', 'file_path', 'file_name', 'event_type', 'file_extension', 'label', 'entropy',   'size', 'file_size', 'file_entropy', 'event_type', 'file_extension']
    feature_columns = [col for col in df.columns if col not in exclude_columns]
    
    print(f"📊 Using features: {feature_columns}")
    
    X = df[feature_columns].fillna(0)
    y = df['label']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📈 Training set: {X_train.shape}")
    print(f"📈 Test set: {X_test.shape}")
    
    # Train Random Forest model with improved parameters
    rf_model = RandomForestClassifier(
        n_estimators=2000,  # Increased number of trees
        max_depth=None,  # Allow full depth for better capacity
        random_state=42,
        class_weight='balanced'
    )
    
    rf_model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # FIXED: printf -> print
    print(f"✅ Random Forest Accuracy: {accuracy:.4f}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\n📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save the model (ensure directory exists)
    os.makedirs('data/models', exist_ok=True)
    
    # FIXED: Only save Random Forest model (removed svm_model)
    joblib.dump(rf_model, 'data/models/rf_model.joblib')
    print("💾 Random Forest model saved to: data/models/rf_model.joblib")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf_model.feature_importances_  # FIXED: Added underscore
    }).sort_values('importance', ascending=False)
    
    print("\n🌲 Feature Importance:")
    print(feature_importance)
    
    return rf_model, accuracy

if __name__ == "__main__":
    model, accuracy = train_random_forest()
    if model is not None:
        print(f"\n🎉 Training completed! Final accuracy: {accuracy:.4f}")
        print("You can now use the trained model for predictions.")
        print("Next command: python models/evaluate_model.py")
