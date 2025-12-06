#!/usr/bin/env node
/**
 * CCO Statusline - Full Mode
 * 4-line comprehensive status display
 * Line 1: Project | User | Size | CC Version | Model
 * Line 2: Branch | Conflicts | Stash | Ahead | Last Activity
 * Line 3: Unstaged changes breakdown
 * Line 4: Staged changes breakdown
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

function run(cmd, fallback = '') {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
  } catch {
    return fallback;
  }
}

// Line 1: Project | User | Size | CC Version | Model
function getProjectName() {
  const gitRoot = run('git rev-parse --show-toplevel');
  if (gitRoot) return path.basename(gitRoot);
  return path.basename(process.cwd());
}

function getUser() {
  return os.userInfo().username;
}

function getDirSize() {
  // Get approximate directory size (excluding .git, node_modules, etc.)
  const size = run("du -sh --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='.venv' --exclude='venv' . 2>/dev/null | cut -f1", '?');
  return size || '?';
}

function getClaudeVersion() {
  const version = run('claude --version 2>/dev/null | head -1', '');
  // Extract version number (e.g., "2.0.56" from various formats)
  const match = version.match(/(\d+\.\d+\.\d+)/);
  return match ? `CC ${match[1]}` : 'CC ?';
}

function getModel() {
  // Try to detect model from environment or config
  const model = process.env.ANTHROPIC_MODEL || process.env.CLAUDE_MODEL || '';
  if (model.includes('opus')) return 'Opus 4.5';
  if (model.includes('sonnet')) return 'Sonnet 4';
  if (model.includes('haiku')) return 'Haiku 4';
  return 'Opus 4.5'; // Default assumption
}

// Line 2: Branch | Conflicts | Stash | Ahead | Last Activity
function getGitBranch() {
  return run('git rev-parse --abbrev-ref HEAD', 'no-git');
}

function getConflicts() {
  const conflicts = run("git diff --name-only --diff-filter=U 2>/dev/null | wc -l", '0');
  return parseInt(conflicts) || 0;
}

function getStashCount() {
  const stash = run('git stash list 2>/dev/null | wc -l', '0');
  return parseInt(stash) || 0;
}

function getAheadBehind() {
  const upstream = run('git rev-parse --abbrev-ref @{upstream} 2>/dev/null', '');
  if (!upstream) return { ahead: 0, behind: 0 };

  const counts = run('git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null', '0\t0');
  const [ahead, behind] = counts.split('\t').map(n => parseInt(n) || 0);
  return { ahead, behind };
}

function getLastActivity() {
  // Time since last commit
  const timestamp = run('git log -1 --format=%ct 2>/dev/null', '');
  if (!timestamp) return '?';

  const now = Math.floor(Date.now() / 1000);
  const diff = now - parseInt(timestamp);

  if (diff < 60) return `${diff}s`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m`;
  if (diff < 86400) {
    const hours = Math.floor(diff / 3600);
    const mins = Math.floor((diff % 3600) / 60);
    return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}`;
  }
  return `${Math.floor(diff / 86400)}d`;
}

// Lines 3-4: Change breakdown
function getChangeBreakdown() {
  // Get detailed diff stats
  const unstagedRaw = run('git diff --numstat 2>/dev/null', '');
  const stagedRaw = run('git diff --cached --numstat 2>/dev/null', '');

  // Get file status for categorization
  const statusRaw = run('git status --porcelain 2>/dev/null', '');

  function parseNumstat(raw) {
    let added = 0, deleted = 0;
    const lines = raw.split('\n').filter(l => l.trim());
    for (const line of lines) {
      const [a, d] = line.split('\t');
      added += parseInt(a) || 0;
      deleted += parseInt(d) || 0;
    }
    return { added, deleted, files: lines.length };
  }

  function categorizeChanges(statusLines, staged) {
    let edit = 0, newFile = 0, del = 0, move = 0;

    for (const line of statusLines.split('\n').filter(l => l.trim())) {
      const index = line[0];
      const worktree = line[1];
      const status = staged ? index : worktree;

      // Skip if not relevant to staged/unstaged
      if (staged && index === ' ') continue;
      if (!staged && worktree === ' ') continue;

      if (status === 'M') edit++;
      else if (status === 'A' || status === '?') newFile++;
      else if (status === 'D') del++;
      else if (status === 'R') move++;
    }

    return { edit, new: newFile, del, move };
  }

  const unstaged = parseNumstat(unstagedRaw);
  const staged = parseNumstat(stagedRaw);

  const unstagedCat = categorizeChanges(statusRaw, false);
  const stagedCat = categorizeChanges(statusRaw, true);

  return {
    unstaged: { ...unstaged, ...unstagedCat },
    staged: { ...staged, ...stagedCat }
  };
}

// Build output
const project = getProjectName();
const user = getUser();
const size = getDirSize();
const ccVersion = getClaudeVersion();
const model = getModel();

const branch = getGitBranch();
const conflicts = getConflicts();
const stash = getStashCount();
const { ahead, behind } = getAheadBehind();
const lastActivity = getLastActivity();

const changes = getChangeBreakdown();

// Format ahead/behind
let aheadBehindStr = `Ahead ${ahead}`;
if (behind > 0) aheadBehindStr += ` Behind ${behind}`;

// Line 1
console.log(`${project} | \u{1F464} ${user} | ${size} | ${ccVersion} | \u{1F9E0} ${model}`);

// Line 2
console.log(`\u{26A1} ${branch} | Conf ${conflicts} | Stash ${stash} | ${aheadBehindStr} | Last ${lastActivity}`);

// Line 3: Unstaged
console.log(`Unstaged + ${changes.unstaged.added} - ${changes.unstaged.deleted} | edit ${changes.unstaged.edit} | new ${changes.unstaged.new} | del ${changes.unstaged.del} | move ${changes.unstaged.move}`);

// Line 4: Staged
console.log(`Staged   + ${changes.staged.added} - ${changes.staged.deleted} | edit ${changes.staged.edit} | new ${changes.staged.new} | del ${changes.staged.del} | move ${changes.staged.move}`);
