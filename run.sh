#!/bin/bash
# Chạy Face Recognition với Jetson Orin
set -e

IMAGE_NAME="vongochoa/chamilohull"
TAG="latest"
CONTAINER_NAME="chamilohull"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  $IMAGE_NAME:$TAG"
echo "============================================"

# Kiểm tra image
if ! docker image inspect $IMAGE_NAME:$TAG > /dev/null 2>&1; then
    echo "Image chưa có, đang build..."
    docker build -t $IMAGE_NAME:$TAG "$SCRIPT_DIR"
fi

# Tạo thư mục data
mkdir -p "$SCRIPT_DIR/known_faces"
mkdir -p "$SCRIPT_DIR/attendance_records"

# Cho phép X11
export DISPLAY=${DISPLAY:-:0}
xhost +local:docker 2>/dev/null || xhost + 2>/dev/null || true

# Dừng container cũ
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Tìm camera
CAMERA_DEVICE="/dev/video0"
if [ ! -e "$CAMERA_DEVICE" ]; then
    echo "Camera /dev/video0 không tìm thấy."
    ls /dev/video* 2>/dev/null || echo "Không có camera"
    read -p "Nhập device camera: " CAMERA_DEVICE
fi

echo "Camera: $CAMERA_DEVICE"
echo "============================================"

docker run -it --rm \
    --name $CONTAINER_NAME \
    --network host \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -e QT_QPA_PLATFORM=xcb \
    -e XDG_RUNTIME_DIR=/tmp/runtime-root \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "$SCRIPT_DIR/known_faces":/app/known_faces \
    -v "$SCRIPT_DIR/attendance_records":/app/attendance_records \
    --device "$CAMERA_DEVICE":/dev/video0 \
    $IMAGE_NAME:$TAG
