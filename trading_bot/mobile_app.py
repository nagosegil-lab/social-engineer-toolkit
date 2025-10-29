"""
Mobile-friendly web interface for the Trading Bot
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import plotly.graph_objs as go
import plotly.utils
import json
import logging
from datetime import datetime, timedelta
from trading_bot import TradingBot
from config import Config

app = Flask(__name__)
CORS(app)

# Global bot instance
bot = None
bot_thread = None

def init_bot():
    """Initialize the trading bot"""
    global bot
    if bot is None:
        bot = TradingBot()
    return bot

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get bot status"""
    try:
        bot = init_bot()
        status = bot.get_bot_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the trading bot"""
    try:
        global bot_thread
        import threading
        
        bot = init_bot()
        
        if not bot.running:
            bot_thread = threading.Thread(target=bot.start, daemon=True)
            bot_thread.start()
            return jsonify({'status': 'started'})
        else:
            return jsonify({'status': 'already_running'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the trading bot"""
    try:
        bot = init_bot()
        bot.stop()
        return jsonify({'status': 'stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/positions')
def get_positions():
    """Get current positions"""
    try:
        bot = init_bot()
        if bot.mt5.connected:
            positions = bot.mt5.get_positions()
            return jsonify(positions)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/close_position/<int:ticket>', methods=['POST'])
def close_position(ticket):
    """Close a specific position"""
    try:
        bot = init_bot()
        if bot.mt5.connected:
            success = bot.mt5.close_position(ticket)
            if success:
                return jsonify({'status': 'closed'})
            else:
                return jsonify({'error': 'Failed to close position'}), 500
        else:
            return jsonify({'error': 'Not connected to MT5'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance')
def get_performance():
    """Get performance statistics"""
    try:
        bot = init_bot()
        stats = bot.get_performance_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart_data')
def get_chart_data():
    """Get chart data for visualization"""
    try:
        bot = init_bot()
        if not bot.mt5.connected:
            return jsonify({'error': 'Not connected to MT5'}), 500
        
        # Get historical data
        df = bot.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 100)
        if df is None:
            return jsonify({'error': 'Failed to get chart data'}), 500
        
        # Create candlestick chart
        candlestick = go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=Config.SYMBOL
        )
        
        # Add moving averages
        if 'sma_20' in df.columns:
            sma20 = go.Scatter(
                x=df.index,
                y=df['sma_20'],
                name='SMA 20',
                line=dict(color='orange', width=1)
            )
        else:
            sma20 = None
            
        if 'sma_50' in df.columns:
            sma50 = go.Scatter(
                x=df.index,
                y=df['sma_50'],
                name='SMA 50',
                line=dict(color='blue', width=1)
            )
        else:
            sma50 = None
        
        # Prepare data
        data = [candlestick]
        if sma20:
            data.append(sma20)
        if sma50:
            data.append(sma50)
        
        # Create layout
        layout = go.Layout(
            title=f'{Config.SYMBOL} - {Config.TIMEFRAME}',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Price'),
            template='plotly_dark'
        )
        
        # Create figure
        fig = go.Figure(data=data, layout=layout)
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'chart': graphJSON})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai_analysis')
def get_ai_analysis():
    """Get AI analysis and predictions"""
    try:
        bot = init_bot()
        if not bot.mt5.connected:
            return jsonify({'error': 'Not connected to MT5'}), 500
        
        # Get historical data
        df = bot.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 500)
        if df is None:
            return jsonify({'error': 'Failed to get data for analysis'}), 500
        
        # Get AI prediction
        prediction = bot.ai.predict(df)
        if not prediction:
            return jsonify({'error': 'No AI prediction available'}), 500
        
        # Get market sentiment
        sentiment = bot.ai.get_market_sentiment(df)
        if not sentiment:
            return jsonify({'error': 'No sentiment analysis available'}), 500
        
        return jsonify({
            'prediction': prediction,
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Get or update bot settings"""
    if request.method == 'GET':
        return jsonify({
            'symbol': Config.SYMBOL,
            'timeframe': Config.TIMEFRAME,
            'lot_size': Config.LOT_SIZE,
            'max_positions': Config.MAX_POSITIONS,
            'stop_loss_pips': Config.STOP_LOSS_PIPS,
            'take_profit_pips': Config.TAKE_PROFIT_PIPS,
            'max_daily_loss': Config.MAX_DAILY_LOSS,
            'max_daily_profit': Config.MAX_DAILY_PROFIT
        })
    
    elif request.method == 'POST':
        # Update settings (in a real app, you'd save these to a config file)
        data = request.get_json()
        # Here you would update the configuration
        return jsonify({'status': 'Settings updated'})

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create templates directory and files
    import os
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create the main HTML template
    create_html_template()
    create_css_file()
    create_js_file()
    
    # Run the app
    app.run(host='0.0.0.0', port=Config.MOBILE_PORT, debug=Config.DEBUG)

def create_html_template():
    """Create the main HTML template"""
    html_content = '''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>בוט מסחר MT5 + AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-robot"></i> בוט מסחר MT5 + AI
            </span>
            <div class="d-flex">
                <button class="btn btn-outline-light me-2" onclick="toggleBot()">
                    <i class="fas fa-power-off"></i> <span id="botStatus">התחל</span>
                </button>
                <button class="btn btn-outline-light" onclick="refreshData()">
                    <i class="fas fa-sync-alt"></i> רענן
                </button>
            </div>
        </div>
    </nav>

    <div class="container-fluid mt-3">
        <!-- Status Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card bg-primary text-white">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-chart-line"></i> יתרה</h5>
                        <h3 id="balance">₪0.00</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-success text-white">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-coins"></i> רווח/הפסד</h5>
                        <h3 id="profit">₪0.00</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-info text-white">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-chart-bar"></i> פוזיציות פתוחות</h5>
                        <h3 id="positions">0</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-warning text-white">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-brain"></i> AI פעיל</h5>
                        <h3 id="aiStatus">כן</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Chart Section -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-candlestick"></i> גרף מחירים</h5>
                    </div>
                    <div class="card-body">
                        <div id="chart"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- AI Analysis and Positions -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-brain"></i> ניתוח AI</h5>
                    </div>
                    <div class="card-body">
                        <div id="aiAnalysis">
                            <p>טוען ניתוח...</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-list"></i> פוזיציות פתוחות</h5>
                    </div>
                    <div class="card-body">
                        <div id="positionsList">
                            <p>טוען פוזיציות...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_css_file():
    """Create CSS file"""
    css_content = '''body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: 1px solid rgba(0, 0, 0, 0.125);
    margin-bottom: 1rem;
}

.card-header {
    background-color: #fff;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    font-weight: 600;
}

.navbar-brand {
    font-weight: bold;
}

#chart {
    height: 400px;
}

.btn {
    border-radius: 0.375rem;
}

.table {
    margin-bottom: 0;
}

.badge {
    font-size: 0.75em;
}

/* Mobile optimizations */
@media (max-width: 768px) {
    .container-fluid {
        padding: 0.5rem;
    }
    
    .card-body {
        padding: 0.75rem;
    }
    
    #chart {
        height: 300px;
    }
    
    .btn {
        font-size: 0.875rem;
        padding: 0.375rem 0.75rem;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #212529;
        color: #fff;
    }
    
    .card {
        background-color: #343a40;
        color: #fff;
    }
    
    .card-header {
        background-color: #495057;
        color: #fff;
    }
}'''
    
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

def create_js_file():
    """Create JavaScript file"""
    js_content = '''let botRunning = false;
let refreshInterval;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    refreshData();
    startAutoRefresh();
});

// Toggle bot start/stop
async function toggleBot() {
    const button = document.querySelector('button[onclick="toggleBot()"]');
    const statusSpan = document.getElementById('botStatus');
    
    try {
        if (botRunning) {
            const response = await fetch('/api/stop', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'stopped') {
                botRunning = false;
                button.innerHTML = '<i class="fas fa-power-off"></i> התחל';
                button.className = 'btn btn-outline-success me-2';
                statusSpan.textContent = 'עצור';
            }
        } else {
            const response = await fetch('/api/start', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'started' || data.status === 'already_running') {
                botRunning = true;
                button.innerHTML = '<i class="fas fa-power-off"></i> עצור';
                button.className = 'btn btn-outline-danger me-2';
                statusSpan.textContent = 'פועל';
            }
        }
    } catch (error) {
        console.error('Error toggling bot:', error);
        alert('שגיאה בהפעלת/עצירת הבוט');
    }
}

// Refresh all data
async function refreshData() {
    try {
        await Promise.all([
            updateStatus(),
            updateChart(),
            updateAIAnalysis(),
            updatePositions()
        ]);
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

// Update status information
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.account) {
            document.getElementById('balance').textContent = '₪' + data.account.balance.toFixed(2);
            document.getElementById('profit').textContent = '₪' + (data.account.equity - data.account.balance).toFixed(2);
            document.getElementById('positions').textContent = data.positions ? data.positions.length : 0;
        }
        
        if (data.running) {
            botRunning = true;
            const button = document.querySelector('button[onclick="toggleBot()"]');
            button.innerHTML = '<i class="fas fa-power-off"></i> עצור';
            button.className = 'btn btn-outline-danger me-2';
            document.getElementById('botStatus').textContent = 'פועל';
        }
        
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Update chart
async function updateChart() {
    try {
        const response = await fetch('/api/chart_data');
        const data = await response.json();
        
        if (data.chart) {
            const chartData = JSON.parse(data.chart);
            Plotly.newPlot('chart', chartData.data, chartData.layout, {responsive: true});
        }
    } catch (error) {
        console.error('Error updating chart:', error);
    }
}

// Update AI analysis
async function updateAIAnalysis() {
    try {
        const response = await fetch('/api/ai_analysis');
        const data = await response.json();
        
        if (data.prediction && data.sentiment) {
            const analysisDiv = document.getElementById('aiAnalysis');
            
            const predictionText = data.prediction.prediction === 1 ? 'קנה' : 
                                 data.prediction.prediction === -1 ? 'מכור' : 'המתן';
            const confidence = (data.prediction.confidence * 100).toFixed(1);
            
            const sentimentText = data.sentiment.overall_sentiment;
            const sentimentClass = sentimentText === 'bullish' ? 'text-success' : 
                                 sentimentText === 'bearish' ? 'text-danger' : 'text-warning';
            
            analysisDiv.innerHTML = `
                <div class="row">
                    <div class="col-6">
                        <h6>חיזוי AI:</h6>
                        <span class="badge bg-${data.prediction.prediction === 1 ? 'success' : data.prediction.prediction === -1 ? 'danger' : 'secondary'} fs-6">
                            ${predictionText}
                        </span>
                        <p class="mt-2">ביטחון: ${confidence}%</p>
                    </div>
                    <div class="col-6">
                        <h6>מצב השוק:</h6>
                        <span class="badge bg-${sentimentText === 'bullish' ? 'success' : sentimentText === 'bearish' ? 'danger' : 'warning'} fs-6">
                            ${sentimentText}
                        </span>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-12">
                        <h6>פירוט ניתוח:</h6>
                        <ul class="list-unstyled">
                            <li>RSI: ${data.sentiment.rsi.value.toFixed(2)} (${data.sentiment.rsi.sentiment})</li>
                            <li>MACD: ${data.sentiment.macd.sentiment}</li>
                            <li>ממוצעים נעים: ${data.sentiment.moving_average.sentiment}</li>
                            <li>Bollinger Bands: ${data.sentiment.bollinger_bands.sentiment}</li>
                        </ul>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error updating AI analysis:', error);
    }
}

// Update positions list
async function updatePositions() {
    try {
        const response = await fetch('/api/positions');
        const positions = await response.json();
        
        const positionsDiv = document.getElementById('positionsList');
        
        if (positions.length === 0) {
            positionsDiv.innerHTML = '<p class="text-muted">אין פוזיציות פתוחות</p>';
            return;
        }
        
        let html = '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>סוג</th><th>נפח</th><th>רווח</th><th>פעולה</th></tr></thead><tbody>';
        
        positions.forEach(position => {
            const typeText = position.type === 0 ? 'קנייה' : 'מכירה';
            const typeClass = position.type === 0 ? 'text-success' : 'text-danger';
            const profitClass = position.profit > 0 ? 'text-success' : 'text-danger';
            
            html += `
                <tr>
                    <td><span class="${typeClass}">${typeText}</span></td>
                    <td>${position.volume}</td>
                    <td class="${profitClass}">₪${position.profit.toFixed(2)}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger" onclick="closePosition(${position.ticket})">
                            <i class="fas fa-times"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
        positionsDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Error updating positions:', error);
    }
}

// Close position
async function closePosition(ticket) {
    try {
        const response = await fetch(`/api/close_position/${ticket}`, { method: 'POST' });
        const data = await response.json();
        
        if (data.status === 'closed') {
            alert('הפוזיציה נסגרה בהצלחה');
            updatePositions();
        } else {
            alert('שגיאה בסגירת הפוזיציה: ' + data.error);
        }
    } catch (error) {
        console.error('Error closing position:', error);
        alert('שגיאה בסגירת הפוזיציה');
    }
}

// Start auto refresh
function startAutoRefresh() {
    refreshInterval = setInterval(refreshData, 30000); // Refresh every 30 seconds
}

// Stop auto refresh
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

// Handle page visibility change
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        stopAutoRefresh();
    } else {
        startAutoRefresh();
        refreshData();
    }
});'''
    
    with open('static/js/app.js', 'w', encoding='utf-8') as f:
        f.write(js_content)