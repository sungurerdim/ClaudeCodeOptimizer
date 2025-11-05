---
description: Sync files across codebase (config, deps, types, constants)
category: sync
cost: 1
---

# CCO Sync Commands

Keep files synchronized across your codebase: configuration, dependencies, type definitions, and constants.

**Architecture:** Primarily Haiku (fast data operations)
- **Haiku**: Config sync, type sync, constants - data comparison and updates
- **Sonnet**: Only for complex dependency conflicts - reasoning about breaking changes

---

## Step 1: Select What to Sync

**Use AskUserQuestion tool**:

```json
{
  "questions": [{
    "question": "What would you like to synchronize?",
    "header": "Sync",
    "multiSelect": true,
    "options": [
      {"label": "All", "description": "Sync everything below (recommended, Haiku - fast)"},
      {"label": "Config Files", "description": "Keep tsconfig, .eslintrc, pyproject.toml in sync (Haiku)"},
      {"label": "Dependencies", "description": "Sync package.json, requirements.txt, go.mod across services (Haiku/Sonnet)"},
      {"label": "Type Definitions", "description": "Sync TypeScript types, Python protocols across modules (Haiku)"},
      {"label": "Constants", "description": "Sync shared constants, enums, config values (Haiku)"}
    ]
  }]
}
```

---

## Sync: All

Run all sync operations below.

---

## Sync: Config Files

**Keep configuration files consistent across services/modules**

**Method:** Haiku Explore agent (fast data comparison)

### Detect Config Files

- `tsconfig.json`, `.eslintrc.json`, `prettier.config.js`
- `pyproject.toml`, `.flake8`, `mypy.ini`
- `.editorconfig`, `.gitignore`

### Sync Process

```
Task: Sync configuration files
Agent: Explore
Model: haiku
Thoroughness: quick

1. Find all config files of same type
2. Identify canonical version (most complete)
3. For each other version:
   - Merge unique settings
   - Update outdated settings
   - Preserve environment-specific settings
4. Write back merged configs
```

**Why Haiku:** Config sync is data comparison and merging. No complex reasoning required.

### Example: TypeScript Config

```typescript
// Service A: tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020"
  }
}

// Service B: tsconfig.json (outdated)
{
  "compilerOptions": {
    "target": "ES2015"  // ← Sync to ES2020
  }
}
```

---

## Sync: Dependencies

**Sync package versions across services in monorepo**

**Method:** Hybrid - Haiku for scanning, Sonnet only if conflicts

### Detect Dependency Files

- `package.json` (JavaScript/TypeScript)
- `requirements.txt`, `pyproject.toml` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)

### Sync Strategy (Phase 1: Scanning with Haiku)

```
Task: Scan and sync simple dependencies
Agent: Explore
Model: haiku
Thoroughness: quick

1. Scan all dependency files
2. Group by package name
3. For minor/patch version differences:
   - Update to highest semantic version
   - Apply automatically (safe)
4. For major version differences:
   - Flag for Sonnet analysis
5. Run install to verify compatibility
```

**Why Haiku:** Most dependency syncs are minor/patch updates (safe). Fast scanning and automatic updates.

### Sync Strategy (Phase 2: Conflicts with Sonnet)

Only run if major version conflicts detected:

```
Task: Resolve dependency conflicts
Agent: Plan
Model: sonnet

For each flagged major version conflict:
1. Check for breaking changes in changelog
2. Assess impact on existing code
3. Recommend upgrade path or pin version
4. Generate migration guide if needed
```

**Why Sonnet:** Major version upgrades require understanding breaking changes and migration strategies.

### Example: Package Version Sync

```
Service A: "react": "18.2.0"
Service B: "react": "18.1.5"  ← Upgrade to 18.2.0 [Haiku - automatic]

Service C: "react": "17.0.2"  ← Major version conflict [Sonnet - analysis]
⚠️  Major version change detected
   Sonnet analyzing breaking changes...
```

---

## Sync: Type Definitions

**Sync shared types across modules**

**Method:** Haiku Explore agent (fast code extraction and update)

### Common Use Cases

1. **API Types**: Request/response interfaces
2. **Domain Models**: Shared entities
3. **Enums**: Status codes, roles
4. **Utility Types**: Generic helpers

### Sync Process

```
Task: Sync type definitions
Agent: Explore
Model: haiku
Thoroughness: quick

1. Identify shared types (used in >1 module)
2. Find canonical source (most complete definition)
3. For each usage:
   - Compare with canonical
   - Update if different
   - Preserve module-specific extensions
4. Consider extracting to shared types package
```

**Why Haiku:** Type sync is code extraction and text comparison. No complex reasoning required, fast execution for many files.

### Example: User Type Sync

```typescript
// Module A (canonical)
interface User {
  id: string;
  email: string;
  role: "admin" | "user";
  createdAt: Date;
}

// Module B (outdated)
interface User {
  id: string;
  email: string;
  // Missing: role, createdAt ← Sync these
}
```

---

## Sync: Constants

**Sync shared constants and configuration values**

**Method:** Haiku Explore agent (fast find and replace)

### Common Constants

- API endpoints
- Error codes
- Feature flags
- Environment variables
- Default values

### Sync Process

```
Task: Sync constants
Agent: Explore
Model: haiku
Thoroughness: quick

1. Find all constant definitions (UPPER_CASE, const, enum)
2. Group by name/purpose
3. For duplicates:
   - Verify values match
   - If different, prompt user for canonical value
   - Update all occurrences
4. Suggest extracting to shared config file
```

**Why Haiku:** Constant sync is pattern matching and replacement. Simple data operation, fast execution.

### Example: API URL Sync

```javascript
// Service A
const API_URL = "https://api.example.com/v2";

// Service B (outdated)
const API_URL = "https://api.example.com/v1";  ← Sync to v2

// Service C (hardcoded)
fetch("https://api.example.com/v1/users");  ← Update to API_URL
```

---

## Step 3: Verify Sync

After sync operations:

```bash
# Run tests
npm test  # or pytest, go test, etc.

# Check for build errors
npm run build

# Verify no regressions
```

---

## Step 4: Summary

```
============================================================
SYNC SUMMARY
============================================================

Synced:
✓ Config Files:     5 files updated (tsconfig, .eslintrc) [Haiku - fast]
✓ Dependencies:     3 packages upgraded to consistent versions [Haiku]
✓ Type Definitions: 12 interfaces synced across 4 modules [Haiku - fast]
✓ Constants:        8 constants unified [Haiku - instant]

Files Modified:     23
Services Affected:  4

Test Status:        ✓ All passing
Build Status:       ✓ Success

Performance:
- Haiku: 2-3x faster than Sonnet for data operations
- Sonnet: Only used for complex dependency conflicts
- Total time: ~50-70% faster than all-Sonnet approach

Next Steps:
1. Review changes: git diff
2. Commit: git commit -m "Sync configs, deps, types"
3. Deploy services in order: [list]
============================================================
```

---

## Safety Features

1. **Backup**: Create git branch before sync
2. **Verification**: Run tests after each sync
3. **Rollback**: Revert if tests fail
4. **Prompts**: Ask user for major version changes

---

## Error Handling

- **Merge conflicts**: Prompt user to resolve manually
- **Breaking changes**: Warn and ask for confirmation
- **Test failures**: Rollback sync for that file
- **No changes found**: Inform user all is in sync

---

## Related Commands

- `/cco-audit` - Find inconsistencies
- `/cco-fix` - Fix issues found
- `/cco-config export` - Share config across team
