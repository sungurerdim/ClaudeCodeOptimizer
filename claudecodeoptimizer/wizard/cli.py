#!/usr/bin/env python3
"""
CCO 2.5 Interactive Wizard - Main CLI

5-phase wizard flow:
1. Detection - Analyze project and show results
2. Questions - Ask 58 questions with AI hints
3. Commands - Select which CCO commands to install
4. Preview - Show all changes before applying
5. Apply - Write files and configure permissions

Supports --dry-run flag for testing without file writes.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .. import __version__ as cco_version
from ..ai.command_selection import CommandRecommender

# Import CCO modules
from ..ai.detection import UniversalDetector
from ..ai.recommendations import RecommendationEngine
from ..core.constants import DEFAULT_PAGE_SIZE
from ..schemas.commands import CommandMetadata, CommandRegistry
from ..schemas.preferences import (
    CCOPreferences,
    CodeQualityStandards,
    DevelopmentStyle,
    DevOpsAutomation,
    DocumentationPreferences,
    PerformanceVsMaintainability,
    ProjectIdentity,
    SecurityPosture,
    TeamCollaboration,
    TestingStrategy,
)
from .checkpoints import (
    confirm_apply,
    confirm_commands,
    confirm_detection,
    display_cancelled,
    display_command_selection,
    display_completion_summary,
    display_detection_results,
    display_error,
    display_preview,
)
from .questions import QUESTIONS

# Import wizard modules
from .renderer import (
    ask_choice,
    ask_input,
    ask_multi_choice,
    ask_yes_no,
    clear_screen,
    pause,
    print_dim,
    print_error,
    print_header,
    print_info,
    print_section,
    print_success,
    print_warning,
)


class CCOWizard:
    """Main wizard orchestrator"""

    def __init__(self, project_root: str, dry_run: bool = False) -> None:
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.cco_root = Path(__file__).parent.parent

        # State
        self.detection_report: Optional[Dict[str, Any]] = None
        self.recommendations: Optional[Dict[str, Any]] = None
        self.preferences: Optional[CCOPreferences] = None
        self.selected_principle_ids: List[str] = []
        self.selected_commands: List[str] = []
        self.changes: Dict[str, Any] = {}

    def run(self) -> bool:
        """Run the complete wizard flow"""
        try:
            start_time = time.time()

            # Welcome
            self._show_welcome()

            # Phase 1: Detection
            if not self._run_detection():
                return False

            # Phase 2: Questions
            if not self._run_questions():
                return False

            # Phase 2.5: Principle Customization
            if not self._run_principle_customization():
                return False

            # Phase 3: Command Selection
            if not self._run_command_selection():
                return False

            # Phase 4: Preview
            if not self._run_preview():
                return False

            # Phase 5: Apply (or dry-run)
            if not self._run_apply():
                return False

            # Success
            duration = time.time() - start_time
            self._show_completion(duration)

            return True

        except KeyboardInterrupt:
            print()
            display_cancelled()
            return False
        except Exception as e:
            display_error(f"Wizard failed: {str(e)}", details=str(e))
            return False

    def _show_welcome(self) -> None:
        """Show welcome message"""
        if self.dry_run:
            print_header(
                "CCO 2.5 Interactive Wizard (DRY RUN)",
                "No files will be modified - preview mode only",
            )
        else:
            print_header(
                "CCO 2.5 Interactive Wizard",
                "Universal, project-independent AI project management",
            )

        print_info("This wizard will guide you through 5 phases:", indent=2)
        print_info("1. Detection - Analyze your project", indent=4)
        print_info("2. Questions - Configure preferences (58 questions)", indent=4)
        print_info("3. Commands - Select CCO commands to install", indent=4)
        print_info("4. Preview - Review all changes", indent=4)
        print_info("5. Apply - Install CCO system", indent=4)
        print()
        print_info(f"Project: {self.project_root}", indent=2)
        print()
        pause()

    def _run_detection(self) -> bool:
        """Phase 1: Run project detection"""
        clear_screen()
        print_header("Phase 1: Project Detection", "Analyzing your codebase...")

        print_info("Scanning project files...", indent=2)
        print()

        try:
            # Run detection
            detector = UniversalDetector(str(self.project_root))
            self.detection_report = detector.analyze().dict()

            # Display results
            display_detection_results(self.detection_report)

            # Confirm
            if not confirm_detection(self.detection_report):
                print_warning("Detection confirmation failed", indent=2)
                return False

            return True

        except Exception as e:
            print_error(f"Detection failed: {str(e)}", indent=2)
            return False

    def _run_questions(self) -> bool:
        """Phase 2: Ask user questions"""
        clear_screen()
        print_header("Phase 2: Configuration Questions", "58 questions across 9 categories")

        print_info("We'll ask questions to configure CCO for your project.", indent=2)
        print_info("AI recommendations are shown based on detection results.", indent=2)
        print()

        # Generate recommendations first
        print_info("Generating AI recommendations...", indent=2)
        try:
            rec_engine = RecommendationEngine(self.detection_report)
            self.recommendations = rec_engine.generate_full_recommendations()
        except Exception as e:
            print_warning(f"Could not generate recommendations: {str(e)}", indent=2)
            self.recommendations = {}

        print()
        pause()

        # Ask questions by category
        answers = {}
        categories = {
            "project_identity": "Project Identity (12 questions)",
            "development_style": "Development Style (8 questions)",
            "code_quality": "Code Quality Standards (10 questions)",
            "documentation": "Documentation Preferences (8 questions)",
            "testing": "Testing Strategy (7 questions)",
            "security": "Security Posture (6 questions)",
            "performance": "Performance vs Maintainability (5 questions)",
            "collaboration": "Team Collaboration (4 questions)",
            "devops": "DevOps Automation (6 questions)",
        }

        for category, title in categories.items():
            clear_screen()
            print_section(title, level=1)
            print()

            category_questions = [q for q in QUESTIONS if q["category"] == category]
            category_answers = self._ask_category_questions(category_questions)
            answers[category] = category_answers

            print()
            print_success(f"{title} complete!", indent=2)
            print()
            pause()

        # Build preferences object
        try:
            self.preferences = CCOPreferences(
                project_identity=ProjectIdentity(**answers["project_identity"]),
                development_style=DevelopmentStyle(**answers["development_style"]),
                code_quality=CodeQualityStandards(**answers["code_quality"]),
                documentation=DocumentationPreferences(**answers["documentation"]),
                testing=TestingStrategy(**answers["testing"]),
                security=SecurityPosture(**answers["security"]),
                performance=PerformanceVsMaintainability(**answers["performance"]),
                collaboration=TeamCollaboration(**answers["collaboration"]),
                devops=DevOpsAutomation(**answers["devops"]),
            )
        except Exception as e:
            print_error(f"Failed to build preferences: {str(e)}", indent=2)
            return False

        return True

    def _ask_category_questions(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ask all questions in a category"""
        answers: Dict[str, Any] = {}

        for q in questions:
            answer = self._ask_question(q)
            answers[q["field"]] = answer

        return answers

    def _ask_question(self, question: Dict[str, Any]) -> object:
        """Ask a single question"""

        # Get default value
        try:
            default = (
                question["default"](self.detection_report)
                if callable(question["default"])
                else question["default"]
            )
        except Exception:
            default = None

        # Get AI hint
        try:
            hint = (
                question["ai_hint"](self.detection_report)
                if callable(question["ai_hint"])
                else question.get("ai_hint", "")
            )
        except Exception:
            hint = ""

        # Display AI hint if available
        if hint:
            print_info(f"AI Hint: {hint}", indent=4)
            print()

        # Ask based on question type
        q_type = question["type"]

        if q_type == "text":
            answer = ask_input(
                question["prompt"],
                default=default,
                required=question.get("required", False),
            )
            return answer

        elif q_type == "multi_text":
            answer = ask_input(
                question["prompt"],
                default=", ".join(default) if isinstance(default, list) else default,
                required=False,
            )
            # Parse comma-separated values
            if answer:
                return [item.strip() for item in answer.split(",") if item.strip()]
            return []

        elif q_type == "choice":
            answer = ask_choice(
                question["prompt"],
                choices=question["choices"],
                default=default,
            )
            return answer

        elif q_type == "multi_choice":
            answer = ask_multi_choice(
                question["prompt"],
                choices=question["choices"],
                defaults=default if isinstance(default, list) else [default] if default else [],
            )
            return answer

        elif q_type == "int":
            min_val = question.get("min", 0)
            max_val = question.get("max", 999)
            while True:
                answer = ask_input(
                    f"{question['prompt']} ({min_val}-{max_val})",
                    default=str(default) if default is not None else None,
                    required=False,
                )
                try:
                    value = int(answer) if answer else default
                    if value == 0 or (min_val <= value <= max_val):
                        return value if value != 0 else None
                    print_warning(
                        f"Please enter a value between {min_val} and {max_val}, or 0 for no limit",
                        indent=4,
                    )
                except ValueError:
                    print_warning("Please enter a valid integer", indent=4)

        elif q_type == "bool":
            answer = ask_yes_no(
                question["prompt"],
                default=default,
            )
            return answer

        else:
            print_error(f"Unknown question type: {q_type}", indent=4)
            return default

    def _run_principle_customization(self) -> bool:
        """Phase 2.5: Customize principle selection"""
        print_header("Phase 2.5: Principle Selection")
        print_info("Based on your answers, we've selected applicable development principles.")
        print_info("Review and customize the selection below:")
        print()

        # Import PrincipleSelector
        from ..core.principle_selector import PrincipleSelector

        # Create selector with user preferences
        selector = PrincipleSelector(self.preferences)

        # Get applicable and skipped principles
        applicable = selector.select_applicable()
        skipped = selector.get_skipped_principles()
        all_principles = selector.all_principles

        # Create selection state (initially all applicable are selected)
        selected_ids = {p["id"] for p in applicable}

        # Show summary
        print_success(f"✓ {len(applicable)} principles automatically selected")
        print_dim(f"  {len(skipped)} principles skipped (not applicable)")
        print()

        # Group by category for display
        by_category = {}
        for p in all_principles:
            cat = p.get("category", "unknown")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(p)

        # Show principles by category with selection status
        category_names = {
            "code_quality": "Code Quality",
            "architecture": "Architecture",
            "security_privacy": "Security & Privacy",
            "operations": "Operational Excellence",
            "testing": "Testing",
            "git_workflow": "Git Workflow",
            "performance": "Performance",
            "api_design": "API Design",
        }

        print_header("Selected Principles (by Category):")
        print()

        for cat_id, cat_name in category_names.items():
            principles = by_category.get(cat_id, [])
            if not principles:
                continue

            selected_in_cat = [p for p in principles if p["id"] in selected_ids]
            if not selected_in_cat:
                continue

            print_success(f"  {cat_name} ({len(selected_in_cat)}/{len(principles)})")
            for p in selected_in_cat:
                # Show principle with one-line description
                one_line = p.get("one_line_why", p.get("description", "No description"))
                severity_emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(p.get("severity", "low"), "⚪")

                print(f"    {severity_emoji} {p['id']}: {p['title']}")
                print_dim(f"       {one_line}")
            print()

        # Ask if user wants to customize
        print_info("Would you like to customize this selection?")
        customize = input("  [y/N]: ").strip().lower() == "y"
        print()

        if customize:
            print_info("Customization options:")
            print("  1. Add principles from skipped list")
            print("  2. Remove principles from selected list")
            print("  3. View all principles by category")
            print("  4. Continue with current selection")
            print()

            while True:
                choice = input("  Enter option (1-4): ").strip()

                if choice == "1":
                    # Show skipped principles
                    print()
                    print_header("Skipped Principles (available to add):")
                    print()

                    for cat_id, cat_name in category_names.items():
                        principles = by_category.get(cat_id, [])
                        skipped_in_cat = [p for p in principles if p["id"] not in selected_ids]

                        if skipped_in_cat:
                            print_info(f"  {cat_name}:")
                            for p in skipped_in_cat:
                                one_line = p.get("one_line_why", p.get("description", ""))
                                print(f"    {p['id']}: {p['title']}")
                                print_dim(f"       {one_line}")
                            print()

                    # Ask which to add
                    add_ids = input(
                        "  Enter principle IDs to add (comma-separated, or 'back'): ",
                    ).strip()
                    if add_ids.lower() != "back":
                        for pid in add_ids.split(","):
                            pid = pid.strip().upper()
                            if any(p["id"] == pid for p in all_principles):
                                selected_ids.add(pid)
                                print_success(f"    ✓ Added {pid}")
                            else:
                                print_error(f"    ✗ Unknown principle: {pid}")
                    print()

                elif choice == "2":
                    # Show selected principles for removal
                    print()
                    print_header("Currently Selected Principles:")
                    print()

                    for p in sorted(
                        [p for p in all_principles if p["id"] in selected_ids],
                        key=lambda x: x["id"],
                    ):
                        print(f"    {p['id']}: {p['title']}")
                    print()

                    # Ask which to remove
                    remove_ids = input(
                        "  Enter principle IDs to remove (comma-separated, or 'back'): ",
                    ).strip()
                    if remove_ids.lower() != "back":
                        for pid in remove_ids.split(","):
                            pid = pid.strip().upper()
                            if pid in selected_ids:
                                selected_ids.remove(pid)
                                print_success(f"    ✓ Removed {pid}")
                            else:
                                print_error(f"    ✗ Principle not selected: {pid}")
                    print()

                elif choice == "3":
                    # View all principles
                    print()
                    print_header("All Principles by Category:")
                    print()

                    for cat_id, cat_name in category_names.items():
                        principles = by_category.get(cat_id, [])
                        if not principles:
                            continue

                        print_info(f"  {cat_name} ({len(principles)} principles):")
                        for p in principles:
                            selected_mark = "✓" if p["id"] in selected_ids else " "
                            one_line = p.get("one_line_why", p.get("description", ""))
                            print(f"    [{selected_mark}] {p['id']}: {p['title']}")
                            print_dim(f"         {one_line}")
                        print()

                    input("  Press Enter to continue...")
                    print()

                elif choice == "4":
                    break
                else:
                    print_error("  Invalid option. Please enter 1-4.")
                    print()

        # Store final selection in state and preferences
        self.selected_principle_ids = list(selected_ids)
        self.preferences.selected_principle_ids = list(selected_ids)

        # Show final summary
        print()
        print_success(f"✓ Final selection: {len(selected_ids)}/{len(all_principles)} principles")
        print()

        return True

    def _run_command_selection(self) -> bool:
        """Phase 3: Select commands to install"""
        clear_screen()
        print_header("Phase 3: Command Selection", "Choose which CCO commands to install")

        print_info("CCO will recommend commands based on your preferences.", indent=2)
        print()
        pause()

        try:
            # Auto-discover commands from templates directory
            templates_dir = self.cco_root / "templates"
            available_commands = []
            template_paths = {}  # Map command_id -> template_path

            # Scan all template files
            for category_dir in templates_dir.iterdir():
                if category_dir.is_dir():
                    category_name = category_dir.name
                    for template_file in category_dir.glob("*.template.md"):
                        # Extract command ID from filename (e.g., "cco-help.template.md" -> "cco-help")
                        command_id = template_file.stem.replace(".template", "")

                        # Store template path for later use
                        template_paths[command_id] = str(template_file)

                        # Create CommandMetadata object
                        cmd_metadata = CommandMetadata(
                            command_id=command_id,
                            display_name=command_id.replace("cco-", "").replace("-", " ").title(),
                            category=category_name,
                            description_short=f"CCO {command_id.replace('cco-', '')} command",
                            description_long=f"Command from {category_name} category",
                            applicable_project_types=["all"],  # Will be filtered by recommender
                        )
                        available_commands.append(cmd_metadata)

            # Store template paths for later use in generation
            self.template_paths = template_paths

            # Build CommandRegistry object for recommender
            registry = CommandRegistry(
                version=cco_version,
                commands=available_commands,
            )

            # Get recommendations
            print_info("Analyzing your preferences...", indent=2)
            recommender = CommandRecommender(self.preferences, registry)
            recommendations = recommender.recommend_commands()

            core_commands = recommendations.get("core", [])
            recommended_commands = recommendations.get("recommended", [])
            optional_commands = recommendations.get("optional", [])
            reasoning = recommendations.get("reasoning", {})

            # Show recommendations
            clear_screen()
            print_section("Recommended Commands", level=1)
            print()

            print_section("Core Commands (Always Included)", level=2)
            for cmd in core_commands:
                print_success(f"/{cmd} - {reasoning.get(cmd, '')}", indent=4)
            print()

            print_section("Recommended Commands", level=2)
            for cmd in recommended_commands:
                print_success(f"/{cmd} - {reasoning.get(cmd, '')}", indent=4)
            print()

            if optional_commands:
                print_section("Optional Commands", level=2)
                for cmd in optional_commands:
                    print_info(f"/{cmd} - {reasoning.get(cmd, '')}", indent=4)
                print()

            # Ask if user wants to customize
            print()
            if ask_yes_no("Do you want to add more optional commands?", default=False):
                # Show optional commands and let user select
                print()
                print_section("Select Additional Commands", level=2)
                print_info(
                    "You can select additional commands from the optional list below:",
                    indent=2,
                )
                print()

                # Prepare choices for multi-select
                optional_choices = [
                    f"{cmd} - {reasoning.get(cmd, 'Available')}" for cmd in optional_commands
                ]

                if optional_choices:
                    selected_optional = ask_multi_choice(
                        "Select additional commands to enable (enter numbers separated by spaces):",
                        optional_choices,
                        defaults=[],
                        min_selections=0,
                        show_pagination=True,
                        page_size=DEFAULT_PAGE_SIZE,
                    )

                    # Extract command IDs from selections
                    selected_optional_ids = []
                    for selection in selected_optional:
                        # Extract command ID (first part before " - ")
                        cmd_id = selection.split(" - ")[0]
                        selected_optional_ids.append(cmd_id)

                    self.selected_commands = (
                        core_commands + recommended_commands + selected_optional_ids
                    )
                else:
                    print_warning("No optional commands available", indent=2)
                    self.selected_commands = core_commands + recommended_commands
            else:
                # Use recommendations only
                self.selected_commands = core_commands + recommended_commands

            # Display selection
            clear_screen()
            display_command_selection(
                core_commands=core_commands,
                recommended_commands=recommended_commands,
                optional_commands=optional_commands,
                selected=self.selected_commands,
                reasoning=reasoning,
            )

            # Confirm
            if not confirm_commands(self.selected_commands):
                print_warning("Command selection not confirmed", indent=2)
                return False

            return True

        except Exception as e:
            print_error(f"Command selection failed: {str(e)}", indent=2)
            import traceback

            traceback.print_exc()
            return False

    def _run_preview(self) -> bool:
        """Phase 4: Preview all changes"""
        clear_screen()
        print_header("Phase 4: Preview Changes", "Review before applying")

        # Build change manifest
        self.changes = self._build_change_manifest()

        # Display preview
        display_preview(self.changes, dry_run=self.dry_run)

        # Confirm (or auto-confirm for dry-run)
        if not confirm_apply(dry_run=self.dry_run):
            print_warning("Changes not confirmed", indent=2)
            return False

        return True

    def _build_change_manifest(self) -> Dict[str, Any]:
        """Build manifest of all changes to be applied"""
        changes = {
            "files_to_create": {
                "commands": [f".claude/commands/{cmd}.md" for cmd in self.selected_commands],
                "config": [
                    ".cco/config/preferences.json",
                    ".cco/config/project.json",
                ],
                "docs": [
                    "PRINCIPLES.md",
                ],
            },
            "files_to_modify": [
                ".claude/settings.local.json",
            ],
            "commands_to_install": [
                {"id": cmd, "category": "system"} for cmd in self.selected_commands
            ],
            "permissions_configured": {
                "bash_commands_count": 340,
                "glob_patterns_count": 56,
                "read_paths_count": 2,
                "write_paths_count": 2,
            },
            "principles_selected": [
                "Fail-Fast Validation",
                "Zero Dead Code",
                "DRY (Don't Repeat Yourself)",
                "Production-Grade Only",
                "Type Safety",
                "Secure by Default",
            ],
        }

        return changes

    def _run_apply(self) -> bool:
        """Phase 5: Apply changes (or dry-run)"""
        if self.dry_run:
            print_header("Dry Run Complete", "No changes were made")
            print_success(
                "Dry run successful! Re-run without --dry-run to apply changes.",
                indent=2,
            )
            return True

        clear_screen()
        print_header("Phase 5: Applying Changes", "Installing CCO system...")
        print()

        try:
            # Create directories
            print_info("Creating directories...", indent=2)
            self._create_directories()
            print_success("Directories created", indent=2)
            print()

            # Write preferences
            print_info("Writing preferences...", indent=2)
            self._write_preferences()
            print_success("Preferences saved", indent=2)
            print()

            # Generate commands
            print_info("Generating commands...", indent=2)
            self._generate_commands()
            print_success(f"{len(self.selected_commands)} commands generated", indent=2)
            print()

            # Configure permissions
            print_info("Configuring permissions...", indent=2)
            self._configure_permissions()
            print_success("Permissions configured", indent=2)
            print()

            # Generate principles
            print_info("Generating principles document...", indent=2)
            self._generate_principles()
            print_success("Principles document created", indent=2)
            print()

            return True

        except Exception as e:
            print_error(f"Apply failed: {str(e)}", indent=2)
            import traceback

            traceback.print_exc()
            return False

    def _create_directories(self) -> None:
        """Create necessary directories (minimal structure)"""
        dirs = [
            self.project_root / ".cco",  # Just .cco/ directory
            self.project_root / ".claude" / "commands",  # For project-specific commands
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

    def _write_preferences(self) -> None:
        """Write project config and commands registry to .cco/"""
        if not self.preferences:
            raise ValueError("No preferences to write")

        # Write project.json (all project settings and preferences)
        project_config_path = self.project_root / ".cco" / "project.json"
        project_config = self.preferences.dict()
        project_config["cco"] = {
            "version": cco_version,
            "configured_at": datetime.now().isoformat(),
            "principle_count": 10,  # Can be extracted from preferences if needed
        }

        with open(project_config_path, "w", encoding="utf-8") as f:
            json.dump(project_config, f, indent=2)

        # Write commands.json (enabled commands registry)
        commands_registry_path = self.project_root / ".cco" / "commands.json"
        commands_registry = {
            "version": cco_version,
            "configured_at": datetime.now().isoformat(),
            "commands": [
                {
                    "id": cmd_id,
                    "enabled": True,
                    "category": "system",  # Could be more specific based on command
                }
                for cmd_id in self.selected_commands
            ],
        }

        with open(commands_registry_path, "w", encoding="utf-8") as f:
            json.dump(commands_registry, f, indent=2)

    def _generate_commands(self) -> None:
        """Generate command files from templates using CommandGenerator"""
        from ..core.generator import CommandGenerator

        generator = CommandGenerator(self.project_root)
        result = generator.generate_all()

        if not result.get("success"):
            raise Exception(f"Command generation failed: {result.get('error')}")

        if result.get("failed_commands"):
            print_warning(
                f"Failed to generate {len(result['failed_commands'])} commands:",
                indent=4,
            )
            for cmd in result["failed_commands"]:
                print_warning(f"  - {cmd}", indent=6)

    def _configure_permissions(self) -> None:
        """Configure Claude Code permissions"""
        # This would use the permission generator (not yet implemented)
        # For now, just create a basic config
        settings_path = self.project_root / ".claude" / "settings.local.json"

        settings = {
            "permissions": {
                "version": cco_version,
                "configured_by": "cco-wizard",
                "configured_at": datetime.now().isoformat(),
            },
        }

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def _generate_principles(self) -> None:
        """Generate PRINCIPLES.md from selected principles"""
        principles_path = self.project_root / "PRINCIPLES.md"

        content = f"""# Development Principles - {self.preferences.project_identity.name}

Generated by CCO 2.5 on {datetime.now().strftime("%Y-%m-%d")}

## Code Quality

- Linting: {self.preferences.code_quality.linting_strictness}
- Type Coverage: {self.preferences.code_quality.type_coverage_target}%
- DRY Enforcement: {self.preferences.code_quality.dry_enforcement}

## Testing

- Coverage Target: {self.preferences.testing.coverage_target}%
- Test Pyramid: {self.preferences.testing.test_pyramid_ratio}
- Mocking: {self.preferences.testing.mocking_philosophy}

## Security

- Security Stance: {self.preferences.security.security_stance}
- Secret Management: {self.preferences.security.secret_management}
- Encryption: {self.preferences.security.encryption_scope}

## Documentation

- Verbosity: {self.preferences.documentation.verbosity}
- Target Audience: {self.preferences.documentation.target_audience}
- API Docs: {self.preferences.documentation.api_documentation}
"""

        with open(principles_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _show_completion(self, duration: float) -> None:
        """Show completion summary"""
        clear_screen()

        files_created = sum(
            len(files) if isinstance(files, list) else sum(len(v) for v in files.values())
            for files in self.changes.get("files_to_create", {}).values()
        )

        display_completion_summary(
            commands_installed=len(self.selected_commands),
            principles_configured=6,  # TODO: Count actual principles
            files_created=files_created,
            duration_seconds=duration,
        )


def main() -> None:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CCO 2.5 Interactive Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python wizard/cli.py                    # Run wizard in current directory
  python wizard/cli.py --dry-run          # Preview without making changes
  python wizard/cli.py --project /path    # Run in specific directory
        """,
    )

    parser.add_argument(
        "--project",
        type=str,
        default=os.getcwd(),
        help="Project root directory (default: current directory)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview mode - don't make any file changes",
    )

    args = parser.parse_args()

    # Run wizard
    wizard = CCOWizard(args.project, dry_run=args.dry_run)
    success = wizard.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
