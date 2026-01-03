# import cv2
# import os
# import shutil
# import time
# import math
# import mediapipe as mp

# from PySide6.QtWidgets import (
#     QMainWindow, QLabel, QVBoxLayout, QWidget,
#     QPushButton, QFileDialog, QSizePolicy
# )
# from PySide6.QtCore import QTimer, Qt, Signal
# from PySide6.QtGui import QImage, QPixmap

# STYLE = """
# QWidget {
#     background-color: #1E1E2F;
#     color: #ECEFF4;
#     font-family: 'Segoe UI', sans-serif;
# }
# QLabel#instruction_label {
#     font-size: 20px;
#     font-weight: bold;
#     color: #88C0D0;
#     padding: 10px;
# }
# QLabel#video_label {
#     border: 2px solid #5E81AC;
#     border-radius: 10px;
# }
# QLabel#person_label {
#     font-size: 18px;
#     font-weight: bold;
#     color: #A3BE8C;
#     padding: 8px 0;
# }
# QLabel#status_label {
#     font-size: 16px;
#     color: #D8DEE9;
#     padding: 5px 0;
# }
# QPushButton {
#     padding: 10px;
#     background-color: #5E81AC;
#     color: white;
#     border: none;
#     border-radius: 5px;
#     font-weight: bold;
# }
# QPushButton:hover {
#     background-color: #81A1C1;
# }
# """

# class AutoCaptureWindow(QMainWindow):
#     finished = Signal()

#     def __init__(self, person_name):
#         super().__init__()
#         self.setWindowTitle("Thêm dữ liệu khuôn mặt")
#         self.setGeometry(500, 100, 600, 750)
#         self.setFixedSize(600, 750)
#         self.setStyleSheet(STYLE)

#         self.person_name = person_name
#         self.capture_folder = os.path.join("known_faces", self.person_name)
#         os.makedirs(self.capture_folder, exist_ok=True)

#         self.cap = cv2.VideoCapture(0)
#         if not self.cap.isOpened():
#             print("🚫 Không mở được camera.")
#             return

#         self.person_label = QLabel(f"👤 Đang thêm dữ liệu cho: {self.person_name}")
#         self.person_label.setObjectName("person_label")
#         self.person_label.setAlignment(Qt.AlignCenter)

#         self.video_label = QLabel()
#         self.video_label.setObjectName("video_label")
#         self.video_label.setMinimumSize(360, 360)
#         self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.video_label.setAlignment(Qt.AlignCenter)

#         self.instruction_label = QLabel("")
#         self.instruction_label.setObjectName("instruction_label")
#         self.instruction_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#         self.instruction_label.setWordWrap(True)

#         self.status_label = QLabel("")
#         self.status_label.setObjectName("status_label")
#         self.status_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#         self.status_label.setWordWrap(True)

#         self.btn_restart = QPushButton("🔁 Chụp lại từ đầu")
#         self.btn_restart.clicked.connect(self.restart_capture)

#         layout = QVBoxLayout()
#         layout.addWidget(self.person_label)
#         layout.addWidget(self.video_label)
#         layout.addWidget(self.instruction_label)
#         layout.addWidget(self.status_label)
#         layout.addWidget(self.btn_restart)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#         self.image_index = 1
#         self.current_frame = None

#         self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
#         self.captured_angles = {"frontal": False, "left": False, "right": False}
#         self.last_capture_time = time.time()

#         self.flash_frames_remaining = 0

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if not ret: return

#         frame = cv2.flip(frame, 1)

#         if self.flash_frames_remaining > 0:
#             overlay = frame.copy()
#             cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), -1)
#             cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
#             self.flash_frames_remaining -= 1
        
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.face_mesh.process(rgb_frame)

#         h, w = frame.shape[:2]
#         center = (w // 2, h // 2)
#         radius = int(min(w, h) * 0.3)
#         circle_color = (0, 255, 0)
#         instruction = "Căn khuôn mặt vào khung và xoay lần lượt: trái – chính diện – phải"

#         if results.multi_face_landmarks:
#             face_landmarks = results.multi_face_landmarks[0]
            
#             nose_tip = face_landmarks.landmark[1]
#             face_center_x, face_center_y = int(nose_tip.x * w), int(nose_tip.y * h)
            
#             distance = math.sqrt((face_center_x - center[0])**2 + (face_center_y - center[1])**2)

#             if distance < radius:
#                 left_eye = face_landmarks.landmark[33]
#                 right_eye = face_landmarks.landmark[263]
#                 dx = right_eye.x - left_eye.x
#                 dy = right_eye.y - left_eye.y
#                 yaw = math.degrees(math.atan2(dy, dx))
#                 now = time.time()
#                 delay = 1.5
#                 direction = None

#                 if -15 < yaw < 15 and not self.captured_angles["frontal"]:
#                     direction = "frontal"
#                     instruction = "👀 Nhìn chính diện"
#                 elif yaw <= -15 and not self.captured_angles["left"]:
#                     direction = "left"
#                     instruction = "↩️ Xoay mặt sang TRÁI"
#                 elif yaw >= 15 and not self.captured_angles["right"]:
#                     direction = "right"
#                     instruction = "➡️ Xoay mặt sang PHẢI"

#                 if direction and now - self.last_capture_time > delay:
#                     original_frame_to_save = cv2.flip(self.cap.read()[1], 1)
                    
#                     filename = f"{self.person_name}_{direction}_{self.image_index:03}.jpg"
#                     save_path = os.path.join(self.capture_folder, filename)
#                     cv2.imwrite(save_path, original_frame_to_save)
#                     print(f"✅ Đã lưu tự động: {save_path}")
                    
#                     self.flash_frames_remaining = 5
#                     self.status_label.setText(f"✅ Đã chụp góc: {direction.upper()}")
#                     self.image_index += 1
#                     self.captured_angles[direction] = True
#                     self.last_capture_time = now

#                     if all(self.captured_angles.values()):
#                         self.instruction_label.setText("🎉 Đã hoàn tất tự động quét 3 góc!")
#                         self.status_label.setText("Đang quay lại màn hình chính...")
#                         QTimer.singleShot(1500, self.complete_and_close)
#             else:
#                 circle_color = (0, 0, 255)
#                 instruction = "Vui lòng di chuyển khuôn mặt vào trong vòng tròn"
        
#         cv2.circle(frame, center, radius, circle_color, 2)
        
#         self.instruction_label.setText(instruction)
        
#         # === ĐÂY LÀ DÒNG SỬA LỖI MÀU SẮC ===
#         # Sử dụng 'frame' (định dạng BGR) thay vì 'rgb_frame'
#         qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)

#         self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
#             self.video_label.width(), self.video_label.height(),
#             Qt.KeepAspectRatio, Qt.SmoothTransformation))
#         self.current_frame = frame

#     def complete_and_close(self):
#         self.close()

#     def restart_capture(self):
#         if os.path.exists(self.capture_folder):
#             try:
#                 shutil.rmtree(self.capture_folder)
#                 print(f"Đã xóa các ảnh cũ trong thư mục: {self.capture_folder}")
#             except Exception as e:
#                 print(f'Lỗi khi xóa thư mục {self.capture_folder}. Lý do: {e}')
        
#         os.makedirs(self.capture_folder, exist_ok=True)
#         self.image_index = 1
#         self.captured_angles = {"frontal": False, "left": False, "right": False}
#         self.status_label.setText("")
#         self.instruction_label.setText("🔁 Vui lòng xoay mặt lại 3 hướng")

#     def closeEvent(self, event):
#         self.timer.stop()
#         self.cap.release()
#         self.finished.emit()
#         event.accept()


# import cv2
# import os
# import shutil
# import time
# import math
# import mediapipe as mp

# from PySide6.QtWidgets import (
#     QMainWindow, QLabel, QVBoxLayout, QWidget,
#     QPushButton, QFileDialog, QSizePolicy, QHBoxLayout
# )
# from PySide6.QtCore import QTimer, Qt, Signal
# from PySide6.QtGui import QImage, QPixmap

# STYLE = """
# QWidget {
#     background-color: #1E1E2F;
#     color: #ECEFF4;
#     font-family: 'Segoe UI', sans-serif;
# }
# QLabel#instruction_label {
#     font-size: 20px;
#     font-weight: bold;
#     color: #88C0D0;
#     padding: 10px;
# }
# QLabel#video_label {
#     border: 2px solid #5E81AC;
#     border-radius: 10px;
# }
# QLabel#person_label {
#     font-size: 18px;
#     font-weight: bold;
#     color: #A3BE8C;
#     padding: 8px 0;
# }
# QLabel#status_label {
#     font-size: 16px;
#     color: #D8DEE9;
#     padding: 5px 0;
# }
# QPushButton {
#     padding: 12px;
#     background-color: #5E81AC;
#     color: white;
#     border: none;
#     border-radius: 5px;
#     font-weight: bold;
# }
# QPushButton:hover {
#     background-color: #81A1C1;
# }
# QPushButton#btn_capture {
#     background-color: #88C0D0; /* Màu xanh lam nhạt */
#     font-size: 16px;
# }
# QPushButton#btn_capture:hover {
#     background-color: #8FBCBB;
# }
# QPushButton:disabled {
#     background-color: #4C566A;
# }
# """

# class AutoCaptureWindow(QMainWindow):
#     finished = Signal()

#     def __init__(self, person_name):
#         super().__init__()
#         self.setWindowTitle("Thêm dữ liệu khuôn mặt (Thủ công)")
#         self.setGeometry(500, 100, 600, 750)
#         self.setFixedSize(600, 750)
#         self.setStyleSheet(STYLE)

#         self.person_name = person_name
#         self.capture_folder = os.path.join("known_faces", self.person_name)
#         os.makedirs(self.capture_folder, exist_ok=True)

#         self.cap = cv2.VideoCapture(0)
#         if not self.cap.isOpened():
#             print("🚫 Không mở được camera.")
#             return

#         self.person_label = QLabel(f"👤 Đang thêm dữ liệu cho: {self.person_name}")
#         self.person_label.setObjectName("person_label")
#         self.person_label.setAlignment(Qt.AlignCenter)

#         self.video_label = QLabel()
#         self.video_label.setObjectName("video_label")
#         self.video_label.setMinimumSize(360, 360)
#         self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.video_label.setAlignment(Qt.AlignCenter)
        
#         # === THÊM LOGIC HƯỚNG DẪN TỪNG BƯỚC ===
#         self.poses_to_capture = ["Chính diện", "Nghiêng trái", "Nghiêng phải"]
#         self.current_pose_index = 0
        
#         self.instruction_label = QLabel()
#         self.instruction_label.setObjectName("instruction_label")
#         self.instruction_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#         self.instruction_label.setWordWrap(True)

#         self.status_label = QLabel("Sẵn sàng chụp...")
#         self.status_label.setObjectName("status_label")
#         self.status_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#         self.status_label.setWordWrap(True)
        
#         self.update_instructions() # Cập nhật hướng dẫn ban đầu

#         self.btn_capture = QPushButton("📸 Chụp ảnh")
#         self.btn_capture.setObjectName("btn_capture")
#         self.btn_capture.clicked.connect(self.manual_capture)

#         self.btn_restart = QPushButton("🔁 Chụp lại từ đầu")
#         self.btn_finish = QPushButton("✅ Hoàn tất")
#         self.btn_restart.clicked.connect(self.restart_capture)
#         self.btn_finish.clicked.connect(self.close)

#         bottom_buttons_layout = QHBoxLayout()
#         bottom_buttons_layout.addWidget(self.btn_restart)
#         bottom_buttons_layout.addWidget(self.btn_finish)
        
#         layout = QVBoxLayout()
#         layout.addWidget(self.person_label)
#         layout.addWidget(self.video_label)
#         layout.addWidget(self.instruction_label)
#         layout.addWidget(self.status_label)
#         layout.addWidget(self.btn_capture)
#         layout.addLayout(bottom_buttons_layout)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#         self.image_index = 1
#         self.face_is_in_zone = False

#         self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
#         self.flash_frames_remaining = 0

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)
    
#     def update_instructions(self):
#         """Cập nhật văn bản hướng dẫn dựa trên trạng thái hiện tại."""
#         if self.current_pose_index < len(self.poses_to_capture):
#             pose_name = self.poses_to_capture[self.current_pose_index]
#             self.instruction_label.setText(f"Đưa mặt vào vùng tròn và chụp góc: **{pose_name}**")
#         else:
#             self.instruction_label.setText("🎉 Đã chụp đủ các góc. Vui lòng nhấn 'Hoàn tất'.")
#             self.btn_capture.setEnabled(False) # Vô hiệu hóa nút chụp

#     def manual_capture(self):
#         if self.face_is_in_zone:
#             ret, frame = self.cap.read()
#             if not ret: return
            
#             frame_to_save = cv2.flip(frame, 1)
            
#             # Lấy tên góc chụp hiện tại để đặt tên file
#             current_pose = self.poses_to_capture[self.current_pose_index]
#             filename = f"{self.person_name}_{current_pose}_{int(time.time())}.jpg"
#             save_path = os.path.join(self.capture_folder, filename)
#             cv2.imwrite(save_path, frame_to_save)
#             print(f"✅ Đã lưu thủ công: {save_path}")

#             self.flash_frames_remaining = 5
#             self.status_label.setText(f"✅ Đã chụp: {current_pose}")
            
#             # Chuyển sang góc chụp tiếp theo
#             self.current_pose_index += 1
#             self.update_instructions()
#         else:
#             self.status_label.setText("⚠️ Không thể chụp, mặt nằm ngoài vùng quét!")

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if not ret: return

#         frame = cv2.flip(frame, 1)

#         if self.flash_frames_remaining > 0:
#             overlay = frame.copy()
#             cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), -1)
#             cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
#             self.flash_frames_remaining -= 1
        
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.face_mesh.process(rgb_frame)

#         h, w = frame.shape[:2]
#         center = (w // 2, h // 2)
#         # === TĂNG KÍCH THƯỚC VÒNG TRÒN ===
#         radius = int(min(w, h) * 0.4) # Tăng từ 0.3 lên 0.4
        
#         circle_color = (0, 0, 255)
#         self.face_is_in_zone = False

#         if results.multi_face_landmarks:
#             face_landmarks = results.multi_face_landmarks[0]
#             nose_tip = face_landmarks.landmark[1]
#             face_center_x, face_center_y = int(nose_tip.x * w), int(nose_tip.y * h)
#             distance = math.sqrt((face_center_x - center[0])**2 + (face_center_y - center[1])**2)

#             if distance < radius:
#                 circle_color = (0, 255, 0)
#                 self.face_is_in_zone = True
        
#         cv2.circle(frame, center, radius, circle_color, 2)
        
#         qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
#         self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
#             self.video_label.width(), self.video_label.height(),
#             Qt.KeepAspectRatio, Qt.SmoothTransformation))

#     def restart_capture(self):
#         if os.path.exists(self.capture_folder):
#             try:
#                 shutil.rmtree(self.capture_folder)
#                 print(f"Đã xóa các ảnh cũ trong thư mục: {self.capture_folder}")
#             except Exception as e:
#                 print(f'Lỗi khi xóa thư mục {self.capture_folder}. Lý do: {e}')
        
#         os.makedirs(self.capture_folder, exist_ok=True)
        
#         # Reset lại trạng thái hướng dẫn
#         self.current_pose_index = 0
#         self.update_instructions()
#         self.status_label.setText("Sẵn sàng chụp...")
#         self.btn_capture.setEnabled(True) # Kích hoạt lại nút chụp

#     def closeEvent(self, event):
#         self.timer.stop()
#         self.cap.release()
#         self.finished.emit()
#         event.accept()


import cv2
import os
import shutil
import time
import math
import mediapipe as mp

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QSizePolicy, QHBoxLayout
)
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QImage, QPixmap

STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
}
QWidget {
    background: transparent;
    color: #f1f5f9;
    font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
}
QWidget#container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
}
QLabel#instruction_label {
    font-size: 16px;
    font-weight: 600;
    color: white;
    padding: 14px 20px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 12px;
}
QLabel#video_label {
    border: 4px solid rgba(102, 126, 234, 0.6);
    border-radius: 20px;
    background-color: #1a1a2e;
}
QLabel#person_label {
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
    padding: 12px 20px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 12px;
    border: 1px solid rgba(102, 126, 234, 0.2);
}
QLabel#status_label {
    font-size: 15px;
    font-weight: 500;
    color: #64748b;
    padding: 10px;
}
QPushButton {
    padding: 14px 28px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #5a67d8);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7c8cf8, stop:1 #667eea);
}
QPushButton:pressed {
    background: #4c51bf;
}
QPushButton#btn_capture {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #10b981, stop:1 #059669);
    font-size: 16px;
    padding: 18px 32px;
}
QPushButton#btn_capture:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #34d399, stop:1 #10b981);
}
QPushButton#btn_restart {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f59e0b, stop:1 #d97706);
}
QPushButton#btn_restart:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #fbbf24, stop:1 #f59e0b);
}
QPushButton#btn_finish {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #5a67d8);
}
QPushButton:disabled {
    background: #94a3b8;
    color: #e2e8f0;
}
QProgressBar {
    background: #e2e8f0;
    border-radius: 8px;
    height: 12px;
    text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 8px;
}
"""

class AutoCaptureWindow(QMainWindow):
    finished = Signal()

    def __init__(self, person_name):
        super().__init__()
        self.setWindowTitle("Add Face Data (Manual)")
        self.setGeometry(500, 100, 600, 750)
        self.setFixedSize(600, 750)
        self.setStyleSheet(STYLE)

        self.person_name = person_name
        self.capture_folder = os.path.join("known_faces", self.person_name)
        os.makedirs(self.capture_folder, exist_ok=True)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("🚫 Cannot open camera.")
            return

        self.person_label = QLabel(f"👤 Adding data for: {self.person_name}")
        self.person_label.setObjectName("person_label")
        self.person_label.setAlignment(Qt.AlignCenter)

        self.video_label = QLabel()
        self.video_label.setObjectName("video_label")
        self.video_label.setMinimumSize(360, 360)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        
        self.instruction_label = QLabel("Align your face inside the circle and press 'Capture'")
        self.instruction_label.setObjectName("instruction_label")
        self.instruction_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.instruction_label.setWordWrap(True)

        self.status_label = QLabel("Ready to capture...")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.status_label.setWordWrap(True)
        
        self.btn_capture = QPushButton("📸 Capture")
        self.btn_capture.setObjectName("btn_capture")
        self.btn_capture.clicked.connect(self.manual_capture)

        self.btn_restart = QPushButton("🔁 Restart")
        self.btn_finish = QPushButton("✅ Finish")
        self.btn_restart.clicked.connect(self.restart_capture)
        self.btn_finish.clicked.connect(self.close)

        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addWidget(self.btn_restart)
        bottom_buttons_layout.addWidget(self.btn_finish)
        
        layout = QVBoxLayout()
        layout.addWidget(self.person_label)
        layout.addWidget(self.video_label)
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.btn_capture)
        layout.addLayout(bottom_buttons_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.captured_count = 0
        self.face_is_in_zone = False

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.flash_frames_remaining = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    
    def manual_capture(self):
        if self.face_is_in_zone:
            ret, frame = self.cap.read()
            if not ret: return
            
            frame_to_save = cv2.flip(frame, 1)
            
            self.captured_count += 1
            filename = f"{self.person_name}_{self.captured_count}.jpg"
            save_path = os.path.join(self.capture_folder, filename)
            cv2.imwrite(save_path, frame_to_save)
            print(f"✅ Saved: {save_path}")

            self.flash_frames_remaining = 5
            self.status_label.setText(f"✅ Captured {self.captured_count} images")
        else:
            self.status_label.setText("⚠️ Cannot capture, face is outside the circle!")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return

        frame = cv2.flip(frame, 1)

        if self.flash_frames_remaining > 0:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), -1)
            cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            self.flash_frames_remaining -= 1
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        radius = int(min(w, h) * 0.4)
        
        circle_color = (0, 0, 255)
        self.face_is_in_zone = False

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            nose_tip = face_landmarks.landmark[1]
            face_center_x, face_center_y = int(nose_tip.x * w), int(nose_tip.y * h)
            distance = math.sqrt((face_center_x - center[0])**2 + (face_center_y - center[1])**2)

            if distance < radius:
                circle_color = (0, 255, 0)
                self.face_is_in_zone = True
        
        cv2.circle(frame, center, radius, circle_color, 2)
        
        qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.video_label.width(), self.video_label.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def restart_capture(self):
        if os.path.exists(self.capture_folder):
            try:
                shutil.rmtree(self.capture_folder)
                print(f"Deleted old images in folder: {self.capture_folder}")
            except Exception as e:
                print(f'Error deleting folder {self.capture_folder}. Reason: {e}')
        
        os.makedirs(self.capture_folder, exist_ok=True)
        
        self.captured_count = 0
        self.status_label.setText("Ready to capture...")
        self.btn_capture.setEnabled(True)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        self.finished.emit()
        event.accept()
