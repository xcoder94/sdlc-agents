---
name: security-kickoff
description: Private kickoff skill of the security role. Run first in every run to restore your own state and select only the skills the current task needs.
---
# security — kickoff

## Steps
1. Read `work/state/security.md` if it exists. This is your own handoff from the previous run.
   If it does not exist — this is your first run; say so in one line and proceed.
2. Read the task file(s) the super-agent named (usually `work/tasks/<phase>-security.md`). Nothing else yet.
3. Compare the task with `## Where I stopped` and `## Next action` in the state file:
   - same task → continue from `Next action`; do not redo verified findings.
   - new task → note in one line what is still open, then start the new task.
   - state contradicts the filesystem → trust the filesystem, mark the line `stale`, tell the super-agent.
4. Learn the code layout only via `docs/map.md`; read only the relevant sources, not the whole repo.

## Skill selection (mandatory)
Read `.claude/role-skills/security/INDEX.md` — and only that — to decide which skills apply. Open an
individual `SKILL.md` ONLY when the current task matches its "when to apply" row. Reading the whole
skills folder, or any `SKILL.md` not selected via INDEX, is forbidden. If no row matches, open none
and proceed.

## Boundaries
- Read only `.claude/role-skills/security/`. Never open another role's skills or `work/state/<other>.md`.
- No "look around the project". Navigate via `docs/map.md` when you need a path.
- If `## Questions for the super-agent / owner` in your state has unanswered blocking items, return
  them to the super-agent immediately instead of guessing.

## Output of the kickoff
Before doing the work, tell the super-agent in ≤ 3 lines (English): first run or continuation, what
you continue from, which skills you selected from INDEX. Then do the task and finish with your handoff
skill (`.claude/role-skills/security/handoff/SKILL.md`).
