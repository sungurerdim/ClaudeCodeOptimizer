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
                indent=2
            )
            print()

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
        answer = self.ui_adapter.ask_decision(decision, self.answer_context)

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

            # Auto-select all available guides/agents/skills (knowledge base)
            from ..core.knowledge_setup import get_available_guides, get_available_agents, get_available_skills, get_principle_categories

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
                if not hasattr(self, 'print_heading'):
                    from .renderer import print_heading
                print_heading("Knowledge Base Selection", level=2)
                print_info("Select which knowledge base components to symlink:", indent=2)
                print()

                # Guides selection with descriptions
                available_guides = get_available_guides()
                if available_guides:
                    # Guide descriptions
                    guide_descriptions = {
                        "verification-protocol": "Evidence-based verification workflow (P067)",
                        "git-workflow": "Git commit, branching, PR guidelines (P072-P074)",
                        "security-response": "Security incident response and remediation plan",
                        "performance-optimization": "Performance analysis and optimization workflow",
                        "container-best-practices": "Docker/Kubernetes deployment best practices",
                    }

                    # Recommend guides based on project context
                    recommended_guides = self._recommend_guides_for_project()

                    print_info(f"Available guides ({len(available_guides)}):", indent=2)
                    print_info(f"  Recommended for your project: {len(recommended_guides)}", indent=2)
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

                    response = input("  Select guides (all/recommended/none or numbers like 1,3,5) [default: recommended]: ").strip().lower()
                    if response == "all":
                        self.selected_guides = available_guides
                        print_success(f"✓ Selected all {len(available_guides)} guides", indent=2)
                    elif response == "" or response == "recommended":
                        self.selected_guides = recommended_guides
                        print_success(f"✓ Selected {len(recommended_guides)} recommended guides", indent=2)
                    elif response == "none":
                        self.selected_guides = []
                        print_info("✓ No guides selected", indent=2)
                    else:
                        # Parse number selection (e.g., "1,3,5")
                        try:
                            indices = [int(x.strip()) - 1 for x in response.split(",")]
                            self.selected_guides = [
                                available_guides[i] for i in indices
                                if 0 <= i < len(available_guides)
                            ]
                            print_success(f"✓ Selected {len(self.selected_guides)} guides", indent=2)
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
                    print_info("  Custom agents are advanced - select only if you created them", indent=2)
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
                    print_info("Tip: Create custom agents using templates in ~/.cco/agents/", indent=2)
                    print()

                # Skills selection with workflow-based recommendations
                available_skills = get_available_skills()
                if available_skills:
                    # Recommend skills based on project workflow needs
                    recommended_skills = self._recommend_skills_for_project()

                    # Skill descriptions
                    skill_descriptions = {
                        "verification-protocol": "Evidence-based fix-verify-commit loop (P067)",
                        "test-first-verification": "Generate tests before code changes (P035)",
                        "root-cause-analysis": "Analyze WHY violations exist, not just WHERE",
                        "incremental-improvement": "Break large tasks into achievable milestones",
                        "security-emergency-response": "Immediate P0 CRITICAL security remediation",
                    }

                    print_info(f"Available workflow skills ({len(available_skills)}):", indent=2)
                    print_info(f"  Recommended for your project: {len(recommended_skills)}", indent=2)
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

                    response = input("  Select skills (all/recommended/none) [default: recommended]: ").strip().lower()
                    if response == "all":
                        self.selected_skills = [s for s in available_skills if not s.startswith("_") and s != "README"]
                        print_success(f"✓ Selected all {len(self.selected_skills)} skills", indent=2)
                    elif response == "" or response == "recommended":
                        self.selected_skills = recommended_skills
                        print_success(f"✓ Selected {len(recommended_skills)} recommended skills", indent=2)
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
            # Create .claude directory structure
            (self.project_root / ".claude" / "commands").mkdir(parents=True, exist_ok=True)

            # Write project.json to .claude directory
            self._write_project_config()
            print_success("✓ Created .claude/project.json", indent=2)

            # Setup knowledge base symlinks
            self._setup_knowledge_symlinks()
            print_success("✓ Created knowledge base symlinks", indent=2)

            # Update .gitignore for symlinks
            self._update_gitignore()
            print_success("✓ Updated .gitignore", indent=2)

            # Generate settings.json
            self._generate_settings()
            print_success("✓ Created .claude/settings.json", indent=2)

            # Copy statusline.js template
            self._copy_statusline()
            print_success("✓ Copied .claude/statusline.js", indent=2)

            # Generate CLAUDE.md
            self._generate_claude_md()
            print_success("✓ Created CLAUDE.md", indent=2)

            # Generate .editorconfig (if not exists)
            if not (self.project_root / ".editorconfig").exists():
                self._generate_editorconfig()
                print_success("✓ Created .editorconfig", indent=2)

            # Generate .pre-commit-config.yaml (if precommit hooks selected)
            if self.answer_context and self.answer_context.has_answer("precommit_hooks"):
                hooks = self.answer_context.get("precommit_hooks", [])
                if hooks:
                    self._generate_precommit_config(hooks)
                    print_success("✓ Created .pre-commit-config.yaml", indent=2)

            # Generate .github/workflows/ci.yml (if GitHub Actions selected)
            if self.answer_context and self.answer_context.has_answer("ci_provider"):
                ci_provider = self.answer_context.get("ci_provider")
                if ci_provider == "github_actions":
                    self._generate_github_actions_workflow()
                    print_success("✓ Created .github/workflows/ci.yml", indent=2)
                elif ci_provider == "gitlab_ci":
                    self._generate_gitlab_ci()
                    print_success("✓ Created .gitlab-ci.yml", indent=2)

            # Generate .github/pull_request_template.md (if team project)
            if self.answer_context and self.answer_context.has_answer("team_dynamics"):
                team_dynamics = self.answer_context.get("team_dynamics", "solo")
                if team_dynamics != "solo":
                    self._generate_pr_template()
                    print_success("✓ Created .github/pull_request_template.md", indent=2)

            # Generate .github/CODEOWNERS (if team project)
            if self.answer_context and self.answer_context.has_answer("team_dynamics"):
                team_dynamics = self.answer_context.get("team_dynamics", "solo")
                if team_dynamics != "solo":
                    self._generate_codeowners()
                    print_success("✓ Created .github/CODEOWNERS", indent=2)

            # Generate .vscode/settings.json (always, if not exists)
            if not (self.project_root / ".vscode" / "settings.json").exists():
                self._generate_vscode_settings()
                print_success("✓ Created .vscode/settings.json", indent=2)

            # Generate .env.template (if secrets_management selected)
            if self.answer_context and self.answer_context.has_answer("secrets_management"):
                self._generate_env_template()
                if (self.project_root / ".env.template").exists():
                    print_success("✓ Created .env.template", indent=2)

            # Generate logging configuration (if logging_level selected)
            if self.answer_context and self.answer_context.has_answer("logging_level"):
                self._generate_logging_config()
                if (self.project_root / "logging.yaml").exists() or (self.project_root / "logger.config.js").exists():
                    print_success("✓ Created logging configuration", indent=2)

            print()
            return True

        except Exception as e:
            print_error(f"File generation failed: {e}", indent=2)
            return False

    def _write_project_config(self) -> None:
        """Write .claude/project.json (NEW ARCHITECTURE v3.1)"""
        # NEW: Write to .claude/project.json instead of .cco/project.json
        config_path = self.project_root / ".claude" / "project.json"

        from .. import __version__
        from ..schemas.project_config import ProjectConfig, DetectionInfo

        # Build detection info
        detection_info = DetectionInfo(
            project_type=getattr(self.system_context, 'detected_language', 'unknown') if self.system_context else 'unknown',
            languages=getattr(self.system_context, 'languages', []) if self.system_context else [],
            frameworks=[],
            team_size="solo",
            maturity="development",
            security_level="standard",
            philosophy="balanced"
        )

        # Build project config
        project_config = ProjectConfig(
            project_name=self.project_root.name,
            project_root=str(self.project_root),
            initialized_at=datetime.now().isoformat(),
            wizard_mode=self.mode,
            cco_version=__version__,
            detection=detection_info,
            selected_principles=self._build_selected_principles_dict(),
            command_overrides={},
            selected_commands=self.selected_commands,
            selected_guides=self.selected_guides if hasattr(self, 'selected_guides') else [],
            selected_skills=self.selected_skills if hasattr(self, 'selected_skills') else [],
            selected_agents=self.selected_agents if hasattr(self, 'selected_agents') else [],
            preferences={}
        )

        # Save to .claude/project.json
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(project_config.model_dump(), f, indent=2)


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
        """
        import os
        import platform
        from .. import config as CCOConfig
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

        # Get global knowledge directories
        global_commands_dir = CCOConfig.get_global_commands_dir()
        global_guides_dir = CCOConfig.get_guides_dir()
        global_principles_dir = CCOConfig.get_principles_dir()
        global_agents_dir = CCOConfig.get_agents_dir()
        global_skills_dir = CCOConfig.get_skills_dir()

        # Map selected items to their source directories
        symlink_map = []

        # Commands
        for cmd in self.selected_commands:
            source = global_commands_dir / f"{cmd}.md"
            target = claude_dir / "commands" / f"{cmd}.md"
            symlink_map.append((source, target))

        # Guides
        for guide in self.selected_guides:
            source = global_guides_dir / f"{guide}.md"
            target = claude_dir / "guides" / f"{guide}.md"
            symlink_map.append((source, target))

        # Principles
        # FIRST: Always symlink ALL universal principles (U001-U012)
        for u_num in range(1, 13):  # U001 through U012
            u_id = f"U{u_num:03d}"
            source = global_principles_dir / f"{u_id}.md"
            target = claude_dir / "principles" / f"{u_id}.md"
            if source.exists():
                symlink_map.append((source, target))

        # SECOND: Symlink only AI-selected project-specific principles (P001-P069)
        for principle in self.selected_principles:
            # Skip if it's a universal principle (already linked above)
            if not principle.startswith('U'):
                source = global_principles_dir / f"{principle}.md"
                target = claude_dir / "principles" / f"{principle}.md"
                symlink_map.append((source, target))

        # Agents (if any selected)
        if hasattr(self, 'selected_agents'):
            for agent in self.selected_agents:
                source = global_agents_dir / f"{agent}.md"
                target = claude_dir / "agents" / f"{agent}.md"
                symlink_map.append((source, target))

        # Skills (if any selected)
        if hasattr(self, 'selected_skills'):
            for skill in self.selected_skills:
                source = global_skills_dir / f"{skill}.md"
                target = claude_dir / "skills" / f"{skill}.md"
                symlink_map.append((source, target))

        # Create symlinks
        for source, target in symlink_map:
            # Ensure parent directory exists (for language-specific skills like python/*)
            target.parent.mkdir(parents=True, exist_ok=True)

            # Remove existing symlink/file if exists
            if target.exists() or target.is_symlink():
                target.unlink()

            # Create symlink (cross-platform)
            if platform.system() == "Windows":
                # Windows: use mklink
                import subprocess
                subprocess.run(
                    ["cmd", "/c", "mklink", str(target), str(source)],
                    check=True,
                    capture_output=True
                )
            else:
                # Unix: use symlink_to
                target.symlink_to(source)

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

    def _generate_settings(self) -> None:
        """Generate .claude/settings.json from global template"""
        import json
        from pathlib import Path

        from .. import config as CCOConfig  # noqa: N812

        # Try to load from global templates first, fallback to package assets
        templates_dir = CCOConfig.get_templates_dir()
        template_path = templates_dir / "settings.json.template"

        if not template_path.exists():
            # Fallback to package assets
            package_root = Path(__file__).parent.parent
            template_path = package_root / "assets" / "settings.json.template"

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

        # Check if .claude/settings.json already exists
        settings_path = self.project_root / ".claude" / "settings.json"

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
        """Generate CLAUDE.md using ClaudeMdGenerator with full principle injection"""
        from ..core.claude_md_generator import ClaudeMdGenerator

        # Build preferences dict with selected principles
        preferences_dict = {
            "project_identity": {
                "name": self.project_root.name,
                "team_trajectory": self.answer_context.get("team_dynamics", "solo") if self.answer_context else "solo",
            },
            "code_quality": {
                "linting_strictness": "strict",  # Default
            },
            "testing": {
                "strategy": "balanced",  # Default
            },
            "selected_principle_ids": self.selected_principles if self.selected_principles else []
        }

        # Generate CLAUDE.md
        output_path = self.project_root / "CLAUDE.md"
        generator = ClaudeMdGenerator(
            preferences_dict,
            selected_skills=self.selected_skills if hasattr(self, 'selected_skills') else [],
            selected_agents=self.selected_agents if hasattr(self, 'selected_agents') else [],
        )
        generator.generate(output_path)

    def _build_selected_principles_dict(self) -> Dict[str, List[str]]:
        """Build selected principles dictionary by category."""
        import json
        from pathlib import Path

        # Load all principles to get universal count dynamically
        principles_json = Path(__file__).parent.parent.parent / "content" / "principles.json"
        with open(principles_json, encoding="utf-8") as f:
            data = json.load(f)

        # Get all universal principles dynamically
        universal_ids = [p["id"] for p in data.get("principles", [])
                        if p.get("category") == "universal"]

        principles_dict = {
            "universal": universal_ids
        }

        # Group project-specific principles by category
        if self.selected_principles:
            # Categorize based on actual category from principles.json
            all_principles = {p["id"]: p for p in data.get("principles", [])}

            for pid in self.selected_principles:
                if pid.startswith('U'):  # Skip universal (already added)
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
                additions.append("**Defensive Programming**: Validate all inputs, check all assumptions, fail gracefully.\n")
                additions.append("- Validate all function inputs at entry points")
                additions.append("- Use type hints and runtime type checking")
                additions.append("- Provide helpful error messages with context")
                additions.append("- Log errors with full stack traces")
            elif error_handling == "fail_fast":
                additions.append("**Fail-Fast**: Errors cause immediate visible failure. No silent fallbacks.\n")
                additions.append("- Never swallow exceptions without re-raising")
                additions.append("- Fail immediately on invalid state")
                additions.append("- Use assertions for invariants")
                additions.append("- See P001: Fail-Fast Error Handling in CLAUDE.md")
            elif error_handling == "exception_hierarchy":
                additions.append("**Exception Hierarchy**: Custom exception types for different error categories.\n")
                additions.append("- Define custom exception classes per domain")
                additions.append("- Catch specific exceptions, not generic Exception")
                additions.append("- Include error context in exception data")
                additions.append("- Document which exceptions each function can raise")
            elif error_handling == "result_types":
                additions.append("**Result Types**: Use Result/Option types instead of exceptions for expected failures.\n")
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
        if hasattr(self, 'selected_agents') and self.selected_agents:
            additions.append("\n### Agents (Project Selected)\n")
            additions.append("Use these specialized agents for complex tasks:\n")
            for agent in self.selected_agents:
                agent_name = agent.replace("-", " ").title()
                additions.append(f"- **@.claude/agents/{agent}.md** - {agent_name}")

        # Skills
        if hasattr(self, 'selected_skills') and self.selected_skills:
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
                    footer_marker,
                    "\n\n" + "\n".join(additions) + footer_marker
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

        # Count major files created (CLAUDE.md, settings.json, project.json, statusline.js, .gitignore update)
        files_count = 3  # CLAUDE.md, settings.json, project.json
        if (self.project_root / ".claude" / "statusline.js").exists():
            files_count += 1
        if (self.project_root / ".gitignore").exists():
            files_count += 1  # Modified .gitignore

        display_completion_summary(
            commands_installed=len(self.selected_commands),
            principles_configured=len(self.selected_principles),
            files_created=files_count,
            duration_seconds=duration,
            guides_installed=len(self.selected_guides) if hasattr(self, 'selected_guides') else 0,
            skills_installed=len(self.selected_skills) if hasattr(self, 'selected_skills') else 0,
            agents_installed=len(self.selected_agents) if hasattr(self, 'selected_agents') else 0,
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

        answers = self.answer_context.answers

        # Get primary language from system context
        primary_language = (
            self.system_context.detected_language
            if self.system_context and hasattr(self.system_context, 'detected_language')
            else 'python'
        )

        # Map git_workflow values
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

        return {
            "project_identity": {
                "name": self.project_root.name,
                "types": answers.get("project_purpose", []),
                "primary_language": primary_language,
                "team_trajectory": answers.get("team_dynamics", "solo"),
                "project_maturity": answers.get("project_maturity", "active-dev"),
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
                "security_stance": security_mapping.get(
                    answers.get("security_stance", "standard"),
                    "balanced"
                ),
            },
            "documentation": {
                "verbosity": doc_mapping.get(
                    answers.get("documentation_level", "minimal"),
                    "minimal"
                ),
            },
            "code_quality": {
                "linting_strictness": self._map_strategy_to_strictness(
                    answers.get("principle_strategy", "recommended"),
                ),
            },
            "collaboration": {
                "git_workflow": git_workflow_mapping.get(
                    answers.get("git_workflow", "main_only"),
                    "trunk-based"
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
            recommended.append("verification-protocol")

        # For all team projects (non-solo)
        if team_size != "solo":
            recommended.append("verification-protocol")

        # Git Workflow Guide: for team projects with structured workflows
        if team_size in ["small_team", "growing_team", "large_org"]:
            recommended.append("git-workflow")

        # Also for git flow or github flow
        if git_workflow in ["git_flow", "github_flow"]:
            if "git-workflow" not in recommended:
                recommended.append("git-workflow")

        # TIER 2 Mappings: Strategy Decisions

        # Security Response: for production or high security stance
        if security in ["production", "high"] or maturity == "production":
            recommended.append("security-response")

        # For web/API projects (security critical)
        if any(pt in project_types for pt in ["api_service", "web_app", "microservice", "spa"]):
            if "security-response" not in recommended:
                recommended.append("security-response")

        # Performance Optimization: for backend services or data pipelines
        if any(pt in project_types for pt in ["api_service", "microservice", "data_pipeline", "ml_pipeline", "stream_processing"]):
            recommended.append("performance-optimization")

        # For projects that need retry/resilience
        if error_handling in ["retry_logic", "graceful_degradation"]:
            if "performance-optimization" not in recommended:
                recommended.append("performance-optimization")

        # Container Best Practices: for containerized infrastructure
        if any(pt in project_types for pt in ["microservice", "infrastructure", "data_pipeline", "ml_pipeline"]):
            recommended.append("container-best-practices")

        # TIER 3 Mappings: Tactical Decisions

        # Additional test-focused recommendations
        if testing in ["comprehensive", "balanced"]:
            if "verification-protocol" not in recommended:
                recommended.append("verification-protocol")

        return list(set(recommended))  # Remove duplicates

    def _recommend_skills_for_project(self) -> List[str]:
        """Add all universal skills + language-specific skills to project"""
        # Universal skills - always included in every project
        universal_skills = [
            "verification-protocol",
            "test-first-verification",
            "root-cause-analysis",
            "incremental-improvement",
            "security-emergency-response",
        ]

        # Language-specific skills - add if language detected
        language_specific_skills = []

        # Get detected languages from system context
        if self.system_context and hasattr(self.system_context, 'detected_languages'):
            detected_languages = self.system_context.detected_languages

            # Add language-specific skills
            if 'python' in [lang.lower() for lang in detected_languages]:
                language_specific_skills.extend([
                    "python/async-patterns",
                    "python/packaging-modern",
                    "python/performance",
                    "python/testing-pytest",
                    "python/type-hints-advanced",
                ])

            if 'go' in [lang.lower() for lang in detected_languages]:
                # Go-specific skills (when available)
                pass

            if 'rust' in [lang.lower() for lang in detected_languages]:
                # Rust-specific skills (when available)
                pass

            if any(lang.lower() in ['typescript', 'javascript'] for lang in detected_languages):
                # TypeScript/JS-specific skills (when available)
                pass

        return list(set(universal_skills + language_specific_skills))  # Remove duplicates

    def _recommend_agents_for_project(self) -> List[str]:
        """Add all universal agents to every project (always included)"""
        # Universal agents - always included in every project
        universal_agents = [
            "audit-agent",
            "fix-agent",
            "generate-agent",
        ]

        return universal_agents

    def _generate_editorconfig(self) -> None:
        """Generate .editorconfig from template"""
        from pathlib import Path

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / ".editorconfig.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Get line length from answers (default 88 for Python)
        line_length = "88"
        if self.answer_context:
            line_length = self.answer_context.get("line_length_preference", "88")

        # Get naming convention guidance
        naming_guide = ""
        if self.answer_context and self.answer_context.has_answer("naming_convention"):
            naming_conv = self.answer_context.get("naming_convention", "language_default")
            if naming_conv == "snake_case":
                naming_guide = "\n# Naming: Use snake_case for files and identifiers"
            elif naming_conv == "camelCase":
                naming_guide = "\n# Naming: Use camelCase for identifiers"
            elif naming_conv == "language_default":
                naming_guide = "\n# Naming: Follow language conventions (Python: snake_case, JS: camelCase)"

        # Replace template variables
        content = content.replace("${LINE_LENGTH}", str(line_length))

        # Add naming guidance as comment at the end
        if naming_guide:
            content += naming_guide

        # Write to project root
        output_path = self.project_root / ".editorconfig"
        output_path.write_text(content, encoding="utf-8")

    def _generate_precommit_config(self, hooks: List[str]) -> None:
        """Generate .pre-commit-config.yaml based on selected hooks"""

        # Get linting strictness from principle_strategy
        strictness = "strict"  # Default
        if self.answer_context and self.answer_context.has_answer("principle_strategy"):
            principle_strategy = self.answer_context.get("principle_strategy", "recommended")
            strictness = self._map_strategy_to_strictness(principle_strategy)

        # Configure ruff args based on strictness
        if strictness == "pedantic":
            ruff_args_format = "[--fix, --select=ALL]"
            ruff_args_lint = "[--select=ALL]"
        elif strictness == "strict":
            ruff_args_format = "[--fix]"
            ruff_args_lint = "[]"
        else:  # moderate
            ruff_args_format = "[--fix, --ignore=E501]"  # Ignore line length
            ruff_args_lint = "[--ignore=E501]"

        # Pre-commit hook configurations
        hook_configs = {
            "format": f"""  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: {ruff_args_format}""",
            "lint": f"""  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: {ruff_args_lint}""",
            "type_check": """  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]""",
            "secrets": """  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks""",
            "test": """  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true""",
        }

        # Build hooks section
        hooks_content = []
        for hook in hooks:
            if hook in hook_configs:
                hooks_content.append(hook_configs[hook])

        # Load template
        from pathlib import Path

        template_path = Path(__file__).parent.parent.parent / "templates" / ".pre-commit-config.yaml.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        hooks_str = "\n".join(hooks_content)
        content = content.replace("${HOOKS}", hooks_str)

        # Write to project root
        output_path = self.project_root / ".pre-commit-config.yaml"
        output_path.write_text(content, encoding="utf-8")

    def _generate_github_actions_workflow(self) -> None:
        """Generate .github/workflows/ci.yml based on project language and tools"""
        from pathlib import Path

        # Get project language
        primary_language = "python"  # Default
        if self.detection_report:
            primary_language = self.detection_report.get("detected_language", {}).get("primary", "python")

        # Get default branch
        default_branch = "main"
        if self.system_context and self.system_context.is_git_repo:
            # Try to detect default branch
            import subprocess
            try:
                result = subprocess.run(
                    ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    default_branch = result.stdout.strip().split("/")[-1]
            except Exception:
                pass  # Keep default

        # Language-specific configurations
        configs = self._get_language_ci_config(primary_language)

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / ".github-workflows-ci.yml.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        content = content.replace("${PRIMARY_LANGUAGE}", primary_language)
        content = content.replace("${DEFAULT_BRANCH}", default_branch)
        content = content.replace("${LINT_STEPS}", configs["lint_steps"])
        content = content.replace("${TYPE_CHECK_STEPS}", configs["type_check_steps"])
        content = content.replace("${TEST_MATRIX}", configs["test_matrix"])
        content = content.replace("${TEST_STEPS}", configs["test_steps"])
        content = content.replace("${SECURITY_STEPS}", configs["security_steps"])

        # Create .github/workflows directory
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Write workflow file
        output_path = workflows_dir / "ci.yml"
        output_path.write_text(content, encoding="utf-8")

    def _get_language_ci_config(self, language: str) -> dict:
        """Get CI configuration steps for a specific language"""
        # Get package manager from answer context
        package_manager = "pip"  # Default
        if self.answer_context and self.answer_context.has_answer("package_manager"):
            package_manager = self.answer_context.get("package_manager", "pip")

        # Generate Python install commands based on package manager
        if language.lower() == "python":
            if package_manager == "poetry":
                lint_install = "poetry install"
                type_install = "poetry install"
                test_install = "poetry install"
            elif package_manager == "pdm":
                lint_install = "pdm install"
                type_install = "pdm install"
                test_install = "pdm install"
            else:  # pip
                lint_install = "python -m pip install --upgrade pip\n          pip install ruff"
                type_install = "python -m pip install --upgrade pip\n          pip install -e \".[dev]\""
                test_install = "python -m pip install --upgrade pip\n          pip install -e \".[dev]\""

        # Generate JavaScript/TypeScript install commands based on package manager
        js_install = "npm ci"  # default
        if language.lower() in ["javascript", "typescript"]:
            if package_manager == "yarn":
                js_install = "yarn install"
            elif package_manager == "pnpm":
                js_install = "pnpm install"
            else:  # npm
                js_install = "npm ci"

        configs = {
            "python": {
                "lint_steps": f"""      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: {lint_install}
      - name: Run Ruff lint
        run: ruff check .
      - name: Run Ruff format check
        run: ruff format --check .""",
                "type_check_steps": f"""      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          {type_install}
      - name: Run mypy
        run: mypy --strict .""",
                "test_matrix": """        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']""",
                "test_steps": f"""      - uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - name: Install dependencies
        run: |
          {test_install}
      - name: Run tests
        run: pytest tests/ --cov --cov-report=xml
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        uses: codecov/codecov-action@v3""",
                "security_steps": """      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
            },
            "javascript": {
                "lint_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: {js_install}
      - name: Run ESLint
        run: npm run lint""",
                "type_check_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: {js_install}
      - name: Type check
        run: npm run type-check""",
                "test_matrix": """        node-version: ['18', '20', '21']""",
                "test_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: ${{{{ matrix.node-version }}}}
      - name: Install dependencies
        run: {js_install}
      - name: Run tests
        run: npm test -- --coverage
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node-version == '20'
        uses: codecov/codecov-action@v3""",
                "security_steps": """      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Run npm audit
        run: npm audit
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
            },
            "typescript": {
                "lint_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: {js_install}
      - name: Run ESLint
        run: npm run lint""",
                "type_check_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: {js_install}
      - name: Type check
        run: npm run type-check || tsc --noEmit""",
                "test_matrix": """        node-version: ['18', '20', '21']""",
                "test_steps": f"""      - uses: actions/setup-node@v4
        with:
          node-version: ${{{{ matrix.node-version }}}}
      - name: Install dependencies
        run: {js_install}
      - name: Run tests
        run: npm test -- --coverage
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node-version == '20'
        uses: codecov/codecov-action@v3""",
                "security_steps": """      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Run npm audit
        run: npm audit
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
            },
            "go": {
                "lint_steps": """      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'
      - name: Run golangci-lint
        uses: golangci/golangci-lint-action@v3
        with:
          version: latest""",
                "type_check_steps": """      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'
      - name: Type check (go vet)
        run: go vet ./...""",
                "test_matrix": """        go-version: ['1.20', '1.21', '1.22']""",
                "test_steps": """      - uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go-version }}
      - name: Run tests
        run: go test -v -race -coverprofile=coverage.txt -covermode=atomic ./...
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.go-version == '1.21'
        uses: codecov/codecov-action@v3""",
                "security_steps": """      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'
      - name: Run gosec
        uses: securego/gosec@master
        with:
          args: './...'
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
            },
            "rust": {
                "lint_steps": """      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          components: rustfmt, clippy
      - name: Run rustfmt
        run: cargo fmt -- --check
      - name: Run clippy
        run: cargo clippy -- -D warnings""",
                "type_check_steps": """      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      - name: Type check (cargo check)
        run: cargo check --all-features""",
                "test_matrix": """        rust-version: ['stable', 'beta']""",
                "test_steps": """      - uses: actions-rs/toolchain@v1
        with:
          toolchain: ${{ matrix.rust-version }}
      - name: Run tests
        run: cargo test --all-features
      - name: Generate coverage
        if: matrix.os == 'ubuntu-latest' && matrix.rust-version == 'stable'
        run: |
          cargo install cargo-tarpaulin
          cargo tarpaulin --out Xml
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.rust-version == 'stable'
        uses: codecov/codecov-action@v3""",
                "security_steps": """      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      - name: Run cargo audit
        uses: actions-rs/audit-check@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
            }
        }

        # Default to python if language not found
        return configs.get(language.lower(), configs["python"])



    def _generate_pr_template(self) -> None:
        """Generate .github/pull_request_template.md for team projects"""
        from pathlib import Path

        # Get testing and documentation requirements
        testing_checklist = ""
        if self.answer_context and self.answer_context.has_answer("testing_approach"):
            testing_approach = self.answer_context.get("testing_approach", "critical_paths")
            # testing_approach is a single value: no_tests, critical_paths, balanced, comprehensive
            if testing_approach in ["balanced", "comprehensive"]:
                testing_checklist += "\n- [ ] Unit test coverage >= 80%"
                testing_checklist += "\n- [ ] Integration tests added"
            if testing_approach == "comprehensive":
                testing_checklist += "\n- [ ] E2E tests added"
            elif testing_approach == "critical_paths":
                testing_checklist += "\n- [ ] Critical path tests added"

        documentation_checklist = ""
        review_checklist = ""

        # Use documentation_strategy answer
        if self.answer_context and self.answer_context.has_answer("documentation_strategy"):
            doc_strategy = self.answer_context.get("documentation_strategy", "standard")
            if doc_strategy in ["standard", "comprehensive"]:
                documentation_checklist += "\n- [ ] Code comments added for complex logic"
                documentation_checklist += "\n- [ ] README updated if needed"
            if doc_strategy == "comprehensive":
                documentation_checklist += "\n- [ ] Architecture documentation updated"
                documentation_checklist += "\n- [ ] API documentation generated"

        # Use code_review_requirements answer
        if self.answer_context and self.answer_context.has_answer("code_review_requirements"):
            review_req = self.answer_context.get("code_review_requirements", "optional")
            if review_req == "required_one":
                review_checklist += "\n- [ ] At least 1 reviewer approval required"
            elif review_req == "required_two":
                review_checklist += "\n- [ ] At least 2 reviewer approvals required"
                review_checklist += "\n- [ ] All review comments addressed"

        # Use branch_naming_convention answer
        if self.answer_context and self.answer_context.has_answer("branch_naming_convention"):
            branch_naming = self.answer_context.get("branch_naming_convention", "conventional")
            if branch_naming == "conventional":
                review_checklist += "\n- [ ] Branch follows naming convention (feature/*, bugfix/*, hotfix/*)"
            elif branch_naming == "ticket_based":
                review_checklist += "\n- [ ] Branch name includes ticket number"

        # For API projects, add specific checks
        project_types = self.answer_context.get("project_purpose", []) if self.answer_context else []
        if any(pt in project_types for pt in ["api_service", "web_app", "microservice"]):
            documentation_checklist += "\n- [ ] API endpoints documented"
            review_checklist += "\n- [ ] Rate limiting considered"

            # Use auth_pattern answer if available
            if self.answer_context and self.answer_context.has_answer("auth_pattern"):
                auth_pattern = self.answer_context.get("auth_pattern", "jwt")
                review_checklist += f"\n- [ ] {auth_pattern.upper()} authentication/authorization verified"
            else:
                review_checklist += "\n- [ ] Authentication/authorization verified"

            # Use api_docs_tool answer if available
            if self.answer_context and self.answer_context.has_answer("api_docs_tool"):
                api_docs = self.answer_context.get("api_docs_tool", "openapi")
                if api_docs != "none":
                    documentation_checklist += f"\n- [ ] {api_docs.replace('_', ' ').title()} documentation updated"

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / "pull_request_template.md.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        content = content.replace("${TESTING_CHECKLIST}", testing_checklist)
        content = content.replace("${DOCUMENTATION_CHECKLIST}", documentation_checklist)
        content = content.replace("${REVIEW_CHECKLIST}", review_checklist)

        # Create .github directory
        github_dir = self.project_root / ".github"
        github_dir.mkdir(parents=True, exist_ok=True)

        # Write PR template file
        output_path = github_dir / "pull_request_template.md"
        output_path.write_text(content, encoding="utf-8")

    def _generate_codeowners(self) -> None:
        """Generate .github/CODEOWNERS for team projects"""
        from pathlib import Path

        # Determine team structure from answers
        team_dynamics = self.answer_context.get("team_dynamics", "solo") if self.answer_context else "solo"

        # Generate ownership patterns based on project structure
        global_owners = "@team-leads"
        component_ownership = ""
        doc_owners = "@docs-team"
        devops_owners = "@devops-team"
        security_owners = "@security-team"

        # For small teams, simplify
        if team_dynamics == "small_team":
            global_owners = "@core-team"
            doc_owners = "@core-team"
            devops_owners = "@core-team"
            security_owners = "@core-team"

        # Add component-specific ownership based on project type
        project_types = self.answer_context.get("project_purpose", []) if self.answer_context else []
        if "api_service" in project_types or "web_app" in project_types:
            component_ownership = """
# API/Backend
/api/ @backend-team
/src/api/ @backend-team

# Frontend
/frontend/ @frontend-team
/src/components/ @frontend-team
"""
        elif "data_pipeline" in project_types or "ml_system" in project_types:
            component_ownership = """
# Data pipelines
/pipelines/ @data-team
/etl/ @data-team

# ML models
/models/ @ml-team
"""

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / "CODEOWNERS.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        content = content.replace("${GLOBAL_OWNERS}", global_owners)
        content = content.replace("${COMPONENT_OWNERSHIP}", component_ownership.strip())
        content = content.replace("${DOC_OWNERS}", doc_owners)
        content = content.replace("${DEVOPS_OWNERS}", devops_owners)
        content = content.replace("${SECURITY_OWNERS}", security_owners)

        # Create .github directory
        github_dir = self.project_root / ".github"
        github_dir.mkdir(parents=True, exist_ok=True)

        # Write CODEOWNERS file
        output_path = github_dir / "CODEOWNERS"
        output_path.write_text(content, encoding="utf-8")

    def _generate_vscode_settings(self) -> None:
        """Generate .vscode/settings.json with language-specific configurations"""
        from pathlib import Path

        # Get line length from answers or use default
        line_length = 88
        if self.answer_context:
            line_length = int(self.answer_context.get("line_length_preference", "88"))

        # Get primary language
        primary_language = "python"
        if self.detection_report:
            primary_language = self.detection_report.get("detected_language", {}).get("primary", "python")

        # Language-specific settings
        language_settings_map = {
            "python": """
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true,
      "source.fixAll": true
    }
  },
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "none",
  "python.analysis.typeCheckingMode": "basic",""",
            "typescript": """
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true,
      "source.fixAll.eslint": true
    }
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,""",
            "javascript": """
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": true
    }
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },""",
            "go": """
  "[go]": {
    "editor.defaultFormatter": "golang.go",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "go.useLanguageServer": true,
  "go.lintTool": "golangci-lint",
  "go.lintOnSave": "package",""",
            "rust": """
  "[rust]": {
    "editor.defaultFormatter": "rust-lang.rust-analyzer",
    "editor.formatOnSave": true
  },
  "rust-analyzer.check.command": "clippy",
  "rust-analyzer.checkOnSave.allTargets": true,"""
        }

        language_settings = language_settings_map.get(primary_language.lower(), language_settings_map["python"])

        # Testing settings
        testing_settings = ""
        if primary_language == "python":
            testing_settings = """
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],"""
        elif primary_language in ["typescript", "javascript"]:
            testing_settings = """
  "jest.autoRun": "off",
  "jest.showCoverageOnLoad": false,"""

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / ".vscode-settings.json.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        content = content.replace("${LINE_LENGTH}", str(line_length))
        content = content.replace("${LANGUAGE_SETTINGS}", language_settings)
        content = content.replace("${TESTING_SETTINGS}", testing_settings)

        # Create .vscode directory
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(parents=True, exist_ok=True)

        # Write settings file
        output_path = vscode_dir / "settings.json"
        output_path.write_text(content, encoding="utf-8")
    def _generate_gitlab_ci(self) -> None:
        """Generate .gitlab-ci.yml based on project language and tools"""
        from pathlib import Path

        # Get project language
        primary_language = "python"
        if self.detection_report:
            primary_language = self.detection_report.get("detected_language", {}).get("primary", "python")

        # Get default branch
        default_branch = "main"
        if self.system_context and self.system_context.is_git_repo:
            import subprocess
            try:
                result = subprocess.run(
                    ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    default_branch = result.stdout.strip().split("/")[-1]
            except Exception:
                pass

        # Language-specific configurations
        configs = self._get_language_gitlab_config(primary_language)

        # Load template
        template_path = Path(__file__).parent.parent.parent / "templates" / ".gitlab-ci.yml.template"
        if not template_path.exists():
            return

        content = template_path.read_text(encoding="utf-8")

        # Replace template variables
        content = content.replace("${PRIMARY_LANGUAGE}", primary_language)
        content = content.replace("${DEFAULT_BRANCH}", default_branch)
        content = content.replace("${CACHE_VARIABLES}", configs["cache_variables"])
        content = content.replace("${CACHE_PATHS}", configs["cache_paths"])
        content = content.replace("${LINT_JOB}", configs["lint_job"])
        content = content.replace("${TYPE_CHECK_JOB}", configs["type_check_job"])
        content = content.replace("${TEST_JOB}", configs["test_job"])
        content = content.replace("${SECURITY_JOB}", configs["security_job"])

        # Write GitLab CI file
        output_path = self.project_root / ".gitlab-ci.yml"
        output_path.write_text(content, encoding="utf-8")

    def _get_language_gitlab_config(self, language: str) -> dict:
        """Get GitLab CI configuration for a specific language"""

        # Get package manager from answer context
        package_manager = "pip"  # Default
        if self.answer_context and self.answer_context.has_answer("package_manager"):
            package_manager = self.answer_context.get("package_manager", "pip")

        # Generate install commands based on package manager
        if language.lower() == "python":
            if package_manager == "poetry":
                py_install = "poetry install"
            elif package_manager == "pdm":
                py_install = "pdm install"
            else:
                py_install = "pip install -e \".[dev]\""

        if language.lower() in ["javascript", "typescript"]:
            if package_manager == "yarn":
                js_install = "yarn install"
            elif package_manager == "pnpm":
                js_install = "pnpm install"
            else:
                js_install = "npm ci"

        # Simplified configs for GitLab CI
        python_cfg = {
            "cache_variables": 'PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"',
            "cache_paths": "paths:\n    - .cache/pip\n    - .venv/",
            "lint_job": "image: python:3.12\n  before_script:\n    - pip install ruff\n  script:\n    - ruff check .\n    - ruff format --check .\n  only:\n    - merge_requests\n    - main",
            "type_check_job": f"image: python:3.12\n  before_script:\n    - {py_install}\n  script:\n    - mypy --strict .\n  only:\n    - merge_requests\n    - main",
            "test_job": f"image: python:3.12\n  before_script:\n    - {py_install}\n  script:\n    - pytest tests/ --cov\n  only:\n    - merge_requests\n    - main",
            "security_job": "image: python:3.12\n  script:\n    - echo 'Security scanning placeholder'\n  allow_failure: true\n  only:\n    - merge_requests\n    - main"
        }

        ts_cfg = {
            "cache_variables": 'NPM_CONFIG_CACHE: "$CI_PROJECT_DIR/.npm"',
            "cache_paths": "paths:\n    - .npm\n    - node_modules/",
            "lint_job": f"image: node:20\n  before_script:\n    - {js_install}\n  script:\n    - npm run lint\n  only:\n    - merge_requests\n    - main",
            "type_check_job": f"image: node:20\n  before_script:\n    - {js_install}\n  script:\n    - npm run type-check\n  only:\n    - merge_requests\n    - main",
            "test_job": f"image: node:20\n  before_script:\n    - {js_install}\n  script:\n    - npm test -- --coverage\n  only:\n    - merge_requests\n    - main",
            "security_job": f"image: node:20\n  before_script:\n    - {js_install}\n  script:\n    - npm audit\n  allow_failure: true\n  only:\n    - merge_requests\n    - main"
        }
        
        go_cfg = {
            "cache_variables": 'GOPATH: "$CI_PROJECT_DIR/.go"',
            "cache_paths": "paths:\n    - .go/pkg/mod/",
            "lint_job": "image: golangci/golangci-lint:v1.55\n  script:\n    - golangci-lint run ./...\n  only:\n    - merge_requests\n    - main",
            "type_check_job": "image: golang:1.21\n  script:\n    - go vet ./...\n  only:\n    - merge_requests\n    - main",
            "test_job": "image: golang:1.21\n  script:\n    - go test -v ./...\n  only:\n    - merge_requests\n    - main",
            "security_job": "image: golang:1.21\n  script:\n    - echo 'Security scanning placeholder'\n  allow_failure: true\n  only:\n    - merge_requests\n    - main"
        }
        
        rust_cfg = {
            "cache_variables": 'CARGO_HOME: "$CI_PROJECT_DIR/.cargo"',
            "cache_paths": "paths:\n    - .cargo\n    - target/",
            "lint_job": "image: rust:latest\n  before_script:\n    - rustup component add clippy\n  script:\n    - cargo clippy\n  only:\n    - merge_requests\n    - main",
            "type_check_job": "image: rust:latest\n  script:\n    - cargo check\n  only:\n    - merge_requests\n    - main",
            "test_job": "image: rust:latest\n  script:\n    - cargo test\n  only:\n    - merge_requests\n    - main",
            "security_job": "image: rust:latest\n  script:\n    - echo 'Security scanning placeholder'\n  allow_failure: true\n  only:\n    - merge_requests\n    - main"
        }
        
        configs = {
            "python": python_cfg,
            "typescript": ts_cfg,
            "javascript": ts_cfg,
            "go": go_cfg,
            "rust": rust_cfg
        }
        
        return configs.get(language.lower(), python_cfg)

    def _generate_env_template(self) -> None:
        """Generate .env.template for secrets management"""
        from pathlib import Path

        # Only generate if secrets_management answer exists
        if not self.answer_context or not self.answer_context.has_answer("secrets_management"):
            return

        secrets_mgmt = self.answer_context.get("secrets_management", "env_files")

        # Only generate for env_files strategy
        if secrets_mgmt != "env_files":
            return

        # Check if template already exists
        env_template_path = self.project_root / ".env.template"
        if env_template_path.exists():
            return

        # Generate basic .env.template based on project type
        project_types = self.answer_context.get("project_purpose", []) if self.answer_context else []

        content_lines = [
            "# Environment Variables Template",
            "# Copy this file to .env and fill in your values",
            "# .env is in .gitignore and should never be committed",
            "",
        ]

        # Add common variables
        content_lines.extend([
            "# Application",
            "# APP_ENV=development",
            "# DEBUG=true",
            "",
        ])

        # Add API-specific variables
        if any(pt in project_types for pt in ["api_service", "web_app", "microservice"]):
            content_lines.extend([
                "# API Configuration",
                "# API_KEY=your_api_key_here",
                "# API_SECRET=your_api_secret_here",
                "",
            ])

            # Add auth-specific variables based on auth_pattern
            if self.answer_context.has_answer("auth_pattern"):
                auth_pattern = self.answer_context.get("auth_pattern", "jwt")
                if auth_pattern == "jwt":
                    content_lines.extend([
                        "# JWT Authentication",
                        "# JWT_SECRET=your_jwt_secret_here",
                        "# JWT_EXPIRATION=3600",
                        "",
                    ])
                elif auth_pattern == "oauth":
                    content_lines.extend([
                        "# OAuth Configuration",
                        "# OAUTH_CLIENT_ID=your_client_id",
                        "# OAUTH_CLIENT_SECRET=your_client_secret",
                        "# OAUTH_CALLBACK_URL=http://localhost:3000/auth/callback",
                        "",
                    ])

        # Add database variables for data-heavy projects
        if any(pt in project_types for pt in ["data_pipeline", "web_app", "api_service"]):
            content_lines.extend([
                "# Database",
                "# DATABASE_URL=postgresql://user:password@localhost:5432/dbname",
                "",
            ])

        # Write file
        env_template_path.write_text("\n".join(content_lines), encoding="utf-8")

        # Also update .gitignore to include .env
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text(encoding="utf-8")
            if ".env" not in gitignore_content:
                gitignore_path.write_text(gitignore_content + "\n# Environment variables\n.env\n", encoding="utf-8")

    def _generate_logging_config(self) -> None:
        """Generate logging configuration file based on logging_level answer"""
        from pathlib import Path

        # Only generate if logging_level answer exists
        if not self.answer_context or not self.answer_context.has_answer("logging_level"):
            return

        logging_level = self.answer_context.get("logging_level", "INFO")

        # Get primary language
        primary_language = "python"
        if self.detection_report:
            primary_language = self.detection_report.get("detected_language", {}).get("primary", "python")

        # Generate language-specific logging config
        if primary_language == "python":
            # Generate logging.yaml or logging.json
            config_path = self.project_root / "logging.yaml"
            if config_path.exists():
                return

            content = f"""# Logging Configuration
version: 1
disable_existing_loggers: false

formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: {logging_level}
    formatter: default
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: {logging_level}
    formatter: detailed
    filename: app.log
    maxBytes: 10485760  # 10MB
    backupCount: 3

root:
  level: {logging_level}
  handlers: [console, file]

loggers:
  __main__:
    level: {logging_level}
    handlers: [console, file]
    propagate: false
"""
            config_path.write_text(content, encoding="utf-8")

        elif primary_language in ["javascript", "typescript"]:
            # Generate winston or pino config
            config_path = self.project_root / "logger.config.js"
            if config_path.exists():
                return

            level_map = {"DEBUG": "debug", "INFO": "info", "WARNING": "warn", "ERROR": "error"}
            js_level = level_map.get(logging_level, "info")

            content = f"""// Logging Configuration
const winston = require('winston');

const logger = winston.createLogger({{
  level: '{js_level}',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({{ stack: true }}),
    winston.format.splat(),
    winston.format.json()
  ),
  defaultMeta: {{ service: 'app' }},
  transports: [
    new winston.transports.Console({{
      format: winston.format.simple(),
    }}),
    new winston.transports.File({{
      filename: 'error.log',
      level: 'error'
    }}),
    new winston.transports.File({{
      filename: 'combined.log'
    }})
  ]
}});

module.exports = logger;
"""
            config_path.write_text(content, encoding="utf-8")


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
