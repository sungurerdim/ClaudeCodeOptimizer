#!/usr/bin/env node

// CCO Statusline - Full Mode
// Features:
// - Progressive context warning (early thresholds: 50%/70%/85%)
// - Todo progress indicator (from transcript)
// - Conditional rendering (hide irrelevant lines)
// - Git status: branch + changes + ahead/behind
// - CLAUDE_VERSION env var → skip claude --version process

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');
const crypto = require('crypto');

// ============================================================================
// ANSI COLORS
// ============================================================================
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  gray: '\x1b[90m',
  red: '\x1b[91m',
  green: '\x1b[92m',
  yellow: '\x1b[93m',
  blue: '\x1b[94m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
  white: '\x1b[97m',
  redBold: '\x1b[1;91m',
};

function c(text, ...styles) {
  const styleStr = styles.map(s => C[s] || '').join('');
  return `${styleStr}${text}${C.reset}`;
}

// ============================================================================
// UTILITIES
// ============================================================================
function getVisibleLength(str) {
  let s = str.replace(/\x1b\[[0-9;]*m/g, '');
  s = s.replace(/[\u{FE00}-\u{FE0F}\u{200B}-\u{200D}\u{2060}\u{FEFF}]/gu, '');
  const wideEmoji = /[\u{1F300}-\u{1F9FF}\u{1FA00}-\u{1FAFF}]/gu;
  s = s.replace(wideEmoji, '  ');
  return s.length;
}

// Justify row parts to target width by distributing spaces evenly around separators
function justifyRow(parts, targetWidth, sepChar) {
  if (parts.length === 0) return '';
  if (parts.length === 1) return parts[0];

  const gaps = parts.length - 1;
  const sepWidth = sepChar ? 1 : 0; // · is 1 char
  const contentWidth = parts.reduce((sum, p) => sum + getVisibleLength(p), 0);
  const totalSepWidth = gaps * sepWidth;
  const availableSpace = Math.max(0, targetWidth - contentWidth - totalSepWidth);

  const spacePerGap = Math.floor(availableSpace / gaps);
  const extraSpaces = availableSpace % gaps;

  let result = parts[0];
  for (let i = 1; i < parts.length; i++) {
    const gapSpace = spacePerGap + (i <= extraSpaces ? 1 : 0);
    const leftPad = Math.floor(gapSpace / 2);
    const rightPad = gapSpace - leftPad;
    const sep = sepChar ? c(sepChar, 'gray') : '';
    result += ' '.repeat(leftPad) + sep + ' '.repeat(rightPad) + parts[i];
  }
  return result;
}

function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 }).replace(/\n$/, '');
  } catch { return null; }
}

// ============================================================================
// CLAUDE CODE VERSION (0-1 process)
// Set CLAUDE_VERSION env var to skip process spawn:
//   export CLAUDE_VERSION=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
// ============================================================================
function getClaudeCodeVersion() {
  // Check env var first (0 processes)
  if (process.env.CLAUDE_VERSION) {
    return process.env.CLAUDE_VERSION;
  }
  // Fallback to command (1 process)
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
  return name.replace(/^Claude\s+/, '');
}

// ============================================================================
// CONTEXT USAGE - Progressive Warning System
// Uses CC's built-in used_percentage (v2.1.6+) with manual fallback
// Thresholds: 0-50% green, 50-70% yellow, 70-85% yellow+breakdown, 85%+ red+warning
// ============================================================================
function formatContextUsage(contextWindow) {
  if (!contextWindow) return { text: c('ctx ?', 'gray'), percent: 0, breakdown: null };
  const contextSize = contextWindow.context_window_size || 0;
  if (contextSize === 0) return { text: c('ctx ?', 'gray'), percent: 0, breakdown: null };

  const currentUsage = contextWindow.current_usage;
  let inputTokens = 0, cacheTokens = 0, currentTokens = 0;

  if (currentUsage) {
    inputTokens = currentUsage.input_tokens || 0;
    cacheTokens = (currentUsage.cache_creation_input_tokens || 0) +
                  (currentUsage.cache_read_input_tokens || 0);
    currentTokens = inputTokens + cacheTokens;
  } else {
    currentTokens = contextWindow.total_input_tokens || 0;
    inputTokens = currentTokens;
  }

  // Use CC's built-in percentage (v2.1.6+) or calculate manually
  const percent = contextWindow.used_percentage !== undefined
    ? Math.round(contextWindow.used_percentage)
    : Math.round(currentTokens * 100 / contextSize);

  const formatK = n => n >= 1000 ? Math.round(n / 1000) + 'K' : n.toString();

  // Progressive color thresholds (earlier warnings)
  let color, warning = null, breakdown = null;
  if (percent >= 85) {
    color = 'red';
    warning = '⚠ COMPACT';
    breakdown = `in:${formatK(inputTokens)} cache:${formatK(cacheTokens)}`;
  } else if (percent >= 70) {
    color = 'yellow';
    breakdown = `in:${formatK(inputTokens)} cache:${formatK(cacheTokens)}`;
  } else if (percent >= 50) {
    color = 'yellow';
  } else {
    color = 'green';
  }

  const baseText = `${formatK(currentTokens)} ${percent}%`;
  let text = c(baseText, color);
  if (warning) {
    text += ' ' + c(warning, 'redBold');
  }

  return { text, percent, breakdown };
}

// ============================================================================
// PROGRESS - Read from Claude transcript
// ============================================================================
function getTranscriptPath(cwd) {
  // Claude stores transcripts in ~/.claude/projects/{hash}/
  const claudeDir = path.join(os.homedir(), '.claude', 'projects');
  if (!fs.existsSync(claudeDir)) return null;

  // Hash is based on project path
  const hash = crypto.createHash('sha256').update(cwd).digest('hex').slice(0, 16);
  const transcriptPath = path.join(claudeDir, hash, 'transcript.jsonl');

  return fs.existsSync(transcriptPath) ? transcriptPath : null;
}

function getTodoProgress(cwd) {
  const transcriptPath = getTranscriptPath(cwd);
  if (!transcriptPath) return null;

  try {
    // Read last 50KB of transcript (recent activity)
    const stat = fs.statSync(transcriptPath);
    const readSize = Math.min(stat.size, 50000);
    const fd = fs.openSync(transcriptPath, 'r');
    const buffer = Buffer.alloc(readSize);
    fs.readSync(fd, buffer, 0, readSize, Math.max(0, stat.size - readSize));
    fs.closeSync(fd);

    const content = buffer.toString('utf-8');
    const lines = content.split('\n').filter(Boolean);

    // Find last TodoWrite call (reverse search)
    let todos = null;
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(lines[i]);
        if (entry.type === 'tool_use' && entry.tool === 'TodoWrite') {
          todos = entry.input?.todos || null;
          break;
        }
        // Also check nested message format
        if (entry.message?.content) {
          const content = Array.isArray(entry.message.content)
            ? entry.message.content
            : [entry.message.content];
          for (const block of content) {
            if (block.type === 'tool_use' && block.name === 'TodoWrite') {
              todos = block.input?.todos || null;
              break;
            }
          }
          if (todos) break;
        }
      } catch { /* skip invalid JSON */ }
    }

    if (!todos || !Array.isArray(todos) || todos.length === 0) return null;

    const completed = todos.filter(t => t.status === 'completed').length;
    const inProgress = todos.find(t => t.status === 'in_progress');
    const total = todos.length;

    return { completed, total, inProgress };
  } catch {
    return null;
  }
}

function formatTodoProgress(todoInfo) {
  if (!todoInfo) return null;

  const { completed, total, inProgress } = todoInfo;

  if (completed === total) {
    return c(`✓ Done (${total}/${total})`, 'green');
  }

  // Truncate task content to 30 chars
  const taskName = inProgress?.content || 'Working...';
  const truncated = taskName.length > 30 ? taskName.slice(0, 27) + '...' : taskName;

  return c('▸ ', 'yellow') + c(truncated, 'white') + ' ' + c(`(${completed}/${total})`, 'gray');
}

// ============================================================================
// GIT INFO
// ============================================================================

// Find git root by walking up directories (fs.statSync only, no file reads)
function findGitRoot(startDir) {
  let dir = startDir;
  for (let i = 0; i < 20; i++) {
    try {
      const gitPath = path.join(dir, '.git');
      const stat = fs.statSync(gitPath);
      // .git can be file (worktree) or directory - both mean we found it
      if (stat.isDirectory() || stat.isFile()) return { root: dir };
    } catch { /* not found */ }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}


function getGitInfo() {
  // Find git root via fs stat (no file content reads)
  const gitInfo = findGitRoot(process.cwd());
  if (!gitInfo) return null;

  const repoName = path.basename(gitInfo.root);

  // Tag via git describe (1 process) - git handles disk caching
  const releaseTag = execCmd('git describe --tags --abbrev=0') || null;

  // Branch + changes + ahead/behind via git status (1 process)
  const statusV2 = execCmd('git status --porcelain=v2 -b');
  if (!statusV2) return null;

  let branch = null, ahead = 0, behind = 0;
  let mod = 0, add = 0, del = 0, ren = 0;
  let sMod = 0, sAdd = 0, sDel = 0, sRen = 0;
  let conflict = 0;

  for (const line of statusV2.split('\n')) {
    if (!line) continue;

    // Branch from status header
    if (line.startsWith('# branch.head ')) {
      branch = line.substring(14);
    }
    // Ahead/behind from status header
    else if (line.startsWith('# branch.ab ')) {
      const match = line.match(/\+(\d+) -(\d+)/);
      if (match) {
        ahead = parseInt(match[1], 10);
        behind = parseInt(match[2], 10);
      }
    }
    // Unmerged (conflicts)
    else if (line.startsWith('u ')) {
      conflict++;
    }
    // Changed entries
    else if (line.startsWith('1 ') || line.startsWith('2 ')) {
      const xy = line.substring(2, 4);
      const idx = xy.charAt(0);
      const wt = xy.charAt(1);

      if (wt === 'M') mod++;
      if (wt === 'D') del++;

      if (idx === 'M') sMod++;
      if (idx === 'A') sAdd++;
      if (idx === 'D') sDel++;
      if (idx === 'R') sRen++;
      if (idx === 'C') sAdd++;
    }
    // Untracked
    else if (line.startsWith('? ')) {
      add++;
    }
  }

  if (!branch) return null;

  const hasStaged = sMod > 0 || sAdd > 0 || sDel > 0 || sRen > 0;

  return {
    branch, repoName, releaseTag,
    mod, add, del, ren,
    sMod, sAdd, sDel, sRen,
    unpushed: ahead, behind, conflict,
    hasStaged
  };
}

// ============================================================================
// BUILD STATUSLINE - Conditional Rendering
// Layout:
//   Row 1: ▸ task (n/m) (only if todos exist) - TOP for visibility
//   Row 2: repo:branch · tag (only if git exists)
//   Row 3: △/▽ · mod/add/del/mv (only if git exists)
//   Row 4: user · CC version · model · context [in:X cache:Y] (always)
// ============================================================================
function formatStatusline(input, git, todoInfo) {
  const username = os.userInfo().username || 'user';
  const fullPath = input.cwd || process.cwd();
  const projectName = path.basename(fullPath);
  const modelDisplay = formatModelName(input.model);
  const ccVersion = getClaudeCodeVersion();
  const contextData = formatContextUsage(input.context_window);

  const emptyLine = '\u200B';

  // Prepare base parts
  const usernameStr = c(username, 'cyan');
  const versionStr = ccVersion ? c(`CC ${ccVersion}`, 'yellow') : c('CC ?', 'gray');
  const modelStr = c(modelDisplay, 'magenta');

  // Context with inline breakdown
  let contextStr = contextData.text;
  if (contextData.breakdown) {
    contextStr += ' ' + c(`[${contextData.breakdown}]`, 'gray');
  }

  // File changes helper
  function buildChangesParts(m, a, d, r) {
    return [
      m > 0 ? c(`mod ${m}`, 'yellow') : c('mod 0', 'gray'),
      a > 0 ? c(`add ${a}`, 'green') : c('add 0', 'gray'),
      d > 0 ? c(`del ${d}`, 'red') : c('del 0', 'gray'),
      r > 0 ? c(`mv ${r}`, 'cyan') : c('mv 0', 'gray')
    ];
  }

  // Calculate min row width
  function minRowWidth(parts) {
    return parts.reduce((sum, p) => sum + getVisibleLength(p), 0) + (parts.length - 1) * 3;
  }

  // Collect all rows (conditional)
  const rows = [];

  // Row 1: Todo progress (TOP - most actionable info first)
  const todoStr = formatTodoProgress(todoInfo);
  if (todoStr) {
    rows.push([todoStr]);
  }

  // Row 2 & 3: Git info (only if git exists)
  if (git) {
    const repoDisplay = `${git.repoName || projectName}:${git.branch}`;
    const repoStr = c(repoDisplay, 'green');
    const tagStr = git.releaseTag ? c(git.releaseTag, 'cyan') : null;
    const row1Parts = tagStr ? [repoStr, tagStr] : [repoStr];
    rows.push(row1Parts);

    const aheadStr = git.unpushed > 0
      ? c('△ ', 'green') + c(git.unpushed, 'white')
      : c('△ 0', 'gray');
    const behindStr = git.behind > 0
      ? c('▽ ', 'yellow') + c(git.behind, 'white')
      : c('▽ 0', 'gray');
    const alerts = [aheadStr, behindStr];
    if (git.conflict > 0) {
      alerts.push(c(`${git.conflict} conflict${git.conflict > 1 ? 's' : ''}`, 'redBold'));
    }

    const totalMod = git.mod + git.sMod;
    const totalAdd = git.add + git.sAdd;
    const totalDel = git.del + git.sDel;
    const totalRen = git.ren + git.sRen;

    const row2Parts = [alerts.join(' '), ...buildChangesParts(totalMod, totalAdd, totalDel, totalRen)];
    rows.push(row2Parts);
  }

  // Row 4: Session info (always - context with inline breakdown)
  const sessionParts = [usernameStr, versionStr, modelStr, contextStr];
  rows.push(sessionParts);

  // Calculate max width across all rows
  const maxWidth = Math.max(...rows.map(minRowWidth));

  // Build justified output
  const lines = rows.map(parts => justifyRow(parts, maxWidth, '·'));
  lines.push(emptyLine);

  return lines.join('\n');
}

// ============================================================================
// MAIN
// ============================================================================
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  const cwd = input.cwd || process.cwd();
  const git = getGitInfo();
  const todoInfo = getTodoProgress(cwd);
  console.log(formatStatusline(input, git, todoInfo));
} catch (error) {
  console.log(`[Statusline Error: ${error.message}]`);
}
