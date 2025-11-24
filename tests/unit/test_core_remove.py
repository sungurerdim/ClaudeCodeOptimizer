"""
Unit tests for Core Remove Module

Tests CCORemover class and remove_cco function for clean uninstallation.
Target Coverage: 100%
"""

import pytest

from claudecodeoptimizer.core.remove import CCORemover, remove_cco


class TestCCORemover:
    """Test CCORemover class"""

    def test_init_sets_claude_dir(self, tmp_path, monkeypatch) -> None:
        """Test that __init__ sets claude_dir to ~/.claude/"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        remover = CCORemover()
        assert remover.claude_dir == tmp_path / ".claude"

    def test_remove_returns_success_result(self, tmp_path, monkeypatch) -> None:
        """Test that remove() returns success result dict"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        remover = CCORemover()
        result = remover.remove()

        assert result["success"] is True
        assert "actions" in result
        assert (
            len(result["actions"]) == 7
        )  # agents, commands, skills, principles, standards, templates, claude.md

    def test_remove_without_cleaning_claude_md(self, tmp_path, monkeypatch) -> None:
        """Test remove() without cleaning CLAUDE.md"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        remover = CCORemover()
        result = remover.remove(clean_claude_md=False)

        assert result["success"] is True
        assert (
            len(result["actions"]) == 6
        )  # agents, commands, skills, principles, standards, templates (no claude.md)


class TestRemoveCommands:
    """Test _remove_commands method"""

    def test_removes_cco_commands(self, tmp_path, monkeypatch) -> None:
        """Test that CCO command files are removed"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(parents=True)

        # Create CCO command files
        cco_files = ["cco-audit.md", "cco-fix.md", "cco-generate.md"]
        for filename in cco_files:
            (commands_dir / filename).write_text("content")

        # Create non-CCO file (should not be removed)
        other_file = commands_dir / "other-command.md"
        other_file.write_text("other content")

        remover = CCORemover()
        remover._remove_commands()

        # CCO files should be removed
        for filename in cco_files:
            assert not (commands_dir / filename).exists()

        # Non-CCO file should remain
        assert other_file.exists()

    def test_handles_missing_commands_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing commands directory is handled gracefully"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        # commands dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_commands()

    def test_handles_unlink_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that unlink errors are logged and skipped"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(parents=True)

        # Create a file
        cmd_file = commands_dir / "cco-test.md"
        cmd_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_cco_test(self, *args: object, **kwargs: object) -> None:
            if "cco-test.md" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_cco_test)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_commands()

        # File should still exist since unlink failed
        assert cmd_file.exists()


class TestRemovePrinciples:
    """Test _remove_principles method"""

    def test_removes_all_principle_patterns(self, tmp_path, monkeypatch) -> None:
        """Test that U_*, C_*, P_*.md files are removed"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        principles_dir = claude_dir / "principles"
        principles_dir.mkdir(parents=True)

        # Create CCO principle files for all patterns
        cco_files = [
            "U_CHANGE_VERIFICATION.md",
            "U_DRY.md",
            "C_FOLLOW_PATTERNS.md",
            "C_MODEL_SELECTION.md",
            "P_CUSTOM.md",
        ]
        for filename in cco_files:
            (principles_dir / filename).write_text("content")

        # Create non-CCO file
        other_file = principles_dir / "other-principle.md"
        other_file.write_text("other content")

        remover = CCORemover()
        remover._remove_principles()

        # CCO files should be removed
        for filename in cco_files:
            assert not (principles_dir / filename).exists()

        # Non-CCO file should remain
        assert other_file.exists()

    def test_handles_missing_principles_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing principles directory is handled gracefully"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        # principles dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_principles()

    def test_handles_unlink_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that unlink errors are logged and skipped (lines 168-169)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        principles_dir = claude_dir / "principles"
        principles_dir.mkdir(parents=True)

        # Create files
        principle_file = principles_dir / "U_TEST.md"
        principle_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_principle(self, *args: object, **kwargs: object):
            if "U_TEST.md" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_principle)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_principles()

        # File should still exist since unlink failed
        assert principle_file.exists()


class TestRemoveAgents:
    """Test _remove_agents method"""

    def test_removes_cco_agents(self, tmp_path, monkeypatch) -> None:
        """Test that CCO agent files are removed"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        agents_dir = claude_dir / "agents"
        agents_dir.mkdir(parents=True)

        # Create CCO agent files
        cco_files = ["cco-agent-audit.md", "cco-agent-fix.md"]
        for filename in cco_files:
            (agents_dir / filename).write_text("content")

        # Create non-CCO file
        other_file = agents_dir / "other-agent.md"
        other_file.write_text("other content")

        remover = CCORemover()
        remover._remove_agents()

        # CCO files should be removed
        for filename in cco_files:
            assert not (agents_dir / filename).exists()

        # Non-CCO file should remain
        assert other_file.exists()

    def test_handles_missing_agents_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing agents directory is handled gracefully"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        # agents dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_agents()

    def test_handles_agent_unlink_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that agent unlink errors are logged (lines 182-183)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        agents_dir = claude_dir / "agents"
        agents_dir.mkdir(parents=True)

        # Create files
        agent_file = agents_dir / "cco-agent-test.md"
        agent_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_agent(self, *args: object, **kwargs: object):
            if "cco-agent-test.md" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_agent)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_agents()

        # File should still exist since unlink failed
        assert agent_file.exists()


class TestRemoveSkills:
    """Test _remove_skills method"""

    def test_removes_cco_skills(self, tmp_path, monkeypatch) -> None:
        """Test that CCO skill files are removed"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir(parents=True)

        # Create CCO skill files
        cco_files = ["cco-skill-test.md", "cco-skill-security.md"]
        for filename in cco_files:
            (skills_dir / filename).write_text("content")

        # Create non-CCO file
        other_file = skills_dir / "other-skill.md"
        other_file.write_text("other content")

        remover = CCORemover()
        remover._remove_skills()

        # CCO files should be removed
        for filename in cco_files:
            assert not (skills_dir / filename).exists()

        # Non-CCO file should remain
        assert other_file.exists()

    def test_removes_skills_recursively(self, tmp_path, monkeypatch) -> None:
        """Test that CCO skill files in subdirectories are removed"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        skills_dir = claude_dir / "skills"
        subdir = skills_dir / "category"
        subdir.mkdir(parents=True)

        # Create CCO skill files in root and subdirectory
        (skills_dir / "cco-skill-root.md").write_text("content")
        (subdir / "cco-skill-nested.md").write_text("content")

        remover = CCORemover()
        remover._remove_skills()

        # Both files should be removed
        assert not (skills_dir / "cco-skill-root.md").exists()
        assert not (subdir / "cco-skill-nested.md").exists()

    def test_handles_missing_skills_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing skills directory is handled gracefully"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        # skills dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_skills()

    def test_handles_skill_unlink_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that skill unlink errors are logged (lines 196-197)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir(parents=True)

        # Create files
        skill_file = skills_dir / "cco-skill-test.md"
        skill_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_skill(self, *args: object, **kwargs: object):
            if "cco-skill-test.md" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_skill)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_skills()

        # File should still exist since unlink failed
        assert skill_file.exists()


class TestCleanClaudeMd:
    """Test _clean_claude_md method"""

    def test_removes_cco_markers(self, tmp_path, monkeypatch) -> None:
        """Test that CCO markers are removed from CLAUDE.md"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        content = """# My Claude Config

Some user content here.

<!-- CCO_PRINCIPLES_START -->
@principles/U_CHANGE_VERIFICATION.md
@principles/C_FOLLOW_PATTERNS.md
<!-- CCO_PRINCIPLES_END -->

More user content.
"""
        claude_md.write_text(content, encoding="utf-8")

        remover = CCORemover()
        remover._clean_claude_md()

        result = claude_md.read_text(encoding="utf-8")
        assert "CCO_PRINCIPLES_START" not in result
        assert "CCO_PRINCIPLES_END" not in result
        assert "@principles/" not in result
        assert "My Claude Config" in result
        assert "Some user content here" in result
        assert "More user content" in result

    def test_cleans_extra_blank_lines(self, tmp_path, monkeypatch) -> None:
        """Test that extra blank lines are cleaned up"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        content = """# Title


<!-- CCO_PRINCIPLES_START -->
content
<!-- CCO_PRINCIPLES_END -->



More content.
"""
        claude_md.write_text(content, encoding="utf-8")

        remover = CCORemover()
        remover._clean_claude_md()

        result = claude_md.read_text(encoding="utf-8")
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in result

    def test_handles_missing_claude_md(self, tmp_path, monkeypatch) -> None:
        """Test that missing CLAUDE.md is handled gracefully"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        # CLAUDE.md does not exist

        remover = CCORemover()
        # Should not raise
        remover._clean_claude_md()

    def test_handles_no_cco_markers(self, tmp_path, monkeypatch) -> None:
        """Test that CLAUDE.md without CCO markers is handled"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        original_content = "# User Config\n\nSome content.\n"
        claude_md.write_text(original_content, encoding="utf-8")

        remover = CCORemover()
        remover._clean_claude_md()

        result = claude_md.read_text(encoding="utf-8")
        assert "User Config" in result
        assert "Some content" in result

    def test_preserves_file_ending_newline(self, tmp_path, monkeypatch) -> None:
        """Test that file ends with single newline"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        content = "# Title\n\n<!-- CCO_PRINCIPLES_START -->\ncontent\n<!-- CCO_PRINCIPLES_END -->"
        claude_md.write_text(content, encoding="utf-8")

        remover = CCORemover()
        remover._clean_claude_md()

        result = claude_md.read_text(encoding="utf-8")
        assert result.endswith("\n")
        assert not result.endswith("\n\n")


class TestRemoveCcoFunction:
    """Test remove_cco convenience function"""

    def test_calls_remover_with_default(self, tmp_path, monkeypatch) -> None:
        """Test that remove_cco calls CCORemover.remove() with defaults"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        result = remove_cco()

        assert result["success"] is True
        assert len(result["actions"]) == 7

    def test_passes_clean_claude_md_false(self, tmp_path, monkeypatch) -> None:
        """Test that clean_claude_md=False is passed through"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        result = remove_cco(clean_claude_md=False)

        assert result["success"] is True
        assert len(result["actions"]) == 6


class TestRemoveStandardsAndTemplates:
    """Test _remove_standards and _remove_templates methods"""

    def test_removes_standards_with_count(self, tmp_path, monkeypatch) -> None:
        """Test that standards are counted properly (line 81)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Create standards files matching the actual pattern
        (claude_dir / "SKILLS_STANDARDS.md").write_text("skills standard")
        (claude_dir / "AGENTS_STANDARDS.md").write_text("agents standard")
        (claude_dir / "PRINCIPLE_FORMAT.md").write_text("principle format")

        remover = CCORemover()
        counts = remover._get_file_counts()

        # Should count standards files (2 *_STANDARDS.md + 1 PRINCIPLE_FORMAT.md)
        assert counts.get("standards", 0) == 3

    def test_removes_templates_with_count(self, tmp_path, monkeypatch) -> None:
        """Test that templates are counted properly (line 87)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Create template files
        (claude_dir / "settings.json.cco").write_text("settings")
        (claude_dir / "statusline.js.cco").write_text("statusline")

        remover = CCORemover()
        counts = remover._get_file_counts()

        # Should count template files
        assert counts.get("templates", 0) == 2

    def test_handles_standards_removal_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that standards removal errors are logged (lines 218-221)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Create a standards file matching the hardcoded list in _remove_standards
        standards_file = claude_dir / "STANDARDS_SKILLS.md"
        standards_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_standards(self, *args: object, **kwargs: object):
            if "STANDARDS_SKILLS.md" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_standards)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_standards()

        # File should still exist since unlink failed
        assert standards_file.exists()

    def test_handles_templates_removal_error(self, tmp_path, monkeypatch, caplog) -> None:
        """Test that templates removal errors are logged (lines 230-233)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Create a template file
        template_file = claude_dir / "settings.json.cco"
        template_file.write_text("content")

        remover = CCORemover()

        # Mock Path.unlink to raise on this specific file
        from pathlib import Path

        original_unlink = Path.unlink

        def raise_on_template(self, *args: object, **kwargs: object):
            if "settings.json.cco" in str(self):
                raise PermissionError("Cannot delete")
            return original_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(Path, "unlink", raise_on_template)

        # Should not raise, should log
        import logging

        with caplog.at_level(logging.DEBUG):
            remover._remove_templates()

        # File should still exist since unlink failed
        assert template_file.exists()

    def test_handles_missing_standards_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing claude dir for standards is handled (line 202)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        # claude dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_standards()

    def test_handles_missing_templates_dir(self, tmp_path, monkeypatch) -> None:
        """Test that missing claude dir for templates is handled (line 226)"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        # claude dir does not exist

        remover = CCORemover()
        # Should not raise
        remover._remove_templates()


class TestRemoveIntegration:
    """Integration tests for complete removal workflow"""

    def test_full_removal_workflow(self, tmp_path, monkeypatch) -> None:
        """Test complete CCO removal from a fully installed state"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"

        # Set up full CCO installation
        commands_dir = claude_dir / "commands"
        principles_dir = claude_dir / "principles"
        agents_dir = claude_dir / "agents"
        skills_dir = claude_dir / "skills"

        commands_dir.mkdir(parents=True)
        principles_dir.mkdir(parents=True)
        agents_dir.mkdir(parents=True)
        skills_dir.mkdir(parents=True)

        # Create CCO files
        (commands_dir / "cco-audit.md").write_text("audit")
        (commands_dir / "cco-fix.md").write_text("fix")
        (principles_dir / "U_DRY.md").write_text("dry")
        (principles_dir / "C_MODEL.md").write_text("model")
        (agents_dir / "cco-agent-audit.md").write_text("agent")
        (skills_dir / "cco-skill-test.md").write_text("skill")

        # Create CLAUDE.md with markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(
            "# Config\n\n<!-- CCO_PRINCIPLES_START -->\n@principles/U_DRY.md\n<!-- CCO_PRINCIPLES_END -->\n",
            encoding="utf-8",
        )

        # Create non-CCO files (should remain)
        (commands_dir / "user-command.md").write_text("user")
        (principles_dir / "user-principle.md").write_text("user")

        # Run removal
        result = remove_cco()

        # Verify results
        assert result["success"] is True
        assert len(result["actions"]) == 7

        # CCO files should be gone
        assert not (commands_dir / "cco-audit.md").exists()
        assert not (commands_dir / "cco-fix.md").exists()
        assert not (principles_dir / "U_DRY.md").exists()
        assert not (principles_dir / "C_MODEL.md").exists()
        assert not (agents_dir / "cco-agent-audit.md").exists()
        assert not (skills_dir / "cco-skill-test.md").exists()

        # User files should remain
        assert (commands_dir / "user-command.md").exists()
        assert (principles_dir / "user-principle.md").exists()

        # CLAUDE.md should be cleaned
        cleaned_content = claude_md.read_text(encoding="utf-8")
        assert "CCO_PRINCIPLES_START" not in cleaned_content
        assert "Config" in cleaned_content

    def test_removal_with_empty_installation(self, tmp_path, monkeypatch) -> None:
        """Test removal when no CCO files exist"""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        result = remove_cco()

        assert result["success"] is True
        # Should still report actions even if nothing was removed
        assert len(result["actions"]) == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
