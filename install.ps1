# CCO — Claude Code Optimizer Installer (Windows)
#
# Stable (latest release):
#   irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
#
# Dev (latest dev branch):
#   iex "& { $(irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1) } --dev"

$ErrorActionPreference = "Stop"

$Repo = "sungurerdim/ClaudeCodeOptimizer"
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"
$Channel = "stable"

# Parse args (--dev / --stable)
foreach ($a in $args) {
    switch ($a) {
        "--dev"    { $Channel = "dev" }
        "--stable" { $Channel = "stable" }
    }
}

# Also honor environment variable (fallback for piped execution)
if ($env:CCO_CHANNEL -and $Channel -eq "stable") { $Channel = $env:CCO_CHANNEL }

$RulesFiles = @("rules/cco-rules.md")
$CommandFiles = @(
    "commands/cco-optimize.md"
    "commands/cco-align.md"
    "commands/cco-commit.md"
    "commands/cco-research.md"
    "commands/cco-preflight.md"
    "commands/cco-docs.md"
    "commands/cco-update.md"
)
$AgentFiles = @(
    "agents/cco-agent-analyze.md"
    "agents/cco-agent-apply.md"
    "agents/cco-agent-research.md"
)

function Write-Info  { param($Msg) Write-Host $Msg -ForegroundColor Cyan }
function Write-Ok    { param($Msg) Write-Host $Msg -ForegroundColor Green }
function Write-Err   { param($Msg) Write-Host $Msg -ForegroundColor Red }

Write-Info "CCO Installer"
Write-Info "============="

# Resolve channel to a git ref
if ($Channel -eq "dev") {
    $Ref = "dev"
    Write-Info "Channel: dev (latest commit)"
} else {
    try {
        $Tags = Invoke-RestMethod "https://api.github.com/repos/$Repo/tags?per_page=1" -UseBasicParsing
        if ($Tags -and $Tags.Count -gt 0) {
            $Ref = $Tags[0].name
            Write-Info "Channel: stable ($Ref)"
        } else {
            $Ref = "main"
            Write-Info "Channel: stable (main - no tags found)"
        }
    } catch {
        $Ref = "main"
        Write-Info "Channel: stable (main - API unavailable)"
    }
}

$BaseUrl = "https://raw.githubusercontent.com/$Repo/$Ref"

# Create directories
foreach ($Dir in @("rules", "commands", "agents")) {
    $Path = Join-Path $ClaudeDir $Dir
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Install-File {
    param($File)
    $Url = "$BaseUrl/$File"
    $Dest = Join-Path $ClaudeDir $File
    try {
        Invoke-WebRequest -Uri $Url -OutFile $Dest -UseBasicParsing
        Write-Ok "  + $File"
        return $true
    } catch {
        Write-Err "  ! $File (download failed)"
        return $false
    }
}

$Failed = 0

Write-Info ""
Write-Info "Installing rules..."
foreach ($File in $RulesFiles) {
    if (-not (Install-File $File)) { $Failed++ }
}

Write-Info ""
Write-Info "Installing commands..."
foreach ($File in $CommandFiles) {
    if (-not (Install-File $File)) { $Failed++ }
}

Write-Info ""
Write-Info "Installing agents..."
foreach ($File in $AgentFiles) {
    if (-not (Install-File $File)) { $Failed++ }
}

# Update version frontmatter with current timestamp
$RulesPath = Join-Path $ClaudeDir "rules\cco-rules.md"
if (Test-Path $RulesPath) {
    $Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $Content = Get-Content $RulesPath -Raw
    $Content = $Content -replace "last_update_check:.*", "last_update_check: $Timestamp"
    Set-Content -Path $RulesPath -Value $Content -NoNewline
}

# Clean up env var
if ($env:CCO_CHANNEL) { Remove-Item Env:CCO_CHANNEL -ErrorAction SilentlyContinue }

Write-Info ""
if ($Failed -eq 0) {
    Write-Ok "CCO installed successfully! ($Ref)"
    Write-Info ""
    Write-Info "Installed to: $ClaudeDir\"
    Write-Info "  rules\cco-rules.md"
    Write-Info "  commands\cco-*.md (7 commands)"
    Write-Info "  agents\cco-agent-*.md (3 agents)"
    Write-Info ""
    Write-Info "Restart Claude Code to activate."
    Write-Info "Run /cco-optimize to get started."
} else {
    Write-Err "Installation completed with $Failed error(s)."
    Write-Err "Re-run the installer or download files manually."
    exit 1
}
