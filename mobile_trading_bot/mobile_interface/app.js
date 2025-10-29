// Mobile Trading Bot - Client Application
// בוט מסחר נייד - אפליקציית לקוח

const API_BASE_URL = window.location.origin + '/api/v1';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    checkConnection();
    refreshAccountInfo();
    refreshPositions();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        if (document.getElementById('dashboard').classList.contains('active')) {
            refreshAccountInfo();
        }
        if (document.getElementById('positions').classList.contains('active')) {
            refreshPositions();
        }
    }, 30000);
});

// Tab Navigation
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to selected tab
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// API Helper Functions
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

// Connection Status
async function checkConnection() {
    try {
        const health = await apiCall('/health');
        updateConnectionStatus(health.mt5_connected);
    } catch (error) {
        updateConnectionStatus(false);
    }
}

function updateConnectionStatus(connected) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.getElementById('statusText');
    
    if (connected) {
        statusDot.classList.add('connected');
        statusText.textContent = 'מחובר';
    } else {
        statusDot.classList.remove('connected');
        statusText.textContent = 'לא מחובר';
    }
}

// Account Info
async function refreshAccountInfo() {
    try {
        const accountInfo = await apiCall('/mt5/account');
        
        document.getElementById('balance').textContent = formatCurrency(accountInfo.balance);
        document.getElementById('equity').textContent = formatCurrency(accountInfo.equity);
        document.getElementById('profit').textContent = formatCurrency(accountInfo.profit);
        
        const positions = await apiCall('/mt5/positions');
        document.getElementById('openPositions').textContent = positions.count;
        
    } catch (error) {
        console.error('Failed to refresh account info:', error);
    }
}

// Connect MT5
async function connectMT5(event) {
    event.preventDefault();
    
    const login = document.getElementById('mt5Login').value;
    const password = document.getElementById('mt5Password').value;
    const server = document.getElementById('mt5Server').value;
    
    showLoading('מתחבר ל-MT5...');
    
    try {
        const result = await apiCall('/mt5/connect', 'POST', {
            login: login ? parseInt(login) : null,
            password: password || null,
            server: server || null
        });
        
        if (result.success) {
            showToast('התחברות הצליחה!', 'success');
            updateConnectionStatus(true);
            refreshAccountInfo();
            
            // Switch to dashboard
            document.querySelector('[data-tab="dashboard"]').click();
        }
    } catch (error) {
        showToast('התחברות נכשלה', 'error');
    } finally {
        hideLoading();
    }
}

// Get Symbol Price
async function getSymbolPrice() {
    const symbol = document.getElementById('symbol').value.toUpperCase();
    if (!symbol) {
        showToast('נא להכניס סמל מסחר', 'error');
        return;
    }
    
    showLoading('מביא מחיר...');
    
    try {
        const price = await apiCall(`/mt5/price/${symbol}`);
        document.getElementById('price').value = price.ask;
        showToast(`מחיר ${symbol}: ${price.bid} / ${price.ask}`, 'success');
    } catch (error) {
        showToast('שגיאה בקבלת מחיר', 'error');
    } finally {
        hideLoading();
    }
}

// Place Order
async function placeOrder(event) {
    event.preventDefault();
    
    const orderData = {
        symbol: document.getElementById('symbol').value.toUpperCase(),
        order_type: document.getElementById('orderType').value,
        volume: parseFloat(document.getElementById('volume').value),
        price: document.getElementById('price').value ? parseFloat(document.getElementById('price').value) : null,
        stop_loss: document.getElementById('stopLoss').value ? parseFloat(document.getElementById('stopLoss').value) : null,
        take_profit: document.getElementById('takeProfit').value ? parseFloat(document.getElementById('takeProfit').value) : null,
    };
    
    showLoading('מבצע עסקה...');
    
    try {
        const result = await apiCall('/mt5/order', 'POST', orderData);
        
        if (result.success) {
            showToast('עסקה בוצעה בהצלחה!', 'success');
            document.getElementById('tradeForm').reset();
            refreshAccountInfo();
            refreshPositions();
        } else {
            showToast('ביצוע עסקה נכשל: ' + result.comment, 'error');
        }
    } catch (error) {
        showToast('שגיאה בביצוע עסקה', 'error');
    } finally {
        hideLoading();
    }
}

// Quick Trade
async function quickTrade(type) {
    const symbol = document.getElementById('quickSymbol').value;
    
    showLoading(`מבצע ${type === 'BUY' ? 'קנייה' : 'מכירה'}...`);
    
    try {
        // Get current price
        const price = await apiCall(`/mt5/price/${symbol}`);
        
        const orderData = {
            symbol: symbol,
            order_type: type,
            volume: 0.01,
        };
        
        const result = await apiCall('/mt5/order', 'POST', orderData);
        
        if (result.success) {
            showToast(`${type === 'BUY' ? 'קנייה' : 'מכירה'} בוצעה בהצלחה!`, 'success');
            refreshAccountInfo();
            refreshPositions();
            
            // Update price display
            document.getElementById('currentBid').textContent = price.bid.toFixed(5);
            document.getElementById('currentAsk').textContent = price.ask.toFixed(5);
        }
    } catch (error) {
        showToast('ביצוע עסקה נכשל', 'error');
    } finally {
        hideLoading();
    }
}

// Update quick trade price
async function updateQuickTradePrice() {
    const symbol = document.getElementById('quickSymbol').value;
    try {
        const price = await apiCall(`/mt5/price/${symbol}`);
        document.getElementById('currentBid').textContent = price.bid.toFixed(5);
        document.getElementById('currentAsk').textContent = price.ask.toFixed(5);
    } catch (error) {
        document.getElementById('currentBid').textContent = '-';
        document.getElementById('currentAsk').textContent = '-';
    }
}

// Update price when symbol changes
document.getElementById('quickSymbol').addEventListener('change', updateQuickTradePrice);
setInterval(updateQuickTradePrice, 5000); // Update every 5 seconds

// AI Analysis
async function getAIAnalysis() {
    const symbol = document.getElementById('aiSymbol').value.toUpperCase();
    if (!symbol) {
        showToast('נא להכניס סמל מסחר', 'error');
        return;
    }
    
    showLoading('מנתח עם AI...');
    
    try {
        const prediction = await apiCall(`/ai/predict/${symbol}`);
        
        const resultsDiv = document.getElementById('aiResults');
        resultsDiv.innerHTML = `
            <div class="signal-badge signal-${prediction.signal.toLowerCase()}">
                ${prediction.signal === 'BUY' ? '🟢 קנייה' : prediction.signal === 'SELL' ? '🔴 מכירה' : '⚪ החזקה'}
            </div>
            <p><strong>ביטחון:</strong> ${(prediction.confidence * 100).toFixed(1)}%</p>
            <p><strong>הסתברות קנייה:</strong> ${(prediction.buy_probability * 100).toFixed(1)}%</p>
            ${prediction.analysis ? `
                <hr style="margin: 1rem 0;">
                <h3>ניתוח טכני:</h3>
                <p><strong>מגמה:</strong> ${prediction.analysis.trend}</p>
                <p><strong>RSI:</strong> ${prediction.analysis.rsi.toFixed(2)}</p>
                <p><strong>המלצה:</strong> ${prediction.analysis.recommendation}</p>
            ` : ''}
        `;
        
        showToast('ניתוח הושלם', 'success');
    } catch (error) {
        showToast('שגיאה בניתוח AI', 'error');
    } finally {
        hideLoading();
    }
}

// Train AI Model
async function trainAIModel() {
    const symbol = document.getElementById('trainSymbol').value.toUpperCase();
    const periods = parseInt(document.getElementById('trainPeriods').value);
    
    if (!symbol) {
        showToast('נא להכניס סמל מסחר', 'error');
        return;
    }
    
    showLoading('מאמן מודל AI (זה יכול לקחת זמן)...');
    
    try {
        const result = await apiCall('/ai/train', 'POST', {
            symbol: symbol,
            periods: periods
        });
        
        const resultsDiv = document.getElementById('trainingResults');
        resultsDiv.innerHTML = `
            <div class="signal-badge signal-buy">
                אימון הושלם בהצלחה!
            </div>
            <p><strong>דיוק אימון:</strong> ${(result.metrics.train_accuracy * 100).toFixed(2)}%</p>
            <p><strong>דיוק בדיקה:</strong> ${(result.metrics.test_accuracy * 100).toFixed(2)}%</p>
            <p><strong>דגימות:</strong> ${result.metrics.samples}</p>
        `;
        
        showToast('אימון הושלם בהצלחה!', 'success');
    } catch (error) {
        showToast('שגיאה באימון מודל', 'error');
    } finally {
        hideLoading();
    }
}

// Positions
async function refreshPositions() {
    try {
        const positions = await apiCall('/mt5/positions');
        
        const positionsList = document.getElementById('positionsList');
        
        if (positions.count === 0) {
            positionsList.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">אין פוזיציות פתוחות</p>';
            return;
        }
        
        positionsList.innerHTML = positions.positions.map(pos => {
            const profit = pos.profit || 0;
            const profitClass = profit >= 0 ? 'positive' : 'negative';
            const typeText = pos.type === 0 ? 'קנייה' : 'מכירה';
            
            return `
                <div class="position-item">
                    <div class="position-info">
                        <div><strong>${pos.symbol}</strong> - ${typeText}</div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                            Volume: ${pos.volume} | Price: ${pos.price_open}
                        </div>
                    </div>
                    <div class="position-profit ${profitClass}">
                        ${formatCurrency(profit)}
                    </div>
                    <button class="btn btn-small" onclick="closePosition(${pos.ticket})" style="margin-right: 0.5rem;">סגור</button>
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Failed to refresh positions:', error);
    }
}

// Close Position
async function closePosition(ticket) {
    if (!confirm('האם אתה בטוח שברצונך לסגור את הפוזיציה?')) {
        return;
    }
    
    showLoading('סוגר פוזיציה...');
    
    try {
        const result = await apiCall(`/mt5/close/${ticket}`, 'POST');
        
        if (result.success) {
            showToast('פוזיציה נסגרה בהצלחה!', 'success');
            refreshAccountInfo();
            refreshPositions();
        }
    } catch (error) {
        showToast('שגיאה בסגירת פוזיציה', 'error');
    } finally {
        hideLoading();
    }
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('he-IL', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function showLoading(text = 'טוען...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = text;
    overlay.classList.add('show');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('show');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
