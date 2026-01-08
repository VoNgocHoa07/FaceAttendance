@echo off
setlocal EnableDelayedExpansion

title Face Attendance - Setup

echo.
echo ================================================================
echo     FACE RECOGNITION ATTENDANCE SYSTEM - WINDOWS SETUP
echo ================================================================
echo.
echo   Dang cai dat... Vui long cho doi.
echo.
echo ================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"
set "DEPS_DIR=%SCRIPT_DIR%windows_deps"
set "PYTHON_EMBED=%DEPS_DIR%\python"
set "WHEELS_DIR=%DEPS_DIR%\wheels"
set "DLIB_WHEEL=%WHEELS_DIR%\dlib-19.24.99-cp310-cp310-win_amd64.whl"

:: ============================================================
:: CHECK BUNDLED DEPENDENCIES
:: ============================================================
echo [1/5] Kiem tra dependencies da dinh kem...
echo.

if not exist "%PYTHON_EMBED%\python.exe" (
    echo     [LOI] Khong tim thay Python trong windows_deps\python
    echo     Du an co the bi thieu file. Vui long tai lai du an.
    pause
    exit /b 1
)
echo     [OK] Python Embeddable 3.10

if not exist "%DLIB_WHEEL%" (
    echo     [LOI] Khong tim thay dlib wheel trong windows_deps\wheels
    echo     Du an co the bi thieu file. Vui long tai lai du an.
    pause
    exit /b 1
)
echo     [OK] dlib wheel
echo.

:: ============================================================
:: SETUP PYTHON EMBEDDABLE
:: ============================================================
echo [2/5] Cau hinh Python Embeddable...
echo.

:: Enable pip in embedded Python - modify python310._pth
set "PTH_FILE=%PYTHON_EMBED%\python310._pth"
if exist "%PTH_FILE%" (
    findstr /c:"import site" "%PTH_FILE%" >nul 2>&1
    if errorlevel 1 (
        echo import site>> "%PTH_FILE%"
        echo     [OK] Da kich hoat site-packages
    ) else (
        echo     [OK] site-packages da duoc kich hoat
    )
)

:: Download get-pip.py if not exists (nho, chi ~2.5MB)
set "GET_PIP=%PYTHON_EMBED%\get-pip.py"
if not exist "%GET_PIP%" (
    echo     Dang tai get-pip.py (2.5MB)...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%GET_PIP%'}" 2>nul
    if not exist "%GET_PIP%" (
        echo     [LOI] Khong the tai get-pip.py
        echo     Kiem tra ket noi internet va thu lai.
        pause
        exit /b 1
    )
)

:: Install pip
if not exist "%PYTHON_EMBED%\Scripts\pip.exe" (
    echo     Dang cai dat pip...
    "%PYTHON_EMBED%\python.exe" "%GET_PIP%" --no-warn-script-location >nul 2>&1
    if errorlevel 1 (
        echo     [LOI] Khong the cai dat pip
        pause
        exit /b 1
    )
)
echo     [OK] pip da san sang
echo.

:: ============================================================
:: SETUP ENVIRONMENT
:: ============================================================
echo [3/5] Thiet lap moi truong...
echo.

:: Use embedded python directly (simpler, more reliable)
set "PY=%PYTHON_EMBED%\python.exe"
set "PIP=%PYTHON_EMBED%\Scripts\pip.exe"
echo     [OK] Su dung Python Embeddable truc tiep
echo.

:: ============================================================
:: INSTALL DEPENDENCIES
:: ============================================================
echo [4/5] Cai dat thu vien (can internet)...
echo.

:: Upgrade pip
echo     Nang cap pip...
"%PY%" -m pip install --upgrade pip --quiet 2>nul
echo     [OK] pip

:: Install wheel and setuptools
echo     Cai dat build tools...
"%PIP%" install --upgrade wheel setuptools --quiet 2>nul
echo     [OK] build tools

:: Install numpy first (required for dlib/face_recognition)
echo     Cai dat numpy...
"%PIP%" install "numpy>=1.24.0,<2.0.0" --quiet 2>nul
echo     [OK] numpy

:: Install dlib from LOCAL wheel (no download needed!)
echo     Cai dat dlib tu file dinh kem...
"%PIP%" install "%DLIB_WHEEL%" --quiet 2>nul
if errorlevel 1 (
    echo     [LOI] Khong the cai dat dlib
    pause
    exit /b 1
)
echo     [OK] dlib

:: Install face_recognition
echo     Cai dat face_recognition...
"%PIP%" install face_recognition --quiet 2>nul
echo     [OK] face_recognition

:: Install other packages
echo     Cai dat opencv-python...
"%PIP%" install "opencv-python<4.10" --quiet 2>nul
echo     [OK] opencv-python

echo     Cai dat PySide6...
"%PIP%" install PySide6 --quiet 2>nul
echo     [OK] PySide6

echo     Cai dat pandas, openpyxl...
"%PIP%" install pandas openpyxl --quiet 2>nul
echo     [OK] pandas, openpyxl

echo     Cai dat mediapipe...
"%PIP%" install mediapipe --quiet 2>nul
echo     [OK] mediapipe

echo.

:: ============================================================
:: VERIFY AND FINISH
:: ============================================================
echo [5/5] Kiem tra cai dat...
echo.

"%PY%" -c "import cv2; import face_recognition; import PySide6; import pandas; import mediapipe; print('OK')" 2>nul
if errorlevel 1 (
    echo     [LOI] Mot so thu vien chua duoc cai dat dung!
    echo     Thu chay lai setup.bat
    pause
    exit /b 1
)
echo     [OK] Tat ca thu vien da san sang

:: Create directories
if not exist "%SCRIPT_DIR%known_faces" mkdir "%SCRIPT_DIR%known_faces"
if not exist "%SCRIPT_DIR%attendance_records" mkdir "%SCRIPT_DIR%attendance_records"
echo     [OK] Thu muc da tao

:: Save python path for start.bat
echo %PY%> "%SCRIPT_DIR%.python_path"

echo.
echo ================================================================
echo            CAI DAT HOAN TAT THANH CONG!
echo ================================================================
echo.
echo   Chay "start.bat" de khoi dong ung dung.
echo.
echo ================================================================
echo.
pause
exit /b 0
