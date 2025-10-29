"""
Flask Web Application for Trading Bot Mobile Interface
"""
import asyncio
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os
from functools import wraps

from ..core.bot import TradingBot
from ..config.settings import WEB_CONFIG

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = WEB_CONFIG['secret_key']
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Global bot instance
    trading_bot = None
    
    def require_auth(f):
        """Simple authentication decorator"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple session-based auth (replace with proper auth in production)
            if 'authenticated' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Simple login page"""
        if request.method == 'POST':
            password = request.form.get('password')
            # Simple password check (replace with proper auth)
            if password == 'trading123':  # Change this!
                session['authenticated'] = True
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid password')
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        """Logout"""
        session.pop('authenticated', None)
        return redirect(url_for('login'))
    
    @app.route('/')
    @require_auth
    def dashboard():
        """Main dashboard"""
        return render_template('dashboard.html')
    
    @app.route('/api/status')
    @require_auth
    def get_status():
        """Get bot status"""
        try:
            if trading_bot:
                status = asyncio.run(trading_bot.get_status())
            else:
                status = {
                    'is_running': False,
                    'error': 'Bot not initialized'
                }
            
            return jsonify(status)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/start', methods=['POST'])
    @require_auth
    def start_bot():
        """Start the trading bot"""
        try:
            global trading_bot
            if not trading_bot:
                trading_bot = TradingBot()
            
            # Start bot in background
            asyncio.create_task(trading_bot.start())
            
            return jsonify({'success': True, 'message': 'Bot starting...'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/stop', methods=['POST'])
    @require_auth
    def stop_bot():
        """Stop the trading bot"""
        try:
            if trading_bot:
                asyncio.create_task(trading_bot.stop())
            
            return jsonify({'success': True, 'message': 'Bot stopping...'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/positions')
    @require_auth
    def get_positions():
        """Get current positions"""
        try:
            if trading_bot and trading_bot.mt5:
                positions = asyncio.run(trading_bot.mt5.get_positions())
                return jsonify(positions or [])
            else:
                return jsonify([])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/history')
    @require_auth
    def get_history():
        """Get trading history"""
        try:
            if trading_bot and trading_bot.mt5:
                history = asyncio.run(trading_bot.mt5.get_history_deals(days=7))
                return jsonify(history or [])
            else:
                return jsonify([])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/settings', methods=['GET', 'POST'])
    @require_auth
    def settings():
        """Get/Update bot settings"""
        try:
            if request.method == 'GET':
                # Return current settings
                if trading_bot:
                    risk_metrics = trading_bot.risk_manager.get_risk_metrics()
                    return jsonify(risk_metrics)
                else:
                    return jsonify({})
            
            elif request.method == 'POST':
                # Update settings
                new_settings = request.json
                
                if trading_bot:
                    trading_bot.risk_manager.update_risk_parameters(new_settings)
                    return jsonify({'success': True, 'message': 'Settings updated'})
                else:
                    return jsonify({'error': 'Bot not initialized'}), 400
                    
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/test-notifications', methods=['POST'])
    @require_auth
    def test_notifications():
        """Test notification system"""
        try:
            if trading_bot:
                results = asyncio.run(trading_bot.notifier.test_notifications())
                return jsonify(results)
            else:
                return jsonify({'error': 'Bot not initialized'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/market-data/<symbol>')
    @require_auth
    def get_market_data(symbol):
        """Get market data for symbol"""
        try:
            if trading_bot and trading_bot.mt5:
                data = asyncio.run(trading_bot.mt5.get_rates(symbol, 'H1', 24))
                return jsonify(data or [])
            else:
                return jsonify([])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # SocketIO events for real-time updates
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        if 'authenticated' not in session:
            return False
        
        emit('connected', {'message': 'Connected to Trading Bot'})
        logger.info('Client connected to SocketIO')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info('Client disconnected from SocketIO')
    
    @socketio.on('request_status')
    def handle_status_request():
        """Handle status request via SocketIO"""
        try:
            if trading_bot:
                status = asyncio.run(trading_bot.get_status())
                emit('status_update', status)
        except Exception as e:
            emit('error', {'message': str(e)})
    
    # Background task to send real-time updates
    def background_updates():
        """Send periodic updates to connected clients"""
        while True:
            try:
                if trading_bot:
                    status = asyncio.run(trading_bot.get_status())
                    socketio.emit('status_update', status)
                
                socketio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                logger.error(f"Error in background updates: {e}")
                socketio.sleep(10)
    
    # Start background task
    socketio.start_background_task(background_updates)
    
    return app, socketio

# Template functions
def create_templates():
    """Create HTML templates"""
    
    # Create templates directory
    templates_dir = 'trading_bot/web/templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Trading Bot{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-running { background-color: #28a745; }
        .status-stopped { background-color: #dc3545; }
        .card-metric {
            text-align: center;
            padding: 20px;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
        }
        .metric-label {
            color: #6c757d;
            font-size: 0.9rem;
        }
        .mobile-optimized {
            padding: 10px;
        }
        @media (max-width: 768px) {
            .metric-value { font-size: 1.5rem; }
            .card { margin-bottom: 15px; }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-robot"></i> Trading Bot
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/logout">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container mobile-optimized">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    with open(f'{templates_dir}/base.html', 'w') as f:
        f.write(base_template)
    
    # Login template
    login_template = '''{% extends "base.html" %}

{% block title %}Login - Trading Bot{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-4">
        <div class="card">
            <div class="card-header text-center">
                <h4><i class="fas fa-lock"></i> Login</h4>
            </div>
            <div class="card-body">
                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
                
                <form method="POST">
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    with open(f'{templates_dir}/login.html', 'w') as f:
        f.write(login_template)
    
    # Dashboard template
    dashboard_template = '''{% extends "base.html" %}

{% block content %}
<div class="row mt-3">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2><i class="fas fa-tachometer-alt"></i> Dashboard</h2>
            <div>
                <span class="status-indicator" id="statusIndicator"></span>
                <span id="statusText">Loading...</span>
            </div>
        </div>
    </div>
</div>

<!-- Control Buttons -->
<div class="row mb-4">
    <div class="col-12">
        <div class="btn-group w-100" role="group">
            <button class="btn btn-success" id="startBtn">
                <i class="fas fa-play"></i> Start
            </button>
            <button class="btn btn-danger" id="stopBtn">
                <i class="fas fa-stop"></i> Stop
            </button>
            <button class="btn btn-info" id="refreshBtn">
                <i class="fas fa-sync"></i> Refresh
            </button>
        </div>
    </div>
</div>

<!-- Metrics Cards -->
<div class="row">
    <div class="col-6 col-md-3">
        <div class="card card-metric">
            <div class="metric-value text-primary" id="balance">$0</div>
            <div class="metric-label">Balance</div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card card-metric">
            <div class="metric-value text-success" id="equity">$0</div>
            <div class="metric-label">Equity</div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card card-metric">
            <div class="metric-value" id="dailyPnl">$0</div>
            <div class="metric-label">Daily P&L</div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card card-metric">
            <div class="metric-value text-info" id="positions">0</div>
            <div class="metric-label">Positions</div>
        </div>
    </div>
</div>

<!-- Positions Table -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-line"></i> Open Positions</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-sm" id="positionsTable">
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Volume</th>
                                <th>Entry</th>
                                <th>Current</th>
                                <th>P&L</th>
                            </tr>
                        </thead>
                        <tbody id="positionsBody">
                            <tr>
                                <td colspan="6" class="text-center">No positions</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Settings Modal -->
<div class="modal fade" id="settingsModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Bot Settings</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="settingsForm">
                    <div class="mb-3">
                        <label class="form-label">Max Risk Per Trade (%)</label>
                        <input type="number" class="form-control" id="maxRiskPerTrade" step="0.01" min="0" max="10">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Max Daily Loss (%)</label>
                        <input type="number" class="form-control" id="maxDailyLoss" step="0.01" min="0" max="50">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Max Open Positions</label>
                        <input type="number" class="form-control" id="maxOpenPositions" min="1" max="20">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" id="saveSettings">Save</button>
            </div>
        </div>
    </div>
</div>

<!-- Bottom Navigation -->
<div class="fixed-bottom bg-light border-top p-2 d-md-none">
    <div class="row text-center">
        <div class="col-3">
            <button class="btn btn-link" onclick="refreshData()">
                <i class="fas fa-home"></i><br><small>Home</small>
            </button>
        </div>
        <div class="col-3">
            <button class="btn btn-link" data-bs-toggle="modal" data-bs-target="#settingsModal">
                <i class="fas fa-cog"></i><br><small>Settings</small>
            </button>
        </div>
        <div class="col-3">
            <button class="btn btn-link" onclick="testNotifications()">
                <i class="fas fa-bell"></i><br><small>Test</small>
            </button>
        </div>
        <div class="col-3">
            <button class="btn btn-link" onclick="location.reload()">
                <i class="fas fa-sync"></i><br><small>Refresh</small>
            </button>
        </div>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
    const socket = io();
    
    // Socket events
    socket.on('connect', function() {
        console.log('Connected to server');
        socket.emit('request_status');
    });
    
    socket.on('status_update', function(data) {
        updateDashboard(data);
    });
    
    socket.on('error', function(data) {
        showAlert('Error: ' + data.message, 'danger');
    });
    
    // Button handlers
    document.getElementById('startBtn').onclick = startBot;
    document.getElementById('stopBtn').onclick = stopBot;
    document.getElementById('refreshBtn').onclick = refreshData;
    document.getElementById('saveSettings').onclick = saveSettings;
    
    function startBot() {
        fetch('/api/start', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.error, 'danger');
                }
            })
            .catch(error => showAlert('Error: ' + error, 'danger'));
    }
    
    function stopBot() {
        fetch('/api/stop', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.error, 'danger');
                }
            })
            .catch(error => showAlert('Error: ' + error, 'danger'));
    }
    
    function refreshData() {
        socket.emit('request_status');
        loadPositions();
    }
    
    function updateDashboard(data) {
        // Update status indicator
        const indicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (data.is_running) {
            indicator.className = 'status-indicator status-running';
            statusText.textContent = 'Running';
        } else {
            indicator.className = 'status-indicator status-stopped';
            statusText.textContent = 'Stopped';
        }
        
        // Update metrics
        document.getElementById('balance').textContent = '$' + (data.account_balance || 0).toFixed(2);
        document.getElementById('equity').textContent = '$' + (data.account_equity || 0).toFixed(2);
        
        const dailyPnl = data.daily_pnl || 0;
        const pnlElement = document.getElementById('dailyPnl');
        pnlElement.textContent = '$' + dailyPnl.toFixed(2);
        pnlElement.className = 'metric-value ' + (dailyPnl >= 0 ? 'text-success' : 'text-danger');
        
        document.getElementById('positions').textContent = data.open_positions || 0;
    }
    
    function loadPositions() {
        fetch('/api/positions')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('positionsBody');
                tbody.innerHTML = '';
                
                if (data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No positions</td></tr>';
                } else {
                    data.forEach(pos => {
                        const row = `
                            <tr>
                                <td>${pos.symbol}</td>
                                <td>${pos.type === 0 ? 'Buy' : 'Sell'}</td>
                                <td>${pos.volume}</td>
                                <td>${pos.price_open}</td>
                                <td>${pos.price_current}</td>
                                <td class="${pos.profit >= 0 ? 'text-success' : 'text-danger'}">
                                    $${pos.profit.toFixed(2)}
                                </td>
                            </tr>
                        `;
                        tbody.innerHTML += row;
                    });
                }
            })
            .catch(error => console.error('Error loading positions:', error));
    }
    
    function saveSettings() {
        const settings = {
            max_risk_per_trade: parseFloat(document.getElementById('maxRiskPerTrade').value) / 100,
            max_daily_loss: parseFloat(document.getElementById('maxDailyLoss').value) / 100,
            max_open_positions: parseInt(document.getElementById('maxOpenPositions').value)
        };
        
        fetch('/api/settings', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(settings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Settings saved successfully', 'success');
                bootstrap.Modal.getInstance(document.getElementById('settingsModal')).hide();
            } else {
                showAlert(data.error, 'danger');
            }
        })
        .catch(error => showAlert('Error: ' + error, 'danger'));
    }
    
    function testNotifications() {
        fetch('/api/test-notifications', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                let message = 'Notification test results:\\n';
                message += 'Telegram: ' + (data.telegram ? 'Success' : 'Failed') + '\\n';
                message += 'Email: ' + (data.email ? 'Success' : 'Failed');
                alert(message);
            })
            .catch(error => showAlert('Error: ' + error, 'danger'));
    }
    
    function showAlert(message, type) {
        const alert = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.querySelector('.container');
        container.insertAdjacentHTML('afterbegin', alert);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alertElement = container.querySelector('.alert');
            if (alertElement) {
                alertElement.remove();
            }
        }, 5000);
    }
    
    // Load initial data
    refreshData();
    
    // Auto-refresh every 30 seconds
    setInterval(refreshData, 30000);
</script>
{% endblock %}'''
    
    with open(f'{templates_dir}/dashboard.html', 'w') as f:
        f.write(dashboard_template)

# Create templates when module is imported
create_templates()