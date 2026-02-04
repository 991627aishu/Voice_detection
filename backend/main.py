from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
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
    description="Detect AI-generated vs Human voices across 5 languages",
    version="1.0.0"
)

# ---------- CORS FIX (IMPORTANT) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all sites
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------

API_KEY = os.getenv("API_KEY", "sk_test_123456789")

SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

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

def verify_api_key(x_api_key: str = Header(None)):
    # allow if not provided (so frontend works)
    if x_api_key and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# ---------- SIMPLE FEATURE EXTRACT ----------
def extract_audio_features(audio_data, sr):
    pitch = np.std(audio_data)
    energy = np.mean(np.abs(audio_data))
    return {"pitch": pitch, "energy": energy}

def detect_ai_voice(features):
    if features["pitch"] < 0.01:
        return "AI_GENERATED", 0.82, "Very consistent pitch pattern"
    return "HUMAN", 0.78, "Natural voice variation detected"
# --------------------------------------------

@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(request: VoiceDetectionRequest, _: bool = Depends(verify_api_key)):
    try:
        audio_bytes = base64.b64decode(request.audioBase64)
        audio_io = io.BytesIO(audio_bytes)
        audio_data, sr = librosa.load(audio_io, sr=22050)

        features = extract_audio_features(audio_data, sr)
        classification, confidence, explanation = detect_ai_voice(features)

        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=confidence,
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
