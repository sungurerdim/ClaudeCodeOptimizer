"""
Comprehensive tests for wizard context_matrix module.

Tests cover:
- Context matrix building and management
- All matrix operations and recommendation methods
- Integration with wizard components
- External dependency mocking
- Edge cases and error handling

Target: 80%+ coverage
"""

from unittest.mock import patch

import pytest

from claudecodeoptimizer.wizard.context_matrix import (
    ContextMatrix,
    _get_available_principle_count,
)
from claudecodeoptimizer.wizard.models import AnswerContext, Option, SystemContext


class TestGetAvailablePrincipleCount:
    """Test _get_available_principle_count helper function"""

    def test_count_principles_when_directory_exists(self, tmp_path):
        """Test counting principles from existing directory"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create some principle files
        (principles_dir / "P_TEST_1.md").touch()
        (principles_dir / "P_TEST_2.md").touch()
        (principles_dir / "P_ANOTHER.md").touch()
        (principles_dir / "U_UNIVERSAL.md").touch()  # Should not be counted
        (principles_dir / "README.md").touch()  # Should not be counted

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            count = _get_available_principle_count()
            assert count == 3  # Only P*.md files

    def test_count_principles_when_directory_missing(self, tmp_path):
        """Test counting principles when directory doesn't exist"""
        nonexistent = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=nonexistent):
            count = _get_available_principle_count()
            assert count == 0

    def test_count_principles_empty_directory(self, tmp_path):
        """Test counting principles from empty directory"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            count = _get_available_principle_count()
            assert count == 0


class TestContextMatrixVersioningStrategy:
    """Test recommend_versioning_strategy method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    def test_solo_developer_strategy(self, matrix):
        """Test versioning strategy for solo developer"""
        result = matrix.recommend_versioning_strategy("solo", "prototype", has_ci=False)

        assert result["strategy"] == "auto_semver"
        assert "Zero overhead" in result["reason"]
        assert "manual_semver" in result["alternatives"]
        assert "calver" in result["alternatives"]

    def test_small_team_with_ci_production(self, matrix):
        """Test versioning strategy for small team with CI in production"""
        result = matrix.recommend_versioning_strategy("small_team", "production", has_ci=True)

        assert result["strategy"] == "pr_based_semver"
        assert "PR merge" in result["reason"]
        assert "auto_semver" in result["alternatives"]
        assert "manual_semver" in result["alternatives"]

    def test_small_team_with_ci_legacy(self, matrix):
        """Test versioning strategy for small team with CI in legacy"""
        result = matrix.recommend_versioning_strategy("small_team", "legacy", has_ci=True)

        assert result["strategy"] == "pr_based_semver"
        assert "PR merge" in result["reason"]

    def test_small_team_without_ci(self, matrix):
        """Test versioning strategy for small team without CI"""
        result = matrix.recommend_versioning_strategy("small_team", "mvp", has_ci=False)

        assert result["strategy"] == "auto_semver"
        assert "upgrade to PR-based" in result["reason"]
        assert "manual_semver" in result["alternatives"]

    def test_small_team_prototype_without_ci(self, matrix):
        """Test versioning strategy for small team in prototype phase without CI"""
        result = matrix.recommend_versioning_strategy("small_team", "prototype", has_ci=False)

        assert result["strategy"] == "auto_semver"
        assert "manual_semver" in result["alternatives"]

    def test_large_org_strategy(self, matrix):
        """Test versioning strategy for large organization"""
        result = matrix.recommend_versioning_strategy("large_org", "production", has_ci=True)

        assert result["strategy"] == "manual_semver"
        assert "release managers" in result["reason"]
        assert "pr_based_semver" in result["alternatives"]

    def test_default_strategy(self, matrix):
        """Test default versioning strategy for unknown team size"""
        result = matrix.recommend_versioning_strategy("unknown_size", "mvp", has_ci=False)

        assert result["strategy"] == "auto_semver"
        assert "Balanced approach" in result["reason"]
        assert result["alternatives"] == {}


class TestContextMatrixPrincipleIntensity:
    """Test recommend_principle_intensity method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    def test_minimal_intensity_solo_prototype_move_fast(self, matrix, tmp_path):
        """Test minimal intensity for solo developer prototype with move fast"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("solo", "prototype", "move_fast")

            assert result["intensity"] == "minimal"
            assert result["score"] == 2  # 5 + 0 - 2 - 1 = 2
            assert "core principles only" in result["reason"]
            assert "Prototype phase" in result["reason"]
            assert "Move fast" in result["reason"]
            # Check principle count scaling
            assert "-" in result["principle_count"]

    def test_recommended_intensity_solo_mvp_balanced(self, matrix, tmp_path):
        """Test recommended intensity for balanced solo developer MVP"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("solo", "mvp", "balanced")

            assert result["intensity"] == "recommended"
            assert result["score"] == 5  # 5 + 0 + 0 + 0 = 5
            assert "Balanced approach" in result["reason"]

    def test_recommended_intensity_small_team_mvp_balanced(self, matrix, tmp_path):
        """Test recommended intensity for small team MVP balanced"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("small_team", "mvp", "balanced")

            assert result["intensity"] == "recommended"
            assert result["score"] == 6  # 5 + 1 + 0 + 0 = 6
            assert "Team collaboration" in result["reason"]
            assert "MVP phase" in result["reason"]

    def test_comprehensive_intensity_small_team_production_balanced(self, matrix, tmp_path):
        """Test comprehensive intensity for small team production balanced"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("small_team", "production", "balanced")

            # 5 + 1 (small_team) + 2 (production) + 0 (balanced) = 8
            assert result["intensity"] == "comprehensive"
            assert result["score"] == 8
            assert "Strong foundation" in result["reason"]
            assert "Production system" in result["reason"]

    def test_comprehensive_intensity_production_quality_first(self, matrix, tmp_path):
        """Test comprehensive intensity for production quality first"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity(
                "small_team", "production", "quality_first"
            )

            # 5 + 1 (small_team) + 2 (production) + 2 (quality_first) = 10
            assert result["intensity"] == "maximum"
            assert result["score"] == 10
            assert "Maximum quality" in result["reason"]
            assert "Quality-first" in result["reason"]

    def test_comprehensive_intensity_large_org_mvp(self, matrix, tmp_path):
        """Test comprehensive intensity for large org in MVP"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("large_org", "mvp", "balanced")

            # 5 + 3 (large_org) + 0 (mvp) + 0 (balanced) = 8
            assert result["intensity"] == "comprehensive"
            assert result["score"] == 8
            assert "Strong foundation" in result["reason"]
            assert "Large team requires comprehensive standards" in result["reason"]

    def test_comprehensive_intensity_large_org_production(self, matrix, tmp_path):
        """Test comprehensive intensity for large org in production"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("large_org", "production", "balanced")

            # 5 + 3 (large_org) + 2 (production) + 0 (balanced) = 10
            assert result["intensity"] == "maximum"
            assert result["score"] == 10
            assert "Maximum quality" in result["reason"]

    def test_maximum_intensity_large_org_quality_first(self, matrix, tmp_path):
        """Test maximum intensity for large org quality first"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity(
                "large_org", "production", "quality_first"
            )

            assert result["intensity"] == "maximum"
            assert result["score"] == 10  # 5 + 3 + 2 + 2 = 12, clamped to 10
            assert "Maximum quality" in result["reason"]
            assert "Quality-first" in result["reason"]
            assert "+" in result["principle_count"]

    def test_score_clamping_minimum(self, matrix, tmp_path):
        """Test score is clamped to minimum of 1"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        for i in range(50):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("solo", "prototype", "move_fast")

            # 5 + 0 - 2 - 1 = 2, should still be >= 1
            assert result["score"] >= 1
            assert result["intensity"] in ["minimal", "recommended"]

    def test_principle_count_scaling_with_low_total(self, matrix, tmp_path):
        """Test principle count scaling when total available is low"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()
        # Only 5 principles available
        for i in range(5):
            (principles_dir / f"P_TEST_{i}.md").touch()

        with patch("claudecodeoptimizer.config.get_principles_dir", return_value=principles_dir):
            result = matrix.recommend_principle_intensity("solo", "prototype", "move_fast")

            # Should still provide reasonable counts
            assert result["intensity"] == "minimal"
            # Minimum is max(5, int(5 * 0.07)) = 5
            assert "5" in result["principle_count"] or "-" in result["principle_count"]


class TestContextMatrixPrecommitHooks:
    """Test recommend_precommit_hooks method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    def test_solo_without_ci(self, matrix):
        """Test pre-commit hooks for solo developer without CI"""
        hooks = matrix.recommend_precommit_hooks("solo", has_ci=False)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" not in hooks
        assert "type-check" not in hooks
        assert "test" not in hooks

    def test_solo_with_ci(self, matrix):
        """Test pre-commit hooks for solo developer with CI"""
        hooks = matrix.recommend_precommit_hooks("solo", has_ci=True)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" not in hooks
        assert "test" not in hooks

    def test_small_team_without_ci(self, matrix):
        """Test pre-commit hooks for small team without CI"""
        hooks = matrix.recommend_precommit_hooks("small_team", has_ci=False)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" in hooks
        assert "test" in hooks  # Added because no CI
        assert "type-check" not in hooks

    def test_small_team_with_ci(self, matrix):
        """Test pre-commit hooks for small team with CI"""
        hooks = matrix.recommend_precommit_hooks("small_team", has_ci=True)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" in hooks
        assert "test" not in hooks  # CI handles testing
        assert "type-check" not in hooks

    def test_large_org_without_ci(self, matrix):
        """Test pre-commit hooks for large org without CI"""
        hooks = matrix.recommend_precommit_hooks("large_org", has_ci=False)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" in hooks
        assert "type-check" in hooks
        assert "test" in hooks

    def test_large_org_with_ci(self, matrix):
        """Test pre-commit hooks for large org with CI"""
        hooks = matrix.recommend_precommit_hooks("large_org", has_ci=True)

        assert "format" in hooks
        assert "secrets" in hooks
        assert "lint" in hooks
        assert "type-check" in hooks
        assert "test" not in hooks  # CI handles testing


class TestContextMatrixGitWorkflow:
    """Test recommend_git_workflow method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    def test_solo_workflow(self, matrix):
        """Test git workflow for solo developer"""
        result = matrix.recommend_git_workflow("solo", "mvp", has_ci=False)

        assert result["workflow"] == "main_only"
        assert "Simple and fast" in result["reason"]
        assert "github_flow" in result["alternatives"]

    def test_small_team_with_ci(self, matrix):
        """Test git workflow for small team with CI"""
        result = matrix.recommend_git_workflow("small_team", "production", has_ci=True)

        assert result["workflow"] == "github_flow"
        assert "Feature branches" in result["reason"]
        assert "CI checks" in result["reason"]
        assert "main_only" in result["alternatives"]
        assert "git_flow" in result["alternatives"]

    def test_small_team_without_ci(self, matrix):
        """Test git workflow for small team without CI"""
        result = matrix.recommend_git_workflow("small_team", "mvp", has_ci=False)

        assert result["workflow"] == "main_only"
        assert "upgrade to GitHub Flow" in result["reason"]
        assert "github_flow" in result["alternatives"]

    def test_large_org_production(self, matrix):
        """Test git workflow for large org in production"""
        result = matrix.recommend_git_workflow("large_org", "production", has_ci=True)

        assert result["workflow"] == "git_flow"
        assert "Structured releases" in result["reason"]
        assert "trunk_based" in result["alternatives"]

    def test_large_org_legacy(self, matrix):
        """Test git workflow for large org legacy system"""
        result = matrix.recommend_git_workflow("large_org", "legacy", has_ci=True)

        assert result["workflow"] == "git_flow"
        assert "develop/release branches" in result["reason"]

    def test_large_org_mvp(self, matrix):
        """Test git workflow for large org MVP"""
        result = matrix.recommend_git_workflow("large_org", "mvp", has_ci=False)

        assert result["workflow"] == "github_flow"
        assert "Flexible for growing teams" in result["reason"]
        assert "git_flow" in result["alternatives"]

    def test_default_workflow(self, matrix):
        """Test default git workflow for unknown team size"""
        result = matrix.recommend_git_workflow("unknown", "prototype", has_ci=False)

        assert result["workflow"] == "github_flow"
        assert "Balanced workflow" in result["reason"]
        assert result["alternatives"] == {}


class TestContextMatrixTestingApproach:
    """Test recommend_testing_approach method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    def test_prototype_move_fast(self, matrix):
        """Test testing approach for prototype with move fast"""
        result = matrix.recommend_testing_approach("solo", "prototype", "move_fast")

        assert result["approach"] == "critical_paths"
        assert result["coverage_target"] == "30-50%"
        assert "Test critical paths only" in result["reason"]

    def test_production_quality_first(self, matrix):
        """Test testing approach for production with quality first"""
        result = matrix.recommend_testing_approach("small_team", "production", "quality_first")

        assert result["approach"] == "comprehensive"
        assert result["coverage_target"] == "90%+"
        assert "Production system" in result["reason"]
        assert "quality focus" in result["reason"]

    def test_legacy_quality_first(self, matrix):
        """Test testing approach for legacy system with quality first"""
        result = matrix.recommend_testing_approach("solo", "legacy", "quality_first")

        assert result["approach"] == "comprehensive"
        assert result["coverage_target"] == "90%+"

    def test_large_org_any_maturity(self, matrix):
        """Test testing approach for large org"""
        result = matrix.recommend_testing_approach("large_org", "mvp", "balanced")

        assert result["approach"] == "balanced"
        assert result["coverage_target"] == "80%"
        assert "Large teams" in result["reason"]

    def test_mvp_small_team(self, matrix):
        """Test testing approach for MVP with small team"""
        result = matrix.recommend_testing_approach("small_team", "mvp", "balanced")

        assert result["approach"] == "balanced"
        assert result["coverage_target"] == "70-80%"
        assert "Balanced testing" in result["reason"]

    def test_production_balanced(self, matrix):
        """Test testing approach for production balanced"""
        result = matrix.recommend_testing_approach("solo", "production", "balanced")

        assert result["approach"] == "balanced"
        assert result["coverage_target"] == "70-80%"

    def test_default_critical_paths(self, matrix):
        """Test default testing approach"""
        result = matrix.recommend_testing_approach("solo", "prototype", "balanced")

        assert result["approach"] == "critical_paths"
        assert result["coverage_target"] == "50-70%"
        assert "Focus on critical functionality" in result["reason"]


class TestContextMatrixTeamSpecificNote:
    """Test get_team_specific_note method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    @pytest.fixture
    def system_context(self) -> SystemContext:
        """Sample system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
        )

    def test_no_team_dynamics_answer(self, matrix, system_context):
        """Test returns empty string when team dynamics not answered"""
        context = AnswerContext(system=system_context)
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_team_specific_note(option, context)
        assert note == ""

    def test_option_without_recommended_for(self, matrix, system_context):
        """Test returns empty string when option has no recommended_for"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_team_specific_note(option, context)
        assert note == ""

    def test_option_recommended_for_team_size(self, matrix, system_context):
        """Test returns positive note when option matches team size"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["solo"],
        )

        note = matrix.get_team_specific_note(option, context)
        assert "✓" in note
        assert "solo developers" in note

    def test_solo_option_for_team(self, matrix, system_context):
        """Test warning when solo option shown to team"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "small_team"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["solo"],
        )

        note = matrix.get_team_specific_note(option, context)
        assert "⚠️" in note
        assert "too simple for teams" in note

    def test_large_org_option_for_solo(self, matrix, system_context):
        """Test warning when large org option shown to solo"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["large_org"],
        )

        note = matrix.get_team_specific_note(option, context)
        assert "⚠️" in note
        assert "too high for solo" in note

    def test_small_team_option_for_large_org(self, matrix, system_context):
        """Test warning when small team option shown to large org"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "large_org"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["small_team"],
        )

        note = matrix.get_team_specific_note(option, context)
        assert "⚠️" in note
        assert "not scale to large" in note

    def test_humanize_team_size_solo(self, matrix):
        """Test humanizing solo team size"""
        result = matrix._humanize_team_size("solo")
        assert "solo developers" in result

    def test_humanize_team_size_small_team(self, matrix):
        """Test humanizing small team size"""
        result = matrix._humanize_team_size("small_team")
        assert "small teams" in result
        assert "2-10" in result

    def test_humanize_team_size_large_org(self, matrix):
        """Test humanizing large org size"""
        result = matrix._humanize_team_size("large_org")
        assert "large organizations" in result
        assert "10+" in result

    def test_humanize_team_size_unknown(self, matrix):
        """Test humanizing unknown team size"""
        result = matrix._humanize_team_size("unknown")
        assert result == "unknown"


class TestContextMatrixMaturitySpecificNote:
    """Test get_maturity_specific_note method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    @pytest.fixture
    def system_context(self) -> SystemContext:
        """Sample system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
        )

    def test_no_maturity_answer(self, matrix, system_context):
        """Test returns empty string when maturity not answered"""
        context = AnswerContext(system=system_context)
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_maturity_specific_note(option, context)
        assert note == ""

    def test_option_without_recommended_for(self, matrix, system_context):
        """Test returns empty string when option has no recommended_for"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_maturity_specific_note(option, context)
        assert note == ""

    def test_option_recommended_for_maturity(self, matrix, system_context):
        """Test returns positive note when option matches maturity"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["production"],
        )

        note = matrix.get_maturity_specific_note(option, context)
        assert "✓" in note
        assert "production" in note

    def test_prototype_option_for_production(self, matrix, system_context):
        """Test warning when prototype option shown to production"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["prototype"],
        )

        note = matrix.get_maturity_specific_note(option, context)
        assert "⚠️" in note
        assert "too lightweight" in note

    def test_prototype_option_for_legacy(self, matrix, system_context):
        """Test warning when prototype option shown to legacy"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "legacy"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["prototype"],
        )

        note = matrix.get_maturity_specific_note(option, context)
        assert "⚠️" in note
        assert "too lightweight" in note

    def test_production_option_for_prototype(self, matrix, system_context):
        """Test warning when production option shown to prototype"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "prototype"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["production"],
        )

        note = matrix.get_maturity_specific_note(option, context)
        assert "⚠️" in note
        assert "overkill for prototypes" in note


class TestContextMatrixPhilosophySpecificNote:
    """Test get_philosophy_specific_note method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    @pytest.fixture
    def system_context(self) -> SystemContext:
        """Sample system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
        )

    def test_no_philosophy_answer(self, matrix, system_context):
        """Test returns empty string when philosophy not answered"""
        context = AnswerContext(system=system_context)
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_philosophy_specific_note(option, context)
        assert note == ""

    def test_option_without_recommended_for(self, matrix, system_context):
        """Test returns empty string when option has no recommended_for"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "balanced"},
        )
        option = Option(value="test", label="Test", description="Test")

        note = matrix.get_philosophy_specific_note(option, context)
        assert note == ""

    def test_option_recommended_for_move_fast(self, matrix, system_context):
        """Test positive note for move_fast philosophy"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "move_fast"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["move_fast"],
        )

        note = matrix.get_philosophy_specific_note(option, context)
        assert "✓" in note
        assert "fast iteration" in note

    def test_option_recommended_for_balanced(self, matrix, system_context):
        """Test positive note for balanced philosophy"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "balanced"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["balanced"],
        )

        note = matrix.get_philosophy_specific_note(option, context)
        assert "✓" in note
        assert "balanced development" in note

    def test_option_recommended_for_quality_first(self, matrix, system_context):
        """Test positive note for quality_first philosophy"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "quality_first"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["quality_first"],
        )

        note = matrix.get_philosophy_specific_note(option, context)
        assert "✓" in note
        assert "quality-first approach" in note


class TestContextMatrixRecommendationScore:
    """Test calculate_recommendation_score method"""

    @pytest.fixture
    def matrix(self) -> ContextMatrix:
        """Create context matrix instance"""
        return ContextMatrix()

    @pytest.fixture
    def system_context(self) -> SystemContext:
        """Sample system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
            is_git_repo=True,
            has_ci=True,
        )

    def test_base_score_no_recommendations(self, matrix, system_context):
        """Test base score when option has no recommendations"""
        context = AnswerContext(system=system_context)
        option = Option(value="test", label="Test", description="Test")

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50

    def test_team_size_match(self, matrix, system_context):
        """Test score increases for team size match"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["solo"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 80  # 50 + 30

    def test_maturity_match(self, matrix, system_context):
        """Test score increases for maturity match"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["production"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 70  # 50 + 20

    def test_philosophy_match(self, matrix, system_context):
        """Test score increases for philosophy match"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "quality_first"},
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["quality_first"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 65  # 50 + 15

    def test_ci_match(self, matrix, system_context):
        """Test score increases for CI match"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["has_ci"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 60  # 50 + 10

    def test_git_match(self, matrix, system_context):
        """Test score increases for git match"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["has_git"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 55  # 50 + 5

    def test_all_matches(self, matrix, system_context):
        """Test score with all matches"""
        context = AnswerContext(
            system=system_context,
            answers={
                "team_dynamics": "solo",
                "project_maturity": "production",
                "development_philosophy": "quality_first",
            },
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["solo", "production", "quality_first", "has_ci", "has_git"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        # 50 + 30 + 20 + 15 + 10 + 5 = 130, clamped to 100
        assert score == 100

    def test_score_capped_at_100(self, matrix, system_context):
        """Test score is capped at 100"""
        context = AnswerContext(
            system=system_context,
            answers={
                "team_dynamics": "large_org",
                "project_maturity": "production",
                "development_philosophy": "quality_first",
            },
        )
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["large_org", "production", "quality_first", "has_ci", "has_git"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 100

    def test_no_team_dynamics_answer(self, matrix, system_context):
        """Test score when team dynamics not answered"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["solo"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50  # No team size bonus

    def test_no_maturity_answer(self, matrix, system_context):
        """Test score when maturity not answered"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["production"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50  # No maturity bonus

    def test_no_philosophy_answer(self, matrix, system_context):
        """Test score when philosophy not answered"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["quality_first"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50  # No philosophy bonus

    def test_ci_no_match(self, matrix):
        """Test CI bonus not applied when CI not available"""
        system_context = SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
            has_ci=False,  # No CI
        )
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["has_ci"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50  # No CI bonus

    def test_git_no_match(self, matrix):
        """Test git bonus not applied when git not available"""
        system_context = SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11",
            python_executable="python3",
            pip_version="23.0",
            git_installed=True,
            is_git_repo=False,  # Not a git repo
        )
        context = AnswerContext(system=system_context)
        option = Option(
            value="test",
            label="Test",
            description="Test",
            recommended_for=["has_git"],
        )

        score = matrix.calculate_recommendation_score(option, context)
        assert score == 50  # No git bonus
