@echo off
REM =========================================================
REM VOICE CLONING & LIP-SYNC SETUP & RUN SCRIPT (WINDOWS)
REM =========================================================
REM This script automates:
REM 1. Environment setup
REM 2. Dependency installation
REM 3. Configuration
REM 4. Web application launch
REM =========================================================

setlocal enabledelayedexpansion

cls
echo =========================================================
echo.
echo   🎙️  VOICE CLONING ^& LIP-SYNC SETUP ^& RUN (Windows)
echo.
echo =========================================================
echo.

REM =========================================================
REM Step 1: Check Python version
REM =========================================================
echo [Step 1/6] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM =========================================================
REM Step 2: Create virtual environment
REM =========================================================
echo [Step 2/6] Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM =========================================================
REM Step 3: Install dependencies
REM =========================================================
echo [Step 3/6] Installing dependencies...
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

echo Installing project dependencies (this may take 2-5 minutes)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM =========================================================
REM Step 4: Create necessary directories
REM =========================================================
echo [Step 4/6] Creating necessary directories...
if not exist "weights" mkdir weights
if not exist "outputs" mkdir outputs
if not exist "temp" mkdir temp
if not exist "assets\sample" mkdir assets\sample
if not exist "logs" mkdir logs
echo ✓ Directories created
echo.

REM =========================================================
REM Step 5: Check for Wav2Lip weights
REM =========================================================
echo [Step 5/6] Checking Wav2Lip weights...
if not exist "weights\wav2lip_gan.pth" (
    echo.
    echo ⚠️  WARNING: Wav2Lip weights not found!
    echo.
    echo Please download wav2lip_gan.pth from:
    echo https://github.com/Rudrabha/Wav2Lip
    echo.
    echo And place it in: weights\wav2lip_gan.pth
    echo.
    echo The application will still start, but lip-sync will fail until weights are added.
    echo.
) else (
    echo ✓ Wav2Lip weights found
    echo.
)

REM =========================================================
REM Step 6: Check for ffmpeg
REM =========================================================
echo [Step 6/6] Checking ffmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: ffmpeg not found!
    echo.
    echo Please install ffmpeg:
    echo Option 1: Download from https://ffmpeg.org/download.html
    echo Option 2: Use Chocolatey: choco install ffmpeg
    echo.
    pause
    exit /b 1
)
echo ✓ ffmpeg found
echo.

REM =========================================================
REM Select and Launch App
REM =========================================================
echo =========================================================
echo ✓ Setup Complete!
echo =========================================================
echo.
echo Choose which interface to launch:
echo.
echo   1) Streamlit UI (Simpler, recommended for beginners)
echo   2) Gradio UI (More flexible, easy to deploy to Hugging Face)
echo   3) Exit setup without launching
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Launching Streamlit app...
    echo.
    echo The app will open in your browser at http://localhost:8501
    echo.
    streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo Launching Gradio app...
    echo.
    echo The app will open in your browser at http://localhost:7860
    echo.
    python gradio_app.py
) else if "%choice%"=="3" (
    echo.
    echo Setup complete. You can manually launch:
    echo.
    echo   Streamlit:  streamlit run app.py
    echo   Gradio:     python gradio_app.py
    echo.
) else (
    echo Invalid choice. Exiting.
)

pause
endlocal