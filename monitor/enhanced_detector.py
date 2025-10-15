import joblib
import pandas as pd
from monitor.advanced_alert_system import AdvancedAlertSystem
from monitor.live_detector import LiveRansomwareDetector
import threading
import time

class EnhancedRansomwareDetector:
    def __init__(self):
        self.detector = LiveRansomwareDetector()
        self.alert_system = AdvancedAlertSystem()
        self.performance_stats = {
            'detections': 0,
            'false_positives': 0,
            'response_times': []
        }
    
    def process_file_event(self, file_path, event_type):
        """Enhanced file event processing with comprehensive alerting"""
        start_time = time.time()

        try:
            # Use existing detection logic
            attack_detected, _ = self.detector.process_file_event(file_path, event_type)

            if attack_detected:
                # Calculate response time
                response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                self.performance_stats['response_times'].append(response_time)
                self.performance_stats['detections'] += 1
                
                # Create detailed alert
                alert_data = {
                    "severity": "high",
                    "timestamp": pd.Timestamp.now().isoformat(),
                    "message": f"Ransomware activity detected in {event_type} operation",
                    "file_path": file_path,
                    "confidence": 0.95,  # Could be based on ML probability
                    "action": "quarantine_file",
                    "response_time_ms": response_time
                }
                
                # Send alert through all channels
                self.alert_system.send_alert(alert_data)
                
                # Update dashboard if available
                self.update_dashboard(alert_data)
                
                return True
                
        except Exception as e:
            print(f"Error in enhanced detection: {e}")
            
        return False
    
    def update_dashboard(self, alert_data):
        """Update web dashboard with new alert"""
        try:
            import requests
            # Send alert to dashboard
            requests.post('http://localhost:5000/api/alerts', json=alert_data, timeout=2)
        except:
            # Dashboard might not be running, which is fine
            pass
    
    def get_performance_metrics(self):
        """Get current performance metrics"""
        if self.performance_stats['response_times']:
            avg_response = sum(self.performance_stats['response_times']) / len(self.performance_stats['response_times'])
        else:
            avg_response = 0
            
        return {
            'total_detections': self.performance_stats['detections'],
            'false_positives': self.performance_stats['false_positives'],
            'average_response_time_ms': avg_response,
            'accuracy': 1 - (self.performance_stats['false_positives'] / max(1, self.performance_stats['detections']))
        }

# Enhanced demo script
def run_enhanced_demo():
    """Run enhanced demonstration with all features"""
    enhanced_detector = EnhancedRansomwareDetector()
    
    print("🚀 Starting Enhanced Ransomware Detection Demo")
    print("=" * 50)
    
    # Simulate various file events
    test_events = [
        ("/iot_test_files/normal_config.txt", "modified"),
        ("/iot_test_files/suspicious.encrypted", "created"),
        ("/iot_test_files/logfile.log", "modified"),
        ("/iot_test_files/ransomware_pattern.bin", "created")
    ]
    
    for file_path, event_type in test_events:
        print(f"Processing: {event_type} - {file_path}")
        result = enhanced_detector.process_file_event(file_path, event_type)
        
        if result:
            print(f"🔴 ALERT: Attack detected in {file_path}")
        else:
            print(f"🟢 CLEAN: Normal activity in {file_path}")
        
        time.sleep(1)
    
    # Show performance metrics
    metrics = enhanced_detector.get_performance_metrics()
    print("\n" + "=" * 50)
    print("PERFORMANCE METRICS:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    run_enhanced_demo()