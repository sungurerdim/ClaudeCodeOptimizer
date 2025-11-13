---
id: cco-commit
description: Smart git commit with AI-powered semantic analysis and grouping
category: tools
priority: high
---

# CCO Smart Git Commit

AI-powered commit helper for **${PROJECT_NAME}**. Analyzes changes semantically, groups logically related files, generates high-quality conventional commit messages.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

---

## Architecture

**Skill Layer (Mekanik)**: Git operations utility
**Command Layer (AI)**: Semantic analysis + grouping + message generation

**Model**: Sonnet (reasoning required for semantic understanding)

---

## Prerequisites

```python
from pathlib import Path
import sys

# Add CCO to path
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

print("📚 Loading git commit helper...\n")
```

---

## Phase 1: Gather Changes

Get all uncommitted changes and their diffs:

```python
from claudecodeoptimizer.skills.commit_skill import GitCommitHelper

helper = GitCommitHelper(Path("."))
files = helper.get_uncommitted_changes()

if not files:
    print("✓ No uncommitted changes")
    import sys
    sys.exit(0)

print(f"Found {len(files)} uncommitted file(s):\n")

# Show files with status
file_summary = helper.get_file_summary(files)
print(file_summary)
print()

# Get full diff for AI analysis
full_diff = helper.get_diff()
```

---

## Phase 2: AI Semantic Analysis

**CRITICAL**: Use AI (you!) to analyze changes and propose logical commit groups.

Analyze the changes above and create commit proposals following these rules:

### Analysis Guidelines

1. **Group by logical purpose**, not by file location
   - Example: "Add versioning feature" includes wizard/, schemas/, core/ files
   - NOT: Separate commits for each directory

2. **Identify related changes**
   - Files changed together for same feature → same commit
   - Documentation updates for feature → include in feature commit
   - TODO.md updates → include in relevant feature commit

3. **Follow conventional commits**
   - `feat(scope):` - New features
   - `fix(scope):` - Bug fixes
   - `docs(scope):` - Documentation only
   - `refactor(scope):` - Code refactoring
   - `test(scope):` - Tests
   - `chore(scope):` - Maintenance

4. **Scope selection**
   - Use specific scope from path (wizard, skills, core, etc.)
   - For multi-scope changes, use most prominent scope
   - Example: Changes in skills/ + commands/ → use "skills" if that's primary

5. **Subject line quality**
   - Descriptive, not generic
   - ✅ "add smart commit with atomic grouping"
   - ❌ "update 5 files"
   - ✅ "add versioning strategy selection"
   - ❌ "update wizard"

6. **Bullet points**
   - Describe what was implemented/changed
   - ✅ "Implement CommitSkill class with context detection"
   - ❌ "Add commit_skill.py"
   - ✅ "Add versioning_strategy field to preferences schema"
   - ❌ "Update preferences.py"

### Example Analysis

Given these changes:
```
[M ] wizard/orchestrator.py
[M ] schemas/preferences.py
[A ] core/version_manager.py
[M ] docs/principles/git-workflow.md
[M ] TODO.md
```

**Good grouping:**
```
Commit 1: feat(wizard): add versioning strategy selection

- Add versioning_strategy field to preferences schema
- Update orchestrator to map versioning answers to preferences
- Implement VersionManager for automated version detection
- Add P052 automated versioning principle
- Mark P0.8 Task 1 complete in TODO.md
```

**Bad grouping:**
```
Commit 1: feat(schemas): update preferences
- Update preferences.py

Commit 2: feat(wizard): update orchestrator
- Update orchestrator.py

Commit 3: feat(core): add version manager
- Add version_manager.py

Commit 4: docs(docs): update git-workflow
- Update git-workflow.md

Commit 5: docs(repo): update TODO
- Update TODO.md
```

---

## Phase 3: Present Proposals

After analyzing, present your proposals:

```python
# You will provide proposals in this format:
proposals = [
    {
        "type": "feat",
        "scope": "skills",
        "subject": "add smart commit with atomic grouping",
        "body": [
            "- Implement GitCommitHelper for git operations",
            "- Add CCO enhancement command with AI analysis",
            "- Simplify skill to utility layer (600→210 lines)",
            "- Move semantic logic to AI command layer"
        ],
        "files": [
            "claudecodeoptimizer/skills/commit_skill.py",
            "claudecodeoptimizer/commands/commit.md",
            ".claude/skills/commit.md"
        ]
    }
]

print("=== Proposed Commits ===\n")

for i, proposal in enumerate(proposals, 1):
    print(f"Commit {i}: {proposal['type']}({proposal['scope']})")
    print(f"Subject: {proposal['subject']}")
    print(f"\nFiles ({len(proposal['files'])}):")
    for file in proposal['files']:
        print(f"  - {file}")
    print(f"\nMessage:")
    for line in proposal['body']:
        print(f"  {line}")
    print()
```

---

## Phase 4: User Approval

Ask for confirmation before creating commits:

```python
response = input("Create these commits? [Y/n] ").strip().lower()

if response and response != "y":
    print("\n❌ Cancelled by user")
    import sys
    sys.exit(1)
```

---

## Phase 5: Create Commits

Execute the approved commits:

```python
from claudecodeoptimizer.skills.commit_skill import CommitProposal

print("\n=== Creating Commits ===\n")

created_hashes = []

for i, proposal_dict in enumerate(proposals, 1):
    # Convert dict to CommitProposal
    proposal = CommitProposal(
        type=proposal_dict["type"],
        scope=proposal_dict["scope"],
        subject=proposal_dict["subject"],
        body=proposal_dict["body"],
        files=proposal_dict["files"]
    )

    # Stage files
    if not helper.stage_files(proposal.files):
        print(f"❌ Failed to stage files for commit {i}")
        continue

    # Format message
    message = helper.format_commit_message(proposal)

    # Create commit
    commit_hash = helper.create_commit(message)

    if commit_hash:
        created_hashes.append(commit_hash)
        print(f"✓ Created commit {commit_hash}: {proposal.type}({proposal.scope})")
    else:
        print(f"❌ Failed to create commit {i}")

print(f"\n✅ Created {len(created_hashes)} commit(s)")
```

---

## Phase 6: Optional Push

```python
push_response = input("\nPush to remote? [y/N] ").strip().lower()

if push_response == "y":
    print("\n=== Pushing to Remote ===\n")

    if helper.push():
        print("✅ Successfully pushed to remote")
    else:
        print("❌ Push failed. Check remote configuration.")
else:
    print("\n✓ Commits created locally. Use 'git push' when ready.")
```

---

## Quality Standards

**Your analysis must produce commits like these:**

✅ **Good Examples** (from git history):
```
feat(knowledge): add custom agent/skill templates and sync workflow

- Add agent template with structured format (_template-agent.md)
- Add skill template with workflow format (_template-skill.md)
- Add comprehensive README files for agents and skills directories
- Update knowledge_setup.py to copy templates to global storage
- Add "Knowledge Base Sync" section to sync.md command
- Filter template files from available agents/skills lists

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
feat(principles): add universal principles system

- Add U001-U012 universal principles (always active)
- Migrate from principles.json to .md frontmatter (SSOT)
- Add python-frontmatter for metadata parsing
- Add principle_md_loader module for unified loading
- Update 6 core files to use new loader

Co-Authored-By: Claude <noreply@anthropic.com>
```

❌ **Bad Examples** (avoid):
```
feat(claudecodeoptimizer): update 5 files
- Update preferences.py
- Update orchestrator.py
- Add commit.md
- Add __init__.py
- Add commit_skill.py
```

```
docs(repo): update TODO.md
- Update TODO
```

---

## Notes

**Why AI analysis?**
- Mekanik grouping `(type, scope)` → 10+ commits (too granular)
- AI semantic analysis → 2-3 logical commits (proper atomicity)
- AI understands "this is all one feature" across multiple files

**Skill vs Command split:**
- **Skill**: Pure git operations (stage, commit, push)
- **Command**: AI reasoning (analysis, grouping, message generation)

**Model choice:**
- Sonnet required (not Haiku) for semantic understanding

---

*Smart commits powered by AI reasoning + clean git utilities*
