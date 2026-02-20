package main

import (
	"bytes"
	"encoding/json"
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
		MaxIdleConnsPerHost: 5,
		IdleConnTimeout:     30 * time.Second,
	},
}

func resolveLatestTag() string {
	url := fmt.Sprintf("https://api.github.com/repos/%s/tags?per_page=1", repo)
	resp, err := httpClient.Get(url)
	if err != nil {
		return "main"
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
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
	if strings.Contains(path, "..") {
		return "", fmt.Errorf("invalid path: %s", path)
	}

	url := fmt.Sprintf("%s/%s", baseURL, path)
	resp, err := httpClient.Get(url)
	if err != nil {
		return "", fmt.Errorf("download failed: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("HTTP %d for %s", resp.StatusCode, path)
	}

	body, err := io.ReadAll(io.LimitReader(resp.Body, 10*1024*1024))
	if err != nil {
		return "", fmt.Errorf("read failed: %w", err)
	}

	if !bytes.HasPrefix(body, []byte("---")) || !bytes.Contains(body, []byte("\n---\n")) {
		return "", fmt.Errorf("unexpected content for %s (missing YAML frontmatter)", path)
	}

	return string(body), nil
}

func writeFile(base, path, content string) error {
	fullPath := filepath.Join(base, filepath.FromSlash(path))
	dir := filepath.Dir(fullPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("mkdir failed: %w", err)
	}
	return os.WriteFile(fullPath, []byte(content), 0644)
}
