"""Project management for ClaudeCodeOptimizer."""

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
from .constants import (
    DEFAULT_TEST_COVERAGE_TARGET,
    MINIMAL_TEST_COVERAGE_TARGET,
    SEPARATOR_WIDTH,
    TOP_ITEMS_DISPLAY,
)
from .principle_selector import PrincipleSelector
from .safe_print import safe_print
from .utils import print_separator

logger = logging.getLogger(__name__)


class ProjectManager:
    """Manages CCO project initialization and configuration."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.absolute()
        self.config = CCOConfig
        self.analyzer = ProjectAnalyzer(self.project_root)

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
        5. Generate commands
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

        # Add selected principle IDs to preferences BEFORE generating CLAUDE.md
        preferences_dict = preferences.model_dump(mode="json")
        preferences_dict["selected_principle_ids"] = [p["id"] for p in selected_principles]

        # STEP 3.5: Generate/Update CLAUDE.md
        safe_print("\n📝 Generating CLAUDE.md...")
        claude_md_result = self._generate_claude_md(preferences_dict)
        if claude_md_result["success"]:
            safe_print(f"   ✓ CLAUDE.md {claude_md_result.get('strategy', 'generated')}")

        # STEP 4: Install principles symlinks to .claude/principles/
        self._install_principles_symlinks(selected_principles)

        # STEP 7: Install guides symlinks to .claude/guides/
        self._install_guides_symlinks(analysis)

        # STEP 8: Install skills symlinks to .claude/skills/
        self._install_skills_symlinks(analysis)

        # STEP 9: Install agents symlinks to .claude/agents/
        self._install_agents_symlinks(analysis)

        # STEP 9.5: Install settings.json template reference (if not exists)
        self._install_settings_template()

        # STEP 10: Generate generic commands
        commands_generated = self._generate_generic_commands(analysis)

        # STEP 11: Print recommendations
        self._print_recommendations(analysis)

        # STEP 12: Print installation summary report
        self._print_installation_summary()

        return {
            "success": True,
            "mode": "quick",
            "project_name": project_name,
            "analysis": analysis,
            "preferences": preferences_dict,
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

        # CLAUDE.md with principles
        claude_md_file = self.project_root / "CLAUDE.md"
        if claude_md_file.exists():
            try:
                content = claude_md_file.read_text(encoding="utf-8")

                # Count core principles (always 3)
                core_count = content.count("#### P")

                # Check if additional principles section exists
                has_additional = "Additional Principles by Category" in content

                safe_print("✓ CLAUDE.md")
                safe_print(f"  └─ {core_count} core principles (always loaded)")
                if has_additional:
                    safe_print("     └─ Links to project-specific principles across 8 categories")
            except Exception:
                safe_print("✓ CLAUDE.md (created)")
        else:
            safe_print("✗ CLAUDE.md (not found)")

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
        backup_dir = self.config.get_project_backups_dir(project_name)

        safe_print("✓ Configuration")

        # Check for backups in global storage
        if backup_dir.exists() and any(backup_dir.iterdir()):
            backup_count = len(list(backup_dir.iterdir()))
            safe_print(f"  └─ ~/.cco/{project_name}/backups/ ({backup_count} backups)")
        else:
            safe_print(f"  └─ ~/.cco/{project_name}/backups/ (ready)")

        safe_print()
        print_separator("-", SEPARATOR_WIDTH)
        safe_print()

        # Quick Start
        safe_print("## 🚀 Quick Start")
        safe_print()
        safe_print("1. View active principles:     @CLAUDE.md")
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

    def _create_link(self, source: Path, destination: Path) -> str:
        """
        Create link from destination to source using preference order.

        Tries in order: symlink → hardlink → copy
        Returns: link type used ("symlink", "hardlink", "copy")
        """
        import shutil

        # Remove existing if present
        if destination.exists() or destination.is_symlink():
            destination.unlink()

        # Try symlink first (best: auto-updates)
        try:
            destination.symlink_to(source.absolute())
            return "symlink"
        except (OSError, NotImplementedError):
            pass

        # Try hardlink (good: same disk, no duplication)
        try:
            destination.hardlink_to(source.absolute())
            return "hardlink"
        except (OSError, NotImplementedError):
            pass

        # Fallback to copy (works everywhere)
        shutil.copy2(source, destination)
        return "copy"

    def _install_principles_symlinks(self, selected_principles: List[Dict[str, Any]]) -> None:
        """
        Install principle symlinks based on selected principles.

        Only installs principle categories that are actually selected.

        Args:
            selected_principles: List of selected principle dictionaries
        """
        # Get unique categories from selected principles
        selected_categories = set()
        for principle in selected_principles:
            category = principle.get("category", "")
            if category:
                selected_categories.add(category)

        # Install only selected categories
        def should_include_principle(name: str, parent_dir: str = "") -> bool:
            return any(cat in name.lower() for cat in selected_categories)

        self._install_knowledge_symlinks("principles", filter_func=should_include_principle)

    def _install_guides_symlinks(self, analysis: Dict[str, Any]) -> None:
        """
        Install guide symlinks based on project needs.

        Selects guides based on:
        - Has CI/CD: Include CI/CD guides
        - Has Docker: Include container guides
        - Security stance: Include security guides

        Args:
            analysis: Project analysis dictionary
        """

        def should_include_guide(name: str, parent_dir: str = "") -> bool:
            name_lower = name.lower()
            # Always include core guides
            if any(x in name_lower for x in ["git-workflow", "verification"]):
                return True
            # Conditional guides
            if "container" in name_lower and analysis.get("has_docker"):
                return True
            if "security" in name_lower:
                return True
            if "performance" in name_lower:
                return True
            return False

        self._install_knowledge_symlinks("guides", filter_func=should_include_guide)

    def _install_skills_symlinks(self, analysis: Dict[str, Any]) -> None:
        """
        Install skill symlinks based on project language and type.

        Selects skills based on:
        - Primary language (e.g., Python → python/ skills)
        - Project type (e.g., API → async patterns)
        - Tools detected

        Args:
            analysis: Project analysis dictionary
        """
        primary_lang = analysis.get("primary_language", "").lower()

        def should_include_skill(name: str, parent_dir: str = "") -> bool:
            # Always include general skills (no parent dir)
            if not parent_dir:
                return True

            # Language-specific: only include if matches project language
            parent_lower = parent_dir.lower()
            if parent_lower == primary_lang:
                return True

            return False

        self._install_knowledge_symlinks("skills", filter_func=should_include_skill)

    def _install_agents_symlinks(self, analysis: Dict[str, Any]) -> None:
        """
        Install agent symlinks (currently just templates).

        Args:
            analysis: Project analysis dictionary
        """
        # For now, just install templates
        self._install_knowledge_symlinks("agents")

    def _install_settings_template(self) -> None:
        """
        Create settings.json in .claude/ from global template.

        Only creates if it doesn't exist - never overwrites existing settings.
        Template uses relative paths only - no absolute path exposure.
        """
        import shutil

        # Check if settings.json already exists
        project_claude_dir = self.config.get_project_claude_dir(self.project_root)
        settings_file = project_claude_dir / "settings.json"

        # Never overwrite existing settings.json
        if settings_file.exists():
            logger.debug("settings.json already exists, skipping template installation")
            return

        # Get global template (deployed from settings.json.template)
        templates_dir = self.config.get_templates_dir()
        template_file = templates_dir / "settings.json"

        if not template_file.exists():
            logger.debug("settings.json not found in global templates")
            return

        # Create .claude directory if needed
        project_claude_dir.mkdir(parents=True, exist_ok=True)

        # Copy template as-is (no placeholder replacement needed)
        shutil.copy2(template_file, settings_file)

        # Track in manifest
        self.manifest.track_file_created(
            settings_file, "Created settings.json from global template"
        )

        logger.debug(f"Created settings.json from template at {settings_file}")

    def _install_knowledge_symlinks(
        self, category: str, filter_func: Optional[callable] = None
    ) -> None:
        """
        Generic function to install links for a category.

        Uses preference order: symlink → hardlink → copy

        Args:
            category: Category name (principles, guides, skills, agents)
            filter_func: Optional function(name, parent_dir="") -> bool to filter files
        """
        # Source: global directory for this category
        category_methods = {
            "principles": self.config.get_principles_dir,
            "guides": self.config.get_guides_dir,
            "skills": self.config.get_skills_dir,
            "agents": self.config.get_agents_dir,
        }

        global_category_dir = category_methods[category]()
        if not global_category_dir.exists():
            logger.debug(f"Global {category} directory not found, skipping")
            return

        # Destination: project .claude/{category} directory
        project_claude_dir = self.config.get_project_claude_dir(self.project_root)
        project_category_dir = project_claude_dir / category
        project_category_dir.mkdir(parents=True, exist_ok=True)

        # Get all .md files from global directory (excluding templates and READMEs)
        all_global_files = [
            f
            for f in global_category_dir.glob("*.md")
            if not f.name.startswith("_") and not f.name.upper() == "README.MD"
        ]

        # Apply filter if provided
        if filter_func:
            global_files = [f for f in all_global_files if filter_func(f.stem, "")]
        else:
            global_files = all_global_files

        # Get subdirectories (for language-specific skills)
        all_subdirs = [
            d
            for d in global_category_dir.iterdir()
            if d.is_dir() and not d.name.startswith(("_", "."))
        ]

        # Filter subdirectories if filter_func provided
        if filter_func:
            subdirs = [d for d in all_subdirs if filter_func("", d.name)]
        else:
            subdirs = all_subdirs

        if not global_files and not subdirs:
            logger.debug(f"No {category} files found in global directory")
            return

        linked_count = 0

        # First, link all root-level files
        for global_file in global_files:
            project_file = project_category_dir / global_file.name
            self._create_link(global_file, project_file)
            linked_count += 1

        # Second, link files from subdirectories (e.g., skills/python/, skills/go/)
        for subdir in subdirs:
            # Create corresponding subdirectory in project
            project_subdir = project_category_dir / subdir.name
            project_subdir.mkdir(parents=True, exist_ok=True)

            # Link all .md files from this subdirectory
            for global_file in subdir.glob("*.md"):
                if global_file.name.startswith("_") or global_file.name.upper() == "README.MD":
                    continue

                # Apply filter if provided
                if filter_func and not filter_func(global_file.stem, subdir.name):
                    continue

                project_file = project_subdir / global_file.name
                self._create_link(global_file, project_file)
                linked_count += 1

        logger.debug(f"Symlinked {linked_count} {category} files to .claude/{category}/")

    def _generate_generic_commands(self, analysis: Dict[str, Any]) -> int:
        """
        Generate project commands by linking to global command repository.

        Intelligently selects commands based on project analysis:
        - Core commands (always included)
        - Docker commands (if Docker detected)
        - CI/CD commands (if CI/CD detected)
        - Testing commands (based on testing needs)

        Uses preference order: symlink → hardlink → copy
        Benefits: pip install -U updates global commands → all projects auto-update (symlink/hardlink)

        Returns:
            Number of commands generated
        """
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

        if not global_commands_dir.exists():
            # Global commands not installed yet
            return 0

        # Define command filter logic
        def should_include_command(command_name: str) -> bool:
            """Filter commands based on project analysis."""
            name_lower = command_name.lower()

            # Core commands (always include)
            core_commands = {
                "init",
                "config",
                "status",
                "remove",
                "analyze",
                "audit",
                "fix",
                "refactor",
                "test",
                "commit",
                "sync",
                "generate",
                "implement-feature",
                "scan-secrets",
                "optimize-code",
                "optimize-deps",
                "analyze-complexity",
                "analyze-dependencies",
                "analyze-structure",
            }
            if name_lower in core_commands:
                return True

            # Documentation commands (always useful)
            if any(x in name_lower for x in ["generate-docs", "audit-docs", "fix-docs"]):
                return True

            # Docker/Container commands (only if Docker detected)
            if "docker" in name_lower:
                return analysis.get("has_docker", False)

            # CI/CD commands (only if CI/CD detected)
            if any(x in name_lower for x in ["cicd", "monitoring"]):
                return analysis.get("has_cicd", False)

            # Testing commands (based on test framework detection)
            if "test" in name_lower and "generate" in name_lower:
                # Include if project has tests or test frameworks
                return bool(analysis.get("test_frameworks") or analysis.get("has_tests"))

            # Default: exclude
            return False

        for command_file in global_commands_dir.glob("*.md"):
            # Check if command should be included
            if not should_include_command(command_file.stem):
                continue
            # Determine command name with cco- prefix
            # Command: "status.md" → Project: "cco-status.md"
            base_name = command_file.stem  # "status"
            command_name = f"cco-{base_name}.md"
            dest_file = project_commands / command_name

            # Create link using preference order
            self._create_link(command_file, dest_file)
            commands_generated += 1
            command_names.append(f"cco-{base_name}")

        # Track commands installation in manifest
        if command_names:
            self.manifest.track_commands_installed(command_names)

        # Log summary
        if commands_generated > 0:
            safe_print(f"  Linked {commands_generated} commands (auto-update enabled)")

        return commands_generated

    def _initialize_interactive(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Interactive initialization with full wizard.

        Note: CCO keeps project directories completely clean.
        Wizard generates commands in .claude/commands/ only (standard Claude Code location).
        All project data stored in global registry.
        """
        from ..wizard.orchestrator import CCOWizard

        # Launch unified wizard (interactive mode)
        wizard = CCOWizard(project_root=self.project_root, mode="interactive", dry_run=False)
        result = wizard.run()

        # Handle both old (bool) and new (WizardResult) return types
        success = result.success if hasattr(result, "success") else result

        if not success:
            error_msg = (
                result.error
                if hasattr(result, "error")
                else "Interactive wizard was cancelled or failed"
            )
            return {
                "success": False,
                "error": error_msg,
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

    def uninitialize(self) -> Dict[str, Any]:
        """
        Remove CCO from project.

        Removes all cco-*.md command files from .claude/commands/

        Returns:
            Uninitialization result
        """
        try:
            # Get project name from directory
            project_name = self.project_root.name
            files_removed = []

            # Remove all cco-*.md command files
            project_commands_dir = self.config.get_project_commands_dir(self.project_root)
            if project_commands_dir.exists():
                for cmd_file in project_commands_dir.glob("cco-*.md"):
                    cmd_file.unlink()
                    files_removed.append(str(cmd_file.relative_to(self.project_root)))

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
        """
        Select applicable principles based on preferences.

        NOTE: Principles are now embedded in CLAUDE.md via symlinks to ~/.cco/principles/.
        No separate PRINCIPLES.md file is generated.
        """
        selector = PrincipleSelector(preferences.model_dump(mode="json"))
        applicable_principles = selector.select_applicable()

        # Track principles addition in manifest (no file generation)
        principle_ids = [p["id"] for p in applicable_principles]
        self.manifest.track_principles_added(principle_ids)

        return applicable_principles

    def _generate_claude_md(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or update CLAUDE.md file."""
        from .claude_md_generator import ClaudeMdGenerator

        claude_md_file = self.project_root / "CLAUDE.md"

        # Check if file exists before generation
        is_new_file = not claude_md_file.exists()

        # Generate CLAUDE.md (preferences is already a dict)
        generator = ClaudeMdGenerator(preferences)
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
