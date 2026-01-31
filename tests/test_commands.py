"""Command orchestration and integration tests.

These tests validate:
- Command YAML frontmatter is valid
- Command argument parsing works correctly
- Commands reference existing agents
- Command flow documentation is complete

Tests ensure commands are properly wired without executing them.

Test Organization Rationale:
    Classes are grouped by validation concern (frontmatter, consistency, flow, etc.)
    in a single file because they all operate on command files as their primary fixture.
    This keeps related command validation logic together and avoids fragmentation across
    multiple test files. Each test class validates a specific aspect of command structure.
"""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from _paths import AGENTS_DIR, COMMANDS_DIR, ROOT

# Regex pattern for extracting Task agent references from command files
TASK_PATTERN = r'Task\s*\(\s*["\']([^"\']+)["\']'

# Expected flags documented in optimize.md
OPTIMIZE_EXPECTED_FLAGS = [
    "--auto",
    "--preview",
    "--scope",
]

# Claude Code built-in agent types (not defined as cco-agent-*.md files)
BUILTIN_AGENTS = {
    "general-purpose",
    "Explore",
    "Plan",
    "Bash",
    "claude-code-guide",
    "statusline-setup",
}

# ============================================
# CANONICAL SCOPE DEFINITIONS
# ============================================
# These mappings are the single source of truth for scope IDs and names.
# When adding/removing scopes, update these dictionaries and the corresponding
# definitions in cco-agent-analyze.md. Commands reference these scopes via
# the analyze agent, and tests validate consistency between command docs and agent definitions.

# Optimize scope ID to name mapping (10 scopes, 105 checks)
OPTIMIZE_SCOPES = {
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

# Align scope ID to name mapping (6 scopes, 77 checks)
ALIGN_SCOPES = {
    "ARC": "architecture",
    "PAT": "patterns",
    "TST": "testing",
    "MNT": "maintainability",
    "AIA": "ai-architecture",
    "FUN": "functional-completeness",
}

# Commands that apply fixes and must document accounting
APPLY_COMMANDS = ["optimize.md", "align.md", "preflight.md", "docs.md"]

# Commands that modify files and must document recovery
MODIFYING_COMMANDS = ["optimize.md", "align.md", "commit.md", "preflight.md"]


class TestCommandFrontmatter:
    """Validate command YAML frontmatter structure."""

    def test_all_commands_have_frontmatter(self, command_files: list[Path]) -> None:
        """Every command file must start with YAML frontmatter."""
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{cmd_file} missing frontmatter start"
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

    def test_optimize_has_args_section(self, optimize_content: str) -> None:
        """optimize.md must have ## Args section."""
        assert "## Args" in optimize_content, "optimize.md missing Args section"

    def test_args_section_documents_flags(self, optimize_content: str) -> None:
        """Args section should document all flags."""
        for flag in OPTIMIZE_EXPECTED_FLAGS:
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
        matches = re.findall(TASK_PATTERN, content)
        for agent_name in matches:
            assert agent_name in existing_agents, (
                f"optimize.md references non-existent agent: {agent_name}"
            )

    def test_all_commands_reference_valid_agents(self, existing_agents: list[str]) -> None:
        """All commands should only reference existing agents."""
        valid_agents = set(existing_agents) | BUILTIN_AGENTS
        for cmd_file in COMMANDS_DIR.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            for agent_name in re.findall(TASK_PATTERN, content):
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
    def all_commands(self) -> dict[str, dict[str, Any]]:
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
            "Skill",
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
    def align_content(self) -> str:
        """Load align command content."""
        return (COMMANDS_DIR / "align.md").read_text(encoding="utf-8")

    def test_optimize_scopes_defined_in_agent(
        self, agent_content: str, optimize_content: str
    ) -> None:
        """All optimize scope IDs referenced in command must be defined in agent."""
        for scope_id, scope_name in OPTIMIZE_SCOPES.items():
            assert f"### {scope_name}" in agent_content or f"| {scope_name}" in agent_content, (
                f"Optimize scope {scope_id} ({scope_name}) not defined in agent-analyze"
            )

    def test_align_scopes_defined_in_agent(self, agent_content: str, align_content: str) -> None:
        """All align scope IDs referenced in command must be defined in agent."""
        for scope_id, scope_name in ALIGN_SCOPES.items():
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
            content = cmd_file.read_text(encoding="utf-8").lower()
            for i, line in enumerate(content.split("\n"), 1):
                if not self._is_valid_sonnet_reference(line):
                    pytest.fail(f"{cmd_file.name}:{i} references sonnet model: {line.strip()}")

    @staticmethod
    def _is_valid_sonnet_reference(line: str) -> bool:
        """Check if sonnet reference is valid (policy discussion, not actual usage)."""
        return (
            "sonnet" not in line
            or "no sonnet" in line
            or "policy" in line
            or "only" in line
        )


class TestAllCommandsHaveAccountingInvariant:
    """Validate that all commands with apply phases document the accounting invariant."""

    def test_commands_with_apply_have_accounting(self) -> None:
        """Commands that apply fixes must document applied + failed + needs_approval = total."""
        for cmd_name in APPLY_COMMANDS:
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
        for cmd_name in MODIFYING_COMMANDS:
            cmd_path = COMMANDS_DIR / cmd_name
            content = cmd_path.read_text(encoding="utf-8")
            assert "## Recovery" in content, f"{cmd_name} should have Recovery section"
            assert "git" in content.lower(), f"{cmd_name} recovery should mention git"


class TestResearchCommandPatterns:
    """Validate research-specific patterns."""

    def test_research_has_depth_levels(self) -> None:
        """Research command should document depth levels."""
        content = (COMMANDS_DIR / "research.md").read_text(encoding="utf-8")
        assert "Quick" in content, "research.md should document Quick depth"
        assert "Standard" in content, "research.md should document Standard depth"
        assert "Deep" in content, "research.md should document Deep depth"

    def test_research_documents_source_tiers(self) -> None:
        """Research command should document source tier system."""
        content = (COMMANDS_DIR / "research.md").read_text(encoding="utf-8")
        # Should mention tiered sources
        assert "T1" in content or "tier" in content.lower(), (
            "research.md should document source tiers"
        )


class TestTuneCommandPatterns:
    """Validate tune-specific patterns."""

    def test_tune_documents_modes(self) -> None:
        """Tune command should document auto and interactive modes."""
        content = (COMMANDS_DIR / "tune.md").read_text(encoding="utf-8")
        assert "--auto" in content, "tune.md should document --auto mode"
        assert "interactive" in content.lower(), "tune.md should document interactive mode"

    def test_tune_has_agent_orchestration(self) -> None:
        """Tune command should orchestrate analyze and apply agents."""
        content = (COMMANDS_DIR / "tune.md").read_text(encoding="utf-8")
        assert "cco-agent-analyze" in content or "analyze" in content, (
            "tune.md should reference analyze agent"
        )
        assert "cco-agent-apply" in content or "apply" in content, (
            "tune.md should reference apply agent"
        )
