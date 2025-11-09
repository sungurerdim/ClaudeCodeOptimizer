"""Project management for ClaudeCodeOptimizer."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .. import config as CCOConfig  # noqa: N812
from ..schemas.preferences import (
    CCOPreferences,
    CodeQualityStandards,
    DevelopmentStyle,
    ProjectIdentity,
)
from .analyzer import ProjectAnalyzer
from .change_manifest import ChangeManifest
from .constants import (
    DEFAULT_TEST_COVERAGE_TARGET,
    MINIMAL_TEST_COVERAGE_TARGET,
    SEPARATOR_WIDTH,
    TOP_ITEMS_DISPLAY,
)
from .principle_selector import PrincipleSelector
from .registry import ProjectRegistry
from .safe_print import safe_print
from .utils import print_separator

logger = logging.getLogger(__name__)


class ProjectManager:
    """Manages CCO project initialization and configuration."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.absolute()
        self.config = CCOConfig
        self.registry = ProjectRegistry()
        self.analyzer = ProjectAnalyzer(self.project_root)
        self.manifest = ChangeManifest(self.project_root)

    def initialize(
        self,
        project_name: Optional[str] = None,
        mode: str = "quick",
    ) -> Dict[str, Any]:
        """
        Initialize CCO for the project.

        NOTE: Every init performs full analysis - no difference between first and 20th run.
        This ensures project state is always accurate and up-to-date.

        Two modes:
        1. Quick mode (default): Auto-detect and setup with defaults
        2. Interactive mode: Full wizard with comprehensive customization

        Args:
            project_name: Project name (defaults to directory name)
            mode: Initialization mode ('quick' or 'interactive')

        Returns:
            Initialization result dictionary
        """
        # Validate mode parameter
        if mode not in ("quick", "interactive"):
            raise ValueError(f"Invalid mode '{mode}'. Must be 'quick' or 'interactive'")

        # Interactive mode: Launch full wizard
        if mode == "interactive":
            return self._initialize_interactive(project_name)

        # Quick mode: Full analysis every time
        return self._initialize_quick(project_name)

    def _initialize_quick(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced quick initialization with AI-driven preferences.

        Every init performs:
        1. Full project analysis with Universal Detector
        2. AI creates intelligent preferences (instead of user answering 58 questions)
        3. Select applicable principles based on preferences
        4. Generate PRINCIPLES.md
        5. Register in global registry
        6. Install statusline
        7. Generate generic commands
        """

        # Determine project name
        if not project_name:
            project_name = self.project_root.name

        # STEP 1: Comprehensive project analysis
        safe_print(f"\n📊 Analyzing project: {project_name}")
        safe_print("   This may take a moment...")

        analysis = self.analyzer.analyze()

        # Print analysis summary
        self._print_analysis_summary(analysis)

        # STEP 2: AI creates intelligent preferences
        safe_print("\n🤖 Creating intelligent preferences...")
        preferences = self._create_ai_preferences(project_name, analysis)

        # STEP 3: Select applicable principles
        safe_print("\n📋 Selecting applicable principles...")
        selected_principles = self._select_and_generate_principles(preferences)
        safe_print(f"   ✓ {len(selected_principles)} principles selected")

        # STEP 3.5: Generate/Update CLAUDE.md
        safe_print("\n📝 Generating CLAUDE.md...")
        claude_md_result = self._generate_claude_md(preferences)
        if claude_md_result["success"]:
            safe_print(f"   ✓ CLAUDE.md {claude_md_result.get('strategy', 'generated')}")

        # STEP 4: Register/update in global registry
        # Add selected principle IDs to preferences for storage
        preferences_dict = preferences.model_dump(mode="json")
        preferences_dict["selected_principle_ids"] = [p["id"] for p in selected_principles]

        self.registry.register_project(
            project_name=project_name,
            project_root=self.project_root,
            analysis=analysis,
            preferences=preferences_dict,
        )

        # STEP 5: Install statusline to project
        self._install_project_statusline()

        # STEP 6: Generate generic commands
        commands_generated = self._generate_generic_commands(analysis)

        # STEP 7: Print recommendations
        self._print_recommendations(analysis)

        # STEP 8: Save change tracking manifest
        # Note: Manifest is now stored in global storage (~/.cco/projects/{name}/changes.json)
        # No .cco/ directory is created in project - zero project pollution
        self.manifest.save()

        # STEP 9: Print installation summary report
        self._print_installation_summary()

        return {
            "success": True,
            "mode": "quick",
            "project_name": project_name,
            "analysis": analysis,
            "preferences": preferences.model_dump(mode="json"),
            "selected_principles": [p["id"] for p in selected_principles],
            "commands_generated": commands_generated,
        }

    def _print_analysis_summary(self, analysis: Dict[str, Any]) -> None:
        """Print detailed analysis summary."""
        safe_print()
        print_separator("=", SEPARATOR_WIDTH)
        safe_print("PROJECT ANALYSIS SUMMARY")
        print_separator("=", SEPARATOR_WIDTH)

        # Languages
        if analysis.get("languages"):
            safe_print("\n📝 Languages Detected:")
            for lang in analysis["languages"][: TOP_ITEMS_DISPLAY["languages"]]:
                confidence = lang["confidence"]
                evidence = ", ".join(lang["evidence"][:2])
                safe_print(f"   • {lang['name']:15} {confidence:5.1f}%  ({evidence})")

        # Primary language
        if analysis.get("primary_language"):
            safe_print(f"\n🎯 Primary Language: {analysis['primary_language']}")

        # Frameworks
        if analysis.get("frameworks"):
            safe_print("\n🔧 Frameworks Detected:")
            for fw in analysis["frameworks"][: TOP_ITEMS_DISPLAY["frameworks"]]:
                confidence = fw["confidence"]
                evidence = ", ".join(fw["evidence"][:1])
                safe_print(f"   • {fw['name']:20} {confidence:5.1f}%  ({evidence})")

        # Primary framework
        if analysis.get("primary_framework"):
            safe_print(f"\n🎯 Primary Framework: {analysis['primary_framework']}")

        # Project type
        if analysis.get("project_types"):
            safe_print("\n📦 Project Type:")
            for ptype in analysis["project_types"][: TOP_ITEMS_DISPLAY["project_types"]]:
                confidence = ptype["confidence"]
                safe_print(f"   • {ptype['type']:15} {confidence:5.1f}%")

        # Tools
        if analysis.get("tools"):
            safe_print("\n🛠️  Development Tools:")
            tool_categories = {
                "Testing": ["pytest", "jest", "mocha", "unittest"],
                "Linting": ["black", "ruff", "eslint", "prettier", "mypy"],
                "CI/CD": ["github-actions", "gitlab-ci", "jenkins", "circleci"],
                "Containers": ["docker", "kubernetes"],
                "Package Mgmt": ["npm", "yarn", "pip", "poetry", "cargo"],
            }

            for category, tool_names in tool_categories.items():
                category_tools = [t for t in analysis["tools"] if t["name"] in tool_names]
                if category_tools:
                    safe_print(f"\n   {category}:")
                    for tool in category_tools[:3]:
                        confidence = tool["confidence"]
                        safe_print(f"      • {tool['name']:15} {confidence:5.1f}%")

        # Statistics
        if analysis.get("statistics"):
            stats = analysis["statistics"]
            safe_print("\n📈 Statistics:")
            safe_print(f"   • Total Files:      {stats.get('total_files', 0)}")
            safe_print(f"   • Source Files:     {stats.get('source_files', 0)}")
            safe_print(f"   • Config Files:     {stats.get('config_files', 0)}")
            safe_print(f"   • Languages Found:  {stats.get('languages_count', 0)}")
            safe_print(f"   • Frameworks Found: {stats.get('frameworks_count', 0)}")

        # Feature flags
        safe_print("\n✨ Features:")
        safe_print(f"   • Tests:   {'✓' if analysis.get('has_tests') else '✗'}")
        safe_print(f"   • Docker:  {'✓' if analysis.get('has_docker') else '✗'}")
        safe_print(f"   • CI/CD:   {'✓' if analysis.get('has_ci_cd') else '✗'}")
        safe_print(f"   • Git:     {'✓' if analysis.get('has_git') else '✗'}")

        # Confidence
        if analysis.get("confidence_level"):
            confidence_emoji = {
                "high": "🟢",
                "medium": "🟡",
                "low": "🔴",
            }
            emoji = confidence_emoji.get(analysis["confidence_level"], "⚪")
            safe_print(f"\n{emoji} Analysis Confidence: {analysis['confidence_level'].upper()}")

        # Duration
        if analysis.get("analysis_duration_ms"):
            duration_sec = analysis["analysis_duration_ms"] / 1000
            safe_print(f"⏱️  Analysis Duration: {duration_sec:.2f}s")

        print_separator("=", SEPARATOR_WIDTH)

    def _print_recommendations(self, analysis: Dict[str, Any]) -> None:
        """Print intelligent recommendations."""
        suggestions = analysis.get("suggestions", [])
        commands = analysis.get("commands", [])

        if suggestions:
            safe_print("\n💡 Recommendations:")
            for i, suggestion in enumerate(suggestions, 1):
                safe_print(f"   {i}. {suggestion}")

        if commands:
            safe_print("\n📋 Available Commands:")
            safe_print(f"   {len(commands)} CCO commands configured based on your project")
            safe_print("\n   Run these commands in Claude Code:")
            for cmd in commands[: TOP_ITEMS_DISPLAY["commands"]]:
                safe_print(f"      • /{cmd}")
            if len(commands) > TOP_ITEMS_DISPLAY["commands"]:
                safe_print(f"      ... and {len(commands) - TOP_ITEMS_DISPLAY['commands']} more")

        safe_print()

    def _print_installation_summary(self) -> None:
        """Print comprehensive installation summary report."""
        from datetime import datetime

        safe_print()
        print_separator("=", SEPARATOR_WIDTH)
        safe_print("   CCO INITIALIZATION COMPLETE")
        print_separator("=", SEPARATOR_WIDTH)
        safe_print()

        # Project info
        safe_print(f"📦 Project: {self.project_root.name}")
        safe_print(f"📅 Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        safe_print()

        # === INSTALLED COMPONENTS ===
        safe_print("## 🎯 Installed Components")
        safe_print()

        # Principles
        principles_file = self.project_root / "PRINCIPLES.md"
        if principles_file.exists():
            try:
                content = principles_file.read_text(encoding="utf-8")

                # Count by severity
                critical = content.count("## CRITICAL")
                high = content.count("## HIGH PRIORITY")

                # Total principles
                total_principles = content.count("### P")

                safe_print("✓ PRINCIPLES.md")
                safe_print(f"  └─ {total_principles} active principles")
                if critical > 0:
                    safe_print(f"     ├─ {critical} Critical (must follow)")
                if high > 0:
                    safe_print(f"     └─ {high} High Priority")
            except Exception:
                safe_print("✓ PRINCIPLES.md (created)")
        else:
            safe_print("✗ PRINCIPLES.md (not found)")

        safe_print()

        # Commands
        commands_dir = self.project_root / ".claude" / "commands"
        if commands_dir.exists():
            cco_commands = sorted(commands_dir.glob("cco-*.md"))

            safe_print(f"✓ Slash Commands ({len(cco_commands)} installed)")

            # Group commands by category
            audit_cmds = [c for c in cco_commands if "audit" in c.stem or "fix" in c.stem]
            generate_cmds = [
                c for c in cco_commands if "generate" in c.stem or "optimize" in c.stem
            ]
            info_cmds = [c for c in cco_commands if "status" in c.stem or "config" in c.stem]

            if audit_cmds:
                safe_print("  ├─ Analysis & Audit")
                for cmd in audit_cmds[:3]:
                    safe_print(f"  │  └─ /{cmd.stem}")

            if generate_cmds:
                safe_print("  ├─ Code Generation")
                for cmd in generate_cmds[:3]:
                    safe_print(f"  │  └─ /{cmd.stem}")

            if info_cmds:
                safe_print("  └─ Info & Config")
                for cmd in info_cmds[:2]:
                    safe_print(f"     └─ /{cmd.stem}")
        else:
            safe_print("✗ Slash Commands (not found)")

        safe_print()

        # Configuration (stored in global storage)
        project_name = self.project_root.name
        changes_file = self.config.get_project_changes_file(project_name)
        backup_dir = self.config.get_project_backups_dir(project_name)

        safe_print("✓ Configuration")
        safe_print(f"  ├─ ~/.cco/projects/{project_name}/changes.json (change tracking)")

        # Check for backups in global storage
        if backup_dir.exists() and any(backup_dir.iterdir()):
            backup_count = len(list(backup_dir.iterdir()))
            safe_print(f"  └─ ~/.cco/projects/{project_name}/backups/ ({backup_count} backups)")
        else:
            safe_print(f"  └─ ~/.cco/projects/{project_name}/backups/ (ready)")

        safe_print()
        print_separator("-", SEPARATOR_WIDTH)
        safe_print()

        # Quick Start
        safe_print("## 🚀 Quick Start")
        safe_print()
        safe_print("1. View active principles:     @PRINCIPLES.md")
        safe_print("2. Check project status:       /cco-status")
        safe_print("3. Audit your codebase:        /cco-audit")
        safe_print("4. Fix violations:             /cco-fix")
        safe_print()

        # Tips
        safe_print("## 💡 Tips")
        safe_print()
        safe_print("• All work must follow active principles (non-negotiable)")
        safe_print("• Use /cco-status to see current CCO configuration")
        safe_print("• Use /cco-remove for granular component removal")
        safe_print("• Re-run /cco-init to update configuration")
        safe_print()

        print_separator("=", SEPARATOR_WIDTH)
        safe_print()

    def _install_project_statusline(self) -> None:
        """Install statusline from global CCO to project .claude/ directory."""
        import shutil

        # Source: global CCO statusline
        global_statusline = self.config.get_global_dir() / "statusline.js"

        # Destination: project .claude directory
        project_claude_dir = self.config.get_project_claude_dir(self.project_root)
        project_claude_dir.mkdir(parents=True, exist_ok=True)
        project_statusline = project_claude_dir / "statusline.js"

        if global_statusline.exists():
            shutil.copy2(global_statusline, project_statusline)

    def _generate_generic_commands(self, analysis: Dict[str, Any]) -> int:
        """
        Generate project commands by linking to global command repository.

        Linking Strategy (platform-aware):
        - Unix/Linux/macOS: symlink > hardlink > copy
          (symlink is more flexible, works cross-volume)
        - Windows: hardlink > symlink > copy
          (hardlink doesn't require admin, symlink needs Developer Mode)

        Benefits:
        - pip install -U updates global commands → all projects auto-update
        - No per-project maintenance needed
        - Single source of truth

        Returns:
            Number of commands generated
        """
        import os
        import sys

        # Source: global commands (project-agnostic, ready-to-use)
        global_commands_dir = self.config.get_global_commands_dir()

        # Destination: project .claude/commands/
        project_commands = self.config.get_project_commands_dir(self.project_root)

        # Track .claude directory creation if needed
        claude_dir = self.project_root / ".claude"
        claude_dir_created = not claude_dir.exists()

        # Track .claude/commands directory creation if needed
        commands_dir_created = not project_commands.exists()

        project_commands.mkdir(parents=True, exist_ok=True)

        # Track directory creations
        if claude_dir_created:
            self.manifest.track_directory_created(
                claude_dir,
                "Created .claude directory for project configuration",
            )
        if (
            commands_dir_created and not claude_dir_created
        ):  # Only if .claude existed but commands didn't
            self.manifest.track_directory_created(
                project_commands,
                "Created .claude/commands directory for slash commands",
            )

        commands_generated = 0
        command_names = []  # Track command names for manifest
        symlinks_created = 0
        hardlinks_created = 0
        copies_created = 0

        if not global_commands_dir.exists():
            # Global commands not installed yet
            return 0

        # Determine platform-specific strategy
        is_unix = sys.platform in ["linux", "darwin"]

        for command_file in global_commands_dir.glob("*.md"):
            # Determine command name with cco- prefix
            # Command: "status.md" → Project: "cco-status.md"
            base_name = command_file.stem  # "status"
            command_name = f"cco-{base_name}.md"
            dest_file = project_commands / command_name

            # Remove existing file if present
            if dest_file.exists() or dest_file.is_symlink():
                dest_file.unlink()

            # Try linking strategies in platform-specific order
            linked = False

            if is_unix:
                # Unix/Linux/macOS: Prefer symlink (more flexible)
                try:
                    dest_file.symlink_to(command_file.absolute())
                    symlinks_created += 1
                    linked = True
                except (OSError, NotImplementedError):
                    pass

            if not linked:
                # Try hardlink (works same-volume, no admin on Windows)
                try:
                    os.link(str(command_file.absolute()), str(dest_file.absolute()))
                    hardlinks_created += 1
                    linked = True
                except (OSError, NotImplementedError):
                    pass

            if not linked and not is_unix:
                # Windows fallback: Try symlink (needs Developer Mode/Admin)
                try:
                    dest_file.symlink_to(command_file.absolute())
                    symlinks_created += 1
                    linked = True
                except (OSError, NotImplementedError):
                    pass

            if not linked:
                # Final fallback: Copy file (always works, but no auto-update)
                try:
                    dest_file.write_text(
                        command_file.read_text(encoding="utf-8"),
                        encoding="utf-8",
                    )
                    copies_created += 1
                    linked = True
                except Exception as e:
                    # Skip this command if all linking methods fail
                    logger.debug(f"Failed to link command {command_name}: {e}")
                    continue

            if linked:
                commands_generated += 1
                command_names.append(f"cco-{base_name}")  # Track command name

        # Track commands installation in manifest
        if command_names:
            self.manifest.track_commands_installed(command_names)

        # Log summary (for user feedback)
        if symlinks_created > 0:
            safe_print(f"  Symlinked {symlinks_created} commands (auto-update enabled)")
        if hardlinks_created > 0:
            safe_print(f"  Hardlinked {hardlinks_created} commands (auto-update enabled)")
        if copies_created > 0:
            safe_print(f"  Copied {copies_created} commands (manual update required)")
            safe_print("  Note: Run 'cco init --force' after pip install -U to update")

        return commands_generated

    def _initialize_interactive(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Interactive initialization with full wizard.

        Note: CCO keeps project directories completely clean.
        Wizard generates commands in .claude/commands/ only (standard Claude Code location).
        All project data stored in global registry.
        """
        from ..wizard.cli import CCOWizard

        # Launch wizard
        wizard = CCOWizard(project_root=str(self.project_root), dry_run=False)
        success = wizard.run()

        if not success:
            return {
                "success": False,
                "error": "Interactive wizard was cancelled or failed",
            }

        # Wizard generates commands in .claude/commands/
        # All preferences stored in global registry
        # No CCO-specific files in project directory

        if not project_name:
            project_name = self.project_root.name

        return {
            "success": True,
            "mode": "interactive",
            "project_name": project_name,
            "message": "Project initialized with interactive wizard",
        }

    def get_project_config(self) -> Optional[Dict[str, Any]]:
        """
        Get project configuration from global registry.

        Note: CCO keeps project directories clean - no local files.
        Searches global registry by project root path.

        Returns:
            Project data from ~/.cco/projects/ or None
        """
        # Search registry by project root path
        project_root_str = str(self.project_root.absolute())

        try:
            registry_dir = self.config.get_projects_registry_dir()
            if not registry_dir.exists():
                return None

            # Check all registry files
            for registry_file in registry_dir.glob("*.json"):
                if registry_file.name == "index.json":
                    continue
                try:
                    data = json.loads(registry_file.read_text())
                    if data.get("root") == project_root_str:
                        return data
                except Exception as e:
                    logger.debug(f"Failed to parse registry file {registry_file}: {e}")
                    continue

            return None
        except Exception:
            return None

    def update_project_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update project configuration in global registry.

        Args:
            updates: Configuration updates

        Returns:
            Update result
        """
        try:
            project_data = self.get_project_config()

            if not project_data:
                return {
                    "success": False,
                    "error": "Project not initialized",
                }

            # Merge updates into analysis
            if "analysis" in project_data:
                project_data["analysis"].update(updates.get("analysis", {}))

            # Update in registry
            project_name = project_data.get("name")
            result = self.registry.update_project_analysis(
                project_name=project_name,
                analysis=project_data.get("analysis", {}),
            )

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def uninitialize(self) -> Dict[str, Any]:
        """
        Remove CCO from project.

        Removes:
        1. All cco-*.md command files from .claude/commands/
        2. statusline.js from .claude/ directory
        3. Project entry from global registry

        Returns:
            Uninitialization result
        """
        try:
            # Get project data
            project_data = self.get_project_config()
            if not project_data:
                return {
                    "success": False,
                    "error": "Project not initialized",
                }

            project_name = project_data.get("name")
            files_removed = []

            # STEP 1: Remove all cco-*.md command files
            project_commands_dir = self.config.get_project_commands_dir(self.project_root)
            if project_commands_dir.exists():
                for cmd_file in project_commands_dir.glob("cco-*.md"):
                    cmd_file.unlink()
                    files_removed.append(str(cmd_file.relative_to(self.project_root)))

            # STEP 2: Remove statusline.js
            project_claude_dir = self.config.get_project_claude_dir(self.project_root)
            statusline_file = project_claude_dir / "statusline.js"
            if statusline_file.exists():
                statusline_file.unlink()
                files_removed.append(str(statusline_file.relative_to(self.project_root)))

            # STEP 3: Unregister from global registry
            if project_name:
                self.registry.unregister_project(project_name)

            return {
                "success": True,
                "project_name": project_name,
                "files_removed": files_removed,
                "message": f"CCO uninitialized. Removed {len(files_removed)} files.",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _create_ai_preferences(self, project_name: str, analysis: Dict[str, Any]) -> CCOPreferences:
        """Create intelligent preferences from project analysis (AI-driven quick mode)."""
        primary_lang = analysis.get("primary_language", "python")
        frameworks = [f["name"] for f in analysis.get("frameworks", [])[:3]]
        has_tests = analysis.get("has_tests", False)

        team_size = "solo"

        # Check if linting tools are present
        tools = [t["name"] for t in analysis.get("tools", [])]
        has_linting_tools = any(
            tool in tools for tool in ["black", "ruff", "eslint", "prettier", "mypy"]
        )
        linting_strictness = "strict" if has_linting_tools else "standard"

        test_coverage_target = (
            str(DEFAULT_TEST_COVERAGE_TARGET) if has_tests else str(MINIMAL_TEST_COVERAGE_TARGET)
        )

        # Let PrincipleSelector dynamically select based on preferences
        # No pre-selected IDs - fully dynamic selection like interactive mode
        return CCOPreferences(
            project_identity=ProjectIdentity(
                name=project_name,
                types=["backend"],
                primary_language=primary_lang,
                frameworks=frameworks,
                team_trajectory=team_size,
                project_maturity="active-dev",
                business_domain=["general-purpose"],
            ),
            development_style=DevelopmentStyle(
                code_philosophy="pragmatic",
                development_pace="balanced",
                refactoring_appetite="balanced",
            ),
            code_quality=CodeQualityStandards(
                linting_strictness=linting_strictness,
                type_checking_level="standard",
                test_coverage_target=test_coverage_target,
                code_review_depth="standard",
                documentation_level="standard",
                security_stance="standard",
            ),
        )

    def _select_and_generate_principles(self, preferences: CCOPreferences) -> List[Dict[str, Any]]:
        """Select applicable principles and generate PRINCIPLES.md."""
        selector = PrincipleSelector(preferences.model_dump(mode="json"))
        applicable_principles = selector.select_applicable()
        principles_file = self.project_root / "PRINCIPLES.md"

        # Check if file exists before generation (to detect creation vs modification)
        is_new_file = not principles_file.exists()

        selector.generate_principles_md(principles_file)

        # Track file change in manifest
        if is_new_file:
            self.manifest.track_file_created(
                principles_file,
                f"Created PRINCIPLES.md with {len(applicable_principles)} principles",
            )
        else:
            # File already exists, this is a modification
            self.manifest.track_file_modified(
                principles_file,
                f"Updated PRINCIPLES.md with {len(applicable_principles)} principles",
            )

        # Track principles addition
        principle_ids = [p["id"] for p in applicable_principles]
        self.manifest.track_principles_added(principle_ids)

        return applicable_principles

    def _generate_claude_md(self, preferences: CCOPreferences) -> Dict[str, Any]:
        """Generate or update CLAUDE.md file."""
        from .claude_md_generator import ClaudeMdGenerator

        claude_md_file = self.project_root / "CLAUDE.md"

        # Check if file exists before generation
        is_new_file = not claude_md_file.exists()

        # Generate CLAUDE.md
        generator = ClaudeMdGenerator(preferences.model_dump(mode="json"))
        result = generator.generate(claude_md_file)

        # Track file change in manifest
        if is_new_file:
            self.manifest.track_file_created(
                claude_md_file,
                "Created CLAUDE.md with project-specific guidelines",
            )
        else:
            self.manifest.track_file_modified(
                claude_md_file,
                f"Updated CLAUDE.md ({result.get('strategy', 'updated')})",
            )

        return result
