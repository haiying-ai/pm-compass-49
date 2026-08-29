#!/usr/bin/env python3
"""Portable smoke tests for the Skill package; uses only the Python standard library."""
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CATALOG = ROOT / "references" / "process-catalog.zh-CN.json"

def run(*args: str, expect: int = 0) -> str:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != expect:
        raise AssertionError(f"command failed ({result.returncode} != {expect}): {args}\n{result.stdout}\n{result.stderr}")
    return result.stdout

def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8")); ps = catalog["processes"]
    assert len(ps) == 49
    assert len({p["code"] for p in ps}) == 49
    assert {p["processGroup"] for p in ps} == {"启动过程组", "规划过程组", "执行过程组", "监控过程组", "收尾过程组"}
    with tempfile.TemporaryDirectory(prefix="pm-compass-49-") as tmp:
        project = Path(tmp) / "new-year-dinner"
        first = json.loads(run(str(SCRIPTS / "init_project.py"), str(project), "--name", "2027年家庭年夜饭", "--manager", "爸爸", "--sponsor", "全家"))
        assert "project.yaml" in first["created"]
        second = json.loads(run(str(SCRIPTS / "init_project.py"), str(project), "--name", "2027年家庭年夜饭", "--manager", "爸爸", "--sponsor", "全家"))
        assert second["created"] == []
        validation = json.loads(run(str(SCRIPTS / "validate_project.py"), str(project)))
        assert validation["valid"] is True
        assert "4.1 制定项目章程" in run(str(SCRIPTS / "process_status.py"), str(project), "--code", "制定项目章程")
        assert "11.2 识别风险" in run(str(SCRIPTS / "process_status.py"), str(project), "--code", "Identify Risks")
        assert "匹配" in run(str(SCRIPTS / "process_status.py"), str(project), "--code", "风险")
        report = run(str(SCRIPTS / "generate_report.py"), str(project), "--kind", "weekly")
        assert "项目周报" in report and "过程完成度：0/49" in report and "风险条目：0" in report and "问题条目：0" in report
        output = project / "reports" / "weekly.md"
        run(str(SCRIPTS / "generate_report.py"), str(project), "--kind", "weekly", "--output", str(output))
        run(str(SCRIPTS / "generate_report.py"), str(project), "--kind", "weekly", "--output", str(output), expect=1)
    print("PASS: catalog, initialization, idempotence, validation, lookup, report, overwrite protection")
    return 0

if __name__ == "__main__": raise SystemExit(main())
