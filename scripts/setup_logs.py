#!/usr/bin/env python3
"""
Quick script to create log files and directories
"""

import os
import datetime

def setup_logs():
    print("📁 Setting up log system...")
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Create log files with headers
    log_files = {
        'monitoring.log': 'MONITORING LOG - Ransomware Detection System\n' +
                         '=' * 50 + '\n' +
                         'Timestamp - Level - Message\n' +
                         '=' * 50 + '\n',
        
        'detection_alerts.log': 'DETECTION ALERTS LOG - Ransomware Detection System\n' +
                               '=' * 50 + '\n' +
                               'Timestamp - ALERT - Message\n' +
                               '=' * 50 + '\n',
        
        'system.log': 'SYSTEM LOG - Ransomware Detection System\n' +
                     '=' * 50 + '\n' +
                     'System startup and shutdown events\n' +
                     '=' * 50 + '\n'
    }
    
    for filename, header in log_files.items():
        filepath = os.path.join('logs', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(header)
            print(f"✅ Created: logs/{filename}")
        else:
            print(f"📄 Already exists: logs/{filename}")
    
    # Add startup entry
    with open('logs/system.log', 'a') as f:
        f.write(f"{datetime.datetime.now()} - SYSTEM - Log system initialized\n")
    
    print("\n🎯 Log files are ready!")
    print("   You can now run: tail -f logs/monitoring.log")

if __name__ == "__main__":
    setup_logs()