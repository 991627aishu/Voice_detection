#!/bin/bash

echo "========================================"
echo "AI Voice Detection - Dependency Installer"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python3 --version

echo ""
echo "Step 1: Upgrading pip..."
python3 -m pip install --upgrade pip

echo ""
echo "Step 2: Installing core dependencies first..."
pip3 install numpy scipy

echo ""
echo "Step 3: Installing audio processing libraries..."
pip3 install librosa soundfile

echo ""
echo "Step 4: Installing web framework..."
pip3 install fastapi uvicorn[standard] python-multipart

echo ""
echo "Step 5: Installing remaining dependencies..."
pip3 install pydantic python-jose[cryptography] passlib[bcrypt] python-dotenv aiofiles pydub scikit-learn

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "To verify installation, run:"
echo "  python3 -c \"import fastapi, librosa, numpy; print('All packages installed successfully!')\""
echo ""




