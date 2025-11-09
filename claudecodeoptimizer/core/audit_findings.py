"""
Audit Findings Manager - CCO

Stores and manages audit findings for batch fixing.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional


class AuditFinding:
    """Represents a single audit finding."""

    def __init__(
        self,
        finding_id: str,
        category: Literal["security", "tests", "code_quality", "documentation", "principles"],
        severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        priority_tier: Literal["IMMEDIATE", "THIS_WEEK", "THIS_SPRINT", "BACKLOG"],
        title: str,
        description: str,
        command: str,
        risk_reduction_percent: int,
        file: Optional[str] = None,
        line: Optional[int] = None,
        principle: Optional[str] = None,
        audits_affected: Optional[List[str]] = None,
    ):
        self.id = finding_id
        self.category = category
        self.severity = severity
        self.priority_tier = priority_tier
        self.title = title
        self.description = description
        self.file = file
        self.line = line
        self.principle = principle
        self.audits_affected = audits_affected or [category]
        self.command = command
        self.risk_reduction_percent = risk_reduction_percent
        self.status = "pending"  # pending, fixed, skipped, failed
        self.timestamp = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity,
            "priority_tier": self.priority_tier,
            "title": self.title,
            "description": self.description,
            "file": self.file,
            "line": self.line,
            "principle": self.principle,
            "audits_affected": self.audits_affected,
            "command": self.command,
            "risk_reduction_percent": self.risk_reduction_percent,
            "status": self.status,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditFinding":
        """Create AuditFinding from dictionary."""
        finding = cls(
            finding_id=data["id"],
            category=data["category"],
            severity=data["severity"],
            priority_tier=data["priority_tier"],
            title=data["title"],
            description=data["description"],
            command=data["command"],
            risk_reduction_percent=data["risk_reduction_percent"],
            file=data.get("file"),
            line=data.get("line"),
            principle=data.get("principle"),
            audits_affected=data.get("audits_affected"),
        )
        finding.status = data.get("status", "pending")
        finding.timestamp = data.get("timestamp")
        return finding


class AuditFindingsManager:
    """Manages audit findings storage and retrieval."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.findings_file = project_root / ".cco" / "audit-findings.json"
        self.findings: List[AuditFinding] = []
        self.metadata: Dict[str, Any] = {}

        # Load existing findings if available
        if self.findings_file.exists():
            self._load()

    def add_finding(self, finding: AuditFinding) -> None:
        """Add a finding to the list."""
        self.findings.append(finding)

    def save(
        self,
        overall_health: int,
        risk_level: str,
    ) -> None:
        """Save findings to disk."""
        # Ensure directory exists
        self.findings_file.parent.mkdir(parents=True, exist_ok=True)

        # Organize findings by priority tier
        fix_plan = {
            "immediate": [],
            "this_week": [],
            "this_sprint": [],
            "backlog": [],
        }

        for finding in self.findings:
            tier_map = {
                "IMMEDIATE": "immediate",
                "THIS_WEEK": "this_week",
                "THIS_SPRINT": "this_sprint",
                "BACKLOG": "backlog",
            }
            tier = tier_map.get(finding.priority_tier, "backlog")
            fix_plan[tier].append(finding.id)

        # Calculate stats
        stats = self._calculate_stats()

        # Build JSON structure
        data = {
            "version": "1.0.0",
            "audit_date": datetime.now().isoformat(),
            "project": self.project_root.name,
            "overall_health": overall_health,
            "risk_level": risk_level,
            "findings": [f.to_dict() for f in self.findings],
            "fix_plan": fix_plan,
            "stats": stats,
        }

        # Write to file
        with open(self.findings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load(self) -> None:
        """Load findings from disk."""
        try:
            with open(self.findings_file, encoding="utf-8") as f:
                data = json.load(f)

            self.metadata = {
                "version": data.get("version"),
                "audit_date": data.get("audit_date"),
                "project": data.get("project"),
                "overall_health": data.get("overall_health"),
                "risk_level": data.get("risk_level"),
                "fix_plan": data.get("fix_plan", {}),
                "stats": data.get("stats", {}),
            }

            self.findings = [AuditFinding.from_dict(f) for f in data.get("findings", [])]

        except Exception:
            # If load fails, start fresh
            self.findings = []
            self.metadata = {}

    def _calculate_stats(self) -> Dict[str, Any]:
        """Calculate statistics about findings."""
        stats = {
            "total_findings": len(self.findings),
            "by_severity": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
            "by_category": {},
        }

        for finding in self.findings:
            # Count by severity
            stats["by_severity"][finding.severity] += 1

            # Count by category
            if finding.category not in stats["by_category"]:
                stats["by_category"][finding.category] = 0
            stats["by_category"][finding.category] += 1

        return stats

    def get_findings_by_priority(
        self,
        priority: Literal["IMMEDIATE", "THIS_WEEK", "THIS_SPRINT", "BACKLOG"],
    ) -> List[AuditFinding]:
        """Get findings by priority tier."""
        return [f for f in self.findings if f.priority_tier == priority]

    def get_findings_by_category(
        self,
        category: Literal["security", "tests", "code_quality", "documentation", "principles"],
    ) -> List[AuditFinding]:
        """Get findings by category."""
        return [f for f in self.findings if f.category == category]

    def get_pending_findings(self) -> List[AuditFinding]:
        """Get all pending (unfixed) findings."""
        return [f for f in self.findings if f.status == "pending"]

    def mark_as_fixed(self, finding_id: str) -> None:
        """Mark a finding as fixed."""
        for finding in self.findings:
            if finding.id == finding_id:
                finding.status = "fixed"
                finding.timestamp = datetime.now().isoformat()
                break

    def mark_as_failed(self, finding_id: str) -> None:
        """Mark a finding as failed (couldn't fix)."""
        for finding in self.findings:
            if finding.id == finding_id:
                finding.status = "failed"
                finding.timestamp = datetime.now().isoformat()
                break

    def mark_as_skipped(self, finding_id: str) -> None:
        """Mark a finding as skipped (user chose not to fix)."""
        for finding in self.findings:
            if finding.id == finding_id:
                finding.status = "skipped"
                finding.timestamp = datetime.now().isoformat()
                break

    def get_fix_commands(
        self,
        priority: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[str]:
        """Get list of fix commands, optionally filtered."""
        findings = self.get_pending_findings()

        if priority:
            findings = [f for f in findings if f.priority_tier == priority]
        if category:
            findings = [f for f in findings if f.category == category]

        # Sort by priority tier, then severity
        priority_order = {"IMMEDIATE": 0, "THIS_WEEK": 1, "THIS_SPRINT": 2, "BACKLOG": 3}
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

        findings.sort(
            key=lambda f: (
                priority_order.get(f.priority_tier, 99),
                severity_order.get(f.severity, 99),
            ),
        )

        return [f.command for f in findings]
