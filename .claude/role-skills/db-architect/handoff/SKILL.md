---
name: db-architect-handoff
description: Private handoff skill of the db-architect role. Run before finishing any run, so the next run of db-architect (or the owner in a direct session) continues from exactly where it stopped.
---
# db-architect — handoff

Rewrite `work/state/db-architect.md` as a **snapshot** of your work. Only you read it. Write in English.

## Rules
- Only what you **verified** in this run (ran a command, read output, got an explicit owner decision).
  Everything else is marked `unverified`.
- Do not retell code, spec or design — reference by path (and line when useful). They are cheaper to re-read.
- Delete stale lines; do not append history. ≤ 80 lines.
- Absolute dates only (e.g. 2026-09-22).
- Write via bash heredoc (`cat > work/state/db-architect.md <<'EOF'`), never Write/Edit. No diffs in the terminal.

## Sections (in this order)
1. `## Where I stopped` — one paragraph: what was being done at the moment of stopping and how far it got.
2. `## Next action` — exactly one concrete next step, with the file or command to start from.
3. `## Role facts` — the items below, each on its own line:
- Mode (initial / delta / review) and phase.
- Engine, hosting and retention decisions: confirmed by owner or still proposed.
- Which of work/db/schema.md, capacity.md, ops.md are current; which tables lack a growth cap.
- Pending backend proposals in work/db/proposals/ and your verdict on each.
- Migrations written and whether they were applied locally.
4. `## Decisions` — decisions made in this run with a one-line "why".
5. `## Caution` — unverified, misleading, known pitfalls, things that looked done but were not.
6. `## Questions for the super-agent / owner` — numbered; empty section if none.

## After writing
Report to the super-agent in ≤ 5 lines: result of the run, the report path (if any), and
"state saved to work/state/db-architect.md". Do not paste the state file.
