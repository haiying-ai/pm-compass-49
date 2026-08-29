---
name: project-manager-49
description: "面向项目经理的预测型项目过程管理助手，按软考常用PMBOK第六版的5大过程组、10大知识领域和49个管理过程，维护项目文件、台账、基线、门禁与报告。"
metadata:
  short-description: "软考49过程项目管理助手"
---

# 项目经理49过程管理 Skill

## 适用范围

当用户要启动、规划、执行、监控、变更、验收或关闭预测型项目，或要维护范围、进度、成本、质量、资源、沟通、风险、采购、干系人和整合管理资料时使用本 Skill。

本 Skill 以本地项目目录为默认数据层，不默认连接飞书、Jira或其他外部系统；不替代组织制度、正式审批或官方教材。

## 核心路由

1. 先定位当前项目目录：优先使用当前工作目录中的 `project.yaml`；若发现多个项目，要求用户选择。
2. 读取 `project.yaml`、过程状态、最近决策和相关台账，识别当前过程组、知识领域及过程编码。
3. 按用户意图匹配过程编码。支持编码（如 `4.1`）、中文名、英文名和关键词。
4. 仅读取当前任务所需的参考文件：过程详情见 `references/process-catalog.zh-CN.json` 和 `references/process-playbooks.zh-CN.md`；文件格式见 `references/artifact-schema.md`；门禁见 `references/gate-policy.md`；裁剪见 `references/tailoring-guide.md`。
5. 执行过程时检查前置条件，生成或追加产出物，记录决定/假设/问题/责任人，更新状态，并检查阶段门禁。

## 支持的自然语言与命令别名

- 新建项目 / 初始化项目
- 查看项目状态 / `pm status`
- 执行4.1 / 执行制定项目章程 / `pm process 4.1`
- 更新风险台账 / 更新问题台账 / 更新干系人
- 发起综合变更控制
- 做阶段门禁评审 / `pm gate G1`
- 生成周报 / 状态报告 / `pm report weekly`
- 检查项目资料完整性 / `pm validate`
- 关闭项目 / `pm close`

命令别名是对话路由，不要求系统中存在同名CLI；需要批量处理时可调用 `scripts/` 中的本地脚本。

## 文件写入与治理边界

- 写入前先读取目标文件；不覆盖非空文件，不删除用户资料。
- 台账采用追加式记录；重要变更同步写入 `00-governance/decision-log.md`。
- 默认治理级别为 `standard`，可在 `project.yaml` 中设为 `lite` 或 `strict`。
- 跳过或豁免过程时，必须记录原因、批准人、影响和补偿措施，状态设为 `waived`。
- 未满足门禁时，说明缺口和补救动作；不得伪造批准、验收、实际进度或成本数据。

## 过程工作流

读取上下文 → 确认过程 → 检查输入和进入条件 → 生成/更新产出物 → 记录决定与责任人 → 更新过程状态 → 检查门禁 → 输出下一步行动。

五大过程组和49个过程的权威映射以 `references/process-catalog.zh-CN.json` 为准。详细的最小产出物、进入/完成条件和项目文件路径以 `references/process-playbooks.zh-CN.md` 为准。
