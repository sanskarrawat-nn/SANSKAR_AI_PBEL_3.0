import sys
import os
import importlib

def check_dependencies():
    dependencies = ["pandas", "fastapi", "uvicorn", "requests", "streamlit"]
    missing = []
    
    print("Checking system dependencies...")
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"  [OK] {dep} is installed")
        except ImportError:
            missing.append(dep)
            print(f"  [FAIL] {dep} is missing!")
            
    return missing

def verify_data():
    courses_path = "data/courses.csv"
    modules_path = "data/modules.csv"
    
    print(f"\nVerifying database locations...")
    data_missing = not os.path.exists(courses_path) or not os.path.exists(modules_path)
    
    if data_missing:
        print(f"  [WARN] Database CSV files are missing! Triggering scripts/generate_data.py...")
        try:
            from scripts.generate_data import generate_all
            generate_all()
            print("  [OK] Relational course and module datasets generated successfully.")
        except Exception as e:
            print(f"  [FAIL] Could not generate datasets automatically: {e}")
            return False
    else:
        print(f"  [OK] Courses dataset found at '{courses_path}'")
        print(f"  [OK] Modules dataset found at '{modules_path}'")
    return True

if __name__ == "__main__":
    missing_deps = check_dependencies()
    data_ok = verify_data()
    
    print("\n--- Environmental Audit Summary ---")
    if missing_deps:
        print(f"FAIL: Verification FAILED: Missing libraries: {', '.join(missing_deps)}")
        print("Please run: pip install pandas fastapi uvicorn requests streamlit")
        sys.exit(1)
    elif not data_ok:
        print("FAIL: Verification FAILED: Could not secure database files.")
        sys.exit(1)
    else:
        print("SUCCESS: Environment is fully qualified and ready for launch!")
        sys.exit(0)
