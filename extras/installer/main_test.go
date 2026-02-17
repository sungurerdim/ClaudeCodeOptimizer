package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
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

		content, err := os.ReadFile(filepath.Join(base, "a", "b", "c.md"))
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
		content, _ := os.ReadFile(filepath.Join(base, "a", "b", "c.md"))
		if string(content) != "second" {
			t.Errorf("got %q, want %q", string(content), "second")
		}
	})
}

func TestRemoveIfExists(t *testing.T) {
	base := t.TempDir()

	t.Run("removes existing file", func(t *testing.T) {
		path := "test.md"
		_ = os.WriteFile(filepath.Join(base, path), []byte("x"), 0644)

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
		_ = os.MkdirAll(dir, 0755)
		_ = os.WriteFile(filepath.Join(dir, "file.txt"), []byte("x"), 0644)

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
		_ = os.WriteFile(filepath.Join(base, "file.txt"), []byte("x"), 0644)
		removed := removeDirIfExists(base, "file.txt")
		if removed {
			t.Error("expected false for file (not directory)")
		}
	})
}

func TestDownloadFile(t *testing.T) {
	t.Run("successful download with valid content", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			fmt.Fprint(w, "---\nname: test\n---\n# Content")
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
			fmt.Fprint(w, "<html>Not a CCO file</html>")
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
}

func TestResolveLatestTag(t *testing.T) {
	originalClient := httpClient
	defer func() { httpClient = originalClient }()

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
			fmt.Fprint(w, "[]")
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

// rewriteTransport redirects all requests to a test server URL.
type rewriteTransport struct {
	base string
}

func (t *rewriteTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	req.URL.Scheme = "http"
	parsed, _ := http.NewRequest(req.Method, t.base+req.URL.Path+"?"+req.URL.RawQuery, req.Body)
	return http.DefaultTransport.RoundTrip(parsed)
}

func TestUpdateTimestamp(t *testing.T) {
	base := t.TempDir()
	rulesDir := filepath.Join(base, "rules")
	_ = os.MkdirAll(rulesDir, 0755)

	t.Run("updates existing timestamp", func(t *testing.T) {
		content := "---\ncco_version: 4.2.0\nlast_update_check: 2024-01-01T00:00:00Z\n---\n# Rules"
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"), []byte(content), 0644)

		updateTimestamp(base)

		updated, _ := os.ReadFile(filepath.Join(rulesDir, "cco-rules.md"))
		if strings.Contains(string(updated), "2024-01-01") {
			t.Error("timestamp should have been updated")
		}
		if !strings.Contains(string(updated), "last_update_check:") {
			t.Error("timestamp line should still exist")
		}
	})

	t.Run("does nothing if no timestamp line", func(t *testing.T) {
		content := "---\ncco_version: 4.2.0\n---\n# Rules"
		_ = os.WriteFile(filepath.Join(rulesDir, "cco-rules.md"), []byte(content), 0644)

		updateTimestamp(base)

		updated, _ := os.ReadFile(filepath.Join(rulesDir, "cco-rules.md"))
		if string(updated) != content {
			t.Error("file should be unchanged when no timestamp line exists")
		}
	})

	t.Run("does nothing if file missing", func(t *testing.T) {
		_ = os.Remove(filepath.Join(rulesDir, "cco-rules.md"))
		// Should not panic
		updateTimestamp(base)
	})
}

func TestCleanupLegacy(t *testing.T) {
	t.Run("removes v3 legacy commands", func(t *testing.T) {
		base := t.TempDir()
		cmdDir := filepath.Join(base, "commands")
		_ = os.MkdirAll(cmdDir, 0755)

		for _, f := range legacyV3Commands {
			_ = os.WriteFile(filepath.Join(base, filepath.FromSlash(f)), []byte("x"), 0644)
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
		_ = os.MkdirAll(filepath.Join(skillsDir, "cco-optimize"), 0755)
		// Create a stale skill
		_ = os.MkdirAll(filepath.Join(skillsDir, "cco-oldskill"), 0755)

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
		_ = os.MkdirAll(agentDir, 0755)

		// Create a current agent
		_ = os.WriteFile(filepath.Join(agentDir, "cco-agent-analyze.md"), []byte("x"), 0644)
		// Create a stale agent
		_ = os.WriteFile(filepath.Join(agentDir, "cco-agent-old.md"), []byte("x"), 0644)

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
			_ = os.MkdirAll(filepath.Join(base, filepath.FromSlash(d)), 0755)
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
		// Verify that the file manifest arrays are consistent with the
		// cleanup maps. If a skill is added to skillFiles but not to
		// currentSkills, legacy cleanup would incorrectly remove it.
		expectedSkills := map[string]bool{
			"cco-optimize":  true,
			"cco-align":     true,
			"cco-commit":    true,
			"cco-research":  true,
			"cco-docs":      true,
			"cco-update":    true,
			"cco-blueprint": true,
			"cco-pr":        true,
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
