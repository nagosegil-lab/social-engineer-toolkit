# Social-Engineer Toolkit (SET) - Comprehensive API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core API Reference](#core-api-reference)
3. [Attack Modules](#attack-modules)
4. [Web Attack Vectors](#web-attack-vectors)
5. [Phishing Modules](#phishing-modules)
6. [Payload Generation](#payload-generation)
7. [Configuration Management](#configuration-management)
8. [Third-Party Modules](#third-party-modules)
9. [Usage Examples](#usage-examples)
10. [Installation and Setup](#installation-and-setup)

## Overview

The Social-Engineer Toolkit (SET) is an open-source penetration testing framework designed for social engineering attacks. It provides a comprehensive suite of tools for creating believable attacks quickly and efficiently.

### Key Features

- **Spear-phishing Attack Vectors**: Mass email attacks with malicious payloads
- **Website Attack Vectors**: Java applets, browser exploits, credential harvesting
- **Infectious Media Generator**: USB/CD autorun attacks
- **Payload Generation**: Custom payload creation and listeners
- **Mass Mailer**: Large-scale email campaigns
- **Wireless Attacks**: Access point attacks
- **Third-Party Module Support**: Extensible architecture

### Supported Platforms

- Linux (Primary)
- Mac OS X (Experimental)
- Windows (Limited functionality)

## Core API Reference

### Core Module (`src/core/setcore.py`)

The core module provides essential functionality for SET operations.

#### System Functions

```python
def check_os()
```
**Description**: Detects the operating system
**Returns**: `str` - "posix" for Unix-like systems, "windows" for Windows
**Usage**: Used throughout SET to determine OS-specific behavior

```python
def definepath()
```
**Description**: Determines the main SET installation path
**Returns**: `str` - Path to SET installation directory
**Usage**: Sets up proper paths for module imports and file operations

#### User Interface Functions

```python
def setprompt(category, text)
```
**Description**: Creates standardized prompts for user input
**Parameters**:
- `category`: List or string indicating menu category
- `text`: String for prompt text
**Returns**: `str` - Formatted prompt string
**Example**:
```python
prompt = setprompt(["1"], "Enter your choice")
# Returns: "set:1> Enter your choice: "
```

```python
def yesno_prompt(category, text)
```
**Description**: Creates yes/no prompts with validation
**Parameters**:
- `category`: Menu category identifier
- `text`: Prompt text
**Returns**: `str` - "YES" or "NO"
**Example**:
```python
response = yesno_prompt("0", "Continue with attack [yes|no]")
```

#### Output Functions

```python
def print_status(message)
```
**Description**: Prints status messages with formatting
**Parameters**: `message` (str) - Status message to display

```python
def print_info(message)
```
**Description**: Prints informational messages
**Parameters**: `message` (str) - Information to display

```python
def print_warning(message)
```
**Description**: Prints warning messages in yellow
**Parameters**: `message` (str) - Warning message

```python
def print_error(message)
```
**Description**: Prints error messages in red
**Parameters**: `message` (str) - Error message

#### Network Functions

```python
def detect_public_ip()
```
**Description**: Detects the public IP address of the system
**Returns**: `str` - Public IP address
**Usage**: Used for configuring reverse connections and web servers

```python
def validate_ip(address)
```
**Description**: Validates IP address format
**Parameters**: `address` (str) - IP address to validate
**Returns**: `bool` - True if valid IP address

```python
def is_valid_ipv4(ip)
```
**Description**: Validates IPv4 address format
**Parameters**: `ip` (str) - IPv4 address to validate
**Returns**: `bool` - True if valid IPv4

```python
def is_valid_ipv6(ip)
```
**Description**: Validates IPv6 address format
**Parameters**: `ip` (str) - IPv6 address to validate
**Returns**: `bool` - True if valid IPv6

#### File and Directory Operations

```python
def copyfolder(sourcePath, destPath)
```
**Description**: Recursively copies folders and files
**Parameters**:
- `sourcePath` (str) - Source directory path
- `destPath` (str) - Destination directory path
**Usage**: Used for cloning websites and copying templates

```python
def cleanup_routine()
```
**Description**: Performs cleanup operations on exit
**Usage**: Automatically called when SET exits to clean temporary files

#### Configuration Management

```python
def check_config(param)
```
**Description**: Checks configuration parameter values
**Parameters**: `param` (str) - Configuration parameter name
**Returns**: `str` - Configuration value or "0" if not found

```python
def update_options(option)
```
**Description**: Updates configuration options
**Parameters**: `option` (str) - Configuration option in "KEY=VALUE" format
**Example**:
```python
update_options("IPADDR=192.168.1.100")
```

#### Payload and Exploit Functions

```python
def generate_shellcode(payload, ipaddr, port)
```
**Description**: Generates shellcode for specified payload
**Parameters**:
- `payload` (str) - Payload type
- `ipaddr` (str) - IP address for reverse connection
- `port` (str) - Port for reverse connection
**Returns**: `str` - Generated shellcode

```python
def metasploit_shellcode(payload, ipaddr, port)
```
**Description**: Generates Metasploit-compatible shellcode
**Parameters**:
- `payload` (str) - Metasploit payload name
- `ipaddr` (str) - LHOST parameter
- `port` (str) - LPORT parameter
**Returns**: `str` - Metasploit shellcode

#### Web Server Functions

```python
def start_web_server(directory)
```
**Description**: Starts a threaded web server
**Parameters**: `directory` (str) - Directory to serve files from
**Usage**: Used for hosting malicious websites and payloads

```python
def java_applet_attack(website, port, directory)
```
**Description**: Launches Java applet attack
**Parameters**:
- `website` (str) - Target website URL
- `port` (str) - Port for web server
- `directory` (str) - Directory containing attack files

#### Utility Functions

```python
def generate_random_string(low, high)
```
**Description**: Generates random alphanumeric string
**Parameters**:
- `low` (int) - Minimum length
- `high` (int) - Maximum length
**Returns**: `str` - Random string

```python
def site_cloner(website, exportpath, *args)
```
**Description**: Clones websites for phishing attacks
**Parameters**:
- `website` (str) - URL of website to clone
- `exportpath` (str) - Path to save cloned files
- `*args` - Additional arguments
**Usage**: Core function for website cloning attacks

### Menu System (`src/core/menu/text.py`)

The menu system provides structured navigation through SET's features.

#### Menu Definitions

```python
main_menu = [
    'Social-Engineering Attacks',
    'Penetration Testing (Fast-Track)',
    'Third Party Modules',
    'Update the Social-Engineer Toolkit',
    'Update SET configuration',
    'Help, Credits, and About'
]
```

#### Attack Categories

```python
main = [
    'Spear-Phishing Attack Vectors',
    'Website Attack Vectors', 
    'Infectious Media Generator',
    'Create a Payload and Listener',
    'Mass Mailer Attack',
    'Arduino-Based Attack Vector',
    'Wireless Access Point Attack Vector',
    'QRCode Generator Attack Vector',
    'Powershell Attack Vectors',
    'Third Party Modules'
]
```

## Attack Modules

### Web Attack Vectors (`src/webattack/`)

#### Credential Harvester (`src/webattack/harvester/harvester.py`)

```python
class SETHandler(BaseHTTPRequestHandler)
```
**Description**: HTTP request handler for credential harvesting
**Methods**:
- `do_GET()`: Handles GET requests
- `do_POST()`: Captures POST data (credentials)
- `log_message()`: Custom logging for captured data

**Usage Example**:
```python
# The harvester automatically captures form submissions
# Configuration is done through SET's menu system
```

#### Multi-Attack Vector (`src/webattack/multi_attack/multiattack.py`)

```python
def flag_on(vector)
```
**Description**: Enables specific attack vector
**Parameters**: `vector` (str) - Attack vector name

```python
def flag_off(vector)
```
**Description**: Disables specific attack vector
**Parameters**: `vector` (str) - Attack vector name

```python
def write_file(filename, results)
```
**Description**: Writes attack results to file
**Parameters**:
- `filename` (str) - Output filename
- `results` (str) - Results data

#### HTA Attack Vector (`src/webattack/hta/main.py`)

```python
def gen_hta_cool_stuff()
```
**Description**: Generates HTA (HTML Application) attack files
**Usage**: Creates malicious HTA files for client-side attacks

### Phishing Modules (`src/phishing/`)

#### SMTP Client (`src/phishing/smtp/client/smtp_client.py`)

```python
def mail(to, subject, text, attach, prioflag1, prioflag2)
```
**Description**: Sends email with optional attachments
**Parameters**:
- `to` (str) - Recipient email address
- `subject` (str) - Email subject
- `text` (str) - Email body
- `attach` (str) - Attachment file path
- `prioflag1` (str) - Priority flag 1
- `prioflag2` (str) - Priority flag 2

**Usage Example**:
```python
mail("target@example.com", "Important Update", 
     "Please see attachment", "/path/to/payload.pdf", "1", "1")
```

## Payload Generation

### Solo Payload Generator (`src/core/payloadgen/solo.py`)

```python
def payload_generate(payload, lhost, port)
```
**Description**: Generates standalone payloads
**Parameters**:
- `payload` (str) - Payload type identifier
- `lhost` (str) - Listening host IP address
- `port` (str) - Listening port
**Returns**: Generated payload file path

**Supported Payload Types**:
- Windows reverse shells
- Linux reverse shells
- Meterpreter payloads
- Custom shellcode

## Configuration Management

### Configuration Updates (`src/core/update_config.py`)

```python
def update_config()
```
**Description**: Updates SET configuration files
**Usage**: Called automatically to maintain configuration consistency

```python
def value_type(value)
```
**Description**: Determines configuration value type
**Parameters**: `value` (str) - Configuration value
**Returns**: Processed value with correct type

## Third-Party Modules

### Module Handler (`src/core/module_handler.py`)

The module handler provides a framework for loading and executing third-party modules.

#### Module Structure

Third-party modules must follow this structure:

```python
# Example module: modules/example_module.py

MAIN = "Example Attack Module"  # Required: Module description

def main():
    """
    Required: Main function called when module is selected
    """
    print("Executing example attack...")
    # Module logic here
```

#### Available Modules

1. **Google Analytics Attack** (`modules/google_analytics_attack.py`)
   - Exploits Google Analytics for information gathering

2. **RATTE Module** (`modules/ratte_module.py`)
   - Remote Administration Tool functionality

3. **RATTE Only Module** (`modules/ratte_only_module.py`)
   - Standalone RATTE functionality

## Usage Examples

### Basic Website Cloning Attack

```python
# This is typically done through the menu system, but the core function is:
from src.core.setcore import site_cloner

# Clone a website for phishing
site_cloner("https://example.com/login", "/tmp/cloned_site")
```

### Credential Harvesting Setup

```bash
# Through SET menu:
# 1) Social-Engineering Attacks
# 2) Website Attack Vectors  
# 3) Credential Harvester Attack Method
# 2) Site Cloner
# Enter URL to clone: https://gmail.com
```

### Mass Email Campaign

```bash
# Through SET menu:
# 1) Social-Engineering Attacks
# 5) Mass Mailer Attack
# Configure SMTP settings and recipient list
```

### Custom Payload Generation

```bash
# Through SET menu:
# 1) Social-Engineering Attacks
# 4) Create a Payload and Listener
# Select payload type and configure LHOST/LPORT
```

### Java Applet Attack

```bash
# Through SET menu:
# 1) Social-Engineering Attacks
# 2) Website Attack Vectors
# 1) Java Applet Attack Method
# 2) Site Cloner
# Configure target website and payload
```

## Installation and Setup

### Requirements

```bash
# Install dependencies
pip3 install -r requirements.txt

# For full functionality, install:
# - Metasploit Framework
# - Apache web server
# - Sendmail (for email spoofing)
```

### Basic Installation

```bash
# Clone repository
git clone https://github.com/trustedsec/social-engineer-toolkit/ setoolkit/
cd setoolkit

# Install dependencies
pip3 install -r requirements.txt

# Run setup
python3 setup.py

# Start SET
./setoolkit
```

### Configuration

SET uses configuration files in `/etc/setoolkit/`:

- `set.config` - Main configuration file
- `set_config.py` - Python configuration module

Key configuration options:

```bash
# Auto-detect IP address
AUTO_DETECT=ON

# Web server settings
WEBATTACK_PORT=80
APACHE_SERVER=ON

# Email settings
SENDMAIL=OFF
GMAIL_USER=username
GMAIL_PASSWORD=password

# Metasploit settings
METASPLOIT_PATH=/usr/share/metasploit-framework/
```

## Security Considerations

### Legal Usage

⚠️ **IMPORTANT**: SET is designed for authorized penetration testing only. Usage must comply with:

- Written authorization from target organization
- Local and international laws
- Ethical hacking guidelines
- Professional penetration testing standards

### Best Practices

1. **Authorization**: Always obtain written permission before testing
2. **Scope**: Stay within defined testing scope
3. **Documentation**: Maintain detailed logs of all activities
4. **Cleanup**: Remove all payloads and artifacts after testing
5. **Reporting**: Provide comprehensive reports with remediation guidance

### Defensive Measures

Organizations can defend against SET attacks by:

1. **User Training**: Regular security awareness training
2. **Email Filtering**: Advanced email security solutions
3. **Web Filtering**: Block malicious websites and downloads
4. **Endpoint Protection**: Deploy comprehensive endpoint security
5. **Network Monitoring**: Monitor for suspicious network activity

## Contributing

### Adding Custom Modules

To create a custom third-party module:

1. Create a Python file in the `modules/` directory
2. Include the required `MAIN` variable with module description
3. Implement the `main()` function with your attack logic
4. Test thoroughly before deployment

### Code Style

- Follow PEP 8 Python style guidelines
- Include comprehensive docstrings
- Add error handling for all user inputs
- Maintain compatibility with Python 2/3

### Reporting Issues

Report bugs and feature requests through the official GitHub repository:
https://github.com/trustedsec/social-engineer-toolkit/issues

---

*This documentation covers the major APIs and functionality of SET. For the most current information, refer to the official repository and user manual.*