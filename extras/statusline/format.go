package main

import (
	"bytes"
	"fmt"
	"strconv"
	"strings"
	"unicode/utf8"
)

func formatModelName(name string) string {
	name = strings.TrimPrefix(name, "Claude ")
	if name == "" {
		return "Unknown"
	}
	return name
}

func formatK(n int64) string {
	if n >= 1000 {
		return strconv.FormatInt((n+500)/1000, 10) + "K"
	}
	return strconv.FormatInt(n, 10)
}

func formatContextUsage(input *Input) string {
	cw := input.ContextWindow
	if cw == nil || cw.ContextWindowSize == 0 {
		return ""
	}

	var tokens int64
	if cw.CurrentUsage != nil {
		tokens = cw.CurrentUsage.InputTokens +
			cw.CurrentUsage.CacheCreationInputTokens +
			cw.CurrentUsage.CacheReadInputTokens
	} else {
		tokens = cw.TotalInputTokens
	}

	percent := tokens * 100 / cw.ContextWindowSize
	return fmt.Sprintf("%s %d%%", formatK(tokens), percent)
}

// visibleLen returns the display width of a string, excluding ANSI escape codes
func visibleLen(s string) int {
	inEsc := false
	n := 0
	for i := 0; i < len(s); {
		if s[i] == '\x1b' {
			inEsc = true
			i++
			continue
		}
		if inEsc {
			if s[i] == 'm' {
				inEsc = false
			}
			i++
			continue
		}
		_, size := utf8.DecodeRuneInString(s[i:])
		n++
		i += size
	}
	return n
}

// justifyRow distributes parts evenly across targetWidth with separator
func justifyRow(parts []string, targetWidth int, sep string) string {
	if len(parts) == 0 {
		return ""
	}
	if len(parts) == 1 {
		return parts[0]
	}

	gaps := len(parts) - 1
	contentWidth := 0
	for _, p := range parts {
		contentWidth += visibleLen(p)
	}
	sepWidth := gaps // each separator is 1 visible char
	available := targetWidth - contentWidth - sepWidth
	if available < 0 {
		available = 0
	}

	perGap := available / gaps
	extra := available % gaps

	var buf bytes.Buffer
	buf.WriteString(parts[0])

	for i := 1; i < len(parts); i++ {
		gap := perGap
		if i <= extra {
			gap++
		}
		left := gap / 2
		right := gap - left
		for j := 0; j < left; j++ {
			buf.WriteByte(' ')
		}
		buf.WriteString(c(sep, gray))
		for j := 0; j < right; j++ {
			buf.WriteByte(' ')
		}
		buf.WriteString(parts[i])
	}

	return buf.String()
}

func minRowWidth(parts []string) int {
	w := 0
	for _, p := range parts {
		w += visibleLen(p)
	}
	// " · " = 3 chars between each part
	return w + (len(parts)-1)*3
}
