# Dockerfile for Face Recognition Attendance System
# For Linux x86_64 connecting to Jetson Orin
# Image name: vongochoa/chamilohull:latest

FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV QT_QPA_PLATFORM=xcb
ENV DISPLAY=:0
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV PYTHONUNBUFFERED=1

# Install system dependencies (minimal for GUI and camera)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libx11-dev \
    libxcb1 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxkbcommon-x11-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libdbus-1-3 \
    libegl1 \
    libxkbcommon0 \
    libxcb-util1 \
    libxcb-glx0 \
    libopenblas-dev \
    liblapack-dev \
    v4l-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.1.4 \
    opencv-python-headless==4.9.0.80 \
    PySide6==6.6.1 \
    mediapipe==0.10.9 \
    dlib==19.24.2 \
    face_recognition==1.3.0 \
    openpyxl==3.1.2

# Copy application code
COPY app_main.py cv_logic.py auto_capture.py ./
COPY Logo/ ./Logo/

RUN mkdir -p /app/known_faces /app/attendance_records /tmp/runtime-root \
    && chmod 700 /tmp/runtime-root

CMD ["python3", "app_main.py"]
