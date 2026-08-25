#!/usr/bin/env bash
# Адаптер: даёт задачу стороннему кодеру через Cursor CLI, пишет расход токенов в ledger.
# Использование: cursor-run.sh <model> <role> "<prompt>"
set -euo pipefail
MODEL="${1:?model}"; ROLE="${2:?role}"; PROMPT="${3:?prompt}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cursor-agent -p --trust --output-format json --model "$MODEL" "$PROMPT" \
  | python3 "$ROOT/tools/ledger_cursor.py" "$ROLE" "$MODEL" "$ROOT"
