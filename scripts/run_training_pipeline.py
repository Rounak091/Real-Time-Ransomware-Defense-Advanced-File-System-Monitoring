#!/usr/bin/env python3
"""
Complete training pipeline script
Run this to generate data and train models
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_normal_data import generate_normal_dataset
from scripts.generate_attack_data import generate_attack_dataset
from models.train_model import ModelTrainer

def main():
    print("🚀 Starting Complete Training Pipeline")
    print("=" * 50)
    
    # Step 1: Generate normal data
    print("📊 Step 1: Generating normal activity data...")
    generate_normal_dataset()
    
    # Step 2: Generate attack data
    print("🦠 Step 2: Generating attack data...")
    generate_attack_dataset()
    
    # Step 3: Train models
    print("🤖 Step 3: Training machine learning models...")
    trainer = ModelTrainer()
    trainer.train_all_models()
    
    print("✅ Training pipeline completed successfully!")
    print("📁 Generated files:")
    print("   - data/raw/normal_activity.csv")
    print("   - data/raw/attack_activity.csv")
    print("   - data/processed/dataset.csv")
    print("   - data/models/rf_model.joblib")
    print("   - data/models/svm_model.joblib")

if __name__ == "__main__":
    main()