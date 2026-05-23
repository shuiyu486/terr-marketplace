---
description: Preview and choose the hook-terr sound notification
allowed-tools: ["PowerShell", "AskUserQuestion"]
---

# hook-terr Sound

Preview Windows `.wav` notification sounds and save one as the global `sound` channel notification.

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

### 2. Ask sound group

Use `AskUserQuestion`:

- Question: `想试听哪一类 sound 提示音？`
- Header: `声音分类`
- Options:
  1. `Recommended` — `tada`, `notify`, `Windows Notify`, `Windows Ding`.
  2. `Classic` — `chimes`, `ding`, `chord`, `Windows Balloon`.
  3. `Windows` — `Windows Default`, `Windows Exclamation`, `Windows Foreground`, `Windows Message Nudge`.
  4. `Alerts` — `Alarm01`, `Alarm02`, `Ring01`, `Windows Error`.

### 3. Ask sound in selected group

Use `AskUserQuestion` with the selected group options:

Recommended:
- `tada` — `C:\Windows\Media\tada.wav`; recommended default.
- `notify` — `C:\Windows\Media\notify.wav`; short classic notification.
- `Windows Notify` — `C:\Windows\Media\Windows Notify System Generic.wav`; Windows notification style.
- `Windows Ding` — `C:\Windows\Media\Windows Ding.wav`; short ding.

Classic:
- `chimes` — `C:\Windows\Media\chimes.wav`.
- `ding` — `C:\Windows\Media\ding.wav`.
- `chord` — `C:\Windows\Media\chord.wav`.
- `Windows Balloon` — `C:\Windows\Media\Windows Balloon.wav`.

Windows:
- `Windows Default` — `C:\Windows\Media\Windows Default.wav`.
- `Windows Exclamation` — `C:\Windows\Media\Windows Exclamation.wav`.
- `Windows Foreground` — `C:\Windows\Media\Windows Foreground.wav`.
- `Windows Message Nudge` — `C:\Windows\Media\Windows Message Nudge.wav`.

Alerts:
- `Alarm01` — `C:\Windows\Media\Alarm01.wav`.
- `Alarm02` — `C:\Windows\Media\Alarm02.wav`.
- `Ring01` — `C:\Windows\Media\Ring01.wav`.
- `Windows Error` — `C:\Windows\Media\Windows Error.wav`.

### 4. Play selected sound

Run:

```powershell
$wavPath = '<selected-wav-path>'
if (-not (Test-Path -LiteralPath $wavPath)) { Write-Output "ERROR: sound file not found: $wavPath"; exit 1 }
$player = New-Object System.Media.SoundPlayer $wavPath
$player.Load()
$player.PlaySync()
```

### 5. Ask whether to save or preview another

Use `AskUserQuestion`:

- Question: `要把刚才试听的声音保存为 sound 提示音吗？`
- Header: `保存`
- Options:
  1. `Save` — write this sound to global `~/.claude/hook-terr/settings.json`.
  2. `Preview another` — go back to step 2.
  3. `Cancel` — make no changes.

### 6. Save global setting

Only when the user chooses `Save`, run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$cwd = (Get-Location).Path
python (Join-Path $pluginPath 'core\settings_writer.py') --cwd $cwd --sound-wav-path '<selected-wav-path>'
```

### 7. Confirm

Tell the user:

```text
已更新 hook-terr sound 提示音。
写入位置: <path printed by settings_writer.py>
sound wavPath: <selected-wav-path>
配置会在下一次 hook 触发时生效。
```
