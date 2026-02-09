# CCO Statusline

Optional status line for Claude Code that shows git, model, and session info at a glance.

## What it shows

```
ClaudeCodeOptimizer:dev  ·  v3.0.0
△ 2 ▽ 0  ·  mod 1  ·  add 0  ·  del 0  ·  mv 0
Sungur  ·  CC 1.0.80  ·  Opus 4.6  ·  45K 22%
```

| Row | Content |
|-----|---------|
| 1 | Repo:branch, latest tag |
| 2 | Ahead/behind, file changes (mod/add/del/mv) |
| 3 | Username, CC version, model, context usage |

## Setup

### Install

Pre-built binaries are in the `bin/` directory. Copy the one matching your platform to `~/.claude/`.

**Mac (Apple Silicon):**
```bash
cp extras/statusline/bin/cco-statusline-darwin-arm64 ~/.claude/cco-statusline
chmod +x ~/.claude/cco-statusline
```

**Mac (Intel):**
```bash
cp extras/statusline/bin/cco-statusline-darwin-amd64 ~/.claude/cco-statusline
chmod +x ~/.claude/cco-statusline
```

**Linux (x64):**
```bash
cp extras/statusline/bin/cco-statusline-linux-amd64 ~/.claude/cco-statusline
chmod +x ~/.claude/cco-statusline
```

**Linux (ARM64):**
```bash
cp extras/statusline/bin/cco-statusline-linux-arm64 ~/.claude/cco-statusline
chmod +x ~/.claude/cco-statusline
```

**Windows:**
```powershell
Copy-Item extras\statusline\bin\cco-statusline-windows-amd64.exe ~\.claude\cco-statusline.exe
```

Add to `~/.claude/settings.json`:

**Mac / Linux:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/cco-statusline",
    "padding": 1
  }
}
```

**Windows:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "%USERPROFILE%\\.claude\\cco-statusline.exe",
    "padding": 1
  }
}
```

### Restart Claude Code

The status line appears after the first assistant message.

## Build from source

Requires [Go 1.23+](https://go.dev/dl/).

```bash
cd extras/statusline
go build -ldflags="-s -w" -o cco-statusline .
```

Cross-compile for all platforms:

```bash
GOOS=linux   GOARCH=amd64 go build -ldflags="-s -w" -o dist/cco-statusline-linux-amd64 .
GOOS=linux   GOARCH=arm64 go build -ldflags="-s -w" -o dist/cco-statusline-linux-arm64 .
GOOS=darwin  GOARCH=amd64 go build -ldflags="-s -w" -o dist/cco-statusline-darwin-amd64 .
GOOS=darwin  GOARCH=arm64 go build -ldflags="-s -w" -o dist/cco-statusline-darwin-arm64 .
GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o dist/cco-statusline-windows-amd64.exe .
```

Compress with [UPX](https://upx.github.io/) (optional, ~60% smaller):

```bash
upx --best --lzma dist/cco-statusline-*
```

## Improvements over the JS version

| Area | JS version | Go binary |
|------|------------|-----------|
| CC version | Spawns `claude --version` process | Reads `input.version` from stdin JSON (zero cost) |
| Tag lookup | `git tag --sort` (lists all tags) | `git for-each-ref --count=1` (single result) |
| Git root | Walks up 20 dirs with `statSync` | `git rev-parse --show-toplevel` (single call) |
| Git calls | Sequential (blocking) | Parallel (goroutines) |
| Timeout | 3000ms | 1500ms |
| Runtime | Requires Node.js | Standalone binary |
| Settings | Complex spawn wrapper | Direct path |

## Input format

Claude Code pipes JSON to the statusline via stdin on every update:

```json
{
  "cwd": "/path/to/project",
  "version": "1.0.80",
  "model": { "id": "claude-opus-4-6", "display_name": "Opus 4.6" },
  "context_window": {
    "total_input_tokens": 15234,
    "context_window_size": 200000,
    "used_percentage": 8,
    "current_usage": {
      "input_tokens": 8500,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  },
  "cost": { "total_cost_usd": 0.01234 },
  "vim": { "mode": "NORMAL" }
}
```

See [Claude Code docs](https://code.claude.com/docs/en/statusline) for the full schema.
