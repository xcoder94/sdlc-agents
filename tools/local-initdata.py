#!/usr/bin/env python3
"""fix16: генерирует валидную Telegram WebApp initData, подписанную реальным
токеном бота (services/bot/.env или services/backend/.env, TELEGRAM_BOT_TOKEN),
чтобы локально (без Telegram) открыть мини-апп и получить не-401 ответ от
backend.

Алгоритм подписи — тот, что использует сам Telegram и что проверяет
services/backend/app/auth/telegram.py:verify_init_data:
    secret_key = HMAC_SHA256(key=b"WebAppData", msg=bot_token)
    hash = HMAC_SHA256(key=secret_key, msg=data_check_string).hexdigest()

Использование:
    tools/local-initdata.py [--telegram-id 555001] [--name "Иван Петров"] [--lang ru]

Выводит:
    - строку initData (для X-Telegram-Init-Data / localStorage)
    - готовый URL http://127.0.0.1:8080/#tgWebAppData=<urlencoded initData>
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import time
import urllib.parse
from pathlib import Path

# NB: tools/ is a symlink shared across sibling repos in this environment --
# do NOT .resolve() __file__ (that would follow the symlink to the wrong
# repo). Anchor on cwd if it looks like this repo, else fall back to the
# unresolved script path.
if (Path.cwd() / "services" / "bot" / "config.py").exists():
    REPO_ROOT = Path.cwd()
else:
    REPO_ROOT = Path(__file__).parent.parent


def _read_env_var(env_path: Path, name: str) -> str | None:
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == name:
            return value.strip()
    return None


def find_bot_token() -> str:
    for rel in ("services/bot/.env", "services/backend/.env"):
        value = _read_env_var(REPO_ROOT / rel, "TELEGRAM_BOT_TOKEN")
        if value:
            return value
    raise SystemExit(
        "error: TELEGRAM_BOT_TOKEN не найден ни в services/bot/.env, ни в "
        "services/backend/.env -- впишите реальный токен бота туда."
    )


def build_init_data(bot_token: str, telegram_id: int, first_name: str, last_name: str, lang: str) -> str:
    user = {
        "id": telegram_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": f"user{telegram_id}",
        "language_code": lang,
        "allows_write_to_pm": True,
    }
    params = {
        "query_id": f"AAH_local_{telegram_id}",
        "user": json.dumps(user, ensure_ascii=False, separators=(",", ":")),
        "auth_date": str(int(time.time())),
    }
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    signature = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["hash"] = signature
    return urllib.parse.urlencode(params)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--telegram-id", type=int, default=555001)
    parser.add_argument("--name", default="Иван Петров", help="'Имя Фамилия', по умолчанию кириллическое")
    parser.add_argument("--lang", default="ru")
    parser.add_argument("--miniapp-url", default=os.environ.get("MINIAPP_LOCAL_URL", "http://127.0.0.1:8080"))
    args = parser.parse_args()

    parts = args.name.split(maxsplit=1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    bot_token = find_bot_token()
    init_data = build_init_data(bot_token, args.telegram_id, first_name, last_name, args.lang)

    print("initData:")
    print(init_data)
    print()
    print("URL (открыть в обычном браузере):")
    print(f"{args.miniapp_url.rstrip('/')}/#tgWebAppData={urllib.parse.quote(init_data, safe='')}")


if __name__ == "__main__":
    main()
