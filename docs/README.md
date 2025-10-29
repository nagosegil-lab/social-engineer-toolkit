# SET Documentation Suite

This directory contains comprehensive documentation for the Social-Engineer Toolkit (SET), covering all aspects from basic usage to advanced development.

## Documentation Overview

### 📚 Core Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples and usage instructions
- **[FUNCTION_REFERENCE.md](FUNCTION_REFERENCE.md)** - Detailed function-by-function reference guide
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Practical examples and step-by-step tutorials

### 🎯 Specialized Guides

- **[ATTACK_MODULES_REFERENCE.md](ATTACK_MODULES_REFERENCE.md)** - In-depth coverage of all attack modules
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Guide for extending SET and contributing code

## Quick Start

### For Users
1. Start with [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for an overview
2. Follow practical examples in [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
3. Reference specific attacks in [ATTACK_MODULES_REFERENCE.md](ATTACK_MODULES_REFERENCE.md)

### For Developers
1. Read the [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for architecture overview
2. Use [FUNCTION_REFERENCE.md](FUNCTION_REFERENCE.md) for API details
3. Follow contribution guidelines in the developer guide

## Documentation Structure

```
docs/
├── README.md                      # This file - documentation overview
├── API_DOCUMENTATION.md           # Complete API reference
├── FUNCTION_REFERENCE.md          # Detailed function reference
├── USAGE_EXAMPLES.md             # Practical usage examples
├── ATTACK_MODULES_REFERENCE.md   # Attack module documentation
└── DEVELOPER_GUIDE.md            # Development and contribution guide
```

## Key Features Documented

### Core Functionality
- ✅ System initialization and configuration
- ✅ User interface and menu systems
- ✅ Network and web server functions
- ✅ Payload generation and handling
- ✅ File operations and utilities

### Attack Vectors
- ✅ Web attack vectors (Java applets, browser exploits, credential harvesting)
- ✅ Spear-phishing campaigns and mass mailers
- ✅ Infectious media generation (USB/CD attacks)
- ✅ Teensy/Arduino HID attacks
- ✅ Wireless access point attacks
- ✅ PowerShell attack vectors
- ✅ Third-party module system

### Development Support
- ✅ Module creation guidelines
- ✅ Core function extension
- ✅ Testing and debugging procedures
- ✅ Code style and contribution standards

## Usage Examples by Category

### Basic Operations
```bash
# Start SET
sudo ./setoolkit

# Credential harvesting
Menu: 1 > 2 > 3 > 2
URL: https://login.company.com
IP: 192.168.1.100
```

### Advanced Attacks
```bash
# Multi-vector campaign
# 1. Email phishing
# 2. Credential harvesting backup  
# 3. USB payload distribution
# 4. Wireless access point
```

### Development
```python
# Create custom module
MAIN = "Custom Attack Description"

def main():
    from src.core.setcore import *
    print_status("Custom attack started")
    # Attack logic here
```

## Security and Legal Considerations

⚠️ **IMPORTANT**: All documentation emphasizes:

- **Legal Authorization Required** - Only use with written permission
- **Ethical Guidelines** - Follow responsible disclosure practices  
- **Security Best Practices** - Implement proper operational security
- **Defensive Measures** - Include protection recommendations

## Getting Help

### Documentation Issues
- Check the specific documentation file for your topic
- Review the function reference for API details
- Look at usage examples for practical guidance

### Technical Support
- Review troubleshooting sections in usage examples
- Check the developer guide for architecture questions
- Refer to the main SET repository for bug reports

### Contributing
- Follow the developer guide for contribution procedures
- Ensure all code includes proper documentation
- Add examples and usage instructions for new features

## Documentation Maintenance

This documentation suite is designed to be:

- **Comprehensive** - Covers all major SET functionality
- **Practical** - Includes working examples and use cases
- **Current** - Reflects the latest SET capabilities
- **Accessible** - Organized for both users and developers

### Last Updated
Generated: 2024-10-29
SET Version: Compatible with SET 8.x series

### Version History
- v1.0 - Initial comprehensive documentation suite
- Covers all major SET components and functionality
- Includes practical examples and developer guidance

---

*This documentation provides complete coverage of SET's capabilities. Always ensure proper authorization before using these tools in any environment.*