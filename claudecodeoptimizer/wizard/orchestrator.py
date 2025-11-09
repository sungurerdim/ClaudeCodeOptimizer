"""
Wizard Orchestrator - Unified Interactive & Quick Modes

Executes the same decision tree in two modes:
- Interactive: Ask user for each decision
- Quick: Use AI auto-strategy for each decision

Both modes produce identical WizardResult structures.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Literal, Optional

from ..ai.detection import UniversalDetector
from ..schemas.preferences import CCOPreferences
from .checkpoints import (
    display_completion_summary,
    display_detection_results,
)
from .decision_tree import get_all_decisions
from .models import AnswerContext, DecisionPoint, SystemContext, WizardResult
from .recommendations import RecommendationEngine
from .renderer import (
    ask_choice,
    ask_multi_choice,
    clear_screen,
    pause,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
)
from .system_detection import SystemDetector


class CCOWizard:
    """
    Unified wizard orchestrator for both Interactive and Quick modes.

    Both modes:
    1. Detect system context (TIER 0)
    2. Detect project structure
    3. Execute decision tree (TIER 1-3)
    4. Select principles based on answers
    5. Select commands based on answers
    6. Generate configuration files
    """

    def __init__(
        self,
        project_root: Path,
        mode: Literal["interactive", "quick"],
        dry_run: bool = False,
    ) -> None:
        """
        Initialize wizard.

        Args:
            project_root: Project root directory
            mode: "interactive" (ask user) or "quick" (auto AI)
            dry_run: If True, don't write files
        """
        self.project_root = project_root
        self.mode = mode
        self.dry_run = dry_run

        # State
        self.system_context: Optional[SystemContext] = None
        self.detection_report: Optional[Dict] = None
        self.answer_context: Optional[AnswerContext] = None
        self.selected_principles: List[str] = []
        self.selected_commands: List[str] = []

        # Engines
        self.rec_engine = RecommendationEngine()

    # ========================================================================
    # Main Execution Flow
    # ========================================================================

    def run(self) -> WizardResult:
        """
        Run complete wizard flow.

        Returns:
            WizardResult with success status and all data
        """
        start_time = time.time()

        try:
            # Welcome
            self._show_welcome()

            # TIER 0: System Detection (automatic, silent)
            if not self._run_system_detection():
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers={},
                    error="System detection failed",
                )

            # Project Detection (UniversalDetector)
            if not self._run_project_detection():
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers={},
                    error="Project detection failed",
                )

            # Decision Tree (TIER 1-3)
            if not self._run_decision_tree():
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers if self.answer_context else {},
                    error="Decision tree execution failed",
                )

            # Principle Selection
            if not self._run_principle_selection():
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers,
                    error="Principle selection failed",
                )

            # Command Selection
            if not self._run_command_selection():
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers,
                    selected_principles=self.selected_principles,
                    error="Command selection failed",
                )

            # File Generation (unless dry-run)
            if not self.dry_run:
                if not self._run_file_generation():
                    return WizardResult(
                        success=False,
                        mode=self.mode,
                        system_context=self.system_context,
                        answers=self.answer_context.answers,
                        selected_principles=self.selected_principles,
                        selected_commands=self.selected_commands,
                        error="File generation failed",
                    )

            # Success
            duration = time.time() - start_time
            self._show_completion(duration)

            return WizardResult(
                success=True,
                mode=self.mode,
                system_context=self.system_context,
                answers=self.answer_context.answers,
                selected_principles=self.selected_principles,
                selected_commands=self.selected_commands,
                duration_seconds=duration,
            )

        except KeyboardInterrupt:
            print("\n")
            print_warning("Wizard cancelled by user", indent=2)
            return WizardResult(
                success=False,
                mode=self.mode,
                system_context=self.system_context,
                answers=self.answer_context.answers if self.answer_context else {},
                error="Cancelled by user",
            )
        except Exception as e:
            print_error(f"Wizard failed: {str(e)}", indent=2)
            return WizardResult(
                success=False,
                mode=self.mode,
                system_context=self.system_context,
                answers=self.answer_context.answers if self.answer_context else {},
                error=str(e),
            )

    # ========================================================================
    # Phase 0: Welcome
    # ========================================================================

    def _show_welcome(self) -> None:
        """Show welcome message"""
        clear_screen()

        if self.mode == "interactive":
            print_header(
                "CCO Wizard - Interactive Mode",
                "We'll ask you questions to configure CCO for your project",
            )
            print_info("This wizard guides you through 3 tiers of decisions:", indent=2)
            print_info("  • Tier 1: Project fundamentals (purpose, team, maturity)", indent=2)
            print_info("  • Tier 2: Strategy (principles, testing, security)", indent=2)
            print_info("  • Tier 3: Tactical (tool preferences, commands)", indent=2)
        else:  # quick
            print_header(
                "CCO Wizard - Quick Mode",
                "AI will automatically configure CCO based on your project",
            )
            print_info("Quick mode analyzes your project and makes smart decisions:", indent=2)
            print_info("  • Detect project structure and tools", indent=2)
            print_info("  • Select appropriate principles and practices", indent=2)
            print_info("  • Configure commands based on your needs", indent=2)

        print()
        print_info(f"Project: {self.project_root}", indent=2)
        print_info(f"Mode: {self.mode}", indent=2)
        if self.dry_run:
            print_warning("DRY RUN - No files will be written", indent=2)
        print()

        if self.mode == "interactive":
            pause()

    # ========================================================================
    # Phase 1: System Detection (TIER 0)
    # ========================================================================

    def _run_system_detection(self) -> bool:
        """Detect system context"""
        if self.mode == "interactive":
            clear_screen()
            print_header("Phase 0: System Detection", "Detecting your environment...")
            print()

        try:
            detector = SystemDetector(self.project_root)
            self.system_context = detector.detect_all()

            if self.mode == "interactive":
                print_success(f"✓ OS: {self.system_context.os_type}", indent=2)
                print_success(f"✓ Shell: {self.system_context.shell_type}", indent=2)
                print_success(f"✓ Python: {self.system_context.python_version}", indent=2)
                print_success(f"✓ Locale: {self.system_context.detected_language}", indent=2)
                print()
                pause()

            return True

        except Exception as e:
            print_error(f"System detection failed: {e}", indent=2)
            return False

    # ========================================================================
    # Phase 2: Project Detection
    # ========================================================================

    def _run_project_detection(self) -> bool:
        """Run UniversalDetector to analyze project"""
        if self.mode == "interactive":
            clear_screen()
            print_header("Phase 1: Project Detection", "Analyzing your codebase...")
            print()

        try:
            detector = UniversalDetector(str(self.project_root))
            analysis = detector.analyze()
            self.detection_report = analysis.dict()

            # Enrich system context with project data
            system_detector = SystemDetector(self.project_root)
            self.system_context = system_detector.enrich_with_project_detection(
                self.system_context,
                self.detection_report,
            )

            # Display results
            if self.mode == "interactive":
                display_detection_results(self.detection_report)
                print()

                # Ask user to confirm or adjust analysis
                if not self._confirm_analysis():
                    print_warning("Analysis confirmation cancelled", indent=2)
                    return False

            else:  # quick mode
                # Log detection summary
                print_info("Project detected:", indent=2)
                print_info(
                    f"  Languages: {', '.join([lang['detected_value'] for lang in self.detection_report.get('languages', [])])}",
                    indent=2,
                )
                print_info(
                    f"  Frameworks: {', '.join([f['detected_value'] for f in self.detection_report.get('frameworks', [])])}",
                    indent=2,
                )
                print_info(
                    f"  Files: {self.detection_report.get('codebase_patterns', {}).get('total_files', 0)}",
                    indent=2,
                )
                print()

            return True

        except Exception as e:
            print_error(f"Project detection failed: {e}", indent=2)
            return False

    def _confirm_analysis(self) -> bool:
        """
        Ask user to confirm analysis results (Interactive mode only).

        Returns:
            True if user confirms, False if cancelled
        """
        from .terminal_ui import ask_yes_no

        print_info("Analysis complete! Does this look correct?", indent=2)
        print()

        print_info(f"  Primary Language: {self._get_primary_language_name()}", indent=2)
        print_info(f"  Frameworks: {self._get_frameworks_summary()}", indent=2)
        print_info(f"  Project Type: {self._get_project_type_summary()}", indent=2)
        print()

        print_info("Note: If detection is incorrect, you can:", indent=2)
        print_info("  1. Continue anyway (AI will adjust recommendations)", indent=2)
        print_info("  2. Cancel and manually configure (advanced)", indent=2)
        print()

        confirmed = ask_yes_no("Continue with this analysis?", default=True)

        if confirmed:
            print_success("Analysis confirmed!", indent=2)
            return True
        else:
            return False

    def _get_primary_language_name(self) -> str:
        """Get primary language name from detection report"""
        languages = self.detection_report.get("languages", [])
        if languages:
            return languages[0].get("detected_value", "Unknown")
        return "Unknown"

    def _get_frameworks_summary(self) -> str:
        """Get frameworks summary"""
        frameworks = self.detection_report.get("frameworks", [])
        if frameworks:
            names = [fw.get("detected_value", "") for fw in frameworks[:3]]  # Top 3
            return ", ".join(names) if names else "None"
        return "None"

    def _get_project_type_summary(self) -> str:
        """Get project type summary"""
        types = self.detection_report.get("project_types", [])
        if types:
            names = [t.get("name", "") for t in types[:2]]  # Top 2
            return ", ".join(names) if names else "Unknown"
        return "Unknown"

    # ========================================================================
    # Phase 3: Decision Tree (TIER 1-3)
    # ========================================================================

    def _run_decision_tree(self) -> bool:
        """Execute decision tree for all tiers"""
        # Initialize answer context
        self.answer_context = AnswerContext(system=self.system_context)

        # Get all decision points
        try:
            all_decisions = get_all_decisions(self.answer_context)
        except Exception as e:
            print_error(f"Failed to build decision tree: {e}", indent=2)
            return False

        # Execute each decision
        for decision in all_decisions:
            # Check if should ask
            if not decision.should_ask(self.answer_context.answers):
                continue

            # Ask question (mode-dependent)
            try:
                answer = self._execute_decision(decision)
                self.answer_context.set(decision.id, answer)
            except Exception as e:
                print_error(f"Failed to execute decision '{decision.id}': {e}", indent=2)
                return False

        return True

    def _execute_decision(self, decision: DecisionPoint) -> any:
        """
        Execute a single decision point.

        Interactive mode: Ask user
        Quick mode: Use auto_strategy
        """
        if self.mode == "interactive":
            return self._ask_user_decision(decision)
        else:  # quick
            return self._auto_decide(decision)

    def _ask_user_decision(self, decision: DecisionPoint) -> any:
        """Ask user for decision (Interactive mode)"""
        clear_screen()

        # Show tier header
        tier_names = {
            1: "Fundamental Decisions",
            2: "Strategy Decisions",
            3: "Tactical Decisions",
        }
        tier_name = tier_names.get(decision.tier, "Decisions")
        print_header(f"Tier {decision.tier}: {tier_name}", decision.question)
        print()

        # Show why this question matters
        if decision.why_this_question:
            print_info(decision.why_this_question, indent=2)
            print()

        # Show AI hint
        ai_hint = decision.get_ai_hint(self.answer_context)
        if ai_hint:
            print_info(ai_hint, indent=2)
            print()

        # Ask question
        if decision.multi_select:
            # Multi-choice
            choices = [f"{opt.label}\n    {opt.description}" for opt in decision.options]
            recommended = decision.get_recommended_option(self.answer_context)
            defaults = (
                recommended
                if isinstance(recommended, list)
                else [recommended]
                if recommended
                else []
            )

            selected_indices = ask_multi_choice(
                decision.question,
                choices,
                defaults=[
                    choices.index(
                        f"{decision.options[i].label}\n    {decision.options[i].description}",
                    )
                    for i, opt in enumerate(decision.options)
                    if opt.value in defaults
                ],
            )

            # Map back to values
            answer = [decision.options[i].value for i in selected_indices]

        else:
            # Single choice
            choices = [opt.label for opt in decision.options]
            recommended = decision.get_recommended_option(self.answer_context)

            # Find recommended index
            default_idx = None
            if recommended:
                for i, opt in enumerate(decision.options):
                    if opt.value == recommended:
                        default_idx = i
                        break

            selected_idx = ask_choice(
                decision.question,
                choices,
                default=choices[default_idx] if default_idx is not None else None,
            )

            answer = decision.options[selected_idx].value

        return answer

    def _auto_decide(self, decision: DecisionPoint) -> any:
        """Auto-decide using AI strategy (Quick mode)"""
        answer = decision.get_recommended_option(self.answer_context)

        # Log decision
        if decision.multi_select:
            answer_str = ", ".join(answer) if isinstance(answer, list) else answer
        else:
            answer_str = answer

        print_info(f"[AUTO] {decision.question}", indent=2)
        print_success(f"       → {answer_str}", indent=2)

        # Show reasoning
        ai_hint = decision.get_ai_hint(self.answer_context)
        if ai_hint:
            print_info(f"       {ai_hint}", indent=2)
        print()

        return answer

    # ========================================================================
    # Phase 4: Principle Selection
    # ========================================================================

    def _run_principle_selection(self) -> bool:
        """Select principles based on answers"""
        if self.mode == "interactive":
            clear_screen()
            print_header("Phase 4: Principle Selection", "Selecting development principles...")
            print()

        try:
            # Build preferences object from answers
            preferences = self._build_preferences()

            # Use PrincipleSelector
            from ..core.principle_selector import PrincipleSelector

            selector = PrincipleSelector(preferences)

            # Get all principles and recommended ones
            all_principles = selector.all_principles
            recommended = selector.select_applicable()
            recommended_ids = [p["id"] for p in recommended]

            if self.mode == "interactive":
                # Show all principles with recommended ones pre-selected
                print_info(
                    f"We recommend {len(recommended_ids)} principles based on your answers.",
                    indent=2,
                )
                print_info("Review and customize the selection below:", indent=2)
                print()

                # Create principle options for multiselect
                principle_choices = []
                for principle in all_principles:
                    pid = principle["id"]
                    title = principle.get("title", pid)
                    severity = principle.get("severity", "medium")
                    category = principle.get("category", "general")

                    # Format: "P001: Principle Title (severity, category)"
                    label = f"{pid}: {title}"
                    description = f"{severity.upper()} - {category}"

                    principle_choices.append(
                        {"id": pid, "label": label, "description": description},
                    )

                # Use ask_multi_choice from renderer
                selected_labels = ask_multi_choice(
                    "Select principles to apply (recommended are pre-selected):",
                    [p["label"] for p in principle_choices],
                    defaults=[p["label"] for p in principle_choices if p["id"] in recommended_ids],
                    default_label="recommended",
                    page_size=20,  # Show more principles per page
                )

                # Extract selected IDs
                self.selected_principles = [
                    p["id"] for p in principle_choices if p["label"] in selected_labels
                ]

                print()
                print_success(f"✓ {len(self.selected_principles)} principles selected", indent=2)
                print()
                pause()

            else:  # quick mode
                # Auto-select recommended principles
                self.selected_principles = recommended_ids
                print_success(f"✓ Selected {len(self.selected_principles)} principles", indent=2)
                print()

            return True

        except Exception as e:
            print_error(f"Principle selection failed: {e}", indent=2)
            return False

    # ========================================================================
    # Phase 5: Command Selection
    # ========================================================================

    def _run_command_selection(self) -> bool:
        """Select commands based on answers"""
        if self.mode == "interactive":
            clear_screen()
            print_header("Phase 5: Command Selection", "Selecting CCO commands...")
            print()

        try:
            # Build preferences for CommandRecommender
            preferences = self._build_preferences()

            # Build minimal command registry from global commands
            from ..ai.command_selection import CommandRecommender

            registry = self._build_command_registry()

            # Create recommender and get recommendations
            recommender = CommandRecommender(CCOPreferences(**preferences), registry)
            command_recs = recommender.recommend_commands()

            # Install only core + recommended commands (NOT optional)
            self.selected_commands = command_recs["core"] + command_recs["recommended"]

            if self.mode == "interactive":
                # Show what will be installed
                print_info("Commands to install:", indent=2)
                print()

                print_success("  Core commands:", indent=2)
                for cmd in command_recs["core"]:
                    reason = command_recs["reasoning"].get(cmd, "Essential command")
                    print_success(f"    /{cmd}", indent=2)
                    print_info(f"      {reason}", indent=2)
                print()

                print_success("  Recommended commands:", indent=2)
                for cmd in command_recs["recommended"]:
                    reason = command_recs["reasoning"].get(cmd, "Recommended for your project")
                    print_success(f"    /{cmd}", indent=2)
                    print_info(f"      {reason}", indent=2)
                print()

                # Show optional commands (available but not installed)
                if command_recs["optional"]:
                    print_info("Optional commands available (not installed):", indent=2)
                    print_info("  You can enable these later with /cco-config", indent=2)
                    for cmd in command_recs["optional"][:10]:  # Show first 10
                        print_info(f"    /{cmd}", indent=2)
                    if len(command_recs["optional"]) > 10:
                        print_info(
                            f"    ... and {len(command_recs['optional']) - 10} more",
                            indent=2,
                        )
                    print()

                pause()

            else:  # quick mode
                print_success(f"✓ Installing {len(self.selected_commands)} commands", indent=2)
                print_info(f"  Core: {len(command_recs['core'])} commands", indent=2)
                print_info(f"  Recommended: {len(command_recs['recommended'])} commands", indent=2)
                if command_recs["optional"]:
                    print_info(
                        f"  Optional (available): {len(command_recs['optional'])} commands",
                        indent=2,
                    )
                print()

            return True

        except Exception as e:
            print_error(f"Command selection failed: {e}", indent=2)
            return False

    def _build_command_registry(self) -> "CommandRegistry":  # noqa: F821
        """Build command registry from available global commands"""
        from .. import config as CCOConfig  # noqa: N812
        from ..schemas.commands import CommandMetadata, CommandRegistry

        # Get global commands directory
        global_commands_dir = CCOConfig.get_global_commands_dir()

        commands = []
        if global_commands_dir.exists():
            for cmd_file in global_commands_dir.glob("*.md"):
                # Extract command ID from filename
                command_id = (
                    f"cco-{cmd_file.stem}"
                    if not cmd_file.stem.startswith("cco-")
                    else cmd_file.stem
                )

                # Create minimal metadata
                commands.append(
                    CommandMetadata(
                        command_id=command_id,
                        display_name=cmd_file.stem.replace("-", " ").title(),
                        category="general",
                        description_short=f"{cmd_file.stem} command",
                        description_long=f"CCO {cmd_file.stem} command",
                        applicable_project_types=["all"],
                    ),
                )

        return CommandRegistry(commands=commands)

    # ========================================================================
    # Phase 6: File Generation
    # ========================================================================

    def _run_file_generation(self) -> bool:
        """Generate all configuration files"""
        if self.mode == "interactive":
            clear_screen()
            print_header("Phase 6: File Generation", "Creating configuration files...")
            print()

        try:
            # Create directories
            (self.project_root / ".cco").mkdir(exist_ok=True)
            (self.project_root / ".claude" / "commands").mkdir(parents=True, exist_ok=True)

            # Write project.json
            self._write_project_config()
            print_success("✓ Created .cco/project.json", indent=2)

            # Write commands.json
            self._write_commands_registry()
            print_success("✓ Created .cco/commands.json", indent=2)

            # Generate command files
            self._generate_command_files()
            print_success(f"✓ Generated {len(self.selected_commands)} command files", indent=2)

            # Generate PRINCIPLES.md
            self._generate_principles_md()
            print_success("✓ Created PRINCIPLES.md", indent=2)

            # Generate settings.local.json
            self._generate_settings_local()
            print_success("✓ Created .claude/settings.local.json", indent=2)

            # Copy statusline.js template
            self._copy_statusline()
            print_success("✓ Copied .claude/statusline.js", indent=2)

            # Generate CLAUDE.md
            self._generate_claude_md()
            print_success("✓ Created CLAUDE.md", indent=2)

            print()
            return True

        except Exception as e:
            print_error(f"File generation failed: {e}", indent=2)
            return False

    def _write_project_config(self) -> None:
        """Write .cco/project.json"""
        config_path = self.project_root / ".cco" / "project.json"

        preferences = self._build_preferences()
        config = preferences.dict()
        from .. import __version__

        config["cco"] = {
            "version": __version__,
            "configured_at": datetime.now().isoformat(),
            "mode": self.mode,
            "principle_count": len(self.selected_principles),
            "command_count": len(self.selected_commands),
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def _write_commands_registry(self) -> None:
        """Write .cco/commands.json"""
        registry_path = self.project_root / ".cco" / "commands.json"

        from .. import __version__

        registry = {
            "version": __version__,
            "configured_at": datetime.now().isoformat(),
            "commands": [
                {"id": cmd, "enabled": True, "category": "system"} for cmd in self.selected_commands
            ],
        }

        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

    def _generate_command_files(self) -> None:
        """Generate command files from templates"""
        from ..core.generator import CommandGenerator

        generator = CommandGenerator(self.project_root)
        result = generator.generate_all()

        if not result.get("success"):
            raise Exception(f"Command generation failed: {result.get('error')}")

    def _generate_principles_md(self) -> None:
        """Generate PRINCIPLES.md and category files"""
        from ..core.principle_selector import PrincipleSelector

        preferences = self._build_preferences()
        selector = PrincipleSelector(preferences)

        # Generate main PRINCIPLES.md
        output_path = self.project_root / "PRINCIPLES.md"
        selector.generate_principles_md(output_path)

        # Generate category files in docs/cco/principles/
        docs_path = self.project_root / "docs" / "cco" / "principles"
        selector.generate_category_files(docs_path)

    def _generate_settings_local(self) -> None:
        """Generate .claude/settings.local.json from global template"""
        import json
        from pathlib import Path

        from .. import config as CCOConfig  # noqa: N812

        # Try to load from global templates first, fallback to package assets
        templates_dir = CCOConfig.get_templates_dir()
        template_path = templates_dir / "generic" / "settings.local.template.json"

        if not template_path.exists():
            # Fallback to package assets
            package_root = Path(__file__).parent.parent
            template_path = package_root / "assets" / "settings.local.template.json"

        if not template_path.exists():
            print_warning(f"Template not found: {template_path}", indent=2)
            return

        with open(template_path, encoding="utf-8") as f:
            template_content = f.read()

        # Replace ${PROJECT_DIR} with actual project path
        # Convert to forward slashes for cross-platform compatibility
        project_dir_posix = str(self.project_root).replace("\\", "/")
        settings_content = template_content.replace("${PROJECT_DIR}", project_dir_posix)

        # Parse as JSON
        new_settings = json.loads(settings_content)

        # Check if .claude/settings.local.json already exists
        settings_path = self.project_root / ".claude" / "settings.local.json"

        if settings_path.exists():
            # Merge with existing settings
            with open(settings_path, encoding="utf-8") as f:
                existing_settings = json.load(f)

            merged_settings = self._merge_settings(existing_settings, new_settings)
        else:
            merged_settings = new_settings

        # Write merged settings
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(merged_settings, f, indent=2)

    def _copy_statusline(self) -> None:
        """Copy statusline.js from global template to .claude/"""
        import shutil
        from pathlib import Path

        from .. import config as CCOConfig  # noqa: N812

        # Try to load from global templates first, fallback to package assets
        templates_dir = CCOConfig.get_templates_dir()
        statusline_source = templates_dir / "generic" / "statusline.js"

        if not statusline_source.exists():
            # Fallback to package assets
            package_root = Path(__file__).parent.parent
            statusline_source = package_root / "assets" / "statusline.js"

        if not statusline_source.exists():
            print_warning(f"Statusline template not found: {statusline_source}", indent=2)
            return

        # Copy to project .claude directory
        statusline_dest = self.project_root / ".claude" / "statusline.js"
        statusline_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(statusline_source, statusline_dest)

    def _generate_claude_md(self) -> None:
        """Generate CLAUDE.md from template with customization"""
        from ..core.claude_md_generator import generate_claude_md

        # Build preferences
        preferences = self._build_preferences()

        # Output path - project root
        output_path = self.project_root / "CLAUDE.md"

        # Generate
        result = generate_claude_md(preferences.dict(), output_path)

        if not result.get("success"):
            raise Exception(f"CLAUDE.md generation failed: {result.get('error')}")

    def _merge_settings(self, existing: dict, template: dict) -> dict:
        """Merge template settings with existing settings"""
        merged = existing.copy()

        # Merge permissions
        if "permissions" in template:
            if "permissions" not in merged:
                merged["permissions"] = {}

            for key in ["allow", "deny", "ask"]:
                if key in template.get("permissions", {}):
                    existing_rules = set(merged.get("permissions", {}).get(key, []))
                    template_rules = set(template["permissions"].get(key, []))
                    # Merge: existing + new template rules
                    merged["permissions"][key] = sorted(existing_rules | template_rules)

        # Keep existing hooks, statusLine, outputStyle (user customizations)
        return merged

    # ========================================================================
    # Phase 7: Completion
    # ========================================================================

    def _show_completion(self, duration: float) -> None:
        """Show completion summary"""
        if self.mode == "interactive":
            clear_screen()

        print_header("✅ CCO Configuration Complete!", "Your project is ready")
        print()

        display_completion_summary(
            commands_installed=len(self.selected_commands),
            principles_configured=len(self.selected_principles),
            files_created=4,  # project.json, commands.json, PRINCIPLES.md, commands
            duration_seconds=duration,
        )

        print()
        print_info("Next steps:", indent=2)
        print_info("  1. Review PRINCIPLES.md to understand your principles", indent=2)
        print_info("  2. Run /cco-status to see your configuration", indent=2)
        print_info("  3. Run /cco-audit to analyze your codebase", indent=2)
        print()

    # ========================================================================
    # Helpers
    # ========================================================================

    def _build_preferences(self) -> Dict:
        """Build CCOPreferences object from answers"""
        # This is a simplified version
        # TODO: Map all answers to proper CCOPreferences schema

        answers = self.answer_context.answers

        return {
            "project_identity": {
                "name": self.project_root.name,
                "types": answers.get("project_purpose", []),
                "team_trajectory": answers.get("team_dynamics", "solo"),
                "project_maturity": answers.get("project_maturity", "prototype"),
            },
            "development_style": {
                "code_philosophy": answers.get("development_philosophy", "balanced"),
            },
            "testing": {
                "coverage_target": self._map_testing_to_coverage(
                    answers.get("testing_approach", "no_tests"),
                ),
            },
            "security": {
                "security_stance": answers.get("security_stance", "standard"),
            },
            "documentation": {
                "verbosity": answers.get("documentation_level", "minimal"),
            },
            "code_quality": {
                "linting_strictness": self._map_strategy_to_strictness(
                    answers.get("principle_strategy", "recommended"),
                ),
            },
            "selected_principle_ids": self.selected_principles,
        }

    def _map_testing_to_coverage(self, testing_approach: str) -> str:
        """Map testing approach to coverage target"""
        mapping = {
            "no_tests": "0",
            "critical_paths": "50",
            "balanced": "80",
            "comprehensive": "90",
        }
        return mapping.get(testing_approach, "80")

    def _map_strategy_to_strictness(self, strategy: str) -> str:
        """Map principle strategy to linting strictness"""
        mapping = {
            "minimal": "moderate",
            "recommended": "strict",
            "comprehensive": "pedantic",
            "custom": "strict",
        }
        return mapping.get(strategy, "strict")


# ============================================================================
# Convenience Functions
# ============================================================================


def run_interactive_wizard(project_root: Path, dry_run: bool = False) -> WizardResult:
    """Run wizard in interactive mode"""
    wizard = CCOWizard(project_root, mode="interactive", dry_run=dry_run)
    return wizard.run()


def run_quick_wizard(project_root: Path, dry_run: bool = False) -> WizardResult:
    """Run wizard in quick mode"""
    wizard = CCOWizard(project_root, mode="quick", dry_run=dry_run)
    return wizard.run()
