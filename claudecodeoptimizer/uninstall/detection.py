"""CCO Uninstall - Detection functions for installed components."""

import subprocess
from pathlib import Path

from ..config import (
    ALL_RULE_NAMES,
    CCO_PERMISSIONS_MARKER,
    CCO_UNIVERSAL_PATTERN_COMPILED,
    CLAUDE_DIR,
    MAX_CLAUDE_MD_SIZE,
    OLD_RULE_FILES,
    OLD_RULES_ROOT,
    RULES_DIR,
    SETTINGS_FILE,
    STATUSLINE_FILE,
    SUBPROCESS_TIMEOUT,
    get_cco_agents,
    get_cco_commands,
    load_json_file,
)


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
                encoding="utf-8",
                errors="replace",
                timeout=SUBPROCESS_TIMEOUT,
                shell=False,
            )
            if "claudecodeoptimizer" in result.stdout:
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # Tool not installed or unresponsive, try next detection method
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


def has_cco_permissions(settings_file: Path = SETTINGS_FILE) -> bool:
    """Check if CCO permissions are installed in settings.json."""
    if not settings_file.exists():
        return False
    settings = load_json_file(settings_file)
    permissions = settings.get("permissions", {})
    # Check for CCO marker or _meta field (from permissions JSON)
    if CCO_PERMISSIONS_MARKER in settings:
        return True
    if isinstance(permissions, dict) and "_meta" in permissions:
        return True
    return False


def has_rules_dir() -> bool:
    """Check if any CCO rule files exist in ~/.claude/rules/cco/."""
    if not RULES_DIR.exists():
        return False
    # Check for current structure: ~/.claude/rules/cco/{core,ai}.md
    return any((RULES_DIR / f).exists() for f in ALL_RULE_NAMES)


def has_rules_dir_old() -> bool:
    """Check if any old CCO rule files exist in ~/.claude/rules/ root."""
    if not OLD_RULES_ROOT.exists():
        return False
    # Check for old root-level: ~/.claude/rules/cco-{core,ai,tools,adaptive}.md
    return any((OLD_RULES_ROOT / f).exists() for f in OLD_RULE_FILES)


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

    Uses universal pattern to detect ANY CCO marker.
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
