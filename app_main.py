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
                               QProgressBar, QSpacerItem, QGridLayout, QStackedWidget,
                               QSlider, QCheckBox, QTabWidget, QSpinBox, QHeaderView,
                               QCalendarWidget, QDateEdit)
from PySide6.QtGui import (QImage, QPixmap, QFont, QColor, QPainter, QBrush, QPen, 
                           QLinearGradient, QIcon, QPainterPath, QRadialGradient)
from PySide6.QtCore import (Qt, QThread, Signal, Slot, QTimer, QPropertyAnimation, 
                            QEasingCurve, QRect, Property, QSize, QDate, QPoint)

from cv_logic import CVLogic
from auto_capture import AutoCaptureWindow

# ============== ENHANCED MODERN STYLE ==============
MODERN_STYLE = """
* {
    font-family: 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
}

QWidget#central_widget {
    background: transparent;
}

QFrame#glass_card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

QFrame#sidebar {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.5);
}

QFrame#video_frame {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 24px;
    border: 3px solid rgba(102, 126, 234, 0.5);
}

QFrame#left_panel_frame {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QLabel#app_title {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    background: transparent;
    padding: 10px;
}

QLabel#app_subtitle {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    background: transparent;
}

QLabel#section_title {
    font-size: 16px;
    font-weight: 700;
    color: white;
    padding: 12px 20px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 12px;
}

QLabel#section_title_dark {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    padding: 8px 0;
    background: transparent;
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
    background: #0a0a0f;
    border-radius: 20px;
}

QLabel#time_label {
    font-size: 56px;
    font-weight: 200;
    color: #ffffff;
    background: transparent;
    letter-spacing: 2px;
}

QLabel#date_label {
    font-size: 18px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
    background: transparent;
}

QLabel#status_online {
    font-size: 13px;
    font-weight: 600;
    color: #10b981;
    background: rgba(16, 185, 129, 0.15);
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid rgba(16, 185, 129, 0.3);
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

QPushButton#btn_glass {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 12px 24px;
    border-radius: 12px;
}

QPushButton#btn_glass:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
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

QPushButton#btn_icon_dark {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    padding: 10px;
    border-radius: 10px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

QPushButton#btn_icon_dark:hover {
    background: rgba(255, 255, 255, 0.2);
}

QPushButton#nav_btn {
    background: transparent;
    color: rgba(255, 255, 255, 0.6);
    padding: 14px 20px;
    border-radius: 12px;
    text-align: left;
    font-size: 14px;
}

QPushButton#nav_btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

QPushButton#nav_btn_active {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(102, 126, 234, 0.3), stop:1 rgba(118, 75, 162, 0.3));
    color: white;
    padding: 14px 20px;
    border-radius: 12px;
    text-align: left;
    font-size: 14px;
    border-left: 3px solid #667eea;
}

QLineEdit {
    background: rgba(241, 245, 249, 0.9);
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

QLineEdit#search_dark {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 12px 16px 12px 40px;
}

QLineEdit#search_dark:focus {
    border-color: #667eea;
    background: rgba(255, 255, 255, 0.12);
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: rgba(255, 255, 255, 0.05);
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
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

QFrame#attendance_card:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.02);
}

QFrame#attendance_card_dark {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QFrame#attendance_card_dark:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.5);
}

QFrame#stat_card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
}

QFrame#stat_card_dark {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
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
    padding: 14px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
}

QProgressBar {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 8px;
}

QSlider::groove:horizontal {
    background: rgba(255, 255, 255, 0.1);
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #667eea;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #7c8cf8;
}

QTabWidget::pane {
    border: none;
    background: transparent;
}

QTabBar::tab {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.6);
    padding: 12px 24px;
    border-radius: 8px;
    margin-right: 8px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    color: white;
}

QTabBar::tab:hover:!selected {
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

QCheckBox {
    color: white;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    background: transparent;
}

QCheckBox::indicator:checked {
    background: #667eea;
    border-color: #667eea;
}

QSpinBox {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 8px;
    color: white;
}

QCalendarWidget {
    background: white;
    border-radius: 12px;
}

QCalendarWidget QToolButton {
    color: #1e293b;
    background: transparent;
    padding: 8px;
}

QCalendarWidget QMenu {
    background: white;
}

QCalendarWidget QSpinBox {
    background: white;
    color: #1e293b;
}
"""


class GlowEffect(QGraphicsDropShadowEffect):
    """Hiệu ứng glow cho các thành phần"""
    def __init__(self, color="#667eea", blur=30, parent=None):
        super().__init__(parent)
        self.setBlurRadius(blur)
        self.setXOffset(0)
        self.setYOffset(0)
        self.setColor(QColor(color))


class AnimatedStatCard(QFrame):
    """Card thống kê với animation"""
    def __init__(self, icon, value, label, color="#667eea", trend=None, parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card_dark")
        self.setFixedSize(180, 140)
        self.color = color
        self._value = 0
        self.target_value = value if isinstance(value, int) else 0
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        top_layout = QHBoxLayout()
        icon_container = QLabel(icon)
        icon_container.setStyleSheet(f"""
            font-size: 28px;
            background: {color}20;
            padding: 10px;
            border-radius: 12px;
        """)
        top_layout.addWidget(icon_container)
        top_layout.addStretch()
        
        if trend:
            trend_label = QLabel(trend)
            trend_color = "#10b981" if "+" in trend else "#ef4444"
            trend_label.setStyleSheet(f"""
                font-size: 12px;
                font-weight: 600;
                color: {trend_color};
                background: {trend_color}15;
                padding: 4px 8px;
                border-radius: 6px;
            """)
            top_layout.addWidget(trend_label)
        
        layout.addLayout(top_layout)
        
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"""
            font-size: 36px;
            font-weight: 800;
            color: white;
        """)
        layout.addWidget(self.value_label)
        
        self.text_label = QLabel(label)
        self.text_label.setStyleSheet("font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.6);")
        layout.addWidget(self.text_label)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
        
    def update_value(self, value):
        self.value_label.setText(str(value))

    def animate_value(self, target):
        self.target_value = target
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_step)
        self.animation_timer.start(30)
    
    def _animate_step(self):
        if self._value < self.target_value:
            self._value += max(1, (self.target_value - self._value) // 5)
            self.value_label.setText(str(self._value))
        else:
            self._value = self.target_value
            self.value_label.setText(str(self._value))
            self.animation_timer.stop()


class ModernAttendanceCard(QFrame):
    """Card điểm danh hiện đại"""
    edit_clicked = Signal(str)
    delete_clicked = Signal(str)
    
    def __init__(self, name, time, session, avatar_color=None, parent=None):
        super().__init__(parent)
        self.name = name
        self.setObjectName("attendance_card_dark")
        self.setFixedHeight(80)
        self.setCursor(Qt.PointingHandCursor)
        
        colors = ["#667eea", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        self.avatar_color = avatar_color or colors[hash(name) % len(colors)]
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)
        
        avatar_label = QLabel(name[0].upper() if name else "?")
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setFixedSize(50, 50)
        avatar_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.avatar_color}, stop:1 {self.avatar_color}cc);
            border-radius: 25px;
        """)
        layout.addWidget(avatar_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 15px; font-weight: 600; color: white;")
        
        detail_label = QLabel(f"🕐 {time}  •  {session}")
        detail_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.5);")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(detail_label)
        layout.addLayout(info_layout, 1)
        
        status_badge = QLabel("✓ Present")
        status_badge.setStyleSheet("""
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            font-size: 11px;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 14px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        """)
        layout.addWidget(status_badge)
        
        btn_container = QHBoxLayout()
        btn_container.setSpacing(6)
        
        btn_edit = QPushButton("✏️")
        btn_edit.setObjectName("btn_icon_dark")
        btn_edit.setFixedSize(36, 36)
        btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.name))
        
        btn_del = QPushButton("🗑️")
        btn_del.setObjectName("btn_icon_dark")
        btn_del.setFixedSize(36, 36)
        btn_del.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.15);
                color: #ef4444;
                border-radius: 10px;
                border: 1px solid rgba(239, 68, 68, 0.2);
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.25);
            }
        """)
        btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.name))
        
        btn_container.addWidget(btn_edit)
        btn_container.addWidget(btn_del)
        layout.addLayout(btn_container)


class QuickActionButton(QPushButton):
    """Nút hành động nhanh với icon và label"""
    def __init__(self, icon, text, color="#667eea", parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 90)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 11px; font-weight: 600; color: white; background: transparent;")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }}
            QPushButton:hover {{
                background: {color}30;
                border-color: {color}50;
            }}
            QPushButton:pressed {{
                background: {color}40;
            }}
        """)


class SettingsDialog(QDialog):
    """Dialog cài đặt"""
    settings_changed = Signal(dict)
    
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings")
        self.setStyleSheet(MODERN_STYLE + """
            QDialog {
                background: #1a1a2e;
            }
        """)
        self.setMinimumSize(500, 600)
        self.settings = current_settings.copy()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("⚙️ Settings")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(header)
        
        tabs = QTabWidget()
        tabs.addTab(self.create_recognition_tab(), "🎯 Recognition")
        tabs.addTab(self.create_display_tab(), "🎨 Display")
        tabs.addTab(self.create_notification_tab(), "🔔 Notifications")
        layout.addWidget(tabs)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("btn_secondary")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("💾 Save Settings")
        btn_save.setObjectName("btn_primary")
        btn_save.clicked.connect(self.save_settings)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
    
    def create_recognition_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        tolerance_group = QFrame()
        tolerance_group.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px;")
        tg_layout = QVBoxLayout(tolerance_group)
        
        tg_header = QHBoxLayout()
        tg_label = QLabel("Recognition Tolerance")
        tg_label.setStyleSheet("font-size: 14px; font-weight: 600; color: white;")
        self.tolerance_value = QLabel(f"{self.settings.get('tolerance', 0.35)}")
        self.tolerance_value.setStyleSheet("font-size: 14px; color: #667eea;")
        tg_header.addWidget(tg_label)
        tg_header.addStretch()
        tg_header.addWidget(self.tolerance_value)
        tg_layout.addLayout(tg_header)
        
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(20, 60)
        self.tolerance_slider.setValue(int(self.settings.get('tolerance', 0.35) * 100))
        self.tolerance_slider.valueChanged.connect(lambda v: self.tolerance_value.setText(f"{v/100:.2f}"))
        tg_layout.addWidget(self.tolerance_slider)
        
        tg_desc = QLabel("Lower = stricter matching (less false positives)\nHigher = more lenient (may have false positives)")
        tg_desc.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.5);")
        tg_layout.addWidget(tg_desc)
        
        layout.addWidget(tolerance_group)
        
        confirm_group = QFrame()
        confirm_group.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px;")
        cg_layout = QVBoxLayout(confirm_group)
        
        cg_header = QHBoxLayout()
        cg_label = QLabel("Confirmation Frames")
        cg_label.setStyleSheet("font-size: 14px; font-weight: 600; color: white;")
        self.confirm_spin = QSpinBox()
        self.confirm_spin.setRange(1, 10)
        self.confirm_spin.setValue(self.settings.get('confirmation_count', 3))
        cg_header.addWidget(cg_label)
        cg_header.addStretch()
        cg_header.addWidget(self.confirm_spin)
        cg_layout.addLayout(cg_header)
        
        cg_desc = QLabel("Number of consecutive frames needed to confirm identity")
        cg_desc.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.5);")
        cg_layout.addWidget(cg_desc)
        
        layout.addWidget(confirm_group)
        layout.addStretch()
        
        return widget
    
    def create_display_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        self.show_fps = QCheckBox("Show FPS counter")
        self.show_fps.setChecked(self.settings.get('show_fps', False))
        layout.addWidget(self.show_fps)
        
        self.show_confidence = QCheckBox("Show confidence score")
        self.show_confidence.setChecked(self.settings.get('show_confidence', True))
        layout.addWidget(self.show_confidence)
        
        self.dark_mode = QCheckBox("Dark mode video overlay")
        self.dark_mode.setChecked(self.settings.get('dark_overlay', True))
        layout.addWidget(self.dark_mode)
        
        layout.addStretch()
        return widget
    
    def create_notification_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        self.sound_enabled = QCheckBox("Enable sound notifications")
        self.sound_enabled.setChecked(self.settings.get('sound_enabled', True))
        layout.addWidget(self.sound_enabled)
        
        self.toast_enabled = QCheckBox("Show toast notifications")
        self.toast_enabled.setChecked(self.settings.get('toast_enabled', True))
        layout.addWidget(self.toast_enabled)
        
        layout.addStretch()
        return widget
    
    def save_settings(self):
        self.settings = {
            'tolerance': self.tolerance_slider.value() / 100,
            'confirmation_count': self.confirm_spin.value(),
            'show_fps': self.show_fps.isChecked(),
            'show_confidence': self.show_confidence.isChecked(),
            'dark_overlay': self.dark_mode.isChecked(),
            'sound_enabled': self.sound_enabled.isChecked(),
            'toast_enabled': self.toast_enabled.isChecked(),
        }
        self.settings_changed.emit(self.settings)
        self.accept()


class ReportDialog(QDialog):
    """Dialog báo cáo thống kê"""
    def __init__(self, master_file, parent=None):
        super().__init__(parent)
        self.master_file = master_file
        self.setWindowTitle("📊 Attendance Report")
        self.setStyleSheet(MODERN_STYLE + """
            QDialog {
                background: #1a1a2e;
            }
        """)
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("📊 Attendance Analytics")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(header)
        
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("📅 From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.date_from)
        
        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.date_to)
        
        btn_filter = QPushButton("🔍 Apply Filter")
        btn_filter.setObjectName("btn_primary")
        btn_filter.clicked.connect(self.apply_filter)
        filter_layout.addWidget(btn_filter)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        stats_layout = QHBoxLayout()
        self.stat_cards = {}
        
        for icon, key, label, color in [
            ("📊", "total", "Total Records", "#667eea"),
            ("👥", "unique", "Unique People", "#10b981"),
            ("📈", "avg", "Avg per Day", "#f59e0b"),
            ("🏆", "best", "Best Day", "#8b5cf6"),
        ]:
            card = AnimatedStatCard(icon, 0, label, color)
            self.stat_cards[key] = card
            stats_layout.addWidget(card)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                gridline-color: rgba(255,255,255,0.1);
            }
            QTableWidget::item {
                color: white;
                padding: 10px;
            }
            QHeaderView::section {
                background: rgba(102, 126, 234, 0.3);
                color: white;
                font-weight: 600;
                padding: 12px;
                border: none;
            }
        """)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        
        btn_export_pdf = QPushButton("📄 Export PDF")
        btn_export_pdf.setObjectName("btn_warning")
        btn_export_pdf.clicked.connect(self.export_pdf)
        
        btn_export_excel = QPushButton("📊 Export Excel")
        btn_export_excel.setObjectName("btn_success")
        btn_export_excel.clicked.connect(self.export_excel)
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btn_secondary")
        btn_close.clicked.connect(self.close)
        
        btn_layout.addWidget(btn_export_pdf)
        btn_layout.addWidget(btn_export_excel)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
        
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.master_file):
                self.df = pd.read_csv(self.master_file)
                self.apply_filter()
            else:
                self.df = pd.DataFrame()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {e}")
    
    def apply_filter(self):
        if self.df.empty:
            return
            
        try:
            df = self.df.copy()
            df['Attendance Date'] = pd.to_datetime(df['Attendance Date'])
            
            date_from = self.date_from.date().toPython()
            date_to = self.date_to.date().toPython()
            
            mask = (df['Attendance Date'].dt.date >= date_from) & (df['Attendance Date'].dt.date <= date_to)
            filtered = df[mask]
            
            self.stat_cards['total'].update_value(len(filtered))
            self.stat_cards['unique'].update_value(filtered['Name'].nunique() if not filtered.empty else 0)
            
            if not filtered.empty:
                daily_counts = filtered.groupby(filtered['Attendance Date'].dt.date).size()
                self.stat_cards['avg'].update_value(f"{daily_counts.mean():.1f}")
                self.stat_cards['best'].update_value(daily_counts.max())
            
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(list(df.columns))
            self.table.setRowCount(len(filtered))
            
            for r, row in enumerate(filtered.itertuples(index=False)):
                for c, val in enumerate(row):
                    item = QTableWidgetItem(str(val))
                    item.setForeground(QColor("white"))
                    self.table.setItem(r, c, item)
            
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
        except Exception as e:
            print(f"Filter error: {e}")
    
    def export_pdf(self):
        QMessageBox.information(self, "Export PDF", 
            "PDF export requires additional libraries.\nPlease use Excel export instead.")
    
    def export_excel(self):
        if self.df.empty:
            QMessageBox.information(self, "No Data", "No data to export.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", 
            f"attendance_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel Files (*.xlsx)")
        
        if file_path:
            try:
                self.df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"Report exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")


class Worker(QThread):
    ImageUpdate = Signal(QImage, list)
    FaceDetected = Signal(int)
    FPSUpdate = Signal(float)

    def __init__(self, cv_logic):
        super().__init__()
        self.cv_logic = cv_logic
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        self.reload_data_flag = False
        self.fps_counter = 0
        self.fps_time = time.time()

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
            
            self.fps_counter += 1
            if time.time() - self.fps_time >= 1.0:
                self.FPSUpdate.emit(self.fps_counter)
                self.fps_counter = 0
                self.fps_time = time.time()
            
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
        
        self.settings = {
            'tolerance': 0.35,
            'confirmation_count': 3,
            'show_fps': True,
            'show_confidence': True,
            'dark_overlay': True,
            'sound_enabled': True,
            'toast_enabled': True,
        }
        self.load_settings()
        
        if not os.path.exists(self.master_file):
            pd.DataFrame(columns=["Name", "Check-in Datetime", "Attendance Date", "Session"]).to_csv(
                self.master_file, index=False, encoding="utf-8-sig")

        self.current_fps = 0
        self.init_ui()
        self.init_worker()
        self.start_clock()
        
    def load_settings(self):
        settings_file = os.path.join(os.getcwd(), "settings.json")
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    self.settings.update(json.load(f))
            except:
                pass
    
    def save_settings_to_file(self):
        settings_file = os.path.join(os.getcwd(), "settings.json")
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass

    def init_ui(self):
        central = QWidget()
        central.setObjectName("central_widget")
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ============== LEFT NAV ==============
        nav_frame = QFrame()
        nav_frame.setFixedWidth(70)
        nav_frame.setStyleSheet("background: rgba(0,0,0,0.3);")
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(10)
        
        logo = QLabel("🎯")
        logo.setStyleSheet("font-size: 32px; background: transparent;")
        logo.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(logo)
        nav_layout.addSpacing(30)
        
        nav_buttons = [
            ("🏠", "Home", self.show_home),
            ("📊", "Reports", self.show_reports),
            ("👥", "Members", self.show_members_dialog),
            ("⚙️", "Settings", self.show_settings),
        ]
        
        self.nav_btns = []
        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setObjectName("btn_icon_dark")
            btn.setFixedSize(50, 50)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.nav_btns.append(btn)
        
        nav_layout.addStretch()
        
        btn_quit = QPushButton("🚪")
        btn_quit.setObjectName("btn_icon_dark")
        btn_quit.setFixedSize(50, 50)
        btn_quit.setToolTip("Exit")
        btn_quit.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.2);
                color: #ef4444;
                border-radius: 12px;
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.3);
            }
        """)
        btn_quit.clicked.connect(self.close)
        nav_layout.addWidget(btn_quit, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(nav_frame)

        # ============== MAIN CONTENT ==============
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title = QLabel("Face Attendance")
        title.setObjectName("app_title")
        subtitle = QLabel("Real-time face recognition attendance system")
        subtitle.setObjectName("app_subtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header.addLayout(title_layout)
        
        header.addStretch()
        
        self.status_label = QLabel("● System Online")
        self.status_label.setObjectName("status_online")
        header.addWidget(self.status_label)
        
        header.addSpacing(20)
        
        clock_layout = QVBoxLayout()
        clock_layout.setAlignment(Qt.AlignRight)
        self.time_label = QLabel("00:00:00")
        self.time_label.setObjectName("time_label")
        self.date_label = QLabel("Loading...")
        self.date_label.setObjectName("date_label")
        clock_layout.addWidget(self.time_label)
        clock_layout.addWidget(self.date_label)
        header.addLayout(clock_layout)
        
        content_layout.addLayout(header)

        # Main Body
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        # Left - Video Section
        video_section = QVBoxLayout()
        video_section.setSpacing(16)
        
        video_container = QFrame()
        video_container.setObjectName("video_frame")
        video_inner = QVBoxLayout(video_container)
        video_inner.setContentsMargins(12, 12, 12, 12)
        
        self.video_label = QLabel()
        self.video_label.setObjectName("video_label")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(800, 500)
        video_inner.addWidget(self.video_label)
        
        video_info = QHBoxLayout()
        
        self.face_count_label = QLabel("👥 0 faces")
        self.face_count_label.setStyleSheet("""
            font-size: 13px; color: rgba(255,255,255,0.8);
            background: rgba(0,0,0,0.4); padding: 8px 16px;
            border-radius: 8px;
        """)
        video_info.addWidget(self.face_count_label)
        
        video_info.addStretch()
        
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet("""
            font-size: 13px; color: rgba(255,255,255,0.8);
            background: rgba(0,0,0,0.4); padding: 8px 16px;
            border-radius: 8px;
        """)
        video_info.addWidget(self.fps_label)
        
        video_inner.addLayout(video_info)
        video_section.addWidget(video_container, 1)

        # Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_total = AnimatedStatCard("👥", self.get_total_members(), "Members", "#667eea", "+2")
        self.stat_today = AnimatedStatCard("✅", len(self.attendance_list), "Today", "#10b981")
        self.stat_week = AnimatedStatCard("📊", self.get_week_attendance(), "This Week", "#f59e0b")
        self.stat_rate = AnimatedStatCard("📈", f"{self.get_attendance_rate()}%", "Rate", "#8b5cf6")
        
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_today)
        stats_layout.addWidget(self.stat_week)
        stats_layout.addWidget(self.stat_rate)
        stats_layout.addStretch()
        
        video_section.addLayout(stats_layout)
        body_layout.addLayout(video_section, 2)

        # Right - Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("left_panel_frame")
        sidebar.setFixedWidth(380)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(16)

        # Quick Actions
        actions_title = QLabel("⚡ Quick Actions")
        actions_title.setObjectName("section_title_dark")
        sidebar_layout.addWidget(actions_title)
        
        actions_grid = QGridLayout()
        actions_grid.setSpacing(12)
        
        btn_add = QuickActionButton("➕", "Add Person", "#667eea")
        btn_add.clicked.connect(self.add_new_person)
        
        btn_reset = QuickActionButton("🔄", "Reset", "#f59e0b")
        btn_reset.clicked.connect(self.reset_attendance)
        
        btn_export = QuickActionButton("📤", "Export", "#10b981")
        btn_export.clicked.connect(self.export_attendance_excel)
        
        btn_history = QuickActionButton("📋", "History", "#8b5cf6")
        btn_history.clicked.connect(self.open_master_list)
        
        actions_grid.addWidget(btn_add, 0, 0)
        actions_grid.addWidget(btn_reset, 0, 1)
        actions_grid.addWidget(btn_export, 0, 2)
        actions_grid.addWidget(btn_history, 0, 3)
        
        sidebar_layout.addLayout(actions_grid)

        # Search
        search_container = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_dark")
        self.search_input.setPlaceholderText("Search attendee...")
        self.search_input.textChanged.connect(self.filter_attendance)
        search_container.addWidget(self.search_input)
        sidebar_layout.addLayout(search_container)

        # Attendance List
        list_header = QHBoxLayout()
        list_title = QLabel("📋 Today's Attendance")
        list_title.setObjectName("section_title_dark")
        list_header.addWidget(list_title)
        list_header.addStretch()
        
        self.attendance_count = QLabel("0")
        self.attendance_count.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
            color: white; font-size: 13px; font-weight: bold;
            padding: 4px 12px; border-radius: 10px;
        """)
        list_header.addWidget(self.attendance_count)
        sidebar_layout.addLayout(list_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.attendance_widget = QWidget()
        self.attendance_layout = QVBoxLayout(self.attendance_widget)
        self.attendance_layout.setAlignment(Qt.AlignTop)
        self.attendance_layout.setSpacing(10)
        self.attendance_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self.attendance_widget)
        
        sidebar_layout.addWidget(scroll, 1)

        body_layout.addWidget(sidebar)
        content_layout.addLayout(body_layout, 1)
        
        main_layout.addLayout(content_layout, 1)

        # Success Overlay
        self.success_overlay = QLabel(self.video_label)
        self.success_overlay.setAlignment(Qt.AlignCenter)
        self.success_overlay.setStyleSheet("""
            font-size: 18px; font-weight: bold; color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(16, 185, 129, 0.95), stop:1 rgba(5, 150, 105, 0.95));
            padding: 16px 32px; border-radius: 16px;
            border: 2px solid rgba(255,255,255,0.2);
        """)
        self.success_overlay.setFixedSize(420, 70)
        self.success_overlay.hide()

    def init_worker(self):
        self.worker = Worker(self.cv_logic)
        self.worker.ImageUpdate.connect(self.update_frame)
        self.worker.FaceDetected.connect(self.update_face_count)
        self.worker.FPSUpdate.connect(self.update_fps)
        self.worker.start()

    def start_clock(self):
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
        self.date_label.setText(now.strftime("%A, %B %d, %Y"))

    @Slot(float)
    def update_fps(self, fps):
        self.current_fps = fps
        if self.settings.get('show_fps', True):
            self.fps_label.setText(f"FPS: {int(fps)}")
            self.fps_label.show()
        else:
            self.fps_label.hide()

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
            if status == "Confirming":
                color = (234, 126, 102)
                thickness = 2
            elif status == "Recognized":
                color = (129, 230, 217)
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
            elif status == "Checked-in":
                color = (94, 172, 86)
                thickness = 2
            else:
                color = (208, 135, 112)
                thickness = 2

            cv2.rectangle(frame_to_draw, (left, top), (right, bottom), color, thickness)
            
            corner_length = 20
            cv2.line(frame_to_draw, (left, top), (left + corner_length, top), color, 3)
            cv2.line(frame_to_draw, (left, top), (left, top + corner_length), color, 3)
            cv2.line(frame_to_draw, (right, top), (right - corner_length, top), color, 3)
            cv2.line(frame_to_draw, (right, top), (right, top + corner_length), color, 3)
            cv2.line(frame_to_draw, (left, bottom), (left + corner_length, bottom), color, 3)
            cv2.line(frame_to_draw, (left, bottom), (left, bottom - corner_length), color, 3)
            cv2.line(frame_to_draw, (right, bottom), (right - corner_length, bottom), color, 3)
            cv2.line(frame_to_draw, (right, bottom), (right, bottom - corner_length), color, 3)
            
            label_size = cv2.getTextSize(display_name, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            label_x = left
            label_y = top - 12
            
            overlay = frame_to_draw.copy()
            cv2.rectangle(overlay,
                         (label_x - 5, label_y - label_size[1] - 10),
                         (label_x + label_size[0] + 10, label_y + 5),
                         color, -1)
            cv2.addWeighted(overlay, 0.7, frame_to_draw, 0.3, 0, frame_to_draw)
            
            cv2.putText(frame_to_draw, display_name,
                       (label_x, label_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        h, w, ch = frame_to_draw.shape
        final_image = QImage(frame_to_draw.data, w, h, ch * w, QImage.Format_BGR888)
        
        pixmap = QPixmap.fromImage(final_image)
        self.video_label.setPixmap(pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def add_attendance_card(self, name, time, session, date=None):
        card = ModernAttendanceCard(name, time, session)
        card.edit_clicked.connect(self.edit_attendee)
        card.delete_clicked.connect(self.delete_attendee)
        card._att_datetime = time
        card._att_date = date
        self.attendance_layout.insertWidget(0, card)
        
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
        if not self.settings.get('toast_enabled', True):
            return
            
        self.success_overlay.setText(f"✅ {name} - Check-in successful!")
        
        vw = self.video_label.width()
        sw = self.success_overlay.width()
        x = (vw - sw) // 2
        self.success_overlay.move(max(0, x), 20)
        self.success_overlay.show()
        self.success_overlay.raise_()
        
        QTimer.singleShot(2500, self.success_overlay.hide)

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
        dlg.setWindowTitle("📋 Attendance History")
        dlg.setStyleSheet(MODERN_STYLE + "QDialog { background: #1a1a2e; }")
        dlg.resize(1000, 650)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(25, 25, 25, 25)
        
        header = QLabel("📋 Attendance History")
        header.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin-bottom: 16px;")
        layout.addWidget(header)
        
        table = QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                gridline-color: rgba(255,255,255,0.1);
            }
            QTableWidget::item { color: white; padding: 12px; }
            QHeaderView::section {
                background: rgba(102, 126, 234, 0.3);
                color: white; font-weight: 600; padding: 14px; border: none;
            }
        """)
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(list(df.columns))
        table.setRowCount(len(df))
        
        for r in range(len(df)):
            for c, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[r, c]))
                table.setItem(r, c, item)
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(table)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_delete = QPushButton("🗑️ Delete Selected")
        btn_delete.setObjectName("btn_danger")
        btn_delete.clicked.connect(lambda: self.delete_history_rows(table, dlg))
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btn_glass")
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
        dlg.setWindowTitle("👥 Members")
        dlg.setStyleSheet(MODERN_STYLE + "QDialog { background: #1a1a2e; }")
        dlg.resize(500, 650)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(25, 25, 25, 25)
        
        header = QLabel(f"👥 Members ({len(members)})")
        header.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)
        
        colors = ["#667eea", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        
        for idx, name in enumerate(members):
            color = colors[idx % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }}
                QFrame:hover {{
                    background: rgba(255, 255, 255, 0.08);
                    border-color: {color}80;
                }}
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            
            avatar = QLabel(name[0].upper())
            avatar.setAlignment(Qt.AlignCenter)
            avatar.setFixedSize(45, 45)
            avatar.setStyleSheet(f"""
                font-size: 18px; font-weight: 700; color: white;
                background: {color}; border-radius: 22px;
            """)
            card_layout.addWidget(avatar)
            
            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 15px; font-weight: 600; color: white;")
            card_layout.addWidget(name_label, 1)
            
            btn_delete = QPushButton("🗑️")
            btn_delete.setObjectName("btn_icon_dark")
            btn_delete.setFixedSize(38, 38)
            btn_delete.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 68, 68, 0.15);
                    color: #ef4444; border-radius: 10px;
                    border: 1px solid rgba(239, 68, 68, 0.2);
                }
                QPushButton:hover { background: rgba(239, 68, 68, 0.25); }
            """)
            btn_delete.clicked.connect(lambda _, n=name, c=card: self.delete_member(n, c, dlg))
            card_layout.addWidget(btn_delete)
            
            content_layout.addWidget(card)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btn_glass")
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

    def show_home(self):
        pass
    
    def show_reports(self):
        dlg = ReportDialog(self.master_file, self)
        dlg.exec()
    
    def show_settings(self):
        dlg = SettingsDialog(self.settings, self)
        dlg.settings_changed.connect(self.apply_settings)
        dlg.exec()
    
    def apply_settings(self, new_settings):
        self.settings = new_settings
        self.save_settings_to_file()
        
        if hasattr(self.cv_logic, 'TOLERANCE'):
            self.cv_logic.TOLERANCE = new_settings.get('tolerance', 0.35)
        if hasattr(self.cv_logic, 'CONFIRMATION_COUNT'):
            self.cv_logic.CONFIRMATION_COUNT = new_settings.get('confirmation_count', 3)

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
        self.save_settings_to_file()
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
