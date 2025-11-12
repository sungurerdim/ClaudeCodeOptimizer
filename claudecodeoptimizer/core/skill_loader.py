"""
Skill Loader - Progressive Disclosure System

Implements 3-tier loading for skills:
- Tier 1: Metadata only (~50 tokens)
- Tier 2: + Instructions (~150 tokens)
- Tier 3: + Examples & Resources (~500 tokens)

Pattern from wshobson/agents for token optimization.
"""

**STATUS**: ⚠️ NOT CURRENTLY INTEGRATED
This module is fully implemented but not yet integrated into the codebase.
Future integration planned for progressive disclosure for skills.

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class SkillMetadata:
    """Skill metadata (Tier 1)"""

    name: str
    activation_keywords: List[str]
    category: str
    summary: str
    token_estimate: int = 50


class SkillLoader:
    """Progressive disclosure loader for skills"""

    def __init__(self, skills_dir: Optional[Path] = None) -> None:
        """
        Initialize skill loader.

        Args:
            skills_dir: Base directory for skills (default: ~/.cco/skills/)
        """
        if skills_dir is None:
            from ..config import CCOConfig
            skills_dir = CCOConfig.get_skills_dir()

        if not skills_dir.exists():
            raise FileNotFoundError(
                f"Skills directory not found: {skills_dir}\n"
                f"Please ensure CCO is properly installed."
            )

        self.skills_dir = skills_dir
        self._metadata_cache: Dict[str, SkillMetadata] = {}
        self._instructions_cache: Dict[str, str] = {}
        self._resources_cache: Dict[str, str] = {}

    def load_skill_metadata(self, skill_path: Path) -> SkillMetadata:
        """
        Load only metadata from skill file (Tier 1: ~50 tokens).

        Args:
            skill_path: Path to skill .md file

        Returns:
            SkillMetadata with name, keywords, category, summary
        """
        cache_key = str(skill_path)
        if cache_key in self._metadata_cache:
            return self._metadata_cache[cache_key]

        content = skill_path.read_text(encoding="utf-8")

        # Parse frontmatter metadata
        metadata_match = re.search(
            r"^---\s*\nmetadata:\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE
        )

        if metadata_match:
            # Parse YAML-style metadata
            metadata_text = metadata_match.group(1)
            name_match = re.search(r'name:\s*["\']?([^"\'\n]+)["\']?', metadata_text)
            keywords_match = re.search(
                r"activation_keywords:\s*\[(.*?)\]", metadata_text
            )
            category_match = re.search(
                r'category:\s*["\']?([^"\'\n]+)["\']?', metadata_text
            )

            name = name_match.group(1).strip() if name_match else skill_path.stem
            keywords = (
                [
                    k.strip().strip('"').strip("'")
                    for k in keywords_match.group(1).split(",")
                ]
                if keywords_match
                else []
            )
            category = (
                category_match.group(1).strip() if category_match else "general"
            )
        else:
            # Fallback: use filename
            name = skill_path.stem.replace("-", " ").title()
            keywords = [skill_path.stem]
            category = "general"

        # Extract summary (first paragraph after metadata)
        summary_match = re.search(
            r"^---.*?---\s*\n+#[^\n]+\s*\n+(.*?)(?:\n\n|\n#)", content, re.DOTALL
        )
        summary = (
            summary_match.group(1).strip()[:200] if summary_match else "No summary"
        )

        metadata = SkillMetadata(
            name=name, activation_keywords=keywords, category=category, summary=summary
        )

        self._metadata_cache[cache_key] = metadata
        return metadata

    def load_skill_instructions(self, skill_path: Path) -> str:
        """
        Load instructions section (Tier 2: ~150 tokens).

        Args:
            skill_path: Path to skill .md file

        Returns:
            Instructions section content
        """
        cache_key = str(skill_path)
        if cache_key in self._instructions_cache:
            return self._instructions_cache[cache_key]

        content = skill_path.read_text(encoding="utf-8")

        # Extract content between <!-- INSTRUCTIONS --> markers or ## Detailed Instructions
        instructions_match = re.search(
            r"<!-- INSTRUCTIONS:.*?-->\s*\n(.*?)(?:<!-- RESOURCES:|$)",
            content,
            re.DOTALL,
        )

        if not instructions_match:
            # Fallback: look for ## Detailed Instructions or ## Instructions
            instructions_match = re.search(
                r"##\s+(?:Detailed\s+)?Instructions\s*\n(.*?)(?:\n##|$)",
                content,
                re.DOTALL,
            )

        instructions = (
            instructions_match.group(1).strip() if instructions_match else ""
        )
        self._instructions_cache[cache_key] = instructions
        return instructions

    def load_skill_resources(self, skill_path: Path) -> str:
        """
        Load examples & resources section (Tier 3: ~500 tokens).

        Args:
            skill_path: Path to skill .md file

        Returns:
            Resources section content
        """
        cache_key = str(skill_path)
        if cache_key in self._resources_cache:
            return self._resources_cache[cache_key]

        content = skill_path.read_text(encoding="utf-8")

        # Extract content after <!-- RESOURCES --> marker or ## Examples & Resources
        resources_match = re.search(
            r"<!-- RESOURCES:.*?-->\s*\n(.*?)$", content, re.DOTALL
        )

        if not resources_match:
            # Fallback: look for ## Examples or ## Resources sections
            resources_match = re.search(
                r"##\s+(?:Examples|Resources).*?\n(.*?)$", content, re.DOTALL
            )

        resources = resources_match.group(1).strip() if resources_match else ""
        self._resources_cache[cache_key] = resources
        return resources

    def is_activated(self, skill_path: Path, context: str) -> bool:
        """
        Check if skill should be activated based on context.

        Args:
            skill_path: Path to skill file
            context: Context string (e.g., user query, command name)

        Returns:
            True if any activation keyword found in context
        """
        metadata = self.load_skill_metadata(skill_path)
        context_lower = context.lower()

        return any(
            keyword.lower() in context_lower
            for keyword in metadata.activation_keywords
        )

    def discover_skills(self, category: Optional[str] = None) -> List[Path]:
        """
        Discover all skill files in skills directory.

        Args:
            category: Optional category filter

        Returns:
            List of skill file paths
        """
        if not self.skills_dir.exists():
            return []

        skills = list(self.skills_dir.glob("*.md"))

        if category:
            # Filter by category
            filtered = []
            for skill in skills:
                metadata = self.load_skill_metadata(skill)
                if metadata.category == category:
                    filtered.append(skill)
            return filtered

        return skills

    def load_full_skill(self, skill_path: Path) -> str:
        """
        Load complete skill (all 3 tiers).

        Args:
            skill_path: Path to skill file

        Returns:
            Full skill content
        """
        return skill_path.read_text(encoding="utf-8")

    def clear_cache(self) -> None:
        """Clear all caches."""
        self._metadata_cache.clear()
        self._instructions_cache.clear()
        self._resources_cache.clear()
