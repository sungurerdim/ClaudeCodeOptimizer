#!/usr/bin/env bash
# CCO — Claude Code Optimizer Installer (Unix/Mac)
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash

set -euo pipefail

REPO="sungurerdim/ClaudeCodeOptimizer"
CLAUDE_DIR="${HOME}/.claude"

# Files to install
RULES_FILES=(
  "rules/cco-rules.md"
)
COMMAND_FILES=(
  "commands/cco-optimize.md"
  "commands/cco-align.md"
  "commands/cco-commit.md"
  "commands/cco-research.md"
  "commands/cco-docs.md"
  "commands/cco-update.md"
  "commands/cco-blueprint.md"
  "commands/cco-pr.md"
)
AGENT_FILES=(
  "agents/cco-agent-analyze.md"
  "agents/cco-agent-apply.md"
  "agents/cco-agent-research.md"
)
# v2.x commands without cco- prefix (must be hardcoded, no distinguishing pattern)
LEGACY_NON_PREFIXED_FILES=(
  "commands/optimize.md"
  "commands/align.md"
  "commands/commit.md"
  "commands/research.md"
  "commands/preflight.md"
  "commands/docs.md"
  "commands/tune.md"
)
# v2.x directories to remove entirely
LEGACY_DIRS=(
  "commands/schemas"
  "rules/core"
  "rules/frameworks"
  "rules/languages"
  "rules/operations"
  "hooks"
)
# Current v3 files to keep (everything else matching cco-* gets removed)
CURRENT_COMMANDS=()
for f in "${COMMAND_FILES[@]}"; do CURRENT_COMMANDS+=("$(basename "$f")"); done
CURRENT_AGENTS=()
for f in "${AGENT_FILES[@]}"; do CURRENT_AGENTS+=("$(basename "$f")"); done
CURRENT_RULES=("cco-rules.md")

info()  { printf "\033[0;34m%s\033[0m\n" "$1"; }
ok()    { printf "\033[0;32m%s\033[0m\n" "$1"; }
warn()  { printf "\033[0;33m%s\033[0m\n" "$1"; }
err()   { printf "\033[0;31m%s\033[0m\n" "$1" >&2; }

info "CCO Installer"
info "============="

# Resolve latest release tag
LATEST_TAG=$(curl -fsSL "https://api.github.com/repos/${REPO}/tags?per_page=1" 2>/dev/null \
  | grep -m1 '"name"' \
  | sed 's/.*"name": *"\([^"]*\)".*/\1/' 2>/dev/null) || true

if [ -n "${LATEST_TAG:-}" ]; then
  REF="$LATEST_TAG"
  info "Channel: stable ($LATEST_TAG)"
else
  REF="main"
  info "Channel: stable (main — no tags found)"
fi

BASE_URL="https://raw.githubusercontent.com/${REPO}/${REF}"

# Preflight: verify the resolved ref has the expected file structure
info ""
info "Verifying source..."
TEST_CONTENT=$(curl -fsSL "${BASE_URL}/rules/cco-rules.md" 2>/dev/null) || true
if [ -z "${TEST_CONTENT:-}" ] || ! printf '%s' "$TEST_CONTENT" | head -1 | grep -q "^---"; then
  err "  Source verification failed: ${REF} does not contain CCO files."
  err ""
  err "  The latest release tag (${REF}) may predate the install-script distribution model."
  err "  Check the repository for updates: https://github.com/${REPO}"
  exit 1
fi
ok "  Source verified (${REF})"

# Create directories
for dir in rules commands agents; do
  mkdir -p "${CLAUDE_DIR}/${dir}"
done

# Download, validate, and install a single file
download() {
  local file="$1"
  local dest="${CLAUDE_DIR}/${file}"
  local content

  content=$(curl -fsSL "${BASE_URL}/${file}" 2>/dev/null) || {
    err "  ! ${file} (download failed)"
    return 1
  }

  # Validate: CCO markdown files must start with YAML frontmatter
  if [ -z "$content" ] || ! printf '%s' "$content" | head -1 | grep -q "^---"; then
    err "  ! ${file} (invalid content - not a CCO file)"
    return 1
  fi

  # Write validated content to disk
  printf '%s\n' "$content" > "$dest"
  ok "  + ${file}"
}

failed=0

info ""
info "Installing rules..."
for file in "${RULES_FILES[@]}"; do
  download "${file}" || failed=$((failed + 1))
done

info ""
info "Installing commands..."
for file in "${COMMAND_FILES[@]}"; do
  download "${file}" || failed=$((failed + 1))
done

info ""
info "Installing agents..."
for file in "${AGENT_FILES[@]}"; do
  download "${file}" || failed=$((failed + 1))
done

# Clean up legacy files from previous CCO versions (v1.x + v2.x)
legacy_cleaned=0

# Uninstall v2.x plugin if present (files managed by Claude Code plugin system)
if command -v claude >/dev/null 2>&1; then
  claude plugin uninstall "cco@ClaudeCodeOptimizer" >/dev/null 2>&1 || true
  claude plugin marketplace remove "ClaudeCodeOptimizer" >/dev/null 2>&1 || true
fi

# Uninstall v1.x pip package if present
if command -v pip >/dev/null 2>&1; then
  pip uninstall claudecodeoptimizer -y >/dev/null 2>&1 || true
fi

# Helper: check if value is in array
is_current() {
  local needle="$1"; shift
  for item in "$@"; do [ "$item" = "$needle" ] && return 0; done
  return 1
}

# Remove v2.x non-prefixed command files
for file in "${LEGACY_NON_PREFIXED_FILES[@]}"; do
  legacy_path="${CLAUDE_DIR}/${file}"
  if [ -f "$legacy_path" ]; then
    rm -f "$legacy_path"
    legacy_cleaned=$((legacy_cleaned + 1))
  fi
done

# Remove any cco-*.md in commands/ that is NOT a current v3 command
for file in "${CLAUDE_DIR}"/commands/cco-*.md; do
  [ -f "$file" ] || continue
  is_current "$(basename "$file")" "${CURRENT_COMMANDS[@]}" || {
    rm -f "$file"
    legacy_cleaned=$((legacy_cleaned + 1))
  }
done

# Remove any cco-*.md in agents/ that is NOT a current v3 agent
for file in "${CLAUDE_DIR}"/agents/cco-*.md; do
  [ -f "$file" ] || continue
  is_current "$(basename "$file")" "${CURRENT_AGENTS[@]}" || {
    rm -f "$file"
    legacy_cleaned=$((legacy_cleaned + 1))
  }
done

# Remove any cco-*.md in rules/ that is NOT cco-rules.md
for file in "${CLAUDE_DIR}"/rules/cco-*.md; do
  [ -f "$file" ] || continue
  is_current "$(basename "$file")" "${CURRENT_RULES[@]}" || {
    rm -f "$file"
    legacy_cleaned=$((legacy_cleaned + 1))
  }
done

# Remove legacy directories
for dir in "${LEGACY_DIRS[@]}"; do
  legacy_path="${CLAUDE_DIR}/${dir}"
  if [ -d "$legacy_path" ]; then
    rm -rf "$legacy_path"
    legacy_cleaned=$((legacy_cleaned + 1))
  fi
done

# Update version frontmatter with current timestamp
RULES_PATH="${CLAUDE_DIR}/rules/cco-rules.md"
if [ -f "${RULES_PATH}" ]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S" 2>/dev/null)
  if [ "$(uname)" = "Darwin" ]; then
    # macOS BSD sed requires '' after -i
    sed -i '' "s/^last_update_check:.*/last_update_check: ${TIMESTAMP}/" "${RULES_PATH}"
  else
    sed -i "s/^last_update_check:.*/last_update_check: ${TIMESTAMP}/" "${RULES_PATH}"
  fi
fi

info ""
if [ "${failed}" -eq 0 ]; then
  ok "CCO installed successfully! (${REF})"
  info ""
  info "Installed to: ${CLAUDE_DIR}/"
  info "  rules/cco-rules.md"
  info "  commands/cco-*.md (8 commands)"
  info "  agents/cco-agent-*.md (3 agents)"
  if [ "${legacy_cleaned}" -gt 0 ]; then
    info ""
    warn "Cleaned up ${legacy_cleaned} legacy file(s) from previous CCO version."
  fi
  info ""
  info "Restart Claude Code to activate."
  info "Run /cco-optimize to get started."
else
  err "Installation completed with ${failed} error(s)."
  err "Re-run the installer or download files manually."
  exit 1
fi
