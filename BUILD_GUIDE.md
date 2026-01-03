# Face Attendance System - Hướng dẫn cài đặt và sử dụng

---

## 📥 DOWNLOAD

| Hệ điều hành | Link Download | Kích thước |
|--------------|---------------|------------|
| **macOS (ARM64)** | [FaceAttendance_macOS.zip](dist/FaceAttendance_macOS.zip) | ~430 MB |
| **Windows** | Cần build trên máy Windows (xem hướng dẫn bên dưới) | - |
| **Linux** | Cần build trên máy Linux (xem hướng dẫn bên dưới) | - |

---

## 🚀 HƯỚNG DẪN SỬ DỤNG NHANH

### macOS
1. Tải file `FaceAttendance_macOS.zip`
2. Giải nén file zip
3. Mở `FaceAttendance.app` (double-click)
4. Nếu bị chặn: System Settings → Privacy & Security → "Open Anyway"

### Windows / Linux
Xem phần **Build từ source** bên dưới.

---

## 🔧 BUILD TỪ SOURCE

### Yêu cầu
- Python 3.10+ 
- pip hoặc conda

### Bước 1: Tạo môi trường ảo

**Cách 1: Dùng venv (khuyến nghị)**
```bash
cd NhanDienKhuonMat
python3 -m venv venv

# Kích hoạt môi trường
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Cài đặt packages
pip install numpy pandas opencv-python-headless PySide6 openpyxl mediapipe face_recognition pyinstaller
```

**Cách 2: Dùng Conda**
```bash
conda env create -f environment.yml
conda activate face_attendance
```

### Bước 2: Build ứng dụng

**Windows:**
```batch
build_windows.bat
```

**Linux:**
```bash
chmod +x build_linux.sh
./build_linux.sh
```

**macOS:**
```bash
source venv/bin/activate
pyinstaller --noconfirm --onedir --windowed \
    --name "FaceAttendance" \
    --add-data "Logo:Logo" \
    --hidden-import "PySide6.QtCore" \
    --hidden-import "PySide6.QtGui" \
    --hidden-import "PySide6.QtWidgets" \
    --hidden-import "cv2" \
    --hidden-import "mediapipe" \
    --hidden-import "face_recognition" \
    --collect-all "mediapipe" \
    --collect-all "face_recognition" \
    app_main.py
```

### Bước 3: Chạy ứng dụng

| OS | Đường dẫn |
|----|-----------|
| Windows | `dist\FaceAttendance\FaceAttendance.exe` |
| Linux | `dist/FaceAttendance/FaceAttendance` |
| macOS | `dist/FaceAttendance.app` |

---

## 📁 CẤU TRÚC THƯ MỤC

```
FaceAttendance/
├── FaceAttendance.exe / FaceAttendance / FaceAttendance.app
├── Logo/                    # Logo ứng dụng
├── known_faces/             # Ảnh khuôn mặt đã đăng ký
├── attendance_records/      # File điểm danh CSV
└── _internal/               # Thư viện runtime
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Cross-compile không được hỗ trợ**: 
   - Phải build trên Windows để có file .exe
   - Phải build trên Linux để có file cho Linux
   - Phải build trên macOS để có file .app

2. **Camera**: Đảm bảo webcam hoạt động và được cấp quyền

3. **Linux dependencies**:
   ```bash
   sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libgl1-mesa-glx
   ```

---

## 🐛 TROUBLESHOOTING

| Lỗi | Giải pháp |
|-----|-----------|
| ModuleNotFoundError | Thêm `--hidden-import "module_name"` khi build |
| libGL not found (Linux) | `sudo apt-get install libgl1-mesa-glx` |
| Camera không hoạt động | Kiểm tra quyền truy cập camera |
| App bị chặn (macOS) | System Settings → Privacy & Security → Open Anyway |
