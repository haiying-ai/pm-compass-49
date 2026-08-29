#!/usr/bin/env python3
"""Generate deterministic, reviewable test cases for all 49 processes."""
from __future__ import annotations
import argparse, json
from pathlib import Path

FOCUS_ZH = {
    "项目整合管理": "把菜单、预算、时间和家庭成员安排整合为一份可执行决定",
    "项目范围管理": "把‘丰盛但不铺张’转成明确菜品、份量和不在范围清单",
    "项目进度管理": "在两口灶和19:00开饭约束下安排采购、备菜和烹饪顺序",
    "项目成本管理": "在1200元成本基线内完成采购并保留预备金",
    "项目质量管理": "用食品安全、口味、温度和摆盘标准验收菜品",
    "项目资源管理": "按家庭成员技能和可用灶台分配角色、工具和时间",
    "项目沟通管理": "让家人及时知道菜单、分工、变更和风险",
    "项目风险管理": "提前处理缺鱼、堵灶、过敏和延误等不确定性",
    "项目采购管理": "比较菜市场和线上供应，按质量、价格、交付时间采购",
    "项目干系人管理": "平衡老人、小孩、厨师和不吃辣家人的需求",
}
FOCUS_EN = {
    "项目整合管理": "integrate menu, budget, timing, and family responsibilities into one executable decision",
    "项目范围管理": "turn a generous-but-not-wasteful dinner into explicit dishes, portions, and exclusions",
    "项目进度管理": "sequence shopping, prep, and cooking around two burners and a 19:00 dinner",
    "项目成本管理": "stay within the RMB 1,200 cost baseline while retaining contingency",
    "项目质量管理": "accept dishes against food-safety, taste, temperature, and presentation criteria",
    "项目资源管理": "assign family roles, tools, and stove time by skill and availability",
    "项目沟通管理": "keep the family informed about menu, ownership, changes, and risks",
    "项目风险管理": "prepare responses for fish shortages, stove congestion, allergies, and delays",
    "项目采购管理": "source ingredients by quality, price, and delivery time",
    "项目干系人管理": "balance the needs of elders, children, cooks, and non-spicy diners",
}

def gate_precondition(item: dict) -> str:
    group = item["processGroup"]
    if group == "启动过程组": return "项目需求或商业机会已提出，发起人和主要约束可识别"
    if group == "规划过程组": return "G0启动门禁已批准，项目章程可读取"
    if group == "执行过程组": return "G1计划与范围/进度/成本基线已批准"
    if group == "监控过程组": return "G2执行准备已完成，已有工作绩效或监控数据"
    return "G3验收与移交已完成，项目资料和合同状态可读取"

def activity(item: dict) -> str:
    special = {
        "制定项目章程": "确认12人、预算1200元、除夕19:00开饭和成功标准，并记录假设",
        "制定项目管理计划": "把范围、进度、成本、质量、资源、沟通、风险和采购安排合并为可执行计划",
        "收集需求": "分别访谈老人、小朋友、厨师和其他家人，记录低盐、不辣、必备菜和份量需求",
        "创建 WBS": "将菜单交付物拆到采购、洗切、腌制、烹饪、摆盘和验收工作包",
        "制定进度计划": "用两口灶约束倒排采购、备菜、凉菜、热菜和19:00上桌里程碑",
        "制定预算": "按肉类海鲜、蔬菜调料、饮品水果和预备金建立1200元成本基线",
        "识别风险": "组织家庭成员头脑风暴并登记缺鱼、堵灶、过敏和延误风险",
        "实施风险应对": "为缺鱼和堵灶风险指定触发条件、应对负责人和备用方案",
        "监督风险": "检查鱼类采购、灶台排程和过敏标识的风险应对是否生效",
        "控制范围": "核对临时增加蛋糕的请求是否超出8道菜范围并记录变更建议",
        "控制进度": "将实际采购和备菜时间与19:00开饭基线比较并记录偏差",
        "控制成本": "将已发生采购额与1200元基线比较，计算剩余预备金",
        "控制质量": "检查鱼虾新鲜度、熟度、低盐和不辣标识，记录不合格项",
        "确认范围": "让全家逐项确认8道菜、饮品水果和不在范围清单",
        "管理干系人参与": "协调老人、小朋友和厨师对菜单冲突的解决方案",
        "监督干系人参与": "回访家人满意度并记录是否需要调整沟通或参与方式",
        "结束项目或阶段": "确认开饭、费用结算、厨房归还和经验教训后关闭项目",
    }
    return special.get(item["nameZh"], f"围绕{item['knowledgeArea']}的‘{item['nameZh']}’完成一次年夜饭场景演练，明确输入、判断、责任人和输出")

def case(item: dict) -> dict:
    return {
        "id": f"TC-{item['code']}", "processCode": item["code"], "nameZh": item["nameZh"], "nameEn": item["nameEn"], "processGroup": item["processGroup"], "knowledgeArea": item["knowledgeArea"],
        "scenarioZh": f"为2027年家庭年夜饭测试“{item['nameZh']}”：12位家人，预算1200元，除夕19:00开饭。",
        "scenarioEn": f"Test {item['nameEn']} for a 2027 family New Year dinner: 12 guests, RMB 1,200, dinner at 19:00 on New Year's Eve.",
        "focusZh": FOCUS_ZH[item["knowledgeArea"]], "focusEn": FOCUS_EN[item["knowledgeArea"]],
        "preconditionsZh": ["项目目录已初始化且项目经理为爸爸", gate_precondition(item), "家庭成员和饮食限制已收集"],
        "preconditionsEn": ["The project workspace exists and Dad is the project manager", f"The prerequisite for the {item['processGroup']} stage is satisfied", "Family members and dietary constraints are known"],
        "inputsZh": item.get("inputs", []), "inputsEn": item.get("inputsEn", []),
        "actionsZh": [f"读取与‘{item['nameZh']}’相关的项目文件和输入。", f"组织家庭成员确认：{FOCUS_ZH[item['knowledgeArea']]}。", f"保存过程输出到 `{item['requiredArtifacts'][0]}`，并在决策日志记录责任人、日期和下一步。"],
        "actionsEn": [f"Read the project files and inputs for {item['nameEn']}.", f"Have the family confirm how to {FOCUS_EN[item['knowledgeArea']]}.", f"Save outputs to `{item['requiredArtifacts'][0]}` and record owner, date, and next action in the decision log."],
        "outputsZh": item.get("outputs", []), "outputsEn": item.get("outputsEn", []),
        "acceptanceZh": [f"最小产出文件 `{item['requiredArtifacts'][0]}` 存在且内容可追溯", "责任人和后续行动明确", "若无法完成，状态为blocked并写明缺口；若豁免，状态为waived并记录批准人"],
        "acceptanceEn": [f"The minimum artifact `{item['requiredArtifacts'][0]}` exists and is traceable", "An owner and next action are explicit", "If incomplete, mark blocked with the gap; if waived, record the approver"],
        "negativeZh": "故意删除一个前置输入或必需产出物，验证Skill提示阻塞而不是编造完成。",
        "negativeEn": "Deliberately remove one prerequisite input or required artifact and verify that the Skill reports a block instead of inventing completion.",
    }

def render(cases: list[dict], lang: str) -> str:
    zh = lang == "zh"
    title = "# 49个过程测试案例" if zh else "# 49 Process Test Cases"
    intro = "每个案例都使用同一份年夜饭项目作为可重复测试夹具。" if zh else "Every case uses the same New Year dinner project as a repeatable fixture."
    lines = [title, "", intro, "", "## 测试约定" if zh else "## Test convention", "", ("执行后应更新过程状态；通过标准是产出物可追溯、责任人明确、缺口可见。" if zh else "After execution, update process status. Pass means artifacts are traceable, ownership is explicit, and gaps are visible."), ""]
    sep = "；" if zh else "; "
    for c in cases:
        heading = f"{c['nameZh']}（{c['nameEn']}）" if zh else f"{c['nameEn']} ({c['nameZh']})"
        lines += [f"## {c['id']} · {heading}", "", f"- 过程编码：`{c['processCode']}`" if zh else f"- Process code: `{c['processCode']}`", f"- 场景：{c['scenarioZh'] if zh else c['scenarioEn']}" if zh else f"- Scenario: {c['scenarioEn']}", f"- 测试重点：{c['focusZh'] if zh else c['focusEn']}" if zh else f"- Focus: {c['focusEn']}", "", "### 前置条件" if zh else "### Preconditions"]
        lines += [f"- {x}" for x in (c["preconditionsZh"] if zh else c["preconditionsEn"])]
        lines += ["", "### 输入" if zh else "### Inputs", f"- {sep.join(c['inputsZh'] if zh else c['inputsEn']) or ('由项目经理确认' if zh else 'Confirmed by the project manager')}", "", "### 测试步骤" if zh else "### Steps"]
        lines += [f"{i}. {x}" for i, x in enumerate(c["actionsZh"] if zh else c["actionsEn"], 1)]
        lines += ["", "### 预期输出" if zh else "### Expected outputs", f"- {sep.join(c['outputsZh'] if zh else c['outputsEn']) or ('过程结论与行动项' if zh else 'Process decision and action items')}", "", "### 验收标准" if zh else "### Acceptance criteria"]
        lines += [f"- {x}" for x in (c["acceptanceZh"] if zh else c["acceptanceEn"])]
        lines += ["", "### 失败路径" if zh else "### Negative path", c["negativeZh"] if zh else c["negativeEn"], ""]
    return "\n".join(lines)

def customize(c: dict) -> dict:
    """Add process-specific preconditions, actions, and negative paths."""
    item = c
    group = c["processGroup"]
    gate = {"启动过程组": "商业机会和发起人可识别", "规划过程组": "G0启动门禁已批准", "执行过程组": "G1计划和基线已批准", "监控过程组": "G2执行准备已完成", "收尾过程组": "G3验收移交已完成"}[group]
    c["preconditionsZh"][1] = gate
    c["preconditionsEn"][1] = f"The prerequisite for the {group} stage is satisfied"
    c["actionsZh"][1] = f"围绕‘{c['nameZh']}’完成年夜饭专属活动：{activity({'nameZh': c['nameZh'], 'knowledgeArea': c['knowledgeArea']})}。"
    c["actionsEn"][1] = f"Perform the dinner-specific activity for {c['nameEn']}: {c['focusEn']}."
    c["negativeZh"] = f"删除或留空关键输入‘{(c.get('inputsZh') or ['项目上下文'])[0]}’，验证{c['nameZh']}状态变为blocked并显示缺口。"
    c["negativeEn"] = f"Remove or blank the key input '{(c.get('inputsEn') or ['project context'])[0]}' and verify that {c['nameEn']} becomes blocked with a visible gap."
    return c

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser(); ap.add_argument("--catalog", type=Path, default=root / "references" / "process-catalog.zh-CN.json"); ap.add_argument("--output-dir", type=Path, default=root / "tests"); args=ap.parse_args()
    catalog=json.loads(args.catalog.read_text(encoding="utf-8")); cases=[customize(case(p)) for p in catalog["processes"]]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"process-test-cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (args.output_dir/"process-test-cases.zh-CN.md").write_text(render(cases,"zh"), encoding="utf-8")
    (args.output_dir/"process-test-cases.en.md").write_text(render(cases,"en"), encoding="utf-8")
    print(f"generated {len(cases)} test cases")
    return 0

if __name__ == "__main__": raise SystemExit(main())
