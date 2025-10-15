import os
import time
import random
import string
from datetime import datetime

def simulate_normal_operations(directory="iot_test_files/normal", duration=60, operations_per_minute=10):
    """
    Simulate normal smart home device file operations
    - Reading config files
    - Writing log files  
    - Occasional file modifications
    - Normal access patterns
    """
    print(f"📁 Starting normal operations simulation in: {directory}")
    print(f"⏱️  Duration: {duration} seconds, Operations: {operations_per_minute}/minute")
    
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Get list of existing files or create some if none exist
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if len(files) == 0:
        print("⚠️  No files found, creating sample files...")
        files = create_sample_files(directory, 20)
    
    print(f"📊 Operating on {len(files)} files")
    
    start_time = time.time()
    operation_count = 0
    
    while (time.time() - start_time) < duration:
        try:
            # Randomly choose an operation type
            operation = random.choice(['read', 'write', 'modify', 'create', 'delete'])
            
            if operation == 'read' and files:
                # Simulate reading a file
                file_to_read = random.choice(files)
                file_path = os.path.join(directory, file_to_read)
                simulate_file_read(file_path)
                
            elif operation == 'write' and files:
                # Simulate writing to a file (append)
                file_to_write = random.choice(files)
                file_path = os.path.join(directory, file_to_write)
                simulate_file_write(file_path)
                
            elif operation == 'modify' and files:
                # Simulate modifying a file
                file_to_modify = random.choice(files)
                file_path = os.path.join(directory, file_to_modify)
                simulate_file_modify(file_path)
                
            elif operation == 'create':
                # Create a new file
                new_filename = f"log_{int(time.time())}_{random.randint(1000,9999)}.txt"
                file_path = os.path.join(directory, new_filename)
                simulate_file_create(file_path)
                files.append(new_filename)
                
            elif operation == 'delete' and len(files) > 5:
                # Delete a file (but keep minimum 5 files)
                file_to_delete = random.choice(files)
                file_path = os.path.join(directory, file_to_delete)
                simulate_file_delete(file_path)
                files.remove(file_to_delete)
            
            operation_count += 1
            print(f"🔧 Operation {operation_count}: {operation}")
            
            # Wait between operations to maintain rate
            time_between_ops = 60.0 / operations_per_minute
            time.sleep(time_between_ops)
            
        except Exception as e:
            print(f"❌ Error during operation: {e}")
            continue
    
    print(f"✅ Normal operations simulation completed!")
    print(f"📈 Total operations performed: {operation_count}")
    return operation_count

def create_sample_files(directory, num_files=20):
    """Create sample files for simulation"""
    files_created = []
    
    for i in range(num_files):
        # Create different types of files
        if i % 4 == 0:
            filename = f"config_device_{i}.cfg"
            content = f"[Device_{i}]\nport=8080\ntimeout=30\nretries=3\nstatus=active"
        elif i % 4 == 1:
            filename = f"sensor_data_{i}.json"
            content = f'{{"sensor_id": {i}, "temperature": {random.uniform(20, 30):.1f}, "humidity": {random.uniform(40, 80):.1f}}}'
        elif i % 4 == 2:
            filename = f"system_log_{i}.log"
            content = f"{datetime.now().isoformat()} - Device {i} operational\nMemory usage: {random.randint(30, 70)}%\nError count: 0"
        else:
            filename = f"backup_data_{i}.dat"
            content = f"Backup created at {datetime.now().isoformat()}\n" + "".join(random.choices(string.ascii_letters + string.digits, k=100))
        
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        files_created.append(filename)
    
    print(f"✅ Created {len(files_created)} sample files")
    return files_created

def simulate_file_read(file_path):
    """Simulate reading a file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Simulate processing time
        time.sleep(random.uniform(0.01, 0.1))
        return True
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def simulate_file_write(file_path):
    """Simulate writing to a file (append)"""
    try:
        with open(file_path, 'a') as f:
            timestamp = datetime.now().isoformat()
            log_entry = f"\n{timestamp} - Normal operation completed"
            f.write(log_entry)
        time.sleep(random.uniform(0.02, 0.15))
        return True
    except Exception as e:
        print(f"❌ Error writing to {file_path}: {e}")
        return False

def simulate_file_modify(file_path):
    """Simulate modifying a file"""
    try:
        # Read current content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Modify slightly (add timestamp)
        modified_content = content + f"\n# Last updated: {datetime.now().isoformat()}"
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(modified_content)
        
        time.sleep(random.uniform(0.03, 0.2))
        return True
    except Exception as e:
        print(f"❌ Error modifying {file_path}: {e}")
        return False

def simulate_file_create(file_path):
    """Simulate creating a new file"""
    try:
        content = f"File created at: {datetime.now().isoformat()}\n"
        content += "Normal system operation log\n"
        content += "=" * 40 + "\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        time.sleep(random.uniform(0.05, 0.25))
        return True
    except Exception as e:
        print(f"❌ Error creating {file_path}: {e}")
        return False

def simulate_file_delete(file_path):
    """Simulate deleting a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            time.sleep(random.uniform(0.01, 0.1))
            return True
        return False
    except Exception as e:
        print(f"❌ Error deleting {file_path}: {e}")
        return False

# Test function
def test_normal_operations():
    """Test the normal operations simulation"""
    print("🧪 Testing Normal Operations Simulation")
    operations = simulate_normal_operations(duration=10, operations_per_minute=2)
    print(f"Test completed with {operations} operations")

if __name__ == "__main__":
    test_normal_operations()