@echo off
echo ========================================
echo AI Voice Detection - Dependency Installer
echo ========================================
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing core dependencies first...
pip install numpy scipy

echo.
echo Step 3: Installing audio processing libraries...
pip install librosa soundfile

echo.
echo Step 4: Installing web framework...
pip install fastapi uvicorn[standard] python-multipart

echo.
echo Step 5: Installing remaining dependencies...
pip install pydantic python-jose[cryptography] passlib[bcrypt] python-dotenv aiofiles pydub scikit-learn

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To verify installation, run:
echo   python -c "import fastapi, librosa, numpy; print('All packages installed successfully!')"
echo.
pause




