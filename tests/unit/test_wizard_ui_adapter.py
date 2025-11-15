"""
Comprehensive tests for wizard UI adapter module.

Tests cover:
- ClaudeCodeUIAdapter initialization and mode detection
- ask_decision method for both Claude Code and terminal modes
- Context-aware UI formatting and option building
- Recommendation logic and team-specific notes
- Progress and summary display
"""

import os
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.wizard.models import (
    AnswerContext,
    DecisionPoint,
    Option,
    SystemContext,
)
from claudecodeoptimizer.wizard.ui_adapter import ClaudeCodeUIAdapter


class TestClaudeCodeUIAdapterInit:
    """Test ClaudeCodeUIAdapter initialization and mode detection"""

    def test_init_auto_detect_terminal(self):
        """Test auto-detection defaults to terminal mode"""
        with patch.dict(os.environ, {}, clear=True):
            adapter = ClaudeCodeUIAdapter()
            assert adapter.mode == "terminal"

    def test_init_auto_detect_claude_code_env1(self):
        """Test auto-detection with CLAUDE_CODE=1"""
        with patch.dict(os.environ, {"CLAUDE_CODE": "1"}):
            adapter = ClaudeCodeUIAdapter()
            assert adapter.mode == "claude_code"

    def test_init_auto_detect_claude_code_env2(self):
        """Test auto-detection with ANTHROPIC_CLI"""
        with patch.dict(os.environ, {"ANTHROPIC_CLI": "true"}):
            adapter = ClaudeCodeUIAdapter()
            assert adapter.mode == "claude_code"

    def test_init_auto_detect_claude_code_env3(self):
        """Test auto-detection with CLAUDE_SESSION"""
        with patch.dict(os.environ, {"CLAUDE_SESSION": "session-123"}):
            adapter = ClaudeCodeUIAdapter()
            assert adapter.mode == "claude_code"

    def test_init_forced_terminal_mode(self):
        """Test forcing terminal mode"""
        with patch.dict(os.environ, {"CLAUDE_CODE": "1"}):
            adapter = ClaudeCodeUIAdapter(mode="terminal")
            assert adapter.mode == "terminal"

    def test_init_forced_claude_code_mode(self):
        """Test forcing Claude Code mode"""
        with patch.dict(os.environ, {}, clear=True):
            adapter = ClaudeCodeUIAdapter(mode="claude_code")
            assert adapter.mode == "claude_code"

    def test_detect_claude_code_context_all_indicators(self):
        """Test detection with all indicators present"""
        with patch.dict(
            os.environ,
            {
                "CLAUDE_CODE": "1",
                "ANTHROPIC_CLI": "true",
                "CLAUDE_SESSION": "session-123",
            },
        ):
            adapter = ClaudeCodeUIAdapter()
            assert adapter.mode == "claude_code"


class TestClaudeCodeUIAdapterAskDecision:
    """Test ask_decision method"""

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
            has_ci=True,
            is_git_repo=True,
        )

    @pytest.fixture
    def answer_context(self, system_context) -> AnswerContext:
        """Sample answer context"""
        return AnswerContext(
            system=system_context,
            answers={
                "team_dynamics": "solo",
                "project_maturity": "prototype",
                "development_philosophy": "balanced",
            },
        )

    @pytest.fixture
    def sample_decision(self) -> DecisionPoint:
        """Sample decision point"""
        return DecisionPoint(
            id="test_decision",
            tier=1,
            category="project_identity",
            question="What is your project type?",
            options=[
                Option(
                    value="web_app",
                    label="Web Application",
                    description="Full-stack web application",
                    recommended_for=["solo", "small_team"],
                ),
                Option(
                    value="cli_tool",
                    label="CLI Tool",
                    description="Command-line interface tool",
                    recommended_for=["solo"],
                ),
                Option(
                    value="api_service",
                    label="API Service",
                    description="RESTful API backend",
                    recommended_for=["large_org"],
                ),
            ],
        )

    def test_ask_decision_routes_to_claude_tool(self, sample_decision, answer_context):
        """Test ask_decision routes to Claude tool in claude_code mode"""
        adapter = ClaudeCodeUIAdapter(mode="claude_code")

        # Mock the terminal fallback that _ask_via_claude_tool calls
        with patch.object(adapter, "_ask_via_terminal") as mock_terminal:
            mock_terminal.return_value = "web_app"
            result = adapter.ask_decision(sample_decision, answer_context)

            # Should have printed Claude UI info and fallen back to terminal
            mock_terminal.assert_called_once_with(sample_decision, answer_context)
            assert result == "web_app"

    def test_ask_decision_routes_to_terminal(self, sample_decision, answer_context):
        """Test ask_decision routes to terminal in terminal mode"""
        adapter = ClaudeCodeUIAdapter(mode="terminal")

        with patch("builtins.input", return_value="1"):
            result = adapter.ask_decision(sample_decision, answer_context)
            assert result == "web_app"


class TestClaudeCodeUIAdapterClaudeTool:
    """Test _ask_via_claude_tool method"""

    @pytest.fixture
    def adapter(self):
        """Claude Code mode adapter"""
        return ClaudeCodeUIAdapter(mode="claude_code")

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

    @pytest.fixture
    def answer_context(self, system_context) -> AnswerContext:
        """Sample answer context"""
        return AnswerContext(system=system_context)

    @pytest.fixture
    def sample_decision(self) -> DecisionPoint:
        """Sample decision point"""
        return DecisionPoint(
            id="test",
            tier=1,
            category="project_identity",
            question="Choose your option?",
            options=[
                Option(
                    value="opt1",
                    label="Option 1",
                    description="First option",
                ),
                Option(
                    value="opt2",
                    label="Option 2",
                    description="Second option",
                ),
            ],
        )

    def test_ask_via_claude_tool_builds_correct_structure(
        self, adapter, sample_decision, answer_context, capsys
    ):
        """Test _ask_via_claude_tool builds correct question data"""
        with patch.object(adapter, "_ask_via_terminal") as mock_terminal:
            mock_terminal.return_value = "opt1"

            result = adapter._ask_via_claude_tool(sample_decision, answer_context)

            # Check console output contains expected elements
            captured = capsys.readouterr()
            assert "Claude Code UI Adapter" in captured.out
            assert "Choose your option?" in captured.out
            assert "Multi-Select: False" in captured.out
            assert "Option 1" in captured.out
            assert "First option" in captured.out


class TestClaudeCodeUIAdapterTerminal:
    """Test _ask_via_terminal method"""

    @pytest.fixture
    def adapter(self):
        """Terminal mode adapter"""
        return ClaudeCodeUIAdapter(mode="terminal")

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

    @pytest.fixture
    def answer_context(self, system_context) -> AnswerContext:
        """Sample answer context"""
        return AnswerContext(system=system_context)

    @pytest.fixture
    def sample_decision(self) -> DecisionPoint:
        """Sample decision point"""
        return DecisionPoint(
            id="test",
            tier=1,
            category="project_identity",
            question="Choose your option?",
            options=[
                Option(
                    value="opt1",
                    label="Option 1",
                    description="First option",
                    recommended_for=["solo"],
                ),
                Option(
                    value="opt2",
                    label="Option 2",
                    description="Second option",
                ),
            ],
        )

    def test_ask_via_terminal_single_select_valid(
        self, adapter, sample_decision, answer_context
    ):
        """Test terminal single select with valid input"""
        with patch("builtins.input", return_value="1"):
            result = adapter._ask_via_terminal(sample_decision, answer_context)
            assert result == "opt1"

    def test_ask_via_terminal_single_select_second_option(
        self, adapter, sample_decision, answer_context
    ):
        """Test terminal single select with second option"""
        with patch("builtins.input", return_value="2"):
            result = adapter._ask_via_terminal(sample_decision, answer_context)
            assert result == "opt2"

    def test_ask_via_terminal_multi_select_valid(self, adapter, system_context):
        """Test terminal multi-select with valid input"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Choose options?",
            multi_select=True,
            options=[
                Option(value="opt1", label="Option 1", description="First"),
                Option(value="opt2", label="Option 2", description="Second"),
                Option(value="opt3", label="Option 3", description="Third"),
            ],
        )
        context = AnswerContext(system=system_context)

        with patch("builtins.input", return_value="1,3"):
            result = adapter._ask_via_terminal(decision, context)
            assert result == ["opt1", "opt3"]

    def test_ask_via_terminal_invalid_then_valid(
        self, adapter, sample_decision, answer_context
    ):
        """Test terminal with invalid then valid input"""
        with patch("builtins.input", side_effect=["invalid", "99", "1"]):
            result = adapter._ask_via_terminal(sample_decision, answer_context)
            assert result == "opt1"

    def test_ask_via_terminal_empty_input_with_recommendation(
        self, adapter, system_context
    ):
        """Test terminal with empty input uses recommendation"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Choose?",
            options=[
                Option(value="opt1", label="Option 1", description="First"),
                Option(value="opt2", label="Option 2", description="Second"),
            ],
            auto_strategy=lambda ctx: "opt2",
        )
        context = AnswerContext(system=system_context)

        with patch("builtins.input", return_value=""):
            result = adapter._ask_via_terminal(decision, context)
            assert result == "opt2"

    def test_ask_via_terminal_displays_ai_hint(
        self, adapter, system_context, capsys
    ):
        """Test terminal displays AI hint when available"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Choose?",
            options=[
                Option(value="opt1", label="Option 1", description="First"),
            ],
            ai_hint_generator=lambda ctx: "I recommend option 1",
        )
        context = AnswerContext(system=system_context)

        with patch("builtins.input", return_value="1"):
            adapter._ask_via_terminal(decision, context)
            captured = capsys.readouterr()
            assert "AI Suggestion" in captured.out
            assert "I recommend option 1" in captured.out


class TestClaudeCodeUIAdapterFormatting:
    """Test formatting methods"""

    @pytest.fixture
    def adapter(self):
        """Terminal mode adapter"""
        return ClaudeCodeUIAdapter(mode="terminal")

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
            has_ci=True,
            is_git_repo=True,
        )

    @pytest.fixture
    def answer_context(self, system_context) -> AnswerContext:
        """Sample answer context"""
        return AnswerContext(
            system=system_context,
            answers={
                "team_dynamics": "solo",
                "project_maturity": "production",
                "project_purpose": ["web_app"],
            },
        )

    def test_format_header_short(self, adapter, answer_context):
        """Test header formatting for short category"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="team",
            question="Test?",
            options=[Option(value="opt1", label="Opt1", description="Desc")],
        )

        header = adapter._format_header(decision, answer_context)
        assert header == "Team"
        assert len(header) <= 12

    def test_format_header_long_truncated(self, adapter, answer_context):
        """Test header formatting truncates long category"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="very_long_category_name",
            question="Test?",
            options=[Option(value="opt1", label="Opt1", description="Desc")],
        )

        header = adapter._format_header(decision, answer_context)
        assert len(header) <= 12

    def test_format_header_underscores_to_title(self, adapter, answer_context):
        """Test header formatting converts underscores to title case"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="project_type",
            question="Test?",
            options=[Option(value="opt1", label="Opt1", description="Desc")],
        )

        header = adapter._format_header(decision, answer_context)
        assert header == "Project Type"

    def test_build_rich_options_with_recommendation(self, adapter, answer_context):
        """Test building rich options with recommendation marker"""
        decision = DecisionPoint(
            id="test",
            tier=1,
            category="test",
            question="Test?",
            options=[
                Option(
                    value="opt1",
                    label="Option 1",
                    description="First option",
                    recommended_for=["solo"],
                ),
                Option(
                    value="opt2",
                    label="Option 2",
                    description="Second option",
                    recommended_for=["large_org"],
                ),
            ],
        )

        options = adapter._build_rich_options(decision, answer_context)

        assert len(options) == 2
        assert "⭐" in options[0]["label"]  # Recommended for solo
        assert "⭐" not in options[1]["label"]  # Not recommended for solo

    def test_build_context_description_full(self, adapter, answer_context):
        """Test building context description with all elements"""
        option = Option(
            value="opt1",
            label="Option 1",
            description="Base description",
            recommended_for=["solo"],
            trade_offs="Fast but simple",
            time_investment="2 hours",
            effects="Creates new files",
        )

        desc = adapter._build_context_description(option, answer_context, True)

        assert "Base description" in desc
        assert "Fast but simple" in desc
        assert "2 hours" in desc
        assert "Creates new files" in desc


class TestClaudeCodeUIAdapterRecommendations:
    """Test recommendation and context logic"""

    @pytest.fixture
    def adapter(self):
        """Terminal mode adapter"""
        return ClaudeCodeUIAdapter(mode="terminal")

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
            has_ci=True,
            is_git_repo=True,
        )

    def test_is_recommended_for_context_match(self, adapter, system_context):
        """Test recommendation matching for context"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["solo"],
        )

        assert adapter._is_recommended_for_context(option, context) is True

    def test_is_recommended_for_context_no_match(self, adapter, system_context):
        """Test recommendation not matching for context"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["large_org"],
        )

        assert adapter._is_recommended_for_context(option, context) is False

    def test_is_recommended_for_context_no_recommendations(self, adapter, system_context):
        """Test option without recommendations"""
        context = AnswerContext(system=system_context)
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
        )

        assert adapter._is_recommended_for_context(option, context) is False

    def test_get_context_tags_team_size(self, adapter, system_context):
        """Test context tags include team size"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )

        tags = adapter._get_context_tags(context)
        assert "solo" in tags

    def test_get_context_tags_maturity(self, adapter, system_context):
        """Test context tags include maturity"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )

        tags = adapter._get_context_tags(context)
        assert "production" in tags

    def test_get_context_tags_philosophy(self, adapter, system_context):
        """Test context tags include philosophy"""
        context = AnswerContext(
            system=system_context,
            answers={"development_philosophy": "strict"},
        )

        tags = adapter._get_context_tags(context)
        assert "strict" in tags

    def test_get_context_tags_project_types_list(self, adapter, system_context):
        """Test context tags include project types as list"""
        context = AnswerContext(
            system=system_context,
            answers={"project_purpose": ["web_app", "api_service"]},
        )

        tags = adapter._get_context_tags(context)
        assert "web_app" in tags
        assert "api_service" in tags

    def test_get_context_tags_has_ci(self, adapter, system_context):
        """Test context tags include CI/CD detection"""
        context = AnswerContext(system=system_context)

        tags = adapter._get_context_tags(context)
        assert "has_ci" in tags

    def test_get_context_tags_has_git(self, adapter, system_context):
        """Test context tags include git detection"""
        context = AnswerContext(system=system_context)

        tags = adapter._get_context_tags(context)
        assert "has_git" in tags

    def test_get_recommendation_reason_solo(self, adapter, system_context):
        """Test recommendation reason for solo developer"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["solo"],
        )

        reason = adapter._get_recommendation_reason(option, context)
        assert "solo" in reason.lower()

    def test_get_recommendation_reason_small_team(self, adapter, system_context):
        """Test recommendation reason for small team"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "small_team"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["small_team"],
        )

        reason = adapter._get_recommendation_reason(option, context)
        assert "small team" in reason.lower()

    def test_get_recommendation_reason_production(self, adapter, system_context):
        """Test recommendation reason for production maturity"""
        context = AnswerContext(
            system=system_context,
            answers={"project_maturity": "production"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["production"],
        )

        reason = adapter._get_recommendation_reason(option, context)
        assert "production" in reason.lower()

    def test_get_team_specific_note_solo_with_large_org_option(
        self, adapter, system_context
    ):
        """Test team-specific note warns solo about large org option"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "solo"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["large_org"],
        )

        note = adapter._get_team_specific_note(option, context)
        assert "overkill" in note.lower()

    def test_get_team_specific_note_large_org_with_solo_option(
        self, adapter, system_context
    ):
        """Test team-specific note warns large org about solo option"""
        context = AnswerContext(
            system=system_context,
            answers={"team_dynamics": "large_org"},
        )
        option = Option(
            value="opt1",
            label="Option 1",
            description="Desc",
            recommended_for=["solo"],
        )

        note = adapter._get_team_specific_note(option, context)
        assert "robust" in note.lower()


class TestClaudeCodeUIAdapterDisplay:
    """Test display methods"""

    @pytest.fixture
    def adapter(self):
        """Terminal mode adapter"""
        return ClaudeCodeUIAdapter(mode="terminal")

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

    def test_show_progress_terminal_mode(self, adapter, capsys):
        """Test progress display in terminal mode"""
        adapter.show_progress(3, 10, "Processing...")
        captured = capsys.readouterr()

        assert "[3/10]" in captured.out
        assert "Processing..." in captured.out

    def test_show_progress_claude_code_mode(self, capsys):
        """Test progress display in Claude Code mode"""
        adapter = ClaudeCodeUIAdapter(mode="claude_code")
        adapter.show_progress(5, 10, "Processing...")
        captured = capsys.readouterr()

        assert "50%" in captured.out
        assert "Processing..." in captured.out
        assert "█" in captured.out or "░" in captured.out

    def test_show_summary_displays_all_answers(self, adapter, system_context, capsys):
        """Test summary displays all answers"""
        context = AnswerContext(
            system=system_context,
            answers={
                "team_dynamics": "solo",
                "project_maturity": "production",
                "testing_approach": "tdd",
            },
        )

        adapter.show_summary(context)
        captured = capsys.readouterr()

        assert "Configuration Summary" in captured.out
        assert "Team Dynamics" in captured.out
        assert "solo" in captured.out
        assert "Project Maturity" in captured.out
        assert "production" in captured.out

    def test_show_summary_formats_lists(self, adapter, system_context, capsys):
        """Test summary formats list values correctly"""
        context = AnswerContext(
            system=system_context,
            answers={
                "project_purpose": ["web_app", "api_service"],
            },
        )

        adapter.show_summary(context)
        captured = capsys.readouterr()

        assert "web_app, api_service" in captured.out
