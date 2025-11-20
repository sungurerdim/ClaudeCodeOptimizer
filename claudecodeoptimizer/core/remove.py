"""
CCO Removal - Clean uninstall of CCO from ~/.claude/

Removes:
- ~/.claude/commands/cco-*.md
- ~/.claude/principles/U_*.md, C_*.md, P_*.md
- ~/.claude/agents/cco-*.md
- ~/.claude/skills/cco-*.md
- CCO markers from ~/.claude/CLAUDE.md
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class CCORemover:
    """Remove CCO from global ~/.claude/ directory."""

    def __init__(self) -> None:
        """Initialize remover."""
        self.claude_dir = Path.home() / ".claude"

    def remove(self, clean_claude_md: bool = True) -> dict[str, Any]:
        """
        Remove CCO installation from ~/.claude/.

        Args:
            clean_claude_md: Remove CCO markers from ~/.claude/CLAUDE.md

        Returns:
            Removal results
        """
        results: dict[str, Any] = {"success": True, "actions": []}

        # Remove CCO commands
        self._remove_commands()
        results["actions"].append("Removed ~/.claude/commands/cco-*.md")

        # Remove CCO principles
        self._remove_principles()
        results["actions"].append("Removed ~/.claude/principles/[UCP]_*.md")

        # Remove CCO agents
        self._remove_agents()
        results["actions"].append("Removed ~/.claude/agents/cco-*.md")

        # Remove CCO skills
        self._remove_skills()
        results["actions"].append("Removed ~/.claude/skills/cco-*.md")

        # Clean CLAUDE.md markers
        if clean_claude_md:
            self._clean_claude_md()
            results["actions"].append("Cleaned ~/.claude/CLAUDE.md CCO markers")

        return results

    def _remove_commands(self) -> None:
        """Remove all cco-*.md files from ~/.claude/commands/"""
        commands_dir = self.claude_dir / "commands"

        if not commands_dir.exists():
            return

        # Remove all cco-*.md files
        for cmd_file in commands_dir.glob("cco-*.md"):
            try:
                cmd_file.unlink()
            except Exception as e:
                logger.debug(f"Skipped removal of {cmd_file}: {e}")

    def _remove_principles(self) -> None:
        """Remove all U_*.md, C_*.md, P_*.md files from ~/.claude/principles/"""
        principles_dir = self.claude_dir / "principles"

        if not principles_dir.exists():
            return

        # Remove all CCO principle files
        for pattern in ["U_*.md", "C_*.md", "P_*.md"]:
            for principle_file in principles_dir.glob(pattern):
                try:
                    principle_file.unlink()
                except Exception as e:
                    logger.debug(f"Skipped removal of {principle_file}: {e}")

    def _remove_agents(self) -> None:
        """Remove all cco-*.md files from ~/.claude/agents/"""
        agents_dir = self.claude_dir / "agents"

        if not agents_dir.exists():
            return

        # Remove all cco-*.md files
        for agent_file in agents_dir.glob("cco-*.md"):
            try:
                agent_file.unlink()
            except Exception as e:
                logger.debug(f"Skipped removal of {agent_file}: {e}")

    def _remove_skills(self) -> None:
        """Remove all cco-*.md files from ~/.claude/skills/ (including subdirectories)"""
        skills_dir = self.claude_dir / "skills"

        if not skills_dir.exists():
            return

        # Remove all cco-*.md files recursively
        for skill_file in skills_dir.rglob("cco-*.md"):
            try:
                skill_file.unlink()
            except Exception as e:
                logger.debug(f"Skipped removal of {skill_file}: {e}")

    def _clean_claude_md(self) -> None:
        """Remove CCO markers and content from ~/.claude/CLAUDE.md"""
        claude_md = self.claude_dir / "CLAUDE.md"

        if not claude_md.exists():
            return

        content = claude_md.read_text(encoding="utf-8")

        # Remove CCO marker section
        pattern = r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?"
        content = re.sub(pattern, "", content, flags=re.DOTALL)

        # Clean up extra blank lines (more than 2 consecutive)
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Write cleaned content
        claude_md.write_text(content.strip() + "\n", encoding="utf-8")


def remove_cco(clean_claude_md: bool = True) -> dict[str, Any]:
    """
    Convenience function to remove CCO from ~/.claude/.

    Args:
        clean_claude_md: Clean ~/.claude/CLAUDE.md markers

    Returns:
        Removal results
    """
    remover = CCORemover()
    return remover.remove(clean_claude_md=clean_claude_md)
