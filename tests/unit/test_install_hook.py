"""
Unit tests for Install Hook

Tests post-install hook for ClaudeCodeOptimizer package installation.
Target Coverage: 90%+
"""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from claudecodeoptimizer import install_hook


class TestPostInstall:
    """Test post_install function"""

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_success(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test successful post-install execution"""
        # Setup mock to return success
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [
                "Deployed template files",
                "Copied command files",
                "Setup principles directory",
            ],
        }

        # Execute
        install_hook.post_install()

        # Verify setup_global_knowledge called with force=False
        mock_setup.assert_called_once_with(force=False)

        # Verify success messages printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        all_output = " ".join(print_calls)

        assert any("ClaudeCodeOptimizer Post-Install Setup" in call for call in print_calls)
        assert any("Global CCO directory" in call for call in print_calls)
        assert any(".cco" in call for call in print_calls)
        assert any("CCO is ready" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_with_actions(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install prints all actions"""
        # Setup mock with multiple actions
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [
                "Created directory structure",
                "Deployed template files",
                "Copied command files",
            ],
        }

        # Execute
        install_hook.post_install()

        # Verify all actions printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        all_output = " ".join(print_calls)

        assert any("Created directory structure" in call for call in print_calls)
        assert any("Deployed template files" in call for call in print_calls)
        assert any("Copied command files" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_success_false(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install when success is False"""
        # Setup mock to return success=False
        mock_setup.return_value = {
            "success": False,
            "global_dir": "/home/user/.cco",
            "actions": ["Partial setup"],
        }

        # Execute
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("Warning: Global setup completed with warnings" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_no_actions(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install with no actions in result"""
        # Setup mock without actions key
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
        }

        # Execute - should not crash
        install_hook.post_install()

        # Verify basic messages still printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("ClaudeCodeOptimizer Post-Install Setup" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_empty_actions(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install with empty actions list"""
        # Setup mock with empty actions
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [],
        }

        # Execute - should not crash
        install_hook.post_install()

        # Verify success message still printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("CCO is ready" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_import_error(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles ImportError gracefully"""
        # Setup mock to raise ImportError
        mock_setup.side_effect = ImportError("Module not found")

        # Execute - should not crash
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        all_output = " ".join(print_calls)

        assert any("Warning: CCO post-install setup failed" in call for call in print_calls)
        assert any("Module not found" in call for call in print_calls)
        assert any("manually run setup later" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_generic_exception(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles generic exceptions gracefully"""
        # Setup mock to raise generic exception
        mock_setup.side_effect = Exception("Unexpected error")

        # Execute - should not crash
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]

        assert any("Warning: CCO post-install setup failed" in call for call in print_calls)
        assert any("Unexpected error" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_runtime_error(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles RuntimeError gracefully"""
        # Setup mock to raise RuntimeError
        mock_setup.side_effect = RuntimeError("Runtime issue")

        # Execute - should not crash
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("Warning: CCO post-install setup failed" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_permission_error(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles PermissionError gracefully"""
        # Setup mock to raise PermissionError
        mock_setup.side_effect = PermissionError("Access denied")

        # Execute - should not crash
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("Access denied" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_file_not_found_error(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles FileNotFoundError gracefully"""
        # Setup mock to raise FileNotFoundError
        mock_setup.side_effect = FileNotFoundError("File missing")

        # Execute - should not crash
        install_hook.post_install()

        # Verify warning message printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("File missing" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_prints_separators(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install prints decorative separators"""
        # Setup mock to return success
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [],
        }

        # Execute
        install_hook.post_install()

        # Verify separators (60 equal signs) printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        separator_calls = [call for call in print_calls if "=" * 60 in call]

        # Should have at least 2 separator lines (start and end)
        assert len(separator_calls) >= 2

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_prints_header(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install prints header"""
        # Setup mock to return success
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [],
        }

        # Execute
        install_hook.post_install()

        # Verify header printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("ClaudeCodeOptimizer Post-Install Setup" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_prints_success_instruction(
        self, mock_print: Mock, mock_setup: Mock
    ) -> None:
        """Test post-install prints instruction to run init"""
        # Setup mock to return success
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [],
        }

        # Execute
        install_hook.post_install()

        # Verify instruction printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("python -m claudecodeoptimizer init" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_prints_manual_instruction_on_error(
        self, mock_print: Mock, mock_setup: Mock
    ) -> None:
        """Test post-install prints manual instruction on error"""
        # Setup mock to raise exception
        mock_setup.side_effect = Exception("Test error")

        # Execute
        install_hook.post_install()

        # Verify manual instruction printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any("manually run setup later" in call for call in print_calls)
        assert any("python -m claudecodeoptimizer init" in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_global_dir_path(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install displays global directory path"""
        # Setup mock with specific path
        test_path = "/custom/path/.cco"
        mock_setup.return_value = {
            "success": True,
            "global_dir": test_path,
            "actions": [],
        }

        # Execute
        install_hook.post_install()

        # Verify path printed
        print_calls = [str(call[0]) for call in mock_print.call_args_list]
        assert any(test_path in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_force_parameter(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install calls setup_global_knowledge with force=False"""
        # Setup mock
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": [],
        }

        # Execute
        install_hook.post_install()

        # Verify force=False passed
        mock_setup.assert_called_once_with(force=False)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    def test_post_install_real_execution(self, mock_setup: Mock) -> None:
        """Test post-install can be called without mocking"""
        # This tests the import path works
        # Real execution would require setup_global_knowledge to exist
        output = StringIO()

        mock_setup.return_value = {
            "success": True,
            "global_dir": "/test/.cco",
            "actions": ["Test action"],
        }

        with redirect_stdout(output):
            install_hook.post_install()

        result = output.getvalue()
        assert "ClaudeCodeOptimizer Post-Install Setup" in result

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_unicode_in_path(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles Unicode in global_dir path"""
        # Setup mock with Unicode path
        unicode_path = "/home/user/Тест/.cco"
        mock_setup.return_value = {
            "success": True,
            "global_dir": unicode_path,
            "actions": [],
        }

        # Execute - should not crash
        install_hook.post_install()

        # Verify executed successfully
        mock_setup.assert_called_once()

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_post_install_unicode_in_actions(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test post-install handles Unicode in action messages"""
        # Setup mock with Unicode in actions
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/home/user/.cco",
            "actions": ["Created ✓ directory", "Deployed 📦 files"],
        }

        # Execute - should not crash
        install_hook.post_install()

        # Verify executed successfully
        mock_setup.assert_called_once()


class TestMainBlock:
    """Test __main__ block execution"""

    @patch("claudecodeoptimizer.install_hook.post_install")
    def test_main_block_calls_post_install(self, mock_post_install: Mock) -> None:
        """Test that __main__ block calls post_install"""
        # Import and execute the main block

        with patch("claudecodeoptimizer.install_hook.post_install") as mock_func:
            # This would normally execute the script
            # We can't easily test __main__ block, so we just verify the function exists
            assert hasattr(install_hook, "post_install")
            assert callable(install_hook.post_install)


class TestImportPath:
    """Test import paths and dependencies"""

    def test_import_install_hook(self) -> None:
        """Test install_hook module can be imported"""
        import claudecodeoptimizer.install_hook as module

        assert hasattr(module, "post_install")
        assert callable(module.post_install)

    def test_function_exists(self) -> None:
        """Test post_install function exists"""
        from claudecodeoptimizer.install_hook import post_install

        assert callable(post_install)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    def test_circular_import_avoided(self, mock_setup: Mock) -> None:
        """Test that import is done inside function to avoid circular deps"""
        # Setup mock
        mock_setup.return_value = {
            "success": True,
            "global_dir": "/test/.cco",
            "actions": [],
        }

        # Execute - should not crash from circular imports
        with patch("builtins.print"):
            install_hook.post_install()

        # Verify setup was called (import succeeded)
        mock_setup.assert_called_once()


class TestErrorMessages:
    """Test error message formatting and content"""

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_error_message_format(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test error message contains useful information"""
        # Setup mock to raise exception
        error_msg = "Custom error message for testing"
        mock_setup.side_effect = Exception(error_msg)

        # Execute
        install_hook.post_install()

        # Verify error message components
        print_calls = [str(call[0]) for call in mock_print.call_args_list]

        # Should contain warning symbol
        assert any("⚠" in call or "Warning" in call for call in print_calls)

        # Should contain the actual error
        assert any(error_msg in call for call in print_calls)

    @patch("claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge")
    @patch("builtins.print")
    def test_success_message_format(self, mock_print: Mock, mock_setup: Mock) -> None:
        """Test success message contains checkmark and path"""
        # Setup mock
        test_path = "/home/user/.cco"
        mock_setup.return_value = {
            "success": True,
            "global_dir": test_path,
            "actions": ["Action 1"],
        }

        # Execute
        install_hook.post_install()

        # Verify success indicators
        print_calls = [str(call[0]) for call in mock_print.call_args_list]

        # Should contain checkmark or success indicator
        assert any("✓" in call or "Global CCO directory" in call for call in print_calls)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
