---
description: Restart cc-statusline by stopping its running statusline Node processes
allowed-tools: ["Bash", "PowerShell"]
---

# cc-statusline Restart

Restart the long-running cc-statusline process without changing configuration or rebuilding. Claude Code will start it again on the next status-line refresh.

This command only targets Node processes whose command line points at:

```text
plugins/cache/terr-marketplace/cc-statusline/*/dist/index.js
```

It does not stop unrelated Node.js processes.

## Windows (PowerShell)

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$cacheRootForMatch = (Join-Path $claudeDir 'plugins\cache\terr-marketplace\cc-statusline') -replace '\\','/'
$escapedRoot = [regex]::Escape($cacheRootForMatch)
$pattern = "$escapedRoot/.+/dist/index\.js"
$matches = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'node.exe' -and (($_.CommandLine -replace '\\','/') -match $pattern)
})

foreach ($proc in $matches) {
    Stop-Process -Id $proc.ProcessId -Force -Confirm:$false
}

Write-Output "Restarted cc-statusline processes: $($matches.Count)"
```

## macOS / Linux

```bash
CACHE_ROOT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline"
STOPPED=0
while IFS= read -r pid; do
    kill "$pid" 2>/dev/null && STOPPED=$((STOPPED + 1))
done < <(ps -eo pid=,args= | awk -v root="$CACHE_ROOT" '$0 ~ /node/ && index($0, root) && $0 ~ /\/dist\/index\.js/ { print $1 }')
echo "Restarted cc-statusline processes: $STOPPED"
```

Tell the user:

> cc-statusline restart requested. Claude Code will launch a fresh status line process on the next refresh.
