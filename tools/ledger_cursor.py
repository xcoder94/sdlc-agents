#!/usr/bin/env python3
# Читает JSON cursor-agent из stdin, дописывает строку в docs/ledger.md, печатает result.
# argv: <role> <model> <root>
import sys, json, datetime
role, model, root = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(sys.stdin)
u = d.get("usage", {})
i = u.get("inputTokens", 0); cr = u.get("cacheReadTokens", 0); o = u.get("outputTokens", 0)
ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M")
sid = (d.get("session_id") or "")[:8]
row = f"| {ts} | {role} (cursor) | {model} | {sid} | {i} | {cr} | {o} | {i+o} |\n"
with open(f"{root}/docs/ledger.md", "a") as f:
    f.write(row)
print(d.get("result", ""))
