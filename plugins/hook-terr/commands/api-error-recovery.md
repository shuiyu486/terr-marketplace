---
description: Configure hook-terr API error recovery for the current directory
allowed-tools: ["PowerShell", "Read", "Write", "Edit", "AskUserQuestion"]
---

# hook-terr API Error Recovery Configure

Configure `features.apiErrorRecovery` for the current directory. This feature sends commands back to the current WezTerm pane when Claude Code emits a matching `StopFailure` API error. It is disabled by default.

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
$cwd = (Get-Location).Path
$env:HOOK_TERR_CWD = $cwd
python (Join-Path $pluginPath 'core\config_status.py')
```

Summarize the current `features.apiErrorRecovery` status before changing anything.

### 2. Ask activation mode

Use `AskUserQuestion`:

- Question: `这次 API error recovery 如何启用？`
- Header: `启用范围`
- Options:
  1. `当前项目启用` — Recommended. Write `<current project>/.claude/hook-terr/settings.json`; only this workspace loads it.
  2. `全局仅当前目录` — Write `~/.claude/hook-terr/settings.json` with `scopes.cwd.default=false` and append the current directory to `enabledPrefixes`.
  3. `全局默认启用` — Write global settings with `scopes.cwd.default=true`.
  4. `禁用当前目录` — Exclude the current directory. If current project settings already define `features.apiErrorRecovery`, write project scope and set `enabled=false`; otherwise write global scope and append current directory to `disabledPrefixes`.

Recommend `当前项目启用` because api error recovery sends automatic input to the terminal.

### 3. Ask model commands

Explain:

```text
/model 命令使用当前 Claude Code 环境或自定义 API/gateway 的模型解析。opus/sonnet 可能映射到 GPT、GLM 或其他模型。如果 /model 会弹 Switch model? 确认框，建议开启自动输入 1 确认。
```

Use `AskUserQuestion`:

- Question: `恢复策略使用哪组 /model 命令？`
- Header: `模型命令`
- Options:
  1. `opus → sonnet` — primary `/model opus`, fallback `/model sonnet`. Good for gateway setups where opus maps to GPT and sonnet maps to GLM.
  2. `fable → sonnet` — primary `/model fable`, fallback `/model sonnet`.
  3. `sonnet → opus` — primary `/model sonnet`, fallback `/model opus`.
  4. `自定义` — Ask the user for exact `primaryModelCommand` and `fallbackModelCommand` before writing.

If custom input is needed, ask only for full commands, e.g. `/model gpt-5.5[1m]` and `/model glm-5.2[1m]`.

### 4. Ask model switch confirmation

Use `AskUserQuestion`:

- Question: `/model 切换会弹确认框吗？`
- Header: `确认框`
- Options:
  1. `会，输入 1` — Recommended when Claude Code shows `Switch model?` and option `1. Yes`.
  2. `不会` — Leave confirm commands empty.

When enabled, settings writer stores:

```json
"primaryConfirmCommand": "1",
"fallbackConfirmCommand": "1",
"modelSwitchConfirmDelayMs": 500,
"postModelSwitchDelayMs": 500
```

### 5. Write settings

Map activation mode to one of:

- `project`
- `global-current-dir`
- `global-default`
- `disable-current-dir`

Choose `--scope` before writing:

- For `当前项目启用`, pass `--scope project`.
- For `禁用当前目录`, if `<cwd>\.claude\hook-terr\settings.json` contains `features.apiErrorRecovery`, pass `--scope project` so project-level enable is actually disabled. Otherwise pass `--scope global`.
- For other global modes, omit scope or pass `--scope global`.

Then run:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
python (Join-Path $pluginPath 'core\settings_writer.py') `
  --api-error-recovery `
  --scope '<project-or-global>' `
  --activation-mode '<activation-mode>' `
  --cwd $cwd `
  --primary-model-command '<primary command>' `
  --fallback-model-command '<fallback command>' `
  --confirm-model-switch '<true-or-false>'
```

Keep the path printed by `settings_writer.py`.

### 6. Validate

Parse the written settings file:

```powershell
python -m json.tool '<settings path printed by settings_writer.py>' | Out-Null
```

Rerun status helper:

```powershell
$env:CLAUDE_PLUGIN_ROOT = $pluginPath
$env:HOOK_TERR_CWD = $cwd
python (Join-Path $pluginPath 'core\config_status.py')
```

Check that `features.apiErrorRecovery.enabled` and model commands match the selected choices. For `禁用当前目录`, check that the current cwd is no longer effectively enabled; if project settings still override the global disable, rerun the write step with `--scope project`. If status diagnostics contain errors, report them and do not claim success.

### 7. Confirm

Successful confirmation template:

```text
已更新 hook-terr API error recovery 配置。
写入 settings: <path>
启用范围: <activation mode>
primary: <primaryModelCommand>
fallback: <fallbackModelCommand>
/model 确认: <enabled/disabled>

当 Claude Code 在 WezTerm pane 内触发匹配的 StopFailure 时，首次会发送 continue；短时间再次失败会按配置切 fallback 模型、确认后 continue；正常 Stop 或超时后会切回 primary 模型。
```
