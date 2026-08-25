# Процесс разработки (SDLC средой агентов)

## Роли
| Роль | Файл агента | Читает | Пишет |
|---|---|---|---|
| superagent | CLAUDE.md | handoff, state, reports | ничего предметного |
| analyst | .claude/agents/analyst.md | spec, design artefacts, map.md | work/design/design.md, work/tasks/*, docs/map.md, docs/plan.md |
| designer | .claude/agents/designer.md | work/design/design.md | work/design/* (html/md-мокапы) |
| backend | .claude/agents/backend.md | work/tasks/<phase>-backend.md, state/backend.md | код, work/reports/<phase>-backend.md (+ API-контракт) |
| frontend | .claude/agents/frontend.md | tasks/<phase>-frontend.md, design, API-контракт | код, reports |
| qa | .claude/agents/qa.md | tasks/<phase>-qa.md, адреса сервисов | тесты, reports/<phase>-qa.md |
| security | .claude/agents/security.md | tasks/<phase>-security.md, адреса | reports/<phase>-security.md |
| devops | .claude/agents/devops.md | reports, .claude/mcp/devops.json | деплой, reports/deploy.md |
| innovator | .claude/agents/innovator.md | интернет, репо кандидатов | work/reports/innovator-*.md (ТОЛЬКО предложения) |

## Шаги
1. Хозяин: `/superagent` → «в папке лежит spec, начинай».
2. analyst → `work/design/design.md` (что должно быть в UI: экраны, данные, действия).
3. designer + хозяин → итерации до «дизайн принимаю».
4. analyst → `docs/plan.md` (фазы), `work/tasks/<phase>-<role>.md` для каждой роли, `docs/map.md`.
5. По фазе: backend → frontend → (qa ∥ security) → fix → re-check. Максимум 3 круга.
6. Фаза принята → следующая. Все фазы → хозяин смотрит MVP → devops.

## Правила экономии
- Субагент читает только свои skills (`.claude/role-skills/<role>/`) + файлы, названные в задаче. Никакого «осмотрись в проекте».
- Одна задача = один субагент. Порог задачи ~150k, жёсткий потолок 250k.
- Отчёт ≤ 1 страницы. Полные логи — в файл, в отчёте — путь.
- Супер-агент: оценка при 400k, перезагрузка до 500k (`/handoff` → `/clear` → `/kickoff`).

## Ledger
`docs/ledger.md` — таблица: дата | сессия | роль | модель | задача | in | cache_read | out | итого.
Заполняется хуком `SubagentStop` (`.claude/hooks/ledger.py`) и адаптером `tools/cursor-run.sh`.
