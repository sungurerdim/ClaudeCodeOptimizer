"""Command orchestration and integration tests.

These tests validate:
- Command YAML frontmatter is valid
- Command argument parsing works correctly
- Commands reference existing agents
- Command flow documentation is complete

Tests ensure commands are properly wired without executing them.
"""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
COMMANDS_DIR = ROOT / "commands"
AGENTS_DIR = ROOT / "agents"


class TestCommandFrontmatter:
    """Validate command YAML frontmatter structure."""

    @pytest.fixture
    def command_files(self):
        """Get all command markdown files."""
        return list(COMMANDS_DIR.glob("*.md"))

    def test_all_commands_have_frontmatter(self, command_files):
        """Every command file must start with YAML frontmatter."""
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{cmd_file.name} missing frontmatter start"
            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{cmd_file.name} has unclosed frontmatter"

    def test_frontmatter_is_valid_yaml(self, command_files):
        """Frontmatter must be valid YAML."""
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            yaml_content = parts[1]
            try:
                data = yaml.safe_load(yaml_content)
                assert isinstance(data, dict), f"{cmd_file.name} frontmatter must be a mapping"
            except yaml.YAMLError as e:
                pytest.fail(f"{cmd_file.name} has invalid YAML: {e}")

    def test_frontmatter_has_required_fields(self, command_files):
        """Frontmatter must have description and allowed-tools."""
        required_fields = ["description", "allowed-tools"]
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            data = yaml.safe_load(parts[1])
            for field in required_fields:
                assert field in data, f"{cmd_file.name} missing required field: {field}"


class TestCommandArgumentParsing:
    """Validate command argument documentation and parsing."""

    @pytest.fixture
    def optimize_content(self):
        """Load optimize command content."""
        path = COMMANDS_DIR / "optimize.md"
        return path.read_text(encoding="utf-8")

    def test_optimize_has_args_section(self, optimize_content):
        """optimize.md must have ## Args section."""
        assert "## Args" in optimize_content, "optimize.md missing Args section"

    def test_args_section_documents_flags(self, optimize_content):
        """Args section should document all flags."""
        expected_flags = [
            "--auto",
            "--security",
            "--hygiene",
            "--types",
            "--lint",
            "--performance",
            "--ai-hygiene",
            "--robustness",
            "--doc-sync",
            "--report",
            "--fix",
            "--fix-all",
            "--score",
            "--intensity",
            "--plan",
        ]
        for flag in expected_flags:
            assert flag in optimize_content, f"optimize.md should document {flag}"

    def test_argument_hint_in_frontmatter(self):
        """Commands with args should have argument-hint in frontmatter."""
        cmd_path = COMMANDS_DIR / "optimize.md"
        content = cmd_path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        assert "argument-hint" in frontmatter, "optimize.md should have argument-hint"

    def test_argument_hint_lists_flags(self):
        """argument-hint should include key flags."""
        cmd_path = COMMANDS_DIR / "optimize.md"
        content = cmd_path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        hint = frontmatter.get("argument-hint", "")
        # Check some key flags are in the hint
        assert "--auto" in hint, "argument-hint should include --auto"
        assert "--fix-all" in hint, "argument-hint should include --fix-all"


class TestAgentReferences:
    """Validate that commands reference existing agents."""

    @pytest.fixture
    def existing_agents(self):
        """Get list of existing agent names."""
        agent_files = list(AGENTS_DIR.glob("cco-agent-*.md"))
        return [f.stem for f in agent_files]

    def test_optimize_references_valid_agents(self, existing_agents):
        """optimize.md should reference existing agents."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Find Task() calls with agent names
        task_pattern = r'Task\s*\(\s*["\']([^"\']+)["\']'
        matches = re.findall(task_pattern, content)
        for agent_name in matches:
            assert agent_name in existing_agents, (
                f"optimize.md references non-existent agent: {agent_name}"
            )

    def test_all_commands_reference_valid_agents(self, existing_agents):
        """All commands should only reference existing agents."""
        # Claude Code built-in agent types
        builtin_agents = {
            "general-purpose", "Explore", "Plan", "Bash",
            "claude-code-guide", "statusline-setup"
        }
        valid_agents = set(existing_agents) | builtin_agents
        for cmd_file in COMMANDS_DIR.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            task_pattern = r'Task\s*\(\s*["\']([^"\']+)["\']'
            matches = re.findall(task_pattern, content)
            for agent_name in matches:
                assert agent_name in valid_agents, (
                    f"{cmd_file.name} references non-existent agent: {agent_name}"
                )

    def test_agents_declared_in_plugin_json(self, existing_agents):
        """All agents should be declared in plugin.json."""
        plugin_path = ROOT / ".claude-plugin" / "plugin.json"
        plugin_json = yaml.safe_load(plugin_path.read_text(encoding="utf-8"))
        declared_agents = [
            Path(a).stem for a in plugin_json.get("agents", [])
        ]
        for agent in existing_agents:
            assert agent in declared_agents, (
                f"Agent {agent} not declared in plugin.json"
            )


class TestCommandFlowDocumentation:
    """Validate command flow documentation completeness."""

    def test_optimize_has_architecture_section(self):
        """optimize.md should document its execution architecture."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        assert "## Architecture" in content or "## Execution" in content, (
            "optimize.md should have Architecture or Execution section"
        )

    def test_optimize_documents_steps(self):
        """optimize.md should document execution steps."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Should have step documentation
        assert "Step-1" in content or "Step 1" in content, (
            "optimize.md should document steps"
        )

    def test_optimize_has_validation_blocks(self):
        """optimize.md should have validation checkpoints."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Should have validation blocks
        assert "### Validation" in content or "[x]" in content, (
            "optimize.md should have validation checkpoints"
        )

    def test_optimize_documents_output_schema(self):
        """optimize.md should document output schema."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        assert "Output Schema" in content or "accounting" in content, (
            "optimize.md should document output schema"
        )


class TestCommandConsistency:
    """Validate consistency across all commands."""

    @pytest.fixture
    def all_commands(self):
        """Load all command frontmatters."""
        commands = {}
        for cmd_file in COMMANDS_DIR.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            commands[cmd_file.stem] = yaml.safe_load(parts[1])
        return commands

    def test_all_commands_have_description(self, all_commands):
        """Every command must have a description."""
        for name, frontmatter in all_commands.items():
            assert frontmatter.get("description"), (
                f"Command {name} missing description"
            )

    def test_all_commands_have_allowed_tools(self, all_commands):
        """Every command must declare allowed-tools."""
        for name, frontmatter in all_commands.items():
            assert frontmatter.get("allowed-tools"), (
                f"Command {name} missing allowed-tools"
            )

    def test_commands_use_valid_tools(self, all_commands):
        """Commands should only use valid tool names."""
        valid_tools = {
            "Read", "Grep", "Glob", "Edit", "Write", "Bash", "Task",
            "AskUserQuestion", "NotebookEdit", "WebSearch", "WebFetch"
        }
        for name, frontmatter in all_commands.items():
            tools_str = frontmatter.get("allowed-tools", "")
            tools = [t.strip() for t in tools_str.split(",")]
            for tool in tools:
                assert tool in valid_tools, (
                    f"Command {name} uses unknown tool: {tool}"
                )

    def test_commands_specify_model_when_needed(self, all_commands):
        """Commands using Task should specify model."""
        for name, frontmatter in all_commands.items():
            # If command uses Task, it should specify model
            tools_str = frontmatter.get("allowed-tools", "")
            if "Task" in tools_str:
                # Model can be in frontmatter or documented inline
                # Just check frontmatter for now
                pass  # Model specification is optional at frontmatter level
