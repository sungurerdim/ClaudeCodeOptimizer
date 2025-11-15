"""
Comprehensive tests for wizard models module.

Tests cover:
- Option model validation and properties
- DecisionPoint model validation and logic
- SystemContext model and utility methods
- AnswerContext model and property accessors
- WizardResult model and serialization
- ToolComparison model
"""

from pathlib import Path
from typing import List

import pytest

from claudecodeoptimizer.wizard.models import (
    AnswerContext,
    DecisionPoint,
    Option,
    SystemContext,
    ToolComparison,
    WizardResult,
)


class TestOption:
    """Test Option model"""

    def test_option_creation_minimal(self):
        """Test creating option with minimal required fields"""
        opt = Option(
            value="test_value",
            label="Test Label",
            description="Test description",
        )

        assert opt.value == "test_value"
        assert opt.label == "Test Label"
        assert opt.description == "Test description"
        assert opt.recommended_for == []
        assert opt.effects == ""
        assert opt.time_investment == ""
        assert opt.trade_offs == ""
        assert opt.conflicts_with == []
        assert opt.requires == []

    def test_option_creation_full(self):
        """Test creating option with all fields"""
        opt = Option(
            value="api_service",
            label="API Service",
            description="REST API backend service",
            recommended_for=["web_app", "microservice"],
            effects="Enables API endpoints",
            time_investment="2-4 hours",
            trade_offs="More complexity but better separation",
            conflicts_with=["cli_tool"],
            requires=["database"],
        )

        assert opt.value == "api_service"
        assert opt.label == "API Service"
        assert "API backend" in opt.description
        assert "web_app" in opt.recommended_for
        assert opt.effects == "Enables API endpoints"
        assert opt.time_investment == "2-4 hours"
        assert "complexity" in opt.trade_offs
        assert "cli_tool" in opt.conflicts_with
        assert "database" in opt.requires

    def test_option_validation_missing_value(self):
        """Test option validation fails without value"""
        with pytest.raises(ValueError, match="must have value and label"):
            Option(value="", label="Test", description="Test")

    def test_option_validation_missing_label(self):
        """Test option validation fails without label"""
        with pytest.raises(ValueError, match="must have value and label"):
            Option(value="test", label="", description="Test")

    def test_option_lists_default_to_empty(self):
        """Test that list fields default to empty lists"""
        opt = Option(value="test", label="Test", description="Test")
        assert isinstance(opt.recommended_for, list)
        assert isinstance(opt.conflicts_with, list)
        assert isinstance(opt.requires, list)


class TestDecisionPoint:
    """Test DecisionPoint model"""

    @pytest.fixture
    def sample_options(self) -> List[Option]:
        """Sample options for testing"""
        return [
            Option(value="solo", label="Solo", description="Solo developer"),
            Option(value="team", label="Team", description="Team of developers"),
            Option(value="org", label="Organization", description="Large organization"),
        ]

    def test_decision_point_creation_minimal(self, sample_options):
        """Test creating decision point with minimal fields"""
        dp = DecisionPoint(
            id="team_size",
            tier=1,
            category="project_identity",
            question="How many developers?",
            options=sample_options,
        )

        assert dp.id == "team_size"
        assert dp.tier == 1
        assert dp.category == "project_identity"
        assert dp.question == "How many developers?"
        assert len(dp.options) == 3
        assert dp.multi_select is False
        assert dp.auto_strategy is None
        assert dp.why_this_question == ""
        assert dp.ai_hint_generator is None
        assert dp.skip_if is None
        assert dp.required_for == []
        assert dp.validator is None

    def test_decision_point_should_ask_no_skip_condition(self, sample_options):
        """Test should_ask returns True when no skip condition"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
        )

        assert dp.should_ask({}) is True
        assert dp.should_ask({"any": "context"}) is True

    def test_decision_point_should_ask_with_skip_condition(self, sample_options):
        """Test should_ask respects skip condition"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            skip_if=lambda ctx: ctx.get("skip_me") is True,
        )

        assert dp.should_ask({}) is True
        assert dp.should_ask({"skip_me": False}) is True
        assert dp.should_ask({"skip_me": True}) is False

    def test_decision_point_get_ai_hint_no_generator(self, sample_options):
        """Test get_ai_hint returns empty string without generator"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
        )

        assert dp.get_ai_hint({}) == ""

    def test_decision_point_get_ai_hint_with_generator(self, sample_options):
        """Test get_ai_hint uses generator function"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            ai_hint_generator=lambda ctx: f"Based on {ctx.get('project_type', 'unknown')}",
        )

        assert "Based on" in dp.get_ai_hint({})
        assert "web_app" in dp.get_ai_hint({"project_type": "web_app"})

    def test_decision_point_get_recommended_option_no_strategy(self, sample_options):
        """Test get_recommended_option returns None without strategy"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
        )

        assert dp.get_recommended_option({}) is None

    def test_decision_point_get_recommended_option_single(self, sample_options):
        """Test get_recommended_option returns single value"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            auto_strategy=lambda ctx: "solo",
        )

        result = dp.get_recommended_option({})
        assert result == "solo"

    def test_decision_point_get_recommended_option_multi(self, sample_options):
        """Test get_recommended_option returns list for multi-select"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            multi_select=True,
            auto_strategy=lambda ctx: ["solo", "team"],
        )

        result = dp.get_recommended_option({})
        assert isinstance(result, list)
        assert "solo" in result
        assert "team" in result

    def test_decision_point_validate_answer_single_valid(self, sample_options):
        """Test validate_answer accepts valid single answer"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
        )

        assert dp.validate_answer("solo") is True
        assert dp.validate_answer("team") is True
        assert dp.validate_answer("org") is True

    def test_decision_point_validate_answer_single_invalid(self, sample_options):
        """Test validate_answer rejects invalid single answer"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
        )

        assert dp.validate_answer("invalid") is False
        assert dp.validate_answer("") is False

    def test_decision_point_validate_answer_multi_valid(self, sample_options):
        """Test validate_answer accepts valid multi-select answer"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            multi_select=True,
        )

        assert dp.validate_answer(["solo"]) is True
        assert dp.validate_answer(["solo", "team"]) is True
        assert dp.validate_answer(["solo", "team", "org"]) is True

    def test_decision_point_validate_answer_multi_invalid(self, sample_options):
        """Test validate_answer rejects invalid multi-select answer"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            multi_select=True,
        )

        assert dp.validate_answer("solo") is False  # Not a list
        assert dp.validate_answer(["invalid"]) is False
        assert dp.validate_answer(["solo", "invalid"]) is False

    def test_decision_point_validate_answer_custom_validator(self, sample_options):
        """Test validate_answer uses custom validator"""
        dp = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=sample_options,
            validator=lambda ans: ans == "solo",
        )

        assert dp.validate_answer("solo") is True
        assert dp.validate_answer("team") is False


class TestSystemContext:
    """Test SystemContext model"""

    @pytest.fixture
    def windows_context(self) -> SystemContext:
        """Sample Windows system context"""
        return SystemContext(
            os_type="windows",
            os_version="10.0.19045",
            os_platform="win32",
            shell_type="powershell",
            terminal_emulator="windows-terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11.0",
            python_executable="C:\\Python311\\python.exe",
            pip_version="23.0.1",
            git_installed=True,
            git_user_name="Test User",
            git_user_email="test@example.com",
        )

    @pytest.fixture
    def linux_context(self) -> SystemContext:
        """Sample Linux system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15.0",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="gnome-terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11.0",
            python_executable="/usr/bin/python3",
            pip_version="23.0.1",
            git_installed=True,
        )

    def test_system_context_creation(self, windows_context):
        """Test creating system context"""
        assert windows_context.os_type == "windows"
        assert windows_context.shell_type == "powershell"
        assert windows_context.git_installed is True

    def test_get_shell_syntax_windows(self, windows_context):
        """Test get_shell_syntax returns powershell for Windows"""
        assert windows_context.get_shell_syntax() == "powershell"

    def test_get_shell_syntax_linux(self, linux_context):
        """Test get_shell_syntax returns bash for Linux"""
        assert linux_context.get_shell_syntax() == "bash"

    def test_get_path_separator_windows(self, windows_context):
        """Test get_path_separator returns backslash for Windows"""
        assert windows_context.get_path_separator() == "\\"

    def test_get_path_separator_linux(self, linux_context):
        """Test get_path_separator returns forward slash for Linux"""
        assert linux_context.get_path_separator() == "/"

    def test_supports_unicode_true(self, windows_context):
        """Test supports_unicode returns True when enabled"""
        assert windows_context.supports_unicode() is True

    def test_supports_unicode_false_encoding(self):
        """Test supports_unicode returns False with wrong encoding"""
        ctx = SystemContext(
            os_type="windows",
            os_version="10",
            os_platform="win32",
            shell_type="cmd",
            terminal_emulator="cmd",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="cp1252",
            python_version="3.11",
            python_executable="python.exe",
            pip_version="23.0",
            git_installed=False,
        )

        assert ctx.supports_unicode() is False

    def test_get_progress_chars_unicode(self, windows_context):
        """Test get_progress_chars returns unicode when supported"""
        chars = windows_context.get_progress_chars()

        assert chars["check"] == "✓"
        assert chars["cross"] == "✗"
        assert chars["arrow"] == "→"
        assert chars["bullet"] == "•"

    def test_get_progress_chars_ascii(self):
        """Test get_progress_chars returns ASCII when unicode not supported"""
        ctx = SystemContext(
            os_type="windows",
            os_version="10",
            os_platform="win32",
            shell_type="cmd",
            terminal_emulator="cmd",
            color_support=False,
            unicode_support=False,
            system_locale="en_US",
            detected_language="en",
            encoding="cp1252",
            python_version="3.11",
            python_executable="python.exe",
            pip_version="23.0",
            git_installed=False,
        )

        chars = ctx.get_progress_chars()

        assert chars["check"] == "[OK]"
        assert chars["cross"] == "[X]"
        assert chars["arrow"] == "->"
        assert chars["bullet"] == "*"

    def test_system_context_default_fields(self):
        """Test system context has proper defaults"""
        ctx = SystemContext(
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

        assert ctx.git_user_name is None
        assert ctx.git_user_email is None
        assert ctx.detected_editors == []
        assert ctx.active_editor is None
        assert ctx.project_root == Path.cwd()
        assert ctx.is_git_repo is False
        assert ctx.existing_tools == []
        assert ctx.file_count == 0
        assert ctx.line_count == 0
        assert ctx.has_tests is False
        assert ctx.has_ci is False


class TestAnswerContext:
    """Test AnswerContext model"""

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

    def test_answer_context_creation_empty(self, system_context):
        """Test creating empty answer context"""
        ctx = AnswerContext(system=system_context)

        assert ctx.system == system_context
        assert ctx.answers == {}

    def test_answer_context_creation_with_answers(self, system_context):
        """Test creating answer context with initial answers"""
        ctx = AnswerContext(
            system=system_context,
            answers={"team_size": "solo", "testing": "pytest"},
        )

        assert ctx.answers["team_size"] == "solo"
        assert ctx.answers["testing"] == "pytest"

    def test_answer_context_property_accessors(self, system_context):
        """Test property accessors return correct values"""
        ctx = AnswerContext(
            system=system_context,
            answers={
                "project_purpose": ["web_app", "api_service"],
                "team_dynamics": "small_team",
                "project_maturity": "production",
                "development_philosophy": "strict",
                "principle_strategy": "comprehensive",
                "testing_approach": "tdd",
                "security_stance": "paranoid",
                "documentation_level": "comprehensive",
                "git_workflow": "git-flow",
            },
        )

        assert ctx.project_types == ["web_app", "api_service"]
        assert ctx.team_size == "small_team"
        assert ctx.maturity == "production"
        assert ctx.philosophy == "strict"
        assert ctx.principle_strategy == "comprehensive"
        assert ctx.testing_approach == "tdd"
        assert ctx.security_stance == "paranoid"
        assert ctx.documentation_level == "comprehensive"
        assert ctx.git_workflow == "git-flow"

    def test_answer_context_property_defaults(self, system_context):
        """Test property accessors return defaults when missing"""
        ctx = AnswerContext(system=system_context)

        assert ctx.project_types == []
        assert ctx.team_size == "solo"
        assert ctx.maturity == "prototype"
        assert ctx.philosophy == "balanced"
        assert ctx.principle_strategy == "recommended"
        assert ctx.testing_approach == "no_tests"
        assert ctx.security_stance == "standard"
        assert ctx.documentation_level == "minimal"
        assert ctx.git_workflow == "main_only"

    def test_answer_context_get_method(self, system_context):
        """Test get method works correctly"""
        ctx = AnswerContext(
            system=system_context,
            answers={"key1": "value1"},
        )

        assert ctx.get("key1") == "value1"
        assert ctx.get("key2") is None
        assert ctx.get("key2", "default") == "default"

    def test_answer_context_set_method(self, system_context):
        """Test set method works correctly"""
        ctx = AnswerContext(system=system_context)

        ctx.set("new_key", "new_value")
        assert ctx.answers["new_key"] == "new_value"

    def test_answer_context_has_answer(self, system_context):
        """Test has_answer method works correctly"""
        ctx = AnswerContext(
            system=system_context,
            answers={"existing": "value"},
        )

        assert ctx.has_answer("existing") is True
        assert ctx.has_answer("missing") is False


class TestWizardResult:
    """Test WizardResult model"""

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

    def test_wizard_result_success(self, system_context):
        """Test creating successful wizard result"""
        result = WizardResult(
            success=True,
            mode="interactive",
            system_context=system_context,
            answers={"team_size": "solo"},
            selected_principles=["U_DRY", "U_TEST_FIRST"],
            selected_commands=["cco-status", "cco-test"],
            duration_seconds=45.2,
        )

        assert result.success is True
        assert result.mode == "interactive"
        assert result.system_context == system_context
        assert result.answers["team_size"] == "solo"
        assert len(result.selected_principles) == 2
        assert len(result.selected_commands) == 2
        assert result.skipped_questions == []
        assert result.duration_seconds == 45.2
        assert result.error is None

    def test_wizard_result_failure(self, system_context):
        """Test creating failed wizard result"""
        result = WizardResult(
            success=False,
            mode="quick",
            system_context=system_context,
            answers={},
            error="User cancelled wizard",
            duration_seconds=5.0,
        )

        assert result.success is False
        assert result.mode == "quick"
        assert result.error == "User cancelled wizard"

    def test_wizard_result_to_dict(self, system_context):
        """Test to_dict serialization"""
        result = WizardResult(
            success=True,
            mode="interactive",
            system_context=system_context,
            answers={"team_size": "solo"},
            selected_principles=["U_DRY"],
            selected_commands=["cco-status"],
            skipped_questions=["advanced_question"],
            duration_seconds=30.5,
        )

        data = result.to_dict()

        assert isinstance(data, dict)
        assert data["success"] is True
        assert data["mode"] == "interactive"
        assert data["answers"]["team_size"] == "solo"
        assert data["selected_principles"] == ["U_DRY"]
        assert data["selected_commands"] == ["cco-status"]
        assert data["skipped_questions"] == ["advanced_question"]
        assert data["duration_seconds"] == 30.5
        assert data["error"] is None


class TestToolComparison:
    """Test ToolComparison model"""

    def test_tool_comparison_creation(self):
        """Test creating tool comparison"""
        comparison = ToolComparison(
            category="formatter",
            tools=["black", "ruff"],
            recommended="ruff",
            reason="Faster and includes linting",
            alternatives={"black": "Pure formatter, well-established"},
        )

        assert comparison.category == "formatter"
        assert len(comparison.tools) == 2
        assert "black" in comparison.tools
        assert comparison.recommended == "ruff"
        assert "Faster" in comparison.reason
        assert "black" in comparison.alternatives

    def test_tool_comparison_defaults(self):
        """Test tool comparison has proper defaults"""
        comparison = ToolComparison(
            category="linter",
            tools=["pylint"],
            recommended="pylint",
            reason="Only tool detected",
        )

        assert comparison.alternatives == {}
