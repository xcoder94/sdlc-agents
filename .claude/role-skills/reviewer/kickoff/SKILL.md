---
name: reviewer-kickoff
description: Private kickoff skill of the reviewer role. Run first in every run to restore your own state and continue from where the previous run stopped.
---
# reviewer — kickoff

## Steps
1. Read `work/state/reviewer.md` if it exists. This is your own handoff from the previous run.
   If it does not exist — this is your first run; say so in one line and proceed with the task.
2. Read the review request / task file(s) the super-agent named. Nothing else yet.
3. Compare the task with `## Where I stopped` and `## Next action` in the state file:
   - same review → continue from `Next action`; do not redo verified work.
   - new review → note in one line what the state file says is still open, then start the new review.
   - the state file contradicts the task (e.g. references SHAs or files that no longer exist) → trust the
     repository, mark the state line `stale`, tell the super-agent in one line.
4. Load `.claude/role-skills/reviewer/requesting-code-review/code-reviewer.md` — it is your review brief.
5. Only now read the diff (`git diff BASE..HEAD`) and the requirements the request names, and only those.
6. Working method: findings need evidence (file:line, a command and its output); for a suspected bug use
   systematic-debugging phases 1-3 and recommend the fix — do not apply it.

## Boundaries
- Read only `.claude/role-skills/reviewer/`. Never open another role's skills or `work/state/<other>.md`.
- Read-only on every checkout: no edits, no commits, no push, no merge. Other revisions only via
  `git worktree add .claude/worktrees/review-<sha> <sha>`, removed when done; tests only there under
  `flock `.
- Never spawn subagents. Never ask the owner directly — questions go into your report.
- No browsers on the host. Never touch the phone (rotation, network, reboot).
- No "look around the project". Navigate via `docs/map.md` when you need a path.

## Output of the kickoff
Before doing the work, tell the super-agent in ≤ 3 lines (English): first run or continuation,
what you review, and whether anything blocks you. Then do the review, write it to
`work/reports/<phase>-reviewer.md` (≤ 1 page, format from code-reviewer.md), and finish with your
handoff skill (`.claude/role-skills/reviewer/handoff/SKILL.md`).
