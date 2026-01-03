#!/bin/bash
# Script build Linux executable using Docker (chạy được trên macOS/Windows/Linux)

echo "========================================"
echo " Building Face Attendance for Linux"
echo " Using Docker (cross-platform)"
echo "========================================"

cd "$(dirname "$0")"

# Create output directory
mkdir -p output

# Build Docker image
echo "[1/3] Building Docker image..."
docker build -f Dockerfile.build -t face-attendance-builder .

# Run container to create tar.gz
echo "[2/3] Creating Linux package..."
docker run --rm -v "$(pwd)/output:/output" face-attendance-builder

# Check result
if [ -f "output/FaceAttendance_Linux.tar.gz" ]; then
    echo ""
    echo "========================================"
    echo " Build SUCCESS!"
    echo " Output: output/FaceAttendance_Linux.tar.gz"
    echo ""
    echo " Để sử dụng trên Linux:"
    echo "   tar -xzvf FaceAttendance_Linux.tar.gz"
    echo "   cd FaceAttendance"
    echo "   ./FaceAttendance"
    echo "========================================"
else
    echo "Build FAILED!"
    exit 1
fi
