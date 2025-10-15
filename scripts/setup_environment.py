#!/usr/bin/env python3
"""
Environment setup script for Ransomware Detection System
Creates necessary directories, configuration files, and verifies dependencies
"""

import os
import sys
import json
import subprocess
import platform

class EnvironmentSetup:
    def __init__(self):
        self.required_dirs = [
            'data/raw',
            'data/processed',
            'data/models',
            'logs',
            'config',
            'backups',
            'dashboard/static',
            'dashboard/templates',
            'iot_test_files/normal',
            'iot_test_files/attacked',
            'iot_test_files/backups'
        ]
        
        self.required_packages = [
            'paho-mqtt',
            'watchdog', 
            'pandas',
            'numpy',
            'scikit-learn',
            'matplotlib',
            'seaborn',
            'cryptography',
            'joblib',
            'flask',
            'psutil',
            'requests'
        ]

    def setup_directories(self):
        """Create all required directories"""
        print("📁 Creating directory structure...")
        
        for directory in self.required_dirs:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"  ✅ Created: {directory}")
            except Exception as e:
                print(f"  ❌ Failed to create {directory}: {e}")
                return False
        return True

    def check_python_version(self):
        """Check Python version compatibility"""
        print("🐍 Checking Python version...")
        
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"  ❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
            return False

    def install_dependencies(self):
        """Install required Python packages"""
        print("📦 Installing dependencies...")
        
        try:
            # First, try to install from requirements.txt if it exists
            if os.path.exists('requirements.txt'):
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("  ✅ Installed from requirements.txt")
            else:
                # Install packages individually
                for package in self.required_packages:
                    try:
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                        print(f"  ✅ Installed: {package}")
                    except subprocess.CalledProcessError:
                        print(f"  ⚠️  Failed to install: {package}")
            
            return True
        except Exception as e:
            print(f"  ❌ Dependency installation failed: {e}")
            return False

    def create_config_files(self):
        """Create default configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Alert configuration
        alert_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "your_email@gmail.com",
                "sender_password": "your_app_password",
                "recipient_emails": ["admin@yourdomain.com"]
            },
            "webhook": {
                "enabled": True,
                "slack_webhook": "https://hooks.slack.com/services/XXX/XXX/XXX",
                "discord_webhook": "https://discord.com/api/webhooks/XXX/XXX"
            },
            "sms": {
                "enabled": False,
                "twilio_sid": "your_twilio_sid",
                "twilio_token": "your_twilio_token",
                "twilio_number": "+1234567890",
                "recipient_numbers": ["+1234567890"]
            }
        }
        
        # Monitor configuration
        monitor_config = {
            "monitoring_paths": [
                "iot_test_files/normal",
                "iot_test_files/attacked"
            ],
            "entropy_threshold": 7.5,
            "access_threshold": 10,
            "check_interval": 1.0,
            "max_file_size_mb": 10,
            "log_level": "INFO"
        }
        
        # Dashboard configuration
        dashboard_config = {
            "host": "0.0.0.0",
            "port": 5000,
            "debug": False,
            "refresh_interval": 5000
        }
        
        configs = {
            'config/alert_config.json': alert_config,
            'config/monitor_config.json': monitor_config,
            'config/dashboard_config.json': dashboard_config
        }
        
        try:
            for config_file, config_data in configs.items():
                with open(config_file, 'w') as f:
                    json.dump(config_data, f, indent=2)
                print(f"  ✅ Created: {config_file}")
            return True
        except Exception as e:
            print(f"  ❌ Config creation failed: {e}")
            return False

    def check_mqtt_broker(self):
        """Check if MQTT broker is available"""
        print("📡 Checking MQTT broker...")
        
        system = platform.system().lower()
        
        if system == 'linux':
            try:
                # Check if mosquitto is installed and running
                result = subprocess.run(['systemctl', 'is-active', 'mosquitto'], 
                                      capture_output=True, text=True)
                if result.stdout.strip() == 'active':
                    print("  ✅ Mosquitto MQTT broker is running")
                    return True
                else:
                    print("  ⚠️  Mosquitto not running. Attempting to install and start mosquitto...")
                    # Try to install mosquitto and mosquitto-clients
                    install_result = subprocess.run(['sudo', 'apt', 'install', '-y', 'mosquitto', 'mosquitto-clients'])
                    if install_result.returncode != 0:
                        print("  ❌ Failed to install mosquitto. Please install manually.")
                        return False
                    # Start and enable mosquitto service
                    subprocess.run(['sudo', 'systemctl', 'start', 'mosquitto'])
                    subprocess.run(['sudo', 'systemctl', 'enable', 'mosquitto'])
                    # Re-check status
                    result = subprocess.run(['systemctl', 'is-active', 'mosquitto'], capture_output=True, text=True)
                    if result.stdout.strip() == 'active':
                        print("  ✅ Mosquitto MQTT broker installed and running")
                        return True
                    else:
                        print("  ❌ Mosquitto service failed to start. Please check manually.")
                        return False
            except Exception as e:
                print(f"  ⚠️  Could not check MQTT broker status: {e}")
                return False
        else:
            print("  ⚠️  MQTT broker check skipped (non-Linux system)")
            return True

    def create_sample_files(self):
        """Create sample test files"""
        print("📄 Creating sample test files...")
        
        try:
            # Create sample Python files for testing
            sample_files = {
                'iot_test_files/normal/config.txt': 'device_name=smart_camera\ntemperature_threshold=25\n',
                'iot_test_files/normal/settings.json': '{"device_id": 1, "status": "active", "version": "1.0"}',
                'iot_test_files/normal/app.log': '2024-01-15 10:30:00 - Device started\n2024-01-15 10:31:00 - Temperature: 24.5C'
            }
            
            for file_path, content in sample_files.items():
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"  ✅ Created: {file_path}")
            
            return True
        except Exception as e:
            print(f"  ❌ Sample file creation failed: {e}")
            return False

    def verify_setup(self):
        """Verify the setup was successful"""
        print("\n🔍 Verifying setup...")
        
        checks = [
            ("Directory structure", self.verify_directories),
            ("Python packages", self.verify_packages),
            ("Configuration files", self.verify_configs),
            ("Sample files", self.verify_sample_files)
        ]
        
        all_checks_passed = True
        
        for check_name, check_function in checks:
            try:
                if check_function():
                    print(f"  ✅ {check_name}: OK")
                else:
                    print(f"  ❌ {check_name}: FAILED")
                    all_checks_passed = False
            except Exception as e:
                print(f"  ❌ {check_name}: ERROR - {e}")
                all_checks_passed = False
        
        return all_checks_passed

    def verify_directories(self):
        """Verify all directories were created"""
        for directory in self.required_dirs:
            if not os.path.exists(directory):
                return False
        return True

    def verify_packages(self):
        """Verify required packages are installed"""
        # Map package names to their import names
        import_names = {
            'paho-mqtt': 'paho.mqtt',
            'scikit-learn': 'sklearn',
            'watchdog': 'watchdog',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'cryptography': 'cryptography',
            'joblib': 'joblib',
            'flask': 'flask',
            'psutil': 'psutil',
            'requests': 'requests'
        }

        for package in self.required_packages:
            import_name = import_names.get(package, package)
            try:
                __import__(import_name)
            except ImportError:
                return False
        return True

    def verify_configs(self):
        """Verify configuration files exist"""
        config_files = [
            'config/alert_config.json',
            'config/monitor_config.json',
            'config/dashboard_config.json'
        ]
        return all(os.path.exists(f) for f in config_files)

    def verify_sample_files(self):
        """Verify sample files were created"""
        sample_files = [
            'iot_test_files/normal/config.txt',
            'iot_test_files/normal/settings.json',
            'iot_test_files/normal/app.log'
        ]
        return all(os.path.exists(f) for f in sample_files)

    def display_next_steps(self):
        """Display next steps after setup"""
        print("\n🎯 NEXT STEPS:")
        print("=" * 50)
        print("1. Train ML models:")
        print("   python scripts/run_training_pipeline.py")
        print()
        print("2. Start the detection system:")
        print("   python monitor/file_monitor.py")
        print("   python monitor/live_detector.py")
        print()
        print("3. Launch web dashboard:")
        print("   python dashboard/app.py")
        print()
        print("4. Run a demo:")
        print("   python scripts/demo_attack.py")
        print()
        print("5. View dashboard at: http://localhost:5000")
        print()
        print("📝 Don't forget to:")
        print("   - Configure alert_config.json with your email/Slack settings")
        print("   - Update monitor_config.json with your monitoring paths")
        print("   - Install MQTT broker if needed: sudo apt install mosquitto")

    def run_setup(self):
        """Run complete setup process"""
        print("🚀 RANSOMWARE DETECTION - ENVIRONMENT SETUP")
        print("=" * 60)
        
        steps = [
            ("Python version check", self.check_python_version),
            ("Directory setup", self.setup_directories),
            ("Dependency installation", self.install_dependencies),
            ("Configuration setup", self.create_config_files),
            ("MQTT broker check", self.check_mqtt_broker),
            ("Sample files", self.create_sample_files),
            ("Setup verification", self.verify_setup)
        ]
        
        for step_name, step_function in steps:
            print(f"\n{step_name}...")
            if not step_function():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 ENVIRONMENT SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        self.display_next_steps()
        return True

def main():
    """Main setup function"""
    setup = EnvironmentSetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()