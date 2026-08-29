# Contributing to PM Compass 49

欢迎提交过程模板、行业案例、翻译、缺陷修复和脚本改进。

## 提交流程

1. Fork 仓库并创建功能分支。
2. 保持 Skill 的本地、可迁移和不绑定厂商的边界。
3. 修改过程目录时，确保49个编码、过程组和知识领域计数不变。
4. 新增案例时，至少包含场景、前置条件、输入、步骤、预期产出和验收标准。
5. 运行：

```powershell
python tests/run_smoke_tests.py
python D:/CodexData/skills/.system/skill-creator/scripts/quick_validate.py project-manager-49
```

6. Pull Request 中说明行为变化、兼容性影响和测试结果。

## 内容准则

- 不提交真实个人信息、密钥或未脱敏的客户资料。
- 不伪造审批、验收、进度和成本证据。
- 对PMBOK内容进行摘要和映射时，保留学习辅助工具定位，不替代官方出版物。
