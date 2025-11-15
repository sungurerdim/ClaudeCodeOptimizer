"""
CCO Removal - Complete cleanup of CCO from project and/or global installation

Provides clean uninstall with three scopes:
- local: Remove CCO from current project only
- global: Remove entire ~/.cco/ directory
- both: Complete removal (project + global)
"""

import re
import shutil
from pathlib import Path
from typing import Any, Dict, Literal


class CCORemover:
    """Remove CCO from project or globally."""

    def __init__(self, project_root: Path) -> None:
        """
        Initialize remover.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root

    def remove(
        self,
        scope: Literal["local", "global", "both"] = "local",
        clean_claude_md: bool = True,
    ) -> Dict[str, Any]:
        """
        Remove CCO installation.

        Args:
            scope: "local" (project only), "global" (all CCO), "both"
            clean_claude_md: Remove CCO markers from CLAUDE.md

        Returns:
            Removal results
        """
        results = {"success": True, "actions": []}

        if scope in ["local", "both"]:
            # Remove local .claude/ CCO files
            self._remove_local_cco()
            results["actions"].append("Removed local .claude/ CCO files")

            # Clean CLAUDE.md markers
            if clean_claude_md:
                self._clean_claude_md()
                results["actions"].append("Cleaned CLAUDE.md CCO markers")

        if scope in ["global", "both"]:
            # Remove global ~/.cco/
            self._remove_global_cco()
            results["actions"].append("Removed global ~/.cco/")

            # Remove global ~/.claude/commands/ init/remove
            self._remove_global_commands()
            results["actions"].append("Removed ~/.claude/commands/ CCO commands")

        return results

    def _remove_local_cco(self) -> None:
        """Remove all cco-* files from .claude/"""
        claude_dir = self.project_root / ".claude"

        if not claude_dir.exists():
            return

        # Remove CCO files from all subdirectories
        for pattern in [
            "commands/cco-*.md",
            "principles/*.md",
            "guides/cco-*.md",
            "skills/cco-*.md",
            "agents/cco-*.md",
        ]:
            for file in claude_dir.glob(pattern):
                # Only remove if it's a symlink or starts with cco-
                if file.is_symlink() or file.name.startswith("cco-"):
                    try:
                        file.unlink()
                    except Exception:
                        pass  # Ignore errors (broken symlinks, etc.)

    def _clean_claude_md(self) -> None:
        """Remove CCO markers and content from CLAUDE.md"""
        claude_md = self.project_root / "CLAUDE.md"
        if not claude_md.exists():
            return

        content = claude_md.read_text(encoding="utf-8")

        # Remove all CCO marker sections
        markers = [
            ("<!-- CCO_PRINCIPLES_START -->", "<!-- CCO_PRINCIPLES_END -->"),
            ("<!-- CCO_SKILLS_START -->", "<!-- CCO_SKILLS_END -->"),
            ("<!-- CCO_AGENTS_START -->", "<!-- CCO_AGENTS_END -->"),
            ("<!-- CCO_COMMANDS_START -->", "<!-- CCO_COMMANDS_END -->"),
            ("<!-- CCO_GUIDES_START -->", "<!-- CCO_GUIDES_END -->"),
            ("<!-- CCO_CLAUDE_START -->", "<!-- CCO_CLAUDE_END -->"),
        ]

        for start, end in markers:
            pattern = f"{re.escape(start)}.*?{re.escape(end)}"
            content = re.sub(pattern, "", content, flags=re.DOTALL)

        # Clean up extra blank lines (more than 2 consecutive)
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Remove CCO metadata lines if present
        lines = content.split("\n")
        cleaned_lines = []
        for line in lines:
            # Skip CCO-generated metadata
            if any(marker in line for marker in ["**Generated:**", "**Quality:**", "**Testing:**"]):
                # Only skip if it looks like CCO metadata (has date format)
                if "**Generated:**" in line or line.strip().startswith("**"):
                    continue
            cleaned_lines.append(line)

        content = "\n".join(cleaned_lines)

        # Write cleaned content
        claude_md.write_text(content.strip() + "\n", encoding="utf-8")

    def _remove_global_cco(self) -> None:
        """Remove ~/.cco/ directory"""
        global_cco = Path.home() / ".cco"
        if global_cco.exists():
            try:
                shutil.rmtree(global_cco)
            except Exception:
                # Ignore errors (permissions, etc.)
                pass

    def _remove_global_commands(self) -> None:
        """Remove ~/.claude/commands/ CCO commands"""
        global_commands = Path.home() / ".claude" / "commands"

        if not global_commands.exists():
            return

        for cmd in ["cco-init.md", "cco-remove.md"]:
            cmd_file = global_commands / cmd
            if cmd_file.exists():
                try:
                    cmd_file.unlink()
                except Exception:
                    pass


def remove_cco(
    project_root: Path,
    scope: Literal["local", "global", "both"] = "local",
    clean_claude_md: bool = True,
) -> Dict[str, Any]:
    """
    Convenience function to remove CCO.

    Args:
        project_root: Project root directory
        scope: Removal scope
        clean_claude_md: Clean CLAUDE.md markers

    Returns:
        Removal results
    """
    remover = CCORemover(project_root)
    return remover.remove(scope=scope, clean_claude_md=clean_claude_md)
