#!/usr/bin/env node

// CCO Statusline - Minimal Mode (Optimized)
// Single line compact view with minimal I/O

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
// GIT INFO - OPTIMIZED (1-2 processes)
// ============================================================================
function getRepoInfo() {
  const statusV2 = execCmd('git status --porcelain=v2 -b 2>/dev/null');
  if (!statusV2) return null;

  let branch = null;
  let changed = 0, untracked = 0;

  for (const line of statusV2.split('\n')) {
    if (!line) continue;
    if (line.startsWith('# branch.head ')) {
      branch = line.substring(14);
    } else if (line.startsWith('1 ') || line.startsWith('2 ')) {
      changed++;
    } else if (line.startsWith('? ')) {
      untracked++;
    }
  }

  if (!branch) return null;

  const gitRoot = execCmd('git rev-parse --show-toplevel');
  const repoName = gitRoot ? path.basename(gitRoot) : null;
  const releaseTag = execCmd('git describe --tags --abbrev=0 2>/dev/null') || null;

  return { branch, repoName, releaseTag, changed, untracked };
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

function formatContextUsage(contextWindow) {
  if (!contextWindow) return null;
  const inputTokens = contextWindow.total_input_tokens || 0;
  const outputTokens = contextWindow.total_output_tokens || 0;
  const contextSize = contextWindow.context_window_size || 0;
  if (contextSize === 0) return null;

  const totalUsed = inputTokens + outputTokens;
  const percent = Math.round(totalUsed * 100 / contextSize);
  const formatK = n => n >= 1000 ? Math.round(n / 1000) + 'K' : n.toString();

  return `${formatK(totalUsed)}/${formatK(contextSize)} · ${percent}%`;
}

// ============================================================================
// MAIN
// ============================================================================
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  const repo = getRepoInfo();
  const ccVersion = getClaudeCodeVersion();
  const modelDisplay = formatModelName(input.model);
  const contextUsage = formatContextUsage(input.context_window);

  // Build output
  const repoDisplay = repo ? `${repo.repoName}:${repo.branch}` : 'no-git';
  const releaseStr = repo?.releaseTag ? '  ' + c(repo.releaseTag, 'cyan') : '';

  // File counts instead of line counts
  const totalChanges = repo ? repo.changed + repo.untracked : 0;
  const changesStr = totalChanges > 0 ? c(`${totalChanges} files`, 'yellow') : c('clean', 'gray');

  const versionStr = ccVersion ? c(`v${ccVersion}`, 'yellow') : c('v?', 'gray');
  const modelStr = c(modelDisplay, 'magenta');
  const sep = c('·', 'gray');

  const emptyLine = '\u200B';
  const lines = [];

  if (contextUsage) {
    lines.push(c(contextUsage, 'cyan'));
  } else {
    lines.push(emptyLine);
  }

  lines.push(repoDisplay + releaseStr);
  lines.push(`${changesStr} ${sep} ${versionStr} ${sep} ${modelStr}`);
  lines.push(emptyLine);

  console.log(lines.join('\n'));
} catch (error) {
  console.log(`[Statusline Error: ${error.message}]`);
}
