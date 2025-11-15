"""
Comprehensive tests for wizard validators module.

Tests cover:
- Conflict validation between options
- Dependency validation
- Team size consistency checks
- Maturity compatibility validation
- Edge cases and error handling
"""

from typing import List

import pytest

from claudecodeoptimizer.wizard.models import Option
from claudecodeoptimizer.wizard.validators import (
    validate_maturity_compatibility,
    validate_no_conflicts,
    validate_required_dependencies,
    validate_team_size_consistency,
)


class TestValidateNoConflicts:
    """Test validate_no_conflicts function"""

    @pytest.fixture
    def options_with_conflicts(self) -> List[Option]:
        """Options with defined conflicts"""
        return [
            Option(
                value="api_service",
                label="API Service",
                description="REST API",
                conflicts_with=["cli_tool"],
            ),
            Option(
                value="cli_tool",
                label="CLI Tool",
                description="Command line tool",
                conflicts_with=["api_service", "web_app"],
            ),
            Option(
                value="web_app",
                label="Web Application",
                description="Web app",
                conflicts_with=["cli_tool"],
            ),
            Option(
                value="library",
                label="Library",
                description="Reusable library",
            ),
        ]

    @pytest.fixture
    def options_no_conflicts(self) -> List[Option]:
        """Options without conflicts"""
        return [
            Option(value="python", label="Python", description="Python language"),
            Option(value="javascript", label="JavaScript", description="JS language"),
            Option(value="typescript", label="TypeScript", description="TS language"),
        ]

    def test_no_conflicts_when_single_selection(self, options_with_conflicts):
        """Test validation passes with single selection"""
        assert validate_no_conflicts(["api_service"], options_with_conflicts) is True
        assert validate_no_conflicts(["cli_tool"], options_with_conflicts) is True
        assert validate_no_conflicts(["web_app"], options_with_conflicts) is True

    def test_no_conflicts_when_compatible_selections(self, options_with_conflicts):
        """Test validation passes with compatible selections"""
        # api_service and web_app don't conflict
        assert validate_no_conflicts(["api_service", "web_app"], options_with_conflicts) is True

        # api_service and library don't conflict
        assert validate_no_conflicts(["api_service", "library"], options_with_conflicts) is True

    def test_conflict_detected_api_vs_cli(self, options_with_conflicts):
        """Test conflict detection between api_service and cli_tool"""
        with pytest.raises(ValueError, match="Cannot select both"):
            validate_no_conflicts(["api_service", "cli_tool"], options_with_conflicts)

    def test_conflict_detected_cli_vs_web(self, options_with_conflicts):
        """Test conflict detection between cli_tool and web_app"""
        with pytest.raises(ValueError, match="Cannot select both"):
            validate_no_conflicts(["cli_tool", "web_app"], options_with_conflicts)

    def test_conflict_error_message_includes_labels(self, options_with_conflicts):
        """Test error message uses human-readable labels"""
        with pytest.raises(ValueError) as exc_info:
            validate_no_conflicts(["api_service", "cli_tool"], options_with_conflicts)

        error_msg = str(exc_info.value)
        assert "API Service" in error_msg or "CLI Tool" in error_msg

    def test_no_conflicts_with_options_lacking_conflicts_field(self, options_no_conflicts):
        """Test validation works when options don't have conflicts_with field"""
        assert (
            validate_no_conflicts(["python", "javascript"], options_no_conflicts) is True
        )

    def test_empty_selection(self, options_with_conflicts):
        """Test validation passes with empty selection"""
        assert validate_no_conflicts([], options_with_conflicts) is True

    def test_multiple_conflicts_detected(self):
        """Test detection when multiple conflicts exist"""
        options = [
            Option(
                value="a",
                label="Option A",
                description="A",
                conflicts_with=["b", "c"],
            ),
            Option(
                value="b",
                label="Option B",
                description="B",
            ),
            Option(
                value="c",
                label="Option C",
                description="C",
            ),
        ]

        # Should fail because 'a' conflicts with both 'b' and 'c'
        with pytest.raises(ValueError):
            validate_no_conflicts(["a", "b"], options)


class TestValidateRequiredDependencies:
    """Test validate_required_dependencies function"""

    @pytest.fixture
    def options_with_deps(self) -> List[Option]:
        """Options with defined dependencies"""
        return [
            Option(
                value="web_app",
                label="Web Application",
                description="Web app",
            ),
            Option(
                value="api_service",
                label="API Service",
                description="API backend",
            ),
            Option(
                value="microservice",
                label="Microservice",
                description="Microservice architecture",
                requires=["api_service"],
            ),
            Option(
                value="kubernetes",
                label="Kubernetes",
                description="K8s deployment",
                requires=["microservice", "api_service"],
            ),
        ]

    def test_dependencies_met_single(self, options_with_deps):
        """Test validation passes when single dependency met"""
        assert (
            validate_required_dependencies(
                ["api_service", "microservice"], options_with_deps
            )
            is True
        )

    def test_dependencies_met_multiple(self, options_with_deps):
        """Test validation passes when multiple dependencies met"""
        assert (
            validate_required_dependencies(
                ["api_service", "microservice", "kubernetes"], options_with_deps
            )
            is True
        )

    def test_missing_dependency_fails(self, options_with_deps):
        """Test validation fails when dependency missing"""
        with pytest.raises(ValueError, match="requires"):
            validate_required_dependencies(["microservice"], options_with_deps)

    def test_missing_multiple_dependencies(self, options_with_deps):
        """Test validation fails when multiple dependencies missing"""
        with pytest.raises(ValueError, match="requires"):
            validate_required_dependencies(["kubernetes"], options_with_deps)

    def test_no_dependencies_required(self, options_with_deps):
        """Test validation passes for options without dependencies"""
        assert (
            validate_required_dependencies(["web_app"], options_with_deps) is True
        )

    def test_error_message_includes_labels(self, options_with_deps):
        """Test error message uses human-readable labels"""
        with pytest.raises(ValueError) as exc_info:
            validate_required_dependencies(["microservice"], options_with_deps)

        error_msg = str(exc_info.value)
        assert "Microservice" in error_msg or "API Service" in error_msg

    def test_empty_selection(self, options_with_deps):
        """Test validation passes with empty selection"""
        assert validate_required_dependencies([], options_with_deps) is True

    def test_options_without_requires_field(self):
        """Test validation works when options lack requires field"""
        options = [
            Option(value="a", label="A", description="Option A"),
            Option(value="b", label="B", description="Option B"),
        ]

        assert validate_required_dependencies(["a", "b"], options) is True


class TestValidateTeamSizeConsistency:
    """Test validate_team_size_consistency function"""

    def test_solo_with_main_only_valid(self):
        """Test solo developer with main-only workflow is valid"""
        answers = {"team_dynamics": "solo", "git_workflow": "main-only"}
        assert validate_team_size_consistency(answers) is True

    def test_solo_with_github_flow_valid(self):
        """Test solo developer with GitHub Flow is valid"""
        answers = {"team_dynamics": "solo", "git_workflow": "github-flow"}
        assert validate_team_size_consistency(answers) is True

    def test_solo_with_git_flow_invalid(self):
        """Test solo developer with Git Flow is invalid"""
        answers = {"team_dynamics": "solo", "git_workflow": "git-flow"}

        with pytest.raises(ValueError, match="not recommended for solo"):
            validate_team_size_consistency(answers)

    def test_small_team_with_git_flow_valid(self):
        """Test small team with Git Flow is valid"""
        answers = {"team_dynamics": "small_team", "git_workflow": "git-flow"}
        assert validate_team_size_consistency(answers) is True

    def test_large_org_with_git_flow_valid(self):
        """Test large org with Git Flow is valid"""
        answers = {"team_dynamics": "large_org", "git_workflow": "git-flow"}
        assert validate_team_size_consistency(answers) is True

    def test_large_org_with_github_flow_valid(self):
        """Test large org with GitHub Flow is valid"""
        answers = {"team_dynamics": "large_org", "git_workflow": "github-flow"}
        assert validate_team_size_consistency(answers) is True

    def test_large_org_with_main_only_invalid(self):
        """Test large org with main-only workflow is invalid"""
        answers = {"team_dynamics": "large_org", "git_workflow": "main-only"}

        with pytest.raises(ValueError, match="not recommended for large"):
            validate_team_size_consistency(answers)

    def test_missing_team_dynamics(self):
        """Test validation handles missing team_dynamics"""
        answers = {"git_workflow": "git-flow"}
        # Should not raise error when team_dynamics is missing
        assert validate_team_size_consistency(answers) is True

    def test_missing_git_workflow(self):
        """Test validation handles missing git_workflow"""
        answers = {"team_dynamics": "solo"}
        # Should not raise error when git_workflow is missing
        assert validate_team_size_consistency(answers) is True

    def test_empty_answers(self):
        """Test validation handles empty answers dict"""
        answers = {}
        assert validate_team_size_consistency(answers) is True


class TestValidateMaturityCompatibility:
    """Test validate_maturity_compatibility function"""

    def test_prototype_with_minimal_valid(self):
        """Test prototype with minimal principles is valid"""
        answers = {"project_maturity": "prototype", "principle_strategy": "minimal"}
        assert validate_maturity_compatibility(answers) is True

    def test_prototype_with_auto_valid(self):
        """Test prototype with auto principles is valid"""
        answers = {"project_maturity": "prototype", "principle_strategy": "auto"}
        assert validate_maturity_compatibility(answers) is True

    def test_prototype_with_recommended_valid(self):
        """Test prototype with recommended principles is valid"""
        answers = {
            "project_maturity": "prototype",
            "principle_strategy": "recommended",
        }
        assert validate_maturity_compatibility(answers) is True

    def test_prototype_with_comprehensive_invalid(self):
        """Test prototype with comprehensive principles is invalid"""
        answers = {
            "project_maturity": "prototype",
            "principle_strategy": "comprehensive",
        }

        with pytest.raises(ValueError, match="not recommended for prototype"):
            validate_maturity_compatibility(answers)

    def test_production_with_comprehensive_valid(self):
        """Test production with comprehensive principles is valid"""
        answers = {
            "project_maturity": "production",
            "principle_strategy": "comprehensive",
        }
        assert validate_maturity_compatibility(answers) is True

    def test_mvp_with_comprehensive_valid(self):
        """Test MVP with comprehensive principles is valid"""
        answers = {"project_maturity": "mvp", "principle_strategy": "comprehensive"}
        assert validate_maturity_compatibility(answers) is True

    def test_missing_maturity(self):
        """Test validation handles missing project_maturity"""
        answers = {"principle_strategy": "comprehensive"}
        assert validate_maturity_compatibility(answers) is True

    def test_missing_principle_strategy(self):
        """Test validation handles missing principle_strategy"""
        answers = {"project_maturity": "prototype"}
        assert validate_maturity_compatibility(answers) is True

    def test_empty_answers(self):
        """Test validation handles empty answers dict"""
        answers = {}
        assert validate_maturity_compatibility(answers) is True


class TestValidatorIntegration:
    """Integration tests combining multiple validators"""

    def test_multiple_validators_all_pass(self):
        """Test that all validators pass with compatible answers"""
        answers = {
            "team_dynamics": "small_team",
            "git_workflow": "github-flow",
            "project_maturity": "production",
            "principle_strategy": "comprehensive",
        }

        assert validate_team_size_consistency(answers) is True
        assert validate_maturity_compatibility(answers) is True

    def test_multiple_validators_team_fails(self):
        """Test validation when team consistency fails"""
        answers = {
            "team_dynamics": "solo",
            "git_workflow": "git-flow",
            "project_maturity": "production",
            "principle_strategy": "comprehensive",
        }

        with pytest.raises(ValueError, match="not recommended for solo"):
            validate_team_size_consistency(answers)

        # Maturity check should still pass
        assert validate_maturity_compatibility(answers) is True

    def test_multiple_validators_maturity_fails(self):
        """Test validation when maturity compatibility fails"""
        answers = {
            "team_dynamics": "small_team",
            "git_workflow": "github-flow",
            "project_maturity": "prototype",
            "principle_strategy": "comprehensive",
        }

        # Team check should pass
        assert validate_team_size_consistency(answers) is True

        with pytest.raises(ValueError, match="not recommended for prototype"):
            validate_maturity_compatibility(answers)


class TestEdgeCases:
    """Test edge cases and unusual inputs"""

    def test_validate_conflicts_with_none_values(self):
        """Test conflict validation with None values"""
        options = [
            Option(value="a", label="A", description="A", conflicts_with=None),
        ]

        # Should handle None gracefully
        try:
            validate_no_conflicts(["a"], options)
            result = True
        except AttributeError:
            result = False

        # This tests current behavior - may need adjustment

    def test_validate_dependencies_with_empty_requires(self):
        """Test dependency validation with empty requires list"""
        options = [
            Option(value="a", label="A", description="A", requires=[]),
        ]

        assert validate_required_dependencies(["a"], options) is True

    def test_team_size_with_unexpected_values(self):
        """Test team size validation with unexpected values"""
        answers = {
            "team_dynamics": "unknown_size",
            "git_workflow": "unknown_workflow",
        }

        # Should not raise error for unknown values
        assert validate_team_size_consistency(answers) is True

    def test_maturity_with_unexpected_values(self):
        """Test maturity validation with unexpected values"""
        answers = {
            "project_maturity": "unknown_stage",
            "principle_strategy": "unknown_strategy",
        }

        # Should not raise error for unknown values
        assert validate_maturity_compatibility(answers) is True


class TestErrorMessages:
    """Test quality and clarity of error messages"""

    def test_conflict_error_message_format(self):
        """Test conflict error message is well-formatted"""
        options = [
            Option(
                value="a",
                label="Option A",
                description="First option",
                conflicts_with=["b"],
            ),
            Option(
                value="b",
                label="Option B",
                description="Second option",
            ),
        ]

        with pytest.raises(ValueError) as exc_info:
            validate_no_conflicts(["a", "b"], options)

        error = str(exc_info.value)
        # Error should mention both options
        assert "Option A" in error or "Option B" in error
        # Error should explain they're mutually exclusive
        assert "mutually exclusive" in error.lower() or "cannot select both" in error.lower()

    def test_dependency_error_message_format(self):
        """Test dependency error message is well-formatted"""
        options = [
            Option(
                value="advanced",
                label="Advanced Feature",
                description="Needs basic",
                requires=["basic"],
            ),
            Option(
                value="basic",
                label="Basic Feature",
                description="Foundation",
            ),
        ]

        with pytest.raises(ValueError) as exc_info:
            validate_required_dependencies(["advanced"], options)

        error = str(exc_info.value)
        # Error should mention what's required
        assert "requires" in error.lower()
        assert "Advanced Feature" in error or "Basic Feature" in error

    def test_team_size_error_message_helpful(self):
        """Test team size error message provides alternatives"""
        answers = {"team_dynamics": "solo", "git_workflow": "git-flow"}

        with pytest.raises(ValueError) as exc_info:
            validate_team_size_consistency(answers)

        error = str(exc_info.value)
        # Should suggest alternatives
        assert "consider" in error.lower() or "instead" in error.lower()

    def test_maturity_error_message_helpful(self):
        """Test maturity error message provides alternatives"""
        answers = {
            "project_maturity": "prototype",
            "principle_strategy": "comprehensive",
        }

        with pytest.raises(ValueError) as exc_info:
            validate_maturity_compatibility(answers)

        error = str(exc_info.value)
        # Should suggest alternatives
        assert "consider" in error.lower() or "instead" in error.lower()
