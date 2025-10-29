## Examples (safe snippets)

These examples show how to use utilities and helpers that are safe to run locally. They don’t perform attacks and are useful for testing or understanding APIs.

### Detect your public IPv4 address
```python
from src.core.setcore import detect_public_ip

print(detect_public_ip())
```

### Validate an IP address
```python
from src.core.setcore import validate_ip

print(validate_ip("192.168.1.10"))  # True
print(validate_ip("300.168.1.10"))  # False
```

### Generate a random string (letters only)
```python
from src.core.setcore import generate_random_string

print(generate_random_string(6, 12))  # random length between 6 and 12
```

### Create a QR code image from a URL
This writes `qrcode_attack.png` under `~/.set/reports/`.
```python
from src.qrcode.qrgenerator import gen_qrcode

gen_qrcode("https://example.com")
```

### Start a local HTTP server in a directory (requires privileges)
Binds to port 80 and serves files from a directory. Use only in isolated test environments.
```python
import os
from src.core.setcore import start_web_server_unthreaded

# Serve files from your user reports directory (adjust as needed)
from src.core.setcore import userconfigpath
root = os.path.join(userconfigpath, "web_clone")

# Ensure directory exists
os.makedirs(root, exist_ok=True)
with open(os.path.join(root, "index.html"), "w") as f:
    f.write("<h1>Test</h1>")

# Requires root on POSIX because of port 80
start_web_server_unthreaded(root)
```

### Automate a benign console session
Feed inputs to open the main menu and exit immediately.
```bash
printf "\n\n99\n" > /tmp/inputs.set
./seautomate /tmp/inputs.set
```

## Tips
- Run examples in a disposable VM or lab network.
- Avoid binding privileged ports unless necessary; use containers or non-privileged ports where possible.
- If an example requires root (e.g., port 80 listeners), consider adapting it to non-privileged ports for development.
