@echo off
setlocal EnableDelayedExpansion

title Face Attendance System

echo.
echo ================================================================
echo       FACE RECOGNITION ATTENDANCE SYSTEM
echo ================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "VENV_PY=%SCRIPT_DIR%venv\Scripts\python.exe"
set "EMBED_PY=%SCRIPT_DIR%windows_deps\python\python.exe"
set "PY_PATH_FILE=%SCRIPT_DIR%.python_path"

:: Find Python
set "PYTHON_EXE="

:: Try saved path first
if exist "%PY_PATH_FILE%" (
    set /p PYTHON_EXE=<"%PY_PATH_FILE%"
    if exist "!PYTHON_EXE!" (
        goto :run_app
    )
)

:: Try venv
if exist "%VENV_PY%" (
    set "PYTHON_EXE=%VENV_PY%"
    goto :run_app
)

:: Try embedded
if exist "%EMBED_PY%" (
    set "PYTHON_EXE=%EMBED_PY%"
    goto :run_app
)

echo     [LOI] Khong tim thay Python!
echo     Vui long chay setup.bat truoc.
echo.
pause
exit /b 1

:run_app
cd /d "%SCRIPT_DIR%"

if not exist "app_main.py" (
    echo     [LOI] Khong tim thay app_main.py!
    pause
    exit /b 1
)

:: Create directories if needed
if not exist "known_faces" mkdir "known_faces"
if not exist "attendance_records" mkdir "attendance_records"

echo     Dang khoi dong ung dung...
echo     (Nhan Ctrl+C hoac dong cua so de thoat)
echo.
echo ================================================================
echo.

"%PYTHON_EXE%" app_main.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo   [LOI] Ung dung da thoat voi loi!
    echo ================================================================
    echo.
    echo   Thu chay lai setup.bat neu gap van de.
    echo.
    pause
    exit /b 1
)

echo.
echo Ung dung da dong.
pause
exit /b 0
