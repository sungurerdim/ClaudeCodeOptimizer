"""CCO Uninstall - Uninstall CCO files from ~/.claude/"""

import argparse
import sys
from typing import TypedDict

from ..config import SEPARATOR, SETTINGS_FILE, cli_entrypoint
from ..ui import display_removal_plan
from .detection import (
    detect_install_method,
    has_cco_permissions,
    has_cco_statusline,
    has_claude_md_rules,
    has_rules_dir,
    has_rules_dir_old,
    list_cco_files,
)
from .removal import (
    remove_cco_files,
    remove_claude_md_rules,
    remove_permissions,
    remove_rules_dir,
    remove_rules_dir_old,
    remove_statusline,
    uninstall_package,
)


class RemovalItems(TypedDict):
    """Type-safe container for removal items.

    Note: cco-uninstall only handles global ~/.claude/ files.
    Local project files (./.claude/) are managed by cco-config.
    """

    method: str | None
    files: dict[str, list[str]]
    rules: list[str]
    rules_dir: bool
    rules_dir_old: bool  # Old root-level: ~/.claude/rules/cco-*.md
    statusline: bool
    permissions: bool
    total_files: int
    total: int


def _collect_removal_items() -> RemovalItems:
    """Collect all items to be removed.

    Note: Only collects global ~/.claude/ items.
    Local project files are managed by cco-config.
    """
    method = detect_install_method()
    files = list_cco_files()
    rules = has_claude_md_rules()
    rules_dir = has_rules_dir()
    rules_dir_old = has_rules_dir_old()
    statusline = has_cco_statusline()
    permissions = has_cco_permissions(SETTINGS_FILE)
    total_files = sum(len(f) for f in files.values())
    total = (
        (1 if method else 0)
        + total_files
        + len(rules)
        + (1 if rules_dir else 0)
        + (1 if rules_dir_old else 0)
        + (1 if statusline else 0)
        + (1 if permissions else 0)
    )

    return {
        "method": method,
        "files": files,
        "rules": rules,
        "rules_dir": rules_dir,
        "rules_dir_old": rules_dir_old,
        "statusline": statusline,
        "permissions": permissions,
        "total_files": total_files,
        "total": total,
    }


def _remove_package(items: RemovalItems) -> None:
    """Remove package via package manager.

    Args:
        items: Removal items containing method
    """
    method = items["method"]
    if method is None:
        return

    print("Removing package...")
    if uninstall_package(method):
        print("  Package removed")
    else:
        print("  Failed to remove package")
    print()


def _remove_files(items: RemovalItems) -> None:
    """Remove CCO files (commands and agents).

    Args:
        items: Removal items (unused but kept for consistency)
    """
    print("Removing files...")
    remove_cco_files()
    print()


def _remove_claude_md(items: RemovalItems) -> None:
    """Remove CLAUDE.md sections.

    Args:
        items: Removal items (unused but kept for consistency)
    """
    print("Removing CLAUDE.md sections...")
    remove_claude_md_rules()
    print()


def _remove_rules_directories(items: RemovalItems) -> None:
    """Remove rules directories.

    Args:
        items: Removal items containing rules_dir flags
    """
    print("Removing rules directory...")
    if items["rules_dir"]:
        remove_rules_dir()
    if items["rules_dir_old"]:
        remove_rules_dir_old()
    print()


def _remove_settings(items: RemovalItems) -> None:
    """Remove settings (statusline and permissions).

    Args:
        items: Removal items containing statusline and permissions flags
    """
    print("Removing settings...")
    if items["statusline"]:
        remove_statusline()
    if items["permissions"]:
        remove_permissions(SETTINGS_FILE)
    print()


def _execute_removal(items: RemovalItems) -> None:
    """Execute the removal of all items."""
    operations = [
        (_remove_package, items["method"]),
        (_remove_files, items["total_files"]),
        (_remove_claude_md, items["rules"]),
        (_remove_rules_directories, items["rules_dir"] or items["rules_dir_old"]),
        (_remove_settings, items["statusline"] or items["permissions"]),
    ]

    for operation, condition in operations:
        if condition:
            operation(items)

    print(SEPARATOR)
    print("CCO removed successfully.")
    print()
    print("Note: Local project files (./.claude/) are managed by /cco-config.")
    print(SEPARATOR)
    print()


@cli_entrypoint
def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="cco-uninstall",
        description="Uninstall CCO files from ~/.claude/",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompt (for scripting)",
    )
    args = parser.parse_args()

    items = _collect_removal_items()

    if items["total"] == 0:
        print("CCO is not installed.")
        return 0

    display_removal_plan(
        items["method"],
        items["files"]["commands"],
        items["files"]["agents"],
        items["rules"],
        items["rules_dir"],
        items["rules_dir_old"],
        items["statusline"],
        items["permissions"],
        items["total"],
    )

    if not args.yes:
        confirm = input("Remove all CCO components? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return 0

    print()
    _execute_removal(items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
