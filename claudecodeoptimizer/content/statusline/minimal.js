#!/usr/bin/env node

// CCO Statusline - Minimal Mode
// Claude Code Statusline - Single line: repo:branch  +N  -N | CC X.X.X  Model

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

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
};


function c(text, color) {
  return `${C[color] || ''}${text}${C.reset}`;
}

// ============================================================================
// UTILITIES
// ============================================================================
function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 }).replace(/\n$/, '');
  } catch { return null; }
}

// ============================================================================
// DATA GATHERING
// ============================================================================
function getRepoInfo() {
  const branch = execCmd('git rev-parse --abbrev-ref HEAD');
  if (!branch) return null;

  const gitRoot = execCmd('git rev-parse --show-toplevel');
  const repoName = gitRoot ? path.basename(gitRoot) : null;

  // Line counts (unstaged + untracked)
  let addLines = 0, remLines = 0;

  const unstaged = execCmd('git diff --numstat');
  if (unstaged) {
    for (const line of unstaged.split('\n')) {
      const p = line.split(/\s+/);
      if (p.length >= 2) {
        const a = parseInt(p[0], 10), r = parseInt(p[1], 10);
        if (!isNaN(a)) addLines += a;
        if (!isNaN(r)) remLines += r;
      }
    }
  }

  // Untracked files line count
  const statusOutput = execCmd('git status --porcelain') || '';
  let untracked = 0;
  for (const line of statusOutput.split('\n')) {
    if (line.startsWith('??')) untracked++;
  }

  if (untracked > 0 && untracked <= 100) {
    const untrackedLines = execCmd('bash -c "git ls-files --others --exclude-standard | head -100 | xargs cat 2>/dev/null | wc -l"');
    if (untrackedLines) {
      const lines = parseInt(untrackedLines, 10);
      if (!isNaN(lines)) addLines += lines;
    }
  }

  return { branch, repoName, addLines, remLines };
}

function getClaudeCodeVersion() {
  const version = execCmd('claude --version');
  if (version) {
    const match = version.match(/(\d+\.\d+\.\d+)/);
    if (match) return match[1];
  }
  return null;
}

function formatModelName(modelData) {
  const name = modelData?.display_name || 'Unknown';
  return name.replace(/^Claude\s+/, '');
}

function getLatestRelease() {
  const tag = execCmd('git describe --tags --abbrev=0 2>/dev/null');
  return tag || null;
}

// ============================================================================
// MAIN
// ============================================================================
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  const repo = getRepoInfo();
  const ccVersion = getClaudeCodeVersion();
  const modelDisplay = formatModelName(input.model);
  const latestRelease = getLatestRelease();

  // Build output parts - dynamic width, no padding
  const repoDisplay = repo ? `${repo.repoName}:${repo.branch}` : 'no-git';
  const releaseStr = latestRelease ? '  ' + c(latestRelease, 'cyan') : '';
  const addStr = repo && repo.addLines > 0 ? c(`+${repo.addLines}`, 'green') : c('+0', 'gray');
  const remStr = repo && repo.remLines > 0 ? c(`-${repo.remLines}`, 'red') : c('-0', 'gray');
  const versionStr = ccVersion ? c(`v${ccVersion}`, 'yellow') : c('v?', 'gray');
  const modelStr = c(modelDisplay, 'magenta');
  const sep = c('·', 'gray');

  // Two line output
  console.log(repoDisplay + releaseStr);
  console.log(`${addStr} ${remStr} ${sep} ${versionStr} ${sep} ${modelStr}`);
} catch (error) {
  console.log(`[Statusline Error: ${error.message}]`);
}
