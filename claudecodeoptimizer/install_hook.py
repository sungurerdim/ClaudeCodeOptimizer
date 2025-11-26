"""CCO Setup - Install commands, agents, and rules to ~/.claude/"""

import re
import shutil
import sys
from pathlib import Path

from .config import AGENTS_DIR, CLAUDE_DIR, COMMANDS_DIR


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def setup_commands() -> int:
    """Copy cco-*.md commands to ~/.claude/commands/"""
    src = get_content_dir() / "commands"
    if not src.exists():
        return 0
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    for old in COMMANDS_DIR.glob("cco-*.md"):
        old.unlink()
    count = 0
    for f in src.glob("cco-*.md"):
        shutil.copy2(f, COMMANDS_DIR / f.name)
        count += 1
    return count


def setup_agents() -> int:
    """Copy cco-*.md agents to ~/.claude/agents/"""
    src = get_content_dir() / "agents"
    if not src.exists():
        return 0
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    for old in AGENTS_DIR.glob("cco-*.md"):
        old.unlink()
    count = 0
    for f in src.glob("cco-*.md"):
        shutil.copy2(f, AGENTS_DIR / f.name)
        count += 1
    return count


def setup_templates() -> int:
    """Copy *.template files as *.cco to ~/.claude/"""
    src = Path(__file__).parent.parent / "templates"
    if not src.exists():
        return 0
    count = 0
    for f in src.glob("*.template"):
        dest = CLAUDE_DIR / f.name.replace(".template", ".cco")
        shutil.copy2(f, dest)
        count += 1
    return count


def setup_claude_md() -> None:
    """Add CCO Rules to ~/.claude/CLAUDE.md"""
    rules = """<!-- CCO_RULES_START -->
# CCO Rules

## Paths
Forward slash (/), relative, quote spaces, Git Bash preferred

## Reference Integrity
Before delete/rename/move: find ALL refs → update (def→type→caller→import→test→doc) → verify (grep old=0, new=expected)

## Verification
- total = done + skip + fail (must match)
- No "fixed" without Read/diff proof
- Verify agent outputs

## Safety
Commit first, test before+after, max 10 files/batch
<!-- CCO_RULES_END -->
"""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        content = re.sub(
            r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?",
            "",
            content,
            flags=re.DOTALL,
        )
        if "<!-- CCO_RULES_START -->" in content:
            content = re.sub(
                r"<!-- CCO_RULES_START -->.*?<!-- CCO_RULES_END -->\n?",
                rules,
                content,
                flags=re.DOTALL,
            )
        else:
            content = content.rstrip() + "\n\n" + rules
    else:
        content = rules

    content = re.sub(r"\n{3,}", "\n\n", content)
    claude_md.write_text(content, encoding="utf-8")


def post_install() -> int:
    """CLI entry point for cco-setup."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cco-setup")
        print("Install CCO commands, agents, and rules to ~/.claude/")
        return 0

    try:
        print("\nCCO Setup")
        print("-" * 40)

        cmds = setup_commands()
        agents = setup_agents()
        templates = setup_templates()
        setup_claude_md()

        print(f"Location: {CLAUDE_DIR}")
        print(f"Commands: {cmds}")
        print(f"Agents: {agents}")
        print(f"Templates: {templates}")
        print("Rules: added to CLAUDE.md")
        print("\nCCO ready! Try: /cco-help")
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())
