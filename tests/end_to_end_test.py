import unittest
import time
import os
from monitor.live_detector import LiveRansomwareDetector
from simulator.simulate_attack import simulate_ransomware_attack

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.detector = LiveRansomwareDetector()
        self.test_dir = "iot_test_files/test_scenario"
        os.makedirs(self.test_dir, exist_ok=True)
    
    def test_normal_activity(self):
        """Test that normal activity doesn't trigger false positives"""
        normal_files = ['config.txt', 'logfile.log', 'data.json']
        for file in normal_files:
            file_path = os.path.join(self.test_dir, file)
            with open(file_path, 'w') as f:
                f.write("Normal content")

            detected, message = self.detector.process_file_event(file_path, 'created')
            self.assertFalse(detected, "False positive on normal file")
    
    def test_attack_scenario(self):
        """Test ransomware attack detection"""
        # Simulate attack
        simulate_ransomware_attack(self.test_dir, self.test_dir + "_attack", 0.5)
        
        # Check if detection works
        attack_file = os.path.join(self.test_dir + "_attack", "test.encrypted")
        with open(attack_file, 'wb') as f:
            f.write(os.urandom(1024))  # High entropy file
            
        detected = self.detector.process_file_event(attack_file, 'created')
        self.assertTrue(detected, "Failed to detect ransomware attack")

if __name__ == '__main__':
    unittest.main()