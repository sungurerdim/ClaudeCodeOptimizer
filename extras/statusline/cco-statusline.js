#!/usr/bin/env node

// CCO Statusline (Node.js fallback)
// Use the Go binary for zero-dependency, faster execution.
// This version is for users who have Node.js but not the compiled binary.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// ============================================================================
// ANSI COLORS
// ============================================================================
const C = {
  reset: '\x1b[0m',
  gray: '\x1b[90m',
  red: '\x1b[91m',
  green: '\x1b[92m',
  yellow: '\x1b[93m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
  white: '\x1b[97m',
  redBold: '\x1b[1;91m',
};

function c(text, style) {
  return `${C[style] || ''}${text}${C.reset}`;
}

// ============================================================================
// UTILITIES
// ============================================================================
function visibleLen(str) {
  return str.replace(/\x1b\[[0-9;]*m/g, '').length;
}

function justifyRow(parts, targetWidth, sep) {
  if (parts.length <= 1) return parts[0] || '';

  const gaps = parts.length - 1;
  const contentWidth = parts.reduce((sum, p) => sum + visibleLen(p), 0);
  const available = Math.max(0, targetWidth - contentWidth - gaps);

  const perGap = Math.floor(available / gaps);
  const extra = available % gaps;

  let result = parts[0];
  for (let i = 1; i < parts.length; i++) {
    const gap = perGap + (i <= extra ? 1 : 0);
    const left = Math.floor(gap / 2);
    const right = gap - left;
    result += ' '.repeat(left) + c(sep, 'gray') + ' '.repeat(right) + parts[i];
  }
  return result;
}

function execGit(...args) {
  try {
    return execSync('git ' + args.join(' '), {
      encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 1500,
    }).replace(/\n$/, '');
  } catch { return null; }
}

// ============================================================================
// GIT INFO
// ============================================================================
function getGitInfo() {
  // Use git rev-parse instead of walking dirs with statSync
  const repoRoot = execGit('rev-parse', '--show-toplevel');
  if (!repoRoot) return null;

  const repoName = path.basename(repoRoot);

  // Single tag via for-each-ref (no need to list all tags)
  const tag = execGit('for-each-ref', '--sort=-v:refname', '--count=1', '--format=%(refname:short)', 'refs/tags/');

  const statusV2 = execGit('status', '--porcelain=v2', '-b');
  if (!statusV2) return null;

  let branch = null, ahead = 0, behind = 0;
  let mod = 0, add = 0, del = 0, ren = 0, conflict = 0;

  for (const line of statusV2.split('\n')) {
    if (!line) continue;

    if (line.startsWith('# branch.head ')) {
      branch = line.substring(14);
    } else if (line.startsWith('# branch.ab ')) {
      const m = line.match(/\+(\d+) -(\d+)/);
      if (m) { ahead = +m[1]; behind = +m[2]; }
    } else if (line.startsWith('u ')) {
      conflict++;
    } else if (line.startsWith('1 ') || line.startsWith('2 ')) {
      if (line.length < 4) continue;
      const idx = line[2], wt = line[3];
      if (wt === 'M') mod++;
      if (wt === 'D') del++;
      if (idx === 'M') mod++;
      if (idx === 'A' || idx === 'C') add++;
      if (idx === 'D') del++;
      if (idx === 'R') ren++;
    } else if (line.startsWith('? ')) {
      add++;
    }
  }

  if (!branch) return null;
  return { branch, repoName, tag: tag || null, mod, add, del, ren, ahead, behind, conflict };
}

// ============================================================================
// FORMAT
// ============================================================================
function formatContextUsage(cw) {
  if (!cw || !cw.context_window_size) return null;
  const cu = cw.current_usage;
  const tokens = cu
    ? (cu.input_tokens || 0) + (cu.cache_creation_input_tokens || 0) + (cu.cache_read_input_tokens || 0)
    : (cw.total_input_tokens || 0);
  const pct = Math.round(tokens * 100 / cw.context_window_size);
  const k = tokens >= 1000 ? Math.round(tokens / 1000) + 'K' : String(tokens);
  return `${k} ${pct}%`;
}

function buildStatusline(input, git) {
  const username = os.userInfo().username || 'user';
  const projectName = path.basename(input.cwd || process.cwd());
  const model = (input.model?.display_name || 'Unknown').replace(/^Claude\s+/, '');
  // Read version from stdin JSON (no process spawn needed)
  const version = input.version || null;
  const ctx = formatContextUsage(input.context_window);

  // Row 1: Location
  const repo = git ? `${git.repoName}:${git.branch}` : projectName;
  const row1 = [c(repo, 'green')];
  if (git?.tag) row1.push(c(git.tag, 'cyan'));

  // Row 2: Status
  let row2;
  if (!git) {
    row2 = [c('No git', 'gray')];
  } else {
    const ah = git.ahead > 0 ? c('\u25B3 ', 'green') + c(git.ahead, 'white') : c('\u25B3 0', 'gray');
    const bh = git.behind > 0 ? c('\u25BD ', 'yellow') + c(git.behind, 'white') : c('\u25BD 0', 'gray');
    let alert = ah + ' ' + bh;
    if (git.conflict > 0) alert += ' ' + c(`${git.conflict} conflict`, 'redBold');

    const ch = (label, n, style) => n > 0 ? c(`${label} ${n}`, style) : c(`${label} 0`, 'gray');
    row2 = [alert, ch('mod', git.mod, 'yellow'), ch('add', git.add, 'green'), ch('del', git.del, 'red'), ch('mv', git.ren, 'cyan')];
  }

  // Row 3: Session
  const verStr = version ? c(`CC ${version}`, 'yellow') : c('CC ?', 'gray');
  const row3 = [c(username, 'cyan'), verStr, c(model, 'magenta')];
  if (ctx) row3.push(c(ctx, 'cyan'));

  // Justify
  const minW = parts => parts.reduce((s, p) => s + visibleLen(p), 0) + (parts.length - 1) * 3;
  const maxW = Math.max(minW(row1), minW(row2), minW(row3));

  return [
    justifyRow(row1, maxW, '\u00B7'),
    justifyRow(row2, maxW, '\u00B7'),
    justifyRow(row3, maxW, '\u00B7'),
    '\u200B',
  ].join('\n');
}

// ============================================================================
// MAIN
// ============================================================================
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  console.log(buildStatusline(input, getGitInfo()));
} catch (e) {
  console.log(`[Statusline Error: ${e.message}]`);
}
