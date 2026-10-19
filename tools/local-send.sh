#!/usr/bin/env bash
# fix16: отправляет готовые Telegram-апдейты напрямую в POST /webhook локально
# запущенного бота, с верным X-Telegram-Bot-Api-Secret-Token.
#
# Использование:
#   tools/local-send.sh start   [TELEGRAM_ID] [ИМЯ]
#   tools/local-send.sh text    "<вопрос>" [TELEGRAM_ID] [ИМЯ]
#   tools/local-send.sh approve TARGET_TELEGRAM_ID [ADMIN_TELEGRAM_ID]
#   tools/local-send.sh reject  TARGET_TELEGRAM_ID [ADMIN_TELEGRAM_ID]
#   tools/local-send.sh revoke  TARGET_TELEGRAM_ID [ADMIN_TELEGRAM_ID]
#
# Секрет берётся из services/bot/.env (WEBHOOK_SECRET), URL бота — из BOT_URL
# (по умолчанию http://127.0.0.1:8002).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BOT_ENV="$REPO_ROOT/services/bot/.env"
BOT_URL="${BOT_URL:-http://127.0.0.1:8002}"

if [[ ! -f "$BOT_ENV" ]]; then
  echo "error: $BOT_ENV не найден" >&2
  exit 1
fi
WEBHOOK_SECRET="$(grep '^WEBHOOK_SECRET=' "$BOT_ENV" | head -1 | cut -d= -f2-)"
if [[ -z "$WEBHOOK_SECRET" ]]; then
  echo "error: WEBHOOK_SECRET пуст в $BOT_ENV" >&2
  exit 1
fi

CMD="${1:-}"
UPDATE_ID=$RANDOM$RANDOM

send() {
  local body="$1"
  curl -sS -o /tmp_response_body 2>/dev/null || true
  local resp
  resp="$(curl -sS -w '\n%{http_code}' \
    -H "Content-Type: application/json" \
    -H "X-Telegram-Bot-Api-Secret-Token: $WEBHOOK_SECRET" \
    -d "$body" \
    "$BOT_URL/webhook")"
  echo "$resp"
}

case "$CMD" in
  start)
    TG_ID="${2:-1001}"
    NAME="${3:-Иван Петров}"
    FIRST="${NAME%% *}"
    LAST="${NAME#* }"
    [[ "$LAST" == "$NAME" ]] && LAST=""
    BODY=$(cat <<JSON
{"update_id": $UPDATE_ID, "message": {"message_id": 1, "date": $(date +%s),
 "chat": {"id": $TG_ID, "type": "private"},
 "from": {"id": $TG_ID, "is_bot": false, "first_name": "$FIRST", "last_name": "$LAST", "language_code": "ru"},
 "text": "/start"}}
JSON
)
    send "$BODY"
    ;;

  text)
    QUESTION="${2:-Остатки по складу}"
    TG_ID="${3:-1001}"
    NAME="${4:-Иван Петров}"
    FIRST="${NAME%% *}"
    LAST="${NAME#* }"
    [[ "$LAST" == "$NAME" ]] && LAST=""
    # экранируем кавычки в вопросе для JSON
    Q_ESCAPED=$(printf '%s' "$QUESTION" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])')
    BODY=$(cat <<JSON
{"update_id": $UPDATE_ID, "message": {"message_id": 2, "date": $(date +%s),
 "chat": {"id": $TG_ID, "type": "private"},
 "from": {"id": $TG_ID, "is_bot": false, "first_name": "$FIRST", "last_name": "$LAST", "language_code": "ru"},
 "text": "$Q_ESCAPED"}}
JSON
)
    send "$BODY"
    ;;

  approve|reject|revoke)
    TARGET_ID="${2:?нужен TARGET_TELEGRAM_ID}"
    ADMIN_ID="${3:-1001}"
    BODY=$(cat <<JSON
{"update_id": $UPDATE_ID, "callback_query": {"id": "cb$UPDATE_ID",
 "from": {"id": $ADMIN_ID, "is_bot": false, "first_name": "Admin", "language_code": "ru"},
 "message": {"message_id": 3, "date": $(date +%s), "chat": {"id": $ADMIN_ID, "type": "private"},
   "from": {"id": 0, "is_bot": true, "first_name": "bot"}},
 "chat_instance": "1", "data": "admin:$CMD:$TARGET_ID"}}
JSON
)
    send "$BODY"
    ;;

  *)
    echo "Использование: $0 {start|text|approve|reject|revoke} ..." >&2
    exit 2
    ;;
esac
