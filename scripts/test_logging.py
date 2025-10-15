#!/usr/bin/env python3
"""
Test script to verify logging is working
"""

import os
import logging
import time

def test_logging_system():
    print("🧪 Testing logging system...")
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Test basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/monitoring.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('TestLogger')
    
    # Test different log levels
    logger.info("This is an INFO message - normal operation")
    logger.warning("This is a WARNING message - suspicious activity")
    logger.error("This is an ERROR message - something went wrong")
    
    print("✅ Log messages written. Check logs/monitoring.log")
    
    # Show log file content
    print("\n📄 Current log file content:")
    try:
        with open('logs/monitoring.log', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Log file not created yet")

def create_test_files():
    """Create test files to trigger monitoring"""
    print("\n📁 Creating test files...")
    
    test_dir = "iot_test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create different types of files
    test_files = [
        ("normal_config.txt", "This is a normal configuration file"),
        ("log_file.log", "2024-01-15 10:30:00 - Device started successfully"),
        ("high_entropy.bin", None)  # Will create with random data
    ]
    
    for filename, content in test_files:
        filepath = os.path.join(test_dir, filename)
        if content:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"   Created: {filename} (text)")
        else:
            # Create high entropy file
            with open(filepath, 'wb') as f:
                f.write(os.urandom(1024))  # 1KB of random data
            print(f"   Created: {filename} (high entropy)")
    
    print(f"✅ Test files created in {test_dir}/")

if __name__ == "__main__":
    test_logging_system()
    create_test_files()
    
    print("\n🎯 Now run this in one terminal:")
    print("   python -m monitor.live_detector")
    print("\n🎯 And in another terminal, watch the logs:")
    print("   tail -f logs/monitoring.log")
    print("   tail -f logs/detection_alerts.log")