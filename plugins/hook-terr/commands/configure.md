---
description: Configure hook-terr Stop notification channels interactively
allowed-tools: ["PowerShell", "Read", "Write", "Edit", "AskUserQuestion"]
---

# hook-terr Configure

Configure Stop notification channels. Always ask whether to write global or project settings before modifying files.

## Steps

### 1. Read current status

Run the same status helper used by `/hook-terr`:

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

### 2. Ask scope

Use `AskUserQuestion`:

- Question: `这次 Stop 通知配置写到哪里？`
- Header: `写入范围`
- Options:
  1. `Global` — write `~/.claude/hook-terr/settings.json`; personal default across projects.
  2. `Project` — write `<current project>/.claude/hook-terr/settings.json`; only this workspace.

### 3. Ask channels

Use `AskUserQuestion` with `multiSelect: true`:

- Question: `Stop 阶段启用哪些通知通道？`
- Header: `通知通道`
- Options:
  1. `sound` — Windows `.wav` notification sound.
  2. `popup` — Windows MessageBox popup; default recommended together with sound.
  3. `windows_toast` — Windows tray balloon notification.

If the user selects no channels, stop and say no changes were made.

### 4. Write settings

Convert selected labels to a comma-separated list such as `sound,popup`. Then run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$scope = '<global-or-project>'
$channels = '<comma-separated-channels>'
$cwd = (Get-Location).Path
python (Join-Path $pluginPath 'core\settings_writer.py') --scope $scope --cwd $cwd --channels $channels
```

### 5. Confirm

Tell the user:

```text
已更新 hook-terr Stop 通知配置。
写入位置: <path printed by settings_writer.py>
Stop channels: <channels>
配置会在下一次 hook 触发时生效。
```

If `sound` is enabled, also tell the user:

```text
你启用了 sound 通道。可运行 /hook-terr:sound 试听并选择提示音。
```
