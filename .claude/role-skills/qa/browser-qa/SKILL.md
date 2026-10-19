---
name: qa-browser-qa
description: Browser QA method for any web surface. Use on every QA pass that touches a web UI. Real browser, every screen, every control, gates, evidence, specs kept in repo.
---
# qa — browser QA (web)

Why: clicking through the UI as a human catches what API-level QA and code reading miss (dead controls,
media that does not play, buttons that do nothing, broken empty states). API checks are NOT a substitute
for opening the screen and using it.

## Rules (all mandatory)
1. Every screen opened in a real browser, never "verified in code".
2. Every visible control on every screen is clicked / typed / selected: buttons, tabs, chips, selects,
   text/date inputs, checkboxes, links, dialogs (open, fill, cancel; submit where safe), pagination.
   An input that sends no request and changes nothing is a bug.
3. Media is actually played: `video.play()` then `currentTime` advances, `videoWidth > 0`, `error == null`;
   before play: `paused == true`, poster set, no segment requests. If the runner's browser lacks the codec
   (`MediaSource.isTypeSupported(...)` false), note it and verify the codec check elsewhere — never mark
   playback "ok" untested.
4. Gate per screen and per click: zero console errors, zero HTTP >= 400 / failed requests, no raw i18n keys
   in the UI, no wrong-language chrome. Gate failures are bugs unless explained.
5. Screenshots are INSPECTED (Read the PNG), not just produced. Look for: black boxes, empty panes,
   wrong empty-state text, overflow, misaligned/hidden buttons, untranslated text.
6. If the app has multiple languages and/or roles, cover each: every supported language on every screen,
   and every role — each role sees exactly its allowed screens, forbidden screens show a forbidden state,
   read-only roles have no action buttons and never hit 403 merely by opening an allowed screen.
7. Run ONLY against an isolated QA environment with throwaway data. Never production, never a shared demo.
   Bring the stack down at the end.

## Industry practice kept in repo
- Smoke checklist per screen as a spec (screen x role x language + click-all crawl).
- Feature E2E specs per flow. Each owner/QA bug gets a spec that FAILS on the bug; specs for known-broken
  behaviour stay red until fixed.
- Shared gate helpers and player-check helpers factored into a lib the specs import.
- Sessions: a setup step logs in each role once using throwaway QA accounts, password from a local
  (git-ignored) env file.

## How to run
Use the project's e2e entry point (or `scripts/with_server.py` for a local server). Artifacts to
`work/qa-artifacts/e2e-<ts>/` (`results.json`, screenshots, HTML report). Parse failures from results.json;
open PNGs of every failure and at least one per screen.

## Report
Each bug: severity, screen, repro steps, evidence PNG path, failing spec name, root-cause guess (frontend/backend).
