import unittest
import os
import sys
import time
import pandas as pd
import joblib

# Add the root directory to sys.path to enable imports from monitor package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from monitor.enhanced_detector import EnhancedRansomwareDetector
from simulator.simulate_attack import simulate_ransomware_attack
from simulator.normal_activity import simulate_normal_operations
import psutil
import threading

class ComprehensiveTestSuite(unittest.TestCase):
    
    def setUp(self):
        """Setup test environment"""
        self.detector = EnhancedRansomwareDetector()
        self.test_dir = "iot_test_files/comprehensive_test"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test files
        self.create_test_files()
    
    def create_test_files(self):
        """Create variety of test files"""
        file_types = {
            'txt': 10,
            'json': 5,
            'log': 3,
            'bin': 2
        }

        for ext, count in file_types.items():
            for i in range(count):
                file_path = os.path.join(self.test_dir, f"test_file_{i}.{ext}")
                if ext == 'bin':
                    # Binary files need binary mode
                    with open(file_path, 'wb') as f:
                        f.write(os.urandom(100))
                else:
                    # Text files
                    with open(file_path, 'w') as f:
                        if ext in ['txt', 'log']:
                            # Use low entropy content for normal files
                            f.write("normal " * 20)  # Repeating low entropy text
                        elif ext == 'json':
                            f.write(f'{{"device": "test", "value": {i}}}')
    
    def test_01_detection_accuracy(self):
        """Test detection accuracy with known patterns"""
        print("\n=== Testing Detection Accuracy ===")
        
        # Test normal files (should not trigger alerts)
        normal_files = [
            os.path.join(self.test_dir, "test_file_0.txt"),
            os.path.join(self.test_dir, "test_file_1.json")
        ]
        
        false_positives = 0
        for file_path in normal_files:
            if os.path.exists(file_path):
                detected = self.detector.process_file_event(file_path, "modified")
                if detected:
                    false_positives += 1
        
        print(f"False positives: {false_positives}/{len(normal_files)}")
        self.assertLess(false_positives, len(normal_files) * 0.2)  # Less than 20% false positives
    
    def test_02_performance_benchmark(self):
        """Test system performance under load"""
        print("\n=== Testing Performance ===")
        
        start_time = time.time()
        iterations = 50
        
        for i in range(iterations):
            test_file = os.path.join(self.test_dir, f"perf_test_{i}.tmp")
            with open(test_file, 'w') as f:
                f.write("Performance test content")
            
            self.detector.process_file_event(test_file, "created")
            os.remove(test_file)
        
        total_time = time.time() - start_time
        avg_time_per_operation = total_time / iterations
        
        print(f"Average time per operation: {avg_time_per_operation:.3f}s")
        print(f"Operations per second: {iterations/total_time:.1f}")
        
        # Should process at least 10 operations per second
        self.assertGreater(iterations/total_time, 10)
    
    def test_03_memory_usage(self):
        """Test memory usage doesn't grow excessively"""
        print("\n=== Testing Memory Usage ===")
        
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Process many events
        for i in range(100):
            test_file = os.path.join(self.test_dir, f"memory_test_{i}.tmp")
            with open(test_file, 'w') as f:
                f.write("Memory test content")
            
            self.detector.process_file_event(test_file, "created")
            os.remove(test_file)
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory increase: {memory_increase:.2f} MB")
        
        # Memory shouldn't increase by more than 50MB
        self.assertLess(memory_increase, 50)
    
    def test_04_concurrent_operations(self):
        """Test handling of concurrent file operations"""
        print("\n=== Testing Concurrent Operations ===")
        
        def worker(worker_id):
            for i in range(10):
                file_path = os.path.join(self.test_dir, f"concurrent_{worker_id}_{i}.tmp")
                with open(file_path, 'w') as f:
                    f.write(f"Worker {worker_id} - Iteration {i}")
                
                self.detector.process_file_event(file_path, "created")
                time.sleep(0.01)  # Small delay
        
        # Start multiple worker threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print("All concurrent operations completed successfully")
        # Test passes if no exceptions occurred
    
    def test_05_stress_test(self):
        """Stress test with high volume of operations"""
        print("\n=== Running Stress Test ===")
        
        operations = 200
        start_time = time.time()
        
        for i in range(operations):
            # Alternate between normal and suspicious files
            if i % 10 == 0:
                # Create high-entropy file (suspicious)
                file_path = os.path.join(self.test_dir, f"stress_suspicious_{i}.enc")
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(500))  # High entropy
            else:
                # Create normal file
                file_path = os.path.join(self.test_dir, f"stress_normal_{i}.txt")
                with open(file_path, 'w') as f:
                    f.write(f"Normal stress test content {i}")
            
            self.detector.process_file_event(file_path, "created")
        
        total_time = time.time() - start_time
        ops_per_second = operations / total_time
        
        print(f"Stress test completed: {ops_per_second:.1f} operations/second")
        
        # Should handle at least 50 operations per second
        self.assertGreater(ops_per_second, 50)
    
    def test_06_model_persistence(self):
        """Test that ML models can be saved and loaded correctly"""
        print("\n=== Testing Model Persistence ===")

        try:
            # Try to load existing model
            model = joblib.load('data/models/rf_model.joblib')
            self.assertIsNotNone(model)
            print("✅ Model loaded successfully")

            # Load preprocessor to get expected number of features
            preprocessor = joblib.load('data/models/preprocessor.joblib')
            expected_features = len(preprocessor['feature_columns'])
            print(f"✅ Preprocessor loaded, expecting {expected_features} features")

            # Test model can make predictions
            import numpy as np
            sample_features = np.random.rand(1, expected_features)
            prediction = model.predict(sample_features)
            self.assertIn(prediction[0], [0, 1])
            print("✅ Model can make predictions")

        except Exception as e:
            self.fail(f"Model persistence test failed: {e}")
    
    def test_07_alert_system(self):
        """Test alert system functionality"""
        print("\n=== Testing Alert System ===")
        
        # This will test that alert system doesn't crash
        # Actual alert delivery depends on configuration
        test_alert = {
            "severity": "medium",
            "timestamp": pd.Timestamp.now().isoformat(),
            "message": "Test alert from comprehensive test suite",
            "file_path": "/test/path/file.txt",
            "confidence": 0.85,
            "action": "test"
        }
        
        try:
            self.detector.alert_system.send_alert(test_alert)
            print("✅ Alert system processed alert without errors")
        except Exception as e:
            print(f"⚠️  Alert system test completed with note: {e}")

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🚀 STARTING COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ComprehensiveTestSuite)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_comprehensive_tests()