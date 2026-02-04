# AI-Generated Voice Detection System

A sophisticated multi-language voice detection system that identifies whether a voice sample is AI-generated or human-spoken across five supported languages: Tamil, English, Hindi, Malayalam, and Telugu.

## 🌟 Features

- **Multi-Language Support**: Detects voices in Tamil, English, Hindi, Malayalam, and Telugu
- **Advanced Audio Analysis**: Uses spectral analysis, MFCC features, pitch detection, and more
- **Beautiful Modern UI**: Intuitive, responsive interface with real-time audio visualization
- **Secure API**: Protected with API key authentication
- **High Accuracy**: Confidence scores with detailed explanations
- **Real-time Processing**: Fast analysis with visual feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (optional, for serving frontend)

### Installation

1. **Clone the repository**
```bash
cd Buildthon
```

2. **Install Python dependencies**

**Option A: Quick Install (Recommended)**
```bash
# Windows
install_dependencies.bat

# Linux/Mac
chmod +x install_dependencies.sh
./install_dependencies.sh
```

**Option B: Standard Install**
```bash
pip install -r requirements.txt
```

**Option C: If you encounter errors, try step-by-step:**
```bash
pip install numpy scipy
pip install librosa soundfile
pip install fastapi uvicorn[standard] python-multipart
pip install pydantic python-jose[cryptography] passlib[bcrypt]
pip install python-dotenv aiofiles pydub scikit-learn
```

**Verify Installation:**
```bash
python verify_installation.py
```

3. **Set up environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env and set your API_KEY
```

4. **Start the backend server**
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

5. **Open the frontend**
- Simply open `frontend/index.html` in your web browser
- Or serve it using a local server:
```bash
cd frontend
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

## 📡 API Usage

### Endpoint
```
POST /api/voice-detection
```

### Headers
```
Content-Type: application/json
x-api-key: sk_test_123456789
```

### Request Body
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO_STRING"
}
```

### Response
```json
{
  "status": "success",
  "language": "English",
  "classification": "HUMAN",
  "confidenceScore": 0.87,
  "explanation": "Natural human speech patterns with expected variations"
}
```

### cURL Example
```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "YOUR_BASE64_AUDIO"
  }'
```

## 🎯 How It Works

The system analyzes audio using multiple features:

1. **Pitch Analysis**: Detects pitch consistency (AI voices are often more uniform)
2. **Spectral Features**: Analyzes frequency distribution patterns
3. **MFCC (Mel-Frequency Cepstral Coefficients)**: Captures timbral characteristics
4. **Zero Crossing Rate**: Measures signal variations
5. **Energy Analysis**: Examines amplitude patterns
6. **Spectral Rolloff**: Analyzes frequency distribution

These features are combined using heuristic rules to determine if the voice is AI-generated or human.

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Librosa**: Audio analysis library
- **NumPy & SciPy**: Scientific computing
- **Scikit-learn**: Machine learning utilities

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5 & CSS3**: Modern web standards
- **Web Audio API**: Real-time audio visualization

## 📁 Project Structure

```
Buildthon/
├── backend/
│   ├── main.py              # FastAPI application
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Styling
│   └── script.js            # Frontend logic
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔒 Security

- API key authentication required for all requests
- Input validation and sanitization
- Error handling to prevent information leakage
- CORS configured for frontend access

## 🎨 UI Features

- **Drag & Drop Upload**: Easy file selection
- **Audio Preview**: Listen to uploaded audio
- **Real-time Waveform**: Visual audio representation
- **Confidence Meter**: Animated progress bar
- **Detailed Results**: Classification with explanations
- **Responsive Design**: Works on all devices

## 📊 Supported Languages

1. **Tamil** (தமிழ்)
2. **English**
3. **Hindi** (हिंदी)
4. **Malayalam** (മലയാളം)
5. **Telugu** (తెలుగు)

## 🐛 Troubleshooting

### Audio Loading Issues
- Ensure audio is in MP3 format
- Check that Base64 encoding is correct
- Verify audio length is between 0.5-60 seconds

### API Errors
- Verify API key is correct
- Check that language is one of the supported languages
- Ensure audio file is not corrupted

### Frontend Issues
- Clear browser cache
- Check browser console for errors
- Ensure backend is running on port 8000

## 📝 License

This project is built for the Buildthon hackathon.

## 🙏 Acknowledgments

Built with ❤️ for the AI Voice Detection challenge.

