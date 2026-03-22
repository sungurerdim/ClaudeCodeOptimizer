package main

import (
	"context"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

// gitTimeout is the git command timeout, resolved once at init from
// CCO_GIT_TIMEOUT env var (default 5000ms, range 100-60000ms).
var gitTimeout = func() time.Duration {
	const (
		defaultTimeout = 5000
		minTimeout     = 100
		maxTimeout     = 60000
	)
	if envTimeout := os.Getenv("CCO_GIT_TIMEOUT"); envTimeout != "" {
		if t, err := strconv.Atoi(envTimeout); err == nil && t >= minTimeout && t <= maxTimeout {
			return time.Duration(t) * time.Millisecond
		}
	}
	return defaultTimeout * time.Millisecond
}()

func execGit(args ...string) (string, bool) {
	ctx, cancel := context.WithTimeout(context.Background(), gitTimeout)
	defer cancel()

	cmd := exec.CommandContext(ctx, "git", args...)
	out, err := cmd.Output()
	if err != nil {
		return "", false
	}
	return strings.TrimRight(string(out), "\n"), true
}

// parseGitStatus parses output from `git status --porcelain=v2 -b` into GitInfo fields.
// Format reference: https://git-scm.com/docs/git-status#_porcelain_format_version_2
func parseGitStatus(statusOut string, info *GitInfo) {
	for _, line := range strings.Split(statusOut, "\n") {
		if len(line) == 0 {
			continue
		}

		const branchHeadPrefix = "# branch.head "

		switch {
		case strings.HasPrefix(line, branchHeadPrefix):
			if len(line) > len(branchHeadPrefix) {
				info.Branch = line[len(branchHeadPrefix):]
			}
		// "# branch.ab +N -M" — ahead/behind counts
		case strings.HasPrefix(line, "# branch.ab "):
			parts := strings.Fields(line)
			// Validate format: expect exactly 4 fields ("#", "branch.ab", "+N", "-M")
			if len(parts) < 4 {
				continue
			}
			ab := parts[2:]
			hasAhead, hasBehind := false, false
			var ahead, behind int
			for _, p := range ab {
				if strings.HasPrefix(p, "+") {
					if v, err := strconv.Atoi(p[1:]); err == nil {
						ahead = v
						hasAhead = true
					}
				} else if strings.HasPrefix(p, "-") {
					if v, err := strconv.Atoi(p[1:]); err == nil {
						behind = v
						hasBehind = true
					}
				}
			}
			if hasAhead && hasBehind {
				info.Ahead = ahead
				info.Behind = behind
			}
		// "u ..." — unmerged (conflict) entry
		case strings.HasPrefix(line, "u "):
			info.Conflict++
		// "1 XY ..." — ordinary change; "2 XY ..." — rename/copy
		// Position 2 = index status, position 3 = working tree status
		case strings.HasPrefix(line, "1 "), strings.HasPrefix(line, "2 "):
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
		// "? <path>" — untracked file
		case strings.HasPrefix(line, "? "):
			info.Add++
		}
	}
}

// getGitInfo runs git commands in parallel and returns parsed info.
// Returns nil if git status fails or no branch is detected (e.g. not a git repo).
func getGitInfo() *GitInfo {
	var wg sync.WaitGroup
	var statusOut, tagOut string
	var statusOk, tagOk bool

	wg.Add(2)

	go func() {
		defer wg.Done()
		statusOut, statusOk = execGit("status", "--porcelain=v2", "-b")
	}()

	go func() {
		defer wg.Done()
		tagOut, tagOk = execGit("describe", "--tags", "--abbrev=0")
	}()

	wg.Wait()

	if !statusOk {
		return nil
	}

	info := &GitInfo{}
	if tagOk && tagOut != "" {
		info.Tag = tagOut
	}

	parseGitStatus(statusOut, info)

	if info.Branch == "" {
		return nil
	}

	return info
}
