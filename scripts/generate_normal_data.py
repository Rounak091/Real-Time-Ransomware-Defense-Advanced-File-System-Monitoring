import os
import sys

# Add the project root directory to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import random
import pandas as pd# Create __init__.py files to make directories Python packages
from monitor.file_monitor import start_monitoring
from simulator.normal_activity import simulate_normal_operations

def generate_normal_dataset():
    """Generate normal file activity data for training"""
    print("=== Generating Normal Activity Dataset ===")
    
    # Start file monitoring
    log_file = "data/raw/normal_activity.csv"
    monitor = start_monitoring("iot_test_files/normal", log_file, label=0)
    
    # Simulate normal operations for 10 minutes
    print("Simulating normal file activities...")
    simulate_normal_operations(
        directory="iot_test_files/normal",
        duration=600,  # 10 minutes
        operations_per_minute=5
    )
    
    # Stop monitoring
    monitor.stop()
    monitor.join()
    
    # Process and clean the data
    df = pd.read_csv(log_file)
    print(f"Generated {len(df)} normal activity records")
    return df

if __name__ == "__main__":
    generate_normal_dataset()