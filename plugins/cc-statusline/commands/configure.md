---
description: Configure cc-statusline display options (effort, tokens, path, tools, agents, todos, limits, thresholds)
allowed-tools: ["Bash", "PowerShell", "Read", "Edit", "Write", "AskUserQuestion"]
---

# cc-statusline Configuration

Configure which elements the status line displays. Settings are saved to `${CLAUDE_CONFIG_DIR}/cc-statusline.json`, or `~/.claude/cc-statusline.json` when `CLAUDE_CONFIG_DIR` is unset.

`codexProbeAllowedHosts` is preserved by this command but not edited here. Remote Codex probe hosts are authorized by `/cc-statusline:setup`.

## Find Plugin Path

Use the same installed plugin path discovery as `/cc-statusline:setup`, then ensure `dist/configCli.js` exists. If the build is missing, run `npm install && npm run build` from the plugin path.

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$pluginPath = (Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\cc-statusline\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1).FullName
if (-not $pluginPath) { Write-Output 'ERROR: cc-statusline plugin not found. Run /plugin install cc-statusline first.'; exit 1 }
$configCli = Join-Path $pluginPath 'dist\configCli.js'
if (-not (Test-Path $configCli)) { Push-Location $pluginPath; npm install; if ($LASTEXITCODE -ne 0) { exit 1 }; npm run build; $code = $LASTEXITCODE; Pop-Location; if ($code -ne 0) { exit $code } }
```

**macOS/Linux:**

```bash
PLUGIN_PATH=$(ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/cc-statusline/*/ 2>/dev/null | sort -V | tail -1)
[ -n "$PLUGIN_PATH" ] || { echo 'ERROR: cc-statusline plugin not found. Run /plugin install cc-statusline first.'; exit 1; }
CONFIG_CLI="$PLUGIN_PATH/dist/configCli.js"
if [ ! -f "$CONFIG_CLI" ]; then
    cd "$PLUGIN_PATH" && npm install && npm run build || exit 1
fi
```

## Read Current Config

Use the shared config CLI so this command does not duplicate schema/default/normalize logic.

**Windows:**

```powershell
$configJson = node $configCli read
if ($LASTEXITCODE -ne 0) { Write-Output 'ERROR: failed to read config'; exit 1 }
$config = ($configJson | ConvertFrom-Json).config
```

**macOS/Linux:**

```bash
CONFIG_JSON=$(node "$CONFIG_CLI" read) || { echo 'ERROR: failed to read config'; exit 1; }
```

Default values and normalization come from `src/config.ts` via `dist/configCli.js`; do not duplicate the full schema in this command.

## Show Current State

Summarize the current config to the user. For each toggle, show its state with a symbol (✓ enabled, ✗ disabled):

```text
当前配置:
  ✓ Effort 级别    ✓ Token 统计    ✓ 当前路径
  ✓ Tool 主开关    ✓ Running tools    ✓ Completed tools
  ✓ Agent 追踪    ✓ Todo 进度    ✓ 用量限制
  Agent 显示: compact
  上下文阈值: 警告 70% / 危险 90%
  Codex 用量刷新: 3 分钟
  Codex 远程探测域名: 未配置（由 /cc-statusline:setup 管理）
```

## Ask the User

Use AskUserQuestion. The first question uses **toggle semantics**: the user checks items whose state they want to **flip** (on→off or off→on). Items the user leaves unchecked keep their current state.

**Question 1** (multiSelect): split across 3 sub-questions (max 4 options each per API limit):

Sub-question 1a "显示基础 — 选择要切换开关的功能": Effort 级别, Token 统计, 当前路径, Tool 主开关
Sub-question 1b "工具与追踪 — 选择要切换开关的功能": Running tools, Completed tools, Agent 追踪
Sub-question 1c "其他 — 选择要切换开关的功能": Todo 进度, 用量限制

For each option, describe current state AND what checking it will do. Format: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"

**Question 2** (single select): "上下文窗口告警阈值"

Present threshold preset options. Mark the preset closest to current values as "(Recommended)":

1. label: "警告 50% / 危险 75%", description: "敏感 — 上下文到一半就告警"
2. label: "警告 60% / 危险 80%", description: "中等"
3. label: "警告 70% / 危险 90%", description: "较不敏感（默认）"
4. label: "保持当前不变", description: "当前: 警告 {WARN}% / 危险 {DANGER}%"

Because Question 1 is split into three sub-questions and AskUserQuestion supports at most 4 questions per call, ask Questions 3-4 in a second AskUserQuestion call after the first answers are collected.

**Question 3** (single select): "Agent 显示模式"

1. label: "compact", description: "默认值，单行摘要：运行中 agent 明细 + 已完成 agent 按类型聚合"
2. label: "multiline", description: "多行展开：显示最近保留的全部 agent，包含 model"
3. label: "保持当前", description: "当前: {MODE}"

**Question 4** (single select): "Codex 用量刷新间隔"

1. label: "1 分钟", description: "刷新更快，请求更频繁"
2. label: "3 分钟", description: "默认值，刷新及时且请求较少"
3. label: "5 分钟", description: "较省请求"
4. label: "保持当前", description: "当前: {MINUTES} 分钟；配置支持 1-10 分钟，手动写入时会自动夹取范围"

## Apply Answers

After the user answers:

1. **Question 1**: For each selected item, flip that boolean value from the current config. Items NOT selected keep their current value.
2. **Question 2**: If the user picked a preset (1-3), use those threshold values. If the user picked "保持当前不变" (4), keep the current threshold values.
3. **Question 3**: If the user picked `compact` or `multiline`, set `agentDisplayMode` to that value. If the user picked "保持当前" (3), keep the current value.
4. **Question 4**: If the user picked an interval preset (1-3), set `codexProbeIntervalMinutes` to 1, 3, or 5. If the user picked "保持当前" (4), keep the current value.
5. Write only the changed display fields as a patch using the shared config CLI. Do not include `codexProbeAllowedHosts` in the patch; it will be preserved automatically.

## Write Config

Build a JSON patch containing only the display/configuration fields managed by this command, then call `configCli patch`.

**Windows (PowerShell):**

```powershell
$patch = @{
    showEffort = $showEffort
    showTokensLine = $showTokensLine
    showPath = $showPath
    showToolActivity = $showToolActivity
    showRunningTools = $showRunningTools
    showCompletedTools = $showCompletedTools
    showAgentTracking = $showAgentTracking
    agentDisplayMode = if ($agentDisplayMode -eq 'multiline') { 'multiline' } else { 'compact' }
    showTodoProgress = $showTodoProgress
    showUsageLimits = $showUsageLimits
    codexProbeIntervalMinutes = [Math]::Min(10, [Math]::Max(1, [int]$codexProbeIntervalMinutes))
    ctxWarnThreshold = $ctxWarn
    ctxDangerThreshold = $ctxDanger
} | ConvertTo-Json -Compress
node $configCli patch $patch
if ($LASTEXITCODE -ne 0) { Write-Output 'ERROR: config save failed'; exit 1 }
```

**macOS/Linux:**

```bash
PATCH=$(node -e "process.stdout.write(JSON.stringify({showEffort:process.argv[1]==='true',showTokensLine:process.argv[2]==='true',showPath:process.argv[3]==='true',showToolActivity:process.argv[4]==='true',showRunningTools:process.argv[5]==='true',showCompletedTools:process.argv[6]==='true',showAgentTracking:process.argv[7]==='true',agentDisplayMode:process.argv[8]==='multiline'?'multiline':'compact',showTodoProgress:process.argv[9]==='true',showUsageLimits:process.argv[10]==='true',codexProbeIntervalMinutes:parseInt(process.argv[11],10)||3,ctxWarnThreshold:parseInt(process.argv[12],10),ctxDangerThreshold:parseInt(process.argv[13],10)}))" "<showEffort>" "<showTokensLine>" "<showPath>" "<showToolActivity>" "<showRunningTools>" "<showCompletedTools>" "<showAgentTracking>" "<agentDisplayMode>" "<showTodoProgress>" "<showUsageLimits>" "<codexProbeIntervalMinutes>" "<ctxWarn>" "<ctxDanger>")
node "$CONFIG_CLI" patch "$PATCH" || { echo 'ERROR: config save failed'; exit 1; }
```

Tell the user:

> Configuration saved. Changes take effect immediately on the next status line update. Remote Codex probe hosts are managed by `/cc-statusline:setup` and were preserved.
