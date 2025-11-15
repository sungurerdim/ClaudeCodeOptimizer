"""
Comprehensive tests for wizard orchestrator module.

Tests cover:
- CCOWizard initialization
- System detection
- Project detection
- Decision tree execution
- Principle selection
- Command selection
- File generation
- Result creation and saving
- Export questions functionality
- Run with answers functionality
- Uninitialize functionality
- Error handling and edge cases
"""

from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from claudecodeoptimizer.wizard.models import (
    AnswerContext,
    DecisionPoint,
    Option,
    SystemContext,
    WizardResult,
)
from claudecodeoptimizer.wizard.orchestrator import (
    CCOWizard,
    run_interactive_wizard,
    run_quick_wizard,
)

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_project(tmp_path) -> Path:
    """Create temporary project directory"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def mock_system_context() -> SystemContext:
    """Create mock system context"""
    return SystemContext(
        os_type="linux",
        os_version="5.15.0",
        os_platform="x86_64",
        shell_type="bash",
        terminal_emulator="gnome-terminal",
        color_support=True,
        unicode_support=True,
        system_locale="en_US.UTF-8",
        detected_language="en",
        encoding="utf-8",
        python_version="3.11.0",
        python_executable="/usr/bin/python3",
        pip_version="23.0",
        git_installed=True,
        is_git_repo=True,
        project_root=Path("/tmp/test"),
    )


@pytest.fixture
def mock_detection_report() -> Dict[str, Any]:
    """Create mock detection report"""
    return {
        "languages": [
            {
                "detected_value": "python",
                "confidence": 0.95,
                "evidence": ["*.py files", "requirements.txt"],
            }
        ],
        "frameworks": [
            {
                "detected_value": "pytest",
                "confidence": 0.85,
                "evidence": ["conftest.py", "test_*.py"],
            }
        ],
        "project_types": [{"detected_value": "cli_tool", "confidence": 0.80}],
        "tools": [{"detected_value": "git", "category": "vcs"}],
        "codebase_patterns": {
            "total_files": 50,
            "total_lines": 2000,
            "file_distribution": {".py": 40, ".md": 5, ".txt": 5},
        },
    }


@pytest.fixture
def mock_decision_point() -> DecisionPoint:
    """Create mock decision point"""
    return DecisionPoint(
        id="test_decision",
        tier=1,
        category="fundamentals",
        question="What is your project purpose?",
        why_this_question="To understand project context",
        options=[
            Option(
                value="cli_tool",
                label="CLI Tool",
                description="Command-line interface application",
            ),
            Option(
                value="web_app",
                label="Web App",
                description="Web application",
            ),
        ],
        multi_select=False,
        auto_strategy="first",
    )


# ============================================================================
# Test CCOWizard Initialization
# ============================================================================


class TestCCOWizardInit:
    """Test CCOWizard initialization"""

    def test_init_interactive_mode(self, temp_project):
        """Test initialization in interactive mode"""
        wizard = CCOWizard(temp_project, mode="interactive", dry_run=False)

        assert wizard.project_root == temp_project
        assert wizard.mode == "interactive"
        assert wizard.dry_run is False
        assert wizard.system_context is None
        assert wizard.detection_report is None
        assert wizard.answer_context is None
        assert wizard.selected_principles == []
        assert wizard.selected_commands == []
        assert wizard.selected_guides == []
        assert wizard.selected_agents == []
        assert wizard.selected_skills == []
        assert wizard.rec_engine is not None
        assert wizard.ui_adapter is not None

    def test_init_quick_mode(self, temp_project):
        """Test initialization in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick", dry_run=False)

        assert wizard.mode == "quick"
        assert wizard.dry_run is False

    def test_init_dry_run(self, temp_project):
        """Test initialization with dry_run=True"""
        wizard = CCOWizard(temp_project, mode="interactive", dry_run=True)

        assert wizard.dry_run is True


# ============================================================================
# Test System Detection
# ============================================================================


class TestSystemDetection:
    """Test system detection phase"""

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.pause")
    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    def test_run_system_detection_interactive_success(
        self, mock_clear, mock_pause, mock_detector_class, temp_project, mock_system_context
    ):
        """Test successful system detection in interactive mode"""
        # Setup mock detector
        mock_detector = Mock()
        mock_detector.detect_all.return_value = mock_system_context
        mock_detector_class.return_value = mock_detector

        wizard = CCOWizard(temp_project, mode="interactive")
        result = wizard._run_system_detection()

        assert result is True
        assert wizard.system_context == mock_system_context
        mock_detector.detect_all.assert_called_once()
        mock_clear.assert_called_once()
        mock_pause.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    def test_run_system_detection_quick_success(
        self, mock_detector_class, temp_project, mock_system_context
    ):
        """Test successful system detection in quick mode (no UI interaction)"""
        mock_detector = Mock()
        mock_detector.detect_all.return_value = mock_system_context
        mock_detector_class.return_value = mock_detector

        wizard = CCOWizard(temp_project, mode="quick")
        result = wizard._run_system_detection()

        assert result is True
        assert wizard.system_context == mock_system_context
        mock_detector.detect_all.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_error")
    def test_run_system_detection_failure(
        self, mock_print_error, mock_detector_class, temp_project
    ):
        """Test system detection failure"""
        mock_detector = Mock()
        mock_detector.detect_all.side_effect = Exception("Detection failed")
        mock_detector_class.return_value = mock_detector

        wizard = CCOWizard(temp_project, mode="quick")
        result = wizard._run_system_detection()

        assert result is False
        mock_print_error.assert_called_once()


# ============================================================================
# Test Project Detection
# ============================================================================


class TestProjectDetection:
    """Test project detection phase"""

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.display_detection_results")
    def test_run_project_detection_quick_success(
        self,
        mock_display,
        mock_detector_class,
        mock_sys_detector_class,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test successful project detection in quick mode"""
        # Setup wizard with system context
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        # Setup mock detector
        mock_detector = Mock()
        mock_analysis = Mock()
        mock_analysis.dict.return_value = mock_detection_report
        mock_detector.analyze.return_value = mock_analysis
        mock_detector_class.return_value = mock_detector

        # Setup mock system detector for enrichment
        mock_sys_detector = Mock()
        mock_sys_detector.enrich_with_project_detection.return_value = mock_system_context
        mock_sys_detector_class.return_value = mock_sys_detector

        result = wizard._run_project_detection()

        assert result is True
        assert wizard.detection_report == mock_detection_report
        mock_detector.analyze.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_error")
    def test_run_project_detection_failure(
        self, mock_print_error, mock_detector_class, temp_project, mock_system_context
    ):
        """Test project detection failure"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_detector = Mock()
        mock_detector.analyze.side_effect = Exception("Analysis failed")
        mock_detector_class.return_value = mock_detector

        result = wizard._run_project_detection()

        assert result is False
        mock_print_error.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.display_detection_results")
    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.renderer.ask_yes_no")
    def test_confirm_analysis_confirmed(
        self,
        mock_ask_yes_no,
        mock_clear,
        mock_display,
        mock_detector_class,
        mock_sys_detector_class,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test user confirming analysis in interactive mode"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context

        mock_detector = Mock()
        mock_analysis = Mock()
        mock_analysis.dict.return_value = mock_detection_report
        mock_detector.analyze.return_value = mock_analysis
        mock_detector_class.return_value = mock_detector

        mock_sys_detector = Mock()
        mock_sys_detector.enrich_with_project_detection.return_value = mock_system_context
        mock_sys_detector_class.return_value = mock_sys_detector

        mock_ask_yes_no.return_value = True

        result = wizard._run_project_detection()

        assert result is True


# ============================================================================
# Test Helper Methods
# ============================================================================


class TestHelperMethods:
    """Test helper methods"""

    def test_get_primary_language_name(self, temp_project, mock_detection_report):
        """Test getting primary language name"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.detection_report = mock_detection_report

        language = wizard._get_primary_language_name()
        assert language == "python"

    def test_get_primary_language_name_empty(self, temp_project):
        """Test getting primary language when none detected"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.detection_report = {"languages": []}

        language = wizard._get_primary_language_name()
        assert language == "Unknown"

    def test_get_frameworks_summary(self, temp_project, mock_detection_report):
        """Test getting frameworks summary"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.detection_report = mock_detection_report

        summary = wizard._get_frameworks_summary()
        assert summary == "pytest"

    def test_get_frameworks_summary_empty(self, temp_project):
        """Test getting frameworks summary when none detected"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.detection_report = {"frameworks": []}

        summary = wizard._get_frameworks_summary()
        assert summary == "None"

    def test_get_project_type_summary(self, temp_project, mock_detection_report):
        """Test getting project type summary"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.detection_report = {
            "project_types": [
                {"name": "CLI Tool", "confidence": 0.9},
                {"name": "Library", "confidence": 0.7},
            ]
        }

        summary = wizard._get_project_type_summary()
        assert summary == "CLI Tool, Library"

    def test_map_testing_to_coverage(self, temp_project):
        """Test mapping testing approach to coverage target"""
        wizard = CCOWizard(temp_project, mode="quick")

        assert wizard._map_testing_to_coverage("no_tests") == "0"
        assert wizard._map_testing_to_coverage("critical_paths") == "50"
        assert wizard._map_testing_to_coverage("balanced") == "80"
        assert wizard._map_testing_to_coverage("comprehensive") == "90"
        assert wizard._map_testing_to_coverage("unknown") == "80"  # default

    def test_map_strategy_to_strictness(self, temp_project):
        """Test mapping principle strategy to linting strictness"""
        wizard = CCOWizard(temp_project, mode="quick")

        assert wizard._map_strategy_to_strictness("minimal") == "moderate"
        assert wizard._map_strategy_to_strictness("recommended") == "strict"
        assert wizard._map_strategy_to_strictness("comprehensive") == "pedantic"
        assert wizard._map_strategy_to_strictness("custom") == "strict"
        assert wizard._map_strategy_to_strictness("unknown") == "strict"  # default


# ============================================================================
# Test Decision Tree Execution
# ============================================================================


class TestDecisionTree:
    """Test decision tree execution"""

    @patch("claudecodeoptimizer.wizard.orchestrator.get_all_decisions")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_info")
    def test_run_decision_tree_quick_mode(
        self, mock_print, mock_get_decisions, temp_project, mock_system_context
    ):
        """Test running decision tree in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        # Create a proper mock decision with all required attributes
        mock_decision = Mock()
        mock_decision.id = "test_decision"
        mock_decision.question = "Test question"
        mock_decision.multi_select = False
        mock_decision.should_ask.return_value = True
        mock_decision.get_recommended_option.return_value = "cli_tool"
        mock_decision.get_ai_hint.return_value = "Recommended"

        # Setup mock decisions
        mock_get_decisions.return_value = [mock_decision]

        result = wizard._run_decision_tree()

        assert result is True
        assert wizard.answer_context is not None
        assert "test_decision" in wizard.answer_context.answers

    @patch("claudecodeoptimizer.wizard.orchestrator.get_all_decisions")
    def test_run_decision_tree_skip_conditional(
        self, mock_get_decisions, temp_project, mock_system_context
    ):
        """Test skipping conditional questions in decision tree"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        # Create decision that should be skipped
        mock_decision = Mock(spec=DecisionPoint)
        mock_decision.should_ask.return_value = False
        mock_get_decisions.return_value = [mock_decision]

        result = wizard._run_decision_tree()

        assert result is True
        # Decision should not be executed
        mock_decision.get_recommended_option.assert_not_called()

    @patch("claudecodeoptimizer.wizard.orchestrator.get_all_decisions")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_error")
    def test_run_decision_tree_failure(
        self, mock_print_error, mock_get_decisions, temp_project, mock_system_context
    ):
        """Test decision tree execution failure"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_get_decisions.side_effect = Exception("Decision tree build failed")

        result = wizard._run_decision_tree()

        assert result is False
        mock_print_error.assert_called_once()

    def test_auto_decide(self, temp_project, mock_system_context, mock_decision_point):
        """Test auto-decision in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Mock the decision to return a specific answer
        mock_decision_point.get_recommended_option = Mock(return_value="cli_tool")
        mock_decision_point.get_ai_hint = Mock(return_value="Recommended for your project")

        answer = wizard._auto_decide(mock_decision_point)

        assert answer == "cli_tool"
        mock_decision_point.get_recommended_option.assert_called_once()

    def test_auto_decide_multi_select(self, temp_project, mock_system_context):
        """Test auto-decision with multi-select question"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Create multi-select decision
        multi_decision = DecisionPoint(
            id="test_multi",
            tier=1,
            category="fundamentals",
            question="Select project types",
            why_this_question="To understand context",
            options=[
                Option(value="cli", label="CLI", description="CLI tool"),
                Option(value="web", label="Web", description="Web app"),
            ],
            multi_select=True,
            auto_strategy="all",
        )
        multi_decision.get_recommended_option = Mock(return_value=["cli", "web"])
        multi_decision.get_ai_hint = Mock(return_value="Both recommended")

        answer = wizard._auto_decide(multi_decision)

        assert answer == ["cli", "web"]


# ============================================================================
# Test Principle Selection
# ============================================================================


class TestPrincipleSelection:
    """Test principle selection phase"""

    @patch("claudecodeoptimizer.core.principle_selector.PrincipleSelector")
    def test_run_principle_selection_quick_mode(
        self, mock_selector_class, temp_project, mock_system_context
    ):
        """Test principle selection in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Setup mock selector
        mock_selector = Mock()
        mock_selector.all_principles = [
            {"id": "U_DRY", "title": "DRY Principle", "category": "universal"},
            {"id": "P_TEST_COVERAGE", "title": "Test Coverage", "category": "testing"},
        ]
        mock_selector.select_applicable.return_value = [
            {"id": "U_DRY", "title": "DRY Principle"},
        ]
        mock_selector_class.return_value = mock_selector

        result = wizard._run_principle_selection()

        assert result is True
        assert wizard.selected_principles == ["U_DRY"]

    @patch("claudecodeoptimizer.core.principle_selector.PrincipleSelector")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_error")
    def test_run_principle_selection_failure(
        self, mock_print_error, mock_selector_class, temp_project, mock_system_context
    ):
        """Test principle selection failure"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        mock_selector_class.side_effect = Exception("Selection failed")

        result = wizard._run_principle_selection()

        assert result is False
        mock_print_error.assert_called_once()


# ============================================================================
# Test Command Selection
# ============================================================================


class TestCommandSelection:
    """Test command selection phase"""

    @patch("claudecodeoptimizer.ai.command_selection.CommandRecommender")
    def test_run_command_selection_quick_mode(
        self, mock_recommender_class, temp_project, mock_system_context
    ):
        """Test command selection in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Setup mock recommender
        mock_recommender = Mock()
        mock_recommender.recommend_commands.return_value = {
            "core": ["cco-init", "cco-status"],
            "recommended": ["cco-audit", "cco-fix"],
            "optional": ["cco-optimize"],
            "reasoning": {
                "cco-init": "Essential initialization",
                "cco-status": "Essential status check",
            },
        }
        mock_recommender_class.return_value = mock_recommender

        result = wizard._run_command_selection()

        assert result is True
        assert "cco-init" in wizard.selected_commands
        assert "cco-audit" in wizard.selected_commands
        # Optional commands should NOT be auto-selected
        assert "cco-optimize" not in wizard.selected_commands

    def test_build_command_registry(self, temp_project):
        """Test building command registry from global commands"""
        wizard = CCOWizard(temp_project, mode="quick")

        with patch("claudecodeoptimizer.config.get_global_commands_dir") as mock_get_dir:
            mock_commands_dir = Mock()
            mock_commands_dir.exists.return_value = True
            mock_commands_dir.glob.return_value = [
                Mock(stem="cco-init"),
                Mock(stem="cco-status"),
            ]
            mock_get_dir.return_value = mock_commands_dir

            registry = wizard._build_command_registry()

            assert len(registry.commands) == 2
            assert any(cmd.command_id == "cco-init" for cmd in registry.commands)


# ============================================================================
# Test File Generation
# ============================================================================


class TestFileGeneration:
    """Test file generation phase"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._setup_knowledge_symlinks")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._update_gitignore")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._generate_claude_md")
    def test_run_file_generation_success(
        self,
        mock_generate_md,
        mock_update_gitignore,
        mock_setup_symlinks,
        temp_project,
    ):
        """Test successful file generation"""
        wizard = CCOWizard(temp_project, mode="quick", dry_run=False)

        result = wizard._run_file_generation()

        assert result is True
        mock_setup_symlinks.assert_called_once()
        mock_update_gitignore.assert_called_once()
        mock_generate_md.assert_called_once()
        # Check .claude/commands directory created
        assert (temp_project / ".claude" / "commands").exists()

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._setup_knowledge_symlinks")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_error")
    def test_run_file_generation_failure(self, mock_print_error, mock_setup_symlinks, temp_project):
        """Test file generation failure"""
        wizard = CCOWizard(temp_project, mode="quick", dry_run=False)

        mock_setup_symlinks.side_effect = Exception("Symlink failed")

        result = wizard._run_file_generation()

        assert result is False
        mock_print_error.assert_called_once()

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_setup_knowledge_symlinks(
        self,
        mock_get_skills,
        mock_get_agents,
        mock_get_principles,
        mock_get_guides,
        mock_get_commands,
        mock_setup_global,
        temp_project,
    ):
        """Test setting up knowledge base symlinks"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init", "cco-status"]
        wizard.selected_guides = ["cco-git-workflow"]
        wizard.selected_principles = ["P_TEST_COVERAGE"]
        wizard.selected_agents = []
        wizard.selected_skills = []

        # Setup mock directories
        mock_commands_dir = temp_project / "mock_commands"
        mock_guides_dir = temp_project / "mock_guides"
        mock_principles_dir = temp_project / "mock_principles"
        mock_commands_dir.mkdir()
        mock_guides_dir.mkdir()
        mock_principles_dir.mkdir()

        # Create mock files
        (mock_commands_dir / "cco-init.md").touch()
        (mock_commands_dir / "cco-status.md").touch()
        (mock_guides_dir / "cco-git-workflow.md").touch()
        (mock_principles_dir / "P_TEST_COVERAGE.md").touch()
        (mock_principles_dir / "U_DRY.md").touch()

        mock_get_commands.return_value = mock_commands_dir
        mock_get_guides.return_value = mock_guides_dir
        mock_get_principles.return_value = mock_principles_dir
        mock_get_agents.return_value = temp_project / "mock_agents"
        mock_get_skills.return_value = temp_project / "mock_skills"

        wizard._setup_knowledge_symlinks()

        # Check directories created
        assert (temp_project / ".claude" / "commands").exists()
        assert (temp_project / ".claude" / "guides").exists()
        assert (temp_project / ".claude" / "principles").exists()

    def test_update_gitignore_new_file(self, temp_project):
        """Test updating .gitignore when file doesn't exist"""
        wizard = CCOWizard(temp_project, mode="quick")

        wizard._update_gitignore()

        gitignore_path = temp_project / ".gitignore"
        assert gitignore_path.exists()

        content = gitignore_path.read_text()
        assert "# CCO: Symlinked knowledge base" in content
        assert ".claude/commands/*" in content

    def test_update_gitignore_existing_file(self, temp_project):
        """Test updating .gitignore when file already exists"""
        wizard = CCOWizard(temp_project, mode="quick")

        # Create existing .gitignore
        gitignore_path = temp_project / ".gitignore"
        gitignore_path.write_text("*.pyc\n__pycache__/\n")

        wizard._update_gitignore()

        content = gitignore_path.read_text()
        assert "*.pyc" in content  # Original content preserved
        assert "# CCO: Symlinked knowledge base" in content

    def test_update_gitignore_already_has_cco_section(self, temp_project):
        """Test updating .gitignore when CCO section already exists"""
        wizard = CCOWizard(temp_project, mode="quick")

        # Create .gitignore with CCO section
        gitignore_path = temp_project / ".gitignore"
        gitignore_path.write_text("# CCO: Symlinked knowledge base\n.claude/commands/*\n")

        original_content = gitignore_path.read_text()
        wizard._update_gitignore()

        # Content should be unchanged
        assert gitignore_path.read_text() == original_content

    @patch("claudecodeoptimizer.core.claude_md_generator.ClaudeMdGenerator")
    def test_generate_claude_md(self, mock_generator_class, temp_project, mock_system_context):
        """Test generating CLAUDE.md"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.selected_principles = ["U_DRY", "P_TEST_COVERAGE"]

        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator

        wizard._generate_claude_md()

        mock_generator.generate.assert_called_once_with(temp_project / "CLAUDE.md")


# ============================================================================
# Test Build Preferences
# ============================================================================


class TestBuildPreferences:
    """Test building preferences from answers"""

    def test_build_preferences_minimal(self, temp_project, mock_system_context):
        """Test building preferences with minimal answers"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.selected_principles = []

        prefs = wizard._build_preferences()

        assert prefs["project_identity"]["name"] == temp_project.name
        assert "team_trajectory" in prefs["project_identity"]
        assert "code_philosophy" in prefs["development_style"]

    def test_build_preferences_full(self, temp_project, mock_system_context):
        """Test building preferences with all answers"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Set answers
        wizard.answer_context.set("project_purpose", ["cli_tool", "library"])
        wizard.answer_context.set("team_dynamics", "small-2-5")
        wizard.answer_context.set("project_maturity", "production")
        wizard.answer_context.set("development_philosophy", "quality_first")
        wizard.answer_context.set("testing_approach", "comprehensive")
        wizard.answer_context.set("security_stance", "high")
        wizard.answer_context.set("documentation_level", "comprehensive")
        wizard.answer_context.set("git_workflow", "github_flow")

        wizard.selected_principles = ["U_DRY", "P_TEST_COVERAGE"]

        prefs = wizard._build_preferences()

        assert prefs["project_identity"]["types"] == ["cli_tool", "library"]
        assert prefs["project_identity"]["team_trajectory"] == "small-2-5"
        assert prefs["project_identity"]["project_maturity"] == "production"
        assert prefs["development_style"]["code_philosophy"] == "conservative"
        assert prefs["testing"]["coverage_target"] == "90"
        assert prefs["security"]["security_stance"] == "very-strict"
        assert prefs["documentation"]["verbosity"] == "extensive"
        assert prefs["collaboration"]["git_workflow"] == "github-flow"
        assert prefs["selected_principle_ids"] == ["U_DRY", "P_TEST_COVERAGE"]


# ============================================================================
# Test Recommendation Functions
# ============================================================================


class TestRecommendations:
    """Test recommendation helper functions"""

    def test_recommend_guides_for_production_project(self, temp_project, mock_system_context):
        """Test guide recommendations for production project"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        wizard.answer_context.set("project_maturity", "production")
        wizard.answer_context.set("security_stance", "high")
        wizard.answer_context.set("project_purpose", ["backend", "microservice"])

        guides = wizard._recommend_guides_for_project()

        assert "cco-verification-protocol" in guides
        assert "cco-security-response" in guides
        assert "cco-performance-optimization" in guides

    def test_recommend_guides_for_team_project(self, temp_project, mock_system_context):
        """Test guide recommendations for team project"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        wizard.answer_context.set("team_dynamics", "small-2-5")
        wizard.answer_context.set("git_workflow", "github_flow")

        guides = wizard._recommend_guides_for_project()

        assert "cco-verification-protocol" in guides
        assert "cco-git-workflow" in guides

    def test_recommend_skills_for_project(self, temp_project, mock_system_context):
        """Test skill recommendations"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        skills = wizard._recommend_skills_for_project()

        # Universal skills should always be included
        assert "cco-skill-verification-protocol" in skills
        assert "cco-skill-test-first-verification" in skills
        assert "cco-skill-root-cause-analysis" in skills
        assert "cco-skill-incremental-improvement" in skills
        assert "cco-skill-security-emergency-response" in skills

    def test_recommend_agents_for_project(self, temp_project, mock_system_context):
        """Test agent recommendations"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        agents = wizard._recommend_agents_for_project()

        # Universal agents should always be included
        assert "cco-agent-audit" in agents
        assert "cco-agent-fix" in agents
        assert "cco-agent-generate" in agents


# ============================================================================
# Test Export Questions
# ============================================================================


class TestExportQuestions:
    """Test export_questions functionality"""

    @patch("claudecodeoptimizer.wizard.decision_tree.get_all_decisions")
    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    def test_export_questions_success(
        self,
        mock_detector_class,
        mock_sys_detector_class,
        mock_get_decisions,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test exporting questions for Claude Code UI"""
        wizard = CCOWizard(temp_project, mode="interactive")

        # Setup mocks
        mock_sys_detector = Mock()
        mock_sys_detector.detect_all.return_value = mock_system_context
        mock_sys_detector.enrich_with_project_detection.return_value = mock_system_context
        mock_sys_detector_class.return_value = mock_sys_detector

        mock_detector = Mock()
        mock_analysis = Mock()
        mock_analysis.dict.return_value = mock_detection_report
        mock_detector.analyze.return_value = mock_analysis
        mock_detector_class.return_value = mock_detector

        # Create a proper mock decision point
        mock_decision = Mock(spec=DecisionPoint)
        mock_decision.id = "test_decision"
        mock_decision.tier = 1
        mock_decision.category = "fundamentals"
        mock_decision.question = "Test question"
        mock_decision.multi_select = False
        mock_decision.why_this_question = "For testing"
        mock_decision.options = [
            Mock(value="cli_tool", label="CLI Tool", description="Command-line interface"),
        ]
        mock_decision.should_ask.return_value = True
        mock_decision.get_recommended_option.return_value = "cli_tool"
        mock_decision.get_ai_hint.return_value = "Recommended for your project"
        mock_get_decisions.return_value = [mock_decision]

        result = wizard.export_questions()

        assert "questions" in result
        assert "system_context" in result
        assert "project_detection" in result
        assert len(result["questions"]) == 1

        question = result["questions"][0]
        assert question["id"] == "test_decision"
        assert question["tier"] == 1
        assert question["category"] == "fundamentals"
        assert question["ai_recommendation"] == "cli_tool"

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    def test_export_questions_system_detection_failed(self, mock_sys_detector_class, temp_project):
        """Test export_questions when system detection fails"""
        wizard = CCOWizard(temp_project, mode="interactive")

        mock_sys_detector = Mock()
        mock_sys_detector.detect_all.side_effect = Exception("Detection failed")
        mock_sys_detector_class.return_value = mock_sys_detector

        result = wizard.export_questions()

        assert "error" in result
        assert result["error"] == "System detection failed"


# ============================================================================
# Test Run with Answers
# ============================================================================


class TestRunWithAnswers:
    """Test run_with_answers functionality"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_command_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_file_generation")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_completion")
    def test_run_with_answers_success(
        self,
        mock_show_completion,
        mock_file_gen,
        mock_cmd_sel,
        mock_prin_sel,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test running wizard with pre-collected answers"""
        wizard = CCOWizard(temp_project, mode="interactive", dry_run=False)
        wizard.system_context = mock_system_context
        wizard.detection_report = mock_detection_report

        # Setup mocks
        mock_prin_sel.return_value = True
        mock_cmd_sel.return_value = True
        mock_file_gen.return_value = True

        answers = {
            "project_purpose": ["cli_tool"],
            "team_dynamics": "solo",
            "project_maturity": "active-dev",
        }

        result = wizard.run_with_answers(answers)

        assert result.success is True
        assert result.mode == "interactive"
        assert "project_purpose" in result.answers

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    def test_run_with_answers_system_detection_needed(self, mock_sys_detect, temp_project):
        """Test run_with_answers when system detection is needed"""
        wizard = CCOWizard(temp_project, mode="interactive")
        # Don't set system_context - it should auto-detect

        mock_sys_detect.return_value = False

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "System detection failed" in result.error

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    def test_run_with_answers_principle_selection_failed(
        self, mock_prin_sel, temp_project, mock_system_context, mock_detection_report
    ):
        """Test run_with_answers when principle selection fails"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        wizard.detection_report = mock_detection_report

        mock_prin_sel.return_value = False

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "Principle selection failed" in result.error


# ============================================================================
# Test Uninitialize
# ============================================================================


class TestUninitialize:
    """Test uninitialize functionality"""

    def test_uninitialize_success(self, temp_project):
        """Test successful uninitialize"""
        # Create CCO structure
        claude_dir = temp_project / ".claude"
        (claude_dir / "commands").mkdir(parents=True)
        (claude_dir / "principles").mkdir(parents=True)
        (claude_dir / "commands" / "cco-init.md").touch()
        (claude_dir / "principles" / "U_DRY.md").touch()
        (temp_project / "CLAUDE.md").write_text(
            "# CLAUDE\n<!-- CCO_SECTION -->\nstuff\n<!-- /CCO_SECTION -->"
        )
        (temp_project / ".gitignore").write_text("# CCO:\n.claude/commands/*\n")

        result = CCOWizard.uninitialize(temp_project)

        assert result["success"] is True
        assert "files_removed" in result
        assert len(result["files_removed"]) > 0

    def test_uninitialize_empty_project(self, temp_project):
        """Test uninitialize on project without CCO"""
        result = CCOWizard.uninitialize(temp_project)

        assert result["success"] is True
        assert result["files_removed"] == []

    def test_uninitialize_exception(self, temp_project):
        """Test uninitialize with exception"""
        # Make directory non-writable to trigger exception
        with patch("pathlib.Path.exists", side_effect=Exception("Access denied")):
            result = CCOWizard.uninitialize(temp_project)

        assert result["success"] is False
        assert "error" in result


# ============================================================================
# Test Complete Wizard Run
# ============================================================================


class TestCompleteWizardRun:
    """Test complete wizard execution flow"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_project_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_decision_tree")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_command_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_file_generation")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_completion")
    def test_run_quick_mode_success(
        self,
        mock_show_completion,
        mock_file_gen,
        mock_cmd_sel,
        mock_prin_sel,
        mock_decision_tree,
        mock_proj_detect,
        mock_sys_detect,
        mock_welcome,
        temp_project,
        mock_system_context,
    ):
        """Test successful complete wizard run in quick mode"""
        wizard = CCOWizard(temp_project, mode="quick", dry_run=False)
        wizard.system_context = mock_system_context

        # Setup all mocks to succeed
        mock_sys_detect.return_value = True
        mock_proj_detect.return_value = True
        mock_decision_tree.return_value = True
        mock_prin_sel.return_value = True
        mock_cmd_sel.return_value = True
        mock_file_gen.return_value = True

        # Initialize answer_context for test
        wizard.answer_context = AnswerContext(system=mock_system_context)

        result = wizard.run()

        assert result.success is True
        assert result.mode == "quick"
        mock_welcome.assert_called_once()
        mock_sys_detect.assert_called_once()
        mock_proj_detect.assert_called_once()
        mock_decision_tree.assert_called_once()
        mock_prin_sel.assert_called_once()
        mock_cmd_sel.assert_called_once()
        mock_file_gen.assert_called_once()
        mock_show_completion.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    def test_run_system_detection_failure(
        self, mock_sys_detect, mock_welcome, temp_project, mock_system_context
    ):
        """Test wizard run with system detection failure"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_sys_detect.return_value = False

        result = wizard.run()

        assert result.success is False
        assert result.error == "System detection failed"

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_project_detection")
    def test_run_project_detection_failure(
        self, mock_proj_detect, mock_sys_detect, mock_welcome, temp_project, mock_system_context
    ):
        """Test wizard run with project detection failure"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_sys_detect.return_value = True
        mock_proj_detect.return_value = False

        result = wizard.run()

        assert result.success is False
        assert result.error == "Project detection failed"

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    def test_run_keyboard_interrupt(
        self, mock_sys_detect, mock_welcome, temp_project, mock_system_context
    ):
        """Test wizard run with KeyboardInterrupt"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_sys_detect.side_effect = KeyboardInterrupt()

        result = wizard.run()

        assert result.success is False
        assert result.error == "Cancelled by user"

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    def test_run_unexpected_exception(
        self, mock_sys_detect, mock_welcome, temp_project, mock_system_context
    ):
        """Test wizard run with unexpected exception"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context

        mock_sys_detect.side_effect = Exception("Unexpected error")

        result = wizard.run()

        assert result.success is False
        assert "Unexpected error" in result.error

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._show_welcome")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_project_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_decision_tree")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_command_selection")
    def test_run_dry_run_mode(
        self,
        mock_cmd_sel,
        mock_prin_sel,
        mock_decision_tree,
        mock_proj_detect,
        mock_sys_detect,
        mock_welcome,
        temp_project,
        mock_system_context,
    ):
        """Test wizard run in dry-run mode (no file generation)"""
        wizard = CCOWizard(temp_project, mode="quick", dry_run=True)
        wizard.system_context = mock_system_context

        # Setup mocks
        mock_sys_detect.return_value = True
        mock_proj_detect.return_value = True
        mock_decision_tree.return_value = True
        mock_prin_sel.return_value = True
        mock_cmd_sel.return_value = True

        wizard.answer_context = AnswerContext(system=mock_system_context)

        with patch.object(wizard, "_run_file_generation") as mock_file_gen:
            result = wizard.run()

            # File generation should NOT be called in dry-run mode
            mock_file_gen.assert_not_called()

        assert result.success is True


# ============================================================================
# Test Convenience Functions
# ============================================================================


class TestConvenienceFunctions:
    """Test convenience wrapper functions"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_run_interactive_wizard(self, mock_wizard_class, temp_project):
        """Test run_interactive_wizard convenience function"""
        mock_wizard = Mock()
        mock_wizard.run.return_value = WizardResult(
            success=True,
            mode="interactive",
            system_context=Mock(),
            answers={},
        )
        mock_wizard_class.return_value = mock_wizard

        result = run_interactive_wizard(temp_project, dry_run=True)

        mock_wizard_class.assert_called_once_with(temp_project, mode="interactive", dry_run=True)
        assert result.success is True

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_run_quick_wizard(self, mock_wizard_class, temp_project):
        """Test run_quick_wizard convenience function"""
        mock_wizard = Mock()
        mock_wizard.run.return_value = WizardResult(
            success=True,
            mode="quick",
            system_context=Mock(),
            answers={},
        )
        mock_wizard_class.return_value = mock_wizard

        result = run_quick_wizard(temp_project, dry_run=False)

        mock_wizard_class.assert_called_once_with(temp_project, mode="quick", dry_run=False)
        assert result.success is True


# ============================================================================
# Test Show Welcome and Completion
# ============================================================================


class TestDisplayMethods:
    """Test display methods"""

    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_header")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_info")
    @patch("claudecodeoptimizer.wizard.orchestrator.pause")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._ensure_global_knowledge_base")
    def test_show_welcome_interactive(
        self,
        mock_ensure_kb,
        mock_pause,
        mock_print_info,
        mock_print_header,
        mock_clear,
        temp_project,
    ):
        """Test showing welcome message in interactive mode"""
        wizard = CCOWizard(temp_project, mode="interactive")

        wizard._show_welcome()

        mock_clear.assert_called_once()
        mock_print_header.assert_called_once()
        mock_pause.assert_called_once()
        mock_ensure_kb.assert_called_once()

    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_header")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._ensure_global_knowledge_base")
    def test_show_welcome_quick(self, mock_ensure_kb, mock_print_header, mock_clear, temp_project):
        """Test showing welcome message in quick mode (no pause)"""
        wizard = CCOWizard(temp_project, mode="quick")

        with patch("claudecodeoptimizer.wizard.orchestrator.pause") as mock_pause:
            wizard._show_welcome()

            # Quick mode should not pause
            mock_pause.assert_not_called()

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_info")
    def test_ensure_global_knowledge_base_new(self, mock_print_info, mock_setup, temp_project):
        """Test ensuring global knowledge base when new setup is needed"""
        wizard = CCOWizard(temp_project, mode="quick")

        mock_setup.return_value = {
            "actions": ["Created ~/.cco/", "Downloaded principles"],
        }

        wizard._ensure_global_knowledge_base()

        mock_setup.assert_called_once_with(force=False)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    def test_ensure_global_knowledge_base_existing(self, mock_setup, temp_project):
        """Test ensuring global knowledge base when already exists"""
        wizard = CCOWizard(temp_project, mode="quick")

        mock_setup.return_value = {
            "actions": ["Knowledge base already up to date"],
        }

        with patch("claudecodeoptimizer.wizard.orchestrator.print_info") as mock_print:
            wizard._ensure_global_knowledge_base()

            # Should not print anything for "already up to date"
            mock_print.assert_not_called()

    @patch("claudecodeoptimizer.wizard.orchestrator.print_header")
    @patch("claudecodeoptimizer.wizard.orchestrator.display_completion_summary")
    def test_show_completion(self, mock_display_summary, mock_print_header, temp_project):
        """Test showing completion summary"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init", "cco-status"]
        wizard.selected_principles = ["U_DRY"]
        wizard.selected_guides = ["cco-git-workflow"]
        wizard.selected_skills = ["cco-skill-verification-protocol"]
        wizard.selected_agents = ["cco-agent-audit"]

        wizard._show_completion(5.5)

        mock_print_header.assert_called_once()
        mock_display_summary.assert_called_once()


# ============================================================================
# Test Edge Cases and Error Handling
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_wizard_with_missing_system_context(self, temp_project):
        """Test that wizard fails gracefully without system context"""
        wizard = CCOWizard(temp_project, mode="quick")
        # Don't set system_context

        with pytest.raises(AssertionError):
            # This should raise because system_context is required
            wizard._run_decision_tree()

    @patch("claudecodeoptimizer.core.principle_selector.PrincipleSelector")
    def test_wizard_with_missing_answer_context(
        self, mock_selector_class, temp_project, mock_system_context
    ):
        """Test that wizard fails gracefully without answer context"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        # Don't initialize answer_context

        # Mock the selector to avoid ImportError
        mock_selector_class.return_value = Mock()

        # This should fail because answer_context is None
        result = wizard._run_principle_selection()
        # The method will handle the missing answer_context gracefully
        assert result is False

    def test_build_preferences_with_empty_answers(self, temp_project, mock_system_context):
        """Test building preferences with no user answers"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.selected_principles = []

        prefs = wizard._build_preferences()

        # Should use defaults
        assert prefs["project_identity"]["team_trajectory"] == "solo"
        assert prefs["project_identity"]["project_maturity"] == "active-dev"

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    def test_build_selected_principles_dict(self, mock_load_principles, temp_project):
        """Test building selected principles dictionary"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_principles = ["P_TEST_COVERAGE", "P_LINTING_SAST"]

        mock_load_principles.return_value = [
            {"id": "U_DRY", "category": "universal"},
            {"id": "P_TEST_COVERAGE", "category": "testing"},
            {"id": "P_LINTING_SAST", "category": "code_quality"},
        ]

        result = wizard._build_selected_principles_dict()

        assert "universal" in result
        assert "U_DRY" in result["universal"]
        assert "testing" in result
        assert "P_TEST_COVERAGE" in result["testing"]
        assert "code_quality" in result
        assert "P_LINTING_SAST" in result["code_quality"]


# ============================================================================
# Test Export Questions - Additional Coverage
# ============================================================================


class TestExportQuestionsAdditional:
    """Test export_questions edge cases"""

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    def test_export_questions_project_detection_failed(
        self, mock_detector_class, mock_sys_detector_class, temp_project, mock_system_context
    ):
        """Test export_questions when project detection fails"""
        wizard = CCOWizard(temp_project, mode="interactive")

        # System detection succeeds
        mock_sys_detector = Mock()
        mock_sys_detector.detect_all.return_value = mock_system_context
        mock_sys_detector_class.return_value = mock_sys_detector

        # Project detection fails
        mock_detector = Mock()
        mock_detector.analyze.side_effect = Exception("Analysis failed")
        mock_detector_class.return_value = mock_detector

        result = wizard.export_questions()

        assert "error" in result
        assert result["error"] == "Project detection failed"


# ============================================================================
# Test Run with Answers - Additional Coverage
# ============================================================================


class TestRunWithAnswersAdditional:
    """Test run_with_answers edge cases"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_system_detection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_project_detection")
    def test_run_with_answers_project_detection_needed(
        self, mock_proj_detect, mock_sys_detect, temp_project, mock_system_context
    ):
        """Test run_with_answers when project detection is needed"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        # Don't set detection_report - it should auto-detect

        mock_sys_detect.return_value = True
        mock_proj_detect.return_value = False

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "Project detection failed" in result.error

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_command_selection")
    def test_run_with_answers_command_selection_failed(
        self, mock_cmd_sel, mock_prin_sel, temp_project, mock_system_context, mock_detection_report
    ):
        """Test run_with_answers when command selection fails"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        wizard.detection_report = mock_detection_report

        mock_prin_sel.return_value = True
        mock_cmd_sel.return_value = False

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "Command selection failed" in result.error

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_command_selection")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_file_generation")
    def test_run_with_answers_file_generation_failed(
        self,
        mock_file_gen,
        mock_cmd_sel,
        mock_prin_sel,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test run_with_answers when file generation fails"""
        wizard = CCOWizard(temp_project, mode="interactive", dry_run=False)
        wizard.system_context = mock_system_context
        wizard.detection_report = mock_detection_report

        mock_prin_sel.return_value = True
        mock_cmd_sel.return_value = True
        mock_file_gen.return_value = False

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "File generation failed" in result.error

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._run_principle_selection")
    def test_run_with_answers_exception_handling(
        self, mock_prin_sel, temp_project, mock_system_context, mock_detection_report
    ):
        """Test run_with_answers exception handling"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        wizard.detection_report = mock_detection_report

        mock_prin_sel.side_effect = Exception("Unexpected error")

        result = wizard.run_with_answers({})

        assert result.success is False
        assert "Wizard failed" in result.error
        assert "Unexpected error" in result.error

    def test_run_with_answers_exception_without_system_context(self, temp_project):
        """Test run_with_answers exception handling when system_context is None"""
        wizard = CCOWizard(temp_project, mode="interactive")
        # Don't set system_context - force exception path

        with patch.object(wizard, "_run_system_detection", side_effect=Exception("Test error")):
            result = wizard.run_with_answers({})

        assert result.success is False
        # Should create a minimal SystemContext for error reporting
        assert result.system_context is not None


# ============================================================================
# Test Interactive Mode Decision Execution
# ============================================================================


class TestInteractiveModeDecisions:
    """Test interactive mode decision execution paths"""

    @patch("claudecodeoptimizer.wizard.orchestrator.get_all_decisions")
    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_header")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_info")
    def test_ask_user_decision_tier1(
        self,
        mock_print_info,
        mock_print_header,
        mock_clear,
        mock_get_decisions,
        temp_project,
        mock_system_context,
        mock_decision_point,
    ):
        """Test asking user for Tier 1 decision in interactive mode"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Mock UI adapter to return answer
        with patch.object(wizard.ui_adapter, "ask_decision", return_value="cli_tool"):
            answer = wizard._ask_user_decision(mock_decision_point)

        assert answer == "cli_tool"
        # In terminal mode, should show tier header
        if wizard.ui_adapter.mode == "terminal":
            mock_clear.assert_called()
            mock_print_header.assert_called()

    @patch("claudecodeoptimizer.wizard.orchestrator.get_all_decisions")
    def test_execute_decision_error_handling(
        self, mock_get_decisions, temp_project, mock_system_context
    ):
        """Test decision execution error handling"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Create decision that will fail
        mock_decision = Mock()
        mock_decision.id = "failing_decision"
        mock_decision.question = "This will fail"
        mock_decision.should_ask.return_value = True
        mock_decision.get_recommended_option.side_effect = Exception("Decision failed")

        mock_get_decisions.return_value = [mock_decision]

        with patch("claudecodeoptimizer.wizard.orchestrator.print_error"):
            result = wizard._run_decision_tree()

        assert result is False


# ============================================================================
# Test Interactive Mode File Generation
# ============================================================================


class TestInteractiveModeFileGeneration:
    """Test interactive mode file generation paths"""

    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._setup_knowledge_symlinks")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._update_gitignore")
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard._generate_claude_md")
    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_header")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_success")
    def test_run_file_generation_interactive_mode(
        self,
        mock_print_success,
        mock_print_header,
        mock_clear,
        mock_generate_md,
        mock_update_gitignore,
        mock_setup_symlinks,
        temp_project,
    ):
        """Test file generation in interactive mode with UI feedback"""
        wizard = CCOWizard(temp_project, mode="interactive", dry_run=False)

        result = wizard._run_file_generation()

        assert result is True
        mock_clear.assert_called_once()
        mock_print_header.assert_called_once()
        assert mock_print_success.call_count >= 3  # Three success messages


# ============================================================================
# Test Uninitialize Edge Cases
# ============================================================================


class TestUninitializeAdditional:
    """Test additional uninitialize scenarios"""

    def test_uninitialize_with_nested_directories(self, temp_project):
        """Test uninitialize with nested language-specific directories"""
        # Create CCO structure with nested dirs (e.g., skills/python/)
        claude_dir = temp_project / ".claude"
        (claude_dir / "skills" / "python").mkdir(parents=True)
        (claude_dir / "skills" / "python" / "async-patterns.md").write_text("test")

        result = CCOWizard.uninitialize(temp_project)

        assert result["success"] is True
        assert not (claude_dir / "skills" / "python").exists()

    def test_uninitialize_preserves_non_cco_gitignore_content(self, temp_project):
        """Test that uninitialize preserves non-CCO .gitignore content"""
        gitignore_path = temp_project / ".gitignore"
        gitignore_path.write_text(
            "# Custom section\n*.pyc\n\n# CCO: Symlinked knowledge base\n.claude/commands/*\n\n# More custom\n__pycache__/\n"
        )

        result = CCOWizard.uninitialize(temp_project)

        content = gitignore_path.read_text()
        assert "*.pyc" in content
        assert "__pycache__/" in content
        assert "# CCO:" not in content


# ============================================================================
# Test Recommendation Logic Edge Cases
# ============================================================================


class TestRecommendationEdgeCases:
    """Test edge cases in recommendation logic"""

    def test_recommend_guides_various_project_types(self, temp_project, mock_system_context):
        """Test guide recommendations for various project types"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        # Backend microservice with high security
        wizard.answer_context.set("project_purpose", ["backend", "microservice"])
        wizard.answer_context.set("security_stance", "production")
        wizard.answer_context.set("project_maturity", "production")

        guides = wizard._recommend_guides_for_project()

        assert "cco-security-response" in guides
        assert "cco-performance-optimization" in guides
        assert "cco-container-best-practices" in guides

    def test_recommend_guides_with_retry_logic(self, temp_project, mock_system_context):
        """Test guide recommendations for retry/resilience patterns"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)

        wizard.answer_context.set("error_handling", "retry_logic")

        guides = wizard._recommend_guides_for_project()

        assert "cco-performance-optimization" in guides

    def test_recommend_skills_with_detected_languages(self, temp_project):
        """Test skill recommendations with language detection"""
        wizard = CCOWizard(temp_project, mode="quick")

        # Create system context with Python detected
        mock_ctx = SystemContext(
            os_type="linux",
            os_version="5.15.0",
            os_platform="x86_64",
            shell_type="bash",
            terminal_emulator="gnome-terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US.UTF-8",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11.0",
            python_executable="/usr/bin/python3",
            pip_version="23.0",
            git_installed=True,
            is_git_repo=True,
            project_root=Path("/tmp/test"),
        )
        # Add detected_languages attribute
        mock_ctx.detected_languages = ["Python", "JavaScript"]
        wizard.system_context = mock_ctx

        skills = wizard._recommend_skills_for_project()

        # Should include universal skills
        assert "cco-skill-verification-protocol" in skills
        assert "cco-skill-test-first-verification" in skills
        # Should include Python-specific skills
        assert "python/cco-skill-async-patterns" in skills
        assert "python/cco-skill-type-hints-advanced" in skills


# ============================================================================
# Test Error Injection in CLAUDE.md
# ============================================================================


class TestInjectKnowledgeReferences:
    """Test knowledge reference injection"""

    def test_inject_knowledge_references_with_error_handling(
        self, temp_project, mock_system_context
    ):
        """Test injecting error handling strategy into CLAUDE.md"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.answer_context.set("error_handling", "fail_fast")
        wizard.selected_principles = ["U_FAIL_FAST"]
        wizard.selected_guides = []
        wizard.selected_skills = []

        content = "# CLAUDE\n\n---\n\n*Part of CCO Documentation System*"
        result = wizard._inject_knowledge_references(content)

        assert "Fail-Fast" in result
        assert "U_FAIL_FAST" in result

    def test_inject_knowledge_references_with_guides(self, temp_project, mock_system_context):
        """Test injecting guides into CLAUDE.md"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.selected_principles = []
        wizard.selected_guides = ["cco-git-workflow", "cco-security-response"]
        wizard.selected_skills = []
        wizard.selected_agents = []

        content = "# CLAUDE\n\n---\n\n*Part of CCO Documentation System*"
        result = wizard._inject_knowledge_references(content)

        assert "cco-git-workflow.md" in result
        assert "cco-security-response.md" in result

    def test_inject_knowledge_references_with_skills_and_agents(
        self, temp_project, mock_system_context
    ):
        """Test injecting skills and agents into CLAUDE.md"""
        wizard = CCOWizard(temp_project, mode="quick")
        wizard.system_context = mock_system_context
        wizard.answer_context = AnswerContext(system=mock_system_context)
        wizard.selected_principles = []
        wizard.selected_guides = []
        wizard.selected_skills = ["cco-skill-verification-protocol"]
        wizard.selected_agents = ["cco-agent-audit"]

        content = "# CLAUDE\n\n---\n\n*Part of CCO Documentation System*"
        result = wizard._inject_knowledge_references(content)

        assert "cco-verification-protocol" in result or "cco-skill-verification-protocol" in result
        assert "cco-agent-audit" in result


# ============================================================================
# Test Ensure Global Knowledge Base
# ============================================================================


class TestEnsureGlobalKnowledgeBase:
    """Test global knowledge base setup"""

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.wizard.orchestrator.print_warning")
    def test_ensure_global_knowledge_base_exception(
        self, mock_print_warning, mock_setup, temp_project
    ):
        """Test handling exception during global knowledge base setup"""
        wizard = CCOWizard(temp_project, mode="quick")

        mock_setup.side_effect = Exception("Setup failed")

        # Should not raise, but print warning
        wizard._ensure_global_knowledge_base()

        mock_print_warning.assert_called_once()


# ============================================================================
# Test Project Detection Interactive Mode
# ============================================================================


class TestProjectDetectionInteractive:
    """Test project detection in interactive mode"""

    @patch("claudecodeoptimizer.wizard.orchestrator.SystemDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.UniversalDetector")
    @patch("claudecodeoptimizer.wizard.orchestrator.display_detection_results")
    @patch("claudecodeoptimizer.wizard.orchestrator.clear_screen")
    @patch("claudecodeoptimizer.wizard.renderer.ask_yes_no")
    def test_confirm_analysis_cancelled(
        self,
        mock_ask_yes_no,
        mock_clear,
        mock_display,
        mock_detector_class,
        mock_sys_detector_class,
        temp_project,
        mock_system_context,
        mock_detection_report,
    ):
        """Test user cancelling analysis confirmation"""
        wizard = CCOWizard(temp_project, mode="interactive")
        wizard.system_context = mock_system_context

        mock_detector = Mock()
        mock_analysis = Mock()
        mock_analysis.dict.return_value = mock_detection_report
        mock_detector.analyze.return_value = mock_analysis
        mock_detector_class.return_value = mock_detector

        mock_sys_detector = Mock()
        mock_sys_detector.enrich_with_project_detection.return_value = mock_system_context
        mock_sys_detector_class.return_value = mock_sys_detector

        # User cancels
        mock_ask_yes_no.return_value = False

        result = wizard._run_project_detection()

        assert result is False


# ============================================================================
# Test Symlink Creation Edge Cases
# ============================================================================


class TestSymlinkCreation:
    """Test symlink/hardlink/copy fallback logic"""

    @patch("platform.system")
    @patch("subprocess.run")
    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_setup_knowledge_symlinks_windows_success(
        self,
        mock_get_skills,
        mock_get_agents,
        mock_get_principles,
        mock_get_guides,
        mock_get_commands,
        mock_setup_global,
        mock_subprocess_run,
        mock_platform_system,
        temp_project,
    ):
        """Test symlink creation on Windows with mklink success"""
        mock_platform_system.return_value = "Windows"
        mock_subprocess_run.return_value = Mock(returncode=0)

        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init"]
        wizard.selected_guides = []
        wizard.selected_principles = []
        wizard.selected_agents = []
        wizard.selected_skills = []

        # Setup mock directories
        mock_commands_dir = temp_project / "mock_commands"
        mock_commands_dir.mkdir()
        (mock_commands_dir / "cco-init.md").write_text("test")

        mock_get_commands.return_value = mock_commands_dir
        mock_get_guides.return_value = temp_project / "mock_guides"
        mock_get_principles.return_value = temp_project / "mock_principles"
        mock_get_agents.return_value = temp_project / "mock_agents"
        mock_get_skills.return_value = temp_project / "mock_skills"

        wizard._setup_knowledge_symlinks()

        # Should have called mklink
        assert mock_subprocess_run.called

    @patch("platform.system")
    @patch("subprocess.run")
    @patch("os.link")
    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_setup_knowledge_symlinks_windows_fallback_to_hardlink(
        self,
        mock_get_skills,
        mock_get_agents,
        mock_get_principles,
        mock_get_guides,
        mock_get_commands,
        mock_setup_global,
        mock_os_link,
        mock_subprocess_run,
        mock_platform_system,
        temp_project,
    ):
        """Test fallback to hardlink when Windows mklink fails"""
        mock_platform_system.return_value = "Windows"
        # mklink fails
        import subprocess

        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd")

        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init"]
        wizard.selected_guides = []
        wizard.selected_principles = []
        wizard.selected_agents = []
        wizard.selected_skills = []

        # Setup mock directories
        mock_commands_dir = temp_project / "mock_commands"
        mock_commands_dir.mkdir()
        (mock_commands_dir / "cco-init.md").write_text("test")

        mock_get_commands.return_value = mock_commands_dir
        mock_get_guides.return_value = temp_project / "mock_guides"
        mock_get_principles.return_value = temp_project / "mock_principles"
        mock_get_agents.return_value = temp_project / "mock_agents"
        mock_get_skills.return_value = temp_project / "mock_skills"

        wizard._setup_knowledge_symlinks()

        # Should have tried hardlink
        assert mock_os_link.called

    @patch("platform.system")
    @patch("subprocess.run")
    @patch("os.link")
    @patch("shutil.copy2")
    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_setup_knowledge_symlinks_fallback_to_copy(
        self,
        mock_get_skills,
        mock_get_agents,
        mock_get_principles,
        mock_get_guides,
        mock_get_commands,
        mock_setup_global,
        mock_shutil_copy2,
        mock_os_link,
        mock_subprocess_run,
        mock_platform_system,
        temp_project,
    ):
        """Test fallback to copy when both symlink and hardlink fail"""
        mock_platform_system.return_value = "Windows"
        # mklink fails
        import subprocess

        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        # hardlink fails
        mock_os_link.side_effect = OSError("Hardlink not supported")

        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init"]
        wizard.selected_guides = []
        wizard.selected_principles = []
        wizard.selected_agents = []
        wizard.selected_skills = []

        # Setup mock directories
        mock_commands_dir = temp_project / "mock_commands"
        mock_commands_dir.mkdir()
        (mock_commands_dir / "cco-init.md").write_text("test")

        mock_get_commands.return_value = mock_commands_dir
        mock_get_guides.return_value = temp_project / "mock_guides"
        mock_get_principles.return_value = temp_project / "mock_principles"
        mock_get_agents.return_value = temp_project / "mock_agents"
        mock_get_skills.return_value = temp_project / "mock_skills"

        wizard._setup_knowledge_symlinks()

        # Should have fallen back to copy
        assert mock_shutil_copy2.called

    @patch("platform.system")
    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_setup_knowledge_symlinks_unix_success(
        self,
        mock_get_skills,
        mock_get_agents,
        mock_get_principles,
        mock_get_guides,
        mock_get_commands,
        mock_setup_global,
        mock_platform_system,
        temp_project,
    ):
        """Test symlink creation on Unix systems"""
        mock_platform_system.return_value = "Linux"

        wizard = CCOWizard(temp_project, mode="quick")
        wizard.selected_commands = ["cco-init"]
        wizard.selected_guides = []
        wizard.selected_principles = []
        wizard.selected_agents = []
        wizard.selected_skills = []

        # Setup mock directories
        mock_commands_dir = temp_project / "mock_commands"
        mock_commands_dir.mkdir()
        (mock_commands_dir / "cco-init.md").write_text("test")

        mock_get_commands.return_value = mock_commands_dir
        mock_get_guides.return_value = temp_project / "mock_guides"
        mock_get_principles.return_value = temp_project / "mock_principles"
        mock_get_agents.return_value = temp_project / "mock_agents"
        mock_get_skills.return_value = temp_project / "mock_skills"

        wizard._setup_knowledge_symlinks()

        # Check symlink was created
        target = temp_project / ".claude" / "commands" / "cco-init.md"
        assert target.exists()
