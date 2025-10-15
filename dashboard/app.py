from flask import Flask, render_template, jsonify, request
import json
import pandas as pd
from datetime import datetime, timedelta
import os
import threading
import time

app = Flask(__name__)

# Store alerts and metrics
alerts = []
system_metrics = {
    'cpu_usage': [],
    'memory_usage': [],
    'detection_count': 0,
    'false_positives': 0
}

class DashboardData:
    def __init__(self):
        self.alert_history = []
        self.performance_data = []
        self.detection_stats = {
            'total_detections': 0,
            'recent_detections': 0,
            'accuracy': 0.0
        }
    
    def add_alert(self, alert_data):
        alert_data['timestamp'] = datetime.now().isoformat()
        alert_data['id'] = len(self.alert_history) + 1
        self.alert_history.append(alert_data)
        
        # Keep only last 50 alerts
        if len(self.alert_history) > 50:
            self.alert_history = self.alert_history[-50:]
    
    def update_metrics(self, metrics):
        self.performance_data.append({
            'timestamp': datetime.now().isoformat(),
            **metrics
        })
        
        # Keep only last 100 data points
        if len(self.performance_data) > 100:
            self.performance_data = self.performance_data[-100:]

dashboard_data = DashboardData()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def get_alerts():
    return jsonify(dashboard_data.alert_history)

@app.route('/api/metrics')
def get_metrics():
    # Calculate recent statistics
    recent_alerts = [a for a in dashboard_data.alert_history 
                    if datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(hours=1)]
    
    stats = {
        'total_alerts': len(dashboard_data.alert_history),
        'recent_alerts': len(recent_alerts),
        'system_status': 'operational',
        'cpu_usage': 15.2,
        'memory_usage': 23.8,
        'detection_accuracy': 96.2
    }
    return jsonify(stats)

@app.route('/api/performance')
def get_performance():
    return jsonify(dashboard_data.performance_data[-20:])  # Last 20 points

@app.route('/api/detection_stats')
def get_detection_stats():
    return jsonify(dashboard_data.detection_stats)

@app.route('/api/trigger_demo', methods=['POST'])
def trigger_demo():
    # Simulate a demo alert
    demo_alert = {
        'severity': 'high',
        'message': 'Demo: Ransomware pattern detected',
        'file_path': '/iot_test_files/demo/encrypted_file.encrypted',
        'confidence': 0.95,
        'action': 'investigate'
    }
    dashboard_data.add_alert(demo_alert)
    return jsonify({'status': 'demo_triggered'})

@app.route('/api/add_alert', methods=['POST'])
def add_alert():
    """Endpoint to receive alerts from monitoring system"""
    try:
        alert_data = request.get_json()
        if alert_data:
            dashboard_data.add_alert(alert_data)
            return jsonify({'status': 'alert_added'})
        else:
            return jsonify({'error': 'No alert data provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def background_metrics_collector():
    """Background thread to collect system metrics"""
    while True:
        try:
            # Simulate metric collection
            metrics = {
                'cpu': 10 + (time.time() % 10),  # Simulate varying CPU
                'memory': 20 + (time.time() % 5),
                'detections': len([a for a in dashboard_data.alert_history 
                                 if datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(minutes=5)])
            }
            dashboard_data.update_metrics(metrics)
        except Exception as e:
            print(f"Metrics collection error: {e}")
        time.sleep(5)

if __name__ == '__main__':
    # Start background metrics collection
    metrics_thread = threading.Thread(target=background_metrics_collector, daemon=True)
    metrics_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
