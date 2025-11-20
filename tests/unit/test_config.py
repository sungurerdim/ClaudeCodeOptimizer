"""Unit tests for claudecodeoptimizer/config.py module."""

from pathlib import Path

from claudecodeoptimizer.config import (
    BRAND_NAME,
    CLI_NAME,
    COMMAND_PREFIX,
    CONFIG,
    DISPLAY_NAME,
    FULL_NAME,
    SHORT_NAME,
    VERSION,
    CCOConfig,
    get_agents_dir,
    get_all_paths,
    get_claude_dir,
    get_command_name,
    get_global_commands_dir,
    get_home_dir,
    get_principles_dir,
    get_skills_dir,
)


class TestModuleConstants:
    """Test module-level constants."""

    def test_brand_name(self):
        """Test BRAND_NAME constant."""
        assert BRAND_NAME == "CCO"

    def test_full_name(self):
        """Test FULL_NAME constant."""
        assert FULL_NAME == "ClaudeCodeOptimizer"

    def test_display_name(self):
        """Test DISPLAY_NAME constant."""
        assert DISPLAY_NAME == "Claude Code Optimizer"

    def test_short_name(self):
        """Test SHORT_NAME constant."""
        assert SHORT_NAME == "CCO"

    def test_cli_name(self):
        """Test CLI_NAME constant."""
        assert CLI_NAME == "cco"

    def test_version(self):
        """Test VERSION constant is set."""
        assert VERSION is not None
        assert isinstance(VERSION, str)

    def test_command_prefix(self):
        """Test COMMAND_PREFIX constant."""
        assert COMMAND_PREFIX == "cco"


class TestPathHelpers:
    """Test path helper functions."""

    def test_get_home_dir(self):
        """Test get_home_dir returns Path.home()."""
        result = get_home_dir()
        assert isinstance(result, Path)
        assert result == Path.home()

    def test_get_claude_dir(self):
        """Test get_claude_dir returns ~/.claude/."""
        result = get_claude_dir()
        assert isinstance(result, Path)
        assert result.name == ".claude"
        assert result.parent == Path.home()

    def test_get_global_commands_dir(self):
        """Test get_global_commands_dir returns ~/.claude/commands/."""
        result = get_global_commands_dir()
        assert isinstance(result, Path)
        assert result.name == "commands"
        assert result.parent.name == ".claude"

    def test_get_principles_dir(self):
        """Test get_principles_dir returns ~/.claude/principles/."""
        result = get_principles_dir()
        assert isinstance(result, Path)
        assert result.name == "principles"
        assert result.parent.name == ".claude"

    def test_get_agents_dir(self):
        """Test get_agents_dir returns ~/.claude/agents/."""
        result = get_agents_dir()
        assert isinstance(result, Path)
        assert result.name == "agents"
        assert result.parent.name == ".claude"

    def test_get_skills_dir(self):
        """Test get_skills_dir returns ~/.claude/skills/."""
        result = get_skills_dir()
        assert isinstance(result, Path)
        assert result.name == "skills"
        assert result.parent.name == ".claude"


class TestCommandNaming:
    """Test command naming functions."""

    def test_get_command_name(self):
        """Test get_command_name generates correct command names."""
        assert get_command_name("remove") == "/cco-remove"
        assert get_command_name("status") == "/cco-status"
        assert get_command_name("test") == "/cco-test"

    def test_get_command_name_with_special_chars(self):
        """Test get_command_name with various inputs."""
        assert get_command_name("audit-code") == "/cco-audit-code"
        assert get_command_name("fix") == "/cco-fix"


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_all_paths_returns_dict(self):
        """Test get_all_paths returns dictionary of paths."""
        result = get_all_paths()
        assert isinstance(result, dict)

    def test_get_all_paths_contains_expected_keys(self):
        """Test get_all_paths contains all expected keys."""
        result = get_all_paths()
        expected_keys = {
            "claude_dir",
            "commands_dir",
            "principles_dir",
            "skills_dir",
            "agents_dir",
        }
        assert set(result.keys()) == expected_keys

    def test_get_all_paths_values_are_paths(self):
        """Test get_all_paths returns Path objects."""
        result = get_all_paths()
        for value in result.values():
            assert isinstance(value, Path)


class TestCCOConfigClass:
    """Test CCOConfig class."""

    def test_ccoconfig_has_brand_constants(self):
        """Test CCOConfig class has brand constants."""
        assert CCOConfig.BRAND_NAME == BRAND_NAME
        assert CCOConfig.FULL_NAME == FULL_NAME
        assert CCOConfig.DISPLAY_NAME == DISPLAY_NAME
        assert CCOConfig.SHORT_NAME == SHORT_NAME
        assert CCOConfig.CLI_NAME == CLI_NAME
        assert CCOConfig.COMMAND_PREFIX == COMMAND_PREFIX

    def test_ccoconfig_has_static_methods(self):
        """Test CCOConfig class has static methods."""
        assert callable(CCOConfig.get_home_dir)
        assert callable(CCOConfig.get_claude_dir)
        assert callable(CCOConfig.get_global_commands_dir)
        assert callable(CCOConfig.get_principles_dir)
        assert callable(CCOConfig.get_skills_dir)
        assert callable(CCOConfig.get_agents_dir)
        assert callable(CCOConfig.get_command_name)
        assert callable(CCOConfig.get_all_paths)

    def test_ccoconfig_static_methods_work(self):
        """Test CCOConfig static methods return expected values."""
        assert CCOConfig.get_home_dir() == get_home_dir()
        assert CCOConfig.get_claude_dir() == get_claude_dir()
        assert CCOConfig.get_command_name("test") == "/cco-test"

    def test_ccoconfig_to_dict(self):
        """Test CCOConfig.to_dict returns complete dictionary."""
        result = CCOConfig.to_dict()
        assert isinstance(result, dict)
        assert "branding" in result
        assert "paths" in result
        assert "commands" in result
        assert "defaults" in result

    def test_ccoconfig_to_dict_branding(self):
        """Test CCOConfig.to_dict branding section."""
        result = CCOConfig.to_dict()
        branding = result["branding"]
        assert branding["brand_name"] == BRAND_NAME
        assert branding["full_name"] == FULL_NAME
        assert branding["display_name"] == DISPLAY_NAME
        assert branding["cli_name"] == CLI_NAME
        assert branding["version"] == VERSION

    def test_ccoconfig_to_dict_paths(self):
        """Test CCOConfig.to_dict paths section."""
        result = CCOConfig.to_dict()
        paths = result["paths"]
        assert isinstance(paths, dict)
        assert all(isinstance(v, str) for v in paths.values())
        assert "claude_dir" in paths

    def test_ccoconfig_to_dict_commands(self):
        """Test CCOConfig.to_dict commands section."""
        result = CCOConfig.to_dict()
        commands = result["commands"]
        assert commands["prefix"] == COMMAND_PREFIX
        assert commands["status"] == "/cco-status"
        assert commands["help"] == "/cco-help"

    def test_config_singleton(self):
        """Test CONFIG singleton is CCOConfig instance."""
        assert isinstance(CONFIG, CCOConfig)


class TestDefaultConfig:
    """Test DEFAULT_CONFIG dictionary."""

    def test_default_config_has_version(self):
        """Test DEFAULT_CONFIG contains version."""
        from claudecodeoptimizer.config import DEFAULT_CONFIG

        assert "version" in DEFAULT_CONFIG
        assert DEFAULT_CONFIG["version"] == VERSION

    def test_default_config_has_brand(self):
        """Test DEFAULT_CONFIG contains brand info."""
        from claudecodeoptimizer.config import DEFAULT_CONFIG

        assert "brand" in DEFAULT_CONFIG
        brand = DEFAULT_CONFIG["brand"]
        assert brand["name"] == BRAND_NAME
        assert brand["full_name"] == FULL_NAME
        assert brand["display_name"] == DISPLAY_NAME

    def test_default_config_has_paths(self):
        """Test DEFAULT_CONFIG contains paths."""
        from claudecodeoptimizer.config import DEFAULT_CONFIG

        assert "paths" in DEFAULT_CONFIG
        paths = DEFAULT_CONFIG["paths"]
        assert "claude_dir" in paths


class TestMessageConstants:
    """Test message constants."""

    def test_message_constants_exist(self):
        """Test message constants are defined."""
        from claudecodeoptimizer.config import (
            MSG_ALREADY_INSTALLED,
            MSG_GLOBAL_INSTALL_SUCCESS,
            MSG_INSTALL_FAILED,
            MSG_NOT_INSTALLED,
        )

        assert MSG_GLOBAL_INSTALL_SUCCESS is not None
        assert MSG_ALREADY_INSTALLED is not None
        assert MSG_NOT_INSTALLED is not None
        assert MSG_INSTALL_FAILED is not None

    def test_message_constants_contain_brand_name(self):
        """Test message constants contain brand name."""
        from claudecodeoptimizer.config import MSG_GLOBAL_INSTALL_SUCCESS

        assert (
            DISPLAY_NAME in MSG_GLOBAL_INSTALL_SUCCESS or SHORT_NAME in MSG_GLOBAL_INSTALL_SUCCESS
        )


class TestGitignorePatterns:
    """Test GITIGNORE_PATTERNS."""

    def test_gitignore_patterns_is_list(self):
        """Test GITIGNORE_PATTERNS is a list."""
        from claudecodeoptimizer.config import GITIGNORE_PATTERNS

        assert isinstance(GITIGNORE_PATTERNS, list)

    def test_gitignore_patterns_empty(self):
        """Test GITIGNORE_PATTERNS is empty (clean project directories)."""
        from claudecodeoptimizer.config import GITIGNORE_PATTERNS

        # CCO keeps project directories clean, so should be empty
        assert len(GITIGNORE_PATTERNS) == 0


class TestExports:
    """Test __all__ exports."""

    def test_all_exports_exist(self):
        """Test __all__ exports are defined."""
        from claudecodeoptimizer import config

        assert hasattr(config, "__all__")
        assert isinstance(config.__all__, list)

    def test_all_exports_importable(self):
        """Test all exports can be imported."""
        from claudecodeoptimizer import config
        from claudecodeoptimizer.config import __all__

        for name in __all__:
            assert hasattr(config, name)
