"""Unit tests for ui module."""

from claudecodeoptimizer.ui import (
    display_file_categories,
    display_package_info,
    display_removal_plan,
    display_rules_directories,
    display_settings,
    print_removal_header,
)


class TestPrintRemovalHeader:
    """Test print_removal_header function."""

    def test_prints_header_with_separator(self, capsys) -> None:
        """Test print_removal_header prints formatted header."""
        print_removal_header()

        captured = capsys.readouterr()
        assert "CCO Uninstall" in captured.out
        assert "Location:" in captured.out

    def test_includes_claude_dir_in_output(self, capsys) -> None:
        """Test print_removal_header includes CLAUDE_DIR in output."""
        print_removal_header()

        captured = capsys.readouterr()
        assert ".claude" in captured.out


class TestDisplayPackageInfo:
    """Test display_package_info function."""

    def test_displays_package_with_method(self, capsys) -> None:
        """Test display_package_info displays package with install method."""
        display_package_info("pipx")

        captured = capsys.readouterr()
        assert "Package:" in captured.out
        assert "claudecodeoptimizer" in captured.out
        assert "pipx" in captured.out

    def test_displays_nothing_when_method_none(self, capsys) -> None:
        """Test display_package_info displays nothing when method is None."""
        display_package_info(None)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_displays_different_package_managers(self, capsys) -> None:
        """Test display_package_info works with different package managers."""
        for method in ["pipx", "uv", "pip"]:
            display_package_info(method)
            captured = capsys.readouterr()
            assert method in captured.out


class TestDisplayFileCategories:
    """Test display_file_categories function."""

    def test_displays_commands(self, capsys) -> None:
        """Test display_file_categories displays commands."""
        commands = ["cco-config.md", "cco-optimize.md"]
        agents: list[str] = []
        rules: list[str] = []

        display_file_categories(commands, agents, rules)

        captured = capsys.readouterr()
        assert "Commands:" in captured.out
        assert "cco-config.md" in captured.out
        assert "cco-optimize.md" in captured.out

    def test_displays_agents(self, capsys) -> None:
        """Test display_file_categories displays agents."""
        commands: list[str] = []
        agents = ["cco-apply.md", "cco-audit.md"]
        rules: list[str] = []

        display_file_categories(commands, agents, rules)

        captured = capsys.readouterr()
        assert "Agents:" in captured.out
        assert "cco-apply.md" in captured.out
        assert "cco-audit.md" in captured.out

    def test_displays_claude_md_sections(self, capsys) -> None:
        """Test display_file_categories displays CLAUDE.md sections."""
        commands: list[str] = []
        agents: list[str] = []
        rules = ["CCO_STANDARDS", "CCO_ADAPTIVE"]

        display_file_categories(commands, agents, rules)

        captured = capsys.readouterr()
        assert "CLAUDE.md sections:" in captured.out
        assert "CCO_STANDARDS" in captured.out
        assert "CCO_ADAPTIVE" in captured.out

    def test_displays_all_categories(self, capsys) -> None:
        """Test display_file_categories displays all categories together."""
        commands = ["cco-config.md"]
        agents = ["cco-apply.md"]
        rules = ["CCO_STANDARDS"]

        display_file_categories(commands, agents, rules)

        captured = capsys.readouterr()
        assert "Commands:" in captured.out
        assert "Agents:" in captured.out
        assert "CLAUDE.md sections:" in captured.out

    def test_displays_nothing_when_all_empty(self, capsys) -> None:
        """Test display_file_categories displays nothing when all lists empty."""
        commands: list[str] = []
        agents: list[str] = []
        rules: list[str] = []

        display_file_categories(commands, agents, rules)

        captured = capsys.readouterr()
        assert captured.out == ""


class TestDisplayRulesDirectories:
    """Test display_rules_directories function."""

    def test_displays_current_rules_directory(self, capsys) -> None:
        """Test display_rules_directories displays current rules directory."""
        display_rules_directories(rules_dir=True, rules_dir_old=False)

        captured = capsys.readouterr()
        assert "Rules directory:" in captured.out
        assert "~/.claude/rules/cco/" in captured.out

    def test_displays_old_rules_directory(self, capsys) -> None:
        """Test display_rules_directories displays old rules directory."""
        display_rules_directories(rules_dir=False, rules_dir_old=True)

        captured = capsys.readouterr()
        assert "Rules directory:" in captured.out
        assert "~/.claude/rules/ root (old files)" in captured.out

    def test_displays_both_directories(self, capsys) -> None:
        """Test display_rules_directories displays both directories."""
        display_rules_directories(rules_dir=True, rules_dir_old=True)

        captured = capsys.readouterr()
        assert "~/.claude/rules/cco/" in captured.out
        assert "~/.claude/rules/ root (old files)" in captured.out

    def test_displays_nothing_when_both_false(self, capsys) -> None:
        """Test display_rules_directories displays nothing when both False."""
        display_rules_directories(rules_dir=False, rules_dir_old=False)

        captured = capsys.readouterr()
        assert captured.out == ""


class TestDisplaySettings:
    """Test display_settings function."""

    def test_displays_statusline_setting(self, capsys) -> None:
        """Test display_settings displays statusline setting."""
        display_settings(statusline=True, permissions=False)

        captured = capsys.readouterr()
        assert "Settings (~/.claude/):" in captured.out
        assert "cco-statusline.js" in captured.out
        assert "settings.json (statusLine config)" in captured.out

    def test_displays_permissions_setting(self, capsys) -> None:
        """Test display_settings displays permissions setting."""
        display_settings(statusline=False, permissions=True)

        captured = capsys.readouterr()
        assert "Settings (~/.claude/):" in captured.out
        assert "settings.json (permissions)" in captured.out

    def test_displays_both_settings(self, capsys) -> None:
        """Test display_settings displays both settings."""
        display_settings(statusline=True, permissions=True)

        captured = capsys.readouterr()
        assert "cco-statusline.js" in captured.out
        assert "settings.json (statusLine config)" in captured.out
        assert "settings.json (permissions)" in captured.out

    def test_displays_nothing_when_both_false(self, capsys) -> None:
        """Test display_settings displays nothing when both False."""
        display_settings(statusline=False, permissions=False)

        captured = capsys.readouterr()
        assert captured.out == ""


class TestDisplayRemovalPlan:
    """Test display_removal_plan function."""

    def test_displays_complete_removal_plan(self, capsys) -> None:
        """Test display_removal_plan displays complete removal plan."""
        display_removal_plan(
            method="pipx",
            commands=["cco-config.md"],
            agents=["cco-apply.md"],
            rules=["CCO_STANDARDS"],
            rules_dir=True,
            rules_dir_old=True,
            statusline=True,
            permissions=True,
            total=10,
        )

        captured = capsys.readouterr()
        output = captured.out

        # Check header
        assert "CCO Uninstall" in output

        # Check package info
        assert "claudecodeoptimizer" in output
        assert "pipx" in output

        # Check file categories
        assert "Commands:" in output
        assert "cco-config.md" in output
        assert "Agents:" in output
        assert "cco-apply.md" in output
        assert "CLAUDE.md sections:" in output
        assert "CCO_STANDARDS" in output

        # Check rules directories
        assert "~/.claude/rules/cco/" in output
        assert "~/.claude/rules/ root (old files)" in output

        # Check settings
        assert "cco-statusline.js" in output
        assert "settings.json" in output

        # Check total
        assert "Total: 10 items to remove" in output

    def test_displays_minimal_removal_plan(self, capsys) -> None:
        """Test display_removal_plan displays minimal removal plan."""
        display_removal_plan(
            method=None,
            commands=[],
            agents=[],
            rules=[],
            rules_dir=False,
            rules_dir_old=False,
            statusline=False,
            permissions=False,
            total=0,
        )

        captured = capsys.readouterr()
        output = captured.out

        # Should still have header and total
        assert "CCO Uninstall" in output
        assert "Total: 0 items to remove" in output

    def test_displays_partial_removal_plan(self, capsys) -> None:
        """Test display_removal_plan displays partial removal plan."""
        display_removal_plan(
            method="pip",
            commands=["cco-config.md"],
            agents=[],
            rules=[],
            rules_dir=False,
            rules_dir_old=False,
            statusline=False,
            permissions=False,
            total=2,
        )

        captured = capsys.readouterr()
        output = captured.out

        assert "pip" in output
        assert "cco-config.md" in output
        assert "Total: 2 items to remove" in output
