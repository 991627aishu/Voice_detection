// API Configuration
const DEFAULT_API_URL = 'https://voice-detection-backend.onrender.com/api/voice-detection';
let API_URL = DEFAULT_API_URL;

// DOM Elements
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

// Base64 Input Handler
base64Input.addEventListener('input', (e) => {
    currentBase64 = e.target.value.trim();
    base64Length.textContent = `${currentBase64.length} characters`;
    updateAnalyzeButton();
});

// Endpoint Handler
endpointInput.addEventListener('input', (e) => {
    API_URL = e.target.value.trim() || DEFAULT_API_URL;
    updateAnalyzeButton();
});

// Enable / Disable Button
function updateAnalyzeButton() {
    analyzeBtn.disabled = currentBase64.length < 20;
}

// Analyze Button
analyzeBtn.addEventListener('click', async () => {
    const endpoint = endpointInput.value.trim() || DEFAULT_API_URL;
    const apiKey = apiKeyInput.value.trim();
    const language = languageSelect.value;
    const audioFormat = audioFormatInput.value;

    if (!currentBase64 || currentBase64.length < 20) {
        showError('Paste valid Base64 audio');
        return;
    }

    try {
        loadingOverlay.style.display = 'flex';
        hideError();

        const base64Audio = currentBase64.replace(/^data:audio\/[^;]+;base64,/, '');

        const controller = new AbortController();
        setTimeout(() => controller.abort(), 60000); // 60 sec

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

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'API Failed');
        }

        displayResults(data);

    } catch (error) {
        console.error(error);
        showError('Server unreachable OR audio too large (>1MB)');
    } finally {
        loadingOverlay.style.display = 'none';
    }
});

// Display Results
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

    const confidence = Math.round(data.confidenceScore * 100);
    document.getElementById('confidenceValue').textContent = `${confidence}%`;
    document.getElementById('meterFill').style.width = `${confidence}%`;

    document.getElementById('resultLanguage').textContent = data.language;
    document.getElementById('resultStatus').textContent = data.status;
    document.getElementById('explanationText').textContent = data.explanation;

    resultsSection.style.display = 'block';
}

// Error
function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Init
updateAnalyzeButton();
console.log('Voice Detection Frontend Ready');
