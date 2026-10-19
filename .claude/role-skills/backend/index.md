# Allowed vault skills for this role
Load a skill ONLY if the super-agent named it in your task prompt ("Skills: …").
You may load one extra skill from this list only if the task truly needs it — then name it in your report.
Path: .claude/skill-vault/<skill>/SKILL.md. Never read skills not listed here.

| skill | use when |
|---|---|
| anti-hallucinate | writing facts, APIs, versions, or claims that must be verified against sources |

# Local role skills (always available to this role)
Path: `.claude/role-skills/backend/<skill>/SKILL.md`. Third-party, security-vetted and pinned (fx43); see each file's source header.

| skill | use when |
|---|---|
| test-driven-development | every task: new behaviour or a bug fix starts with a failing test (`writing-good-tests.md` when writing/changing tests) |
| verification-before-completion | before any claim that something is done, fixed or passing — run the command, read the output |
| systematic-debugging | a bug, a failing test or unexpected behaviour: root cause before any fix (+ root-cause-tracing, condition-based-waiting, defense-in-depth, `find-polluter.sh` — worktree only, takes the heavy-job lock) |
| receiving-code-review | a task hands you reviewer / QA findings: verify each item before implementing, push back with evidence |
