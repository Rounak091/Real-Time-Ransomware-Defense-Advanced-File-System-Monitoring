#!/usr/bin/env python3
"""
Demo script for live ransomware attack simulation
"""

import time
import threading
import os
import sys

# Add the project root directory to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitor.live_detector import LiveRansomwareDetector
from simulator.simulate_attack import simulate_ransomware_attack
from simulator.normal_activity import simulate_normal_operations

def main():
    print("🚀 Starting Live Ransomware Detection Demo")
    print("=" * 60)
    
    # Initialize detector
    detector = LiveRansomwareDetector()
    test_dir = "iot_test_files/normal"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create some initial files
    print("1. Creating demo environment...")
    for i in range(20):
        with open(f"{test_dir}/normal_file_{i}.txt", "w") as f:
            f.write(f"Normal configuration data for device {i}")
    
    # Phase 1: Normal activity (30 seconds)
    print("2. Starting normal activity simulation...")
    
    def run_normal():
        simulate_normal_operations(test_dir, duration=30, operations_per_minute=3)
    
    normal_thread = threading.Thread(target=run_normal)
    normal_thread.start()
    
    # Wait a bit then start attack
    time.sleep(10)
    
    # Phase 2: Ransomware attack
    print("3. 💀 SIMULATING RANSOMWARE ATTACK...")
    
    def run_attack():
        # Simulate the attack
        files_encrypted = simulate_ransomware_attack(
            source_dir=test_dir,
            target_dir=test_dir + "_encrypted",
            attack_intensity=0.6
        )
        print(f"   Encrypted {files_encrypted} files simulated")
    
    attack_thread = threading.Thread(target=run_attack)
    attack_thread.start()
    
    # Wait for both to complete
    normal_thread.join()
    attack_thread.join()
    
    print("4. 📊 Demo completed!")
    print(f"   Check 'logs/detection_alerts.log' for detection results")
    print(f"   Encrypted files in: {test_dir}_encrypted/")

if __name__ == "__main__":
    main()