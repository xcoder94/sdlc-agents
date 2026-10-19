---
name: security-handoff
description: Private handoff skill of the security role. Run before finishing every run to persist state for the next run.
---
# security — handoff

## Steps
1. Write/update `work/state/security.md` (heredoc only) with:
   - `## Where I stopped` — what was audited, what passed, what is still open.
   - `## Next action` — the first concrete step for the next run.
   - `## Unverified / stale` — findings not yet confirmed by real exploitation.
   - `## Questions for the super-agent / owner` — blocking items, if any.
2. Ensure the report `work/reports/<phase>-security.md` exists and is ≤ 1 page:
   - clean → short "no holes found".
   - findings → "N holes found" + list with severity and how to fix, plus top-3.
3. Do not print diffs or file contents to the terminal. Describe outcomes in words.

## Boundaries
- Touch only `work/state/security.md`, `work/reports/<phase>-security.md` and files the task assigned.
- Never edit another role's state, skills, or the schema in `work/db/`.
