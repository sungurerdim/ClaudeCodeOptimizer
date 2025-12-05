#!/usr/bin/env node
/**
 * CCO Statusline - Full Mode
 * Shows: Project | Branch | Changes
 */

const { execSync } = require('child_process');
const path = require('path');

function run(cmd, fallback = '') {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
  } catch {
    return fallback;
  }
}

function getProjectName() {
  const gitRoot = run('git rev-parse --show-toplevel');
  if (gitRoot) return path.basename(gitRoot);
  return path.basename(process.cwd());
}

function getGitBranch() {
  return run('git rev-parse --abbrev-ref HEAD', 'no-git');
}

function getGitChanges() {
  const staged = run('git diff --cached --numstat | wc -l', '0').trim();
  const unstaged = run('git diff --numstat | wc -l', '0').trim();
  const stagedNum = parseInt(staged) || 0;
  const unstagedNum = parseInt(unstaged) || 0;

  if (stagedNum === 0 && unstagedNum === 0) return 'clean';
  return `${stagedNum}/${unstagedNum}`;
}

const project = getProjectName();
const branch = getGitBranch();
const changes = getGitChanges();

console.log(`${project} | ${branch} | ${changes}`);
