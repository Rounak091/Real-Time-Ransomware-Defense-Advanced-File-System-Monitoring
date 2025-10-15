# 🔒 Ransomware Detection in Smart Home Devices

A real-time ransomware detection system for IoT environments using machine learning and behavioral analysis.

## 🚀 Features

- **Real-time File Monitoring**: Continuous monitoring of file system activities
- **Machine Learning Detection**: Random Forest and SVM models with >95% accuracy
- **Hybrid Approach**: Combines ML with rule-based detection
- **Safe Testing Environment**: Isolated simulation without real system impact
- **Multi-channel Alerts**: Email, Slack, Discord, and SMS notifications
- **Web Dashboard**: Real-time monitoring and visualization
- **Performance Optimization**: Adaptive resource management

## 📁 Project Structure
iot-ransomware-detection/
├── monitor/ # Real-time detection system
├── models/ # Machine learning models
├── simulator/ # Safe attack simulation
├── dashboard/ # Web dashboard
├── iot_sim/ # IoT device simulation
├── data/ # Datasets and models
├── tests/ # Comprehensive test suite
├── scripts/ # Utility scripts
└── docs/ # Documentation

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- Mosquitto MQTT broker

### 1. Clone and Setup
```bash
git clone <repository-url>
cd iot-ransomware-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt