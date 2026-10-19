---
name: backend-handoff
description: Private handoff skill of the backend role. Run before finishing any run, so the next run of backend (or the owner in a direct session) continues from exactly where it stopped.
---
# backend — handoff

Rewrite `work/state/backend.md` as a **snapshot** of your work. Only you read it. Write in English.

## Rules
- Only what you **verified** in this run (ran a command, read output, got an explicit owner decision).
  Everything else is marked `unverified`.
- Do not retell code, spec or design — reference by path (and line when useful). They are cheaper to re-read.
- Delete stale lines; do not append history. ≤ 80 lines.
- Absolute dates only (e.g. 2026-09-22).
- Write via bash heredoc (`cat > work/state/backend.md <<'EOF'`), never Write/Edit. No diffs in the terminal.

## Sections (in this order)
1. `## Where I stopped` — one paragraph: what was being done at the moment of stopping and how far it got.
2. `## Next action` — exactly one concrete next step, with the file or command to start from.
3. `## Role facts` — the items below, each on its own line:
- Phase, task file, which endpoints are done / in progress / not started.
- Whether the service starts locally and how (command, port, env vars needed).
- API contract: written to the report or not; breaking changes since the last contract.
- Schema change proposals waiting for db-architect.
- Bugs from QA / security reports fixed vs still open.
4. `## Decisions` — decisions made in this run with a one-line "why".
5. `## Caution` — unverified, misleading, known pitfalls, things that looked done but were not.
6. `## Questions for the super-agent / owner` — numbered; empty section if none.

## After writing
Report to the super-agent in ≤ 5 lines: result of the run, the report path (if any), and
"state saved to work/state/backend.md". Do not paste the state file.
