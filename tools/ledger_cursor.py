#!/usr/bin/env python3
# Читает JSON cursor-agent из stdin, upsert строки в docs/ledger.md, печатает result.
# argv: <role> <model> <root>
import sys, json, datetime, os
role, model, root = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(root, "tools"))
import ledger_common
d = json.load(sys.stdin)
u = d.get("usage", {})
i = u.get("inputTokens", 0); cr = u.get("cacheReadTokens", 0); o = u.get("outputTokens", 0)
ts = datetime.datetime.now(datetime.UTC).strftime("%d.%m.%Y %H:%M")
sid = (d.get("session_id") or ts)
ledger_common.upsert(root, f"cursor:{sid}", ts, f"{role} (cursor)", model, role, i, cr, o)
print(d.get("result", ""))
