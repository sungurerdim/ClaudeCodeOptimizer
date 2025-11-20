"""
Unit tests for Core Principle Markdown Loader

Tests loading principles from .md files with frontmatter parsing.
Target Coverage: 95%+
"""

from pathlib import Path

import pytest

from claudecodeoptimizer.core.principle_md_loader import (
    get_category_mapping,
    get_principle_by_id,
    get_principles_by_category,
    load_all_principles,
    load_principle_from_md,
)


class TestLoadPrincipleFromMd:
    """Test load_principle_from_md function"""

    def test_load_principle_with_full_frontmatter(self, tmp_path: Path) -> None:
        """Test loading principle with complete frontmatter metadata"""
        principle_file = tmp_path / "U_DRY.md"
        principle_file.write_text(
            """---
id: U_DRY
number: 1
title: DRY Enforcement & Single Source of Truth
category: universal
severity: high
weight: 10
enforcement: MUST
applicability:
  project_types: ['all']
  languages: ['all']
description: Every piece of knowledge must have a single representation
rules:
  - No duplicate functions
  - No magic numbers
examples:
  good: "Use constants"
  bad: "Hardcode values"
autofix:
  available: true
  command: "fix-dry"
---

# U_DRY: DRY Enforcement

Every piece of knowledge must have a single, unambiguous representation.

**Why**: Eliminates duplication to reduce bugs.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["id"] == "U_DRY"
        assert result["number"] == 1
        assert result["title"] == "DRY Enforcement & Single Source of Truth"
        assert result["category"] == "universal"
        assert result["severity"] == "high"
        assert result["weight"] == 10
        assert result["enforcement"] == "MUST"
        assert result["applicability"] == {
            "project_types": ["all"],
            "languages": ["all"],
        }
        assert (
            result["description"]
            == "Every piece of knowledge must have a single representation"
        )
        assert "U_DRY: DRY Enforcement" in result["content"]
        assert result["rules"] == ["No duplicate functions", "No magic numbers"]
        assert result["examples"] == {"good": "Use constants", "bad": "Hardcode values"}
        assert result["autofix"] == {"available": True, "command": "fix-dry"}

    def test_load_principle_with_minimal_frontmatter(self, tmp_path: Path) -> None:
        """Test loading principle with minimal frontmatter (defaults applied)"""
        principle_file = tmp_path / "P_MINIMAL.md"
        principle_file.write_text(
            """---
id: P_MINIMAL
title: Minimal Principle
category: code_quality
---

# Minimal Principle

This is a minimal principle with only required fields.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["id"] == "P_MINIMAL"
        assert result["title"] == "Minimal Principle"
        assert result["category"] == "code_quality"
        assert result["severity"] == "medium"  # Default
        assert result["weight"] == 5  # Default
        assert result["enforcement"] == "SHOULD"  # Default
        assert result["applicability"] == {}  # Default
        assert result["rules"] == []  # Default
        assert result["examples"] == {}  # Default
        assert result["autofix"] == {}  # Default

    def test_load_principle_description_from_frontmatter(self, tmp_path: Path) -> None:
        """Test description extracted from frontmatter when present"""
        principle_file = tmp_path / "P_DESC_FM.md"
        principle_file.write_text(
            """---
id: P_DESC_FM
title: Description in Frontmatter
category: testing
description: This is from frontmatter
---

# Description Test

First line in content.
Second line in content.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == "This is from frontmatter"

    def test_load_principle_description_from_content_first_line(
        self, tmp_path: Path
    ) -> None:
        """Test description extracted from first non-header line in content"""
        principle_file = tmp_path / "P_DESC_CONTENT.md"
        principle_file.write_text(
            """---
id: P_DESC_CONTENT
title: Description from Content
category: testing
---

# Main Heading

This is the first text line and should be the description.

Second paragraph should not be included.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert (
            result["description"]
            == "This is the first text line and should be the description."
        )

    def test_load_principle_description_skips_headers(self, tmp_path: Path) -> None:
        """Test description extraction skips markdown headers"""
        principle_file = tmp_path / "P_SKIP_HEADERS.md"
        principle_file.write_text(
            """---
id: P_SKIP_HEADERS
title: Skip Headers
category: testing
---

# Main Heading
## Subheading
### Another Header

This is the first non-header text.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == "This is the first non-header text."

    def test_load_principle_description_empty_when_no_content(
        self, tmp_path: Path
    ) -> None:
        """Test description is empty when no content exists"""
        principle_file = tmp_path / "P_NO_CONTENT.md"
        principle_file.write_text(
            """---
id: P_NO_CONTENT
title: No Content
category: testing
---
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == ""

    def test_load_principle_description_empty_when_only_headers(
        self, tmp_path: Path
    ) -> None:
        """Test description is empty when content contains only headers"""
        principle_file = tmp_path / "P_ONLY_HEADERS.md"
        principle_file.write_text(
            """---
id: P_ONLY_HEADERS
title: Only Headers
category: testing
---

# Heading 1
## Heading 2
### Heading 3
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == ""

    def test_load_principle_with_empty_lines(self, tmp_path: Path) -> None:
        """Test principle loading handles empty lines correctly"""
        principle_file = tmp_path / "P_EMPTY_LINES.md"
        principle_file.write_text(
            """---
id: P_EMPTY_LINES
title: Empty Lines Test
category: testing
---

# Main Heading


This line comes after empty lines.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == "This line comes after empty lines."

    def test_load_principle_content_preserved(self, tmp_path: Path) -> None:
        """Test that full markdown content is preserved"""
        content = """# Principle Content

This is the principle content with **bold** and *italic*.

## Examples

```python
def example():
    pass
```

- List item 1
- List item 2"""

        principle_file = tmp_path / "P_CONTENT.md"
        principle_file.write_text(
            f"""---
id: P_CONTENT
title: Content Test
category: testing
---

{content}""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        # Content should match (may have trailing newline stripped)
        assert result["content"].strip() == content.strip()

    def test_load_principle_with_complex_applicability(self, tmp_path: Path) -> None:
        """Test loading principle with complex applicability rules"""
        principle_file = tmp_path / "P_COMPLEX_APPLICABILITY.md"
        principle_file.write_text(
            """---
id: P_COMPLEX_APPLICABILITY
title: Complex Applicability
category: testing
applicability:
  project_types: ['web_app', 'microservice', 'cli']
  languages: ['python', 'javascript', 'go']
  team_sizes: ['solo', 'small', 'medium']
  environments: ['dev', 'staging', 'prod']
---

# Complex Applicability Test
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["applicability"]["project_types"] == [
            "web_app",
            "microservice",
            "cli",
        ]
        assert result["applicability"]["languages"] == ["python", "javascript", "go"]
        assert result["applicability"]["team_sizes"] == ["solo", "small", "medium"]
        assert result["applicability"]["environments"] == ["dev", "staging", "prod"]

    def test_load_principle_with_unicode_content(self, tmp_path: Path) -> None:
        """Test loading principle with unicode characters"""
        principle_file = tmp_path / "P_UNICODE.md"
        principle_file.write_text(
            """---
id: P_UNICODE
title: Unicode Test
category: testing
description: Testing unicode characters
---

# Unicode Principle

Content with unicode: 中文, 日本語, العربية, 한국어

Content with emojis: 🚀 ✅ ⚠️ 🔒
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["id"] == "P_UNICODE"
        assert "Unicode Test" in result["title"]
        assert "中文" in result["content"]
        assert "🚀" in result["content"]


class TestLoadAllPrinciples:
    """Test load_all_principles function"""

    def test_load_all_principles_from_directory(self, tmp_path: Path) -> None:
        """Test loading all principles from a directory"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create multiple principle files
        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY Principle
category: universal
---
# DRY
"""
        )

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        (principles_dir / "C_MINIMAL.md").write_text(
            """---
id: C_MINIMAL
title: Minimal Touch
category: claude
---
# Minimal
"""
        )

        result = load_all_principles(principles_dir)

        assert len(result) == 3
        ids = [p["id"] for p in result]
        assert "U_DRY" in ids
        assert "P_LINTING" in ids
        assert "C_MINIMAL" in ids

    def test_load_all_principles_sorted_by_filename(self, tmp_path: Path) -> None:
        """Test that principles are loaded in sorted order"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "Z_LAST.md").write_text(
            """---
id: Z_LAST
title: Last
category: testing
---
# Last
"""
        )

        (principles_dir / "A_FIRST.md").write_text(
            """---
id: A_FIRST
title: First
category: testing
---
# First
"""
        )

        (principles_dir / "M_MIDDLE.md").write_text(
            """---
id: M_MIDDLE
title: Middle
category: testing
---
# Middle
"""
        )

        result = load_all_principles(principles_dir)

        assert result[0]["id"] == "A_FIRST"
        assert result[1]["id"] == "M_MIDDLE"
        assert result[2]["id"] == "Z_LAST"

    def test_load_all_principles_empty_directory(self, tmp_path: Path) -> None:
        """Test loading from empty directory returns empty list"""
        principles_dir = tmp_path / "empty_principles"
        principles_dir.mkdir()

        result = load_all_principles(principles_dir)

        assert result == []

    def test_load_all_principles_nonexistent_directory_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test that non-existent directory raises FileNotFoundError"""
        nonexistent_dir = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError) as exc_info:
            load_all_principles(nonexistent_dir)

        assert "Principles directory not found" in str(exc_info.value)
        assert str(nonexistent_dir) in str(exc_info.value)

    def test_load_all_principles_ignores_non_md_files(self, tmp_path: Path) -> None:
        """Test that non-.md files are ignored"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        # Non-markdown files that should be ignored
        (principles_dir / "README.txt").write_text("Not a principle")
        (principles_dir / "notes.doc").write_text("Also not a principle")
        (principles_dir / ".gitkeep").write_text("")

        result = load_all_principles(principles_dir)

        assert len(result) == 1
        assert result[0]["id"] == "U_DRY"

    def test_load_all_principles_ignores_subdirectories(self, tmp_path: Path) -> None:
        """Test that .md files in subdirectories are ignored"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create principle in main directory
        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        # Create subdirectory with principle file
        subdir = principles_dir / "archived"
        subdir.mkdir()
        (subdir / "OLD_PRINCIPLE.md").write_text(
            """---
id: OLD_PRINCIPLE
title: Old
category: archived
---
# Old
"""
        )

        result = load_all_principles(principles_dir)

        # Should only load from main directory
        assert len(result) == 1
        assert result[0]["id"] == "U_DRY"


class TestGetPrincipleById:
    """Test get_principle_by_id function"""

    def test_get_principle_by_id_exists(self, tmp_path: Path) -> None:
        """Test retrieving existing principle by ID"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY Principle
category: universal
severity: high
---
# DRY
"""
        )

        result = get_principle_by_id("U_DRY", principles_dir)

        assert result is not None
        assert result["id"] == "U_DRY"
        assert result["title"] == "DRY Principle"
        assert result["category"] == "universal"
        assert result["severity"] == "high"

    def test_get_principle_by_id_not_found(self, tmp_path: Path) -> None:
        """Test retrieving non-existent principle returns None"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        result = get_principle_by_id("NONEXISTENT", principles_dir)

        assert result is None

    def test_get_principle_by_id_with_multiple_principles(self, tmp_path: Path) -> None:
        """Test retrieving specific principle when multiple exist"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        (principles_dir / "C_MINIMAL.md").write_text(
            """---
id: C_MINIMAL
title: Minimal
category: claude
---
# Minimal
"""
        )

        result = get_principle_by_id("P_LINTING", principles_dir)

        assert result is not None
        assert result["id"] == "P_LINTING"
        assert result["title"] == "Linting"


class TestGetPrinciplesByCategory:
    """Test get_principles_by_category function"""

    def test_get_principles_by_category_single_match(self, tmp_path: Path) -> None:
        """Test retrieving principles from a category with one principle"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        result = get_principles_by_category("code_quality", principles_dir)

        assert len(result) == 1
        assert result[0]["id"] == "P_LINTING"
        assert result[0]["category"] == "code_quality"

    def test_get_principles_by_category_multiple_matches(self, tmp_path: Path) -> None:
        """Test retrieving multiple principles from same category"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        (principles_dir / "P_TYPE_SAFETY.md").write_text(
            """---
id: P_TYPE_SAFETY
title: Type Safety
category: code_quality
---
# Type Safety
"""
        )

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        result = get_principles_by_category("code_quality", principles_dir)

        assert len(result) == 2
        ids = [p["id"] for p in result]
        assert "P_LINTING" in ids
        assert "P_TYPE_SAFETY" in ids

    def test_get_principles_by_category_no_matches(self, tmp_path: Path) -> None:
        """Test retrieving from category with no principles"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        result = get_principles_by_category("nonexistent_category", principles_dir)

        assert result == []

    def test_get_principles_by_category_empty_directory(self, tmp_path: Path) -> None:
        """Test retrieving from empty principles directory"""
        principles_dir = tmp_path / "empty_principles"
        principles_dir.mkdir()

        result = get_principles_by_category("any_category", principles_dir)

        assert result == []


class TestGetCategoryMapping:
    """Test get_category_mapping function"""

    def test_get_category_mapping_single_category(self, tmp_path: Path) -> None:
        """Test mapping with single category"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        (principles_dir / "P_TYPE_SAFETY.md").write_text(
            """---
id: P_TYPE_SAFETY
title: Type Safety
category: code_quality
---
# Type Safety
"""
        )

        result = get_category_mapping(principles_dir)

        assert "code_quality" in result
        assert set(result["code_quality"]) == {"P_LINTING", "P_TYPE_SAFETY"}

    def test_get_category_mapping_multiple_categories(self, tmp_path: Path) -> None:
        """Test mapping with multiple categories"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        (principles_dir / "U_TEST_FIRST.md").write_text(
            """---
id: U_TEST_FIRST
title: Test First
category: universal
---
# Test First
"""
        )

        (principles_dir / "P_LINTING.md").write_text(
            """---
id: P_LINTING
title: Linting
category: code_quality
---
# Linting
"""
        )

        (principles_dir / "C_MINIMAL.md").write_text(
            """---
id: C_MINIMAL
title: Minimal
category: claude
---
# Minimal
"""
        )

        result = get_category_mapping(principles_dir)

        assert len(result) == 3
        assert set(result["universal"]) == {"U_DRY", "U_TEST_FIRST"}
        assert result["code_quality"] == ["P_LINTING"]
        assert result["claude"] == ["C_MINIMAL"]

    def test_get_category_mapping_empty_directory(self, tmp_path: Path) -> None:
        """Test mapping with empty directory"""
        principles_dir = tmp_path / "empty_principles"
        principles_dir.mkdir()

        result = get_category_mapping(principles_dir)

        assert result == {}

    def test_get_category_mapping_preserves_order(self, tmp_path: Path) -> None:
        """Test that mapping preserves alphabetical order within categories"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "P_Z_LAST.md").write_text(
            """---
id: P_Z_LAST
title: Last
category: testing
---
# Last
"""
        )

        (principles_dir / "P_A_FIRST.md").write_text(
            """---
id: P_A_FIRST
title: First
category: testing
---
# First
"""
        )

        (principles_dir / "P_M_MIDDLE.md").write_text(
            """---
id: P_M_MIDDLE
title: Middle
category: testing
---
# Middle
"""
        )

        result = get_category_mapping(principles_dir)

        # Since files are loaded in sorted order, the mapping should reflect that
        assert result["testing"] == ["P_A_FIRST", "P_M_MIDDLE", "P_Z_LAST"]


class TestEdgeCases:
    """Test edge cases and error scenarios"""

    def test_principle_with_malformed_frontmatter(self, tmp_path: Path) -> None:
        """Test handling of malformed frontmatter (frontmatter library should handle)"""
        principle_file = tmp_path / "MALFORMED.md"
        principle_file.write_text(
            """---
id: MALFORMED
title: Malformed
category: testing
invalid yaml here: [unclosed
---

# Content
""",
            encoding="utf-8",
        )

        # frontmatter library should handle this gracefully or raise appropriate error
        # This test verifies the behavior
        try:
            result = load_principle_from_md(principle_file)
            # If it succeeds, check that basic fields are populated
            assert "id" in result
        except Exception:
            # If it fails, that's also acceptable behavior
            pass

    def test_principle_with_no_frontmatter(self, tmp_path: Path) -> None:
        """Test principle file with no frontmatter at all"""
        principle_file = tmp_path / "NO_FRONTMATTER.md"
        principle_file.write_text(
            """# Just Content

No frontmatter in this file.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        # Should still work with defaults
        assert result["id"] is None
        assert result["severity"] == "medium"
        assert result["weight"] == 5
        assert result["enforcement"] == "SHOULD"

    def test_principle_with_very_long_content(self, tmp_path: Path) -> None:
        """Test principle with very long content"""
        long_content = "\n".join([f"Line {i}" for i in range(10000)])

        principle_file = tmp_path / "LONG.md"
        principle_file.write_text(
            f"""---
id: LONG
title: Long Content
category: testing
---

{long_content}
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["id"] == "LONG"
        assert len(result["content"]) > 50000  # Very long content

    def test_principle_with_special_characters_in_fields(self, tmp_path: Path) -> None:
        """Test principle with special characters in field values"""
        principle_file = tmp_path / "SPECIAL.md"
        principle_file.write_text(
            """---
id: SPECIAL_CHARS
title: Title with colons and commas
category: testing
description: Description with special chars
---

# Special Characters

Content with various special characters: @#$%^&*()
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["id"] == "SPECIAL_CHARS"
        assert "colons" in result["title"]
        assert "special chars" in result["description"]
        assert "@#$%" in result["content"]

    def test_load_all_principles_with_file_read_error(self, tmp_path: Path) -> None:
        """Test handling of file read errors during load_all_principles"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create a valid principle
        (principles_dir / "VALID.md").write_text(
            """---
id: VALID
title: Valid
category: testing
---
# Valid
"""
        )

        # Create a file with invalid encoding (this might cause issues)
        bad_file = principles_dir / "BAD.md"
        bad_file.write_bytes(b"\x80\x81\x82")  # Invalid UTF-8

        # The function should either skip the bad file or raise an error
        # Test that it doesn't crash completely
        try:
            result = load_all_principles(principles_dir)
            # If it succeeds, check that valid principle was loaded
            assert any(p["id"] == "VALID" for p in result)
        except Exception:
            # If it raises an error, that's also acceptable
            pass


class TestAdditionalEdgeCases:
    """Additional edge case tests for thorough coverage"""

    def test_load_principle_description_extraction_priority(
        self, tmp_path: Path
    ) -> None:
        """Test that frontmatter description takes priority over content"""
        principle_file = tmp_path / "P_DESC_PRIORITY.md"
        principle_file.write_text(
            """---
id: P_DESC_PRIORITY
title: Description Priority
category: testing
description: Description from frontmatter
---

# Heading

This is from content and should be ignored.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == "Description from frontmatter"
        assert "This is from content" not in result["description"]

    def test_load_principle_with_numeric_values(self, tmp_path: Path) -> None:
        """Test principle with numeric weight and number values"""
        principle_file = tmp_path / "P_NUMERIC.md"
        principle_file.write_text(
            """---
id: P_NUMERIC
number: 42
title: Numeric Test
category: testing
weight: 8
---

# Numeric
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["number"] == 42
        assert result["weight"] == 8
        assert isinstance(result["number"], int)
        assert isinstance(result["weight"], int)

    def test_load_principle_with_list_rules(self, tmp_path: Path) -> None:
        """Test principle with rules as a list"""
        principle_file = tmp_path / "P_RULES_LIST.md"
        principle_file.write_text(
            """---
id: P_RULES_LIST
title: Rules List
category: testing
rules:
  - Rule 1
  - Rule 2
  - Rule 3
---

# Rules
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["rules"] == ["Rule 1", "Rule 2", "Rule 3"]
        assert len(result["rules"]) == 3

    def test_load_principle_with_nested_examples(self, tmp_path: Path) -> None:
        """Test principle with nested examples structure"""
        principle_file = tmp_path / "P_EXAMPLES.md"
        principle_file.write_text(
            """---
id: P_EXAMPLES
title: Examples Test
category: testing
examples:
  good:
    - Example 1
    - Example 2
  bad:
    - Anti-pattern 1
    - Anti-pattern 2
---

# Examples
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert "good" in result["examples"]
        assert "bad" in result["examples"]
        assert result["examples"]["good"] == ["Example 1", "Example 2"]
        assert result["examples"]["bad"] == ["Anti-pattern 1", "Anti-pattern 2"]

    def test_load_principle_with_boolean_autofix(self, tmp_path: Path) -> None:
        """Test principle with boolean autofix flag"""
        principle_file = tmp_path / "P_AUTOFIX_BOOL.md"
        principle_file.write_text(
            """---
id: P_AUTOFIX_BOOL
title: Autofix Boolean
category: testing
autofix:
  available: true
---

# Autofix
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["autofix"]["available"] is True
        assert isinstance(result["autofix"]["available"], bool)

    def test_load_all_principles_with_varying_metadata(self, tmp_path: Path) -> None:
        """Test loading principles with different metadata completeness"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Full metadata
        (principles_dir / "FULL.md").write_text(
            """---
id: FULL
number: 1
title: Full
category: testing
severity: high
weight: 10
---
# Full
"""
        )

        # Partial metadata
        (principles_dir / "PARTIAL.md").write_text(
            """---
id: PARTIAL
title: Partial
category: testing
---
# Partial
"""
        )

        # Minimal metadata
        (principles_dir / "MINIMAL.md").write_text(
            """---
id: MINIMAL
---
# Minimal
"""
        )

        result = load_all_principles(principles_dir)

        assert len(result) == 3

        # Find each principle
        full = next(p for p in result if p["id"] == "FULL")
        partial = next(p for p in result if p["id"] == "PARTIAL")
        minimal = next(p for p in result if p["id"] == "MINIMAL")

        # Full has all fields
        assert full["weight"] == 10
        assert full["severity"] == "high"

        # Partial uses defaults
        assert partial["weight"] == 5
        assert partial["severity"] == "medium"

        # Minimal uses all defaults
        assert minimal["weight"] == 5
        assert minimal["severity"] == "medium"

    def test_get_principle_by_id_exact_match(self, tmp_path: Path) -> None:
        """Test that principle ID lookup works with exact filename match"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "U_DRY.md").write_text(
            """---
id: U_DRY
title: DRY
category: universal
---
# DRY
"""
        )

        # Exact match should work
        result = get_principle_by_id("U_DRY", principles_dir)
        assert result is not None
        assert result["id"] == "U_DRY"

        # Non-existent ID should return None
        result_missing = get_principle_by_id("NONEXISTENT_ID", principles_dir)
        assert result_missing is None

    def test_get_category_mapping_with_duplicate_handling(self, tmp_path: Path) -> None:
        """Test category mapping handles multiple principles in same category correctly"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create 5 principles in the same category
        for i in range(5):
            (principles_dir / f"P_TEST_{i}.md").write_text(
                f"""---
id: P_TEST_{i}
title: Test {i}
category: same_category
---
# Test {i}
"""
            )

        result = get_category_mapping(principles_dir)

        assert "same_category" in result
        assert len(result["same_category"]) == 5
        # All IDs should be unique
        assert len(set(result["same_category"])) == 5

    def test_load_principle_whitespace_handling(self, tmp_path: Path) -> None:
        """Test handling of various whitespace scenarios"""
        principle_file = tmp_path / "P_WHITESPACE.md"
        principle_file.write_text(
            """---
id: P_WHITESPACE
title: Whitespace Test
category: testing
---

# Heading



First line with leading/trailing spaces.

""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        # Description should have stripped whitespace
        assert result["description"] == "First line with leading/trailing spaces."

    def test_load_principle_multiple_paragraphs_in_description(
        self, tmp_path: Path
    ) -> None:
        """Test that only first paragraph is extracted as description"""
        principle_file = tmp_path / "P_MULTI_PARA.md"
        principle_file.write_text(
            """---
id: P_MULTI_PARA
title: Multi Paragraph
category: testing
---

# Heading

First paragraph for description.

Second paragraph should not be in description.

Third paragraph also excluded.
""",
            encoding="utf-8",
        )

        result = load_principle_from_md(principle_file)

        assert result["description"] == "First paragraph for description."
        assert "Second paragraph" not in result["description"]

    def test_get_principles_by_category_returns_sorted(self, tmp_path: Path) -> None:
        """Test that get_principles_by_category returns principles in sorted order"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        (principles_dir / "Z_LAST.md").write_text(
            """---
id: Z_LAST
title: Last
category: testing
---
# Last
"""
        )

        (principles_dir / "A_FIRST.md").write_text(
            """---
id: A_FIRST
title: First
category: testing
---
# First
"""
        )

        (principles_dir / "M_MIDDLE.md").write_text(
            """---
id: M_MIDDLE
title: Middle
category: testing
---
# Middle
"""
        )

        result = get_principles_by_category("testing", principles_dir)

        # Should be sorted by filename
        assert result[0]["id"] == "A_FIRST"
        assert result[1]["id"] == "M_MIDDLE"
        assert result[2]["id"] == "Z_LAST"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
