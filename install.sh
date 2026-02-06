#!/usr/bin/env bash
# CCO — Claude Code Optimizer Installer (Unix/Mac)
#
# Stable (latest release):
#   curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
#
# Dev (latest dev branch):
#   curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/dev/install.sh | bash -s -- --dev

set -euo pipefail

REPO="sungurerdim/ClaudeCodeOptimizer"
CLAUDE_DIR="${HOME}/.claude"
CHANNEL="${CCO_CHANNEL:-stable}"

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dev)    CHANNEL="dev" ;;
    --stable) CHANNEL="stable" ;;
  esac
done

# Files to install
RULES_FILES=(
  "rules/cco-rules.md"
)
COMMAND_FILES=(
  "commands/cco-optimize.md"
  "commands/cco-align.md"
  "commands/cco-commit.md"
  "commands/cco-research.md"
  "commands/cco-preflight.md"
  "commands/cco-docs.md"
  "commands/cco-update.md"
)
AGENT_FILES=(
  "agents/cco-agent-analyze.md"
  "agents/cco-agent-apply.md"
  "agents/cco-agent-research.md"
)
# Old file names from previous CCO versions (for cleanup)
LEGACY_COMMAND_FILES=(
  "commands/optimize.md"
  "commands/align.md"
  "commands/commit.md"
  "commands/research.md"
  "commands/preflight.md"
  "commands/docs.md"
)

info()  { printf "\033[0;34m%s\033[0m\n" "$1"; }
ok()    { printf "\033[0;32m%s\033[0m\n" "$1"; }
warn()  { printf "\033[0;33m%s\033[0m\n" "$1"; }
err()   { printf "\033[0;31m%s\033[0m\n" "$1" >&2; }

info "CCO Installer"
info "============="

# Resolve channel to a git ref
if [ "$CHANNEL" = "dev" ]; then
  REF="dev"
  info "Channel: dev (latest commit)"
else
  # Fetch latest tag from GitHub API
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
fi

BASE_URL="https://raw.githubusercontent.com/${REPO}/${REF}"

# Preflight: verify the resolved ref has the expected file structure
info ""
info "Verifying source..."
TEST_CONTENT=$(curl -fsSL "${BASE_URL}/rules/cco-rules.md" 2>/dev/null) || true
if [ -z "${TEST_CONTENT:-}" ] || ! printf '%s' "$TEST_CONTENT" | head -1 | grep -q "^---"; then
  err "  Source verification failed: ${REF} does not contain CCO files."
  err ""
  if [ "$CHANNEL" = "stable" ]; then
    err "  The latest release tag (${REF}) predates the install-script distribution model."
    err "  Use the dev channel until a new release is published:"
    err ""
    err "    curl -fsSL https://raw.githubusercontent.com/${REPO}/dev/install.sh | bash -s -- --dev"
    err ""
  else
    err "  Could not download files from the '${REF}' ref."
    err "  Check the repository URL and try again."
  fi
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

# Clean up legacy files from previous CCO versions
legacy_cleaned=0
for file in "${LEGACY_COMMAND_FILES[@]}"; do
  legacy_path="${CLAUDE_DIR}/${file}"
  if [ -f "$legacy_path" ]; then
    rm -f "$legacy_path"
    legacy_cleaned=$((legacy_cleaned + 1))
  fi
done
# Legacy schema files
schema_dir="${CLAUDE_DIR}/commands/schemas"
if [ -d "$schema_dir" ]; then
  rm -rf "$schema_dir"
  legacy_cleaned=$((legacy_cleaned + 1))
fi

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
  info "  commands/cco-*.md (7 commands)"
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
