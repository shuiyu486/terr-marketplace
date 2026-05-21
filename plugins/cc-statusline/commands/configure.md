---
description: Configure cc-statusline display options (effort, tokens, path, tools, agents, todos, limits, thresholds)
allowed-tools: ["Bash", "Read", "Edit", "Write", "AskUserQuestion"]
---

# cc-statusline Configuration

Configure which elements the status line displays. Settings are saved to `~/.claude/cc-statusline.json`.

## Read Current Config

Read the config file if it exists:

```bash
cat "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/cc-statusline.json" 2>/dev/null || echo "no config file"
```

If no config file exists, these are the defaults:

```json
{
  "showEffort": true,
  "showTokensLine": true,
  "showPath": true,
  "ctxWarnThreshold": 70,
  "ctxDangerThreshold": 90,
  "showToolActivity": true,
  "showRunningTools": true,
  "showCompletedTools": true,
  "showAgentTracking": true,
  "showTodoProgress": true,
  "showUsageLimits": true,
  "codexProbeIntervalMinutes": 3
}
```

## Show Current State

Summarize the current config to the user. For each toggle, show its state with a symbol (✓ enabled, ✗ disabled):

```
当前配置:
  ✓ Effort 级别    ✓ Token 统计    ✓ 当前路径
  ✓ Tool 主开关    ✓ Running tools    ✓ Completed tools
  ✓ Agent 追踪    ✓ Todo 进度    ✓ 用量限制
  上下文阈值: 警告 70% / 危险 90%
  Codex 用量刷新: 3 分钟
```

## Ask the User

Use AskUserQuestion. The first question uses **toggle semantics**: the user checks items whose state they want to **flip** (on→off or off→on). Items the user leaves unchecked keep their current state. This avoids the "re-check everything" problem since AskUserQuestion multiSelect does not support pre-selected checkboxes (`additionalProperties: false` on options).

**Question 1** (multiSelect): split across 3 sub-questions (max 4 options each per API limit):

Sub-question 1a "显示基础 — 选择要切换开关的功能": Effort 级别, Token 统计, 当前路径, Tool 主开关
Sub-question 1b "工具与追踪 — 选择要切换开关的功能": Running tools, Completed tools, Agent 追踪
Sub-question 1c "其他 — 选择要切换开关的功能": Todo 进度, 用量限制

For each option, describe current state AND what checking it will do. Format: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"

9 toggle options with descriptions:

1. label: "Effort 级别", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
2. label: "Token 统计", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
3. label: "当前路径", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
4. label: "Tool 主开关", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
5. label: "Running tools", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
6. label: "Completed tools", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
7. label: "Agent 追踪", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
8. label: "Todo 进度", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"
9. label: "用量限制", description: "当前: [开启/关闭]。勾选 = 切换为[关闭/开启]"

**IMPORTANT**: The `[开启/关闭]` placeholders above must be filled in with the user's ACTUAL current config values. If showEffort is true, write "当前: 开启。勾选 = 切换为关闭".

**Question 2** (single select): "上下文窗口告警阈值"

Present threshold preset options. Mark the preset closest to current values as "(Recommended)":

1. label: "警告 50% / 危险 75%", description: "敏感 — 上下文到一半就告警"
2. label: "警告 60% / 危险 80%", description: "中等"
3. label: "警告 70% / 危险 90%", description: "较不敏感（默认）"
4. label: "保持当前不变", description: "当前: 警告 {WARN}% / 危险 {DANGER}%"

Because Question 1 is split into three sub-questions and AskUserQuestion supports at most 4 questions per call, ask Question 3 in a second AskUserQuestion call after the first answers are collected.

**Question 3** (single select): "Codex 用量刷新间隔"

Present interval preset options. Mark the current or closest value as "(Recommended)":

1. label: "1 分钟", description: "刷新更快，请求更频繁"
2. label: "3 分钟", description: "默认值，刷新及时且请求较少"
3. label: "5 分钟", description: "较省请求"
4. label: "保持当前", description: "当前: {MINUTES} 分钟；配置支持 1-10 分钟，手动写入时会自动夹取范围"

## Apply Answers

After the user answers:

1. **Question 1**: For each item in the user's selected array, flip that feature's boolean value from the current config. Items NOT selected keep their current value.
2. **Question 2**: If the user picked a preset (1-3), use those threshold values. If the user picked "保持当前不变" (4), keep the current threshold values.
3. **Question 3**: If the user picked an interval preset (1-3), set `codexProbeIntervalMinutes` to 1, 3, or 5. If the user picked "保持当前" (4), keep the current value. Clamp any manually provided value to 1-10.
4. Write the final config using the Write Config section below.

## Write Config

After the user confirms their choices, write the config file:

**macOS/Linux:**

```bash
node -e "
const fs = require('fs');
const path = require('path');
const p = path.join(process.env.CLAUDE_CONFIG_DIR || require('os').homedir() + '/.claude', 'cc-statusline.json');
const config = {
  showEffort: process.argv[1] === 'true',
  showTokensLine: process.argv[2] === 'true',
  showPath: process.argv[3] === 'true',
  showToolActivity: process.argv[4] === 'true',
  showRunningTools: process.argv[5] === 'true',
  showCompletedTools: process.argv[6] === 'true',
  showAgentTracking: process.argv[7] === 'true',
  showTodoProgress: process.argv[8] === 'true',
  showUsageLimits: process.argv[9] === 'true',
  codexProbeIntervalMinutes: Math.min(10, Math.max(1, parseInt(process.argv[10], 10) || 3)),
  ctxWarnThreshold: parseInt(process.argv[11], 10),
  ctxDangerThreshold: parseInt(process.argv[12], 10)
};
fs.writeFileSync(p, JSON.stringify(config, null, 2));
console.log('Config saved to', p);
" "<showEffort>" "<showTokensLine>" "<showPath>" "<showToolActivity>" "<showRunningTools>" "<showCompletedTools>" "<showAgentTracking>" "<showTodoProgress>" "<showUsageLimits>" "<codexProbeIntervalMinutes>" "<ctxWarn>" "<ctxDanger>"
```

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$configPath = Join-Path $claudeDir 'cc-statusline.json'
$config = @{
    showEffort = $showEffort
    showTokensLine = $showTokensLine
    showPath = $showPath
    showToolActivity = $showToolActivity
    showRunningTools = $showRunningTools
    showCompletedTools = $showCompletedTools
    showAgentTracking = $showAgentTracking
    showTodoProgress = $showTodoProgress
    showUsageLimits = $showUsageLimits
    codexProbeIntervalMinutes = [Math]::Min(10, [Math]::Max(1, [int]$codexProbeIntervalMinutes))
    ctxWarnThreshold = $ctxWarn
    ctxDangerThreshold = $ctxDanger
}
$json = $config | ConvertTo-Json
[System.IO.File]::WriteAllText($configPath, $json, (New-Object System.Text.UTF8Encoding $false))
Write-Output "Config saved to $configPath"
```

Tell the user:

> Configuration saved. Changes take effect immediately on the next status line update.
