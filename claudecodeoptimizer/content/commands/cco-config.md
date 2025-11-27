---
name: cco-config
description: Configure statusline and permissions
---

# /cco-config

**Configuration** - Detect existing → show details → remove/update/add.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Write | `cco-agent-action` | Create/update config files |

## Pre-Check

Silently detect existing configuration:

```
globalStatusline = exists(~/.claude/statusline.js)
globalSettings = exists(~/.claude/settings.json) with permissions/statusLine
localStatusline = exists(./.claude/statusline.js)
localSettings = exists(./.claude/settings.local.json) with permissions/statusLine
```

If any config exists, show summary:
```
Detected CCO configuration:

Global (~/.claude/):
  [Y] statusline.js  - 5-column grid with git status
  [Y] settings.json  - Permissive (45 allow, 3 ask, 28 deny)

Local (./.claude/):
  [N] statusline.js  - Not configured
  [N] settings.json  - Not configured
```

## Flow

1. **Detect** - Check global/local for statusline.js and settings.json
2. **Action** - If exists: AskUserQuestion → Remove / Update / Add
3. **Remove** - Show details, select items, delete, EXIT
4. **Configure** - Scope + Features + Permission level (single question set)
5. **Validate** - JSON syntax, conflicts, security rules
6. **Write** - Apply changes, preserve non-CCO settings

## Remove Flow

When "Remove" selected, show detailed summary:

```
[Global Statusline] ~/.claude/statusline.js
  Type: 5-column grid with box drawing
  Features: Path, User, Git status, Model info

[Global Permissions] ~/.claude/settings.json
  Mode: Permissive
  Allow: 45 rules (Read, Write, Bash commands...)
  Ask: 3 rules (git push, npm publish)
  Deny: 28 rules (dangerous commands)
  Other: alwaysThinkingEnabled (preserved)
```

AskUserQuestion (multiSelect):
- **All** - Remove all CCO configuration
- **Global Statusline** - statusline.js + statusLine setting
- **Global Permissions** - permissions section only
- **Local Statusline** - local statusline.js + setting
- **Local Permissions** - local permissions section

Actions:
- Delete statusline.js files
- Remove statusLine/permissions keys from settings.json
- Preserve other settings (hooks, mcpServers, etc.)
- If settings.json empty after removal, delete file
- Show removed/preserved summary, then EXIT

## Configure Flow

AskUserQuestion with 3 questions:

**Scope:** Global (~/.claude/) | Local (./.claude/)

**Features (multiSelect):** All | Statusline | Permissions

**Permission level:** Safe | Balanced | Permissive

## Statusline

Target: `{scope}/statusline.js`

Features:
- 5-column grid with box drawing
- Row 1: Path | User | Size | CC Version | Model
- Row 2: Repo:Branch | Conflicts | Stash | Ahead | Last
- Row 3-4: Unstaged/Staged changes with line counts
- Configurable: pathSegments, showHostname, emojiWidth

### Full Code

Write the following JavaScript to `{scope}/statusline.js`. Cross-platform compatible:

```javascript
#!/usr/bin/env node

// Claude Code Statusline - Privacy-Focused & Feature-Rich
// Clean box design with icons, minimal path exposure

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// ============================================================================
// CONFIGURATION
// ============================================================================
const CONFIG = {
  pathSegments: 2,      // Show last N path segments (0 = hide)
  showHostname: false,  // true = user@host, false = just user
  emojiWidth: 2,        // Terminal emoji width (1 or 2, try 1 if alignment is off)
};

// ============================================================================
// ICONS
// ============================================================================
const ICON = {
  user: '👤',
  folder: '📁',
  model: '🤖',
  cc: '🔷',
  repo: '🔗',
  stage: '📤',
  commit: '📦',
  push: '🚀',
  modified: '📝',
  new: '✨',
  deleted: '🗑️',
  renamed: '📎',
  conflict: '⚠️',
  stash: '📚',
  time: '🕐',
  lastCommit: '⏰',
};

// ============================================================================
// BOX DRAWING
// ============================================================================
const BOX = {
  tl: '┌', tr: '┐', bl: '└', br: '┘',
  h: '─', v: '│', sep: '│',
};

// ============================================================================
// ANSI COLORS
// ============================================================================
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[91m',
  green: '\x1b[92m',
  yellow: '\x1b[93m',
  blue: '\x1b[94m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
  white: '\x1b[97m',
  gray: '\x1b[90m',
};

function c(text, color) {
  return `${C[color] || ''}${text}${C.reset}`;
}

// ============================================================================
// UTILITIES
// ============================================================================
function getVisibleLength(str) {
  // Remove ANSI escape codes
  let s = str.replace(/\x1b\[[0-9;]*m/g, '');

  // Remove zero-width characters (variation selectors, joiners, etc.)
  s = s.replace(/[\u{FE00}-\u{FE0F}\u{200B}-\u{200D}\u{2060}\u{FEFF}]/gu, '');

  // Replace ALL emojis with configured width
  // Covers: Misc Symbols, Dingbats, Emoticons, Transport, Misc Symbols Extended, etc.
  const emojiReplace = CONFIG.emojiWidth === 1 ? ' ' : '  ';
  s = s.replace(/[\u{2000}-\u{2BFF}\u{1F000}-\u{1FFFF}]/gu, emojiReplace);

  return s.length;
}

function padRight(str, len) {
  const visible = getVisibleLength(str);
  return visible >= len ? str : str + ' '.repeat(len - visible);
}

function padLeft(str, len) {
  const visible = getVisibleLength(str);
  return visible >= len ? str : ' '.repeat(len - visible) + str;
}

function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 }).replace(/\n$/, '');
  } catch { return null; }
}

// ============================================================================
// PATH FORMATTING
// ============================================================================
function formatPath(fullPath) {
  if (CONFIG.pathSegments === 0) return '';
  const parts = fullPath.replace(/\\/g, '/').split('/').filter(Boolean);
  if (parts.length <= CONFIG.pathSegments) return parts.join('/');
  return parts.slice(-CONFIG.pathSegments).join('/');
}

// ============================================================================
// MODEL NAME PARSING
// ============================================================================
function formatModelName(modelData) {
  return modelData?.display_name || 'Unknown';
}

// ============================================================================
// CLAUDE CODE VERSION
// ============================================================================
function getClaudeCodeVersion() {
  const version = execCmd('claude --version');
  if (version) {
    const match = version.match(/(\d+\.\d+\.\d+)/);
    if (match) return match[1];
  }
  return null;
}

// ============================================================================
// PROJECT SIZE (Git tracked files only)
// ============================================================================
function formatBytes(bytes) {
  if (bytes >= 1073741824) {
    return (bytes / 1073741824).toFixed(1) + 'G';
  } else if (bytes >= 1048576) {
    return (bytes / 1048576).toFixed(1) + 'M';
  } else if (bytes >= 1024) {
    return (bytes / 1024).toFixed(0) + 'K';
  }
  return bytes + 'B';
}

function getProjectSize() {
  // Get list of files (tracked + untracked but not ignored)
  const tracked = execCmd('git ls-files');
  const untracked = execCmd('git ls-files --others --exclude-standard');

  if (!tracked && !untracked) return null;

  // Combine file lists
  const files = [];
  if (tracked) files.push(...tracked.split('\n').filter(f => f.trim()));
  if (untracked) files.push(...untracked.split('\n').filter(f => f.trim()));

  if (files.length === 0) return null;

  // Calculate total size using Node.js fs.statSync
  let totalBytes = 0;
  for (const file of files) {
    try {
      const stat = fs.statSync(file);
      if (stat.isFile()) {
        totalBytes += stat.size;
      }
    } catch {}
  }

  return totalBytes > 0 ? formatBytes(totalBytes) : null;
}

// ============================================================================
// GIT INFO
// ============================================================================
function getGitInfo() {
  const branch = execCmd('git rev-parse --abbrev-ref HEAD');
  if (!branch) return null;

  const statusOutput = execCmd('git status --porcelain') || '';
  let mod = 0, add = 0, del = 0, ren = 0;
  let sMod = 0, sAdd = 0, sDel = 0, sRen = 0;
  let conflict = 0, untracked = 0;

  for (const line of statusOutput.split('\n')) {
    if (!line || line.length < 2) continue;
    const idx = line.charAt(0);
    const wt = line.charAt(1);

    if (idx === 'U' || wt === 'U' || (idx === 'D' && wt === 'D') || (idx === 'A' && wt === 'A')) {
      conflict++; continue;
    }
    if (idx === '?' && wt === '?') { untracked++; continue; }

    // Working tree changes
    if (wt === 'M') mod++;
    if (wt === 'D') del++;

    // Staged changes
    if (idx === 'M') sMod++;
    if (idx === 'A') sAdd++;
    if (idx === 'D') sDel++;
    if (idx === 'R') sRen++;  // Rename as separate category
    if (idx === 'C') sAdd++;  // Copy as add
  }

  add = untracked;

  // Line counts
  let unstAdd = 0, unstRem = 0, stAdd = 0, stRem = 0;

  const unstaged = execCmd('git diff --numstat');
  if (unstaged) {
    for (const line of unstaged.split('\n')) {
      const p = line.split(/\s+/);
      if (p.length >= 2) {
        const a = parseInt(p[0], 10), r = parseInt(p[1], 10);
        if (!isNaN(a)) unstAdd += a;
        if (!isNaN(r)) unstRem += r;
      }
    }
  }

  // Untracked file lines (cross-platform using Node.js)
  if (untracked > 0 && untracked <= 100) {
    const untrackedFiles = execCmd('git ls-files --others --exclude-standard');
    if (untrackedFiles) {
      const files = untrackedFiles.split('\n').filter(f => f.trim()).slice(0, 100);
      for (const file of files) {
        try {
          const content = fs.readFileSync(file, 'utf-8');
          unstAdd += content.split('\n').length;
        } catch {}
      }
    }
  }

  const staged = execCmd('git diff --cached --numstat');
  if (staged) {
    for (const line of staged.split('\n')) {
      const p = line.split(/\s+/);
      if (p.length >= 2) {
        const a = parseInt(p[0], 10), r = parseInt(p[1], 10);
        if (!isNaN(a)) stAdd += a;
        if (!isNaN(r)) stRem += r;
      }
    }
  }

  // Unpushed
  let unpushed = 0;
  const tracking = execCmd('git rev-parse --abbrev-ref @{u}');
  if (tracking) {
    const cnt = execCmd('git rev-list --count @{u}..HEAD');
    unpushed = parseInt(cnt || '0', 10);
  }

  // Stash
  const stashList = execCmd('git stash list');
  const stash = stashList ? stashList.split('\n').filter(x => x.trim()).length : 0;

  // Repo name
  const gitRoot = execCmd('git rev-parse --show-toplevel');
  const repoName = gitRoot ? path.basename(gitRoot) : null;

  // Last commit time (Unix timestamp)
  const lastCommitTs = execCmd('git log -1 --format=%ct');
  const lastCommit = lastCommitTs ? parseInt(lastCommitTs, 10) : null;

  return {
    branch, repoName,
    mod, add, del, ren,
    sMod, sAdd, sDel, sRen,
    unstAdd, unstRem,
    stAdd, stRem,
    unpushed, conflict, stash,
    lastCommit
  };
}

// ============================================================================
// FORMAT STATUSLINE
// ============================================================================
function formatStatusline(input, git) {
  const termWidth = process.stdout.columns || 100;
  const username = os.userInfo().username || 'user';
  const host = os.hostname() || 'host';
  const userDisplay = CONFIG.showHostname ? `${username}@${host}` : username;

  const fullPath = input.cwd || process.cwd();
  const pathDisplay = formatPath(fullPath);
  const modelDisplay = formatModelName(input.model);
  const ccVersion = getClaudeCodeVersion();
  const projectSize = getProjectSize();

  // ─────────────────────────────────────────────────────────────────────────
  // BUILD 5-COLUMN GRID
  // ─────────────────────────────────────────────────────────────────────────
  // Row 1: Path | User | Size | CC | Model
  // Row 2: Repo:Branch | Conflicts | Stash | Ahead | Last
  // Row 3: Unstaged +/- | edit | new | del | move
  // Row 4: Staged +/- | edit | new | del | move

  const row1 = [
    `${ICON.folder} ${c(pathDisplay, 'white')}`,
    `${ICON.user} ${c(userDisplay, 'cyan')}`,
    projectSize ? c(projectSize, 'blue') : c('?', 'gray'),
    ccVersion ? c('CC ' + ccVersion, 'yellow') : c('CC ?', 'gray'),
    `${ICON.model} ${c(modelDisplay, 'magenta')}`
  ];

  let row2;
  if (git) {
    const repoText = git.repoName ? `${git.repoName}:${git.branch}` : git.branch;
    const issueColor = git.conflict > 0 ? 'red' : 'gray';
    const savedColor = git.stash > 0 ? 'cyan' : 'gray';
    const syncColor = git.unpushed > 0 ? 'magenta' : 'gray';

    // Format last commit time from Unix timestamp
    let lastCommitShort = 'never';
    if (git.lastCommit) {
      const nowSec = Math.floor(Date.now() / 1000);
      const diffSec = nowSec - git.lastCommit;
      const diffMin = Math.floor(diffSec / 60);
      const diffHour = Math.floor(diffSec / 3600);
      const diffDay = Math.floor(diffSec / 86400);

      if (diffDay >= 1) {
        // 1+ days: show "#d #h" format
        const hours = Math.floor((diffSec % 86400) / 3600);
        lastCommitShort = hours > 0 ? `${diffDay}d ${hours}h` : `${diffDay}d`;
      } else {
        // Less than 1 day: show "hh:mm" format
        const hours = diffHour;
        const mins = diffMin % 60;
        lastCommitShort = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
      }
    }

    row2 = [
      `${ICON.repo} ${c(repoText, 'green')}`,
      `${c('Conflicts:', issueColor)} ${c(String(git.conflict), issueColor)}`,
      `${c('Stash:', savedColor)} ${c(String(git.stash), savedColor)}`,
      `${c('Ahead:', syncColor)} ${c(String(git.unpushed), syncColor)}`,
      `${c('Last:', 'gray')} ${c(lastCommitShort, 'gray')}`
    ];
  } else {
    row2 = [
      c('Not a git repo', 'gray'),
      '',
      '',
      ''
    ];
  }

  // Build Unstaged/Staged rows
  let row3, row4;
  if (git) {
    const modStr = padLeft(String(git.mod), 2);
    const addStr = padLeft(String(git.add), 2);
    const delStr = padLeft(String(git.del), 2);
    const renStr = padLeft(String(git.ren), 2);
    const unstAddStr = padLeft(String(git.unstAdd), 4);
    const unstRemStr = padLeft(String(git.unstRem), 4);

    const sModStr = padLeft(String(git.sMod), 2);
    const sAddStr = padLeft(String(git.sAdd), 2);
    const sDelStr = padLeft(String(git.sDel), 2);
    const sRenStr = padLeft(String(git.sRen), 2);
    const stAddStr = padLeft(String(git.stAdd), 4);
    const stRemStr = padLeft(String(git.stRem), 4);

    // Row 3: Unstaged changes (working tree)
    row3 = [
      `${c('Unstaged', 'white')} ${c('+' + unstAddStr, 'green')} ${c('-' + unstRemStr, 'red')}`,
      `${c('edit', 'gray')} ${c(modStr, 'yellow')}`,
      `${c('new', 'gray')} ${c(addStr, 'green')}`,
      `${c('del', 'gray')} ${c(delStr, 'red')}`,
      `${c('move', 'gray')} ${c(renStr, 'cyan')}`
    ];

    // Row 4: Staged changes (index, ready to commit)
    row4 = [
      `${c('Staged', 'white')}   ${c('+' + stAddStr, 'green')} ${c('-' + stRemStr, 'red')}`,
      `${c('edit', 'gray')} ${c(sModStr, 'yellow')}`,
      `${c('new', 'gray')} ${c(sAddStr, 'green')}`,
      `${c('del', 'gray')} ${c(sDelStr, 'red')}`,
      `${c('move', 'gray')} ${c(sRenStr, 'cyan')}`
    ];
  }

  // Calculate column widths from ALL rows
  const colWidths = [];
  const allRows = [row1, row2, row3, row4].filter(Boolean);
  for (let i = 0; i < 5; i++) {
    let maxWidth = 0;
    for (const row of allRows) {
      if (row[i]) {
        maxWidth = Math.max(maxWidth, getVisibleLength(row[i]));
      }
    }
    colWidths[i] = maxWidth + 1;
  }

  // ─────────────────────────────────────────────────────────────────────────
  // BUILD LINES
  // ─────────────────────────────────────────────────────────────────────────
  const lines = [];

  // Helper to build a row with columns
  function buildRow(cells, leftChar, sepChar, rightChar) {
    let result = c(leftChar, 'gray');
    for (let i = 0; i < cells.length; i++) {
      const content = cells[i];
      const pad = colWidths[i] - getVisibleLength(content);
      result += ` ${content}${' '.repeat(pad)}`;
      if (i < cells.length - 1) {
        result += c(sepChar, 'gray');
      }
    }
    result += c(rightChar, 'gray');
    return result;
  }

  // Helper to build a separator line
  function buildSep(leftChar, midChar, rightChar, fillChar) {
    let result = c(leftChar, 'gray');
    for (let i = 0; i < colWidths.length; i++) {
      result += c(fillChar.repeat(colWidths[i] + 1), 'gray');
      if (i < colWidths.length - 1) {
        result += c(midChar, 'gray');
      }
    }
    result += c(rightChar, 'gray');
    return result;
  }

  // Title row (same structure as buildRow, but with space/| instead of │)
  lines.push(buildRow(row1, ' ', c('|', 'gray'), ' '));

  // Top border of table
  lines.push(buildSep('┌', '┬', '┐', '─'));

  // Row 2 (git info)
  lines.push(buildRow(row2, '│', '│', '│'));

  if (git) {
    // Middle separator (4 columns)
    lines.push(buildSep('├', '┼', '┤', '─'));

    // Unstaged row (working tree changes)
    lines.push(buildRow(row3, '│', '│', '│'));

    // Staged row (index changes)
    lines.push(buildRow(row4, '│', '│', '│'));

    // Bottom border (4 columns)
    lines.push(buildSep('└', '┴', '┘', '─'));
  } else {
    // Bottom border (with columns)
    lines.push(buildSep('└', '┴', '┘', '─'));
  }

  return lines.join('\n');
}

// ============================================================================
// MAIN
// ============================================================================
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  const git = getGitInfo();
  console.log(formatStatusline(input, git));
} catch (error) {
  console.log(`[Statusline Error: ${error.message}]`);
}
```

Cross-platform command for settings.json:
```json
"statusLine": {
  "type": "command",
  "command": "node -e \"const p=require('path'),o=require('os'),{spawnSync:s}=require('child_process'),r=s('node',[p.join(o.homedir(),'.claude','statusline.js')],{stdio:['inherit','inherit','inherit']});process.exit(r.status||0)\""
}
```

## Permissions

Target: `{scope}/settings.json`

### Agent Compatibility

| Level | detect | scan | action | Use Case |
|-------|--------|------|--------|----------|
| Safe | ✓ | ✗ | ✗ | Maximum security, manual approval |
| Balanced | ✓ | ✓ | ✓ | Normal workflow (recommended) |
| Permissive | ✓ | ✓ | ✓ | Minimal prompts, trusted projects |

**Agent tool requirements:**
- `cco-agent-detect`: Read, Glob, Grep (all read-only)
- `cco-agent-scan`: + Bash (read-only: ruff check, pytest --collect-only, git log)
- `cco-agent-action`: + Edit, Write, NotebookEdit, Bash (format, lint, test runners)

### Always Allow (all levels)

These safe tools are always in allow list:
```
Read, Glob, Grep, WebSearch, WebFetch, Task, TodoWrite,
SlashCommand, Skill, AskUserQuestion
```

**Safe:** Maximum security
```
allow: [always allow]
ask: Write, Edit, NotebookEdit, all Bash
deny: dangerous commands
```
⚠️ Every file change and command needs approval.

**Balanced (default):** Normal workflow
```
allow: [always allow] + Write, Edit, NotebookEdit
       Bash: git, ruff, pytest, npm test, cargo check, etc.
ask: rm/del, pip install, npm install, git push
deny: dangerous commands
```
✓ Code changes auto, destructive/install commands ask.

**Permissive:** Trusted projects
```
allow: [always allow] + Write, Edit, NotebookEdit
       Bash: everything except push and system
ask: git push, npm publish, sudo, system commands
deny: dangerous commands
```
✓ Even rm/install auto, only publish/push asks.

### Difference Table

| Action | Safe | Balanced | Permissive |
|--------|------|----------|------------|
| Edit/Write files | ask | allow | allow |
| git status/diff/log | ask | allow | allow |
| ruff/pytest/npm test | ask | allow | allow |
| rm file, del file | ask | **ask** | allow |
| pip/npm install | ask | **ask** | allow |
| git push | ask | ask | **ask** |
| npm publish | ask | ask | **ask** |
| rm -rf, format, dd | **deny** | **deny** | **deny** |
| sudo, su, chmod 777 | **deny** | **deny** | **deny** |
| curl\|bash, eval | **deny** | **deny** | **deny** |
| .env, secrets, keys | **deny** | **deny** | **deny** |

### Always Deny (all levels)

These dangerous patterns are always in deny list regardless of permission level:

**Destructive Commands:**
```
Bash(rm -rf /*:*)        # Root deletion
Bash(rm -rf ~/*:*)       # Home deletion
Bash(rm -rf .:*)         # Current dir recursive
Bash(del /s /q:*)        # Windows recursive delete
Bash(format:*)           # Disk format
Bash(mkfs:*)             # Filesystem format
Bash(dd if=:*)           # Raw disk write
```

**System/Privilege:**
```
Bash(sudo:*)             # Privilege escalation
Bash(su:*)               # Switch user
Bash(chmod 777:*)        # World writable
Bash(chown root:*)       # Change to root
Bash(shutdown:*)         # System shutdown
Bash(reboot:*)           # System reboot
Bash(halt:*)             # System halt
```

**Git Dangerous:**
```
Bash(git push --force:*)      # Force push
Bash(git push -f:*)           # Force push short
Bash(git reset --hard:*)      # Hard reset
Bash(git clean -fdx:*)        # Clean all untracked
Bash(git rebase -i:*)         # Interactive rebase
```

**Remote Code Execution:**
```
Bash(curl*|*sh:*)        # Pipe to shell
Bash(curl*|*bash:*)      # Pipe to bash
Bash(wget*|*sh:*)        # Wget pipe to shell
Bash(eval:*)             # Eval command
```

**Sensitive Files:**
```
Edit(**/.env)            # Environment files
Edit(**/.env.*)          # Environment variants
Edit(**/secrets/**)      # Secrets directory
Edit(**/*.pem)           # Private keys
Edit(**/*.key)           # Key files
Edit(**/*secret*)        # Secret files
Write(**/.env)           # Write env
Write(**/.env.*)         # Write env variants
Write(**/secrets/**)     # Write secrets
Read(**/.ssh/id_*)       # SSH private keys
Read(**/.aws/credentials)# AWS credentials
Read(**/.kube/config)    # Kubernetes config
Read(**/*password*)      # Password files
```

**Combined deny array:**
```json
"deny": [
  "Bash(rm -rf /*:*)", "Bash(rm -rf ~/*:*)", "Bash(rm -rf .:*)",
  "Bash(del /s /q:*)", "Bash(format:*)", "Bash(mkfs:*)", "Bash(dd if=:*)",
  "Bash(sudo:*)", "Bash(su:*)", "Bash(chmod 777:*)", "Bash(chown root:*)",
  "Bash(shutdown:*)", "Bash(reboot:*)", "Bash(halt:*)",
  "Bash(git push --force:*)", "Bash(git push -f:*)",
  "Bash(git reset --hard:*)", "Bash(git clean -fdx:*)",
  "Bash(curl*|*sh:*)", "Bash(curl*|*bash:*)", "Bash(wget*|*sh:*)", "Bash(eval:*)",
  "Edit(**/.env)", "Edit(**/.env.*)", "Edit(**/secrets/**)", "Edit(**/*.pem)",
  "Edit(**/*.key)", "Edit(**/*secret*)",
  "Write(**/.env)", "Write(**/.env.*)", "Write(**/secrets/**)",
  "Read(**/.ssh/id_*)", "Read(**/.aws/credentials)", "Read(**/.kube/config)"
]
```

## Validation

Before writing:
1. **JSON Syntax** - Must be parseable
2. **Conflicts** - Same pattern cannot be in allow AND deny
3. **Security** - Dangerous commands must be in deny

On failure: show issues, offer auto-fix for safe issues

## Usage

```bash
/cco-config                    # Interactive
/cco-config --global           # Global scope
/cco-config --local            # Local scope
/cco-config --statusline       # Statusline only
/cco-config --permissions      # Permissions only
```

## Rules

1. NEVER modify non-CCO settings in settings.json
2. ALWAYS preserve existing structure
3. ALWAYS include dangerous command denials
4. Backup before replacement
5. Local overrides Global for that project
