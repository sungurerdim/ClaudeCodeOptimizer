"""State tracking system for ClaudeCodeOptimizer.

Tracks sessions, command usage, and audit history for projects.
All state is stored in global registry (~/.cco/projects/PROJECT_NAME.json).
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import CCOConfig
from .constants import AUDIT_RECENT_COUNT, AUDIT_TREND_WINDOW, MAX_AUDIT_HISTORY
from .registry import ProjectRegistry


class StateTracker:
    """Manages state tracking for CCO projects."""

    def __init__(self, project_name: str) -> None:
        """
        Initialize state tracker for a project.

        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.config = CCOConfig
        self.registry = ProjectRegistry()

    def _get_project_data(self) -> Optional[Dict[str, Any]]:
        """Get current project data from registry."""
        return self.registry.get_project(self.project_name)

    def _save_project_data(self, project_data: Dict[str, Any]) -> bool:
        """Save updated project data to registry."""
        try:
            project_file = self.config.get_project_registry_file(self.project_name)
            project_data["last_updated"] = datetime.now().isoformat()
            project_file.write_text(json.dumps(project_data, indent=2))
            return True
        except Exception:
            return False

    # ========================================================================
    # Session Tracking
    # ========================================================================

    def start_session(self) -> Optional[str]:
        """
        Start a new session.

        Returns:
            Session ID or None if failed
        """
        project_data = self._get_project_data()
        if not project_data:
            return None

        session_id = str(uuid.uuid4())
        session = {
            "id": session_id,
            "start": datetime.now().isoformat(),
            "end": None,
            "duration": None,
            "commands_run": 0,
        }

        # Initialize state if not present
        if "state" not in project_data:
            project_data["state"] = {
                "sessions": [],
                "command_usage": {},
                "audit_history": [],
                "last_session_id": None,
                "total_sessions": 0,
                "total_commands_run": 0,
            }

        project_data["state"]["sessions"].append(session)
        project_data["state"]["last_session_id"] = session_id
        project_data["state"]["total_sessions"] += 1

        self._save_project_data(project_data)
        return session_id

    def end_session(self, session_id: str) -> bool:
        """
        End an active session.

        Args:
            session_id: Session ID to end

        Returns:
            True if successful, False otherwise
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return False

        # Find and update session
        for session in project_data["state"]["sessions"]:
            if session["id"] == session_id and session["end"] is None:
                end_time = datetime.now()
                start_time = datetime.fromisoformat(session["start"])
                duration = int((end_time - start_time).total_seconds())

                session["end"] = end_time.isoformat()
                session["duration"] = duration

                return self._save_project_data(project_data)

        return False

    def get_active_session(self) -> Optional[Dict[str, Any]]:
        """
        Get the current active session.

        Returns:
            Active session data or None
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return None

        # Find most recent session without end time
        for session in reversed(project_data["state"]["sessions"]):
            if session["end"] is None:
                return session

        return None

    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get session statistics.

        Returns:
            Dictionary with session stats
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return {
                "total_sessions": 0,
                "average_duration": 0,
                "total_duration": 0,
            }

        sessions = project_data["state"]["sessions"]
        completed_sessions = [s for s in sessions if s.get("duration") is not None]

        total_duration = sum(s["duration"] for s in completed_sessions)
        avg_duration = total_duration / len(completed_sessions) if completed_sessions else 0

        return {
            "total_sessions": len(sessions),
            "completed_sessions": len(completed_sessions),
            "active_sessions": len(sessions) - len(completed_sessions),
            "average_duration": int(avg_duration),
            "total_duration": total_duration,
        }

    # ========================================================================
    # Command Usage Tracking
    # ========================================================================

    def record_command(
        self,
        command: str,
        duration_ms: Optional[int] = None,
        success: bool = True,
    ) -> bool:
        """
        Record command execution.

        Args:
            command: Command name (e.g., "cco-status")
            duration_ms: Execution duration in milliseconds
            success: Whether command succeeded

        Returns:
            True if recorded successfully
        """
        project_data = self._get_project_data()
        if not project_data:
            return False

        # Initialize state if not present
        if "state" not in project_data:
            project_data["state"] = {
                "sessions": [],
                "command_usage": {},
                "audit_history": [],
                "last_session_id": None,
                "total_sessions": 0,
                "total_commands_run": 0,
            }

        command_usage = project_data["state"]["command_usage"]

        # Initialize command stats if not present
        if command not in command_usage:
            command_usage[command] = {
                "count": 0,
                "total_duration_ms": 0,
                "avg_duration_ms": 0,
                "success_count": 0,
                "failure_count": 0,
                "success_rate": 1.0,
                "last_run": None,
            }

        stats = command_usage[command]
        stats["count"] += 1
        stats["last_run"] = datetime.now().isoformat()

        if success:
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1

        stats["success_rate"] = stats["success_count"] / stats["count"]

        if duration_ms is not None:
            stats["total_duration_ms"] += duration_ms
            stats["avg_duration_ms"] = stats["total_duration_ms"] // stats["count"]

        # Update total commands run
        project_data["state"]["total_commands_run"] += 1

        # Update active session
        active_session = self.get_active_session()
        if active_session:
            for session in project_data["state"]["sessions"]:
                if session["id"] == active_session["id"]:
                    session["commands_run"] += 1
                    break

        return self._save_project_data(project_data)

    def get_command_stats(self, command: Optional[str] = None) -> Dict[str, Any]:
        """
        Get command usage statistics.

        Args:
            command: Specific command name, or None for all commands

        Returns:
            Dictionary with command stats
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return {}

        command_usage = project_data["state"]["command_usage"]

        if command:
            return command_usage.get(command, {})

        return command_usage

    def get_most_used_commands(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most frequently used commands.

        Args:
            limit: Maximum number of commands to return

        Returns:
            List of command stats, sorted by usage count
        """
        command_usage = self.get_command_stats()

        commands = [{"command": cmd, **stats} for cmd, stats in command_usage.items()]

        commands.sort(key=lambda x: x["count"], reverse=True)
        return commands[:limit]

    # ========================================================================
    # Audit History Tracking
    # ========================================================================

    def record_audit(
        self,
        command: str,
        passed: int,
        failed: int,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Record audit results.

        Args:
            command: Audit command name
            passed: Number of checks passed
            failed: Number of checks failed
            details: Optional additional details

        Returns:
            True if recorded successfully
        """
        project_data = self._get_project_data()
        if not project_data:
            return False

        # Initialize state if not present
        if "state" not in project_data:
            project_data["state"] = {
                "sessions": [],
                "command_usage": {},
                "audit_history": [],
                "last_session_id": None,
                "total_sessions": 0,
                "total_commands_run": 0,
            }

        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "passed": passed,
            "failed": failed,
            "total": passed + failed,
            "success_rate": passed / (passed + failed) if (passed + failed) > 0 else 0,
        }

        if details:
            audit_entry["details"] = details

        project_data["state"]["audit_history"].append(audit_entry)

        # Keep only last MAX_AUDIT_HISTORY audit entries
        if len(project_data["state"]["audit_history"]) > MAX_AUDIT_HISTORY:
            project_data["state"]["audit_history"] = project_data["state"]["audit_history"][
                -MAX_AUDIT_HISTORY:
            ]

        return self._save_project_data(project_data)

    def get_audit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent audit history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of audit entries, most recent first
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return []

        audit_history = project_data["state"]["audit_history"]
        return list(reversed(audit_history[-limit:]))

    def get_audit_trends(self) -> Dict[str, Any]:
        """
        Get audit trend statistics.

        Returns:
            Dictionary with audit trends
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return {
                "total_audits": 0,
                "average_success_rate": 0,
                "trend": "stable",
            }

        audit_history = project_data["state"]["audit_history"]

        if not audit_history:
            return {
                "total_audits": 0,
                "average_success_rate": 0,
                "trend": "stable",
            }

        # Calculate average success rate
        avg_success_rate = sum(a["success_rate"] for a in audit_history) / len(audit_history)

        # Calculate trend (last N vs previous N)
        trend = "stable"
        if len(audit_history) >= AUDIT_TREND_WINDOW:
            recent_rate = (
                sum(a["success_rate"] for a in audit_history[-AUDIT_RECENT_COUNT:])
                / AUDIT_RECENT_COUNT
            )
            previous_rate = (
                sum(
                    a["success_rate"]
                    for a in audit_history[-AUDIT_TREND_WINDOW:-AUDIT_RECENT_COUNT]
                )
                / AUDIT_RECENT_COUNT
            )

            if recent_rate > previous_rate + 0.1:
                trend = "improving"
            elif recent_rate < previous_rate - 0.1:
                trend = "declining"

        return {
            "total_audits": len(audit_history),
            "average_success_rate": avg_success_rate,
            "trend": trend,
            "last_audit": audit_history[-1] if audit_history else None,
        }

    # ========================================================================
    # Principles & Variables Management
    # ========================================================================

    def set_active_principles(self, principle_ids: List[str]) -> bool:
        """
        Set active principles for the project.

        Args:
            principle_ids: List of principle IDs to activate

        Returns:
            True if saved successfully
        """
        project_data = self._get_project_data()
        if not project_data:
            return False

        if "state" not in project_data:
            project_data["state"] = {}

        project_data["state"]["active_principles"] = principle_ids
        return self._save_project_data(project_data)

    def get_active_principles(self) -> List[str]:
        """
        Get active principles for the project.

        Returns:
            List of principle IDs
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return []

        return project_data["state"].get("active_principles", [])

    def set_template_variables(self, variables: Dict[str, Any]) -> bool:
        """
        Set template variables for the project.

        Args:
            variables: Dictionary of variable name -> value

        Returns:
            True if saved successfully
        """
        project_data = self._get_project_data()
        if not project_data:
            return False

        if "state" not in project_data:
            project_data["state"] = {}

        project_data["state"]["template_variables"] = variables
        return self._save_project_data(project_data)

    def get_template_variables(self) -> Dict[str, Any]:
        """
        Get template variables for the project.

        Returns:
            Dictionary of variables
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return {}

        return project_data["state"].get("template_variables", {})

    def update_analysis(self, analysis: Dict[str, Any]) -> bool:
        """
        Update project analysis data.

        Args:
            analysis: Analysis dictionary

        Returns:
            True if saved successfully
        """
        project_data = self._get_project_data()
        if not project_data:
            return False

        project_data["analysis"] = analysis
        return self._save_project_data(project_data)

    def get_analysis(self) -> Dict[str, Any]:
        """
        Get project analysis data.

        Returns:
            Analysis dictionary
        """
        project_data = self._get_project_data()
        if not project_data:
            return {}

        return project_data.get("analysis", {})

    # ========================================================================
    # Data Cleanup & Maintenance
    # ========================================================================

    def cleanup_old_data(self, retention_days: int = 90) -> bool:
        """
        Clean up data older than retention period.

        Args:
            retention_days: Number of days to retain data (default: 90)

        Returns:
            True if cleaned successfully
        """
        project_data = self._get_project_data()
        if not project_data or "state" not in project_data:
            return False

        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=retention_days)

        # Clean old sessions
        if "sessions" in project_data["state"]:
            project_data["state"]["sessions"] = [
                s
                for s in project_data["state"]["sessions"]
                if datetime.fromisoformat(s["start"]) > cutoff_date
            ]

        # Clean old audit history
        if "audit_history" in project_data["state"]:
            project_data["state"]["audit_history"] = [
                a
                for a in project_data["state"]["audit_history"]
                if datetime.fromisoformat(a["timestamp"]) > cutoff_date
            ]

        return self._save_project_data(project_data)

    # ========================================================================
    # State Export & Summary
    # ========================================================================

    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get complete state summary.

        Returns:
            Dictionary with all state information
        """
        project_data = self._get_project_data()

        return {
            "project_name": self.project_name,
            "session_stats": self.get_session_stats(),
            "command_stats": {
                "total_commands_run": (
                    project_data.get("state", {}).get("total_commands_run", 0)
                    if project_data
                    else 0
                ),
                "most_used": self.get_most_used_commands(5),
            },
            "audit_stats": self.get_audit_trends(),
            "active_principles_count": len(self.get_active_principles()),
            "template_variables_count": len(self.get_template_variables()),
        }

    def export_state(self, output_file: Path) -> bool:
        """
        Export state data to JSON file.

        Args:
            output_file: Output file path

        Returns:
            True if exported successfully
        """
        try:
            project_data = self._get_project_data()
            if not project_data or "state" not in project_data:
                return False

            state_data = {
                "project_name": self.project_name,
                "exported_at": datetime.now().isoformat(),
                "state": project_data["state"],
                "analysis": project_data.get("analysis", {}),
            }

            output_file.write_text(json.dumps(state_data, indent=2))
            return True

        except Exception:
            return False
