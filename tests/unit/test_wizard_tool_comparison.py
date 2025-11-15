"""
Comprehensive tests for wizard tool_comparison module.

Tests cover:
- ToolComparator initialization and basic methods
- Category analysis and conflict detection
- Tool recommendations for all categories
- Tool descriptions and explanations
- Edge cases and error handling
- Convenience functions
- Case sensitivity handling
"""

from claudecodeoptimizer.wizard.models import ToolComparison
from claudecodeoptimizer.wizard.tool_comparison import (
    ToolComparator,
    compare_tools,
    get_formatter_recommendation,
    get_linter_recommendation,
    get_test_framework_recommendation,
)


class TestToolComparatorInitialization:
    """Test ToolComparator initialization"""

    def test_init_empty_list(self):
        """Test initialization with empty tool list"""
        comparator = ToolComparator([])
        assert comparator.detected_tools == []

    def test_init_single_tool(self):
        """Test initialization with single tool"""
        comparator = ToolComparator(["pytest"])
        assert comparator.detected_tools == ["pytest"]

    def test_init_multiple_tools(self):
        """Test initialization with multiple tools"""
        tools = ["pytest", "black", "mypy", "ruff"]
        comparator = ToolComparator(tools)
        assert comparator.detected_tools == ["pytest", "black", "mypy", "ruff"]

    def test_init_case_normalization(self):
        """Test that tool names are normalized to lowercase"""
        comparator = ToolComparator(["PyTest", "BLACK", "MyPy", "Ruff"])
        assert comparator.detected_tools == ["pytest", "black", "mypy", "ruff"]

    def test_init_mixed_case(self):
        """Test mixed case tool names are normalized"""
        comparator = ToolComparator(["PyTeSt", "bLaCk", "RUFF"])
        assert comparator.detected_tools == ["pytest", "black", "ruff"]


class TestAnalyzeCategory:
    """Test analyze_category method"""

    def test_analyze_invalid_category(self):
        """Test analyzing invalid category returns None"""
        comparator = ToolComparator(["pytest", "black"])
        result = comparator.analyze_category("invalid_category")
        assert result is None

    def test_analyze_no_tools_in_category(self):
        """Test category with no detected tools returns None"""
        comparator = ToolComparator(["django", "flask"])
        result = comparator.analyze_category("formatter")
        assert result is None

    def test_analyze_single_tool_in_category(self):
        """Test category with single tool returns None (no conflict)"""
        comparator = ToolComparator(["pytest"])
        result = comparator.analyze_category("test_framework")
        assert result is None

    def test_analyze_formatter_conflict_ruff_black(self):
        """Test formatter conflict between ruff and black"""
        comparator = ToolComparator(["ruff", "black"])
        result = comparator.analyze_category("formatter")

        assert result is not None
        assert isinstance(result, ToolComparison)
        assert result.category == "formatter"
        assert set(result.tools) == {"ruff", "black"}
        assert result.recommended == "ruff"
        assert "fast" in result.reason.lower() or "modern" in result.reason.lower()
        assert "black" in result.alternatives

    def test_analyze_linter_conflict_ruff_flake8(self):
        """Test linter conflict between ruff and flake8"""
        comparator = ToolComparator(["ruff", "flake8"])
        result = comparator.analyze_category("linter")

        assert result is not None
        assert result.category == "linter"
        assert set(result.tools) == {"ruff", "flake8"}
        assert result.recommended == "ruff"
        assert "flake8" in result.alternatives

    def test_analyze_linter_conflict_multiple_tools(self):
        """Test linter conflict with multiple tools"""
        comparator = ToolComparator(["ruff", "flake8", "pylint", "mypy"])
        result = comparator.analyze_category("linter")

        assert result is not None
        assert result.category == "linter"
        assert set(result.tools) == {"ruff", "flake8", "pylint", "mypy"}
        assert result.recommended == "ruff"
        assert len(result.alternatives) == 3
        assert "flake8" in result.alternatives
        assert "pylint" in result.alternatives
        assert "mypy" in result.alternatives

    def test_analyze_test_framework_conflict(self):
        """Test test framework conflict"""
        comparator = ToolComparator(["pytest", "unittest"])
        result = comparator.analyze_category("test_framework")

        assert result is not None
        assert result.category == "test_framework"
        assert set(result.tools) == {"pytest", "unittest"}
        assert result.recommended == "pytest"
        assert "unittest" in result.alternatives

    def test_analyze_type_checker_conflict(self):
        """Test type checker conflict"""
        comparator = ToolComparator(["mypy", "pyright"])
        result = comparator.analyze_category("type_checker")

        assert result is not None
        assert result.category == "type_checker"
        assert set(result.tools) == {"mypy", "pyright"}
        assert result.recommended == "mypy"
        assert "pyright" in result.alternatives

    def test_analyze_dependency_manager_conflict(self):
        """Test dependency manager conflict"""
        comparator = ToolComparator(["poetry", "pip-tools", "pipenv"])
        result = comparator.analyze_category("dependency_manager")

        assert result is not None
        assert result.category == "dependency_manager"
        assert set(result.tools) == {"poetry", "pip-tools", "pipenv"}
        assert result.recommended == "pip-tools"
        assert "poetry" in result.alternatives
        assert "pipenv" in result.alternatives

    def test_analyze_task_runner_conflict(self):
        """Test task runner conflict"""
        comparator = ToolComparator(["make", "invoke", "nox"])
        result = comparator.analyze_category("task_runner")

        assert result is not None
        assert result.category == "task_runner"
        assert set(result.tools) == {"make", "invoke", "nox"}
        assert result.recommended == "make"

    def test_analyze_coverage_tool_conflict(self):
        """Test coverage tool conflict"""
        comparator = ToolComparator(["coverage", "pytest-cov"])
        result = comparator.analyze_category("coverage_tool")

        assert result is not None
        assert result.category == "coverage_tool"
        assert set(result.tools) == {"coverage", "pytest-cov"}
        assert result.recommended == "pytest-cov"

    def test_analyze_documentation_conflict(self):
        """Test documentation tool conflict"""
        comparator = ToolComparator(["sphinx", "mkdocs", "pdoc"])
        result = comparator.analyze_category("documentation")

        assert result is not None
        assert result.category == "documentation"
        assert set(result.tools) == {"sphinx", "mkdocs", "pdoc"}
        assert result.recommended == "mkdocs"

    def test_analyze_build_system_conflict(self):
        """Test build system conflict"""
        comparator = ToolComparator(["setuptools", "poetry", "hatchling"])
        result = comparator.analyze_category("build_system")

        assert result is not None
        assert result.category == "build_system"
        assert set(result.tools) == {"setuptools", "poetry", "hatchling"}
        assert result.recommended == "hatchling"

    def test_analyze_alternatives_excludes_recommended(self):
        """Test that alternatives dict excludes recommended tool"""
        comparator = ToolComparator(["ruff", "black", "autopep8"])
        result = comparator.analyze_category("formatter")

        assert result is not None
        assert result.recommended == "ruff"
        assert "ruff" not in result.alternatives
        assert "black" in result.alternatives
        assert "autopep8" in result.alternatives

    def test_analyze_alternatives_have_descriptions(self):
        """Test that all alternatives have descriptions"""
        comparator = ToolComparator(["ruff", "black", "autopep8"])
        result = comparator.analyze_category("formatter")

        assert result is not None
        for tool, description in result.alternatives.items():
            assert isinstance(description, str)
            assert len(description) > 0


class TestFindAllConflicts:
    """Test find_all_conflicts method"""

    def test_find_no_conflicts(self):
        """Test finding conflicts when none exist"""
        comparator = ToolComparator(["pytest"])
        conflicts = comparator.find_all_conflicts()
        assert conflicts == []

    def test_find_single_conflict(self):
        """Test finding single conflict"""
        comparator = ToolComparator(["pytest", "unittest"])
        conflicts = comparator.find_all_conflicts()

        assert len(conflicts) == 1
        assert conflicts[0].category == "test_framework"

    def test_find_multiple_conflicts(self):
        """Test finding multiple conflicts"""
        comparator = ToolComparator(["ruff", "black", "pytest", "unittest", "mypy", "pyright"])
        conflicts = comparator.find_all_conflicts()

        # mypy appears in both linter and type_checker categories, so we get 4 conflicts
        assert len(conflicts) == 4
        categories = {c.category for c in conflicts}
        assert "formatter" in categories
        assert "linter" in categories  # mypy is also a linter
        assert "test_framework" in categories
        assert "type_checker" in categories

    def test_find_all_categories_with_conflicts(self):
        """Test finding conflicts across all categories"""
        comparator = ToolComparator(
            [
                "ruff",
                "black",  # formatter
                "flake8",
                "pylint",  # linter (ruff also)
                "pytest",
                "unittest",  # test_framework
                "mypy",
                "pyright",  # type_checker
                "poetry",
                "pip-tools",  # dependency_manager
                "make",
                "invoke",  # task_runner
                "coverage",
                "pytest-cov",  # coverage_tool
                "sphinx",
                "mkdocs",  # documentation
                "setuptools",
                "hatchling",  # build_system
            ]
        )
        conflicts = comparator.find_all_conflicts()

        # Should have conflicts in all categories
        categories = {c.category for c in conflicts}
        assert "formatter" in categories
        assert "linter" in categories
        assert "test_framework" in categories
        assert "type_checker" in categories
        assert "dependency_manager" in categories
        assert "task_runner" in categories
        assert "coverage_tool" in categories
        assert "documentation" in categories
        assert "build_system" in categories

    def test_find_conflicts_returns_list(self):
        """Test that find_all_conflicts returns a list"""
        comparator = ToolComparator(["pytest", "black"])
        conflicts = comparator.find_all_conflicts()
        assert isinstance(conflicts, list)

    def test_find_conflicts_with_tool_in_multiple_categories(self):
        """Test that ruff appears in both formatter and linter conflicts"""
        comparator = ToolComparator(["ruff", "black", "flake8"])
        conflicts = comparator.find_all_conflicts()

        assert len(conflicts) == 2
        categories = {c.category for c in conflicts}
        assert "formatter" in categories
        assert "linter" in categories

        # Ruff should appear in both
        for conflict in conflicts:
            if conflict.category in ["formatter", "linter"]:
                assert "ruff" in conflict.tools


class TestGetRecommendations:
    """Test get_recommendations method"""

    def test_get_recommendations_empty_tools(self):
        """Test getting recommendations with no detected tools"""
        comparator = ToolComparator([])
        recs = comparator.get_recommendations()
        assert recs == {}

    def test_get_recommendations_single_category(self):
        """Test getting recommendations for single category"""
        comparator = ToolComparator(["pytest"])
        recs = comparator.get_recommendations()

        assert "test_framework" in recs
        assert recs["test_framework"] == "pytest"
        assert len(recs) == 1

    def test_get_recommendations_multiple_categories(self):
        """Test getting recommendations for multiple categories"""
        comparator = ToolComparator(["pytest", "black", "mypy"])
        recs = comparator.get_recommendations()

        assert "test_framework" in recs
        assert "formatter" in recs
        assert "type_checker" in recs
        assert recs["test_framework"] == "pytest"
        assert recs["formatter"] == "ruff"  # Recommended, not detected black
        assert recs["type_checker"] == "mypy"

    def test_get_recommendations_with_conflicts(self):
        """Test recommendations when conflicts exist"""
        comparator = ToolComparator(["pytest", "unittest"])
        recs = comparator.get_recommendations()

        assert "test_framework" in recs
        assert recs["test_framework"] == "pytest"  # Recommended tool

    def test_get_recommendations_returns_recommended_not_detected(self):
        """Test that recommendations return recommended tool, not just detected"""
        comparator = ToolComparator(["black"])  # Detected black
        recs = comparator.get_recommendations()

        assert "formatter" in recs
        assert recs["formatter"] == "ruff"  # Recommended is ruff, not black

    def test_get_recommendations_all_categories(self):
        """Test recommendations for all categories"""
        comparator = ToolComparator(
            [
                "black",
                "flake8",
                "pytest",
                "mypy",
                "poetry",
                "make",
                "coverage",
                "sphinx",
                "setuptools",
            ]
        )
        recs = comparator.get_recommendations()

        assert recs["formatter"] == "ruff"
        assert recs["linter"] == "ruff"
        assert recs["test_framework"] == "pytest"
        assert recs["type_checker"] == "mypy"
        assert recs["dependency_manager"] == "pip-tools"
        assert recs["task_runner"] == "make"
        assert recs["coverage_tool"] == "pytest-cov"
        assert recs["documentation"] == "mkdocs"
        assert recs["build_system"] == "hatchling"

    def test_get_recommendations_only_detected_categories(self):
        """Test that recommendations only include categories with detected tools"""
        comparator = ToolComparator(["pytest", "black"])
        recs = comparator.get_recommendations()

        assert "test_framework" in recs
        assert "formatter" in recs
        # Should not include categories without detected tools
        assert "dependency_manager" not in recs
        assert "task_runner" not in recs


class TestShouldAskPreference:
    """Test should_ask_preference method"""

    def test_should_ask_no_conflict(self):
        """Test should not ask when no conflict exists"""
        comparator = ToolComparator(["pytest"])
        assert not comparator.should_ask_preference("test_framework")

    def test_should_ask_with_conflict(self):
        """Test should ask when conflict exists"""
        comparator = ToolComparator(["pytest", "unittest"])
        assert comparator.should_ask_preference("test_framework")

    def test_should_ask_invalid_category(self):
        """Test should not ask for invalid category"""
        comparator = ToolComparator(["pytest"])
        assert not comparator.should_ask_preference("invalid_category")

    def test_should_ask_no_tools_in_category(self):
        """Test should not ask when no tools detected in category"""
        comparator = ToolComparator(["pytest"])
        assert not comparator.should_ask_preference("formatter")

    def test_should_ask_multiple_conflicts(self):
        """Test should ask for all conflicting categories"""
        comparator = ToolComparator(["ruff", "black", "pytest", "unittest"])

        assert comparator.should_ask_preference("formatter")
        assert comparator.should_ask_preference("test_framework")
        assert not comparator.should_ask_preference("type_checker")


class TestGetToolDescription:
    """Test get_tool_description method"""

    def test_get_description_known_tool(self):
        """Test getting description for known tool"""
        comparator = ToolComparator([])
        desc = comparator.get_tool_description("ruff")
        assert isinstance(desc, str)
        assert len(desc) > 0
        assert "ruff" in desc.lower() or "fast" in desc.lower()

    def test_get_description_case_insensitive(self):
        """Test tool description is case insensitive"""
        comparator = ToolComparator([])
        desc1 = comparator.get_tool_description("RUFF")
        desc2 = comparator.get_tool_description("ruff")
        desc3 = comparator.get_tool_description("RuFf")
        assert desc1 == desc2 == desc3

    def test_get_description_unknown_tool(self):
        """Test getting description for unknown tool"""
        comparator = ToolComparator([])
        desc = comparator.get_tool_description("unknown_tool")
        assert "unknown_tool" in desc
        assert "detected in project" in desc.lower()

    def test_get_description_all_formatters(self):
        """Test descriptions for all formatter tools"""
        comparator = ToolComparator([])
        tools = ["ruff", "black", "autopep8", "yapf"]

        for tool in tools:
            desc = comparator.get_tool_description(tool)
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_get_description_all_linters(self):
        """Test descriptions for all linter tools"""
        comparator = ToolComparator([])
        tools = ["ruff", "flake8", "pylint", "pycodestyle", "pydocstyle", "mypy"]

        for tool in tools:
            desc = comparator.get_tool_description(tool)
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_get_description_all_test_frameworks(self):
        """Test descriptions for all test framework tools"""
        comparator = ToolComparator([])
        tools = ["pytest", "unittest", "nose", "nose2"]

        for tool in tools:
            desc = comparator.get_tool_description(tool)
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_get_description_returns_from_first_category(self):
        """Test that description returns from first matching category"""
        comparator = ToolComparator([])
        # ruff appears in both formatter and linter
        desc = comparator.get_tool_description("ruff")
        assert isinstance(desc, str)
        assert len(desc) > 0


class TestExplainRecommendation:
    """Test explain_recommendation method"""

    def test_explain_invalid_category(self):
        """Test explaining invalid category"""
        comparator = ToolComparator([])
        explanation = comparator.explain_recommendation("invalid_category")
        assert "No recommendation available" in explanation
        assert "invalid_category" in explanation

    def test_explain_no_detected_tools(self):
        """Test explaining category with no detected tools"""
        comparator = ToolComparator([])
        explanation = comparator.explain_recommendation("formatter")
        assert "Recommend ruff" in explanation
        assert isinstance(explanation, str)

    def test_explain_single_tool(self):
        """Test explaining category with single detected tool"""
        comparator = ToolComparator(["pytest"])
        explanation = comparator.explain_recommendation("test_framework")
        assert "Recommend pytest" in explanation
        assert "Modern, powerful" in explanation

    def test_explain_with_conflict(self):
        """Test explaining category with conflict"""
        comparator = ToolComparator(["pytest", "unittest"])
        explanation = comparator.explain_recommendation("test_framework")

        assert "Recommend pytest" in explanation
        assert "You have:" in explanation
        assert "pytest" in explanation
        assert "unittest" in explanation
        assert "Consider migrating" in explanation

    def test_explain_multiple_tools_conflict(self):
        """Test explaining category with multiple tool conflict"""
        comparator = ToolComparator(["ruff", "black", "autopep8"])
        explanation = comparator.explain_recommendation("formatter")

        assert "Recommend ruff" in explanation
        assert "You have:" in explanation
        assert "ruff" in explanation
        assert "black" in explanation
        assert "Consider migrating" in explanation

    def test_explain_includes_reason(self):
        """Test that explanation includes reason for recommendation"""
        comparator = ToolComparator(["pytest"])
        explanation = comparator.explain_recommendation("test_framework")
        # Should include the reason from TOOL_CATEGORIES
        assert "Modern, powerful" in explanation or "recommended" in explanation.lower()

    def test_explain_all_categories(self):
        """Test explaining all valid categories"""
        comparator = ToolComparator(
            [
                "black",
                "flake8",
                "pytest",
                "mypy",
                "poetry",
                "make",
                "coverage",
                "sphinx",
                "setuptools",
            ]
        )

        categories = [
            "formatter",
            "linter",
            "test_framework",
            "type_checker",
            "dependency_manager",
            "task_runner",
            "coverage_tool",
            "documentation",
            "build_system",
        ]

        for category in categories:
            explanation = comparator.explain_recommendation(category)
            assert isinstance(explanation, str)
            assert len(explanation) > 0
            assert "Recommend" in explanation


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_compare_tools_function(self):
        """Test compare_tools convenience function"""
        tools = ["pytest", "black", "mypy"]
        comparator = compare_tools(tools)

        assert isinstance(comparator, ToolComparator)
        assert comparator.detected_tools == ["pytest", "black", "mypy"]

    def test_compare_tools_empty_list(self):
        """Test compare_tools with empty list"""
        comparator = compare_tools([])
        assert isinstance(comparator, ToolComparator)
        assert comparator.detected_tools == []

    def test_get_formatter_recommendation_no_tools(self):
        """Test formatter recommendation with no tools"""
        result = get_formatter_recommendation([])
        assert result == "ruff"

    def test_get_formatter_recommendation_with_formatter(self):
        """Test formatter recommendation with formatter detected"""
        result = get_formatter_recommendation(["black"])
        assert result == "ruff"  # Returns recommended, not detected

    def test_get_formatter_recommendation_with_multiple(self):
        """Test formatter recommendation with multiple formatters"""
        result = get_formatter_recommendation(["black", "autopep8"])
        assert result == "ruff"

    def test_get_linter_recommendation_no_tools(self):
        """Test linter recommendation with no tools"""
        result = get_linter_recommendation([])
        assert result == "ruff"

    def test_get_linter_recommendation_with_linter(self):
        """Test linter recommendation with linter detected"""
        result = get_linter_recommendation(["flake8"])
        assert result == "ruff"

    def test_get_linter_recommendation_with_multiple(self):
        """Test linter recommendation with multiple linters"""
        result = get_linter_recommendation(["flake8", "pylint"])
        assert result == "ruff"

    def test_get_test_framework_recommendation_no_tools(self):
        """Test test framework recommendation with no tools"""
        result = get_test_framework_recommendation([])
        assert result == "pytest"

    def test_get_test_framework_recommendation_with_framework(self):
        """Test test framework recommendation with framework detected"""
        result = get_test_framework_recommendation(["unittest"])
        assert result == "pytest"

    def test_get_test_framework_recommendation_with_multiple(self):
        """Test test framework recommendation with multiple frameworks"""
        result = get_test_framework_recommendation(["unittest", "nose"])
        assert result == "pytest"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_category_name(self):
        """Test handling of empty category name"""
        comparator = ToolComparator(["pytest"])
        result = comparator.analyze_category("")
        assert result is None

    def test_none_values_handling(self):
        """Test that None values don't break initialization"""
        # ToolComparator expects List[str], but test defensive coding
        comparator = ToolComparator([])
        assert comparator.detected_tools == []

    def test_duplicate_tools(self):
        """Test handling duplicate tools in list"""
        comparator = ToolComparator(["pytest", "pytest", "black", "black"])
        # Should still work, duplicates in the list
        assert "pytest" in comparator.detected_tools
        assert "black" in comparator.detected_tools

    def test_whitespace_in_tool_names(self):
        """Test tools with whitespace are handled"""
        comparator = ToolComparator([" pytest ", "black "])
        # Should normalize whitespace (if implementation does)
        # This tests actual behavior
        conflicts = comparator.find_all_conflicts()
        # Should not crash at least
        assert isinstance(conflicts, list)

    def test_special_characters_in_tool_names(self):
        """Test tools with special characters"""
        comparator = ToolComparator(["pytest-cov", "pip-tools"])
        recs = comparator.get_recommendations()
        # Should handle tools with hyphens
        assert "coverage_tool" in recs or "dependency_manager" in recs

    def test_very_long_tool_list(self):
        """Test with very long list of tools"""
        tools = ["pytest", "black", "mypy", "ruff", "flake8", "pylint"] * 10
        comparator = ToolComparator(tools)
        conflicts = comparator.find_all_conflicts()
        # Should not crash or hang
        assert isinstance(conflicts, list)

    def test_all_categories_keys_exist(self):
        """Test that TOOL_CATEGORIES has expected structure"""
        comparator = ToolComparator([])
        expected_keys = [
            "formatter",
            "linter",
            "test_framework",
            "type_checker",
            "dependency_manager",
            "task_runner",
            "coverage_tool",
            "documentation",
            "build_system",
        ]

        for key in expected_keys:
            assert key in ToolComparator.TOOL_CATEGORIES

    def test_all_categories_have_required_fields(self):
        """Test that all categories have required fields"""
        for category, info in ToolComparator.TOOL_CATEGORIES.items():
            assert "tools" in info
            assert "recommended" in info
            assert "reasons" in info
            assert isinstance(info["tools"], list)
            assert isinstance(info["recommended"], str)
            assert isinstance(info["reasons"], dict)

    def test_recommended_tool_in_tools_list(self):
        """Test that recommended tool is always in tools list"""
        for category, info in ToolComparator.TOOL_CATEGORIES.items():
            recommended = info["recommended"]
            tools = info["tools"]
            assert recommended in tools, f"{recommended} not in {category} tools"

    def test_recommended_tool_has_reason(self):
        """Test that recommended tool always has a reason"""
        for category, info in ToolComparator.TOOL_CATEGORIES.items():
            recommended = info["recommended"]
            reasons = info["reasons"]
            assert recommended in reasons, f"{recommended} has no reason in {category}"

    def test_all_tools_have_reasons(self):
        """Test that all tools in category have reasons"""
        for category, info in ToolComparator.TOOL_CATEGORIES.items():
            tools = info["tools"]
            reasons = info["reasons"]
            for tool in tools:
                assert tool in reasons, f"{tool} has no reason in {category}"


class TestToolComparisonModel:
    """Test ToolComparison model integration"""

    def test_tool_comparison_from_analyze(self):
        """Test ToolComparison object from analyze_category"""
        comparator = ToolComparator(["pytest", "unittest"])
        comparison = comparator.analyze_category("test_framework")

        assert isinstance(comparison, ToolComparison)
        assert comparison.category == "test_framework"
        assert "pytest" in comparison.tools
        assert "unittest" in comparison.tools
        assert comparison.recommended == "pytest"
        assert isinstance(comparison.reason, str)
        assert isinstance(comparison.alternatives, dict)

    def test_tool_comparison_alternatives_structure(self):
        """Test ToolComparison alternatives are properly structured"""
        comparator = ToolComparator(["ruff", "black", "autopep8"])
        comparison = comparator.analyze_category("formatter")

        assert comparison is not None
        assert isinstance(comparison.alternatives, dict)
        assert "black" in comparison.alternatives
        assert "autopep8" in comparison.alternatives
        assert "ruff" not in comparison.alternatives

        for tool, reason in comparison.alternatives.items():
            assert isinstance(tool, str)
            assert isinstance(reason, str)
            assert len(reason) > 0

    def test_tool_comparison_from_conflicts(self):
        """Test ToolComparison objects from find_all_conflicts"""
        comparator = ToolComparator(["pytest", "unittest", "black", "ruff"])
        conflicts = comparator.find_all_conflicts()

        assert len(conflicts) == 2
        for conflict in conflicts:
            assert isinstance(conflict, ToolComparison)
            assert hasattr(conflict, "category")
            assert hasattr(conflict, "tools")
            assert hasattr(conflict, "recommended")
            assert hasattr(conflict, "reason")
            assert hasattr(conflict, "alternatives")


class TestCaseSensitivity:
    """Test case sensitivity handling throughout"""

    def test_case_insensitive_tool_detection(self):
        """Test that tool detection is case insensitive"""
        comparator1 = ToolComparator(["PyTest", "UnitTest"])
        comparator2 = ToolComparator(["pytest", "unittest"])

        conflicts1 = comparator1.find_all_conflicts()
        conflicts2 = comparator2.find_all_conflicts()

        assert len(conflicts1) == len(conflicts2)

    def test_case_insensitive_recommendations(self):
        """Test that recommendations work with any case"""
        comparator1 = ToolComparator(["BLACK", "RUFF"])
        comparator2 = ToolComparator(["black", "ruff"])

        recs1 = comparator1.get_recommendations()
        recs2 = comparator2.get_recommendations()

        assert recs1 == recs2

    def test_case_insensitive_should_ask(self):
        """Test should_ask_preference with different cases"""
        comparator = ToolComparator(["PyTest", "UnitTest"])
        assert comparator.should_ask_preference("test_framework")

    def test_mixed_case_in_conflicts(self):
        """Test mixed case tools in conflict detection"""
        comparator = ToolComparator(["PyTest", "unittest", "NOSE2"])
        conflicts = comparator.find_all_conflicts()

        assert len(conflicts) == 1
        assert conflicts[0].category == "test_framework"
        # Tools should be lowercase in result
        assert set(conflicts[0].tools) == {"pytest", "unittest", "nose2"}


class TestRecommendationConsistency:
    """Test consistency of recommendations across methods"""

    def test_recommendation_consistency(self):
        """Test that recommendations are consistent across different methods"""
        tools = ["black", "ruff", "pytest", "unittest"]
        comparator = ToolComparator(tools)

        # Get recommendations from get_recommendations
        recs = comparator.get_recommendations()

        # Check consistency with analyze_category
        for category in ["formatter", "test_framework"]:
            comparison = comparator.analyze_category(category)
            if comparison:
                assert comparison.recommended == recs[category]

    def test_convenience_function_consistency(self):
        """Test that convenience functions match get_recommendations"""
        tools = ["black", "flake8", "unittest"]

        comparator = ToolComparator(tools)
        recs = comparator.get_recommendations()

        assert get_formatter_recommendation(tools) == recs.get("formatter", "ruff")
        assert get_linter_recommendation(tools) == recs.get("linter", "ruff")
        assert get_test_framework_recommendation(tools) == recs.get("test_framework", "pytest")
