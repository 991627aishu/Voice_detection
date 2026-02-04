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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Voice Detection API",
    description="Detect AI-generated vs Human voices across 5 languages",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key (in production, use environment variable)
API_KEY = os.getenv("API_KEY", "sk_test_123456789")

# Supported languages
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class VoiceDetectionRequest(BaseModel):
    language: str = Field(..., description="Language: Tamil, English, Hindi, Malayalam, or Telugu")
    audioFormat: str = Field(default="mp3", description="Audio format (always mp3)")
    audioBase64: str = Field(..., description="Base64-encoded MP3 audio")

class VoiceDetectionResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str
    message: str

def verify_api_key(x_api_key: str = Header(...)) -> bool:
    """Verify API key from header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

def extract_audio_features(audio_data: np.ndarray, sr: int) -> dict:
    """Extract features from audio for AI detection"""
    features = {}
    
    # Fundamental frequency (pitch) - improved extraction
    try:
        # Use pyin for more accurate pitch tracking
        f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, 
                                                      fmin=librosa.note_to_hz('C2'),
                                                      fmax=librosa.note_to_hz('C7'))
        pitch_values = f0[~np.isnan(f0)]
        
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
            features['pitch_voiced_ratio'] = np.sum(~np.isnan(f0)) / len(f0)
        else:
            # Fallback to piptrack if pyin fails
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                features['pitch_mean'] = np.mean(pitch_values)
                features['pitch_std'] = np.std(pitch_values)
                features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
                features['pitch_voiced_ratio'] = len(pitch_values) / pitches.shape[1]
            else:
                features['pitch_mean'] = 0
                features['pitch_std'] = 0
                features['pitch_range'] = 0
                features['pitch_voiced_ratio'] = 0
    except Exception as e:
        logger.warning(f"Pitch extraction failed: {str(e)}, using fallback")
        # Fallback
        pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if pitch_values:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
            features['pitch_voiced_ratio'] = len(pitch_values) / pitches.shape[1]
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_range'] = 0
            features['pitch_voiced_ratio'] = 0
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroids)
    features['spectral_centroid_std'] = np.std(spectral_centroids)
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_std'] = np.std(zcr)
    
    # MFCC features
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
    features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
    features['mfcc_std'] = np.std(mfccs, axis=1).tolist()
    
    # Chroma features (using chroma_stft in librosa 0.11+)
    try:
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        features['chroma_mean'] = np.mean(chroma, axis=1).tolist()
    except Exception as e:
        # If chroma extraction fails, use a default value
        logger.warning(f"Chroma extraction failed: {str(e)}")
        features['chroma_mean'] = [0.0] * 12
    
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
    features['tempo'] = tempo
    
    # Energy
    rms = librosa.feature.rms(y=audio_data)[0]
    features['energy_mean'] = np.mean(rms)
    features['energy_std'] = np.std(rms)
    
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
    features['rolloff_mean'] = np.mean(rolloff)
    features['rolloff_std'] = np.std(rolloff)
    
    # Spectral bandwidth (AI voices might have narrower bandwidth)
    bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)[0]
    features['bandwidth_mean'] = np.mean(bandwidth)
    features['bandwidth_std'] = np.std(bandwidth)
    
    # Spectral contrast (harmonic content analysis)
    contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sr)
    features['contrast_mean'] = np.mean(contrast)
    features['contrast_std'] = np.std(contrast)
    
    # Tonnetz (harmonic network features)
    try:
        tonnetz = librosa.feature.tonnetz(y=audio_data, sr=sr)
        features['tonnetz_mean'] = np.mean(tonnetz)
        features['tonnetz_std'] = np.std(tonnetz)
    except:
        features['tonnetz_mean'] = 0
        features['tonnetz_std'] = 0
    
    # Poly features (polynomial approximation of spectral envelope)
    poly_features = librosa.feature.poly_features(y=audio_data, sr=sr)
    features['poly_mean'] = np.mean(poly_features)
    features['poly_std'] = np.std(poly_features)
    
    return features

def detect_ai_voice(features: dict, language: str) -> tuple[str, float, str]:
    """
    Detect if voice is AI-generated based on audio features
    Uses improved heuristic rules with better thresholds
    """
    ai_score = 0.0
    reasons = []
    
    # Get feature values with defaults
    pitch_std = features.get('pitch_std', 0)
    pitch_range = features.get('pitch_range', 0)
    spectral_centroid_std = features.get('spectral_centroid_std', 0)
    mfcc_std_mean = np.mean(features.get('mfcc_std', [0]))
    zcr_std = features.get('zcr_std', 0)
    energy_std = features.get('energy_std', 0)
    rolloff_std = features.get('rolloff_std', 0)
    bandwidth_std = features.get('bandwidth_std', 0)
    contrast_std = features.get('contrast_std', 0)
    poly_std = features.get('poly_std', 0)
    
    # Feature 1: Pitch consistency (MOST IMPORTANT - AI voices are very consistent)
    # Human voices typically have pitch std > 20-40 Hz, AI voices < 15 Hz
    if pitch_std > 0:
        if pitch_std < 5:
            ai_score += 0.30
            reasons.append("Extremely consistent pitch patterns")
        elif pitch_std < 12:
            ai_score += 0.25
            reasons.append("Unusually consistent pitch patterns")
        elif pitch_std < 20:
            ai_score += 0.15
            reasons.append("Consistent pitch patterns")
        elif pitch_std > 50:
            ai_score -= 0.20  # Strong human indicator
            reasons.append("Natural pitch variation")
        elif pitch_std > 35:
            ai_score -= 0.10
    
    # Feature 2: Pitch range (AI voices have limited range)
    if pitch_range > 0:
        if pitch_range < 30:
            ai_score += 0.20
            reasons.append("Very limited pitch range")
        elif pitch_range < 60:
            ai_score += 0.15
            reasons.append("Limited pitch variation")
        elif pitch_range > 200:
            ai_score -= 0.15
            reasons.append("Wide natural pitch range")
        elif pitch_range > 150:
            ai_score -= 0.10
    
    # Feature 3: Spectral centroid uniformity (AI voices are more uniform)
    if spectral_centroid_std > 0:
        if spectral_centroid_std < 250:
            ai_score += 0.15
            reasons.append("Uniform spectral characteristics")
        elif spectral_centroid_std < 500:
            ai_score += 0.10
        elif spectral_centroid_std > 1200:
            ai_score -= 0.10
    
    # Feature 4: MFCC smoothness (AI voices have smoother transitions)
    if mfcc_std_mean > 0:
        if mfcc_std_mean < 25:
            ai_score += 0.15
            reasons.append("Smooth MFCC transitions typical of synthesis")
        elif mfcc_std_mean < 50:
            ai_score += 0.10
        elif mfcc_std_mean > 120:
            ai_score -= 0.10
            reasons.append("Natural MFCC variations")
    
    # Feature 5: Zero crossing rate consistency
    if zcr_std > 0:
        if zcr_std < 0.003:
            ai_score += 0.10
            reasons.append("Consistent zero-crossing patterns")
        elif zcr_std < 0.008:
            ai_score += 0.05
        elif zcr_std > 0.04:
            ai_score -= 0.05
    
    # Feature 6: Energy consistency
    if energy_std > 0:
        if energy_std < 0.003:
            ai_score += 0.10
            reasons.append("Uniform energy distribution")
        elif energy_std < 0.008:
            ai_score += 0.05
        elif energy_std > 0.04:
            ai_score -= 0.05
    
    # Feature 7: Spectral rolloff consistency
    if rolloff_std > 0:
        if rolloff_std < 250:
            ai_score += 0.08
            reasons.append("Consistent spectral rolloff")
        elif rolloff_std > 1000:
            ai_score -= 0.05
    
    # Feature 8: Spectral bandwidth
    if bandwidth_std > 0:
        if bandwidth_std < 150:
            ai_score += 0.08
            reasons.append("Narrow spectral bandwidth")
        elif bandwidth_std > 600:
            ai_score -= 0.05
    
    # Feature 9: Spectral contrast
    if contrast_std > 0:
        if contrast_std < 4:
            ai_score += 0.05
        elif contrast_std > 18:
            ai_score -= 0.05
    
    # Feature 10: Poly features (spectral envelope)
    if poly_std > 0:
        if poly_std < 0.08:
            ai_score += 0.05
            reasons.append("Smooth spectral envelope")
        elif poly_std > 0.35:
            ai_score -= 0.05
    
    # Normalize score to 0-1 range
    ai_score = max(0.0, min(1.0, ai_score))
    
    # Classification with improved threshold
    # Lower threshold (0.35) to catch more AI voices
    if ai_score >= 0.35:
        classification = "AI_GENERATED"
        # Confidence calculation
        if ai_score >= 0.65:
            confidence = 0.75 + (ai_score - 0.65) * 0.57  # 0.75-0.95
        elif ai_score >= 0.50:
            confidence = 0.65 + (ai_score - 0.50) * 0.67  # 0.65-0.75
        else:
            confidence = 0.55 + (ai_score - 0.35) * 0.67  # 0.55-0.65
        confidence = min(0.95, max(0.55, confidence))
        
        if not reasons:
            explanation = "Synthetic voice patterns detected through audio analysis"
        else:
            explanation = " | ".join(reasons[:3])
    else:
        classification = "HUMAN"
        # Confidence for human classification
        human_score = 1.0 - ai_score
        if human_score >= 0.75:
            confidence = 0.80 + (human_score - 0.75) * 0.60  # 0.80-0.95
        elif human_score >= 0.60:
            confidence = 0.70 + (human_score - 0.60) * 0.67  # 0.70-0.80
        else:
            confidence = 0.60 + (human_score - 0.50) * 0.67  # 0.60-0.70
        confidence = min(0.95, max(0.60, confidence))
        explanation = "Natural human speech patterns with expected variations"
    
    logger.info(f"Detection: {classification} | AI Score: {ai_score:.3f} | Confidence: {confidence:.2f} | Pitch std: {pitch_std:.2f} | Pitch range: {pitch_range:.2f}")
    
    return classification, round(confidence, 2), explanation

@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(
    request: VoiceDetectionRequest,
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Main endpoint for voice detection
    """
    try:
        # Validate language
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Must be one of: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        
        # Validate audio format
        if request.audioFormat.lower() != "mp3":
            raise HTTPException(
                status_code=400,
                detail="Only MP3 format is supported"
            )
        
        # Decode Base64 audio
        try:
            audio_bytes = base64.b64decode(request.audioBase64)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Base64 encoding: {str(e)}"
            )
        
        # Load audio using librosa
        try:
            audio_io = io.BytesIO(audio_bytes)
            audio_data, sr = librosa.load(audio_io, sr=22050)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to load audio file: {str(e)}"
            )
        
        # Validate audio length
        if len(audio_data) < sr * 0.5:  # At least 0.5 seconds
            raise HTTPException(
                status_code=400,
                detail="Audio too short. Minimum 0.5 seconds required"
            )
        
        if len(audio_data) > sr * 60:  # Max 60 seconds
            raise HTTPException(
                status_code=400,
                detail="Audio too long. Maximum 60 seconds allowed"
            )
        
        # Extract features
        features = extract_audio_features(audio_data, sr)
        
        # Detect AI voice
        classification, confidence, explanation = detect_ai_voice(features, request.language)
        
        logger.info(f"Detection result: {classification} (confidence: {confidence:.2f}) for {request.language}")
        
        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "success",
        "message": "AI Voice Detection API is running",
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

