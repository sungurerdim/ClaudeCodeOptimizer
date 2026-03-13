---
description: Check for updates and upgrade CCO to the latest version. Use when checking for CCO updates or upgrading.
argument-hint: "[--auto] [--check]"
allowed-tools:
  - WebFetch
  - Read
  - Edit
  - Bash
  - AskUserQuestion
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

1. Run `cco version --json` via Bash → parse `{"version":"X.Y.Z"}`. If `cco` is not in PATH or returns `{"installed":false}`, fall back to: Read `~/.claude/rules/cco-rules.md` and extract `cco_version` from YAML frontmatter.
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

> **Note:** These commands are identical to the installation commands in `docs/getting-started.md`.
> Update both files if the binary distribution scheme changes.

**macOS / Linux:**
```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') && mkdir -p ~/.local/bin && curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$ARCH -o ~/.local/bin/cco && chmod +x ~/.local/bin/cco && ~/.local/bin/cco install
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

## Auto-Check via Hook (Optional)

Users can configure an `InstructionsLoaded` hook to auto-trigger update checks on session start. Add to Claude Code settings (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "InstructionsLoaded": [{
      "command": "echo 'Run /cco-update --check to check for updates'",
      "once": true
    }]
  }
}
```

This fires once per session when CCO rules are loaded. The `once: true` flag prevents repeated triggers.
