from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
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
    version="3.0.0"
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
    return True


# ---------- FEATURE EXTRACTION ----------
def extract_audio_features(audio_data, sr):
    rms = np.mean(librosa.feature.rms(y=audio_data))
    zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
    centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
    bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio_data, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr))
    pitch_std = np.std(audio_data)

    return {
        "rms": rms,
        "zcr": zcr,
        "centroid": centroid,
        "bandwidth": bandwidth,
        "rolloff": rolloff,
        "pitch_std": pitch_std
    }


# ---------- SMART DETECTION ----------
def detect_ai_voice(features):
    ai_score = 0
    human_score = 0

    # Pitch stability
    if features["pitch_std"] < 0.015:
        ai_score += 2
    else:
        human_score += 2

    # RMS energy
    if 0.01 < features["rms"] < 0.04:
        ai_score += 1
    else:
        human_score += 1

    # ZCR
    if features["zcr"] < 0.06:
        ai_score += 1
    else:
        human_score += 1

    # Spectral centroid
    if features["centroid"] < 2500:
        ai_score += 1
    else:
        human_score += 1

    # Bandwidth
    if features["bandwidth"] < 3000:
        ai_score += 1
    else:
        human_score += 1

    # Rolloff
    if features["rolloff"] < 4000:
        ai_score += 1
    else:
        human_score += 1

    total = ai_score + human_score
    confidence = max(ai_score, human_score) / total

    if ai_score > human_score:
        return "AI_GENERATED", round(confidence, 2), "Synthetic stability and spectral smoothness detected"

    return "HUMAN", round(confidence, 2), "Natural pitch variation and dynamic frequency detected"


# ---------- ROUTES ----------
@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(request: VoiceDetectionRequest, _: bool = Depends(verify_api_key)):
    try:
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")

        audio_bytes = base64.b64decode(request.audioBase64)
        audio_io = io.BytesIO(audio_bytes)

        audio_data, sr = librosa.load(audio_io, sr=22050, mono=True)

        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio")

        features = extract_audio_features(audio_data, sr)
        classification, confidence, explanation = detect_ai_voice(features)

        return JSONResponse(
            content={
                "status": "success",
                "language": request.language,
                "classification": classification,
                "confidenceScore": confidence,
                "explanation": explanation
            }
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
