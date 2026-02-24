package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

var httpClient = &http.Client{
	Timeout: 30 * time.Second,
	Transport: &http.Transport{
		MaxIdleConns:        10,
		MaxIdleConnsPerHost: 15,
		IdleConnTimeout:     30 * time.Second,
	},
}

// retryBackoff calculates the backoff duration for a retry attempt.
// Overridable in tests for faster execution.
var retryBackoff = func(attempt int) time.Duration {
	return time.Duration(1<<uint(attempt)) * time.Second // 1s, 2s, 4s
}

func resolveLatestTag() string {
	url := fmt.Sprintf("https://api.github.com/repos/%s/tags?per_page=1", repo)
	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Warning: could not fetch latest tag: %v (falling back to main)\n", err)
		return "main"
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		fmt.Fprintf(os.Stderr, "Warning: GitHub API returned %d (falling back to main)\n", resp.StatusCode)
		return "main"
	}

	var tags []struct {
		Name string `json:"name"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&tags); err != nil || len(tags) == 0 {
		fmt.Fprintf(os.Stderr, "Warning: no tags found in repository (falling back to main)\n")
		return "main"
	}
	return tags[0].Name
}

func downloadFile(baseURL, path string) (string, error) {
	cleanPath := filepath.Clean(path)
	if strings.HasPrefix(cleanPath, "..") || filepath.IsAbs(cleanPath) {
		return "", fmt.Errorf("invalid path: %s", path)
	}

	const maxRetries = 3
	for attempt := 0; ; attempt++ {
		content, err := tryDownload(baseURL, path)
		if err == nil {
			return content, nil
		}
		if !isRetryable(err) || attempt >= maxRetries {
			return "", err
		}
		time.Sleep(retryBackoff(attempt))
	}
}

// httpError represents an HTTP response error with a status code.
type httpError struct {
	StatusCode int
	Path       string
}

func (e *httpError) Error() string {
	return fmt.Sprintf("HTTP %d for %s", e.StatusCode, e.Path)
}

// isRetryable returns true for transient errors worth retrying:
// network errors, 5xx server errors, and 429 rate limiting.
// Content validation errors and 4xx client errors are not retryable.
func isRetryable(err error) bool {
	var he *httpError
	if errors.As(err, &he) {
		return he.StatusCode >= 500 || he.StatusCode == http.StatusTooManyRequests
	}
	// Only retry network-level errors (download failed / read failed),
	// not content validation errors (frontmatter check).
	msg := err.Error()
	return strings.HasPrefix(msg, "download failed:") || strings.HasPrefix(msg, "read failed:")
}

func tryDownload(baseURL, path string) (string, error) {
	url := fmt.Sprintf("%s/%s", baseURL, path)
	resp, err := httpClient.Get(url)
	if err != nil {
		return "", fmt.Errorf("download failed: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		return "", &httpError{StatusCode: resp.StatusCode, Path: path}
	}

	const maxFileSize = 10 * 1024 * 1024
	body, err := io.ReadAll(io.LimitReader(resp.Body, maxFileSize))
	if err != nil {
		return "", fmt.Errorf("read failed: %w", err)
	}
	// Check for truncation: if there's more data, the file exceeds the limit
	probe := make([]byte, 1)
	if n, _ := resp.Body.Read(probe); n > 0 {
		return "", fmt.Errorf("file exceeds 10MB limit: %s", path)
	}

	if !bytes.HasPrefix(body, []byte("---\n")) || !bytes.Contains(body, []byte("\n---\n")) {
		return "", fmt.Errorf("unexpected content for %s (missing YAML frontmatter)", path)
	}

	return string(body), nil
}

func writeFile(base, path, content string) error {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	dir := filepath.Dir(fullPath)
	if err := os.MkdirAll(dir, 0750); err != nil {
		return fmt.Errorf("mkdir failed: %w", err)
	}

	// Atomic write: write to temp file, then rename to final path.
	// This prevents partial writes from corrupting installed files.
	tmpPath := fullPath + ".tmp"
	if err := os.WriteFile(tmpPath, []byte(content), 0600); err != nil {
		return fmt.Errorf("write failed: %w", err)
	}
	if err := os.Rename(tmpPath, fullPath); err != nil {
		_ = os.Remove(tmpPath)
		return fmt.Errorf("rename failed: %w", err)
	}
	return nil
}
