#!/usr/bin/env node

// CCO Statusline - Minimal Mode
// Single line: user · CC version · model · context

const fs = require('fs');
const { execSync } = require('child_process');
const os = require('os');

const C = {
  reset: '\x1b[0m',
  gray: '\x1b[90m',
  yellow: '\x1b[93m',
  magenta: '\x1b[95m',
  cyan: '\x1b[96m',
};

function c(text, color) {
  return `${C[color] || ''}${text}${C.reset}`;
}

function getClaudeCodeVersion() {
  try {
    const version = execSync('claude --version', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 });
    const match = version.match(/(\d+\.\d+\.\d+)/);
    return match ? match[1] : null;
  } catch { return null; }
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

  return `${formatK(totalUsed)} ${percent}%`;
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
    c(modelName, 'magenta')
  ];
  if (contextUsage) parts.push(c(contextUsage, 'cyan'));

  console.log('\n' + parts.join(sep) + '\n');
} catch (error) {
  console.log(`[Error: ${error.message}]`);
}
