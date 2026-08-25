# ERP-Assistant — агентная среда SDLC

Один spec → MVP силами субагентов. Человек участвует только в продукте, дизайне и приёмке.

## Установка в проект
```bash
git clone <this-repo> erp-assistant-env
./erp-assistant-env/install.sh /path/to/your-project
cd /path/to/your-project
claude
/superagent
```
Работает на связке Claude ($20) + Cursor CLI ($20): дорогие роли (analyst/qa/security) — Opus,
код (backend/frontend) — через Cursor (grok/composer/sonnet). Проверка кода — QA + security.

## Что внутри среды (переносится install.sh)
- `CLAUDE.md` — правила супер-агента (оркестратор).
- `.claude/agents/` — 8 субагентов (analyst, designer, backend, frontend, qa, security, devops, innovator).
- `.claude/role-skills/<role>/` — скиллы, изолированные по ролям (другие агенты их не видят).
- `.claude/commands/` — `/superagent`, `/handoff`, `/kickoff`.
- `.claude/hooks/ledger.py` + `docs/ledger.md` — учёт токенов.
- `tools/cursor-run.sh` — адаптер сторонних моделей через Cursor CLI.
- `docs/process.md` — процесс и роли.

## Продукт vs среда
Код продукта появляется в проекте при работе (свои папки). Файлы среды — только перечисленные выше,
плюс рабочие артефакты в `work/`. Обновить среду — перезапустить `install.sh` (перезапишет файлы среды,
код продукта не тронет). Извлечь среду в новый проект — тот же `install.sh` на пустую папку.

## Опционально: entire.io Checkpoints (история сессий агентов)
```bash
brew install --cask entire   # или: curl -fsSL https://entire.io/install.sh | bash
entire enable
```
