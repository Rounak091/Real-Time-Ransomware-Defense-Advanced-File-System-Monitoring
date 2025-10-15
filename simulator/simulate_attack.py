import os
import random
import shutil
from datetime import datetime
import requests
import threading

def simulate_ransomware_attack(source_dir="iot_test_files", target_dir="iot_test_files/normal", attack_intensity=0.3):
    """
    SAFE ransomware simulation - creates high-entropy copies without real encryption
    """
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"❌ ERROR: Source directory '{source_dir}' does not exist!")
        print("Please run generate_dummy_files.py first")
        return 0
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    print(f"✅ Created target directory: {target_dir}")
    
    # Get list of files from source directory
    try:
        files = [f for f in os.listdir(source_dir) 
                 if os.path.isfile(os.path.join(source_dir, f))]
        print(f"📁 Found {len(files)} files in source directory")
    except Exception as e:
        print(f"❌ Error reading source directory: {e}")
        return 0
    
    if len(files) == 0:
        print("❌ No files found to attack!")
        return 0
    
    # Select random files to "encrypt" based on attack intensity
    num_files_to_attack = max(1, int(len(files) * attack_intensity))
    files_to_attack = random.sample(files, num_files_to_attack)
    
    print(f"🔒 Simulating ransomware attack on {num_files_to_attack} files...")
    
    attacked_count = 0
    for filename in files_to_attack:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename + ".encrypted")
        
        try:
            # Read original file size
            original_size = os.path.getsize(source_path)
            
            # Create high-entropy file (simulates encryption)
            with open(target_path, 'wb') as f:
                f.write(os.urandom(original_size))  # Random bytes = high entropy
            
            print(f"   ✅ Encrypted: {filename} -> {filename}.encrypted")
            attacked_count += 1

            # Send alert to dashboard for each attacked file
            send_alert_to_dashboard(target_path, filename)
            
        except Exception as e:
            print(f"   ❌ Failed to encrypt {filename}: {e}")
    
    # Create ransom note
    ransom_note_path = os.path.join(target_dir, "READ_ME_FOR_DECRYPT.txt")
    with open(ransom_note_path, 'w') as f:
        f.write("=== SAFE SIMULATION ONLY ===\n")
        f.write("This is a simulated ransomware attack for research purposes.\n")
        f.write("No actual files have been encrypted.\n")
        f.write(f"Attack simulated at: {datetime.now()}\n")
        f.write(f"Files affected: {attacked_count}\n")
    
    print(f"🎯 Ransomware simulation complete. Created {attacked_count} encrypted files.")
    print(f"📝 Ransom note created: {ransom_note_path}")
    print(f"🚨 Sent {attacked_count} alerts to dashboard")

    return attacked_count

def send_alert_to_dashboard(file_path, original_filename):
    """Send alert to dashboard for attacked file"""
    def send_alert():
        try:
            alert_data = {
                'timestamp': datetime.now().isoformat(),
                'file_path': file_path,
                'filepath': file_path,
                'event_type': 'ransomware_attack',
                'message': f'Ransomware attack detected: {original_filename} encrypted',
                'entropy': 7.8,  # High entropy for encrypted files
                'severity': 'HIGH',
                'rules_triggered': 1,
                'confidence': 0.95
            }

            url = "http://localhost:5000/api/add_alert"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=alert_data, headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"   🚨 Alert sent to dashboard: {original_filename}")
            else:
                print(f"   ⚠️  Failed to send alert to dashboard: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Exception sending alert: {e}")

    # Send alert asynchronously
    threading.Thread(target=send_alert, daemon=True).start()

if __name__ == "__main__":
    print("🚀 Starting Safe Ransomware Simulation")
    print("=" * 50)
    
    # Run the simulation
    result = simulate_ransomware_attack(
        source_dir="iot_test_files",
        target_dir="iot_test_files/normal", 
        attack_intensity=0.4
    )
    
    if result > 0:
        print(f"✅ Simulation successful! {result} files attacked.")
        print("\nTo verify, run: ls -la iot_test_files/normal/")
    else:
        print("❌ Simulation failed. Please check the errors above.")