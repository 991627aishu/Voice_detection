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
    version="8.0.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "sk_test_123456789")

SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# ---------------- MODELS ----------------
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


# ---------------- API KEY ----------------
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


# ---------------- FEATURE EXTRACTION ----------------
def extract_audio_features(audio_data, sr):
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=20)

    features = {
        "rms": float(np.mean(librosa.feature.rms(y=audio_data))),
        "zcr": float(np.mean(librosa.feature.zero_crossing_rate(audio_data))),
        "centroid": float(np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))),
        "bandwidth": float(np.mean(librosa.feature.spectral_bandwidth(y=audio_data, sr=sr))),
        "rolloff": float(np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr))),
        "mfcc_std": float(np.std(mfcc)),
        "mfcc_mean": float(np.mean(mfcc)),
    }

    return features


# ---------------- AI / HUMAN DETECTION ----------------
def detect_ai_voice(f):
    ai_score = 0
    human_score = 0

    # MFCC Smoothness
    if f["mfcc_std"] < 22:
        ai_score += 2
    else:
        human_score += 2

    # RMS Energy
    if 0.01 < f["rms"] < 0.05:
        ai_score += 1
    else:
        human_score += 1

    # Zero Crossing Rate
    if f["zcr"] < 0.08:
        ai_score += 1
    else:
        human_score += 1

    # Spectral Centroid
    if f["centroid"] < 2800:
        ai_score += 1
    else:
        human_score += 1

    # Bandwidth
    if f["bandwidth"] < 3500:
        ai_score += 1
    else:
        human_score += 1

    # Rolloff
    if f["rolloff"] < 5000:
        ai_score += 1
    else:
        human_score += 1

    total = ai_score + human_score
    confidence = round(max(ai_score, human_score) / total, 2)

    # IMPORTANT BALANCE LOGIC
    if ai_score > human_score + 1:
        return (
            "AI_GENERATED",
            confidence,
            "Smooth spectral patterns and low pitch variation detected"
        )

    return (
        "HUMAN",
        confidence,
        "Natural pitch variation and dynamic speech characteristics detected"
    )


# ---------------- ROUTES ----------------
@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(request: VoiceDetectionRequest, _: bool = Depends(verify_api_key)):
    try:
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")

        clean_base64 = request.audioBase64.split(",")[-1]

        try:
            audio_bytes = base64.b64decode(clean_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Base64")

        audio_io = io.BytesIO(audio_bytes)
        audio_data, sr = librosa.load(audio_io, sr=22050, mono=True)

        if len(audio_data) < 2000:
            raise HTTPException(status_code=400, detail="Audio too short")

        features = extract_audio_features(audio_data, sr)
        classification, confidence, explanation = detect_ai_voice(features)

        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=confidence,
            explanation=explanation
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Processing error")


@app.get("/")
def root():
    return {"status": "success", "message": "API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
