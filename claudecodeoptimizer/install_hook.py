"""CCO Setup - Install commands, agents, and standards to ~/.claude/"""

import re
import shutil
import sys
from pathlib import Path

from .config import (
    AGENTS_DIR,
    CCO_MARKER_PATTERNS,
    CLAUDE_DIR,
    COMMANDS_DIR,
    SEPARATOR,
    get_standards_breakdown,
)


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def _setup_content(src_subdir: str, dest_dir: Path, verbose: bool = True) -> list[str]:
    """Copy cco-*.md files from source to destination directory."""
    src = get_content_dir() / src_subdir
    if not src.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
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


def setup_claude_md(verbose: bool = True) -> dict[str, int]:
    """Add CCO Principles to ~/.claude/CLAUDE.md

    Returns:
        Dictionary with installed counts (universal, claude_specific)
    """
    standards = _load_standards()
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    action = "created"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")

        # Check if standards marker exists and update or append
        if "<!-- CCO_STANDARDS_START -->" in content:
            pattern, flags = CCO_MARKER_PATTERNS["standards"]
            content = re.sub(pattern, standards, content, flags=flags)
            action = "updated"
        else:
            content = content.rstrip() + "\n\n" + standards
            action = "appended"
    else:
        content = standards

    content = re.sub(r"\n{3,}", "\n\n", content)
    claude_md.write_text(content, encoding="utf-8")

    breakdown = get_standards_breakdown()
    installed = breakdown["universal"] + breakdown["claude_specific"]

    if verbose:
        print(f"  CLAUDE.md: {installed} standards {action}")

    return {"universal": breakdown["universal"], "claude_specific": breakdown["claude_specific"]}


def post_install() -> int:
    """CLI entry point for cco-setup."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cco-setup")
        print("Install CCO commands, agents, and standards to ~/.claude/")
        return 0

    try:
        print("\n" + SEPARATOR)
        print("CCO Setup")
        print(SEPARATOR)
        print(f"\nLocation: {CLAUDE_DIR}\n")

        # Commands
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
        installed = standards["universal"] + standards["claude_specific"]
        breakdown = get_standards_breakdown()
        print(SEPARATOR)
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents, {installed} standards")
        print(f"Available: +{breakdown['conditional']} conditional standards via /cco-tune")
        print(SEPARATOR)
        print()
        print("⚠️  Restart Claude Code for changes to take effect.")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())
