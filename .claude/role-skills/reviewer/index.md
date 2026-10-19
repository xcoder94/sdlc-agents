# reviewer — role skills
Independent code reviewer (model fable), invoked by the super-agent on a finished change. Read-only:
never edits app code, never commits, pushes or merges, never spawns subagents, never asks the owner directly.
Path: `.claude/role-skills/reviewer/<skill>/SKILL.md`. Never read other roles' skills.
Third-party skills are security-vetted and pinned (fx43); see each file's source header.

| skill | use when |
|---|---|
| kickoff | first step of every run |
| handoff | last step of every run (state `work/state/reviewer.md`) |
| requesting-code-review | understanding the review request you were given; `code-reviewer.md` in it is your review brief and output format — follow it on every review |
| receiving-code-review | a dev role pushed back on your findings: re-check each disputed item against the code, concede or hold with evidence |
| systematic-debugging | a finding needs a root cause (failing test, bug, odd behaviour): phases 1-3, fix recommendation only |
| systematic-debugging/root-cause-tracing.md | the symptom is deep in a call chain: trace back to the original trigger |
