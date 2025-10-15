import os
import random
import string

def create_test_environment():
    """Create test directory with dummy files"""
    # Create test directory
    test_dir = "iot_test_files"
    os.makedirs(test_dir, exist_ok=True)
    print(f"✅ Created directory: {test_dir}")
    
    # Create various file types to simulate smart home environment
    file_types = {
        'txt': 50,    # Configuration files
        'json': 30,    # Device settings  
        'log': 20,     # Log files
        'cfg': 10,     # Config files
        'dat': 10      # Data files
    }
    
    file_id = 0
    total_files = 0
    
    for extension, count in file_types.items():
        for i in range(count):
            filename = f"device_{file_id:03d}.{extension}"
            filepath = os.path.join(test_dir, filename)
            
            # Generate realistic content based on file type
            if extension == 'txt':
                content = f"Configuration settings for device {file_id}\n" + \
                         f"temperature_threshold=25\nhumidity_limit=60%\n" + \
                         "device_status=active\nupdate_interval=30s"
            elif extension == 'json':
                content = f'{{"device_id": {file_id}, "status": "active", "values": [1, 2, 3]}}'
            elif extension == 'log':
                content = f"2024-01-15 10:30:{file_id} - Device operational\nError count: 0\nMemory usage: 45%"
            elif extension == 'cfg':
                content = f"[Device_{file_id}]\nport=8080\ntimeout=30\nretries=3"
            else:
                content = "Sample binary data " + "".join(random.choices(string.printable, k=200))
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            file_id += 1
            total_files += 1
    
    print(f"✅ Created {total_files} test files in {test_dir}")
    print("📁 File types created:")
    for ext, count in file_types.items():
        print(f"   - {ext}: {count} files")
    
    return total_files

if __name__ == "__main__":
    print("📂 Generating Dummy Files for Testing")
    print("=" * 40)
    
    count = create_test_environment()
    print(f"\n🎉 Successfully created {count} files!")
    print("\nTo verify, run: ls -la iot_test_files/")