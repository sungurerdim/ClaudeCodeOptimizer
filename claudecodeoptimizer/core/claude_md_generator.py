"""
CLAUDE.md Generator - Marker-Based System with Complete Content Preservation

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
from typing import Any, Dict, List, Optional


class ClaudeMdGenerator:
    """
    CLAUDE.md generator with STRICT original content preservation.

    Uses marker-based injection only. Original content NEVER modified.
    """

    # CCO markers
    MARKERS = {
        "header": ("<!-- CCO_HEADER_START -->", "<!-- CCO_HEADER_END -->"),
        "principles": ("<!-- CCO_PRINCIPLES_START -->", "<!-- CCO_PRINCIPLES_END -->"),
        "skills": ("<!-- CCO_SKILLS_START -->", "<!-- CCO_SKILLS_END -->"),
        "agents": ("<!-- CCO_AGENTS_START -->", "<!-- CCO_AGENTS_END -->"),
        "commands": ("<!-- CCO_COMMANDS_START -->", "<!-- CCO_COMMANDS_END -->"),
        "guides": ("<!-- CCO_GUIDES_START -->", "<!-- CCO_GUIDES_END -->"),
    }

    def __init__(
        self,
        preferences: Dict[str, Any],
        project_root: Path,
        selected_skills: List[str] | None = None,
        selected_agents: List[str] | None = None,
        selected_commands: List[str] | None = None,
        selected_guides: List[str] | None = None,
    ) -> None:
        """
        Initialize generator.

        Args:
            preferences: User preferences
            project_root: Project root (to read from .claude/ directory - SSOT)
            selected_skills: Selected skill IDs
            selected_agents: Selected agent IDs
            selected_commands: Selected command IDs
            selected_guides: Selected guide IDs
        """
        self.preferences = preferences
        self.project_root = project_root
        self.selected_skills = selected_skills or []
        self.selected_agents = selected_agents or []
        self.selected_commands = selected_commands or []
        self.selected_guides = selected_guides or []
        # SSOT: Read from .claude/principles/ (actual symlinks) not content/principles/
        self.principles_dir = project_root / ".claude" / "principles"

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

        # Normalize multiple empty lines to single empty lines
        content = self._normalize_empty_lines(content)

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
                # Marker doesn't exist
                if section == "header":
                    # Header goes at the beginning
                    updated = f"{start_marker}\n{new_content}\n{end_marker}\n\n{updated}"
                else:
                    # Other markers go at the end
                    updated += f"\n\n{start_marker}\n{new_content}\n{end_marker}\n"
                markers_added.append(section)

        # Normalize multiple empty lines to single empty lines
        updated = self._normalize_empty_lines(updated)

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

    def _normalize_empty_lines(self, content: str) -> str:
        """
        Normalize multiple consecutive empty lines to single empty lines.

        Replaces 3+ newlines with exactly 2 newlines (one empty line).
        """
        # Replace 3 or more consecutive newlines with exactly 2
        while "\n\n\n" in content:
            content = content.replace("\n\n\n", "\n\n")
        return content

    def _get_base_template(self) -> str:
        """Get base CLAUDE.md template for new files - only markers."""
        return """<!-- CCO_HEADER_START -->
<!-- CCO_HEADER_END -->

<!-- CCO_PRINCIPLES_START -->
<!-- CCO_PRINCIPLES_END -->

<!-- CCO_SKILLS_START -->
<!-- CCO_SKILLS_END -->

<!-- CCO_AGENTS_START -->
<!-- CCO_AGENTS_END -->

<!-- CCO_COMMANDS_START -->
<!-- CCO_COMMANDS_END -->

<!-- CCO_GUIDES_START -->
<!-- CCO_GUIDES_END -->
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
            section: Section name (header, principles, skills, agents, etc.)

        Returns:
            Formatted content for that section
        """
        if section == "header":
            return self._generate_header_content()
        elif section == "principles":
            return self._generate_principles_content()
        elif section == "skills":
            return self._generate_skills_content()
        elif section == "agents":
            return self._generate_agents_content()
        elif section == "commands":
            return self._generate_commands_content()
        elif section == "guides":
            return self._generate_guides_content()
        else:
            return f"[{section.title()} content]"

    def _generate_header_content(self) -> str:
        """Generate header section content."""
        # Get project metadata
        project_name = self.preferences.get("project_identity", {}).get("name") or "Project"
        team_size = (
            self.preferences.get("project_identity", {}).get("team_trajectory") or "Solo Developer"
        )
        quality = self.preferences.get("code_quality", {}).get("linting_strictness") or "Strict"
        testing = self.preferences.get("testing", {}).get("strategy") or "Balanced"

        lines = [
            "# Claude Code Development Guide",
            "",
            f"**Project:** {project_name} | **Team:** {team_size} | **Quality:** {quality} | **Testing:** {testing}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}",
        ]

        return "\n".join(lines)

    def _generate_principles_content(self) -> str:
        """Generate principles section content."""
        lines = [
            "## Development Principles",
            "",
        ]

        # Universal principles
        universal = self._get_universal_principles()
        if universal:
            lines.append(f"<!-- Universal Principles ({len(universal)}) -->")
            for p in sorted(universal):
                lines.append(f"@.claude/principles/{p}.md")
            lines.append("")

        # Project-specific principles
        project_specific = self._get_project_specific_principles()
        if project_specific:
            lines.append(f"<!-- Project-Specific Principles ({len(project_specific)}) -->")
            for p in sorted(project_specific):
                lines.append(f"@.claude/principles/{p}.md")
            lines.append("")

        # Claude guidelines
        claude_guidelines = self._get_claude_guidelines()
        if claude_guidelines:
            lines.append(f"<!-- Claude Guidelines ({len(claude_guidelines)}) -->")
            for p in sorted(claude_guidelines):
                lines.append(f"@.claude/principles/{p}.md")

        return "\n".join(lines)

    def _generate_skills_content(self) -> str:
        """Generate skills section content."""
        lines = ["## Available Skills", ""]

        if not self.selected_skills:
            lines.append("<!-- No skills selected for this project -->")
            return "\n".join(lines)

        # Group skills by type (core vs language-specific)
        core_skills = []
        python_skills = []

        for skill in self.selected_skills:
            # Check if skill is in python subdirectory
            skill_file_python = self.project_root / ".claude" / "skills" / "python" / f"{skill}.md"
            if skill_file_python.exists():
                python_skills.append(skill)
            else:
                core_skills.append(skill)

        # Core skills
        if core_skills:
            lines.append(f"<!-- Core Skills ({len(core_skills)}) -->")
            for skill in sorted(core_skills):
                lines.append(f"@.claude/skills/{skill}.md")
            lines.append("")

        # Python skills
        if python_skills:
            lines.append(f"<!-- Python Skills ({len(python_skills)}) -->")
            for skill in sorted(python_skills):
                lines.append(f"@.claude/skills/python/{skill}.md")

        return "\n".join(lines)

    def _generate_agents_content(self) -> str:
        """Generate agents section content."""
        lines = ["## Available Agents", ""]

        if not self.selected_agents:
            lines.append("<!-- No agents selected for this project -->")
            return "\n".join(lines)

        for agent in sorted(self.selected_agents):
            lines.append(f"@.claude/agents/{agent}.md")

        return "\n".join(lines)

    def _generate_commands_content(self) -> str:
        """Generate commands section content."""
        lines = ["## Available Commands", ""]

        if not self.selected_commands:
            lines.append("- Run `/cco-status` to see all available commands")
            return "\n".join(lines)

        for cmd in sorted(self.selected_commands):
            # Try to read title from frontmatter
            cmd_file = self.project_root / ".claude" / "commands" / f"{cmd}.md"
            title = self._read_frontmatter_field(cmd_file, "title")

            # Fallback to formatted ID
            if not title:
                title = cmd.replace("cco-", "").replace("-", " ").title()

            lines.append(f"- **/{cmd}**: {title}")

        return "\n".join(lines)


    def _generate_guides_content(self) -> str:
        """Generate guides section content."""
        lines = ["## Available Guides", ""]

        if not self.selected_guides:
            lines.append("<!-- No guides selected for this project -->")
            return "\n".join(lines)

        for guide in sorted(self.selected_guides):
            lines.append(f"@.claude/guides/{guide}.md")

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
        """Get list of project-specific principle IDs from .claude/principles/P_*.md"""
        project_specific = []
        if self.principles_dir.exists():
            for file in self.principles_dir.glob("P_*.md"):
                project_specific.append(file.stem)
        return project_specific

    def _get_claude_guidelines(self) -> List[str]:
        """Get list of Claude guideline IDs."""
        claude = []
        if self.principles_dir.exists():
            for file in self.principles_dir.glob("C_*.md"):
                claude.append(file.stem)
        return claude

    def _read_frontmatter_field(
        self, file_path: Path, field_name: str, nested_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Read a field from markdown frontmatter.

        Args:
            file_path: Path to markdown file
            field_name: Field name to extract (e.g., 'title', 'name')
            nested_path: Nested path for fields like 'metadata.name'

        Returns:
            Field value or None
        """
        if not file_path.exists():
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            # Match YAML frontmatter
            match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if match:
                frontmatter = match.group(1)

                # Handle nested fields (e.g., metadata.name)
                if nested_path:
                    # Simple nested field support
                    nested_match = re.search(
                        rf"^{nested_path}:\s*\n\s+{field_name}:\s*[\"']?(.+?)[\"']?$",
                        frontmatter,
                        re.MULTILINE,
                    )
                    if nested_match:
                        return nested_match.group(1).strip()
                else:
                    # Direct field
                    field_match = re.search(
                        rf"^{field_name}:\s*(.+)$", frontmatter, re.MULTILINE
                    )
                    if field_match:
                        return field_match.group(1).strip().strip('"\'')
        except Exception:
            pass

        return None

    def _read_markdown_title(self, file_path: Path) -> Optional[str]:
        """Read title from markdown header (# Title)."""
        if not file_path.exists():
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            # Skip frontmatter if exists
            content_without_frontmatter = re.sub(
                r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL
            )
            # Extract first # header
            header_match = re.search(r"^#\s+(.+)$", content_without_frontmatter, re.MULTILINE)
            if header_match:
                return header_match.group(1).strip()
        except Exception:
            pass

        return None

    def _get_principle_title(self, principle_id: str) -> str:
        """Get human-readable title for principle from frontmatter."""
        # Try to read from actual file in .claude/principles/
        principle_file = self.principles_dir / f"{principle_id}.md"
        title = self._read_frontmatter_field(principle_file, "title")

        if title:
            return title

        # Fallback to formatted ID
        return principle_id.replace("_", " ").title()

