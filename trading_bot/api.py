"""
Mobile API Server
Provides REST API for controlling the bot from mobile devices
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from functools import wraps
import logging
from bot import TradingBot
from config import API_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) if API_CONFIG['enable_cors'] else None
app.secret_key = API_CONFIG['secret_key']

# Initialize bot
bot = None


def require_auth(f):
    """Authentication decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token or token != f"Bearer {API_CONFIG['auth_token']}":
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


@app.route('/')
def index():
    """Mobile-friendly web interface"""
    return render_template_string(MOBILE_HTML)


@app.route('/api/status', methods=['GET'])
@require_auth
def get_status():
    """Get bot status"""
    if bot is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    status = bot.get_status()
    return jsonify(status)


@app.route('/api/start', methods=['POST'])
@require_auth
def start_bot():
    """Start the trading bot"""
    if bot is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    if bot.is_running:
        return jsonify({'message': 'Bot is already running'}), 200
    
    bot.start()
    return jsonify({'message': 'Bot started successfully'})


@app.route('/api/stop', methods=['POST'])
@require_auth
def stop_bot():
    """Stop the trading bot"""
    if bot is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    if not bot.is_running:
        return jsonify({'message': 'Bot is not running'}), 200
    
    bot.stop()
    return jsonify({'message': 'Bot stopped successfully'})


@app.route('/api/positions', methods=['GET'])
@require_auth
def get_positions():
    """Get all open positions"""
    if bot is None or not bot.mt5.connected:
        return jsonify({'error': 'Not connected to MT5'}), 500
    
    positions = bot.mt5.get_open_positions()
    return jsonify({'positions': positions})


@app.route('/api/positions/<int:ticket>/close', methods=['POST'])
@require_auth
def close_position(ticket):
    """Close a specific position"""
    if bot is None or not bot.mt5.connected:
        return jsonify({'error': 'Not connected to MT5'}), 500
    
    success = bot.mt5.close_position(ticket)
    
    if success:
        return jsonify({'message': f'Position {ticket} closed successfully'})
    else:
        return jsonify({'error': f'Failed to close position {ticket}'}), 500


@app.route('/api/account', methods=['GET'])
@require_auth
def get_account():
    """Get account information"""
    if bot is None or not bot.mt5.connected:
        return jsonify({'error': 'Not connected to MT5'}), 500
    
    account_info = bot.mt5.get_account_info()
    return jsonify(account_info)


@app.route('/api/train', methods=['POST'])
@require_auth
def retrain_model():
    """Retrain the AI model"""
    if bot is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    try:
        df = bot.mt5.get_historical_data(
            symbol='EURUSD',
            timeframe='H1',
            bars=5000
        )
        
        if df is None:
            return jsonify({'error': 'Failed to get historical data'}), 500
        
        train_score, test_score = bot.ai_strategy.train_model(df)
        
        return jsonify({
            'message': 'Model retrained successfully',
            'train_accuracy': train_score,
            'test_accuracy': test_score
        })
    
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
@require_auth
def get_statistics():
    """Get trading statistics"""
    if bot is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    return jsonify(bot.stats)


# Mobile-friendly HTML interface
MOBILE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MT5 Trading Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
        }
        
        h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 20px;
        }
        
        .status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-indicator.active {
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
        }
        
        .status-indicator.inactive {
            background: #ef4444;
        }
        
        .button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
        }
        
        .button-primary {
            background: #10b981;
            color: white;
        }
        
        .button-primary:active {
            transform: scale(0.98);
            background: #059669;
        }
        
        .button-danger {
            background: #ef4444;
            color: white;
        }
        
        .button-danger:active {
            transform: scale(0.98);
            background: #dc2626;
        }
        
        .button-secondary {
            background: #6366f1;
            color: white;
        }
        
        .button-secondary:active {
            transform: scale(0.98);
            background: #4f46e5;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .stat-row:last-child {
            border-bottom: none;
        }
        
        .stat-label {
            color: #6b7280;
            font-size: 14px;
        }
        
        .stat-value {
            color: #111827;
            font-weight: 600;
            font-size: 14px;
        }
        
        .position {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .position-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .position-type {
            font-weight: 600;
            font-size: 16px;
        }
        
        .position-type.buy {
            color: #10b981;
        }
        
        .position-type.sell {
            color: #ef4444;
        }
        
        .position-profit {
            font-weight: 600;
            font-size: 16px;
        }
        
        .position-profit.positive {
            color: #10b981;
        }
        
        .position-profit.negative {
            color: #ef4444;
        }
        
        .close-btn {
            width: 100%;
            padding: 10px;
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }
        
        .loading {
            text-align: center;
            color: #6b7280;
            padding: 20px;
        }
        
        #authToken {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 MT5 Trading Bot</h1>
        
        <div class="card">
            <h2>Authentication</h2>
            <input type="password" id="authToken" placeholder="Enter your auth token">
        </div>
        
        <div class="card">
            <h2>Bot Control</h2>
            <div class="status">
                <div style="display: flex; align-items: center;">
                    <div class="status-indicator" id="statusIndicator"></div>
                    <span id="statusText">Loading...</span>
                </div>
            </div>
            <button class="button button-primary" onclick="startBot()">▶ Start Bot</button>
            <button class="button button-danger" onclick="stopBot()">⏸ Stop Bot</button>
            <button class="button button-secondary" onclick="retrainModel()">🧠 Retrain AI Model</button>
        </div>
        
        <div class="card">
            <h2>Account Info</h2>
            <div id="accountInfo">
                <div class="loading">Loading...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Open Positions</h2>
            <div id="positions">
                <div class="loading">Loading...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Statistics</h2>
            <div id="statistics">
                <div class="loading">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        const API_BASE = window.location.origin;
        let authToken = '';
        
        function getAuthToken() {
            return document.getElementById('authToken').value || authToken;
        }
        
        function getHeaders() {
            const token = getAuthToken();
            return {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            };
        }
        
        async function apiCall(endpoint, method = 'GET') {
            try {
                const response = await fetch(`${API_BASE}/api/${endpoint}`, {
                    method: method,
                    headers: getHeaders()
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    alert(error.error || 'Request failed');
                    return null;
                }
                
                return await response.json();
            } catch (error) {
                alert('Network error: ' + error.message);
                return null;
            }
        }
        
        async function startBot() {
            const result = await apiCall('start', 'POST');
            if (result) {
                alert(result.message);
                updateStatus();
            }
        }
        
        async function stopBot() {
            const result = await apiCall('stop', 'POST');
            if (result) {
                alert(result.message);
                updateStatus();
            }
        }
        
        async function retrainModel() {
            if (confirm('Retrain AI model? This may take a few minutes.')) {
                const result = await apiCall('train', 'POST');
                if (result) {
                    alert(`Model retrained!\\nTrain: ${(result.train_accuracy * 100).toFixed(1)}%\\nTest: ${(result.test_accuracy * 100).toFixed(1)}%`);
                }
            }
        }
        
        async function updateStatus() {
            const status = await apiCall('status');
            if (!status) return;
            
            const indicator = document.getElementById('statusIndicator');
            const text = document.getElementById('statusText');
            
            if (status.is_running) {
                indicator.className = 'status-indicator active';
                text.textContent = 'Bot is Running';
            } else {
                indicator.className = 'status-indicator inactive';
                text.textContent = 'Bot is Stopped';
            }
            
            updateAccount(status.account);
            updatePositions(status.open_positions);
            updateStatistics(status.statistics);
        }
        
        function updateAccount(account) {
            if (!account) return;
            
            document.getElementById('accountInfo').innerHTML = `
                <div class="stat-row">
                    <span class="stat-label">Balance</span>
                    <span class="stat-value">$${account.balance.toFixed(2)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Equity</span>
                    <span class="stat-value">$${account.equity.toFixed(2)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Profit</span>
                    <span class="stat-value" style="color: ${account.profit >= 0 ? '#10b981' : '#ef4444'}">
                        $${account.profit.toFixed(2)}
                    </span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Margin Level</span>
                    <span class="stat-value">${account.margin_level.toFixed(2)}%</span>
                </div>
            `;
        }
        
        function updatePositions(positions) {
            if (!positions || positions.length === 0) {
                document.getElementById('positions').innerHTML = '<div class="loading">No open positions</div>';
                return;
            }
            
            let html = '';
            positions.forEach(pos => {
                const profitClass = pos.profit >= 0 ? 'positive' : 'negative';
                const typeClass = pos.type.toLowerCase();
                
                html += `
                    <div class="position">
                        <div class="position-header">
                            <span class="position-type ${typeClass}">${pos.type} ${pos.symbol}</span>
                            <span class="position-profit ${profitClass}">$${pos.profit.toFixed(2)}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Volume</span>
                            <span class="stat-value">${pos.volume}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Open Price</span>
                            <span class="stat-value">${pos.price_open.toFixed(5)}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Current Price</span>
                            <span class="stat-value">${pos.price_current.toFixed(5)}</span>
                        </div>
                        <button class="close-btn" onclick="closePosition(${pos.ticket})">Close Position</button>
                    </div>
                `;
            });
            
            document.getElementById('positions').innerHTML = html;
        }
        
        function updateStatistics(stats) {
            if (!stats) return;
            
            const winRate = stats.total_trades > 0 
                ? (stats.winning_trades / stats.total_trades * 100).toFixed(1) 
                : 0;
            
            document.getElementById('statistics').innerHTML = `
                <div class="stat-row">
                    <span class="stat-label">Total Trades</span>
                    <span class="stat-value">${stats.total_trades}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Win Rate</span>
                    <span class="stat-value">${winRate}%</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Total Profit</span>
                    <span class="stat-value" style="color: ${stats.total_profit >= 0 ? '#10b981' : '#ef4444'}">
                        $${stats.total_profit.toFixed(2)}
                    </span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Daily Profit</span>
                    <span class="stat-value" style="color: ${stats.daily_profit >= 0 ? '#10b981' : '#ef4444'}">
                        $${stats.daily_profit.toFixed(2)}
                    </span>
                </div>
            `;
        }
        
        async function closePosition(ticket) {
            if (confirm(`Close position #${ticket}?`)) {
                const result = await apiCall(`positions/${ticket}/close`, 'POST');
                if (result) {
                    alert(result.message);
                    updateStatus();
                }
            }
        }
        
        // Auto-update every 5 seconds
        setInterval(updateStatus, 5000);
        
        // Initial update
        updateStatus();
    </script>
</body>
</html>
'''


def run_server(trading_bot):
    """Run the API server"""
    global bot
    bot = trading_bot
    
    logger.info(f"Starting API server on {API_CONFIG['host']}:{API_CONFIG['port']}")
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=False
    )


if __name__ == "__main__":
    # For testing purposes
    from bot import TradingBot
    
    bot = TradingBot()
    if bot.initialize():
        run_server(bot)
