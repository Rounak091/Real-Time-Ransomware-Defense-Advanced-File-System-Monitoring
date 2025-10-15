#!/usr/bin/env python3
"""
Test script for the complete ransomware detection system
"""

import os
import time
import sys
import site

# Add virtual environment site-packages to sys.path to fix joblib import error
venv_site = '/home/rounak/iot-ransomware-detection/venv/lib/python3.13/site-packages'
if venv_site not in sys.path:
    sys.path.insert(0, venv_site)

from monitor.live_detector import LiveRansomwareDetector

def main():
    print("🧪 Testing Ransomware Detection System")
    print("=" * 50)
    
    # Initialize detector
    detector = LiveRansomwareDetector()
    
    # Test scenarios
    test_cases = [
        {
            'name': 'Normal text file',
            'file': 'iot_test_files/normal/config.txt',
            'expected': 'No detection'
        },
        {
            'name': 'Encrypted file',
            'file': 'iot_test_files/attacked/document.encrypted', 
            'expected': 'Detection expected'
        },
        {
            'name': 'Ransom note',
            'file': 'iot_test_files/attacked/READ_ME.txt',
            'expected': 'Detection expected'
        }
    ]
    
    # Create test files if they don't exist
    if not os.path.exists('iot_test_files/attacked/document.encrypted'):
        with open('iot_test_files/attacked/document.encrypted', 'wb') as f:
            f.write(os.urandom(2048))  # High entropy
    
    if not os.path.exists('iot_test_files/attacked/READ_ME.txt'):
        with open('iot_test_files/attacked/READ_ME.txt', 'w') as f:
            f.write("Your files have been encrypted. Send bitcoin to recover.")
    
    # Run tests
    for test in test_cases:
        print(f"\n🔍 Testing: {test['name']}")
        print(f"File: {test['file']}")
        
        if os.path.exists(test['file']):
            detected, message = detector.process_file_event(test['file'], 'created')
            print(f"Result: {'🚨 DETECTED' if detected else '✅ CLEAN'}")
            print(f"Message: {message}")
            print(f"Expected: {test['expected']}")
        else:
            print(f"❌ Test file not found: {test['file']}")
    
    # Show statistics
    print("\n📊 Detection Statistics:")
    stats = detector.get_statistics()
    for key, value in stats.items():
        if key != 'recent_alerts':
            print(f"  {key}: {value}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        print("✅ Test completed")
        print("=" * 50)
        print("Thank you for testing the ransomware detection system!")
              