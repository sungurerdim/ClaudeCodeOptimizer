"""
Unit tests for RecommendationService

Tests the centralized recommendation service for CCO file recommendations.
Target Coverage: 100%
"""

from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.core.recommendation_service import (
    RecommendationService,
    recommendation_service,
)


class TestRecommendationServiceInit:
    """Test RecommendationService initialization"""

    def test_init_creates_metadata_manager_reference(self) -> None:
        """Test that init sets metadata manager reference"""
        service = RecommendationService()
        assert service.metadata is not None
        assert hasattr(service.metadata, "recommend_files")

    def test_singleton_instance_exists(self) -> None:
        """Test that singleton instance is available"""
        assert recommendation_service is not None
        assert isinstance(recommendation_service, RecommendationService)


class TestRecommendSkills:
    """Test recommend_skills method"""

    def test_recommend_skills_universal_only(self) -> None:
        """Test recommending universal skills (no language specified)"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {
            "project_maturity": "production",
            "team_dynamics": "small-2-5",
        }

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-skill-testing", "cco-skill-security"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = ["cco-skill-testing", "cco-skill-security", "cco-skill-api"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers)

        assert "cco-skill-testing" in result
        assert "cco-skill-security" in result

    def test_recommend_skills_with_detected_languages(self) -> None:
        """Test recommending skills with language-specific skills"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}
        detected_languages = ["python", "javascript"]

        with patch.object(service, "metadata") as mock_metadata:
            # First call for universal, then for each language
            mock_metadata.recommend_files.side_effect = [
                ["cco-skill-testing"],  # Universal
                ["python/cco-skill-async"],  # Python
                ["javascript/cco-skill-react"],  # JavaScript
            ]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = [
                    "cco-skill-testing",
                    "python/cco-skill-async",
                    "python/cco-skill-typing",
                    "javascript/cco-skill-react",
                ]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers, detected_languages)

        assert "cco-skill-testing" in result
        assert "python/cco-skill-async" in result
        assert "javascript/cco-skill-react" in result

    def test_recommend_skills_removes_duplicates(self) -> None:
        """Test that duplicate recommendations are removed"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}
        detected_languages = ["python"]

        with patch.object(service, "metadata") as mock_metadata:
            # Return same skill from multiple sources
            mock_metadata.recommend_files.side_effect = [
                ["cco-skill-testing"],  # Universal
                ["cco-skill-testing"],  # Python (duplicate)
            ]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = [
                    "cco-skill-testing",
                    "python/cco-skill-async",
                ]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers, detected_languages)

        # Should only appear once
        assert result.count("cco-skill-testing") == 1

    def test_recommend_skills_empty_context(self) -> None:
        """Test recommending skills with empty context"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = ["cco-skill-testing"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers)

        assert result == []

    def test_recommend_skills_filters_universal_correctly(self) -> None:
        """Test that universal skills don't have '/' in path"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-skill-testing"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                # Mix of universal and language-specific
                mock_skills.return_value = [
                    "cco-skill-testing",  # Universal (no /)
                    "python/cco-skill-async",  # Language-specific
                    "cco-skill-api",  # Universal
                ]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers)

        # Verify recommend_files was called with only universal skills
        call_args = mock_metadata.recommend_files.call_args
        available_files = call_args[1]["available_files"]
        assert "cco-skill-testing" in available_files
        assert "cco-skill-api" in available_files
        assert "python/cco-skill-async" not in available_files

    def test_recommend_skills_language_case_insensitive(self) -> None:
        """Test that language matching is case-insensitive"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}
        detected_languages = ["Python"]  # Uppercase

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.side_effect = [
                [],  # Universal
                ["python/cco-skill-async"],  # Python (lowercase match)
            ]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = [
                    "python/cco-skill-async",
                ]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    result = service.recommend_skills(context_answers, detected_languages)

        assert "python/cco-skill-async" in result


class TestRecommendAgents:
    """Test recommend_agents method"""

    def test_recommend_agents_basic(self) -> None:
        """Test basic agent recommendation"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {
            "project_maturity": "production",
            "development_philosophy": "quality_first",
        }

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-agent-audit", "cco-agent-fix"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents:
                mock_agents.return_value = ["cco-agent-audit", "cco-agent-fix", "cco-agent-generate"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/agents")

                    result = service.recommend_agents(context_answers)

        assert "cco-agent-audit" in result
        assert "cco-agent-fix" in result
        mock_metadata.recommend_files.assert_called_once()

    def test_recommend_agents_empty_context(self) -> None:
        """Test agent recommendation with empty context"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents:
                mock_agents.return_value = ["cco-agent-audit"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/agents")

                    result = service.recommend_agents(context_answers)

        assert result == []

    def test_recommend_agents_passes_correct_args(self) -> None:
        """Test that correct arguments are passed to recommend_files"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "greenfield"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents:
                mock_agents.return_value = ["cco-agent-audit"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/agents")

                    service.recommend_agents(context_answers)

        # Verify correct arguments
        mock_metadata.recommend_files.assert_called_once_with(
            available_files=["cco-agent-audit"],
            files_dir=Path("/mock/agents"),
            context_answers=context_answers,
        )


class TestRecommendCommands:
    """Test recommend_commands method"""

    def test_recommend_commands_basic(self) -> None:
        """Test basic command recommendation"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {
            "project_maturity": "production",
            "team_dynamics": "medium-6-15",
        }

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-audit", "cco-status"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_commands"
            ) as mock_commands:
                mock_commands.return_value = ["cco-audit", "cco-status", "cco-init"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_global_commands_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/commands")

                    result = service.recommend_commands(context_answers)

        assert "cco-audit" in result
        assert "cco-status" in result

    def test_recommend_commands_empty_context(self) -> None:
        """Test command recommendation with empty context"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_commands"
            ) as mock_commands:
                mock_commands.return_value = ["cco-audit"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_global_commands_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/commands")

                    result = service.recommend_commands(context_answers)

        assert result == []

    def test_recommend_commands_passes_correct_args(self) -> None:
        """Test that correct arguments are passed to recommend_files"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"development_philosophy": "velocity_first"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_commands"
            ) as mock_commands:
                mock_commands.return_value = ["cco-status"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_global_commands_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/commands")

                    service.recommend_commands(context_answers)

        # Verify correct arguments
        mock_metadata.recommend_files.assert_called_once_with(
            available_files=["cco-status"],
            files_dir=Path("/mock/commands"),
            context_answers=context_answers,
        )


class TestRecommendationServiceIntegration:
    """Integration tests for RecommendationService"""

    def test_multiple_recommendations_independence(self) -> None:
        """Test that skills, agents, commands can be recommended independently"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}

        with patch.object(service, "metadata") as mock_metadata:
            # Different results for each type
            mock_metadata.recommend_files.side_effect = [
                ["cco-skill-testing"],  # Skills
                ["cco-agent-audit"],  # Agents
                ["cco-status"],  # Commands
            ]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills, patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents, patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_commands"
            ) as mock_commands, patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
            ) as mock_skills_dir, patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
            ) as mock_agents_dir, patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_global_commands_dir"
            ) as mock_commands_dir:

                mock_skills.return_value = ["cco-skill-testing"]
                mock_agents.return_value = ["cco-agent-audit"]
                mock_commands.return_value = ["cco-status"]
                mock_skills_dir.return_value = Path("/mock/skills")
                mock_agents_dir.return_value = Path("/mock/agents")
                mock_commands_dir.return_value = Path("/mock/commands")

                skills = service.recommend_skills(context_answers)
                agents = service.recommend_agents(context_answers)
                commands = service.recommend_commands(context_answers)

        assert skills == ["cco-skill-testing"]
        assert agents == ["cco-agent-audit"]
        assert commands == ["cco-status"]

    def test_consistent_context_passing(self) -> None:
        """Test that same context is passed to all recommendation methods"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {
            "project_maturity": "production",
            "team_dynamics": "large-16-plus",
            "development_philosophy": "quality_first",
        }

        captured_contexts: List[Dict[str, Any]] = []

        def capture_context(**kwargs: Any) -> List[str]:
            captured_contexts.append(kwargs.get("context_answers", {}))
            return []

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.side_effect = capture_context

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills, patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents, patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_commands"
            ) as mock_commands, patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
            ), patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
            ), patch(
                "claudecodeoptimizer.core.recommendation_service.config.get_global_commands_dir"
            ):

                mock_skills.return_value = []
                mock_agents.return_value = []
                mock_commands.return_value = []

                service.recommend_skills(context_answers)
                service.recommend_agents(context_answers)
                service.recommend_commands(context_answers)

        # All captured contexts should match
        for captured in captured_contexts:
            assert captured == context_answers


class TestRecommendationServiceEdgeCases:
    """Edge case tests for RecommendationService"""

    def test_none_detected_languages(self) -> None:
        """Test handling of None detected_languages"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-skill-testing"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = ["cco-skill-testing"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    # Explicit None
                    result = service.recommend_skills(context_answers, None)

        assert "cco-skill-testing" in result
        # Should only call recommend_files once (for universal)
        assert mock_metadata.recommend_files.call_count == 1

    def test_empty_detected_languages_list(self) -> None:
        """Test handling of empty detected_languages list"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = ["cco-skill-testing"]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = ["cco-skill-testing"]

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    # Empty list
                    result = service.recommend_skills(context_answers, [])

        assert "cco-skill-testing" in result
        # Should only call recommend_files once (for universal)
        assert mock_metadata.recommend_files.call_count == 1

    def test_no_available_files(self) -> None:
        """Test handling when no files are available"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.return_value = []

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_agents"
            ) as mock_agents:
                mock_agents.return_value = []  # No agents available

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_agents_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/agents")

                    result = service.recommend_agents(context_answers)

        assert result == []

    def test_special_characters_in_language_name(self) -> None:
        """Test handling of special characters in language names"""
        service = RecommendationService()
        context_answers: Dict[str, Any] = {"project_maturity": "production"}
        detected_languages = ["c++", "c#"]

        with patch.object(service, "metadata") as mock_metadata:
            mock_metadata.recommend_files.side_effect = [
                [],  # Universal
                [],  # c++
                [],  # c#
            ]

            with patch(
                "claudecodeoptimizer.core.recommendation_service.get_available_skills"
            ) as mock_skills:
                mock_skills.return_value = []

                with patch(
                    "claudecodeoptimizer.core.recommendation_service.config.get_skills_dir"
                ) as mock_dir:
                    mock_dir.return_value = Path("/mock/skills")

                    # Should not raise
                    result = service.recommend_skills(context_answers, detected_languages)

        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
