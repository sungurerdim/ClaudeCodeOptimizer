#!/usr/bin/env bash
# CCO — Claude Code Optimizer Installer (Unix/Mac)
#
# Stable (latest release):
#   curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
#
# Dev (latest dev branch):
#   curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash -s -- --dev

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
RULES_FILES="rules/cco-rules.md"
COMMAND_FILES="
  commands/cco-optimize.md
  commands/cco-align.md
  commands/cco-commit.md
  commands/cco-research.md
  commands/cco-preflight.md
  commands/cco-docs.md
  commands/cco-update.md
"
AGENT_FILES="
  agents/cco-agent-analyze.md
  agents/cco-agent-apply.md
  agents/cco-agent-research.md
"

info()  { printf "\033[0;34m%s\033[0m\n" "$1"; }
ok()    { printf "\033[0;32m%s\033[0m\n" "$1"; }
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

# Create directories
for dir in rules commands agents; do
  mkdir -p "${CLAUDE_DIR}/${dir}"
done

# Download and install files
download() {
  local file="$1"
  local dest="${CLAUDE_DIR}/${file}"
  if curl -fsSL "${BASE_URL}/${file}" -o "${dest}" 2>/dev/null; then
    ok "  + ${file}"
  else
    err "  ! ${file} (download failed)"
    return 1
  fi
}

failed=0

info ""
info "Installing rules..."
for file in ${RULES_FILES}; do
  download "${file}" || ((failed++))
done

info ""
info "Installing commands..."
for file in ${COMMAND_FILES}; do
  download "${file}" || ((failed++))
done

info ""
info "Installing agents..."
for file in ${AGENT_FILES}; do
  download "${file}" || ((failed++))
done

# Update version frontmatter with current timestamp
RULES_PATH="${CLAUDE_DIR}/rules/cco-rules.md"
if [ -f "${RULES_PATH}" ]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S" 2>/dev/null)
  if command -v sed >/dev/null 2>&1; then
    sed -i.bak "s/^last_update_check:.*/last_update_check: ${TIMESTAMP}/" "${RULES_PATH}" 2>/dev/null && rm -f "${RULES_PATH}.bak"
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
  info ""
  info "Restart Claude Code to activate."
  info "Run /cco-optimize to get started."
else
  err "Installation completed with ${failed} error(s)."
  err "Re-run the installer or download files manually."
  exit 1
fi
