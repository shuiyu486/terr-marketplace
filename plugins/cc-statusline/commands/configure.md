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
  "showAgentTracking": true,
  "showTodoProgress": true,
  "showUsageLimits": true
}
```

## Ask the User

Use AskUserQuestion to ask the user which options they want to change. Present these options:

1. **Show effort level** — Display the effort level (max/xhigh/high/medium/low) on line 1. Default: true
2. **Show token statistics** — Display the second line with in/out/ses/api token counts and timestamp. Default: true
3. **Show current path** — Display the current working directory on line 3. Default: true
4. **Show tool activity** — Display running and completed tools (Read, Edit, Grep, etc.). Default: true
5. **Show agent tracking** — Display subagent status (Task/Agent type, description, elapsed time). Default: true
6. **Show todo progress** — Display current in-progress task and completion count. Default: true
7. **Show usage limits** — Display 5-hour rate limit usage bar and reset time (only when available). Default: true
8. **Context warning threshold** — Percentage at which context turns yellow. Default: 70
9. **Context danger threshold** — Percentage at which context turns red. Default: 90

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
  showAgentTracking: process.argv[5] === 'true',
  showTodoProgress: process.argv[6] === 'true',
  showUsageLimits: process.argv[7] === 'true',
  ctxWarnThreshold: parseInt(process.argv[8], 10),
  ctxDangerThreshold: parseInt(process.argv[9], 10)
};
fs.writeFileSync(p, JSON.stringify(config, null, 2));
console.log('Config saved to', p);
" "<showEffort>" "<showTokensLine>" "<showPath>" "<showToolActivity>" "<showAgentTracking>" "<showTodoProgress>" "<showUsageLimits>" "<ctxWarn>" "<ctxDanger>"
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
    showAgentTracking = $showAgentTracking
    showTodoProgress = $showTodoProgress
    showUsageLimits = $showUsageLimits
    ctxWarnThreshold = $ctxWarn
    ctxDangerThreshold = $ctxDanger
}
$json = $config | ConvertTo-Json
[System.IO.File]::WriteAllText($configPath, $json, (New-Object System.Text.UTF8Encoding $false))
Write-Output "Config saved to $configPath"
```

Tell the user:

> Configuration saved. Changes take effect immediately on the next status line update.
