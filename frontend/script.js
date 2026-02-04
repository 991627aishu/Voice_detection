// API Configuration
let API_URL = 'http://localhost:8000/api/voice-detection';

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

// Base64 Input Handler
base64Input.addEventListener('input', (e) => {
    currentBase64 = e.target.value.trim();
    base64Length.textContent = `${currentBase64.length} characters`;
    updateAnalyzeButton();
});

// Endpoint URL Handler
endpointInput.addEventListener('input', (e) => {
    API_URL = e.target.value.trim() || 'http://localhost:8000/api/voice-detection';
    updateAnalyzeButton();
});

// API Key Input Handler
apiKeyInput.addEventListener('input', () => {
    updateAnalyzeButton();
});

// Update Analyze Button State
function updateAnalyzeButton() {
    analyzeBtn.disabled = !currentBase64 || !apiKeyInput.value.trim() || !endpointInput.value.trim();
}

// Analyze Button Click
analyzeBtn.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();
    if (!apiKey) {
        showError('Please enter an API key');
        return;
    }
    
    if (!currentBase64) {
        showError('Please paste Base64-encoded audio');
        return;
    }
    
    const endpoint = endpointInput.value.trim();
    if (!endpoint) {
        showError('Please enter an endpoint URL');
        return;
    }
    
    const language = languageSelect.value;
    const audioFormat = audioFormatInput.value;
    
    try {
        loadingOverlay.style.display = 'flex';
        hideError();
        
        // Clean Base64 string (remove data URL prefix if present)
        const base64Audio = currentBase64.replace(/^data:audio\/[^;]+;base64,/, '');
        
        // Make API request
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': apiKey
            },
            body: JSON.stringify({
                language: language,
                audioFormat: audioFormat,
                audioBase64: base64Audio
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || data.detail || 'API request failed');
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to analyze audio. Please try again.');
    } finally {
        loadingOverlay.style.display = 'none';
    }
});

// Display Results
function displayResults(data) {
    if (data.status !== 'success') {
        showError(data.message || 'Analysis failed');
        return;
    }
    
    // Update classification badge
    const classificationBadge = document.getElementById('classificationBadge');
    const classificationText = document.getElementById('classificationText');
    
    classificationBadge.className = 'classification-badge ' + 
        (data.classification === 'AI_GENERATED' ? 'ai-generated' : 'human');
    classificationText.textContent = data.classification === 'AI_GENERATED' 
        ? '🤖 AI Generated' 
        : '👤 Human Voice';
    
    // Update confidence score
    const confidenceValue = document.getElementById('confidenceValue');
    const meterFill = document.getElementById('meterFill');
    const confidence = Math.round(data.confidenceScore * 100);
    
    confidenceValue.textContent = `${confidence}%`;
    meterFill.style.width = `${confidence}%`;
    
    // Update details
    document.getElementById('resultLanguage').textContent = data.language;
    document.getElementById('resultStatus').textContent = data.status;
    document.getElementById('explanationText').textContent = data.explanation;
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show Error
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.animation = 'shake 0.5s ease-out';
    }, 10);
}

// Hide Error
function hideError() {
    errorMessage.style.display = 'none';
}

// Initialize
updateAnalyzeButton();
console.log('AI Voice Detection System initialized');
