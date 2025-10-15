import os
import time
from collections import defaultdict

class RuleBasedDetector:
    def __init__(self):
        # Threshold configurations
        self.entropy_threshold = 7.5  # Files above this entropy are suspicious
        self.access_threshold = 10    # Max files per minute
        self.modification_threshold = 8  # Max modifications per minute
        self.encrypted_extension_threshold = 5  # Max .encrypted files per minute
        
        # Tracking for rate limiting
        self.access_timestamps = defaultdict(list)
        self.modification_timestamps = defaultdict(list)
        self.encrypted_files_created = defaultdict(list)
        self.recent_entropies = []  # Track entropies for rapid access check
        
        # Time window in seconds
        self.time_window = 60  # 1 minute
    
    def detect_anomaly(self, file_path, event_type, entropy, file_size):
        """
        Rule-based anomaly detection
        Returns: list of alert messages if anomalies detected
        """
        alerts = []
        current_time = time.time()

        # Update tracking
        self._update_tracking(file_path, event_type, current_time, entropy)
        
        # Rule 1: High Entropy Detection
        if entropy > self.entropy_threshold:
            alerts.append(f"High entropy detected: {entropy:.2f} (threshold: {self.entropy_threshold})")
        
        # Rule 2: Rapid File Access
        recent_accesses = self._get_recent_events(self.access_timestamps, current_time)
        if recent_accesses > self.access_threshold:
            # Calculate average entropy of recent files
            recent_entropy_values = [e for t, e in self.recent_entropies if current_time - t <= self.time_window]
            avg_entropy = sum(recent_entropy_values) / len(recent_entropy_values) if recent_entropy_values else 0
            if avg_entropy > 5.0:  # Only alert if average entropy > 5.0
                alerts.append(f"Rapid file access: {recent_accesses} files/min (threshold: {self.access_threshold}, avg entropy: {avg_entropy:.2f})")
        
        # Rule 3: Many File Modifications
        recent_modifications = self._get_recent_events(self.modification_timestamps, current_time)
        if recent_modifications > self.modification_threshold:
            alerts.append(f"Many file modifications: {recent_modifications} mods/min (threshold: {self.modification_threshold})")
        
        # Rule 4: Multiple Encrypted Files Created
        if event_type == 'created' and file_path.endswith('.encrypted'):
            recent_encrypted = self._get_recent_events(self.encrypted_files_created, current_time)
            if recent_encrypted > self.encrypted_extension_threshold:
                alerts.append(f"Multiple encrypted files created: {recent_encrypted} files/min (threshold: {self.encrypted_extension_threshold})")
        
        # Rule 5: Ransom Note Detection
        if self._is_ransom_note(file_path):
            alerts.append(f"Ransom note detected: {os.path.basename(file_path)}")
        
        # Rule 6: Suspicious File Size Changes
        if event_type == 'modified' and self._suspicious_size_change(file_path, file_size):
            alerts.append(f"Suspicious file size change: {file_path}")
        
        return alerts
    
    def _update_tracking(self, file_path, event_type, current_time, entropy=None):
        """Update tracking dictionaries with current event"""
        if event_type in ['created', 'modified', 'accessed']:
            self.access_timestamps['all_events'].append(current_time)
            if entropy is not None:
                self.recent_entropies.append((current_time, entropy))

        if event_type == 'modified':
            self.modification_timestamps['all_events'].append(current_time)

        if event_type == 'created' and file_path.endswith('.encrypted'):
            self.encrypted_files_created['all_events'].append(current_time)

        # Clean old events (older than time_window)
        self._clean_old_events(current_time)
    
    def _get_recent_events(self, event_dict, current_time):
        """Count events in the recent time window"""
        key = 'all_events'
        if key not in event_dict:
            return 0
        
        recent_events = [
            ts for ts in event_dict[key] 
            if current_time - ts <= self.time_window
        ]
        return len(recent_events)
    
    def _clean_old_events(self, current_time):
        """Remove events older than the time window"""
        for event_dict in [self.access_timestamps, self.modification_timestamps, self.encrypted_files_created]:
            for key in list(event_dict.keys()):
                event_dict[key] = [
                    ts for ts in event_dict[key]
                    if current_time - ts <= self.time_window
                ]
        # Clean recent entropies
        self.recent_entropies = [
            (t, e) for t, e in self.recent_entropies
            if current_time - t <= self.time_window
        ]
    
    def _is_ransom_note(self, file_path):
        """Check if file appears to be a ransom note"""
        ransom_indicators = [
            'readme', 'decrypt', 'ransom', 'recover', 'payment',
            'bitcoin', 'crypto', 'unlock', 'help_restore', 'how_to_recover'
        ]
        
        filename = os.path.basename(file_path).lower()
        
        # Check filename for ransom indicators
        for indicator in ransom_indicators:
            if indicator in filename:
                return True
        
        # Check file content if it's a text file
        if filename.endswith(('.txt', '.html', '.htm')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000).lower()  # Read first 1000 chars
                    for indicator in ransom_indicators:
                        if indicator in content:
                            return True
            except:
                pass
        
        return False
    
    def _suspicious_size_change(self, file_path, new_size):
        """
        Detect suspicious file size changes
        Encrypted files often have different size patterns
        """
        # Very small or very large size changes might be suspicious
        if new_size == 0:
            return True  # File emptied
        
        # Check if size changed dramatically (placeholder logic)
        # In a real implementation, you'd track previous file sizes
        return False
    
    def get_detection_summary(self):
        """Get current detection statistics"""
        current_time = time.time()
        
        return {
            'recent_accesses': self._get_recent_events(self.access_timestamps, current_time),
            'recent_modifications': self._get_recent_events(self.modification_timestamps, current_time),
            'recent_encrypted_creations': self._get_recent_events(self.encrypted_files_created, current_time),
            'entropy_threshold': self.entropy_threshold,
            'access_threshold': self.access_threshold,
            'modification_threshold': self.modification_threshold
        }