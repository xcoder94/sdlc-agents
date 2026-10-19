#!/usr/bin/env python3
# SubagentStop hook: upsert расхода последнего субагента в docs/ledger.md (через ledger_common).
import json, sys, os, glob, datetime
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(root, "tools"))
import ledger_common
try: ev = json.load(sys.stdin)
except Exception: sys.exit(0)
sid = ev.get("session_id", "")
# Папка сессий Claude Code: абсолютный путь корня проекта, где все не-буквенно-цифровые
# символы заменены на "-". Так хук работает в любом проекте, а не только в одном захардкоженном.
import re
proj = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(root))
sub = os.path.expanduser(f"~/.claude/projects/{proj}/{sid}/subagents")
files = sorted(glob.glob(f"{sub}/agent-*.jsonl"), key=os.path.getmtime) if os.path.isdir(sub) else []
if not files: sys.exit(0)
f = files[-1]; aid = os.path.basename(f)[6:-6]
meta = f[:-6] + ".meta.json"; task = "?"; model = "?"
if os.path.exists(meta):
    m = json.load(open(meta)); task = m.get("description", "?")[:40]; model = m.get("model", "?")
i = cr = o = 0
for l in open(f):
    try: msg = json.loads(l).get("message", {})
    except: continue
    u = msg.get("usage") if isinstance(msg, dict) else None
    if u:
        i += u.get("input_tokens", 0); cr += u.get("cache_read_input_tokens", 0); o += u.get("output_tokens", 0)
ts = datetime.datetime.now(datetime.UTC).strftime("%d.%m.%Y %H:%M")
ledger_common.upsert(root, aid, ts, "субагент", model, task, i, cr, o)
