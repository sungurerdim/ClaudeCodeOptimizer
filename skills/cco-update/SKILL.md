---
description: Check for updates and upgrade CCO to the latest version. Use when checking for CCO updates or upgrading.
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

1. Use the Read tool to read the **installed** `~/.claude/rules/cco-rules.md` (resolve `~` to user home). Extract `cco_version` from YAML frontmatter.
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

### Step 3: Run Install One-liner

Detect platform, run the appropriate install one-liner:

**macOS / Linux:**
```bash
mkdir -p ~/.local/bin && curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o ~/.local/bin/cco && chmod +x ~/.local/bin/cco && ~/.local/bin/cco install
```

**Windows (PowerShell):**
```powershell
$b="$HOME\.local\bin"; New-Item $b -ItemType Directory -Force >$null; irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile "$b\cco.exe"; & "$b\cco.exe" install
```

### Step 4: Verify & Summary

Read the **installed** `~/.claude/rules/cco-rules.md` from disk → confirm `cco_version` matches latest.

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest}` |
| Interactive | Version info, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."
