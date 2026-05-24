# hook-terr Sound Fast Picker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `/hook-terr:sound` faster by adding a default-sound quick path, moving sound preview into an external PowerShell picker, and ensuring `/hook-terr:configure` initializes the default sound when `sound` is enabled.

**Architecture:** Keep configuration writes centralized in `core/settings_writer.py`. Add a standalone `scripts/sound_picker.ps1` that only previews sounds and prints the selected id/alias/path; it never writes settings. Simplify `commands/sound.md` so Claude Code asks one top-level question, opens the picker only when requested, then writes the selected wav path through the existing Python writer.

**Tech Stack:** Claude Code slash command markdown, PowerShell 5.1, Python stdlib `unittest`, JSON settings files.

---

## File Structure

- Modify: `plugins/hook-terr/core/settings_writer.py`
  - Add a default sound path constant.
  - Ensure `write_stop_channels(..., channels=[..., "sound", ...])` explicitly initializes `notifications.sound.wavPath` to the default when missing.
  - Keep existing `write_sound()` behavior for custom wav path updates.

- Create: `plugins/hook-terr/scripts/sound_picker.ps1`
  - Display the 16 built-in Windows wav candidates.
  - Let the user preview by entering an id or alias.
  - Let the user confirm a selection.
  - Print a final machine-readable `wavPath: ...` line for easy copy-back.
  - Do not modify any settings files.

- Modify: `plugins/hook-terr/commands/sound.md`
  - Replace the current group-by-group preview flow.
  - Add one top-level choice: `Use default`, `Open picker`, `Cancel`.
  - Save default immediately when requested.
  - For picker flow, instruct the user to return with an id, alias, or wavPath.
  - Include the fixed alias/id mapping so a follow-up user message can be applied directly.

- Modify: `plugins/hook-terr/references/notifications.md`
  - Document that `/hook-terr:sound` supports default quick apply and external picker preview.

- Modify: `plugins/hook-terr/references/configuration.md`
  - Document that `/hook-terr:configure` initializes default `sound.wavPath` when `sound` is selected and no wavPath is configured in that settings layer.

- Modify: `plugins/hook-terr/tests/test_sound_config.py`
  - Add tests for configure writer default initialization.
  - Add tests that existing custom wavPath is preserved when enabling `sound` via configure.

---

### Task 1: Make configure initialize default sound settings

**Files:**
- Modify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\core\settings_writer.py`
- Test: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\tests\test_sound_config.py`

- [ ] **Step 1: Write the failing tests**

Add these imports and tests to `tests/test_sound_config.py`.

```python
from core.settings_writer import DEFAULT_SOUND_WAV_PATH, write_stop_channels, write_sound
```

Replace the existing import line:

```python
from core.settings_writer import write_sound
```

with the line above.

Add these tests inside `SoundConfigTests`:

```python
    def test_write_stop_channels_initializes_default_sound_config(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            settings_path = write_stop_channels("global", cwd, ["sound"])

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound"])
            self.assertTrue(settings["notifications"]["sound"]["enabled"])
            self.assertEqual(settings["notifications"]["sound"]["wavPath"], DEFAULT_SOUND_WAV_PATH)

    def test_write_stop_channels_preserves_existing_sound_wav_path(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            custom_path = r"C:\Windows\Media\notify.wav"
            write_sound(cwd, custom_path)

            settings_path = write_stop_channels("global", cwd, ["sound", "popup"])

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound", "popup"])
            self.assertEqual(settings["notifications"]["sound"]["wavPath"], custom_path)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\tests\test_sound_config.py
```

Expected: fail because `DEFAULT_SOUND_WAV_PATH` is not exported yet and/or `write_stop_channels()` does not set `wavPath`.

- [ ] **Step 3: Implement the minimal writer change**

In `core/settings_writer.py`, add this constant after `VALID_CHANNELS`:

```python
DEFAULT_SOUND_WAV_PATH = r"C:\Windows\Media\tada.wav"
```

Change the body of `write_stop_channels()` so the loop becomes:

```python
    notifications = settings.setdefault("notifications", {})
    for channel in channels:
        channel_config = notifications.setdefault(channel, {})
        channel_config["enabled"] = True
        if channel == "sound":
            channel_config.setdefault("wavPath", DEFAULT_SOUND_WAV_PATH)
```

Change `write_sound()` so it uses the same default constant when callers pass an empty value:

```python
def write_sound(cwd: str, wav_path: str) -> str:
    path = settings_path("global", cwd)
    settings = deepcopy(read_settings(path))
    notifications = settings.setdefault("notifications", {})
    sound = notifications.setdefault("sound", {})
    sound["enabled"] = True
    sound["wavPath"] = wav_path or DEFAULT_SOUND_WAV_PATH
    replace_stop_channel(settings, "beep", "sound")
    write_settings(path, settings)
    return path
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\tests\test_sound_config.py
```

Expected: all tests pass.

---

### Task 2: Add the external PowerShell sound picker

**Files:**
- Create: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\scripts\sound_picker.ps1`

- [ ] **Step 1: Create the script directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\scripts'
```

Expected: directory exists.

- [ ] **Step 2: Create `sound_picker.ps1`**

Write this file:

```powershell
$sounds = @(
    @{ Id = 1; Alias = 'tada'; Path = 'C:\Windows\Media\tada.wav'; Description = 'recommended default' },
    @{ Id = 2; Alias = 'notify'; Path = 'C:\Windows\Media\notify.wav'; Description = 'short classic notification' },
    @{ Id = 3; Alias = 'windows-notify'; Path = 'C:\Windows\Media\Windows Notify System Generic.wav'; Description = 'Windows notification style' },
    @{ Id = 4; Alias = 'windows-ding'; Path = 'C:\Windows\Media\Windows Ding.wav'; Description = 'short ding' },
    @{ Id = 5; Alias = 'chimes'; Path = 'C:\Windows\Media\chimes.wav'; Description = 'classic chimes' },
    @{ Id = 6; Alias = 'ding'; Path = 'C:\Windows\Media\ding.wav'; Description = 'classic ding' },
    @{ Id = 7; Alias = 'chord'; Path = 'C:\Windows\Media\chord.wav'; Description = 'classic chord' },
    @{ Id = 8; Alias = 'windows-balloon'; Path = 'C:\Windows\Media\Windows Balloon.wav'; Description = 'Windows balloon' },
    @{ Id = 9; Alias = 'windows-default'; Path = 'C:\Windows\Media\Windows Default.wav'; Description = 'Windows default' },
    @{ Id = 10; Alias = 'windows-exclamation'; Path = 'C:\Windows\Media\Windows Exclamation.wav'; Description = 'Windows exclamation' },
    @{ Id = 11; Alias = 'windows-foreground'; Path = 'C:\Windows\Media\Windows Foreground.wav'; Description = 'Windows foreground' },
    @{ Id = 12; Alias = 'windows-message-nudge'; Path = 'C:\Windows\Media\Windows Message Nudge.wav'; Description = 'Windows message nudge' },
    @{ Id = 13; Alias = 'alarm01'; Path = 'C:\Windows\Media\Alarm01.wav'; Description = 'alarm 01' },
    @{ Id = 14; Alias = 'alarm02'; Path = 'C:\Windows\Media\Alarm02.wav'; Description = 'alarm 02' },
    @{ Id = 15; Alias = 'ring01'; Path = 'C:\Windows\Media\Ring01.wav'; Description = 'ring 01' },
    @{ Id = 16; Alias = 'windows-error'; Path = 'C:\Windows\Media\Windows Error.wav'; Description = 'Windows error' }
)

function Show-Sounds {
    Write-Host ''
    Write-Host 'hook-terr sound picker'
    Write-Host 'Enter an id or alias to preview. Enter s <id|alias> to select. Enter q to quit.'
    Write-Host ''
    foreach ($sound in $sounds) {
        $status = if (Test-Path -LiteralPath $sound.Path) { 'ok' } else { 'missing' }
        Write-Host ("{0,2}. {1,-22} [{2}] {3}" -f $sound.Id, $sound.Alias, $status, $sound.Path)
    }
    Write-Host ''
}

function Find-Sound([string] $Value) {
    $normalized = $Value.Trim().ToLowerInvariant()
    foreach ($sound in $sounds) {
        if ([string]$sound.Id -eq $normalized -or $sound.Alias.ToLowerInvariant() -eq $normalized) {
            return $sound
        }
    }
    return $null
}

function Play-Sound($Sound) {
    if (-not (Test-Path -LiteralPath $Sound.Path)) {
        Write-Host "Missing wav file: $($Sound.Path)"
        return
    }
    $player = New-Object System.Media.SoundPlayer $Sound.Path
    $player.Load()
    $player.PlaySync()
}

Show-Sounds
while ($true) {
    $inputValue = Read-Host 'preview id/alias, select with s id/alias, or q'
    if (-not $inputValue) { continue }
    $trimmed = $inputValue.Trim()
    if ($trimmed.ToLowerInvariant() -eq 'q') { exit 0 }

    if ($trimmed -match '^s\s+(.+)$') {
        $selected = Find-Sound $Matches[1]
        if ($null -eq $selected) {
            Write-Host "Unknown sound: $($Matches[1])"
            continue
        }
        if (-not (Test-Path -LiteralPath $selected.Path)) {
            Write-Host "Cannot select missing wav file: $($selected.Path)"
            continue
        }
        Write-Host ''
        Write-Host 'Selected sound:'
        Write-Host "  id: $($selected.Id)"
        Write-Host "  alias: $($selected.Alias)"
        Write-Host "  wavPath: $($selected.Path)"
        exit 0
    }

    $sound = Find-Sound $trimmed
    if ($null -eq $sound) {
        Write-Host "Unknown sound: $trimmed"
        continue
    }
    Play-Sound $sound
}
```

- [ ] **Step 3: Manually verify the script opens and lists sounds**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File 'C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\scripts\sound_picker.ps1'
```

Expected: terminal menu lists 16 sounds. Entering `1` previews `tada`. Entering `s 1` prints `wavPath: C:\Windows\Media\tada.wav` and exits.

---

### Task 3: Simplify `/hook-terr:sound`

**Files:**
- Modify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\commands\sound.md`

- [ ] **Step 1: Replace the command flow**

Replace the existing command body with this content while keeping frontmatter `allowed-tools: ["PowerShell", "AskUserQuestion"]`:

```markdown
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
powershell -ExecutionPolicy Bypass -File $pickerPath
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
```

- [ ] **Step 2: Smoke test the default path manually**

Invoke `/hook-terr:sound`, choose `Use default`.

Expected: it writes `C:\Windows\Media\tada.wav` without playing sound and without asking group/sound/save questions.

- [ ] **Step 3: Smoke test picker path manually**

Invoke `/hook-terr:sound`, choose `Open picker`.

Expected: external picker opens; after selecting `s 1`, Claude asks the user to return with id/alias/path instead of asking more category questions.

---

### Task 4: Update references

**Files:**
- Modify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\references\notifications.md`
- Modify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\references\configuration.md`

- [ ] **Step 1: Update notifications reference**

Replace the `sound` section in `references/notifications.md` with:

```markdown
## sound

Windows 下播放 `.wav` 提示音。默认使用 `C:\Windows\Media\tada.wav`。

`/hook-terr:sound` 支持两种路径：

- `Use default`：跳过试听，直接保存默认 `tada.wav`。
- `Open picker`：打开外部 PowerShell 试听菜单，用户试听后把 id、alias 或 wavPath 回填给 Claude Code，再写入全局 settings。

外部 picker 只负责试听和输出选择，不直接修改 settings。
```

- [ ] **Step 2: Update configuration reference**

Replace the slash command bullet list in `references/configuration.md` with:

```markdown
- `/hook-terr` 只读取并显示当前生效配置。
- `/hook-terr:configure` 会先询问写入全局还是项目 settings，然后更新 Stop 通知通道。选择 `sound` 时，会在目标 settings 层显式初始化 `notifications.sound.wavPath` 为 `C:\Windows\Media\tada.wav`，除非该层已有自定义 wavPath。
- `/hook-terr:sound` 可直接保存默认提示音，或打开外部 PowerShell picker 试听后，将所选 sound 提示音写入全局 settings。
```

- [ ] **Step 3: Verify docs remain concise**

Read both files and confirm they do not duplicate the full 16-sound alias table. The table should live only in `commands/sound.md` and `scripts/sound_picker.ps1`.

---

### Task 5: Full verification

**Files:**
- Verify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\core\settings_writer.py`
- Verify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\commands\sound.md`
- Verify: `C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\scripts\sound_picker.ps1`

- [ ] **Step 1: Run Python tests**

Run:

```powershell
python C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\tests\test_sound_config.py
```

Expected: all tests pass.

- [ ] **Step 2: Verify JSON status after enabling sound through configure writer**

Run:

```powershell
$pluginPath = 'C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('hook-terr-plan-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
$env:USERPROFILE = $tempRoot
$env:HOME = $tempRoot
python (Join-Path $pluginPath 'core\settings_writer.py') --scope global --cwd $tempRoot --channels sound
Get-Content (Join-Path $tempRoot '.claude\hook-terr\settings.json')
```

Expected JSON includes:

```json
"notifications": {
  "sound": {
    "enabled": true,
    "wavPath": "C:\\Windows\\Media\\tada.wav"
  }
}
```

- [ ] **Step 3: Validate the picker syntax**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace\plugins\hook-terr\scripts\sound_picker.ps1'
```

Expected: no parse errors; the menu appears. Enter `q` to exit.

- [ ] **Step 4: Validate plugin metadata if available**

Run from the marketplace root:

```powershell
claude plugin validate C:\Users\13209\.claude\plugins\marketplaces\terr-marketplace
```

Expected: validation passes. If `claude plugin validate` is unavailable in this environment, record the exact error and do not claim marketplace validation passed.

---

## Self-Review

- Spec coverage: The plan covers default quick apply, external picker preview, user回填 id/alias/wavPath, centralized settings writes, and configure selecting `sound` initializing default `wavPath`.
- Placeholder scan: No `TBD`, `TODO`, or vague implementation steps remain.
- Type consistency: The plan consistently uses `DEFAULT_SOUND_WAV_PATH`, `write_stop_channels()`, `write_sound()`, `sound_picker.ps1`, id/alias/wavPath terminology.
