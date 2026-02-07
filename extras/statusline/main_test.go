package main

import (
	"testing"
)

// ============================================================================
// visibleLen
// ============================================================================

func TestVisibleLen_PlainText(t *testing.T) {
	if got := visibleLen("hello"); got != 5 {
		t.Errorf("visibleLen(\"hello\") = %d, want 5", got)
	}
}

func TestVisibleLen_WithANSI(t *testing.T) {
	s := "\x1b[92mhello\x1b[0m"
	if got := visibleLen(s); got != 5 {
		t.Errorf("visibleLen(green hello) = %d, want 5", got)
	}
}

func TestVisibleLen_MultipleANSI(t *testing.T) {
	s := c("repo", green) + ":" + c("main", cyan)
	// "repo:main" = 9 visible chars
	if got := visibleLen(s); got != 9 {
		t.Errorf("visibleLen(repo:main) = %d, want 9", got)
	}
}

func TestVisibleLen_Empty(t *testing.T) {
	if got := visibleLen(""); got != 0 {
		t.Errorf("visibleLen(\"\") = %d, want 0", got)
	}
}

// ============================================================================
// formatModelName
// ============================================================================

func TestFormatModelName_StripClaude(t *testing.T) {
	if got := formatModelName("Claude Opus 4.6"); got != "Opus 4.6" {
		t.Errorf("formatModelName = %q, want \"Opus 4.6\"", got)
	}
}

func TestFormatModelName_NoPrefix(t *testing.T) {
	if got := formatModelName("Sonnet 4.5"); got != "Sonnet 4.5" {
		t.Errorf("formatModelName = %q, want \"Sonnet 4.5\"", got)
	}
}

func TestFormatModelName_Empty(t *testing.T) {
	if got := formatModelName(""); got != "Unknown" {
		t.Errorf("formatModelName(\"\") = %q, want \"Unknown\"", got)
	}
}

// ============================================================================
// formatK
// ============================================================================

func TestFormatK_Under1000(t *testing.T) {
	if got := formatK(500); got != "500" {
		t.Errorf("formatK(500) = %q, want \"500\"", got)
	}
}

func TestFormatK_Exact1000(t *testing.T) {
	// (1000+500)/1000 = 1 (integer division)
	if got := formatK(1000); got != "1K" {
		t.Errorf("formatK(1000) = %q, want \"1K\"", got)
	}
}

func TestFormatK_Large(t *testing.T) {
	// (45000+500)/1000 = 45 (integer division)
	if got := formatK(45000); got != "45K" {
		t.Errorf("formatK(45000) = %q, want \"45K\"", got)
	}
}

func TestFormatK_Zero(t *testing.T) {
	if got := formatK(0); got != "0" {
		t.Errorf("formatK(0) = %q, want \"0\"", got)
	}
}

// ============================================================================
// formatContextUsage
// ============================================================================

func TestFormatContextUsage_Nil(t *testing.T) {
	input := &Input{}
	if got := formatContextUsage(input); got != "" {
		t.Errorf("formatContextUsage(nil cw) = %q, want \"\"", got)
	}
}

func TestFormatContextUsage_WithCurrentUsage(t *testing.T) {
	input := &Input{}
	input.ContextWindow = &struct {
		ContextWindowSize int64 `json:"context_window_size"`
		TotalInputTokens  int64 `json:"total_input_tokens"`
		CurrentUsage      *struct {
			InputTokens              int64 `json:"input_tokens"`
			CacheCreationInputTokens int64 `json:"cache_creation_input_tokens"`
			CacheReadInputTokens     int64 `json:"cache_read_input_tokens"`
		} `json:"current_usage"`
	}{
		ContextWindowSize: 200000,
		CurrentUsage: &struct {
			InputTokens              int64 `json:"input_tokens"`
			CacheCreationInputTokens int64 `json:"cache_creation_input_tokens"`
			CacheReadInputTokens     int64 `json:"cache_read_input_tokens"`
		}{
			InputTokens:              30000,
			CacheCreationInputTokens: 10000,
			CacheReadInputTokens:     5000,
		},
	}
	got := formatContextUsage(input)
	// tokens = 30000+10000+5000 = 45000, (45000+500)/1000=45, percent = 45000*100/200000=22
	if got != "45K 22%" {
		t.Errorf("formatContextUsage = %q", got)
	}
}

func TestFormatContextUsage_FallbackToTotal(t *testing.T) {
	input := &Input{}
	input.ContextWindow = &struct {
		ContextWindowSize int64 `json:"context_window_size"`
		TotalInputTokens  int64 `json:"total_input_tokens"`
		CurrentUsage      *struct {
			InputTokens              int64 `json:"input_tokens"`
			CacheCreationInputTokens int64 `json:"cache_creation_input_tokens"`
			CacheReadInputTokens     int64 `json:"cache_read_input_tokens"`
		} `json:"current_usage"`
	}{
		ContextWindowSize: 200000,
		TotalInputTokens:  10000,
	}
	got := formatContextUsage(input)
	// tokens=10000, (10000+500)/1000=10, percent=10000*100/200000=5
	if got != "10K 5%" {
		t.Errorf("formatContextUsage(fallback) = %q", got)
	}
}

// ============================================================================
// c (color helper)
// ============================================================================

func TestColor(t *testing.T) {
	got := c("test", green)
	want := "\x1b[92mtest\x1b[0m"
	if got != want {
		t.Errorf("c(\"test\", green) = %q, want %q", got, want)
	}
}

// ============================================================================
// justifyRow
// ============================================================================

func TestJustifyRow_Empty(t *testing.T) {
	if got := justifyRow(nil, 40, "·"); got != "" {
		t.Errorf("justifyRow(nil) = %q, want \"\"", got)
	}
}

func TestJustifyRow_Single(t *testing.T) {
	parts := []string{"hello"}
	if got := justifyRow(parts, 40, "·"); got != "hello" {
		t.Errorf("justifyRow(single) = %q, want \"hello\"", got)
	}
}

func TestJustifyRow_Multiple(t *testing.T) {
	parts := []string{"a", "b", "c"}
	got := justifyRow(parts, 20, "·")
	// Should contain separators and spaces
	if visibleLen(got) == 0 {
		t.Error("justifyRow produced empty output")
	}
	// Should contain all parts
	for _, p := range []string{"a", "b", "c"} {
		if !containsVisible(got, p) {
			t.Errorf("justifyRow missing part %q", p)
		}
	}
}

func containsVisible(s, sub string) bool {
	// Strip ANSI codes and check
	plain := ""
	inEsc := false
	for i := 0; i < len(s); i++ {
		if s[i] == '\x1b' {
			inEsc = true
			continue
		}
		if inEsc {
			if s[i] == 'm' {
				inEsc = false
			}
			continue
		}
		plain += string(s[i])
	}
	return len(plain) > 0 && contains(plain, sub)
}

func contains(s, sub string) bool {
	for i := 0; i <= len(s)-len(sub); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

// ============================================================================
// minRowWidth
// ============================================================================

func TestMinRowWidth(t *testing.T) {
	parts := []string{"abc", "de"} // 3 + 2 = 5 content + 3 separator = 8
	if got := minRowWidth(parts); got != 8 {
		t.Errorf("minRowWidth = %d, want 8", got)
	}
}

// ============================================================================
// buildStatusline (integration)
// ============================================================================

func TestBuildStatusline_NoGit(t *testing.T) {
	input := &Input{
		CWD:     "/home/user/project",
		Version: "1.0.80",
	}
	input.Model.DisplayName = "Claude Opus 4.6"

	out := buildStatusline(input, nil)
	if len(out) == 0 {
		t.Error("buildStatusline produced empty output")
	}
	// Should contain project name
	if !containsVisible(out, "project") {
		t.Error("missing project name")
	}
	// Should contain "No git"
	if !containsVisible(out, "No git") {
		t.Error("missing 'No git' indicator")
	}
	// Should contain version
	if !containsVisible(out, "CC 1.0.80") {
		t.Error("missing CC version")
	}
	// Should contain model
	if !containsVisible(out, "Opus 4.6") {
		t.Error("missing model name")
	}
}

func TestBuildStatusline_WithGit(t *testing.T) {
	input := &Input{
		CWD:     "/home/user/myrepo",
		Version: "1.0.80",
	}
	input.Model.DisplayName = "Sonnet 4.5"

	git := &GitInfo{
		Branch:   "main",
		RepoName: "myrepo",
		Tag:      "v1.0.0",
		Mod:      3,
		Add:      1,
		Ahead:    2,
	}

	out := buildStatusline(input, git)
	if !containsVisible(out, "myrepo:main") {
		t.Error("missing repo:branch")
	}
	if !containsVisible(out, "v1.0.0") {
		t.Error("missing tag")
	}
	if !containsVisible(out, "mod 3") {
		t.Error("missing mod count")
	}
	if !containsVisible(out, "add 1") {
		t.Error("missing add count")
	}
}
