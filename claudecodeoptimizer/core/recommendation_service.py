"""
Recommendation Service (Recommendation Layer)

Centralized service for AI-powered file recommendations.
Uses MetadataManager for metadata parsing and context matching.

Separation of Concerns:
- MetadataManager: Parses metadata, matches context (pure logic)
- RecommendationService: Business logic, applies recommendation strategy
- Orchestrator: Only orchestrates, no recommendation logic
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .. import config
from .knowledge_setup import (
    get_available_agents,
    get_available_commands,
    get_available_guides,
    get_available_skills,
)
from .metadata_manager import metadata_manager


class RecommendationService:
    """
    Centralized recommendation service for all CCO file types.

    SSOT for recommendation logic across guides, skills, agents, commands.
    """

    def __init__(self) -> None:
        """Initialize recommendation service"""
        self.metadata = metadata_manager

    # ========================================================================
    # GUIDES
    # ========================================================================

    def recommend_guides(self, context_answers: Dict[str, Any]) -> List[str]:
        """
        Recommend guides based on context answers.

        Uses metadata-based matching from guide frontmatter.
        """
        available_guides = get_available_guides()
        guides_dir = config.get_guides_dir()

        return self.metadata.recommend_files(
            available_files=available_guides,
            files_dir=guides_dir,
            context_answers=context_answers,
        )

    # ========================================================================
    # SKILLS
    # ========================================================================

    def recommend_skills(
        self, context_answers: Dict[str, Any], detected_languages: Optional[List[str]] = None
    ) -> List[str]:
        """
        Recommend skills based on context + detected languages.

        Returns:
        - Universal skills (metadata-matched)
        - Language-specific skills (if language detected)
        """
        available_skills = get_available_skills()
        skills_dir = config.get_skills_dir()

        recommended = []

        # Universal skills (no "/" in path)
        universal_skills = [s for s in available_skills if "/" not in s]
        recommended.extend(
            self.metadata.recommend_files(
                available_files=universal_skills,
                files_dir=skills_dir,
                context_answers=context_answers,
            )
        )

        # Language-specific skills
        if detected_languages:
            for lang in detected_languages:
                lang_lower = lang.lower()
                # Get all skills for this language
                lang_skills = [s for s in available_skills if s.startswith(f"{lang_lower}/")]

                # Metadata-match language skills
                recommended.extend(
                    self.metadata.recommend_files(
                        available_files=lang_skills,
                        files_dir=skills_dir,
                        context_answers=context_answers,
                    )
                )

        return list(set(recommended))  # Remove duplicates

    # ========================================================================
    # AGENTS
    # ========================================================================

    def recommend_agents(self, context_answers: Dict[str, Any]) -> List[str]:
        """
        Recommend agents based on context answers.

        Uses metadata-based matching from agent frontmatter.
        """
        available_agents = get_available_agents()
        agents_dir = config.get_agents_dir()

        return self.metadata.recommend_files(
            available_files=available_agents,
            files_dir=agents_dir,
            context_answers=context_answers,
        )

    # ========================================================================
    # COMMANDS
    # ========================================================================

    def recommend_commands(self, context_answers: Dict[str, Any]) -> List[str]:
        """
        Recommend commands based on context answers.

        Uses metadata-based matching from command frontmatter.
        """
        available_commands = get_available_commands()
        commands_dir = config.get_global_commands_dir()

        return self.metadata.recommend_files(
            available_files=available_commands,
            files_dir=commands_dir,
            context_answers=context_answers,
        )


# Singleton instance
recommendation_service = RecommendationService()
