#!/usr/bin/env python3
"""
Clean demo script without warnings
"""

import warnings
import os
import sys
import time
import threading

# Suppress warnings for clean demo output
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitor.live_detector import LiveRansomwareDetector, start_demo_monitoring
from simulator.simulate_attack import simulate_ransomware_attack

def run_clean_demo():
    print("🎬 CLEAN DEMO: Ransomware Detection System")
    print("=" * 60)
    print("This demo suppresses warnings for clean output")
    print("=" * 60)
    
    # Start monitoring in a separate thread
    print("1. 🚀 Starting real-time monitoring...")
    monitor_thread = threading.Thread(target=start_demo_monitoring, daemon=True)
    monitor_thread.start()
    
    # Wait for monitoring to start
    time.sleep(3)
    
    # Create test directory
    test_dir = "iot_test_files/demo_clean"
    os.makedirs(test_dir, exist_ok=True)
    
    # Phase 1: Create some normal files
    print("2. 📁 Creating normal files...")
    for i in range(5):
        with open(f"{test_dir}/normal_config_{i}.txt", "w") as f:
            f.write(f"Normal device configuration #{i}")
        time.sleep(1)
    
    # Phase 2: Simulate ransomware attack
    print("3. 💀 SIMULATING RANSOMWARE ATTACK...")
    files_encrypted = simulate_ransomware_attack(
        source_dir=test_dir,
        target_dir=test_dir + "_encrypted",
        attack_intensity=0.8
    )
    
    print(f"4. ✅ Attack simulated on {files_encrypted} files")
    print("5. 🔍 Monitoring for detection... (waiting 30 seconds)")
    
    # Keep running to see detections
    time.sleep(30)
    
    print("6. 🎉 Demo complete!")
    print("\n📋 Check these files for results:")
    print("   - logs/detection_alerts.log")
    print("   - tail -f logs/monitoring.log")

if __name__ == "__main__":
    run_clean_demo()