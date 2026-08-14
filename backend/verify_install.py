#!/usr/bin/env python3
"""
Verification script to test if all dependencies install correctly
Run this before deploying to Render
"""
import sys
import subprocess

def verify_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 11:
        print("✓ Python 3.11 detected - GOOD!")
        return True
    elif version.major == 3 and version.minor == 12:
        print("✓ Python 3.12 detected - Also compatible")
        return True
    else:
        print(f"⚠ WARNING: Python {version.major}.{version.minor} detected")
        print("  Recommended: Python 3.11 for best Render compatibility")
        return False

def test_imports():
    """Test if all critical imports work"""
    print("\n--- Testing Critical Imports ---")
    
    packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
        ('pydantic_settings', 'Pydantic Settings'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('aiosqlite', 'aiosqlite'),
        ('requests', 'Requests'),
        ('httpx', 'HTTPX'),
    ]
    
    all_good = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"✗ {name} FAILED: {e}")
            all_good = False
    
    return all_good

def check_pydantic_core():
    """Check if pydantic-core is properly installed"""
    print("\n--- Checking pydantic-core ---")
    try:
        import pydantic_core
        print(f"✓ pydantic-core version: {pydantic_core.__version__}")
        print("✓ pydantic-core installed successfully (no compilation needed)")
        return True
    except ImportError as e:
        print(f"✗ pydantic-core FAILED: {e}")
        return False

def main():
    print("=" * 60)
    print("TRENDLOOM BACKEND - DEPENDENCY VERIFICATION")
    print("=" * 60)
    
    py_ok = verify_python_version()
    imports_ok = test_imports()
    pydantic_ok = check_pydantic_core()
    
    print("\n" + "=" * 60)
    if py_ok and imports_ok and pydantic_ok:
        print("✓✓✓ ALL CHECKS PASSED ✓✓✓")
        print("Your backend is ready to deploy to Render!")
        return 0
    else:
        print("✗✗✗ SOME CHECKS FAILED ✗✗✗")
        print("Please fix the issues above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
