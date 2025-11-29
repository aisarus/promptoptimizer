/**
 * Metrics Display Component
 */

function displayMetrics(result) {
    const container = document.getElementById('metricsResults');
    
    const html = `
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Original Length</div>
                <div class="metric-value neutral">${result.original_length}</div>
                <small style="color: var(--text-secondary);">words</small>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Final Length</div>
                <div class="metric-value neutral">${result.final_length}</div>
                <small style="color: var(--text-secondary);">words</small>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Length Change</div>
                <div class="metric-value ${result.length_change_percent > 0 ? 'positive' : 'negative'}">
                    ${result.length_change_percent >= 0 ? '+' : ''}${result.length_change_percent.toFixed(1)}%
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Processing Time</div>
                <div class="metric-value neutral">${result.processing_time_seconds.toFixed(2)}s</div>
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <div class="metric-card" style="grid-column: span 2;">
                <div class="metric-label">Convergence Status</div>
                ${result.converged ? 
                    `<span class="badge success">✅ Converged at iteration ${result.convergence_iteration}</span>` :
                    `<span class="badge warning">⚠️ Did not converge (max iterations reached)</span>`
                }
            </div>
        </div>
        
        <div class="comparison-grid" style="margin-top: 25px;">
            <div class="comparison-item">
                <h4>📄 Original Prompt</h4>
                <div class="code-display">
                    <pre style="max-height: 200px; overflow-y: auto;">${escapeHtml(result.original_prompt)}</pre>
                </div>
            </div>
            <div class="comparison-item">
                <h4>✨ Final Prompt</h4>
                <div class="code-display">
                    <pre style="max-height: 200px; overflow-y: auto;">${escapeHtml(result.final_prompt)}</pre>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}
