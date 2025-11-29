/**
 * D/S Iterations Display Component
 */

function displayDSIterations(iterations) {
    const container = document.getElementById('dsResults');
    
    if (!iterations || iterations.length === 0) {
        container.innerHTML = '<p>No D/S iterations performed</p>';
        return;
    }
    
    const iterationsHtml = iterations.map(iter => `
        <div class="iteration-item">
            <div class="iteration-header">
                <span class="iteration-number">Iteration ${iter.iteration}</span>
                <span class="iteration-stats">
                    Length: ${iter.length} words | Change: ${(iter.change_rate * 100).toFixed(1)}%
                </span>
            </div>
            
            <div class="expandable">
                <div class="expandable-header" onclick="toggleExpandable(this)">
                    <h4>🔄 D-Block (Diversification)</h4>
                    <span class="expandable-icon">▶</span>
                </div>
                <div class="expandable-content">
                    <div class="code-display">
                        <pre>${escapeHtml(iter.d_block_output)}</pre>
                    </div>
                </div>
            </div>
            
            <div class="expandable">
                <div class="expandable-header" onclick="toggleExpandable(this)">
                    <h4>🎯 S-Block (Stabilization)</h4>
                    <span class="expandable-icon">▶</span>
                </div>
                <div class="expandable-content">
                    <div class="code-display">
                        <pre>${escapeHtml(iter.s_block_output)}</pre>
                    </div>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${Math.min(iter.change_rate * 100, 100)}%"></div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="iteration-list">${iterationsHtml}</div>`;
}

/**
 * Display final prompt
 */
function displayFinalPrompt(finalPrompt) {
    const container = document.getElementById('finalPrompt');
    
    container.innerHTML = `
        <div class="code-display">
            <pre>${escapeHtml(finalPrompt)}</pre>
        </div>
    `;
}
