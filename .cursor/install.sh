#!/usr/bin/env bash
#
# Cloud Agent install script for the Social-Engineer Toolkit (SET).
#
# SET is a Python 3 CLI framework. It must run as root (it enforces euid 0),
# so its Python dependencies are installed system-wide with sudo pip so that
# they are importable when the toolkit is launched via `sudo ./setoolkit`.
#
# Notes on dependency handling:
#   - `pycrypto` (pinned in requirements.txt) is abandoned and cannot compile
#     on modern CPython (3.12), so it is replaced here with the maintained,
#     API-namespace-compatible `pycryptodome`. The toolkit only imports
#     `Crypto` optionally, so this keeps the optional import resolvable without
#     modifying the repository's requirements.txt.
#   - A Debian-managed `blinker` shadows the copy required by a transitive
#     dependency (Flask via impacket); it is reinstalled with --ignore-installed.
#
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[*] Installing system build dependencies..."
sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    libgmp-dev \
    freetds-dev \
    libssl-dev

echo "[*] Resolving Python requirements (excluding unbuildable pycrypto)..."
mapfile -t REQS < <(grep -vE '^\s*(#|$)' requirements.txt | grep -vix 'pycrypto')

echo "[*] Reconciling Debian-managed blinker..."
sudo pip3 install --break-system-packages --ignore-installed blinker

echo "[*] Installing Python dependencies system-wide..."
sudo pip3 install --break-system-packages \
    pycryptodome \
    flake8 \
    pytest \
    "${REQS[@]}"

echo "[*] Verifying core imports as root..."
sudo python3 -c "import pexpect, requests, pefile, impacket, qrcode, pymssql; from Crypto.Cipher import AES; from PIL import Image; import OpenSSL; print('[OK] SET dependencies import successfully')"

echo "[*] Install complete. Launch the toolkit with: sudo ./setoolkit"
