#!/usr/bin/env bash
# Setup branch protection rules for main branch
# Requires: gh CLI authenticated with admin access
# Usage: ./scripts/setup-branch-protection.sh

set -euo pipefail

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Setting up branch protection for $REPO main branch..."

gh api "repos/$REPO/branches/main/protection" \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Validate Plugin Structure",
      "Lint & Type Check",
      "Run Tests"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

echo "Branch protection configured successfully."
echo ""
echo "Rules applied:"
echo "  - Require PR before merging"
echo "  - Require status checks: validate, lint, test"
echo "  - Strict status checks (branch must be up to date)"
echo "  - Enforce for admins (no bypassing)"
echo "  - No force pushes"
echo "  - No branch deletion"
