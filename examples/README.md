# SET API Examples

This directory contains practical examples demonstrating how to use the Social-Engineer Toolkit (SET) APIs programmatically.

## Examples Included

### 1. Java Applet Attack (`example_java_applet_attack.py`)

Demonstrates how to:
- Configure a Java Applet attack
- Clone a target website
- Inject malicious Java applet
- Generate payloads
- Set up Metasploit listeners

**Usage**:
```bash
sudo python3 example_java_applet_attack.py
```

### 2. Credential Harvester (`example_credential_harvester.py`)

Demonstrates how to:
- Clone a login page
- Set up credential harvesting
- Monitor and capture submitted credentials
- Handle NAT/port forwarding scenarios

**Usage**:
```bash
sudo python3 example_credential_harvester.py
```

### 3. Payload Generator (`example_payload_generator.py`)

Demonstrates how to:
- Generate Windows Meterpreter executables
- Create PowerShell payloads
- Generate raw shellcode
- Create Metasploit listener configurations

**Usage**:
```bash
python3 example_payload_generator.py
```

## Prerequisites

1. **SET Installation**: Ensure SET is properly installed
   ```bash
   cd /workspace
   pip3 install -r requirements.txt
   python3 setup.py
   ```

2. **Root Privileges**: Many operations require root access
   ```bash
   sudo su
   ```

3. **Metasploit**: Required for payload generation and listeners
   ```bash
   # Check if Metasploit is installed
   which msfconsole
   ```

## Important Notes

### Legal and Ethical Considerations

⚠️ **WARNING**: These tools are for **AUTHORIZED TESTING ONLY**

- Always obtain written authorization before testing
- Only test systems you own or have explicit permission to test
- Unauthorized access is illegal and punishable by law
- Document all activities and maintain proper chain of custody

### Configuration

Before running examples, verify your SET configuration:

```bash
# Configuration file location
/etc/setoolkit/set.config

# Key settings to check:
# - METASPLOIT_PATH=/usr/bin/
# - AUTO_DETECT=ON
# - EMAIL_PROVIDER=gmail (if using email features)
```

### Common Issues

#### "Not running as root"
```bash
# Solution: Run with sudo
sudo python3 example_script.py
```

#### "Metasploit not found"
```bash
# Solution: Install Metasploit or configure path
# Edit /etc/setoolkit/set.config
METASPLOIT_PATH=/usr/bin/
```

#### "Website cloning failed"
```bash
# Possible causes:
# - No internet connection
# - Target site blocks scraping
# - Invalid URL

# Solution: Check connectivity and try different URL
```

## Customization

### Modifying Examples

Each example can be customized by editing the configuration section:

```python
# Configuration section at the top of each file
target_website = "https://www.example.com"
attacker_ip = "192.168.1.100"
listener_port = "443"
```

### Creating Your Own Scripts

Use these examples as templates for your own automation:

```python
#!/usr/bin/env python3
from src.core.setcore import *
import sys

# Your custom SET automation here
def my_custom_attack():
    # Configure
    update_options("IPADDR=10.0.0.5")
    
    # Execute attack
    # ...
    
if __name__ == "__main__":
    try:
        my_custom_attack()
    except KeyboardInterrupt:
        cleanup_routine()
```

## Testing Workflow

### Recommended Testing Process

1. **Lab Setup**
   - Use isolated test environment
   - Configure virtual machines
   - Set up network segmentation

2. **Authorization**
   - Obtain written permission
   - Define scope clearly
   - Set time boundaries

3. **Execution**
   - Start with passive reconnaissance
   - Use examples as starting point
   - Document all activities

4. **Reporting**
   - Compile captured data
   - Create detailed report
   - Provide remediation recommendations

5. **Cleanup**
   - Remove all payloads
   - Clean up logs
   - Verify complete removal

## Additional Resources

- **Full API Documentation**: See `../API_DOCUMENTATION.md`
- **Quick Reference**: See `../API_QUICK_REFERENCE.md`
- **SET User Manual**: See `../readme/User_Manual.pdf`
- **GitHub**: https://github.com/trustedsec/social-engineer-toolkit

## Support

If you encounter issues:

1. Check the logs: `src/logs/set_logfile.log`
2. Review API documentation
3. Open an issue: https://github.com/trustedsec/social-engineer-toolkit/issues

## Contributing

To contribute your own examples:

1. Fork the repository
2. Add your example with clear comments
3. Test thoroughly in lab environment
4. Submit pull request with description

## License

These examples are part of the Social-Engineer Toolkit and are subject to the same license. See `../readme/LICENSE` for details.

---

**Remember**: With great power comes great responsibility. Use these tools ethically and legally.
