# Face Attendance - Face Recognition Attendance System

A modern, cross-platform face recognition attendance system built with Python, PySide6, and OpenCV.

## Downloads

Download the latest version for your operating system:

| Platform | Download |
|----------|----------|
| Windows | [FaceAttendance-Windows.zip](../../releases/latest/download/FaceAttendance-Windows.zip) |
| macOS | [FaceAttendance-macOS.dmg](../../releases/latest/download/FaceAttendance-macOS.dmg) |
| Linux | [FaceAttendance-Linux.tar.gz](../../releases/latest/download/FaceAttendance-Linux.tar.gz) |

## Installation

### Windows
1. Download `FaceAttendance-Windows.zip`
2. Extract the ZIP file
3. Run `FaceAttendance.exe`

### macOS
1. Download `FaceAttendance-macOS.dmg`
2. Mount the DMG file
3. Drag `FaceAttendance.app` to Applications folder
4. Right-click and select "Open" (first time only)

### Linux
1. Download `FaceAttendance-Linux.tar.gz`
2. Extract: `tar -xzvf FaceAttendance-Linux.tar.gz`
3. Run: `./FaceAttendance`

## Features

- Real-time face recognition attendance
- Modern dark theme UI with animations
- Add/manage members with photo capture
- Export attendance to Excel/CSV
- Attendance reports and analytics
- Multi-session support (Morning/Afternoon/Evening/Night)
- Settings customization
- Cross-platform (Windows, macOS, Linux)

## Requirements

- Camera/Webcam
- Windows 10+, macOS 10.15+, or Ubuntu 20.04+

## Usage

1. **Add Members**: Click "Add Person" to capture face photos
2. **Take Attendance**: Face the camera - recognized faces are automatically logged
3. **Export**: Export attendance records to Excel/CSV
4. **Reports**: View attendance analytics and statistics

## Development

### Prerequisites
- Python 3.11+
- CMake
- Webcam

### Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/NhanDienKhuonMat.git
cd NhanDienKhuonMat

# Install dependencies
pip install -r requirements.txt

# Run application
python app_main.py
```

### Build
```bash
# Build executable
pyinstaller FaceAttendance.spec
```

## License

MIT License

## Author

Created with love using Python, PySide6, OpenCV, and face_recognition library.
