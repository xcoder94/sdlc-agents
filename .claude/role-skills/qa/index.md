# Allowed vault skills for this role
Load a skill ONLY if the super-agent named it in your task prompt ("Skills: …").
You may load one extra skill from this list only if the task truly needs it — then name it in your report.
Path: .claude/skill-vault/<skill>/SKILL.md. Never read skills not listed here.

| skill | use when |
|---|---|
| anti-hallucinate | writing facts, APIs, versions, or claims that must be verified against sources |

# Local role skills (always available to this role)
Path: `.claude/role-skills/qa/<skill>/SKILL.md`. Third-party skills are security-vetted and pinned (fx43); see each file's source header.

| skill | use when |
|---|---|
| browser-qa | every QA pass that touches a web UI (mandatory method) |
| verification-before-completion | before reporting any bug closed, any suite green, any screen verified — fresh evidence only |
| requesting-code-review | you want an independent code review of a change: return a review request to the super-agent (`code-reviewer.md` is the reviewer brief) |
| webapp-testing | writing Playwright scripts for a web surface — against an isolated QA environment; `scripts/with_server.py` for local servers inside the container |
