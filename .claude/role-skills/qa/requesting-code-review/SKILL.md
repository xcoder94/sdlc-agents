---
name: requesting-code-review
description: Use when completing tasks or implementing major features, to get the work reviewed against its requirements — by returning a review request to the super-agent, never by spawning a reviewer yourself
---
<!-- Source: obra/superpowers skills/requesting-code-review/SKILL.md @ bb92a77741419a4ab5f06e711a283343f1ada0c3 (MIT, Copyright (c) 2025 Jesse Vincent). Adapted (security-vetted, fx43) (edits 1, 4): "dispatch a general-purpose subagent" -> "return a review request to the super-agent"; "Before merge to main" dropped; subagent-driven-development references dropped (not adopted). -->

# Requesting Code Review

Get an independent reviewer to catch issues before they cascade. In this project roles never spawn
subagents: you **return a review request to the super-agent**, and the super-agent invokes the
reviewer role with [code-reviewer.md](code-reviewer.md). The reviewer gets precisely crafted context
for evaluation — never your session's history.

**Core principle:** Review early, review often.

## Environment rules
- You are a role run by the super-agent. You never spawn subagents and never ask the owner directly.
  Every ambiguity or "ask your human partner" moment goes into your report
  (`work/reports/<phase>-<role>.md`) and into `## Questions for the super-agent / owner` in your state file.
- No push, no merge to main. Work only within the scope your task defines.
- Run tests and builds with the project's own commands (find them via `docs/map.md`).

## When to Request Review

**Mandatory:**
- After completing a major feature or a task the super-agent marked for review

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs (on your branch, inside your worktree):**
```bash
BASE_SHA=$(git merge-base main HEAD)   # or the commit before your task
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Return a review request to the super-agent.** Put it in your report
(`work/reports/<phase>-<role>.md`) under `## Review request`, filling the placeholders of
[code-reviewer.md](code-reviewer.md):

- `[DESCRIPTION]` - Brief summary of what you built
- `[PLAN_OR_REQUIREMENTS]` - What it should do (task file path, spec section)
- `[BASE_SHA]` - Starting commit
- `[HEAD_SHA]` - Ending commit
- Branch / worktree name

Then finish your run (handoff skill). Do not wait in a loop for the review.

**3. Act on feedback** (it comes back through the super-agent in a later task):
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning, in your report)

## Example

```
[Just completed Task 2: Add verification function]

## Review request
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: work/tasks/fx43-backend.md, task 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  BRANCH: fx43-backend (worktree .claude/worktrees/fx43-backend)

[Later the super-agent hands back the reviewer's findings]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to accept with fixes

[Next task: fix progress indicators, then continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of requesting a reviewer" | A self-review is not an independent review. Request one; the super-agent decides whether it runs. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context (task path, SHAs, summary), never your session's history. That keeps the reviewer on the work product, not your thought process. |
| "I'll spawn a reviewer subagent myself, it's faster" | Roles never spawn agents. Return the request. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
- Push or merge — acceptance and merge are the super-agent's call

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification (in your report)

See template at: [code-reviewer.md](code-reviewer.md)
