# scripts/final_check.py
from scripts import check  # This will now look for check.py in the same directory

def final_system_check():
    """Comprehensive system validation"""
    checks = [
        check.rule_based_detector,  # Fixed: removed spaces from function name
        check.alert_system,         # Fixed: removed spaces
        check.backup_system,        # Fixed: removed spaces
        check.simulation_environment,  # Fixed: removed spaces
        check.end_to_end_test,
        check.documentation,
    ]

    print("🚀 Starting Final System Check...")
    print("=" * 50)
    
    for i, check_func in enumerate(checks, 1):
        try:
            print(f"{i}. Running {check_func.__name__}...")
            result = check_func()
            status = "PASSED" if result else "FAILED"
            print(f"   Result: {status}")
        except Exception as e:
            print(f"   {check_func.__name__}: FAILED - {e}")

    print("=" * 50)
    print("System ready for demonstration!")

if __name__ == "__main__":
    final_system_check()