package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "install":
		tag := ""
		if len(os.Args) >= 3 {
			tag = os.Args[2]
		}
		runInstall(tag)
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
	fmt.Println("  cco install [tag]   Install or update CCO (optional: specific version tag)")
	fmt.Println("  cco uninstall       Remove CCO files")
	fmt.Println("  cco version         Show installed version")
}

func claudeDir() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("cannot determine home directory: %w", err)
	}
	return filepath.Join(home, ".claude"), nil
}

// installInfo holds resolved installation state from the verification phase.
type installInfo struct {
	ref            string
	baseURL        string
	currentVersion string
	newVersion     string
	testContent    string
}

func runInstall(tag string) {
	base, err := claudeDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	// State recovery: detect interrupted previous install
	stateFile := filepath.Join(base, ".cco-installing")
	if _, err := os.Stat(stateFile); err == nil {
		fmt.Println("  Note: Previous installation may have been interrupted.")
		fmt.Println("  Proceeding with fresh install...")
		fmt.Println()
	}
	if err := os.WriteFile(stateFile, []byte("installing"), 0600); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: could not write state file: %v\n", err)
	}
	defer func() { _ = os.Remove(stateFile) }()

	fmt.Println("CCO Installer")
	fmt.Println("=============")

	info, ok := resolveAndVerify(base, tag)
	if !ok {
		return
	}

	failed := downloadAllFiles(base, info)

	legacyRemoved := cleanupLegacy(base)

	printSummary(base, info, failed, legacyRemoved)
}

// resolveAndVerify resolves the release tag, downloads cco-rules.md for
// source verification, and compares versions. Returns (info, false) if
// the installed version is already up to date and no action is needed.
func resolveAndVerify(base, tag string) (installInfo, bool) {
	// Detect currently installed version
	currentVersion := ""
	if content, err := os.ReadFile(filepath.Join(base, "rules", "cco-rules.md")); err == nil {
		currentVersion = extractVersion(string(content))
	}

	// Resolve release tag
	var ref string
	if tag != "" {
		ref = tag
		fmt.Printf("Channel: pinned (%s)\n", ref)
	} else {
		ref = resolveLatestTag()
		if ref == "main" {
			fmt.Println("Channel: stable (main — no tags found)")
		} else {
			fmt.Printf("Channel: stable (%s)\n", ref)
		}
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
		if currentVersion == newVersion && tag == "" {
			fmt.Printf("  Version: v%s (already up to date)\n", currentVersion)
			fmt.Println()
			fmt.Println("Already up to date. Nothing to do.")
			return installInfo{}, false
		} else if currentVersion == newVersion {
			fmt.Printf("  Version: v%s (reinstalling)\n", currentVersion)
		} else {
			fmt.Printf("  Update: v%s → v%s\n", currentVersion, newVersion)
		}
	} else if currentVersion != "" {
		fmt.Printf("  Installed: v%s\n", currentVersion)
	} else if newVersion != "" {
		fmt.Printf("  Version: v%s (fresh install)\n", newVersion)
	}

	return installInfo{
		ref:            ref,
		baseURL:        baseURL,
		currentVersion: currentVersion,
		newVersion:     newVersion,
		testContent:    testContent,
	}, true
}

// installFile represents a file to download and install, with its manifest group.
type installFile struct {
	path  string
	group string
}

// downloadResult holds the outcome of a single file download.
type downloadResult struct {
	path    string
	group   string
	content string
	err     error
}

// downloadAllFiles downloads all manifest files in parallel, writes them
// sequentially, and returns the count of non-critical failures.
func downloadAllFiles(base string, info installInfo) int {
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

	// Download all files in parallel
	results := make([]downloadResult, len(allFiles))
	var wg sync.WaitGroup
	sem := make(chan struct{}, 10)

	for i, f := range allFiles {
		// Reuse already-downloaded content from verification step
		if f.path == "rules/cco-rules.md" {
			results[i] = downloadResult{path: f.path, group: f.group, content: info.testContent}
			continue
		}
		wg.Add(1)
		go func(idx int, file installFile) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()
			content, dlErr := downloadFile(info.baseURL, file.path)
			results[idx] = downloadResult{path: file.path, group: file.group, content: content, err: dlErr}
		}(i, f)
	}

	wg.Wait()

	// Write files and print output sequentially
	failed := 0
	currentGroup := ""
	for _, r := range results {
		if r.group != currentGroup {
			fmt.Println()
			fmt.Printf("Installing %s...\n", r.group)
			currentGroup = r.group
		}

		if r.err != nil {
			fmt.Fprintf(os.Stderr, "  ! %s (%v)\n", r.path, r.err)
			if criticalFiles[r.path] {
				fmt.Fprintf(os.Stderr, "\nCritical file failed. Installation aborted.\n")
				os.Exit(1)
			}
			failed++
			continue
		}

		if err := writeFile(base, r.path, r.content); err != nil {
			fmt.Fprintf(os.Stderr, "  ! %s (%v)\n", r.path, err)
			if criticalFiles[r.path] {
				fmt.Fprintf(os.Stderr, "\nCritical file write failed. Installation aborted.\n")
				os.Exit(1)
			}
			failed++
			continue
		}

		fmt.Printf("  + %s\n", r.path)
	}

	return failed
}

// printSummary outputs the installation result and next steps.
func printSummary(base string, info installInfo, failed int, legacyRemoved []string) {
	fmt.Println()
	if failed == 0 {
		if info.currentVersion != "" && info.newVersion != "" && info.currentVersion != info.newVersion {
			fmt.Printf("CCO updated successfully! (v%s → v%s)\n", info.currentVersion, info.newVersion)
		} else {
			fmt.Printf("CCO installed successfully! (%s)\n", info.ref)
		}
		fmt.Println()
		fmt.Printf("Installed to: %s%c\n", base, filepath.Separator)
		fmt.Println("  rules/cco-rules.md")
		fmt.Printf("  skills/cco-*/SKILL.md (%d skills)\n", len(skillFiles))
		fmt.Printf("  agents/cco-agent-*.md (%d agents)\n", len(agentFiles))
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
	base, err := claudeDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

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
		{"CCO skills", nil, true, fmt.Sprintf("%d skills", len(skillFiles))},
		{"CCO agents", agentFiles, false, fmt.Sprintf("%d files", len(agentFiles))},
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
	base, err := claudeDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")

	content, err := os.ReadFile(rulesPath)
	if err != nil {
		fmt.Println("CCO is not installed.")
		return
	}

	if version := extractVersion(string(content)); version != "" {
		fmt.Printf("CCO v%s\n", version)
	} else {
		fmt.Println("CCO installed (version unknown)")
	}
}
