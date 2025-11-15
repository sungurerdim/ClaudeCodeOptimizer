"""
Wizard Orchestrator - Unified Interactive & Quick Modes

Executes the same decision tree in two modes:
- Interactive: Ask user for each decision
- Quick: Use AI auto-strategy for each decision

Both modes produce identical WizardResult structures.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from ..ai.detection import UniversalDetector
from ..schemas.commands import CommandRegistry
from ..schemas.preferences import CCOPreferences
from .checkpoints import (
    display_completion_summary,
    display_detection_results,
)
from .decision_tree import get_all_decisions
from .models import AnswerContext, DecisionPoint, SystemContext, WizardResult
from .recommendations import RecommendationEngine
from .renderer import (
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
from .ui_adapter import ClaudeCodeUIAdapter


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
        self.selected_guides: List[str] = []
        self.selected_agents: List[str] = []
        self.selected_skills: List[str] = []

        # Engines
        self.rec_engine = RecommendationEngine()

        # UI Adapter (auto-detects Claude Code context)
        self.ui_adapter = ClaudeCodeUIAdapter()

    # ========================================================================
    # Main Execution Flow
    # ========================================================================

    def export_questions(self) -> Dict:
        """
        Export questions for Claude Code UI interaction.

        Returns dict with:
        - questions: List of questions in AskUserQuestion format
        - system_context: Detected system info
        - project_detection: Detected project info
        """
        # Run detection silently (no user interaction needed)
        # Temporarily switch to quick mode for detection
        original_mode = self.mode
        self.mode = "quick"

        try:
            if not self._run_system_detection():
                return {"error": "System detection failed"}

            if not self._run_project_detection():
                return {"error": "Project detection failed"}
        finally:
            # Restore original mode
            self.mode = original_mode

        # Initialize answer context
        assert self.system_context is not None, "System context must be initialized"  # noqa: S101 - Type narrowing after detection
        self.answer_context = AnswerContext(system=self.system_context)

        # Get all decision points
        from .decision_tree import get_all_decisions

        all_decisions = get_all_decisions(self.answer_context)

        # Convert to AskUserQuestion format with AI recommendations
        questions_export = []
        for decision in all_decisions:
            # Skip conditional questions for now (we'll handle them in phase 2)
            if not decision.should_ask({}):
                continue

            # Get AI recommendation for this question
            ai_recommendation = decision.get_recommended_option(self.answer_context)
            ai_hint = decision.get_ai_hint(self.answer_context)

            # Build options with recommendation markers
            options_with_recommendations = []
            for opt in decision.options:
                option_dict = {
                    "value": opt.value,
                    "label": opt.label,
                    "description": opt.description,
                }

                # Mark recommended option
                if decision.multi_select:
                    # For multi-select, check if this option is in recommendation list
                    if isinstance(ai_recommendation, list) and opt.value in ai_recommendation:
                        option_dict["recommended"] = True
                        option_dict["label"] = f"⭐ {opt.label}"
                else:
                    # For single-select, check if this is the recommended option
                    if ai_recommendation == opt.value:
                        option_dict["recommended"] = True
                        option_dict["label"] = f"⭐ {opt.label}"

                options_with_recommendations.append(option_dict)

            question_data = {
                "id": decision.id,
                "tier": decision.tier,
                "category": decision.category,
                "question": decision.question,
                "header": decision.category.replace("_", " ").title()[:12],
                "multiSelect": decision.multi_select,
                "options": options_with_recommendations,
                "why": decision.why_this_question,
                "ai_recommendation": ai_recommendation,  # Include AI recommendation
                "ai_hint": ai_hint,  # Include AI reasoning
            }
            questions_export.append(question_data)

        assert self.system_context is not None, "System context must be initialized"  # noqa: S101 - Type narrowing after detection
        assert self.detection_report is not None, "Detection report must be initialized"  # noqa: S101 - Type narrowing after detection

        return {
            "questions": questions_export,
            "system_context": {
                "os": self.system_context.os_type,
                "language": self.system_context.detected_language,
                "is_git": self.system_context.is_git_repo,
            },
            "project_detection": {
                "languages": [
                    lang["detected_value"] for lang in self.detection_report.get("languages", [])
                ],
                "frameworks": [
                    f["detected_value"] for f in self.detection_report.get("frameworks", [])
                ],
            },
        }

    def run_with_answers(self, answers_dict: Dict) -> WizardResult:
        """
        Run wizard with pre-collected answers from Claude Code UI.

        Args:
            answers_dict: Dict mapping question IDs to user answers

        Returns:
            WizardResult with success status and all data
        """
        start_time = time.time()

        # Run in quick mode to avoid interactive prompts
        original_mode = self.mode
        self.mode = "quick"

        try:
            # System & project detection should already be done in export_questions()
            # If not, run them now
            if self.system_context is None:
                if not self._run_system_detection():
                    # Create a minimal SystemContext for the error case
                    from pathlib import Path

                    minimal_ctx = SystemContext(
                        os_type="linux",
                        os_version="unknown",
                        os_platform="unknown",
                        shell_type="unknown",
                        terminal_emulator="unknown",
                        color_support=False,
                        unicode_support=True,
                        system_locale="en_US",
                        detected_language="en",
                        encoding="utf-8",
                        python_version="unknown",
                        python_executable="python",
                        pip_version="unknown",
                        git_installed=False,
                        project_root=Path.cwd(),
                    )
                    return WizardResult(
                        success=False,
                        mode=original_mode,
                        system_context=minimal_ctx,
                        answers={},
                        error="System detection failed",
                    )

            if self.detection_report is None:
                if not self._run_project_detection():
                    assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                    return WizardResult(
                        success=False,
                        mode=original_mode,
                        system_context=self.system_context,
                        answers={},
                        error="Project detection failed",
                    )

            # Initialize answer context with provided answers
            assert self.system_context is not None, "System context must be initialized"  # noqa: S101 - Type narrowing after detection
            self.answer_context = AnswerContext(system=self.system_context)
            for question_id, answer in answers_dict.items():
                self.answer_context.set(question_id, answer)

            # Continue with principle selection
            assert self.answer_context is not None  # noqa: S101 - Type narrowing after initialization
            if not self._run_principle_selection():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers,
                    error="Principle selection failed",
                )

            # Command Selection
            if not self._run_command_selection():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
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
                    assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
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

            assert self.system_context is not None  # noqa: S101 - Type narrowing for final result
            return WizardResult(
                success=True,
                mode=original_mode,
                system_context=self.system_context,
                answers=self.answer_context.answers,
                selected_principles=self.selected_principles,
                selected_commands=self.selected_commands,
                duration_seconds=duration,
            )

        except Exception as e:
            import traceback
            from pathlib import Path

            # Ensure we have a valid SystemContext for error reporting
            if self.system_context is None:
                minimal_ctx = SystemContext(
                    os_type="linux",
                    os_version="unknown",
                    os_platform="unknown",
                    shell_type="unknown",
                    terminal_emulator="unknown",
                    color_support=False,
                    unicode_support=True,
                    system_locale="en_US",
                    detected_language="en",
                    encoding="utf-8",
                    python_version="unknown",
                    python_executable="python",
                    pip_version="unknown",
                    git_installed=False,
                    project_root=Path.cwd(),
                )
                ctx = minimal_ctx
            else:
                ctx = self.system_context

            return WizardResult(
                success=False,
                mode=original_mode,
                system_context=ctx,
                answers=self.answer_context.answers if self.answer_context else {},
                error=f"Wizard failed: {e}\n{traceback.format_exc()}",
            )
        finally:
            # Restore original mode
            self.mode = original_mode

    @staticmethod
    def uninitialize(project_root: Path) -> Dict:
        """
        Remove CCO from project.

        This is a static method that doesn't require wizard initialization.

        Args:
            project_root: Path to project root directory

        Returns:
            Dict with:
                - success (bool): True if successful
                - project_name (str): Name of project
                - files_removed (list): List of removed files
                - message (str): Success message
                OR
                - success (bool): False if failed
                - error (str): Error message
        """
        from ..config import get_project_commands_dir
        from ..core.hybrid_claude_md_generator import remove_cco_section

        try:
            project_name = project_root.name
            files_removed = []
            claude_dir = project_root / ".claude"

            # 1. Remove all symlinks in .claude/ subdirectories
            categories = ["commands", "guides", "principles", "agents", "skills"]
            for category in categories:
                category_dir = claude_dir / category
                if category_dir.exists():
                    for item in category_dir.iterdir():
                        # Remove symlinks and regular files (but keep .gitkeep)
                        if item.name != ".gitkeep":
                            if item.is_symlink() or item.is_file():
                                item.unlink()
                                files_removed.append(str(item.relative_to(project_root)))
                            elif item.is_dir():
                                # Remove directories recursively
                                import shutil

                                shutil.rmtree(item)
                                files_removed.append(str(item.relative_to(project_root)))

            # 2. Remove all cco-*.md command files from .claude/commands/
            project_commands_dir = get_project_commands_dir(project_root)
            if project_commands_dir.exists():
                for cmd_file in project_commands_dir.glob("cco-*.md"):
                    if cmd_file.exists():  # May have been removed in step 1
                        cmd_file.unlink()
                        rel_path = str(cmd_file.relative_to(project_root))
                        if rel_path not in files_removed:
                            files_removed.append(rel_path)

            # 3. Clean CCO sections from CLAUDE.md
            claude_md_path = project_root / "CLAUDE.md"
            if claude_md_path.exists():
                if remove_cco_section(claude_md_path):
                    files_removed.append("CLAUDE.md (CCO sections removed)")

            # 4. Clean CCO section from .gitignore
            gitignore_path = project_root / ".gitignore"
            if gitignore_path.exists():
                content = gitignore_path.read_text(encoding="utf-8")
                lines = content.splitlines(keepends=True)
                new_lines = []
                skip = False

                for line in lines:
                    # Start of CCO section
                    if "# CCO: Symlinked knowledge base" in line or "# CCO:" in line:
                        skip = True
                        continue
                    # End of CCO section (next non-CCO comment or content)
                    elif (
                        skip
                        and line.strip()
                        and not line.startswith(".claude/")
                        and not line.startswith("!.claude/")
                    ):
                        skip = False

                    if not skip:
                        new_lines.append(line)

                # Write back if changed
                new_content = "".join(new_lines)
                if new_content != content:
                    gitignore_path.write_text(new_content, encoding="utf-8")
                    files_removed.append(".gitignore (CCO section removed)")

            # 5. Remove empty .claude/ subdirectories
            for category in categories:
                category_dir = claude_dir / category
                if category_dir.exists() and not any(category_dir.iterdir()):
                    category_dir.rmdir()
                    files_removed.append(str(category_dir.relative_to(project_root)))

            # 6. Remove .claude/ if empty
            if claude_dir.exists() and not any(claude_dir.iterdir()):
                claude_dir.rmdir()
                files_removed.append(str(claude_dir.relative_to(project_root)))

            return {
                "success": True,
                "project_name": project_name,
                "files_removed": files_removed,
                "message": f"CCO uninitialized. Removed {len(files_removed)} items.",
            }

        except Exception as e:
            import logging

            logging.exception("Uninitialize failed")
            return {
                "success": False,
                "error": str(e),
            }

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
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers={},
                    error="System detection failed",
                )

            # Project Detection (UniversalDetector)
            if not self._run_project_detection():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers={},
                    error="Project detection failed",
                )

            # Decision Tree (TIER 1-3)
            if not self._run_decision_tree():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers if self.answer_context else {},
                    error="Decision tree execution failed",
                )

            # Principle Selection
            assert self.answer_context is not None  # noqa: S101 - Type narrowing after decision tree
            if not self._run_principle_selection():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
                return WizardResult(
                    success=False,
                    mode=self.mode,
                    system_context=self.system_context,
                    answers=self.answer_context.answers,
                    error="Principle selection failed",
                )

            # Command Selection
            if not self._run_command_selection():
                assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
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
                    assert self.system_context is not None  # noqa: S101 - Type narrowing for error reporting
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

            assert self.system_context is not None  # noqa: S101 - Type narrowing for final result
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
            assert self.system_context is not None  # noqa: S101 - Type narrowing for error handling
            return WizardResult(
                success=False,
                mode=self.mode,
                system_context=self.system_context,
                answers=self.answer_context.answers if self.answer_context else {},
                error="Cancelled by user",
            )
        except Exception as e:
            print_error(f"Wizard failed: {str(e)}", indent=2)
            assert self.system_context is not None  # noqa: S101 - Type narrowing for error handling
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
        """Show welcome message and ensure global content base is initialized"""
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

        # Ensure global content base is initialized
        self._ensure_global_knowledge_base()

        if self.mode == "interactive":
            pause()

    def _ensure_global_knowledge_base(self) -> None:
        """Ensure global content base (~/.cco/) is initialized"""
        from ..core.knowledge_setup import setup_global_knowledge

        try:
            # Setup global knowledge if not exists
            result = setup_global_knowledge(force=False)

            if result["actions"] and result["actions"][0] != "Knowledge base already up to date":
                print_info("✓ Global content base initialized", indent=2)
                for action in result["actions"]:
                    print_info(f"  - {action}", indent=2)
                print()
        except Exception as e:
            print_warning(f"Content base setup warning: {e}", indent=2)
            print_info("Continuing with wizard...", indent=2)
            print()

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
            assert self.system_context is not None, (  # noqa: S101
                "System context must be initialized before enrichment"
            )
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
        from .renderer import ask_yes_no

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
        assert self.detection_report is not None, "Detection report must be initialized"  # noqa: S101 - Type narrowing after detection
        languages = self.detection_report.get("languages", [])
        if languages:
            return languages[0].get("detected_value", "Unknown")
        return "Unknown"

    def _get_frameworks_summary(self) -> str:
        """Get frameworks summary"""
        assert self.detection_report is not None, "Detection report must be initialized"  # noqa: S101 - Type narrowing after detection
        frameworks = self.detection_report.get("frameworks", [])
        if frameworks:
            names = [fw.get("detected_value", "") for fw in frameworks[:3]]  # Top 3
            return ", ".join(names) if names else "None"
        return "None"

    def _get_project_type_summary(self) -> str:
        """Get project type summary"""
        assert self.detection_report is not None, "Detection report must be initialized"  # noqa: S101 - Type narrowing after detection
        types = self.detection_report.get("project_types", [])
        if types:
            names = [t.get("name", "") for t in types[:2]]  # Top 2
            return ", ".join(names) if names else "Unknown"
        return "Unknown"

    # ========================================================================
    # Phase 3: Decision Tree (TIER 1-3)
    # ========================================================================

    def _run_decision_tree(self) -> bool:
        """
        Execute decision tree for all tiers.

        IMPORTANT: Both interactive and quick modes execute THE SAME decision points.
        The only difference is HOW each decision is answered:
        - Interactive mode: User is prompted for input
        - Quick mode: AI auto-strategy is used

        This ensures consistency across both modes - same decisions, same order,
        just different input methods.
        """
        # Initialize answer context
        assert self.system_context is not None, "System context must be initialized"  # noqa: S101 - Type narrowing after detection
        self.answer_context = AnswerContext(system=self.system_context)

        # Get all decision points (TIER 1-3)
        try:
            all_decisions = get_all_decisions(self.answer_context)
        except Exception as e:
            print_error(f"Failed to build decision tree: {e}", indent=2)
            return False

        # Track execution for verification
        decisions_executed = 0
        decisions_skipped = 0

        # Execute each decision (same for both modes)
        for decision in all_decisions:
            # Check if should ask (conditional questions may be skipped)
            if not decision.should_ask(self.answer_context.answers):
                decisions_skipped += 1
                continue

            # Ask question (mode-dependent: interactive vs quick)
            try:
                answer = self._execute_decision(decision)
                self.answer_context.set(decision.id, answer)
                decisions_executed += 1
            except Exception as e:
                print_error(f"Failed to execute decision '{decision.id}': {e}", indent=2)
                return False

        # Log execution summary for verification
        if self.mode == "quick":
            print_info(
                f"Decision tree complete: {decisions_executed} decisions made, "
                f"{decisions_skipped} skipped (conditional)",
                indent=2,
            )
            print()

        return True

    def _execute_decision(self, decision: DecisionPoint) -> Any:  # noqa: ANN401
        """
        Execute a single decision point.

        Interactive mode: Ask user
        Quick mode: Use auto_strategy
        """
        if self.mode == "interactive":
            return self._ask_user_decision(decision)
        else:  # quick
            return self._auto_decide(decision)

    def _ask_user_decision(self, decision: DecisionPoint) -> Any:  # noqa: ANN401
        """Ask user for decision (Interactive mode)"""
        # Use UI adapter for context-aware presentation
        # The adapter handles both Claude Code rich UI and terminal fallback

        # Show tier header for terminal mode (UI adapter will handle its own formatting)
        if self.ui_adapter.mode == "terminal":
            clear_screen()
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

        # Delegate to UI adapter
        assert self.answer_context is not None, "Answer context must be initialized"  # noqa: S101 - Type narrowing after initialization
        answer = self.ui_adapter.ask_decision(decision, self.answer_context)

        return answer

    def _auto_decide(self, decision: DecisionPoint) -> Any:  # noqa: ANN401
        """Auto-decide using AI strategy (Quick mode)"""
        assert self.answer_context is not None, "Answer context must be initialized"  # noqa: S101 - Type narrowing after initialization
        answer = decision.get_recommended_option(self.answer_context)

        # Log decision
        if decision.multi_select:
            answer_str = ", ".join(answer) if isinstance(answer, list) else str(answer)
        else:
            answer_str = str(answer)

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

                    # Format: "U_DRY: Principle Title (severity, category)"
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

            # Auto-select all available guides/agents/skills (knowledge base)
            from ..core.knowledge_setup import (
                get_available_agents,
                get_available_guides,
                get_available_skills,
            )

            # In quick mode: auto-select recommended
            # In interactive mode: let user choose
            if self.mode == "quick":
                self.selected_guides = self._recommend_guides_for_project()
                self.selected_agents = self._recommend_agents_for_project()
                self.selected_skills = self._recommend_skills_for_project()

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

                # Knowledge Base Selection (interactive only)
                print_header("Knowledge Base Selection", "Select components to symlink")
                print_info("Select which knowledge base components to symlink:", indent=2)
                print()

                # Guides selection with descriptions
                available_guides = get_available_guides()
                if available_guides:
                    # Guide descriptions
                    guide_descriptions = {
                        "cco-verification-protocol": "Evidence-based verification workflow (U_EVIDENCE_BASED)",
                        "cco-git-workflow": "Git commit, branching, PR guidelines (U_ATOMIC_COMMITS, U_CONCISE_COMMITS)",
                        "cco-security-response": "Security incident response and remediation plan",
                        "cco-performance-optimization": "Performance analysis and optimization workflow",
                        "cco-container-best-practices": "Docker/Kubernetes deployment best practices",
                    }

                    # Recommend guides based on project context
                    recommended_guides = self._recommend_guides_for_project()

                    print_info(f"Available guides ({len(available_guides)}):", indent=2)
                    print_info(
                        f"  Recommended for your project: {len(recommended_guides)}",
                        indent=2,
                    )
                    print()

                    # Show each guide with description and recommendation
                    for i, guide in enumerate(available_guides, 1):
                        guide_name = guide.replace("-", " ").title()
                        description = guide_descriptions.get(guide, "")
                        is_recommended = guide in recommended_guides
                        marker = "⭐" if is_recommended else "  "

                        print_info(f"{marker} {i}. {guide_name}", indent=2)
                        if description:
                            print_info(f"      {description}", indent=2)
                    print()

                    response = (
                        input(
                            "  Select guides (all/recommended/none or numbers like 1,3,5) [default: recommended]: "
                        )
                        .strip()
                        .lower()
                    )
                    if response == "all":
                        self.selected_guides = available_guides
                        print_success(f"✓ Selected all {len(available_guides)} guides", indent=2)
                    elif response == "" or response == "recommended":
                        self.selected_guides = recommended_guides
                        print_success(
                            f"✓ Selected {len(recommended_guides)} recommended guides",
                            indent=2,
                        )
                    elif response == "none":
                        self.selected_guides = []
                        print_info("✓ No guides selected", indent=2)
                    else:
                        # Parse number selection (e.g., "1,3,5")
                        try:
                            indices = [int(x.strip()) - 1 for x in response.split(",")]
                            self.selected_guides = [
                                available_guides[i]
                                for i in indices
                                if 0 <= i < len(available_guides)
                            ]
                            print_success(
                                f"✓ Selected {len(self.selected_guides)} guides",
                                indent=2,
                            )
                        except (ValueError, IndexError):
                            # Fallback to recommended
                            self.selected_guides = recommended_guides
                            print_warning("Invalid selection, using recommended", indent=2)
                    print()
                else:
                    self.selected_guides = []
                    print_info("No guides available", indent=2)

                # Agents selection (simplified for now - agents are advanced use case)
                available_agents = get_available_agents()
                if available_agents:
                    print_info(f"Available custom agents ({len(available_agents)}):", indent=2)
                    print_info(
                        "  Custom agents are advanced - select only if you created them",
                        indent=2,
                    )
                    print()

                    response = input("  Select agents (all/none) [default: none]: ").strip().lower()
                    if response == "all":
                        self.selected_agents = available_agents
                        print_success(f"✓ Selected all {len(available_agents)} agents", indent=2)
                    else:
                        self.selected_agents = []
                        print_info("✓ No custom agents selected", indent=2)
                    print()
                else:
                    self.selected_agents = []
                    print_info("No custom agents available", indent=2)
                    print_info(
                        "Tip: Create custom agents using templates in ~/.cco/agents/",
                        indent=2,
                    )
                    print()

                # Skills selection with workflow-based recommendations
                available_skills = get_available_skills()
                if available_skills:
                    # Recommend skills based on project workflow needs
                    recommended_skills = self._recommend_skills_for_project()

                    # Skill descriptions
                    skill_descriptions = {
                        "cco-skill-verification-protocol": "Evidence-based fix-verify-commit loop (U_EVIDENCE_BASED)",
                        "cco-skill-test-first-verification": "Generate tests before code changes (U_TEST_FIRST)",
                        "cco-skill-root-cause-analysis": "Analyze WHY violations exist, not just WHERE",
                        "cco-skill-incremental-improvement": "Break large tasks into achievable milestones",
                        "cco-skill-security-emergency-response": "Immediate P0 CRITICAL security remediation",
                    }

                    print_info(
                        f"Available workflow skills ({len(available_skills)}):",
                        indent=2,
                    )
                    print_info(
                        f"  Recommended for your project: {len(recommended_skills)}",
                        indent=2,
                    )
                    print()

                    # Show each skill with description and recommendation
                    for i, skill in enumerate(available_skills, 1):
                        # Skip templates and README
                        if skill.startswith("_") or skill == "README":
                            continue

                        skill_name = skill.replace("-", " ").title()
                        description = skill_descriptions.get(skill, "")
                        is_recommended = skill in recommended_skills
                        marker = "⭐" if is_recommended else "  "

                        print_info(f"{marker} {i}. {skill_name}", indent=2)
                        if description:
                            print_info(f"      {description}", indent=2)
                    print()

                    response = (
                        input("  Select skills (all/recommended/none) [default: recommended]: ")
                        .strip()
                        .lower()
                    )
                    if response == "all":
                        self.selected_skills = [
                            s for s in available_skills if not s.startswith("_") and s != "README"
                        ]
                        print_success(
                            f"✓ Selected all {len(self.selected_skills)} skills",
                            indent=2,
                        )
                    elif response == "" or response == "recommended":
                        self.selected_skills = recommended_skills
                        print_success(
                            f"✓ Selected {len(recommended_skills)} recommended skills",
                            indent=2,
                        )
                    else:
                        self.selected_skills = []
                        print_info("✓ No skills selected", indent=2)
                    print()
                else:
                    self.selected_skills = []
                    print_info("No workflow skills available", indent=2)
                    print()

                pause()

            else:  # quick mode
                print_success(f"✓ Installing {len(self.selected_commands)} commands", indent=2)
                print_info(f"  Core: {len(command_recs['core'])} commands", indent=2)
                print_info(
                    f"  Recommended: {len(command_recs['recommended'])} commands",
                    indent=2,
                )
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

    def _build_command_registry(self) -> CommandRegistry:
        """Build command registry from available global commands"""
        from .. import config as CCOConfig  # noqa: N812
        from ..schemas.commands import CommandMetadata, CommandRegistry

        # Get global commands directory
        global_commands_dir = CCOConfig.get_global_commands_dir()

        commands = []
        if global_commands_dir.exists():
            for cmd_file in global_commands_dir.glob("*.md"):
                # Extract command ID from filename (already has cco- prefix)
                command_id = cmd_file.stem

                # Create minimal metadata
                commands.append(
                    CommandMetadata(
                        command_id=command_id,
                        display_name=cmd_file.stem.replace("-", " ").title(),
                        category="general",
                        description_short=f"{cmd_file.stem} command",
                        description_long=f"CCO {cmd_file.stem} command",
                        applicable_project_types=["all"],
                        is_core=False,
                        is_experimental=False,
                        usage_frequency=0,
                        success_rate=None,
                        last_used=None,
                    ),
                )

        from .. import __version__ as cco_version

        return CommandRegistry(commands=commands, version=cco_version)

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
            # Create .claude directory structure
            (self.project_root / ".claude" / "commands").mkdir(parents=True, exist_ok=True)

            # Setup knowledge base symlinks
            self._setup_knowledge_symlinks()
            print_success("✓ Created knowledge base symlinks", indent=2)

            # Update .gitignore for symlinks
            self._update_gitignore()
            print_success("✓ Updated .gitignore", indent=2)

            # Generate CLAUDE.md
            self._generate_claude_md()
            print_success("✓ Created CLAUDE.md", indent=2)

            # REMOVED: All optional file generation (editorconfig, pre-commit, CI/CD, GitHub templates, IDE configs, env, logging)
            # CCO PRINCIPLE: Keep project directories clean - only .claude/ and CLAUDE.md

            print()
            return True

        except Exception as e:
            print_error(f"File generation failed: {e}", indent=2)
            return False

    def _generate_command_files(self) -> None:
        """Generate command files from templates"""
        from ..core.generator import CommandGenerator

        generator = CommandGenerator(self.project_root)
        result = generator.generate_all()

        if not result.get("success"):
            raise Exception(f"Command generation failed: {result.get('error')}")

    def _setup_knowledge_symlinks(self) -> None:
        """
        Create symlinks in .claude/ to global knowledge base.

        Symlinks selected commands, guides, principles, agents, skills from
        ~/.cco/knowledge/ to project .claude/ directory.

        IMPORTANT: Cleans directories before installation to ensure only selected items are present.
        """
        import platform

        from .. import config
        from ..core.knowledge_setup import setup_global_knowledge

        # Ensure global knowledge base exists
        setup_global_knowledge()

        # Create .claude subdirectories
        claude_dir = self.project_root / ".claude"
        categories = ["commands", "guides", "principles", "agents", "skills"]

        for category in categories:
            (claude_dir / category).mkdir(parents=True, exist_ok=True)
            # Create .gitkeep to preserve directory structure
            (claude_dir / category / ".gitkeep").touch()

        # STEP 1: Clean only CCO-managed files (CRITICAL: Don't delete user's custom files!)
        # Read list of previously managed files from tracking file
        managed_file_path = claude_dir / ".cco-managed"
        previously_managed = set()
        if managed_file_path.exists():
            try:
                content = managed_file_path.read_text(encoding="utf-8")
                previously_managed = {line.strip() for line in content.splitlines() if line.strip()}
            except Exception:
                # If can't read tracking file, skip cleanup (safer than deleting unknown files)
                pass

        # Remove only files that were installed by CCO in previous init
        for category in categories:
            category_dir = claude_dir / category
            if category_dir.exists():
                for old_file in category_dir.rglob("*"):
                    if old_file.is_file() and old_file.name != ".gitkeep":
                        # Get relative path from .claude/ directory
                        relative_path = old_file.relative_to(claude_dir).as_posix()

                        # Only delete if it was managed by CCO
                        if relative_path in previously_managed:
                            old_file.unlink()

        # Get global knowledge directories
        global_commands_dir = config.get_global_commands_dir()
        global_guides_dir = config.get_guides_dir()
        global_principles_dir = config.get_principles_dir()
        global_agents_dir = config.get_agents_dir()
        global_skills_dir = config.get_skills_dir()

        # Map selected items to their source directories
        symlink_map = []

        # Commands
        for cmd in self.selected_commands:
            source = global_commands_dir / f"{cmd}.md"
            target = claude_dir / "commands" / f"{cmd}.md"
            symlink_map.append((source, target, "command"))

        # Guides
        for guide in self.selected_guides:
            source = global_guides_dir / f"{guide}.md"
            target = claude_dir / "guides" / f"{guide}.md"
            symlink_map.append((source, target, "guide"))

        # Principles
        # FIRST: Always symlink ALL universal principles (U*.md - dynamically discovered)
        for u_file in sorted(global_principles_dir.glob("U*.md")):
            u_id = u_file.stem  # e.g., "U_DRY"
            source = u_file
            target = claude_dir / "principles" / f"{u_id}.md"
            symlink_map.append((source, target, "principle"))

        # SECOND: Symlink only AI-selected project-specific principles (P_*)
        for principle in self.selected_principles:
            # Skip if it's a universal principle (already linked above)
            if not principle.startswith("U"):
                source = global_principles_dir / f"{principle}.md"
                target = claude_dir / "principles" / f"{principle}.md"
                symlink_map.append((source, target, "principle"))

        # Agents (if any selected)
        if hasattr(self, "selected_agents"):
            for agent in self.selected_agents:
                source = global_agents_dir / f"{agent}.md"
                target = claude_dir / "agents" / f"{agent}.md"
                symlink_map.append((source, target, "agent"))

        # Skills (if any selected)
        if hasattr(self, "selected_skills"):
            for skill in self.selected_skills:
                source = global_skills_dir / f"{skill}.md"
                target = claude_dir / "skills" / f"{skill}.md"
                symlink_map.append((source, target, "skill"))

        # STEP 2: Create symlinks with fallback (symlink -> hardlink -> copy)
        # Track installation counts by category
        installation_counts = {
            "command": 0,
            "guide": 0,
            "principle": 0,
            "agent": 0,
            "skill": 0,
        }

        for source, target, category in symlink_map:
            # Ensure parent directory exists (for language-specific skills like python/*)
            target.parent.mkdir(parents=True, exist_ok=True)

            # Note: We already cleaned directories, so no need to unlink here

            # Try symlink -> hardlink -> copy (cross-platform fallback)
            link_created = False

            # 1. Try symlink first (best option)
            if platform.system() == "Windows":
                # Windows: try mklink (requires Developer Mode or admin)
                import subprocess

                try:
                    subprocess.run(  # noqa: S603
                        [  # noqa: S607 - cmd is built-in Windows command
                            "cmd",
                            "/c",
                            "mklink",
                            str(target),
                            str(source),
                        ],
                        check=True,
                        capture_output=True,
                    )
                    link_created = True
                except subprocess.CalledProcessError:
                    pass  # Fall through to hardlink
            else:
                # Unix: use symlink_to
                try:
                    target.symlink_to(source)
                    link_created = True
                except OSError:
                    pass  # Fall through to hardlink

            # 2. Try hardlink if symlink failed
            if not link_created:
                try:
                    import os

                    os.link(source, target)
                    link_created = True
                except (OSError, NotImplementedError):
                    pass  # Fall through to copy

            # 3. Fall back to hard copy if both symlink and hardlink failed
            if not link_created:
                import shutil

                shutil.copy2(source, target)

            # Count successful installation
            installation_counts[category] += 1

        # STEP 3: Store installation counts for reporting
        self.installed_commands_count = installation_counts["command"]
        self.installed_guides_count = installation_counts["guide"]
        self.installed_principles_count = installation_counts["principle"]
        self.installed_agents_count = installation_counts["agent"]
        self.installed_skills_count = installation_counts["skill"]

        # STEP 4: Validate that installed counts match expected counts
        expected_commands = len(self.selected_commands)
        expected_guides = len(self.selected_guides)
        # For principles: U_* (all) + selected P_*/C_* (non-U)
        expected_principles = len(list(global_principles_dir.glob("U*.md"))) + len(
            [p for p in self.selected_principles if not p.startswith("U")]
        )
        expected_agents = len(self.selected_agents) if hasattr(self, "selected_agents") else 0
        expected_skills = len(self.selected_skills) if hasattr(self, "selected_skills") else 0

        # Validation: raise error if mismatch
        mismatches = []
        if self.installed_commands_count != expected_commands:
            mismatches.append(
                f"Commands: expected {expected_commands}, installed {self.installed_commands_count}"
            )
        if self.installed_guides_count != expected_guides:
            mismatches.append(
                f"Guides: expected {expected_guides}, installed {self.installed_guides_count}"
            )
        if self.installed_principles_count != expected_principles:
            mismatches.append(
                f"Principles: expected {expected_principles}, installed {self.installed_principles_count}"
            )
        if self.installed_agents_count != expected_agents:
            mismatches.append(
                f"Agents: expected {expected_agents}, installed {self.installed_agents_count}"
            )
        if self.installed_skills_count != expected_skills:
            mismatches.append(
                f"Skills: expected {expected_skills}, installed {self.installed_skills_count}"
            )

        if mismatches:
            raise Exception(
                "Installation validation failed - mismatch between selected and installed:\n"
                + "\n".join(f"  - {m}" for m in mismatches)
            )

        # STEP 5: Write tracking file (SSOT for CCO-managed files)
        # List all installed files for future cleanup
        managed_files = []
        for _, target, _ in symlink_map:
            # Store relative path from .claude/ directory
            relative_path = target.relative_to(claude_dir).as_posix()
            managed_files.append(relative_path)

        # Write tracking file
        managed_file_path.write_text("\n".join(sorted(managed_files)) + "\n", encoding="utf-8")

    def _update_gitignore(self) -> None:
        """
        Update .gitignore to ignore symlinked knowledge base files.

        Adds CCO-specific section to .gitignore to exclude:
        - .claude/*/  symlinks (except .gitkeep)
        """
        gitignore_path = self.project_root / ".gitignore"

        # CCO gitignore section
        cco_section = """
# CCO: Symlinked knowledge base (ignore)
.claude/commands/*
.claude/guides/*
.claude/principles/*
.claude/agents/*
.claude/skills/*

# CCO: Tracking file (local only, regenerated on each init)
.claude/.cco-managed

# Keep directory structure
!.claude/commands/.gitkeep
!.claude/guides/.gitkeep
!.claude/principles/.gitkeep
!.claude/agents/.gitkeep
!.claude/skills/.gitkeep
"""

        # Check if .gitignore exists
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")

            # Check if CCO section already exists
            if "# CCO: Symlinked knowledge base" in content:
                # Already exists, skip
                return

            # Append CCO section
            if not content.endswith("\n"):
                content += "\n"
            content += cco_section

            gitignore_path.write_text(content, encoding="utf-8")
        else:
            # Create new .gitignore with CCO section
            gitignore_path.write_text(cco_section.lstrip(), encoding="utf-8")

    def _generate_claude_md(self) -> None:
        """Generate CLAUDE.md using ClaudeMdGenerator with full principle injection"""
        from ..core.claude_md_generator import ClaudeMdGenerator

        # Build preferences dict with selected principles
        preferences_dict = {
            "project_identity": {
                "name": self.project_root.name,
                "team_trajectory": (
                    self.answer_context.get("team_dynamics", "solo")
                    if self.answer_context
                    else "solo"
                ),
            },
            "code_quality": {
                "linting_strictness": "strict",  # Default
            },
            "testing": {
                "strategy": "balanced",  # Default
            },
            "selected_principle_ids": (
                self.selected_principles if self.selected_principles else []
            ),
        }

        # Generate CLAUDE.md
        output_path = self.project_root / "CLAUDE.md"
        generator = ClaudeMdGenerator(
            preferences_dict,
            selected_skills=(self.selected_skills if hasattr(self, "selected_skills") else []),
            selected_agents=(self.selected_agents if hasattr(self, "selected_agents") else []),
        )
        generator.generate(output_path)

    def _build_selected_principles_dict(self) -> Dict[str, List[str]]:
        """Build selected principles dictionary by category."""
        from pathlib import Path

        from ..core.principle_md_loader import load_all_principles

        # Load all principles to get universal count dynamically
        principles_dir = Path(__file__).parent.parent.parent / "content" / "principles"
        principles_list = load_all_principles(principles_dir)

        # Get all universal principles dynamically
        universal_ids = [p["id"] for p in principles_list if p.get("category") == "universal"]

        principles_dict = {"universal": universal_ids}

        # Group project-specific principles by category
        if self.selected_principles:
            # Categorize based on actual category from .md files
            all_principles = {p["id"]: p for p in principles_list}

            for pid in self.selected_principles:
                if pid.startswith("U"):  # Skip universal (already added)
                    continue

                principle = all_principles.get(pid)
                if principle:
                    category = principle.get("category", "other")
                    if category not in principles_dict:
                        principles_dict[category] = []
                    principles_dict[category].append(pid)

        return principles_dict

    def _inject_knowledge_references(self, content: str) -> str:
        """Inject selected principle/guide/agent/skill references into CLAUDE.md"""
        additions = []

        # Add error handling strategy if answered
        if self.answer_context and self.answer_context.has_answer("error_handling"):
            error_handling = self.answer_context.get("error_handling", "defensive")
            additions.append("\n### Error Handling Strategy (Project Configuration)\n")

            if error_handling == "defensive":
                additions.append(
                    "**Defensive Programming**: Validate all inputs, check all assumptions, fail gracefully.\n"
                )
                additions.append("- Validate all function inputs at entry points")
                additions.append("- Use type hints and runtime type checking")
                additions.append("- Provide helpful error messages with context")
                additions.append("- Log errors with full stack traces")
            elif error_handling == "fail_fast":
                additions.append(
                    "**Fail-Fast**: Errors cause immediate visible failure. No silent fallbacks.\n"
                )
                additions.append("- Never swallow exceptions without re-raising")
                additions.append("- Fail immediately on invalid state")
                additions.append("- Use assertions for invariants")
                additions.append("- See U_FAIL_FAST: Fail-Fast Error Handling in CLAUDE.md")
            elif error_handling == "exception_hierarchy":
                additions.append(
                    "**Exception Hierarchy**: Custom exception types for different error categories.\n"
                )
                additions.append("- Define custom exception classes per domain")
                additions.append("- Catch specific exceptions, not generic Exception")
                additions.append("- Include error context in exception data")
                additions.append("- Document which exceptions each function can raise")
            elif error_handling == "result_types":
                additions.append(
                    "**Result Types**: Use Result/Option types instead of exceptions for expected failures.\n"
                )
                additions.append("- Return Result[T, Error] for operations that can fail")
                additions.append("- Use Option[T] for nullable values")
                additions.append("- Reserve exceptions for truly exceptional cases")
                additions.append("- Chain operations with map/flatMap/and_then")

        # Category-specific principles
        if self.selected_principles:
            additions.append("\n### Category-Specific Principles (Project Selected)\n")
            additions.append("Load these principles based on your task context:\n")
            for principle in self.selected_principles:
                additions.append(f"- @.claude/principles/{principle}.md")

        # Detailed guides
        if self.selected_guides:
            additions.append("\n### Detailed Guides (Project Selected)\n")
            additions.append("Load these guides as needed:\n")
            for guide in self.selected_guides:
                # Humanize guide name
                guide_name = guide.replace("-", " ").title()
                additions.append(f"- **@.claude/guides/{guide}.md** - {guide_name}")

        # Agents
        if hasattr(self, "selected_agents") and self.selected_agents:
            additions.append("\n### Agents (Project Selected)\n")
            additions.append("Use these specialized agents for complex tasks:\n")
            for agent in self.selected_agents:
                agent_name = agent.replace("-", " ").title()
                additions.append(f"- **@.claude/agents/{agent}.md** - {agent_name}")

        # Skills
        if hasattr(self, "selected_skills") and self.selected_skills:
            additions.append("\n### Skills (Project Selected)\n")
            additions.append("Available skills via slash commands:\n")
            for skill in self.selected_skills:
                skill_name = skill.replace("-", " ").title()
                additions.append(f"- `/{skill}` - @.claude/skills/{skill}.md - {skill_name}")

        # Insert additions before footer
        if additions:
            footer_marker = "\n---\n\n*Part of CCO Documentation System*"
            if footer_marker in content:
                content = content.replace(
                    footer_marker, "\n\n" + "\n".join(additions) + footer_marker
                )
            else:
                # No footer, append to end
                content += "\n\n" + "\n".join(additions)

        return content

    def _old_generate_claude_md(self) -> None:
        """OLD: Generate CLAUDE.md from template with customization"""
        from ..core.claude_md_generator import generate_claude_md

        # Build preferences
        preferences = self._build_preferences()

        # Output path - project root
        output_path = self.project_root / "CLAUDE.md"

        # Generate
        result = generate_claude_md(preferences, output_path)

        if not result.get("success"):
            raise Exception(f"CLAUDE.md generation failed: {result.get('error')}")

    # ========================================================================
    # Phase 7: Completion
    # ========================================================================

    def _show_completion(self, duration: float) -> None:
        """Show completion summary with actual installation counts"""
        if self.mode == "interactive":
            clear_screen()

        print_header("✅ CCO Configuration Complete!", "Your project is ready")
        print()

        # Count major files created (CLAUDE.md, .gitignore update)
        files_count = 1  # CLAUDE.md
        if (self.project_root / ".gitignore").exists():
            files_count += 1  # Modified .gitignore

        # Use actual installed counts (tracked during installation)
        display_completion_summary(
            commands_installed=(
                self.installed_commands_count
                if hasattr(self, "installed_commands_count")
                else len(self.selected_commands)
            ),
            principles_configured=(
                self.installed_principles_count
                if hasattr(self, "installed_principles_count")
                else len(self.selected_principles)
            ),
            files_created=files_count,
            duration_seconds=duration,
            guides_installed=(
                self.installed_guides_count
                if hasattr(self, "installed_guides_count")
                else (len(self.selected_guides) if hasattr(self, "selected_guides") else 0)
            ),
            skills_installed=(
                self.installed_skills_count
                if hasattr(self, "installed_skills_count")
                else (len(self.selected_skills) if hasattr(self, "selected_skills") else 0)
            ),
            agents_installed=(
                self.installed_agents_count
                if hasattr(self, "installed_agents_count")
                else (len(self.selected_agents) if hasattr(self, "selected_agents") else 0)
            ),
        )

        print()
        print_info("Next steps:", indent=2)
        print_info("  1. Review CLAUDE.md to understand your development guide", indent=2)
        print_info("  2. Run /cco-status to see your configuration", indent=2)
        print_info("  3. Run /cco-audit to analyze your codebase", indent=2)
        print()

    # ========================================================================
    # Helpers
    # ========================================================================

    def _build_preferences(self) -> Dict:
        """Build CCOPreferences object from answers"""
        # Map answers to proper CCOPreferences schema

        assert self.answer_context is not None, "Answer context must be initialized"  # noqa: S101 - Type narrowing after initialization
        answers = self.answer_context.answers

        # Get primary language from system context
        primary_language = (
            self.system_context.detected_language
            if self.system_context and hasattr(self.system_context, "detected_language")
            else "python"
        )

        # Map git_workflow values (still needed for internal->schema conversion)
        git_workflow_mapping = {
            "main_only": "trunk-based",
            "trunk_based": "trunk-based",
            "git_flow": "git-flow",
            "github_flow": "github-flow",
            "gitlab_flow": "gitlab-flow",
        }

        # Map security_stance values
        security_mapping = {
            "production": "strict",
            "high": "very-strict",
            "standard": "balanced",
            "basic": "pragmatic",
        }

        # Map documentation_level values
        doc_mapping = {
            "comprehensive": "extensive",
            "standard": "concise",
            "minimal": "minimal",
        }

        # Map development_philosophy values
        philosophy_mapping = {
            "move_fast": "progressive",
            "quality_first": "conservative",
            "balanced": "balanced",
        }

        return {
            "project_identity": {
                "name": self.project_root.name,
                "types": answers.get("project_purpose", []),
                "primary_language": primary_language,
                "team_trajectory": answers.get("team_dynamics", "solo"),
                "project_maturity": answers.get("project_maturity", "active-dev"),
            },
            "development_style": {
                "code_philosophy": philosophy_mapping.get(
                    answers.get("development_philosophy", "balanced"), "balanced"
                ),
            },
            "testing": {
                "coverage_target": self._map_testing_to_coverage(
                    answers.get("testing_approach", "no_tests"),
                ),
            },
            "security": {
                "security_stance": security_mapping.get(
                    answers.get("security_stance", "standard"), "balanced"
                ),
            },
            "documentation": {
                "verbosity": doc_mapping.get(
                    answers.get("documentation_level", "minimal"), "minimal"
                ),
            },
            "code_quality": {
                "linting_strictness": self._map_strategy_to_strictness(
                    answers.get("principle_strategy", "recommended"),
                ),
            },
            "collaboration": {
                "git_workflow": git_workflow_mapping.get(
                    answers.get("git_workflow", "main_only"), "trunk-based"
                ),
                "versioning_strategy": answers.get("versioning_strategy", "auto_semver"),
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

    def _recommend_guides_for_project(self) -> List[str]:
        """
        Recommend guides based on comprehensive decision tree analysis.

        Maps all 24 decision points to relevant guides.
        """
        if not self.answer_context:
            return []

        recommended = []
        answers = self.answer_context.answers

        # Extract key decisions
        project_types = answers.get("project_purpose", [])
        team_size = answers.get("team_dynamics", "solo")
        maturity = answers.get("project_maturity", "prototype")
        philosophy = answers.get("development_philosophy", "balanced")
        testing = answers.get("testing_approach", "balanced")
        security = answers.get("security_stance", "standard")
        git_workflow = answers.get("git_workflow", "main_only")
        error_handling = answers.get("error_handling", "fail_fast")

        # TIER 1 Mappings: Fundamental Decisions

        # Verification Protocol: for quality-conscious projects
        if philosophy == "quality_first" or maturity in ["production", "legacy"]:
            recommended.append("cco-verification-protocol")

        # For all team projects (non-solo)
        if team_size != "solo":
            recommended.append("cco-verification-protocol")

        # Git Workflow Guide: for team projects with structured workflows
        if team_size in ["small-2-5", "medium-10-20", "large-20-50"]:
            recommended.append("cco-git-workflow")

        # Also for git flow or github flow
        if git_workflow in ["git_flow", "github_flow"]:
            if "cco-git-workflow" not in recommended:
                recommended.append("cco-git-workflow")

        # TIER 2 Mappings: Strategy Decisions

        # Security Response: for production or high security stance
        if security in ["production", "high"] or maturity == "production":
            recommended.append("cco-security-response")

        # For web/API projects (security critical)
        if any(pt in project_types for pt in ["backend", "web-app", "microservice", "spa"]):
            if "cco-security-response" not in recommended:
                recommended.append("cco-security-response")

        # Performance Optimization: for backend services or data pipelines
        if any(
            pt in project_types
            for pt in [
                "backend",
                "microservice",
                "data-pipeline",
                "ml",
                "analytics",
            ]
        ):
            recommended.append("cco-performance-optimization")

        # For projects that need retry/resilience
        if error_handling in ["retry_logic", "graceful_degradation"]:
            if "cco-performance-optimization" not in recommended:
                recommended.append("cco-performance-optimization")

        # Container Best Practices: for containerized infrastructure
        if any(pt in project_types for pt in ["microservice", "devtools", "data-pipeline", "ml"]):
            recommended.append("cco-container-best-practices")

        # TIER 3 Mappings: Tactical Decisions

        # Additional test-focused recommendations
        if testing in ["comprehensive", "balanced"]:
            if "cco-verification-protocol" not in recommended:
                recommended.append("cco-verification-protocol")

        return list(set(recommended))  # Remove duplicates

    def _recommend_skills_for_project(self) -> List[str]:
        """Add all universal skills + language-specific skills to project"""
        # Universal skills - always included in every project
        universal_skills = [
            "cco-skill-verification-protocol",
            "cco-skill-test-first-verification",
            "cco-skill-root-cause-analysis",
            "cco-skill-incremental-improvement",
            "cco-skill-security-emergency-response",
        ]

        # Language-specific skills - add if language detected
        language_specific_skills = []

        # Get detected languages from system context
        if self.system_context and hasattr(self.system_context, "detected_languages"):
            detected_languages = self.system_context.detected_languages

            # Add language-specific skills
            if "python" in [lang.lower() for lang in detected_languages]:
                language_specific_skills.extend(
                    [
                        "python/cco-skill-async-patterns",
                        "python/cco-skill-packaging-modern",
                        "python/cco-skill-performance",
                        "python/cco-skill-testing-pytest",
                        "python/cco-skill-type-hints-advanced",
                    ]
                )

            if "go" in [lang.lower() for lang in detected_languages]:
                # Go-specific skills (when available)
                pass

            if "rust" in [lang.lower() for lang in detected_languages]:
                # Rust-specific skills (when available)
                pass

            if any(lang.lower() in ["typescript", "javascript"] for lang in detected_languages):
                # TypeScript/JS-specific skills (when available)
                pass

        return list(set(universal_skills + language_specific_skills))  # Remove duplicates

    def _recommend_agents_for_project(self) -> List[str]:
        """Add all universal agents to every project (always included)"""
        # Universal agents - always included in every project
        universal_agents = [
            "cco-agent-audit",
            "cco-agent-fix",
            "cco-agent-generate",
        ]

        return universal_agents


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
