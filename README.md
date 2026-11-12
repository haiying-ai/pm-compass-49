# PM Compass 49｜项目经理的 AI 项目管理罗盘

> 把软考常用的 5 大过程组、10 大知识领域、49 个管理过程，变成可安装、可执行、可审计的 AI 项目管理 Skill。

[![CI](https://github.com/haiying-ai/pm-compass-49/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/haiying-ai/pm-compass-49/actions/workflows/ci.yml)

[English README](README.en.md) · [49 个过程测试案例](tests/process-test-cases.zh-CN.md) · [年夜饭示例](examples/new-year-dinner/README.md)

## 为什么值得使用

很多项目管理方法停留在知识点、表格和会议纪要层面；PM Compass 49 把它们连接成一条可执行的项目流程：知道当前处于哪个过程、应该读取什么输入、需要产出什么文件、是否满足阶段门禁，以及下一步由谁完成什么。

它适合个人项目经理、小型团队、咨询顾问、项目管理办公室（PMO）和正在准备软考项目管理的学习者。Skill 以本地 Markdown/YAML/JSON 为数据层，不绑定特定厂商，项目资料可以进入 Git 版本控制，也可以在后续同步到团队协作工具。

## 核心能力

- **49 过程路由**：按过程编码、中文名称、英文名称或自然语言关键词定位过程。
- **项目全生命周期**：启动、规划、执行、监控、验收、收尾一体化管理。
- **十域台账**：范围、进度、成本、质量、资源、沟通、风险、采购、干系人和整合管理。
- **标准项目目录**：自动生成章程、计划、基线、风险/问题台账、门禁记录和报告目录。
- **阶段门禁**：G0 启动、G1 计划基线、G2 执行准备、G3 验收移交、G4 关闭。
- **可裁剪治理**：`lite`、`standard`、`strict` 三种治理级别。
- **可审计变更**：追加式台账、决策日志、变更影响和豁免记录。
- **离线可迁移**：不依赖外部 API，任何安装了该 Skill 的人都可以在本地项目目录使用。
- **可测试可扩展**：提供49个过程测试案例、冒烟测试和目录生成脚本。

## 49 个过程覆盖

| 过程组 | 数量 | 知识领域数量 |
|---|---:|---:|
| 启动 | 2 | 1 |
| 规划 | 24 | 10 |
| 执行 | 10 | 8 |
| 监控 | 12 | 9 |
| 收尾 | 1 | 1 |

完整机器可读目录见 [`references/process-catalog.zh-CN.json`](references/process-catalog.zh-CN.json)，每个过程包含输入、输出、最小产出物、进入/完成条件、门禁影响和裁剪提示。
重建目录使用仓库内随附的 [`references/pmbok-49-source.zh-CN.json`](references/pmbok-49-source.zh-CN.json)，不依赖仓库外部数据：

```powershell
python scripts/build_catalog.py
```

## 一键安装

### 方式 A：从仓库根目录复制到 Codex Skill 目录（Windows PowerShell）

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $skillRoot 'project-manager-49') | Out-Null
Copy-Item -Recurse -Force -Path (Join-Path (Resolve-Path .) '*') -Destination (Join-Path $skillRoot 'project-manager-49')
```

### 方式 B：从 GitHub 克隆后安装

```powershell
git clone https://github.com/haiying-ai/pm-compass-49.git
Set-Location pm-compass-49
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Copy-Item -Recurse -Force . (Join-Path $skillRoot 'project-manager-49')
```

也可以直接运行仓库内安装脚本：`powershell -ExecutionPolicy Bypass -File .\install.ps1`；macOS/Linux 使用 `bash install.sh`。安装脚本只更新目标 Skill 目录，不会修改项目业务目录。

安装后重新打开 Codex，或显式输入 `$project-manager-49`。

## 5 分钟上手

```text
新建一个“2027年家庭年夜饭”项目，负责人是爸爸，预算1200元，12人参加，除夕19:00开饭。
```

Skill 会建立项目目录。随后可以直接说：

```text
查看项目状态
执行 4.1 制定项目章程
更新风险台账：年夜当天可能买不到鱼
做 G1 阶段门禁评审
生成项目周报
```

也可以使用本地脚本：

```powershell
python scripts/init_project.py ./my-project --name "示例项目" --manager "项目经理A"
python scripts/validate_project.py ./my-project
python scripts/process_status.py ./my-project
python scripts/generate_report.py ./my-project --kind weekly
```

## 项目目录

初始化后会得到 `project.yaml`、`00-governance` 至 `13-closing` 的标准目录，以及一个包含49条过程状态记录的 `process-status.json`。写入规则是：先读后写、非空文件不覆盖、台账追加、重要决定进入决策日志。

## 测试案例

每一个过程都有一条可复现测试案例，包含：场景、前置条件、输入、操作步骤、预期产出、验收标准和失败路径。

- [中文49过程测试案例](tests/process-test-cases.zh-CN.md)
- [英文49过程测试案例](tests/process-test-cases.en.md)
- [自动冒烟测试](tests/run_smoke_tests.py)
- [年夜饭端到端示例](examples/new-year-dinner/README.md)

运行测试：

```powershell
python tests/run_smoke_tests.py
python D:/CodexData/skills/.system/skill-creator/scripts/quick_validate.py .
```

## 方法论边界

v1 基于 PMBOK 第六版预测型过程模型，适配软考常用术语；不内置完整 Scrum/敏捷流程，不伪造审批、验收、成本或进度数据。后续可以通过独立扩展加入敏捷裁剪、飞书同步、仪表盘和团队权限。

## 许可证

本项目采用 MIT License。PMBOK® 等名称和商标归其各自权利人所有；本项目是学习和项目治理辅助工具，不替代官方指南或组织制度。

## 贡献

欢迎补充行业模板、真实但脱敏的测试案例、翻译和脚本改进。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并运行 `tests/run_smoke_tests.py`。
