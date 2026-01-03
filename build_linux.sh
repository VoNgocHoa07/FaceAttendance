#!/bin/bash
# Build script for Linux - Face Recognition Attendance System
# Requires: conda environment "face_attendance"

echo "========================================"
echo " Building Face Attendance for Linux"
echo "========================================"

# Activate conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate face_attendance

# Clean previous builds
rm -rf dist build FaceAttendance.spec

# Build with PyInstaller
pyinstaller --noconfirm --onedir --windowed \
    --name "FaceAttendance" \
    --add-data "Logo:Logo" \
    --add-data "known_faces:known_faces" \
    --add-data "attendance_records:attendance_records" \
    --hidden-import "PySide6.QtCore" \
    --hidden-import "PySide6.QtGui" \
    --hidden-import "PySide6.QtWidgets" \
    --hidden-import "cv2" \
    --hidden-import "mediapipe" \
    --hidden-import "face_recognition" \
    --hidden-import "dlib" \
    --hidden-import "numpy" \
    --hidden-import "pandas" \
    --hidden-import "openpyxl" \
    --collect-all "mediapipe" \
    --collect-all "face_recognition" \
    app_main.py

# Create empty folders if not exist
mkdir -p dist/FaceAttendance/known_faces
mkdir -p dist/FaceAttendance/attendance_records

# Make executable
chmod +x dist/FaceAttendance/FaceAttendance

# Create run script
cat > dist/FaceAttendance/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./FaceAttendance
EOF
chmod +x dist/FaceAttendance/run.sh

echo ""
echo "========================================"
echo " Build completed!"
echo " Output: dist/FaceAttendance/"
echo " Run: ./dist/FaceAttendance/FaceAttendance"
echo "   or: ./dist/FaceAttendance/run.sh"
echo "========================================"
