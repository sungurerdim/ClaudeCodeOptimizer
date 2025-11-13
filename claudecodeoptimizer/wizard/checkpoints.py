"""
Confirmation and Preview Screens - CCO Wizard

Checkpoint functions for user confirmation at key decision points:
1. Detection results review
2. Recommendations preview
3. Command selection confirmation
4. Final changes preview
"""

from typing import Any, Dict, List, Optional

from ..core.utils import format_confidence
from .renderer import (
    Colors,
    ask_yes_no,
    pause,
    print_box,
    print_header,
    print_info,
    print_key_value,
    print_list,
    print_section,
    print_success,
    print_table,
    print_warning,
)


def display_detection_results(report: Dict[str, Any]) -> None:
    """Display project detection results for user review"""

    print_header(
        "Project Detection Results",
        "CCO has analyzed your project and detected the following",
    )

    # Languages
    print_section("Detected Languages", level=1)
    if report.get("languages"):
        lang_data = [
            {
                "Language": lang["detected_value"],
                "Confidence": f"{int(format_confidence(lang['confidence'], 0))}%",
                "Evidence": ", ".join(lang["evidence"][:2]),
            }
            for lang in report["languages"]
        ]
        print_table(lang_data)
    else:
        print_warning("No languages detected", indent=4)

    # Frameworks
    print_section("Detected Frameworks", level=1)
    if report.get("frameworks"):
        framework_data = [
            {
                "Framework": fw["detected_value"],
                "Confidence": f"{int(format_confidence(fw['confidence'], 0))}%",
                "Evidence": ", ".join(fw["evidence"][:2]),
            }
            for fw in report["frameworks"]
        ]
        print_table(framework_data)
    else:
        print_info("No frameworks detected", indent=4)

    # Project Types
    print_section("Detected Project Types", level=1)
    if report.get("project_types"):
        types = [
            f"{pt['detected_value']} ({int(format_confidence(pt['confidence'], 0))}%)"
            for pt in report["project_types"]
        ]
        print_list(types, indent=4)
    else:
        print_warning("No project types detected", indent=4)

    # Tools
    print_section("Detected Tools", level=1)
    if report.get("tools"):
        tools_by_category = {}
        for tool in report["tools"]:
            category = tool.get("category", "other")
            if category not in tools_by_category:
                tools_by_category[category] = []
            tools_by_category[category].append(tool["detected_value"])

        for category, tools in sorted(tools_by_category.items()):
            print_section(category.replace("_", " ").title(), level=2)
            print_list(tools, indent=6)
    else:
        print_info("No tools detected", indent=4)

    # Codebase Patterns
    print_section("Codebase Statistics", level=1)
    patterns = report.get("codebase_patterns", {})
    if patterns:
        print_key_value("Total Files", patterns.get("total_files", 0), indent=4)
        print_key_value("Lines of Code", patterns.get("total_lines", 0), indent=4)
        print_key_value("Project Root", patterns.get("project_root", "N/A"), indent=4)

        if "file_distribution" in patterns:
            print()
            print_section("File Distribution", level=2)
            dist_data = [
                {"Extension": ext, "Count": count}
                for ext, count in sorted(
                    patterns["file_distribution"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]  # Top 10
            ]
            print_table(dist_data)

    print()


def display_recommendations(recommendations: Dict[str, Any]) -> None:
    """Display AI-generated recommendations"""

    print_header(
        "CCO Recommendations",
        "Based on your project, we recommend the following configuration",
    )

    # Project Identity Recommendations
    if "project_identity" in recommendations:
        print_section("Project Identity", level=1)
        identity = recommendations["project_identity"]

        for key, value in identity.items():
            if isinstance(value, list):
                print_key_value(key.replace("_", " ").title(), ", ".join(value), indent=4)
            else:
                print_key_value(key.replace("_", " ").title(), value, indent=4)
        print()

    # Development Style Recommendations
    if "development_style" in recommendations:
        print_section("Development Style", level=1)
        style = recommendations["development_style"]

        for key, value in style.items():
            print_key_value(key.replace("_", " ").title(), value, indent=4)
        print()

    # Code Quality Recommendations
    if "code_quality" in recommendations:
        print_section("Code Quality Standards", level=1)
        quality = recommendations["code_quality"]

        for key, value in quality.items():
            print_key_value(key.replace("_", " ").title(), value, indent=4)
        print()

    # Security Recommendations
    if "security_recs" in recommendations:
        print_section("Security Recommendations", level=1)
        security = recommendations["security_recs"]

        if isinstance(security, list):
            for rec in security:
                if isinstance(rec, dict):
                    priority = rec.get("priority", "medium")
                    icon = (
                        "[!]" if priority == "high" else "[!]" if priority == "medium" else "[OK]"
                    )
                    print_info(f"{icon} {rec.get('recommendation', rec)}", indent=4)
                else:
                    print_info(f"* {rec}", indent=4)
        print()

    # Performance Recommendations
    if "performance_recs" in recommendations:
        print_section("Performance Recommendations", level=1)
        performance = recommendations["performance_recs"]

        if isinstance(performance, list):
            for rec in performance:
                if isinstance(rec, dict):
                    print_info(f"* {rec.get('recommendation', rec)}", indent=4)
                else:
                    print_info(f"* {rec}", indent=4)
        print()

    print()


def display_command_selection(
    core_commands: List[str],
    recommended_commands: List[str],
    optional_commands: List[str],
    selected: List[str],
    reasoning: Optional[Dict[str, str]] = None,
) -> None:
    """Display command selection summary"""

    print_header(
        "Selected CCO Commands",
        f"You have selected {len(selected)} commands",
    )

    # Core commands (always selected)
    print_section("Core Commands (Required)", level=1)
    print_info(f"{len(core_commands)} commands - Always included", indent=4)
    print()
    for cmd in core_commands:
        reason = reasoning.get(cmd, "") if reasoning else ""
        if reason:
            print_success(f"/{cmd} - {reason}", indent=4)
        else:
            print_success(f"/{cmd}", indent=4)
    print()

    # Recommended commands (selected by default)
    if recommended_commands:
        selected_recommended = [cmd for cmd in recommended_commands if cmd in selected]
        print_section(
            f"Recommended Commands ({len(selected_recommended)}/{len(recommended_commands)})",
            level=1,
        )
        print()
        for cmd in recommended_commands:
            if cmd in selected:
                reason = reasoning.get(cmd, "") if reasoning else ""
                if reason:
                    print_success(f"+ /{cmd} - {reason}", indent=4)
                else:
                    print_success(f"+ /{cmd}", indent=4)
            else:
                print_info(f"  /{cmd} (not selected)", indent=4)
        print()

    # Optional commands (user choice)
    if optional_commands:
        selected_optional = [cmd for cmd in optional_commands if cmd in selected]
        if selected_optional:
            print_section(f"Optional Commands ({len(selected_optional)} selected)", level=1)
            print()
            for cmd in selected_optional:
                reason = reasoning.get(cmd, "") if reasoning else ""
                if reason:
                    print_success(f"+ /{cmd} - {reason}", indent=4)
                else:
                    print_success(f"+ /{cmd}", indent=4)
            print()

    # Summary
    print_box(
        [
            f"Total Commands: {len(selected)}",
            f"Core: {len(core_commands)}",
            f"Recommended: {len([c for c in recommended_commands if c in selected])}",
            f"Optional: {len([c for c in optional_commands if c in selected])}",
        ],
        title="Summary",
    )


def display_preview(changes: Dict[str, Any], dry_run: bool = False) -> None:
    """Display preview of all changes that will be applied"""

    if dry_run:
        print_header(
            "Preview Mode - No Changes Will Be Made",
            "This is a dry-run. Review what WOULD happen",
        )
    else:
        print_header(
            "Final Preview",
            "Review all changes before applying",
        )

    # Files to create
    if changes.get("files_to_create"):
        print_section("Files to Create", level=1)
        files = changes["files_to_create"]

        if isinstance(files, dict):
            for category, file_list in files.items():
                print_section(category.replace("_", " ").title(), level=2)
                for file_path in file_list:
                    print_success(f"CREATE {file_path}", indent=6)
        else:
            for file_path in files:
                print_success(f"CREATE {file_path}", indent=4)
        print()

    # Files to modify
    if changes.get("files_to_modify"):
        print_section("Files to Modify", level=1)
        for file_path in changes["files_to_modify"]:
            print_warning(f"MODIFY {file_path}", indent=4)
        print()

    # Files to delete (if any)
    if changes.get("files_to_delete"):
        print_section("Files to Delete", level=1)
        for file_path in changes["files_to_delete"]:
            print_warning(f"DELETE {file_path}", indent=4)
        print()

    # Commands to install
    if changes.get("commands_to_install"):
        print_section("Commands to Install", level=1)
        commands = changes["commands_to_install"]
        print_info(f"{len(commands)} CCO commands will be generated", indent=4)
        print()

        # Group by category
        commands_by_category = {}
        for cmd_info in commands:
            category = cmd_info.get("category", "other")
            if category not in commands_by_category:
                commands_by_category[category] = []
            commands_by_category[category].append(cmd_info["id"])

        for category, cmd_list in sorted(commands_by_category.items()):
            print_section(category.replace("_", " ").title(), level=2)
            for cmd in cmd_list:
                print_success(f"/{cmd}", indent=6)
        print()

    # Permissions to configure
    if changes.get("permissions_configured"):
        print_section("Permission System", level=1)
        perms = changes["permissions_configured"]

        print_key_value("Auto-approve bash commands", perms.get("bash_commands_count", 0), indent=4)
        print_key_value("Auto-approve glob patterns", perms.get("glob_patterns_count", 0), indent=4)
        print_key_value("Auto-approve read paths", perms.get("read_paths_count", 0), indent=4)
        print_key_value("Auto-approve write paths", perms.get("write_paths_count", 0), indent=4)
        print()

        print_warning("Note: You must restart Claude Code after initialization", indent=4)
        print()

    # Principles to install
    if changes.get("principles_selected"):
        print_section("Development Principles", level=1)
        principles = changes["principles_selected"]
        print_info(f"{len(principles)} principles will be enforced", indent=4)
        print()

        for principle in principles:
            if isinstance(principle, dict):
                print_success(f"* {principle.get('name', principle)}", indent=4)
            else:
                print_success(f"* {principle}", indent=4)
        print()

    # Summary box
    summary_lines = []
    if changes.get("files_to_create"):
        count = (
            len(changes["files_to_create"])
            if isinstance(changes["files_to_create"], list)
            else sum(len(v) for v in changes["files_to_create"].values())
        )
        summary_lines.append(f"Files to create: {count}")
    if changes.get("files_to_modify"):
        summary_lines.append(f"Files to modify: {len(changes['files_to_modify'])}")
    if changes.get("commands_to_install"):
        summary_lines.append(f"Commands to install: {len(changes['commands_to_install'])}")
    if changes.get("principles_selected"):
        summary_lines.append(f"Principles to enforce: {len(changes['principles_selected'])}")

    if summary_lines:
        print_box(summary_lines, title="Summary")

    if dry_run:
        print_info("DRY RUN: No actual changes will be made to your project", indent=2)
        print()


def confirm_action(prompt: str, default: bool = False) -> bool:
    """Ask user to confirm an action"""
    return ask_yes_no(prompt, default=default)


def confirm_detection(report: Dict[str, Any]) -> bool:
    """Confirm detection results"""
    print()
    return confirm_action(
        "Does this detection look correct?",
        default=True,
    )


def confirm_recommendations(recommendations: Dict[str, Any]) -> bool:
    """Confirm recommendations"""
    print()
    return confirm_action(
        "Do you want to use these recommendations as defaults?",
        default=True,
    )


def confirm_commands(selected: List[str]) -> bool:
    """Confirm command selection"""
    print()
    return confirm_action(
        f"Install {len(selected)} commands?",
        default=True,
    )


def confirm_apply(dry_run: bool = False) -> bool:
    """Confirm final apply"""
    if dry_run:
        print()
        print_info("DRY RUN: No changes will be made")
        pause()
        return True
    else:
        print()
        return confirm_action(
            "Apply these changes to your project?",
            default=False,
        )


def display_completion_summary(
    commands_installed: int,
    principles_configured: int,
    files_created: int,
    duration_seconds: float,
    guides_installed: int = 0,
    skills_installed: int = 0,
    agents_installed: int = 0,
) -> None:
    """Display completion summary"""
    from .. import __version__

    print_header(
        f"CCO {__version__} Initialization Complete!",
        f"Setup completed in {duration_seconds:.1f} seconds",
    )

    # Build summary lines
    summary_lines = [
        f"+ {commands_installed} commands installed",
        f"+ {principles_configured} principles configured",
    ]

    # Add optional items only if > 0
    if guides_installed > 0:
        summary_lines.append(f"+ {guides_installed} guides linked")
    if skills_installed > 0:
        summary_lines.append(f"+ {skills_installed} skills linked")
    if agents_installed > 0:
        summary_lines.append(f"+ {agents_installed} agents linked")

    summary_lines.extend(
        [
            f"+ {files_created} files created",
            "",
            "Next steps:",
            "1. Restart Claude Code to load new commands",
            "2. Run /cco-status to verify installation",
            "3. Run /cco-help to see all available commands",
        ]
    )

    print_box(
        summary_lines,
        title="Success",
        style="double",
    )

    print_success("CCO is ready to use!", indent=2)
    print()


def display_error(error: str, details: Optional[str] = None) -> None:
    """Display error message"""
    c = Colors

    print()
    print_box(
        [
            f"{c.colorize('ERROR:', c.RED)} {error}",
            "",
            details or "Check the logs for more information.",
        ],
        title="Installation Failed",
    )
    print()


def display_cancelled() -> None:
    """Display cancellation message"""
    print()
    print_box(
        [
            "CCO initialization was cancelled.",
            "",
            "No changes were made to your project.",
            "Run the wizard again when you're ready.",
        ],
        title="Cancelled",
    )
    print()
