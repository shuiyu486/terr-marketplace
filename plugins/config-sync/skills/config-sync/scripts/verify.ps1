<#
.SYNOPSIS
    Verify config file syntax and integrity after sync
.DESCRIPTION
    Checks file size sanity, BOM detection, and WezTerm availability.
    Exit code 0 = all good, 1 = issues found.
.PARAMETER ConfigDir
    Directory containing config files to verify (local env or ccNovaTerm config/)
.PARAMETER Mode
    "local" or "project" - affects which checks run
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$ConfigDir,
    [ValidateSet("local","project")]
    [string]$Mode = "local"
)

$ErrorActionPreference = 'Continue'
$issues = 0

function Write-OK([string]$msg) { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-NG([string]$msg) { Write-Host "  [NG] $msg" -ForegroundColor Red; $script:issues++ }

Write-Host "Verifying configs in: $ConfigDir" -ForegroundColor Cyan

# --- BOM detection (EF BB BF breaks Nushell alias parsing) ---
Write-Host "Checking for BOM..." -ForegroundColor Cyan
$bomFiles = @()
$checkFiles = @(".wezterm.lua", "config.nu", "env.nu", "starship.toml", "yazi\yazi.toml", "yazi\keymap.toml", "yazi\package.toml")
foreach ($f in $checkFiles) {
    $fp = Join-Path $ConfigDir $f
    if (-not (Test-Path $fp)) { continue }
    $bytes = [System.IO.File]::ReadAllBytes($fp)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-NG "$f starts with BOM - will break Nushell alias parsing"
        $bomFiles += $f
    }
}
if ($bomFiles.Count -eq 0) { Write-OK "No BOM detected" }

# --- File size sanity ---
$files = @(".wezterm.lua", "config.nu", "env.nu", "starship.toml", "yazi\yazi.toml", "yazi\keymap.toml", "yazi\package.toml")
foreach ($f in $files) {
    $fp = Join-Path $ConfigDir $f
    if (Test-Path $fp) {
        $size = (Get-Item $fp).Length
        if ($size -gt 10) { Write-OK "$f ($size bytes)" }
        else { Write-NG "$f too small ($size bytes) - may be corrupted" }
    }
}

# --- wezterm.lua basic structure ---
$weztermPath = Join-Path $ConfigDir ".wezterm.lua"
if (Test-Path $weztermPath) {
    $luaContent = Get-Content $weztermPath -Raw
    if ($luaContent -match 'return config') {
        Write-OK ".wezterm.lua has return statement"
    } else {
        Write-NG ".wezterm.lua missing 'return config'"
    }
}

# --- Unicode integrity (starship.toml Nerd Font PUA characters) ---
$starshipPath = Join-Path $ConfigDir "starship.toml"
if (Test-Path $starshipPath) {
    try {
        $rawBytes = [System.IO.File]::ReadAllBytes($starshipPath)
        $utf8Content = [System.Text.Encoding]::UTF8.GetString($rawBytes)
        # Check for common encoding corruption markers: CJK chars where PUA chars should be
        $corruptionMarkers = @([char]0x9850, [char]0x79B2, [char]0x7669, [char]0x997E, [char]0x715D)
        $foundCorruption = $false
        foreach ($m in $corruptionMarkers) {
            if ($utf8Content.Contains($m)) { $foundCorruption = $true; break }
        }
        if ($foundCorruption) {
            Write-NG "starship.toml has CJK replacement characters; Nerd Font PUA chars may be corrupted. Re-write with UTF-8 encoding."
        } else {
            Write-OK "starship.toml Unicode integrity"
        }
    } catch {
        Write-NG "starship.toml encoding check failed: $_"
    }
}

# --- Yazi package lock sanity ---
$yaziPackagePath = Join-Path $ConfigDir "yazi\package.toml"
if (Test-Path $yaziPackagePath) {
    $pkgContent = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($yaziPackagePath))
    if ($pkgContent -match 'yazi-rs/plugins:toggle-pane') {
        Write-OK "yazi/package.toml includes toggle-pane dependency"
    } else {
        Write-NG "yazi/package.toml missing toggle-pane dependency"
    }
}

# --- WezTerm availability (only for local mode) ---
if ($Mode -eq "local") {
    try {
        $weztermOut = wezterm cli list 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-OK "wezterm is running"
        } else {
            Write-OK "wezterm cli available (not running or no windows)"
        }
    } catch {
        Write-OK "wezterm not on PATH (ok if not installed yet)"
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
if ($issues -eq 0) {
    Write-Host "  All checks passed" -ForegroundColor Green
    exit 0
} else {
    Write-Host "  $issues issue(s) found" -ForegroundColor Red
    exit 1
}
