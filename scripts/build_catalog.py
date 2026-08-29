#!/usr/bin/env python3
"""Build the portable 49-process catalog from the workspace source snapshot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

AREA_ZH = {
    "Integration Management": "项目整合管理", "Scope Management": "项目范围管理",
    "Schedule Management": "项目进度管理", "Cost Management": "项目成本管理",
    "Quality Management": "项目质量管理", "Resource Management": "项目资源管理",
    "Communications Management": "项目沟通管理", "Risk Management": "项目风险管理",
    "Procurement Management": "项目采购管理", "Stakeholder Management": "项目干系人管理",
}
GROUP_ZH = {
    "Initiating": "启动过程组", "Planning": "规划过程组", "Executing": "执行过程组",
    "Monitoring & Controlling": "监控过程组", "Closing": "收尾过程组",
}
AREA_DIR = {
    "Integration Management": "00-governance", "Scope Management": "01-scope",
    "Schedule Management": "02-schedule", "Cost Management": "03-cost",
    "Quality Management": "04-quality", "Resource Management": "05-resource",
    "Communications Management": "06-communications", "Risk Management": "07-risk",
    "Procurement Management": "08-procurement", "Stakeholder Management": "09-stakeholder",
}

def gate_for(item: dict) -> str:
    code = item["code"]
    if code == "4.1": return "G0"
    if code == "4.2": return "G1"
    if code == "4.3": return "G2"
    if item["processGroup"] == "Closing": return "G4"
    if item["name"] in {"确认范围", "控制范围", "控制进度", "控制成本", "控制质量", "控制资源"}: return "G3"
    return ""

def artifact_path(item: dict) -> str:
    area = AREA_DIR[item["knowledgeArea"]]
    slug = item["code"].replace(".", "-")
    return f"{area}/{slug}-{item['name']}.md"

def keywords(item: dict) -> tuple[list[str], list[str]]:
    zh = [item["name"], AREA_ZH[item["knowledgeArea"]], GROUP_ZH[item["processGroup"]]]
    en = [item["process"], item["knowledgeArea"], item["processGroup"]]
    # Keep short, useful aliases for conversational routing.
    if item["knowledgeArea"] == "Risk Management": zh += ["风险", "风险台账"]
    if item["knowledgeArea"] == "Scope Management": zh += ["范围", "需求", "WBS"]
    if item["knowledgeArea"] == "Schedule Management": zh += ["进度", "排期", "时间表"]
    if item["knowledgeArea"] == "Cost Management": zh += ["成本", "预算", "费用"]
    return sorted(set(zh)), sorted(set(en))

def build(source: Path, destination: Path) -> None:
    raw = json.loads(source.read_text(encoding="utf-8"))
    processes = []
    for item in raw["processes"]:
        keywords_zh, keywords_en = keywords(item)
        processes.append({
            "code": item["code"], "nameZh": item["name"], "nameEn": item["process"],
            "processGroup": GROUP_ZH[item["processGroup"]],
            "knowledgeArea": AREA_ZH[item["knowledgeArea"]],
            "keywordsZh": keywords_zh, "keywordsEn": keywords_en,
            "purpose": f"通过“{item['name']}”形成可审计的项目管理决策和产出物。",
            "inputs": item.get("inputsZh", []), "outputs": item.get("outputsZh", []),
            "inputsEn": item.get("inputs", []), "outputsEn": item.get("outputs", []),
            "requiredArtifacts": [artifact_path(item)],
            "entryCriteria": [f"已识别{item['knowledgeArea']}相关目标、约束或待解决事项"],
            "exitCriteria": ["产出物已保存并由责任人确认", "决定、假设、问题和后续行动已记录"],
            "gateImpact": gate_for(item),
            "tailoring": {
                "lite": {"minimum": "保留结论、责任人和关键证据"},
                "standard": {"minimum": "完成过程最小产出物并更新相关台账"},
                "strict": {"minimum": "保留完整输入输出、审批链和影响分析"},
            },
        })
    result = {
        "schemaVersion": "1.0.0", "methodology": "PMBOK6-predictive-soft-exam",
        "source": "workspace pmbok-process-map snapshot", "groups": raw["groups"],
        "areas": raw["areas"], "processes": processes,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    playbook = destination.parent / "process-playbooks.zh-CN.md"
    lines = ["# 49个过程执行手册", "", "每个过程遵循：读取输入 → 形成判断/计划 → 保存输出 → 更新台账 → 记录责任人和下一步。", ""]
    for p in processes:
        lines += [f"## {p['code']} {p['nameZh']}（{p['nameEn']}）", "",
                  f"- 过程组：{p['processGroup']}；知识领域：{p['knowledgeArea']}",
                  f"- 目的：{p['purpose']}", f"- 输入：{'、'.join(p['inputs']) or '由项目经理确认'}",
                  f"- 输出：{'、'.join(p['outputs']) or '过程结论与行动项'}",
                  f"- 最小文件：`{p['requiredArtifacts'][0]}`",
                  f"- 进入条件：{p['entryCriteria'][0]}",
                  f"- 完成条件：{'；'.join(p['exitCriteria'])}",
                  f"- 门禁影响：{p['gateImpact'] or '无直接门禁'}", ""]
    playbook.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--source", type=Path, default=root / "references" / "pmbok-49-source.zh-CN.json")
    parser.add_argument("--destination", type=Path, default=root / "references" / "process-catalog.zh-CN.json")
    args = parser.parse_args()
    build(args.source, args.destination)
