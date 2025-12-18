"""CCO Uninstall - Removal functions for installed components."""

import re
import subprocess
from pathlib import Path

from ..config import (
    ALL_RULE_NAMES,
    CCO_PERMISSIONS_MARKER,
    CLAUDE_DIR,
    OLD_RULE_FILES,
    OLD_RULES_ROOT,
    RULES_DIR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    SUBPROCESS_TIMEOUT_PACKAGE,
    get_cco_agents,
    get_cco_commands,
    load_json_file,
    save_json_file,
)
from ..operations import remove_all_cco_markers
from .detection import _read_claude_md, has_cco_statusline


def remove_statusline(verbose: bool = True) -> bool:
    """Remove CCO cco-statusline.js and clean settings.json."""
    removed = False

    # Remove cco-statusline.js if it's a CCO file
    if has_cco_statusline():
        STATUSLINE_FILE.unlink(missing_ok=True)
        removed = True
        if verbose:
            print("  - cco-statusline.js")

    # Clean statusLine from settings.json
    if SETTINGS_FILE.exists():
        settings = load_json_file(SETTINGS_FILE)
        if "statusLine" in settings:
            del settings["statusLine"]
            save_json_file(SETTINGS_FILE, settings)
            if verbose:
                print("  - settings.json (statusLine removed)")
            removed = True

    return removed


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

    settings = load_json_file(settings_file)
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
        save_json_file(settings_file, settings)
        if verbose:
            print("  - settings.json (permissions removed)")

    return removed


def remove_rules_dir(verbose: bool = True) -> bool:
    """Remove CCO rule files from ~/.claude/rules/cco/."""
    if not RULES_DIR.exists():
        return False

    removed_count = 0
    # Include all possible rule files
    for rule_name in ALL_RULE_NAMES:
        rule_path = RULES_DIR / rule_name
        if rule_path.exists():
            rule_path.unlink(missing_ok=True)
            removed_count += 1

    # Remove empty cco/ directory
    try:
        if RULES_DIR.exists() and not any(RULES_DIR.iterdir()):
            RULES_DIR.rmdir()
    except OSError:
        pass  # Directory not empty or already removed

    if removed_count == 0:
        return False

    if verbose:
        print(f"  - rules/cco/ ({removed_count} files)")
    return True


def remove_rules_dir_old(verbose: bool = True) -> bool:
    """Remove old CCO rule files from ~/.claude/rules/ root."""
    if not OLD_RULES_ROOT.exists():
        return False

    removed_count = 0
    # Include all old root-level CCO rule files
    for rule_file in OLD_RULE_FILES:
        rule_path = OLD_RULES_ROOT / rule_file
        if rule_path.exists():
            rule_path.unlink(missing_ok=True)
            removed_count += 1

    if removed_count == 0:
        return False

    if verbose:
        print(f"  - rules/ root ({removed_count} old CCO files)")
    return True


def remove_cco_files(verbose: bool = True) -> dict[str, int]:
    """Remove CCO files with detailed output."""
    removed = {"commands": 0, "agents": 0}
    for key, getter in [("commands", get_cco_commands), ("agents", get_cco_agents)]:
        for f in getter():
            f.unlink(missing_ok=True)
            removed[key] += 1
            if verbose:
                print(f"  - {f.name}")
    return removed


def remove_claude_md_rules(verbose: bool = True) -> list[str]:
    """Remove ALL CCO content from CLAUDE.md.

    Uses universal pattern to remove any CCO marker.
    Ensures complete cleanup regardless of marker names.

    Args:
        verbose: If True, print progress messages.

    Returns:
        List of removed section descriptions, empty if none found.
    """
    content = _read_claude_md()
    if content is None:
        return []

    # Use universal pattern to remove ALL CCO markers
    content, count = remove_all_cco_markers(content)

    if count > 0:
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md = CLAUDE_DIR / "CLAUDE.md"
        claude_md.write_text(content, encoding="utf-8")
        if verbose:
            print(f"  - CCO Content ({count} section(s) removed)")
        return [f"CCO Content ({count} section(s))"]

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
