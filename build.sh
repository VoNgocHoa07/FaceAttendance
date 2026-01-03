#!/bin/bash
# Build Docker Image: vongochoa/chamilohull:latest
set -e

IMAGE_NAME="vongochoa/chamilohull"
TAG="latest"

echo "============================================"
echo "  BUILD: $IMAGE_NAME:$TAG"
echo "============================================"

docker build -t $IMAGE_NAME:$TAG .

echo ""
echo "Build hoàn tất!"
echo "Chạy: ./run.sh"
echo "Push: docker login && docker push $IMAGE_NAME:$TAG"
