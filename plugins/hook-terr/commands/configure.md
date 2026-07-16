---
description: Configure hook-terr Stop notification channels interactively
allowed-tools: ["PowerShell", "Read", "Write", "Edit", "AskUserQuestion"]
---

# hook-terr Configure

Configure Stop notification channels and optionally create an explicit Stop notify rule. Do not modify the built-in default Stop rule. Always ask whether to write global or project settings before modifying files.

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
  1. `Global` — write `<CLAUDE_CONFIG_DIR>/hook-terr/settings.json` when `CLAUDE_CONFIG_DIR` is set, otherwise `~/.claude/hook-terr/settings.json`; personal default across projects.
  2. `Project` — write `<current project>/.claude/hook-terr/settings.json`; only this workspace.

### 3. Ask channels

Use `AskUserQuestion` with `multiSelect: true`:

- Question: `显式 Stop notify 规则使用哪些通知通道？`
- Header: `通知通道`
- Options:
  1. `sound` — Windows `.wav` notification sound.
  2. `popup` — Windows MessageBox popup; default recommended together with sound.
  3. `windows_toast` — Windows tray balloon notification.

If the user selects no channels, stop and say no changes were made.

### 4. Ask activation mode

Explain before asking:

```text
仅选择通知通道只会保存 Stop channel 偏好。内置默认 stop-notify 规则保持关闭，不会返回普通 Stop 自检提示，也不会直接播放 sound、弹 popup 或发送 toast。
如果希望配置后主会话 Stop 立即触发外部通知，需要创建一个显式 Stop notify 规则。
```

Use `AskUserQuestion`:

- Question: `希望这次 Stop 通知如何生效？`
- Header: `生效方式`
- Options:
  1. `立即生效` — write settings and create or update an explicit Stop notify rule for the selected scope. When Stop is not intercepted first by a runtime feature such as documentationReminder, the matched main-session Stop rule will use the selected channels.
  2. `仅保存通道` — only write settings. Existing or future rules with `notify.enabled=true` can use these channels; the built-in default Stop rule remains disabled and silent.
  3. `取消` — stop and make no changes.

If the user chooses `取消`, stop and say no changes were made.

### 5. Write settings

Convert selected labels to a comma-separated list such as `sound,popup`. Then run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$scope = '<global-or-project>'
$channels = '<comma-separated-channels>'
$cwd = (Get-Location).Path
python (Join-Path $pluginPath 'core\settings_writer.py') --scope $scope --cwd $cwd --channels $channels
```

Keep the path printed by `settings_writer.py`; report it in the final confirmation.

### 6. Optionally create explicit Stop notify rule

Only do this when the user chose `立即生效`.

Use the same scope selected in Step 2. First resolve the rule path to an absolute path and ensure its parent directory exists. Recompute `$claudeDir` so global rules follow `CLAUDE_CONFIG_DIR`:

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$rulePath = if ($scope -eq 'global') {
    Join-Path $claudeDir 'hook-terr\rules\stop.notify.explicit.json'
} else {
    Join-Path $cwd '.claude\hook-terr\rules\stop.notify.explicit.json'
}
$rulePath = [System.IO.Path]::GetFullPath($rulePath)
$ruleDir = Split-Path -Parent $rulePath
New-Item -ItemType Directory -Force -Path $ruleDir | Out-Null
```

Use the resolved absolute `$rulePath` for every `Read`, `Write`, and final confirmation.

If the target rule file already exists, `Read` it first and ask whether to overwrite it:

- Question: `explicit Stop notify rule 已存在，要覆盖吗？`
- Header: `已有规则`
- Options:
  1. `保留现有` — do not overwrite the rule; keep the user's existing conditions and message.
  2. `覆盖规则` — replace it with the standard rule below.

Recommend `保留现有` unless the user explicitly wants the standard rule.

If creating or overwriting, write this JSON. Do not include `notify.channels`; that intentionally lets the rule use `settings.events.Stop.notifications` written in Step 5. The rule is a pure external notification rule: it must not return a Stop `systemMessage` that could make Claude continue after notifying.

```json
{
  "version": 1,
  "id": "stop-notify-explicit",
  "enabled": true,
  "event": "Stop",
  "priority": 200,
  "decision": "allow",
  "when": [
    {
      "field": "is_subagent",
      "op": "equals",
      "value": "false"
    }
  ],
  "message": {
    "system": true,
    "text": ""
  },
  "notify": {
    "enabled": true,
    "title": "Claude Code 提醒",
    "text": "Claude Code 本轮任务已停止或正在等待你协助。"
  }
}
```

### 7. Validate

Before confirming success, verify the written configuration.

Parse the settings path printed by `settings_writer.py` and, when a rule was created or overwritten, the resolved absolute `$rulePath`:

```powershell
python -m json.tool '<settings path printed by settings_writer.py>' | Out-Null
python -m json.tool $rulePath | Out-Null
```

For `仅保存通道`, only validate the settings path. If validation fails, do not claim success; report the failing path and error.

Then rerun the status helper:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$env:HOOK_TERR_CWD = $cwd
python (Join-Path $pluginPath 'core\config_status.py')
```

If the user chose `立即生效` and the rule was created or overwritten, check the status output before confirming success:

- `stopRule.id` should be `stop-notify-explicit`.
- `stopRule.notify.enabled` should be `true`.
- `stopRule.decision` should be `allow`.
- `stopRule.message.text` should be empty.
- `stopChannels` should match the selected channels.

If a different rule still wins, or `stopChannels` does not match, report that the files were written but the effective Stop configuration is not the expected one. Include the status diagnostics and do not say the rule is active.

### 8. Confirm

If the user chose `立即生效` and the rule was created or overwritten and validation shows it is effective, tell the user:

```text
已更新 hook-terr Stop 通知配置，并创建/更新 explicit Stop notify rule。
写入 settings: <path printed by settings_writer.py>
写入 rule: <rule path>
Stop channels: <channels>
主会话 Stop 未先被 documentationReminder 等 runtime feature 拦截并命中该 rule 时会触发外部通知；内置默认 stop-notify 规则保持关闭。
```

If the user chose `立即生效` but kept an existing rule, tell the user:

```text
已更新 hook-terr Stop 通知配置，并保留现有 explicit Stop notify rule。
写入 settings: <path printed by settings_writer.py>
保留 rule: <rule path>
Stop channels: <channels>
现有 rule 仍决定何时触发外部通知；内置默认 stop-notify 规则保持关闭。
```

If the user chose `仅保存通道`, tell the user:

```text
已更新 hook-terr Stop 通知通道偏好。
写入 settings: <path printed by settings_writer.py>
Stop channels: <channels>
注意：这次只保存通道。内置默认 stop-notify 规则保持关闭，不会返回普通 Stop 自检提示，也不会直接触发 sound/popup/toast。需要外部通知时，请创建或启用 explicit Stop notify rule。
```

If `sound` is enabled, also tell the user:

```text
你启用了 sound 通道。可运行 /hook-terr:sound 试听并选择提示音。
```
