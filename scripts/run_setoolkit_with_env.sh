#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.fbs_trading.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

sudo -E python3 setoolkit
