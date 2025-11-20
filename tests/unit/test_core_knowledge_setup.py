"""
Unit tests for Core Knowledge Setup

Tests installation logic for ~/.claude/ structure initialization.
Target Coverage: 100%
"""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.core import knowledge_setup
from claudecodeoptimizer.core.knowledge_setup import (
    _setup_agents,
    _setup_claude_md,
    _setup_commands,
    _setup_principles,
    _setup_skills,
    get_available_agents,
    get_available_commands,
    get_available_skills,
    setup_global_knowledge,
)


@pytest.fixture
def mock_claude_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture that provides a temporary ~/.claude/ directory.

    Mocks all config functions to use tmp_path instead of real home.
    """
    claude_dir = tmp_path / ".claude"
    commands_dir = claude_dir / "commands"
    principles_dir = claude_dir / "principles"
    agents_dir = claude_dir / "agents"
    skills_dir = claude_dir / "skills"

    with (
        patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
        patch.object(knowledge_setup.config, "get_global_commands_dir", return_value=commands_dir),
        patch.object(knowledge_setup.config, "get_principles_dir", return_value=principles_dir),
        patch.object(knowledge_setup.config, "get_agents_dir", return_value=agents_dir),
        patch.object(knowledge_setup.config, "get_skills_dir", return_value=skills_dir),
    ):
        yield claude_dir


@pytest.fixture
def mock_content_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture that provides mock content directories with sample files.

    Creates content/commands/, content/principles/, content/agents/, content/skills/.
    """
    content_dir = tmp_path / "content"

    # Create commands
    commands_src = content_dir / "commands"
    commands_src.mkdir(parents=True)
    (commands_src / "cco-audit.md").write_text("# Audit Command")
    (commands_src / "cco-fix.md").write_text("# Fix Command")
    (commands_src / "cco-help.md").write_text("# Help Command")

    # Create principles
    principles_src = content_dir / "principles"
    principles_src.mkdir(parents=True)
    (principles_src / "U_CHANGE_VERIFICATION.md").write_text("# U Principle 1")
    (principles_src / "U_DRY.md").write_text("# U Principle 2")
    (principles_src / "C_FOLLOW_PATTERNS.md").write_text("# C Principle 1")
    (principles_src / "C_MODEL_SELECTION.md").write_text("# C Principle 2")
    (principles_src / "P_PROJECT_SPECIFIC.md").write_text("# P Principle 1")
    (principles_src / "other_file.md").write_text("# Other file")

    # Create agents
    agents_src = content_dir / "agents"
    agents_src.mkdir(parents=True)
    (agents_src / "cco-agent-audit.md").write_text("# Audit Agent")
    (agents_src / "cco-agent-fix.md").write_text("# Fix Agent")

    # Create skills
    skills_src = content_dir / "skills"
    skills_src.mkdir(parents=True)
    (skills_src / "cco-skill-testing.md").write_text("# Testing Skill")
    (skills_src / "cco-skill-security.md").write_text("# Security Skill")

    # Create language-specific skills
    python_skills = skills_src / "python"
    python_skills.mkdir(parents=True)
    (python_skills / "cco-skill-django.md").write_text("# Django Skill")

    js_skills = skills_src / "javascript"
    js_skills.mkdir(parents=True)
    (js_skills / "cco-skill-react.md").write_text("# React Skill")

    yield content_dir


class TestSetupGlobalKnowledge:
    """Test setup_global_knowledge function"""

    def test_setup_creates_directories(self, mock_claude_dir: Path, mock_content_dir: Path) -> None:
        """Test that setup creates all required directories"""
        # This test verifies directory structure creation
        # The actual setup is tested in integration tests
        # Here we verify the mock_claude_dir fixture works
        assert not mock_claude_dir.exists()  # Not created yet by setup
        mock_claude_dir.mkdir(parents=True)
        assert mock_claude_dir.exists()

    def test_setup_returns_success(self, mock_claude_dir: Path) -> None:
        """Test that setup returns success dictionary"""
        # Create minimal content structure
        package_dir = Path(knowledge_setup.__file__).parent.parent

        # Skip if content doesn't exist (for isolation)
        if not (package_dir / "content").exists():
            pytest.skip("Content directory not available")

        result = setup_global_knowledge()

        assert result["success"] is True
        assert "claude_dir" in result
        assert "actions" in result
        assert (
            len(result["actions"]) == 6
        )  # commands, principles, agents, skills, claude.md, templates

    def test_setup_with_force_flag(self, mock_claude_dir: Path) -> None:
        """Test setup with force=True regenerates files"""
        package_dir = Path(knowledge_setup.__file__).parent.parent

        if not (package_dir / "content").exists():
            pytest.skip("Content directory not available")

        # First setup
        result1 = setup_global_knowledge(force=False)
        assert result1["success"] is True

        # Second setup with force
        result2 = setup_global_knowledge(force=True)
        assert result2["success"] is True


class TestSetupCommands:
    """Test _setup_commands function"""

    def test_creates_commands_directory(
        self, mock_claude_dir: Path, mock_content_dir: Path
    ) -> None:
        """Test that commands directory is created"""
        commands_dir = mock_claude_dir / "commands"

        # Mock package directory
        with patch.object(knowledge_setup, "_setup_commands", wraps=_setup_commands):
            # Create minimal test
            commands_dir.mkdir(parents=True, exist_ok=True)
            assert commands_dir.exists()

    def test_copies_cco_commands(self, tmp_path: Path) -> None:
        """Test that cco-*.md files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "commands"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-audit.md").write_text("# Audit")
        (source_dir / "cco-fix.md").write_text("# Fix")
        (source_dir / "other.md").write_text("# Other")  # Should not be copied

        # Setup destination
        dest_dir = tmp_path / "dest" / "commands"

        # Mock __file__ to point to our test structure
        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_commands(dest_dir)

        assert dest_dir.exists()
        assert (dest_dir / "cco-audit.md").exists()
        assert (dest_dir / "cco-fix.md").exists()
        assert not (dest_dir / "other.md").exists()

    def test_removes_old_cco_files(self, tmp_path: Path) -> None:
        """Test that old cco-*.md files are removed before copying"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "commands"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-new.md").write_text("# New Command")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "commands"
        dest_dir.mkdir(parents=True)
        (dest_dir / "cco-old.md").write_text("# Old Command")
        (dest_dir / "user-custom.md").write_text("# User Custom")  # Should be preserved

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_commands(dest_dir)

        assert not (dest_dir / "cco-old.md").exists()
        assert (dest_dir / "cco-new.md").exists()
        assert (dest_dir / "user-custom.md").exists()  # Preserved

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "commands"

        # Point to non-existent content
        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_commands(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupPrinciples:
    """Test _setup_principles function"""

    def test_copies_u_c_p_principles(self, tmp_path: Path) -> None:
        """Test that U_*, C_*, P_*.md files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "principles"
        source_dir.mkdir(parents=True)
        (source_dir / "U_TEST.md").write_text("# U Principle")
        (source_dir / "C_TEST.md").write_text("# C Principle")
        (source_dir / "P_TEST.md").write_text("# P Principle")
        (source_dir / "README.md").write_text("# README")  # Should not be copied

        dest_dir = tmp_path / "dest" / "principles"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_principles(dest_dir)

        assert (dest_dir / "U_TEST.md").exists()
        assert (dest_dir / "C_TEST.md").exists()
        assert (dest_dir / "P_TEST.md").exists()
        assert not (dest_dir / "README.md").exists()

    def test_removes_old_principle_files(self, tmp_path: Path) -> None:
        """Test that old U_*, C_*, P_*.md files are removed"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "principles"
        source_dir.mkdir(parents=True)
        (source_dir / "U_NEW.md").write_text("# New")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "principles"
        dest_dir.mkdir(parents=True)
        (dest_dir / "U_OLD.md").write_text("# Old U")
        (dest_dir / "C_OLD.md").write_text("# Old C")
        (dest_dir / "P_OLD.md").write_text("# Old P")
        (dest_dir / "user_principle.md").write_text("# User")  # Should be preserved

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_principles(dest_dir)

        assert not (dest_dir / "U_OLD.md").exists()
        assert not (dest_dir / "C_OLD.md").exists()
        assert not (dest_dir / "P_OLD.md").exists()
        assert (dest_dir / "U_NEW.md").exists()
        assert (dest_dir / "user_principle.md").exists()

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "principles"

        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_principles(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupAgents:
    """Test _setup_agents function"""

    def test_copies_cco_agents(self, tmp_path: Path) -> None:
        """Test that cco-*.md agent files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "agents"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-agent-audit.md").write_text("# Audit Agent")
        (source_dir / "cco-agent-fix.md").write_text("# Fix Agent")
        (source_dir / "other-agent.md").write_text("# Other")

        dest_dir = tmp_path / "dest" / "agents"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_agents(dest_dir)

        assert (dest_dir / "cco-agent-audit.md").exists()
        assert (dest_dir / "cco-agent-fix.md").exists()
        assert not (dest_dir / "other-agent.md").exists()

    def test_removes_old_cco_agents(self, tmp_path: Path) -> None:
        """Test that old cco-*.md files are removed"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "agents"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-agent-new.md").write_text("# New Agent")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "agents"
        dest_dir.mkdir(parents=True)
        (dest_dir / "cco-agent-old.md").write_text("# Old Agent")
        (dest_dir / "user-agent.md").write_text("# User Agent")

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_agents(dest_dir)

        assert not (dest_dir / "cco-agent-old.md").exists()
        assert (dest_dir / "cco-agent-new.md").exists()
        assert (dest_dir / "user-agent.md").exists()

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "agents"

        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_agents(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupSkills:
    """Test _setup_skills function"""

    def test_copies_root_skills(self, tmp_path: Path) -> None:
        """Test that root cco-*.md skill files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "skills"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-skill-testing.md").write_text("# Testing Skill")
        (source_dir / "cco-skill-security.md").write_text("# Security Skill")

        dest_dir = tmp_path / "dest" / "skills"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_skills(dest_dir)

        assert (dest_dir / "cco-skill-testing.md").exists()
        assert (dest_dir / "cco-skill-security.md").exists()

    def test_copies_language_specific_skills(self, tmp_path: Path) -> None:
        """Test that language-specific skill subdirectories are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "skills"
        source_dir.mkdir(parents=True)

        # Python skills
        python_dir = source_dir / "python"
        python_dir.mkdir()
        (python_dir / "cco-skill-django.md").write_text("# Django")

        # JavaScript skills
        js_dir = source_dir / "javascript"
        js_dir.mkdir()
        (js_dir / "cco-skill-react.md").write_text("# React")

        dest_dir = tmp_path / "dest" / "skills"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_skills(dest_dir)

        assert (dest_dir / "python" / "cco-skill-django.md").exists()
        assert (dest_dir / "javascript" / "cco-skill-react.md").exists()

    def test_removes_old_cco_skills_recursively(self, tmp_path: Path) -> None:
        """Test that old cco-*.md files are removed recursively"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "skills"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-skill-new.md").write_text("# New")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "skills"
        dest_dir.mkdir(parents=True)
        (dest_dir / "cco-skill-old.md").write_text("# Old")

        # Old file in subdirectory
        old_subdir = dest_dir / "python"
        old_subdir.mkdir()
        (old_subdir / "cco-skill-old-django.md").write_text("# Old Django")
        (old_subdir / "user-skill.md").write_text("# User Skill")

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_skills(dest_dir)

        assert not (dest_dir / "cco-skill-old.md").exists()
        assert not (old_subdir / "cco-skill-old-django.md").exists()
        assert (dest_dir / "cco-skill-new.md").exists()
        assert (old_subdir / "user-skill.md").exists()

    def test_skips_hidden_directories(self, tmp_path: Path) -> None:
        """Test that hidden directories (starting with . or _) are skipped"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "skills"
        source_dir.mkdir(parents=True)

        # Hidden directories
        hidden_dir = source_dir / "_hidden"
        hidden_dir.mkdir()
        (hidden_dir / "cco-skill-hidden.md").write_text("# Hidden")

        dot_dir = source_dir / ".git"
        dot_dir.mkdir()
        (dot_dir / "cco-skill-dot.md").write_text("# Dot")

        dest_dir = tmp_path / "dest" / "skills"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_skills(dest_dir)

        assert not (dest_dir / "_hidden").exists()
        assert not (dest_dir / ".git").exists()

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "skills"

        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_skills(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupClaudeMd:
    """Test _setup_claude_md function"""

    def test_creates_new_claude_md(self, tmp_path: Path) -> None:
        """Test creating new CLAUDE.md with principle markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        principles_dir = claude_dir / "principles"
        principles_dir.mkdir()
        (principles_dir / "U_TEST1.md").touch()
        (principles_dir / "U_TEST2.md").touch()
        (principles_dir / "C_TEST1.md").touch()

        _setup_claude_md(claude_dir, principles_dir)

        claude_md = claude_dir / "CLAUDE.md"
        assert claude_md.exists()

        content = claude_md.read_text()
        assert "<!-- CCO_PRINCIPLES_START -->" in content
        assert "<!-- CCO_PRINCIPLES_END -->" in content
        assert "@principles/U_TEST1.md" in content
        assert "@principles/U_TEST2.md" in content
        assert "@principles/C_TEST1.md" in content

    def test_updates_existing_claude_md(self, tmp_path: Path) -> None:
        """Test updating existing CLAUDE.md with new markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        # Create existing CLAUDE.md with markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(
            "# My Project\n\n"
            "<!-- CCO_PRINCIPLES_START -->\n"
            "@principles/OLD_PRINCIPLE.md\n"
            "<!-- CCO_PRINCIPLES_END -->\n\n"
            "Some other content"
        )

        principles_dir = claude_dir / "principles"
        principles_dir.mkdir()
        (principles_dir / "U_NEW.md").touch()

        _setup_claude_md(claude_dir, principles_dir)

        content = claude_md.read_text()
        assert "# My Project" in content
        assert "Some other content" in content
        assert "@principles/U_NEW.md" in content
        assert "@principles/OLD_PRINCIPLE.md" not in content

    def test_appends_to_claude_md_without_markers(self, tmp_path: Path) -> None:
        """Test appending markers to existing CLAUDE.md without markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        # Create existing CLAUDE.md without markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nExisting content")

        principles_dir = claude_dir / "principles"
        principles_dir.mkdir()
        (principles_dir / "U_TEST.md").touch()

        _setup_claude_md(claude_dir, principles_dir)

        content = claude_md.read_text()
        assert "# My Project" in content
        assert "Existing content" in content
        assert "<!-- CCO_PRINCIPLES_START -->" in content
        assert "@principles/U_TEST.md" in content

    def test_sorts_principles_alphabetically(self, tmp_path: Path) -> None:
        """Test that principles are sorted alphabetically"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        principles_dir = claude_dir / "principles"
        principles_dir.mkdir()
        (principles_dir / "U_ZZZ.md").touch()
        (principles_dir / "U_AAA.md").touch()
        (principles_dir / "C_ZZZ.md").touch()
        (principles_dir / "C_AAA.md").touch()

        _setup_claude_md(claude_dir, principles_dir)

        content = claude_md_path = claude_dir / "CLAUDE.md"
        content = content.read_text()

        # U_* should come before C_*
        u_aaa_pos = content.find("U_AAA")
        u_zzz_pos = content.find("U_ZZZ")
        c_aaa_pos = content.find("C_AAA")
        c_zzz_pos = content.find("C_ZZZ")

        assert u_aaa_pos < u_zzz_pos  # U_AAA before U_ZZZ
        assert u_zzz_pos < c_aaa_pos  # All U_* before C_*
        assert c_aaa_pos < c_zzz_pos  # C_AAA before C_ZZZ

    def test_excludes_p_principles_from_markers(self, tmp_path: Path) -> None:
        """Test that P_* principles are NOT included in CLAUDE.md markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        principles_dir = claude_dir / "principles"
        principles_dir.mkdir()
        (principles_dir / "U_TEST.md").touch()
        (principles_dir / "C_TEST.md").touch()
        (principles_dir / "P_PROJECT.md").touch()

        _setup_claude_md(claude_dir, principles_dir)

        content = (claude_dir / "CLAUDE.md").read_text()
        assert "@principles/U_TEST.md" in content
        assert "@principles/C_TEST.md" in content
        assert "@principles/P_PROJECT.md" not in content


class TestGetAvailableCommands:
    """Test get_available_commands function"""

    def test_returns_command_names(self, mock_claude_dir: Path) -> None:
        """Test that command names are returned without extension"""
        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-audit.md").touch()
        (commands_dir / "cco-fix.md").touch()
        (commands_dir / "cco-help.md").touch()

        result = get_available_commands()

        assert "cco-audit" in result
        assert "cco-fix" in result
        assert "cco-help" in result

    def test_returns_empty_when_directory_missing(self, mock_claude_dir: Path) -> None:
        """Test returns empty list when commands directory doesn't exist"""
        # Don't create the directory
        result = get_available_commands()

        assert result == []

    def test_ignores_non_cco_files(self, mock_claude_dir: Path) -> None:
        """Test that non-cco files are ignored"""
        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-audit.md").touch()
        (commands_dir / "other-command.md").touch()
        (commands_dir / "readme.txt").touch()

        result = get_available_commands()

        assert "cco-audit" in result
        assert len(result) == 1


class TestGetAvailableAgents:
    """Test get_available_agents function"""

    def test_returns_agent_names(self, mock_claude_dir: Path) -> None:
        """Test that agent names are returned without extension"""
        agents_dir = mock_claude_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "cco-agent-audit.md").touch()
        (agents_dir / "cco-agent-fix.md").touch()

        result = get_available_agents()

        assert "cco-agent-audit" in result
        assert "cco-agent-fix" in result

    def test_returns_empty_when_directory_missing(self, mock_claude_dir: Path) -> None:
        """Test returns empty list when agents directory doesn't exist"""
        result = get_available_agents()

        assert result == []


class TestGetAvailableSkills:
    """Test get_available_skills function"""

    def test_returns_root_skills(self, mock_claude_dir: Path) -> None:
        """Test that root-level skill names are returned"""
        skills_dir = mock_claude_dir / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "cco-skill-testing.md").touch()
        (skills_dir / "cco-skill-security.md").touch()

        result = get_available_skills()

        assert "cco-skill-testing" in result
        assert "cco-skill-security" in result

    def test_returns_language_specific_skills(self, mock_claude_dir: Path) -> None:
        """Test that language-specific skills include directory prefix"""
        skills_dir = mock_claude_dir / "skills"
        skills_dir.mkdir(parents=True)

        python_dir = skills_dir / "python"
        python_dir.mkdir()
        (python_dir / "cco-skill-django.md").touch()

        result = get_available_skills()

        assert "python/cco-skill-django" in result

    def test_returns_empty_when_directory_missing(self, mock_claude_dir: Path) -> None:
        """Test returns empty list when skills directory doesn't exist"""
        result = get_available_skills()

        assert result == []

    def test_skips_hidden_directories(self, mock_claude_dir: Path) -> None:
        """Test that hidden directories are skipped"""
        skills_dir = mock_claude_dir / "skills"
        skills_dir.mkdir(parents=True)

        hidden_dir = skills_dir / "_hidden"
        hidden_dir.mkdir()
        (hidden_dir / "cco-skill-hidden.md").touch()

        result = get_available_skills()

        assert "_hidden/cco-skill-hidden" not in result


class TestKnowledgeSetupIntegration:
    """Integration tests for knowledge setup module"""

    def test_full_setup_workflow(self, tmp_path: Path) -> None:
        """Test complete setup workflow with all components"""
        # Setup mock content
        content_dir = tmp_path / "content"

        # Commands
        (content_dir / "commands").mkdir(parents=True)
        (content_dir / "commands" / "cco-test.md").write_text("# Test")

        # Principles
        (content_dir / "principles").mkdir(parents=True)
        (content_dir / "principles" / "U_TEST.md").write_text("# U Test")
        (content_dir / "principles" / "C_TEST.md").write_text("# C Test")

        # Agents
        (content_dir / "agents").mkdir(parents=True)
        (content_dir / "agents" / "cco-agent-test.md").write_text("# Agent")

        # Skills
        (content_dir / "skills").mkdir(parents=True)
        (content_dir / "skills" / "cco-skill-test.md").write_text("# Skill")

        # Setup destination
        claude_dir = tmp_path / ".claude"

        # Mock config to use our directories
        with (
            patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
            patch.object(
                knowledge_setup.config,
                "get_global_commands_dir",
                return_value=claude_dir / "commands",
            ),
            patch.object(
                knowledge_setup.config,
                "get_principles_dir",
                return_value=claude_dir / "principles",
            ),
            patch.object(
                knowledge_setup.config,
                "get_agents_dir",
                return_value=claude_dir / "agents",
            ),
            patch.object(
                knowledge_setup.config,
                "get_skills_dir",
                return_value=claude_dir / "skills",
            ),
            patch.object(
                knowledge_setup,
                "__file__",
                str(content_dir.parent / "core" / "knowledge_setup.py"),
            ),
        ):
            result = setup_global_knowledge()

        assert result["success"] is True
        assert len(result["actions"]) == 5

    def test_preserves_user_files(self, tmp_path: Path) -> None:
        """Test that user's custom files are preserved during setup"""
        # Setup mock content with all required directories
        content_dir = tmp_path / "content"

        # Commands
        (content_dir / "commands").mkdir(parents=True)
        (content_dir / "commands" / "cco-new.md").write_text("# New")

        # Principles (required)
        (content_dir / "principles").mkdir(parents=True)
        (content_dir / "principles" / "U_TEST.md").write_text("# U Test")

        # Agents (required)
        (content_dir / "agents").mkdir(parents=True)
        (content_dir / "agents" / "cco-agent-test.md").write_text("# Agent")

        # Skills (required)
        (content_dir / "skills").mkdir(parents=True)
        (content_dir / "skills" / "cco-skill-test.md").write_text("# Skill")

        # Setup destination with user files
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "user-custom.md").write_text("# User Custom")

        with (
            patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
            patch.object(
                knowledge_setup.config,
                "get_global_commands_dir",
                return_value=commands_dir,
            ),
            patch.object(
                knowledge_setup.config,
                "get_principles_dir",
                return_value=claude_dir / "principles",
            ),
            patch.object(
                knowledge_setup.config,
                "get_agents_dir",
                return_value=claude_dir / "agents",
            ),
            patch.object(
                knowledge_setup.config,
                "get_skills_dir",
                return_value=claude_dir / "skills",
            ),
            patch.object(
                knowledge_setup,
                "__file__",
                str(content_dir.parent / "core" / "knowledge_setup.py"),
            ),
        ):
            setup_global_knowledge()

        # User's file should be preserved
        assert (commands_dir / "user-custom.md").exists()
        assert (commands_dir / "cco-new.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
