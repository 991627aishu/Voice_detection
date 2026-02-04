// API Configuration
let API_URL = 'https://voice-detection-3qdu.onrender.com/api/voice-detection';

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

// Set default endpoint
endpointInput.value = API_URL;

// Base64 Input Handler
base64Input.addEventListener('input', (e) => {
    currentBase64 = e.target.value.trim();
    base64Length.textContent = `${currentBase64.length} characters`;
    updateAnalyzeButton();
});

// Endpoint URL Handler
endpointInput.addEventListener('input', (e) => {
    API_URL = e.target.value.trim() || API_URL;
    updateAnalyzeButton();
});

// Update Analyze Button State
function updateAnalyzeButton() {
    analyzeBtn.disabled = !currentBase64 || !endpointInput.value.trim();
}

// Analyze Button Click
analyzeBtn.addEventListener('click', async () => {
    const endpoint = endpointInput.value.trim() || API_URL;
    const apiKey = apiKeyInput.value.trim(); // optional
    const language = languageSelect.value;
    const audioFormat = audioFormatInput.value;

    if (!currentBase64) {
        showError('Please paste Base64 audio');
        return;
    }

    try {
        loadingOverlay.style.display = 'flex';
        hideError();

        const base64Audio = currentBase64.replace(/^data:audio\/[^;]+;base64,/, '');

        // Timeout controller
        const controller = new AbortController();
        setTimeout(() => controller.abort(), 30000);

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
            throw new Error(data.detail || 'API failed');
        }

        displayResults(data);

    } catch (error) {
        console.error(error);
        showError('Server unreachable or audio too large');
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

// Show Error
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

// Hide Error
function hideError() {
    errorMessage.style.display = 'none';
}

// Initialize
updateAnalyzeButton();
console.log('AI Voice Detection System Ready');
