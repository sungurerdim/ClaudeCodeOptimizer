package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

const repo = "sungurerdim/ClaudeCodeOptimizer"

var httpClient = &http.Client{Timeout: 30 * time.Second}

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

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "install":
		runInstall()
	case "uninstall":
		runUninstall()
	case "version":
		runVersion()
	default:
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println("CCO — Claude Code Optimizer")
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Println("  cco install     Install or update CCO")
	fmt.Println("  cco uninstall   Remove CCO files")
	fmt.Println("  cco version     Show installed version")
}

func claudeDir() string {
	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: cannot determine home directory: %v\n", err)
		os.Exit(1)
	}
	return filepath.Join(home, ".claude")
}

func resolveLatestTag() string {
	url := fmt.Sprintf("https://api.github.com/repos/%s/tags?per_page=1", repo)
	resp, err := httpClient.Get(url)
	if err != nil {
		return "main"
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return "main"
	}

	var tags []struct {
		Name string `json:"name"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&tags); err != nil || len(tags) == 0 {
		return "main"
	}
	return tags[0].Name
}

func downloadFile(baseURL, path string) (string, error) {
	url := fmt.Sprintf("%s/%s", baseURL, path)
	resp, err := httpClient.Get(url)
	if err != nil {
		return "", fmt.Errorf("download failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("HTTP %d for %s", resp.StatusCode, path)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("read failed: %w", err)
	}

	content := string(body)
	if !strings.HasPrefix(content, "---") {
		return "", fmt.Errorf("invalid content (not a CCO file)")
	}

	return content, nil
}

func writeFile(base, path, content string) error {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	dir := filepath.Dir(fullPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("mkdir failed: %w", err)
	}
	return os.WriteFile(fullPath, []byte(content), 0644)
}

func removeIfExists(base, path string) bool {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	if _, err := os.Stat(fullPath); err == nil {
		if err := os.Remove(fullPath); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to remove %s: %v\n", path, err)
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

func extractVersion(content string) string {
	for _, line := range strings.Split(content, "\n") {
		if strings.HasPrefix(line, "cco_version:") {
			v := strings.TrimSpace(strings.TrimPrefix(line, "cco_version:"))
			if idx := strings.Index(v, "#"); idx > 0 {
				v = strings.TrimSpace(v[:idx])
			}
			return v
		}
	}
	return ""
}

func runInstall() {
	base := claudeDir()

	fmt.Println("CCO Installer")
	fmt.Println("=============")

	// Detect currently installed version
	currentVersion := ""
	if content, err := os.ReadFile(filepath.Join(base, "rules", "cco-rules.md")); err == nil {
		currentVersion = extractVersion(string(content))
	}

	// Resolve latest release tag
	ref := resolveLatestTag()
	if ref == "main" {
		fmt.Println("Channel: stable (main — no tags found)")
	} else {
		fmt.Printf("Channel: stable (%s)\n", ref)
	}

	baseURL := fmt.Sprintf("https://raw.githubusercontent.com/%s/%s", repo, ref)

	// Source verification
	fmt.Println()
	fmt.Println("Verifying source...")
	testContent, err := downloadFile(baseURL, "rules/cco-rules.md")
	if err != nil {
		fmt.Fprintf(os.Stderr, "  Source verification failed: %s does not contain CCO files.\n", ref)
		fmt.Fprintf(os.Stderr, "  Check the repository for updates: https://github.com/%s\n", repo)
		os.Exit(1)
	}

	newVersion := extractVersion(testContent)
	fmt.Printf("  Source verified (%s)\n", ref)

	// Show version info
	if currentVersion != "" && newVersion != "" {
		if currentVersion == newVersion {
			fmt.Printf("  Version: v%s (already up to date)\n", currentVersion)
		} else {
			fmt.Printf("  Update: v%s → v%s\n", currentVersion, newVersion)
		}
	} else if currentVersion != "" {
		fmt.Printf("  Installed: v%s\n", currentVersion)
	} else if newVersion != "" {
		fmt.Printf("  Version: v%s (fresh install)\n", newVersion)
	}

	// Download and install all files
	type installFile struct {
		path  string
		group string
	}

	failed := 0
	var allFiles []installFile

	for _, f := range rulesFiles {
		allFiles = append(allFiles, installFile{f, "rules"})
	}
	for _, f := range skillFiles {
		allFiles = append(allFiles, installFile{f, "skills"})
	}
	for _, f := range agentFiles {
		allFiles = append(allFiles, installFile{f, "agents"})
	}

	// Critical files that must succeed for a valid installation
	criticalFiles := map[string]bool{
		"rules/cco-rules.md": true,
	}

	currentGroup := ""
	for _, f := range allFiles {
		if f.group != currentGroup {
			fmt.Println()
			fmt.Printf("Installing %s...\n", f.group)
			currentGroup = f.group
		}

		content, err := downloadFile(baseURL, f.path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "  ! %s (%v)\n", f.path, err)
			if criticalFiles[f.path] {
				fmt.Fprintf(os.Stderr, "\nCritical file failed. Installation aborted.\n")
				os.Exit(1)
			}
			failed++
			continue
		}

		if err := writeFile(base, f.path, content); err != nil {
			fmt.Fprintf(os.Stderr, "  ! %s (%v)\n", f.path, err)
			if criticalFiles[f.path] {
				fmt.Fprintf(os.Stderr, "\nCritical file write failed. Installation aborted.\n")
				os.Exit(1)
			}
			failed++
			continue
		}

		fmt.Printf("  + %s\n", f.path)
	}

	// Legacy cleanup
	legacyRemoved := cleanupLegacy(base)

	// Update timestamp
	updateTimestamp(base)

	// Summary
	fmt.Println()
	if failed == 0 {
		if currentVersion != "" && newVersion != "" && currentVersion != newVersion {
			fmt.Printf("CCO updated successfully! (v%s → v%s)\n", currentVersion, newVersion)
		} else {
			fmt.Printf("CCO installed successfully! (%s)\n", ref)
		}
		fmt.Println()
		fmt.Printf("Installed to: %s%c\n", base, filepath.Separator)
		fmt.Println("  rules/cco-rules.md")
		fmt.Println("  skills/cco-*/SKILL.md (8 skills)")
		fmt.Println("  agents/cco-agent-*.md (3 agents)")
		if len(legacyRemoved) > 0 {
			fmt.Println()
			fmt.Printf("Cleaned up %d legacy file(s) from previous CCO version:\n", len(legacyRemoved))
			for _, item := range legacyRemoved {
				fmt.Printf("  - %s\n", item)
			}
		}
		ensurePATH()
		fmt.Println()
		fmt.Println("Restart Claude Code to activate.")
		fmt.Println()
		fmt.Println("Quick Start:")
		fmt.Println("  /cco-blueprint  — Create a project profile")
		fmt.Println("  /cco-align      — Architecture gap analysis")
		fmt.Println("  /cco-optimize   — Scan and fix issues")
	} else {
		fmt.Fprintf(os.Stderr, "Installation completed with %d error(s).\n", failed)
		fmt.Fprintf(os.Stderr, "Re-run the installer or download files manually.\n")
		os.Exit(1)
	}
}

func ensurePATH() {
	exe, err := os.Executable()
	if err != nil {
		return
	}
	binDir := filepath.Dir(exe)

	// Check if binary's directory is already in PATH
	pathEnv := os.Getenv("PATH")
	sep := string(os.PathListSeparator)
	for _, dir := range strings.Split(pathEnv, sep) {
		if filepath.Clean(dir) == filepath.Clean(binDir) {
			return
		}
	}

	fmt.Println()
	if runtime.GOOS == "windows" {
		// Add to user PATH via setx
		cmd := exec.Command("setx", "PATH", binDir+sep+"%PATH%")
		if err := cmd.Run(); err != nil {
			fmt.Printf("Add this to your PATH: %s\n", binDir)
			return
		}
		fmt.Printf("Added %s to user PATH (restart your terminal to use 'cco' directly).\n", binDir)
	} else {
		fmt.Printf("Add this to your shell profile to use 'cco' directly:\n")
		fmt.Printf("  export PATH=\"%s:$PATH\"\n", binDir)
	}
}

func cleanupLegacy(base string) []string {
	var removed []string

	// v1.x pip cleanup (best-effort, skip if pip not available)
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
	cmdDir := filepath.Join(base, "commands")
	if entries, err := os.ReadDir(cmdDir); err == nil {
		for _, e := range entries {
			if strings.HasPrefix(e.Name(), "cco-") && strings.HasSuffix(e.Name(), ".md") {
				path := "commands/" + e.Name()
				if removeIfExists(base, path) {
					removed = append(removed, path)
				}
			}
		}
	}

	// Any cco-*.md in agents/ that isn't current
	currentAgents := map[string]bool{
		"cco-agent-analyze.md":  true,
		"cco-agent-apply.md":    true,
		"cco-agent-research.md": true,
	}
	agentDir := filepath.Join(base, "agents")
	if entries, err := os.ReadDir(agentDir); err == nil {
		for _, e := range entries {
			if strings.HasPrefix(e.Name(), "cco-") && strings.HasSuffix(e.Name(), ".md") && !currentAgents[e.Name()] {
				path := "agents/" + e.Name()
				if removeIfExists(base, path) {
					removed = append(removed, path)
				}
			}
		}
	}

	// Any cco-*.md in rules/ that isn't cco-rules.md
	rulesDir := filepath.Join(base, "rules")
	if entries, err := os.ReadDir(rulesDir); err == nil {
		for _, e := range entries {
			if strings.HasPrefix(e.Name(), "cco-") && strings.HasSuffix(e.Name(), ".md") && e.Name() != "cco-rules.md" {
				path := "rules/" + e.Name()
				if removeIfExists(base, path) {
					removed = append(removed, path)
				}
			}
		}
	}

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
	skillsDir := filepath.Join(base, "skills")
	if entries, err := os.ReadDir(skillsDir); err == nil {
		for _, e := range entries {
			name := e.Name()
			if e.IsDir() && strings.HasPrefix(name, "cco-") && !currentSkills[name] {
				path := "skills/" + name
				if removeDirIfExists(base, path) {
					removed = append(removed, path+"/")
				}
			}
			// v2 plugin symlinks: cco:*.md files (not directories)
			if !e.IsDir() && strings.HasPrefix(name, "cco:") && strings.HasSuffix(name, ".md") {
				fullPath := filepath.Join(skillsDir, name)
				if err := os.Remove(fullPath); err != nil {
					fmt.Fprintf(os.Stderr, "Warning: failed to remove %s: %v\n", "skills/"+name, err)
				}
				removed = append(removed, "skills/"+name)
			}
		}
	}

	return removed
}

func updateTimestamp(base string) {
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")
	content, err := os.ReadFile(rulesPath)
	if err != nil {
		return
	}

	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")
	lines := strings.Split(string(content), "\n")
	for i, line := range lines {
		if strings.HasPrefix(line, "last_update_check:") {
			lines[i] = "last_update_check: " + timestamp
			break
		}
	}

	if err := os.WriteFile(rulesPath, []byte(strings.Join(lines, "\n")), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: failed to update timestamp: %v\n", err)
	}
}

func runUninstall() {
	base := claudeDir()

	fmt.Println("CCO Uninstaller")
	fmt.Println("===============")
	fmt.Println()

	// Check if CCO is installed
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")
	if _, err := os.Stat(rulesPath); os.IsNotExist(err) {
		fmt.Println("CCO is not installed.")
		return
	}

	fmt.Print("Remove all CCO files? [y/N] ")
	var answer string
	_, _ = fmt.Scanln(&answer)

	if strings.ToLower(answer) == "y" {
		removeAll(base)
		return
	}

	// Per-group removal
	groups := []struct {
		name    string
		paths   []string
		isDirs  bool
		display string
	}{
		{"CCO rules", []string{"rules/cco-rules.md"}, false, "1 file"},
		{"CCO skills", nil, true, "8 skills"},
		{"CCO agents", []string{
			"agents/cco-agent-analyze.md",
			"agents/cco-agent-apply.md",
			"agents/cco-agent-research.md",
		}, false, "3 files"},
	}

	for _, g := range groups {
		fmt.Printf("Remove %s? (%s) [y/N] ", g.name, g.display)
		_, _ = fmt.Scanln(&answer)
		if strings.ToLower(answer) != "y" {
			continue
		}

		if g.name == "CCO skills" {
			skillsDir := filepath.Join(base, "skills")
			if entries, err := os.ReadDir(skillsDir); err == nil {
				for _, e := range entries {
					if e.IsDir() && strings.HasPrefix(e.Name(), "cco-") {
						os.RemoveAll(filepath.Join(skillsDir, e.Name()))
						fmt.Printf("  - skills/%s/\n", e.Name())
					}
				}
			}
		} else {
			for _, p := range g.paths {
				if removeIfExists(base, p) {
					fmt.Printf("  - %s\n", p)
				}
			}
		}
	}

	// Check for statusline
	statuslineBin := ""
	switch runtime.GOOS {
	case "windows":
		statuslineBin = filepath.Join(base, "statusline", "cco-statusline-windows-amd64.exe")
	default:
		statuslineBin = filepath.Join(base, "statusline", fmt.Sprintf("cco-statusline-%s-%s", runtime.GOOS, runtime.GOARCH))
	}
	if _, err := os.Stat(statuslineBin); err == nil {
		fmt.Print("Remove statusline binary? [y/N] ")
		_, _ = fmt.Scanln(&answer)
		if strings.ToLower(answer) == "y" {
			os.Remove(statuslineBin)
			fmt.Printf("  - %s\n", statuslineBin)
		}
	}

	fmt.Println()
	fmt.Println("Note: Remove CCO sections from project CLAUDE.md files manually.")
	fmt.Println("      Look for markers: cco-blueprint-start/end, CCO_ADAPTIVE_START/END,")
	fmt.Println("      CCO_CONTEXT_START/END, CCO_PRINCIPLES_START/END")
	fmt.Println()
	fmt.Println("CCO uninstalled. Restart Claude Code to apply changes.")
}

func removeAll(base string) {
	removeIfExists(base, "rules/cco-rules.md")

	// Remove all cco- skill directories
	skillsDir := filepath.Join(base, "skills")
	if entries, err := os.ReadDir(skillsDir); err == nil {
		for _, e := range entries {
			if e.IsDir() && strings.HasPrefix(e.Name(), "cco-") {
				os.RemoveAll(filepath.Join(skillsDir, e.Name()))
			}
		}
	}

	// Remove agent files
	for _, f := range agentFiles {
		removeIfExists(base, f)
	}

	// Also remove any legacy commands
	for _, f := range legacyV3Commands {
		removeIfExists(base, f)
	}

	fmt.Println("All CCO files removed.")
	fmt.Println()
	fmt.Println("Note: Remove CCO sections from project CLAUDE.md files manually.")
	fmt.Println("      Look for markers: cco-blueprint-start/end, CCO_ADAPTIVE_START/END,")
	fmt.Println("      CCO_CONTEXT_START/END, CCO_PRINCIPLES_START/END")
	fmt.Println()
	fmt.Println("CCO uninstalled. Restart Claude Code to apply changes.")
}

func runVersion() {
	base := claudeDir()
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")

	content, err := os.ReadFile(rulesPath)
	if err != nil {
		fmt.Println("CCO is not installed.")
		return
	}

	lines := strings.Split(string(content), "\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "cco_version:") {
			version := strings.TrimSpace(strings.TrimPrefix(line, "cco_version:"))
			// Remove inline comment
			if idx := strings.Index(version, "#"); idx > 0 {
				version = strings.TrimSpace(version[:idx])
			}
			fmt.Printf("CCO v%s\n", version)
			return
		}
	}

	fmt.Println("CCO installed (version unknown)")
}
