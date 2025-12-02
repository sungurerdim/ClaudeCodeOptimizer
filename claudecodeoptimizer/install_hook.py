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


def setup_claude_md(verbose: bool = True) -> None:
    """Add CCO Principles to ~/.claude/CLAUDE.md"""
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

    if verbose:
        breakdown = get_standards_breakdown()
        print(f"  CLAUDE.md: CCO Standards {action}")
        print(
            f"    {breakdown['universal']} universal + {breakdown['claude_specific']} Claude-specific"
        )
        print(f"    (+ {breakdown['conditional']} conditional via /cco-tune)")


def post_install() -> int:
    """CLI entry point for cco-setup."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cco-setup")
        print("Install CCO commands, agents, and standards to ~/.claude/")
        return 0

    try:
        print("\n" + "=" * 50)
        print("CCO Setup")
        print("=" * 50)
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

        # Rules
        print("Rules:")
        setup_claude_md()
        print()

        # Summary
        breakdown = get_standards_breakdown()
        print("=" * 50)
        print("Summary")
        print("=" * 50)
        print(f"  Commands:  {len(cmds)}")
        print(f"  Agents:    {len(agents)}")
        print(f"  Standards: {breakdown['total']} total")
        print(
            f"    {breakdown['universal']} universal + {breakdown['claude_specific']} Claude-specific + {breakdown['conditional']} conditional"
        )
        print()
        print("CCO ready! Try: /cco-tune")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())
