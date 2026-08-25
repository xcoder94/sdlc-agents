#!/usr/bin/env bash
# Установщик агентной среды SDLC в проект — через СИМЛИНКИ.
# Файлы среды остаются в этом репо; в проекте создаются симлинки на них.
# Правишь среду здесь → изменения сразу видны во всех проектах.
#   ./install.sh /path/to/target-project
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="${1:?Укажи целевую папку проекта}"
DST="$(cd "$DST" && pwd)"
mkdir -p "$DST"

link() {
  local rel="$1"
  mkdir -p "$DST/$(dirname "$rel")"
  rm -rf "$DST/$rel"
  ln -s "$SRC/$rel" "$DST/$rel"
}

# Симлинки на артефакты СРЕДЫ
link CLAUDE.md
link install.sh
link tools
link docs/process.md
link .claude/agents
link .claude/commands
link .claude/hooks
link .claude/mcp
link .claude/role-skills
link .claude/settings.json

# Локальный (не симлинк) каркас продукта — живёт в самом проекте
mkdir -p "$DST/work/tasks" "$DST/work/reports" "$DST/work/state" "$DST/work/design" "$DST/docs/context"
for d in tasks reports state design; do touch "$DST/work/$d/.gitkeep"; done
[ -f "$DST/docs/ledger.md" ] || printf '# Token ledger\n\n| datetime (UTC) | who | model | task | input | cache_read | output | total |\n|---|---|---|---|---|---|---|---|\n' > "$DST/docs/ledger.md"

echo "Среда подключена симлинками в: $DST"
echo "Дальше: cd $DST && claude → /superagent"
