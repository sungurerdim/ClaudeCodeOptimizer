package main

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

// errUpToDate is a sentinel error indicating the installed version is current.
var errUpToDate = errors.New("already up to date")

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	var err error
	switch os.Args[1] {
	case "install":
		tag := ""
		if len(os.Args) >= 3 {
			tag = os.Args[2]
		}
		err = runInstall(tag)
	case "uninstall":
		err = runUninstall()
	case "version":
		err = runVersion()
	default:
		printUsage()
		os.Exit(1)
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
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

func runInstall(tag string) error {
	base, err := claudeDir()
	if err != nil {
		return err
	}

	stateFile := filepath.Join(base, ".cco-installing")
	checkStaleState(stateFile)
	if err := writeStateFile(stateFile); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: could not write state file: %v\n", err)
	}
	defer func() { _ = os.Remove(stateFile) }()

	fmt.Println("CCO Installer")
	fmt.Println("=============")

	info, err := resolveAndVerify(base, tag)
	if errors.Is(err, errUpToDate) {
		return nil
	}
	if err != nil {
		return err
	}

	failed, err := downloadAllFiles(base, info)
	if err != nil {
		return err
	}

	legacyRemoved := cleanupLegacy(base)
	printSummary(base, info, failed, legacyRemoved)

	if failed > 0 {
		return fmt.Errorf("installation completed with %d error(s). Re-run the installer or download files manually", failed)
	}
	return nil
}

// writeStateFile writes a state file with the current Unix timestamp.
func writeStateFile(path string) error {
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0750); err != nil {
		return err
	}
	content := fmt.Sprintf("%d", time.Now().Unix())
	return os.WriteFile(path, []byte(content), 0600)
}

// checkStaleState checks for an interrupted previous install and warns the user.
// State files older than 1 hour are considered stale and removed silently.
func checkStaleState(path string) {
	info, err := os.Stat(path)
	if err != nil {
		return
	}

	content, readErr := os.ReadFile(path) //nolint:gosec // G304: path constructed from home directory
	if readErr == nil {
		if ts, parseErr := strconv.ParseInt(strings.TrimSpace(string(content)), 10, 64); parseErr == nil {
			age := time.Since(time.Unix(ts, 0))
			if age > time.Hour {
				fmt.Printf("  Note: Found stale installation state (%s old). Cleaning up.\n", age.Truncate(time.Minute))
				_ = os.Remove(path)
				return
			}
		}
	}

	// Fallback: use file modification time if content parsing fails
	if time.Since(info.ModTime()) > time.Hour {
		fmt.Println("  Note: Found stale installation state. Cleaning up.")
		_ = os.Remove(path)
		return
	}

	fmt.Println("  Note: Previous installation may have been interrupted.")
	fmt.Println("  Proceeding with fresh install...")
	fmt.Println()
}

// detectCurrentVersion reads the installed cco-rules.md and extracts its version.
func detectCurrentVersion(base string) string {
	content, err := os.ReadFile(filepath.Join(base, "rules", "cco-rules.md")) //nolint:gosec // G304: path constructed from home directory
	if err != nil {
		return ""
	}
	return extractVersion(string(content))
}

// resolveChannel determines the git ref to download from.
func resolveChannel(tag string) string {
	if tag != "" {
		fmt.Printf("Channel: pinned (%s)\n", tag)
		return tag
	}
	ref := resolveLatestTag()
	if ref == "main" {
		fmt.Println("Channel: stable (main — no tags found)")
	} else {
		fmt.Printf("Channel: stable (%s)\n", ref)
	}
	return ref
}

// printVersionInfo displays version comparison information.
func printVersionInfo(current, new, tag string) {
	switch {
	case current != "" && new != "":
		switch {
		case current == new && tag == "":
			fmt.Printf("  Version: v%s (already up to date)\n", current)
		case current == new:
			fmt.Printf("  Version: v%s (reinstalling)\n", current)
		default:
			fmt.Printf("  Update: v%s → v%s\n", current, new)
		}
	case current != "":
		fmt.Printf("  Installed: v%s\n", current)
	case new != "":
		fmt.Printf("  Version: v%s (fresh install)\n", new)
	}
}

// resolveAndVerify resolves the release tag, downloads cco-rules.md for
// source verification, and compares versions. Returns errUpToDate if
// the installed version is already current and no action is needed.
func resolveAndVerify(base, tag string) (installInfo, error) {
	currentVersion := detectCurrentVersion(base)
	ref := resolveChannel(tag)
	baseURL := fmt.Sprintf("https://raw.githubusercontent.com/%s/%s", repo, ref)

	fmt.Println()
	fmt.Println("Verifying source...")
	testContent, err := downloadFile(baseURL, "rules/cco-rules.md")
	if err != nil {
		return installInfo{}, fmt.Errorf(
			"source verification failed: %s does not contain CCO files.\n"+
				"  Check the repository for updates: https://github.com/%s", ref, repo)
	}

	newVersion := extractVersion(testContent)
	fmt.Printf("  Source verified (%s)\n", ref)

	printVersionInfo(currentVersion, newVersion, tag)

	if currentVersion != "" && newVersion != "" && currentVersion == newVersion && tag == "" {
		fmt.Println()
		fmt.Println("Already up to date. Nothing to do.")
		return installInfo{}, errUpToDate
	}

	return installInfo{
		ref:            ref,
		baseURL:        baseURL,
		currentVersion: currentVersion,
		newVersion:     newVersion,
		testContent:    testContent,
	}, nil
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

// buildFileList constructs the complete list of files to install from manifests.
func buildFileList() []installFile {
	var files []installFile
	for _, f := range rulesFiles {
		files = append(files, installFile{f, "rules"})
	}
	for _, f := range skillFiles {
		files = append(files, installFile{f, "skills"})
	}
	for _, f := range agentFiles {
		files = append(files, installFile{f, "agents"})
	}
	return files
}

// downloadInParallel downloads files concurrently using a bounded semaphore.
// The already-verified rules/cco-rules.md is reused from the verification step.
func downloadInParallel(files []installFile, info installInfo) []downloadResult {
	results := make([]downloadResult, len(files))
	var wg sync.WaitGroup
	sem := make(chan struct{}, 10)

	for i, f := range files {
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
	return results
}

// writeResults writes downloaded content to disk and reports progress.
// Returns the count of non-critical failures and an error for critical failures.
func writeResults(base string, results []downloadResult, criticalFiles map[string]bool) (int, error) {
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
				return failed, fmt.Errorf("critical file failed: %s (%w)", r.path, r.err)
			}
			failed++
			continue
		}

		if err := writeFile(base, r.path, r.content); err != nil {
			fmt.Fprintf(os.Stderr, "  ! %s (%v)\n", r.path, err)
			if criticalFiles[r.path] {
				return failed, fmt.Errorf("critical file write failed: %s (%w)", r.path, err)
			}
			failed++
			continue
		}

		fmt.Printf("  + %s\n", r.path)
	}

	return failed, nil
}

// downloadAllFiles downloads all manifest files in parallel, writes them
// sequentially, and returns the count of non-critical failures.
// Returns an error only for critical file failures.
func downloadAllFiles(base string, info installInfo) (int, error) {
	files := buildFileList()

	criticalFiles := map[string]bool{
		"rules/cco-rules.md": true,
	}

	results := downloadInParallel(files, info)
	return writeResults(base, results, criticalFiles)
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
	}
}

func runUninstall() error {
	base, err := claudeDir()
	if err != nil {
		return err
	}

	fmt.Println("CCO Uninstaller")
	fmt.Println("===============")
	fmt.Println()

	rulesPath := filepath.Join(base, "rules", "cco-rules.md")
	if _, err := os.Stat(rulesPath); os.IsNotExist(err) {
		fmt.Println("CCO is not installed.")
		return nil
	}

	fmt.Print("Remove all CCO files? [y/N] ")
	var answer string
	if _, err := fmt.Scanln(&answer); err != nil {
		answer = "n"
	}

	if strings.ToLower(answer) == "y" {
		removeAll(base)
		return nil
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
	return nil
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

func runVersion() error {
	base, err := claudeDir()
	if err != nil {
		return err
	}
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")

	content, err := os.ReadFile(rulesPath) //nolint:gosec // G304: path constructed from home directory
	if err != nil {
		fmt.Println("CCO is not installed.")
		return nil
	}

	if version := extractVersion(string(content)); version != "" {
		fmt.Printf("CCO v%s\n", version)
	} else {
		fmt.Println("CCO installed (version unknown)")
	}
	return nil
}
