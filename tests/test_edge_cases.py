"""Edge case and error handling tests.

These tests validate:
- Invalid argument combinations are rejected
- Profile exists and is valid
- Hook JSON structure is correct
- Schema files exist and are valid
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


class TestInvalidArgumentCombinations:
    """Validate that conflicting argument combinations are detected."""

    @pytest.fixture
    def schema(self) -> dict | None:
        """Load the optimize command schema."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        if schema_path.exists():
            return json.loads(schema_path.read_text(encoding="utf-8"))
        return None

    def test_preview_and_auto_mutually_exclusive(self, schema: dict | None) -> None:
        """--preview and --auto cannot be used together."""
        # These flags have opposite intents: preview only vs fix everything
        assert schema is not None, "Schema file must exist"

        # The schema should define this constraint in allOf
        all_of = schema.get("allOf", [])
        has_constraint = any(
            "preview" in str(constraint) and "auto" in str(constraint) for constraint in all_of
        )
        assert has_constraint, "Schema should define preview/auto mutual exclusivity"

    def test_schema_has_no_removed_flags(self, schema: dict | None) -> None:
        """Schema should not have --score or --fix-all (removed flags)."""
        assert schema is not None, "Schema file must exist"
        props = schema.get("properties", {})
        assert "score" not in props, "Schema should not have score property"
        assert "fix-all" not in props, "Schema should not have fix-all property"
        assert "intensity" not in props, "Schema should not have intensity property"


class TestMissingProfileHandling:
    """Validate graceful handling when profile doesn't exist."""

    def test_actual_profile_exists_at_conventional_path(self) -> None:
        """Actual project profile should exist at .claude/rules/cco-profile.md."""
        profile_path = ROOT / ".claude" / "rules" / "cco-profile.md"
        assert profile_path.exists(), f"Profile not found at {profile_path}"

    def test_actual_profile_is_valid_markdown(self) -> None:
        """Actual project profile should be readable and non-empty."""
        profile_path = ROOT / ".claude" / "rules" / "cco-profile.md"
        if profile_path.exists():
            content = profile_path.read_text(encoding="utf-8")
            assert len(content) > 50, "Profile content is too short"
            assert "## Stack" in content or "## stack" in content.lower(), (
                "Profile should contain Stack section"
            )


class TestMalformedJsonHandling:
    """Validate detection of malformed JSON in hook files."""

    def test_core_rules_json_is_valid(self) -> None:
        """hooks/core-rules.json must be valid JSON."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        try:
            content = core_rules_path.read_text(encoding="utf-8")
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"core-rules.json is malformed: {e}")

    def test_hook_output_structure_validation(self) -> None:
        """Hook output must have required structure."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        data = json.loads(core_rules_path.read_text(encoding="utf-8"))

        # Required structure for Claude Code hooks
        assert "hookSpecificOutput" in data, "Missing hookSpecificOutput"
        output = data["hookSpecificOutput"]
        assert "hookEventName" in output, "Missing hookEventName"
        assert "additionalContext" in output, "Missing additionalContext"


class TestActualProfileValidation:
    """Validate actual project profile structure."""

    @pytest.fixture
    def profile_content(self) -> str:
        """Load actual profile content."""
        profile_path = ROOT / ".claude" / "rules" / "cco-profile.md"
        if not profile_path.exists():
            pytest.skip("Profile not found")
        return profile_path.read_text(encoding="utf-8")

    def test_profile_has_stack_section(self, profile_content: str) -> None:
        """Profile must document the project stack."""
        assert "## Stack" in profile_content, "Profile missing Stack section"

    def test_profile_has_language_info(self, profile_content: str) -> None:
        """Profile must list at least one language."""
        assert "Languages" in profile_content or "languages" in profile_content, (
            "Profile missing language information"
        )


class TestSchemaExistence:
    """Validate that schema files exist and are loadable."""

    def test_optimize_schema_exists(self) -> None:
        """optimize.schema.json must exist."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        assert schema_path.exists(), f"Schema not found: {schema_path}"

    def test_optimize_schema_is_valid_json(self) -> None:
        """optimize.schema.json must be valid JSON."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        if schema_path.exists():
            content = schema_path.read_text(encoding="utf-8")
            schema = json.loads(content)
            assert "$schema" in schema, "JSON Schema must have $schema field"
            assert "properties" in schema, "Schema must define properties"
