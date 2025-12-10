"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

from .config import (
    CCO_PERMISSIONS_MARKER,
    CCO_RULE_FILES,
    CCO_RULE_NAMES,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    OLD_RULES_ROOT,
    RULES_DIR,
    SEPARATOR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    SUBPROCESS_TIMEOUT,
    get_cco_agents,
    get_cco_commands,
)


class RemovalItems(TypedDict):
    """Type-safe container for removal items.

    Note: cco-remove only handles global ~/.claude/ files.
    Local project files (./.claude/) are managed by cco-tune.
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
    """Remove CCO statusline.js and clean settings.json."""
    removed = False

    # Remove statusline.js if it's a CCO file
    if has_cco_statusline():
        STATUSLINE_FILE.unlink()
        removed = True
        if verbose:
            print("  - statusline.js")

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
    # Check for new v2.x structure: ~/.claude/rules/cco/{core,ai,tools}.md
    return any((RULES_DIR / f).exists() for f in CCO_RULE_NAMES)


def has_rules_dir_old() -> bool:
    """Check if any old CCO rule files exist in ~/.claude/rules/ (v1.x backward compat)."""
    if not OLD_RULES_ROOT.exists():
        return False
    # Check for old v1.x structure: ~/.claude/rules/cco-{core,ai,tools,adaptive}.md
    old_files = list(CCO_RULE_FILES) + ["cco-adaptive.md"]
    return any((OLD_RULES_ROOT / f).exists() for f in old_files)


def remove_rules_dir(verbose: bool = True) -> bool:
    """Remove CCO rule files from ~/.claude/rules/cco/ (v2.x)."""
    if not RULES_DIR.exists():
        return False

    removed_count = 0
    for rule_name in CCO_RULE_NAMES:
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
    old_files = list(CCO_RULE_FILES) + ["cco-adaptive.md"]
    for rule_file in old_files:
        rule_path = OLD_RULES_ROOT / rule_file
        if rule_path.exists():
            rule_path.unlink()
            removed_count += 1

    if removed_count == 0:
        return False

    if verbose:
        print(f"  - rules/ root ({removed_count} old CCO files)")
    return True


def has_claude_md_rules() -> list[str]:
    """Check which CCO sections exist in CLAUDE.md.

    Uses universal pattern to detect ANY CCO marker for backward compatibility.
    """
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []
    content = claude_md.read_text(encoding="utf-8")

    # Use universal pattern to find all CCO markers
    pattern, flags = CCO_UNIVERSAL_PATTERN
    matches = re.findall(pattern, content, flags=flags)
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
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []

    content = claude_md.read_text(encoding="utf-8")

    # Use universal pattern to remove ALL CCO markers
    pattern, flags = CCO_UNIVERSAL_PATTERN
    matches = re.findall(pattern, content, flags=flags)

    if matches:
        content = re.sub(pattern, "", content, flags=flags)
        content = re.sub(r"\n{3,}", "\n\n", content)
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
            cmds[method], capture_output=True, text=True, timeout=30, shell=False
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _collect_removal_items() -> RemovalItems:
    """Collect all items to be removed.

    Note: Only collects global ~/.claude/ items.
    Local project files are managed by cco-tune.
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


def _display_removal_plan(items: RemovalItems) -> None:
    """Display what will be removed."""
    print("\n" + SEPARATOR)
    print("CCO Uninstall")
    print(SEPARATOR)
    print(f"\nLocation: {CLAUDE_DIR}\n")

    if items["method"]:
        print("Package:")
        print(f"  claudecodeoptimizer ({items['method']})")
        print()

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

    if items["rules_dir"] or items["rules_dir_old"]:
        print("Rules directory:")
        if items["rules_dir"]:
            print("  - ~/.claude/rules/cco/ (v2.x)")
        if items["rules_dir_old"]:
            print("  - ~/.claude/rules/ root (v1.x old files)")
        print()

    if items["statusline"] or items["permissions"]:
        print("Settings (~/.claude/):")
        if items["statusline"]:
            print("  - statusline.js")
            print("  - settings.json (statusLine config)")
        if items["permissions"]:
            print("  - settings.json (permissions)")
        print()

    print(SEPARATOR)
    print(f"Total: {items['total']} items to remove")
    print(SEPARATOR)
    print()


def _execute_removal(items: RemovalItems) -> None:
    """Execute the removal of all items."""
    if items["method"]:
        print("Removing package...")
        if uninstall_package(items["method"]):
            print("  Package removed")
        else:
            print("  Failed to remove package")
        print()

    if items["total_files"]:
        print("Removing files...")
        remove_cco_files()
        print()

    if items["rules"]:
        print("Removing CLAUDE.md sections...")
        remove_claude_md_rules()
        print()

    if items["rules_dir"] or items["rules_dir_old"]:
        print("Removing rules directory...")
        if items["rules_dir"]:
            remove_rules_dir()
        if items["rules_dir_old"]:
            remove_rules_dir_old()
        print()

    if items["statusline"] or items["permissions"]:
        print("Removing settings...")
        if items["statusline"]:
            remove_statusline()
        if items["permissions"]:
            remove_permissions(SETTINGS_FILE)
        print()

    print(SEPARATOR)
    print("CCO removed successfully.")
    print()
    print("Note: Local project files (./.claude/) are managed by /cco-tune.")
    print(SEPARATOR)
    print()


def main() -> int:
    """CLI entry point."""
    try:
        items = _collect_removal_items()

        if items["total"] == 0:
            print("CCO is not installed.")
            return 0

        _display_removal_plan(items)

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
