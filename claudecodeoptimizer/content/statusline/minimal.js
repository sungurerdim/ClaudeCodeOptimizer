#!/usr/bin/env node
/**
 * CCO Statusline - Minimal Mode
 * Shows: Project | Branch
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

const project = getProjectName();
const branch = getGitBranch();

console.log(`${project} | ${branch}`);
