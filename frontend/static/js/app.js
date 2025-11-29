/**
 * Main Application Logic
 */

// DOM Elements
const optimizeBtn = document.getElementById('optimizeBtn');
const inputPrompt = document.getElementById('inputPrompt');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const errorDisplay = document.getElementById('errorDisplay');
const copyFinalBtn = document.getElementById('copyFinalBtn');

// Config elements
const backendSelect = document.getElementById('backend');
const geminiKeyInput = document.getElementById('geminiKey');
const xaiKeyInput = document.getElementById('xaiKey');
const maxIterationsInput = document.getElementById('maxIterations');
const convergenceThresholdInput = document.getElementById('convergenceThreshold');
const forceOptimizationCheckbox = document.getElementById('forceOptimization');
const clearKeysBtn = document.getElementById('clearKeysBtn');
const themeToggle = document.getElementById('themeToggle');

// State
let currentResult = null;

// LocalStorage keys
const STORAGE_KEYS = {
    GEMINI_KEY: 'promptopt_gemini_key',
    XAI_KEY: 'promptopt_xai_key',
    THEME: 'promptopt_theme',
    BACKEND: 'promptopt_backend',
    MAX_ITERATIONS: 'promptopt_max_iterations',
    CONVERGENCE: 'promptopt_convergence',
};

/**
 * Load saved settings from localStorage
 */
function loadSavedSettings() {
    // Load API keys
    const savedGeminiKey = localStorage.getItem(STORAGE_KEYS.GEMINI_KEY);
    const savedXaiKey = localStorage.getItem(STORAGE_KEYS.XAI_KEY);
    
    if (savedGeminiKey) {
        geminiKeyInput.value = savedGeminiKey;
    }
    if (savedXaiKey) {
        xaiKeyInput.value = savedXaiKey;
    }
    
    // Load other settings
    const savedBackend = localStorage.getItem(STORAGE_KEYS.BACKEND);
    if (savedBackend) {
        backendSelect.value = savedBackend;
    }
    
    const savedMaxIterations = localStorage.getItem(STORAGE_KEYS.MAX_ITERATIONS);
    if (savedMaxIterations) {
        maxIterationsInput.value = savedMaxIterations;
    }
    
    const savedConvergence = localStorage.getItem(STORAGE_KEYS.CONVERGENCE);
    if (savedConvergence) {
        convergenceThresholdInput.value = savedConvergence;
    }
    
    // Load theme
    const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME) || 'dark';
    setTheme(savedTheme);
    themeToggle.checked = savedTheme === 'light';
}

/**
 * Save API keys to localStorage
 */
function saveApiKeys() {
    if (geminiKeyInput.value) {
        localStorage.setItem(STORAGE_KEYS.GEMINI_KEY, geminiKeyInput.value);
    }
    if (xaiKeyInput.value) {
        localStorage.setItem(STORAGE_KEYS.XAI_KEY, xaiKeyInput.value);
    }
}

/**
 * Save settings to localStorage
 */
function saveSettings() {
    localStorage.setItem(STORAGE_KEYS.BACKEND, backendSelect.value);
    localStorage.setItem(STORAGE_KEYS.MAX_ITERATIONS, maxIterationsInput.value);
    localStorage.setItem(STORAGE_KEYS.CONVERGENCE, convergenceThresholdInput.value);
}

/**
 * Clear saved API keys
 */
function clearApiKeys() {
    if (confirm('Are you sure you want to clear all saved API keys?')) {
        localStorage.removeItem(STORAGE_KEYS.GEMINI_KEY);
        localStorage.removeItem(STORAGE_KEYS.XAI_KEY);
        geminiKeyInput.value = '';
        xaiKeyInput.value = '';
        showSuccess('API keys cleared from browser storage');
    }
}

/**
 * Set theme
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEYS.THEME, theme);
}

/**
 * Toggle theme
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

/**
 * Initialize application
 */
async function init() {
    console.log('Initializing Prompt Optimizer...');
    
    // Load saved settings
    loadSavedSettings();
    
    // Check API health
    try {
        const health = await apiClient.healthCheck();
        console.log('API Health:', health);
    } catch (error) {
        showError('Failed to connect to backend. Make sure the API server is running at http://localhost:8001');
    }
    
    // Event listeners
    optimizeBtn.addEventListener('click', handleOptimize);
    copyFinalBtn.addEventListener('click', handleCopyFinal);
    clearKeysBtn.addEventListener('click', clearApiKeys);
    themeToggle.addEventListener('change', toggleTheme);
    
    // Save settings on change
    geminiKeyInput.addEventListener('blur', saveApiKeys);
    xaiKeyInput.addEventListener('blur', saveApiKeys);
    backendSelect.addEventListener('change', saveSettings);
    maxIterationsInput.addEventListener('change', saveSettings);
    convergenceThresholdInput.addEventListener('change', saveSettings);
}

/**
 * Handle optimize button click with real-time streaming
 */
async function handleOptimize() {
    const prompt = inputPrompt.value.trim();
    
    if (!prompt) {
        showError('Please enter a prompt to optimize');
        return;
    }
    
    // Get configuration
    const config = {
        prompt: prompt,
        backend: backendSelect.value,
        gemini_api_key: geminiKeyInput.value || null,
        xai_api_key: xaiKeyInput.value || null,
        max_iterations: parseInt(maxIterationsInput.value),
        convergence_threshold: parseFloat(convergenceThresholdInput.value),
        force_optimization: forceOptimizationCheckbox.checked
    };
    
    // Validate API keys
    if (config.backend === 'gemini' && !config.gemini_api_key) {
        showError('Please enter your Gemini API key');
        return;
    }
    if (config.backend === 'grok' && !config.xai_api_key) {
        showError('Please enter your xAI API key');
        return;
    }
    
    // Save API keys
    saveApiKeys();
    
    // Show loading and progress
    showLoading(true);
    showRealtimeProgress(true);
    hideError();
    hideResults();
    
    // Reset progress
    const stagesList = document.getElementById('stagesList');
    stagesList.innerHTML = '';
    updateProgress(0, 'Initializing...');
    
    // Track stages for final result
    const stagesData = {
        smart_queue: null,
        pcv: {
            proposed_prompt: null,
            critique: null,
            final_prompt: null
        },
        ds_iterations: [],
        evaluation: null,
        final_prompt: null,
        metadata: {}
    };
    
    try {
        // Call streaming API
        await apiClient.optimizePromptStream(config, (event) => {
            handleStreamEvent(event, stagesData);
        });
        
        // Build final result and display
        if (stagesData.final_prompt) {
            currentResult = buildFinalResult(stagesData, prompt);
            displayResults(currentResult);
            showResults();
        }
        
    } catch (error) {
        showError(error.message || 'An error occurred during optimization');
    } finally {
        showLoading(false);
    }
}

/**
 * Handle streaming event
 */
function handleStreamEvent(event, stagesData) {
    const stage = event.stage;
    const status = event.status;
    const data = event.data;
    const message = event.message;
    
    // Update progress based on stage
    const progressMap = {
        'init': 5,
        'smart_queue': 15,
        'pcv_proposer': 30,
        'pcv_critic': 45,
        'pcv_verifier': 60,
        'ds_iteration_1_d': 65,
        'ds_iteration_1_s': 70,
        'ds_iteration_2_d': 75,
        'ds_iteration_2_s': 80,
        'ds_iteration_3_d': 85,
        'ds_iteration_3_s': 90,
        'evaluation': 95,
        'complete': 100
    };
    
    const progress = progressMap[stage] || 0;
    updateProgress(progress, message || stage);
    
    // Add stage to real-time display
    addStageToDisplay(stage, status, message, data);
    
    // Store data for final result
    if (stage === 'smart_queue' && status === 'complete') {
        stagesData.smart_queue = data;
    } else if (stage === 'pcv_proposer' && status === 'complete') {
        stagesData.pcv.proposed_prompt = data.proposed_prompt;
    } else if (stage === 'pcv_critic' && status === 'complete') {
        stagesData.pcv.critique = data.critique;
    } else if (stage === 'pcv_verifier' && status === 'complete') {
        stagesData.pcv.final_prompt = data.final_prompt;
    } else if (stage.includes('ds_iteration') && stage.includes('_s') && status === 'complete') {
        stagesData.ds_iterations.push(data);
    } else if (stage === 'evaluation' && status === 'complete') {
        stagesData.evaluation = data;
    } else if (stage === 'complete') {
        Object.assign(stagesData.metadata, data);
        stagesData.final_prompt = data.final_prompt;
    }
}

/**
 * Update progress bar
 */
function updateProgress(percent, text) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const loadingMessage = document.getElementById('loadingMessage');
    
    if (progressBar) progressBar.style.width = `${percent}%`;
    if (progressText) progressText.textContent = `${percent}%`;
    if (loadingMessage) loadingMessage.textContent = text;
}

/**
 * Add stage to real-time display
 */
function addStageToDisplay(stage, status, message, data) {
    const stagesList = document.getElementById('stagesList');
    
    // Find existing stage item or create new
    let stageItem = document.getElementById(`stage-${stage}`);
    
    if (!stageItem) {
        stageItem = document.createElement('div');
        stageItem.id = `stage-${stage}`;
        stageItem.className = 'stage-item';
        stagesList.appendChild(stageItem);
    }
    
    // Update status class
    stageItem.className = `stage-item ${status || ''}`;
    
    // Format stage name
    const stageName = formatStageName(stage);
    const statusBadge = status ? `<span class="stage-status ${status}">${status}</span>` : '';
    
    stageItem.innerHTML = `
        <div class="stage-header">
            <span class="stage-title">${stageName}</span>
            ${statusBadge}
        </div>
        ${message ? `<div class="stage-message">${message}</div>` : ''}
    `;
}

/**
 * Format stage name for display
 */
function formatStageName(stage) {
    const nameMap = {
        'init': '🔧 Initialization',
        'smart_queue': '📊 Smart Queue Analysis',
        'pcv_proposer': '📝 Proposer',
        'pcv_critic': '🔍 Critic',
        'pcv_verifier': '✅ Verifier',
        'evaluation': '📈 Quality Evaluation',
        'complete': '✨ Complete'
    };
    
    if (nameMap[stage]) return nameMap[stage];
    
    // Handle D/S iterations
    if (stage.includes('ds_iteration')) {
        const match = stage.match(/ds_iteration_(\d+)_([ds])/);
        if (match) {
            const iter = match[1];
            const type = match[2] === 'd' ? 'Diversification' : 'Stabilization';
            return `🔁 D/S Iteration ${iter} - ${type}`;
        }
    }
    
    return stage;
}

/**
 * Build final result object from stages data
 */
function buildFinalResult(stagesData, originalPrompt) {
    return {
        success: true,
        original_prompt: originalPrompt,
        final_prompt: stagesData.final_prompt,
        smart_queue: stagesData.smart_queue,
        pcv: stagesData.pcv,
        ds_iterations: stagesData.ds_iterations,
        evaluation: stagesData.evaluation,
        ...stagesData.metadata
    };
}

/**
 * Show/hide real-time progress
 */
function showRealtimeProgress(show) {
    const realtimeProgress = document.getElementById('realtimeProgress');
    realtimeProgress.style.display = show ? 'block' : 'none';
}

/**
 * Display optimization results
 */
function displayResults(result) {
    // Smart Queue
    displaySmartQueue(result.smart_queue);
    
    // PCV
    if (result.pcv) {
        displayPCV(result.pcv);
    }
    
    // D/S Iterations
    displayDSIterations(result.ds_iterations);
    
    // Final Prompt
    displayFinalPrompt(result.final_prompt);
    
    // Evaluation
    if (result.evaluation) {
        displayEvaluation(result.evaluation);
    }
    
    // Metrics
    displayMetrics(result);
}

/**
 * Copy final prompt to clipboard
 */
async function handleCopyFinal() {
    if (!currentResult) return;
    
    try {
        await navigator.clipboard.writeText(currentResult.final_prompt);
        
        // Visual feedback
        const originalText = copyFinalBtn.textContent;
        copyFinalBtn.textContent = '✅ Copied!';
        setTimeout(() => {
            copyFinalBtn.textContent = originalText;
        }, 2000);
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
    optimizeBtn.disabled = show;
}

/**
 * Show/hide results section
 */
function showResults() {
    resultsSection.style.display = 'block';
}

function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorDisplay.textContent = `❌ Error: ${message}`;
    errorDisplay.style.display = 'block';
    errorDisplay.className = 'error-display';
}

/**
 * Show success message
 */
function showSuccess(message) {
    errorDisplay.textContent = `✅ ${message}`;
    errorDisplay.style.display = 'block';
    errorDisplay.className = 'success-display';
    setTimeout(() => {
        errorDisplay.style.display = 'none';
    }, 3000);
}

/**
 * Hide error message
 */
function hideError() {
    errorDisplay.style.display = 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
