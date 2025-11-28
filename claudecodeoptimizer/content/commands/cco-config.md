---
name: cco-config
description: Configure statusline and permissions
---

# /cco-config

**Configuration** - Detect existing → show details → remove/update/add.

## Decision Tree

```
User runs /cco-config
  │
  ├─► Pre-check: Glob + Read (NO agent)
  │
  ├─► AskUserQuestion: Scope + Features
  │     │
  │     ├─► Statusline only?
  │     │     └─► Write + Edit (NO agent, NO tech stack)
  │     │
  │     └─► Permissions included?
  │           │
  │           ├─► AskUserQuestion: Permission level
  │           │     │
  │           │     ├─► Safe or Permissive?
  │           │     │     └─► Edit with predefined lists (NO agent)
  │           │     │
  │           │     └─► Balanced?
  │           │           └─► cco-agent-detect (tech stack) → Edit
  │           │
  │           └─► Done
  │
  └─► Done
```

## Tool Selection

Use the **minimum tool** for each task:

| Task | Tool | Why |
|------|------|-----|
| Pre-check config exists | `Read` + `Glob` | Simple file checks |
| Write statusline.js | `Write` | Single file, fixed content |
| Update settings.json | `Read` then `Edit` | Preserve existing settings |
| Tech stack detection | `cco-agent-detect` | Only for Balanced permissions |

**Do NOT use agents for:**
- Statusline (fixed content, no analysis needed)
- Safe/Permissive permissions (no stack detection needed)

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

1. **Detect** - Read + Glob to check config files (no agent needed)
2. **Action** - If exists: AskUserQuestion → Remove / Update / Add
3. **Remove** - Show details, select items, delete, EXIT
4. **Configure** - Scope + Features (then Permission level only if Permissions selected)
5. **Execute** - Direct Write/Edit for statusline; agent only for Balanced permissions
6. **Validate** - JSON syntax, conflicts, security rules

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

**Step 1:** AskUserQuestion with 2 questions:

**Scope:** Global (~/.claude/) | Local (./.claude/)

**Features (multiSelect):** All | Statusline | Permissions

**Step 2:** If Permissions selected, ask:

**Permission level:** Safe | Balanced | Permissive

**Step 3:** Execute based on selections:

```
Statusline selected?
  → Write({scope}/statusline.js)
  → Edit({scope}/settings.json) to add statusLine setting

Permissions selected?
  → If Balanced: cco-agent-detect for tech stack → build allow list
  → If Safe/Permissive: use predefined lists directly
  → Edit({scope}/settings.json) to add permissions
```

## Statusline

Target: `{scope}/statusline.js`

Features:
- 5-column grid with box drawing
- Row 1: Dir | User | Size | CC Version | Model
- Row 2: Branch | Conflicts | Stash | Ahead | Last
- Row 3-4: Unstaged/Staged changes with line counts
- Configurable: showHostname, emojiWidth

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

  // Last commit time (Unix timestamp)
  const lastCommitTs = execCmd('git log -1 --format=%ct');
  const lastCommit = lastCommitTs ? parseInt(lastCommitTs, 10) : null;

  return {
    branch,
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
  const dirName = path.basename(fullPath);
  const modelDisplay = formatModelName(input.model);
  const ccVersion = getClaudeCodeVersion();
  const projectSize = getProjectSize();

  // ─────────────────────────────────────────────────────────────────────────
  // BUILD 5-COLUMN GRID
  // ─────────────────────────────────────────────────────────────────────────
  // Row 1: Dir | User | Size | CC | Model
  // Row 2: Branch | Conflicts | Stash | Ahead | Last
  // Row 3: Unstaged +/- | edit | new | del | move
  // Row 4: Staged +/- | edit | new | del | move

  const row1 = [
    `${ICON.folder} ${c(dirName, 'white')}`,
    `${ICON.user} ${c(userDisplay, 'cyan')}`,
    projectSize ? c(projectSize, 'blue') : c('?', 'gray'),
    ccVersion ? c('CC ' + ccVersion, 'yellow') : c('CC ?', 'gray'),
    `${ICON.model} ${c(modelDisplay, 'magenta')}`
  ];

  let row2;
  if (git) {
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
      `${ICON.repo} ${c(git.branch, 'green')}`,
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

### Always Allow (all scopes, all levels)

These safe read-only tools are ALWAYS in allow list for BOTH global and local:
```
Read, Glob, Grep, WebSearch, WebFetch, Task, TodoWrite,
SlashCommand, Skill, AskUserQuestion
```

### Hybrid Permission Model

**Precedence:** deny > ask > allow

| Level | Model | Security | Flexibility |
|-------|-------|----------|-------------|
| Safe | Whitelist | High | Low |
| Balanced | Whitelist | High | Medium |
| Permissive | Blacklist | Medium | High |

### Command Lists

**Core commands (whitelist base):**
```javascript
const coreCommands = [
  // ═══════════════════════════════════════════════════════════════════════════
  // GIT - Version control operations
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git show:*)",
  "Bash(git branch:*)", "Bash(git remote:*)", "Bash(git fetch:*)", "Bash(git pull:*)",
  "Bash(git add:*)", "Bash(git commit:*)", "Bash(git stash:*)", "Bash(git checkout:*)",
  "Bash(git switch:*)", "Bash(git merge:*)", "Bash(git rebase:*)", "Bash(git cherry-pick:*)",
  "Bash(git tag:*)", "Bash(git rev-parse:*)", "Bash(git ls-files:*)", "Bash(git -C:*)",
  "Bash(git blame:*)", "Bash(git shortlog:*)", "Bash(git describe:*)", "Bash(git config:*)",
  "Bash(git rev-list:*)", "Bash(git ls-tree:*)", "Bash(git cat-file:*)", "Bash(git archive:*)",
  "Bash(git worktree:*)", "Bash(git bisect:*)", "Bash(git reflog:*)", "Bash(git notes:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // FILE SYSTEM - Directory navigation & file operations
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(ls:*)", "Bash(dir:*)", "Bash(pwd:*)", "Bash(cd:*)",
  "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)", "Bash(wc:*)",
  "Bash(find:*)", "Bash(which:*)", "Bash(where:*)", "Bash(type:*)", "Bash(echo:*)",
  "Bash(mkdir:*)", "Bash(cp:*)", "Bash(mv:*)", "Bash(touch:*)", "Bash(tree:*)",
  "Bash(ln:*)", "Bash(readlink:*)", "Bash(realpath:*)", "Bash(basename:*)", "Bash(dirname:*)",
  "Bash(pathchk:*)", "Bash(mktemp:*)", "Bash(stat:*)", "Bash(file:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // SEARCH & TEXT PROCESSING - Pattern matching & text manipulation
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(grep:*)", "Bash(rg:*)", "Bash(fd:*)", "Bash(diff:*)",
  "Bash(sort:*)", "Bash(uniq:*)", "Bash(cut:*)", "Bash(tr:*)",
  "Bash(jq:*)", "Bash(yq:*)", "Bash(sed:*)", "Bash(awk:*)",
  "Bash(xargs:*)", "Bash(tee:*)",
  "Bash(more:*)", "Bash(less:*)", "Bash(nl:*)", "Bash(rev:*)",
  "Bash(expand:*)", "Bash(unexpand:*)", "Bash(fold:*)", "Bash(fmt:*)",
  "Bash(pr:*)", "Bash(column:*)", "Bash(paste:*)", "Bash(join:*)",
  "Bash(comm:*)", "Bash(split:*)", "Bash(csplit:*)", "Bash(strings:*)",
  "Bash(colrm:*)", "Bash(look:*)", "Bash(tsort:*)", "Bash(ptx:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // HASH & CHECKSUM - File integrity verification
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(md5sum:*)", "Bash(sha1sum:*)", "Bash(sha256sum:*)", "Bash(sha512sum:*)",
  "Bash(shasum:*)", "Bash(md5:*)", "Bash(cksum:*)", "Bash(sum:*)",
  "Bash(b2sum:*)", "Bash(sha224sum:*)", "Bash(sha384sum:*)",
  "Bash(xxhsum:*)", "Bash(rhash:*)", "Bash(openssl dgst:*)",
  "Bash(certutil -hashfile:*)",  // Windows

  // ═══════════════════════════════════════════════════════════════════════════
  // ARCHIVE & COMPRESSION - File archiving & compression
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(tar:*)", "Bash(zip:*)", "Bash(unzip:*)", "Bash(zipinfo:*)",
  "Bash(gzip:*)", "Bash(gunzip:*)", "Bash(zcat:*)", "Bash(zless:*)", "Bash(zmore:*)",
  "Bash(bzip2:*)", "Bash(bunzip2:*)", "Bash(bzcat:*)",
  "Bash(xz:*)", "Bash(unxz:*)", "Bash(xzcat:*)", "Bash(lzma:*)", "Bash(unlzma:*)",
  "Bash(zstd:*)", "Bash(unzstd:*)", "Bash(zstdcat:*)",
  "Bash(lz4:*)", "Bash(unlz4:*)", "Bash(lz4cat:*)",
  "Bash(7z:*)", "Bash(7za:*)", "Bash(7zr:*)",
  "Bash(rar:*)", "Bash(unrar:*)",
  "Bash(cpio:*)", "Bash(ar:*)", "Bash(pax:*)",
  "Bash(compress:*)", "Bash(uncompress:*)",
  "Bash(Expand-Archive:*)", "Bash(Compress-Archive:*)",  // PowerShell

  // ═══════════════════════════════════════════════════════════════════════════
  // ENCODING & DECODING - Data encoding/decoding
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(base64:*)", "Bash(base32:*)", "Bash(basenc:*)",
  "Bash(xxd:*)", "Bash(od:*)", "Bash(hexdump:*)", "Bash(hd:*)",
  "Bash(uuencode:*)", "Bash(uudecode:*)",
  "Bash(iconv:*)", "Bash(dos2unix:*)", "Bash(unix2dos:*)",
  "Bash(recode:*)", "Bash(ascii:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // PROCESS & TIME CONTROL - Process management & timing
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(timeout:*)", "Bash(sleep:*)", "Bash(time:*)", "Bash(watch:*)",
  "Bash(wait:*)", "Bash(nohup:*)", "Bash(nice:*)", "Bash(ionice:*)",
  "Bash(ps:*)", "Bash(top:*)", "Bash(htop:*)", "Bash(pgrep:*)",
  "Bash(pidof:*)", "Bash(uptime:*)", "Bash(free:*)", "Bash(vmstat:*)",
  "Bash(lscpu:*)", "Bash(nproc:*)", "Bash(getconf:*)",
  "Bash(taskset:*)", "Bash(chrt:*)", "Bash(schedtool:*)",
  "Bash(Start-Sleep:*)",  // PowerShell

  // ═══════════════════════════════════════════════════════════════════════════
  // DISK & STORAGE INFO - Disk usage & storage information
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(du:*)", "Bash(df:*)", "Bash(lsblk:*)", "Bash(blkid:*)",
  "Bash(findmnt:*)", "Bash(mount:*)", "Bash(mountpoint:*)",
  "Bash(quota:*)", "Bash(ncdu:*)", "Bash(duf:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // NETWORK - Network utilities (read-only/safe)
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(ping:*)", "Bash(ping6:*)", "Bash(traceroute:*)", "Bash(tracepath:*)",
  "Bash(mtr:*)", "Bash(pathping:*)",  // Windows
  "Bash(curl:*)", "Bash(wget:*)", "Bash(http:*)", "Bash(httpie:*)",
  "Bash(nc:*)", "Bash(netcat:*)", "Bash(ncat:*)", "Bash(socat:*)",
  "Bash(nslookup:*)", "Bash(dig:*)", "Bash(host:*)", "Bash(whois:*)",
  "Bash(getent:*)", "Bash(resolvectl:*)",
  "Bash(ifconfig:*)", "Bash(ip:*)", "Bash(ipconfig:*)",  // Windows
  "Bash(netstat:*)", "Bash(ss:*)", "Bash(lsof:*)", "Bash(fuser:*)",
  "Bash(arp:*)", "Bash(route:*)", "Bash(iwconfig:*)", "Bash(iwlist:*)",
  "Bash(nmcli:*)", "Bash(networksetup:*)",  // macOS
  "Bash(Test-Connection:*)", "Bash(Test-NetConnection:*)",  // PowerShell

  // ═══════════════════════════════════════════════════════════════════════════
  // SYSTEM INFO - System information & diagnostics
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(env:*)", "Bash(printenv:*)", "Bash(export:*)", "Bash(set:*)",
  "Bash(date:*)", "Bash(cal:*)", "Bash(ncal:*)", "Bash(timedatectl:*)",
  "Bash(whoami:*)", "Bash(id:*)", "Bash(groups:*)", "Bash(users:*)", "Bash(who:*)", "Bash(w:*)",
  "Bash(hostname:*)", "Bash(hostnamectl:*)", "Bash(domainname:*)",
  "Bash(uname:*)", "Bash(arch:*)", "Bash(lsb_release:*)", "Bash(hostinfo:*)",  // macOS
  "Bash(sw_vers:*)", "Bash(system_profiler:*)",  // macOS
  "Bash(systeminfo:*)", "Bash(ver:*)",  // Windows
  "Bash(locale:*)", "Bash(localectl:*)", "Bash(getopt:*)",
  "Bash(dmesg:*)", "Bash(journalctl:*)", "Bash(sysctl:*)",
  "Bash(lshw:*)", "Bash(lspci:*)", "Bash(lsusb:*)", "Bash(lsmod:*)",
  "Bash(dmidecode:*)", "Bash(inxi:*)", "Bash(neofetch:*)", "Bash(screenfetch:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // MATH & CALCULATION - Numeric operations
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(bc:*)", "Bash(dc:*)", "Bash(expr:*)", "Bash(factor:*)",
  "Bash(seq:*)", "Bash(shuf:*)", "Bash(numfmt:*)",
  "Bash(yes:*)", "Bash(true:*)", "Bash(false:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // TERMINAL & DISPLAY - Terminal control & output
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(printf:*)", "Bash(tput:*)", "Bash(stty:*)", "Bash(reset:*)",
  "Bash(clear:*)", "Bash(cls:*)",  // Windows
  "Bash(tty:*)", "Bash(script:*)", "Bash(screen:*)", "Bash(tmux:*)",
  "Bash(tabs:*)", "Bash(infocmp:*)", "Bash(tic:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // FILE PERMISSIONS & ATTRIBUTES (read-only checks)
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(test:*)", "Bash([:*)",
  "Bash(getfacl:*)", "Bash(lsattr:*)",
  "Bash(namei:*)", "Bash(access:*)",
  "Bash(attrib:*)", "Bash(icacls:*)",  // Windows (read-only usage)

  // ═══════════════════════════════════════════════════════════════════════════
  // WINDOWS-SPECIFIC COMMANDS
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(findstr:*)", "Bash(fc:*)", "Bash(comp:*)", "Bash(path:*)",
  "Bash(tasklist:*)", "Bash(wmic:*)", "Bash(query:*)",
  "Bash(reg query:*)", "Bash(schtasks /query:*)",
  "Bash(Get-Content:*)", "Bash(Get-ChildItem:*)", "Bash(Get-Item:*)",
  "Bash(Get-Process:*)", "Bash(Get-Service:*)", "Bash(Get-Command:*)",
  "Bash(Get-Help:*)", "Bash(Get-Member:*)", "Bash(Get-Location:*)",
  "Bash(Get-Date:*)", "Bash(Get-Host:*)", "Bash(Get-Culture:*)",
  "Bash(Get-FileHash:*)", "Bash(Get-Acl:*)", "Bash(Get-ItemProperty:*)",
  "Bash(Select-String:*)", "Bash(Select-Object:*)", "Bash(Where-Object:*)",
  "Bash(Format-List:*)", "Bash(Format-Table:*)", "Bash(Out-String:*)",
  "Bash(Measure-Object:*)", "Bash(Compare-Object:*)", "Bash(Sort-Object:*)",
  "Bash(Group-Object:*)", "Bash(ConvertTo-Json:*)", "Bash(ConvertFrom-Json:*)",
  "Bash(Test-Path:*)", "Bash(Resolve-Path:*)", "Bash(Split-Path:*)", "Bash(Join-Path:*)",

  // ═══════════════════════════════════════════════════════════════════════════
  // CCO AGENTS - Claude Code Optimizer agent commands
  // ═══════════════════════════════════════════════════════════════════════════
  "Bash(cco-agent-action)", "Bash(cco cco-agent-action:*)"
];
```

**Stack-specific (added by cco-agent-detect for Balanced level ONLY):**

When to detect: `Permissions selected` AND `level == Balanced`
When NOT to detect: Statusline only, Safe, or Permissive

```javascript
const stackCommands = {
  // ═══════════════════════════════════════════════════════════════════════════
  // PYTHON - Python ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  python: [
    // Runtime & package managers
    "Bash(python:*)", "Bash(python3:*)", "Bash(pip:*)", "Bash(pip3:*)",
    "Bash(poetry:*)", "Bash(uv:*)", "Bash(pdm:*)", "Bash(pipenv:*)", "Bash(pipx:*)",
    "Bash(conda:*)", "Bash(mamba:*)", "Bash(pyenv:*)",
    // Testing
    "Bash(pytest:*)", "Bash(pytest-cov:*)", "Bash(coverage:*)", "Bash(tox:*)", "Bash(nox:*)",
    "Bash(hypothesis:*)", "Bash(ward:*)", "Bash(nose2:*)",
    // Linting & formatting
    "Bash(ruff:*)", "Bash(ruff check:*)", "Bash(ruff format:*)",
    "Bash(mypy:*)", "Bash(pyright:*)", "Bash(pyre:*)", "Bash(pytype:*)",
    "Bash(black:*)", "Bash(isort:*)", "Bash(autopep8:*)", "Bash(yapf:*)", "Bash(blue:*)",
    "Bash(flake8:*)", "Bash(pylint:*)", "Bash(pyflakes:*)", "Bash(pydocstyle:*)",
    // Security
    "Bash(bandit:*)", "Bash(safety:*)", "Bash(pip-audit:*)", "Bash(snyk:*)",
    // Documentation
    "Bash(sphinx:*)", "Bash(sphinx-build:*)", "Bash(mkdocs:*)", "Bash(pdoc:*)", "Bash(pydoc:*)",
    // Frameworks & servers
    "Bash(django-admin:*)", "Bash(flask:*)", "Bash(fastapi:*)", "Bash(streamlit:*)",
    "Bash(uvicorn:*)", "Bash(gunicorn:*)", "Bash(hypercorn:*)", "Bash(daphne:*)",
    // Task queues
    "Bash(celery:*)", "Bash(dramatiq:*)", "Bash(rq:*)", "Bash(huey:*)",
    // Data science / ML
    "Bash(ipython:*)", "Bash(jupyter:*)", "Bash(notebook:*)", "Bash(jupyterlab:*)",
    "Bash(papermill:*)", "Bash(nbconvert:*)", "Bash(nbstripout:*)",
    // Database tools
    "Bash(alembic:*)", "Bash(sqlalchemy:*)", "Bash(django:*)",
    // Build
    "Bash(build:*)", "Bash(twine:*)", "Bash(flit:*)", "Bash(hatch:*)", "Bash(setuptools:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // NODE.JS - JavaScript/TypeScript ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  node: [
    // Runtime & package managers
    "Bash(node:*)", "Bash(npm:*)", "Bash(npx:*)", "Bash(yarn:*)", "Bash(pnpm:*)", "Bash(bun:*)",
    "Bash(corepack:*)", "Bash(nvm:*)", "Bash(fnm:*)", "Bash(volta:*)", "Bash(n:*)",
    // Linting & formatting
    "Bash(eslint:*)", "Bash(prettier:*)", "Bash(biome:*)", "Bash(oxlint:*)",
    "Bash(standard:*)", "Bash(xo:*)", "Bash(dprint:*)",
    // TypeScript
    "Bash(tsc:*)", "Bash(tsconfig:*)", "Bash(tsx:*)", "Bash(ts-node:*)", "Bash(tsup:*)",
    // Testing
    "Bash(jest:*)", "Bash(vitest:*)", "Bash(mocha:*)", "Bash(ava:*)", "Bash(tap:*)",
    "Bash(playwright:*)", "Bash(cypress:*)", "Bash(puppeteer:*)", "Bash(nightwatch:*)",
    "Bash(nyc:*)", "Bash(c8:*)",  // coverage
    // Bundlers
    "Bash(webpack:*)", "Bash(vite:*)", "Bash(rollup:*)", "Bash(esbuild:*)", "Bash(swc:*)",
    "Bash(parcel:*)", "Bash(turbopack:*)", "Bash(rspack:*)", "Bash(tsup:*)",
    // Frameworks
    "Bash(next:*)", "Bash(nuxt:*)", "Bash(astro:*)", "Bash(remix:*)", "Bash(svelte:*)",
    "Bash(gatsby:*)", "Bash(angular:*)", "Bash(ng:*)", "Bash(vue:*)", "Bash(react-scripts:*)",
    "Bash(create-react-app:*)", "Bash(create-next-app:*)", "Bash(create-vite:*)",
    "Bash(nest:*)", "Bash(express:*)", "Bash(fastify:*)", "Bash(hono:*)",
    // Database / ORM
    "Bash(prisma:*)", "Bash(drizzle:*)", "Bash(typeorm:*)", "Bash(sequelize:*)",
    "Bash(knex:*)", "Bash(mongoose:*)", "Bash(mikro-orm:*)",
    // Dev tools
    "Bash(nodemon:*)", "Bash(pm2:*)", "Bash(concurrently:*)", "Bash(cross-env:*)",
    "Bash(npm-check:*)", "Bash(depcheck:*)", "Bash(madge:*)", "Bash(npm-run-all:*)",
    // Documentation
    "Bash(typedoc:*)", "Bash(jsdoc:*)", "Bash(storybook:*)", "Bash(docusaurus:*)",
    // Monorepo
    "Bash(lerna:*)", "Bash(nx:*)", "Bash(turbo:*)", "Bash(changesets:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // RUST - Rust ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  rust: [
    "Bash(cargo:*)", "Bash(rustc:*)", "Bash(rustup:*)",
    "Bash(rustfmt:*)", "Bash(clippy:*)", "Bash(cargo-clippy:*)",
    "Bash(cargo-fmt:*)", "Bash(cargo-test:*)", "Bash(cargo-build:*)", "Bash(cargo-run:*)",
    "Bash(cargo-check:*)", "Bash(cargo-doc:*)", "Bash(cargo-bench:*)",
    "Bash(cargo-audit:*)", "Bash(cargo-deny:*)", "Bash(cargo-outdated:*)",
    "Bash(cargo-watch:*)", "Bash(cargo-expand:*)", "Bash(cargo-tree:*)",
    "Bash(cargo-add:*)", "Bash(cargo-rm:*)", "Bash(cargo-update:*)",
    "Bash(cargo-nextest:*)", "Bash(cargo-llvm-cov:*)", "Bash(cargo-tarpaulin:*)",
    "Bash(miri:*)", "Bash(bacon:*)", "Bash(wasm-pack:*)", "Bash(trunk:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // GO - Go ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  go: [
    "Bash(go:*)", "Bash(gofmt:*)", "Bash(goimports:*)",
    "Bash(golint:*)", "Bash(golangci-lint:*)", "Bash(staticcheck:*)", "Bash(revive:*)",
    "Bash(go build:*)", "Bash(go test:*)", "Bash(go run:*)", "Bash(go mod:*)",
    "Bash(go vet:*)", "Bash(go doc:*)", "Bash(go generate:*)", "Bash(go get:*)",
    "Bash(go install:*)", "Bash(go work:*)", "Bash(go env:*)",
    "Bash(govulncheck:*)", "Bash(delve:*)", "Bash(dlv:*)",
    "Bash(air:*)", "Bash(swag:*)", "Bash(mockgen:*)", "Bash(wire:*)",
    "Bash(gotestsum:*)", "Bash(ginkgo:*)", "Bash(gomega:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // JAVA / JVM - Java ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  java: [
    "Bash(java:*)", "Bash(javac:*)", "Bash(jar:*)", "Bash(javadoc:*)", "Bash(jshell:*)",
    "Bash(mvn:*)", "Bash(mvnw:*)", "Bash(gradle:*)", "Bash(gradlew:*)",
    "Bash(ant:*)", "Bash(sbt:*)", "Bash(mill:*)",
    "Bash(checkstyle:*)", "Bash(pmd:*)", "Bash(spotbugs:*)", "Bash(findbugs:*)",
    "Bash(google-java-format:*)", "Bash(spotless:*)",
    "Bash(junit:*)", "Bash(testng:*)", "Bash(jacoco:*)", "Bash(pitest:*)",
    "Bash(jmeter:*)", "Bash(gatling:*)",
    "Bash(spring:*)", "Bash(spring-boot:*)", "Bash(quarkus:*)", "Bash(micronaut:*)",
    "Bash(jbang:*)", "Bash(sdkman:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // .NET - .NET ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  dotnet: [
    "Bash(dotnet:*)", "Bash(nuget:*)", "Bash(msbuild:*)",
    "Bash(dotnet build:*)", "Bash(dotnet test:*)", "Bash(dotnet run:*)",
    "Bash(dotnet publish:*)", "Bash(dotnet restore:*)", "Bash(dotnet clean:*)",
    "Bash(dotnet format:*)", "Bash(dotnet watch:*)", "Bash(dotnet ef:*)",
    "Bash(dotnet new:*)", "Bash(dotnet add:*)", "Bash(dotnet remove:*)",
    "Bash(dotnet tool:*)", "Bash(dotnet pack:*)", "Bash(dotnet sln:*)",
    "Bash(csharp:*)", "Bash(fsharp:*)", "Bash(fsharpc:*)",
    "Bash(xunit:*)", "Bash(nunit:*)", "Bash(coverlet:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // RUBY - Ruby ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  ruby: [
    "Bash(ruby:*)", "Bash(gem:*)", "Bash(bundle:*)", "Bash(bundler:*)",
    "Bash(rake:*)", "Bash(rails:*)", "Bash(rspec:*)", "Bash(minitest:*)",
    "Bash(rubocop:*)", "Bash(erb:*)", "Bash(irb:*)", "Bash(pry:*)",
    "Bash(yard:*)", "Bash(solargraph:*)", "Bash(sorbet:*)", "Bash(srb:*)",
    "Bash(rbenv:*)", "Bash(rvm:*)", "Bash(chruby:*)", "Bash(asdf:*)",
    "Bash(reek:*)", "Bash(brakeman:*)", "Bash(simplecov:*)",
    "Bash(foreman:*)", "Bash(puma:*)", "Bash(unicorn:*)", "Bash(passenger:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // PHP - PHP ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  php: [
    "Bash(php:*)", "Bash(composer:*)", "Bash(artisan:*)",
    "Bash(phpunit:*)", "Bash(pest:*)", "Bash(phpstan:*)", "Bash(psalm:*)",
    "Bash(php-cs-fixer:*)", "Bash(phpcs:*)", "Bash(phpcbf:*)", "Bash(pint:*)",
    "Bash(laravel:*)", "Bash(symfony:*)", "Bash(wp:*)", "Bash(wp-cli:*)",
    "Bash(phpmd:*)", "Bash(phploc:*)", "Bash(phpmetrics:*)",
    "Bash(pecl:*)", "Bash(pear:*)", "Bash(phive:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // SWIFT - Swift/Apple ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  swift: [
    "Bash(swift:*)", "Bash(swiftc:*)", "Bash(swift build:*)", "Bash(swift test:*)",
    "Bash(swift run:*)", "Bash(swift package:*)",
    "Bash(swiftlint:*)", "Bash(swiftformat:*)", "Bash(sourcery:*)",
    "Bash(xcodebuild:*)", "Bash(xcrun:*)", "Bash(simctl:*)", "Bash(xcpretty:*)",
    "Bash(fastlane:*)", "Bash(gym:*)", "Bash(scan:*)", "Bash(match:*)",
    "Bash(pod:*)", "Bash(carthage:*)", "Bash(mint:*)", "Bash(tuist:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // KOTLIN - Kotlin ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  kotlin: [
    "Bash(kotlin:*)", "Bash(kotlinc:*)", "Bash(kapt:*)",
    "Bash(ktlint:*)", "Bash(detekt:*)", "Bash(diktat:*)",
    "Bash(kscript:*)", "Bash(amper:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // SCALA - Scala ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  scala: [
    "Bash(scala:*)", "Bash(scalac:*)", "Bash(sbt:*)", "Bash(mill:*)",
    "Bash(scalafmt:*)", "Bash(scalafix:*)", "Bash(amm:*)", "Bash(bloop:*)",
    "Bash(metals:*)", "Bash(coursier:*)", "Bash(cs:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // ELIXIR - Elixir ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  elixir: [
    "Bash(elixir:*)", "Bash(mix:*)", "Bash(iex:*)", "Bash(erl:*)",
    "Bash(mix test:*)", "Bash(mix compile:*)", "Bash(mix deps:*)",
    "Bash(mix format:*)", "Bash(mix ecto:*)", "Bash(mix phx:*)",
    "Bash(credo:*)", "Bash(dialyzer:*)", "Bash(sobelow:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // HASKELL - Haskell ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  haskell: [
    "Bash(ghc:*)", "Bash(ghci:*)", "Bash(cabal:*)", "Bash(stack:*)",
    "Bash(hlint:*)", "Bash(ormolu:*)", "Bash(stylish-haskell:*)", "Bash(fourmolu:*)",
    "Bash(haddock:*)", "Bash(hpack:*)", "Bash(ghcup:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // CLOJURE - Clojure ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  clojure: [
    "Bash(clj:*)", "Bash(clojure:*)", "Bash(lein:*)", "Bash(boot:*)",
    "Bash(clj-kondo:*)", "Bash(cljfmt:*)", "Bash(zprint:*)",
    "Bash(babashka:*)", "Bash(bb:*)", "Bash(deps:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // C/C++ - C/C++ ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  cpp: [
    "Bash(gcc:*)", "Bash(g++:*)", "Bash(clang:*)", "Bash(clang++:*)",
    "Bash(make:*)", "Bash(cmake:*)", "Bash(ninja:*)", "Bash(meson:*)",
    "Bash(conan:*)", "Bash(vcpkg:*)", "Bash(pkg-config:*)",
    "Bash(clang-format:*)", "Bash(clang-tidy:*)", "Bash(cppcheck:*)",
    "Bash(valgrind:*)", "Bash(gdb:*)", "Bash(lldb:*)",
    "Bash(ctest:*)", "Bash(gtest:*)", "Bash(catch2:*)",
    "Bash(doxygen:*)", "Bash(bear:*)", "Bash(ccache:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // ZIG - Zig ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  zig: [
    "Bash(zig:*)", "Bash(zig build:*)", "Bash(zig test:*)", "Bash(zig run:*)",
    "Bash(zig fmt:*)", "Bash(zls:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // DOCKER - Container ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  docker: [
    "Bash(docker:*)", "Bash(docker-compose:*)", "Bash(docker compose:*)",
    "Bash(docker build:*)", "Bash(docker run:*)", "Bash(docker ps:*)",
    "Bash(docker images:*)", "Bash(docker logs:*)", "Bash(docker exec:*)",
    "Bash(docker inspect:*)", "Bash(docker network:*)", "Bash(docker volume:*)",
    "Bash(docker system:*)", "Bash(docker container:*)", "Bash(docker image:*)",
    "Bash(podman:*)", "Bash(podman-compose:*)", "Bash(buildah:*)", "Bash(skopeo:*)",
    "Bash(nerdctl:*)", "Bash(containerd:*)", "Bash(ctr:*)",
    "Bash(dive:*)", "Bash(hadolint:*)", "Bash(trivy:*)", "Bash(grype:*)", "Bash(syft:*)",
    "Bash(docker-slim:*)", "Bash(lazydocker:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // KUBERNETES - Kubernetes ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  kubernetes: [
    "Bash(kubectl:*)", "Bash(helm:*)", "Bash(k9s:*)", "Bash(kustomize:*)",
    "Bash(kubectl get:*)", "Bash(kubectl describe:*)", "Bash(kubectl logs:*)",
    "Bash(kubectl apply:*)", "Bash(kubectl delete:*)", "Bash(kubectl exec:*)",
    "Bash(kubectl port-forward:*)", "Bash(kubectl rollout:*)", "Bash(kubectl scale:*)",
    "Bash(kubectl config:*)", "Bash(kubectl auth:*)", "Bash(kubectl api-resources:*)",
    "Bash(minikube:*)", "Bash(kind:*)", "Bash(k3d:*)", "Bash(k3s:*)",
    "Bash(kubectx:*)", "Bash(kubens:*)", "Bash(stern:*)", "Bash(lens:*)",
    "Bash(kubeseal:*)", "Bash(argocd:*)", "Bash(flux:*)", "Bash(fluxctl:*)",
    "Bash(kubeconform:*)", "Bash(kubeval:*)", "Bash(polaris:*)", "Bash(kube-score:*)",
    "Bash(kube-linter:*)", "Bash(datree:*)", "Bash(pluto:*)",
    "Bash(velero:*)", "Bash(kops:*)", "Bash(eksctl:*)", "Bash(gke:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // TERRAFORM / IaC - Infrastructure as Code
  // ═══════════════════════════════════════════════════════════════════════════
  terraform: [
    "Bash(terraform:*)", "Bash(tofu:*)", "Bash(opentofu:*)",
    "Bash(terraform init:*)", "Bash(terraform plan:*)", "Bash(terraform apply:*)",
    "Bash(terraform destroy:*)", "Bash(terraform fmt:*)", "Bash(terraform validate:*)",
    "Bash(terraform output:*)", "Bash(terraform state:*)", "Bash(terraform import:*)",
    "Bash(terraform workspace:*)", "Bash(terraform graph:*)", "Bash(terraform providers:*)",
    "Bash(terragrunt:*)", "Bash(tflint:*)", "Bash(tfsec:*)", "Bash(checkov:*)",
    "Bash(terrascan:*)", "Bash(infracost:*)", "Bash(atlantis:*)", "Bash(terraform-docs:*)",
    "Bash(cdktf:*)", "Bash(tfenv:*)", "Bash(tfswitch:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // CLOUD - Cloud provider CLIs
  // ═══════════════════════════════════════════════════════════════════════════
  cloud: [
    // AWS
    "Bash(aws:*)", "Bash(aws-cli:*)", "Bash(sam:*)", "Bash(cdk:*)", "Bash(amplify:*)",
    "Bash(copilot:*)", "Bash(eb:*)", "Bash(ecs-cli:*)", "Bash(eksctl:*)",
    // GCP
    "Bash(gcloud:*)", "Bash(gsutil:*)", "Bash(bq:*)", "Bash(firebase:*)",
    // Azure
    "Bash(az:*)", "Bash(azd:*)", "Bash(func:*)",
    // Multi-cloud / Serverless
    "Bash(pulumi:*)", "Bash(serverless:*)", "Bash(sls:*)", "Bash(sst:*)",
    // PaaS
    "Bash(vercel:*)", "Bash(netlify:*)", "Bash(fly:*)", "Bash(flyctl:*)",
    "Bash(railway:*)", "Bash(render:*)", "Bash(heroku:*)", "Bash(dokku:*)",
    // DigitalOcean / Others
    "Bash(doctl:*)", "Bash(linode-cli:*)", "Bash(vultr-cli:*)",
    "Bash(hcloud:*)", "Bash(oci:*)", "Bash(ibmcloud:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // DATABASE - Database CLIs
  // ═══════════════════════════════════════════════════════════════════════════
  database: [
    // PostgreSQL
    "Bash(psql:*)", "Bash(pg_dump:*)", "Bash(pg_restore:*)", "Bash(pg_dumpall:*)",
    "Bash(createdb:*)", "Bash(dropdb:*)", "Bash(createuser:*)", "Bash(pgcli:*)",
    // MySQL/MariaDB
    "Bash(mysql:*)", "Bash(mysqldump:*)", "Bash(mysqlimport:*)", "Bash(mycli:*)",
    "Bash(mariadb:*)", "Bash(mariadb-dump:*)",
    // SQLite
    "Bash(sqlite3:*)", "Bash(litecli:*)",
    // Redis
    "Bash(redis-cli:*)", "Bash(redis-server:*)", "Bash(redis-benchmark:*)",
    // MongoDB
    "Bash(mongo:*)", "Bash(mongosh:*)", "Bash(mongodump:*)", "Bash(mongorestore:*)",
    "Bash(mongoexport:*)", "Bash(mongoimport:*)",
    // Cassandra
    "Bash(cqlsh:*)", "Bash(nodetool:*)",
    // SQL Server
    "Bash(sqlcmd:*)", "Bash(bcp:*)", "Bash(mssql-cli:*)",
    // Others
    "Bash(influx:*)", "Bash(clickhouse-client:*)", "Bash(cockroach:*)",
    "Bash(etcdctl:*)", "Bash(consul:*)", "Bash(vault:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // ANSIBLE - Ansible ecosystem
  // ═══════════════════════════════════════════════════════════════════════════
  ansible: [
    "Bash(ansible:*)", "Bash(ansible-playbook:*)", "Bash(ansible-galaxy:*)",
    "Bash(ansible-vault:*)", "Bash(ansible-inventory:*)", "Bash(ansible-lint:*)",
    "Bash(ansible-doc:*)", "Bash(ansible-config:*)", "Bash(ansible-pull:*)",
    "Bash(molecule:*)"
  ],

  // ═══════════════════════════════════════════════════════════════════════════
  // DATA / ML - Data science & machine learning
  // ═══════════════════════════════════════════════════════════════════════════
  data: [
    "Bash(dvc:*)", "Bash(mlflow:*)", "Bash(wandb:*)", "Bash(neptune:*)",
    "Bash(kedro:*)", "Bash(dagster:*)", "Bash(prefect:*)", "Bash(airflow:*)",
    "Bash(dbt:*)", "Bash(great_expectations:*)", "Bash(pandera:*)",
    "Bash(spark-submit:*)", "Bash(pyspark:*)", "Bash(databricks:*)",
    "Bash(ray:*)", "Bash(dask:*)", "Bash(vaex:*)"
  ]
};
```

### Permission Levels

**Safe (whitelist, ask everything):**
```json
{
  "allow": [
    "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Task", "TodoWrite",
    "SlashCommand", "Skill", "AskUserQuestion"
  ],
  "ask": ["Edit", "Write", "NotebookEdit", "Bash"],
  "deny": [/* see Always Deny */]
}
```

**Balanced (whitelist, core + stack):**
```javascript
{
  "allow": [
    "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Task", "TodoWrite",
    "SlashCommand", "Skill", "AskUserQuestion",
    "Edit(./**)", "Write(./**)", "NotebookEdit(./**)",
    "Edit(~/.claude/**)", "Write(~/.claude/**)", "Read(~/.claude/**)",
    ...coreCommands,
    ...stackCommands[detected]  // Added by cco-agent-detect
  ],
  "ask": [
    "Bash(rm:*)", "Bash(rmdir:*)", "Bash(del:*)",
    "Bash(pip install:*)", "Bash(npm install:*)", "Bash(yarn add:*)",
    "Bash(git push:*)"
  ],
  "deny": [/* see Always Deny */]
}
```

**Permissive (blacklist, allow all):**
```json
{
  "allow": [
    "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Task", "TodoWrite",
    "SlashCommand", "Skill", "AskUserQuestion",
    "Edit(./**)", "Write(./**)", "NotebookEdit(./**)",
    "Edit(~/.claude/**)", "Write(~/.claude/**)", "Read(~/.claude/**)",
    "Bash"
  ],
  "ask": ["Bash(git push:*)", "Bash(npm publish:*)", "Bash(docker push:*)"],
  "deny": [/* see Always Deny - CRITICAL for this level */]
}
```

### Security Comparison

| Aspect | Safe | Balanced | Permissive |
|--------|------|----------|------------|
| Unknown cmd | Blocked | Blocked | Allowed |
| New threat | Safe | Safe | Risk |
| Flexibility | Low | Medium | High |

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
| curl/wget \| shell | **deny** | **deny** | **deny** |
| .env, secrets, keys | **deny** | **deny** | **deny** |

### OS Detection

Detect OS at runtime and apply platform-specific patterns:

```javascript
const isWindows = process.platform === 'win32';
const isMac = process.platform === 'darwin';
const isLinux = process.platform === 'linux';
```

### Critical Path Protection (all scopes, all levels)

These paths are ALWAYS denied regardless of scope or permission level:

**Cross-Platform (credentials & secrets):**
```
Edit(~/.ssh/**)          # SSH keys
Edit(~/.gnupg/**)        # GPG keys
Edit(~/.aws/**)          # AWS credentials
Edit(~/.kube/**)         # Kubernetes config
Edit(~/.docker/**)       # Docker credentials
Edit(**/.env*)           # Environment files
Edit(**/secrets/**)      # Secrets directories
Edit(**/*.pem)           # Private keys
Edit(**/*.key)           # Key files
```

**Unix/Linux/Mac only:**
```
Edit(/etc/**)            # System config
Edit(/usr/**)            # System binaries
Edit(/var/**)            # System data
Edit(/root/**)           # Root home
Edit(/boot/**)           # Boot files
```

**Windows only:**
```
Edit(C:/Windows/**)      # Windows system
Edit(C:/Program Files/**) # Program files
Edit(C:/Program Files (x86)/**) # Program files x86
Edit(C:/ProgramData/**)  # Program data
Edit(C:/Users/*/AppData/Local/Microsoft/**) # Windows settings
```

**Mac only (additional):**
```
Edit(/System/**)         # macOS system
Edit(/Library/**)        # System library
Edit(~/Library/Keychains/**) # Keychain
```

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
Bash(eval:*)                       # Eval command
```

**Note:** Pipe patterns (e.g., `curl | sh`) are NOT supported by Claude Code.
Use more specific command patterns or rely on other security measures.

**Sensitive Files:**
```
Edit(**/.env*)           # Environment files (.env, .env.local, etc.)
Edit(**/secrets/**)      # Secrets directory
Edit(**/*.pem)           # Private keys
Edit(**/*.key)           # Key files
Edit(**/*secret*)        # Secret files
Write(**/.env*)          # Write env files
Write(**/secrets/**)     # Write secrets
Read(**/.ssh/id_*)       # SSH private keys
Read(**/.aws/credentials)# AWS credentials
Read(**/.kube/config)    # Kubernetes config
Read(**/*password*)      # Password files
```

**Combined deny array (build dynamically):**

```javascript
// Base deny (all platforms)
const baseDeny = [
  // Destructive commands
  "Bash(rm -rf /*:*)", "Bash(rm -rf ~/*:*)", "Bash(rm -rf .:*)",
  "Bash(del /s /q:*)", "Bash(format:*)", "Bash(mkfs:*)", "Bash(dd if=:*)",
  // System/Privilege
  "Bash(sudo:*)", "Bash(su:*)", "Bash(chmod 777:*)", "Bash(chown root:*)",
  "Bash(shutdown:*)", "Bash(reboot:*)", "Bash(halt:*)",
  // Git dangerous
  "Bash(git push --force:*)", "Bash(git push -f:*)",
  "Bash(git reset --hard:*)", "Bash(git clean -fdx:*)",
  // Remote code execution
  "Bash(eval:*)",
  // Credentials (cross-platform)
  "Edit(~/.ssh/**)", "Write(~/.ssh/**)",
  "Edit(~/.gnupg/**)", "Write(~/.gnupg/**)",
  "Edit(~/.aws/**)", "Write(~/.aws/**)",
  "Edit(~/.kube/**)", "Write(~/.kube/**)",
  "Edit(~/.docker/**)", "Write(~/.docker/**)",
  // Sensitive files
  "Edit(**/.env*)", "Edit(**/secrets/**)", "Edit(**/*.pem)", "Edit(**/*.key)",
  "Write(**/.env*)", "Write(**/secrets/**)",
  "Read(**/.ssh/id_*)", "Read(**/.aws/credentials)", "Read(**/.kube/config)"
];

// Unix/Linux/Mac additions
const unixDeny = [
  "Edit(/etc/**)", "Write(/etc/**)",
  "Edit(/usr/**)", "Write(/usr/**)",
  "Edit(/var/**)", "Write(/var/**)",
  "Edit(/root/**)", "Write(/root/**)",
  "Edit(/boot/**)", "Write(/boot/**)"
];

// Windows additions
const windowsDeny = [
  "Edit(C:/Windows/**)", "Write(C:/Windows/**)",
  "Edit(C:/Program Files/**)", "Write(C:/Program Files/**)",
  "Edit(C:/Program Files (x86)/**)", "Write(C:/Program Files (x86)/**)",
  "Edit(C:/ProgramData/**)", "Write(C:/ProgramData/**)"
];

// Mac additions
const macDeny = [
  "Edit(/System/**)", "Write(/System/**)",
  "Edit(/Library/**)", "Write(/Library/**)",
  "Edit(~/Library/Keychains/**)", "Write(~/Library/Keychains/**)"
];

// Build final deny array
const deny = [
  ...baseDeny,
  ...(isWindows ? windowsDeny : unixDeny),
  ...(isMac ? macDeny : [])
];
```

## Settings Syntax Rules

Claude Code permission patterns follow specific syntax. Invalid patterns cause startup errors.

### Pattern Format

| Tool Type | Syntax | Example | Matches |
|-----------|--------|---------|---------|
| Bash prefix | `Bash(cmd:*)` | `Bash(git:*)` | `git status`, `git push`, etc. |
| Bash with args | `Bash(cmd arg:*)` | `Bash(npm run:*)` | `npm run dev`, `npm run build` |
| File glob | `Tool(**/pattern)` | `Edit(**/.env)` | Any `.env` file in tree |
| File glob ext | `Tool(**/*.ext)` | `Read(**/*.pem)` | Any `.pem` file |

### Syntax Rules

1. **Prefix Matching** - Use `:*` suffix for prefix matching
   - ✅ `Bash(git:*)` - matches any git command
   - ❌ `Bash(git*)` - INVALID, causes error

2. **Pipe Patterns** - NOT SUPPORTED
   - ❌ `Bash(curl:* | sh)` - INVALID, pipe patterns don't work
   - ❌ `Bash(curl:* | sh|bash|zsh)` - INVALID, pipe patterns don't work
   - Use more specific command patterns or rely on other security measures

3. **File Globs** - Use `**/` for recursive matching
   - ✅ `Edit(**/.env)` - any .env file
   - ✅ `Edit(**/*.key)` - any .key file
   - ❌ `Edit(.env)` - only root .env

4. **No Duplicates** - Avoid patterns that are subsets of each other
   - If `Bash(curl:*)` exists, don't add `Bash(curl -s:*)`
   - More generic pattern covers all specific cases

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Use ":*" for prefix matching` | Using `*` instead of `:*` | Change `Bash(git*)` → `Bash(git:*)` |
| `Invalid pattern syntax` | Wildcards in middle | Use prefix or pipe patterns |
| `Conflicting patterns` | Same pattern in allow+deny | Remove from one list |

## Validation

Before writing:
1. **JSON Syntax** - Must be parseable
2. **Pattern Syntax** - Must follow Claude Code pattern rules (see above)
3. **Conflicts** - Same pattern cannot be in allow AND deny
4. **Security** - Dangerous commands must be in deny

On failure: show issues, offer auto-fix for safe issues

## Health Check

After writing settings, validate with Claude Code:

```bash
# Test if settings file is valid
claude --version 2>&1

# If error contains "Invalid Settings", parse and fix:
# - Check pattern syntax rules above
# - Look for ":*" vs "*" issues
# - Check pipe pattern format
```

**Validation steps:**
1. Write settings.json
2. Run `claude --version` to trigger validation
3. If "Invalid Settings" error appears:
   - Parse error message for specific patterns
   - Apply syntax fixes from rules above
   - Re-write and re-validate
4. Repeat until no errors

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
