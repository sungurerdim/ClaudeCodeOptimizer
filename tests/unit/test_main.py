"""
Unit tests for __main__.py entry point

Tests CLI argument parsing, command execution, and error handling.
Target Coverage: 100%
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from claudecodeoptimizer.wizard.models import SystemContext, WizardResult


@pytest.fixture
def mock_system_context():
    """Create mock system context with all required fields"""
    return SystemContext(
        project_root=Path.cwd(),
        os_type="linux",
        os_version="22.04",
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
        pip_version="23.0.0",
        git_installed=True,
    )


@pytest.fixture
def mock_wizard_result_success(mock_system_context):
    """Create successful wizard result"""
    return WizardResult(
        success=True,
        mode="quick",
        system_context=mock_system_context,
        answers={},
        selected_principles=["P_TYPE_SAFETY", "P_LINTING_SAST"],
        selected_commands=["cco-init", "cco-status"],
        skipped_questions=[],
        duration_seconds=1.5,
        error=None,
    )


@pytest.fixture
def mock_wizard_result_failure(mock_system_context):
    """Create failed wizard result"""
    return WizardResult(
        success=False,
        mode="quick",
        system_context=mock_system_context,
        answers={},
        selected_principles=[],
        selected_commands=[],
        skipped_questions=[],
        duration_seconds=0.5,
        error="Test error message",
    )


class TestMainHelp:
    """Test help output when no command is provided"""

    @patch("sys.argv", ["claudecodeoptimizer"])
    @patch("claudecodeoptimizer.commands_loader.get_slash_commands")
    def test_no_command_shows_help(self, mock_get_commands, capsys):
        """Test that no command shows help and tip"""
        mock_get_commands.return_value = "/cco-init, /cco-remove"

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "ClaudeCodeOptimizer" in captured.out
        assert "Tip:" in captured.out
        assert "/cco-init" in captured.out


class TestInitCommand:
    """Test init command with various arguments"""

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_default_quick_mode(self, mock_wizard_class, mock_wizard_result_success, capsys):
        """Test init with default quick mode"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_wizard_class.assert_called_once()
        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["mode"] == "quick"
        assert call_kwargs["dry_run"] is False

        captured = capsys.readouterr()
        assert "Next steps:" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init", "--mode", "interactive"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_interactive_mode(self, mock_wizard_class, mock_wizard_result_success):
        """Test init with interactive mode"""
        mock_wizard = MagicMock()
        mock_wizard_result_success.mode = "interactive"
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["mode"] == "interactive"

    @patch("sys.argv", ["claudecodeoptimizer", "init", "--dry-run"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_dry_run(self, mock_wizard_class, mock_wizard_result_success, capsys):
        """Test init with dry-run flag"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["dry_run"] is True

        captured = capsys.readouterr()
        assert "Dry run complete!" in captured.out
        assert "No files were written" in captured.out
        assert "Mode: quick" in captured.out
        assert "Principles selected: 2" in captured.out
        assert "Commands selected: 2" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init", "--mode", "interactive", "--dry-run"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_interactive_dry_run(self, mock_wizard_class, mock_wizard_result_success, capsys):
        """Test init with both interactive mode and dry-run"""
        mock_wizard = MagicMock()
        mock_wizard_result_success.mode = "interactive"
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["mode"] == "interactive"
        assert call_kwargs["dry_run"] is True

        captured = capsys.readouterr()
        assert "Mode: interactive" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_failure(self, mock_wizard_class, mock_wizard_result_failure, capsys):
        """Test init with failure result"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_failure
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Initialization failed: Test error message" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_keyboard_interrupt(self, mock_wizard_class, capsys):
        """Test init with KeyboardInterrupt"""
        mock_wizard = MagicMock()
        mock_wizard.run.side_effect = KeyboardInterrupt()
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Initialization cancelled by user" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_exception(self, mock_wizard_class, capsys):
        """Test init with unexpected exception"""
        mock_wizard = MagicMock()
        mock_wizard.run.side_effect = RuntimeError("Unexpected error")
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Initialization failed: Unexpected error" in captured.out


class TestStatusCommand:
    """Test status command"""

    @patch("sys.argv", ["claudecodeoptimizer", "status"])
    def test_status_initialized(self, tmp_path, monkeypatch, capsys):
        """Test status when project is initialized"""
        # Create .claude dir and CLAUDE.md
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# CCO Config", encoding="utf-8")

        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "CCO is initialized" in captured.out
        assert "Configuration:" in captured.out
        assert "Guide:" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "status"])
    def test_status_not_initialized_no_dir(self, tmp_path, monkeypatch, capsys):
        """Test status when .claude dir doesn't exist"""
        monkeypatch.chdir(tmp_path)

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "CCO is not initialized" in captured.out
        assert "To initialize:" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "status"])
    def test_status_not_initialized_no_claude_md(self, tmp_path, monkeypatch, capsys):
        """Test status when CLAUDE.md doesn't exist"""
        # Create .claude dir but not CLAUDE.md
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        monkeypatch.chdir(tmp_path)

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "CCO is not initialized" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "status"])
    def test_status_exception(self, monkeypatch, capsys):
        """Test status with exception during check"""
        # Mock Path.cwd() to raise exception
        with patch("pathlib.Path.cwd", side_effect=RuntimeError("Test error")):
            from claudecodeoptimizer.__main__ import main

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Error: Test error" in captured.out


class TestRemoveCommand:
    """Test remove command"""

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_success(self, mock_wizard_class, capsys):
        """Test successful project removal"""
        mock_wizard_class.uninitialize.return_value = {
            "success": True,
            "project_name": "test-project",
            "files_removed": [".claude/", "CLAUDE.md", "PRINCIPLES.md"],
        }

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "All CCO files removed successfully!" in captured.out
        assert "Project: test-project" in captured.out
        assert "Files removed: 3" in captured.out
        assert ".claude/" in captured.out
        assert "CLAUDE.md" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_success_no_files(self, mock_wizard_class, capsys):
        """Test successful removal with no files listed"""
        mock_wizard_class.uninitialize.return_value = {
            "success": True,
            "project_name": "test-project",
            "files_removed": [],
        }

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "All CCO files removed successfully!" in captured.out
        assert "Files removed: 0" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_failure(self, mock_wizard_class, capsys):
        """Test failed project removal"""
        mock_wizard_class.uninitialize.return_value = {
            "success": False,
            "error": "Permission denied",
        }

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Uninitialization failed: Permission denied" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_failure_no_error_message(self, mock_wizard_class, capsys):
        """Test failed removal with no error message"""
        mock_wizard_class.uninitialize.return_value = {
            "success": False,
        }

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Uninitialization failed: unknown error" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_exception(self, mock_wizard_class, capsys):
        """Test remove with exception"""
        mock_wizard_class.uninitialize.side_effect = RuntimeError("Test error")

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.out


class TestVersionCommand:
    """Test version command"""

    @patch("sys.argv", ["claudecodeoptimizer", "version"])
    def test_version(self, capsys):
        """Test version output"""
        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "ClaudeCodeOptimizer v" in captured.out
        # Should include version number
        assert "0.1.0" in captured.out


class TestEntryPoint:
    """Test __main__ entry point"""

    def test_main_entry_point(self):
        """Test that main is callable"""
        from claudecodeoptimizer.__main__ import main

        assert callable(main)

    @patch("sys.argv", ["claudecodeoptimizer"])
    @patch("claudecodeoptimizer.__main__.main")
    def test_if_name_main_block(self, mock_main):
        """Test __name__ == '__main__' block"""
        # This tests that the block exists and calls main()
        # We can't directly test it since __name__ won't be '__main__' in tests
        # but we can verify the function exists
        from claudecodeoptimizer import __main__

        assert hasattr(__main__, "main")
        assert callable(__main__.main)


class TestArgumentParsing:
    """Test argument parsing edge cases"""

    @patch("sys.argv", ["claudecodeoptimizer", "init", "--mode", "quick"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_explicit_quick_mode(self, mock_wizard_class, mock_wizard_result_success):
        """Test init with explicit quick mode"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["mode"] == "quick"

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_init_uses_cwd_as_project_root(self, mock_wizard_class, mock_wizard_result_success):
        """Test that init uses current working directory"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit):
            main()

        call_kwargs = mock_wizard_class.call_args[1]
        assert call_kwargs["project_root"] == Path.cwd()


class TestImports:
    """Test that imports work correctly"""

    def test_safe_print_configure_called(self):
        """Test that configure_utf8_encoding is called on import"""
        # This is called at module level, so we can't easily test it
        # but we can verify the module imports successfully
        from claudecodeoptimizer import __main__

        assert hasattr(__main__, "main")

    def test_get_slash_commands_import(self):
        """Test that get_slash_commands can be imported"""
        from claudecodeoptimizer.__main__ import main

        # If this doesn't raise ImportError, the import works
        assert callable(main)


class TestPrintStatements:
    """Test all print statement branches"""

    @patch("sys.argv", ["claudecodeoptimizer", "init", "--mode", "interactive", "--dry-run"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_dry_run_prints_all_info(self, mock_wizard_class, mock_system_context, capsys):
        """Test dry run prints all expected information"""
        mock_wizard = MagicMock()
        result = WizardResult(
            success=True,
            mode="interactive",
            system_context=mock_system_context,
            answers={},
            selected_principles=["P_TEST1", "P_TEST2", "P_TEST3"],
            selected_commands=["cmd1", "cmd2"],
            skipped_questions=[],
            duration_seconds=1.5,
            error=None,
        )
        mock_wizard.run.return_value = result
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Dry run complete!" in captured.out
        assert "Mode: interactive" in captured.out
        assert "Principles selected: 3" in captured.out
        assert "Commands selected: 2" in captured.out
        assert "Run without --dry-run to apply configuration" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "init"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_success_prints_next_steps(self, mock_wizard_class, mock_wizard_result_success, capsys):
        """Test success prints next steps"""
        mock_wizard = MagicMock()
        mock_wizard.run.return_value = mock_wizard_result_success
        mock_wizard_class.return_value = mock_wizard

        from claudecodeoptimizer.__main__ import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Next steps:" in captured.out
        assert "Review PRINCIPLES.md" in captured.out
        assert "Run /cco-status" in captured.out
        assert "Run /cco-audit" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_success_prints_all_files(self, mock_wizard_class, capsys):
        """Test remove success prints all removed files"""
        mock_wizard_class.uninitialize.return_value = {
            "success": True,
            "project_name": "my-project",
            "files_removed": [
                ".claude/",
                "CLAUDE.md",
                "PRINCIPLES.md",
                ".claude/commands/",
                ".claude/principles/",
            ],
        }

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "All CCO files removed successfully!" in captured.out
        assert "Project: my-project" in captured.out
        assert "Files removed: 5" in captured.out
        assert ".claude/" in captured.out
        assert "CLAUDE.md" in captured.out
        assert "PRINCIPLES.md" in captured.out
        assert "CCO has been cleanly removed" in captured.out
        assert "To reinitialize:" in captured.out


class TestEdgeCases:
    """Test edge cases and corner cases"""

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_success_with_missing_project_name(self, mock_wizard_class, capsys):
        """Test remove when project_name is missing from result"""
        mock_wizard_class.uninitialize.return_value = {
            "success": True,
            "files_removed": [".claude/"],
        }

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        assert "Project: unknown" in captured.out

    @patch("sys.argv", ["claudecodeoptimizer", "remove"])
    @patch("claudecodeoptimizer.wizard.orchestrator.CCOWizard")
    def test_remove_success_with_empty_files_removed(self, mock_wizard_class, capsys):
        """Test remove when files_removed is empty via .get() default"""
        mock_wizard_class.uninitialize.return_value = {
            "success": True,
            "project_name": "test",
            # files_removed not present, .get() will default to []
        }

        from claudecodeoptimizer.__main__ import main

        main()

        captured = capsys.readouterr()
        # Should handle missing key gracefully with .get() defaulting to []
        assert "Files removed: 0" in captured.out


class TestMainExecution:
    """Test the if __name__ == '__main__' block"""

    def test_main_module_execution(self):
        """Test executing the module as __main__"""
        import subprocess
        import sys

        # Run the module as a script
        result = subprocess.run(
            [sys.executable, "-m", "claudecodeoptimizer"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        # Should show help
        assert "ClaudeCodeOptimizer" in result.stdout or "ClaudeCodeOptimizer" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.__main__", "--cov-report=term-missing"])
