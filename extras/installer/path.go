package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
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
		fmt.Printf("Add this directory to your PATH to use 'cco' directly:\n")
		fmt.Printf("  %s\n", binDir)
		fmt.Println()
		fmt.Println("PowerShell (run as admin):")
		fmt.Printf("  [Environment]::SetEnvironmentVariable('PATH', '%s;' + [Environment]::GetEnvironmentVariable('PATH', 'User'), 'User')\n", binDir)
	} else {
		fmt.Printf("Add this to your shell profile to use 'cco' directly:\n")
		fmt.Printf("  export PATH=\"%s:$PATH\"\n", binDir)
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
