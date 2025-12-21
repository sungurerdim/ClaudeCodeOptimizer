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
  const contextSize = contextWindow.context_window_size || 0;
  if (contextSize === 0) return null;

  // Use current_usage if available (more accurate), otherwise fallback to total_input_tokens
  // NOTE: Output tokens are NOT counted - they don't consume context window
  const currentUsage = contextWindow.current_usage;
  let currentTokens;

  if (currentUsage) {
    // Accurate: input + cache tokens = actual context usage
    currentTokens = (currentUsage.input_tokens || 0) +
                    (currentUsage.cache_creation_input_tokens || 0) +
                    (currentUsage.cache_read_input_tokens || 0);
  } else {
    // Fallback: only input tokens (not output!)
    currentTokens = contextWindow.total_input_tokens || 0;
  }

  const percent = Math.round(currentTokens * 100 / contextSize);
  const formatK = n => n >= 1000 ? Math.round(n / 1000) + 'K' : n.toString();

  return `${formatK(currentTokens)} ${percent}%`;
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
