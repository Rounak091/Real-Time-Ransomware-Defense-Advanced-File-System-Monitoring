#!/bin/bash

# IoT Ransomware Detection System - Complete Demo Script
# This script launches all components of the system in separate terminals
# Run this script to demonstrate the full project functionality

echo "🚀 Starting IoT Ransomware Detection System Demo"
echo "=================================================="
echo ""

# Function to check if we're in the right directory
check_directory() {
    if [ ! -f "dashboard/app.py" ]; then
        echo "❌ Error: Please run this script from the project root directory (iot-ransomware-detection)"
        exit 1
    fi
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        echo "❌ Error: Virtual environment not found. Please run setup_environment.py first."
        exit 1
    fi
}

# Function to open terminal with command
open_terminal() {
    local title="$1"
    local command="$2"

    echo "📱 Opening terminal: $title"
    gnome-terminal --title="$title" -- bash -c "$command; echo '✅ Operation completed. Press Ctrl+C to exit.'; exec bash" &
    sleep 1
}

# Main demo function
run_demo() {
    echo "🔧 Checking prerequisites..."
    check_directory
    check_venv

    echo "✅ Prerequisites OK"
    echo ""

    # Terminal 1: Environment Setup & Training Pipeline
    open_terminal "Setup & Training" "
        echo '🔧 Setting up environment...';
        source venv/bin/activate;
        echo '📊 Running training pipeline...';
        python scripts/run_training_pipeline.py;
        echo '✅ Training completed!';
        echo '';
        echo 'Press Enter to continue...';
        read
    "

    # Terminal 2: File Monitor (Detection System)
    open_terminal "File Monitor" "
        echo '👁️  Starting file monitoring system...';
        source venv/bin/activate;
        echo 'Monitoring directories: iot_test_files/normal, iot_test_files/attacked';
        python monitor/file_monitor.py;
    "

    # Terminal 3: Live Ransomware Detector
    open_terminal "Live Detector" "
        echo '🛡️  Starting live ransomware detector...';
        source venv/bin/activate;
        python monitor/live_detector.py;
    "

    # Terminal 4: Dashboard Server
    open_terminal "Dashboard Server" "
        echo '🌐 Starting web dashboard server...';
        source venv/bin/activate;
        echo 'Dashboard will be available at: http://localhost:5000';
        python dashboard/app.py;
    "

    # Terminal 5: Normal Activity Simulation
    open_terminal "Normal Activity" "
        echo '🏠 Simulating normal IoT device activity...';
        source venv/bin/activate;
        sleep 5;
        echo 'Starting normal activity simulation...';
        python scripts/run_normal_activity.py;
    "

    # Terminal 6: Demo Attack Script
    open_terminal "Demo Attack" "
        echo '🦠 Preparing ransomware attack simulation...';
        source venv/bin/activate;
        sleep 10;
        echo 'Launching demo attack in 5 seconds...';
        sleep 5;
        python scripts/demo_attack.py;
    "

    # Terminal 7: Test Suite
    open_terminal "Test Suite" "
        echo '🧪 Running comprehensive test suite...';
        source venv/bin/activate;
        sleep 15;
        echo 'Running UI tests...';
        pytest tests/ui_test_dashboard.py -v;
        echo '';
        echo 'Running integration tests...';
        pytest tests/integration_test_dashboard.py -v;
    "
    # Terminal 8: Performance Monitoring (Optional)
    open_terminal "Performance Monitor" "
        echo '📈 Starting performance monitoring...';
        source venv/bin/activate;
        python dashboard/app.py &
        python monitor/performance_monitor.py;
    "
    
    echo ""
    echo "🎯 DEMO COMPONENTS LAUNCHED!"
    echo "============================"
    echo ""
    echo "📋 Active Components:"
    echo "  1. Setup & Training Pipeline"
    echo "  2. File Monitor (Detection System)"
    echo "  3. Live Ransomware Detector"
    echo "  4. Web Dashboard Server"
    echo "  5. Normal Activity Simulator"
    echo "  6. Demo Attack Script"
    echo "  7. Test Suite Runner"
    echo ""
    echo "🌐 Dashboard URL: http://localhost:5000"
    echo ""
    echo "📊 What to expect:"
    echo "  - Dashboard shows real-time monitoring"
    echo "  - Normal activity generates benign file operations"
    echo "  - Demo attack triggers ransomware detection"
    echo "  - Alerts appear in dashboard and logs"
    echo "  - Tests verify system functionality"
    echo ""
    echo "⚡ The system will detect:"
    echo "  - High entropy file creation (ransomware behavior)"
    echo "  - Rapid file modifications"
    echo "  - Suspicious access patterns"
    echo ""
    echo "🔄 All components are running in separate terminals."
    echo "   Close terminals when demo is complete."
    echo ""
}

# Run the demo
run_demo
