"""CCO Setup - Install commands, agents, and rules to ~/.claude/"""

import re
import shutil
import sys
from pathlib import Path

from .config import AGENTS_DIR, CLAUDE_DIR, COMMANDS_DIR


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def setup_commands(verbose: bool = True) -> list[str]:
    """Copy cco-*.md commands to ~/.claude/commands/"""
    src = get_content_dir() / "commands"
    if not src.exists():
        return []
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    for old in COMMANDS_DIR.glob("cco-*.md"):
        old.unlink()
    installed = []
    for f in sorted(src.glob("cco-*.md")):
        shutil.copy2(f, COMMANDS_DIR / f.name)
        installed.append(f.name)
        if verbose:
            print(f"  + {f.name}")
    return installed


def setup_agents(verbose: bool = True) -> list[str]:
    """Copy cco-*.md agents to ~/.claude/agents/"""
    src = get_content_dir() / "agents"
    if not src.exists():
        return []
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    for old in AGENTS_DIR.glob("cco-*.md"):
        old.unlink()
    installed = []
    for f in sorted(src.glob("cco-*.md")):
        shutil.copy2(f, AGENTS_DIR / f.name)
        installed.append(f.name)
        if verbose:
            print(f"  + {f.name}")
    return installed


def setup_claude_md(verbose: bool = True) -> None:
    """Add CCO Rules to ~/.claude/CLAUDE.md"""
    rules = """<!-- CCO_RULES_START -->
# CCO Rules

## Paths
Forward slash (/), relative, quote spaces

## Reference Integrity
Before delete/rename/move: find ALL refs → update in order → verify (grep old=0, new=expected)

## Verification
- total = done + skip + fail + cannot_do (must match)
- cannot_do = third-party, needs migration, needs infra
- No "fixed" without Read proof

## MultiSelect
Always include "All" as first option
<!-- CCO_RULES_END -->
"""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    action = "created"
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
            action = "updated"
        else:
            content = content.rstrip() + "\n\n" + rules
            action = "appended"
    else:
        content = rules

    content = re.sub(r"\n{3,}", "\n\n", content)
    claude_md.write_text(content, encoding="utf-8")

    if verbose:
        print(f"  CLAUDE.md: CCO Rules {action}")
        print("    - Paths")
        print("    - Reference Integrity")
        print("    - Verification")
        print("    - MultiSelect")


def post_install() -> int:
    """CLI entry point for cco-setup."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cco-setup")
        print("Install CCO commands, agents, and rules to ~/.claude/")
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
        print("=" * 50)
        print("Summary")
        print("=" * 50)
        print(f"  Commands:  {len(cmds)}")
        print(f"  Agents:    {len(agents)}")
        print("  Rules:     4 sections in CLAUDE.md")
        print()
        print("CCO ready! Try: /cco-help")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())
