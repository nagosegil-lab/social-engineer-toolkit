# Social Engineering Toolkit (SET) - Module Reference

## Table of Contents
1. [Core Modules](#core-modules)
2. [Attack Modules](#attack-modules)
3. [Utility Modules](#utility-modules)
4. [Configuration Modules](#configuration-modules)
5. [Template Modules](#template-modules)

## Core Modules

### 1. `src.core.setcore`

**Purpose**: Core functionality and utilities for the entire toolkit.

**Key Classes**:
- `bcolors`: Terminal color formatting
- `create_menu`: Dynamic menu generation

**Key Functions**:

#### System Functions
```python
def check_os():
    """Detects operating system (posix/windows)"""

def get_version():
    """Returns current SET version"""

def definepath():
    """Defines SET installation path"""

def check_backbox():
    """Checks if running on BackBox Linux"""

def check_kali():
    """Checks if running on Kali Linux"""
```

#### Network Functions
```python
def grab_ipaddress():
    """Prompts and validates IP address input"""

def detect_public_ip():
    """Auto-detects public IP address"""

def validate_ip(address):
    """Validates IPv4 address format"""

def is_valid_ip(ip):
    """Checks if string is valid IP address"""

def is_valid_ipv4(ip):
    """Validates IPv4 address"""

def is_valid_ipv6(ip):
    """Validates IPv6 address"""

def check_ports(port):
    """Checks if port is available"""

def socket_listener(port):
    """Creates socket listener on specified port"""
```

#### Metasploit Integration
```python
def meta_path():
    """Finds Metasploit installation path"""

def metasploit_shellcode(payload, ipaddr, port):
    """Generates Metasploit shellcode"""

def msf_payload(payload, lhost, lport):
    """Creates Metasploit payload"""
```

#### Configuration Management
```python
def check_config():
    """Validates SET configuration"""

def update_options(option):
    """Updates configuration options"""

def check_options(option):
    """Retrieves configuration values"""

def copyfolder(src, dst):
    """Copies directory structure"""
```

#### User Interface
```python
def print_status(message):
    """Prints status message (green)"""

def print_error(message):
    """Prints error message (red)"""

def print_warning(message):
    """Prints warning message (yellow)"""

def print_info(message):
    """Prints info message (blue)"""

def setprompt(category, text):
    """Creates formatted prompt"""

def yesno_prompt(category, text):
    """Yes/No prompt with validation"""

def return_continue():
    """Press return to continue prompt"""
```

#### Utility Functions
```python
def generate_random_string(low, high):
    """Generates random alphanumeric string"""

def date_time():
    """Returns formatted date/time string"""

def log(message):
    """Logs message to SET log file"""

def cleanup_routine():
    """Cleans up temporary files"""

def kill_proc(process):
    """Kills specified process"""

def upx(payload):
    """Packs executable with UPX"""

def encryptAES(secret, data):
    """Encrypts data with AES"""

def generate_shellcode():
    """Generates shellcode for payloads"""
```

#### CIDR Utilities
```python
def ip2bin(ip):
    """Converts IP to binary"""

def dec2bin(dec):
    """Converts decimal to binary"""

def bin2ip(bin_ip):
    """Converts binary to IP"""

def printCIDR(cidr):
    """Prints CIDR block information"""

def validateCIDRBlock(cidr):
    """Validates CIDR block format"""
```

### 2. `src.core.webserver`

**Purpose**: HTTP server functionality for web attacks.

**Key Classes**:

#### `StoppableHttpRequestHandler`
```python
class StoppableHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with QUIT capability"""
    
    def do_GET(self):
        """Handles GET requests"""
        
    def do_POST(self):
        """Handles POST requests"""
        
    def do_QUIT(self):
        """Stops the server"""
```

#### `StoppableHttpServer`
```python
class StoppableHttpServer(http.server.HTTPServer):
    """HTTP server that can be stopped via QUIT"""
    
    def serve_forever(self):
        """Serves requests until stopped"""
```

**Key Functions**:
```python
def start_server(web_port, path):
    """Starts HTTP server on specified port and path"""

def stop_server(web_port):
    """Stops HTTP server via QUIT request"""
```

### 3. `src.core.module_handler`

**Purpose**: Manages third-party modules.

**Key Functions**:
```python
def load_modules():
    """Loads available third-party modules"""

def execute_module(module_path):
    """Executes selected module"""
```

### 4. `src.core.payloadgen.create_payloads`

**Purpose**: Creates Metasploit payloads and listeners.

**Key Functions**:
```python
def create_payloads():
    """Main payload creation function"""

def shellcode_payload():
    """Creates shellcode injection payload"""

def multipy_payload():
    """Creates multi-platform Python payload"""

def reverse_shell():
    """Creates reverse shell payload"""

def ratte_payload():
    """Creates RATTE payload"""

def custom_executable():
    """Creates custom executable payload"""
```

### 5. `src.core.msf_attacks.create_payload`

**Purpose**: Creates file-format exploits and Metasploit payloads.

**Key Functions**:
```python
def create_payload():
    """Main payload creation function"""

def pdf_attack():
    """Creates PDF-based attack"""

def doc_attack():
    """Creates DOC-based attack"""

def rtf_attack():
    """Creates RTF-based attack"""

def mov_attack():
    """Creates MOV-based attack"""

def dll_hijacking():
    """Creates DLL hijacking attack"""
```

## Attack Modules

### 1. `src.webattack.harvester.harvester`

**Purpose**: Credential harvesting from cloned websites.

**Key Classes**:

#### `SETHandler`
```python
class SETHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler for credential harvesting"""
    
    def do_GET(self):
        """Serves cloned website"""
        
    def do_POST(self):
        """Captures and logs credentials"""
        
    def log_message(self, format, *args):
        """Custom logging for captured data"""
```

**Key Functions**:
```python
def run():
    """Starts the credential harvester server"""

def start_harvester():
    """Initializes harvester configuration"""

def log_credentials(data):
    """Logs captured credentials to file"""
```

### 2. `src.webattack.web_clone.cloner`

**Purpose**: Website cloning for social engineering attacks.

**Key Functions**:
```python
def clone_website(url, output_dir):
    """Clones website using wget or urllib"""

def inject_java_applet(html_content):
    """Injects Java applet into HTML"""

def inject_metasploit_iframe(html_content):
    """Injects Metasploit iframe into HTML"""

def inject_hta_attack(html_content):
    """Injects HTA attack code into HTML"""

def obfuscate_filenames():
    """Randomizes filenames for evasion"""
```

### 3. `src.webattack.browser_exploits.browser_exploits`

**Purpose**: Browser-based exploitation attacks.

**Key Functions**:
```python
def browser_exploits():
    """Main browser exploits function"""

def java_exploit():
    """Java-based browser exploit"""

def flash_exploit():
    """Flash-based browser exploit"""

def silverlight_exploit():
    """Silverlight-based browser exploit"""
```

### 4. `src.webattack.tabnabbing.tabnabbing`

**Purpose**: Tabnabbing attack implementation.

**Key Functions**:
```python
def tabnabbing_attack():
    """Main tabnabbing attack function"""

def create_tabnabbing_page():
    """Creates tabnabbing JavaScript code"""

def inject_tabnabbing(html_content):
    """Injects tabnabbing code into HTML"""
```

### 5. `src.webattack.multi_attack.multi_attack`

**Purpose**: Multi-vector web attacks.

**Key Functions**:
```python
def multi_attack():
    """Main multi-attack function"""

def combine_attacks():
    """Combines multiple attack vectors"""

def attack_selector():
    """Selects appropriate attack vectors"""
```

### 6. `src.webattack.hta.hta`

**Purpose**: HTA (HTML Application) attacks.

**Key Functions**:
```python
def hta_attack():
    """Main HTA attack function"""

def create_hta_file():
    """Creates malicious HTA file"""

def inject_hta_code():
    """Injects HTA code into HTML"""
```

### 7. `src.phishing.smtp.client.smtp_client`

**Purpose**: Email-based social engineering attacks.

**Key Functions**:
```python
def mail(to, subject, text, attach, prioflag1, prioflag2):
    """Sends email with attachment"""

def smtp_connect():
    """Establishes SMTP connection"""

def send_email():
    """Sends email message"""

def attach_file():
    """Attaches file to email"""
```

### 8. `src.teensy.teensy`

**Purpose**: Teensy USB HID attack generation.

**Key Functions**:
```python
def teensy_attack():
    """Main Teensy attack function"""

def writefile(filename, now):
    """Writes Teensy .ino file with IP substitution"""

def generate_powershell_payload():
    """Generates PowerShell payload for Teensy"""

def generate_wscript_payload():
    """Generates wscript payload for Teensy"""

def generate_java_applet_payload():
    """Generates Java applet payload for Teensy"""
```

### 9. `src.powershell.powershell`

**Purpose**: PowerShell-based attack vectors.

**Key Functions**:
```python
def powershell_attack():
    """Main PowerShell attack function"""

def alphanumeric_shellcode():
    """Generates alphanumeric shellcode injector"""

def reverse_shell():
    """Generates PowerShell reverse shell"""

def bind_shell():
    """Generates PowerShell bind shell"""

def sam_dump():
    """Generates SAM database dump script"""
```

### 10. `src.wireless.wifiattack`

**Purpose**: Wireless attack vectors.

**Key Functions**:
```python
def wifi_attack():
    """Main wireless attack function"""

def access_point_attack():
    """Creates malicious access point"""

def dns_spoofing():
    """Implements DNS spoofing attack"""

def deauth_attack():
    """Implements deauthentication attack"""
```

## Utility Modules

### 1. `src.core.dictionaries`

**Purpose**: Mapping functions for user input to Metasploit values.

**Key Functions**:
```python
def ms_payload(payload):
    """Maps payload selection to Metasploit payload name"""

def ms_module(exploit):
    """Maps exploit selection to Metasploit module name"""

def ms_attacks(exploit):
    """Maps file format attack to Metasploit module"""

def ms_encoders(encoder):
    """Maps encoder selection to Metasploit encoder"""

def ms_platforms(platform):
    """Maps platform selection to Metasploit platform"""

def set_attacks(attack):
    """Maps SET attack selection to attack name"""

def teensy_attacks(attack):
    """Maps Teensy attack selection to attack name"""

def wireless_attacks(attack):
    """Maps wireless attack selection to attack name"""
```

### 2. `src.core.menu.text`

**Purpose**: Contains all menu text and descriptions.

**Key Variables**:
```python
main_text = "Social-Engineer Toolkit (SET) main menu"
main_menu = ["Spear-Phishing Attack Vectors", ...]
webattack_text = "Web attack vector descriptions"
teensy_text = "Teensy attack descriptions"
powershell_text = "PowerShell attack descriptions"
fasttrack_text = "Fast-Track attack descriptions"
wireless_text = "Wireless attack descriptions"
infectious_text = "Infectious media descriptions"
```

### 3. `src.qrcode.qrgenerator`

**Purpose**: QR code generation for attacks.

**Key Functions**:
```python
def gen_qrcode(url):
    """Generates QR code for given URL"""

def create_qr_image(data):
    """Creates QR code image"""

def save_qr_code(image, filename):
    """Saves QR code to file"""
```

### 4. `src.autorun.autolaunch`

**Purpose**: Autorun-based attacks for USB/CD media.

**Key Functions**:
```python
def autorun_attack():
    """Main autorun attack function"""

def create_autorun_file():
    """Creates autorun.inf file"""

def generate_payload():
    """Generates payload for autorun"""
```

## Configuration Modules

### 1. `src.core.update_config`

**Purpose**: Configuration file management and updates.

**Key Functions**:
```python
def update_config():
    """Updates SET configuration files"""

def backup_config():
    """Backs up existing configuration"""

def validate_config():
    """Validates configuration file format"""

def migrate_config():
    """Migrates old configuration format"""
```

### 2. `src.core.config.baseline`

**Purpose**: Default configuration template.

**Key Configuration Options**:
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

## Template Modules

### 1. `src.templates`

**Purpose**: Email and web attack templates.

**Key Template Files**:
- `baby.template`: Baby announcement email template
- `ebook.template`: E-book download template
- `newupdate.template`: Software update template
- `receipt.template`: Receipt email template
- `report.template`: Report attachment template
- `securityupdates.template`: Security update template
- `status.template`: Status update template
- `strange.template`: Strange email template

**Template Format**:
```
Subject: {SUBJECT}
From: {FROM_NAME} <{FROM_EMAIL}>
To: {TARGET_EMAIL}

{EMAIL_BODY}

Best regards,
{FROM_NAME}
```

### 2. `src.html.templates`

**Purpose**: HTML templates for web attacks.

**Key Template Files**:
- `java_applet.template`: Java applet attack template
- `browser_exploit.template`: Browser exploit template
- `harvester.template`: Credential harvester template
- `tabnabbing.template`: Tabnabbing attack template

**Template Format**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{PAGE_TITLE}</title>
    {MALICIOUS_CODE}
</head>
<body>
    {PAGE_CONTENT}
</body>
</html>
```

## Module Dependencies

### Core Dependencies
- `src.core.setcore`: Required by all modules
- `src.core.webserver`: Required by web attack modules
- `src.core.dictionaries`: Required by payload generation modules

### Attack Dependencies
- `src.webattack.harvester`: Depends on `src.webattack.web_clone`
- `src.webattack.web_clone`: Depends on `src.core.webserver`
- `src.phishing.smtp`: Depends on `src.core.setcore`
- `src.teensy.teensy`: Depends on `src.core.setcore`
- `src.powershell.powershell`: Depends on `src.core.setcore`

### Utility Dependencies
- `src.qrcode.qrgenerator`: Depends on `qrcode` Python library
- `src.core.menu.text`: Required by all menu systems
- `src.templates`: Required by email and web attack modules

## Module Loading

### Automatic Loading
```python
# Core modules are loaded automatically
import src.core.setcore
import src.core.webserver
import src.core.module_handler
```

### Dynamic Loading
```python
# Attack modules are loaded on demand
from src.webattack.harvester import harvester
from src.phishing.smtp.client import smtp_client
from src.teensy import teensy
```

### Third-Party Modules
```python
# Third-party modules are loaded from modules/ directory
# Must have MAIN="Description" in header
# Must implement main() function
```

## Error Handling

### Module-Level Error Handling
```python
try:
    # Module functionality
    pass
except Exception as e:
    log(f"Module error: {str(e)}")
    print_error(f"Module failed: {str(e)}")
```

### Global Error Handling
```python
# In setcore.py
def debug_msg(message):
    """Debug message with level checking"""
    if DEBUG_LEVEL >= 3:
        print(f"[DEBUG] {message}")

def log(message):
    """Log message to file"""
    with open(LOGFILE, "a") as f:
        f.write(f"{date_time()}: {message}\n")
```

## Module Development

### Creating New Modules
1. Create module file in appropriate directory
2. Add `MAIN="Description"` header
3. Implement `main()` function
4. Add error handling
5. Test module functionality

### Module Template
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module Name: Your Module Name
Description: Brief description of module functionality
Author: Your Name
Version: 1.0
"""

MAIN="Your Module Description"

def main():
    """Main module function"""
    try:
        # Module functionality here
        pass
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    main()
```

---

This module reference provides comprehensive documentation for all modules in the Social Engineering Toolkit, including their purposes, key functions, dependencies, and usage patterns.