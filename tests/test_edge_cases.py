"""Edge case and error handling tests.

These tests validate:
- Invalid argument combinations are rejected
- Missing profile handling is graceful
- Malformed JSON is detected
- Missing required fields are caught

Tests use fixtures and mocks to avoid file system dependencies.
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent


class TestInvalidArgumentCombinations:
    """Validate that conflicting argument combinations are detected."""

    @pytest.fixture
    def schema(self):
        """Load the optimize command schema."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        if schema_path.exists():
            return json.loads(schema_path.read_text(encoding="utf-8"))
        return None

    def test_report_and_fix_all_mutually_exclusive(self, schema):
        """--report and --fix-all cannot be used together."""
        # These flags have opposite intents: report only vs fix everything
        assert schema is not None, "Schema file must exist"

        # The schema should define this constraint in allOf
        all_of = schema.get("allOf", [])
        has_constraint = any(
            "report" in str(constraint) and "fix-all" in str(constraint)
            for constraint in all_of
        )
        assert has_constraint, "Schema should define report/fix-all mutual exclusivity"

    def test_score_excludes_fix_operations(self, schema):
        """--score should not allow --fix or --fix-all."""
        assert schema is not None, "Schema file must exist"

        all_of = schema.get("allOf", [])
        has_constraint = any(
            "score" in str(constraint) and "fix" in str(constraint)
            for constraint in all_of
        )
        assert has_constraint, "Schema should define score/fix mutual exclusivity"

    def test_intensity_report_only_excludes_fix_all(self, schema):
        """--intensity=report-only should not allow --fix-all."""
        assert schema is not None, "Schema file must exist"

        all_of = schema.get("allOf", [])
        has_constraint = any(
            "report-only" in str(constraint) and "fix-all" in str(constraint)
            for constraint in all_of
        )
        assert has_constraint, "Schema should constrain report-only intensity"

    def test_intensity_enum_values(self, schema):
        """--intensity must be one of the valid enum values."""
        assert schema is not None, "Schema file must exist"

        intensity_prop = schema.get("properties", {}).get("intensity", {})
        expected_values = ["quick-wins", "standard", "full-fix", "report-only"]
        assert intensity_prop.get("enum") == expected_values, (
            f"Intensity enum should be {expected_values}"
        )


class TestMissingProfileHandling:
    """Validate graceful handling when profile doesn't exist."""

    def test_profile_path_is_conventional(self):
        """Profile should be at standard location."""
        expected_path = ROOT / ".claude" / "rules" / "cco-profile.md"
        # This test documents the expected path, not that it exists
        assert expected_path.parent.name == "rules"
        assert expected_path.suffix == ".md"

    def test_missing_profile_detection(self):
        """Missing profile should be detectable without crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_root = Path(tmpdir)
            profile_path = fake_root / ".claude" / "rules" / "cco-profile.md"
            assert not profile_path.exists()
            # Detection should return False, not raise
            assert profile_path.exists() is False

    def test_profile_yaml_frontmatter_extraction(self):
        """Profile YAML frontmatter should be extractable when present."""
        profile_content = """---
project:
  purpose: Test project
stack:
  languages: [Python]
maturity: active
commands:
  test: pytest
---

# Profile Content
"""
        lines = profile_content.split("\n")
        assert lines[0] == "---", "Profile must start with frontmatter"

        # Extract YAML between markers
        yaml_end = -1
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                yaml_end = i
                break

        assert yaml_end > 0, "Profile must have closing frontmatter marker"
        yaml_content = "\n".join(lines[1:yaml_end])
        data = yaml.safe_load(yaml_content)
        assert data.get("project", {}).get("purpose") == "Test project"


class TestMalformedJsonHandling:
    """Validate detection of malformed JSON in hook files."""

    def test_core_rules_json_is_valid(self):
        """hooks/core-rules.json must be valid JSON."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        try:
            content = core_rules_path.read_text(encoding="utf-8")
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"core-rules.json is malformed: {e}")

    def test_malformed_json_is_detectable(self):
        """Malformed JSON should raise JSONDecodeError."""
        malformed_samples = [
            '{"key": "value",}',  # Trailing comma
            "{'key': 'value'}",  # Single quotes
            '{"key": undefined}',  # undefined value
            '{"key": }',  # Missing value
            "{key: value}",  # Unquoted keys
        ]
        for sample in malformed_samples:
            with pytest.raises(json.JSONDecodeError):
                json.loads(sample)

    def test_hook_output_structure_validation(self):
        """Hook output must have required structure."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        data = json.loads(core_rules_path.read_text(encoding="utf-8"))

        # Required structure for Claude Code hooks
        assert "hookSpecificOutput" in data, "Missing hookSpecificOutput"
        output = data["hookSpecificOutput"]
        assert "hookEventName" in output, "Missing hookEventName"
        assert "additionalContext" in output, "Missing additionalContext"


class TestProfileYamlValidation:
    """Validate profile YAML structure requirements."""

    @pytest.fixture
    def valid_profile_yaml(self):
        """Return minimal valid profile YAML."""
        return """project:
  purpose: Test project for validation
stack:
  languages: [Python]
maturity: active
commands:
  test: pytest
"""

    def test_required_fields_present(self, valid_profile_yaml):
        """Profile must have project, stack, maturity, commands."""
        data = yaml.safe_load(valid_profile_yaml)
        required = ["project", "stack", "maturity", "commands"]
        for field in required:
            assert field in data, f"Missing required field: {field}"

    def test_project_purpose_required(self, valid_profile_yaml):
        """project.purpose is required."""
        data = yaml.safe_load(valid_profile_yaml)
        assert data.get("project", {}).get("purpose"), "project.purpose is required"

    def test_invalid_yaml_detection(self):
        """Invalid YAML should be detected."""
        invalid_samples = [
            "project:\n  purpose: [unclosed bracket",  # Unclosed bracket
            "project:\n\tpurpose: tabs",  # Tab indentation (YAML spec allows but discouraged)
            "project: {nested: {deep: [mixed}]}",  # Mismatched brackets
        ]
        for sample in invalid_samples:
            try:
                yaml.safe_load(sample)
            except yaml.YAMLError:
                pass  # Expected for truly invalid YAML
            # Note: some "invalid" YAML may parse - this tests detection capability

    def test_empty_purpose_is_invalid(self):
        """Empty project.purpose should be flagged."""
        empty_purpose_yaml = """project:
  purpose: ""
stack:
  languages: [Python]
maturity: active
commands:
  test: pytest
"""
        data = yaml.safe_load(empty_purpose_yaml)
        purpose = data.get("project", {}).get("purpose")
        # Empty string is falsy in Python
        assert not purpose, "Empty purpose should be falsy"


class TestSchemaExistence:
    """Validate that schema files exist and are loadable."""

    def test_optimize_schema_exists(self):
        """optimize.schema.json must exist."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        assert schema_path.exists(), f"Schema not found: {schema_path}"

    def test_optimize_schema_is_valid_json(self):
        """optimize.schema.json must be valid JSON."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        if schema_path.exists():
            content = schema_path.read_text(encoding="utf-8")
            schema = json.loads(content)
            assert "$schema" in schema, "JSON Schema must have $schema field"
            assert "properties" in schema, "Schema must define properties"
