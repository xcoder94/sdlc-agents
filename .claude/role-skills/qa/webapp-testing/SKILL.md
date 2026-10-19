---
name: webapp-testing
description: Toolkit for interacting with and testing web surfaces using Playwright. Verifying frontend functionality, debugging UI behavior, capturing screenshots, reading browser logs. Run against an isolated QA environment, never production.
license: Apache-2.0, complete terms in LICENSE.txt
---
<!-- Source: anthropics/skills skills/webapp-testing/SKILL.md @ dbd4588f9e1033efb41dad4bef2f7947c8993d44 (Apache-2.0, see LICENSE.txt). Generalized for the SDLC agent environment (security-vetted, fx43): black-box instruction removed, run against an isolated QA environment, output paths moved to the QA evidence dir, scripts/with_server.py patched. -->

# Web Application Testing

To test web surfaces, write native Python (or the repo's TypeScript) Playwright scripts.
This skill complements `.claude/role-skills/qa/browser-qa/SKILL.md` (the mandatory QA method); follow that
one for scope, gates and evidence.

## Rules
- Run against an **isolated QA environment** with throwaway data — never production, never a shared demo.
  Prefer running the browser in the project's containerized/CI runner over the host when the project has one.
- Do not install packages (`pip install playwright`, etc.) on the host; use the project's pinned toolchain.
- Evidence (screenshots, console logs) goes to the QA evidence dir `work/qa-artifacts/<run>/`, never `/tmp`.
  Screenshots are opened and inspected, not just produced.
- You never spawn subagents and never ask the owner directly; blockers go into your report
  (`work/reports/<phase>-qa.md`) and `work/state/qa.md`.

**Helper script**: `scripts/with_server.py` manages server lifecycle (supports multiple servers): servers run
in their own process group and are killed as a group on cleanup; output goes to DEVNULL (or `--log-dir`).
Read it before use if you need anything beyond `--help`.

## Decision Tree
```
Task → Is it static HTML (e.g. a design mockup)?
    ├─ Yes → Read HTML file directly to identify selectors → write Playwright script
    └─ No (dynamic webapp) → Is the QA server up?
        ├─ No → start it (project command) or use scripts/with_server.py for a local dev server
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: with_server.py
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  --log-dir work/qa-artifacts/<run>/server-logs \
  -- python your_automation.py
```
An automation script contains only Playwright logic (servers are managed by the helper):
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(QA_BASE_URL)                       # QA URL, passed in by env
    page.wait_for_load_state('networkidle')      # CRITICAL: wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Common Pitfall
❌ Don't inspect the DOM before waiting for `networkidle` on dynamic apps.
✅ Do `page.wait_for_load_state('networkidle')` before inspection.

## Best Practices
- Use `sync_playwright()` for synchronous scripts; always close the browser.
- Descriptive selectors: `text=`, `role=`, CSS, or IDs. Prefer `wait_for_selector()` over fixed timeouts.
- Capture console with `page.on("console", ...)` into `work/qa-artifacts/<run>/console.log`.

(The upstream `examples/` directory is not copied: it wrote to host `/tmp` and `/mnt/user-data/outputs`.)
