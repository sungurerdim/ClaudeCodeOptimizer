"""User interface functions for CCO removal."""

from .config import CLAUDE_DIR, SEPARATOR


def print_removal_header() -> None:
    """Print header for removal plan."""
    print("\n" + SEPARATOR)
    print("CCO Uninstall")
    print(SEPARATOR)
    print(f"\nLocation: {CLAUDE_DIR}\n")


def display_package_info(method: str | None) -> None:
    """Display package information.

    Args:
        method: Package manager method (pipx, uv, pip) or None if not detected.
    """
    if method:
        print("Package:")
        print(f"  claudecodeoptimizer ({method})")
        print()


def display_file_categories(commands: list[str], agents: list[str], rules: list[str]) -> None:
    """Display file categories (commands, agents, CLAUDE.md sections).

    Args:
        commands: List of command files.
        agents: List of agent files.
        rules: List of CLAUDE.md sections.
    """
    categories = [
        ("Commands", commands),
        ("Agents", agents),
        ("CLAUDE.md sections", rules),
    ]
    for title, category_items in categories:
        if category_items:
            print(f"{title}:")
            for item in category_items:
                print(f"  - {item}")
            print()


def display_rules_directories(rules_dir: bool, rules_dir_old: bool) -> None:
    """Display rules directories to be removed.

    Args:
        rules_dir: Whether current rules directory has files to remove.
        rules_dir_old: Whether old rules directory has files to remove.
    """
    if rules_dir or rules_dir_old:
        print("Rules directory:")
        if rules_dir:
            print("  - ~/.claude/rules/cco/")
        if rules_dir_old:
            print("  - ~/.claude/rules/ root (old files)")
        print()


def display_settings(statusline: bool, permissions: bool) -> None:
    """Display settings to be removed.

    Args:
        statusline: Whether statusline is installed.
        permissions: Whether permissions are installed.
    """
    if statusline or permissions:
        print("Settings (~/.claude/):")
        if statusline:
            print("  - cco-statusline.js")
            print("  - settings.json (statusLine config)")
        if permissions:
            print("  - settings.json (permissions)")
        print()


def display_removal_plan(
    method: str | None,
    commands: list[str],
    agents: list[str],
    rules: list[str],
    rules_dir: bool,
    rules_dir_old: bool,
    statusline: bool,
    permissions: bool,
    total: int,
) -> None:
    """Display what will be removed.

    Args:
        method: Package manager method or None.
        commands: List of command files.
        agents: List of agent files.
        rules: List of CLAUDE.md sections.
        rules_dir: Whether current rules directory has files to remove.
        rules_dir_old: Whether old rules directory has files to remove.
        statusline: Whether statusline is installed.
        permissions: Whether permissions are installed.
        total: Total number of items to remove.
    """
    print_removal_header()
    display_package_info(method)
    display_file_categories(commands, agents, rules)
    display_rules_directories(rules_dir, rules_dir_old)
    display_settings(statusline, permissions)

    print(SEPARATOR)
    print(f"Total: {total} items to remove")
    print(SEPARATOR)
    print()
