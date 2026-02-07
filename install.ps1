# CCO — Claude Code Optimizer Installer (Windows)
#
# Stable (latest release):
#   irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
#
# Dev (latest dev branch):
#   iex "& { $(irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/dev/install.ps1) } --dev"

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
# v2.x commands without cco- prefix (must be hardcoded, no distinguishing pattern)
$LegacyNonPrefixedFiles = @(
    "commands/optimize.md"
    "commands/align.md"
    "commands/commit.md"
    "commands/research.md"
    "commands/preflight.md"
    "commands/docs.md"
    "commands/tune.md"
)
# v2.x directories to remove entirely
$LegacyDirs = @(
    "commands/schemas"
    "rules/core"
    "rules/frameworks"
    "rules/languages"
    "rules/operations"
    "hooks"
)
# Current v3 files to keep (everything else matching cco-* gets removed)
$CurrentCommands = $CommandFiles | ForEach-Object { Split-Path $_ -Leaf }
$CurrentAgents = $AgentFiles | ForEach-Object { Split-Path $_ -Leaf }
$CurrentRules = @("cco-rules.md")

function Write-Info  { param($Msg) Write-Host $Msg -ForegroundColor Cyan }
function Write-Ok    { param($Msg) Write-Host $Msg -ForegroundColor Green }
function Write-Warn  { param($Msg) Write-Host $Msg -ForegroundColor Yellow }
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

# Preflight: verify the resolved ref has the expected file structure
Write-Info ""
Write-Info "Verifying source..."
try {
    $TestUrl = "$BaseUrl/rules/cco-rules.md"
    $TestContent = Invoke-WebRequest -Uri $TestUrl -UseBasicParsing -ErrorAction Stop
    $TestBody = $TestContent.Content
    if (-not $TestBody -or -not $TestBody.StartsWith("---")) {
        throw "Invalid content"
    }
    Write-Ok "  Source verified ($Ref)"
} catch {
    Write-Err "  Source verification failed: $Ref does not contain CCO files."
    Write-Err ""
    if ($Channel -eq "stable") {
        Write-Err "  The latest release tag ($Ref) predates the install-script distribution model."
        Write-Err "  Use the dev channel until a new release is published:"
        Write-Err ""
        Write-Err "    iex ""& { `$(irm https://raw.githubusercontent.com/$Repo/dev/install.ps1) } --dev"""
        Write-Err ""
    } else {
        Write-Err "  Could not download files from the '$Ref' ref."
        Write-Err "  Check the repository URL and try again."
    }
    exit 1
}

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
        $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing -ErrorAction Stop
        $Body = $Response.Content

        # Validate: CCO markdown files must start with YAML frontmatter
        if (-not $Body -or -not $Body.StartsWith("---")) {
            Write-Err "  ! $File (invalid content - not a CCO file)"
            return $false
        }

        # Write validated content to disk
        [System.IO.File]::WriteAllText($Dest, $Body)
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

# Clean up legacy files from previous CCO versions (v1.x + v2.x)
$LegacyCleaned = 0

# Uninstall v2.x plugin if present (files managed by Claude Code plugin system)
$ClaudeCli = Get-Command claude -ErrorAction SilentlyContinue
if ($ClaudeCli) {
    & claude plugin uninstall "cco@ClaudeCodeOptimizer" 2>$null | Out-Null
    & claude plugin marketplace remove "ClaudeCodeOptimizer" 2>$null | Out-Null
}

# Uninstall v1.x pip package if present
$PipCmd = Get-Command pip -ErrorAction SilentlyContinue
if ($PipCmd) {
    & pip uninstall claude-code-optimizer -y 2>$null | Out-Null
}

# Remove v2.x non-prefixed command files
foreach ($File in $LegacyNonPrefixedFiles) {
    $LegacyPath = Join-Path $ClaudeDir $File
    if (Test-Path $LegacyPath) {
        Remove-Item -Path $LegacyPath -Force -ErrorAction SilentlyContinue
        $LegacyCleaned++
    }
}

# Remove any cco-*.md in commands/ that is NOT a current v3 command
$CmdDir = Join-Path $ClaudeDir "commands"
if (Test-Path $CmdDir) {
    Get-ChildItem -Path $CmdDir -Filter "cco-*.md" | Where-Object { $CurrentCommands -notcontains $_.Name } | ForEach-Object {
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        $LegacyCleaned++
    }
}

# Remove any cco-*.md in agents/ that is NOT a current v3 agent
$AgentDir = Join-Path $ClaudeDir "agents"
if (Test-Path $AgentDir) {
    Get-ChildItem -Path $AgentDir -Filter "cco-*.md" | Where-Object { $CurrentAgents -notcontains $_.Name } | ForEach-Object {
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        $LegacyCleaned++
    }
}

# Remove any cco-*.md in rules/ that is NOT cco-rules.md
$RulesDir = Join-Path $ClaudeDir "rules"
if (Test-Path $RulesDir) {
    Get-ChildItem -Path $RulesDir -Filter "cco-*.md" | Where-Object { $CurrentRules -notcontains $_.Name } | ForEach-Object {
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        $LegacyCleaned++
    }
}

# Remove legacy directories
foreach ($Dir in $LegacyDirs) {
    $LegacyPath = Join-Path $ClaudeDir $Dir
    if (Test-Path $LegacyPath) {
        Remove-Item -Path $LegacyPath -Recurse -Force -ErrorAction SilentlyContinue
        $LegacyCleaned++
    }
}

# Update version frontmatter with current timestamp
$RulesPath = Join-Path $ClaudeDir "rules\cco-rules.md"
if (Test-Path $RulesPath) {
    $Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $Content = Get-Content $RulesPath -Raw -Encoding UTF8
    $Content = $Content -replace "last_update_check:.*", "last_update_check: $Timestamp"
    [System.IO.File]::WriteAllText($RulesPath, $Content)
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
    if ($LegacyCleaned -gt 0) {
        Write-Info ""
        Write-Warn "Cleaned up $LegacyCleaned legacy file(s) from previous CCO version."
    }
    Write-Info ""
    Write-Info "Restart Claude Code to activate."
    Write-Info "Run /cco-optimize to get started."
} else {
    Write-Err "Installation completed with $Failed error(s)."
    Write-Err "Re-run the installer or download files manually."
    exit 1
}
