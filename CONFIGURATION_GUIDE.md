# Social Engineering Toolkit (SET) - Configuration Guide

## Table of Contents
1. [Configuration Overview](#configuration-overview)
2. [Configuration Files](#configuration-files)
3. [Environment Variables](#environment-variables)
4. [Attack-Specific Configuration](#attack-specific-configuration)
5. [Advanced Configuration](#advanced-configuration)
6. [Troubleshooting Configuration](#troubleshooting-configuration)

## Configuration Overview

The Social Engineering Toolkit (SET) uses multiple configuration files and environment variables to control its behavior. Understanding these configurations is essential for effective use of the toolkit.

### Configuration Hierarchy
1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration files**
4. **Default values** (lowest priority)

## Configuration Files

### 1. Main Configuration File

**Location**: `/etc/setoolkit/set.config`

**Purpose**: Primary configuration file containing all SET settings.

**Format**: Key-value pairs separated by `=`

**Example**:
```bash
# Metasploit Configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
METASPLOIT_MODE=ON
METASPLOIT_DATABASE=postgresql

# Web Server Configuration
WEB_PORT=80
WEBATTACK_SSL=OFF
APACHE_SERVER=OFF
APACHE_DIRECTORY=/var/www/html

# Email Configuration
EMAIL_PROVIDER=gmail
SENDMAIL=OFF

# Attack Configuration
AUTO_DETECT=ON
HARVESTER_REDIRECT=OFF
POWERSHELL_INJECTION=ON
```

### 2. Options File

**Location**: `/root/.set/set.options`

**Purpose**: User-specific options and preferences.

**Format**: Key-value pairs

**Example**:
```bash
# User Preferences
DEFAULT_ATTACK_VECTOR=web
DEFAULT_PAYLOAD=windows/meterpreter/reverse_tcp
DEFAULT_ENCODER=shikata_ga_nai
DEFAULT_ITERATIONS=1

# Display Options
SHOW_BANNER=ON
COLOR_OUTPUT=ON
VERBOSE_MODE=OFF
```

### 3. Baseline Configuration

**Location**: `src/core/config.baseline`

**Purpose**: Default configuration template.

**Format**: Key-value pairs

**Example**:
```bash
# Default Configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
WEB_PORT=80
EMAIL_PROVIDER=gmail
AUTO_DETECT=ON
```

## Environment Variables

### 1. SET Environment Variables

**SET_HOME**: SET installation directory
```bash
export SET_HOME=/usr/local/share/setoolkit
```

**SET_CONFIG**: Configuration file path
```bash
export SET_CONFIG=/etc/setoolkit/set.config
```

**SET_LOGS**: Log directory path
```bash
export SET_LOGS=/root/.set/logs
```

**SET_REPORTS**: Reports directory path
```bash
export SET_REPORTS=/root/.set/reports
```

### 2. Metasploit Environment Variables

**MSF_DATABASE_CONFIG**: Metasploit database configuration
```bash
export MSF_DATABASE_CONFIG=/usr/share/metasploit-framework/config/database.yml
```

**MSF_LOGS**: Metasploit log directory
```bash
export MSF_LOGS=/var/log/metasploit
```

### 3. Python Environment Variables

**PYTHONPATH**: Python module search path
```bash
export PYTHONPATH=$PYTHONPATH:/usr/local/share/setoolkit/src
```

**PYTHONIOENCODING**: Python I/O encoding
```bash
export PYTHONIOENCODING=utf-8
```

## Attack-Specific Configuration

### 1. Web Attack Configuration

**Web Server Settings**:
```bash
# Web server port
WEB_PORT=80

# SSL configuration
WEBATTACK_SSL=OFF
SSL_CERTIFICATE=/etc/setoolkit/ssl.crt
SSL_PRIVATE_KEY=/etc/setoolkit/ssl.key

# Apache integration
APACHE_SERVER=OFF
APACHE_DIRECTORY=/var/www/html
APACHE_CONFIG=/etc/apache2/sites-available/set.conf
```

**Harvester Settings**:
```bash
# Credential harvester
HARVESTER_REDIRECT=OFF
HARVESTER_LOG=/root/.set/logs/harvester.log
HARVESTER_TEMPLATE=default

# Website cloning
CLONE_METHOD=wget
CLONE_DEPTH=1
CLONE_TIMEOUT=30
```

**Browser Exploit Settings**:
```bash
# Java applet
JAVA_APPLET_ENABLED=ON
JAVA_APPLET_PATH=/usr/local/share/setoolkit/src/webattack/java_applet/

# Browser exploits
BROWSER_EXPLOIT_ENABLED=ON
BROWSER_EXPLOIT_PATH=/usr/local/share/setoolkit/src/webattack/browser_exploits/
```

### 2. Email Attack Configuration

**SMTP Settings**:
```bash
# Email provider
EMAIL_PROVIDER=gmail
SENDMAIL=OFF

# Gmail configuration
GMAIL_SMTP=smtp.gmail.com
GMAIL_PORT=587
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password

# Custom SMTP
CUSTOM_SMTP=mail.company.com
CUSTOM_PORT=25
CUSTOM_USER=username
CUSTOM_PASS=password
CUSTOM_TLS=ON
```

**Email Templates**:
```bash
# Template directory
EMAIL_TEMPLATE_DIR=/usr/local/share/setoolkit/src/templates/

# Default template
DEFAULT_EMAIL_TEMPLATE=securityupdates.template

# Email formatting
EMAIL_HTML=ON
EMAIL_ATTACHMENTS=ON
EMAIL_PRIORITY=normal
```

### 3. Teensy Attack Configuration

**Teensy Settings**:
```bash
# Teensy path
TEENSY_PATH=/usr/local/share/setoolkit/src/teensy/

# Arduino IDE
ARDUINO_IDE_PATH=/usr/local/bin/arduino
ARDUINO_BOARD=teensy31

# Payload settings
TEENSY_PAYLOAD_TYPE=powershell
TEENSY_DELAY=1000
TEENSY_REPEAT=1
```

**HID Attack Settings**:
```bash
# HID configuration
HID_LAYOUT=us
HID_DELAY=50
HID_REPEAT_DELAY=100

# Payload obfuscation
HID_OBFUSCATE=ON
HID_RANDOMIZE=ON
```

### 4. PowerShell Attack Configuration

**PowerShell Settings**:
```bash
# PowerShell path
POWERSHELL_PATH=powershell.exe

# Execution policy
POWERSHELL_EXECUTION_POLICY=bypass

# Payload settings
POWERSHELL_PAYLOAD_TYPE=alphanumeric
POWERSHELL_ENCODING=base64
POWERSHELL_OBFUSCATE=ON
```

**Shellcode Settings**:
```bash
# Shellcode generation
SHELLCODE_GENERATOR=msfvenom
SHELLCODE_ENCODER=shikata_ga_nai
SHELLCODE_ITERATIONS=1
SHELLCODE_BADCHARS=\x00\x0a\x0d
```

### 5. Wireless Attack Configuration

**Access Point Settings**:
```bash
# Hostapd configuration
HOSTAPD_CONFIG=/etc/hostapd/hostapd.conf
HOSTAPD_INTERFACE=wlan0
HOSTAPD_SSID=Free_WiFi
HOSTAPD_CHANNEL=6
HOSTAPD_SECURITY=open
```

**DNS Spoofing Settings**:
```bash
# DNS configuration
DNS_SPOOF_INTERFACE=wlan0
DNS_SPOOF_DOMAIN=*.google.com
DNS_SPOOF_REDIRECT=192.168.1.100
DNS_SPOOF_LOG=/root/.set/logs/dns_spoof.log
```

### 6. Infectious Media Configuration

**File Format Settings**:
```bash
# File format exploits
PDF_EXPLOIT=exploit/windows/fileformat/adobe_pdf_embedded_exe
DOC_EXPLOIT=exploit/windows/fileformat/ms10_087_rtf_pfragments_bof
RTF_EXPLOIT=exploit/windows/fileformat/ms10_087_rtf_pfragments_bof
MOV_EXPLOIT=exploit/windows/fileformat/adobe_flash_avm2
```

**Payload Settings**:
```bash
# Payload configuration
PAYLOAD_TYPE=windows/meterpreter/reverse_tcp
PAYLOAD_LHOST=192.168.1.100
PAYLOAD_LPORT=4444
PAYLOAD_ENCODER=shikata_ga_nai
PAYLOAD_ITERATIONS=1
```

## Advanced Configuration

### 1. Custom Module Configuration

**Module Settings**:
```bash
# Module directory
MODULE_DIR=/usr/local/share/setoolkit/modules/

# Module loading
AUTO_LOAD_MODULES=ON
MODULE_DEBUG=OFF
MODULE_TIMEOUT=30
```

**Custom Module Example**:
```python
# Custom module configuration
CUSTOM_MODULE_NAME=MyAttack
CUSTOM_MODULE_PATH=/path/to/my_attack.py
CUSTOM_MODULE_DESCRIPTION=My custom attack module
CUSTOM_MODULE_AUTHOR=Security Researcher
CUSTOM_MODULE_VERSION=1.0
```

### 2. Logging Configuration

**Log Settings**:
```bash
# Log configuration
LOG_LEVEL=INFO
LOG_FILE=/root/.set/logs/set_logfile.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Debug Settings**:
```bash
# Debug configuration
DEBUG_LEVEL=0
DEBUG_FILE=/root/.set/logs/debug.log
DEBUG_CONSOLE=OFF
DEBUG_NETWORK=OFF
```

### 3. Network Configuration

**Network Settings**:
```bash
# Network configuration
AUTO_DETECT=ON
PUBLIC_IP_API=http://ipinfo.io/ip
NETWORK_INTERFACE=eth0
NETWORK_TIMEOUT=30
```

**Proxy Settings**:
```bash
# Proxy configuration
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=https://proxy.company.com:8080
NO_PROXY=localhost,127.0.0.1
```

### 4. Security Configuration

**Security Settings**:
```bash
# Security configuration
ENCRYPTION_KEY=your-secret-key
SSL_VERIFY=ON
CERTIFICATE_VALIDATION=ON
SECURE_MODE=ON
```

**Access Control**:
```bash
# Access control
ALLOWED_IPS=192.168.1.0/24,10.0.0.0/8
BLOCKED_IPS=192.168.1.100,10.0.0.100
ACCESS_LOG=/root/.set/logs/access.log
```

## Troubleshooting Configuration

### 1. Configuration Validation

**Check Configuration**:
```bash
# Validate configuration file
python -c "
import sys
sys.path.append('/usr/local/share/setoolkit/src')
from core.setcore import check_config
check_config()
"
```

**Test Configuration**:
```bash
# Test configuration
setoolkit --test-config
```

### 2. Common Configuration Issues

**Issue**: Configuration file not found
```bash
# Error: Configuration file not found
# Solution: Create configuration file
sudo mkdir -p /etc/setoolkit
sudo cp /usr/local/share/setoolkit/src/core/config.baseline /etc/setoolkit/set.config
```

**Issue**: Permission denied
```bash
# Error: Permission denied
# Solution: Fix permissions
sudo chmod 644 /etc/setoolkit/set.config
sudo chown root:root /etc/setoolkit/set.config
```

**Issue**: Invalid configuration value
```bash
# Error: Invalid configuration value
# Solution: Check configuration format
grep -v "^#" /etc/setoolkit/set.config | grep "="
```

### 3. Configuration Backup and Restore

**Backup Configuration**:
```bash
# Backup configuration
cp /etc/setoolkit/set.config /etc/setoolkit/set.config.backup
cp /root/.set/set.options /root/.set/set.options.backup
```

**Restore Configuration**:
```bash
# Restore configuration
cp /etc/setoolkit/set.config.backup /etc/setoolkit/set.config
cp /root/.set/set.options.backup /root/.set/set.options
```

### 4. Configuration Migration

**Migrate Old Configuration**:
```bash
# Migrate from old version
python /usr/local/share/setoolkit/src/core/update_config.py
```

**Update Configuration**:
```bash
# Update configuration
setoolkit --update-config
```

## Configuration Examples

### 1. Basic Configuration

**Minimal Configuration**:
```bash
# Basic SET configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
WEB_PORT=80
EMAIL_PROVIDER=gmail
AUTO_DETECT=ON
```

### 2. Advanced Configuration

**Advanced Configuration**:
```bash
# Advanced SET configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
METASPLOIT_MODE=ON
METASPLOIT_DATABASE=postgresql
WEB_PORT=80
WEBATTACK_SSL=ON
SSL_CERTIFICATE=/etc/setoolkit/ssl.crt
SSL_PRIVATE_KEY=/etc/setoolkit/ssl.key
APACHE_SERVER=ON
APACHE_DIRECTORY=/var/www/html
EMAIL_PROVIDER=gmail
GMAIL_SMTP=smtp.gmail.com
GMAIL_PORT=587
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password
AUTO_DETECT=ON
HARVESTER_REDIRECT=OFF
POWERSHELL_INJECTION=ON
DEBUG_LEVEL=3
LOG_LEVEL=INFO
LOG_FILE=/root/.set/logs/set_logfile.log
```

### 3. Corporate Configuration

**Corporate Environment**:
```bash
# Corporate SET configuration
METASPLOIT_PATH=/opt/metasploit-framework/
METASPLOIT_MODE=ON
METASPLOIT_DATABASE=postgresql
WEB_PORT=8080
WEBATTACK_SSL=ON
SSL_CERTIFICATE=/etc/ssl/certs/company.crt
SSL_PRIVATE_KEY=/etc/ssl/private/company.key
APACHE_SERVER=ON
APACHE_DIRECTORY=/var/www/html
EMAIL_PROVIDER=custom
CUSTOM_SMTP=mail.company.com
CUSTOM_PORT=25
CUSTOM_USER=security@company.com
CUSTOM_PASS=password
CUSTOM_TLS=ON
AUTO_DETECT=OFF
PUBLIC_IP=203.0.113.1
HARVESTER_REDIRECT=ON
POWERSHELL_INJECTION=ON
DEBUG_LEVEL=1
LOG_LEVEL=WARNING
LOG_FILE=/var/log/setoolkit/set.log
ALLOWED_IPS=192.168.0.0/16,10.0.0.0/8
BLOCKED_IPS=192.168.1.100,10.0.0.100
```

### 4. Testing Configuration

**Testing Environment**:
```bash
# Testing SET configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
METASPLOIT_MODE=ON
WEB_PORT=8080
WEBATTACK_SSL=OFF
EMAIL_PROVIDER=gmail
GMAIL_SMTP=smtp.gmail.com
GMAIL_PORT=587
GMAIL_USER=test@gmail.com
GMAIL_PASS=test-password
AUTO_DETECT=ON
HARVESTER_REDIRECT=OFF
POWERSHELL_INJECTION=ON
DEBUG_LEVEL=6
LOG_LEVEL=DEBUG
LOG_FILE=/tmp/set_test.log
```

## Configuration Management

### 1. Configuration Templates

**Create Configuration Template**:
```bash
# Create configuration template
cat > /etc/setoolkit/set.config.template << EOF
# SET Configuration Template
METASPLOIT_PATH=/usr/share/metasploit-framework/
WEB_PORT=80
EMAIL_PROVIDER=gmail
AUTO_DETECT=ON
EOF
```

**Use Configuration Template**:
```bash
# Use configuration template
cp /etc/setoolkit/set.config.template /etc/setoolkit/set.config
```

### 2. Configuration Validation

**Validate Configuration**:
```bash
# Validate configuration
python -c "
import sys
sys.path.append('/usr/local/share/setoolkit/src')
from core.setcore import check_config
if check_config():
    print('Configuration is valid')
else:
    print('Configuration has errors')
"
```

### 3. Configuration Monitoring

**Monitor Configuration Changes**:
```bash
# Monitor configuration file
inotifywait -m /etc/setoolkit/set.config
```

**Log Configuration Changes**:
```bash
# Log configuration changes
echo "$(date): Configuration changed" >> /var/log/setoolkit/config.log
```

---

This configuration guide provides comprehensive information about configuring the Social Engineering Toolkit for various environments and use cases. Always ensure you have proper authorization before conducting any security tests.