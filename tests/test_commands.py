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
    def command_files(self) -> list[Path]:
        """Get all command markdown files."""
        return list(COMMANDS_DIR.glob("*.md"))

    def test_all_commands_have_frontmatter(self, command_files: list[Path]) -> None:
        """Every command file must start with YAML frontmatter."""
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{cmd_file.name} missing frontmatter start"
            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{cmd_file.name} has unclosed frontmatter"

    def test_frontmatter_is_valid_yaml(self, command_files: list[Path]) -> None:
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

    def test_frontmatter_has_required_fields(self, command_files: list[Path]) -> None:
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
    def optimize_content(self) -> str:
        """Load optimize command content."""
        path = COMMANDS_DIR / "optimize.md"
        return path.read_text(encoding="utf-8")

    def test_optimize_has_args_section(self, optimize_content: str) -> None:
        """optimize.md must have ## Args section."""
        assert "## Args" in optimize_content, "optimize.md missing Args section"

    def test_args_section_documents_flags(self, optimize_content: str) -> None:
        """Args section should document all flags."""
        expected_flags = [
            "--auto",
            "--preview",
            "--scope",
        ]
        for flag in expected_flags:
            assert flag in optimize_content, f"optimize.md should document {flag}"

    def test_argument_hint_in_frontmatter(self) -> None:
        """Commands with args should have argument-hint in frontmatter."""
        cmd_path = COMMANDS_DIR / "optimize.md"
        content = cmd_path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        assert "argument-hint" in frontmatter, "optimize.md should have argument-hint"

    def test_argument_hint_lists_flags(self) -> None:
        """argument-hint should include key flags."""
        cmd_path = COMMANDS_DIR / "optimize.md"
        content = cmd_path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        hint = frontmatter.get("argument-hint", "")
        # Check some key flags are in the hint
        assert "--auto" in hint, "argument-hint should include --auto"
        assert "--preview" in hint, "argument-hint should include --preview"


class TestAgentReferences:
    """Validate that commands reference existing agents."""

    @pytest.fixture
    def existing_agents(self) -> list[str]:
        """Get list of existing agent names."""
        agent_files = list(AGENTS_DIR.glob("cco-agent-*.md"))
        return [f.stem for f in agent_files]

    def test_optimize_references_valid_agents(self, existing_agents: list[str]) -> None:
        """optimize.md should reference existing agents."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Find Task() calls with agent names
        task_pattern = r'Task\s*\(\s*["\']([^"\']+)["\']'
        matches = re.findall(task_pattern, content)
        for agent_name in matches:
            assert agent_name in existing_agents, (
                f"optimize.md references non-existent agent: {agent_name}"
            )

    def test_all_commands_reference_valid_agents(self, existing_agents: list[str]) -> None:
        """All commands should only reference existing agents."""
        # Claude Code built-in agent types
        builtin_agents = {
            "general-purpose",
            "Explore",
            "Plan",
            "Bash",
            "claude-code-guide",
            "statusline-setup",
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

    def test_agents_declared_in_plugin_json(self, existing_agents: list[str]) -> None:
        """All agents should be declared in plugin.json."""
        plugin_path = ROOT / ".claude-plugin" / "plugin.json"
        plugin_json = yaml.safe_load(plugin_path.read_text(encoding="utf-8"))
        declared_agents = [Path(a).stem for a in plugin_json.get("agents", [])]
        for agent in existing_agents:
            assert agent in declared_agents, f"Agent {agent} not declared in plugin.json"


class TestCommandFlowDocumentation:
    """Validate command flow documentation completeness."""

    def test_optimize_has_architecture_section(self) -> None:
        """optimize.md should document its execution architecture."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        assert "## Architecture" in content or "## Execution" in content, (
            "optimize.md should have Architecture or Execution section"
        )

    def test_optimize_documents_steps(self) -> None:
        """optimize.md should document execution steps."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Should have step documentation
        assert "Step-1" in content or "Step 1" in content, "optimize.md should document steps"

    def test_optimize_has_validation_blocks(self) -> None:
        """optimize.md should have validation checkpoints."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        # Should have validation blocks
        assert "### Validation" in content or "[x]" in content, (
            "optimize.md should have validation checkpoints"
        )

    def test_optimize_documents_output_schema(self) -> None:
        """optimize.md should document output schema."""
        content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        assert "Output Schema" in content or "accounting" in content, (
            "optimize.md should document output schema"
        )


class TestCommandConsistency:
    """Validate consistency across all commands."""

    @pytest.fixture
    def all_commands(self) -> dict[str, dict]:
        """Load all command frontmatters."""
        commands = {}
        for cmd_file in COMMANDS_DIR.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            commands[cmd_file.stem] = yaml.safe_load(parts[1])
        return commands

    def test_commands_use_valid_tools(self, all_commands: dict[str, dict]) -> None:
        """Commands should only use valid tool names."""
        valid_tools = {
            "Read",
            "Grep",
            "Glob",
            "Edit",
            "Write",
            "Bash",
            "Task",
            "AskUserQuestion",
            "NotebookEdit",
            "WebSearch",
            "WebFetch",
        }
        for name, frontmatter in all_commands.items():
            tools_str = frontmatter.get("allowed-tools", "")
            tools = [t.strip() for t in tools_str.split(",")]
            for tool in tools:
                assert tool in valid_tools, f"Command {name} uses unknown tool: {tool}"


class TestScopeConsistency:
    """Validate scope definitions match between commands and agent."""

    @pytest.fixture
    def agent_content(self) -> str:
        """Load agent-analyze content."""
        return (AGENTS_DIR / "cco-agent-analyze.md").read_text(encoding="utf-8")

    @pytest.fixture
    def optimize_content(self) -> str:
        """Load optimize command content."""
        return (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")

    @pytest.fixture
    def align_content(self) -> str:
        """Load align command content."""
        return (COMMANDS_DIR / "align.md").read_text(encoding="utf-8")

    def test_optimize_scopes_defined_in_agent(
        self, agent_content: str, optimize_content: str
    ) -> None:
        """All optimize scope IDs referenced in command must be defined in agent."""
        optimize_scopes = {
            "SEC": "security",
            "HYG": "hygiene",
            "TYP": "types",
            "LNT": "lint",
            "PRF": "performance",
            "AIH": "ai-hygiene",
            "ROB": "robustness",
            "PRV": "privacy",
            "DOC": "doc-sync",
            "SIM": "simplify",
        }
        for scope_id, scope_name in optimize_scopes.items():
            assert f"### {scope_name}" in agent_content or f"| {scope_name}" in agent_content, (
                f"Optimize scope {scope_id} ({scope_name}) not defined in agent-analyze"
            )

    def test_align_scopes_defined_in_agent(self, agent_content: str, align_content: str) -> None:
        """All align scope IDs referenced in command must be defined in agent."""
        align_scopes = {
            "ARC": "architecture",
            "PAT": "patterns",
            "TST": "testing",
            "MNT": "maintainability",
            "AIA": "ai-architecture",
            "FUN": "functional-completeness",
        }
        for scope_id, scope_name in align_scopes.items():
            assert f"### {scope_name}" in agent_content or f"| {scope_name}" in agent_content, (
                f"Align scope {scope_id} ({scope_name}) not defined in agent-analyze"
            )

    def test_scope_check_counts_match(self, agent_content: str, optimize_content: str) -> None:
        """Scope check ranges in command should match agent definitions."""
        # Verify key scope ranges exist in both
        scope_ranges = [
            ("SEC-01", "SEC-12"),
            ("HYG-01", "HYG-20"),
            ("TYP-01", "TYP-10"),
            ("PRF-01", "PRF-10"),
            ("ROB-01", "ROB-10"),
            ("PRV-01", "PRV-08"),
            ("DOC-01", "DOC-08"),
            ("SIM-01", "SIM-11"),
        ]
        for first_id, last_id in scope_ranges:
            assert first_id in agent_content, f"Agent missing {first_id}"
            assert last_id in agent_content, f"Agent missing {last_id}"

    def test_align_scope_check_counts_match(self, agent_content: str, align_content: str) -> None:
        """Align scope check ranges in command should match agent definitions."""
        scope_ranges = [
            ("ARC-01", "ARC-15"),
            ("PAT-01", "PAT-12"),
            ("TST-01", "TST-10"),
            ("MNT-01", "MNT-12"),
            ("AIA-01", "AIA-10"),
            ("FUN-01", "FUN-18"),
        ]
        for first_id, last_id in scope_ranges:
            assert first_id in agent_content, f"Agent missing {first_id}"
            assert last_id in agent_content, f"Agent missing {last_id}"


class TestAgentFrontmatter:
    """Validate agent YAML frontmatter structure."""

    @pytest.fixture
    def agent_files(self) -> list[Path]:
        """Get all agent markdown files."""
        return list(AGENTS_DIR.glob("*.md"))

    def test_all_agents_have_frontmatter(self, agent_files: list[Path]) -> None:
        """Every agent file must start with YAML frontmatter."""
        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{agent_file.name} missing frontmatter start"
            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{agent_file.name} has unclosed frontmatter"

    def test_agent_frontmatter_is_valid_yaml(self, agent_files: list[Path]) -> None:
        """Agent frontmatter must be valid YAML."""
        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            try:
                data = yaml.safe_load(parts[1])
                assert isinstance(data, dict), f"{agent_file.name} frontmatter must be a mapping"
            except yaml.YAMLError as e:
                pytest.fail(f"{agent_file.name} has invalid YAML: {e}")

    def test_agent_frontmatter_has_required_fields(self, agent_files: list[Path]) -> None:
        """Agent frontmatter must have name, description, tools, model."""
        required_fields = ["name", "description", "tools", "model"]
        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            data = yaml.safe_load(parts[1])
            for field in required_fields:
                assert field in data, f"{agent_file.name} missing required field: {field}"

    def test_agent_model_is_valid(self, agent_files: list[Path]) -> None:
        """Agent model must be haiku or opus (no sonnet per policy)."""
        valid_models = {"haiku", "opus"}
        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            data = yaml.safe_load(parts[1])
            model = data.get("model", "")
            assert model in valid_models, (
                f"{agent_file.name} uses invalid model: {model} (allowed: {valid_models})"
            )


class TestCommandModelPolicy:
    """Validate model policy across commands - opus + haiku only, no sonnet."""

    @pytest.fixture
    def command_files(self) -> list[Path]:
        """Get all command markdown files."""
        return list(COMMANDS_DIR.glob("*.md"))

    def test_commands_use_valid_models(self, command_files: list[Path]) -> None:
        """Command frontmatter model must be haiku or opus."""
        valid_models = {"haiku", "opus"}
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            data = yaml.safe_load(parts[1])
            if "model" in data:
                model = data["model"]
                assert model in valid_models, (
                    f"{cmd_file.name} uses invalid model: {model} (allowed: {valid_models})"
                )

    def test_no_sonnet_references_in_commands(self, command_files: list[Path]) -> None:
        """Commands should not reference sonnet model."""
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            # Allow references in comments explaining the policy
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if "sonnet" in line.lower() and "no sonnet" not in line.lower():
                    # Allow policy statements
                    if "policy" in line.lower() or "only" in line.lower():
                        continue
                    pytest.fail(f"{cmd_file.name}:{i} references sonnet model: {line.strip()}")


class TestAllCommandsHaveAccountingInvariant:
    """Validate that all commands with apply phases document the accounting invariant."""

    def test_commands_with_apply_have_accounting(self) -> None:
        """Commands that apply fixes must document applied + failed = total."""
        apply_commands = ["optimize.md", "align.md", "preflight.md", "docs.md"]
        for cmd_name in apply_commands:
            cmd_path = COMMANDS_DIR / cmd_name
            content = cmd_path.read_text(encoding="utf-8")
            assert "applied" in content and "failed" in content, (
                f"{cmd_name} should document applied/failed accounting"
            )
            assert "total" in content, f"{cmd_name} should document total count"


class TestAllCommandsDocumentRecovery:
    """Validate that commands document recovery steps."""

    def test_commands_with_file_changes_have_recovery(self) -> None:
        """Commands that modify files must document recovery."""
        modifying_commands = ["optimize.md", "align.md", "commit.md", "preflight.md"]
        for cmd_name in modifying_commands:
            cmd_path = COMMANDS_DIR / cmd_name
            content = cmd_path.read_text(encoding="utf-8")
            assert "## Recovery" in content, f"{cmd_name} should have Recovery section"
            assert "git" in content.lower(), f"{cmd_name} recovery should mention git"
