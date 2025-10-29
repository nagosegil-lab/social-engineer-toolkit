# Social Engineering Toolkit (SET) - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core Modules](#core-modules)
3. [Attack Modules](#attack-modules)
4. [Utility Modules](#utility-modules)
5. [Configuration](#configuration)
6. [Examples](#examples)
7. [Error Handling](#error-handling)

## Overview

The Social Engineering Toolkit (SET) is a comprehensive framework for social engineering attacks and penetration testing. This documentation covers all public APIs, functions, and components available for developers and security professionals.

### Key Features
- **Spear Phishing Attacks**: Email-based social engineering
- **Web Attack Vectors**: Website cloning and credential harvesting
- **Infectious Media**: USB/CD/DVD payload delivery
- **Teensy HID Attacks**: Physical device-based attacks
- **PowerShell Attacks**: Windows PowerShell exploitation
- **Wireless Attacks**: Access point and DNS spoofing

## Core Modules

### 1. SET Core (`src.core.setcore`)

The core module provides essential functionality for the entire toolkit.

#### Key Functions

##### `check_os()`
```python
def check_os():
    """
    Detects the operating system.
    
    Returns:
        str: 'posix' for Unix-like systems, 'windows' for Windows
    """
```

##### `get_version()`
```python
def get_version():
    """
    Gets the current SET version.
    
    Returns:
        str: Version string (e.g., '7.7.9')
    """
```

##### `grab_ipaddress()`
```python
def grab_ipaddress():
    """
    Prompts user for IP address and validates it.
    
    Returns:
        str: Valid IP address or hostname
    """
```

##### `meta_path()`
```python
def meta_path():
    """
    Detects and returns Metasploit installation path.
    
    Returns:
        str: Path to Metasploit installation or False if not found
    """
```

##### `update_options(option)`
```python
def update_options(option):
    """
    Updates SET configuration options.
    
    Args:
        option (str): Configuration option in format 'KEY=VALUE'
    """
```

##### `check_options(option)`
```python
def check_options(option):
    """
    Retrieves configuration option value.
    
    Args:
        option (str): Option key to retrieve
        
    Returns:
        str: Option value or 0 if not found
    """
```

##### `print_status(message)`
```python
def print_status(message):
    """
    Prints a status message with green formatting.
    
    Args:
        message (str): Message to display
    """
```

##### `print_error(message)`
```python
def print_error(message):
    """
    Prints an error message with red formatting.
    
    Args:
        message (str): Error message to display
    """
```

##### `print_warning(message)`
```python
def print_warning(message):
    """
    Prints a warning message with yellow formatting.
    
    Args:
        message (str): Warning message to display
    """
```

##### `yesno_prompt(category, text)`
```python
def yesno_prompt(category, text):
    """
    Prompts user for yes/no response.
    
    Args:
        category (str): Category for prompt formatting
        text (str): Question text
        
    Returns:
        str: 'YES' or 'NO'
    """
```

##### `setprompt(category, text)`
```python
def setprompt(category, text):
    """
    Creates formatted SET prompt.
    
    Args:
        category (str): Category for prompt
        text (str): Additional text
        
    Returns:
        str: Formatted prompt string
    """
```

##### `create_menu(text, menu)`
```python
class create_menu:
    def __init__(self, text, menu):
        """
        Creates and displays a menu.
        
        Args:
            text (str): Menu description text
            menu (list): List of menu options
        """
```

##### `generate_random_string(low, high)`
```python
def generate_random_string(low, high):
    """
    Generates random alphanumeric string.
    
    Args:
        low (int): Minimum length
        high (int): Maximum length
        
    Returns:
        str: Random string
    """
```

##### `validate_ip(address)`
```python
def validate_ip(address):
    """
    Validates IPv4 address format.
    
    Args:
        address (str): IP address to validate
        
    Returns:
        bool: True if valid IPv4 address
    """
```

##### `detect_public_ip()`
```python
def detect_public_ip():
    """
    Auto-detects public IP address.
    
    Returns:
        str: Public IP address
    """
```

##### `metasploit_shellcode(payload, ipaddr, port)`
```python
def metasploit_shellcode(payload, ipaddr, port):
    """
    Generates Metasploit shellcode for specified payload.
    
    Args:
        payload (str): Metasploit payload name
        ipaddr (str): Target IP address
        port (str): Target port
        
    Returns:
        str: Shellcode string
    """
```

##### `encryptAES(secret, data)`
```python
def encryptAES(secret, data):
    """
    Encrypts data using AES encryption.
    
    Args:
        secret (str): Secret key
        data (str): Data to encrypt
        
    Returns:
        str: Encrypted data
    """
```

### 2. Web Server (`src.core.webserver`)

Handles HTTP server functionality for web attacks.

#### Key Classes

##### `StoppableHttpRequestHandler`
```python
class StoppableHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP request handler with QUIT stopping capability.
    """
    
    def do_GET(self):
        """Handle GET requests"""
        
    def do_POST(self):
        """Handle POST requests"""
        
    def do_QUIT(self):
        """Stop the server"""
```

##### `StoppableHttpServer`
```python
class StoppableHttpServer(http.server.HTTPServer):
    """
    HTTP server that can be stopped via QUIT request.
    """
    
    def serve_forever(self):
        """Handle requests until stopped"""
```

#### Key Functions

##### `start_server(web_port, path)`
```python
def start_server(web_port, path):
    """
    Starts HTTP server on specified port and path.
    
    Args:
        web_port (int): Port to listen on
        path (str): Directory to serve
    """
```

##### `stop_server(web_port)`
```python
def stop_server(web_port):
    """
    Stops HTTP server via QUIT request.
    
    Args:
        web_port (int): Port of server to stop
    """
```

### 3. Module Handler (`src.core.module_handler`)

Manages third-party modules.

#### Key Functions

##### Module Loading
```python
# Automatically loads and executes modules from modules/ directory
# Modules must have MAIN="Description" in their header
# Modules must implement main() function
```

## Attack Modules

### 1. Credential Harvester (`src.webattack.harvester.harvester`)

Captures credentials from cloned websites.

#### Key Classes

##### `SETHandler`
```python
class SETHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP handler for credential harvesting.
    """
    
    def do_GET(self):
        """Serve cloned website"""
        
    def do_POST(self):
        """Capture and log credentials"""
```

#### Key Functions

##### `run()`
```python
def run():
    """
    Starts the credential harvester server.
    """
```

### 2. Website Cloner (`src.webattack.web_clone.cloner`)

Clones websites for social engineering attacks.

#### Key Functions

##### Website Cloning
```python
# Automatically clones websites using wget or urllib
# Injects malicious content (Java applets, iframes, etc.)
# Handles different attack vectors (Java, Browser, Harvester, etc.)
```

### 3. SMTP Client (`src.phishing.smtp.client.smtp_client`)

Handles email-based attacks.

#### Key Functions

##### `mail(to, subject, text, attach, prioflag1, prioflag2)`
```python
def mail(to, subject, text, attach, prioflag1, prioflag2):
    """
    Sends email with attachment.
    
    Args:
        to (str): Recipient email
        subject (str): Email subject
        text (str): Email body
        attach (str): Path to attachment
        prioflag1 (str): Priority flag 1
        prioflag2 (str): Priority flag 2
    """
```

### 4. Teensy HID (`src.teensy.teensy`)

Generates Teensy HID attack payloads.

#### Key Functions

##### `writefile(filename, now)`
```python
def writefile(filename, now):
    """
    Writes Teensy .ino file with IP address substitution.
    
    Args:
        filename (str): Source .ino file
        now (datetime): Timestamp for output file
    """
```

### 5. PowerShell Attacks (`src.powershell.powershell`)

Handles PowerShell-based attacks.

#### Key Functions

##### PowerShell Payload Generation
```python
# Generates various PowerShell payloads:
# - Alphanumeric shellcode injection
# - Reverse shell
# - Bind shell
# - SAM database dump
```

## Utility Modules

### 1. Dictionaries (`src.core.dictionaries`)

Provides mapping functions for user input to Metasploit values.

#### Key Functions

##### `ms_payload(payload)`
```python
def ms_payload(payload):
    """
    Maps payload selection to Metasploit payload name.
    
    Args:
        payload (str): User selection (1-9)
        
    Returns:
        str: Metasploit payload name
    """
```

##### `ms_module(exploit)`
```python
def ms_module(exploit):
    """
    Maps exploit selection to Metasploit module name.
    
    Args:
        exploit (str): User selection (1-46)
        
    Returns:
        str: Metasploit module name
    """
```

##### `ms_attacks(exploit)`
```python
def ms_attacks(exploit):
    """
    Maps file format attack selection to Metasploit module.
    
    Args:
        exploit (str): User selection (1-22)
        
    Returns:
        str: Metasploit module name
    """
```

### 2. QR Code Generator (`src.qrcode.qrgenerator`)

Generates QR codes for attacks.

#### Key Functions

##### `gen_qrcode(url)`
```python
def gen_qrcode(url):
    """
    Generates QR code for given URL.
    
    Args:
        url (str): URL to encode in QR code
    """
```

### 3. Menu Text (`src.core.menu.text`)

Contains all menu text and descriptions.

#### Key Variables
- `main_text`: Main menu description
- `main_menu`: Main menu options
- `webattack_text`: Web attack description
- `teensy_text`: Teensy attack description
- `powershell_text`: PowerShell attack description

## Configuration

### Configuration File Location
- **Linux/Unix**: `/etc/setoolkit/set.config`
- **Windows**: `src/program_junk/`

### Key Configuration Options

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

## Examples

### 1. Basic Website Cloning

```python
from src.core.setcore import *
from src.webattack.web_clone.cloner import *

# Set up configuration
update_options("IPADDR=192.168.1.100")
update_options("ATTACK_VECTOR=java")

# Clone website
site_cloner("https://example.com", "/tmp/cloned_site", "java")
```

### 2. Credential Harvester

```python
from src.webattack.harvester.harvester import *

# Start harvester
run()
```

### 3. Email Attack

```python
from src.phishing.smtp.client.smtp_client import *

# Send malicious email
mail("victim@example.com", "Important Update", 
     "Please see attached file", "/path/to/payload.pdf", "", "")
```

### 4. PowerShell Attack

```python
from src.powershell.powershell import *

# Generate PowerShell payload
# (Interactive menu will be displayed)
```

### 5. Teensy HID Attack

```python
from src.teensy.teensy import *

# Generate Teensy .ino file
writefile("powershell_down.ino", datetime.now())
```

## Error Handling

### Common Error Types

1. **Configuration Errors**: Missing or invalid configuration
2. **Network Errors**: Connection issues, port conflicts
3. **File Errors**: Missing files, permission issues
4. **Metasploit Errors**: Missing Metasploit, invalid payloads

### Error Handling Functions

```python
def log(error):
    """
    Logs errors to SET log file.
    
    Args:
        error (str): Error message to log
    """
```

```python
def return_continue():
    """
    Prompts user to press return to continue.
    """
```

### Debugging

Enable debug mode by setting `DEBUG_LEVEL` in `setcore.py`:
- `0`: Debugging OFF
- `1`: Debug imports only
- `2`: Debug imports with pause
- `3`: Imports, info messages
- `4`: Imports, info messages with pause
- `5`: Imports, info messages, menus
- `6`: Imports, info messages, menus with pause

## Security Considerations

⚠️ **IMPORTANT**: This toolkit is designed for authorized penetration testing and security research only. Users must:

1. Obtain explicit written permission before testing
2. Comply with all applicable laws and regulations
3. Use only on systems they own or have explicit permission to test
4. Follow responsible disclosure practices

## Support and Contributing

- **Documentation**: This API documentation
- **Issues**: Report bugs via GitHub issues
- **Contributing**: Follow the contribution guidelines in the repository
- **License**: See LICENSE file for usage terms

## Version Information

- **Current Version**: 7.7.9
- **Python Compatibility**: 2.7+ and 3.x
- **Dependencies**: See requirements.txt
- **Platform Support**: Linux, macOS (experimental)