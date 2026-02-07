package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
	"unicode/utf8"
)

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

type Input struct {
	CWD     string `json:"cwd"`
	Version string `json:"version"`
	Model   struct {
		DisplayName string `json:"display_name"`
	} `json:"model"`
	ContextWindow *struct {
		ContextWindowSize int64 `json:"context_window_size"`
		TotalInputTokens  int64 `json:"total_input_tokens"`
		CurrentUsage      *struct {
			InputTokens              int64 `json:"input_tokens"`
			CacheCreationInputTokens int64 `json:"cache_creation_input_tokens"`
			CacheReadInputTokens     int64 `json:"cache_read_input_tokens"`
		} `json:"current_usage"`
	} `json:"context_window"`
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

func execGit(args ...string) (string, bool) {
	timeout := 1500 * time.Millisecond
	cmd := exec.Command("git", args...)
	cmd.Stderr = nil

	done := make(chan struct{})
	var out []byte
	var err error

	go func() {
		out, err = cmd.Output()
		close(done)
	}()

	select {
	case <-done:
		if err != nil {
			return "", false
		}
		return strings.TrimRight(string(out), "\n"), true
	case <-time.After(timeout):
		if cmd.Process != nil {
			cmd.Process.Kill()
		}
		return "", false
	}
}

func getGitInfo() *GitInfo {
	// Run git status and tag lookup in parallel
	var wg sync.WaitGroup
	var statusOut, tagOut string
	var statusOk, tagOk bool
	var repoRoot string
	var rootOk bool

	wg.Add(3)

	go func() {
		defer wg.Done()
		statusOut, statusOk = execGit("status", "--porcelain=v2", "-b")
	}()

	go func() {
		defer wg.Done()
		tagOut, tagOk = execGit("for-each-ref", "--sort=-v:refname", "--count=1", "--format=%(refname:short)", "refs/tags/")
	}()

	go func() {
		defer wg.Done()
		repoRoot, rootOk = execGit("rev-parse", "--show-toplevel")
	}()

	wg.Wait()

	if !statusOk {
		return nil
	}

	info := &GitInfo{}

	if rootOk {
		info.RepoName = filepath.Base(repoRoot)
	}
	if tagOk && tagOut != "" {
		info.Tag = tagOut
	}

	// Parse git status --porcelain=v2 -b
	for _, line := range strings.Split(statusOut, "\n") {
		if len(line) == 0 {
			continue
		}

		if strings.HasPrefix(line, "# branch.head ") {
			info.Branch = line[14:]
		} else if strings.HasPrefix(line, "# branch.ab ") {
			parts := strings.Fields(line)
			for _, p := range parts {
				if strings.HasPrefix(p, "+") {
					info.Ahead, _ = strconv.Atoi(p[1:])
				} else if strings.HasPrefix(p, "-") {
					info.Behind, _ = strconv.Atoi(p[1:])
				}
			}
		} else if strings.HasPrefix(line, "u ") {
			info.Conflict++
		} else if strings.HasPrefix(line, "1 ") || strings.HasPrefix(line, "2 ") {
			if len(line) < 4 {
				continue
			}
			idx := line[2]
			wt := line[3]

			// Working tree changes
			if wt == 'M' {
				info.Mod++
			}
			if wt == 'D' {
				info.Del++
			}

			// Staged changes (counted into same totals)
			if idx == 'M' {
				info.Mod++
			}
			if idx == 'A' || idx == 'C' {
				info.Add++
			}
			if idx == 'D' {
				info.Del++
			}
			if idx == 'R' {
				info.Ren++
			}
		} else if strings.HasPrefix(line, "? ") {
			info.Add++
		}
	}

	if info.Branch == "" {
		return nil
	}

	return info
}

// ============================================================================
// FORMATTING
// ============================================================================

func formatModelName(name string) string {
	name = strings.TrimPrefix(name, "Claude ")
	if name == "" {
		return "Unknown"
	}
	return name
}

func formatK(n int64) string {
	if n >= 1000 {
		return strconv.FormatInt((n+500)/1000, 10) + "K"
	}
	return strconv.FormatInt(n, 10)
}

func formatContextUsage(input *Input) string {
	cw := input.ContextWindow
	if cw == nil || cw.ContextWindowSize == 0 {
		return ""
	}

	var tokens int64
	if cw.CurrentUsage != nil {
		tokens = cw.CurrentUsage.InputTokens +
			cw.CurrentUsage.CacheCreationInputTokens +
			cw.CurrentUsage.CacheReadInputTokens
	} else {
		tokens = cw.TotalInputTokens
	}

	percent := tokens * 100 / cw.ContextWindowSize
	return fmt.Sprintf("%s %d%%", formatK(tokens), percent)
}

// visibleLen returns the display width of a string, excluding ANSI escape codes
func visibleLen(s string) int {
	inEsc := false
	n := 0
	for i := 0; i < len(s); {
		if s[i] == '\x1b' {
			inEsc = true
			i++
			continue
		}
		if inEsc {
			if s[i] == 'm' {
				inEsc = false
			}
			i++
			continue
		}
		_, size := utf8.DecodeRuneInString(s[i:])
		n++
		i += size
	}
	return n
}

// justifyRow distributes parts evenly across targetWidth with separator
func justifyRow(parts []string, targetWidth int, sep string) string {
	if len(parts) == 0 {
		return ""
	}
	if len(parts) == 1 {
		return parts[0]
	}

	gaps := len(parts) - 1
	contentWidth := 0
	for _, p := range parts {
		contentWidth += visibleLen(p)
	}
	sepWidth := gaps // each separator is 1 visible char
	available := targetWidth - contentWidth - sepWidth
	if available < 0 {
		available = 0
	}

	perGap := available / gaps
	extra := available % gaps

	var buf bytes.Buffer
	buf.WriteString(parts[0])

	for i := 1; i < len(parts); i++ {
		gap := perGap
		if i <= extra {
			gap++
		}
		left := gap / 2
		right := gap - left
		for j := 0; j < left; j++ {
			buf.WriteByte(' ')
		}
		buf.WriteString(c(sep, gray))
		for j := 0; j < right; j++ {
			buf.WriteByte(' ')
		}
		buf.WriteString(parts[i])
	}

	return buf.String()
}

func minRowWidth(parts []string) int {
	w := 0
	for _, p := range parts {
		w += visibleLen(p)
	}
	// " · " = 3 chars between each part
	return w + (len(parts)-1)*3
}

// ============================================================================
// BUILD STATUSLINE
// ============================================================================

func buildStatusline(input *Input, git *GitInfo) string {
	// Username
	username := "user"
	if u, err := user.Current(); err == nil && u.Username != "" {
		// On Windows, user.Current() returns DOMAIN\user
		parts := strings.Split(u.Username, `\`)
		username = parts[len(parts)-1]
	}

	// Project name
	projectName := filepath.Base(input.CWD)

	// Model
	modelDisplay := formatModelName(input.Model.DisplayName)

	// Version (from stdin JSON, no process spawn needed)
	ccVersion := input.Version

	// Context
	contextUsage := formatContextUsage(input)

	// --- Row 1: Location ---
	var repoDisplay string
	if git != nil {
		repoDisplay = git.RepoName + ":" + git.Branch
	} else {
		repoDisplay = projectName
	}
	row1 := []string{c(repoDisplay, green)}
	if git != nil && git.Tag != "" {
		row1 = append(row1, c(git.Tag, cyan))
	}

	// --- Row 2: Status ---
	var row2 []string
	if git == nil {
		row2 = []string{c("No git", gray)}
	} else {
		// Ahead/behind
		var aheadStr, behindStr string
		if git.Ahead > 0 {
			aheadStr = c("\u25B3 ", green) + c(strconv.Itoa(git.Ahead), white)
		} else {
			aheadStr = c("\u25B3 0", gray)
		}
		if git.Behind > 0 {
			behindStr = c("\u25BD ", yellow) + c(strconv.Itoa(git.Behind), white)
		} else {
			behindStr = c("\u25BD 0", gray)
		}
		alertStr := aheadStr + " " + behindStr
		if git.Conflict > 0 {
			alertStr += " " + c(fmt.Sprintf("%d conflict", git.Conflict), redBold)
		}

		// File changes
		changePart := func(label string, count int, style string) string {
			if count > 0 {
				return c(fmt.Sprintf("%s %d", label, count), style)
			}
			return c(fmt.Sprintf("%s 0", label), gray)
		}

		row2 = []string{
			alertStr,
			changePart("mod", git.Mod, yellow),
			changePart("add", git.Add, green),
			changePart("del", git.Del, red),
			changePart("mv", git.Ren, cyan),
		}
	}

	// --- Row 3: Session ---
	versionStr := c("CC ?", gray)
	if ccVersion != "" {
		versionStr = c("CC "+ccVersion, yellow)
	}

	row3 := []string{
		c(username, cyan),
		versionStr,
		c(modelDisplay, magenta),
	}
	if contextUsage != "" {
		row3 = append(row3, c(contextUsage, cyan))
	}

	// Calculate max width
	maxW := minRowWidth(row1)
	if w := minRowWidth(row2); w > maxW {
		maxW = w
	}
	if w := minRowWidth(row3); w > maxW {
		maxW = w
	}

	// Build output
	var out bytes.Buffer
	out.WriteString(justifyRow(row1, maxW, "\u00B7"))
	out.WriteByte('\n')
	out.WriteString(justifyRow(row2, maxW, "\u00B7"))
	out.WriteByte('\n')
	out.WriteString(justifyRow(row3, maxW, "\u00B7"))
	out.WriteByte('\n')
	out.WriteString("\u200B\n") // empty line with zero-width space

	return out.String()
}

// ============================================================================
// MAIN
// ============================================================================

func main() {
	data, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Printf("[Statusline Error: %v]\n", err)
		return
	}

	var input Input
	if err := json.Unmarshal(data, &input); err != nil {
		fmt.Printf("[Statusline Error: %v]\n", err)
		return
	}

	git := getGitInfo()
	fmt.Print(buildStatusline(&input, git))
}
