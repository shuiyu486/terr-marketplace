---
description: Show hook-terr effective hook and notification configuration
allowed-tools: ["PowerShell", "Read", "Glob"]
---

# hook-terr Status

Show the current effective `hook-terr` hook and notification configuration. Do not modify files.

## Steps

1. Locate the plugin root. Prefer `$env:CLAUDE_PLUGIN_ROOT` when set; otherwise use the installed plugin directory for `hook-terr`.
2. Run the status helper:

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$pluginPath = if ($env:CLAUDE_PLUGIN_ROOT) {
    $env:CLAUDE_PLUGIN_ROOT
} else {
    (Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\hook-terr\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1).FullName
}
if (-not $pluginPath) { Write-Output 'ERROR: hook-terr plugin path not found'; exit 1 }
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$env:HOOK_TERR_CWD = (Get-Location).Path
python (Join-Path $pluginPath 'core\config_status.py')
```

3. Summarize the JSON for the user in Chinese:
   - Plugin root
   - Current cwd
   - Existing settings/rule files
   - Whether hook-terr is enabled
   - Whether `features.apiErrorRecovery.enabled` is enabled, plus its strategy, terminal, primary/fallback model commands, and timing window when present
   - Stop effective channels
   - `notifications.sound.enabled` and `notifications.sound.wavPath`
   - `notifications.windows_toast.enabled`, `notifications.popup.enabled`
   - Matched Stop rule id and decision
   - Diagnostics, if any

4. End by saying: `运行 /hook-terr:configure 可以修改启用 notify 的 Stop 规则所使用的通知通道；运行 /hook-terr:api-error-recovery 可以为当前目录配置 API error 自动恢复。`
