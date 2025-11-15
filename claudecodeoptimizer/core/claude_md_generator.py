"""
CLAUDE.md Generator V2 - Stateless Architecture with Original Content Preservation

CRITICAL RULES:
1. NEVER touch content outside CCO markers
2. ONLY update content between markers
3. NO backup needed (original content never modified)
4. If markers don't exist, ADD them at end
5. If markers exist, UPDATE content between them
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class ClaudeMdGenerator:
    """
    CLAUDE.md generator with STRICT original content preservation.

    Uses marker-based injection only. Original content NEVER modified.
    """

    # CCO markers
    MARKERS = {
        "principles": ("<!-- CCO_PRINCIPLES_START -->", "<!-- CCO_PRINCIPLES_END -->"),
        "skills": ("<!-- CCO_SKILLS_START -->", "<!-- CCO_SKILLS_END -->"),
        "agents": ("<!-- CCO_AGENTS_START -->", "<!-- CCO_AGENTS_END -->"),
        "commands": ("<!-- CCO_COMMANDS_START -->", "<!-- CCO_COMMANDS_END -->"),
        "guides": ("<!-- CCO_GUIDES_START -->", "<!-- CCO_GUIDES_END -->"),
        "claude": ("<!-- CCO_CLAUDE_START -->", "<!-- CCO_CLAUDE_END -->"),
    }

    def __init__(
        self,
        preferences: Dict[str, Any],
        selected_skills: List[str] | None = None,
        selected_agents: List[str] | None = None,
    ) -> None:
        """
        Initialize generator.

        Args:
            preferences: User preferences
            selected_skills: Selected skill IDs
            selected_agents: Selected agent IDs
        """
        self.preferences = preferences
        self.selected_skills = selected_skills or []
        self.selected_agents = selected_agents or []
        self.principles_dir = Path(__file__).parent.parent.parent / "content" / "principles"

    def generate(self, output_path: Path) -> Dict[str, Any]:
        """
        Generate or update CLAUDE.md.

        Strategy:
        - New file: Create with markers
        - Existing file: Update markers only (PRESERVE all original content)

        Args:
            output_path: Path to CLAUDE.md

        Returns:
            Generation results
        """
        if not output_path.exists():
            return self._create_new_file(output_path)
        else:
            return self._update_existing_file(output_path)

    def _create_new_file(self, output_path: Path) -> Dict[str, Any]:
        """Create new CLAUDE.md with markers."""
        content = self._get_base_template()

        # Inject all sections
        content = self._inject_all_sections(content)

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "file_path": str(output_path),
            "strategy": "created_new",
            "original_content_preserved": True,  # N/A for new file
            "markers_added": list(self.MARKERS.keys()),
        }

    def _update_existing_file(self, output_path: Path) -> Dict[str, Any]:
        """
        Update existing CLAUDE.md preserving ALL original content.

        CRITICAL: Only marker content is updated, nothing else.
        """
        original = output_path.read_text(encoding="utf-8")
        updated = original
        markers_updated = []
        markers_added = []

        for section, (start_marker, end_marker) in self.MARKERS.items():
            new_content = self._generate_section_content(section)

            if start_marker in updated:
                # Marker exists -> Replace content between markers
                pattern = f"({re.escape(start_marker)}).*?({re.escape(end_marker)})"
                replacement = f"\\1\n{new_content}\n\\2"
                updated = re.sub(pattern, replacement, updated, flags=re.DOTALL)
                markers_updated.append(section)
            else:
                # Marker doesn't exist -> Add at end
                updated += f"\n\n{start_marker}\n{new_content}\n{end_marker}\n"
                markers_added.append(section)

        # Write updated content
        output_path.write_text(updated, encoding="utf-8")

        return {
            "success": True,
            "file_path": str(output_path),
            "strategy": "updated_markers_only",
            "original_content_preserved": True,  # GUARANTEED
            "markers_updated": markers_updated,
            "markers_added": markers_added,
            "backup_created": False,  # Not needed!
        }

    def _get_base_template(self) -> str:
        """Get base CLAUDE.md template for new files."""
        # Get project metadata
        project_name = self.preferences.get("project_identity", {}).get("name") or "Project"
        team_size = (
            self.preferences.get("project_identity", {}).get("team_trajectory") or "Solo Developer"
        )
        quality = self.preferences.get("code_quality", {}).get("linting_strictness") or "Strict"
        testing = self.preferences.get("testing", {}).get("strategy") or "Balanced"

        return f"""# Claude Code Development Guide

**Project:** {project_name}
**Team:** {team_size}
**Quality:** {quality}
**Testing:** {testing}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

## Development Principles

<!-- CCO_PRINCIPLES_START -->
<!-- CCO_PRINCIPLES_END -->

## Available Skills

<!-- CCO_SKILLS_START -->
<!-- CCO_SKILLS_END -->

## Available Agents

<!-- CCO_AGENTS_START -->
<!-- CCO_AGENTS_END -->

## Available Commands

<!-- CCO_COMMANDS_START -->
<!-- CCO_COMMANDS_END -->

## Available Guides

<!-- CCO_GUIDES_START -->
<!-- CCO_GUIDES_END -->

## Claude Guidelines

<!-- CCO_CLAUDE_START -->
<!-- CCO_CLAUDE_END -->
"""

    def _inject_all_sections(self, content: str) -> str:
        """Inject content into all marker sections."""
        for section in self.MARKERS.keys():
            new_section_content = self._generate_section_content(section)
            start_marker, end_marker = self.MARKERS[section]

            # Replace empty marker with content
            pattern = f"({re.escape(start_marker)}).*?({re.escape(end_marker)})"
            replacement = f"\\1\n{new_section_content}\n\\2"
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        return content

    def _generate_section_content(self, section: str) -> str:
        """
        Generate content for a specific marker section.

        Args:
            section: Section name (principles, skills, agents, etc.)

        Returns:
            Formatted content for that section
        """
        if section == "principles":
            return self._generate_principles_content()
        elif section == "skills":
            return self._generate_skills_content()
        elif section == "agents":
            return self._generate_agents_content()
        elif section == "commands":
            return self._generate_commands_content()
        elif section == "guides":
            return self._generate_guides_content()
        elif section == "claude":
            return self._generate_claude_guidelines_content()
        else:
            return f"[{section.title()} content]"

    def _generate_principles_content(self) -> str:
        """Generate principles section content."""
        lines = []

        # Universal principles
        universal = self._get_universal_principles()
        if universal:
            lines.append("**Universal Principles** (apply to all projects):")
            for p in sorted(universal):
                lines.append(
                    f"- **{p}**: {self._get_principle_title(p)} → `.claude/principles/{p}.md`"
                )
            lines.append("")

        # Project-specific principles
        project_specific = self._get_project_specific_principles()
        if project_specific:
            lines.append("**Project-Specific Principles:**")
            lines.append("")

            # Group by category
            by_category = self._group_principles_by_category(project_specific)

            for category, principles in sorted(by_category.items()):
                lines.append(f"*{category.replace('_', ' ').title()}:*")
                for p in sorted(principles):
                    lines.append(
                        f"- **{p}**: {self._get_principle_title(p)} → `.claude/principles/{p}.md`"
                    )
                lines.append("")

        # Claude guidelines
        claude = self._get_claude_guidelines()
        if claude:
            lines.append("*Claude Guidelines:*")
            for p in sorted(claude):
                lines.append(
                    f"- **{p}**: {self._get_principle_title(p)} → `.claude/principles/{p}.md`"
                )

        return "\n".join(lines)

    def _generate_skills_content(self) -> str:
        """Generate skills section content."""
        if not self.selected_skills:
            return "No skills selected for this project."

        lines = []
        for skill in self.selected_skills:
            skill_name = skill.replace("cco-skill-", "").replace("-", " ").title()
            lines.append(f"- **{skill_name}** → `.claude/skills/{skill}.md`")

        return "\n".join(lines)

    def _generate_agents_content(self) -> str:
        """Generate agents section content."""
        if not self.selected_agents:
            return "No agents selected for this project."

        lines = []
        for agent in self.selected_agents:
            agent_name = agent.replace("cco-agent-", "").replace("-", " ").title()
            lines.append(f"- **{agent_name} Agent** → `.claude/agents/{agent}.md`")

        return "\n".join(lines)

    def _generate_commands_content(self) -> str:
        """Generate commands section content."""
        # This would list all symlinked commands in .claude/commands/
        # For now, placeholder
        return "- Run `/cco-status` to see all available commands"

    def _generate_guides_content(self) -> str:
        """Generate guides section content."""
        # This would list all symlinked guides in .claude/guides/
        # For now, placeholder
        return "- **Security Emergency Response** → `.claude/guides/cco-security-response.md`"

    def _generate_claude_guidelines_content(self) -> str:
        """Generate Claude guidelines section content."""
        claude_principles = self._get_claude_guidelines()

        lines = []
        for p in sorted(claude_principles):
            lines.append(f"- **{p}**: {self._get_principle_title(p)} → `.claude/principles/{p}.md`")

        return "\n".join(lines)

    # Helper methods
    def _get_universal_principles(self) -> List[str]:
        """Get list of universal principle IDs."""
        # Read from principles_dir
        universal = []
        if self.principles_dir.exists():
            for file in self.principles_dir.glob("U_*.md"):
                universal.append(file.stem)
        return universal

    def _get_project_specific_principles(self) -> List[str]:
        """Get list of project-specific principle IDs."""
        # This would be based on preferences/detection
        # For now, placeholder - return common ones
        return [
            "P_LINTING_SAST",
            "P_TYPE_SAFETY",
            "P_VERSION_MANAGEMENT",
        ]

    def _get_claude_guidelines(self) -> List[str]:
        """Get list of Claude guideline IDs."""
        claude = []
        if self.principles_dir.exists():
            for file in self.principles_dir.glob("C_*.md"):
                claude.append(file.stem)
        return claude

    def _get_principle_title(self, principle_id: str) -> str:
        """Get human-readable title for principle."""
        # Read from frontmatter or use default
        titles = {
            "U_ATOMIC_COMMITS": "Atomic Commits",
            "U_CHANGE_VERIFICATION": "Change Verification Protocol",
            "P_LINTING_SAST": "Linting & SAST Enforcement",
            # ... more mappings
        }
        return titles.get(principle_id, principle_id.replace("_", " ").title())

    def _group_principles_by_category(self, principles: List[str]) -> Dict[str, List[str]]:
        """Group principles by category."""
        # Placeholder - would read from principle frontmatter
        return {
            "code_quality": [p for p in principles if "LINTING" in p or "TYPE" in p],
            "security": [p for p in principles if "SECURITY" in p or "ENCRYPTION" in p],
        }
