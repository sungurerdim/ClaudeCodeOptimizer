/**
 * CCO Core Rules Injector
 * Runs on SessionStart - injects core rules directly into context via additionalContext.
 * No file copying needed, works on first session.
 */

const fs = require('fs');
const path = require('path');

const PLUGIN_DIR = path.dirname(__dirname);
const CORE_RULES_DIR = path.join(PLUGIN_DIR, 'rules', 'core');

try {
  // Find all cco-*.md files in core
  const coreFiles = fs.readdirSync(CORE_RULES_DIR)
    .filter(f => f.startsWith('cco-') && f.endsWith('.md'))
    .sort();

  // Read and concatenate all core rules
  let rulesContent = '';
  for (const file of coreFiles) {
    const content = fs.readFileSync(path.join(CORE_RULES_DIR, file), 'utf8');
    rulesContent += content + '\n\n';
  }

  // Output JSON with additionalContext for direct context injection
  const output = {
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: rulesContent.trim()
    }
  };

  console.log(JSON.stringify(output));
  process.exit(0);
} catch (err) {
  // On error, exit silently (don't break session)
  console.error(JSON.stringify({ error: err.message }));
  process.exit(0);
}
