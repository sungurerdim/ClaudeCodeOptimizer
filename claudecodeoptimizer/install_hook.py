"""
Post-install hook for ClaudeCodeOptimizer

Automatically sets up ~/.claude/ structure after pip install.
"""

import logging
import sys

logger = logging.getLogger(__name__)


def _show_installation_summary(
    counts_before: dict[str, int], counts_after: dict[str, int]
) -> None:
    """
    Show detailed before/after comparison of installed files.

    Categories:
    - New: Files added (0 → N)
    - Updated: Files overwritten (N → N)
    - Removed: Files deleted (N → 0)
    - Unchanged: Files not created (0 → 0)
    """
    all_categories = sorted(set(counts_before.keys()) | set(counts_after.keys()))

    new_files = []
    updated_files = []
    removed_files = []

    for category in all_categories:
        before = counts_before.get(category, 0)
        after = counts_after.get(category, 0)

        if before == 0 and after > 0:
            # New files
            new_files.append(f"  + {category.capitalize()}: {after} files")
        elif before > 0 and after > 0:
            # Updated files
            if after != before:
                updated_files.append(
                    f"  ↻ {category.capitalize()}: {before} → {after} files"
                )
            else:
                updated_files.append(f"  ↻ {category.capitalize()}: {after} files")
        elif before > 0 and after == 0:
            # Removed files
            removed_files.append(f"  - {category.capitalize()}: {before} files removed")

    # Display results
    if new_files:
        print("\n  New:")
        for line in new_files:
            print(line)

    if updated_files:
        print("\n  Updated:")
        for line in updated_files:
            print(line)

    if removed_files:
        print("\n  Removed:")
        for line in removed_files:
            print(line)

    # Total summary
    total_before = sum(counts_before.values())
    total_after = sum(counts_after.values())
    print(f"\n  Total: {total_before} → {total_after} files")


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
        print("ClaudeCodeOptimizer Post-Install Setup")
        print("=" * 60)

        # Check if CCO is already installed
        existing = check_existing_installation()

        if existing and not force:
            # Interactive mode: Ask user before overwriting
            print("\n[NOTICE] CCO is already installed:")
            for category, count in existing.items():
                print(f"  - {category}: {count} files")
            print()
            print("Overwrite existing files?")
            print("  [y] Yes, overwrite all")
            print("  [n] No, cancel")
            print("  [d] Show diff (what will be overwritten)")
            print()
            choice = input("Choice [y/n/d]: ").strip().lower()

            if choice == "d":
                # Show what will be overwritten
                from claudecodeoptimizer.core.knowledge_setup import (
                    show_installation_diff,
                )

                show_installation_diff()
                print()
                choice = input("Proceed with overwrite? [y/n]: ").strip().lower()

            if choice != "y":
                print("\n[CANCELLED] Installation cancelled by user")
                print("To overwrite without asking, run: cco-setup --force")
                print("=" * 60 + "\n")
                return 0
            else:
                print("\n[OK] Proceeding with overwrite...")

        # Setup global ~/.claude/ structure
        result = setup_global_knowledge(force=force or bool(existing))

        if result.get("success"):
            logger.info(f"Global CCO directory: {result['claude_dir']}")
            for action in result.get("actions", []):
                logger.info(f"  - {action}")
            print(f"\n[OK] Global CCO directory: {result['claude_dir']}")
            for action in result.get("actions", []):
                print(f"  - {action}")

            # Show before/after comparison
            counts_before = result.get("counts_before", {})
            counts_after = result.get("counts_after", {})

            if counts_before or counts_after:
                print("\n[FILE SUMMARY]")
                _show_installation_summary(counts_before, counts_after)

            print("\n[OK] CCO is ready!")
            print("  All CCO commands are now available globally in Claude Code.")
            print("\n  Next steps:")
            print("  1. Open/Restart Claude Code")
            print("  2. Try: /cco-help or /cco-status")
        else:
            logger.warning("Global setup completed with warnings")
            print("\n[WARNING] Global setup completed with warnings")

        print("=" * 60 + "\n")

        # Return success for scripting
        return 0

    except Exception as e:
        # Non-fatal: Don't break pip install if setup fails
        logger.error("CCO post-install setup failed", exc_info=True)
        print(f"\n[WARNING] CCO post-install setup failed: {e}")
        print("You can manually run setup later")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    post_install()
