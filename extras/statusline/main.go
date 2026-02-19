package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

func buildStatusline(input *Input, git *GitInfo) string {
	row1 := buildLocationRow(input, git)
	row2 := buildStatusRow(git)
	row3 := buildSessionRow(input)
	row4 := buildWorkspaceRow(input)

	maxW := minRowWidth(row1)
	if w := minRowWidth(row2); w > maxW {
		maxW = w
	}
	if w := minRowWidth(row3); w > maxW {
		maxW = w
	}
	if row4 != nil {
		if w := minRowWidth(row4); w > maxW {
			maxW = w
		}
	}

	var out bytes.Buffer
	out.WriteString(justifyRow(row1, maxW, "\u00B7"))
	out.WriteByte('\n')
	out.WriteString(justifyRow(row2, maxW, "\u00B7"))
	out.WriteByte('\n')
	out.WriteString(justifyRow(row3, maxW, "\u00B7"))
	out.WriteByte('\n')
	if row4 != nil {
		out.WriteString(justifyRow(row4, maxW, "\u00B7"))
		out.WriteByte('\n')
	}
	out.WriteString("\u200B\n") // empty line with zero-width space

	return out.String()
}

// ============================================================================
// MAIN
// ============================================================================

func main() {
	const maxStdinSize = 10 << 20 // 10 MB
	data, err := io.ReadAll(io.LimitReader(os.Stdin, maxStdinSize))
	if err != nil {
		fmt.Fprintf(os.Stderr, "[Statusline Error: %v]\n", err)
		return
	}

	var input Input
	if err := json.Unmarshal(data, &input); err != nil {
		fmt.Fprintf(os.Stderr, "[Statusline Error: %v]\n", err)
		return
	}
	if input.CWD == "" {
		input.CWD = "."
	}

	git := getGitInfo()
	fmt.Print(buildStatusline(&input, git))
}
