---
description: Check for updates and upgrade CCO to the latest version.
argument-hint: "[--auto] [--check]"
allowed-tools: WebFetch, Read, Edit, Bash, AskUserQuestion
disable-model-invocation: true
---

# /cco-update

**Update Manager** — Check for new versions, upgrade in place via `cco install`.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Silent update, no questions |
| `--check` | Version check only, no changes |

Without flags: check for update, ask before upgrading.

## Execution

### Step 1: Version Check

1. Read current `cco_version` from cco-rules.md frontmatter (already in context)
2. WebFetch `https://api.github.com/repos/sungurerdim/ClaudeCodeOptimizer/tags?per_page=1` → extract latest tag name, strip `v` prefix
3. Compare current vs latest semver

**If same version:** Report up to date, update `last_update_check` timestamp in cco-rules.md frontmatter, done.

**--check mode:** Report version info, update `last_update_check` timestamp, done.

### Step 2: Prompt (skip if --auto)

```javascript
AskUserQuestion([{
  question: "New version available (v{current} → v{latest}). What should be done?",
  header: "Upgrade",
  options: [
    { label: "Upgrade now (Recommended)", description: "Download and install the new version" },
    { label: "Skip", description: "Stay on current version" }
  ],
  multiSelect: false
}])
```

### Step 3: Ensure Binary & Run

The `cco install` binary handles everything: download files, legacy cleanup, timestamp update.

**3a. Check if `cco` is on PATH**

```bash
# Windows
where cco 2>nul

# macOS/Linux
which cco 2>/dev/null
```

If found → skip to 3c.

**3b. Download binary (if not on PATH)**

Download to temp location from GitHub releases:

```bash
# Windows (PowerShell)
irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile "$env:TEMP\cco.exe"

# macOS
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-darwin-$(uname -m) -o /tmp/cco && chmod +x /tmp/cco

# Linux
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-linux-$(uname -m) -o /tmp/cco && chmod +x /tmp/cco
```

Use the temp path for the next step.

**3c. Run installer**

```bash
cco install        # if on PATH
# or
/tmp/cco install   # temp path (macOS/Linux)
$env:TEMP\cco.exe install  # temp path (Windows)
```

### Step 4: Verify & Summary

Read cco-rules.md → confirm `cco_version` matches latest.

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest}` |
| Interactive | Version info, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."
