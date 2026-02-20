package main

// ============================================================================
// ANSI COLORS
// ============================================================================

const (
	reset   = "\x1b[0m"
	gray    = "\x1b[90m"
	red     = "\x1b[91m"
	green   = "\x1b[92m"
	yellow  = "\x1b[93m"
	magenta = "\x1b[95m"
	cyan    = "\x1b[96m"
	white   = "\x1b[97m"
	redBold = "\x1b[1;91m"
)

func c(text, style string) string {
	return style + text + reset
}

// ============================================================================
// INPUT SCHEMA (Claude Code stdin JSON)
// ============================================================================

type CurrentUsage struct {
	InputTokens              int64 `json:"input_tokens"`
	CacheCreationInputTokens int64 `json:"cache_creation_input_tokens"`
	CacheReadInputTokens     int64 `json:"cache_read_input_tokens"`
}

type ContextWindow struct {
	ContextWindowSize int64         `json:"context_window_size"`
	TotalInputTokens  int64         `json:"total_input_tokens"`
	CurrentUsage      *CurrentUsage `json:"current_usage"`
}

type Workspace struct {
	AddedDirs []string `json:"added_dirs"`
}

type Input struct {
	CWD     string `json:"cwd"`
	Version string `json:"version"`
	Model   struct {
		DisplayName string `json:"display_name"`
	} `json:"model"`
	ContextWindow *ContextWindow `json:"context_window"`
	Workspace     *Workspace     `json:"workspace"`
}

// ============================================================================
// GIT INFO
// ============================================================================

type GitInfo struct {
	Branch   string
	RepoName string
	Tag      string
	Mod      int
	Add      int
	Del      int
	Ren      int
	Ahead    int
	Behind   int
	Conflict int
}
