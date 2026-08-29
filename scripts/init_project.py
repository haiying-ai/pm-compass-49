#!/usr/bin/env python3
"""Create a standard local project workspace without overwriting user files."""
from __future__ import annotations
import argparse, json, re
from datetime import date
from pathlib import Path

DIRS = ["00-governance/gate-records", "01-scope", "02-schedule", "03-cost", "04-quality", "05-resource", "06-communications", "07-risk", "08-procurement", "09-stakeholder", "10-execution", "11-monitoring", "12-acceptance", "13-closing", "reports"]
FILES = {
    "00-governance/charter.md": "# 项目章程\n\n- 项目目标：\n- 发起人：\n- 项目经理：\n- 成功标准：\n",
    "00-governance/management-plan.md": "# 项目管理计划\n\n待规划并经G1门禁批准。\n",
    "00-governance/decision-log.md": "# 决策日志\n\n| 日期 | 决策 | 原因/影响 | 责任人 |\n|---|---|---|---|\n",
    "07-risk/risk-register.md": "# 风险登记册\n\n| ID | 风险 | 概率 | 影响 | 应对 | 责任人 | 状态 |\n|---|---|---|---|---|---|---|\n",
    "10-execution/issue-log.md": "# 问题台账\n\n| ID | 问题 | 责任人 | 截止日期 | 状态 | 下一步 |\n|---|---|---|---|---|---|\n",
}

def safe_id(value: str) -> str:
    # Python's Unicode-aware \w keeps Chinese project names usable as IDs.
    value = re.sub(r"[^\w-]+", "-", value.strip(), flags=re.UNICODE).strip("-")
    return value or "project"

def write_if_missing(path: Path, content: str) -> bool:
    if path.exists() and path.stat().st_size > 0:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", type=Path)
    ap.add_argument("--name", required=True)
    ap.add_argument("--manager", default="")
    ap.add_argument("--sponsor", default="")
    ap.add_argument("--id", dest="project_id")
    ap.add_argument("--profile", choices=["lite", "standard", "strict"], default="standard")
    args = ap.parse_args()
    root = args.project_dir.resolve(); root.mkdir(parents=True, exist_ok=True)
    for d in DIRS: (root / d).mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    manifest = f"id: {args.project_id or safe_id(args.name)}\nname: {args.name}\nmanager: {args.manager}\nsponsor: {args.sponsor}\nmethodology: predictive\ngovernance_profile: {args.profile}\nstatus: active\ncurrent_process_group: 启动过程组\ncurrent_phase: 启动\nstart_date: {today}\ntarget_end_date:\nbaselines:\n  scope: null\n  schedule: null\n  cost: null\ntailoring_decisions: []\nlast_reviewed: {today}\n"
    created = []
    if write_if_missing(root / "project.yaml", manifest): created.append("project.yaml")
    for rel, content in FILES.items():
        if write_if_missing(root / rel, content): created.append(rel)
    catalog = Path(__file__).resolve().parents[1] / "references" / "process-catalog.zh-CN.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    state = {"schemaVersion": "1.0.0", "updated": today, "processes": [{"code": p["code"], "status": "not_started", "owner": "", "updated": ""} for p in data["processes"]], "gates": [{"id": f"G{i}", "status": "not_started", "approvedBy": "", "date": "", "notes": ""} for i in range(5)]}
    if write_if_missing(root / "00-governance/process-status.json", json.dumps(state, ensure_ascii=False, indent=2) + "\n"): created.append("00-governance/process-status.json")
    print(json.dumps({"project": str(root), "created": created, "preserved": len(DIRS) + len(FILES) + 2 - len(created)}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
