#!/usr/bin/env python3
"""Summarize process completion by group or inspect one process code."""
from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir", type=Path); ap.add_argument("--code"); ap.add_argument("--json", action="store_true"); args=ap.parse_args()
    root=args.project_dir.resolve(); base=Path(__file__).resolve().parents[1]
    catalog=json.loads((base/"references/process-catalog.zh-CN.json").read_text(encoding="utf-8"))
    state=json.loads((root/"00-governance/process-status.json").read_text(encoding="utf-8"))
    statuses={x["code"]:x for x in state.get("processes",[])}
    if args.code:
        needle=args.code.lower()
        exact=[x for x in catalog["processes"] if x["code"]==args.code or x["nameZh"]==args.code or x["nameEn"].lower()==needle]
        matches=exact or [x for x in catalog["processes"] if needle in (x["nameZh"] + " " + x["nameEn"].lower() + " " + " ".join(x.get("keywordsZh",[]) + x.get("keywordsEn",[])).lower())]
        if not matches: raise SystemExit(f"未找到过程或关键词: {args.code}")
        if len(matches) > 1:
            out={"query":args.code,"matches":[{"code":x["code"],"nameZh":x["nameZh"],"nameEn":x["nameEn"],"status":statuses.get(x["code"],{}).get("status","not_started")} for x in matches]}
        else: out={"process":matches[0],"status":statuses.get(matches[0]["code"],{})}
    else:
        summary=defaultdict(Counter)
        for p in catalog["processes"]: summary[p["processGroup"]][statuses.get(p["code"],{}).get("status","not_started")]+=1
        out={"total":len(catalog["processes"]),"byProcessGroup":{k:dict(v) for k,v in summary.items()},"gates":state.get("gates",[])}
    if args.json: print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
    if args.code:
        if "matches" in out:
            print(f"关键词‘{out['query']}’匹配 {len(out['matches'])} 个过程：")
            for x in out["matches"]: print(f"{x['code']} {x['nameZh']}：{x['status']}")
        else: print(f"{out['process']['code']} {out['process']['nameZh']}：{out['status'].get('status','not_started')}")
    else:
        print(f"过程总数：{out['total']}")
        for group, counts in out["byProcessGroup"].items(): print(f"{group}: " + ", ".join(f"{k}={v}" for k,v in counts.items()))
    return 0

if __name__ == "__main__": raise SystemExit(main())
