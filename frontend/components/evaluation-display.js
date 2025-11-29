/**
 * Evaluation Display Component
 */

function displayEvaluation(evaluation) {
    const container = document.getElementById('evaluationResults');
    
    const getClass = (value) => {
        if (value > 0.3) return 'positive';
        if (value < -0.3) return 'negative';
        return 'neutral';
    };
    
    const formatDelta = (value) => {
        const sign = value >= 0 ? '+' : '';
        return `${sign}${value.toFixed(2)}`;
    };
    
    const html = `
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Clarity Δ</div>
                <div class="metric-value ${getClass(evaluation.clarity)}">
                    ${formatDelta(evaluation.clarity)}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Structure Δ</div>
                <div class="metric-value ${getClass(evaluation.structure)}">
                    ${formatDelta(evaluation.structure)}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Constraints Δ</div>
                <div class="metric-value ${getClass(evaluation.constraints)}">
                    ${formatDelta(evaluation.constraints)}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Usefulness Δ</div>
                <div class="metric-value ${getClass(evaluation.usefulness)}">
                    ${formatDelta(evaluation.usefulness)}
                </div>
            </div>
        </div>
        ${evaluation.comment ? `<div class="comment-box">${escapeHtml(evaluation.comment)}</div>` : ''}
        
        <div style="margin-top: 15px; padding: 15px; background: var(--bg-secondary); border-radius: 8px;">
            <small style="color: var(--text-secondary);">
                <strong>Legend:</strong> 
                +1.0 = Much better | +0.66 = Moderately better | +0.33 = Slightly better | 
                0.0 = Similar | Negative = Original was better
            </small>
        </div>
    `;
    
    container.innerHTML = html;
}
