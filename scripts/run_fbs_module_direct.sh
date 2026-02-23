#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.fbs_trading.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

python3 -c "import importlib.util; spec=importlib.util.spec_from_file_location('fbs','modules/fbs_ai_assistant.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.main()"
