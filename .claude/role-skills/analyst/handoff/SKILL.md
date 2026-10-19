---
name: analyst-handoff
description: Private handoff skill of the analyst role. Run before finishing any run, so the next run of analyst (or the owner in a direct session) continues from exactly where it stopped.
---
# analyst — handoff

Rewrite `work/state/analyst.md` as a **snapshot** of your work. Only you read it. Write in English.

## Rules
- Only what you **verified** in this run (ran a command, read output, got an explicit owner decision).
  Everything else is marked `unverified`.
- Do not retell code, spec or design — reference by path (and line when useful). They are cheaper to re-read.
- Delete stale lines; do not append history. ≤ 80 lines.
- Absolute dates only (e.g. 2026-09-22).
- Write via bash heredoc (`cat > work/state/analyst.md <<'EOF'`), never Write/Edit. No diffs in the terminal.

## Sections (in this order)
1. `## Where I stopped` — one paragraph: what was being done at the moment of stopping and how far it got.
2. `## Next action` — exactly one concrete next step, with the file or command to start from.
3. `## Role facts` — the items below, each on its own line:
- Which mode you were in (spec / design.md / plan) and which phase.
- Which artifacts exist and are final vs draft: docs/spec.md, work/design/design.md, docs/plan.md, docs/map.md, work/tasks/*.
- Open product questions the owner has not answered yet (numbered).
- Tasks still to be written or split (with target role and phase).
4. `## Decisions` — decisions made in this run with a one-line "why".
5. `## Caution` — unverified, misleading, known pitfalls, things that looked done but were not.
6. `## Questions for the super-agent / owner` — numbered; empty section if none.

## After writing
Report to the super-agent in ≤ 5 lines: result of the run, the report path (if any), and
"state saved to work/state/analyst.md". Do not paste the state file.
