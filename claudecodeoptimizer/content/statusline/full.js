#!/usr/bin/env node

// Claude Code Statusline - Compact & Alert-Focused
// 2-column header, dynamic sync alerts, conditional staged row

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// ============================================================================
// CONFIGURATION
// ============================================================================
const CONFIG = {
  emojiWidth: 2, // Terminal emoji width (1 or 2, try 1 if alignment is off)
};

// ============================================================================
// ICONS
// ============================================================================
const ICON = {
  folder: '📁',  // U+1F4C1 - wide (2 cells)
  repo: '🔗',    // U+1F517 - wide (2 cells)
  user: '👤',    // U+1F464 - wide (2 cells)
  model: '🤖',   // U+1F916 - wide (2 cells)
  synced: '✓',   // U+2713 - narrow (1 cell)
  unpushed: '↑', // U+2191 - narrow (1 cell)
  conflict: '⚠', // U+26A0 - narrow (1 cell)
  stash: '📦',   // U+1F4E6 - wide (2 cells) - changed from 📚 for consistency
};

// ============================================================================
// BOX DRAWING
// ============================================================================
const BOX = {
  tl: '┌', tr: '┐', bl: '└', br: '┘',
  h: '─', v: '│',
  ml: '├', mr: '┤', mt: '┬', mb: '┴', mc: '┼',
};

// ============================================================================
// ANSI COLORS
// ============================================================================
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  // Foreground
  gray: '\x1b[90m',
  red: '\x1b[91m',
  green: '\x1b[92m',
  yellow: '\x1b[93m',
  blue: '\x1b[94m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
  white: '\x1b[97m',
  // Bold variants
  redBold: '\x1b[1;91m',
  whiteBold: '\x1b[1;97m',
};

function c(text, ...styles) {
  const styleStr = styles.map(s => C[s] || '').join('');
  return `${styleStr}${text}${C.reset}`;
}

// ============================================================================
// UTILITIES
// ============================================================================
function getVisibleLength(str) {
  // Remove ANSI escape codes
  let s = str.replace(/\x1b\[[0-9;]*m/g, '');
  // Remove zero-width characters
  s = s.replace(/[\u{FE00}-\u{FE0F}\u{200B}-\u{200D}\u{2060}\u{FEFF}]/gu, '');

  // Wide characters: Full-width emoji pictographs (typically 2 cells in terminal)
  // Range: U+1F300 to U+1FAFF (Miscellaneous Symbols and Pictographs, Emoticons, etc.)
  const wideEmoji = /[\u{1F300}-\u{1F9FF}\u{1FA00}-\u{1FAFF}]/gu;
  s = s.replace(wideEmoji, '  ');

  // Narrow symbols (1 cell): Specific symbols that need width tracking
  // Note: Box drawing (U+2500-U+257F) already counts as 1, don't replace
  // Misc Technical (U+2300-U+23FF), Misc Symbols (U+2600-U+26FF),
  // Dingbats (U+2700-U+27BF), Arrows (U+2190-U+21FF, U+2B00-U+2BFF)
  // These are already width 1, so we just keep them as-is in the length calculation
  // The key insight: all non-wide characters are already width 1, no replacement needed

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

function padCenter(str, len) {
  const visible = getVisibleLength(str);
  if (visible >= len) return str;
  const total = len - visible;
  const left = Math.floor(total / 2);
  const right = total - left;
  return ' '.repeat(left) + str + ' '.repeat(right);
}

function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 }).replace(/\n$/, '');
  } catch { return null; }
}

// ============================================================================
// PROJECT SIZE
// ============================================================================
function formatBytes(bytes) {
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(1) + 'G';
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(1) + 'M';
  if (bytes >= 1024) return (bytes / 1024).toFixed(0) + 'K';
  return bytes + 'B';
}

function getProjectSize() {
  const tracked = execCmd('git ls-files');
  const untracked = execCmd('git ls-files --others --exclude-standard');
  if (!tracked && !untracked) return null;

  const files = [];
  if (tracked) files.push(...tracked.split('\n').filter(f => f.trim()));
  if (untracked) files.push(...untracked.split('\n').filter(f => f.trim()));
  if (files.length === 0) return null;

  let totalBytes = 0;
  for (const file of files) {
    try {
      const stat = fs.statSync(file);
      if (stat.isFile()) totalBytes += stat.size;
    } catch {}
  }
  return totalBytes > 0 ? formatBytes(totalBytes) : null;
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
// MODEL NAME
// ============================================================================
function formatModelName(modelData) {
  const name = modelData?.display_name || 'Unknown';
  // Shorten common prefixes
  return name.replace(/^Claude\s+/, '');
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
    if (idx === 'R') sRen++;
    if (idx === 'C') sAdd++;
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

  if (untracked > 0 && untracked <= 100) {
    const untrackedLines = execCmd('bash -c "git ls-files --others --exclude-standard | head -100 | xargs cat 2>/dev/null | wc -l"');
    if (untrackedLines) {
      const lines = parseInt(untrackedLines, 10);
      if (!isNaN(lines)) unstAdd += lines;
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

  // Unpushed commits
  let unpushed = 0;
  const tracking = execCmd('git rev-parse --abbrev-ref @{u}');
  if (tracking) {
    const cnt = execCmd('git rev-list --count @{u}..HEAD');
    unpushed = parseInt(cnt || '0', 10);
  }

  // Stash count
  const stashList = execCmd('git stash list');
  const stash = stashList ? stashList.split('\n').filter(x => x.trim()).length : 0;

  // Repo name
  const gitRoot = execCmd('git rev-parse --show-toplevel');
  const repoName = gitRoot ? path.basename(gitRoot) : null;

  // Last commit time
  const lastCommitTs = execCmd('git log -1 --format=%ct');
  const lastCommit = lastCommitTs ? parseInt(lastCommitTs, 10) : null;

  // Check if there are any staged changes
  const hasStaged = sMod > 0 || sAdd > 0 || sDel > 0 || sRen > 0 || stAdd > 0 || stRem > 0;

  return {
    branch, repoName,
    mod, add, del, ren,
    sMod, sAdd, sDel, sRen,
    unstAdd, unstRem,
    stAdd, stRem,
    unpushed, conflict, stash,
    lastCommit, hasStaged
  };
}

// ============================================================================
// FORMAT LAST COMMIT TIME
// ============================================================================
function formatLastCommit(timestamp) {
  if (!timestamp) return 'never';
  const nowSec = Math.floor(Date.now() / 1000);
  const diffSec = nowSec - timestamp;
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffSec / 3600);
  const diffDay = Math.floor(diffSec / 86400);

  if (diffDay >= 1) {
    const hours = Math.floor((diffSec % 86400) / 3600);
    return hours > 0 ? `${diffDay}d ${hours}h` : `${diffDay}d`;
  }
  const hours = diffHour;
  const mins = diffMin % 60;
  return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
}

// ============================================================================
// BUILD STATUSLINE
// ============================================================================
function formatStatusline(input, git) {
  const username = os.userInfo().username || 'user';
  const fullPath = input.cwd || process.cwd();
  const projectName = path.basename(fullPath);
  const modelDisplay = formatModelName(input.model);
  const ccVersion = getClaudeCodeVersion();
  const projectSize = getProjectSize();

  // Repo display
  const repoDisplay = git ? `${git.repoName || projectName}:${git.branch}` : 'Not a git repo';

  // ─────────────────────────────────────────────────────────────────────────
  // CALCULATE WIDTHS (dynamic based on content)
  // ─────────────────────────────────────────────────────────────────────────
  // Narrow columns for edit/new/del/rename
  const narrowColWidth = 8;
  const narrowTotalWidth = narrowColWidth * 4 + 3; // 4 cols + 3 separators

  // Check for alerts
  const hasAlerts = git && (git.unpushed > 0 || git.conflict > 0 || git.stash > 0);

  // Build ALL content with colors first, then measure
  // Row 1
  const pathContent = ` ${ICON.folder} ${c(projectName, 'whiteBold')} `;
  const repoContent = ` ${ICON.repo} ${c(repoDisplay, 'green')} `;

  // Row 2
  const sizeStr = projectSize ? c(projectSize, 'blue') : c('?', 'gray');
  const userContent = ` ${ICON.user} ${c(username, 'cyan')}  ${sizeStr} `;
  const ccStr = ccVersion ? c(`CC ${ccVersion}`, 'yellow') : c('CC ?', 'gray');
  const modelContent = ` ${ccStr}  ${ICON.model} ${c(modelDisplay, 'magenta')} `;

  // Row 3: Sync
  let syncContent;
  if (!git) {
    syncContent = ` ${c('Not a git repository', 'gray')} `;
  } else if (hasAlerts) {
    const alerts = [];
    if (git.unpushed > 0) alerts.push(`${ICON.unpushed}${git.unpushed} ${c('unpushed', 'yellow')}`);
    if (git.conflict > 0) alerts.push(`${ICON.conflict}${git.conflict} ${c('conflict', 'redBold')}`);
    if (git.stash > 0) alerts.push(`${ICON.stash}${git.stash} ${c('stash', 'blue')}`);
    syncContent = ` ${alerts.join('  ')} `;
  } else {
    syncContent = ` ${c(ICON.synced, 'green')} ${c('Synced with remote', 'green')} `;
  }

  // Row 4+: Unstaged/Staged
  function buildDataRow(label, addLines, remLines, edit, newFiles, delFiles, renameFiles) {
    const addStr = c('+' + addLines.toString().padStart(4), 'green');
    const remStr = c('-' + remLines.toString().padStart(4), 'red');
    const labelContent = ` ${c(label, 'white')}  ${addStr}  ${remStr} `;

    const editVal = edit > 0 ? c(edit.toString(), 'yellow') : c('0', 'gray');
    const newVal = newFiles > 0 ? c(newFiles.toString(), 'green') : c('0', 'gray');
    const delVal = delFiles > 0 ? c(delFiles.toString(), 'red') : c('0', 'gray');
    const renameVal = renameFiles > 0 ? c(renameFiles.toString(), 'cyan') : c('0', 'gray');

    return { labelContent, editVal, newVal, delVal, renameVal };
  }

  const unstaged = git ? buildDataRow('Unstaged', git.unstAdd, git.unstRem, git.mod, git.add, git.del, git.ren) : null;
  const staged = git?.hasStaged ? buildDataRow('Staged', git.stAdd, git.stRem, git.sMod, git.sAdd, git.sDel, git.sRen) : null;

  // Calculate widths from actual colored content
  const leftContents = [pathContent, userContent, syncContent];
  if (unstaged) leftContents.push(unstaged.labelContent);
  if (staged) leftContents.push(staged.labelContent);
  const bodyWideWidth = Math.max(...leftContents.map(s => getVisibleLength(s)));

  const rightContents = [repoContent, modelContent];
  const maxRightWidth = Math.max(...rightContents.map(s => getVisibleLength(s)));
  const headerRightWidth = Math.max(maxRightWidth, narrowTotalWidth);
  const headerLeftWidth = bodyWideWidth;

  // Column headers (centered)
  const editHeader = c('edit', 'yellow');
  const newHeader = c('new', 'green');
  const delHeader = c('del', 'red');
  const renameHeader = c('rename', 'cyan');

  // ─────────────────────────────────────────────────────────────────────────
  // RENDER LINES
  // ─────────────────────────────────────────────────────────────────────────
  const lines = [];

  // Helper: horizontal line with specific corner/junction chars
  function hLine(left, mid, right, width1, width2) {
    return c(left + BOX.h.repeat(width1) + mid + BOX.h.repeat(width2) + right, 'gray');
  }

  function hLine5(left, j1, j2, j3, j4, right, w1, w2, w3, w4, w5) {
    return c(
      left + BOX.h.repeat(w1) + j1 + BOX.h.repeat(w2) + j2 + BOX.h.repeat(w3) + j3 + BOX.h.repeat(w4) + j4 + BOX.h.repeat(w5) + right,
      'gray'
    );
  }

  // Row with 2 columns
  function row2(content1, content2, width1, width2) {
    return c(BOX.v, 'gray') + padRight(content1, width1) + c(BOX.v, 'gray') + padRight(content2, width2) + c(BOX.v, 'gray');
  }

  // Row with 5 columns (1 wide + 4 narrow, narrow cells centered)
  function row5(wideContent, c1, c2, c3, c4, wideWidth) {
    return (
      c(BOX.v, 'gray') + padRight(wideContent, wideWidth) +
      c(BOX.v, 'gray') + padCenter(c1, narrowColWidth) +
      c(BOX.v, 'gray') + padCenter(c2, narrowColWidth) +
      c(BOX.v, 'gray') + padCenter(c3, narrowColWidth) +
      c(BOX.v, 'gray') + padCenter(c4, narrowColWidth) +
      c(BOX.v, 'gray')
    );
  }

  // Top border
  lines.push(hLine(BOX.tl, BOX.mt, BOX.tr, headerLeftWidth, headerRightWidth));

  // Row 1: Path | Repo
  lines.push(row2(pathContent, repoContent, headerLeftWidth, headerRightWidth));

  // Separator
  lines.push(hLine(BOX.ml, BOX.mc, BOX.mr, headerLeftWidth, headerRightWidth));

  // Row 2: User+Size | CC+Model
  lines.push(row2(userContent, modelContent, headerLeftWidth, headerRightWidth));

  // Separator (transition from 2-col to 5-col)
  lines.push(hLine5(BOX.ml, BOX.mc, BOX.mt, BOX.mt, BOX.mt, BOX.mr,
    bodyWideWidth, narrowColWidth, narrowColWidth, narrowColWidth, narrowColWidth));

  // Row 3: Sync | headers
  lines.push(row5(syncContent, editHeader, newHeader, delHeader, renameHeader, bodyWideWidth));

  // Separator
  lines.push(hLine5(BOX.ml, BOX.mc, BOX.mc, BOX.mc, BOX.mc, BOX.mr,
    bodyWideWidth, narrowColWidth, narrowColWidth, narrowColWidth, narrowColWidth));

  // Row 4: Unstaged
  if (unstaged) {
    lines.push(row5(unstaged.labelContent, unstaged.editVal, unstaged.newVal, unstaged.delVal, unstaged.renameVal, bodyWideWidth));

    // Row 5: Staged (only if has staged changes)
    if (staged) {
      lines.push(row5(staged.labelContent, staged.editVal, staged.newVal, staged.delVal, staged.renameVal, bodyWideWidth));
    }
  } else {
    lines.push(row5(` ${c('No git data available', 'gray')} `, c('-', 'gray'), c('-', 'gray'), c('-', 'gray'), c('-', 'gray'), bodyWideWidth));
  }

  // Bottom border
  lines.push(hLine5(BOX.bl, BOX.mb, BOX.mb, BOX.mb, BOX.mb, BOX.br,
    bodyWideWidth, narrowColWidth, narrowColWidth, narrowColWidth, narrowColWidth));

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
