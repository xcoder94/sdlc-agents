#!/usr/bin/env python3
# SubagentStop hook: дописывает расход токенов последнего субагента в docs/ledger.md.
import json,sys,os,glob,datetime
try: ev=json.load(sys.stdin)
except Exception: sys.exit(0)
root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sid=ev.get("session_id",""); 
sub=os.path.expanduser(f"~/.claude/projects/-home-xon-Documents-erp-assistant/{sid}/subagents")
files=sorted(glob.glob(f"{sub}/agent-*.jsonl"),key=os.path.getmtime) if os.path.isdir(sub) else []
if not files: sys.exit(0)
f=files[-1]; aid=os.path.basename(f)[6:-6]
meta=f[:-6]+".meta.json"; role="?" ; model="?"
if os.path.exists(meta):
    m=json.load(open(meta)); role=m.get("description","?")[:30]; model=m.get("model","?")
i=cr=o=0
for l in open(f):
    try: msg=json.loads(l).get("message",{})
    except: continue
    u=msg.get("usage") if isinstance(msg,dict) else None
    if u:
        i+=u.get("input_tokens",0); cr+=u.get("cache_read_input_tokens",0); o+=u.get("output_tokens",0)
ts=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M")
open(f"{root}/docs/ledger.md","a").write(f"| {ts} | {role} | {model} | {aid[:8]} | {i} | {cr} | {o} | {i+o} |\n")
