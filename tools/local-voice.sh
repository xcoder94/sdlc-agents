#!/usr/bin/env bash
# fix16: отправляет аудиофайл напрямую в backend POST /api/ask (multipart),
# так, как это делает бот -- реальный STT из голоса локально проверить иначе
# нельзя (Telegram-скачивание файла бот-путём локально недостижимо).
#
# Использование:
#   tools/local-voice.sh /path/to/audio.ogg [TELEGRAM_ID] [duration_seconds] [language]
#
# TELEGRAM_ID должен принадлежать пользователю со status=approved и
# заданной organization_key в erp_app.users (см. docs/local-testing.md).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_ENV="$REPO_ROOT/services/backend/.env"
BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000}"

AUDIO_FILE="${1:?Использование: $0 audio.ogg [TELEGRAM_ID] [duration_seconds] [language]}"
TG_ID="${2:-777130888}"
DURATION="${3:-3}"
LANG="${4:-ru}"

if [[ ! -f "$AUDIO_FILE" ]]; then
  echo "error: файл не найден: $AUDIO_FILE" >&2
  exit 1
fi
if [[ ! -f "$BACKEND_ENV" ]]; then
  echo "error: $BACKEND_ENV не найден" >&2
  exit 1
fi
INTERNAL_TOKEN="$(grep '^INTERNAL_API_TOKEN=' "$BACKEND_ENV" | head -1 | cut -d= -f2-)"
if [[ -z "$INTERNAL_TOKEN" ]]; then
  echo "error: INTERNAL_API_TOKEN пуст в $BACKEND_ENV" >&2
  exit 1
fi

curl -sS -w '\nHTTP status: %{http_code}\n' \
  -H "X-Internal-Token: $INTERNAL_TOKEN" \
  -H "X-Telegram-User-Id: $TG_ID" \
  -F "audio=@${AUDIO_FILE};type=audio/ogg" \
  -F "duration_seconds=${DURATION}" \
  -F "language=${LANG}" \
  "$BACKEND_URL/api/ask"
