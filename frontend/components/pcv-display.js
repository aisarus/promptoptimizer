/**
 * PCV (Proposer-Critic-Verifier) Display Component
 */

function displayPCV(pcv) {
    const container = document.getElementById('pcvResults');
    
    const html = `
        <div class="expandable">
            <div class="expandable-header" onclick="toggleExpandable(this)">
                <h3>📝 Proposed Prompt (Proposer)</h3>
                <span class="expandable-icon">▶</span>
            </div>
            <div class="expandable-content">
                <div class="code-display">
                    <pre>${escapeHtml(pcv.proposed_prompt)}</pre>
                </div>
            </div>
        </div>
        
        <div class="expandable">
            <div class="expandable-header" onclick="toggleExpandable(this)">
                <h3>🔍 Critique (Critic)</h3>
                <span class="expandable-icon">▶</span>
            </div>
            <div class="expandable-content">
                <div class="code-display">
                    <pre>${escapeHtml(pcv.critique)}</pre>
                </div>
            </div>
        </div>
        
        <div class="expandable">
            <div class="expandable-header" onclick="toggleExpandable(this)">
                <h3>✅ Verified Prompt (Final PCV)</h3>
                <span class="expandable-icon">▶</span>
            </div>
            <div class="expandable-content">
                <div class="code-display">
                    <pre>${escapeHtml(pcv.final_prompt)}</pre>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Toggle expandable section
 */
function toggleExpandable(header) {
    const icon = header.querySelector('.expandable-icon');
    const content = header.nextElementSibling;
    
    const isOpen = content.classList.contains('open');
    
    if (isOpen) {
        content.classList.remove('open');
        icon.classList.remove('open');
    } else {
        content.classList.add('open');
        icon.classList.add('open');
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
