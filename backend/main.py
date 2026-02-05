from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import numpy as np
import librosa
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Voice Detection API",
    description="Detect AI-generated vs Human voices",
    version="2.0.0"
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "sk_test_123456789")

SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# ---------- MODELS ----------
class VoiceDetectionRequest(BaseModel):
    language: str
    audioFormat: str = "mp3"
    audioBase64: str

class VoiceDetectionResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

# ---------- API KEY ----------
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# ---------- FEATURE EXTRACTION ----------
def extract_audio_features(audio_data, sr):
    pitch_std = np.std(audio_data)
    energy = np.mean(np.abs(audio_data))
    zero_cross = np.mean(librosa.feature.zero_crossing_rate(audio_data))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))

    return {
        "pitch_std": pitch_std,
        "energy": energy,
        "zero_cross": zero_cross,
        "centroid": spectral_centroid
    }

# ---------- SMART DETECTION ----------
def detect_ai_voice(features):
    pitch = features["pitch_std"]
    energy = features["energy"]
    zcr = features["zero_cross"]
    centroid = features["centroid"]

    ai_score = 0
    human_score = 0

    # Pitch Stability
    if pitch < 0.02:
        ai_score += 2
    else:
        human_score += 2

    # Energy Uniformity
    if energy > 0.015 and energy < 0.05:
        ai_score += 1
    else:
        human_score += 1

    # Zero Crossing
    if zcr < 0.05:
        ai_score += 1
    else:
        human_score += 1

    # Spectral centroid
    if centroid < 2000:
        ai_score += 1
    else:
        human_score += 1

    if ai_score > human_score:
        confidence = min(0.85 + (ai_score * 0.02), 0.95)
        return "AI_GENERATED", confidence, "Voice shows stable pitch and synthetic patterns"

    confidence = min(0.80 + (human_score * 0.02), 0.95)
    return "HUMAN", confidence, "Voice contains natural variations"

# ---------- ROUTES ----------
@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(request: VoiceDetectionRequest, _: bool = Depends(verify_api_key)):
    try:
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")

        audio_bytes = base64.b64decode(request.audioBase64)
        audio_io = io.BytesIO(audio_bytes)

        audio_data, sr = librosa.load(audio_io, sr=22050, mono=True)

        features = extract_audio_features(audio_data, sr)
        classification, confidence, explanation = detect_ai_voice(features)

        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Processing error")

@app.get("/")
def root():
    return {"status": "success", "message": "API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
