# The Social-Engineer Toolkit (SET)
* Copyright :copyright: 2020
* Written by: David Kennedy (ReL1K) @HackingDave 
* Company: [TrustedSec](https://www.trustedsec.com)

<br/>

## Description
The Social-Engineer Toolkit is an open-source penetration testing framework designed for social engineering. SET has a number of custom attack vectors that allow you to make a believable attack quickly. SET is a product of TrustedSec, LLC – an information security consulting firm located in Cleveland, Ohio.

DISCLAIMER: This is *only* for testing purposes and can only be used where strict consent has been given. Do not use this for illegal purposes, period.
Please read the LICENSE under readme/LICENSE for the licensing of SET. 

#### Supported platforms:
* Linux
* Mac OS X (experimental)

# Installation

## Install via requirements.txt

```bash
pip3 install -r requirements.txt
python3 setup.py 
```

## Install SET
=======
#### Mac OS X
You will need to use a virtual environment for the Python install if you are using an M2 Macbook with the following instructions in your CLI within the social-engineer-toolkit directory. 
```bash
    # to install dependencies, run the following:
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install -r requirements.txt

    # to install SET
    sudo python3 setup.py 
```

<br/>

## Installation
#### Windows 10 WSL/WSL2 Kali Linux
```bash
sudo apt install set -y
```
Kali Linux on Windows 10 is a minimal installation so it doesn't have any tools installed.
You can easily install Social Engineer Toolkit on WSL/WSL2 without needing pip using the above command.

#### Linux
```bash
git clone https://github.com/trustedsec/social-engineer-toolkit/ setoolkit/
cd setoolkit
pip3 install -r requirements.txt
python setup.py
```
<br/>

## Documentation

### Comprehensive Documentation Suite
This repository now includes comprehensive documentation covering all aspects of the Social Engineering Toolkit:

- **[API Documentation](API_DOCUMENTATION.md)**: Complete reference for all public APIs, functions, and components
- **[Usage Guide](USAGE_GUIDE.md)**: Step-by-step instructions and tutorials
- **[Module Reference](MODULE_REFERENCE.md)**: Detailed reference for all modules and their functions
- **[Examples and Tutorials](EXAMPLES_AND_TUTORIALS.md)**: Comprehensive examples and real-world scenarios
- **[Configuration Guide](CONFIGURATION_GUIDE.md)**: Complete configuration reference
- **[Security and Compliance](SECURITY_AND_COMPLIANCE.md)**: Legal, ethical, and security considerations
- **[Comprehensive README](COMPREHENSIVE_README.md)**: Complete overview and quick start guide

### Quick Start
```bash
# Install SET
pip install set

# Launch SET
setoolkit

# Or use the legacy launcher
python src/core/set.py
```

### Basic Example - Credential Harvester
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

### Original Documentation
For the original SET user manual, [visit the SET user manual](https://github.com/trustedsec/social-engineer-toolkit/raw/master/readme/User_Manual.pdf).

<br/>

## Bugs and enhancements
For bug reports or enhancements, please open an [issue](https://github.com/trustedsec/social-engineer-toolkit/issues) here.
<br/>
