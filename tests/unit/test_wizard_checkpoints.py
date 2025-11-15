"""
Comprehensive tests for wizard checkpoints module.

Tests cover:
- Display detection results
- Display recommendations
- Display command selection
- Display preview
- Confirmation dialogs
- Completion summary
- Error and cancellation displays
"""

from typing import Any, Dict
from unittest.mock import patch

import pytest

from claudecodeoptimizer.wizard.checkpoints import (
    confirm_action,
    confirm_apply,
    confirm_commands,
    confirm_detection,
    confirm_recommendations,
    display_cancelled,
    display_command_selection,
    display_completion_summary,
    display_detection_results,
    display_error,
    display_preview,
    display_recommendations,
)


class TestDisplayDetectionResults:
    """Test display_detection_results function"""

    @pytest.fixture
    def minimal_report(self) -> Dict[str, Any]:
        """Minimal detection report"""
        return {
            "languages": [],
            "frameworks": [],
            "project_types": [],
            "tools": [],
            "codebase_patterns": {},
        }

    @pytest.fixture
    def full_report(self) -> Dict[str, Any]:
        """Full detection report with all sections"""
        return {
            "languages": [
                {
                    "detected_value": "python",
                    "confidence": 0.95,
                    "evidence": ["*.py files", "requirements.txt"],
                },
                {
                    "detected_value": "javascript",
                    "confidence": 0.75,
                    "evidence": ["*.js files", "package.json"],
                },
            ],
            "frameworks": [
                {
                    "detected_value": "fastapi",
                    "confidence": 0.85,
                    "evidence": ["from fastapi import", "FastAPI app"],
                }
            ],
            "project_types": [
                {"detected_value": "api_service", "confidence": 0.90},
                {"detected_value": "web_app", "confidence": 0.70},
            ],
            "tools": [
                {"detected_value": "pytest", "category": "testing"},
                {"detected_value": "ruff", "category": "linting"},
            ],
            "codebase_patterns": {
                "total_files": 150,
                "total_lines": 5000,
                "project_root": "/home/user/project",
                "file_distribution": {".py": 100, ".js": 30, ".md": 10},
            },
        }

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_section")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_warning")
    def test_display_empty_report(self, mock_warning, mock_section, mock_header, minimal_report):
        """Test displaying report with no detections"""
        display_detection_results(minimal_report)

        # Should call header
        mock_header.assert_called_once()

        # Should call sections
        assert mock_section.call_count >= 3

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_table")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_list")
    def test_display_full_report(self, mock_list, mock_table, mock_header, full_report):
        """Test displaying complete report"""
        display_detection_results(full_report)

        # Should display header
        mock_header.assert_called_once()

        # Should display tables for languages and frameworks
        assert mock_table.call_count >= 2

        # Should display lists for project types
        mock_list.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_table")
    def test_display_languages_table(self, mock_table, full_report):
        """Test language table display"""
        display_detection_results(full_report)

        # Check that table was called with language data
        calls = mock_table.call_args_list
        # At least one call should be for languages
        assert any("python" in str(call) or "Language" in str(call) for call in calls)

    @patch("claudecodeoptimizer.wizard.checkpoints.print_key_value")
    def test_display_codebase_stats(self, mock_key_value, full_report):
        """Test codebase statistics display"""
        display_detection_results(full_report)

        # Should display total files, lines, and root
        mock_key_value.assert_called()


class TestDisplayRecommendations:
    """Test display_recommendations function"""

    @pytest.fixture
    def sample_recommendations(self) -> Dict[str, Any]:
        """Sample recommendations"""
        return {
            "project_identity": {
                "project_name": "MyProject",
                "project_types": ["api_service", "web_app"],
            },
            "development_style": {
                "team_size": "solo",
                "philosophy": "balanced",
            },
            "code_quality": {
                "linting": "strict",
                "type_checking": "enabled",
            },
            "security_recs": [
                {"priority": "high", "recommendation": "Enable HTTPS"},
                {"priority": "medium", "recommendation": "Add input validation"},
            ],
            "performance_recs": [
                {"recommendation": "Enable caching"},
                {"recommendation": "Optimize database queries"},
            ],
        }

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_section")
    def test_display_recommendations_structure(
        self, mock_section, mock_header, sample_recommendations
    ):
        """Test recommendations display structure"""
        display_recommendations(sample_recommendations)

        # Should display header
        mock_header.assert_called_once()

        # Should display multiple sections
        assert mock_section.call_count >= 4

    @patch("claudecodeoptimizer.wizard.checkpoints.print_key_value")
    def test_display_identity_recommendations(self, mock_key_value, sample_recommendations):
        """Test project identity recommendations display"""
        display_recommendations(sample_recommendations)

        # Should display identity values
        mock_key_value.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_security_recommendations(self, mock_info, sample_recommendations):
        """Test security recommendations display"""
        display_recommendations(sample_recommendations)

        # Should display security recommendations
        mock_info.assert_called()


class TestDisplayCommandSelection:
    """Test display_command_selection function"""

    @pytest.fixture
    def command_data(self) -> tuple:
        """Sample command selection data"""
        core = ["cco-status", "cco-init", "cco-config"]
        recommended = ["cco-test", "cco-audit-code-quality"]
        optional = ["cco-generate-docs", "cco-setup-cicd"]
        selected = core + recommended + ["cco-generate-docs"]
        reasoning = {
            "cco-status": "Essential health check",
            "cco-test": "Automated testing",
        }
        return core, recommended, optional, selected, reasoning

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_section")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_command_selection_structure(
        self, mock_box, mock_section, mock_header, command_data
    ):
        """Test command selection display structure"""
        core, recommended, optional, selected, reasoning = command_data

        display_command_selection(core, recommended, optional, selected, reasoning)

        # Should display header
        mock_header.assert_called_once()

        # Should display sections for core, recommended, optional
        assert mock_section.call_count >= 2

        # Should display summary box
        mock_box.assert_called_once()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_core_commands(self, mock_success, command_data):
        """Test core commands display"""
        core, recommended, optional, selected, reasoning = command_data

        display_command_selection(core, recommended, optional, selected, reasoning)

        # Should display all core commands
        calls = [str(call) for call in mock_success.call_args_list]
        assert any("cco-status" in call for call in calls)

    def test_display_command_counts(self, command_data):
        """Test command count calculation"""
        core, recommended, optional, selected, reasoning = command_data

        # Verify counts
        assert len(core) == 3
        assert len(recommended) == 2
        assert len(selected) == 6  # core + recommended + 1 optional


class TestDisplayPreview:
    """Test display_preview function"""

    @pytest.fixture
    def sample_changes(self) -> Dict[str, Any]:
        """Sample changes to preview"""
        return {
            "files_to_create": {
                "principles": [".claude/principles/U_DRY.md"],
                "commands": [".claude/commands/cco-status.md"],
            },
            "files_to_modify": [".claude/config.json"],
            "files_to_delete": [],
            "commands_to_install": [
                {"id": "cco-status", "category": "health"},
                {"id": "cco-test", "category": "testing"},
            ],
            "permissions_configured": {
                "bash_commands_count": 5,
                "glob_patterns_count": 3,
                "read_paths_count": 10,
                "write_paths_count": 2,
            },
            "principles_selected": [
                {"name": "U_DRY"},
                {"name": "U_TEST_FIRST"},
            ],
        }

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_section")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_preview_structure(self, mock_box, mock_section, mock_header, sample_changes):
        """Test preview display structure"""
        display_preview(sample_changes, dry_run=False)

        # Should display header
        mock_header.assert_called_once()

        # Should display sections
        assert mock_section.call_count >= 3

        # Should display summary box
        mock_box.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    def test_display_preview_dry_run_mode(self, mock_header, sample_changes):
        """Test preview in dry-run mode"""
        display_preview(sample_changes, dry_run=True)

        # Header should indicate dry-run mode
        call_args = str(mock_header.call_args)
        assert "dry" in call_args.lower() or "preview" in call_args.lower()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_files_to_create(self, mock_success, sample_changes):
        """Test display of files to create"""
        display_preview(sample_changes)

        # Should display CREATE messages
        calls = [str(call) for call in mock_success.call_args_list]
        assert any("CREATE" in call for call in calls)

    @patch("claudecodeoptimizer.wizard.checkpoints.print_warning")
    def test_display_files_to_modify(self, mock_warning, sample_changes):
        """Test display of files to modify"""
        display_preview(sample_changes)

        # Should display MODIFY messages
        calls = [str(call) for call in mock_warning.call_args_list]
        assert any("MODIFY" in call for call in calls)


class TestConfirmationFunctions:
    """Test confirmation dialog functions"""

    @patch("claudecodeoptimizer.wizard.checkpoints.ask_yes_no")
    def test_confirm_action_default_false(self, mock_ask):
        """Test confirm_action with default False"""
        mock_ask.return_value = True

        result = confirm_action("Proceed?", default=False)

        mock_ask.assert_called_once_with("Proceed?", default=False)
        assert result is True

    @patch("claudecodeoptimizer.wizard.checkpoints.ask_yes_no")
    def test_confirm_action_default_true(self, mock_ask):
        """Test confirm_action with default True"""
        mock_ask.return_value = False

        result = confirm_action("Continue?", default=True)

        mock_ask.assert_called_once_with("Continue?", default=True)
        assert result is False

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    def test_confirm_detection(self, mock_confirm):
        """Test confirm_detection wrapper"""
        mock_confirm.return_value = True
        report = {}

        result = confirm_detection(report)

        mock_confirm.assert_called_once()
        assert result is True

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    def test_confirm_recommendations(self, mock_confirm):
        """Test confirm_recommendations wrapper"""
        mock_confirm.return_value = True
        recommendations = {}

        result = confirm_recommendations(recommendations)

        mock_confirm.assert_called_once()
        assert result is True

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    def test_confirm_commands(self, mock_confirm):
        """Test confirm_commands wrapper"""
        mock_confirm.return_value = True
        selected = ["cmd1", "cmd2", "cmd3"]

        result = confirm_commands(selected)

        mock_confirm.assert_called_once()
        call_args = str(mock_confirm.call_args)
        assert "3" in call_args  # Should mention count
        assert result is True

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    @patch("claudecodeoptimizer.wizard.checkpoints.pause")
    def test_confirm_apply_dry_run(self, mock_pause, mock_info, mock_confirm):
        """Test confirm_apply in dry-run mode"""
        result = confirm_apply(dry_run=True)

        # Should not ask for confirmation in dry-run
        mock_confirm.assert_not_called()

        # Should display info and pause
        mock_info.assert_called()
        mock_pause.assert_called()

        assert result is True

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    def test_confirm_apply_normal(self, mock_confirm):
        """Test confirm_apply in normal mode"""
        mock_confirm.return_value = False

        result = confirm_apply(dry_run=False)

        mock_confirm.assert_called_once()
        assert result is False


class TestDisplayCompletionSummary:
    """Test display_completion_summary function"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_completion_minimal(self, mock_success, mock_box, mock_header):
        """Test completion summary with minimal items"""
        display_completion_summary(
            commands_installed=5,
            principles_configured=10,
            files_created=15,
            duration_seconds=30.5,
        )

        # Should display header with version
        mock_header.assert_called_once()

        # Should display summary box
        mock_box.assert_called_once()

        # Should display success message
        mock_success.assert_called_once()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_completion_full(self, mock_box):
        """Test completion summary with all optional items"""
        display_completion_summary(
            commands_installed=10,
            principles_configured=15,
            files_created=25,
            duration_seconds=45.2,
            guides_installed=3,
            skills_installed=5,
            agents_installed=2,
        )

        # Get the summary lines passed to print_box
        call_args = mock_box.call_args[0][0]

        # Should include all counts
        summary_text = " ".join(call_args)
        assert "10" in summary_text or "commands" in summary_text
        assert "guides" in summary_text
        assert "skills" in summary_text
        assert "agents" in summary_text

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_completion_omits_zero_optional_items(self, mock_box):
        """Test that zero-count optional items are omitted"""
        display_completion_summary(
            commands_installed=5,
            principles_configured=10,
            files_created=15,
            duration_seconds=30.0,
            guides_installed=0,
            skills_installed=0,
            agents_installed=0,
        )

        call_args = mock_box.call_args[0][0]
        summary_text = " ".join(call_args)

        # Should not mention guides, skills, or agents if count is 0
        assert "0 guides" not in summary_text
        assert "0 skills" not in summary_text
        assert "0 agents" not in summary_text


class TestDisplayError:
    """Test display_error function"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_error_minimal(self, mock_box):
        """Test error display with minimal info"""
        display_error("Something went wrong")

        mock_box.assert_called_once()

        call_args = mock_box.call_args[0][0]
        error_text = " ".join(call_args)

        assert "Something went wrong" in error_text

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_error_with_details(self, mock_box):
        """Test error display with details"""
        display_error("Failed to initialize", details="Permission denied on file X")

        call_args = mock_box.call_args[0][0]
        error_text = " ".join(call_args)

        assert "Failed to initialize" in error_text
        assert "Permission denied" in error_text


class TestDisplayCancelled:
    """Test display_cancelled function"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_cancelled(self, mock_box):
        """Test cancellation message display"""
        display_cancelled()

        mock_box.assert_called_once()

        call_args = mock_box.call_args[0][0]
        message_text = " ".join(call_args)

        assert "cancelled" in message_text.lower()
        assert "no changes" in message_text.lower()


class TestEdgeCases:
    """Test edge cases and unusual inputs"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    def test_display_empty_detection_report(self, mock_header):
        """Test display with completely empty report"""
        display_detection_results({})

        # Should not crash
        mock_header.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    def test_display_empty_recommendations(self, mock_header):
        """Test display with empty recommendations"""
        display_recommendations({})

        # Should not crash
        mock_header.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    def test_display_command_selection_all_empty(self, mock_header):
        """Test command selection with no commands"""
        display_command_selection([], [], [], [], None)

        # Should not crash
        mock_header.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    def test_display_preview_empty_changes(self, mock_header):
        """Test preview with no changes"""
        display_preview({})

        # Should not crash
        mock_header.assert_called()

    def test_completion_summary_zero_duration(self):
        """Test completion summary with zero duration"""
        with patch("claudecodeoptimizer.wizard.checkpoints.print_header"):
            display_completion_summary(
                commands_installed=0,
                principles_configured=0,
                files_created=0,
                duration_seconds=0.0,
            )
        # Should not crash

    @patch("claudecodeoptimizer.wizard.checkpoints.print_box")
    def test_display_error_empty_string(self, mock_box):
        """Test error display with empty error message"""
        display_error("")

        # Should still display something
        mock_box.assert_called()


class TestIntegrationScenarios:
    """Test realistic usage scenarios"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_header")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_table")
    @patch("claudecodeoptimizer.wizard.checkpoints.print_list")
    def test_complete_detection_flow(self, mock_list, mock_table, mock_header):
        """Test complete detection display flow"""
        report = {
            "languages": [{"detected_value": "python", "confidence": 0.95, "evidence": ["*.py"]}],
            "frameworks": [
                {"detected_value": "fastapi", "confidence": 0.85, "evidence": ["fastapi"]}
            ],
            "project_types": [{"detected_value": "api_service", "confidence": 0.90}],
            "tools": [{"detected_value": "pytest", "category": "testing"}],
            "codebase_patterns": {"total_files": 100, "total_lines": 3000},
        }

        display_detection_results(report)

        # All display functions should be called
        mock_header.assert_called()
        mock_table.assert_called()
        mock_list.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.confirm_action")
    def test_complete_confirmation_flow(self, mock_confirm):
        """Test complete confirmation flow"""
        mock_confirm.return_value = True

        # Simulate wizard flow
        assert confirm_detection({}) is True
        assert confirm_recommendations({}) is True
        assert confirm_commands(["cmd1"]) is True
        assert confirm_apply(dry_run=False) is True

        assert mock_confirm.call_count == 4


class TestCoverageGaps:
    """Tests to cover remaining uncovered lines"""

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_security_recs_high_priority(self, mock_info):
        """Test security recommendations with high priority"""
        recommendations = {
            "security_recs": [
                {"priority": "high", "recommendation": "Enable HTTPS"},
            ],
        }

        display_recommendations(recommendations)

        # Should display high priority recommendation
        mock_info.assert_called()
        call_args = str(mock_info.call_args)
        assert "Enable HTTPS" in call_args

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_security_recs_low_priority(self, mock_info):
        """Test security recommendations with low priority"""
        recommendations = {
            "security_recs": [
                {"priority": "low", "recommendation": "Add rate limiting"},
            ],
        }

        display_recommendations(recommendations)

        # Should display low priority recommendation
        mock_info.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_performance_recs_dict(self, mock_info):
        """Test performance recommendations as dict"""
        recommendations = {
            "performance_recs": [
                {"recommendation": "Enable caching"},
            ],
        }

        display_recommendations(recommendations)

        # Should display performance recommendation
        mock_info.assert_called()
        call_args = str(mock_info.call_args)
        assert "Enable caching" in call_args

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_command_selection_no_recommended(self, mock_success):
        """Test command selection with no recommended commands"""
        core = ["cco-status"]
        recommended = []
        optional = ["cco-test"]
        selected = core

        display_command_selection(core, recommended, optional, selected, None)

        # Should display core commands
        mock_success.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_command_selection_no_optional(self, mock_success):
        """Test command selection with no optional commands"""
        core = ["cco-status"]
        recommended = ["cco-test"]
        optional = []
        selected = core + recommended

        display_command_selection(core, recommended, optional, selected, None)

        # Should display commands
        mock_success.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_preview_files_to_create_as_list(self, mock_success):
        """Test preview with files_to_create as list"""
        changes = {
            "files_to_create": [
                ".claude/commands/cco-status.md",
                ".claude/commands/cco-test.md",
            ],
        }

        display_preview(changes)

        # Should display create messages
        calls = [str(call) for call in mock_success.call_args_list]
        assert any("CREATE" in call for call in calls)

    @patch("claudecodeoptimizer.wizard.checkpoints.print_warning")
    def test_display_preview_files_to_delete(self, mock_warning):
        """Test preview with files to delete"""
        changes = {
            "files_to_delete": [
                ".claude/old_config.json",
            ],
        }

        display_preview(changes)

        # Should display delete messages
        calls = [str(call) for call in mock_warning.call_args_list]
        assert any("DELETE" in call for call in calls)

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_preview_principles_as_strings(self, mock_success):
        """Test preview with principles as strings"""
        changes = {
            "principles_selected": ["U_DRY", "U_TEST_FIRST"],
        }

        display_preview(changes)

        # Should display principles
        calls = [str(call) for call in mock_success.call_args_list]
        assert any("U_DRY" in call or "U_TEST_FIRST" in call for call in calls)

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_security_recs_non_dict(self, mock_info):
        """Test security recommendations as non-dict items"""
        recommendations = {
            "security_recs": [
                "Enable HTTPS",
                "Add input validation",
            ],
        }

        display_recommendations(recommendations)

        # Should display recommendations
        mock_info.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_performance_recs_non_dict(self, mock_info):
        """Test performance recommendations as non-dict items"""
        recommendations = {
            "performance_recs": [
                "Enable caching",
                "Optimize queries",
            ],
        }

        display_recommendations(recommendations)

        # Should display recommendations
        mock_info.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_info")
    def test_display_command_selection_unselected_recommended(self, mock_info):
        """Test command selection with unselected recommended commands"""
        core = ["cco-status"]
        recommended = ["cco-test", "cco-audit"]
        optional = []
        selected = core  # Only core, no recommended

        display_command_selection(core, recommended, optional, selected, None)

        # Should display both selected and unselected
        mock_info.assert_called()

    @patch("claudecodeoptimizer.wizard.checkpoints.print_success")
    def test_display_command_selection_with_reasoning(self, mock_success):
        """Test command selection with reasoning for optional commands"""
        core = ["cco-status"]
        recommended = []
        optional = ["cco-test", "cco-audit"]
        selected = core + ["cco-test"]
        reasoning = {"cco-test": "Automated testing is critical"}

        display_command_selection(core, recommended, optional, selected, reasoning)

        # Should display reasoning
        calls = [str(call) for call in mock_success.call_args_list]
        assert any("testing" in call.lower() for call in calls)
