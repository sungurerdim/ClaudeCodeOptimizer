"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import json
import re
import subprocess
import sys
from typing import TypedDict

from .config import (
    CCO_MARKER_PATTERNS,
    CLAUDE_DIR,
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


def has_claude_md_standards() -> list[str]:
    """Check which CCO sections exist in CLAUDE.md."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []
    content = claude_md.read_text(encoding="utf-8")
    sections = []
    if "<!-- CCO_STANDARDS_START -->" in content:
        sections.append("CCO Standards")
    return sections


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
    """Remove CCO standards from CLAUDE.md with detailed output."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []

    content = claude_md.read_text(encoding="utf-8")
    removed = []

    # Remove CCO standards marker
    pattern, flags = CCO_MARKER_PATTERNS["standards"]
    if re.search(pattern, content, flags=flags):
        content = re.sub(pattern, "", content, flags=flags)
        removed.append("CCO Standards")

    if removed:
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md.write_text(content, encoding="utf-8")
        if verbose:
            for section in removed:
                print(f"  - {section}")

    return removed


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
    total_files = sum(len(f) for f in files.values())
    total = (1 if method else 0) + total_files + len(standards) + (1 if statusline else 0)

    return {
        "method": method,
        "files": files,
        "standards": standards,
        "statusline": statusline,
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

    if items["statusline"]:
        print("Statusline:")
        print("  - statusline.js")
        print("  - settings.json (statusLine config)")
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

    if items["statusline"]:
        print("Removing statusline...")
        remove_statusline()
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
