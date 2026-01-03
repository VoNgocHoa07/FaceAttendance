
import sys
import os
import cv2
import shutil
import time
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import threading
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QInputDialog,
                               QScrollArea, QMessageBox, QFrame, QSizePolicy,
                               QFileDialog, QDialog, QTableWidget, QTableWidgetItem,
                               QLineEdit, QComboBox, QGraphicsDropShadowEffect,
                               QProgressBar, QSpacerItem, QGridLayout, QStackedWidget)
from PySide6.QtGui import QImage, QPixmap, QFont, QColor, QPainter, QBrush, QPen, QLinearGradient
from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QPropertyAnimation, QEasingCurve, QRect, Property, QSize

from cv_logic import CVLogic
from auto_capture import AutoCaptureWindow

# ============== MODERN GLASS MORPHISM STYLE ==============
MODERN_STYLE = """
* {
    font-family: 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
}

QWidget#central_widget {
    background: transparent;
}

QFrame#glass_card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

QFrame#sidebar {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.5);
}

QFrame#video_frame {
    background: #1a1a2e;
    border-radius: 20px;
    border: 4px solid rgba(102, 126, 234, 0.6);
}

QLabel#app_title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    background: transparent;
    padding: 10px;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
    padding: 12px 16px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border-radius: 12px;
}

QLabel#stat_number {
    font-size: 36px;
    font-weight: 800;
    color: #667eea;
}

QLabel#stat_label {
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
}

QLabel#video_label {
    background: #0f0f1a;
    border-radius: 16px;
}

QLabel#time_label {
    font-size: 42px;
    font-weight: 300;
    color: #ffffff;
    background: transparent;
}

QLabel#date_label {
    font-size: 16px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    background: transparent;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #667eea, stop:1 #5a67d8);
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7c8cf8, stop:1 #667eea);
}

QPushButton:pressed {
    background: #4c51bf;
}

QPushButton#btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    padding: 16px 32px;
    font-size: 15px;
}

QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c8cf8, stop:1 #8b5cf6);
}

QPushButton#btn_success {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #10b981, stop:1 #059669);
}

QPushButton#btn_success:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #34d399, stop:1 #10b981);
}

QPushButton#btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ef4444, stop:1 #dc2626);
}

QPushButton#btn_danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f87171, stop:1 #ef4444);
}

QPushButton#btn_warning {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f59e0b, stop:1 #d97706);
}

QPushButton#btn_warning:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #fbbf24, stop:1 #f59e0b);
}

QPushButton#btn_secondary {
    background: rgba(100, 116, 139, 0.1);
    color: #475569;
    border: 2px solid #e2e8f0;
}

QPushButton#btn_secondary:hover {
    background: rgba(100, 116, 139, 0.2);
    border-color: #cbd5e1;
}

QPushButton#btn_icon {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
    padding: 12px;
    border-radius: 12px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
}

QPushButton#btn_icon:hover {
    background: rgba(102, 126, 234, 0.2);
}

QLineEdit {
    background: rgba(241, 245, 249, 0.8);
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    color: #1e293b;
}

QLineEdit:focus {
    border-color: #667eea;
    background: white;
}

QLineEdit::placeholder {
    color: #94a3b8;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: rgba(241, 245, 249, 0.5);
    width: 8px;
    border-radius: 4px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: rgba(102, 126, 234, 0.4);
    border-radius: 4px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(102, 126, 234, 0.6);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QFrame#attendance_card {
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 8px;
}

QFrame#attendance_card:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.05);
}

QFrame#stat_card {
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    padding: 16px;
}

QComboBox {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 14px;
    color: #1e293b;
    min-width: 120px;
}

QComboBox:hover {
    border-color: #667eea;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    selection-background-color: #667eea;
}

QTableWidget {
    background: white;
    border: none;
    border-radius: 12px;
    gridline-color: #f1f5f9;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected {
    background: rgba(102, 126, 234, 0.1);
    color: #1e293b;
}

QHeaderView::section {
    background: #f8fafc;
    color: #475569;
    font-weight: 600;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
}

QProgressBar {
    background: #e2e8f0;
    border-radius: 8px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 8px;
}
"""


class AnimatedButton(QPushButton):
    """Button với animation hover effect"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        super().leaveEvent(event)


class StatCard(QFrame):
    """Card hiển thị thống kê"""
    def __init__(self, icon, value, label, color="#667eea", parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        self.setFixedSize(160, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Icon và số
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"font-size: 32px; font-weight: 800; color: {color};")
        
        self.text_label = QLabel(label)
        self.text_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748b;")
        
        layout.addLayout(top_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(self.text_label)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)
        
    def update_value(self, value):
        self.value_label.setText(str(value))


class AttendanceCard(QFrame):
    """Card hiển thị thông tin điểm danh"""
    edit_clicked = Signal(str)
    delete_clicked = Signal(str)
    
    def __init__(self, name, time, session, parent=None):
        super().__init__(parent)
        self.name = name
        self.setObjectName("attendance_card")
        self.setFixedHeight(70)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Avatar
        avatar = QLabel("👤")
        avatar.setStyleSheet("""
            font-size: 24px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 20px;
            padding: 8px;
            min-width: 40px;
            max-width: 40px;
            min-height: 40px;
            max-height: 40px;
        """)
        avatar.setAlignment(Qt.AlignCenter)
        layout.addWidget(avatar)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #1e293b;")
        
        time_label = QLabel(f"🕐 {time} • {session}")
        time_label.setStyleSheet("font-size: 12px; color: #64748b;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(time_label)
        layout.addLayout(info_layout, 1)
        
        # Status badge
        status = QLabel("✓")
        status.setStyleSheet("""
            background: #10b981;
            color: white;
            font-size: 12px;
            font-weight: bold;
            padding: 6px 12px;
            border-radius: 12px;
        """)
        layout.addWidget(status)
        
        # Actions
        btn_edit = QPushButton("✏️")
        btn_edit.setObjectName("btn_icon")
        btn_edit.setFixedSize(36, 36)
        btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.name))
        
        btn_del = QPushButton("🗑️")
        btn_del.setObjectName("btn_icon")
        btn_del.setFixedSize(36, 36)
        btn_del.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.1);
                color: #ef4444;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.2);
            }
        """)
        btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.name))
        
        layout.addWidget(btn_edit)
        layout.addWidget(btn_del)


class Worker(QThread):
    ImageUpdate = Signal(QImage, list)
    FaceDetected = Signal(int)

    def __init__(self, cv_logic):
        super().__init__()
        self.cv_logic = cv_logic
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        self.reload_data_flag = False

    def run(self):
        while self.running:
            if self.reload_data_flag:
                self.cv_logic.load_known_faces()
                self.reload_data_flag = False

            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.cv_logic.process_frame_with_tracking(rgb_frame, self.frame_count)
            self.frame_count += 1
            
            # Emit số lượng khuôn mặt detected
            self.FaceDetected.emit(len(results))

            h, w, ch = frame.shape
            qt_image = QImage(frame.data, w, h, ch * w, QImage.Format_BGR888)
            self.ImageUpdate.emit(qt_image, results)
            time.sleep(0.02)

    def stop(self):
        self.running = False
        self.wait()
        self.cap.release()


class MainWindow(QMainWindow):
    def __init__(self, screen_geometry):
        super().__init__()
        self.setWindowTitle("Face Recognition Attendance System")
        self.setStyleSheet(MODERN_STYLE)

        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.setGeometry(0, 0, screen_width, screen_height - 50)

        self.cv_logic = CVLogic()
        self.current_person_name = ""
        self.attendance_list = {}
        self.records_folder = os.path.join(os.getcwd(), "attendance_records")
        os.makedirs(self.records_folder, exist_ok=True)
        self.master_file = os.path.join(self.records_folder, "attendance_master.csv")
        
        if not os.path.exists(self.master_file):
            pd.DataFrame(columns=["Name", "Check-in Datetime", "Attendance Date", "Session"]).to_csv(
                self.master_file, index=False, encoding="utf-8-sig")

        self.init_ui()
        self.init_worker()
        self.start_clock()

    def init_ui(self):
        central = QWidget()
        central.setObjectName("central_widget")
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ============== LEFT PANEL (Video + Stats) ==============
        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        # Header với time
        header = QHBoxLayout()
        
        # App title
        title = QLabel("🎯 Face Attendance")
        title.setObjectName("app_title")
        header.addWidget(title)
        
        header.addStretch()
        
        # Clock
        clock_layout = QVBoxLayout()
        clock_layout.setAlignment(Qt.AlignRight)
        self.time_label = QLabel("00:00:00")
        self.time_label.setObjectName("time_label")
        self.date_label = QLabel("Thursday, Nov 28, 2025")
        self.date_label.setObjectName("date_label")
        clock_layout.addWidget(self.time_label)
        clock_layout.addWidget(self.date_label)
        header.addLayout(clock_layout)
        
        left_panel.addLayout(header)

        # Video Frame
        video_container = QFrame()
        video_container.setObjectName("video_frame")
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(8, 8, 8, 8)
        
        self.video_label = QLabel()
        self.video_label.setObjectName("video_label")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(800, 500)
        self.video_label.setStyleSheet("background: #0f0f1a; border-radius: 12px;")
        video_layout.addWidget(self.video_label)
        
        # Video overlay info
        self.face_count_label = QLabel("👥 0 faces detected")
        self.face_count_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255,255,255,0.8);
            background: rgba(0,0,0,0.5);
            padding: 8px 16px;
            border-radius: 8px;
        """)
        video_layout.addWidget(self.face_count_label, alignment=Qt.AlignCenter)
        
        left_panel.addWidget(video_container, 1)

        # Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_total = StatCard("👥", self.get_total_members(), "Total Members", "#667eea")
        self.stat_today = StatCard("📅", len(self.attendance_list), "Today", "#10b981")
        self.stat_week = StatCard("📊", self.get_week_attendance(), "This Week", "#f59e0b")
        self.stat_rate = StatCard("📈", f"{self.get_attendance_rate()}%", "Rate", "#8b5cf6")
        
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_today)
        stats_layout.addWidget(self.stat_week)
        stats_layout.addWidget(self.stat_rate)
        stats_layout.addStretch()
        
        left_panel.addLayout(stats_layout)
        
        main_layout.addLayout(left_panel, 2)

        # ============== RIGHT PANEL (Sidebar) ==============
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(400)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(16)

        # Control Section
        control_title = QLabel("⚡ Quick Actions")
        control_title.setObjectName("section_title")
        sidebar_layout.addWidget(control_title)

        # Action Buttons Grid
        btn_grid = QGridLayout()
        btn_grid.setSpacing(12)
        
        btn_add = QPushButton("➕ Add Person")
        btn_add.setObjectName("btn_primary")
        btn_add.setFixedHeight(50)
        btn_add.clicked.connect(self.add_new_person)
        
        btn_reset = QPushButton("🔄 Reset")
        btn_reset.setObjectName("btn_warning")
        btn_reset.setFixedHeight(50)
        btn_reset.clicked.connect(self.reset_attendance)
        
        btn_export = QPushButton("📤 Export")
        btn_export.setObjectName("btn_success")
        btn_export.setFixedHeight(50)
        btn_export.clicked.connect(self.export_attendance_excel)
        
        btn_history = QPushButton("📋 History")
        btn_history.setObjectName("btn_secondary")
        btn_history.setFixedHeight(50)
        btn_history.clicked.connect(self.open_master_list)
        
        btn_grid.addWidget(btn_add, 0, 0)
        btn_grid.addWidget(btn_reset, 0, 1)
        btn_grid.addWidget(btn_export, 1, 0)
        btn_grid.addWidget(btn_history, 1, 1)
        
        sidebar_layout.addLayout(btn_grid)

        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search attendee...")
        self.search_input.textChanged.connect(self.filter_attendance)
        search_layout.addWidget(self.search_input)
        sidebar_layout.addLayout(search_layout)

        # Attendance List Title
        list_header = QHBoxLayout()
        list_title = QLabel("📋 Today's Attendance")
        list_title.setObjectName("section_title")
        list_header.addWidget(list_title)
        
        self.attendance_count = QLabel("0")
        self.attendance_count.setStyleSheet("""
            background: #667eea;
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 12px;
        """)
        list_header.addWidget(self.attendance_count)
        
        sidebar_layout.addLayout(list_header)

        # Attendance Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.attendance_widget = QWidget()
        self.attendance_layout = QVBoxLayout(self.attendance_widget)
        self.attendance_layout.setAlignment(Qt.AlignTop)
        self.attendance_layout.setSpacing(8)
        self.attendance_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self.attendance_widget)
        
        sidebar_layout.addWidget(scroll, 1)

        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        btn_members = QPushButton("👥 Members")
        btn_members.setObjectName("btn_secondary")
        btn_members.clicked.connect(self.show_members_dialog)
        
        btn_quit = QPushButton("🚪 Exit")
        btn_quit.setObjectName("btn_danger")
        btn_quit.clicked.connect(self.close)
        
        bottom_layout.addWidget(btn_members)
        bottom_layout.addWidget(btn_quit)
        
        sidebar_layout.addLayout(bottom_layout)

        # Shadow effect cho sidebar
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(-5)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 40))
        sidebar.setGraphicsEffect(shadow)

        main_layout.addWidget(sidebar)

        # Success overlay (hidden by default)
        self.success_overlay = QLabel(self.video_label)
        self.success_overlay.setAlignment(Qt.AlignCenter)
        self.success_overlay.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(16, 185, 129, 0.95), stop:1 rgba(5, 150, 105, 0.95));
            padding: 16px 32px;
            border-radius: 12px;
        """)
        self.success_overlay.setFixedSize(400, 60)
        self.success_overlay.hide()

    def init_worker(self):
        self.worker = Worker(self.cv_logic)
        self.worker.ImageUpdate.connect(self.update_frame)
        self.worker.FaceDetected.connect(self.update_face_count)
        self.worker.start()

    def start_clock(self):
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
        self.date_label.setText(now.strftime("%A, %b %d, %Y"))

    def get_total_members(self):
        known_dir = os.path.join(os.getcwd(), "known_faces")
        if os.path.exists(known_dir):
            return len([d for d in os.listdir(known_dir) if os.path.isdir(os.path.join(known_dir, d))])
        return 0

    def get_week_attendance(self):
        try:
            if os.path.exists(self.master_file):
                df = pd.read_csv(self.master_file)
                if len(df) > 0:
                    today = datetime.now().date()
                    week_ago = today - timedelta(days=7)
                    df['Attendance Date'] = pd.to_datetime(df['Attendance Date']).dt.date
                    week_data = df[df['Attendance Date'] >= week_ago]
                    return len(week_data)
        except:
            pass
        return 0

    def get_attendance_rate(self):
        total = self.get_total_members()
        today = len(self.attendance_list)
        if total > 0:
            return int((today / total) * 100)
        return 0

    def update_stats(self):
        self.stat_total.update_value(self.get_total_members())
        self.stat_today.update_value(len(self.attendance_list))
        self.stat_week.update_value(self.get_week_attendance())
        self.stat_rate.update_value(f"{self.get_attendance_rate()}%")
        self.attendance_count.setText(str(len(self.attendance_list)))

    @Slot(int)
    def update_face_count(self, count):
        self.face_count_label.setText(f"👥 {count} face{'s' if count != 1 else ''} detected")

    def get_session_from_hour(self, hour: int) -> str:
        if 5 <= hour < 12:
            return "Morning"
        if 12 <= hour < 17:
            return "Afternoon"
        if 17 <= hour < 22:
            return "Evening"
        return "Night"

    @Slot(QImage, list)
    def update_frame(self, qt_image, results):
        buffer = qt_image.constBits()
        arr = np.frombuffer(buffer.tobytes(), dtype=np.uint8).reshape(
            (qt_image.height(), qt_image.width(), qt_image.depth() // 8))
        frame_to_draw = arr.copy()

        for (top, right, bottom, left), display_name, status, confirmed_name in results:
            # Modern bounding box colors
            if status == "Confirming":
                color = (234, 126, 102)  # Coral
                thickness = 2
            elif status == "Recognized":
                color = (129, 230, 217)  # Teal
                thickness = 3
                if confirmed_name not in self.attendance_list:
                    now_dt = datetime.now()
                    time_only = now_dt.strftime("%H:%M:%S")
                    date_only = now_dt.strftime("%Y-%m-%d")
                    session = self.get_session_from_hour(now_dt.hour)
                    
                    self.attendance_list[confirmed_name] = {
                        "datetime": time_only,
                        "date": date_only,
                        "session": session
                    }
                    self.cv_logic.checked_in_names.add(confirmed_name)
                    self.add_attendance_card(confirmed_name, time_only, session, date_only)
                    self.show_success_status(confirmed_name)
                    self.update_stats()
                    self.play_success_sound()
            elif status == "Checked-in":
                color = (94, 172, 86)  # Green
                thickness = 2
            else:
                color = (208, 135, 112)
                thickness = 2

            # Draw rounded rectangle effect
            cv2.rectangle(frame_to_draw, (left, top), (right, bottom), color, thickness)
            
            # Draw name with background
            label_size = cv2.getTextSize(display_name, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame_to_draw, 
                         (left, top - label_size[1] - 10),
                         (left + label_size[0] + 10, top),
                         color, -1)
            cv2.putText(frame_to_draw, display_name, 
                       (left + 5, top - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        h, w, ch = frame_to_draw.shape
        final_image = QImage(frame_to_draw.data, w, h, ch * w, QImage.Format_BGR888)
        
        pixmap = QPixmap.fromImage(final_image)
        self.video_label.setPixmap(pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def add_attendance_card(self, name, time, session, date=None):
        card = AttendanceCard(name, time, session)
        card.edit_clicked.connect(self.edit_attendee)
        card.delete_clicked.connect(self.delete_attendee)
        card._att_datetime = time
        card._att_date = date
        self.attendance_layout.insertWidget(0, card)
        
        # Save to CSV
        try:
            attendance_date = date if date else datetime.now().strftime("%Y-%m-%d")
            row_df = pd.DataFrame([{
                "Name": name,
                "Check-in Datetime": time,
                "Attendance Date": attendance_date,
                "Session": session
            }])
            write_header = not os.path.exists(self.master_file)
            row_df.to_csv(self.master_file, mode='a', header=write_header, 
                         index=False, encoding="utf-8-sig")
        except Exception as e:
            print("Failed to save:", e)

    def show_success_status(self, name: str):
        self.success_overlay.setText(f"✅ {name} - Check-in successful!")
        
        # Center the overlay
        vw = self.video_label.width()
        vh = self.video_label.height()
        sw = self.success_overlay.width()
        sh = self.success_overlay.height()
        x = (vw - sw) // 2
        y = 20
        self.success_overlay.move(x, y)
        self.success_overlay.show()
        self.success_overlay.raise_()
        
        QTimer.singleShot(2000, self.success_overlay.hide)

    def play_success_sound(self):
        # Có thể thêm sound notification ở đây
        pass

    def filter_attendance(self, text):
        for i in range(self.attendance_layout.count()):
            widget = self.attendance_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'name'):
                widget.setVisible(text.lower() in widget.name.lower())

    def add_new_person(self):
        text, ok = QInputDialog.getText(self, "Add New Person", 
                                        "Enter person's name:",
                                        QLineEdit.Normal)
        if ok and text:
            self.current_person_name = text.strip()
            os.makedirs(os.path.join("known_faces", self.current_person_name), exist_ok=True)
            self.worker.stop()
            self.auto_window = AutoCaptureWindow(self.current_person_name)
            self.auto_window.finished.connect(self.auto_capture_done)
            self.auto_window.show()

    @Slot()
    def auto_capture_done(self):
        self.init_worker()
        self.worker.reload_data_flag = True
        self.update_stats()
        QMessageBox.information(self, "Success", 
                               f"Successfully added {self.current_person_name}!")
        self.current_person_name = ""

    def edit_attendee(self, name):
        new_name, ok = QInputDialog.getText(self, "Edit", "New name:", text=name)
        if ok and new_name and new_name.strip() != name:
            new_name = new_name.strip()
            if name in self.attendance_list:
                self.attendance_list[new_name] = self.attendance_list.pop(name)
            # Update UI
            for i in range(self.attendance_layout.count()):
                widget = self.attendance_layout.itemAt(i).widget()
                if widget and getattr(widget, 'name', None) == name:
                    widget.name = new_name
                    break

    def delete_attendee(self, name):
        reply = QMessageBox.question(self, "Delete", 
                                    f"Remove {name} from today's attendance?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.attendance_list.pop(name, None)
            for i in range(self.attendance_layout.count()):
                widget = self.attendance_layout.itemAt(i).widget()
                if widget and getattr(widget, 'name', None) == name:
                    widget.deleteLater()
                    break
            self.update_stats()

    def reset_attendance(self):
        reply = QMessageBox.question(self, "Reset", 
                                    "Clear today's attendance list?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.attendance_list.clear()
            
            if hasattr(self.cv_logic, "checked_in_names"):
                self.cv_logic.checked_in_names.clear()
            
            for i in reversed(range(self.attendance_layout.count())):
                widget = self.attendance_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            self.update_stats()

    def export_attendance_excel(self):
        if not self.attendance_list:
            QMessageBox.information(self, "No Data", "No attendance data to export.")
            return
            
        now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Attendance", 
            f"attendance_{now}.xlsx",
            "Excel Files (*.xlsx);;CSV Files (*.csv)")
        
        if not file_path:
            return
            
        try:
            rows = []
            for name, data in self.attendance_list.items():
                rows.append({
                    "Name": name,
                    "Check-in Time": data.get("datetime", ""),
                    "Date": data.get("date", ""),
                    "Session": data.get("session", "")
                })
            
            df = pd.DataFrame(rows)
            if file_path.endswith(".csv"):
                df.to_csv(file_path, index=False, encoding="utf-8-sig")
            else:
                df.to_excel(file_path, index=False)
            
            QMessageBox.information(self, "Success", f"Exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def open_master_list(self):
        try:
            df = pd.read_csv(self.master_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot read file: {e}")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Attendance History")
        dlg.setStyleSheet(MODERN_STYLE)
        dlg.resize(1000, 600)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("📊 Attendance History")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b; margin-bottom: 16px;")
        layout.addWidget(header)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(list(df.columns))
        table.setRowCount(len(df))
        
        for r in range(len(df)):
            for c, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[r, c]))
                table.setItem(r, c, item)
        
        table.resizeColumnsToContents()
        table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_delete = QPushButton("🗑️ Delete Selected")
        btn_delete.setObjectName("btn_danger")
        btn_delete.clicked.connect(lambda: self.delete_history_rows(table, dlg))
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btn_secondary")
        btn_close.clicked.connect(dlg.close)
        
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
        
        dlg.exec()

    def delete_history_rows(self, table, dialog):
        selected = table.selectionModel().selectedRows()
        if not selected:
            return
        
        if QMessageBox.question(dialog, "Delete", 
                               f"Delete {len(selected)} records?") == QMessageBox.Yes:
            rows = sorted([s.row() for s in selected], reverse=True)
            try:
                df = pd.read_csv(self.master_file)
                df = df.drop(df.index[rows])
                df.to_csv(self.master_file, index=False, encoding="utf-8-sig")
                for r in rows:
                    table.removeRow(r)
            except Exception as e:
                QMessageBox.critical(dialog, "Error", str(e))

    def show_members_dialog(self):
        known_dir = os.path.join(os.getcwd(), "known_faces")
        if not os.path.exists(known_dir):
            os.makedirs(known_dir)
        
        members = sorted([d for d in os.listdir(known_dir) 
                         if os.path.isdir(os.path.join(known_dir, d))])
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Members")
        dlg.setStyleSheet(MODERN_STYLE)
        dlg.resize(500, 600)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel(f"👥 Members ({len(members)})")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(8)
        
        for name in members:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 12px;
                    border: 1px solid #e2e8f0;
                    padding: 12px;
                }
                QFrame:hover {
                    border-color: #667eea;
                }
            """)
            card_layout = QHBoxLayout(card)
            
            avatar = QLabel("👤")
            avatar.setStyleSheet("font-size: 24px;")
            card_layout.addWidget(avatar)
            
            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #1e293b;")
            card_layout.addWidget(name_label, 1)
            
            btn_delete = QPushButton("🗑️")
            btn_delete.setObjectName("btn_icon")
            btn_delete.setFixedSize(36, 36)
            btn_delete.clicked.connect(lambda _, n=name, c=card: self.delete_member(n, c, dlg))
            card_layout.addWidget(btn_delete)
            
            content_layout.addWidget(card)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btn_secondary")
        btn_close.clicked.connect(dlg.close)
        layout.addWidget(btn_close)
        
        dlg.exec()

    def delete_member(self, name, card, dialog):
        if QMessageBox.question(dialog, "Delete Member",
                               f"Delete '{name}' and all their photos?",
                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                path = os.path.join(os.getcwd(), "known_faces", name)
                if os.path.exists(path):
                    shutil.rmtree(path)
                card.deleteLater()
                self.worker.reload_data_flag = True
                self.update_stats()
            except Exception as e:
                QMessageBox.warning(dialog, "Error", str(e))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'success_overlay') and hasattr(self, 'video_label'):
            vw = self.video_label.width()
            sw = self.success_overlay.width()
            x = (vw - sw) // 2
            self.success_overlay.move(max(0, x), 20)

    def closeEvent(self, event):
        self.worker.stop()
        if hasattr(self, 'clock_timer'):
            self.clock_timer.stop()
        event.accept()


if __name__ == "__main__":
    import traceback
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        screen = app.primaryScreen()
        if screen:
            geometry = screen.geometry()
        else:
            class DefaultGeometry:
                def width(self): return 1440
                def height(self): return 900
            geometry = DefaultGeometry()
        
        window = MainWindow(geometry)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
