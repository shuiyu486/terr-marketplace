# Configuration

`hook-terr` 使用三层配置：插件默认配置、用户全局覆盖、项目覆盖。

## 加载顺序

```text
defaults/settings.json
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

设置 `CLAUDE_CONFIG_DIR` 时，用户全局 settings、rules 和 runtime state 都存放在该目录下；未设置时回退到 `~/.claude`。

后加载的配置会深度覆盖前面的配置。数组会整体替换，不做按元素合并。

## 规则加载顺序

```text
defaults/rules/*.json
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为唯一键。项目规则覆盖全局规则，全局规则覆盖默认规则。

## 通知通道来源

`settings.events.<Event>.notifications` 是默认通知通道来源。`rule.notify.channels` 是可选的规则级覆盖；未设置时回退到事件默认通道。

settings 中的 Stop channels 是主会话 Stop 和主会话 `AskUserQuestion` 求助通知共同使用的“通道偏好”。Stop 本身不会仅因配置 channels 就触发外部通知，仍需要命中 `notify.enabled=true` 的 Stop 规则；`AskUserQuestion` 求助场景由 runtime guard 触发并复用 Stop channels。内置 `stop-notify` 默认关闭，不执行外部通知，也不在普通 Stop 中返回自检 `systemMessage`。`SubagentStop` 默认关闭且不配置通知，避免子 agent 结束时弹提示音。

## Slash commands

- `/hook-terr` 只读取并显示当前生效配置。
- `/hook-terr:configure` 会先询问写入全局还是项目 settings，然后更新 Stop 通知通道。随后会询问是否创建/更新 explicit Stop notify rule：选择 `立即生效` 时写入对应 scope 的 `rules/stop.notify.explicit.json`；当主会话 Stop 未先被 documentationReminder 等 runtime feature 拦截并命中该 rule 时，会触发 pure external 外部通知，不返回普通 Stop `systemMessage`。选择 `仅保存通道` 时只修改 settings，内置默认 `stop-notify` 仍保持关闭且不会触发 Stop 外部通知；但 `AskUserQuestion` 求助通知会复用保存的 Stop 通道。选择 `sound` 时，会在目标 settings 层显式初始化 `notifications.sound.wavPath` 为 `C:\\Windows\\Media\\tada.wav`，除非该层已有自定义 wavPath。
- `/hook-terr:api-error-recovery` 会交互式为当前目录开启、修改或关闭 `features.apiErrorRecovery`，写入当前目录的 `.claude/hook-terr/settings.json`，并支持配置恢复方式、StopFailure 匹配文本和模型命令；`/model` 切换确认默认自动检测。
- `/hook-terr:sound` 可直接保存默认提示音，或打开外部 PowerShell picker 试听后，将所选 sound 提示音写入全局 settings。

`/hook-terr:configure` settings 写入位置：

```text
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

`/hook-terr:configure` 选择 `立即生效` 时的 explicit rule 写入位置：

```text
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/stop.notify.explicit.json
<project>/.claude/hook-terr/rules/stop.notify.explicit.json
```

`/hook-terr:sound` 始终写入：

```text
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/settings.json
```

## 文档收尾提醒

`features.documentationReminder` 默认启用，随插件默认 settings 分发；更新插件后，未显式覆盖该配置的机器会自动应用。

默认行为：当当前 `cwd` 看起来像项目，且本会话通过 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改了项目目录内文件时，首次 Stop 会 block 一次，提醒 Claude 更新相关文档并执行必要的测试/验证。状态按 `session_id` 或 `transcript_path` 隔离，避免同一项目内多个 Claude Code 会话互相污染。

禁用方式：

```json
{
  "features": {
    "documentationReminder": {
      "enabled": false
    }
  }
}
```

可覆盖字段：

- `enabled`: 是否启用。
- `tools`: 触发记录的工具名数组，默认 `Write`、`Edit`、`MultiEdit`、`NotebookEdit`。
- `stateTtlHours`: 状态文件保留小时数。
- `message`: Stop block 返回给 Claude 的提醒文案。

运行时状态存储在 `<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/state/documentation-reminder/`。

## API error recovery

`features.apiErrorRecovery` 默认关闭，启用后只支持 WezTerm：

```json
{
  "features": {
    "apiErrorRecovery": {
      "enabled": true,
      "terminal": "wezterm",
      "strategy": "escalate_then_restore",
      "windowSeconds": 600,
      "restoreAfterSeconds": 600,
      "sendDelayMs": 800,
      "match": ["cybersecurity risk"],
      "primaryModelCommand": "/model opus",
      "fallbackModelCommand": "/model sonnet",
      "continueCommand": "continue",
      "recoveryMode": "continue_then_fallback",
      "modelSwitchConfirmMode": "auto",
      "modelSwitchConfirmCommand": "1",
      "modelSwitchConfirmDelayMs": 500,
      "postModelSwitchDelayMs": 500,
      "modelSwitchConfirmScanLines": 20,
      "maxEscalations": 1,
      "lockTimeoutSeconds": 30,
      "dedupeSeconds": 5,
      "requireSamePaneForRestore": true
    }
  }
}
```

`recoveryMode` 控制遇到匹配 API error 时的恢复方式：`continue_only` 每次只发送 `continueCommand`；`continue_then_fallback` 第一次只继续，`windowSeconds` 默认 600 秒内再次失败才先换到备用模型再继续；`fallback_then_continue` 第一次失败就先换到备用模型再继续。换到备用模型后，正常 Stop 或超过 `restoreAfterSeconds` 默认 600 秒后有新动作时会发送 `primaryModelCommand` 切回原模型。`match` 会检查 `error`、`error_details`、`last_assistant_message` 和 `reason` 合并后的文本；默认只匹配 cyber risk 相关 API error，不会拦截所有 StopFailure。状态存储在 `<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/state/api-error-recovery/`，按 `session_id + WEZTERM_PANE` 隔离，多会话、多标签页不会共享恢复状态。

推荐运行 `/hook-terr:api-error-recovery` 给当前目录写入 `<current directory>/.claude/hook-terr/settings.json`；在不同目录分别运行，就能给每个目录保存不同恢复方式、模型和匹配文本，互不影响。关闭某个目录时，该命令也只改这个目录的 settings。底层仍保留 `scopes` 字段供手工高级配置使用；普通交互流程不会展示或要求配置这些高级字段。临时禁用当前启动环境可设置 `HOOK_TERR_API_ERROR_RECOVERY=0`。

`modelSwitchConfirmMode` 支持 `auto`、`always`、`never`。默认 `auto` 会在发送 `/model ...` 后读取当前 WezTerm pane 的近几行文本，只有检测到 `Switch model?` / `Yes, switch to` 时才发送 `modelSwitchConfirmCommand`（默认 `1`）；`always` 保留旧式总是确认行为，`never` 永不发送确认。`modelSwitchConfirmDelayMs`、`postModelSwitchDelayMs` 和 `modelSwitchConfirmScanLines` 分别控制确认框等待、确认后等待和扫描行数。`primaryConfirmCommand` / `fallbackConfirmCommand` 仍兼容旧配置，但新配置建议使用统一的 `modelSwitchConfirmCommand`。`/model` 命令遵循当前 Claude Code 环境或自定义 API/gateway 的模型映射，`opus`、`sonnet` 不一定代表官方模型。

## custom_command 配置迁移

`notifications.custom_command.command` 中不再支持旧模板变量：`{{event}}`、`{{title}}`、`{{message}}`、`{{cwd}}`、`{{timestamp}}`。如果用户或项目 settings 包含这些模板，settings 加载阶段会报诊断并跳过该配置层。

请改用 `HOOK_TERR_*` 环境变量，例如 PowerShell 中使用 `$env:HOOK_TERR_MESSAGE`，sh/bash 中使用 `$HOOK_TERR_MESSAGE`。

## Presets 和 examples

`presets/` 随 marketplace 插件分发，保存带元数据 wrapper 的可复用配置方案；使用时只能复制每个 preset 顶层 `settings` 对象内部的字段，不要把 `version`、`description` 和外层 `settings` wrapper 整份写入配置。`examples/` 保存可复制的配置片段，例如 `examples/config.api-error-recovery.wezterm.example.json`。它们都不会自动加载。

## 禁用上层规则

创建同 `id` 规则并设置：

```json
{ "id": "stop-notify", "enabled": false, "event": "Stop", "decision": "allow" }
```

即可在当前层禁用上层同名规则。
