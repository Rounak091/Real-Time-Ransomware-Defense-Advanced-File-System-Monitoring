import time
import csv
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitor.entropy import file_entropy

class FileActivityHandler(FileSystemEventHandler):
    def __init__(self, log_file, label=0):
        self.log_file = log_file
        self.label = label  # 0 = normal, 1 = attack
        self.setup_csv()
        
    def setup_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'file_path', 'file_size', 'entropy',
                    'event_type', 'file_extension', 'label'
                ])
            print(f"✅ Created new log file: {self.log_file}")
    
    def log_event(self, event_type, file_path):
        """Log file event to CSV"""
        try:
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            entropy = file_entropy(file_path) if os.path.exists(file_path) else 0
            extension = os.path.splitext(file_path)[1].lower()
            
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    time.time(), file_path, file_size, entropy,
                    event_type, extension, self.label
                ])
            
            print(f"📝 Logged: {event_type} - {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"❌ Error logging event: {e}")
    
    def on_created(self, event):
        if not event.is_directory:
            self.log_event('created', event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.log_event('modified', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event('deleted', event.src_path)

def start_monitoring(directory, log_file, label=0):
    """Start monitoring a directory for file changes"""
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    event_handler = FileActivityHandler(log_file, label)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    print(f"👀 Started monitoring: {directory}")
    print(f"📄 Logging to: {log_file}")
    return observer

# Test function
def test_monitor():
    """Test the file monitoring system"""
    print("🧪 Testing File Monitor")
    monitor = start_monitoring("iot_test_files/normal", "data/normal_activity_log.csv", label=0)
    
    try:
        # Monitor for 10 seconds
        time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
        monitor.join()
        print("✅ Monitor test completed")

if __name__ == "__main__":
    test_monitor()