package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

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

func runInstall() {
	base := claudeDir()

	// State recovery: detect interrupted previous install
	stateFile := filepath.Join(base, ".cco-installing")
	if _, err := os.Stat(stateFile); err == nil {
		fmt.Println("  Note: Previous installation may have been interrupted.")
		fmt.Println("  Proceeding with fresh install...")
		fmt.Println()
	}
	_ = os.WriteFile(stateFile, []byte("installing"), 0644)
	defer func() { _ = os.Remove(stateFile) }()

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
	if _, err := fmt.Scanln(&answer); err != nil {
		answer = "n"
	}

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
		if _, err := fmt.Scanln(&answer); err != nil {
			answer = "n"
		}
		if strings.ToLower(answer) != "y" {
			continue
		}

		if g.name == "CCO skills" {
			for _, p := range removeDirEntries(
				filepath.Join(base, "skills"), "skills/",
				func(e os.DirEntry) bool { return e.IsDir() && strings.HasPrefix(e.Name(), "cco-") },
			) {
				fmt.Printf("  - %s\n", p)
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
		if _, err := fmt.Scanln(&answer); err != nil {
			answer = "n"
		}
		if strings.ToLower(answer) == "y" {
			if err := os.Remove(statuslineBin); err != nil {
				fmt.Fprintf(os.Stderr, "  ! Warning: could not remove %s: %v\n", statuslineBin, err)
			}
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
	removeDirEntries(
		filepath.Join(base, "skills"), "skills/",
		func(e os.DirEntry) bool { return e.IsDir() && strings.HasPrefix(e.Name(), "cco-") },
	)

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
