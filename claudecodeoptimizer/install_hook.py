"""CCO Setup - Install commands, agents, and rules to ~/.claude/"""

import argparse
import json
import re
import shutil
import sys
import warnings
from pathlib import Path
from typing import Any

from .config import (
    AGENTS_DIR,
    CCO_PERMISSIONS_MARKER,
    CCO_RULE_FILES,
    CCO_RULE_NAMES,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    COMMANDS_DIR,
    OLD_RULES_ROOT,
    RULES_DIR,
    SEPARATOR,
    get_content_path,
    get_rules_breakdown,
)

# Valid options for local mode
STATUSLINE_MODES = ("cco-full", "cco-minimal")
PERMISSION_LEVELS = ("safe", "balanced", "permissive", "full")


def _load_settings_json(settings_file: Path) -> dict[str, Any]:
    """Load settings.json, returning empty dict if missing or invalid.

    Args:
        settings_file: Path to settings.json file

    Returns:
        Parsed JSON dict, or empty dict if file missing/invalid
    """
    if not settings_file.exists():
        return {}
    try:
        return json.loads(settings_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _is_safe_path(target: Path) -> bool:
    """Check if target path is within home directory or current working directory.

    Security measure to prevent path traversal attacks in --local mode.

    Args:
        target: Path to validate

    Returns:
        True if path is safe (within home or cwd)
    """
    home = Path.home()
    cwd = Path.cwd().resolve()
    return target == home or target == cwd or home in target.parents or cwd in target.parents


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def _remove_command_files(commands_dir: Path, removed: dict[str, int]) -> None:
    """Remove all cco-*.md files from commands directory.

    Args:
        commands_dir: Path to commands directory
        removed: Dictionary to update with count of removed items
    """
    if commands_dir.exists():
        for f in commands_dir.glob("cco-*.md"):
            f.unlink()
            removed["commands"] += 1


def _remove_agent_files(agents_dir: Path, removed: dict[str, int]) -> None:
    """Remove all cco-*.md files from agents directory.

    Args:
        agents_dir: Path to agents directory
        removed: Dictionary to update with count of removed items
    """
    if agents_dir.exists():
        for f in agents_dir.glob("cco-*.md"):
            f.unlink()
            removed["agents"] += 1


def _remove_old_rules(old_rules_dir: Path, removed: dict[str, int]) -> None:
    """Remove old CCO rule files from root (v1.x backward compat).

    Args:
        old_rules_dir: Path to old rules root directory
        removed: Dictionary to update with count of removed items
    """
    old_rule_files = CCO_RULE_FILES + ("cco-adaptive.md", "cco-tools.md")
    if old_rules_dir.exists():
        for rule_file in old_rule_files:
            rule_path = old_rules_dir / rule_file
            if rule_path.exists():
                rule_path.unlink()
                removed["rules"] += 1


def _remove_new_rules(new_rules_dir: Path, removed: dict[str, int]) -> None:
    """Remove CCO rules from cco/ subdirectory (v2.x).

    Args:
        new_rules_dir: Path to new rules cco/ subdirectory
        removed: Dictionary to update with count of removed items
    """
    old_rule_names = CCO_RULE_NAMES + ("tools.md", "adaptive.md")
    if new_rules_dir.exists():
        for rule_name in old_rule_names:
            rule_path = new_rules_dir / rule_name
            if rule_path.exists():
                rule_path.unlink()
                removed["rules"] += 1
        # Remove empty cco/ directory
        if new_rules_dir.exists() and not any(new_rules_dir.iterdir()):
            new_rules_dir.rmdir()


def _clean_claude_md_markers(claude_md: Path, removed: dict[str, int]) -> None:
    """Remove CCO markers from CLAUDE.md.

    Args:
        claude_md: Path to CLAUDE.md file
        removed: Dictionary to update with count of removed items
    """
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        content, count = _remove_all_cco_markers(content)
        if count > 0:
            content = re.sub(r"\n{3,}", "\n\n", content)
            claude_md.write_text(content, encoding="utf-8")
            removed["rules"] += count


def clean_previous_installation(verbose: bool = True) -> dict[str, int]:
    """Remove previous CCO commands, agents, and rules.

    This ensures a clean reinstall by removing:
    - All cco-*.md files in commands/ and agents/
    - CCO markers from CLAUDE.md
    - Old rules from ~/.claude/rules/ root (v1.x backward compat)
    - New rules from ~/.claude/rules/cco/ (v2.x)

    NOTE: Does NOT touch settings.json or statusline.js.
    v1.0.0 never installed these globally, and v1.1.0+ uses local ./.claude/ only.

    Args:
        verbose: If True, print progress messages during cleanup.

    Returns:
        Dictionary with counts of removed items
    """
    removed = {"commands": 0, "agents": 0, "rules": 0}

    # 1. Remove all cco-*.md files from commands/
    _remove_command_files(COMMANDS_DIR, removed)

    # 2. Remove all cco-*.md files from agents/
    _remove_agent_files(AGENTS_DIR, removed)

    # 3a. Remove old CCO rule files from root (v1.x backward compat)
    _remove_old_rules(OLD_RULES_ROOT, removed)

    # 3b. Remove CCO rules from cco/ subdirectory (v2.x)
    _remove_new_rules(RULES_DIR, removed)

    # 4. Remove CCO markers from CLAUDE.md
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    _clean_claude_md_markers(claude_md, removed)

    total = sum(removed.values())
    if verbose and total > 0:
        print("Cleaning previous installation...")
        if removed["commands"]:
            print(f"  - Removed {removed['commands']} command(s)")
        if removed["agents"]:
            print(f"  - Removed {removed['agents']} agent(s)")
        if removed["rules"]:
            print(f"  - Removed {removed['rules']} rule file(s)/section(s)")
        print()

    return removed


def _setup_content(src_subdir: str, dest_dir: Path, verbose: bool = True) -> list[str]:
    """Copy cco-*.md files from source to destination directory.

    Idempotent: removes existing cco-*.md files before copying new ones.
    Safe for reinstall - always results in fresh content from current version.

    Args:
        src_subdir: Subdirectory name under content/ (e.g., 'command-templates', 'agent-templates')
        dest_dir: Target directory path (e.g., ~/.claude/commands/)
        verbose: If True, print progress messages during installation

    Returns:
        List of installed filenames (e.g., ['cco-optimize.md', 'cco-config.md'])
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
    return _setup_content("command-templates", COMMANDS_DIR, verbose)


def setup_agents(verbose: bool = True) -> list[str]:
    """Copy cco-*.md agents to ~/.claude/agents/"""
    return _setup_content("agent-templates", AGENTS_DIR, verbose)


def setup_rules(verbose: bool = True) -> dict[str, int]:
    """Copy rule files to ~/.claude/rules/cco/

    Installs to cco/ subdirectory (namespaced to preserve user's custom rules):
    - core.md (always active)
    - ai.md (always active)

    Note: tools.md and adaptive.md stay in pip package - embedded in commands/agents.

    Returns:
        Dictionary with installed counts per category
    """
    src_dir = get_content_dir() / "rules"
    if not src_dir.exists():
        return {"core": 0, "ai": 0, "tools": 0, "total": 0}

    # Create cco/ subdirectory
    RULES_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing CCO rule files from cco/ subdirectory
    for rule_name in CCO_RULE_NAMES:
        rule_path = RULES_DIR / rule_name
        if rule_path.exists():
            rule_path.unlink()

    # Copy CCO rule files with new names (cco-core.md -> core.md)
    installed = {}

    for src_filename, dest_filename in zip(CCO_RULE_FILES, CCO_RULE_NAMES, strict=True):
        src_file = src_dir / src_filename
        if src_file.exists():
            shutil.copy2(src_file, RULES_DIR / dest_filename)
            # Extract key: core.md -> core
            key = dest_filename.replace(".md", "")
            installed[key] = 1
            if verbose:
                print(f"  + cco/{dest_filename}")

    installed["total"] = sum(installed.values())
    return installed


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


def clean_claude_md(verbose: bool = True) -> int:
    """Clean CCO markers from ~/.claude/CLAUDE.md (backward compatibility).

    v2.x no longer writes rules to CLAUDE.md - they're in ~/.claude/rules/cco/.
    This function only removes old CCO markers from previous installations.

    Args:
        verbose: If True, print progress messages during cleanup.

    Returns:
        Number of markers removed
    """
    claude_md = CLAUDE_DIR / "CLAUDE.md"

    if not claude_md.exists():
        return 0

    content = claude_md.read_text(encoding="utf-8")
    content, removed_count = _remove_all_cco_markers(content)

    if removed_count > 0:
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = content.strip()
        if content:
            claude_md.write_text(content + "\n", encoding="utf-8")
        else:
            # File is empty after removing CCO content - delete it
            claude_md.unlink()

        if verbose:
            print(f"  CLAUDE.md: cleaned {removed_count} old CCO marker(s)")

    return removed_count


# Keep setup_claude_md as alias for backward compatibility in tests
def setup_claude_md(verbose: bool = True) -> dict[str, int]:
    """Deprecated: Use clean_claude_md instead.

    Kept for backward compatibility. Now only cleans old markers,
    does not write new rules (they're in ~/.claude/rules/cco/).
    """
    warnings.warn(
        "setup_claude_md is deprecated, use clean_claude_md instead",
        DeprecationWarning,
        stacklevel=2,
    )
    removed = clean_claude_md(verbose)
    breakdown = get_rules_breakdown()
    return {
        "core": breakdown["core"] if removed else 0,
        "ai": breakdown["ai"] if removed else 0,
    }


# ============================================================================
# LOCAL MODE FUNCTIONS (for cco-config)
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

    # Create .claude/ directory and copy statusline (always overwrite)
    local_claude = project_path / ".claude"
    local_claude.mkdir(parents=True, exist_ok=True)
    dest = local_claude / "cco-statusline.js"
    shutil.copy2(src, dest)

    # Update local settings.json with statusLine config
    settings_file = local_claude / "settings.json"
    settings = _load_settings_json(settings_file)

    # Local statusline - direct path, no fallback
    settings["statusLine"] = {
        "type": "command",
        "command": "node .claude/cco-statusline.js",
        "padding": 1,
    }

    settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if verbose:
        print(f"  + .claude/cco-statusline.js ({mode} mode)")
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
    settings = _load_settings_json(settings_file)

    # Set permissions (keep _meta for tracking)
    settings["permissions"] = perm_data.get("permissions", {})
    settings[CCO_PERMISSIONS_MARKER] = True

    settings_file.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if verbose:
        print(f"  + .claude/settings.json (permissions: {level})")

    return True


def _validate_local_path(path: Path) -> str | None:
    """Validate project path for local setup.

    Args:
        path: Project path to validate

    Returns:
        Error message if invalid, None if valid
    """
    if not path.exists():
        return f"Project path does not exist: {path}"
    if not path.is_dir():
        return f"Not a directory: {path}"
    if not _is_safe_path(path):
        return "Path must be within home directory or current working directory"
    return None


def _execute_local_setup(path: Path, args: argparse.Namespace) -> int:
    """Execute local setup for statusline and/or permissions.

    Args:
        path: Validated project path
        args: Command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print(f"\nCCO Local Setup: {path}\n")

    success = True

    if args.statusline:
        print("Statusline:")
        if not setup_local_statusline(path, args.statusline):
            success = False
        print()

    if args.permissions:
        print("Permissions:")
        if not setup_local_permissions(path, args.permissions):
            success = False
        print()

    if not args.statusline and not args.permissions:
        # Just create .claude/ directory
        local_claude = path / ".claude"
        local_claude.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {local_claude}/")
        print()

    if success:
        print("Local setup complete.")
    else:
        print("Local setup completed with errors.", file=sys.stderr)

    return 0 if success else 1


def _run_local_mode(args: argparse.Namespace) -> int:
    """Handle --local mode for cco-config integration."""
    project_path = Path(args.local).resolve()

    # Validate path
    error = _validate_local_path(project_path)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Execute setup
    return _execute_local_setup(project_path, args)


def _create_install_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for cco-install.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="cco-install",
        description="Install CCO commands, agents, and rules to ~/.claude/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Local mode (for cco-config):
  cco-install --local . --statusline full --permissions balanced

Statusline modes: full, minimal
Permission levels: safe, balanced, permissive, full
""",
    )

    parser.add_argument(
        "--local",
        metavar="PATH",
        help="Project path for local setup (used by /cco-config)",
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

    return parser


def _validate_global_mode_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Validate arguments for global installation mode.

    Args:
        parser: ArgumentParser instance for error reporting.
        args: Parsed command-line arguments.

    Raises:
        SystemExit: If validation fails (via parser.error).
    """
    if args.statusline or args.permissions:
        parser.error("--statusline and --permissions require --local")


def _run_global_install() -> int:
    """Execute global installation to ~/.claude/.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
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

        # Step 3: Install agents
        print("Agents:")
        agents = setup_agents()
        if not agents:
            print("  (none)")
        print()

        # Step 4: Install rules to ~/.claude/rules/cco/
        print("Rules (to cco/ subdirectory):")
        rules_installed = setup_rules()
        print()

        # Step 5: Clean old CCO markers from CLAUDE.md (backward compat)
        markers_cleaned = clean_claude_md(verbose=True)
        if markers_cleaned == 0:
            print("  CLAUDE.md: no old markers to clean")
        print()

        # Summary
        breakdown = get_rules_breakdown()
        print(SEPARATOR)
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents")
        print(f"  Global rules (in cco/): {rules_installed.get('total', 0)}")
        print(f"    - core.md: {breakdown['core']} rules (always loaded)")
        print(f"    - ai.md: {breakdown['ai']} rules (always loaded)")
        print("  Embedded in commands/agents:")
        print(f"    - tools rules: {breakdown['tools']} (workflow rules)")
        print(f"    - adaptive rules: {breakdown['adaptive']} (project-specific)")
        print(SEPARATOR)
        print()
        print("Restart Claude Code for changes to take effect.")
        print()
        print("Next: /cco-config to configure statusline, permissions, and project context")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


def post_install() -> int:
    """CLI entry point for cco-install.

    Orchestrates the installation process by:
    1. Parsing command-line arguments
    2. Routing to local or global installation mode
    3. Validating arguments for global mode
    4. Executing the appropriate installation

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    parser = _create_install_parser()
    args = parser.parse_args()

    # Local mode - used by cco-config
    if args.local:
        return _run_local_mode(args)

    # Validate: --statusline and --permissions require --local
    _validate_global_mode_args(parser, args)

    # Global mode - default behavior
    return _run_global_install()


if __name__ == "__main__":
    sys.exit(post_install())
