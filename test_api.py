"""
Test script for AI Voice Detection API
"""
import requests
import base64
import json
import sys

API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "sk_test_123456789"

def encode_audio_file(file_path):
    """Encode audio file to Base64"""
    try:
        with open(file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            return base64_audio
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error encoding file: {str(e)}")
        return None

def test_voice_detection(audio_path, language="English"):
    """Test the voice detection API"""
    print(f"\n{'='*60}")
    print("Testing Voice Detection API")
    print(f"{'='*60}")
    print(f"Audio file: {audio_path}")
    print(f"Language: {language}")
    
    # Encode audio
    print("\nEncoding audio file...")
    base64_audio = encode_audio_file(audio_path)
    if not base64_audio:
        return False
    
    # Prepare request
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": base64_audio
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    # Make request
    print("Sending request to API...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print("\nFull JSON Response:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print("\n❌ Error!")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("Make sure the backend server is running on http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ Request Timeout!")
        print("The request took too long to complete")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print("⚠️ Backend server responded with error")
            return False
    except:
        print("❌ Backend server is not running")
        return False

if __name__ == "__main__":
    print("AI Voice Detection API - Test Script")
    print("=" * 60)
    
    # Check if server is running
    if not test_health_check():
        print("\nPlease start the backend server first:")
        print("  Windows: start_backend.bat")
        print("  Linux/Mac: ./start_backend.sh")
        sys.exit(1)
    
    # Test with provided audio file
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 else "English"
        test_voice_detection(audio_file, language)
    else:
        print("\nUsage:")
        print("  python test_api.py <audio_file.mp3> [language]")
        print("\nExample:")
        print("  python test_api.py sample.mp3 English")
        print("  python test_api.py sample.mp3 Tamil")
        print("\nSupported languages: Tamil, English, Hindi, Malayalam, Telugu")
