#!/usr/bin/env python3
"""Compact supervisor for running subagents. Prints a short summary: per-subagent status,
context size, call count, errors, and a loop warning when the last calls repeat.
Project-agnostic: the session folder is computed from the project root (argv[1] or cwd)."""
import json, os, glob, time, collections, re, hashlib, sys
root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
proj = re.sub(r"[^A-Za-z0-9]", "-", root)
SUB_GLOB = os.path.expanduser(f"~/.claude/projects/{proj}/*/subagents")
now = time.time()
print(f"== agents (transcripts touched in last 30 min) — {proj}")
found = False
for f in sorted(glob.glob(f"{SUB_GLOB}/agent-*.jsonl"), key=os.path.getmtime):
    age = now - os.path.getmtime(f)
    if age > 1800:
        continue
    found = True
    aid = os.path.basename(f)[6:-6]
    calls, tokens, errors = [], 0, 0
    for ln in open(f):
        try:
            o = json.loads(ln)
        except Exception:
            continue
        m = o.get("message") or {}
        if not isinstance(m, dict):
            continue
        u = m.get("usage") or {}
        tokens = max(tokens, u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0))
        c = m.get("content")
        if isinstance(c, list):
            for x in c:
                if x.get("type") == "tool_use":
                    inp = x.get("input", {})
                    key = x.get("name", "") + ":" + (inp.get("command") or inp.get("file_path") or inp.get("pattern") or json.dumps(inp)[:80])
                    calls.append(re.sub(r"\s+", " ", key)[:100] + " #" + hashlib.md5(key.encode()).hexdigest()[:4])
                elif x.get("type") == "tool_result" and x.get("is_error"):
                    errors += 1
    last10 = calls[-10:]
    rep = collections.Counter(last10).most_common(1)
    loop = rep and rep[0][1] >= 3
    status = "DONE" if calls and calls[-1].startswith("SubagentHandback") and age > 60 else ("STALLED" if age > 600 else "ACTIVE")
    print(f"- {aid[:8]} {status} idle={int(age)}s ctx~{tokens//1000}k calls={len(calls)} errors={errors}" + (f" LOOP? x{rep[0][1]}: {rep[0][0][:90]}" if loop else ""))
    for k in calls[-3:]:
        print(f"    . {k[:110]}")
if not found:
    print("  (no active subagents in the last 30 min)")
