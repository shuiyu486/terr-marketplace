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

### 2. Ask what to do for this directory

Use `AskUserQuestion`:

- Question: `这个目录要怎么设置 API error 自动恢复？`
- Header: `当前目录`
- Options:
  1. `开启或修改` — Recommended. 给当前目录单独保存一套设置；不同目录可以使用不同恢复方式，互不影响。
  2. `关闭这个目录` — 当前目录不再自动恢复 API error；其他目录不受影响。

If the user chooses `关闭这个目录`, skip the recovery mode, model commands, and match text questions. Go directly to the `关闭这个目录` write block.

### 3. Ask recovery mode

Use `AskUserQuestion`:

- Question: `遇到匹配的 API error 后如何恢复？`
- Header: `恢复方式`
- Options:
  1. `二次失败再切` — Recommended. 第一次只自动输入 `continue`；如果 10 分钟内又遇到同类 API error，就先换到备用模型，再自动输入 `continue`。本轮正常结束后会优先切回原模型；如果长回合暂时没有 Stop，切换超过 10 分钟后的主会话工具/提示/失败检查点也会尝试切回。
  2. `只 continue` — 每次遇到匹配的 API error，只自动输入 `continue`，不切换模型。
  3. `立即切模型` — 第一次遇到匹配的 API error，就先换到备用模型，再自动输入 `continue`。本轮正常结束后会优先切回原模型；如果长回合暂时没有 Stop，切换超过 10 分钟后的主会话工具/提示/失败检查点也会尝试切回。

Map choices to:

- `二次失败再切` -> `continue_then_fallback`
- `只 continue` -> `continue_only`
- `立即切模型` -> `fallback_then_continue`

### 4. Ask model commands

If selected recovery mode is `continue_only`, skip this question and use the default model commands; they will not be used by that mode.

Explain:

```text
/model 命令使用当前 Claude Code 环境或自定义 API/gateway 的模型解析。opus/sonnet 可能映射到 GPT、GLM 或其他模型。若 /model 有时弹 Switch model? 确认框，hook-terr 会默认用 auto 模式读取当前 WezTerm pane：只有检测到确认框时才发送 1。
```

Use `AskUserQuestion`:

- Question: `恢复策略使用哪组 /model 命令？`
- Header: `模型命令`
- Options:
  1. `opus → sonnet` — 原模型 `/model opus`，备用模型 `/model sonnet`。适合 opus 映射到 GPT、sonnet 映射到 GLM 的 gateway 环境。
  2. `fable → sonnet` — 原模型 `/model fable`，备用模型 `/model sonnet`。
  3. `sonnet → opus` — 原模型 `/model sonnet`，备用模型 `/model opus`。
  4. `自定义` — Ask the user for exact `primaryModelCommand` and `fallbackModelCommand` before writing.

If custom input is needed, ask only for full commands, e.g. `/model gpt-5.5[1m]` and `/model glm-5.2[1m]`.

### 5. Ask error match text

Explain:

```text
apiErrorRecovery 只处理匹配 StopFailure 错误文本的 API error。匹配会检查 error、error_details、last_assistant_message 和 reason 合并后的文本。默认只匹配 cyber risk 相关报错，不会拦截所有 StopFailure。
```

Use `AskUserQuestion`:

- Question: `要自动恢复哪类 API error？`
- Header: `匹配文本`
- Options:
  1. `默认 cyber risk` — Recommended. Match `This content was flagged for possible cybersecurity risk` and `cybersecurity risk`.
  2. `自定义文本` — Ask the user for one or more exact substrings to pass as repeated `--match-text` arguments.

If custom input is needed, ask for substrings rather than regex. Example: `API Error: 400`, `upstream quota exceeded`.

### 6. Write settings

This command writes only the current directory's settings file:

```text
<current directory>\.claude\hook-terr\settings.json
```

Run a self-contained PowerShell block. Do not rely on variables from Step 1 because `AskUserQuestion` may have happened between tool calls.

For `开启或修改`, run:

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

$matchArgs = @()
# Default cyber risk mode can omit --match-text because settings_writer uses the same defaults.
# Custom mode example:
# $matchArgs = @('--match-text', 'API Error: 400', '--match-text', 'upstream quota exceeded')

python (Join-Path $pluginPath 'core\settings_writer.py') `
  --api-error-recovery `
  --scope 'project' `
  --activation-mode 'project' `
  --cwd $cwd `
  --primary-model-command '<primary command>' `
  --fallback-model-command '<fallback command>' `
  --recovery-mode '<recovery-mode>' `
  --model-switch-confirm-mode 'auto' `
  @matchArgs
```

For `关闭这个目录`, run:

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

python (Join-Path $pluginPath 'core\settings_writer.py') `
  --api-error-recovery `
  --scope 'project' `
  --activation-mode 'disable-current-dir' `
  --cwd $cwd
```

Keep the path printed by `settings_writer.py`.

### 7. Validate

Parse the written settings file:

```powershell
python -m json.tool '<settings path printed by settings_writer.py>' | Out-Null
```

Rerun status helper with another self-contained block:

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

For `开启或修改`, check that `features.apiErrorRecovery.enabled`, `recoveryMode`, model commands, `match`, and `modelSwitchConfirmMode` match the selected choices, and that `apiErrorRecoveryStatus.effectiveForCwd` is true. For `关闭这个目录`, check that `features.apiErrorRecovery.enabled` is false or `apiErrorRecoveryStatus.effectiveForCwd` is false. If status diagnostics contain errors, report them and do not claim success.

### 8. Confirm

For `开启或修改`, use:

```text
已更新这个目录的 hook-terr API error recovery 配置。
写入 settings: <path>
当前目录: <cwd>
原模型: <primaryModelCommand>
备用模型: <fallbackModelCommand>
恢复方式: <只 continue / 二次失败再切 / 立即切模型>
匹配文本: <match list>
/model 确认: auto（检测到 Switch model? 才发送 1）

以后在这个目录运行 Claude Code 时，遇到匹配的 API error 会按上面的恢复方式处理。其他目录不受影响。
```

For `关闭这个目录`, use:

```text
已关闭这个目录的 hook-terr API error recovery。
写入 settings: <path>
当前目录: <cwd>

以后在这个目录运行 Claude Code 时，不会自动恢复 API error。其他目录不受影响。
```
