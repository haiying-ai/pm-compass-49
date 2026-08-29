# 项目文件与台账规范

## 项目清单

项目根目录必须包含 `project.yaml`。字段：`id`、`name`、`manager`、`sponsor`、`methodology`、`governance_profile`、`status`、`current_process_group`、`current_phase`、`start_date`、`target_end_date`、`baselines`、`tailoring_decisions`、`last_reviewed`。

## 目录映射

| 目录 | 主要文件 |
|---|---|
| `00-governance` | 章程、项目管理计划、决策日志、门禁记录 |
| `01-scope` | 范围说明书、需求登记册、WBS、范围验收记录 |
| `02-schedule` | 活动清单、网络图、进度计划、进度基线 |
| `03-cost` | 成本估算、预算、成本基线、挣值记录 |
| `04-quality` | 质量管理计划、质量指标、检查与测试记录 |
| `05-resource` | 资源管理计划、资源日历、团队名册 |
| `06-communications` | 沟通管理计划、会议纪要、状态报告 |
| `07-risk` | 风险管理计划、风险登记册、风险应对记录 |
| `08-procurement` | 采购策略、采购文件、合同与供应商记录 |
| `09-stakeholder` | 干系人登记册、参与评估、参与策略 |
| `10-execution` | 工作绩效数据、交付物、问题处理记录 |
| `11-monitoring` | 工作绩效报告、变更请求、偏差分析 |
| `12-acceptance` | 验收记录、移交清单、最终产品确认 |
| `13-closing` | 关闭报告、经验教训、组织过程资产更新 |

## 台账记录

台账采用Markdown表格或YAML列表。每条记录至少包含：`id`、`date`、`owner`、`status`、`description`、`next_action`、`due_date`。修改不覆盖历史，使用追加记录或明确的状态变更。
