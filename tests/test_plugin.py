"""Plugin structure and schema validation tests."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


class TestPluginStructure:
    """Test plugin directory structure."""

    def test_plugin_json_exists(self):
        """plugin.json must exist."""
        assert (ROOT / ".claude-plugin" / "plugin.json").exists()

    def test_marketplace_json_exists(self):
        """marketplace.json must exist."""
        assert (ROOT / ".claude-plugin" / "marketplace.json").exists()

    def test_hooks_json_exists(self):
        """hooks.json must exist."""
        assert (ROOT / "hooks" / "hooks.json").exists()

    def test_commands_directory_exists(self):
        """commands/ directory must exist."""
        assert (ROOT / "commands").is_dir()

    def test_agents_directory_exists(self):
        """agents/ directory must exist."""
        assert (ROOT / "agents").is_dir()

    def test_rules_directory_exists(self):
        """rules/ directory must exist."""
        assert (ROOT / "rules").is_dir()

    def test_rules_subdirectories_exist(self):
        """rules/ must have core, languages, frameworks, operations subdirs."""
        rules_dir = ROOT / "rules"
        assert (rules_dir / "core").is_dir()
        assert (rules_dir / "languages").is_dir()
        assert (rules_dir / "frameworks").is_dir()
        assert (rules_dir / "operations").is_dir()


class TestPluginJson:
    """Test plugin.json schema."""

    @pytest.fixture
    def plugin_json(self):
        path = ROOT / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_name(self, plugin_json):
        """plugin.json must have name field."""
        assert "name" in plugin_json
        assert plugin_json["name"] == "cco"

    def test_has_version(self, plugin_json):
        """plugin.json must have version field."""
        assert "version" in plugin_json
        assert isinstance(plugin_json["version"], str)

    def test_has_description(self, plugin_json):
        """plugin.json must have description field."""
        assert "description" in plugin_json
        assert isinstance(plugin_json["description"], str)

    def test_has_hooks(self, plugin_json):
        """plugin.json must reference hooks."""
        assert "hooks" in plugin_json
        assert plugin_json["hooks"] == "hooks/hooks.json"


class TestMarketplaceJson:
    """Test marketplace.json schema."""

    @pytest.fixture
    def marketplace_json(self):
        path = ROOT / ".claude-plugin" / "marketplace.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_required_fields(self, marketplace_json):
        """marketplace.json must have required fields."""
        required = ["name", "version", "description", "owner"]
        for field in required:
            assert field in marketplace_json, f"Missing field: {field}"


class TestHooksJson:
    """Test hooks.json schema."""

    @pytest.fixture
    def hooks_json(self):
        path = ROOT / "hooks" / "hooks.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_hooks_field(self, hooks_json):
        """hooks.json must have hooks field."""
        assert "hooks" in hooks_json

    def test_has_session_start(self, hooks_json):
        """hooks.json must have SessionStart hook."""
        assert "SessionStart" in hooks_json["hooks"]


class TestCommands:
    """Test command files."""

    EXPECTED_COMMANDS = [
        "commit.md",
        "config.md",
        "optimize.md",
        "preflight.md",
        "research.md",
        "review.md",
        "status.md",
    ]

    def test_all_commands_exist(self):
        """All expected command files must exist."""
        commands_dir = ROOT / "commands"
        for cmd in self.EXPECTED_COMMANDS:
            assert (commands_dir / cmd).exists(), f"Missing command: {cmd}"

    def test_command_count(self):
        """Must have exactly 7 commands."""
        commands_dir = ROOT / "commands"
        md_files = list(commands_dir.glob("*.md"))
        assert len(md_files) == 7, f"Expected 7 commands, found {len(md_files)}"

    def test_commands_have_frontmatter(self):
        """Command files should start with ---."""
        commands_dir = ROOT / "commands"
        for cmd_file in commands_dir.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{cmd_file.name} missing frontmatter"


class TestAgents:
    """Test agent files."""

    EXPECTED_AGENTS = [
        "cco-agent-analyze.md",
        "cco-agent-apply.md",
        "cco-agent-research.md",
    ]

    def test_all_agents_exist(self):
        """All expected agent files must exist."""
        agents_dir = ROOT / "agents"
        for agent in self.EXPECTED_AGENTS:
            assert (agents_dir / agent).exists(), f"Missing agent: {agent}"

    def test_agent_count(self):
        """Must have exactly 3 agents."""
        agents_dir = ROOT / "agents"
        md_files = list(agents_dir.glob("*.md"))
        assert len(md_files) == 3, f"Expected 3 agents, found {len(md_files)}"


class TestRules:
    """Test rule files structure."""

    def test_core_rules_exist(self):
        """Core rules must exist with cco- prefix."""
        core_dir = ROOT / "rules" / "core"
        assert (core_dir / "cco-foundation.md").exists()
        assert (core_dir / "cco-safety.md").exists()
        assert (core_dir / "cco-workflow.md").exists()

    def test_core_rule_count(self):
        """Must have exactly 3 core rules."""
        core_dir = ROOT / "rules" / "core"
        md_files = list(core_dir.glob("cco-*.md"))
        assert len(md_files) == 3, f"Expected 3 core rules, found {len(md_files)}"

    def test_language_rule_count(self):
        """Must have exactly 21 language rules."""
        lang_dir = ROOT / "rules" / "languages"
        md_files = list(lang_dir.glob("cco-*.md"))
        assert len(md_files) == 21, f"Expected 21 language rules, found {len(md_files)}"

    def test_framework_rule_count(self):
        """Must have exactly 8 framework rules."""
        fw_dir = ROOT / "rules" / "frameworks"
        md_files = list(fw_dir.glob("cco-*.md"))
        assert len(md_files) == 8, f"Expected 8 framework rules, found {len(md_files)}"

    def test_operations_rule_count(self):
        """Must have exactly 12 operations rules."""
        ops_dir = ROOT / "rules" / "operations"
        md_files = list(ops_dir.glob("cco-*.md"))
        assert len(md_files) == 12, f"Expected 12 operations rules, found {len(md_files)}"

    def test_total_rule_count(self):
        """Total rules should be 44."""
        rules_dir = ROOT / "rules"
        total = 0
        for subdir in ["core", "languages", "frameworks", "operations"]:
            total += len(list((rules_dir / subdir).glob("cco-*.md")))
        assert total == 44, f"Expected 44 total rules, found {total}"

    def test_all_rules_have_cco_prefix(self):
        """All rule files should have cco- prefix."""
        rules_dir = ROOT / "rules"
        for subdir in ["core", "languages", "frameworks", "operations"]:
            for md_file in (rules_dir / subdir).glob("*.md"):
                assert md_file.name.startswith("cco-"), f"{md_file} missing cco- prefix"


class TestHookScript:
    """Test hook script exists and is valid."""

    def test_hook_script_exists(self):
        """install-core-rules.js must exist."""
        assert (ROOT / "hooks" / "install-core-rules.js").exists()

    def test_hook_script_has_additional_context(self):
        """Hook script should output additionalContext."""
        script = (ROOT / "hooks" / "install-core-rules.js").read_text(encoding="utf-8")
        assert "additionalContext" in script
        assert "hookSpecificOutput" in script
