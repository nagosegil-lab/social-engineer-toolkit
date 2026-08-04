# AGENTS.md

## Cursor Cloud specific instructions

### What this is
This repo is the **Social-Engineer Toolkit (SET)** — a single, interactive **root-run Python 3 CLI** (entry point `./setoolkit`). There is no web/API backend, no database, and no separate services to start; SET spins up its own transient network servers (HTTP on port 80, etc.) on demand from within its attack modules. Standard install/run steps are in `README.md`.

### Dependencies must be installed system-wide (for root)
`setoolkit` refuses to run unless `os.geteuid() == 0`, so it must be launched with `sudo`. Because of that, Python deps must live in the **system** site-packages, not the user site — packages installed to `~/.local` (the default for `pip --user` / `pip --break-system-packages` as a non-root user) are **invisible to root** and SET will fail to import them. The update script installs everything via `sudo pip3 ... --break-system-packages` for this reason.

Two non-obvious dependency caveats (already handled by the update script):
- `requirements.txt` pins `pycrypto`, which is abandoned and does **not** build on Python 3.12. We install `pycryptodome` instead — it provides the same `Crypto` namespace, and every `from Crypto...` import in SET is wrapped in try/except so this is a safe drop-in.
- `impacket` pulls in `flask` → `blinker`, and pip cannot uninstall the Debian-managed `blinker`; installs use `--ignore-installed blinker` to get past this.

### Running SET (the "app")
- Run from the repo root as root: `sudo python3 setoolkit`.
- **First run** prints the license and requires typing `y` to accept (creates `src/agreement4`). Subsequent runs skip this.
- Non-interactive driving: pipe answers (e.g. `printf 'y\n99\n' | sudo python3 setoolkit`) or use `sudo ./seautomate <answers_file>` (pexpect-driven).
- Config lives at `/etc/setoolkit/set.config`; per-user runtime data at `~/.set` (i.e. `/root/.set` when run via sudo).
- Runtime-generated files (`src/agreement4`, `src/html/index.template`, `src/logs/`, `~/.set/*`) are not tracked and should not be committed.

### Metasploit gating (important when testing features)
Metasploit is **not** installed here. When `msf_path == False`, SET disables several menu options: under *Social-Engineering Attacks* items **1, 3, 4, 8** (Spear-Phishing, Infectious Media, Payload/Listener, and the **QRCode** generator) and under *Website Attack Vectors* items **2 and 9**. The **Credential Harvester** (`1) Social-Engineering Attacks` → `2) Website Attack Vectors` → `3) Credential Harvester` → `1) Web Templates`) works **without** Metasploit and is the simplest end-to-end feature: it serves a cloned login page on port 80 and appends captured POST fields to `src/logs/harvester.log` (Ctrl-C generates a report). Make sure port 80 is free.

### Lint / tests
- Lint is the only CI check (`.github/workflows/Python_tests.yml`): run the two `flake8` commands documented there. Note: CI used flake8 3.x (Python 3.5–3.7); the current flake8 (7.x) additionally reports one **pre-existing** `F824` in `modules/ratte_module.py`, so the strict `--select=E9,F63,F7,F82` command exits non-zero on it. This is not caused by environment setup — do not "fix" it unless asked.
- There is **no automated test suite** (the pytest steps in CI are commented out).
