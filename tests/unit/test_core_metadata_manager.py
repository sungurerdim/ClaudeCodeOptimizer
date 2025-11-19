"""
Unit tests for MetadataManager

Tests centralized metadata parsing, use_cases extraction, context matching,
and file recommendation logic.
Target Coverage: 100%
"""

import tempfile
from pathlib import Path

import pytest

from claudecodeoptimizer.core.metadata_manager import MetadataManager, metadata_manager


class TestMetadataManagerSingleton:
    """Test singleton pattern implementation"""

    def test_singleton_returns_same_instance(self) -> None:
        """Test that multiple instantiations return same object"""
        manager1 = MetadataManager()
        manager2 = MetadataManager()
        assert manager1 is manager2

    def test_module_level_instance_is_singleton(self) -> None:
        """Test that module-level metadata_manager is singleton instance"""
        manager = MetadataManager()
        assert manager is metadata_manager


class TestParseFrontmatter:
    """Test parse_frontmatter method"""

    def test_valid_frontmatter(self) -> None:
        """Test parsing valid YAML frontmatter"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test File
description: A test description
category: testing
tags:
  - unit
  - test
---

# Content here
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)

        assert result["title"] == "Test File"
        assert result["description"] == "A test description"
        assert result["category"] == "testing"
        assert result["tags"] == ["unit", "test"]

        path.unlink()

    def test_frontmatter_with_use_cases(self) -> None:
        """Test parsing frontmatter with use_cases dict"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Skill File
use_cases:
  project_maturity:
    - production
    - legacy
  team_dynamics:
    - small-2-5
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)

        assert result["title"] == "Skill File"
        assert result["use_cases"]["project_maturity"] == ["production", "legacy"]
        assert result["use_cases"]["team_dynamics"] == ["small-2-5"]

        path.unlink()

    def test_file_not_found(self) -> None:
        """Test parsing non-existent file returns empty dict"""
        manager = MetadataManager()
        result = manager.parse_frontmatter(Path("/nonexistent/file.md"))
        assert result == {}

    def test_no_frontmatter(self) -> None:
        """Test parsing file without frontmatter returns empty dict"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Just content\n\nNo frontmatter here.")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)
        assert result == {}

        path.unlink()

    def test_empty_frontmatter(self) -> None:
        """Test parsing file with empty frontmatter returns empty dict"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)
        assert result == {}

        path.unlink()

    def test_nested_metadata(self) -> None:
        """Test parsing frontmatter with nested values"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Nested Test
metadata:
  author: Test Author
  version: 1.0
  config:
    enabled: true
    threshold: 0.8
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)

        assert result["metadata"]["author"] == "Test Author"
        assert result["metadata"]["version"] == 1.0
        assert result["metadata"]["config"]["enabled"] is True
        assert result["metadata"]["config"]["threshold"] == 0.8

        path.unlink()

    def test_invalid_yaml_returns_empty(self) -> None:
        """Test that invalid YAML returns empty dict gracefully"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
invalid: yaml: content: [broken
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.parse_frontmatter(path)
        assert result == {}

        path.unlink()


class TestGetDescription:
    """Test get_description method"""

    def test_description_from_frontmatter(self) -> None:
        """Test getting description from frontmatter field"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
description: This is the description from frontmatter
---

# Content
This is content, not description.
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert result == "This is the description from frontmatter"

        path.unlink()

    def test_description_from_first_paragraph(self) -> None:
        """Test fallback to first paragraph when no frontmatter description"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
---

# Heading

This is the first paragraph that should be used as description.

This is the second paragraph.
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert "first paragraph" in result

        path.unlink()

    def test_description_truncated_to_100_chars(self) -> None:
        """Test that first paragraph description is truncated to 100 chars"""
        long_text = "A" * 200
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(f"""---
title: Test
---

{long_text}
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert len(result) == 100

        path.unlink()

    def test_description_empty_file(self) -> None:
        """Test getting description from empty file returns empty string"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert result == ""

        path.unlink()

    def test_description_nonexistent_file(self) -> None:
        """Test getting description from non-existent file returns empty string"""
        manager = MetadataManager()
        result = manager.get_description(Path("/nonexistent/file.md"))
        assert result == ""

    def test_description_skips_headings(self) -> None:
        """Test that headings are skipped when finding first paragraph"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
---

# Heading 1
## Heading 2
### Heading 3

Actual paragraph content here.
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert "Actual paragraph" in result
        assert "#" not in result

        path.unlink()

    def test_description_multiline_paragraph(self) -> None:
        """Test that multiline paragraphs are joined with spaces"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
---

Line one of paragraph.
Line two of paragraph.

Second paragraph.
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)
        assert "Line one" in result
        assert "Line two" in result
        assert " " in result  # Joined with space

        path.unlink()


class TestGetUseCases:
    """Test get_use_cases method"""

    def test_valid_use_cases(self) -> None:
        """Test extracting use_cases from frontmatter"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
use_cases:
  development_philosophy:
    - quality_first
  project_maturity:
    - production
    - legacy
  team_dynamics:
    - small-2-5
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_use_cases(path)

        assert result["development_philosophy"] == ["quality_first"]
        assert result["project_maturity"] == ["production", "legacy"]
        assert result["team_dynamics"] == ["small-2-5"]

        path.unlink()

    def test_empty_use_cases(self) -> None:
        """Test file without use_cases returns empty dict"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
description: No use_cases here
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_use_cases(path)
        assert result == {}

        path.unlink()

    def test_invalid_use_cases_type(self) -> None:
        """Test that non-dict use_cases returns empty dict"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
use_cases: not_a_dict
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_use_cases(path)
        assert result == {}

        path.unlink()

    def test_use_cases_with_non_list_values(self) -> None:
        """Test that non-list values in use_cases are converted to empty lists"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
use_cases:
  valid_key:
    - value1
  invalid_key: not_a_list
---

Content
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_use_cases(path)

        assert result["valid_key"] == ["value1"]
        assert result["invalid_key"] == []

        path.unlink()

    def test_use_cases_nonexistent_file(self) -> None:
        """Test getting use_cases from non-existent file returns empty dict"""
        manager = MetadataManager()
        result = manager.get_use_cases(Path("/nonexistent/file.md"))
        assert result == {}


class TestMatchesContext:
    """Test matches_context method"""

    def test_single_match(self) -> None:
        """Test matching with single criterion match"""
        manager = MetadataManager()
        use_cases = {"project_maturity": ["production"]}
        context = {"project_maturity": "production"}

        assert manager.matches_context(use_cases, context) is True

    def test_no_match(self) -> None:
        """Test no match when criteria don't align"""
        manager = MetadataManager()
        use_cases = {"project_maturity": ["production"]}
        context = {"project_maturity": "prototype"}

        assert manager.matches_context(use_cases, context) is False

    def test_multiple_criteria_one_matches(self) -> None:
        """Test that ANY matching criterion returns True"""
        manager = MetadataManager()
        use_cases = {
            "project_maturity": ["production"],
            "team_dynamics": ["small-2-5"],
        }
        context = {
            "project_maturity": "prototype",  # No match
            "team_dynamics": "small-2-5",  # Match!
        }

        assert manager.matches_context(use_cases, context) is True

    def test_list_context_answer(self) -> None:
        """Test matching when context answer is a list"""
        manager = MetadataManager()
        use_cases = {"project_purpose": ["backend", "api"]}
        context = {"project_purpose": ["backend", "cli"]}

        assert manager.matches_context(use_cases, context) is True

    def test_list_context_no_match(self) -> None:
        """Test no match when list answer has no overlap"""
        manager = MetadataManager()
        use_cases = {"project_purpose": ["backend", "api"]}
        context = {"project_purpose": ["frontend", "mobile"]}

        assert manager.matches_context(use_cases, context) is False

    def test_empty_use_cases(self) -> None:
        """Test that empty use_cases returns False"""
        manager = MetadataManager()
        assert manager.matches_context({}, {"key": "value"}) is False

    def test_missing_context_key(self) -> None:
        """Test no match when context doesn't have the key"""
        manager = MetadataManager()
        use_cases = {"project_maturity": ["production"]}
        context = {"other_key": "value"}

        assert manager.matches_context(use_cases, context) is False

    def test_multiple_expected_values(self) -> None:
        """Test matching when use_cases has multiple expected values"""
        manager = MetadataManager()
        use_cases = {"project_maturity": ["production", "legacy", "mvp"]}
        context = {"project_maturity": "legacy"}

        assert manager.matches_context(use_cases, context) is True

    def test_none_context_value(self) -> None:
        """Test handling None value in context"""
        manager = MetadataManager()
        use_cases = {"project_maturity": ["production"]}
        context = {"project_maturity": None}

        assert manager.matches_context(use_cases, context) is False


class TestRecommendFiles:
    """Test recommend_files method"""

    def setup_method(self) -> None:
        """Set up test directory with mock files"""
        self.temp_dir = tempfile.mkdtemp()
        self.files_dir = Path(self.temp_dir)

    def teardown_method(self) -> None:
        """Clean up test directory"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def _create_file(self, name: str, use_cases: dict) -> None:
        """Helper to create a test file with use_cases"""
        filepath = self.files_dir / f"{name}.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        use_cases_yaml = ""
        if use_cases:
            use_cases_yaml = "use_cases:\n"
            for key, values in use_cases.items():
                use_cases_yaml += f"  {key}:\n"
                for val in values:
                    use_cases_yaml += f"    - {val}\n"

        filepath.write_text(
            f"""---
title: {name}
{use_cases_yaml}---

Content
""",
            encoding="utf-8",
        )

    def test_basic_recommendation(self) -> None:
        """Test basic file recommendation"""
        self._create_file("file1", {"project_maturity": ["production"]})
        self._create_file("file2", {"project_maturity": ["prototype"]})

        manager = MetadataManager()
        available = ["file1", "file2"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context)

        assert "file1" in result
        assert "file2" not in result

    def test_multiple_recommendations(self) -> None:
        """Test recommending multiple files"""
        self._create_file("file1", {"project_maturity": ["production"]})
        self._create_file("file2", {"project_maturity": ["production"]})
        self._create_file("file3", {"project_maturity": ["prototype"]})

        manager = MetadataManager()
        available = ["file1", "file2", "file3"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context)

        assert "file1" in result
        assert "file2" in result
        assert "file3" not in result

    def test_nested_file_path(self) -> None:
        """Test recommendation with nested file paths (e.g., python/skill)"""
        nested_dir = self.files_dir / "python"
        nested_dir.mkdir()
        (nested_dir / "skill.md").write_text(
            """---
title: Python Skill
use_cases:
  project_purpose:
    - backend
---

Content
""",
            encoding="utf-8",
        )

        manager = MetadataManager()
        available = ["python/skill"]
        context = {"project_purpose": ["backend"]}

        result = manager.recommend_files(available, self.files_dir, context)

        assert "python/skill" in result

    def test_no_recommendations(self) -> None:
        """Test when no files match context"""
        self._create_file("file1", {"project_maturity": ["prototype"]})
        self._create_file("file2", {"project_maturity": ["mvp"]})

        manager = MetadataManager()
        available = ["file1", "file2"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context)

        assert result == []

    def test_file_without_use_cases(self) -> None:
        """Test that files without use_cases are not recommended"""
        self._create_file("with_use_cases", {"project_maturity": ["production"]})
        (self.files_dir / "without_use_cases.md").write_text(
            """---
title: No Use Cases
---

Content
""",
            encoding="utf-8",
        )

        manager = MetadataManager()
        available = ["with_use_cases", "without_use_cases"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context)

        assert "with_use_cases" in result
        assert "without_use_cases" not in result

    def test_custom_file_extension(self) -> None:
        """Test recommendation with custom file extension"""
        (self.files_dir / "file1.txt").write_text(
            """---
title: Text File
use_cases:
  project_maturity:
    - production
---

Content
""",
            encoding="utf-8",
        )

        manager = MetadataManager()
        available = ["file1"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context, file_extension=".txt")

        assert "file1" in result

    def test_missing_file(self) -> None:
        """Test that missing files are simply not recommended"""
        self._create_file("existing", {"project_maturity": ["production"]})

        manager = MetadataManager()
        available = ["existing", "nonexistent"]
        context = {"project_maturity": "production"}

        result = manager.recommend_files(available, self.files_dir, context)

        assert "existing" in result
        assert "nonexistent" not in result


class TestMetadataManagerIntegration:
    """Integration tests for MetadataManager"""

    def test_full_workflow(self) -> None:
        """Test complete workflow: parse, get_use_cases, match, recommend"""
        temp_dir = tempfile.mkdtemp()
        files_dir = Path(temp_dir)

        try:
            # Create test files
            (files_dir / "security-audit.md").write_text(
                """---
title: Security Audit
description: Comprehensive security analysis
use_cases:
  project_maturity:
    - production
    - legacy
  development_philosophy:
    - quality_first
---

Content
""",
                encoding="utf-8",
            )

            (files_dir / "quick-check.md").write_text(
                """---
title: Quick Check
description: Fast validation
use_cases:
  project_maturity:
    - prototype
    - mvp
  development_philosophy:
    - speed_first
---

Content
""",
                encoding="utf-8",
            )

            manager = MetadataManager()

            # Test with production context
            context = {
                "project_maturity": "production",
                "development_philosophy": "quality_first",
            }

            result = manager.recommend_files(["security-audit", "quick-check"], files_dir, context)

            assert "security-audit" in result
            assert "quick-check" not in result

            # Test with prototype context
            context = {
                "project_maturity": "prototype",
                "development_philosophy": "speed_first",
            }

            result = manager.recommend_files(["security-audit", "quick-check"], files_dir, context)

            assert "security-audit" not in result
            assert "quick-check" in result

        finally:
            import shutil

            shutil.rmtree(temp_dir)

    def test_description_priority(self) -> None:
        """Test that frontmatter description takes priority over content"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("""---
title: Test
description: Frontmatter description
---

# Heading

Content paragraph that would be fallback.
""")
            f.flush()
            path = Path(f.name)

        manager = MetadataManager()
        result = manager.get_description(path)

        assert result == "Frontmatter description"
        assert "Content paragraph" not in result

        path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
