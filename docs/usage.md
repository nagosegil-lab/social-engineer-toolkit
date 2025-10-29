## Usage Guide (safe and responsible)

- **Use responsibly**: Only on systems you own or are authorized to test.
- **Environment**: POSIX is the primary target; some features assume Linux.

## Install
```bash
# from repo root
pip3 install -r requirements.txt
```

## Entry points
- **Interactive console** (requires root on POSIX for networking and file paths):
  ```bash
  sudo ./setoolkit
  ```
  - Exits with `99`, `exit`, or `quit`.
  - Displays `README.md` and `readme/CREDITS` via the in-app help.

- **Automation wrapper** (`seautomate`): feed a newline-delimited file of inputs that mimic menu navigation. Use only benign flows for testing.
  ```bash
  # create an input file with harmless navigation (open menu, then exit)
  printf "\n\n99\n" > /tmp/inputs.set
  ./seautomate /tmp/inputs.set
  ```

- **Proxy helper** (`seproxy`): writes proxy settings to `~/.set/proxy.config`.
  ```bash
  ./seproxy
  # follow prompts, e.g. http://127.0.0.1:8080
  ```

- **Updater** (`seupdate`): invokes the internal updater.
  ```bash
  ./seupdate
  ```

## Files and directories
- SET uses a per-user config dir on POSIX: `~/.set/`
  - Reports are written under `~/.set/reports/`
  - Transient files: `~/.set/version.lock`, options, templates, etc.

## Logging
- Runtime errors append to `src/logs/set_logfile.log`. Some features print status and warnings using colored terminal output.

## Networking notes
- Some features require binding to privileged ports (e.g., 80) or spawning listeners. These generally require root and may be blocked by local security tools. Avoid running on production hosts.

## Updating
- On Kali/BackBox, system packages manage updates. Elsewhere, the internal updater runs `git pull` and cleans untracked files.

## Documentation
- Auto-generated API docs live under `docs/api/` after running the generator.
- Improve docstrings in source for richer API pages. Regenerate docs afterward.
