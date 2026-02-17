package main

const repo = "sungurerdim/ClaudeCodeOptimizer"

var rulesFiles = []string{
	"rules/cco-rules.md",
}

var skillFiles = []string{
	"skills/cco-optimize/SKILL.md",
	"skills/cco-align/SKILL.md",
	"skills/cco-commit/SKILL.md",
	"skills/cco-research/SKILL.md",
	"skills/cco-docs/SKILL.md",
	"skills/cco-update/SKILL.md",
	"skills/cco-blueprint/SKILL.md",
	"skills/cco-pr/SKILL.md",
}

var agentFiles = []string{
	"agents/cco-agent-analyze.md",
	"agents/cco-agent-apply.md",
	"agents/cco-agent-research.md",
}

// v3 legacy command files to remove
var legacyV3Commands = []string{
	"commands/cco-optimize.md",
	"commands/cco-align.md",
	"commands/cco-commit.md",
	"commands/cco-research.md",
	"commands/cco-docs.md",
	"commands/cco-update.md",
	"commands/cco-blueprint.md",
	"commands/cco-pr.md",
}

// v2 legacy non-prefixed command files
var legacyV2Commands = []string{
	"commands/optimize.md",
	"commands/align.md",
	"commands/commit.md",
	"commands/research.md",
	"commands/preflight.md",
	"commands/docs.md",
	"commands/tune.md",
}

// Legacy directories to remove
var legacyDirs = []string{
	"commands/schemas",
	"rules/core",
	"rules/frameworks",
	"rules/languages",
	"rules/operations",
	"hooks",
}
