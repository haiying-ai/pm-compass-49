#!/usr/bin/env python3
"""Generate a Markdown status report from project files; writing requires --output."""
from __future__ import annotations
import argparse, json
from datetime import date
from pathlib import Path

def scalar(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(key + ":"): return line.split(":",1)[1].strip() or "未填写"
    return "未填写"

def table_rows(path: Path) -> int:
    if not path.exists(): return 0
    rows = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip().startswith("|")]
    return max(0, len(rows) - 2)  # header + separator

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir",type=Path); ap.add_argument("--kind",choices=["weekly","phase","closing"],default="weekly"); ap.add_argument("--output",type=Path); args=ap.parse_args()
    root=args.project_dir.resolve(); manifest=(root/"project.yaml").read_text(encoding="utf-8"); state=json.loads((root/"00-governance/process-status.json").read_text(encoding="utf-8"))
    ps=state.get("processes",[]); done=sum(x.get("status") in {"approved","completed"} for x in ps); blocked=[x["code"] for x in ps if x.get("status")=="blocked"]
    risk_count=table_rows(root/"07-risk/risk-register.md"); issue_count=table_rows(root/"10-execution/issue-log.md"); change_count=table_rows(root/"00-governance/change-log.md")
    title={"weekly":"项目周报","phase":"阶段报告","closing":"项目收尾报告"}[args.kind]
    rows="\n".join(f"| {g.get('id','')} | {g.get('status','not_started')} | {g.get('approvedBy','')} | {g.get('date','')} |" for g in state.get('gates',[]))
    report=f"# {title}\n\n- 项目：{scalar(manifest,'name')}\n- 项目经理：{scalar(manifest,'manager')}\n- 当前阶段：{scalar(manifest,'current_phase')}\n- 报告日期：{date.today().isoformat()}\n- 过程完成度：{done}/{len(ps)}\n- 风险条目：{risk_count}\n- 问题条目：{issue_count}\n- 变更条目：{change_count}\n\n## 门禁状态\n\n| 门禁 | 状态 | 批准人 | 日期 |\n|---|---|---|---|\n{rows}\n\n## 阻塞过程\n\n{', '.join(blocked) if blocked else '无'}\n\n## 项目经理行动\n\n- 核实逾期事项、未决风险和变更请求。\n- 对未通过门禁的缺口指定责任人和日期。\n- 所有新决定追加到决策日志，避免覆盖历史记录。\n"
    if args.output:
        target=args.output if args.output.is_absolute() else root/args.output
        if target.exists() and target.stat().st_size>0: raise SystemExit(f"拒绝覆盖非空文件: {target}")
        target.parent.mkdir(parents=True,exist_ok=True); target.write_text(report,encoding="utf-8"); print(target)
    else: print(report)
    return 0

if __name__ == "__main__": raise SystemExit(main())
