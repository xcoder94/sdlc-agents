---
name: designer-kickoff
description: Private kickoff skill of the designer role. Run first in every run to restore your own state and continue from where the previous run stopped.
---
# designer — kickoff

## Steps
1. Read `work/state/designer.md` if it exists. This is your own handoff from the previous run.
   If it does not exist — this is your first run; say so in one line and proceed with the task.
2. Read the task file(s) the super-agent named (usually `work/tasks/<phase>-designer.md`). Nothing else yet.
3. Compare the task with `## Where I stopped` and `## Next action` in the state file:
   - same task → continue from `Next action`; do not redo verified work.
   - new task → note in one line what the state file says is still open, then start the new task.
   - the state file contradicts the task (e.g. references files that no longer exist) → trust the
     filesystem, mark the state line `stale`, tell the super-agent in one line.
4. Re-verify anything marked `unverified` or `stale` only if the current task depends on it.
5. Only now read the other inputs your agent file allows (design, contract, schema…), and only those
   the task needs.

## Boundaries
- Read only `.claude/role-skills/designer/`. Never open another role's skills or `work/state/<other>.md`.
- No "look around the project". Navigate via `docs/map.md` when you need a path.
- If `## Questions for the super-agent / owner` in your state has unanswered items that block the task,
  return them to the super-agent immediately instead of guessing.

## Output of the kickoff
Before doing the work, tell the super-agent in ≤ 3 lines (English): first run or continuation,
what you continue from, and whether anything blocks you. Then do the task and finish with your
handoff skill (`.claude/role-skills/designer/handoff/SKILL.md`).
