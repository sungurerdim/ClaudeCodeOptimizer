package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

func ensurePATH() {
	exe, err := os.Executable()
	if err != nil {
		return
	}
	binDir := filepath.Dir(exe)

	// Check if binary's directory is already in PATH
	pathEnv := os.Getenv("PATH")
	sep := string(os.PathListSeparator)
	cleanBinDir := filepath.Clean(binDir)
	for _, dir := range strings.Split(pathEnv, sep) {
		if filepath.Clean(dir) == cleanBinDir {
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

func updateTimestamp(base string) {
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")
	raw, err := os.ReadFile(rulesPath)
	if err != nil {
		return
	}

	content := string(raw)
	const prefix = "last_update_check: "
	idx := strings.Index(content, prefix)
	if idx == -1 {
		return
	}

	// Find the end of the existing timestamp line
	start := idx + len(prefix)
	end := strings.IndexByte(content[start:], '\n')
	var oldLine string
	if end == -1 {
		oldLine = content[idx:]
	} else {
		oldLine = content[idx : start+end]
	}

	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")
	newLine := prefix + timestamp
	updated := strings.Replace(content, oldLine, newLine, 1)

	if err := os.WriteFile(rulesPath, []byte(updated), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: failed to update timestamp: %v\n", err)
	}
}

func extractVersion(content string) string {
	idx := strings.Index(content, "cco_version: ")
	if idx == -1 {
		return ""
	}
	start := idx + len("cco_version: ")
	end := strings.IndexByte(content[start:], '\n')
	var v string
	if end == -1 {
		v = content[start:]
	} else {
		v = content[start : start+end]
	}
	if ci := strings.Index(v, "#"); ci > 0 {
		v = strings.TrimSpace(v[:ci])
	}
	return strings.TrimSpace(v)
}
