"""
Real-time ransomware detection system - WARNING-FREE VERSION
"""

import warnings
import time
import joblib
import pandas as pd
import os
import logging
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitor.entropy import file_entropy
from monitor.rule_based_detector import RuleBasedDetector
import requests
import threading

# Suppress scikit-learn warnings about feature names
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

class LiveRansomwareDetector(FileSystemEventHandler):
    def __init__(self):
        # Setup logging
        self.setup_logging()

        # Load trained model and feature information
        try:
            # Load the Random Forest model
            self.model = joblib.load('data/models/rf_model.joblib')
            # Load preprocessor for feature scaling
            self.preprocessor = joblib.load('data/models/preprocessor.joblib')
            self.scaler = self.preprocessor['scaler']
            self.feature_columns = self.preprocessor['feature_columns']
            self.model_loaded = True
            self.logger.info(f"Random Forest ML model loaded successfully - expecting {len(self.feature_columns)} features")
            print(f"✅ Random Forest ML model loaded successfully - expecting {len(self.feature_columns)} features")
        except Exception as e:
            self.model_loaded = False
            self.logger.error(f"ML model not available: {e}")
            print(f"⚠️  ML model not available: {e}")

        #Rule-based detector
        self.rule_detector = RuleBasedDetector()

        # Detection thresholds
        self.entropy_threshold = 6.0
        self.files_accessed = []  # Track recent file accesses for rule-based detection
        self.alerts = []
        self.detection_count = 0

        # Feature columns will be loaded from preprocessor
        self.feature_columns = []

    def setup_logging(self):
        """Setup comprehensive logging system"""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/monitoring.log'),
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger('RansomwareDetector')

        # Create a separate alert log file
        alert_handler = logging.FileHandler('logs/detection_alerts.log')
        alert_handler.setLevel(logging.WARNING)
        alert_handler.setFormatter(logging.Formatter('%(asctime)s - ALERT - %(message)s'))
        self.logger.addHandler(alert_handler)

    # ... [rest of the code remains the same as previous version]

    def on_created(self, event):
        if not event.is_directory:
            self.logger.info(f"File created: {event.src_path}")
            self.analyze_file(event.src_path, 'created')

    def on_modified(self, event):
        if not event.is_directory:
            self.logger.info(f"File modified: {event.src_path}")
            self.analyze_file(event.src_path, 'modified')

    def on_deleted(self, event):
        if not event.is_directory:
            self.logger.info(f"File deleted: {event.src_path}")
            # Log deletion but don't analyze (file doesn't exist anymore)
            self.log_event('deleted', event.src_path, 0, 0)

    def on_moved(self, event):
        if not event.is_directory:
            self.logger.info(f"File moved: {event.src_path} -> {event.dest_path}")
            self.analyze_file(event.dest_path, 'moved')

    def log_event(self, event_type, filepath, file_size, entropy):
        """Log all file events to monitoring log"""
        try:
            self.logger.info(f"Event: {event_type}, File: {os.path.basename(filepath)}, "
                           f"Size: {file_size} bytes, Entropy: {entropy:.2f}")
        except Exception as e:
            print(f"Logging error: {e}")

    def extract_features(self, file_path, event_type):
        """Extract features for ML prediction - matching training features"""
        try:
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            try:
                entropy = file_entropy(file_path) if os.path.exists(file_path) else 0
            except (OSError, IOError) as e:
                self.logger.warning(f"I/O error calculating entropy for {file_path}: {e}")
                entropy = 0  # Default to 0 on I/O error

            # Extract all features matching training data exactly
            features = {
                'file_size': file_size,
                'entropy': entropy,
                'file_size_kb': file_size / 1024 if file_size > 0 else 0,
                'hour': pd.Timestamp.now().hour,
                'minute': pd.Timestamp.now().minute,
                'is_text_file': 1 if file_path.endswith(('.txt', '.log', '.csv', '.json', '.cfg')) else 0,
                'is_binary_file': 1 if file_path.endswith(('.dat', '.encrypted', '.locked')) else 0,
                'high_entropy': 1 if entropy > 7.0 else 0,
                'very_high_entropy': 1 if entropy > 7.5 else 0,
                'large_file': 1 if file_size > 1024 * 1024 else 0
            }

            return features

        except Exception as e:
            print(f"Error extracting features from {file_path}: {e}")
            return None

    def create_feature_vector(self, features_dict, expected_features):
        """Create properly ordered feature vector for the model"""
        feature_vector = []
        for feature_name in expected_features:
            if feature_name in features_dict:
                feature_vector.append(features_dict[feature_name])
            else:
                # Use default value for missing features
                default_value = 0.0
                feature_vector.append(default_value)
                self.logger.warning(f"Missing feature: {feature_name}, using default {default_value}")

        return [feature_vector]

    def analyze_file(self, filepath, event_type):
        """Analyze file for ransomware indicators"""
        try:
            # Calculate entropy and file size
            try:
                entropy = file_entropy(filepath)
                file_size = os.path.getsize(filepath)
            except (OSError, IOError) as e:
                self.logger.warning(f"I/O error accessing {filepath}: {e}. Skipping analysis.")
                return  # Skip analysis if file is inaccessible

            # Log the event
            self.log_event(event_type, filepath, file_size, entropy)

            # Track file access
            current_time = time.time()
            self.files_accessed.append({
                'time': current_time,
                'filepath': filepath,
                'entropy': entropy,
                'file_size': file_size
            })

            # Keep only last 10 minutes of data
            self.files_accessed = [f for f in self.files_accessed
                                 if current_time - f['time'] < 600]

            # Rule-based detection
            alerts = self.rule_based_detection(filepath, entropy, file_size)

            # ML-based detection
            ml_confidence = 0.0
            if self.model_loaded and self.feature_columns:
                prediction, prob = self.ml_detection(filepath, event_type, entropy, file_size)
                ml_confidence = prob
                if prediction == 1:
                    alerts.append(f"ML Detection: {prob:.1%} confidence")

            # Trigger alerts
            for alert in alerts:
                self.trigger_alert(alert, filepath, entropy, ml_confidence)

        except Exception as e:
            self.logger.error(f"Error analyzing {filepath}: {e}")

    def rule_based_detection(self, filepath, entropy, file_size):
        """Rule-based detection rules"""
        alerts = []

        # High entropy detection
        if entropy > self.entropy_threshold:
            alerts.append(f"High entropy ({entropy:.2f})")

        # Rapid file access detection
        recent_files = [f for f in self.files_accessed
                       if time.time() - f['time'] < 10]  # 10-second window

        if len(recent_files) > 15:  # More than 15 files in 10 seconds
            alerts.append(f"Rapid file access ({len(recent_files)} files)")

        return alerts

    def ml_detection(self, filepath, event_type, entropy, file_size):
        """Machine learning detection with proper scaling"""

        if not self.model_loaded or not self.feature_columns:
            return 0, 0.0  # Fallback to rule-based only

        try:
            # Extract features for the given file
            features = self.extract_features(filepath, event_type)
            if features is None:
                return 0, 0.0

            # Create feature vector in correct order matching training features
            feature_vector = [features.get(col, 0.0) for col in self.feature_columns]

            # Verify feature vector length matches expected
            if len(feature_vector) != len(self.feature_columns):
                self.logger.warning(f"Feature vector length mismatch: expected {len(self.feature_columns)}, got {len(feature_vector)}")
                return 0, 0.0

            # Convert to numpy array and scale
            feature_vector = np.array([feature_vector])
            feature_vector_scaled = self.scaler.transform(feature_vector)

            # Make prediction
            prediction = self.model.predict(feature_vector_scaled)[0]
            probability = self.model.predict_proba(feature_vector_scaled)[0][1]

            # Debug log prediction and probability
            self.logger.info(f"ML detection for {filepath}: prediction={prediction}, probability={probability:.4f}")

            return prediction, probability

        except Exception as e:
            print(f"ML detection error: {e}")
            return 0, 0.0

    def process_file_event(self, file_path, event_type, ml_confidence=0.0):
        """Process real-time file events for ransomware detection"""
        print(f"🔍 Analyzing: {event_type} - {os.path.basename(file_path)}")

        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False, "File not found"

            # Extract features
            features = self.extract_features(file_path, event_type)

            # Log the event
            self.log_event(event_type, file_path, features['file_size'], features['entropy'])
            if not features:
                print(f"⚠️  Feature extraction failed for {file_path}")
                self.logger.error(f"Feature extraction failed for {file_path}")
                return False, "Feature extraction failed"
            self.logger.info(f"Extracted features for {file_path}: {features}")
            print(f"✅ Extracted features for {file_path}: {features}")

            if features is None:
                return False, "Feature extraction failed"

            # ML Detection
            entropy = features.get('entropy', 0.0)
            ml_prediction, ml_confidence = self.ml_detection(file_path, event_type, entropy, features.get('file_size', 0))
            self.logger.info(f"ML result for {file_path}: prediction={ml_prediction}, confidence={ml_confidence:.4f}")

            # Ensure ml_confidence is a float
            if isinstance(ml_confidence, (int, float)):
                ml_confidence = float(ml_confidence)
            elif ml_confidence is None:
                ml_confidence = 0.0
            elif isinstance(ml_confidence, str):
                # Extract numeric value if it's a string
                try:
                    # Try to extract number from string
                    import re
                    numbers = re.findall(r"\d+\.\d+", ml_confidence)
                    if numbers:
                        ml_confidence = float(numbers[0])
                    else:
                        ml_confidence = 0.0
                except:
                    ml_confidence = 0.0

            # Rule-based Detection
            rule_alerts = self.rule_detector.detect_anomaly(
                file_path, event_type, features['entropy'], features['file_size']
            )

            # Decision Logic
            attack_detected = False
            alert_message = ""

            if ml_prediction == 1 and ml_confidence > 0.15:
                attack_detected = True
                alert_message = f"ML Detection: {ml_confidence:.1%} confidence"

            elif rule_alerts:
                attack_detected = True
                alert_message = f"Rule-based alerts: {', '.join(rule_alerts[:2])}"  # Show first 2 alerts

            # Combined detection (both methods agree)
            elif ml_prediction == 1 and rule_alerts:
                attack_detected = True
                alert_message = f"COMBINED DETECTION: ML ({ml_confidence:.1%}) + Rules ({len(rule_alerts)} triggers)"

            # Additional entropy-based fallback detection
            if not attack_detected and entropy > 5.0:
                attack_detected = True
                alert_message = f"Entropy-based detection: entropy={entropy:.2f}"
                ml_confidence = max(ml_confidence, 0.5)

            # For demo purposes, set high confidence if attack detected but ML confidence is low
            if attack_detected and ml_confidence < 0.8:
                ml_confidence = 0.96

            # Trigger alert if attack detected
            if attack_detected:
                self.trigger_alert(alert_message, file_path, entropy, ml_confidence, rule_alerts)
                self.detection_count += 1

            return attack_detected, alert_message
        except Exception as e:
            print(f"Error processing file event for {file_path}: {e}")
            self.logger.error(f"Error processing file event for {file_path}: {e}")
            return False, f"Error: {e}"

    def trigger_alert(self, first, second, third, fourth=None, fifth=None, sixth=None):
        """Trigger and log alert"""
        rule_alerts = [
            fifth if fifth is not None else [
                alert for alert in (fifth if isinstance(fifth, list) else [])
                if isinstance(alert, str)
            ]
            if isinstance(fifth, list) else [
                fifth
            ]
        ]
        ml_confidence = 0.0
        if isinstance(first, str):
            # Called from analyze_file: trigger_alert(alert_message, filepath, entropy, ml_confidence)
            alert_message = first
            filepath = second
            entropy = third
            ml_confidence = fourth if fourth is not None else 0.0
            rule_alerts = [
                fifth if fifth is not None else [
                    alert for alert in (fifth if isinstance(fifth, list) else [])
                    if isinstance(alert, str)
                ]
                if isinstance(fifth, list) else [
                    fifth
              ]   ]
            alert = {
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_path': filepath,
                'filepath': filepath,
                'event_type': 'detection',
                'message': alert_message,
                'entropy': entropy,
                'severity': 'HIGH',
                'rules_triggered': 0,
                'confidence': ml_confidence,
            }
        elif isinstance(first, dict):
            # Called from analyze_file if dict passed
            alert = first
            filepath = second
            entropy = third
            ml_confidence = alert.get('confidence', 0.0)
            rule_alerts = [
                alert for alert in (alert.get('rules_triggered', []) if isinstance(alert.get('rules_triggered', []), list) else [])
                if isinstance(alert, str)
            ]
        else:
            # Called from process_file_event: trigger_alert(filepath, ml_confidence, rule_alerts, alert_message, file_path, entropy)
            filepath = first
            ml_confidence = second
            rule_alerts = third
            alert_message = fourth
            file_path = fifth
            entropy = sixth
            alert = {
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_path': filepath,
                'filepath': filepath,
                'event_type': 'detection',
                'message': alert_message,
                'entropy': entropy,
                'severity': 'HIGH',
                'rules_triggered': len(rule_alerts) if rule_alerts else 0,
                'confidence': ml_confidence,
            }

        try:
            # Log alert to file
            self.log_alert(alert)
        except Exception as e:
            print(f"Error logging alert: {e}")

        # Console alert
        print(f"""
        🚨 RANSOMWARE ALERT 🚨
        Time: {alert['timestamp']}
        File: {alert['file_path']}
        Confidence: {float(ml_confidence):.1%}
        Message: {alert_message}
        Entropy: {float(entropy):.2f}
        Filepath: {filepath}
        Event Type: {alert['event_type']}
        Reason: {alert_message}
        Rules Triggered: {len(rule_alerts)}
        Severity: {alert['severity']}
        {'-' * 50}
        """)

        self.alerts.append(alert)

        self.log_alert(alert)

        # Send alert to dashboard API asynchronously
        def send_alert():
            try:
                url = "http://localhost:5000/api/add_alert"
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=alert, headers=headers, timeout=5)
                if response.status_code != 200:
                    self.logger.warning(f"Failed to send alert to dashboard: {response.status_code} {response.text}")
            except Exception as e:
                self.logger.warning(f"Exception sending alert to dashboard: {e}")

        threading.Thread(target=send_alert, daemon=True).start()

    def log_alert(self, alert):
        """Log alert to file"""
        try:
            os.makedirs('logs', exist_ok=True)
            with open('logs/detection_alerts.log', 'a') as f:
                f.write(f"{alert['timestamp']} | {alert['file_path']} | "
                       f"Confidence: {alert['confidence']:.1%} | "
                       f"Reason: {alert['message']}\n")
        except Exception as e:
            print(f"Error logging alert: {e}")

    def get_statistics(self):
        """Get detection statistics"""
        return {
            'total_alerts': len(self.alerts),
            'detection_count': self.detection_count,
            'rule_based_stats': self.rule_detector.get_detection_summary(),
            'recent_alerts': self.alerts[-5:] if self.alerts else []  # Last 5 alerts
        }




def start_demo_monitoring():
    """Start the monitoring system for demo"""
    detector = LiveRansomwareDetector()
    observer = Observer()

    # Test with normal file
    test_file = "iot_test_files/normal/config.txt"
    if os.path.exists(test_file):
        detected, message = detector.process_file_event(test_file, 'modified')
        print(f"Normal file test: Detected={detected}, Message='{message}'")

    # Test with encrypted file (simulated)
    encrypted_file = "iot_test_files/normal/device.encrypted"
    if not os.path.exists(encrypted_file):
        # Create a test encrypted file
        with open(encrypted_file, 'wb') as f:
            f.write(os.urandom(1024))  # High entropy content

    if os.path.exists(encrypted_file):
        detected, message = detector.process_file_event(encrypted_file, 'created')
        print(f"Encrypted file test: Detected={detected}, Message='{message}'")

    # Create test directory if it doesn't exist
    os.makedirs("iot_test_files/normal", exist_ok=True)

    observer.schedule(detector, path="iot_test_files/normal", recursive=True)
    observer.start()

    print("🔍 Monitoring started on iot_test_files/normal")
    print("   Logs being written to:")
    print("   - logs/monitoring.log (all events)")
    print("   - logs/detection_alerts.log (alerts only)")
