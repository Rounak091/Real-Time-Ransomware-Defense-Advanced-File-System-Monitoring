import os
import sys

# Add the project root directory to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import pandas as pd
from monitor.file_monitor import start_monitoring
from simulator.simulate_attack import simulate_ransomware_attack

def generate_attack_dataset():
    """Generate ransomware attack data for training"""
    print("=== Generating Attack Activity Dataset ===")
    
    # Start file monitoring
    log_file = "data/raw/attack_activity.csv"
    monitor = start_monitoring("iot_test_files/attacked", log_file, label=1)
    
    # Simulate ransomware attack
    print("Simulating ransomware attack...")
    files_attacked = simulate_ransomware_attack(
        source_dir="iot_test_files/normal",
        target_dir="iot_test_files/attacked",
        attack_intensity=0.6
    )
    
    # Wait for monitoring to capture all events
    time.sleep(10)
    
    # Stop monitoring
    monitor.stop()
    monitor.join()
    
    # Process the data
    df = pd.read_csv(log_file)
    print(f"Generated {len(df)} attack activity records")
    print(f"Simulated attack on {files_attacked} files")
    return df

if __name__ == "__main__":
    generate_attack_dataset()