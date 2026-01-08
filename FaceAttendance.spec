# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Face Recognition Attendance System
Builds standalone executable for Windows, macOS, and Linux
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all necessary data files
datas = []
datas += collect_data_files('mediapipe')

# Hidden imports for face_recognition and dlib
hiddenimports = [
    'face_recognition',
    'face_recognition_models',
    'dlib',
    'cv2',
    'numpy',
    'pandas',
    'openpyxl',
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'mediapipe',
    'mediapipe.python',
    'mediapipe.python.solutions',
]
hiddenimports += collect_submodules('mediapipe')

a = Analysis(
    ['app_main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'PyQt5',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Platform-specific settings
if sys.platform == 'darwin':
    # macOS - create .app bundle
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='FaceAttendance',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='FaceAttendance',
    )
    app = BUNDLE(
        coll,
        name='FaceAttendance.app',
        icon=None,
        bundle_identifier='com.faceattendance.app',
        info_plist={
            'CFBundleName': 'FaceAttendance',
            'CFBundleDisplayName': 'Face Attendance',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSCameraUsageDescription': 'This app requires camera access for face recognition.',
            'NSHighResolutionCapable': True,
        },
    )
elif sys.platform == 'win32':
    # Windows - create single .exe
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='FaceAttendance',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,
    )
else:
    # Linux - create executable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='FaceAttendance',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
