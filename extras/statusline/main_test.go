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

// ============================================================================
// parseGitStatus
// ============================================================================

func TestParseGitStatus_BranchAndAheadBehind(t *testing.T) {
	status := "# branch.oid abc123\n# branch.head feature/test\n# branch.ab +3 -1"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Branch != "feature/test" {
		t.Errorf("Branch = %q, want \"feature/test\"", info.Branch)
	}
	if info.Ahead != 3 {
		t.Errorf("Ahead = %d, want 3", info.Ahead)
	}
	if info.Behind != 1 {
		t.Errorf("Behind = %d, want 1", info.Behind)
	}
}

func TestParseGitStatus_ModifiedFiles(t *testing.T) {
	// "1 .M ..." = working tree modified; "1 M. ..." = index modified
	status := "# branch.head main\n1 .M N... 100644 100644 100644 abc def file1.go\n1 M. N... 100644 100644 100644 abc def file2.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Mod != 2 {
		t.Errorf("Mod = %d, want 2 (1 wt + 1 idx)", info.Mod)
	}
}

func TestParseGitStatus_AddedDeletedRenamed(t *testing.T) {
	status := "# branch.head main\n1 A. N... 100644 100644 100644 abc def added.go\n1 .D N... 100644 100644 100644 abc def deleted.go\n2 R. N... 100644 100644 100644 abc def old.go\tnew.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Add != 1 {
		t.Errorf("Add = %d, want 1", info.Add)
	}
	if info.Del != 1 {
		t.Errorf("Del = %d, want 1", info.Del)
	}
	if info.Ren != 1 {
		t.Errorf("Ren = %d, want 1", info.Ren)
	}
}

func TestParseGitStatus_UntrackedFiles(t *testing.T) {
	status := "# branch.head main\n? newfile.go\n? another.txt"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Add != 2 {
		t.Errorf("Add = %d, want 2 (untracked)", info.Add)
	}
}

func TestParseGitStatus_Conflicts(t *testing.T) {
	status := "# branch.head main\nu UU N... 100644 100644 100644 100644 abc def ghi conflict.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Conflict != 1 {
		t.Errorf("Conflict = %d, want 1", info.Conflict)
	}
}

func TestParseGitStatus_EmptyOutput(t *testing.T) {
	info := &GitInfo{}
	parseGitStatus("", info)
	if info.Branch != "" {
		t.Errorf("Branch = %q, want empty", info.Branch)
	}
}

func TestParseGitStatus_ShortLine(t *testing.T) {
	// Lines shorter than 4 chars for "1 " prefix should be skipped
	status := "# branch.head main\n1 M"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Mod != 0 {
		t.Errorf("Mod = %d, want 0 (short line skipped)", info.Mod)
	}
}

func TestParseGitStatus_CopiedFile(t *testing.T) {
	status := "# branch.head main\n1 C. N... 100644 100644 100644 abc def copied.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Add != 1 {
		t.Errorf("Add = %d, want 1 (copied counts as add)", info.Add)
	}
}

func TestParseGitStatus_BothIndexAndWorkTree(t *testing.T) {
	// "1 MM ..." = modified in both index and working tree
	status := "# branch.head main\n1 MM N... 100644 100644 100644 abc def file.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Mod != 2 {
		t.Errorf("Mod = %d, want 2 (idx M + wt M)", info.Mod)
	}
}

func TestParseGitStatus_StagedDelete(t *testing.T) {
	status := "# branch.head main\n1 D. N... 100644 100644 100644 abc def removed.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Del != 1 {
		t.Errorf("Del = %d, want 1 (staged delete)", info.Del)
	}
}

func TestParseGitStatus_MixedChanges(t *testing.T) {
	status := "# branch.head develop\n# branch.ab +5 -2\n1 M. N... 100644 100644 100644 a b mod1.go\n1 .M N... 100644 100644 100644 a b mod2.go\n1 A. N... 100644 100644 100644 a b new.go\n1 .D N... 100644 100644 100644 a b gone.go\n? untracked.txt\nu UU N... 100644 100644 100644 100644 a b c merge.go"
	info := &GitInfo{}
	parseGitStatus(status, info)
	if info.Branch != "develop" {
		t.Errorf("Branch = %q, want \"develop\"", info.Branch)
	}
	if info.Ahead != 5 {
		t.Errorf("Ahead = %d, want 5", info.Ahead)
	}
	if info.Behind != 2 {
		t.Errorf("Behind = %d, want 2", info.Behind)
	}
	if info.Mod != 2 {
		t.Errorf("Mod = %d, want 2", info.Mod)
	}
	if info.Add != 2 {
		t.Errorf("Add = %d, want 2 (1 staged + 1 untracked)", info.Add)
	}
	if info.Del != 1 {
		t.Errorf("Del = %d, want 1", info.Del)
	}
	if info.Conflict != 1 {
		t.Errorf("Conflict = %d, want 1", info.Conflict)
	}
}

// ============================================================================
// visibleLen — multibyte/edge cases
// ============================================================================

func TestVisibleLen_Emoji(t *testing.T) {
	// Each emoji is one rune (even if 4 bytes in UTF-8)
	if got := visibleLen("🎉🚀"); got != 2 {
		t.Errorf("visibleLen(emoji) = %d, want 2", got)
	}
}

func TestVisibleLen_CJK(t *testing.T) {
	// Each CJK character is one rune
	if got := visibleLen("日本語"); got != 3 {
		t.Errorf("visibleLen(CJK) = %d, want 3", got)
	}
}

func TestVisibleLen_ANSIAtEnd(t *testing.T) {
	// ANSI code at end without text after it
	s := "hello\x1b[0m"
	if got := visibleLen(s); got != 5 {
		t.Errorf("visibleLen(trailing ANSI) = %d, want 5", got)
	}
}

func TestVisibleLen_ConsecutiveANSI(t *testing.T) {
	// Two ANSI codes back-to-back with no text between
	s := "\x1b[92m\x1b[1mhello\x1b[0m"
	if got := visibleLen(s); got != 5 {
		t.Errorf("visibleLen(consecutive ANSI) = %d, want 5", got)
	}
}

// ============================================================================
// buildLocationRow / buildStatusRow / buildSessionRow
// ============================================================================

func TestBuildLocationRow_NoGit(t *testing.T) {
	input := &Input{CWD: "/home/user/myproject"}
	row := buildLocationRow(input, nil)
	if len(row) != 1 {
		t.Fatalf("expected 1 element, got %d", len(row))
	}
	if !containsVisible(row[0], "myproject") {
		t.Error("missing project name in location row")
	}
}

func TestBuildLocationRow_WithGitAndTag(t *testing.T) {
	input := &Input{CWD: "/home/user/repo"}
	git := &GitInfo{Branch: "dev", RepoName: "repo", Tag: "v2.0.0"}
	row := buildLocationRow(input, git)
	if len(row) != 2 {
		t.Fatalf("expected 2 elements (repo:branch + tag), got %d", len(row))
	}
	if !containsVisible(row[0], "repo:dev") {
		t.Error("missing repo:branch")
	}
	if !containsVisible(row[1], "v2.0.0") {
		t.Error("missing tag")
	}
}

func TestBuildStatusRow_NoGit(t *testing.T) {
	row := buildStatusRow(nil)
	if len(row) != 1 {
		t.Fatalf("expected 1 element, got %d", len(row))
	}
	if !containsVisible(row[0], "No git") {
		t.Error("missing 'No git'")
	}
}

func TestBuildStatusRow_WithConflict(t *testing.T) {
	git := &GitInfo{Branch: "main", Ahead: 1, Behind: 0, Conflict: 2, Mod: 1}
	row := buildStatusRow(git)
	// Should have 5 elements: alert + mod + add + del + mv
	if len(row) != 5 {
		t.Fatalf("expected 5 elements, got %d", len(row))
	}
	if !containsVisible(row[0], "2 conflict") {
		t.Error("missing conflict count")
	}
}
