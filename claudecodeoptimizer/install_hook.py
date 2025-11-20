"""
Post-install hook for ClaudeCodeOptimizer

Automatically sets up ~/.claude/ structure after pip install.
"""

import logging
import sys

logger = logging.getLogger(__name__)


def _show_installation_summary(
    counts_before: dict[str, int], counts_after: dict[str, int], was_already_installed: bool
) -> None:
    """
    Show detailed before/after comparison of installed files.

    Categories (consistent order):
    - Agents → Commands → Skills → Principles

    States:
    - New: Files added (0 → N)
    - Re-installed: Files overwritten when already installed (N → N or N → M)
    - Removed: Files deleted (N → 0)

    Args:
        counts_before: File counts before installation
        counts_after: File counts after installation
        was_already_installed: Whether CCO was already installed (shows "Re-installed" instead of "Updated")
    """
    # Use consistent category ordering
    category_order = ["agents", "commands", "skills", "principles", "templates"]
    all_categories = sorted(
        set(counts_before.keys()) | set(counts_after.keys()),
        key=lambda x: category_order.index(x) if x in category_order else 999,
    )

    new_files = []
    reinstalled_files = []
    removed_files = []

    for category in all_categories:
        before = counts_before.get(category, 0)
        after = counts_after.get(category, 0)

        if before == 0 and after > 0:
            # New files
            new_files.append(f"  + {category.capitalize()}: {after} files")
        elif before > 0 and after > 0:
            # Re-installed files (when already installed)
            if after != before:
                reinstalled_files.append(f"  ↻ {category.capitalize()}: {before} → {after} files")
            else:
                reinstalled_files.append(f"  ↻ {category.capitalize()}: {after} files")
        elif before > 0 and after == 0:
            # Removed files
            removed_files.append(f"  - {category.capitalize()}: {before} files removed")

    # Display results with consistent formatting
    if new_files:
        print("\n  New:")
        for line in new_files:
            print(line)

    if reinstalled_files:
        # Show "Re-installed" if was already installed, otherwise "Updated"
        section_name = "Re-installed" if was_already_installed else "Updated"
        print(f"\n  {section_name}:")
        for line in reinstalled_files:
            print(line)

    if removed_files:
        print("\n  Removed:")
        for line in removed_files:
            print(line)

    # Total summary with visual separator
    total_before = sum(counts_before.values())
    total_after = sum(counts_after.values())
    print("\n" + "  " + "-" * 56)
    print(f"  Total: {total_before} → {total_after} files")


def post_install() -> int:
    """
    Post-install hook - sets up ~/.claude/ structure.

    Called automatically after pip install.

    Supports flags:
    - --force: Overwrite existing files without asking
    - --help: Show usage

    Returns:
        Exit code (0 for success)
    """
    # Parse command-line arguments
    force = "--force" in sys.argv
    show_help = "--help" in sys.argv or "-h" in sys.argv

    if show_help:
        print("\nUsage: cco-setup [--force] [--help]")
        print()
        print("Setup CCO global configuration in ~/.claude/")
        print()
        print("Options:")
        print("  --force    Overwrite existing files without asking")
        print("  --help     Show this help message")
        print()
        return 0

    try:
        # Import here to avoid circular dependencies
        from claudecodeoptimizer.core.knowledge_setup import (
            check_existing_installation,
            setup_global_knowledge,
        )

        print("\n" + "=" * 60)
        print("ClaudeCodeOptimizer Setup")
        print("=" * 60)

        # Check if CCO is already installed
        existing = check_existing_installation()

        if existing and not force:
            # Interactive mode: Ask user before overwriting
            print("\n[NOTICE] CCO is already installed in ~/.claude/")
            print("\n  Current installation:")
            for category, count in existing.items():
                print(f"    • {category.capitalize()}: {count} files")
            print("\n" + "-" * 60)
            print("  Overwrite existing files?")
            print("    [y] Yes, overwrite all")
            print("    [n] No, cancel")
            print("    [d] Show diff (what will be overwritten)")
            print("-" * 60)
            choice = input("\n  Choice [y/n/d]: ").strip().lower()

            if choice == "d":
                # Show what will be overwritten
                from claudecodeoptimizer.core.knowledge_setup import (
                    show_installation_diff,
                )

                show_installation_diff()
                print("\n" + "-" * 60)
                choice = input("  Proceed with overwrite? [y/n]: ").strip().lower()
                print("-" * 60)

            if choice != "y":
                print("\n[CANCELLED] Setup cancelled by user")
                print("  To overwrite without asking: cco-setup --force")
                print("=" * 60 + "\n")
                return 0
            else:
                print("\n[OK] Proceeding with setup...")

        # Setup global ~/.claude/ structure
        result = setup_global_knowledge(force=force or bool(existing))

        if result.get("success"):
            # Show installation actions
            print("\n" + "-" * 60)
            print("INSTALLATION COMPLETE")
            print("-" * 60)
            print(f"\n  Location: {result['claude_dir']}")
            print("\n  Actions performed:")
            for action in result.get("actions", []):
                print(f"    • {action}")

            # Show before/after comparison
            counts_before = result.get("counts_before", {})
            counts_after = result.get("counts_after", {})

            if counts_before or counts_after:
                print("\n" + "-" * 60)
                print("FILE SUMMARY")
                print("-" * 60)
                _show_installation_summary(counts_before, counts_after, bool(existing))

            print("\n" + "=" * 60)
            print("CCO IS READY!")
            print("=" * 60)
            print("\n  All CCO commands are now available globally.")
            print("\n  Next steps:")
            print("    1. Restart Claude Code (if already open)")
            print("    2. Try: /cco-help or /cco-status")
        else:
            logger.warning("Setup completed with warnings")
            print("\n[WARNING] Setup completed with warnings")

        print("=" * 60 + "\n")

        # Return success for scripting
        return 0

    except Exception as e:
        # Non-fatal: Don't break pip install if setup fails
        logger.error("CCO setup failed", exc_info=True)
        print("\n" + "=" * 60)
        print("[ERROR] Setup failed")
        print("=" * 60)
        print(f"\n  Error: {e}")
        print("\n  You can run setup manually with: cco-setup")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    post_install()
