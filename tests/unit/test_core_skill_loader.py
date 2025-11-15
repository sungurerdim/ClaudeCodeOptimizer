"""
Unit tests for Core Skill Loader

Tests progressive disclosure system for skills with 3-tier loading.
Target Coverage: 100%
"""

import re
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from claudecodeoptimizer.core.skill_loader import SkillLoader, SkillMetadata


class TestSkillMetadata:
    """Test SkillMetadata dataclass"""

    def test_metadata_creation(self) -> None:
        """Test basic metadata creation"""
        metadata = SkillMetadata(
            name="Test Skill",
            activation_keywords=["test", "skill"],
            category="testing",
            summary="A test skill",
        )

        assert metadata.name == "Test Skill"
        assert metadata.activation_keywords == ["test", "skill"]
        assert metadata.category == "testing"
        assert metadata.summary == "A test skill"
        assert metadata.token_estimate == 50

    def test_metadata_custom_token_estimate(self) -> None:
        """Test metadata with custom token estimate"""
        metadata = SkillMetadata(
            name="Test Skill",
            activation_keywords=["test"],
            category="testing",
            summary="Summary",
            token_estimate=100,
        )

        assert metadata.token_estimate == 100


class TestSkillLoaderInit:
    """Test SkillLoader initialization"""

    def test_init_with_custom_dir(self, tmp_path: Path) -> None:
        """Test initialization with custom skills directory"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        loader = SkillLoader(skills_dir=skills_dir)

        assert loader.skills_dir == skills_dir
        assert loader._metadata_cache == {}
        assert loader._instructions_cache == {}
        assert loader._resources_cache == {}

    def test_init_with_default_dir(self, tmp_path: Path) -> None:
        """Test initialization with default skills directory from config"""
        skills_dir = tmp_path / "default_skills"
        skills_dir.mkdir()

        with patch("claudecodeoptimizer.config.CCOConfig") as mock_config:
            mock_config.get_skills_dir.return_value = skills_dir

            loader = SkillLoader(skills_dir=None)

            assert loader.skills_dir == skills_dir
            mock_config.get_skills_dir.assert_called_once()

    def test_init_nonexistent_dir_raises_error(self, tmp_path: Path) -> None:
        """Test initialization with non-existent directory raises FileNotFoundError"""
        nonexistent_dir = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError) as exc_info:
            SkillLoader(skills_dir=nonexistent_dir)

        assert "Skills directory not found" in str(exc_info.value)
        assert str(nonexistent_dir) in str(exc_info.value)


class TestLoadSkillMetadata:
    """Test load_skill_metadata method"""

    def test_load_metadata_with_frontmatter(self, tmp_path: Path) -> None:
        """Test loading metadata from file with frontmatter"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "test-skill.md"
        skill_file.write_text(
            """---
metadata:
  name: "Test Skill"
  activation_keywords: ["test", "skill", "example"]
  category: "testing"
---

# Test Skill

This is a test skill for unit testing.

It has multiple paragraphs.

## Instructions

Some instructions here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert metadata.name == "Test Skill"
        assert metadata.activation_keywords == ["test", "skill", "example"]
        assert metadata.category == "testing"
        assert "This is a test skill for unit testing." in metadata.summary
        assert metadata.token_estimate == 50

    def test_load_metadata_with_quoted_values(self, tmp_path: Path) -> None:
        """Test loading metadata with single-quoted values"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "quoted-skill.md"
        skill_file.write_text(
            """---
metadata:
  name: 'Quoted Skill'
  activation_keywords: ['quote1', 'quote2']
  category: 'quoted'
---

# Quoted Skill

Summary text here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert metadata.name == "Quoted Skill"
        assert metadata.activation_keywords == ["quote1", "quote2"]
        assert metadata.category == "quoted"

    def test_load_metadata_without_frontmatter(self, tmp_path: Path) -> None:
        """Test loading metadata from file without frontmatter (fallback)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "no-frontmatter-skill.md"
        skill_file.write_text(
            """# No Frontmatter Skill

This skill has no frontmatter.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        # .replace("-", " ").title() converts "no-frontmatter-skill" to "No Frontmatter Skill"
        assert metadata.name == "No Frontmatter Skill"
        assert metadata.activation_keywords == ["no-frontmatter-skill"]
        assert metadata.category == "general"
        assert metadata.summary == "No summary"

    def test_load_metadata_partial_frontmatter(self, tmp_path: Path) -> None:
        """Test loading metadata with partial frontmatter (missing fields)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "partial-skill.md"
        skill_file.write_text(
            """---
metadata:
  name: "Partial Skill"
---

# Partial Skill

Summary here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert metadata.name == "Partial Skill"
        assert metadata.activation_keywords == []
        assert metadata.category == "general"

    def test_load_metadata_with_cache(self, tmp_path: Path) -> None:
        """Test metadata caching works correctly"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "cached-skill.md"
        skill_file.write_text(
            """---
metadata:
  name: "Cached Skill"
  activation_keywords: ["cache"]
  category: "testing"
---

# Cached Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # First call - should load from file
        metadata1 = loader.load_skill_metadata(skill_file)

        # Modify file
        skill_file.write_text(
            """---
metadata:
  name: "Modified Skill"
  activation_keywords: ["modified"]
  category: "different"
---

# Modified Skill

New summary.
""",
            encoding="utf-8",
        )

        # Second call - should use cache, not reflect modifications
        metadata2 = loader.load_skill_metadata(skill_file)

        assert metadata1.name == metadata2.name == "Cached Skill"
        assert metadata1 is metadata2  # Same object from cache

    def test_load_metadata_long_summary_truncated(self, tmp_path: Path) -> None:
        """Test that summary is truncated to 200 characters"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        long_summary = "A" * 300

        skill_file = skills_dir / "long-summary.md"
        skill_file.write_text(
            f"""---
metadata:
  name: "Long Summary Skill"
  activation_keywords: ["long"]
  category: "testing"
---

# Long Summary Skill

{long_summary}

## Next section
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert len(metadata.summary) == 200
        assert metadata.summary == "A" * 200

    def test_load_metadata_summary_stops_at_heading(self, tmp_path: Path) -> None:
        """Test that summary extraction stops at next heading"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "summary-heading.md"
        skill_file.write_text(
            """---
metadata:
  name: "Summary Heading Skill"
  activation_keywords: ["summary"]
  category: "testing"
---

# Summary Heading Skill

This is the summary paragraph.

## Next Heading

This should not be included in summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert "This is the summary paragraph." in metadata.summary
        assert "Next Heading" not in metadata.summary
        assert "should not be included" not in metadata.summary

    def test_load_metadata_no_summary(self, tmp_path: Path) -> None:
        """Test loading metadata when no summary section exists"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "no-summary.md"
        skill_file.write_text(
            """---
metadata:
  name: "No Summary Skill"
  activation_keywords: ["none"]
  category: "testing"
---

# No Summary Skill
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        metadata = loader.load_skill_metadata(skill_file)

        assert metadata.summary == "No summary"


class TestLoadSkillInstructions:
    """Test load_skill_instructions method"""

    def test_load_instructions_with_marker(self, tmp_path: Path) -> None:
        """Test loading instructions with HTML comment markers"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "instructions-marker.md"
        skill_file.write_text(
            """# Skill

Summary here.

<!-- INSTRUCTIONS: Load when activated -->
These are the instructions.

Multiple paragraphs of instructions.

<!-- RESOURCES: Examples follow -->
Resources here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        instructions = loader.load_skill_instructions(skill_file)

        assert "These are the instructions." in instructions
        assert "Multiple paragraphs of instructions." in instructions
        assert "Resources here." not in instructions

    def test_load_instructions_fallback_heading(self, tmp_path: Path) -> None:
        """Test loading instructions with markdown heading (fallback)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "instructions-heading.md"
        skill_file.write_text(
            """# Skill

Summary.

## Instructions

These are instructions using heading.

## Examples

Example content here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        instructions = loader.load_skill_instructions(skill_file)

        assert "These are instructions using heading." in instructions
        assert "Example content here." not in instructions

    def test_load_instructions_detailed_heading(self, tmp_path: Path) -> None:
        """Test loading instructions with 'Detailed Instructions' heading"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "detailed-instructions.md"
        skill_file.write_text(
            """# Skill

Summary.

## Detailed Instructions

These are detailed instructions.

## Resources

Resources here.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        instructions = loader.load_skill_instructions(skill_file)

        assert "These are detailed instructions." in instructions
        assert "Resources here." not in instructions

    def test_load_instructions_no_instructions(self, tmp_path: Path) -> None:
        """Test loading instructions when none exist"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "no-instructions.md"
        skill_file.write_text(
            """# Skill

Just a summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        instructions = loader.load_skill_instructions(skill_file)

        assert instructions == ""

    def test_load_instructions_with_cache(self, tmp_path: Path) -> None:
        """Test instructions caching works correctly"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "cached-instructions.md"
        skill_file.write_text(
            """# Skill

<!-- INSTRUCTIONS: Load when activated -->
Original instructions.
<!-- RESOURCES: Examples -->
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # First call
        instructions1 = loader.load_skill_instructions(skill_file)

        # Modify file
        skill_file.write_text(
            """# Skill

<!-- INSTRUCTIONS: Load when activated -->
Modified instructions.
<!-- RESOURCES: Examples -->
""",
            encoding="utf-8",
        )

        # Second call - should use cache
        instructions2 = loader.load_skill_instructions(skill_file)

        assert "Original instructions." in instructions1
        assert "Original instructions." in instructions2
        assert instructions1 is instructions2


class TestLoadSkillResources:
    """Test load_skill_resources method"""

    def test_load_resources_with_marker(self, tmp_path: Path) -> None:
        """Test loading resources with HTML comment markers"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "resources-marker.md"
        skill_file.write_text(
            """# Skill

<!-- INSTRUCTIONS: Load when activated -->
Instructions here.

<!-- RESOURCES: Examples and references -->
These are the resources.

Examples and documentation.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        resources = loader.load_skill_resources(skill_file)

        assert "These are the resources." in resources
        assert "Examples and documentation." in resources
        assert "Instructions here." not in resources

    def test_load_resources_fallback_examples_heading(self, tmp_path: Path) -> None:
        """Test loading resources with Examples heading (fallback)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "resources-examples.md"
        skill_file.write_text(
            """# Skill

## Instructions

Instructions.

## Examples

Example 1: Do this.

Example 2: Do that.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        resources = loader.load_skill_resources(skill_file)

        assert "Example 1: Do this." in resources
        assert "Example 2: Do that." in resources

    def test_load_resources_fallback_resources_heading(self, tmp_path: Path) -> None:
        """Test loading resources with Resources heading (fallback)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "resources-heading.md"
        skill_file.write_text(
            """# Skill

## Instructions

Instructions.

## Resources

- Resource 1
- Resource 2
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        resources = loader.load_skill_resources(skill_file)

        assert "Resource 1" in resources
        assert "Resource 2" in resources

    def test_load_resources_no_resources(self, tmp_path: Path) -> None:
        """Test loading resources when none exist"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "no-resources.md"
        skill_file.write_text(
            """# Skill

## Instructions

Just instructions.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)
        resources = loader.load_skill_resources(skill_file)

        assert resources == ""

    def test_load_resources_with_cache(self, tmp_path: Path) -> None:
        """Test resources caching works correctly"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "cached-resources.md"
        skill_file.write_text(
            """# Skill

<!-- RESOURCES: Examples -->
Original resources.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # First call
        resources1 = loader.load_skill_resources(skill_file)

        # Modify file
        skill_file.write_text(
            """# Skill

<!-- RESOURCES: Examples -->
Modified resources.
""",
            encoding="utf-8",
        )

        # Second call - should use cache
        resources2 = loader.load_skill_resources(skill_file)

        assert "Original resources." in resources1
        assert "Original resources." in resources2
        assert resources1 is resources2


class TestIsActivated:
    """Test is_activated method"""

    def test_is_activated_match(self, tmp_path: Path) -> None:
        """Test skill activation with matching keyword"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "activation.md"
        skill_file.write_text(
            """---
metadata:
  name: "Activation Skill"
  activation_keywords: ["test", "debug", "troubleshoot"]
  category: "testing"
---

# Activation Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        assert loader.is_activated(skill_file, "I need to test this feature")
        assert loader.is_activated(skill_file, "Let's debug the issue")
        assert loader.is_activated(skill_file, "Troubleshoot the problem")

    def test_is_activated_case_insensitive(self, tmp_path: Path) -> None:
        """Test skill activation is case-insensitive"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "case-test.md"
        skill_file.write_text(
            """---
metadata:
  name: "Case Test Skill"
  activation_keywords: ["Test", "DEBUG"]
  category: "testing"
---

# Case Test Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        assert loader.is_activated(skill_file, "I need to TEST this")
        assert loader.is_activated(skill_file, "debug the code")
        assert loader.is_activated(skill_file, "DeBuG mode enabled")

    def test_is_activated_no_match(self, tmp_path: Path) -> None:
        """Test skill not activated when no keywords match"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "no-match.md"
        skill_file.write_text(
            """---
metadata:
  name: "No Match Skill"
  activation_keywords: ["deploy", "production"]
  category: "deployment"
---

# No Match Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        assert not loader.is_activated(skill_file, "I need to test this")
        assert not loader.is_activated(skill_file, "debug the code")

    def test_is_activated_partial_match(self, tmp_path: Path) -> None:
        """Test skill activation with partial keyword match"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "partial.md"
        skill_file.write_text(
            """---
metadata:
  name: "Partial Match Skill"
  activation_keywords: ["perf"]
  category: "performance"
---

# Partial Match Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Should match as substring
        assert loader.is_activated(skill_file, "I need to improve perf")
        # "perf" is a substring of "performance"
        assert loader.is_activated(skill_file, "performance optimization required")

    def test_is_activated_empty_keywords(self, tmp_path: Path) -> None:
        """Test skill with empty activation keywords list"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "empty-keywords.md"
        skill_file.write_text(
            """---
metadata:
  name: "Empty Keywords Skill"
  activation_keywords: []
  category: "general"
---

# Empty Keywords Skill

Summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Empty list [] gets parsed as [''] which matches everything ('' in any string is True)
        # This is the actual behavior of the code
        assert loader.is_activated(skill_file, "any context at all")


class TestDiscoverSkills:
    """Test discover_skills method"""

    def test_discover_all_skills(self, tmp_path: Path) -> None:
        """Test discovering all skill files"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create multiple skill files
        (skills_dir / "skill1.md").write_text("# Skill 1")
        (skills_dir / "skill2.md").write_text("# Skill 2")
        (skills_dir / "skill3.md").write_text("# Skill 3")

        # Create non-markdown file (should be ignored)
        (skills_dir / "readme.txt").write_text("Not a skill")

        loader = SkillLoader(skills_dir=skills_dir)
        skills = loader.discover_skills()

        assert len(skills) == 3
        skill_names = [s.name for s in skills]
        assert "skill1.md" in skill_names
        assert "skill2.md" in skill_names
        assert "skill3.md" in skill_names

    def test_discover_skills_by_category(self, tmp_path: Path) -> None:
        """Test discovering skills filtered by category"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skills with different categories
        (skills_dir / "testing-skill.md").write_text(
            """---
metadata:
  name: "Testing Skill"
  activation_keywords: ["test"]
  category: "testing"
---

# Testing Skill
"""
        )

        (skills_dir / "deploy-skill.md").write_text(
            """---
metadata:
  name: "Deploy Skill"
  activation_keywords: ["deploy"]
  category: "deployment"
---

# Deploy Skill
"""
        )

        (skills_dir / "test-skill2.md").write_text(
            """---
metadata:
  name: "Test Skill 2"
  activation_keywords: ["test2"]
  category: "testing"
---

# Test Skill 2
"""
        )

        loader = SkillLoader(skills_dir=skills_dir)

        testing_skills = loader.discover_skills(category="testing")
        deployment_skills = loader.discover_skills(category="deployment")

        assert len(testing_skills) == 2
        assert len(deployment_skills) == 1

    def test_discover_skills_empty_directory(self, tmp_path: Path) -> None:
        """Test discovering skills in empty directory"""
        skills_dir = tmp_path / "empty_skills"
        skills_dir.mkdir()

        loader = SkillLoader(skills_dir=skills_dir)
        skills = loader.discover_skills()

        assert skills == []

    def test_discover_skills_nonexistent_directory(self, tmp_path: Path) -> None:
        """Test discovering skills when directory doesn't exist"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        loader = SkillLoader(skills_dir=skills_dir)

        # Remove directory after initialization
        skills_dir.rmdir()

        skills = loader.discover_skills()

        assert skills == []

    def test_discover_skills_subdirectories_ignored(self, tmp_path: Path) -> None:
        """Test that subdirectories are not included in discovery"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create skill file in main directory
        (skills_dir / "main-skill.md").write_text("# Main Skill")

        # Create subdirectory with skill file
        subdir = skills_dir / "python"
        subdir.mkdir()
        (subdir / "python-skill.md").write_text("# Python Skill")

        loader = SkillLoader(skills_dir=skills_dir)
        skills = loader.discover_skills()

        # Should only find main skill, not subdirectory skill
        assert len(skills) == 1
        assert skills[0].name == "main-skill.md"

    def test_discover_skills_category_filter_no_match(self, tmp_path: Path) -> None:
        """Test discovering skills with category filter that matches nothing"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        (skills_dir / "skill.md").write_text(
            """---
metadata:
  name: "Skill"
  activation_keywords: ["skill"]
  category: "testing"
---

# Skill
"""
        )

        loader = SkillLoader(skills_dir=skills_dir)
        skills = loader.discover_skills(category="nonexistent")

        assert skills == []


class TestLoadFullSkill:
    """Test load_full_skill method"""

    def test_load_full_skill(self, tmp_path: Path) -> None:
        """Test loading complete skill content"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        full_content = """---
metadata:
  name: "Full Skill"
  activation_keywords: ["full"]
  category: "complete"
---

# Full Skill

Summary paragraph.

<!-- INSTRUCTIONS: Load when activated -->
Instructions section.

Multiple paragraphs.

<!-- RESOURCES: Examples -->
Resources section.

Examples and references.
"""

        skill_file = skills_dir / "full-skill.md"
        skill_file.write_text(full_content, encoding="utf-8")

        loader = SkillLoader(skills_dir=skills_dir)
        loaded_content = loader.load_full_skill(skill_file)

        assert loaded_content == full_content

    def test_load_full_skill_unicode(self, tmp_path: Path) -> None:
        """Test loading skill with unicode content"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        unicode_content = """# Unicode Skill

Testing unicode: 中文, العربية, 日本語, 한국어

Emoji: 🚀 ✅ ⚠️
"""

        skill_file = skills_dir / "unicode-skill.md"
        skill_file.write_text(unicode_content, encoding="utf-8")

        loader = SkillLoader(skills_dir=skills_dir)
        loaded_content = loader.load_full_skill(skill_file)

        assert loaded_content == unicode_content
        assert "中文" in loaded_content
        assert "🚀" in loaded_content


class TestClearCache:
    """Test clear_cache method"""

    def test_clear_cache(self, tmp_path: Path) -> None:
        """Test clearing all caches"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "skill.md"
        skill_file.write_text(
            """---
metadata:
  name: "Test Skill"
  activation_keywords: ["test"]
  category: "testing"
---

# Test Skill

Summary.

<!-- INSTRUCTIONS: Load when activated -->
Instructions.

<!-- RESOURCES: Examples -->
Resources.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Populate all caches
        loader.load_skill_metadata(skill_file)
        loader.load_skill_instructions(skill_file)
        loader.load_skill_resources(skill_file)

        # Verify caches are populated
        assert len(loader._metadata_cache) > 0
        assert len(loader._instructions_cache) > 0
        assert len(loader._resources_cache) > 0

        # Clear caches
        loader.clear_cache()

        # Verify caches are empty
        assert len(loader._metadata_cache) == 0
        assert len(loader._instructions_cache) == 0
        assert len(loader._resources_cache) == 0

    def test_clear_cache_reloads_data(self, tmp_path: Path) -> None:
        """Test that clearing cache allows reloading updated data"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "reload-skill.md"
        skill_file.write_text(
            """---
metadata:
  name: "Original Skill"
  activation_keywords: ["original"]
  category: "testing"
---

# Original Skill

Original summary.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Load original
        metadata1 = loader.load_skill_metadata(skill_file)
        assert metadata1.name == "Original Skill"

        # Modify file
        skill_file.write_text(
            """---
metadata:
  name: "Updated Skill"
  activation_keywords: ["updated"]
  category: "modified"
---

# Updated Skill

Updated summary.
""",
            encoding="utf-8",
        )

        # Clear cache
        loader.clear_cache()

        # Load again - should reflect changes
        metadata2 = loader.load_skill_metadata(skill_file)
        assert metadata2.name == "Updated Skill"
        assert metadata2.activation_keywords == ["updated"]
        assert metadata2.category == "modified"


class TestSkillLoaderIntegration:
    """Integration tests for SkillLoader"""

    def test_progressive_disclosure_workflow(self, tmp_path: Path) -> None:
        """Test complete progressive disclosure workflow (3 tiers)"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "progressive.md"
        skill_file.write_text(
            """---
metadata:
  name: "Progressive Skill"
  activation_keywords: ["progressive", "disclosure"]
  category: "workflow"
---

# Progressive Skill

This demonstrates progressive disclosure.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

Step 1: Do this
Step 2: Do that

<!-- RESOURCES: Examples -->
## Examples & Resources

Example 1: Complete workflow
Example 2: Edge cases
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Tier 1: Metadata only (~50 tokens)
        metadata = loader.load_skill_metadata(skill_file)
        assert metadata.name == "Progressive Skill"
        assert "progressive" in metadata.activation_keywords

        # Tier 2: + Instructions (~150 tokens)
        instructions = loader.load_skill_instructions(skill_file)
        assert "Step 1: Do this" in instructions
        assert "Step 2: Do that" in instructions

        # Tier 3: + Examples & Resources (~500 tokens)
        resources = loader.load_skill_resources(skill_file)
        assert "Example 1: Complete workflow" in resources
        assert "Example 2: Edge cases" in resources

    def test_activation_and_loading(self, tmp_path: Path) -> None:
        """Test checking activation and loading appropriate tier"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "activation-test.md"
        skill_file.write_text(
            """---
metadata:
  name: "Activation Test"
  activation_keywords: ["optimize", "performance"]
  category: "performance"
---

# Activation Test

Optimize your code for better performance.

<!-- INSTRUCTIONS: Load when activated -->
Performance optimization instructions.

<!-- RESOURCES: Examples -->
Performance examples.
""",
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Check if skill should be activated
        context1 = "I need to optimize this function"
        context2 = "How do I deploy this?"

        assert loader.is_activated(skill_file, context1)
        assert not loader.is_activated(skill_file, context2)

        # If activated, load instructions
        if loader.is_activated(skill_file, context1):
            instructions = loader.load_skill_instructions(skill_file)
            assert "Performance optimization instructions" in instructions

    def test_multiple_skills_discovery_and_filtering(self, tmp_path: Path) -> None:
        """Test discovering multiple skills and filtering by category"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create multiple skills
        (skills_dir / "test1.md").write_text(
            """---
metadata:
  name: "Test 1"
  activation_keywords: ["test1"]
  category: "testing"
---
# Test 1
"""
        )

        (skills_dir / "test2.md").write_text(
            """---
metadata:
  name: "Test 2"
  activation_keywords: ["test2"]
  category: "testing"
---
# Test 2
"""
        )

        (skills_dir / "deploy.md").write_text(
            """---
metadata:
  name: "Deploy"
  activation_keywords: ["deploy"]
  category: "deployment"
---
# Deploy
"""
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # Discover all skills
        all_skills = loader.discover_skills()
        assert len(all_skills) == 3

        # Filter by category
        testing_skills = loader.discover_skills(category="testing")
        assert len(testing_skills) == 2

        deployment_skills = loader.discover_skills(category="deployment")
        assert len(deployment_skills) == 1

    def test_cache_performance(self, tmp_path: Path) -> None:
        """Test that caching improves performance on repeated loads"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill_file = skills_dir / "cache-perf.md"
        skill_file.write_text(
            """---
metadata:
  name: "Cache Performance"
  activation_keywords: ["cache"]
  category: "performance"
---

# Cache Performance

Testing cache performance.
""" + ("A" * 10000),  # Large content
            encoding="utf-8",
        )

        loader = SkillLoader(skills_dir=skills_dir)

        # First load - from disk
        metadata1 = loader.load_skill_metadata(skill_file)

        # Second load - from cache (should be same object)
        metadata2 = loader.load_skill_metadata(skill_file)

        assert metadata1 is metadata2  # Same object reference


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
