// ================= API CONFIG =================
const DEFAULT_API_URL = 'https://voice-detection-backend.onrender.com/api/voice-detection';
let API_URL = DEFAULT_API_URL;

// ================= DOM ELEMENTS =================
const languageSelect = document.getElementById('languageSelect');
const audioFormatInput = document.getElementById('audioFormatInput');
const apiKeyInput = document.getElementById('apiKeyInput');
const endpointInput = document.getElementById('endpointInput');
const base64Input = document.getElementById('base64Input');
const base64Length = document.getElementById('base64Length');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorMessage = document.getElementById('errorMessage');

let currentBase64 = '';

// Default endpoint
endpointInput.value = DEFAULT_API_URL;

// ================= BASE64 INPUT =================
base64Input.addEventListener('input', (e) => {
    currentBase64 = e.target.value.trim();
    base64Length.textContent = `${currentBase64.length} characters`;
    updateAnalyzeButton();
});

// ================= ENDPOINT INPUT =================
endpointInput.addEventListener('input', (e) => {
    API_URL = e.target.value.trim() || DEFAULT_API_URL;
    updateAnalyzeButton();
});

// ================= BUTTON ENABLE =================
function updateAnalyzeButton() {
    analyzeBtn.disabled = currentBase64.length < 50; // minimum length
}

// ================= ANALYZE CLICK =================
analyzeBtn.addEventListener('click', async () => {
    const endpoint = endpointInput.value.trim() || DEFAULT_API_URL;
    const apiKey = apiKeyInput.value.trim();
    const language = languageSelect.value;
    const audioFormat = audioFormatInput.value;

    if (!currentBase64 || currentBase64.length < 50) {
        showError('Paste valid Base64 audio (too short)');
        return;
    }

    try {
        loadingOverlay.style.display = 'flex';
        hideError();
        resultsSection.style.display = 'none';

        // Remove data prefix if exists
        const base64Audio = currentBase64.replace(/^data:audio\/[^;]+;base64,/, '');

        // Size check (~1MB base64 ≈ 750KB file)
        if (base64Audio.length > 1400000) {
            showError('Audio too large. Use <10 sec MP3');
            loadingOverlay.style.display = 'none';
            return;
        }

        // ===== TIMEOUT FIX (Render Cold Start) =====
        const controller = new AbortController();
        setTimeout(() => controller.abort(), 120000); // 2 minutes

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(apiKey && { 'x-api-key': apiKey })
            },
            body: JSON.stringify({
                language,
                audioFormat,
                audioBase64: base64Audio
            }),
            signal: controller.signal
        });

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error('Invalid server response');
        }

        if (!response.ok) {
            throw new Error(data.detail || 'API Failed');
        }

        displayResults(data);

    } catch (error) {
        console.error(error);

        if (error.name === 'AbortError') {
            showError('Backend waking up... wait 1 minute and retry');
        } else {
            showError('Server unreachable or audio too large');
        }
    } finally {
        loadingOverlay.style.display = 'none';
    }
});

// ================= DISPLAY RESULTS =================
function displayResults(data) {
    const classificationBadge = document.getElementById('classificationBadge');
    const classificationText = document.getElementById('classificationText');

    classificationBadge.className =
        'classification-badge ' +
        (data.classification === 'AI_GENERATED' ? 'ai-generated' : 'human');

    classificationText.textContent =
        data.classification === 'AI_GENERATED'
            ? '🤖 AI Generated'
            : '👤 Human Voice';

    const confidence = Math.round((data.confidenceScore || 0) * 100);
    document.getElementById('confidenceValue').textContent = `${confidence}%`;
    document.getElementById('meterFill').style.width = `${confidence}%`;

    document.getElementById('resultLanguage').textContent = data.language || '-';
    document.getElementById('resultStatus').textContent = data.status || '-';
    document.getElementById('explanationText').textContent = data.explanation || '-';

    resultsSection.style.display = 'block';
}

// ================= ERROR =================
function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// ================= INIT =================
updateAnalyzeButton();
console.log('Voice Detection Frontend Ready');
