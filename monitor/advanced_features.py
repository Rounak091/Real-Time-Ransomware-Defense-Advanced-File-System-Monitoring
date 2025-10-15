import numpy as np
from collections import deque
import time

class AdvancedFeatureEngine:
    def __init__(self, window_size=60):  # 60-second window
        self.window_size = window_size
        self.event_window = deque(maxlen=1000)  # Store recent events
        self.file_access_patterns = {}
    
    def update_event_window(self, file_path, event_type, entropy, file_size):
        """Update sliding window of events"""
        event = {
            'timestamp': time.time(),
            'file_path': file_path,
            'event_type': event_type,
            'entropy': entropy,
            'file_size': file_size
        }
        self.event_window.append(event)
    
    def calculate_advanced_features(self):
        """Calculate advanced behavioral features"""
        current_time = time.time()
        window_start = current_time - self.window_size
        
        # Events in current window
        recent_events = [e for e in self.event_window 
                        if e['timestamp'] >= window_start]
        
        features = {
            'events_per_second': len(recent_events) / self.window_size,
            'avg_entropy_window': np.mean([e['entropy'] for e in recent_events]),
            'unique_files_accessed': len(set(e['file_path'] for e in recent_events)),
            'encryption_like_pattern': self.detect_encryption_pattern(recent_events)
        }
        
        return features
    
    def detect_encryption_pattern(self, events):
        """Detect patterns typical of encryption behavior"""
        if len(events) < 5:
            return 0
        
        # Check for rapid sequential modifications with increasing entropy
        high_entropy_events = sum(1 for e in events if e['entropy'] > 7.0)
        pattern_score = high_entropy_events / len(events)
        
        return 1 if pattern_score > 0.8 else 0