import paho.mqtt.client as mqtt
import json
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("localhost", 1883, 60)
        
    def send_alert(self, severity, message, file_path, confidence):
        """Send alert via multiple channels"""
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'file_path': file_path,
            'confidence': confidence,
            'action': 'investigate'
        }
        
        # MQTT Alert
        self.mqtt_client.publish("home/security/alerts", json.dumps(alert_data))
        
        # Console Alert
        print(f"""
        ⚠️  SECURITY ALERT ⚠️
        Time: {alert_data['timestamp']}
        Severity: {severity}
        Message: {message}
        File: {file_path}
        Confidence: {confidence:.2%}
        """)
        
        # Log file
        self.log_alert(alert_data)
    
    def log_alert(self, alert_data):
        with open('logs/security_alerts.jsonl', 'a') as f:
            f.write(json.dumps(alert_data) + '\n')