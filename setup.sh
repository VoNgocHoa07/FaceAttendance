#!/bin/bash
# ==============================================
# SETUP SCRIPT - Face Recognition Attendance
# Tuong thich: macOS, Linux (Ubuntu/Debian/Fedora/Arch)
# Chay: bash setup.sh
# ==============================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

print_header() {
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[X] $1${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_success "Detected: macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
            print_success "Detected: Linux ($DISTRO)"
        else
            DISTRO="unknown"
            print_warning "Unknown Linux distribution"
        fi
    else
        print_error "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    print_header "Installing System Dependencies"
    
    if [[ "$OS" == "macos" ]]; then
        if ! command -v brew &> /dev/null; then
            print_warning "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        print_success "Homebrew is installed"
        
        brew install cmake python@3.10 2>/dev/null || true
        print_success "Dependencies installed"
        
    elif [[ "$OS" == "linux" ]]; then
        case "$DISTRO" in
            ubuntu|debian|linuxmint|pop)
                print_success "Using apt package manager"
                sudo apt-get update
                sudo apt-get install -y \
                    build-essential cmake \
                    python3 python3-pip python3-venv \
                    libx11-dev libxcb1 libxcb-xinerama0 libxcb-cursor0 \
                    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
                    libxkbcommon-x11-0 libgl1-mesa-glx libglib2.0-0 \
                    libopenblas-dev liblapack-dev \
                    v4l-utils libegl1 libxkbcommon0
                ;;
            fedora|centos|rhel)
                print_success "Using dnf package manager"
                sudo dnf install -y \
                    gcc gcc-c++ cmake \
                    python3 python3-pip python3-devel \
                    libX11-devel libxcb libxkbcommon-x11 \
                    mesa-libGL openblas-devel lapack-devel
                ;;
            arch|manjaro)
                print_success "Using pacman package manager"
                sudo pacman -Syu --noconfirm \
                    base-devel cmake \
                    python python-pip \
                    libx11 libxcb libxkbcommon-x11 \
                    mesa openblas lapack
                ;;
            *)
                print_warning "Unknown distribution. Please install: cmake, python3, python3-pip, python3-venv"
                ;;
        esac
        print_success "System dependencies installed"
    fi
}

# Setup Python virtual environment
setup_venv() {
    print_header "Setting up Python Environment"
    
    # Find Python 3.10+
    PYTHON_CMD=""
    for py in python3.10 python3.11 python3.12 python3; do
        if command -v $py &> /dev/null; then
            version=$($py --version 2>&1 | sed 's/Python //' | cut -d. -f1,2)
            major=$(echo $version | cut -d. -f1)
            minor=$(echo $version | cut -d. -f2)
            if [[ "$major" -eq 3 && "$minor" -ge 10 ]]; then
                PYTHON_CMD=$py
                print_success "Found Python: $($py --version)"
                break
            fi
        fi
    done
    
    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.10+ not found!"
        print_warning "Please install Python 3.10 or later"
        exit 1
    fi
    
    # Create venv if not exists
    if [ ! -d "$VENV_DIR" ]; then
        print_success "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate venv
    source "$VENV_DIR/bin/activate"
    print_success "Virtual environment activated"
}

# Install Python packages
install_packages() {
    print_header "Installing Python Packages"
    
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    print_success "Upgrading pip..."
    pip install --upgrade pip wheel setuptools -q
    
    # Install numpy first
    print_success "Installing numpy..."
    pip install "numpy>=1.24.0,<2.0.0" -q
    
    # Install dlib
    print_success "Installing dlib (may take a few minutes)..."
    pip install dlib -q
    
    # Install face_recognition
    print_success "Installing face_recognition..."
    pip install face_recognition -q
    
    # Install other packages
    print_success "Installing opencv-python..."
    pip install "opencv-python<4.10" -q
    
    print_success "Installing PySide6..."
    pip install PySide6 -q
    
    print_success "Installing pandas, openpyxl..."
    pip install pandas openpyxl -q
    
    print_success "Installing mediapipe..."
    pip install mediapipe -q
    
    print_success "All packages installed!"
}

# Create directories
create_directories() {
    print_header "Creating Directories"
    
    mkdir -p "$SCRIPT_DIR/known_faces"
    mkdir -p "$SCRIPT_DIR/attendance_records"
    
    print_success "Created: known_faces/"
    print_success "Created: attendance_records/"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"
    
    source "$VENV_DIR/bin/activate"
    
    python -c "import cv2; import face_recognition; import PySide6; import pandas; print('OK')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "All packages verified!"
    else
        print_error "Some packages failed to import"
        exit 1
    fi
}

# Main
main() {
    print_header "Face Recognition Attendance - Setup"
    
    cd "$SCRIPT_DIR"
    
    detect_os
    install_system_deps
    setup_venv
    install_packages
    create_directories
    verify_installation
    
    print_header "Setup Complete!"
    echo ""
    echo -e "${GREEN}To run the application:${NC}"
    echo ""
    echo -e "  ${YELLOW}bash start.sh${NC}"
    echo ""
}

main "$@"
