# CCO Templates

This directory contains all template files for creating new CCO components.

---

## Available Templates

### 1. Command Template
**File**: `_template-command.md`
**Purpose**: Template for creating new CCO commands
**Features**:
- Complete command structure with all required sections
- Command prompt support (default behavior)
- Step 0: Introduction and confirmation
- Step 0.5: Project context discovery (optional)
- Phase-based execution with explicit transitions
- AskUserQuestion for all user interactions
- Complete accounting (total = completed + skipped + failed + cannot-do)
- No hardcoded examples (uses {PLACEHOLDERS})
- TodoWrite integration for progress tracking

**Usage**:
```bash
# Copy template
cp claudecodeoptimizer/content/templates/_template-command.md \
   claudecodeoptimizer/content/commands/cco-[command-name].md

# Edit and replace all [placeholders] with actual content
```

---

### 2. Skill Template
**File**: `_template-skill.md`
**Purpose**: Template for creating new CCO skills
**Features**:
- Skill metadata (keywords, categories, pain points)
- Domain knowledge and best practices
- Pattern detection rules
- Fix/generation guidelines
- Integration with CCO Rules

**Usage**:
```bash
# Copy template
cp claudecodeoptimizer/content/templates/_template-skill.md \
   claudecodeoptimizer/content/skills/cco-skill-[skill-name].md

# Edit and add domain-specific knowledge
```

---

### 3. Agent Template
**File**: `_template-agent.md`
**Purpose**: Template for creating new CCO agents
**Features**:
- Agent role and capabilities
- Tools available to agent
- Model selection guidance
- Execution patterns
- Success criteria

**Usage**:
```bash
# Copy template
cp claudecodeoptimizer/content/templates/_template-agent.md \
   claudecodeoptimizer/content/agents/cco-agent-[agent-name].md

# Edit and define agent behavior
```

---

### 4. Metadata Template
**File**: `_METADATA_TEMPLATE.md`
**Purpose**: Template for component metadata (frontmatter)
**Features**:
- YAML frontmatter structure
- Required fields (name, description, type)
- Optional fields (keywords, categories, pain points, parameters)
- Parameter metadata structure

**Usage**:
Used within other templates for frontmatter sections.

---

## Template Design Standards

All templates follow CCO Component Design Standards:

1. **No Hardcoded Examples** - Use `{PLACEHOLDERS}` instead
2. **Native Tool Interactions** - Use `AskUserQuestion` for all user input
3. **MultiSelect "All" Option** - Every multiSelect has "All" as first option
4. **100% Honest Reporting** - Never claim completion without verification
5. **Complete Accounting** - Every item tracked (completed + skipped + failed + cannot-do = total)
6. **Progress Transparency** - Show "Phase X/Y (Z%)" for long operations
7. **Command Prompt Support** - Accept optional context: `/cco-command --flag "context"`

See `README.md` in parent directory for full CCO Rules documentation.

---

## Creating New Components

### Step 1: Copy Template
```bash
cp templates/_template-[type].md [type]/cco-[type]-[name].md
```

### Step 2: Update Metadata
Edit frontmatter (YAML section at top) with:
- Unique name
- Clear description
- Relevant keywords
- Pain point mappings
- Parameters (if applicable)

### Step 3: Replace All Placeholders
Find and replace:
- `[command-name]` → actual name
- `[Description]` → actual description
- `{FILE_PATH}` → keep as placeholder in examples
- `{LINE_NUMBER}` → keep as placeholder in examples
- All other `[placeholders]` → actual content

### Step 4: Verify Compliance
Run checks:
```bash
# Check for hardcoded examples
python .tmp/scan_hardcoded_examples.py

# Verify standards adherence
grep -n "AskUserQuestion" [your-file].md
grep -n "TodoWrite" [your-file].md
```

### Step 5: Test
- Test command execution
- Verify all user interactions use native tools
- Ensure complete accounting in results
- Check that no hardcoded examples appear in output

---

## Template Maintenance

When updating templates:
1. Update this README if adding new templates
2. Ensure all templates follow latest standards
3. Test template by creating actual component from it
4. Update TODO.md if template changes affect pending tasks
5. Document any breaking changes in template structure

---

## Questions?

See main README.md for comprehensive CCO documentation.
