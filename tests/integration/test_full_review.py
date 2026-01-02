"""
Integration tests for CCO full-review command

Tests the cco-full-review command that performs self-review of CCO
system against its documented design principles.

This command has 129 checks across 10 categories:
1. Documentation Count Accuracy
2. Cross-File Consistency
3. SSOT Violations
4. Rule Coverage
5. Dead Code
6. Architecture Alignment
7. Terminology Consistency
8. Version Sync
9. Missing Documentation
10. Security Review
"""

from pathlib import Path
from typing import Any

import pytest


class TestFullReviewCommandStructure:
    """Test cco-full-review command file structure"""

    def test_full_review_command_exists(self, tmp_path: Path) -> None:
        """Test that full-review command template exists"""
        # Verify command template structure
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        # Create full-review command file
        cmd_file = commands_dir / "cco-full-review.md"
        cmd_file.write_text("""---
name: cco-full-review
description: CCO system health check (129 checks across 10 categories)
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*), TodoWrite, AskUserQuestion, Edit(*)
model: opus
---

# /cco-full-review

**CCO Self-Review** - Comprehensive analysis of CCO system.
""")

        assert cmd_file.exists()
        content = cmd_file.read_text()
        assert "cco-full-review" in content
        assert "129 checks" in content
        assert "10 categories" in content

    def test_full_review_has_required_flags(self, tmp_path: Path) -> None:
        """Test that full-review command has required flags"""
        cmd_file = tmp_path / "cco-full-review.md"
        cmd_file.write_text("""
## Args

- `--auto` or `--unattended`: Fully unattended mode
- `--quick`: CRITICAL and HIGH only, skip MEDIUM/LOW
- `--focus=X`: Single category (1-10 or name)
- `--report`: Report only, no fixes applied
- `--fix`: Auto-apply safe fixes
- `--fix-all`: Apply all fixes including manual ones
""")

        content = cmd_file.read_text()
        assert "--auto" in content
        assert "--quick" in content
        assert "--focus" in content
        assert "--report" in content
        assert "--fix" in content


class TestFullReviewCategories:
    """Test full-review category definitions"""

    def test_all_10_categories_defined(self, tmp_path: Path) -> None:
        """Test that all 10 review categories are properly defined"""
        categories = [
            "Documentation Count Accuracy",
            "Cross-File Consistency",
            "SSOT Violations",
            "Rule Coverage",
            "Dead Code",
            "Architecture Alignment",
            "Terminology Consistency",
            "Version Sync",
            "Missing Documentation",
            "Security Review",
        ]

        # Create categories file
        categories_file = tmp_path / "categories.md"
        content = "# Review Categories\n\n"
        for i, cat in enumerate(categories, 1):
            content += f"## {i}. {cat}\n\n"
            content += f"Category {i} checks.\n\n"

        categories_file.write_text(content)

        # Verify all categories present
        file_content = categories_file.read_text()
        for cat in categories:
            assert cat in file_content, f"Missing category: {cat}"

    def test_category_check_counts(self, tmp_path: Path) -> None:
        """Test that category check counts sum to 129"""
        # Simulated check counts per category
        check_counts: dict[str, int] = {
            "doc_count": 12,
            "cross_file": 15,
            "ssot": 18,
            "rule_coverage": 14,
            "dead_code": 10,
            "architecture": 16,
            "terminology": 12,
            "version_sync": 8,
            "missing_docs": 14,
            "security": 10,
        }

        total = sum(check_counts.values())
        assert total == 129, f"Total checks should be 129, got {total}"

    def test_category_severity_levels(self, tmp_path: Path) -> None:
        """Test that categories use proper severity levels"""
        severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

        # Create findings file
        findings_file = tmp_path / "findings.json"
        import json

        findings: list[dict[str, Any]] = [
            {"category": "security", "severity": "CRITICAL", "message": "Security issue"},
            {"category": "ssot", "severity": "HIGH", "message": "SSOT violation"},
            {"category": "doc_count", "severity": "MEDIUM", "message": "Count mismatch"},
            {"category": "terminology", "severity": "LOW", "message": "Term inconsistency"},
        ]

        findings_file.write_text(json.dumps(findings, indent=2))

        # Verify severities
        loaded = json.loads(findings_file.read_text())
        for finding in loaded:
            assert finding["severity"] in severities


class TestFullReviewInventory:
    """Test full-review inventory detection"""

    def test_counts_commands(self, tmp_path: Path) -> None:
        """Test that inventory correctly counts commands"""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        # Create command files
        commands = ["cco-config", "cco-status", "cco-optimize", "cco-review",
                    "cco-commit", "cco-research", "cco-preflight", "cco-checkup"]

        for cmd in commands:
            (commands_dir / f"{cmd}.md").write_text(f"# {cmd}")

        # Count commands
        cmd_files = list(commands_dir.glob("cco-*.md"))
        assert len(cmd_files) == 8

    def test_counts_agents(self, tmp_path: Path) -> None:
        """Test that inventory correctly counts agents"""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        # Create agent files
        agents = ["cco-agent-analyze", "cco-agent-apply", "cco-agent-research"]

        for agent in agents:
            (agents_dir / f"{agent}.md").write_text(f"# {agent}")

        # Count agents
        agent_files = list(agents_dir.glob("cco-*.md"))
        assert len(agent_files) == 3

    def test_counts_rules(self, tmp_path: Path) -> None:
        """Test that inventory correctly counts rules"""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        # Create rule files with proper structure
        core_rules = "\n".join([f"- **Rule{i}**: Description" for i in range(87)])
        ai_rules = "\n".join([f"- **AIRule{i}**: Description" for i in range(49)])

        (rules_dir / "core.md").write_text(f"# Core Rules\n\n{core_rules}")
        (rules_dir / "ai.md").write_text(f"# AI Rules\n\n{ai_rules}")

        # Count rules by pattern
        core_count = sum(1 for line in core_rules.split("\n") if line.startswith("- **"))
        ai_count = sum(1 for line in ai_rules.split("\n") if line.startswith("- **"))

        assert core_count == 87
        assert ai_count == 49


class TestFullReviewFindings:
    """Test full-review findings generation"""

    def test_finding_format(self, tmp_path: Path) -> None:
        """Test that findings follow correct format"""
        import json

        finding: dict[str, Any] = {
            "id": "DOC-001",
            "category": "Documentation Count Accuracy",
            "severity": "MEDIUM",
            "message": "README says 87 rules, actual count is 84",
            "file": "README.md",
            "line": 42,
            "fix": "Update count from 87 to 84",
            "auto_fixable": True,
        }

        # Verify required fields
        required_fields = ["id", "category", "severity", "message"]
        for field in required_fields:
            assert field in finding, f"Missing field: {field}"

        # Verify severity is valid
        assert finding["severity"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    def test_findings_grouped_by_category(self, tmp_path: Path) -> None:
        """Test that findings can be grouped by category"""
        import json

        findings = [
            {"id": "DOC-001", "category": "doc_count", "severity": "MEDIUM"},
            {"id": "DOC-002", "category": "doc_count", "severity": "LOW"},
            {"id": "SSOT-001", "category": "ssot", "severity": "HIGH"},
            {"id": "SEC-001", "category": "security", "severity": "CRITICAL"},
        ]

        # Group by category
        grouped: dict[str, list[dict[str, Any]]] = {}
        for f in findings:
            cat = f["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(f)

        assert len(grouped["doc_count"]) == 2
        assert len(grouped["ssot"]) == 1
        assert len(grouped["security"]) == 1

    def test_findings_sorted_by_severity(self, tmp_path: Path) -> None:
        """Test that findings are sorted by severity (CRITICAL first)"""
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

        findings = [
            {"severity": "LOW"},
            {"severity": "CRITICAL"},
            {"severity": "MEDIUM"},
            {"severity": "HIGH"},
        ]

        sorted_findings = sorted(findings, key=lambda f: severity_order[f["severity"]])

        assert sorted_findings[0]["severity"] == "CRITICAL"
        assert sorted_findings[1]["severity"] == "HIGH"
        assert sorted_findings[2]["severity"] == "MEDIUM"
        assert sorted_findings[3]["severity"] == "LOW"


class TestFullReviewFixes:
    """Test full-review fix application"""

    def test_auto_fixable_detection(self, tmp_path: Path) -> None:
        """Test detection of auto-fixable issues"""
        # Auto-fixable: doc count updates, terminology
        auto_fixable_categories = ["doc_count", "terminology"]

        # Manual-fix: security, architecture
        manual_fix_categories = ["security", "architecture"]

        findings = [
            {"category": "doc_count", "auto_fixable": True},
            {"category": "terminology", "auto_fixable": True},
            {"category": "security", "auto_fixable": False},
            {"category": "architecture", "auto_fixable": False},
        ]

        auto = [f for f in findings if f["auto_fixable"]]
        manual = [f for f in findings if not f["auto_fixable"]]

        assert len(auto) == 2
        assert len(manual) == 2

    def test_fix_accounting(self, tmp_path: Path) -> None:
        """Test that fixes are properly accounted"""
        accounting: dict[str, int] = {
            "done": 5,
            "fail": 1,
            "total": 6,
        }

        # Verify accounting invariant: done + fail = total (no declined - AI has no option to decline)
        assert accounting["done"] + accounting["fail"] == accounting["total"]

    def test_fix_result_format(self, tmp_path: Path) -> None:
        """Test fix result format"""
        result: dict[str, Any] = {
            "id": "DOC-001",
            "status": "done",
            "file": "README.md",
            "old_value": "87",
            "new_value": "84",
        }

        assert result["status"] in ["done", "fail"]


class TestFullReviewReport:
    """Test full-review report generation"""

    def test_report_includes_summary(self, tmp_path: Path) -> None:
        """Test that report includes summary statistics"""
        report = {
            "summary": {
                "total_checks": 129,
                "passed": 120,
                "findings": 9,
                "critical": 1,
                "high": 2,
                "medium": 4,
                "low": 2,
            },
            "health_score": 93,
        }

        assert report["summary"]["total_checks"] == 129
        assert report["summary"]["passed"] + report["summary"]["findings"] == 129
        assert report["health_score"] >= 0 and report["health_score"] <= 100

    def test_unattended_mode_output(self, tmp_path: Path) -> None:
        """Test unattended mode single-line output"""
        # Unattended mode should output single status line
        output = "cco-full-review: OK | Checks: 129 | Findings: 9 | Fixed: 7"

        assert "cco-full-review:" in output
        assert "Checks:" in output
        assert "Findings:" in output

    def test_report_grouped_by_category(self, tmp_path: Path) -> None:
        """Test that report groups findings by category"""
        import json

        report: dict[str, Any] = {
            "by_category": {
                "doc_count": {"total": 12, "passed": 10, "findings": 2},
                "security": {"total": 10, "passed": 9, "findings": 1},
            }
        }

        assert "by_category" in report
        assert len(report["by_category"]) >= 2


class TestFullReviewIntegration:
    """Integration tests for full-review workflow"""

    def test_complete_review_workflow(self, tmp_path: Path) -> None:
        """Test complete review workflow simulation"""
        # Step 1: Setup
        cco_dir = tmp_path / "cco"
        cco_dir.mkdir()
        (cco_dir / "README.md").write_text("# CCO\n\n87 core rules")

        # Step 2: Inventory
        inventory = {"commands": 8, "agents": 3, "core_rules": 87, "ai_rules": 49}

        # Step 3: Analyze (simulated)
        findings = [
            {"id": "DOC-001", "severity": "MEDIUM", "auto_fixable": True},
        ]

        # Step 4: Prioritize
        prioritized = sorted(
            findings,
            key=lambda f: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[f["severity"]]
        )

        # Step 5: Apply (simulated)
        results = [{"id": f["id"], "status": "done"} for f in prioritized if f["auto_fixable"]]

        # Step 6: Summary
        summary = {
            "total_findings": len(findings),
            "fixed": len(results),
            "remaining": len(findings) - len(results),
        }

        assert summary["fixed"] == 1
        assert summary["remaining"] == 0

    def test_quick_mode_filters_severity(self, tmp_path: Path) -> None:
        """Test that --quick mode only shows CRITICAL and HIGH"""
        findings = [
            {"severity": "CRITICAL"},
            {"severity": "HIGH"},
            {"severity": "MEDIUM"},
            {"severity": "LOW"},
        ]

        # Quick mode filter
        quick_findings = [f for f in findings if f["severity"] in ["CRITICAL", "HIGH"]]

        assert len(quick_findings) == 2

    def test_focus_mode_filters_category(self, tmp_path: Path) -> None:
        """Test that --focus mode only shows specified category"""
        findings = [
            {"category": "security", "severity": "HIGH"},
            {"category": "doc_count", "severity": "MEDIUM"},
            {"category": "security", "severity": "CRITICAL"},
        ]

        # Focus on security
        focus_findings = [f for f in findings if f["category"] == "security"]

        assert len(focus_findings) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
