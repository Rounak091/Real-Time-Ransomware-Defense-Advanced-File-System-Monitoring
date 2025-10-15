# Final model training with all data
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_final_model():
    # Load all available data
    df = pd.read_csv('data/processed/dataset.csv', parse_dates=['timestamp'])
    df['file_extension'] = df['file_path'].str.extract(r'(\.\w+)$')[0].fillna('').str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['hour'] = df['timestamp'].dt.hour
    df['is_text_file'] = df['file_extension'].isin(['.txt', '.log', '.csv'])
    df['high_entropy'] = (df['entropy'] > 7.0).astype(int)
    
    # Use all data for final training
    X = df.drop(['label', 'timestamp', 'file_path', 'file_name', 'file_extension', 'event_type'], axis=1, errors='ignore')
    y = df['label']
    
    # Train final model
    final_model = RandomForestClassifier(
        n_estimators=200,  # More trees for better performance
        max_depth=15,
        random_state=42,
        class_weight='balanced'
    )
    
    final_model.fit(X, y)
    
    # Save final model
    joblib.dump(final_model, 'data/models/rf_model.joblib')
    print("Final model trained and saved!")
    
    # Feature importance
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': final_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("Final Feature Importance:")
    print(importance)

if __name__ == "__main__":
    train_final_model()