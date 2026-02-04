# 🚀 Quick Start Guide

Get your AI Voice Detection System up and running in minutes!

## Step 1: Install Dependencies

### Option A: Step-by-Step Installer (Recommended if you encounter errors)
```bash
# Windows
install_dependencies.bat

# Linux/Mac
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Option B: Standard Install
```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

### Verify Installation
```bash
python verify_installation.py
```

## Step 2: Set Up Environment

1. Copy the environment file:
   ```bash
   cd backend
   copy env.example .env  # Windows
   cp env.example .env    # Linux/Mac
   ```

2. Edit `.env` and set your API key (or use the default)

## Step 3: Start the Backend

### Windows
```bash
start_backend.bat
```

### Linux/Mac
```bash
chmod +x start_backend.sh
./start_backend.sh
```

The API will start at `http://localhost:8000`

## Step 4: Open the Frontend

Simply open `frontend/index.html` in your web browser!

Or use a local server:
```bash
cd frontend
python -m http.server 8080
```
Then visit `http://localhost:8080`

## Step 5: Test It!

1. Upload an MP3 audio file
2. Select the language
3. Enter API key (default: `sk_test_123456789`)
4. Click "Analyze Voice"
5. View the results!

## 🧪 Test with Python Script

```bash
python test_api.py your_audio_file.mp3 English
```

## ✅ Verify Installation

Check if the API is running:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

## 🐳 Using Docker

```bash
docker build -t voice-detection-api .
docker run -p 8000:8000 -e API_KEY=your_key voice-detection-api
```

## 📝 Notes

- Audio files should be MP3 format
- Minimum audio length: 0.5 seconds
- Maximum audio length: 60 seconds
- Supported languages: Tamil, English, Hindi, Malayalam, Telugu

## 🆘 Troubleshooting

**Backend won't start?**
- Check if port 8000 is available
- Verify Python 3.8+ is installed
- Ensure all dependencies are installed

**Frontend can't connect?**
- Make sure backend is running
- Check browser console for errors
- Verify API URL in script.js

**Audio processing fails?**
- Ensure audio is valid MP3 format
- Check file size (not too large)
- Verify librosa is properly installed

## 🎉 You're Ready!

Your AI Voice Detection System is now running. Start detecting AI-generated voices!

