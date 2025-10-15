#!/usr/bin/env python3
"""
Simulate normal smart home device activity
"""

import time
import random
import os
from datetime import datetime

def simulate_normal_operations(directory="iot_test_files/normal", duration=300, operations_per_minute=5):
    """Simulate normal file operations for smart home devices"""
    print(f"📊 Simulating normal activity for {duration} seconds...")
    
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    operations = 0
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Random file operations
        operation = random.choice(['create', 'modify', 'read'])
        file_id = random.randint(0, 50)
        
        if operation == 'create':
            filename = f"{directory}/config_{file_id}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"Device configuration created at {datetime.now()}")
            print(f"   Created: {os.path.basename(filename)}")
        
        elif operation == 'modify':
            # Try to modify an existing file or create new one
            existing_files = [f for f in os.listdir(directory) if f.startswith('config_')]
            if existing_files:
                filename = os.path.join(directory, random.choice(existing_files))
                with open(filename, 'a') as f:
                    f.write(f"\nUpdated at {datetime.now()}")
                print(f"   Modified: {os.path.basename(filename)}")
            else:
                # Create new file if no existing files
                filename = f"{directory}/config_{file_id}_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Device configuration created at {datetime.now()}")
                print(f"   Created: {os.path.basename(filename)}")
        
        operations += 1
        time.sleep(60 / operations_per_minute)  # Spread operations evenly
    
    print(f"✅ Normal activity completed: {operations} operations")

def simulate_normal_activity():
    """Main function to run normal activity simulation"""
    simulate_normal_operations(
        directory="iot_test_files/normal", 
        duration=300,  # 5 minutes
        operations_per_minute=5
    )

if __name__ == "__main__":
    simulate_normal_activity()