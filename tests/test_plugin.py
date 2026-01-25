"""Plugin schema and integration validation tests.

These tests validate:
- JSON schema correctness (catches malformed config)
- Hook integration (catches broken session injection)
- Convention enforcement (catches naming violations)

NOT tested (would break on every file change):
- Hardcoded file counts
- File/directory existence
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


class TestPluginJson:
    """Validate plugin.json schema - catches malformed plugin config."""

    @pytest.fixture
    def plugin_json(self):
        path = ROOT / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_required_fields(self, plugin_json):
        """Plugin must have name, version, description, hooks."""
        assert plugin_json.get("name") == "cco"
        assert isinstance(plugin_json.get("version"), str)
        assert isinstance(plugin_json.get("description"), str)
        assert "SessionStart" in plugin_json.get("hooks", {})


class TestMarketplaceJson:
    """Validate marketplace.json schema - catches broken marketplace listing."""

    @pytest.fixture
    def marketplace_json(self):
        path = ROOT / ".claude-plugin" / "marketplace.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_required_fields(self, marketplace_json):
        """Marketplace listing must have name, version, description, owner."""
        required = ["name", "version", "description", "owner"]
        for field in required:
            assert field in marketplace_json, f"Missing field: {field}"


class TestCoreRulesJson:
    """Validate core-rules.json schema - catches broken rule injection."""

    @pytest.fixture
    def core_rules_json(self):
        path = ROOT / "hooks" / "core-rules.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_hook_output_schema(self, core_rules_json):
        """Hook output must have correct structure for Claude Code."""
        output = core_rules_json.get("hookSpecificOutput", {})
        assert output.get("hookEventName") == "SessionStart"
        assert "additionalContext" in output
        # Content should be substantial (not empty/truncated)
        assert len(output["additionalContext"]) > 1000


class TestCommandFormat:
    """Validate command file format - catches broken command definitions."""

    def test_commands_have_valid_frontmatter(self):
        """Command files must start with YAML frontmatter."""
        commands_dir = ROOT / "commands"
        for cmd_file in commands_dir.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{cmd_file.name} missing frontmatter"
            # Frontmatter must be closed
            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{cmd_file.name} has unclosed frontmatter"


class TestRuleConventions:
    """Validate rule naming conventions - catches accidental pollution."""

    def test_all_rules_have_cco_prefix(self):
        """All rule files must use cco- prefix for safe updates."""
        rules_dir = ROOT / "rules"
        for subdir in ["core", "languages", "frameworks", "operations"]:
            subdir_path = rules_dir / subdir
            if not subdir_path.exists():
                continue
            for md_file in subdir_path.glob("*.md"):
                assert md_file.name.startswith("cco-"), (
                    f"{md_file} missing cco- prefix - would conflict with user rules"
                )


class TestHookIntegration:
    """Validate hook wiring - catches broken session initialization."""

    def test_plugin_hook_references_core_rules(self):
        """Plugin hook must correctly reference core-rules.json."""
        path = ROOT / ".claude-plugin" / "plugin.json"
        plugin_json = json.loads(path.read_text(encoding="utf-8"))

        session_start = plugin_json["hooks"]["SessionStart"]
        assert isinstance(session_start, list), "SessionStart must be a list"

        hook_def = session_start[0]["hooks"][0]
        assert hook_def["type"] == "command"
        assert "core-rules.json" in hook_def["command"]

    def test_core_rules_contains_all_sections(self):
        """Injected rules must contain all core rule sections."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        core_rules = json.loads(core_rules_path.read_text(encoding="utf-8"))
        content = core_rules["hookSpecificOutput"]["additionalContext"]

        # These sections must exist - if missing, rules weren't concatenated properly
        assert "Foundation" in content, "Missing Foundation rules"
        assert "Safety" in content, "Missing Safety rules"
        assert "Workflow" in content, "Missing Workflow rules"
