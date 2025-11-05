"""Central project registry system for ClaudeCodeOptimizer."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import CCOConfig


class ProjectRegistry:
    """Manages central registry of all CCO-managed projects."""

    def __init__(self) -> None:
        self.config = CCOConfig
        self.registry_dir = self.config.get_projects_registry_dir()
        self.index_file = self.config.get_registry_index_file()

    def register_project(
        self,
        project_name: str,
        project_root: Path,
        analysis: Dict[str, Any],
        preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Register a project in the central registry.

        Args:
            project_name: Unique project name
            project_root: Project root directory
            analysis: Project analysis data
            preferences: CCO preferences (from quick or interactive mode)

        Returns:
            Registration result dictionary
        """
        try:
            # Ensure registry directory exists
            self.registry_dir.mkdir(parents=True, exist_ok=True)

            # Create project registry file
            project_file = self.config.get_project_registry_file(project_name)

            project_data = {
                "name": project_name,
                "root": str(project_root.absolute()),
                "registered_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "analysis": analysis,
                "preferences": preferences or {},
                "selected_principles": (
                    preferences.get("selected_principle_ids", []) if preferences else []
                ),
                "status": "active",
                "metadata": {
                    "cco_version": self.config.VERSION,
                    "commands_count": len(analysis.get("commands", [])),
                    "language": analysis.get("language", "unknown"),
                    "type": analysis.get("type", "unknown"),
                },
                "state": {
                    "sessions": [],
                    "command_usage": {},
                    "audit_history": [],
                    "last_session_id": None,
                    "total_sessions": 0,
                    "total_commands_run": 0,
                },
            }

            project_file.write_text(json.dumps(project_data, indent=2))

            # Update index
            self._update_index(project_name, project_root)

            return {
                "success": True,
                "project_name": project_name,
                "registry_file": project_file,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _update_index(self, project_name: str, project_root: Path) -> None:
        """Update the master registry index."""
        # Load existing index
        if self.index_file.exists():
            index_data = json.loads(self.index_file.read_text())
        else:
            index_data = {
                "version": self.config.VERSION,
                "projects": {},
                "total_projects": 0,
            }

        # Add/update project entry
        index_data["projects"][project_name] = {
            "root": str(project_root.absolute()),
            "last_updated": datetime.now().isoformat(),
        }
        index_data["total_projects"] = len(index_data["projects"])

        # Save index
        self.index_file.write_text(json.dumps(index_data, indent=2))

    def get_project(self, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Get project data from registry.

        Args:
            project_name: Project name

        Returns:
            Project data or None if not found
        """
        project_file = self.config.get_project_registry_file(project_name)

        if not project_file.exists():
            return None

        try:
            return json.loads(project_file.read_text())
        except Exception:
            return None

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all registered projects.

        Returns:
            List of project summaries
        """
        if not self.index_file.exists():
            return []

        try:
            index_data = json.loads(self.index_file.read_text())
            projects = []

            for project_name, project_info in index_data.get("projects", {}).items():
                project_data = self.get_project(project_name)
                if project_data:
                    projects.append(
                        {
                            "name": project_name,
                            "root": project_info["root"],
                            "language": project_data.get("analysis", {}).get(
                                "language",
                                "unknown",
                            ),
                            "type": project_data.get("analysis", {}).get("type", "unknown"),
                            "last_updated": project_info["last_updated"],
                            "status": project_data.get("status", "unknown"),
                        },
                    )

            return projects

        except Exception:
            return []

    def unregister_project(self, project_name: str) -> Dict[str, Any]:
        """
        Remove project from registry.

        Args:
            project_name: Project name

        Returns:
            Unregistration result
        """
        try:
            project_file = self.config.get_project_registry_file(project_name)

            if not project_file.exists():
                return {
                    "success": False,
                    "error": "Project not found in registry",
                }

            # Remove project file
            project_file.unlink()

            # Update index
            if self.index_file.exists():
                index_data = json.loads(self.index_file.read_text())
                if project_name in index_data.get("projects", {}):
                    del index_data["projects"][project_name]
                    index_data["total_projects"] = len(index_data["projects"])
                    self.index_file.write_text(json.dumps(index_data, indent=2))

            return {
                "success": True,
                "project_name": project_name,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def update_project_analysis(
        self,
        project_name: str,
        analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update project analysis data.

        Args:
            project_name: Project name
            analysis: New analysis data

        Returns:
            Update result
        """
        try:
            project_data = self.get_project(project_name)

            if not project_data:
                return {
                    "success": False,
                    "error": "Project not found",
                }

            # Update analysis
            project_data["analysis"] = analysis
            project_data["last_updated"] = datetime.now().isoformat()
            project_data["metadata"]["commands_count"] = len(analysis.get("commands", []))

            # Save
            project_file = self.config.get_project_registry_file(project_name)
            project_file.write_text(json.dumps(project_data, indent=2))

            # Update index timestamp
            self._update_index(project_name, Path(project_data["root"]))

            return {
                "success": True,
                "project_name": project_name,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def find_project_by_root(self, project_root: Path) -> Optional[str]:
        """
        Find project name by root directory.

        Args:
            project_root: Project root directory

        Returns:
            Project name or None if not found
        """
        if not self.index_file.exists():
            return None

        try:
            index_data = json.loads(self.index_file.read_text())
            project_root_str = str(project_root.absolute())

            for project_name, project_info in index_data.get("projects", {}).items():
                if project_info["root"] == project_root_str:
                    return project_name

            return None

        except Exception:
            return None
