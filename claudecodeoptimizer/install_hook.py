"""CCO Setup - Install commands, agents, and standards to ~/.claude/"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from .config import (
    AGENTS_DIR,
    CCO_PERMISSIONS_MARKER,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    COMMANDS_DIR,
    SEPARATOR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    get_content_path,
    get_standards_breakdown,
)

# Legacy keys that may exist from older CCO versions
# These are cleaned during reinstall for a fresh start
LEGACY_SETTINGS_KEYS = [
    "_cco_managed",
    "_cco_version",
    "_cco_installed",
    "cco_config",
    "ccoSettings",
]

# Valid options for local mode
STATUSLINE_MODES = ("full", "minimal")
PERMISSION_LEVELS = ("safe", "balanced", "permissive", "full")


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def clean_previous_installation(verbose: bool = True) -> dict[str, int]:
    """Remove all traces of previous CCO installation.

    This ensures a clean reinstall by removing:
    - All cco-*.md files in commands/ and agents/
    - CCO markers from CLAUDE.md
    - CCO-related keys from settings.json
    - CCO statusline.js (if it's a CCO file)

    Returns:
        Dictionary with counts of removed items
    """
    removed = {"commands": 0, "agents": 0, "standards": 0, "settings_keys": 0, "statusline": 0}

    # 1. Remove all cco-*.md files from commands/
    if COMMANDS_DIR.exists():
        for f in COMMANDS_DIR.glob("cco-*.md"):
            f.unlink()
            removed["commands"] += 1

    # 2. Remove all cco-*.md files from agents/
    if AGENTS_DIR.exists():
        for f in AGENTS_DIR.glob("cco-*.md"):
            f.unlink()
            removed["agents"] += 1

    # 3. Remove CCO markers from CLAUDE.md
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        content, count = _remove_all_cco_markers(content)
        if count > 0:
            content = re.sub(r"\n{3,}", "\n\n", content)
            claude_md.write_text(content, encoding="utf-8")
            removed["standards"] = count

    # 4. Clean CCO-related keys from settings.json
    if SETTINGS_FILE.exists():
        try:
            settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            keys_removed = 0

            # Remove legacy CCO keys
            for key in LEGACY_SETTINGS_KEYS:
                if key in settings:
                    del settings[key]
                    keys_removed += 1

            # Remove CCO permissions marker
            if CCO_PERMISSIONS_MARKER in settings:
                del settings[CCO_PERMISSIONS_MARKER]
                keys_removed += 1

            if keys_removed > 0:
                SETTINGS_FILE.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
                removed["settings_keys"] = keys_removed
        except json.JSONDecodeError:
            pass

    # 5. Remove CCO statusline.js (check if it's a CCO file)
    if STATUSLINE_FILE.exists():
        try:
            content = STATUSLINE_FILE.read_text(encoding="utf-8")
            if "CCO Statusline" in content:
                STATUSLINE_FILE.unlink()
                removed["statusline"] = 1
        except (OSError, UnicodeDecodeError):
            pass

    total = sum(removed.values())
    if verbose and total > 0:
        print("Cleaning previous installation...")
        if removed["commands"]:
            print(f"  - Removed {removed['commands']} command(s)")
        if removed["agents"]:
            print(f"  - Removed {removed['agents']} agent(s)")
        if removed["standards"]:
            print(f"  - Removed {removed['standards']} CLAUDE.md section(s)")
        if removed["settings_keys"]:
            print(f"  - Cleaned {removed['settings_keys']} legacy setting(s)")
        if removed["statusline"]:
            print("  - Removed old statusline.js")
        print()

    return removed


def setup_statusline(verbose: bool = True) -> bool:
    """Copy statusline.js to ~/.claude/ and configure settings.json.

    Returns:
        True if statusline was installed/updated
    """
    src = get_content_path("statusline") / "full.js"
    if not src.exists():
        if verbose:
            print("  (statusline source not found)")
        return False

    # Copy statusline.js
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, STATUSLINE_FILE)

    # Update settings.json with statusLine config
    settings: dict = {}
    if SETTINGS_FILE.exists():
        try:
            settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    # Set statusLine with dynamic path: local first, then global fallback
    # This allows projects to override the global statusline
    settings["statusLine"] = {
        "type": "command",
        "command": 'node "$(test -f .claude/statusline.js && echo .claude/statusline.js || echo ~/.claude/statusline.js)"',
    }

    SETTINGS_FILE.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if verbose:
        print("  + statusline.js (Full mode)")
        print("  + settings.json (statusLine configured)")

    return True


def has_statusline() -> bool:
    """Check if CCO statusline is installed."""
    if not STATUSLINE_FILE.exists():
        return False
    content = STATUSLINE_FILE.read_text(encoding="utf-8")
    return "CCO Statusline" in content


def _setup_content(src_subdir: str, dest_dir: Path, verbose: bool = True) -> list[str]:
    """Copy cco-*.md files from source to destination directory.

    Idempotent: removes existing cco-*.md files before copying new ones.
    Safe for reinstall - always results in fresh content from current version.
    """
    src = get_content_dir() / src_subdir
    if not src.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Remove existing cco-*.md files (idempotent reinstall)
    for old in dest_dir.glob("cco-*.md"):
        old.unlink()
    installed = []
    for f in sorted(src.glob("cco-*.md")):
        shutil.copy2(f, dest_dir / f.name)
        installed.append(f.name)
        if verbose:
            print(f"  + {f.name}")
    return installed


def setup_commands(verbose: bool = True) -> list[str]:
    """Copy cco-*.md commands to ~/.claude/commands/"""
    return _setup_content("commands", COMMANDS_DIR, verbose)


def setup_agents(verbose: bool = True) -> list[str]:
    """Copy cco-*.md agents to ~/.claude/agents/"""
    return _setup_content("agents", AGENTS_DIR, verbose)


def _load_standards() -> str:
    """Load CCO standards from file."""
    standards_file = Path(__file__).parent / "content" / "standards" / "cco-standards.md"
    return standards_file.read_text(encoding="utf-8")


def _remove_all_cco_markers(content: str) -> tuple[str, int]:
    """Remove ALL CCO markers from content for backward compatibility.

    Uses universal pattern to match any CCO marker regardless of name.
    Ensures clean upgrade from any previous CCO version.

    Returns:
        Tuple of (cleaned_content, removed_count)
    """
    pattern, flags = CCO_UNIVERSAL_PATTERN
    matches = re.findall(pattern, content, flags=flags)
    cleaned = re.sub(pattern, "", content, flags=flags)
    return cleaned, len(matches)


def setup_claude_md(verbose: bool = True) -> dict[str, int]:
    """Add CCO Standards to ~/.claude/CLAUDE.md

    For backward compatibility:
    1. Remove ALL existing CCO markers (any name/format)
    2. Append fresh standards content

    Returns:
        Dictionary with installed counts (universal, ai_specific, cco_specific)
    """
    standards = _load_standards()
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    action = "created"
    removed_count = 0

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")

        # Remove ALL CCO markers for backward compatibility
        content, removed_count = _remove_all_cco_markers(content)

        # Append fresh standards
        content = content.rstrip() + "\n\n" + standards
        action = "updated" if removed_count > 0 else "appended"
    else:
        content = standards

    content = re.sub(r"\n{3,}", "\n\n", content)
    claude_md.write_text(content, encoding="utf-8")

    breakdown = get_standards_breakdown()
    installed = breakdown["universal"] + breakdown["ai_specific"] + breakdown["cco_specific"]

    if verbose:
        if removed_count > 0:
            print(
                f"  CLAUDE.md: {installed} standards {action} (cleaned {removed_count} old marker(s))"
            )
        else:
            print(f"  CLAUDE.md: {installed} standards {action}")

    return {
        "universal": breakdown["universal"],
        "ai_specific": breakdown["ai_specific"],
        "cco_specific": breakdown["cco_specific"],
    }


# ============================================================================
# LOCAL MODE FUNCTIONS (for cco-tune)
# ============================================================================


def setup_local_statusline(project_path: Path, mode: str, verbose: bool = True) -> bool:
    """Copy statusline to project's .claude/ directory.

    Args:
        project_path: Project root directory
        mode: 'full' or 'minimal'
        verbose: Print progress messages

    Returns:
        True if statusline was installed/updated
    """
    if mode not in STATUSLINE_MODES:
        if verbose:
            print(f"  Error: Invalid mode '{mode}'. Use: {', '.join(STATUSLINE_MODES)}")
        return False

    src = get_content_path("statusline") / f"{mode}.js"
    if not src.exists():
        if verbose:
            print(f"  Error: Statusline source not found: {src}")
        return False

    # Create .claude/ directory and copy statusline
    local_claude = project_path / ".claude"
    local_claude.mkdir(parents=True, exist_ok=True)
    dest = local_claude / "statusline.js"
    shutil.copy2(src, dest)

    # Update local settings.json with statusLine config
    settings_file = local_claude / "settings.json"
    settings: dict = {}
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    # Local statusline - direct path, no fallback
    settings["statusLine"] = {
        "type": "command",
        "command": "node .claude/statusline.js",
    }

    settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if verbose:
        print(f"  + .claude/statusline.js ({mode} mode)")
        print("  + .claude/settings.json (statusLine configured)")

    return True


def setup_local_permissions(project_path: Path, level: str, verbose: bool = True) -> bool:
    """Set permissions in project's .claude/settings.json.

    Args:
        project_path: Project root directory
        level: 'safe', 'balanced', 'permissive', or 'full'
        verbose: Print progress messages

    Returns:
        True if permissions were set
    """
    if level not in PERMISSION_LEVELS:
        if verbose:
            print(f"  Error: Invalid level '{level}'. Use: {', '.join(PERMISSION_LEVELS)}")
        return False

    src = get_content_path("permissions") / f"{level}.json"
    if not src.exists():
        if verbose:
            print(f"  Error: Permissions source not found: {src}")
        return False

    # Load permissions from source
    try:
        perm_data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        if verbose:
            print(f"  Error: Invalid permissions JSON: {e}")
        return False

    # Create .claude/ directory
    local_claude = project_path / ".claude"
    local_claude.mkdir(parents=True, exist_ok=True)

    # Load or create settings.json
    settings_file = local_claude / "settings.json"
    settings: dict = {}
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    # Set permissions (keep _meta for tracking)
    settings["permissions"] = perm_data.get("permissions", {})
    settings[CCO_PERMISSIONS_MARKER] = True

    settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if verbose:
        print(f"  + .claude/settings.json (permissions: {level})")

    return True


def _run_local_mode(args: argparse.Namespace) -> int:
    """Handle --local mode for cco-tune integration."""
    project_path = Path(args.local).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        return 1

    if not project_path.is_dir():
        print(f"Error: Not a directory: {project_path}", file=sys.stderr)
        return 1

    print(f"\nCCO Local Setup: {project_path}\n")

    success = True

    if args.statusline:
        print("Statusline:")
        if not setup_local_statusline(project_path, args.statusline):
            success = False
        print()

    if args.permissions:
        print("Permissions:")
        if not setup_local_permissions(project_path, args.permissions):
            success = False
        print()

    if not args.statusline and not args.permissions:
        # Just create .claude/ directory
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {local_claude}/")
        print()

    if success:
        print("Local setup complete.")
    else:
        print("Local setup completed with errors.", file=sys.stderr)

    return 0 if success else 1


def post_install() -> int:
    """CLI entry point for cco-setup."""
    parser = argparse.ArgumentParser(
        prog="cco-setup",
        description="Install CCO commands, agents, and standards to ~/.claude/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Local mode (for cco-tune):
  cco-setup --local . --statusline full --permissions balanced

Statusline modes: full, minimal
Permission levels: safe, balanced, permissive, full
""",
    )

    parser.add_argument(
        "--local",
        metavar="PATH",
        help="Project path for local setup (used by /cco-tune)",
    )
    parser.add_argument(
        "--statusline",
        choices=STATUSLINE_MODES,
        help="Statusline mode (requires --local)",
    )
    parser.add_argument(
        "--permissions",
        choices=PERMISSION_LEVELS,
        help="Permission level (requires --local)",
    )

    args = parser.parse_args()

    # Local mode - used by cco-tune
    if args.local:
        return _run_local_mode(args)

    # Validate: --statusline and --permissions require --local
    if args.statusline or args.permissions:
        parser.error("--statusline and --permissions require --local")

    # Global mode - default behavior
    try:
        print("\n" + SEPARATOR)
        print("CCO Setup")
        print(SEPARATOR)
        print(f"\nLocation: {CLAUDE_DIR}\n")

        # Step 1: Clean previous installation (ensures fresh state)
        clean_previous_installation()

        # Step 2: Install commands
        print("Commands:")
        cmds = setup_commands()
        if not cmds:
            print("  (none)")
        print()

        # Agents
        print("Agents:")
        agents = setup_agents()
        if not agents:
            print("  (none)")
        print()

        # Standards
        print("Standards:")
        standards = setup_claude_md()
        print()

        # Summary
        installed = standards["universal"] + standards["ai_specific"] + standards["cco_specific"]
        breakdown = get_standards_breakdown()
        print(SEPARATOR)
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents, {installed} standards")
        print(
            f"  Universal: {standards['universal']} | AI-Specific: {standards['ai_specific']} | CCO-Specific: {standards['cco_specific']}"
        )
        print(
            f"Available: +{breakdown['project_specific']} project-specific standards via /cco-tune"
        )
        print(SEPARATOR)
        print()
        print("Restart Claude Code for changes to take effect.")
        print()
        print("Next: /cco-tune to configure statusline, permissions, and project settings")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())
