"""
Report Management System - CCO 3.0

Manages command output reports with:
- Timestamped storage in .cco/reports/{command}/
- Latest report tracking
- Automatic cleanup of old reports (configurable)
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


class ReportManager:
    """
    Manage command output reports.

    Reports are saved to:
    - .cco/reports/{command}/YYYY-MM-DD-HHMMSS-{command}.md
    - .cco/reports/{command}/latest-{command}.md (copy of latest)
    """

    def __init__(self, project_root: Optional[Path] = None) -> None:
        """
        Initialize report manager.

        Args:
            project_root: Project root directory (defaults to cwd)
        """
        self.project_root = project_root or Path.cwd()
        self.reports_dir = self.project_root / ".cco" / "reports"

    def save_report(
        self,
        command: str,
        content: str,
        max_reports: int = 10
    ) -> Path:
        """
        Save report to .cco/reports/{command}/.

        Args:
            command: Command name (e.g., "audit", "status", "fix")
            content: Report content (markdown)
            max_reports: Maximum number of reports to keep (default: 10)

        Returns:
            Path to saved report file
        """
        # Create command-specific directory
        command_dir = self.reports_dir / command
        command_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = f"{timestamp}-{command}.md"
        report_file = command_dir / filename

        # Write report
        report_file.write_text(content, encoding="utf-8")

        # Update latest report (copy instead of symlink for Windows compatibility)
        latest_file = command_dir / f"latest-{command}.md"
        if latest_file.exists():
            latest_file.unlink()
        shutil.copy2(report_file, latest_file)

        # Cleanup old reports (keep last N)
        self._cleanup_old_reports(command_dir, command, max_reports)

        return report_file

    def get_latest_report(self, command: str) -> Optional[str]:
        """
        Get content of latest report for command.

        Args:
            command: Command name

        Returns:
            Report content or None if not found
        """
        latest_file = self.reports_dir / command / f"latest-{command}.md"
        if latest_file.exists():
            return latest_file.read_text(encoding="utf-8")
        return None

    def get_report_history(self, command: str, limit: int = 10) -> list[Path]:
        """
        Get list of report files for command (newest first).

        Args:
            command: Command name
            limit: Maximum number of reports to return

        Returns:
            List of report file paths
        """
        command_dir = self.reports_dir / command
        if not command_dir.exists():
            return []

        # Get all timestamped reports (exclude latest-*.md)
        pattern = f"*-{command}.md"
        reports = [
            f for f in command_dir.glob(pattern)
            if not f.name.startswith("latest-")
        ]

        # Sort by modification time (newest first)
        reports.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        return reports[:limit]

    def _cleanup_old_reports(
        self,
        command_dir: Path,
        command: str,
        max_reports: int
    ) -> None:
        """
        Delete old reports, keeping only the last N.

        Args:
            command_dir: Directory containing reports
            command: Command name
            max_reports: Maximum number of reports to keep
        """
        # Get all timestamped reports (exclude latest-*.md)
        pattern = f"*-{command}.md"
        reports = [
            f for f in command_dir.glob(pattern)
            if not f.name.startswith("latest-")
        ]

        # Sort by modification time (newest first)
        reports.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        # Delete old reports (keep last max_reports)
        for old_report in reports[max_reports:]:
            old_report.unlink()

    def get_report_path(self, command: str) -> Path:
        """
        Get directory path where reports for command are stored.

        Args:
            command: Command name

        Returns:
            Path to report directory
        """
        return self.reports_dir / command

    def clear_reports(self, command: Optional[str] = None) -> int:
        """
        Clear all reports for a command (or all commands).

        Args:
            command: Command name, or None to clear all

        Returns:
            Number of reports deleted
        """
        deleted = 0

        if command:
            # Clear specific command reports
            command_dir = self.reports_dir / command
            if command_dir.exists():
                for report in command_dir.glob("*.md"):
                    report.unlink()
                    deleted += 1
                # Remove directory if empty
                if not any(command_dir.iterdir()):
                    command_dir.rmdir()
        else:
            # Clear all reports
            if self.reports_dir.exists():
                for command_dir in self.reports_dir.iterdir():
                    if command_dir.is_dir():
                        for report in command_dir.glob("*.md"):
                            report.unlink()
                            deleted += 1
                        # Remove directory if empty
                        if not any(command_dir.iterdir()):
                            command_dir.rmdir()

        return deleted


# Convenience function
def save_report(command: str, content: str, project_root: Optional[Path] = None) -> Path:
    """
    Convenience function to save a report.

    Args:
        command: Command name
        content: Report content
        project_root: Project root directory

    Returns:
        Path to saved report
    """
    manager = ReportManager(project_root)
    return manager.save_report(command, content)


__all__ = [
    "ReportManager",
    "save_report",
]
