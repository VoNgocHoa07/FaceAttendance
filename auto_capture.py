import cv2
import os
import shutil
import time
import math
import mediapipe as mp

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QSizePolicy, QHBoxLayout, QFrame,
    QProgressBar, QGraphicsDropShadowEffect
)
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QImage, QPixmap, QColor

STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
}

QWidget {
    background: transparent;
    color: #f1f5f9;
    font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
}

QFrame#container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QLabel#instruction_label {
    font-size: 16px;
    font-weight: 600;
    color: white;
    padding: 16px 24px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 14px;
}

QLabel#video_label {
    border: 4px solid rgba(102, 126, 234, 0.5);
    border-radius: 24px;
    background-color: #0a0a0f;
}

QLabel#person_label {
    font-size: 22px;
    font-weight: 700;
    color: white;
    padding: 14px 24px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

QLabel#status_label {
    font-size: 15px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
    padding: 10px;
}

QLabel#counter_label {
    font-size: 48px;
    font-weight: 800;
    color: white;
    background: transparent;
}

QLabel#counter_subtitle {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
}

QPushButton {
    padding: 16px 32px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #5a67d8);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 600;
    font-size: 15px;
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
    font-size: 18px;
    padding: 20px 40px;
    min-width: 200px;
}

QPushButton#btn_capture:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #34d399, stop:1 #10b981);
}

QPushButton#btn_capture:disabled {
    background: rgba(100, 116, 139, 0.3);
    color: rgba(255, 255, 255, 0.4);
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
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

QPushButton#btn_finish:hover {
    background: rgba(255, 255, 255, 0.15);
}

QProgressBar {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    height: 20px;
    text-align: center;
    font-weight: 600;
    color: white;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 10px;
}

QFrame#tip_card {
    background: rgba(102, 126, 234, 0.15);
    border-radius: 12px;
    border: 1px solid rgba(102, 126, 234, 0.3);
    padding: 12px;
}
"""


class AutoCaptureWindow(QMainWindow):
    finished = Signal()

    def __init__(self, person_name):
        super().__init__()
        self.setWindowTitle("📸 Add Face Data")
        self.setGeometry(400, 80, 700, 850)
        self.setFixedSize(700, 850)
        self.setStyleSheet(STYLE)

        self.person_name = person_name
        self.capture_folder = os.path.join("known_faces", self.person_name)
        os.makedirs(self.capture_folder, exist_ok=True)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera.")
            return

        # Main container
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        
        self.person_label = QLabel(f"👤 {self.person_name}")
        self.person_label.setObjectName("person_label")
        header_layout.addWidget(self.person_label)
        
        header_layout.addStretch()
        
        # Counter
        counter_container = QVBoxLayout()
        counter_container.setAlignment(Qt.AlignCenter)
        self.counter_label = QLabel("0")
        self.counter_label.setObjectName("counter_label")
        self.counter_label.setAlignment(Qt.AlignCenter)
        counter_subtitle = QLabel("photos")
        counter_subtitle.setObjectName("counter_subtitle")
        counter_subtitle.setAlignment(Qt.AlignCenter)
        counter_container.addWidget(self.counter_label)
        counter_container.addWidget(counter_subtitle)
        header_layout.addLayout(counter_container)
        
        main_layout.addLayout(header_layout)

        # Video container
        video_container = QFrame()
        video_container.setObjectName("container")
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(16, 16, 16, 16)
        
        self.video_label = QLabel()
        self.video_label.setObjectName("video_label")
        self.video_label.setMinimumSize(600, 450)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        video_layout.addWidget(self.video_label)
        
        # Add shadow to video container
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        video_container.setGraphicsEffect(shadow)
        
        main_layout.addWidget(video_container)

        # Progress bar
        progress_layout = QVBoxLayout()
        progress_header = QHBoxLayout()
        progress_label = QLabel("📊 Capture Progress")
        progress_label.setStyleSheet("font-size: 14px; font-weight: 600; color: white;")
        self.progress_text = QLabel("0 / 3 recommended")
        self.progress_text.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.6);")
        progress_header.addWidget(progress_label)
        progress_header.addStretch()
        progress_header.addWidget(self.progress_text)
        progress_layout.addLayout(progress_header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 3)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v / %m")
        progress_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(progress_layout)

        # Instruction
        self.instruction_label = QLabel("🎯 Position your face inside the circle and press Capture")
        self.instruction_label.setObjectName("instruction_label")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setWordWrap(True)
        main_layout.addWidget(self.instruction_label)

        # Status
        self.status_label = QLabel("💡 Tip: Capture from different angles for better recognition")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        self.btn_restart = QPushButton("🔄 Restart")
        self.btn_restart.setObjectName("btn_restart")
        self.btn_restart.clicked.connect(self.restart_capture)
        
        self.btn_capture = QPushButton("📸 Capture")
        self.btn_capture.setObjectName("btn_capture")
        self.btn_capture.clicked.connect(self.manual_capture)
        
        self.btn_finish = QPushButton("✅ Finish")
        self.btn_finish.setObjectName("btn_finish")
        self.btn_finish.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_restart)
        btn_layout.addWidget(self.btn_capture, 2)
        btn_layout.addWidget(self.btn_finish)
        
        main_layout.addLayout(btn_layout)

        # Initialize
        self.captured_count = 0
        self.face_is_in_zone = False
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.flash_frames_remaining = 0
        self.last_face_position = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def manual_capture(self):
        if self.face_is_in_zone:
            ret, frame = self.cap.read()
            if not ret:
                return

            frame_to_save = cv2.flip(frame, 1)

            self.captured_count += 1
            filename = f"{self.person_name}_{self.captured_count}_{int(time.time())}.jpg"
            save_path = os.path.join(self.capture_folder, filename)
            cv2.imwrite(save_path, frame_to_save)
            print(f"Saved: {save_path}")

            self.flash_frames_remaining = 8
            self.counter_label.setText(str(self.captured_count))
            self.progress_bar.setValue(min(self.captured_count, 3))
            self.progress_text.setText(f"{self.captured_count} / 3 recommended")
            
            if self.captured_count == 1:
                self.status_label.setText("✅ First capture! Try a different angle")
                self.status_label.setStyleSheet("font-size: 15px; color: #10b981;")
            elif self.captured_count == 2:
                self.status_label.setText("✅ Great! One more angle recommended")
                self.status_label.setStyleSheet("font-size: 15px; color: #10b981;")
            elif self.captured_count >= 3:
                self.status_label.setText("🎉 Perfect! You can finish or capture more")
                self.status_label.setStyleSheet("font-size: 15px; color: #f59e0b;")
                self.instruction_label.setText("🎉 Minimum captures complete! Click Finish or continue")
        else:
            self.status_label.setText("⚠️ Please position your face inside the circle")
            self.status_label.setStyleSheet("font-size: 15px; color: #ef4444;")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        display_frame = frame.copy()

        # Flash effect
        if self.flash_frames_remaining > 0:
            overlay = display_frame.copy()
            alpha = self.flash_frames_remaining / 8 * 0.4
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (129, 230, 217), -1)
            cv2.addWeighted(overlay, alpha, display_frame, 1 - alpha, 0, display_frame)
            self.flash_frames_remaining -= 1

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        radius = int(min(w, h) * 0.38)

        self.face_is_in_zone = False
        circle_color = (100, 100, 100)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            nose_tip = face_landmarks.landmark[1]
            face_center_x, face_center_y = int(nose_tip.x * w), int(nose_tip.y * h)
            distance = math.sqrt((face_center_x - center[0])**2 + (face_center_y - center[1])**2)

            if distance < radius * 0.7:
                circle_color = (129, 230, 217)  # Teal - good position
                self.face_is_in_zone = True
                self.btn_capture.setEnabled(True)
            elif distance < radius:
                circle_color = (102, 126, 234)  # Blue - close
                self.face_is_in_zone = True
                self.btn_capture.setEnabled(True)
            else:
                circle_color = (234, 126, 102)  # Coral - too far
                self.btn_capture.setEnabled(False)

            # Draw face indicator
            cv2.circle(display_frame, (face_center_x, face_center_y), 8, circle_color, -1)
        else:
            self.btn_capture.setEnabled(False)

        # Draw guide circle with glow effect
        for i in range(3, 0, -1):
            alpha = 0.3 / i
            overlay = display_frame.copy()
            cv2.circle(overlay, center, radius + i * 3, circle_color, 2)
            cv2.addWeighted(overlay, alpha, display_frame, 1 - alpha, 0, display_frame)
        
        cv2.circle(display_frame, center, radius, circle_color, 3)

        # Draw corner guides
        corner_length = 30
        corner_offset = int(radius * 0.8)
        corners = [
            (center[0] - corner_offset, center[1] - corner_offset),
            (center[0] + corner_offset, center[1] - corner_offset),
            (center[0] - corner_offset, center[1] + corner_offset),
            (center[0] + corner_offset, center[1] + corner_offset),
        ]
        
        for cx, cy in corners:
            if cx < center[0]:
                cv2.line(display_frame, (cx, cy), (cx + corner_length, cy), circle_color, 2)
            else:
                cv2.line(display_frame, (cx, cy), (cx - corner_length, cy), circle_color, 2)
            if cy < center[1]:
                cv2.line(display_frame, (cx, cy), (cx, cy + corner_length), circle_color, 2)
            else:
                cv2.line(display_frame, (cx, cy), (cx, cy - corner_length), circle_color, 2)

        # Draw center crosshair
        crosshair_size = 15
        cv2.line(display_frame, (center[0] - crosshair_size, center[1]),
                 (center[0] + crosshair_size, center[1]), circle_color, 1)
        cv2.line(display_frame, (center[0], center[1] - crosshair_size),
                 (center[0], center[1] + crosshair_size), circle_color, 1)

        # Convert and display
        qt_image = QImage(display_frame.data, display_frame.shape[1], display_frame.shape[0], 
                         QImage.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.video_label.width(), self.video_label.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def restart_capture(self):
        if os.path.exists(self.capture_folder):
            try:
                shutil.rmtree(self.capture_folder)
                print(f"Deleted folder: {self.capture_folder}")
            except Exception as e:
                print(f'Error: {e}')

        os.makedirs(self.capture_folder, exist_ok=True)

        self.captured_count = 0
        self.counter_label.setText("0")
        self.progress_bar.setValue(0)
        self.progress_text.setText("0 / 3 recommended")
        self.status_label.setText("💡 Tip: Capture from different angles for better recognition")
        self.status_label.setStyleSheet("font-size: 15px; color: rgba(255,255,255,0.7);")
        self.instruction_label.setText("🎯 Position your face inside the circle and press Capture")
        self.btn_capture.setEnabled(True)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        self.finished.emit()
        event.accept()
