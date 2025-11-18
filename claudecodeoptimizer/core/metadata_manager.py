"""
Centralized Metadata Manager (SSOT)

Single Source of Truth for all file metadata parsing and recommendation logic.
Applies DRY principle: one implementation for guides, skills, agents, commands, principles.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class MetadataManager:
    """
    Singleton manager for all CCO file metadata.

    Handles:
    - Frontmatter parsing (YAML)
    - use_cases extraction
    - Context matching
    - Generic recommendations for all file types
    """

    _instance: Optional["MetadataManager"] = None

    def __new__(cls) -> "MetadataManager":
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def parse_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse frontmatter from markdown file.

        Returns dict with all frontmatter fields including:
        - title
        - description
        - category
        - use_cases
        - tags
        - metadata (nested)
        - principles
        """
        if not file_path.exists():
            return {}

        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract frontmatter between --- markers
            match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if not match:
                return {}

            frontmatter = yaml.safe_load(match.group(1))
            return frontmatter or {}

        except Exception as e:
            logger.debug(f"Failed to parse frontmatter from {file_path}: {e}")
            return {}

    def get_description(self, file_path: Path) -> str:
        """
        Get description from frontmatter or first paragraph.

        Priority:
        1. frontmatter['description']
        2. First non-heading paragraph
        """
        frontmatter = self.parse_frontmatter(file_path)
        if "description" in frontmatter:
            return frontmatter["description"]

        # Fallback: extract first paragraph
        try:
            content = file_path.read_text(encoding="utf-8")
            # Remove frontmatter
            content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

            # Find first non-heading paragraph
            lines = content.split("\n")
            paragraph_lines: List[str] = []
            for line in lines:
                line_stripped = line.strip()
                # Skip headings and empty lines
                if not line_stripped or line_stripped.startswith("#"):
                    if paragraph_lines:  # End of paragraph
                        break
                    continue
                paragraph_lines.append(line_stripped)

            if paragraph_lines:
                return " ".join(paragraph_lines)[:100]  # Limit to 100 chars

        except Exception:
            pass

        return ""

    def get_use_cases(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Get use_cases from frontmatter.

        Returns dict like:
        {
            "development_philosophy": ["quality_first"],
            "project_maturity": ["production", "legacy"],
            "team_dynamics": ["small-2-5"],
            "project_purpose": ["backend", "api"],
            ...
        }
        """
        frontmatter = self.parse_frontmatter(file_path)
        return frontmatter.get("use_cases", {})

    def matches_context(
        self, use_cases: Dict[str, List[str]], context_answers: Dict[str, Any]
    ) -> bool:
        """
        Check if use_cases match context answers.

        Returns True if ANY use_case criterion matches.

        Args:
            use_cases: From file frontmatter
            context_answers: From AnswerContext.answers

        Example:
            use_cases = {"project_maturity": ["production"], "team_dynamics": ["small-2-5"]}
            context_answers = {"project_maturity": "production", "team_dynamics": "solo"}
            returns True (maturity matches)
        """
        if not use_cases:
            return False

        for criterion, expected_values in use_cases.items():
            answer = context_answers.get(criterion)

            # Handle list answers (like project_purpose: ["backend", "api"])
            if isinstance(answer, list):
                # Match if any answer value is in expected values
                if any(val in expected_values for val in answer):
                    return True

            # Handle single value answers
            elif answer in expected_values:
                return True

        return False

    def recommend_files(
        self,
        available_files: List[str],
        files_dir: Path,
        context_answers: Dict[str, Any],
        file_extension: str = ".md",
    ) -> List[str]:
        """
        Generic recommendation engine for any file type.

        Args:
            available_files: List of file IDs (e.g., ["cco-status", "cco-audit"])
            files_dir: Directory containing files (e.g., ~/.claude/commands/)
            context_answers: User's answer context
            file_extension: File extension (default: .md)

        Returns:
            List of recommended file IDs
        """
        recommended = []

        for file_id in available_files:
            # Handle nested paths (e.g., python/cco-skill-async-patterns)
            if "/" in file_id:
                parts = file_id.split("/")
                file_path = files_dir / parts[0] / f"{parts[1]}{file_extension}"
            else:
                file_path = files_dir / f"{file_id}{file_extension}"

            use_cases = self.get_use_cases(file_path)

            # Recommend if use_cases match context
            if self.matches_context(use_cases, context_answers):
                recommended.append(file_id)

        return recommended


# Singleton instance
metadata_manager = MetadataManager()
