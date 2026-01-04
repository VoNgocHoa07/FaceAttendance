#!/usr/bin/env python3
"""
Build script for Face Recognition Attendance System
Automatically builds executable for current OS (macOS/Windows/Linux)

Usage:
    python build_app.py
"""

import subprocess
import sys
import os
import shutil
import platform

def check_dependencies():
    """Check and install required build dependencies"""
    print("=" * 50)
    print("Checking dependencies...")
    print("=" * 50)
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("[!] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check other dependencies
    deps = ['face_recognition', 'dlib', 'mediapipe', 'cv2', 'PySide6', 'pandas', 'openpyxl']
    for dep in deps:
        try:
            __import__(dep)
            print(f"[OK] {dep}")
        except ImportError:
            print(f"[!] Missing: {dep}")
            print(f"    Run: pip install -r requirements.txt")
            return False
    
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("\nCleaning previous builds...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  Removed: {d}")

def build():
    """Build the application"""
    system = platform.system()
    print(f"\n{'=' * 50}")
    print(f"Building for {system}...")
    print(f"{'=' * 50}")
    
    # Use spec file
    cmd = [sys.executable, "-m", "PyInstaller", "FaceAttendance.spec", "--clean"]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\n{'=' * 50}")
        print("BUILD SUCCESSFUL!")
        print(f"{'=' * 50}")
        
        if system == "Darwin":
            output = "dist/FaceAttendance.app"
            print(f"\nOutput: {output}")
            print("\nTo run: Double-click FaceAttendance.app")
            print("To distribute: Zip the .app file and share")
        elif system == "Windows":
            output = "dist/FaceAttendance.exe"
            print(f"\nOutput: {output}")
            print("\nTo run: Double-click FaceAttendance.exe")
        else:
            output = "dist/FaceAttendance"
            print(f"\nOutput: {output}")
            print("\nTo run: ./dist/FaceAttendance")
        
        # Create folders for data
        data_dirs = ['dist/known_faces', 'dist/attendance_records']
        for d in data_dirs:
            os.makedirs(d, exist_ok=True)
        print(f"\nCreated data folders in dist/")
        print("\nIMPORTANT: When distributing, include these folders:")
        print("  - known_faces/ (for face data)")
        print("  - attendance_records/ (for attendance logs)")
        
    else:
        print(f"\n{'=' * 50}")
        print("BUILD FAILED!")
        print(f"{'=' * 50}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("2. Try running with verbose output:")
        print("   pyinstaller FaceAttendance.spec --clean --log-level DEBUG")
        
    return result.returncode

def main():
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║   Face Recognition Attendance System Builder      ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    if not check_dependencies():
        print("\nPlease install missing dependencies first!")
        sys.exit(1)
    
    clean_build()
    
    exit_code = build()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
