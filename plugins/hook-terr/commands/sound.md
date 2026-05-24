---
description: Preview and choose the hook-terr sound notification
allowed-tools: ["PowerShell", "AskUserQuestion"]
---

# hook-terr Sound

Configure the global `sound` channel notification. Keep the default path fast, and use the external picker only when the user wants to preview sounds.

## Built-in sound aliases

Use this mapping when the user returns with an id or alias after running the picker:

| id | alias | wavPath |
|---:|---|---|
| 1 | `tada` | `C:\Windows\Media\tada.wav` |
| 2 | `notify` | `C:\Windows\Media\notify.wav` |
| 3 | `windows-notify` | `C:\Windows\Media\Windows Notify System Generic.wav` |
| 4 | `windows-ding` | `C:\Windows\Media\Windows Ding.wav` |
| 5 | `chimes` | `C:\Windows\Media\chimes.wav` |
| 6 | `ding` | `C:\Windows\Media\ding.wav` |
| 7 | `chord` | `C:\Windows\Media\chord.wav` |
| 8 | `windows-balloon` | `C:\Windows\Media\Windows Balloon.wav` |
| 9 | `windows-default` | `C:\Windows\Media\Windows Default.wav` |
| 10 | `windows-exclamation` | `C:\Windows\Media\Windows Exclamation.wav` |
| 11 | `windows-foreground` | `C:\Windows\Media\Windows Foreground.wav` |
| 12 | `windows-message-nudge` | `C:\Windows\Media\Windows Message Nudge.wav` |
| 13 | `alarm01` | `C:\Windows\Media\Alarm01.wav` |
| 14 | `alarm02` | `C:\Windows\Media\Alarm02.wav` |
| 15 | `ring01` | `C:\Windows\Media\Ring01.wav` |
| 16 | `windows-error` | `C:\Windows\Media\Windows Error.wav` |

## Steps

### 1. Locate plugin root

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$pluginPath = if ($env:CLAUDE_PLUGIN_ROOT) {
    $env:CLAUDE_PLUGIN_ROOT
} else {
    (Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\hook-terr\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1).FullName
}
if (-not $pluginPath) { Write-Output 'ERROR: hook-terr plugin path not found'; exit 1 }
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
```

### 2. Ask setup mode

Use `AskUserQuestion`:

- Question: `要如何设置 sound 提示音？`
- Header: `sound`
- Options:
  1. `Use default` — immediately save `C:\Windows\Media\tada.wav`.
  2. `Open picker` — open the external PowerShell picker so the user can preview sounds outside Claude Code.
  3. `Cancel` — make no changes.

### 3. Apply default

If the user chooses `Use default`, run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$cwd = (Get-Location).Path
python (Join-Path $pluginPath 'core\settings_writer.py') --cwd $cwd --sound-wav-path 'C:\Windows\Media\tada.wav'
```

Then tell the user:

```text
已更新 hook-terr sound 提示音。
写入位置: <path printed by settings_writer.py>
sound wavPath: C:\Windows\Media\tada.wav
配置会在下一次 hook 触发时生效。
```

### 4. Open picker

If the user chooses `Open picker`, run:

```powershell
$pickerPath = Join-Path $pluginPath 'scripts\sound_picker.ps1'
if (-not (Test-Path -LiteralPath $pickerPath)) { Write-Output "ERROR: sound picker not found: $pickerPath"; exit 1 }
Start-Process powershell.exe -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-NoExit', '-File', ('"{0}"' -f $pickerPath))
```

Then tell the user:

```text
请在 sound picker 里试听。选好后，把 id、alias 或 wavPath 发回来，例如：选 1 / 用 tada / C:\Windows\Media\tada.wav。
```

### 5. Apply returned choice

If the user returns with an id, alias, or wavPath, map it using the built-in table above. Validate the selected path exists with `Test-Path`, then run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$wavPath = '<selected-wav-path>'
if (-not (Test-Path -LiteralPath $wavPath)) { Write-Output "ERROR: sound file not found: $wavPath"; exit 1 }
$cwd = (Get-Location).Path
python (Join-Path $pluginPath 'core\settings_writer.py') --cwd $cwd --sound-wav-path $wavPath
```

Confirm with the same message format as Step 3.
