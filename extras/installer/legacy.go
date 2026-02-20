package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func isCCOMarkdown(name string) bool {
	return strings.HasPrefix(name, "cco-") && strings.HasSuffix(name, ".md")
}

// removeDirEntries reads dir and removes entries matching filter.
// For directories it uses os.RemoveAll; for files it uses os.Remove.
// Returns relative paths of removed entries (directories suffixed with "/").
// Errors are reported as warnings to stderr but do not stop processing.
func removeDirEntries(dir, prefix string, filter func(os.DirEntry) bool) []string {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return nil
	}
	var removed []string
	for _, e := range entries {
		if !filter(e) {
			continue
		}
		fullPath := filepath.Join(dir, e.Name())
		relPath := prefix + e.Name()
		if e.IsDir() {
			if err := os.RemoveAll(fullPath); err != nil {
				fmt.Fprintf(os.Stderr, "Warning: could not remove %s: %v\n", relPath, err)
				continue
			}
			removed = append(removed, relPath+"/")
		} else {
			if err := os.Remove(fullPath); err != nil {
				fmt.Fprintf(os.Stderr, "Warning: could not remove %s: %v\n", relPath, err)
				continue
			}
			removed = append(removed, relPath)
		}
	}
	return removed
}

func cleanupLegacy(base string) []string {
	var removed []string

	// v1.x pip cleanup (best-effort, skip if pip not available)
	// Deprecation: v1/v2 cleanup can be removed in v6+ (no active users expected).
	if pipPath, err := exec.LookPath("pip"); err == nil {
		// Check if package is actually installed before attempting uninstall
		checkCmd := exec.Command(pipPath, "show", "claudecodeoptimizer")
		if checkCmd.Run() == nil {
			cmd := exec.Command(pipPath, "uninstall", "claudecodeoptimizer", "-y")
			if err := cmd.Run(); err == nil {
				removed = append(removed, "pip:claudecodeoptimizer")
			}
		}
	}

	// v2.x plugin cleanup (best-effort, skip if claude not available)
	if claudePath, err := exec.LookPath("claude"); err == nil {
		cmd := exec.Command(claudePath, "plugin", "uninstall", "cco@ClaudeCodeOptimizer")
		_ = cmd.Run()
		cmd2 := exec.Command(claudePath, "plugin", "marketplace", "remove", "ClaudeCodeOptimizer")
		if err := cmd2.Run(); err == nil {
			removed = append(removed, "plugin:cco@ClaudeCodeOptimizer")
		}
	}

	// v3 legacy commands (migrated to skills/)
	for _, f := range legacyV3Commands {
		if removeIfExists(base, f) {
			removed = append(removed, f)
		}
	}

	// v2 legacy non-prefixed commands
	for _, f := range legacyV2Commands {
		if removeIfExists(base, f) {
			removed = append(removed, f)
		}
	}

	// Any remaining cco-*.md in commands/
	removed = append(removed, removeDirEntries(
		filepath.Join(base, "commands"), "commands/",
		func(e os.DirEntry) bool { return !e.IsDir() && isCCOMarkdown(e.Name()) },
	)...)

	// Any cco-*.md in agents/ that isn't current
	currentAgents := map[string]bool{
		"cco-agent-analyze.md":  true,
		"cco-agent-apply.md":    true,
		"cco-agent-research.md": true,
	}
	removed = append(removed, removeDirEntries(
		filepath.Join(base, "agents"), "agents/",
		func(e os.DirEntry) bool { return !e.IsDir() && isCCOMarkdown(e.Name()) && !currentAgents[e.Name()] },
	)...)

	// Any cco-*.md in rules/ that isn't cco-rules.md
	removed = append(removed, removeDirEntries(
		filepath.Join(base, "rules"), "rules/",
		func(e os.DirEntry) bool { return !e.IsDir() && isCCOMarkdown(e.Name()) && e.Name() != "cco-rules.md" },
	)...)

	// Legacy directories
	for _, d := range legacyDirs {
		if removeDirIfExists(base, d) {
			removed = append(removed, d+"/")
		}
	}

	// Stale skill directories and v2 plugin symlinks in skills/
	currentSkills := map[string]bool{
		"cco-optimize":  true,
		"cco-align":     true,
		"cco-commit":    true,
		"cco-research":  true,
		"cco-docs":      true,
		"cco-update":    true,
		"cco-blueprint": true,
		"cco-pr":        true,
	}
	removed = append(removed, removeDirEntries(
		filepath.Join(base, "skills"), "skills/",
		func(e os.DirEntry) bool {
			name := e.Name()
			// Stale cco- directories
			if e.IsDir() && strings.HasPrefix(name, "cco-") && !currentSkills[name] {
				return true
			}
			// v2 plugin symlinks: cco:*.md files
			if !e.IsDir() && strings.HasPrefix(name, "cco:") && strings.HasSuffix(name, ".md") {
				return true
			}
			return false
		},
	)...)

	return removed
}

func removeIfExists(base, path string) bool {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	if _, err := os.Stat(fullPath); err == nil {
		if err := os.Remove(fullPath); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to remove %s: %v\n", path, err)
			return false
		}
		return true
	}
	return false
}

func removeDirIfExists(base, path string) bool {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	if info, err := os.Stat(fullPath); err == nil && info.IsDir() {
		if err := os.RemoveAll(fullPath); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to remove directory %s: %v\n", path, err)
		}
		return true
	}
	return false
}
