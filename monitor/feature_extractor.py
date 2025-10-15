import pandas as pd
import os
import time
from datetime import datetime, timedelta
from monitor.entropy import file_entropy

class FeatureExtractor:
    def __init__(self, time_window_seconds=60):
        self.time_window = time_window_seconds
        self.activity_log = []
    
    def extract_file_features(self, filepath, event_type):
        """Extract features from a single file event"""
        try:
            stats = os.stat(filepath)
            
            features = {
                'timestamp': time.time(),
                'file_path': filepath,
                'file_name': os.path.basename(filepath),
                'file_size': stats.st_size,
                'entropy': file_entropy(filepath),
                'event_type': event_type,
                'file_extension': os.path.splitext(filepath)[1].lower(),
                'last_modified': stats.st_mtime,
                'access_count': 1  # Will be aggregated later
            }
            
            return features
            
        except Exception as e:
            print(f"Error extracting features from {filepath}: {e}")
            return None
    
    def aggregate_features(self, events_df):
        """Aggregate features over time window"""
        if events_df.empty:
            return None
        
        # Group by time windows
        events_df['time_bucket'] = (events_df['timestamp'] // self.time_window) * self.time_window
        
        aggregated = events_df.groupby('time_bucket').agg({
            'file_size': ['mean', 'std', 'max'],
            'entropy': ['mean', 'max', 'std'],
            'access_count': 'sum',
            'file_path': 'count'  # Number of files accessed
        }).round(4)
        
        # Flatten column names
        aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]
        aggregated = aggregated.reset_index()
        
        return aggregated

# Test the feature extractor
if __name__ == "__main__":
    extractor = FeatureExtractor()
    
    # Test with sample file
    test_file = "iot_test_files/file_0.txt"
    if os.path.exists(test_file):
        features = extractor.extract_file_features(test_file, 'test')
        print("Sample features:", features)