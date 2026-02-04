"""
Quick script to verify all dependencies are installed correctly
"""
import sys
import os

# Fix Windows encoding issues
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # Set UTF-8 encoding

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        status = "[OK]" if sys.platform == 'win32' else "✅"
        print(f"{status} {package_name or module_name}")
        return True
    except ImportError as e:
        status = "[FAIL]" if sys.platform == 'win32' else "❌"
        print(f"{status} {package_name or module_name} - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Verifying AI Voice Detection Dependencies")
    print("=" * 60)
    print()
    
    checks = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("librosa", "Librosa"),
        ("sklearn", "Scikit-learn"),
        ("jose", "Python-JOSE"),
        ("passlib", "Passlib"),
        ("dotenv", "Python-dotenv"),
        ("aiofiles", "Aiofiles"),
        ("pydub", "Pydub"),
    ]
    
    results = []
    for module, name in checks:
        results.append(check_import(module, name))
    
    print()
    print("=" * 60)
    if all(results):
        success_msg = "[SUCCESS]" if sys.platform == 'win32' else "✅"
        print(f"{success_msg} All dependencies installed successfully!")
        print("=" * 60)
        print()
        print("You can now start the backend server:")
        print("  Windows: start_backend.bat")
        print("  Linux/Mac: ./start_backend.sh")
        return 0
    else:
        fail_msg = "[FAILED]" if sys.platform == 'win32' else "❌"
        print(f"{fail_msg} Some dependencies are missing!")
        print("=" * 60)
        print()
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        print()
        print("Or use the step-by-step installer:")
        print("  Windows: install_dependencies.bat")
        print("  Linux/Mac: ./install_dependencies.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main())

