"""
CCO Removal - Clean uninstall of CCO from ~/.claude/

Removes (in consistent order):
- ~/.claude/agents/cco-*.md
- ~/.claude/commands/cco-*.md
- ~/.claude/skills/cco-*.md
- ~/.claude/principles/U_*.md, C_*.md, P_*.md
- ~/.claude/*_STANDARDS.md, PRINCIPLE_FORMAT.md, COMMAND_PATTERNS.md
- ~/.claude/*.cco templates
- CCO markers from ~/.claude/CLAUDE.md
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Consistent category ordering (same as knowledge_setup.py)
CATEGORY_ORDER = ["agents", "commands", "skills", "principles", "standards", "templates"]


class CCORemover:
    """Remove CCO from global ~/.claude/ directory."""

    def __init__(self) -> None:
        """Initialize remover."""
        self.claude_dir = Path.home() / ".claude"

    def _get_file_counts(self) -> dict[str, int]:
        """
        Get current CCO file counts (in consistent order).

        Returns:
            Dictionary with counts by category
        """
        counts = {}

        # Agents
        agents_dir = self.claude_dir / "agents"
        if agents_dir.exists():
            count = sum(1 for _ in agents_dir.glob("cco-*.md"))
            if count > 0:
                counts["agents"] = count

        # Commands
        commands_dir = self.claude_dir / "commands"
        if commands_dir.exists():
            count = sum(1 for _ in commands_dir.glob("cco-*.md"))
            if count > 0:
                counts["commands"] = count

        # Skills (recursive)
        skills_dir = self.claude_dir / "skills"
        if skills_dir.exists():
            count = sum(1 for _ in skills_dir.rglob("cco-*.md"))
            if count > 0:
                counts["skills"] = count

        # Principles (U_*, C_*, P_*)
        principles_dir = self.claude_dir / "principles"
        if principles_dir.exists():
            count = (
                sum(1 for _ in principles_dir.glob("U_*.md"))
                + sum(1 for _ in principles_dir.glob("C_*.md"))
                + sum(1 for _ in principles_dir.glob("P_*.md"))
            )
            if count > 0:
                counts["principles"] = count

        # Standards (*_STANDARDS.md, PRINCIPLE_FORMAT.md, COMMAND_PATTERNS.md)
        if self.claude_dir.exists():
            count = (
                sum(1 for _ in self.claude_dir.glob("*_STANDARDS.md"))
                + sum(1 for _ in self.claude_dir.glob("PRINCIPLE_FORMAT.md"))
                + sum(1 for _ in self.claude_dir.glob("COMMAND_PATTERNS.md"))
            )
            if count > 0:
                counts["standards"] = count

        # Templates (*.cco)
        if self.claude_dir.exists():
            count = sum(1 for _ in self.claude_dir.glob("*.cco"))
            if count > 0:
                counts["templates"] = count

        return counts

    def remove(self, clean_claude_md: bool = True) -> dict[str, Any]:
        """
        Remove CCO installation from ~/.claude/ (in consistent order).

        Args:
            clean_claude_md: Remove CCO markers from ~/.claude/CLAUDE.md

        Returns:
            Removal results with counts before/after deletion
        """
        results: dict[str, Any] = {"success": True, "actions": [], "counts": {}}

        # Get counts before removal
        counts_before = self._get_file_counts()

        # Remove in consistent order: agents → commands → skills → principles → standards → templates
        self._remove_agents()
        results["actions"].append("Removed ~/.claude/agents/cco-*.md")

        self._remove_commands()
        results["actions"].append("Removed ~/.claude/commands/cco-*.md")

        self._remove_skills()
        results["actions"].append("Removed ~/.claude/skills/cco-*.md")

        self._remove_principles()
        results["actions"].append("Removed ~/.claude/principles/[UCP]_*.md")

        self._remove_standards()
        results["actions"].append(
            "Removed ~/.claude/*_STANDARDS.md, PRINCIPLE_FORMAT.md, COMMAND_PATTERNS.md"
        )

        self._remove_templates()
        results["actions"].append("Removed ~/.claude/*.cco templates")

        # Clean CLAUDE.md markers
        if clean_claude_md:
            self._clean_claude_md()
            results["actions"].append("Cleaned ~/.claude/CLAUDE.md CCO markers")

        # Get counts after removal (should all be 0)
        counts_after = self._get_file_counts()

        results["counts"] = {
            "before": counts_before,
            "after": counts_after,
        }

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

    def _remove_standards(self) -> None:
        """Remove all standards files from ~/.claude/"""
        if not self.claude_dir.exists():
            return

        # Standards files to remove
        standards_files = [
            "STANDARDS_SKILLS.md",
            "STANDARDS_AGENTS.md",
            "STANDARDS_COMMANDS.md",
            "STANDARDS_QUALITY.md",
            "STANDARDS_PRINCIPLES.md",
            "LIBRARY_PATTERNS.md",
        ]

        # Remove each standards file
        for filename in standards_files:
            file_path = self.claude_dir / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                except Exception as e:
                    logger.debug(f"Skipped removal of {file_path}: {e}")

    def _remove_templates(self) -> None:
        """Remove all *.cco template files from ~/.claude/"""
        if not self.claude_dir.exists():
            return

        # Remove all *.cco files
        for template_file in self.claude_dir.glob("*.cco"):
            try:
                template_file.unlink()
            except Exception as e:
                logger.debug(f"Skipped removal of {template_file}: {e}")

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
