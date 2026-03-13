package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
	"time"
)

func TestWriteFile(t *testing.T) {
	base := t.TempDir()

	t.Run("creates nested directories and writes file", func(t *testing.T) {
		err := writeFile(base, "a/b/c.md", "hello")
		if err != nil {
			t.Fatalf("writeFile failed: %v", err)
		}

		content, err := os.ReadFile(filepath.Join(base, "a", "b", "c.md")) //nolint:gosec // G304: test path
		if err != nil {
			t.Fatalf("read failed: %v", err)
		}
		if string(content) != "hello" {
			t.Errorf("got %q, want %q", string(content), "hello")
		}
	})

	t.Run("overwrites existing file", func(t *testing.T) {
		if err := writeFile(base, "a/b/c.md", "first"); err != nil {
			t.Fatal(err)
		}
		if err := writeFile(base, "a/b/c.md", "second"); err != nil {
			t.Fatal(err)
		}
		content, _ := os.ReadFile(filepath.Join(base, "a", "b", "c.md")) //nolint:gosec // G304: test path
		if string(content) != "second" {
			t.Errorf("got %q, want %q", string(content), "second")
		}
	})

	t.Run("no temp file remains after write", func(t *testing.T) {
		if err := writeFile(base, "atomic/test.md", "data"); err != nil {
			t.Fatal(err)
		}
		tmpPath := filepath.Join(base, "atomic", "test.md.tmp")
		if _, err := os.Stat(tmpPath); !os.IsNotExist(err) {
			t.Error("temp file should not remain after successful write")
		}
	})
}

func TestRemoveIfExists(t *testing.T) {
	base := t.TempDir()

	t.Run("removes existing file", func(t *testing.T) {
		path := "test.md"
		_ = os.WriteFile(filepath.Join(base, path), []byte("x"), 0600)

		removed := removeIfExists(base, path)
		if !removed {
			t.Error("expected true for existing file")
		}
		if _, err := os.Stat(filepath.Join(base, path)); !os.IsNotExist(err) {
			t.Error("file should not exist after removal")
		}
	})

	t.Run("returns false for non-existing file", func(t *testing.T) {
		removed := removeIfExists(base, "nonexistent.md")
		if removed {
			t.Error("expected false for non-existing file")
		}
	})
}

func TestRemoveDirIfExists(t *testing.T) {
	base := t.TempDir()

	t.Run("removes existing directory", func(t *testing.T) {
		dir := filepath.Join(base, "subdir")
		_ = os.MkdirAll(dir, 0750)
		_ = os.WriteFile(filepath.Join(dir, "file.txt"), []byte("x"), 0600)

		removed := removeDirIfExists(base, "subdir")
		if !removed {
			t.Error("expected true for existing directory")
		}
		if _, err := os.Stat(dir); !os.IsNotExist(err) {
			t.Error("directory should not exist after removal")
		}
	})

	t.Run("returns false for non-existing directory", func(t *testing.T) {
		removed := removeDirIfExists(base, "nonexistent")
		if removed {
			t.Error("expected false for non-existing directory")
		}
	})

	t.Run("returns false for file instead of directory", func(t *testing.T) {
		_ = os.WriteFile(filepath.Join(base, "file.txt"), []byte("x"), 0600)
		removed := removeDirIfExists(base, "file.txt")
		if removed {
			t.Error("expected false for file (not directory)")
		}
	})
}

func TestDownloadFile(t *testing.T) {
	originalBackoff := retryBackoff
	defer func() { retryBackoff = originalBackoff }()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	t.Run("successful download with valid content", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_, _ = fmt.Fprint(w, "---\nname: test\n---\n# Content")
		}))
		defer server.Close()

		content, err := downloadFile(server.URL, "test.md")
		if err != nil {
			t.Fatalf("downloadFile failed: %v", err)
		}
		if !strings.HasPrefix(content, "---") {
			t.Errorf("content should start with ---")
		}
	})

	t.Run("rejects non-200 status", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(404)
		}))
		defer server.Close()

		_, err := downloadFile(server.URL, "missing.md")
		if err == nil {
			t.Error("expected error for 404 response")
		}
	})

	t.Run("rejects invalid content without frontmatter", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_, _ = fmt.Fprint(w, "<html>Not a CCO file</html>")
		}))
		defer server.Close()

		_, err := downloadFile(server.URL, "bad.md")
		if err == nil {
			t.Error("expected error for non-CCO content")
		}
		if !strings.Contains(err.Error(), "missing YAML frontmatter") {
			t.Errorf("error should mention frontmatter validation, got: %v", err)
		}
	})

	t.Run("handles connection error", func(t *testing.T) {
		_, err := downloadFile("http://127.0.0.1:1", "test.md")
		if err == nil {
			t.Error("expected error for connection failure")
		}
	})

	t.Run("retries on 5xx and succeeds", func(t *testing.T) {
		attempts := 0
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			attempts++
			if attempts < 3 {
				w.WriteHeader(500)
				return
			}
			_, _ = fmt.Fprint(w, "---\ntest: true\n---\n# Content")
		}))
		defer server.Close()

		content, err := downloadFile(server.URL, "test.md")
		if err != nil {
			t.Fatalf("downloadFile should succeed after retries: %v", err)
		}
		if !strings.HasPrefix(content, "---") {
			t.Error("content should start with ---")
		}
		if attempts != 3 {
			t.Errorf("expected 3 attempts, got %d", attempts)
		}
	})

	t.Run("does not retry on 404", func(t *testing.T) {
		attempts := 0
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			attempts++
			w.WriteHeader(404)
		}))
		defer server.Close()

		_, err := downloadFile(server.URL, "missing.md")
		if err == nil {
			t.Error("expected error for 404")
		}
		if attempts != 1 {
			t.Errorf("should not retry 404, got %d attempts", attempts)
		}
	})

	t.Run("gives up after max retries", func(t *testing.T) {
		attempts := 0
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			attempts++
			w.WriteHeader(500)
		}))
		defer server.Close()

		_, err := downloadFile(server.URL, "fail.md")
		if err == nil {
			t.Error("expected error after max retries")
		}
		if attempts != 4 { // 1 initial + 3 retries
			t.Errorf("expected 4 attempts, got %d", attempts)
		}
	})
}

func TestResolveLatestTag(t *testing.T) {
	originalClient := httpClient
	originalBackoff := retryBackoff
	defer func() {
		httpClient = originalClient
		retryBackoff = originalBackoff
	}()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	t.Run("returns tag name on success", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_ = json.NewEncoder(w).Encode([]struct {
				Name string `json:"name"`
			}{{"v4.2.0"}})
		}))
		defer server.Close()

		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		tag := resolveLatestTag()
		if tag != "v4.2.0" {
			t.Errorf("got %q, want %q", tag, "v4.2.0")
		}
	})

	t.Run("falls back to main on empty tags", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_, _ = fmt.Fprint(w, "[]")
		}))
		defer server.Close()

		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		tag := resolveLatestTag()
		if tag != "main" {
			t.Errorf("got %q, want %q", tag, "main")
		}
	})

	t.Run("falls back to main on non-200", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(403)
		}))
		defer server.Close()

		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		tag := resolveLatestTag()
		if tag != "main" {
			t.Errorf("got %q, want %q", tag, "main")
		}
	})

	t.Run("falls back to main on connection error", func(t *testing.T) {
		httpClient = &http.Client{
			Timeout:   1 * time.Second,
			Transport: &rewriteTransport{base: "http://127.0.0.1:1"},
		}

		tag := resolveLatestTag()
		if tag != "main" {
			t.Errorf("got %q, want %q", tag, "main")
		}
	})
}

// rewriteTransport redirects all requests to a test server URL for testing with mocked GitHub API responses.
type rewriteTransport struct {
	base string
}

func (t *rewriteTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	req.URL.Scheme = "http"
	parsed, _ := http.NewRequest(req.Method, t.base+req.URL.Path+"?"+req.URL.RawQuery, req.Body)
	return http.DefaultTransport.RoundTrip(parsed)
}

func TestCleanupLegacy(t *testing.T) {
	t.Run("removes v3 legacy commands", func(t *testing.T) {
		base := t.TempDir()
		cmdDir := filepath.Join(base, "commands")
		_ = os.MkdirAll(cmdDir, 0750)

		for _, f := range legacyV3Commands {
			_ = os.WriteFile(filepath.Join(base, filepath.FromSlash(f)), []byte("x"), 0600)
		}

		removed := cleanupLegacy(base)

		for _, f := range legacyV3Commands {
			found := false
			for _, r := range removed {
				if r == f {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("expected %s in removed list", f)
			}
		}
	})

	t.Run("removes stale skill directories", func(t *testing.T) {
		base := t.TempDir()
		skillsDir := filepath.Join(base, "skills")

		// Create a current skill
		_ = os.MkdirAll(filepath.Join(skillsDir, "cco-optimize"), 0750)
		// Create a stale skill
		_ = os.MkdirAll(filepath.Join(skillsDir, "cco-oldskill"), 0750)

		removed := cleanupLegacy(base)

		staleFound := false
		for _, r := range removed {
			if r == "skills/cco-oldskill/" {
				staleFound = true
			}
		}
		if !staleFound {
			t.Error("expected stale skill cco-oldskill to be removed")
		}

		// Current skill should still exist
		if _, err := os.Stat(filepath.Join(skillsDir, "cco-optimize")); os.IsNotExist(err) {
			t.Error("current skill cco-optimize should not be removed")
		}
	})

	t.Run("removes stale agents", func(t *testing.T) {
		base := t.TempDir()
		agentDir := filepath.Join(base, "agents")
		_ = os.MkdirAll(agentDir, 0750)

		// Create a current agent
		_ = os.WriteFile(filepath.Join(agentDir, "cco-agent-analyze.md"), []byte("x"), 0600)
		// Create a stale agent
		_ = os.WriteFile(filepath.Join(agentDir, "cco-agent-old.md"), []byte("x"), 0600)

		removed := cleanupLegacy(base)

		staleFound := false
		for _, r := range removed {
			if r == "agents/cco-agent-old.md" {
				staleFound = true
			}
		}
		if !staleFound {
			t.Error("expected stale agent cco-agent-old.md to be removed")
		}

		// Current agent should still exist
		if _, err := os.Stat(filepath.Join(agentDir, "cco-agent-analyze.md")); os.IsNotExist(err) {
			t.Error("current agent cco-agent-analyze.md should not be removed")
		}
	})

	t.Run("removes legacy directories", func(t *testing.T) {
		base := t.TempDir()

		for _, d := range legacyDirs {
			_ = os.MkdirAll(filepath.Join(base, filepath.FromSlash(d)), 0750)
		}

		removed := cleanupLegacy(base)

		for _, d := range legacyDirs {
			found := false
			for _, r := range removed {
				if r == d+"/" {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("expected %s/ in removed list", d)
			}
		}
	})

	t.Run("returns empty on clean base", func(t *testing.T) {
		base := t.TempDir()
		removed := cleanupLegacy(base)
		if len(removed) != 0 {
			t.Errorf("expected no removals, got %d", len(removed))
		}
	})
}

func TestManifestConsistency(t *testing.T) {
	t.Run("skillFiles matches currentSkills map in cleanupLegacy", func(t *testing.T) {
		// Verify that skillFiles contains all expected skill entries.
		// cleanupLegacy now derives currentSkills from skillFiles directly,
		// so this test guards against accidental removal of a skill from the manifest.
		expectedSkills := map[string]bool{
			"cco-optimize":  true,
			"cco-align":     true,
			"cco-commit":    true,
			"cco-research":  true,
			"cco-docs":      true,
			"cco-update":    true,
			"cco-blueprint": true,
			"cco-pr":        true,
			"cco-repo":      true,
		}

		for _, f := range skillFiles {
			// Extract skill name from path like "skills/cco-optimize/SKILL.md"
			parts := strings.Split(f, "/")
			if len(parts) < 2 {
				t.Errorf("unexpected skill path format: %s", f)
				continue
			}
			name := parts[1]
			if !expectedSkills[name] {
				t.Errorf("skill %q in skillFiles but not in expected skills set", name)
			}
			delete(expectedSkills, name)
		}
		for name := range expectedSkills {
			t.Errorf("skill %q in expected set but not in skillFiles", name)
		}
	})

	t.Run("agentFiles matches currentAgents map in cleanupLegacy", func(t *testing.T) {
		expectedAgents := map[string]bool{
			"cco-agent-analyze.md":  true,
			"cco-agent-apply.md":    true,
			"cco-agent-research.md": true,
		}

		for _, f := range agentFiles {
			parts := strings.Split(f, "/")
			name := parts[len(parts)-1]
			if !expectedAgents[name] {
				t.Errorf("agent %q in agentFiles but not in expected agents set", name)
			}
			delete(expectedAgents, name)
		}
		for name := range expectedAgents {
			t.Errorf("agent %q in expected set but not in agentFiles", name)
		}
	})
}

func TestBuildFileList(t *testing.T) {
	files := buildFileList()

	expectedCount := len(rulesFiles) + len(skillFiles) + len(agentFiles)
	if len(files) != expectedCount {
		t.Errorf("got %d files, want %d", len(files), expectedCount)
	}

	for _, f := range files {
		switch {
		case strings.HasPrefix(f.path, "rules/"):
			if f.group != "rules" {
				t.Errorf("rules file %s has group %q, want 'rules'", f.path, f.group)
			}
		case strings.HasPrefix(f.path, "skills/"):
			if f.group != "skills" {
				t.Errorf("skills file %s has group %q, want 'skills'", f.path, f.group)
			}
		case strings.HasPrefix(f.path, "agents/"):
			if f.group != "agents" {
				t.Errorf("agents file %s has group %q, want 'agents'", f.path, f.group)
			}
		default:
			t.Errorf("unexpected path prefix: %s", f.path)
		}
	}
}

func TestWriteResults(t *testing.T) {
	criticalFiles := map[string]bool{"rules/cco-rules.md": true}

	t.Run("writes all files successfully", func(t *testing.T) {
		base := t.TempDir()
		results := []downloadResult{
			{path: "rules/cco-rules.md", group: "rules", content: "---\ntest\n---\ncontent"},
			{path: "skills/cco-test/SKILL.md", group: "skills", content: "---\nskill\n---\ncontent"},
		}

		failed, err := writeResults(base, results, criticalFiles)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if failed != 0 {
			t.Errorf("got %d failures, want 0", failed)
		}

		// Verify files were written
		for _, r := range results {
			content, readErr := os.ReadFile(filepath.Join(base, filepath.FromSlash(r.path))) //nolint:gosec // G304: test path
			if readErr != nil {
				t.Errorf("file %s not written: %v", r.path, readErr)
			}
			if string(content) != r.content {
				t.Errorf("file %s content mismatch", r.path)
			}
		}
	})

	t.Run("counts non-critical failures", func(t *testing.T) {
		base := t.TempDir()
		results := []downloadResult{
			{path: "skills/cco-bad/SKILL.md", group: "skills", err: fmt.Errorf("download error")},
		}

		failed, err := writeResults(base, results, criticalFiles)
		if err != nil {
			t.Fatalf("unexpected critical error: %v", err)
		}
		if failed != 1 {
			t.Errorf("got %d failures, want 1", failed)
		}
	})

	t.Run("returns error on critical download failure", func(t *testing.T) {
		base := t.TempDir()
		results := []downloadResult{
			{path: "rules/cco-rules.md", group: "rules", err: fmt.Errorf("critical download error")},
		}

		_, err := writeResults(base, results, criticalFiles)
		if err == nil {
			t.Error("expected error for critical file failure")
		}
		if !strings.Contains(err.Error(), "critical file failed") {
			t.Errorf("error should mention critical failure, got: %v", err)
		}
	})
}

func TestStateFile(t *testing.T) {
	t.Run("writes timestamp", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), ".claude", ".cco-installing")
		before := time.Now().Unix()
		if err := writeStateFile(path); err != nil {
			t.Fatalf("writeStateFile failed: %v", err)
		}
		after := time.Now().Unix()

		content, err := os.ReadFile(path) //nolint:gosec // G304: test path
		if err != nil {
			t.Fatalf("read failed: %v", err)
		}
		ts, err := strconv.ParseInt(strings.TrimSpace(string(content)), 10, 64)
		if err != nil {
			t.Fatalf("parse failed: %v", err)
		}
		if ts < before || ts > after {
			t.Errorf("timestamp %d not between %d and %d", ts, before, after)
		}
	})

	t.Run("checkStaleState removes stale file", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), ".cco-installing")
		// Write a timestamp from 2 hours ago
		oldTs := fmt.Sprintf("%d", time.Now().Add(-2*time.Hour).Unix())
		_ = os.WriteFile(path, []byte(oldTs), 0600)

		checkStaleState(path)

		if _, err := os.Stat(path); !os.IsNotExist(err) {
			t.Error("stale state file should have been removed")
		}
	})

	t.Run("checkStaleState keeps recent file", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), ".cco-installing")
		recentTs := fmt.Sprintf("%d", time.Now().Unix())
		_ = os.WriteFile(path, []byte(recentTs), 0600)

		checkStaleState(path)

		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Error("recent state file should not be removed")
		}
	})

	t.Run("checkStaleState handles missing file", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), ".cco-installing")
		// Should not panic
		checkStaleState(path)
	})

	t.Run("checkStaleState handles unparseable timestamp", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), ".cco-installing")
		_ = os.WriteFile(path, []byte("not-a-number"), 0600)
		// Falls back to ModTime; file is recent so it should not be removed.
		checkStaleState(path)
		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Error("recent file with unparseable timestamp should not be removed")
		}
	})

	t.Run("writeStateFile fails when parent is a file", func(t *testing.T) {
		base := t.TempDir()
		// Block the parent directory path with a regular file.
		blocker := filepath.Join(base, "blocked")
		_ = os.WriteFile(blocker, []byte("x"), 0600)
		err := writeStateFile(filepath.Join(blocker, "state"))
		if err == nil {
			t.Error("expected error when parent path is a file, not a directory")
		}
	})
}

func TestDetectCurrentVersion(t *testing.T) {
	t.Run("returns version from installed rules", func(t *testing.T) {
		base := t.TempDir()
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"), []byte("---\ncco_version: 4.4.0\n---\n"), 0600)

		v := detectCurrentVersion(base)
		if v != "4.4.0" {
			t.Errorf("got %q, want %q", v, "4.4.0")
		}
	})

	t.Run("returns empty when not installed", func(t *testing.T) {
		v := detectCurrentVersion(t.TempDir())
		if v != "" {
			t.Errorf("got %q, want empty", v)
		}
	})
}

func TestExtractVersion(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"standard version", "---\ncco_version: 4.4.0\n---\n", "4.4.0"},
		{"version with comment", "---\ncco_version: 4.4.0 # current\n---\n", "4.4.0"},
		{"no version", "---\nname: test\n---\n", ""},
		{"empty content", "", ""},
		{"version at end without newline", "cco_version: 1.0.0", "1.0.0"},
		{"multiple fields", "---\nname: test\ncco_version: 3.2.1\nlast_update: today\n---\n", "3.2.1"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := extractVersion(tt.input)
			if got != tt.want {
				t.Errorf("extractVersion(%q) = %q, want %q", tt.input, got, tt.want)
			}
		})
	}
}

func TestIsRetryable(t *testing.T) {
	tests := []struct {
		name string
		err  error
		want bool
	}{
		{"500 error", &httpError{StatusCode: 500, Path: "test"}, true},
		{"502 error", &httpError{StatusCode: 502, Path: "test"}, true},
		{"429 rate limit", &httpError{StatusCode: 429, Path: "test"}, true},
		{"404 not found", &httpError{StatusCode: 404, Path: "test"}, false},
		{"403 forbidden", &httpError{StatusCode: 403, Path: "test"}, false},
		{"download network error", &retryableNetworkError{cause: fmt.Errorf("connection refused"), op: "download"}, true},
		{"read network error", &retryableNetworkError{cause: fmt.Errorf("timeout"), op: "read"}, true},
		{"frontmatter error", fmt.Errorf("unexpected content for test.md (missing YAML frontmatter)"), false},
		{"generic error", fmt.Errorf("something else"), false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isRetryable(tt.err)
			if got != tt.want {
				t.Errorf("isRetryable(%v) = %v, want %v", tt.err, got, tt.want)
			}
		})
	}
}

func TestResolveChannel(t *testing.T) {
	t.Run("returns tag when specified", func(t *testing.T) {
		ref := resolveChannel("v4.0.0")
		if ref != "v4.0.0" {
			t.Errorf("got %q, want %q", ref, "v4.0.0")
		}
	})

	t.Run("resolves latest tag when no tag specified", func(t *testing.T) {
		originalClient := httpClient
		defer func() { httpClient = originalClient }()

		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_ = json.NewEncoder(w).Encode([]struct {
				Name string `json:"name"`
			}{{"v4.9.0"}})
		}))
		defer server.Close()
		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		ref := resolveChannel("")
		if ref != "v4.9.0" {
			t.Errorf("got %q, want %q", ref, "v4.9.0")
		}
	})

	t.Run("falls back to main when tags API fails", func(t *testing.T) {
		originalClient := httpClient
		defer func() { httpClient = originalClient }()

		httpClient = &http.Client{
			Timeout:   1 * time.Second,
			Transport: &rewriteTransport{base: "http://127.0.0.1:1"},
		}

		ref := resolveChannel("")
		if ref != "main" {
			t.Errorf("got %q, want %q", ref, "main")
		}
	})
}

func TestResolveAndVerify(t *testing.T) {
	originalClient := httpClient
	originalBackoff := retryBackoff
	defer func() {
		httpClient = originalClient
		retryBackoff = originalBackoff
	}()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	validContent := "---\ncco_version: 4.9.0\ndescription: test\n---\n# Rules"

	t.Run("fresh install extracts version", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_, _ = fmt.Fprint(w, validContent)
		}))
		defer server.Close()
		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		base := t.TempDir()
		info, err := resolveAndVerify(base, "v4.9.0")
		if err != nil {
			t.Fatalf("resolveAndVerify failed: %v", err)
		}
		if info.newVersion != "4.9.0" {
			t.Errorf("got version %q, want %q", info.newVersion, "4.9.0")
		}
		if info.ref != "v4.9.0" {
			t.Errorf("got ref %q, want %q", info.ref, "v4.9.0")
		}
	})

	t.Run("already up to date returns errUpToDate", func(t *testing.T) {
		// The up-to-date check only fires when tag=="" (no explicit pin).
		// Server must handle both the tags API and file content requests.
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if strings.Contains(r.URL.RawQuery, "per_page") {
				_ = json.NewEncoder(w).Encode([]struct {
					Name string `json:"name"`
				}{{"v4.9.0"}})
				return
			}
			_, _ = fmt.Fprint(w, validContent)
		}))
		defer server.Close()
		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		base := t.TempDir()
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"), []byte(validContent), 0600)

		_, err := resolveAndVerify(base, "") // no pin → resolves v4.9.0, matches installed
		if err == nil {
			t.Fatal("expected errUpToDate, got nil")
		}
		if err.Error() != errUpToDate.Error() {
			t.Errorf("expected errUpToDate, got %v", err)
		}
	})

	t.Run("source verification failure returns error", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(404)
		}))
		defer server.Close()
		httpClient = &http.Client{
			Timeout:   5 * time.Second,
			Transport: &rewriteTransport{base: server.URL},
		}

		_, err := resolveAndVerify(t.TempDir(), "v4.9.0")
		if err == nil {
			t.Fatal("expected error for 404 source")
		}
	})
}

func TestDownloadInParallel(t *testing.T) {
	originalBackoff := retryBackoff
	defer func() { retryBackoff = originalBackoff }()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	validContent := "---\ncco_version: 4.9.0\ndescription: test\n---\n# Content"
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = fmt.Fprint(w, validContent)
	}))
	defer server.Close()

	files := []installFile{
		{path: "rules/cco-rules.md", group: "rules"},
		{path: "skills/cco-test/SKILL.md", group: "skills"},
		{path: "agents/cco-agent-test.md", group: "agents"},
	}
	info := installInfo{
		baseURL:     server.URL,
		testContent: validContent,
	}

	results := downloadInParallel(files, info)
	if len(results) != len(files) {
		t.Fatalf("got %d results, want %d", len(results), len(files))
	}

	// cco-rules.md must reuse pre-verified content without hitting server
	if results[0].content != validContent {
		t.Error("cco-rules.md should reuse pre-verified testContent")
	}
	if results[0].err != nil {
		t.Errorf("cco-rules.md should not error: %v", results[0].err)
	}

	// Other files should be downloaded from the mock server
	for i := 1; i < len(results); i++ {
		if results[i].err != nil {
			t.Errorf("file %s should not error: %v", results[i].path, results[i].err)
		}
		if results[i].content != validContent {
			t.Errorf("file %s content mismatch", results[i].path)
		}
	}
}

func TestRunVersion(t *testing.T) {
	t.Run("not installed", func(t *testing.T) {
		t.Setenv("CCO_CLAUDE_DIR", t.TempDir())
		if err := runVersion(); err != nil {
			t.Fatalf("runVersion should not error when not installed: %v", err)
		}
	})

	t.Run("installed with version", func(t *testing.T) {
		base := t.TempDir()
		t.Setenv("CCO_CLAUDE_DIR", base)
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
			[]byte("---\ncco_version: 4.9.0\n---\n"), 0600)

		if err := runVersion(); err != nil {
			t.Fatalf("runVersion failed: %v", err)
		}
	})
}

func TestRunInstall(t *testing.T) {
	originalClient := httpClient
	originalBackoff := retryBackoff
	defer func() {
		httpClient = originalClient
		retryBackoff = originalBackoff
	}()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	validContent := "---\ncco_version: 4.9.0\ndescription: test\n---\n# Content"
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if strings.Contains(r.URL.RawQuery, "per_page") {
			_ = json.NewEncoder(w).Encode([]struct {
				Name string `json:"name"`
			}{{"v4.9.0"}})
			return
		}
		_, _ = fmt.Fprint(w, validContent)
	}))
	defer server.Close()
	httpClient = &http.Client{
		Timeout:   5 * time.Second,
		Transport: &rewriteTransport{base: server.URL},
	}

	base := t.TempDir()
	t.Setenv("CCO_CLAUDE_DIR", base)

	if err := runInstall("v4.9.0"); err != nil {
		t.Fatalf("runInstall failed: %v", err)
	}

	// Verify critical rules file installed
	rulesPath := filepath.Join(base, "rules", "cco-rules.md")
	if _, err := os.Stat(rulesPath); os.IsNotExist(err) {
		t.Error("rules/cco-rules.md should be installed")
	}

	// Verify all skill files installed
	for _, f := range skillFiles {
		p := filepath.Join(base, filepath.FromSlash(f))
		if _, err := os.Stat(p); os.IsNotExist(err) {
			t.Errorf("skill file %s should be installed", f)
		}
	}

	// Verify all agent files installed
	for _, f := range agentFiles {
		p := filepath.Join(base, filepath.FromSlash(f))
		if _, err := os.Stat(p); os.IsNotExist(err) {
			t.Errorf("agent file %s should be installed", f)
		}
	}
}

func TestRunInstallPinnedReinstall(t *testing.T) {
	originalClient := httpClient
	originalBackoff := retryBackoff
	defer func() {
		httpClient = originalClient
		retryBackoff = originalBackoff
	}()
	retryBackoff = func(_ int) time.Duration { return time.Millisecond }

	validContent := "---\ncco_version: 4.9.0\ndescription: test\n---\n# Content"
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = fmt.Fprint(w, validContent)
	}))
	defer server.Close()
	httpClient = &http.Client{
		Timeout:   5 * time.Second,
		Transport: &rewriteTransport{base: server.URL},
	}

	base := t.TempDir()
	t.Setenv("CCO_CLAUDE_DIR", base)

	// Pre-install same version so installer detects "up to date"
	rulesDir := filepath.Join(base, "rules")
	_ = os.MkdirAll(rulesDir, 0750)
	_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"), []byte(validContent), 0600)

	// Should succeed without error (up-to-date is a clean exit)
	if err := runInstall("v4.9.0"); err != nil {
		t.Fatalf("runInstall up-to-date should not error: %v", err)
	}
}

func TestRunUninstall(t *testing.T) {
	t.Run("CCO not installed", func(t *testing.T) {
		t.Setenv("CCO_CLAUDE_DIR", t.TempDir())
		if err := runUninstall(); err != nil {
			t.Fatalf("runUninstall should not error when not installed: %v", err)
		}
	})

	t.Run("declines removal", func(t *testing.T) {
		base := t.TempDir()
		t.Setenv("CCO_CLAUDE_DIR", base)
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
			[]byte("---\ncco_version: 4.9.0\n---\n"), 0600)

		// Feed "n" to all stdin prompts
		r, w, _ := os.Pipe()
		oldStdin := os.Stdin
		os.Stdin = r
		defer func() { os.Stdin = oldStdin }()
		_, _ = fmt.Fprint(w, "n\n")
		w.Close()

		if err := runUninstall(); err != nil {
			t.Fatalf("runUninstall failed: %v", err)
		}
		// Rules file should still exist (answered n)
		if _, err := os.Stat(filepath.Join(rulesDir, "cco-rules.md")); os.IsNotExist(err) {
			t.Error("rules file should still exist after declining removal")
		}
	})

	t.Run("confirms full removal", func(t *testing.T) {
		base := t.TempDir()
		t.Setenv("CCO_CLAUDE_DIR", base)
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
			[]byte("---\ncco_version: 4.9.0\n---\n"), 0600)
		// Create a skill dir too
		_ = os.MkdirAll(filepath.Join(base, "skills", "cco-optimize"), 0750)

		// Feed "y" to trigger full removal
		r, w, _ := os.Pipe()
		oldStdin := os.Stdin
		os.Stdin = r
		defer func() { os.Stdin = oldStdin }()
		_, _ = fmt.Fprint(w, "y\n")
		w.Close()

		if err := runUninstall(); err != nil {
			t.Fatalf("runUninstall failed: %v", err)
		}
		// Rules file should be removed (answered y)
		if _, err := os.Stat(filepath.Join(rulesDir, "cco-rules.md")); !os.IsNotExist(err) {
			t.Error("rules file should be removed after confirming full removal")
		}
	})
}

func TestPrintVersionInfo(t *testing.T) {
	// Just verify it doesn't panic with various inputs
	printVersionInfo("", "", "")
	printVersionInfo("4.0.0", "", "")
	printVersionInfo("", "4.1.0", "")
	printVersionInfo("4.0.0", "4.1.0", "")
	printVersionInfo("4.0.0", "4.0.0", "")
	printVersionInfo("4.0.0", "4.0.0", "v4.0.0")
}

func TestErrorMessages(t *testing.T) {
	t.Run("httpError message", func(t *testing.T) {
		e := &httpError{StatusCode: 404, Path: "test/file.md"}
		got := e.Error()
		if !strings.Contains(got, "404") || !strings.Contains(got, "test/file.md") {
			t.Errorf("httpError.Error() = %q, want status and path", got)
		}
	})

	t.Run("retryableNetworkError message", func(t *testing.T) {
		cause := fmt.Errorf("connection refused")
		e := &retryableNetworkError{cause: cause, op: "download"}
		got := e.Error()
		if !strings.Contains(got, "download") || !strings.Contains(got, "connection refused") {
			t.Errorf("retryableNetworkError.Error() = %q, want op and cause", got)
		}
		if e.Unwrap() != cause {
			t.Error("retryableNetworkError.Unwrap() should return cause")
		}
	})
}

func TestRunUninstallPerGroup(t *testing.T) {
	base := t.TempDir()
	t.Setenv("CCO_CLAUDE_DIR", base)

	rulesDir := filepath.Join(base, "rules")
	_ = os.MkdirAll(rulesDir, 0750)
	_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
		[]byte("---\ncco_version: 4.9.0\n---\n"), 0600)
	_ = os.MkdirAll(filepath.Join(base, "skills", "cco-optimize"), 0750)
	agentDir := filepath.Join(base, "agents")
	_ = os.MkdirAll(agentDir, 0750)
	_ = os.WriteFile(filepath.Join(agentDir, "cco-agent-analyze.md"), []byte("x"), 0600)

	// Feed "n" (skip full removal), then "y/y/y" for per-group removal
	r, w, _ := os.Pipe()
	oldStdin := os.Stdin
	os.Stdin = r
	defer func() { os.Stdin = oldStdin }()
	_, _ = fmt.Fprint(w, "n\ny\ny\ny\n")
	w.Close()

	if err := runUninstall(); err != nil {
		t.Fatalf("runUninstall per-group failed: %v", err)
	}
	if _, err := os.Stat(filepath.Join(rulesDir, "cco-rules.md")); !os.IsNotExist(err) {
		t.Error("rules file should be removed after per-group y")
	}
}

func TestPrintSummaryWithFailures(t *testing.T) {
	// Verify printSummary doesn't panic on failure case
	info := installInfo{ref: "v4.9.0"}
	printSummary(t.TempDir(), info, 2, nil)
}

func TestClaudeDirEnvOverride(t *testing.T) {
	expected := t.TempDir()
	t.Setenv("CCO_CLAUDE_DIR", expected)
	got, err := claudeDir()
	if err != nil {
		t.Fatalf("claudeDir failed: %v", err)
	}
	if got != expected {
		t.Errorf("got %q, want %q", got, expected)
	}
}

func TestPrintUsage(t *testing.T) {
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatal(err)
	}
	old := os.Stdout
	os.Stdout = w

	printUsage()

	_ = w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	output := buf.String()

	for _, want := range []string{"CCO", "install", "uninstall", "version"} {
		if !strings.Contains(output, want) {
			t.Errorf("usage output missing %q", want)
		}
	}
}

func TestEnsurePATHNotInPath(t *testing.T) {
	// Set PATH to empty so the binary dir is guaranteed to be absent.
	t.Setenv("PATH", "")

	r, w, err := os.Pipe()
	if err != nil {
		t.Fatal(err)
	}
	old := os.Stdout
	os.Stdout = w

	ensurePATH() // should print PATH advice without panicking

	_ = w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	if buf.Len() == 0 {
		t.Error("ensurePATH should print advice when binary dir is not in PATH")
	}
}

func TestWriteFileRenameFail(t *testing.T) {
	base := t.TempDir()
	// Place a file at "rules" so MkdirAll("base/rules") fails (file exists, not dir).
	_ = os.WriteFile(filepath.Join(base, "rules"), []byte("blocking"), 0600)

	err := writeFile(base, "rules/cco-rules.md", "---\ntest\n---\n")
	if err == nil {
		t.Fatal("expected error when target directory cannot be created")
	}
	if !strings.Contains(err.Error(), "mkdir failed") {
		t.Errorf("expected mkdir error, got: %v", err)
	}
}

func TestWriteResultsCriticalWriteFail(t *testing.T) {
	base := t.TempDir()
	// Block creation of the "rules" directory so writeFile fails on the critical file.
	_ = os.WriteFile(filepath.Join(base, "rules"), []byte("blocking"), 0600)

	criticalFiles := map[string]bool{"rules/cco-rules.md": true}
	results := []downloadResult{
		{path: "rules/cco-rules.md", group: "rules", content: "---\ntest\n---\ncontent"},
	}

	_, err := writeResults(base, results, criticalFiles)
	if err == nil {
		t.Fatal("expected error for critical file write failure")
	}
	if !strings.Contains(err.Error(), "critical file write failed") {
		t.Errorf("expected critical write error, got: %v", err)
	}
}

func captureStdout(t *testing.T, fn func()) string {
	t.Helper()
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatal(err)
	}
	old := os.Stdout
	os.Stdout = w
	fn()
	_ = w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	return buf.String()
}

func TestRunVersionJSON(t *testing.T) {
	origArgs := os.Args
	defer func() { os.Args = origArgs }()

	t.Run("json with version", func(t *testing.T) {
		base := t.TempDir()
		t.Setenv("CCO_CLAUDE_DIR", base)
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
			[]byte("---\ncco_version: 4.9.0\n---\n"), 0600)

		os.Args = []string{"cco", "version", "--json"}
		output := captureStdout(t, func() { _ = runVersion() })

		if !strings.Contains(output, `"version"`) || !strings.Contains(output, "4.9.0") {
			t.Errorf("expected version JSON, got: %q", output)
		}
	})

	t.Run("json not installed", func(t *testing.T) {
		t.Setenv("CCO_CLAUDE_DIR", t.TempDir())
		os.Args = []string{"cco", "version", "--json"}
		output := captureStdout(t, func() { _ = runVersion() })

		if !strings.Contains(output, `"installed":false`) {
			t.Errorf("expected installed:false JSON, got: %q", output)
		}
	})

	t.Run("json installed but no version", func(t *testing.T) {
		base := t.TempDir()
		t.Setenv("CCO_CLAUDE_DIR", base)
		rulesDir := filepath.Join(base, "rules")
		_ = os.MkdirAll(rulesDir, 0750)
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"),
			[]byte("---\nname: no-version-here\n---\n"), 0600)

		os.Args = []string{"cco", "version", "--json"}
		output := captureStdout(t, func() { _ = runVersion() })

		if !strings.Contains(output, `"installed":true`) {
			t.Errorf("expected installed:true JSON, got: %q", output)
		}
	})
}

func TestWriteFileRenameOverDir(t *testing.T) {
	base := t.TempDir()
	// Create target path as a directory — rename over a directory fails on all platforms.
	targetDir := filepath.Join(base, "rules", "cco-rules.md")
	_ = os.MkdirAll(targetDir, 0750)

	err := writeFile(base, "rules/cco-rules.md", "---\ntest\n---\n")
	if err == nil {
		t.Fatal("expected error when target is a directory")
	}
	if !strings.Contains(err.Error(), "rename failed") {
		t.Errorf("expected rename error, got: %v", err)
	}
}

func TestRemoveIfExistsCannotRemove(t *testing.T) {
	base := t.TempDir()
	// Create a non-empty directory at the target path so os.Remove fails.
	target := filepath.Join(base, "nonempty")
	_ = os.MkdirAll(target, 0750)
	_ = os.WriteFile(filepath.Join(target, "file.txt"), []byte("x"), 0600)

	// removeIfExists on a non-empty dir returns false (os.Remove fails for non-empty dirs).
	removed := removeIfExists(base, "nonempty")
	if removed {
		t.Error("expected false when remove fails on non-empty directory")
	}
}
