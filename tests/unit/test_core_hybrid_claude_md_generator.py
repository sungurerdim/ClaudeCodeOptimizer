"""
Comprehensive tests for hybrid CLAUDE.md generator.

Tests cover:
- generate_hybrid_claude_md main function
- _load_universal_template
- _generate_cco_section
- _generate_category_list
- _update_cco_section
- remove_cco_section
- Integration scenarios
- Error handling

Target Coverage: 90%+
"""

from unittest.mock import patch

from claudecodeoptimizer.core.hybrid_claude_md_generator import (
    _generate_category_list,
    _generate_cco_section,
    _load_universal_template,
    _update_cco_section,
    generate_hybrid_claude_md,
    remove_cco_section,
)


class TestLoadUniversalTemplate:
    """Test _load_universal_template function"""

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_load_universal_template_success(self, mock_get_dir, mock_load_principles, temp_dir):
        """Test loading universal template with valid principles"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir

        mock_principles = [
            {
                "id": "U_DRY",
                "title": "DRY Enforcement",
                "category": "universal",
                "one_line_why": "Avoid code duplication",
            },
            {
                "id": "U_TEST_FIRST",
                "title": "Test-First Development",
                "category": "universal",
                "one_line_why": "Write tests before code",
            },
            {
                "id": "P_LINTING",
                "title": "Linting",
                "category": "code_quality",
                "one_line_why": "Ensure code quality",
            },
        ]
        mock_load_principles.return_value = mock_principles

        # Execute
        result = _load_universal_template(temp_dir)

        # Assert
        assert "U_DRY" in result
        assert "DRY Enforcement" in result
        assert "Avoid code duplication" in result
        assert "U_TEST_FIRST" in result
        assert "Test-First Development" in result
        assert "Write tests before code" in result
        # Project-specific principle should not be included
        assert "P_LINTING" not in result

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_load_universal_template_without_one_line_why(
        self, mock_get_dir, mock_load_principles, temp_dir
    ):
        """Test loading template when one_line_why is missing"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir

        mock_principles = [
            {
                "id": "U_DRY",
                "title": "DRY Enforcement",
                "category": "universal",
                # No one_line_why
            }
        ]
        mock_load_principles.return_value = mock_principles

        # Execute
        result = _load_universal_template(temp_dir)

        # Assert
        assert "U_DRY" in result
        assert "DRY Enforcement" in result
        # Should only have the title line, no description
        lines = result.split("\n")
        assert len(lines) == 1

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_load_universal_template_no_principles_dir(self, mock_get_dir, temp_dir):
        """Test loading template when principles directory doesn't exist"""
        # Setup
        principles_dir = temp_dir / "nonexistent"
        mock_get_dir.return_value = principles_dir

        # Execute
        result = _load_universal_template(temp_dir)

        # Assert
        assert "Universal Principles" in result
        assert "U_* principles apply to all projects" in result

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_load_universal_template_empty_principles(
        self, mock_get_dir, mock_load_principles, temp_dir
    ):
        """Test loading template when no principles are loaded"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir
        mock_load_principles.return_value = []

        # Execute
        result = _load_universal_template(temp_dir)

        # Assert
        assert result == "U_* principles apply to all projects."

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_load_universal_template_sorted_by_id(
        self, mock_get_dir, mock_load_principles, temp_dir
    ):
        """Test that universal principles are sorted by ID"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir

        # Provide unsorted principles
        mock_principles = [
            {"id": "U_TEST_FIRST", "title": "Test First", "category": "universal"},
            {"id": "U_DRY", "title": "DRY", "category": "universal"},
            {"id": "U_ATOMIC_COMMITS", "title": "Atomic Commits", "category": "universal"},
        ]
        mock_load_principles.return_value = mock_principles

        # Execute
        result = _load_universal_template(temp_dir)

        # Assert - check order
        lines = result.split("\n")
        assert "U_ATOMIC_COMMITS" in lines[0]
        assert "U_DRY" in lines[1]
        assert "U_TEST_FIRST" in lines[2]


class TestGenerateCategoryList:
    """Test _generate_category_list function"""

    def test_generate_category_list_multiple_categories(self):
        """Test generating list with multiple categories"""
        selected_principles = {
            "universal": ["U_DRY", "U_TEST_FIRST"],
            "code_quality": ["P_LINTING", "P_TYPE_SAFETY"],
            "security_privacy": ["P_ENCRYPTION", "P_AUDIT_LOGGING", "P_PRIVACY_FIRST"],
            "testing": ["P_TEST_COVERAGE"],
        }

        result = _generate_category_list(selected_principles)

        assert "**Code Quality**: 2 principles" in result
        assert "**Security & Privacy**: 3 principles" in result
        assert "**Testing**: 1 principles" in result
        # Universal should be excluded
        assert "universal" not in result.lower()

    def test_generate_category_list_empty_categories(self):
        """Test generating list when categories are empty"""
        selected_principles = {
            "universal": ["U_DRY"],
            "code_quality": [],
            "security_privacy": [],
        }

        result = _generate_category_list(selected_principles)

        # Only categories with principles should be listed
        assert result == "- No project-specific categories selected"

    def test_generate_category_list_no_project_categories(self):
        """Test generating list with only universal category"""
        selected_principles = {"universal": ["U_DRY", "U_TEST_FIRST"]}

        result = _generate_category_list(selected_principles)

        assert result == "- No project-specific categories selected"

    def test_generate_category_list_custom_category_formatting(self):
        """Test category name formatting for unknown categories"""
        selected_principles = {
            "custom_category": ["CUSTOM_1", "CUSTOM_2"],
            "another_custom": ["CUSTOM_3"],
        }

        result = _generate_category_list(selected_principles)

        # Custom categories should be title-cased with underscores replaced
        assert "**Custom Category**: 2 principles" in result
        assert "**Another Custom**: 1 principles" in result

    def test_generate_category_list_all_standard_categories(self):
        """Test all standard category names are mapped correctly"""
        selected_principles = {
            "code_quality": ["P1"],
            "architecture": ["P2"],
            "security_privacy": ["P3"],
            "testing": ["P4"],
            "git_workflow": ["P5"],
            "performance": ["P6"],
            "operations": ["P7"],
            "api_design": ["P8"],
        }

        result = _generate_category_list(selected_principles)

        assert "**Code Quality**: 1 principles" in result
        assert "**Architecture**: 1 principles" in result
        assert "**Security & Privacy**: 1 principles" in result
        assert "**Testing**: 1 principles" in result
        assert "**Git Workflow**: 1 principles" in result
        assert "**Performance**: 1 principles" in result
        assert "**Operations**: 1 principles" in result
        assert "**API Design**: 1 principles" in result


class TestGenerateCCOSection:
    """Test _generate_cco_section function"""

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_generate_cco_section_with_principles(self, mock_get_dir, temp_dir):
        """Test generating CCO section with selected principles"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        # Create some principle files
        (principles_dir / "P_LINTING.md").write_text("linting")
        (principles_dir / "P_TYPE_SAFETY.md").write_text("type safety")
        (principles_dir / "P_ENCRYPTION.md").write_text("encryption")

        mock_get_dir.return_value = principles_dir

        project_config = {
            "selected_principles": {
                "universal": ["U_DRY", "U_TEST_FIRST"],
                "code_quality": ["P_LINTING", "P_TYPE_SAFETY"],
                "security_privacy": ["P_ENCRYPTION"],
            }
        }
        universal_template = "- **U_DRY**: DRY\n- **U_TEST_FIRST**: Test First"

        # Execute
        result = _generate_cco_section(project_config, universal_template)

        # Assert
        assert "<!-- CCO_START -->" in result
        assert "<!-- CCO_END -->" in result
        assert "Universal Principles (Apply to ALL Projects)" in result
        assert universal_template in result
        assert "Project-Specific Principles" in result
        assert "**3** selected principles from 3 available" in result
        assert "**Code Quality**: 2 principles" in result
        assert "**Security & Privacy**: 1 principles" in result

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_generate_cco_section_no_project_principles(self, mock_get_dir, temp_dir):
        """Test generating CCO section with only universal principles"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir

        project_config = {
            "selected_principles": {
                "universal": ["U_DRY", "U_TEST_FIRST"],
            }
        }
        universal_template = "- **U_DRY**: DRY"

        # Execute
        result = _generate_cco_section(project_config, universal_template)

        # Assert
        assert "**0** selected principles from 0 available" in result
        assert "No project-specific categories selected" in result

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_generate_cco_section_empty_config(self, mock_get_dir, temp_dir):
        """Test generating CCO section with empty config"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir

        project_config = {}
        universal_template = "Universal principles"

        # Execute
        result = _generate_cco_section(project_config, universal_template)

        # Assert
        assert "**0** selected principles from 0 available" in result
        assert "Universal principles" in result


class TestUpdateCCOSection:
    """Test _update_cco_section function"""

    def test_update_cco_section_replaces_existing(self):
        """Test updating existing CCO section"""
        existing_content = """# My Project

Some content before.

<!-- CCO_START -->
Old CCO content here
with multiple lines
<!-- CCO_END -->

Content after CCO section.
"""

        new_cco_section = """<!-- CCO_START -->
New CCO content
Updated principles
<!-- CCO_END -->"""

        result = _update_cco_section(existing_content, new_cco_section)

        assert "New CCO content" in result
        assert "Updated principles" in result
        assert "Old CCO content here" not in result
        assert "Some content before." in result
        assert "Content after CCO section." in result

    def test_update_cco_section_multiline_old_content(self):
        """Test updating CCO section with complex multiline content"""
        existing_content = """# Project

<!-- CCO_START -->
## Principles

- Principle 1
- Principle 2

### Details

More details here
<!-- CCO_END -->

After.
"""

        new_cco_section = """<!-- CCO_START -->
## New Principles
Simple content
<!-- CCO_END -->"""

        result = _update_cco_section(existing_content, new_cco_section)

        assert "New Principles" in result
        assert "Principle 1" not in result
        assert "Principle 2" not in result
        assert "After." in result

    def test_update_cco_section_preserves_surrounding_content(self):
        """Test that content before and after CCO section is preserved"""
        existing_content = """# Header

Before content 1
Before content 2

<!-- CCO_START -->
Old
<!-- CCO_END -->

After content 1
After content 2
"""

        new_cco_section = "<!-- CCO_START -->\nNew\n<!-- CCO_END -->"

        result = _update_cco_section(existing_content, new_cco_section)

        assert "Before content 1" in result
        assert "Before content 2" in result
        assert "After content 1" in result
        assert "After content 2" in result
        assert "New" in result
        assert "Old" not in result


class TestRemoveCCOSection:
    """Test remove_cco_section function"""

    def test_remove_cco_section_success(self, temp_dir):
        """Test successfully removing CCO section"""
        claude_md = temp_dir / "CLAUDE.md"
        content = """# Project

User content

---
<!-- CCO_START -->
CCO content to remove
<!-- CCO_END -->

More user content
"""
        claude_md.write_text(content, encoding="utf-8")

        result = remove_cco_section(claude_md)

        assert result is True
        updated_content = claude_md.read_text(encoding="utf-8")
        assert "CCO content to remove" not in updated_content
        assert "User content" in updated_content
        assert "More user content" in updated_content
        assert "<!-- CCO_START -->" not in updated_content
        assert "<!-- CCO_END -->" not in updated_content

    def test_remove_cco_section_file_not_found(self, temp_dir):
        """Test removing CCO section when file doesn't exist"""
        claude_md = temp_dir / "CLAUDE.md"

        result = remove_cco_section(claude_md)

        assert result is False

    def test_remove_cco_section_no_cco_markers(self, temp_dir):
        """Test removing CCO section when markers don't exist"""
        claude_md = temp_dir / "CLAUDE.md"
        content = """# Project

Just regular content
No CCO section here
"""
        claude_md.write_text(content, encoding="utf-8")

        result = remove_cco_section(claude_md)

        assert result is False
        # Content should be unchanged
        assert claude_md.read_text(encoding="utf-8") == content

    def test_remove_cco_section_cleans_multiple_blank_lines(self, temp_dir):
        """Test that multiple blank lines are cleaned up after removal"""
        claude_md = temp_dir / "CLAUDE.md"
        content = """# Project

Content



---
<!-- CCO_START -->
CCO content
<!-- CCO_END -->



More content
"""
        claude_md.write_text(content, encoding="utf-8")

        result = remove_cco_section(claude_md)

        assert result is True
        updated_content = claude_md.read_text(encoding="utf-8")
        # Should not have triple newlines
        assert "\n\n\n" not in updated_content

    def test_remove_cco_section_with_dividers(self, temp_dir):
        """Test removing CCO section with horizontal dividers"""
        claude_md = temp_dir / "CLAUDE.md"
        content = """# Project

Before

---

<!-- CCO_START -->
CCO section
<!-- CCO_END -->

After
"""
        claude_md.write_text(content, encoding="utf-8")

        result = remove_cco_section(claude_md)

        assert result is True
        updated_content = claude_md.read_text(encoding="utf-8")
        assert "CCO section" not in updated_content
        assert "Before" in updated_content
        assert "After" in updated_content


class TestGenerateHybridClaudeMd:
    """Test main generate_hybrid_claude_md function"""

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_generate_new_claude_md(self, mock_generate_section, mock_load_template, temp_dir):
        """Test generating new CLAUDE.md file"""
        # Setup
        mock_load_template.return_value = "Universal template"
        mock_generate_section.return_value = "CCO section"

        project_config = {"project_name": "MyProject"}
        cco_dir = temp_dir / ".cco"
        cco_dir.mkdir(parents=True)

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "# MyProject - Claude Development Guide" in result
        assert "CCO section" in result
        mock_load_template.assert_called_once_with(cco_dir)
        mock_generate_section.assert_called_once()

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_generate_new_claude_md_no_project_name(
        self, mock_generate_section, mock_load_template, temp_dir
    ):
        """Test generating new CLAUDE.md when project_name is missing"""
        # Setup
        mock_load_template.return_value = "Universal template"
        mock_generate_section.return_value = "CCO section"

        project_config = {}
        cco_dir = temp_dir / ".cco"
        cco_dir.mkdir(parents=True)

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert - should use directory name
        assert f"# {temp_dir.name} - Claude Development Guide" in result

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_update_existing_claude_md_with_cco_section(
        self, mock_generate_section, mock_load_template, temp_dir
    ):
        """Test updating existing CLAUDE.md that has CCO section"""
        # Setup
        mock_load_template.return_value = "Universal template"
        mock_generate_section.return_value = """<!-- CCO_START -->
New CCO content
<!-- CCO_END -->"""

        claude_md = temp_dir / "CLAUDE.md"
        existing_content = """# Existing Project

User content

<!-- CCO_START -->
Old CCO
<!-- CCO_END -->

More user content
"""
        claude_md.write_text(existing_content, encoding="utf-8")

        project_config = {}
        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "New CCO content" in result
        assert "Old CCO" not in result
        assert "User content" in result
        assert "More user content" in result

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_append_to_existing_claude_md_without_cco_section(
        self, mock_generate_section, mock_load_template, temp_dir
    ):
        """Test appending CCO section to existing CLAUDE.md without CCO"""
        # Setup
        mock_load_template.return_value = "Universal template"
        mock_generate_section.return_value = "CCO section"

        claude_md = temp_dir / "CLAUDE.md"
        existing_content = """# Existing Project

User-written content
"""
        claude_md.write_text(existing_content, encoding="utf-8")

        project_config = {}
        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "Existing Project" in result
        assert "User-written content" in result
        assert "CCO section" in result
        # Should be appended after existing content
        assert result.index("User-written content") < result.index("CCO section")

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_generate_handles_trailing_whitespace(
        self, mock_generate_section, mock_load_template, temp_dir
    ):
        """Test that trailing whitespace is handled correctly"""
        # Setup
        mock_load_template.return_value = "Universal template"
        mock_generate_section.return_value = "CCO section"

        claude_md = temp_dir / "CLAUDE.md"
        existing_content = "# Project\n\nContent\n\n\n"  # Multiple trailing newlines
        claude_md.write_text(existing_content, encoding="utf-8")

        project_config = {}
        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert - should strip trailing whitespace before appending
        assert not result.endswith("\n\n\nCCO")


class TestIntegrationScenarios:
    """Integration tests for hybrid Claude MD generator"""

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_full_generation_workflow(self, mock_get_dir, mock_load_principles, temp_dir):
        """Test complete workflow from project config to generated CLAUDE.md"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        (principles_dir / "P_LINTING.md").write_text("linting")
        (principles_dir / "P_TYPE_SAFETY.md").write_text("type safety")

        mock_get_dir.return_value = principles_dir
        mock_principles = [
            {
                "id": "U_DRY",
                "title": "DRY Enforcement",
                "category": "universal",
                "one_line_why": "Avoid duplication",
            },
            {
                "id": "U_TEST_FIRST",
                "title": "Test-First Development",
                "category": "universal",
                "one_line_why": "Write tests first",
            },
        ]
        mock_load_principles.return_value = mock_principles

        project_config = {
            "project_name": "IntegrationTest",
            "selected_principles": {
                "universal": ["U_DRY", "U_TEST_FIRST"],
                "code_quality": ["P_LINTING", "P_TYPE_SAFETY"],
            },
        }

        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "# IntegrationTest - Claude Development Guide" in result
        assert "Universal Principles" in result
        assert "U_DRY" in result
        assert "U_TEST_FIRST" in result
        assert "Project-Specific Principles" in result
        assert "**2** selected principles from 2 available" in result
        assert "**Code Quality**: 2 principles" in result

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_update_workflow_preserves_user_content(
        self, mock_get_dir, mock_load_principles, temp_dir
    ):
        """Test that updating preserves user's custom content"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)
        mock_get_dir.return_value = principles_dir
        mock_load_principles.return_value = [
            {"id": "U_DRY", "title": "DRY", "category": "universal"}
        ]

        claude_md = temp_dir / "CLAUDE.md"
        existing_content = """# My Custom Project Setup

## My Custom Section

Important user-written documentation here.

## Guidelines

Custom guidelines.

<!-- CCO_START -->
Old CCO content
<!-- CCO_END -->

## More Custom Sections

Additional content.
"""
        claude_md.write_text(existing_content, encoding="utf-8")

        project_config = {
            "selected_principles": {
                "universal": ["U_DRY"],
            }
        }
        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "My Custom Project Setup" in result
        assert "My Custom Section" in result
        assert "Important user-written documentation here." in result
        assert "Custom guidelines." in result
        assert "More Custom Sections" in result
        assert "Additional content." in result
        assert "Old CCO content" not in result
        assert "<!-- CCO_START -->" in result
        assert "U_DRY" in result

    def test_remove_and_regenerate_cycle(self, temp_dir):
        """Test removing CCO section and regenerating"""
        # Create initial CLAUDE.md with CCO section
        claude_md = temp_dir / "CLAUDE.md"
        initial_content = """# Project

User content

---
<!-- CCO_START -->
CCO content
<!-- CCO_END -->

More content
"""
        claude_md.write_text(initial_content, encoding="utf-8")

        # Remove CCO section
        removed = remove_cco_section(claude_md)
        assert removed is True

        content_after_removal = claude_md.read_text(encoding="utf-8")
        assert "CCO content" not in content_after_removal
        assert "User content" in content_after_removal

        # Now regenerate (simplified - just test append logic)
        with patch(
            "claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template"
        ) as mock_template, patch(
            "claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section"
        ) as mock_section:
            mock_template.return_value = "Universal"
            mock_section.return_value = "New CCO"

            project_config = {}
            cco_dir = temp_dir / ".cco"

            result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

            # Should append new CCO section
            assert "New CCO" in result
            assert "User content" in result


class TestEdgeCases:
    """Test edge cases and error conditions"""

    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._load_universal_template")
    @patch("claudecodeoptimizer.core.hybrid_claude_md_generator._generate_cco_section")
    def test_unicode_handling(self, mock_generate_section, mock_load_template, temp_dir):
        """Test handling of Unicode characters in CLAUDE.md"""
        # Setup
        mock_load_template.return_value = "Template"
        mock_generate_section.return_value = "CCO"

        claude_md = temp_dir / "CLAUDE.md"
        unicode_content = """# Проект

中文内容

<!-- CCO_START -->
Old
<!-- CCO_END -->

émojis 🎉
"""
        claude_md.write_text(unicode_content, encoding="utf-8")

        project_config = {}
        cco_dir = temp_dir / ".cco"

        # Execute
        result = generate_hybrid_claude_md(temp_dir, project_config, cco_dir)

        # Assert
        assert "Проект" in result
        assert "中文内容" in result
        assert "émojis 🎉" in result

    def test_remove_cco_section_unicode(self, temp_dir):
        """Test removing CCO section with Unicode content"""
        claude_md = temp_dir / "CLAUDE.md"
        content = """# Проект

---
<!-- CCO_START -->
CCO with émojis 🎉
<!-- CCO_END -->

More content
"""
        claude_md.write_text(content, encoding="utf-8")

        result = remove_cco_section(claude_md)

        assert result is True
        updated = claude_md.read_text(encoding="utf-8")
        assert "émojis 🎉" not in updated
        assert "Проект" in updated
        assert "More content" in updated

    def test_generate_category_list_empty_dict(self):
        """Test generating category list with empty dictionary"""
        result = _generate_category_list({})
        assert result == "- No project-specific categories selected"

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_generate_cco_section_large_principle_count(
        self, mock_get_dir, mock_load_principles, temp_dir
    ):
        """Test CCO section with large number of principles"""
        # Setup
        principles_dir = temp_dir / "principles"
        principles_dir.mkdir(parents=True)

        # Create many principle files
        for i in range(50):
            (principles_dir / f"P_PRINCIPLE_{i}.md").write_text(f"principle {i}")

        mock_get_dir.return_value = principles_dir
        mock_load_principles.return_value = []

        # Create config with many principles
        principles_ids = [f"P_PRINCIPLE_{i}" for i in range(30)]
        project_config = {
            "selected_principles": {
                "universal": ["U_DRY"],
                "code_quality": principles_ids[:15],
                "security_privacy": principles_ids[15:30],
            }
        }

        universal_template = "U_DRY"

        # Execute
        result = _generate_cco_section(project_config, universal_template)

        # Assert
        assert "**30** selected principles from 50 available" in result
        assert "**Code Quality**: 15 principles" in result
        assert "**Security & Privacy**: 15 principles" in result

    def test_update_cco_section_no_markers_in_content(self):
        """Test update when content doesn't have CCO markers (shouldn't happen but test anyway)"""
        existing_content = """# Project

No CCO markers here
"""

        new_cco_section = "<!-- CCO_START -->\nNew\n<!-- CCO_END -->"

        result = _update_cco_section(existing_content, new_cco_section)

        # Pattern won't match, content should be unchanged
        assert result == existing_content
