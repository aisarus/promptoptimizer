/**
 * Smart Queue Display Component
 */

function displaySmartQueue(smartQueue) {
    const container = document.getElementById('smartQueueResults');
    
    const html = `
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Clarity</div>
                <div class="metric-value">${smartQueue.clarity.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Structure</div>
                <div class="metric-value">${smartQueue.structure.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Constraints</div>
                <div class="metric-value">${smartQueue.constraints.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Needs Optimization</div>
                <div class="metric-value ${smartQueue.needs_optimization ? 'positive' : 'neutral'}">
                    ${smartQueue.needs_optimization ? 'Yes' : 'No'}
                </div>
            </div>
        </div>
        ${smartQueue.comment ? `<div class="comment-box">${smartQueue.comment}</div>` : ''}
    `;
    
    container.innerHTML = html;
}
