#!/usr/bin/env bash
# Установщик агентной среды SDLC в проект.
# Копирует ТОЛЬКО файлы среды (не код продукта) в целевую папку.
# Использование:
#   ./install.sh /path/to/target-project      # локально из этого репо
#   curl -fsSL <raw-url>/install.sh | bash -s /path/to/target   # из git (когда среда в репо)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="${1:?Укажи целевую папку проекта}"
mkdir -p "$DST"
# Файлы СРЕДЫ (переносимые). Код продукта тут не участвует.
copy() { mkdir -p "$DST/$(dirname "$1")"; cp -r "$SRC/$1" "$DST/$(dirname "$1")/"; }
copy CLAUDE.md
copy .claude/agents
copy .claude/commands
copy .claude/hooks
copy .claude/mcp
copy .claude/settings.json
copy .claude/role-skills
copy tools
copy docs/process.md
# Пустой каркас рабочих папок (артефакты продукта появятся тут при работе)
mkdir -p "$DST/work/tasks" "$DST/work/reports" "$DST/work/state" "$DST/work/design" "$DST/docs/context"
[ -f "$DST/docs/ledger.md" ] || printf '# Token ledger\n\n| datetime (UTC) | who | model | task | input | cache_read | output | total |\n|---|---|---|---|---|---|---|---|\n' > "$DST/docs/ledger.md"
echo "Среда установлена в: $DST"
echo "Дальше: cd $DST && claude → /superagent"
