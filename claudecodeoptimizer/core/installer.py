"""Global installation system for ClaudeCodeOptimizer."""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from .. import __version__
from .. import config as CCOConfig
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

            # Install templates
            self._install_templates()

            # Install knowledge base
            self._install_knowledge_base()

            # Install statusline
            self._install_statusline()

            # Install skills
            self._install_skills()

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
        """Create global directory structure."""
        directories = [
            self.config.get_global_dir(),
            self.config.get_templates_dir(),
            self.config.get_knowledge_dir(),
            self.config.get_projects_registry_dir(),
            self.config.get_templates_dir() / "commands",
            self.config.get_templates_dir() / "hooks",
            self.config.get_templates_dir() / "generic",
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

    def _install_templates(self) -> None:
        """
        Install commands (single source of truth: commands/*.md).

        All commands are in one place: claudecodeoptimizer/commands/
        - init.md, remove.md → ~/.claude/commands/cco-*.md (global slash commands)
        - All other *.md → ~/.cco/commands/ (ready-to-use commands for projects)
        """
        package_root = Path(__file__).parent.parent
        package_commands = package_root / "commands"

        if not package_commands.exists():
            return

        # 1. Clean old commands (from previous installs)
        global_commands_dir = self.config.get_global_commands_dir()
        if global_commands_dir.exists():
            for old_file in global_commands_dir.glob("*.md"):
                old_file.unlink()

        global_commands_dir.mkdir(parents=True, exist_ok=True)

        # 2. Install global slash commands to ~/.claude/commands/
        claude_commands = self.config.get_claude_dir() / "commands"
        claude_commands.mkdir(parents=True, exist_ok=True)

        # 3. Install commands
        for command_file in package_commands.glob("*.md"):
            # Global slash commands: init.md, remove.md
            if command_file.stem in ["init", "remove"]:
                dest_file = claude_commands / f"cco-{command_file.name}"
                dest_file.write_text(command_file.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                # Regular commands to global CCO storage
                dest_file = global_commands_dir / command_file.name
                dest_file.write_text(command_file.read_text(encoding="utf-8"), encoding="utf-8")

        # 4. Create sample hook
        self._create_sample_hook()

    def _install_global_commands(self) -> None:
        """Deprecated - merged into _install_templates()."""
        pass

    def _create_sample_hook(self) -> None:
        """Create sample hook."""
        global_dir = self.config.get_global_dir()
        hooks_dir = global_dir / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        sample_hook = hooks_dir / "pre-commit.sh.example"
        sample_hook.write_text(
            """#!/bin/bash
# Sample pre-commit hook for CCO

echo "Running pre-commit checks..."

# Add your checks here

exit 0
""",
        )
        try:
            sample_hook.chmod(EXECUTABLE_PERMISSION)
        except (OSError, NotImplementedError, AttributeError) as e:
            # Windows doesn't fully support chmod, or file system may not support it
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Could not set executable permission on {sample_hook}: {e}")

    def _install_knowledge_base(self) -> None:
        """Install knowledge base files."""
        knowledge_dir = self.config.get_knowledge_dir()
        package_root = Path(__file__).parent.parent

        # Copy complete principles.json from package (52 principles)
        principles_source = package_root / "knowledge" / "principles.json"
        principles_dest = knowledge_dir / "principles.json"

        if principles_source.exists():
            # Copy full principles file
            shutil.copy2(principles_source, principles_dest)
        else:
            # Fallback: Create minimal principles file if source not found
            principles_dest.write_text(
                json.dumps(
                    {
                        "version": __version__,
                        "total_principles": 2,
                        "principles": [
                            {
                                "id": "P001",
                                "number": 1,
                                "title": "Fail-Fast Error Handling",
                                "category": "code_quality",
                                "severity": "critical",
                                "weight": 10,
                                "description": "Catch errors early in development cycle",
                                "applicability": {"project_types": ["all"], "languages": ["all"]},
                                "rules": [],
                                "examples": {"bad": [], "good": []},
                                "autofix": {"available": False},
                            },
                            {
                                "id": "P002",
                                "number": 2,
                                "title": "DRY Enforcement",
                                "category": "code_quality",
                                "severity": "high",
                                "weight": 10,
                                "description": "Avoid code duplication",
                                "applicability": {"project_types": ["all"], "languages": ["all"]},
                                "rules": [],
                                "examples": {"bad": [], "good": []},
                                "autofix": {"available": False},
                            },
                        ],
                        "selection_strategies": {
                            "auto": {"description": "Auto-select based on project", "rules": []},
                            "minimal": {"description": "Minimal set", "include": ["P001", "P002"]},
                            "comprehensive": {"description": "All principles", "include": "all"},
                        },
                    },
                    indent=2,
                ),
            )

        # Create README
        readme_file = knowledge_dir / "README.md"
        readme_file.write_text(
            f"""# {self.config.DISPLAY_NAME} - Knowledge Base

This directory contains development principles and best practices.

## Files

- `principles.json` - 52 development principles
- `patterns.json` - Common code patterns and anti-patterns (future)

## Principles System

CCO includes 52 comprehensive development principles organized by category:
- Code Quality (10 principles)
- Architecture (8 principles)
- Security & Privacy (12 principles)
- Operational Excellence (6 principles)
- Testing (6 principles)
- Git Workflow (5 principles)
- Performance (4 principles)
- API Design (1 principle)

Principles are dynamically selected based on:
- Project type (api, web, ml, microservices, library, cli)
- Primary language (python, javascript, typescript, go, rust, java, etc.)
- Team size (solo, small, medium, large)
- Project characteristics (privacy_critical, security_critical, performance_critical)
- User preferences

## Usage

These principles are used by CCO commands to:
- Validate code quality (cco-audit-code, cco-audit-principles)
- Auto-fix common issues (cco-fix-code)
- Provide intelligent recommendations (cco-self-optimize)
- Generate project-specific guidelines

## Selection Strategies

- **auto**: Dynamically select based on project characteristics (recommended)
- **minimal**: Core 15 principles applicable to all projects
- **comprehensive**: All 52 principles (maximum validation)

Edit `~/.cco/projects/PROJECT_NAME.json` to customize active principles for your project.
""",
        )

    def _install_statusline(self) -> None:
        """
        Install statusline template to global CCO templates directory.

        Template location: ~/.cco/templates/statusline.js
        Projects will copy this template to .claude/statusline.js during init.
        """
        import shutil

        # Get templates directory
        templates_dir = self.config.get_templates_dir()

        # Get statusline from package assets
        package_root = Path(__file__).parent.parent
        statusline_source = package_root / "assets" / "statusline.js"

        if not statusline_source.exists():
            raise FileNotFoundError(
                f"Statusline asset not found: {statusline_source}. "
                "Please ensure the package is properly installed.",
            )

        # Copy to global templates directory (not directly to ~/.claude)
        statusline_dest = templates_dir / "generic" / "statusline.js"
        statusline_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(statusline_source, statusline_dest)

        # Also install settings template
        settings_source = package_root / "assets" / "settings.local.template.json"
        if settings_source.exists():
            settings_dest = templates_dir / "generic" / "settings.local.template.json"
            shutil.copy2(settings_source, settings_dest)

    def _install_skills(self) -> None:
        """Install skills to ~/.claude/skills/ directory."""

        # Get package skills directory
        package_root = Path(__file__).parent.parent
        skills_source = package_root / "skills"

        if not skills_source.exists():
            # Skills directory doesn't exist yet - skip installation
            return

        # Create ~/.claude/skills/ directory
        claude_skills_dir = self.config.get_claude_dir() / "skills"
        claude_skills_dir.mkdir(parents=True, exist_ok=True)

        # Copy all skill files to global skills directory
        for skill_file in skills_source.glob("*.md"):
            dest_file = claude_skills_dir / skill_file.name
            dest_file.write_text(skill_file.read_text(encoding="utf-8"), encoding="utf-8")

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
