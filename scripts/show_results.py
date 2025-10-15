#!/usr/bin/env python3
"""
Display demo results and analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_results():
    print("📈 DEMO RESULTS ANALYSIS")
    print("=" * 50)
    
    # Show alert log
    try:
        with open('logs/detection_alerts.log', 'r') as f:
            alerts = f.readlines()
        
        print("🚨 Detection Alerts:")
        for alert in alerts[-5:]:  # Show last 5 alerts
            print(f"   {alert.strip()}")
    except FileNotFoundError:
        print("   No alerts recorded yet")
    
    # Show model performance
    try:
        import joblib
        model = joblib.load('data/models/rf_model.joblib')
        print(f"\n🤖 Model Info:")
        print(f"   Model: Random Forest Classifier")
        print(f"   Features: {model.n_features_in_}")
        print(f"   Estimators: {model.n_estimators}")
    except Exception as e:
        print(f"   Model info unavailable: {e}")
    
    # Show recent detections
    try:
        df = pd.read_csv('data/processed/dataset.csv')
        attack_count = len(df[df['label'] == 1])
        normal_count = len(df[df['label'] == 0])
        
        print(f"\n📊 Training Data Summary:")
        print(f"   Normal operations: {normal_count} records")
        print(f"   Attack patterns: {attack_count} records")
        print(f"   Total dataset: {len(df)} records")
        print(f"   Attack ratio: {attack_count/len(df)*100:.1f}%")
        
    except Exception as e:
        print(f"   Data summary unavailable: {e}")

if __name__ == "__main__":
    show_results()