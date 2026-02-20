package main

import (
	"fmt"
	"os/user"
	"path/filepath"
	"strconv"
	"strings"
)

// buildLocationRow returns row 1: repo:branch + optional tag, or project name if no git.
func buildLocationRow(input *Input, git *GitInfo) []string {
	var repoDisplay string
	if git != nil {
		repoDisplay = git.RepoName + ":" + git.Branch
	} else {
		repoDisplay = filepath.Base(input.CWD)
	}
	row := []string{c(repoDisplay, green)}
	if git != nil && git.Tag != "" {
		row = append(row, c(git.Tag, cyan))
	}
	return row
}

// changePart formats a label+count pair, highlighting non-zero counts with the given style.
func changePart(label string, count int, style string) string {
	if count > 0 {
		return c(fmt.Sprintf("%s %d", label, count), style)
	}
	return c(fmt.Sprintf("%s 0", label), gray)
}

// buildStatusRow returns row 2: ahead/behind + file change counts, or "No git".
func buildStatusRow(git *GitInfo) []string {
	if git == nil {
		return []string{c("No git", gray)}
	}

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

	return []string{
		alertStr,
		changePart("mod", git.Mod, yellow),
		changePart("add", git.Add, green),
		changePart("del", git.Del, red),
		changePart("mv", git.Ren, cyan),
	}
}

// buildWorkspaceRow returns row 4: added directories via /add-dir, or nil if none.
func buildWorkspaceRow(input *Input) []string {
	if input.Workspace == nil || len(input.Workspace.AddedDirs) == 0 {
		return nil
	}
	parts := make([]string, len(input.Workspace.AddedDirs))
	for i, dir := range input.Workspace.AddedDirs {
		parts[i] = c(abbreviateDir(dir, input.CWD), cyan)
	}
	parts[0] = c("+", green) + " " + parts[0]
	return parts
}

// buildSessionRow returns row 3: username + CC version + model + context usage.
func buildSessionRow(input *Input) []string {
	username := "user"
	if u, err := user.Current(); err == nil && u.Username != "" {
		// On Windows, user.Current() returns DOMAIN\user
		parts := strings.Split(u.Username, `\`)
		username = parts[len(parts)-1]
	}

	versionStr := c("CC ?", gray)
	if input.Version != "" {
		versionStr = c("CC "+input.Version, yellow)
	}

	row := []string{
		c(username, cyan),
		versionStr,
		c(formatModelName(input.Model.DisplayName), magenta),
	}
	if ctx := formatContextUsage(input); ctx != "" {
		row = append(row, c(ctx, cyan))
	}
	return row
}
