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

    def test_commands_directory_exists(self):
        """commands/ directory must exist."""
        assert (ROOT / "commands").is_dir()

    def test_agents_directory_exists(self):
        """agents/ directory must exist."""
        assert (ROOT / "agents").is_dir()

    def test_rules_directory_exists(self):
        """rules/ directory must exist."""
        assert (ROOT / "rules").is_dir()


class TestPluginJson:
    """Test plugin.json schema."""

    @pytest.fixture
    def plugin_json(self):
        path = ROOT / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_name(self, plugin_json):
        """plugin.json must have name field."""
        assert "name" in plugin_json
        assert isinstance(plugin_json["name"], str)

    def test_has_version(self, plugin_json):
        """plugin.json must have version field."""
        assert "version" in plugin_json
        assert isinstance(plugin_json["version"], str)

    def test_has_description(self, plugin_json):
        """plugin.json must have description field."""
        assert "description" in plugin_json
        assert isinstance(plugin_json["description"], str)


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


class TestCommands:
    """Test command files."""

    EXPECTED_COMMANDS = [
        "cco-checkup.md",
        "cco-commit.md",
        "cco-config.md",
        "cco-optimize.md",
        "cco-preflight.md",
        "cco-research.md",
        "cco-review.md",
        "cco-status.md",
    ]

    def test_all_commands_exist(self):
        """All expected command files must exist."""
        commands_dir = ROOT / "commands"
        for cmd in self.EXPECTED_COMMANDS:
            assert (commands_dir / cmd).exists(), f"Missing command: {cmd}"

    def test_command_count(self):
        """Must have exactly 8 commands."""
        commands_dir = ROOT / "commands"
        md_files = list(commands_dir.glob("*.md"))
        assert len(md_files) == 8, f"Expected 8 commands, found {len(md_files)}"

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
    """Test rule files."""

    def test_core_rules_exist(self):
        """core.md must exist."""
        assert (ROOT / "rules" / "core.md").exists()

    def test_ai_rules_exist(self):
        """ai.md must exist."""
        assert (ROOT / "rules" / "ai.md").exists()

    def test_rule_file_count(self):
        """Must have exactly 62 rule files."""
        rules_dir = ROOT / "rules"
        md_files = list(rules_dir.glob("*.md"))
        assert len(md_files) == 62, f"Expected 62 rule files, found {len(md_files)}"

    def test_rule_format_consistency(self):
        """All rules should follow - **Name**: Description format."""
        import re

        rules_dir = ROOT / "rules"
        # Pattern includes numbers for rules like 3-Question-Guard, 80/20-Priority
        rule_pattern = re.compile(r"^- \*\*[A-Za-z0-9].*\*\*:")

        # Known non-rule patterns that use bold syntax (prefix match)
        exception_prefixes = ("- **Skipped**",)

        errors = []
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text(encoding="utf-8")
            for i, line in enumerate(content.split("\n"), 1):
                # Check lines that look like rules but don't match pattern
                if line.startswith("- **") and not rule_pattern.match(line):
                    # Allow table rows, non-rule bullets, and known exceptions
                    is_exception = any(line.startswith(p) for p in exception_prefixes)
                    if "**:" not in line and "| " not in line and not is_exception:
                        errors.append(f"{rule_file.name}:{i}: {line[:60]}")

        assert not errors, f"Invalid rule format:\n" + "\n".join(errors[:10])


class TestRuleCounts:
    """Test rule counts match documentation."""

    def count_rules_in_file(self, filepath: Path) -> int:
        """Count rules in a file using grep pattern."""
        import re

        content = filepath.read_text(encoding="utf-8")
        # Include numbers for rules like 3-Question-Guard, 80/20-Priority
        pattern = re.compile(r"^- \*\*[A-Za-z0-9]", re.MULTILINE)
        return len(pattern.findall(content))

    def test_core_rule_count(self):
        """core.md should have 141 rules."""
        count = self.count_rules_in_file(ROOT / "rules" / "core.md")
        assert count == 141, f"Expected 141 core rules, found {count}"

    def test_ai_rule_count(self):
        """ai.md should have 68 rules."""
        count = self.count_rules_in_file(ROOT / "rules" / "ai.md")
        assert count == 68, f"Expected 68 AI rules, found {count}"

    def test_total_rule_count(self):
        """Total rules should be 1364."""
        rules_dir = ROOT / "rules"
        total = sum(
            self.count_rules_in_file(f) for f in rules_dir.glob("*.md")
        )
        assert total == 1364, f"Expected 1364 total rules, found {total}"

    def test_adaptive_rule_count(self):
        """Adaptive rules (excluding core+ai) should be 1155."""
        rules_dir = ROOT / "rules"
        total = sum(
            self.count_rules_in_file(f)
            for f in rules_dir.glob("*.md")
            if f.name not in ("core.md", "ai.md")
        )
        assert total == 1155, f"Expected 1155 adaptive rules, found {total}"
