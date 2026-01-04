#!/usr/bin/env node

// CCO Statusline - Minimal Mode
// Single line: user · CC version · model · context
// Progressive context warning (50%/70%/85% thresholds)
// CLAUDE_VERSION env var → skip claude --version process

const fs = require('fs');
const { execSync } = require('child_process');
const os = require('os');

const C = {
  reset: '\x1b[0m',
  gray: '\x1b[90m',
  green: '\x1b[92m',
  yellow: '\x1b[93m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
  red: '\x1b[91m',
  redBold: '\x1b[1;91m',
};

function c(text, color) {
  return `${C[color] || ''}${text}${C.reset}`;
}

function getClaudeCodeVersion() {
  if (process.env.CLAUDE_VERSION) return process.env.CLAUDE_VERSION;
  try {
    const version = execSync('claude --version', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 });
    const match = version.match(/(\d+\.\d+\.\d+)/);
    return match ? match[1] : null;
  } catch { return null; }
}

function formatContextUsage(contextWindow) {
  if (!contextWindow) return c('ctx ?', 'gray');
  const contextSize = contextWindow.context_window_size || 0;
  if (contextSize === 0) return c('ctx ?', 'gray');

  const currentUsage = contextWindow.current_usage;
  let currentTokens = 0;

  if (currentUsage) {
    currentTokens = (currentUsage.input_tokens || 0) +
                    (currentUsage.cache_creation_input_tokens || 0) +
                    (currentUsage.cache_read_input_tokens || 0);
  } else {
    currentTokens = contextWindow.total_input_tokens || 0;
  }

  const percent = Math.round(currentTokens * 100 / contextSize);
  const formatK = n => n >= 1000 ? Math.round(n / 1000) + 'K' : n.toString();

  // Progressive color thresholds (earlier warnings)
  let color, warning = '';
  if (percent >= 85) {
    color = 'red';
    warning = ' ' + c('⚠ COMPACT', 'redBold');
  } else if (percent >= 50) {
    color = 'yellow';
  } else {
    color = 'green';
  }

  return c(`${formatK(currentTokens)} ${percent}%`, color) + warning;
}

try {
  const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
  const username = os.userInfo().username || 'user';
  const ccVersion = getClaudeCodeVersion();
  const modelName = (input.model?.display_name || 'Unknown').replace(/^Claude\s+/, '');
  const contextUsage = formatContextUsage(input.context_window);

  const sep = ' ' + c('·', 'gray') + ' ';
  const parts = [
    c(username, 'cyan'),
    ccVersion ? c(`CC ${ccVersion}`, 'yellow') : c('CC ?', 'gray'),
    c(modelName, 'magenta'),
    contextUsage  // Always show context
  ];

  console.log('\n' + parts.join(sep) + '\n');
} catch (error) {
  console.log(`[Error: ${error.message}]`);
}
