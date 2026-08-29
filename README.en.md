# PM Compass 49 | AI Project Management Skill for Project Managers

> Turn the five process groups, ten knowledge areas, and 49 predictive processes used in Chinese software-exam project management into an installable, executable, auditable AI Skill.

[中文说明](README.md) · [49 process test cases](tests/process-test-cases.en.md) · [New Year dinner example](examples/new-year-dinner/README.md)

## Why it matters

PM Compass 49 connects project-management knowledge to daily execution. It identifies the current process, checks inputs and entry criteria, produces the minimum artifact, records decisions and ownership, evaluates stage gates, and recommends the next action.

The Skill is designed for project managers, small teams, consultants, PMOs, and learners preparing for the Chinese software-exam project-management track. Local Markdown/YAML/JSON files are the default data layer, so projects remain portable and version-control friendly.

## Capabilities

- Route requests by process code, Chinese or English name, and natural-language keywords.
- Manage initiation, planning, execution, monitoring, acceptance, and closing.
- Maintain ten knowledge-area artifacts and registers.
- Create a standard project workspace with manifest, baselines, logs, gates, and reports.
- Evaluate G0–G4 stage gates with `lite`, `standard`, and `strict` tailoring.
- Keep append-only decisions, risks, issues, changes, and waivers.
- Run offline with no vendor-specific external API dependency.
- Verify behavior with 49 process cases and automated smoke tests.

## Install in one step

From the repository root in PowerShell:

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Copy-Item -Recurse -Force . (Join-Path $skillRoot 'project-manager-49')
```

You can also run `powershell -ExecutionPolicy Bypass -File .\install.ps1` on Windows or `bash install.sh` on macOS/Linux. The installer updates only the target Skill directory.

Restart Codex and invoke `$project-manager-49`, or let automatic skill discovery route a project-management request.

## Quick start

```text
Create a project called “2027 Family New Year Dinner”. There are 12 guests, a 1,200 RMB budget, and dinner must start at 19:00 on New Year's Eve.
```

Then ask for project status, process `4.1`, a risk update, a `G1` gate review, or a weekly report.

## Test coverage

See [English 49-process test cases](tests/process-test-cases.en.md), the [Chinese cases](tests/process-test-cases.zh-CN.md), and [tests/run_smoke_tests.py](tests/run_smoke_tests.py). The test suite checks catalog counts, idempotent initialization, lookup by code/name, validation, report generation, and overwrite protection.

The source snapshot is included at [`references/pmbok-49-source.zh-CN.json`](references/pmbok-49-source.zh-CN.json), so the catalog can be rebuilt without external files: `python scripts/build_catalog.py`.

## Scope and license

Version 1 follows the PMBOK sixth-edition predictive process model used in the software-exam context. It does not implement a complete Scrum/agile operating model. MIT License; see [LICENSE](LICENSE).
