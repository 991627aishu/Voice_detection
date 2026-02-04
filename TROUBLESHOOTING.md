# 🔧 Troubleshooting Guide

## Common Installation Issues

### Issue: pip install fails with dependency conflicts

**Solution 1: Use the step-by-step installer**
```bash
# Windows
install_dependencies.bat

# Linux/Mac
chmod +x install_dependencies.sh
./install_dependencies.sh
```

**Solution 2: Install packages individually**
```bash
pip install numpy
pip install scipy
pip install librosa
pip install fastapi uvicorn[standard]
pip install python-multipart pydantic
pip install python-jose[cryptography] passlib[bcrypt]
pip install python-dotenv aiofiles pydub scikit-learn
```

**Solution 3: Use virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Then install
pip install -r requirements.txt
```

### Issue: librosa installation fails

**Solution:**
```bash
# Windows - Install system dependencies first
# Download FFmpeg from https://ffmpeg.org/download.html
# Add to PATH

# Linux
sudo apt-get update
sudo apt-get install ffmpeg libsndfile1

# Mac
brew install ffmpeg libsndfile

# Then install librosa
pip install librosa
```

### Issue: numpy compilation errors

**Solution:**
```bash
# Use pre-built wheels
pip install --upgrade pip
pip install numpy --only-binary :all:

# Or install from conda
conda install numpy scipy librosa
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Or change port in start_backend.bat/sh
# Edit: uvicorn main:app --host 0.0.0.0 --port 8080
```

### Issue: Frontend can't connect to backend

**Solutions:**
1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Update API URL in frontend/script.js:**
   ```javascript
   const API_URL = 'http://localhost:8000/api/voice-detection';
   ```

3. **Check CORS settings** - Already configured in backend

4. **Check firewall** - Allow port 8000

### Issue: Audio processing fails

**Solutions:**
1. **Verify audio format:**
   - Must be MP3
   - Check file is not corrupted
   - Length: 0.5-60 seconds

2. **Install audio codecs:**
   ```bash
   # Linux
   sudo apt-get install ffmpeg libavcodec-extra

   # Mac
   brew install ffmpeg
   ```

3. **Check librosa installation:**
   ```bash
   python -c "import librosa; print(librosa.__version__)"
   ```

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Verify installation
python -c "import fastapi, librosa, numpy; print('OK')"

# If fails, reinstall:
pip install --force-reinstall -r requirements.txt
```

### Issue: Permission errors (Linux/Mac)

**Solution:**
```bash
# Don't use sudo with pip (can cause issues)
# Instead, use --user flag:
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Fixes

### Reset Everything
```bash
# Remove all packages
pip freeze > installed.txt
pip uninstall -r installed.txt -y

# Reinstall
pip install -r requirements.txt
```

### Verify Installation
```bash
python -c "
import fastapi
import uvicorn
import librosa
import numpy
import scipy
print('✅ All core packages installed successfully!')
"
```

### Test Backend
```bash
# Start backend
python backend/main.py

# In another terminal:
curl http://localhost:8000/health
```

## Still Having Issues?

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Update pip:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

3. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

4. **Try conda instead:**
   ```bash
   conda create -n voice-detection python=3.9
   conda activate voice-detection
   conda install numpy scipy librosa
   pip install fastapi uvicorn[standard] python-multipart pydantic
   ```

## Getting Help

If you're still stuck:
1. Check the error message carefully
2. Try the step-by-step installer: `install_dependencies.bat` or `install_dependencies.sh`
3. Use a virtual environment
4. Check Python version compatibility



