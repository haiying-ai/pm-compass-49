#!/usr/bin/env python3
"""Validate project structure, manifest fields, catalog mapping, and gate evidence."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REQUIRED = ["id", "name", "manager", "sponsor", "methodology", "governance_profile", "status", "current_process_group", "current_phase", "start_date", "target_end_date", "baselines", "tailoring_decisions", "last_reviewed"]
DIRS = ["00-governance", "01-scope", "02-schedule", "03-cost", "04-quality", "05-resource", "06-communications", "07-risk", "08-procurement", "09-stakeholder", "10-execution", "11-monitoring", "12-acceptance", "13-closing", "reports"]
STATUS = {"not_started", "in_progress", "ready", "blocked", "approved", "waived", "completed"}
GROUP_COUNTS = {"启动过程组": 2, "规划过程组": 24, "执行过程组": 10, "监控过程组": 12, "收尾过程组": 1}
AREA_COUNTS = {"项目整合管理": 7, "项目范围管理": 6, "项目进度管理": 6, "项目成本管理": 4, "项目质量管理": 3, "项目资源管理": 6, "项目沟通管理": 3, "项目风险管理": 7, "项目采购管理": 3, "项目干系人管理": 4}

def yaml_keys(text: str) -> set[str]:
    return {m.group(1) for m in re.finditer(r"^([A-Za-z_][\w-]*):", text, re.M)}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("project_dir", type=Path); args = ap.parse_args()
    root = args.project_dir.resolve(); errors=[]; warnings=[]
    manifest = root / "project.yaml"
    if not manifest.exists(): errors.append("缺少 project.yaml")
    else:
        missing = sorted(set(REQUIRED) - yaml_keys(manifest.read_text(encoding="utf-8")))
        if missing: errors.append("project.yaml缺少字段: " + ", ".join(missing))
    for d in DIRS:
        if not (root / d).is_dir(): errors.append(f"缺少目录: {d}")
    catalog_path = Path(__file__).resolve().parents[1] / "references" / "process-catalog.zh-CN.json"
    try: catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"无法读取过程目录: {exc}"); catalog={"processes":[]}
    ps = catalog.get("processes", []); codes=[p.get("code") for p in ps]
    if len(ps) != 49: errors.append(f"过程数量为{len(ps)}，应为49")
    if len(set(codes)) != len(codes): errors.append("过程编码存在重复")
    if any(not all(p.get(k) is not None for k in ("code", "nameZh", "nameEn", "processGroup", "knowledgeArea", "inputs", "outputs", "requiredArtifacts", "entryCriteria", "exitCriteria", "tailoring")) for p in ps): errors.append("过程目录存在缺失字段")
    if {k: sum(p.get("processGroup") == k for p in ps) for k in GROUP_COUNTS} != GROUP_COUNTS: errors.append("过程组分布不符合2/24/10/12/1")
    if {k: sum(p.get("knowledgeArea") == k for p in ps) for k in AREA_COUNTS} != AREA_COUNTS: errors.append("知识领域分布不符合7/6/6/4/3/6/3/7/3/4")
    state_path = root / "00-governance/process-status.json"
    if not state_path.exists(): errors.append("缺少 00-governance/process-status.json")
    else:
        try:
            state=json.loads(state_path.read_text(encoding="utf-8")); known=set(codes)
            actual={p.get("code") for p in state.get("processes", [])}
            if actual != known: errors.append("过程状态未覆盖完整49个过程")
            if {g.get("id") for g in state.get("gates", [])} != {"G0", "G1", "G2", "G3", "G4"}: errors.append("门禁未完整覆盖G0-G4")
            for process in state.get("processes", []):
                if process.get("status") not in STATUS: errors.append(f"过程{process.get('code')}状态非法: {process.get('status')}")
            for gate in state.get("gates", []):
                if gate.get("status") not in STATUS: errors.append(f"{gate.get('id')}状态非法: {gate.get('status')}")
                if gate.get("status") == "approved" and not gate.get("approvedBy"): errors.append(f"{gate.get('id')}已批准但缺少approvedBy")
        except Exception as exc: errors.append(f"过程状态文件无效: {exc}")
    result={"valid": not errors, "errors": errors, "warnings": warnings, "project": str(root)}
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if not errors else 1

if __name__ == "__main__": raise SystemExit(main())
