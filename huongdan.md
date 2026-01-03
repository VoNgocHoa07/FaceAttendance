# Hướng Dẫn Face Attendance System

## 📥 LINK DOWNLOAD

| Hệ điều hành | Link Download |
|--------------|---------------|
| **Windows** | https://github.com/VoNgocHoa07/FaceAttendance/releases/latest/download/FaceAttendance_Windows.zip |
| **Linux** | https://github.com/VoNgocHoa07/FaceAttendance/releases/latest/download/FaceAttendance_Linux.tar.gz |

---

## 🚀 CÁCH SỬ DỤNG

### Windows
1. Tải file `FaceAttendance_Windows.zip`
2. Giải nén (chuột phải → Extract All)
3. Mở thư mục → Double-click `FaceAttendance.exe`
4. Giao diện hiện ra, sử dụng ngay!

### Linux
```bash
# Tải file
wget https://github.com/VoNgocHoa07/FaceAttendance/releases/latest/download/FaceAttendance_Linux.tar.gz

# Giải nén
tar -xzvf FaceAttendance_Linux.tar.gz

# Chạy
cd FaceAttendance
./FaceAttendance
```

---

## 🔧 CÁCH TẠO LINK DOWNLOAD (Dành cho Developer)

### Bước 1: Tạo GitHub Repository

```bash
# Khởi tạo git trong thư mục dự án
cd /path/to/NhanDienKhuonMat
git init

# Thêm tất cả file
git add -A

# Commit
git commit -m "Initial commit"

# Tạo repo trên GitHub và push (cần cài GitHub CLI)
gh repo create TenRepo --public --source=. --push
```

### Bước 2: Tạo file GitHub Actions

Tạo file `.github/workflows/build-release.yml` với nội dung:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install numpy pandas opencv-python-headless PySide6 openpyxl mediapipe face_recognition pyinstaller
      
      - name: Build with PyInstaller
        run: |
          pyinstaller --noconfirm --onedir --windowed `
            --name "FaceAttendance" `
            --add-data "Logo;Logo" `
            --hidden-import "PySide6.QtCore" `
            --hidden-import "PySide6.QtGui" `
            --hidden-import "PySide6.QtWidgets" `
            --hidden-import "cv2" `
            --hidden-import "mediapipe" `
            --hidden-import "face_recognition" `
            --hidden-import "dlib" `
            --hidden-import "numpy" `
            --hidden-import "pandas" `
            --hidden-import "openpyxl" `
            --collect-all "mediapipe" `
            --collect-all "face_recognition" `
            app_main.py
      
      - name: Create directories
        run: |
          New-Item -ItemType Directory -Force -Path "dist\FaceAttendance\known_faces"
          New-Item -ItemType Directory -Force -Path "dist\FaceAttendance\attendance_records"
      
      - name: Zip Windows build
        run: |
          Compress-Archive -Path "dist\FaceAttendance\*" -DestinationPath "FaceAttendance_Windows.zip"
      
      - name: Upload Windows artifact
        uses: actions/upload-artifact@v4
        with:
          name: FaceAttendance_Windows
          path: FaceAttendance_Windows.zip

  build-linux:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libgl1-mesa-glx \
            libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
            libxcb-render-util0 libegl1 libxcb-shape0
      
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install numpy pandas opencv-python-headless PySide6 openpyxl mediapipe face_recognition pyinstaller
      
      - name: Build with PyInstaller
        run: |
          pyinstaller --noconfirm --onedir \
            --name "FaceAttendance" \
            --add-data "Logo:Logo" \
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
      
      - name: Create directories and run script
        run: |
          mkdir -p dist/FaceAttendance/known_faces
          mkdir -p dist/FaceAttendance/attendance_records
          echo '#!/bin/bash' > dist/FaceAttendance/run.sh
          echo 'cd "$(dirname "$0")"' >> dist/FaceAttendance/run.sh
          echo './FaceAttendance' >> dist/FaceAttendance/run.sh
          chmod +x dist/FaceAttendance/run.sh
          chmod +x dist/FaceAttendance/FaceAttendance
      
      - name: Tar Linux build
        run: |
          cd dist
          tar -czvf ../FaceAttendance_Linux.tar.gz FaceAttendance/
      
      - name: Upload Linux artifact
        uses: actions/upload-artifact@v4
        with:
          name: FaceAttendance_Linux
          path: FaceAttendance_Linux.tar.gz

  release:
    needs: [build-windows, build-linux]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Download Windows artifact
        uses: actions/download-artifact@v4
        with:
          name: FaceAttendance_Windows
      
      - name: Download Linux artifact
        uses: actions/download-artifact@v4
        with:
          name: FaceAttendance_Linux
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            FaceAttendance_Windows.zip
            FaceAttendance_Linux.tar.gz
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Bước 3: Tạo Release để trigger build

```bash
# Tạo tag phiên bản
git tag v1.0.0

# Push tag lên GitHub
git push origin v1.0.0
```

### Bước 4: Chờ build hoàn thành

1. Vào https://github.com/USERNAME/REPO/actions để xem tiến trình
2. Khi thấy ✅ xanh là build xong
3. Vào https://github.com/USERNAME/REPO/releases để lấy link download

---

## 📋 GIẢI THÍCH CÁCH HOẠT ĐỘNG

### GitHub Actions là gì?
- Dịch vụ CI/CD miễn phí của GitHub
- Tự động chạy code trên máy ảo Windows/Linux/macOS
- Khi push tag `v*` → tự động build ứng dụng

### PyInstaller là gì?
- Công cụ đóng gói Python thành file executable
- Gom tất cả Python + thư viện + code vào 1 folder
- Người dùng không cần cài Python

### Quy trình build:
```
Push tag v1.0.0
    ↓
GitHub Actions trigger
    ↓
┌─────────────────┬─────────────────┐
│ Windows Runner  │  Linux Runner   │
│ (windows-latest)│ (ubuntu-22.04)  │
├─────────────────┼─────────────────┤
│ Cài Python 3.11 │ Cài Python 3.11 │
│ Cài thư viện    │ Cài thư viện    │
│ PyInstaller     │ PyInstaller     │
│ build           │ build           │
│ Tạo .zip        │ Tạo .tar.gz     │
└─────────────────┴─────────────────┘
    ↓
Upload lên GitHub Releases
    ↓
Link download sẵn sàng!
```

---

## 🔗 CẤU TRÚC LINK

```
# Link trang Releases (xem tất cả phiên bản)
https://github.com/USERNAME/REPO/releases

# Link download trực tiếp phiên bản mới nhất
https://github.com/USERNAME/REPO/releases/latest/download/TEN_FILE.zip

# Link download phiên bản cụ thể
https://github.com/USERNAME/REPO/releases/download/v1.0.0/TEN_FILE.zip
```

---

## ⚠️ LƯU Ý

1. **Lần đầu chạy trên Windows**: Có thể bị Windows Defender chặn → Click "More info" → "Run anyway"

2. **Linux cần quyền thực thi**:
   ```bash
   chmod +x FaceAttendance
   ```

3. **Camera**: Đảm bảo máy có webcam và được cấp quyền truy cập

4. **Build mất ~10-15 phút**: Kiểm tra tiến trình tại tab "Actions" trên GitHub

---

## 📁 CẤU TRÚC FILE SAU KHI GIẢI NÉN

```
FaceAttendance/
├── FaceAttendance.exe (Windows) / FaceAttendance (Linux)
├── Logo/
├── known_faces/          # Thêm ảnh khuôn mặt vào đây
├── attendance_records/   # File điểm danh CSV
└── _internal/            # Thư viện (không cần quan tâm)
```

---

## 🆘 TROUBLESHOOTING

| Vấn đề | Giải pháp |
|--------|-----------|
| Windows chặn ứng dụng | Click "More info" → "Run anyway" |
| Linux không chạy được | `chmod +x FaceAttendance` |
| Camera không nhận | Kiểm tra quyền truy cập camera |
| Build thất bại | Xem log tại GitHub Actions |
