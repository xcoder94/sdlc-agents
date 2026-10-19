---
name: reviewer-handoff
description: Private handoff skill of the reviewer role. Run before finishing any run, so the next run of reviewer continues from exactly where it stopped.
---
# reviewer — handoff

Rewrite `work/state/reviewer.md` as a **snapshot** of your work. Only you read it. Write in English.

## Rules
- Only what you **verified** in this run (read the code, ran a command, read output). Everything else is
  marked `unverified`.
- Do not retell code, spec or the diff — reference by path, line and SHA.
- Delete stale lines; do not append history. ≤ 80 lines.
- Absolute dates only (e.g. 2026-10-18).
- Write via bash heredoc (`cat > work/state/reviewer.md <<'EOF'`), never Write/Edit. No diffs in the terminal.
- Before writing: remove any `.claude/worktrees/review-<sha>` worktree you created.

## Sections (in this order)
1. `## Where I stopped` — one paragraph: what was being reviewed and how far it got.
2. `## Next action` — exactly one concrete next step, with the file, SHA or command to start from.
3. `## Role facts` — the items below, each on its own line:
- Review request / task file, branch, BASE..HEAD SHAs reviewed.
- Verdict given (Yes / No / With fixes) and the report path.
- Open findings by severity (Critical / Important / Minor); findings re-checked and closed.
- Disputed findings (dev pushback) and their status.
4. `## Decisions` — decisions made in this run with a one-line "why".
5. `## Caution` — unverified, misleading, known pitfalls, parts of the diff not reviewed.
6. `## Questions for the super-agent / owner` — numbered; empty section if none.

## After writing
Report to the super-agent in ≤ 5 lines: verdict, the report path, and
"state saved to work/state/reviewer.md". Do not paste the state file.
