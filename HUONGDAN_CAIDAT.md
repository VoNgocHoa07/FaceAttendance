# Hướng Dẫn Cài Đặt - Face Recognition Attendance System

## 🚀 CÁCH 1: TẢI BẢN ĐÃ ĐÓNG GÓI (KHUYẾN NGHỊ)

**Không cần cài đặt gì cả! Chỉ cần tải và chạy.**

### Bước 1: Tải file phù hợp với hệ điều hành của bạn

Vào trang **Releases** của dự án trên GitHub và tải:
- **Windows:** `FaceAttendance-Windows.zip`
- **macOS:** `FaceAttendance-macOS.zip`  
- **Linux:** `FaceAttendance-Linux.tar.gz`

### Bước 2: Giải nén và chạy

| Hệ điều hành | Cách chạy |
|--------------|-----------|
| **Windows** | Giải nén → Double-click `FaceAttendance.exe` |
| **macOS** | Giải nén → Double-click `FaceAttendance.app` |
| **Linux** | Giải nén → Chạy `./start.sh` hoặc `./FaceAttendance` |

### Lưu ý khi chạy lần đầu:
- **Windows:** Nếu Windows Defender chặn, click "More info" → "Run anyway"
- **macOS:** Nếu bị chặn, vào System Preferences → Security & Privacy → "Open Anyway"
- **Linux:** Nếu lỗi permission, chạy: `chmod +x FaceAttendance start.sh`

---

## 🔧 CÁCH 2: TỰ BUILD TỪ SOURCE CODE

### Yêu Cầu Hệ Thống

- **Python:** 3.10 (bắt buộc)
- **RAM:** Tối thiểu 8GB
- **Ổ cứng:** 5GB trống
- **Camera:** Webcam hoạt động
- **Công cụ:** CMake, Visual Studio Build Tools (Windows)

### Windows

```cmd
1. setup.bat     (cài đặt - chờ đến khi hiện "HOAN TAT")
2. start.bat     (chạy ứng dụng)
```

⚠️ **Lưu ý Windows:** Cần cài Visual Studio Build Tools với C++ workload trước. Tải tại: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### macOS

```bash
# Cài Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài CMake
brew install cmake

# Chạy setup
bash setup.sh
bash start.sh
```

### Linux

```bash
# Cài dependencies
sudo apt-get update
sudo apt-get install -y cmake build-essential python3.10 python3.10-venv
sudo apt-get install -y libopenblas-dev liblapack-dev

# Chạy setup
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

---

## 🏗️ CÁCH 3: TỰ BUILD FILE EXECUTABLE

Nếu bạn muốn tự build file executable cho máy của mình:

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build
python build_app.py

# 3. File output sẽ ở thư mục dist/
```

---

## 📁 Cấu Trúc Thư Mục

```
FaceAttendance/
├── FaceAttendance.exe (hoặc .app)    # Ứng dụng chính
├── known_faces/                       # Lưu ảnh khuôn mặt đã đăng ký
├── attendance_records/                # Lưu dữ liệu điểm danh
└── settings.json                      # Cài đặt ứng dụng
```

---

## ❌ Xử Lý Lỗi Thường Gặp

| Lỗi | Giải pháp |
|-----|-----------|
| Windows Defender chặn | Click "More info" → "Run anyway" |
| macOS: "App cannot be opened" | System Preferences → Security → "Open Anyway" |
| Permission denied (Linux) | `chmod +x FaceAttendance start.sh` |
| Camera không hoạt động | Kiểm tra quyền truy cập camera trong Settings |
| Lỗi dlib trên Windows | Cài Visual Studio Build Tools với C++ workload |

---

## 💾 Backup Dữ Liệu

Copy 2 thư mục sau để backup:
- `known_faces/` - Ảnh khuôn mặt đã đăng ký
- `attendance_records/` - Lịch sử điểm danh
