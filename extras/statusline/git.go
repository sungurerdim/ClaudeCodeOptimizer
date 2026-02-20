package main

import (
	"context"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
)

func execGit(args ...string) (string, bool) {
	ctx, cancel := context.WithTimeout(context.Background(), 1500*time.Millisecond)
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

		// "# branch.head <name>" — current branch name (14 = len("# branch.head "))
		if strings.HasPrefix(line, "# branch.head ") {
			info.Branch = line[14:]
		} else if strings.HasPrefix(line, "# branch.ab ") {
			// "# branch.ab +N -M" — ahead/behind counts
			parts := strings.Fields(line)
			for _, p := range parts {
				if strings.HasPrefix(p, "+") {
					if v, err := strconv.Atoi(p[1:]); err == nil {
						info.Ahead = v
					}
				} else if strings.HasPrefix(p, "-") {
					if v, err := strconv.Atoi(p[1:]); err == nil {
						info.Behind = v
					}
				}
			}
		} else if strings.HasPrefix(line, "u ") {
			// "u ..." — unmerged (conflict) entry
			info.Conflict++
		} else if strings.HasPrefix(line, "1 ") || strings.HasPrefix(line, "2 ") {
			// "1 XY ..." — ordinary change; "2 XY ..." — rename/copy
			// Position 2 = index status, position 3 = working tree status
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
			// "? <path>" — untracked file
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

	parseGitStatus(statusOut, info)

	if info.Branch == "" {
		return nil
	}

	return info
}
