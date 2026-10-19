# Процесс разработки (SDLC средой агентов)

## Роли
| Роль | Файл агента | Читает | Пишет |
|---|---|---|---|
| superagent | CLAUDE.md | handoff, state, reports | ничего предметного |
| analyst | .claude/agents/analyst.md | spec, design artefacts, map.md | work/design/design.md, work/tasks/*, docs/map.md, docs/plan.md |
| designer | .claude/agents/designer.md | work/design/design.md | work/design/* (html/md-мокапы) |
| db-architect | .claude/agents/db-architect.md | tasks/<phase>-db-architect.md, design, spec (нефункц.) | work/db/* (schema/capacity/ops + миграции), reports |
| backend | .claude/agents/backend.md | work/tasks/<phase>-backend.md, state/backend.md | код, work/reports/<phase>-backend.md (+ API-контракт) |
| mobile | .claude/agents/mobile.md | tasks/<phase>-mobile.md, design, API-контракт | код приложения, reports/<phase>-mobile.md |
| frontend | .claude/agents/frontend.md | tasks/<phase>-frontend.md, design, API-контракт | код, reports |
| qa | .claude/agents/qa.md | tasks/<phase>-qa.md, адреса сервисов | тесты, reports/<phase>-qa.md |
| security | .claude/agents/security.md | tasks/<phase>-security.md, адреса | reports/<phase>-security.md |
| reviewer | .claude/agents/reviewer.md | задача ревью, map.md, отчёты неудачных фиксов | work/reviews/<id>.md, reports/<id>.md (только инструкции, не код) |
| devops | .claude/agents/devops.md | reports, .claude/mcp/devops.json | деплой, reports/deploy.md |
| innovator | .claude/agents/innovator.md | интернет, репо кандидатов | work/reports/innovator-*.md (ТОЛЬКО предложения) |

mobile — универсальная роль мобильной разработки (Flutter / React Native / KMP или нативно);
стек выбирается с хозяином один раз и пишется в `docs/map.md`. frontend подключается, если есть веб-поверхность.
reviewer — независимый ревьюер (модель fable): вызывается, когда баг пережил 2–3 попытки фикса или по запросу; код не пишет.

## Шаги
1. Хозяин: `/superagent` → «в папке лежит spec, начинай».
2. analyst → `work/design/design.md` (что должно быть в UI: экраны, данные, действия).
3. designer + хозяин → итерации до «дизайн принимаю».
4. analyst → `docs/plan.md` (фазы), `work/tasks/<phase>-<role>.md` для каждой роли, `docs/map.md`.
5. db-architect → `work/db/*` (один раз: схема/ёмкость/ops; далее дельты по фазам).
6. По фазе: backend → mobile (∥ frontend, если есть веб) → (qa ∥ security) → fix → re-check. Максимум 3 круга.
   Если баг пережил круги — подключается reviewer с инструкцией по корню проблемы.
7. Фаза принята → следующая. Все фазы → хозяин смотрит MVP → security-аудит перед релизом → devops.

## Непрерывность (kickoff/handoff)
- Каждый субагент в начале запуска выполняет свой `.claude/role-skills/<role>/kickoff/SKILL.md`
  (восстанавливает `work/state/<role>.md`), в конце — `.claude/role-skills/<role>/handoff/SKILL.md`.
- Супер-агент при вызове роли всегда говорит: «сделай kickoff в начале, handoff перед завершением».

## Правила экономии
- Субагент читает только свои skills (`.claude/role-skills/<role>/`) + файлы, названные в задаче. Никакого «осмотрись в проекте».
- Одна задача = один субагент. Порог задачи ~150k, жёсткий потолок 250k.
- Отчёт ≤ 1 страницы. Полные логи — в файл, в отчёте — путь.
- Супер-агент: оценка при 400k, перезагрузка до 500k (`/handoff` → `/clear` → `/kickoff`).

## Скиллы
- `.claude/role-skills/<role>/` — изолированы по ролям; `index.md` (или `INDEX.md` у security) перечисляет, что роли доступно.
- `.claude/skill-vault/` — общий реестр vetted-скиллов (одна копия каждого); проверка `cd .claude/skill-vault && sha256sum -c SHA256SUMS`.

## Ledger
`docs/ledger.md` — таблица: дата | сессия/роль | модель | задача | in | cache_read | out | итого.
Заполняется хуком `SubagentStop` (`.claude/hooks/ledger.py`) и адаптером `tools/cursor-run.sh`.
