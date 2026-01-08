#!/bin/bash
# ==============================================
# START SCRIPT - Face Recognition Attendance
# Chay: bash start.sh
# ==============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo ""
echo "============================================"
echo "  Face Recognition Attendance System"
echo "============================================"
echo ""

# Check venv exists
if [ ! -f "$VENV_DIR/bin/python" ]; then
    echo "[X] Virtual environment not found!"
    echo "    Please run: bash setup.sh"
    exit 1
fi

echo "[OK] Found virtual environment"

# Check app file
if [ ! -f "$SCRIPT_DIR/app_main.py" ]; then
    echo "[X] app_main.py not found!"
    exit 1
fi

echo "[OK] Found app_main.py"

# Create directories if needed
mkdir -p "$SCRIPT_DIR/known_faces"
mkdir -p "$SCRIPT_DIR/attendance_records"

echo ""
echo "Starting application..."
echo "(Press Ctrl+C to exit)"
echo ""
echo "============================================"
echo ""

# Run app
cd "$SCRIPT_DIR"
"$VENV_DIR/bin/python" app_main.py
