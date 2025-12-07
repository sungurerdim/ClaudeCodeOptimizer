"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

from .config import (
    CCO_PERMISSIONS_MARKER,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    LOCAL_SETTINGS_FILE,
    LOCAL_STATUSLINE_FILE,
    SEPARATOR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    SUBPROCESS_TIMEOUT,
    get_cco_agents,
    get_cco_commands,
)


class RemovalItems(TypedDict):
    """Type-safe container for removal items."""

    method: str | None
    files: dict[str, list[str]]
    standards: list[str]
    statusline: bool
    permissions: bool
    local_statusline: bool
    local_permissions: bool
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
                [cmd] + args, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT
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
    """Remove CCO permissions from settings.json."""
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
                location = "local" if settings_file == LOCAL_SETTINGS_FILE else "global"
                print(f"  - settings.json ({location} permissions removed)")

        return removed
    except json.JSONDecodeError:
        return False


def has_local_cco_statusline() -> bool:
    """Check if CCO statusline is installed locally."""
    if not LOCAL_STATUSLINE_FILE.exists():
        return False
    content = LOCAL_STATUSLINE_FILE.read_text(encoding="utf-8")
    return "CCO Statusline" in content


def remove_local_statusline(verbose: bool = True) -> bool:
    """Remove local CCO statusline.js."""
    if not has_local_cco_statusline():
        return False

    LOCAL_STATUSLINE_FILE.unlink()
    if verbose:
        print("  - .claude/statusline.js (local)")
    return True


def has_claude_md_standards() -> list[str]:
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


def remove_claude_md_standards(verbose: bool = True) -> list[str]:
    """Remove ALL CCO content from CLAUDE.md.

    Uses universal pattern to remove any CCO marker for backward compatibility.
    Ensures complete cleanup regardless of marker names from previous versions.
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
        result = subprocess.run(cmds[method], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _collect_removal_items() -> RemovalItems:
    """Collect all items to be removed."""
    method = detect_install_method()
    files = list_cco_files()
    standards = has_claude_md_standards()
    statusline = has_cco_statusline()
    permissions = has_cco_permissions(SETTINGS_FILE)
    local_statusline = has_local_cco_statusline()
    local_permissions = has_cco_permissions(LOCAL_SETTINGS_FILE)
    total_files = sum(len(f) for f in files.values())
    total = (
        (1 if method else 0)
        + total_files
        + len(standards)
        + (1 if statusline else 0)
        + (1 if permissions else 0)
        + (1 if local_statusline else 0)
        + (1 if local_permissions else 0)
    )

    return {
        "method": method,
        "files": files,
        "standards": standards,
        "statusline": statusline,
        "permissions": permissions,
        "local_statusline": local_statusline,
        "local_permissions": local_permissions,
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
        ("CLAUDE.md sections", items["standards"]),
    ]
    for title, category_items in categories:
        if category_items:
            print(f"{title}:")
            for item in category_items:
                print(f"  - {item}")
            print()

    if items["statusline"] or items["permissions"]:
        print("Global (~/.claude/):")
        if items["statusline"]:
            print("  - statusline.js")
            print("  - settings.json (statusLine config)")
        if items["permissions"]:
            print("  - settings.json (permissions)")
        print()

    if items["local_statusline"] or items["local_permissions"]:
        print("Local (./.claude/):")
        if items["local_statusline"]:
            print("  - statusline.js")
        if items["local_permissions"]:
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

    if items["standards"]:
        print("Removing CLAUDE.md sections...")
        remove_claude_md_standards()
        print()

    if items["statusline"] or items["permissions"]:
        print("Removing global settings...")
        if items["statusline"]:
            remove_statusline()
        if items["permissions"]:
            remove_permissions(SETTINGS_FILE)
        print()

    if items["local_statusline"] or items["local_permissions"]:
        print("Removing local settings...")
        if items["local_statusline"]:
            remove_local_statusline()
        if items["local_permissions"]:
            remove_permissions(LOCAL_SETTINGS_FILE)
        print()

    print(SEPARATOR)
    print("CCO removed successfully.")
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
