"""
Notification Manager for Trading Bot
"""
import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
import json

from ..config.settings import NOTIFICATION_CONFIG

logger = logging.getLogger(__name__)

class NotificationManager:
    """
    Manage notifications via multiple channels (Telegram, Email, etc.)
    """
    
    def __init__(self):
        self.telegram_token = NOTIFICATION_CONFIG.get('telegram_token', '')
        self.telegram_chat_id = NOTIFICATION_CONFIG.get('telegram_chat_id', '')
        self.email_config = {
            'smtp_server': NOTIFICATION_CONFIG.get('email_smtp_server', ''),
            'port': NOTIFICATION_CONFIG.get('email_port', 587),
            'username': NOTIFICATION_CONFIG.get('email_username', ''),
            'password': NOTIFICATION_CONFIG.get('email_password', ''),
            'to': NOTIFICATION_CONFIG.get('email_to', '')
        }
        
        # Message queue for batch sending
        self.message_queue = []
        self.last_sent_time = {}
        self.rate_limit_seconds = 60  # Minimum time between similar messages
        
    async def send_message(self, message: str, priority: str = 'normal', 
                          channels: List[str] = None) -> bool:
        """Send notification message through specified channels"""
        try:
            if not message:
                return False
                
            # Default channels if none specified
            if channels is None:
                channels = ['telegram', 'email']
                
            # Check rate limiting
            if not self._check_rate_limit(message):
                logger.debug(f"Message rate limited: {message[:50]}...")
                return False
                
            # Format message with timestamp
            formatted_message = self._format_message(message, priority)
            
            # Send through each channel
            success = False
            
            if 'telegram' in channels:
                telegram_success = await self._send_telegram(formatted_message)
                success = success or telegram_success
                
            if 'email' in channels and priority in ['high', 'critical']:
                email_success = await self._send_email(formatted_message, priority)
                success = success or email_success
                
            # Update rate limiting
            self._update_rate_limit(message)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False
            
    async def _send_telegram(self, message: str) -> bool:
        """Send message via Telegram"""
        try:
            if not self.telegram_token or not self.telegram_chat_id:
                logger.debug("Telegram not configured")
                return False
                
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            # Split long messages
            max_length = 4096  # Telegram limit
            if len(message) > max_length:
                messages = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            else:
                messages = [message]
                
            async with aiohttp.ClientSession() as session:
                for msg in messages:
                    payload = {
                        'chat_id': self.telegram_chat_id,
                        'text': msg,
                        'parse_mode': 'HTML'
                    }
                    
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            logger.debug("Telegram message sent successfully")
                        else:
                            logger.error(f"Telegram API error: {response.status}")
                            return False
                            
            return True
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
            
    async def _send_email(self, message: str, priority: str) -> bool:
        """Send message via Email"""
        try:
            if not all([self.email_config['smtp_server'], 
                       self.email_config['username'],
                       self.email_config['password'],
                       self.email_config['to']]):
                logger.debug("Email not configured")
                return False
                
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['username']
            msg['To'] = self.email_config['to']
            msg['Subject'] = f"Trading Bot Alert - {priority.upper()}"
            
            # Add body
            body = f"""
Trading Bot Notification
========================

Priority: {priority.upper()}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message}

---
Automated Trading Bot System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['username'], self.email_config['to'], text)
            server.quit()
            
            logger.debug("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
            
    def _format_message(self, message: str, priority: str) -> str:
        """Format message with priority and timestamp"""
        try:
            # Priority emoji
            priority_emoji = {
                'low': '🔵',
                'normal': '🟢',
                'high': '🟡',
                'critical': '🔴'
            }
            
            emoji = priority_emoji.get(priority, '🟢')
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            formatted = f"{emoji} <b>[{timestamp}]</b> {message}"
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return message
            
    def _check_rate_limit(self, message: str) -> bool:
        """Check if message should be rate limited"""
        try:
            # Create a hash of the message for rate limiting
            message_hash = hash(message[:100])  # Use first 100 chars
            
            current_time = datetime.now()
            
            if message_hash in self.last_sent_time:
                time_diff = (current_time - self.last_sent_time[message_hash]).total_seconds()
                if time_diff < self.rate_limit_seconds:
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True
            
    def _update_rate_limit(self, message: str):
        """Update rate limit tracking"""
        try:
            message_hash = hash(message[:100])
            self.last_sent_time[message_hash] = datetime.now()
            
            # Clean old entries (keep last 100)
            if len(self.last_sent_time) > 100:
                oldest_keys = sorted(self.last_sent_time.keys(), 
                                   key=lambda k: self.last_sent_time[k])[:50]
                for key in oldest_keys:
                    del self.last_sent_time[key]
                    
        except Exception as e:
            logger.error(f"Error updating rate limit: {e}")
            
    async def send_trade_alert(self, trade_info: Dict) -> bool:
        """Send trade-specific alert"""
        try:
            symbol = trade_info.get('symbol', 'Unknown')
            action = trade_info.get('action', 'Unknown')
            volume = trade_info.get('volume', 0)
            entry_price = trade_info.get('entry_price', 0)
            confidence = trade_info.get('confidence', 0)
            
            message = f"""
📊 <b>New Trade Signal</b>

🔸 Symbol: {symbol}
🔸 Action: {action.upper()}
🔸 Volume: {volume}
🔸 Entry: {entry_price:.5f}
🔸 Confidence: {confidence:.1%}
"""
            
            return await self.send_message(message, priority='normal')
            
        except Exception as e:
            logger.error(f"Error sending trade alert: {e}")
            return False
            
    async def send_position_update(self, position_info: Dict) -> bool:
        """Send position update notification"""
        try:
            symbol = position_info.get('symbol', 'Unknown')
            status = position_info.get('status', 'Unknown')
            pnl = position_info.get('pnl', 0)
            
            emoji = '✅' if pnl >= 0 else '❌'
            
            message = f"""
{emoji} <b>Position Update</b>

🔸 Symbol: {symbol}
🔸 Status: {status}
🔸 P&L: {pnl:.2f}
"""
            
            priority = 'high' if abs(pnl) > 100 else 'normal'
            
            return await self.send_message(message, priority=priority)
            
        except Exception as e:
            logger.error(f"Error sending position update: {e}")
            return False
            
    async def send_system_alert(self, alert_type: str, details: str) -> bool:
        """Send system alert notification"""
        try:
            alert_emojis = {
                'error': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️',
                'success': '✅'
            }
            
            emoji = alert_emojis.get(alert_type, 'ℹ️')
            
            message = f"""
{emoji} <b>System Alert</b>

Type: {alert_type.upper()}
Details: {details}
"""
            
            priority = 'critical' if alert_type == 'error' else 'high'
            
            return await self.send_message(message, priority=priority)
            
        except Exception as e:
            logger.error(f"Error sending system alert: {e}")
            return False
            
    async def send_daily_summary(self, summary: Dict) -> bool:
        """Send daily trading summary"""
        try:
            trades_count = summary.get('trades_count', 0)
            total_pnl = summary.get('total_pnl', 0)
            win_rate = summary.get('win_rate', 0)
            account_balance = summary.get('account_balance', 0)
            
            emoji = '📈' if total_pnl >= 0 else '📉'
            
            message = f"""
{emoji} <b>Daily Trading Summary</b>

📊 Trades: {trades_count}
💰 P&L: {total_pnl:.2f}
🎯 Win Rate: {win_rate:.1%}
💳 Balance: {account_balance:.2f}

---
{datetime.now().strftime('%Y-%m-%d')}
"""
            
            return await self.send_message(message, priority='normal')
            
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
            return False
            
    async def test_notifications(self) -> Dict[str, bool]:
        """Test all notification channels"""
        try:
            test_message = f"🧪 Test notification from Trading Bot - {datetime.now().strftime('%H:%M:%S')}"
            
            results = {}
            
            # Test Telegram
            if self.telegram_token and self.telegram_chat_id:
                results['telegram'] = await self._send_telegram(test_message)
            else:
                results['telegram'] = False
                
            # Test Email
            if all([self.email_config['smtp_server'], 
                   self.email_config['username'],
                   self.email_config['password'],
                   self.email_config['to']]):
                results['email'] = await self._send_email(test_message, 'normal')
            else:
                results['email'] = False
                
            return results
            
        except Exception as e:
            logger.error(f"Error testing notifications: {e}")
            return {'telegram': False, 'email': False}
            
    def update_config(self, new_config: Dict):
        """Update notification configuration"""
        try:
            if 'telegram_token' in new_config:
                self.telegram_token = new_config['telegram_token']
                
            if 'telegram_chat_id' in new_config:
                self.telegram_chat_id = new_config['telegram_chat_id']
                
            if 'email' in new_config:
                self.email_config.update(new_config['email'])
                
            logger.info("Notification config updated")
            
        except Exception as e:
            logger.error(f"Error updating notification config: {e}")