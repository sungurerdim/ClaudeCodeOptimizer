"""Global installation system for ClaudeCodeOptimizer."""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from .. import __version__
from .. import config as CCOConfig  # noqa: N812
from .constants import EXECUTABLE_PERMISSION


class GlobalInstaller:
    """Handles system-wide installation of CCO."""

    def __init__(self) -> None:
        self.config = CCOConfig

    def install(self) -> Dict[str, Any]:
        """
        Install CCO globally.

        Always updates global commands (overwrites existing).
        Creates missing directories and files if not present.

        Returns:
            Dictionary with installation result:
            - success: bool
            - install_dir: Path
            - error: Optional error message
        """
        try:
            global_dir = self.config.get_global_dir()

            # Create directory structure (idempotent - safe to call multiple times)
            self._create_directories()

            # Install core files
            self._install_core_files()

            # Install command templates
            self._install_commands()

            # Install knowledge base (principles, guides, skills, agents, templates)
            from .knowledge_setup import setup_global_knowledge
            setup_global_knowledge(force=True)

            # Install statusline
            self._install_statusline()

            # Create marker file
            marker_file = global_dir / self.config.GLOBAL_MARKER_FILE
            marker_file.write_text(
                json.dumps(
                    {
                        "version": self.config.VERSION,
                        "installed_at": str(Path.cwd()),
                    },
                    indent=2,
                ),
            )

            return {
                "success": True,
                "install_dir": global_dir,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _create_directories(self) -> None:
        """Create global directory structure with flat organization."""
        directories = [
            self.config.get_global_dir(),
            self.config.get_templates_dir(),
            self.config.get_global_commands_dir(),
            self.config.get_principles_dir(),
            self.config.get_guides_dir(),
            self.config.get_skills_dir(),
            self.config.get_agents_dir(),
            self.config.get_projects_registry_dir(),
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _install_core_files(self) -> None:
        """Install core configuration files."""
        # Global config file
        config_file = self.config.get_global_config_file()
        config_file.write_text(
            json.dumps(self.config.DEFAULT_CONFIG, indent=2),
        )

        # Registry index
        registry_index = self.config.get_registry_index_file()
        registry_index.write_text(
            json.dumps(
                {
                    "version": self.config.VERSION,
                    "projects": {},
                    "total_projects": 0,
                },
                indent=2,
            ),
        )

    def _install_commands(self) -> None:
        """
        Install command templates to appropriate locations.

        NEW ARCHITECTURE (v3.1):
        - ALL commands → ~/.cco/commands/ (28 commands)
        - ONLY init.md and remove.md → ~/.claude/commands/ (global availability)

        Rationale:
        - Projects symlink selected commands from ~/.cco/commands/ during init
        - init and remove must be globally available before project initialization
        """
        package_root = Path(__file__).parent.parent
        package_commands = package_root / "commands"

        if not package_commands.exists():
            return

        # 1. Install ALL commands to ~/.cco/commands/ (template storage)
        global_commands_dir = self.config.get_global_commands_dir()
        if global_commands_dir.exists():
            for old_file in global_commands_dir.glob("*.md"):
                old_file.unlink()

        global_commands_dir.mkdir(parents=True, exist_ok=True)

        for command_file in package_commands.glob("*.md"):
            dest_file = global_commands_dir / command_file.name
            dest_file.write_text(command_file.read_text(encoding="utf-8"), encoding="utf-8")

        # 2. Install ONLY init.md and remove.md to ~/.claude/commands/ (global availability)
        claude_commands_dir = Path.home() / ".claude" / "commands"
        claude_commands_dir.mkdir(parents=True, exist_ok=True)

        for global_command in ["init.md", "remove.md"]:
            source_file = global_commands_dir / global_command
            if source_file.exists():
                dest_file = claude_commands_dir / f"cco-{global_command}"
                dest_file.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8")


    def _install_statusline(self) -> None:
        """
        Install statusline to global CCO directory.

        Location: ~/.cco/statusline.js
        Projects will symlink to this file from .claude/statusline.js during init.
        """
        import shutil

        # Get global CCO directory
        global_dir = self.config.get_global_dir()

        # Get statusline from package assets
        package_root = Path(__file__).parent.parent
        statusline_source = package_root / "assets" / "statusline.js"

        if not statusline_source.exists():
            raise FileNotFoundError(
                f"Statusline asset not found: {statusline_source}. "
                "Please ensure the package is properly installed.",
            )

        # Copy to global CCO directory (single source of truth)
        statusline_dest = global_dir / "statusline.js"
        shutil.copy2(statusline_source, statusline_dest)

    def uninstall(self) -> Dict[str, Any]:
        """
        Uninstall CCO globally.

        Returns:
            Dictionary with uninstallation result
        """
        try:
            global_dir = self.config.get_global_dir()

            if not global_dir.exists():
                return {
                    "success": False,
                    "error": "CCO is not installed",
                }

            # Move to trash instead of permanent delete
            backup_dir = global_dir.parent / f"{global_dir.name}.uninstalled"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.move(str(global_dir), str(backup_dir))

            return {
                "success": True,
                "backup_dir": backup_dir,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def upgrade(self, from_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Upgrade CCO to latest version.

        Args:
            from_version: Current version (auto-detected if not provided)

        Returns:
            Dictionary with upgrade result
        """
        try:
            # Read current version
            marker_file = self.config.get_global_dir() / self.config.GLOBAL_MARKER_FILE
            if marker_file.exists():
                marker_data = json.loads(marker_file.read_text())
                current_version = marker_data.get("version", "unknown")
            else:
                current_version = "unknown"

            # Perform upgrade (preserve user data)
            # For now, just update marker
            marker_file.write_text(
                json.dumps(
                    {
                        "version": self.config.VERSION,
                        "upgraded_from": current_version,
                    },
                    indent=2,
                ),
            )

            return {
                "success": True,
                "from_version": current_version,
                "to_version": self.config.VERSION,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
