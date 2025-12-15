"""CCO Local Setup - Project-local configuration for statusline and permissions."""

import argparse
import json
import shutil
import sys
from pathlib import Path

from .config import (
    CCO_PERMISSIONS_MARKER,
    get_content_path,
    load_json_file,
    save_json_file,
)

# Valid options for local mode
STATUSLINE_MODES = ("cco-full", "cco-minimal")
PERMISSION_LEVELS = ("safe", "balanced", "permissive", "full")


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


def _get_local_claude_dir(project_path: Path) -> Path:
    """Get or create the local .claude directory."""
    local_claude = project_path / ".claude"
    local_claude.mkdir(parents=True, exist_ok=True)
    return local_claude


def _load_local_settings(project_path: Path) -> tuple[Path, dict]:
    """Load settings.json from project's .claude directory."""
    local_claude = _get_local_claude_dir(project_path)
    settings_file = local_claude / "settings.json"
    settings = load_json_file(settings_file) if settings_file.exists() else {}
    return settings_file, settings


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
    local_claude = _get_local_claude_dir(project_path)
    dest = local_claude / "cco-statusline.js"
    shutil.copy2(src, dest)

    # Update local settings.json with statusLine config
    settings_file, settings = _load_local_settings(project_path)

    # Local statusline - direct path, no fallback
    settings["statusLine"] = {
        "type": "command",
        "command": "node .claude/cco-statusline.js",
        "padding": 1,
    }

    save_json_file(settings_file, settings)

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

    # Load or create settings.json
    settings_file, settings = _load_local_settings(project_path)

    # Set permissions (keep _meta for tracking)
    settings["permissions"] = perm_data.get("permissions", {})
    settings[CCO_PERMISSIONS_MARKER] = True

    save_json_file(settings_file, settings)

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


def run_local_mode(args: argparse.Namespace) -> int:
    """Handle --local mode for cco-config integration."""
    project_path = Path(args.local).resolve()

    # Validate path
    error = _validate_local_path(project_path)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Execute setup
    return _execute_local_setup(project_path, args)
