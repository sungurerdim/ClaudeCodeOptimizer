"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

from .config import (
    ALL_RULE_NAMES,
    CCO_PERMISSIONS_MARKER,
    CCO_UNIVERSAL_PATTERN_COMPILED,
    CLAUDE_DIR,
    MAX_CLAUDE_MD_SIZE,
    OLD_RULE_FILES,
    OLD_RULES_ROOT,
    RULES_DIR,
    SEPARATOR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    SUBPROCESS_TIMEOUT,
    SUBPROCESS_TIMEOUT_PACKAGE,
    get_cco_agents,
    get_cco_commands,
)


class RemovalItems(TypedDict):
    """Type-safe container for removal items.

    Note: cco-remove only handles global ~/.claude/ files.
    Local project files (./.claude/) are managed by cco-config.
    """

    method: str | None
    files: dict[str, list[str]]
    rules: list[str]
    rules_dir: bool
    rules_dir_old: bool  # v1.x backward compat: ~/.claude/rules/cco-*.md
    statusline: bool
    permissions: bool
    total_files: int
    total: int


def detect_install_method() -> str | None:
    """Detect pip/pipx/uv installation."""
    for cmd, args in [
        ("pipx", ["list"]),
        ("uv", ["tool", "list"]),
        ("pip", ["show", "claudecodeoptimizer"]),
    ]:
        try:
            result = subprocess.run(
                [cmd] + args,
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
                shell=False,
            )
            if "claudecodeoptimizer" in result.stdout:
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return None


def list_cco_files() -> dict[str, list[str]]:
    """List CCO files in ~/.claude/ by category."""
    return {
        "commands": sorted(f.name for f in get_cco_commands()),
        "agents": sorted(f.name for f in get_cco_agents()),
    }


def has_cco_statusline() -> bool:
    """Check if CCO statusline is installed."""
    if not STATUSLINE_FILE.exists():
        return False
    content = STATUSLINE_FILE.read_text(encoding="utf-8")
    return "CCO Statusline" in content


def remove_statusline(verbose: bool = True) -> bool:
    """Remove CCO cco-statusline.js and clean settings.json."""
    removed = False

    # Remove cco-statusline.js if it's a CCO file
    if has_cco_statusline():
        STATUSLINE_FILE.unlink()
        removed = True
        if verbose:
            print("  - cco-statusline.js")

    # Clean statusLine from settings.json
    if SETTINGS_FILE.exists():
        try:
            settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            if "statusLine" in settings:
                del settings["statusLine"]
                SETTINGS_FILE.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
                if verbose:
                    print("  - settings.json (statusLine removed)")
                removed = True
        except json.JSONDecodeError:
            pass

    return removed


def has_cco_permissions(settings_file: Path = SETTINGS_FILE) -> bool:
    """Check if CCO permissions are installed in settings.json."""
    if not settings_file.exists():
        return False
    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        permissions = settings.get("permissions", {})
        # Check for CCO marker or _meta field (from permissions JSON)
        if CCO_PERMISSIONS_MARKER in settings:
            return True
        if isinstance(permissions, dict) and "_meta" in permissions:
            return True
    except json.JSONDecodeError:
        pass
    return False


def remove_permissions(settings_file: Path = SETTINGS_FILE, verbose: bool = True) -> bool:
    """Remove CCO permissions from settings.json.

    Args:
        settings_file: Path to settings.json file. Defaults to global settings.
        verbose: If True, print progress messages.

    Returns:
        True if permissions were removed, False otherwise.
    """
    if not settings_file.exists():
        return False

    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        removed = False

        # Remove permissions key
        if "permissions" in settings:
            del settings["permissions"]
            removed = True

        # Remove CCO marker
        if CCO_PERMISSIONS_MARKER in settings:
            del settings[CCO_PERMISSIONS_MARKER]
            removed = True

        if removed:
            settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
            if verbose:
                print("  - settings.json (permissions removed)")

        return removed
    except json.JSONDecodeError:
        return False


def has_rules_dir() -> bool:
    """Check if any CCO rule files exist in ~/.claude/rules/cco/ (v2.x)."""
    if not RULES_DIR.exists():
        return False
    # Check for new v2.x structure: ~/.claude/rules/cco/{core,ai}.md
    # Also check for old intermediate files: tools.md, adaptive.md
    return any((RULES_DIR / f).exists() for f in ALL_RULE_NAMES)


def has_rules_dir_old() -> bool:
    """Check if any old CCO rule files exist in ~/.claude/rules/ (v1.x backward compat)."""
    if not OLD_RULES_ROOT.exists():
        return False
    # Check for old v1.x structure: ~/.claude/rules/cco-{core,ai,tools,adaptive}.md
    # Includes cco-tools.md which existed in intermediate versions
    return any((OLD_RULES_ROOT / f).exists() for f in OLD_RULE_FILES)


def remove_rules_dir(verbose: bool = True) -> bool:
    """Remove CCO rule files from ~/.claude/rules/cco/ (v2.x)."""
    if not RULES_DIR.exists():
        return False

    removed_count = 0
    # Include all possible rule files from any CCO version
    # CCO_RULE_NAMES has current files, plus old files from intermediate versions
    for rule_name in ALL_RULE_NAMES:
        rule_path = RULES_DIR / rule_name
        if rule_path.exists():
            rule_path.unlink()
            removed_count += 1

    # Remove empty cco/ directory
    if RULES_DIR.exists() and not any(RULES_DIR.iterdir()):
        RULES_DIR.rmdir()

    if removed_count == 0:
        return False

    if verbose:
        print(f"  - rules/cco/ ({removed_count} files)")
    return True


def remove_rules_dir_old(verbose: bool = True) -> bool:
    """Remove old CCO rule files from ~/.claude/rules/ root (v1.x backward compat)."""
    if not OLD_RULES_ROOT.exists():
        return False

    removed_count = 0
    # Include all possible old CCO rule files from any previous version
    for rule_file in OLD_RULE_FILES:
        rule_path = OLD_RULES_ROOT / rule_file
        if rule_path.exists():
            rule_path.unlink()
            removed_count += 1

    if removed_count == 0:
        return False

    if verbose:
        print(f"  - rules/ root ({removed_count} old CCO files)")
    return True


def _read_claude_md() -> str | None:
    """Read CLAUDE.md content if it exists and is not too large.

    Returns:
        File content as string if exists and is safe to read, None otherwise.
    """
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return None

    # Safety: Skip regex on very large files
    if claude_md.stat().st_size > MAX_CLAUDE_MD_SIZE:
        return None

    return claude_md.read_text(encoding="utf-8")


def has_claude_md_rules() -> list[str]:
    """Check which CCO sections exist in CLAUDE.md.

    Uses universal pattern to detect ANY CCO marker for backward compatibility.
    Includes file size check to prevent ReDoS on very large files.
    """
    content = _read_claude_md()
    if content is None:
        # Check if file exists but is too large
        claude_md = CLAUDE_DIR / "CLAUDE.md"
        if claude_md.exists():
            return ["CLAUDE.md (file too large for pattern matching)"]
        return []

    # Use universal pattern to find all CCO markers
    matches = CCO_UNIVERSAL_PATTERN_COMPILED.findall(content)
    if matches:
        return [f"CCO Content ({len(matches)} section(s))"]
    return []


def remove_cco_files(verbose: bool = True) -> dict[str, int]:
    """Remove CCO files with detailed output."""
    removed = {"commands": 0, "agents": 0}
    for key, getter in [("commands", get_cco_commands), ("agents", get_cco_agents)]:
        for f in getter():
            f.unlink()
            removed[key] += 1
            if verbose:
                print(f"  - {f.name}")
    return removed


def remove_claude_md_rules(verbose: bool = True) -> list[str]:
    """Remove ALL CCO content from CLAUDE.md.

    Uses universal pattern to remove any CCO marker for backward compatibility.
    Ensures complete cleanup regardless of marker names from previous versions.

    Args:
        verbose: If True, print progress messages.

    Returns:
        List of removed section descriptions, empty if none found.
    """
    content = _read_claude_md()
    if content is None:
        return []

    # Use universal pattern to remove ALL CCO markers
    matches = CCO_UNIVERSAL_PATTERN_COMPILED.findall(content)

    if matches:
        content = CCO_UNIVERSAL_PATTERN_COMPILED.sub("", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md = CLAUDE_DIR / "CLAUDE.md"
        claude_md.write_text(content, encoding="utf-8")
        if verbose:
            print(f"  - CCO Content ({len(matches)} section(s) removed)")
        return [f"CCO Content ({len(matches)} section(s))"]

    return []


def uninstall_package(method: str) -> bool:
    """Uninstall CCO package."""
    cmds = {
        "pipx": ["pipx", "uninstall", "claudecodeoptimizer"],
        "uv": ["uv", "tool", "uninstall", "claudecodeoptimizer"],
        "pip": ["pip", "uninstall", "-y", "claudecodeoptimizer"],
    }
    try:
        result = subprocess.run(
            cmds[method],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT_PACKAGE,
            shell=False,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


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


def _print_removal_header() -> None:
    """Print header for removal plan."""
    print("\n" + SEPARATOR)
    print("CCO Uninstall")
    print(SEPARATOR)
    print(f"\nLocation: {CLAUDE_DIR}\n")


def _display_package_info(items: RemovalItems) -> None:
    """Display package information.

    Args:
        items: Removal items containing package method
    """
    if items["method"]:
        print("Package:")
        print(f"  claudecodeoptimizer ({items['method']})")
        print()


def _display_file_categories(items: RemovalItems) -> None:
    """Display file categories (commands, agents, CLAUDE.md sections).

    Args:
        items: Removal items containing files and rules
    """
    categories = [
        ("Commands", items["files"]["commands"]),
        ("Agents", items["files"]["agents"]),
        ("CLAUDE.md sections", items["rules"]),
    ]
    for title, category_items in categories:
        if category_items:
            print(f"{title}:")
            for item in category_items:
                print(f"  - {item}")
            print()


def _display_rules_directories(items: RemovalItems) -> None:
    """Display rules directories to be removed.

    Args:
        items: Removal items containing rules_dir and rules_dir_old flags
    """
    if items["rules_dir"] or items["rules_dir_old"]:
        print("Rules directory:")
        if items["rules_dir"]:
            print("  - ~/.claude/rules/cco/ (v2.x)")
        if items["rules_dir_old"]:
            print("  - ~/.claude/rules/ root (v1.x old files)")
        print()


def _display_settings(items: RemovalItems) -> None:
    """Display settings to be removed.

    Args:
        items: Removal items containing statusline and permissions flags
    """
    if items["statusline"] or items["permissions"]:
        print("Settings (~/.claude/):")
        if items["statusline"]:
            print("  - cco-statusline.js")
            print("  - settings.json (statusLine config)")
        if items["permissions"]:
            print("  - settings.json (permissions)")
        print()


def _display_removal_plan(items: RemovalItems) -> None:
    """Display what will be removed."""
    _print_removal_header()
    _display_package_info(items)
    _display_file_categories(items)
    _display_rules_directories(items)
    _display_settings(items)

    print(SEPARATOR)
    print(f"Total: {items['total']} items to remove")
    print(SEPARATOR)
    print()


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


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="cco-remove",
        description="Uninstall CCO files from ~/.claude/",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompt (for scripting)",
    )
    args = parser.parse_args()

    try:
        items = _collect_removal_items()

        if items["total"] == 0:
            print("CCO is not installed.")
            return 0

        _display_removal_plan(items)

        if not args.yes:
            confirm = input("Remove all CCO components? [y/N]: ").strip().lower()
            if confirm != "y":
                print("Cancelled.")
                return 0

        print()
        _execute_removal(items)
        return 0

    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
