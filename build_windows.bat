@echo off
REM Build script for Windows - Face Recognition Attendance System
REM Requires: conda environment "face_attendance"

echo ========================================
echo  Building Face Attendance for Windows
echo ========================================

REM Activate conda environment
call conda activate face_attendance

REM Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "FaceAttendance.spec" del /f FaceAttendance.spec

REM Build with PyInstaller
pyinstaller --noconfirm --onedir --windowed ^
    --name "FaceAttendance" ^
    --icon "Logo/icon.ico" ^
    --add-data "Logo;Logo" ^
    --add-data "known_faces;known_faces" ^
    --add-data "attendance_records;attendance_records" ^
    --hidden-import "PySide6.QtCore" ^
    --hidden-import "PySide6.QtGui" ^
    --hidden-import "PySide6.QtWidgets" ^
    --hidden-import "cv2" ^
    --hidden-import "mediapipe" ^
    --hidden-import "face_recognition" ^
    --hidden-import "dlib" ^
    --hidden-import "numpy" ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    --collect-all "mediapipe" ^
    --collect-all "face_recognition" ^
    app_main.py

REM Create empty folders if not exist in dist
if not exist "dist\FaceAttendance\known_faces" mkdir "dist\FaceAttendance\known_faces"
if not exist "dist\FaceAttendance\attendance_records" mkdir "dist\FaceAttendance\attendance_records"

echo.
echo ========================================
echo  Build completed!
echo  Output: dist\FaceAttendance\
echo  Run: dist\FaceAttendance\FaceAttendance.exe
echo ========================================

pause
