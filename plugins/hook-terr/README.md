# hook-terr

`hook-terr` 是一个个人工作流 hook runtime 插件，用于在 Claude Code 的 hook 事件中执行可配置规则。默认普通 Stop 不再向 Claude 返回自检 `systemMessage`，避免影响多轮/自主推进；外部提醒可通过启用 `notify` 的规则调用 Windows 提示音、popup 弹窗、tray 通知或自定义命令。

## 特性

- 注册 `Stop`、`StopFailure`、`SubagentStop`、`PreToolUse`、`PostToolUse`、`UserPromptSubmit` 六类 hook 入口。
- 当主会话调用 `AskUserQuestion` 等待用户选择或输入时，复用 Stop 通知通道触发外部通知。
- 内置普通 Stop 自检规则默认关闭，避免在多轮/自主推进中污染上下文；`SubagentStop` 默认关闭，避免子 agent 结束时弹提示音。
- 规则可匹配 `is_subagent` 与 `agent_type`，用于区分主会话和子 agent；runtime 兼容官方 `agent_id`、旧式 `agentId`、sidechain 和 transcript 路径信号。
- 默认启用文档收尾提醒：项目内使用 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改文件后，首次 Stop 会提醒 Claude 更新相关文档并完成必要验证。
- 可选 `apiErrorRecovery` 会在 WezTerm 中按 pane 精确恢复匹配的 StopFailure API error：可按目录选择只自动输入 `continue`、二次失败再换到备用模型，或首次失败就换到备用模型；自动兼容 `/model` 的 `Switch model?` 确认框，本轮正常结束或超时后的主会话检查点会切回原模型。
- 支持插件内默认配置、用户全局覆盖和项目覆盖。
- Stop 外部通知需要通过用户或项目规则显式启用，避免每次 Stop 都误触发；外部通知在 runtime 层只允许主会话 Stop 和主会话 `AskUserQuestion` 求助场景。
- 支持 Windows tray 通知、提示音、结构化弹窗和高级自定义命令。
- hook 异常 fail open，通知失败不会阻断 Claude Code 主流程，并会把简要诊断追加到 `systemMessage`。

## Commands

- `/hook-terr` — 显示当前生效的 hook-terr 配置。
- `/hook-terr:configure` — 交互式配置 Stop 通知通道，并可选择创建 explicit Stop notify rule 让配置立即生效；启用 `sound` 时会补齐默认提示音。
- `/hook-terr:api-error-recovery` — 交互式为当前目录开启、修改或关闭 WezTerm API error recovery；每个目录单独保存设置，互不影响。
- `/hook-terr:sound` — 直接保存默认 sound 提示音，或打开外部 PowerShell picker 试听后保存全局偏好。

## 配置来源

加载优先级：

```text
defaults/settings.json
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

规则加载优先级：

```text
defaults/rules/*.json
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

用户全局覆盖（设置了 `CLAUDE_CONFIG_DIR` 时，以该目录替代 `~/.claude`）：

```text
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/settings.json
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/*.json
```

项目覆盖：

```text
<project>/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/rules/*.json
```

`presets/` 和 `examples/` 随插件分发，但不会自动加载。preset 文件带有 `version`、`description` 和外层 `settings` 元数据；使用时只能把顶层 `settings` 对象内部的字段合并到全局或项目 `settings.json`，不要整份复制 wrapper。`examples/config.api-error-recovery.wezterm.example.json` 是可直接参考的配置片段，建议先放到项目 `.claude/hook-terr/settings.json` 小范围启用。

## 默认行为

内置普通 `stop-notify` 规则默认关闭，会：

- 不在普通 Stop 中返回自检 `systemMessage`，避免让 Claude 误判本轮应结束。
- 不直接触发 Windows `.wav` sound、popup 或 toast，避免非完成/非求助场景误打扰。
- 保留为可被用户或项目同 `id` 规则覆盖的兼容规则。

默认文档收尾提醒会：

- 仅在当前 `cwd` 看起来像项目，且修改工具命中的文件位于该项目目录内时记录状态。
- 识别 `Write`、`Edit`、`MultiEdit` 和 `NotebookEdit`；不根据 `Bash` 命令猜测文件修改。
- 在同一会话首次 Stop 时返回 `decision: block`，要求 Claude 更新相关文档，并执行必要的测试/验证。
- 同一轮只提醒一次；再次 Stop 会放行。用户或项目 settings 可通过 `features.documentationReminder.enabled=false` 关闭。

Windows notification 仍然可用，但不再由默认 Stop 自检规则触发。`/hook-terr:configure` 可以只保存 Stop 通知通道，也可以在用户确认后创建 explicit Stop notify rule。选择“立即生效”时，会创建 pure external explicit Stop notify rule；当主会话 Stop 未先被 documentationReminder 等 runtime feature 拦截并命中该 rule 时，会使用所选通道触发外部通知，但不会向 Claude 返回普通 Stop `systemMessage`。选择“仅保存通道”时，内置普通 `stop-notify` 仍保持关闭；但主会话 `AskUserQuestion` 求助场景会复用保存的 Stop 通道。通知进程会独立启动，hook 本身不会等待通知关闭。

## API error recovery

`features.apiErrorRecovery` 默认关闭，只处理主会话。启用后，主会话 `StopFailure` 命中配置的 `match` 文本时，会使用 `WEZTERM_PANE` 和 `wezterm cli send-text --pane-id ... --no-paste` 将恢复命令发回触发错误的 WezTerm pane；子 agent 不会创建、推进或恢复该状态。默认 `match` 只覆盖 `This content was flagged for possible cybersecurity risk` / `cybersecurity risk`，匹配范围是 `error`、`error_details`、`last_assistant_message` 和 `reason` 合并后的文本。状态按 `session_id + pane_id` 隔离，并使用 per-session lock 与短时间去重，避免多个 Claude Code 会话或多个 WezTerm 标签页互相串线；模型切换开始前会先保存 pending 状态，因此即使后续 `continue` 发送失败，Stop 仍能安全尝试恢复 primary。

默认恢复方式是 `continue_then_fallback`：第一次命中只发送 `continue`；如果 `windowSeconds` 默认 600 秒内再次命中，先发送 `fallbackModelCommand` 换到备用模型，再发送 `continueCommand`。也可配置 `continue_only` 让每次只继续，或 `fallback_then_continue` 让第一次失败就换到备用模型并继续。换到备用模型后，主会话 `Stop` 会优先发送 `primaryModelCommand` 切回原模型；如果长回合暂时没有 Stop，后续主会话 `PreToolUse`、`PostToolUse`、`UserPromptSubmit` 或再次 `StopFailure` 在超过 `restoreAfterSeconds` 默认 600 秒后也会触发恢复检查。

运行 `/hook-terr:api-error-recovery` 会给当前目录写入 `<current directory>/.claude/hook-terr/settings.json`；在不同目录分别运行，就能给每个目录保存不同恢复方式、模型和匹配文本，互不影响。临时禁用当前启动环境可设置 `HOOK_TERR_API_ERROR_RECOVERY=0`。`modelSwitchConfirmMode` 默认是 `auto`：runtime 会在发送 `/model ...` 后读取当前 WezTerm pane，只有检测到 `Switch model?` / `Yes, switch to` 确认框时才发送 `modelSwitchConfirmCommand`（默认 `1`），避免未弹框时把 `1` 当成普通用户输入。

启用示例：

```json
{
  "features": {
    "apiErrorRecovery": {
      "enabled": true,
      "primaryModelCommand": "/model opus",
      "fallbackModelCommand": "/model sonnet"
    }
  }
}
```

## 通知通道

`settings.events.<Event>.notifications` 是事件默认通知通道来源。`rule.notify.channels` 是可选的规则级覆盖；未设置时回退到事件默认通道。默认 `stop-notify` 关闭且不会返回普通 Stop 自检提示；需要外部通知时，创建启用 `notify` 的用户或项目规则。

`sound` 默认播放 `C:\\Windows\\Media\\tada.wav`。`/hook-terr:sound` 可跳过试听直接保存默认音效；需要试听时会打开外部 PowerShell picker，用户选好后回填 id、alias 或 wavPath 再写入全局偏好。`popup` 默认可用，但只有启用 notify 的规则选择该通道时才会触发。`custom_command` 是高级能力，默认关闭；启用后等价于执行本机命令，只应配置可信命令；动态消息只能通过 `HOOK_TERR_*` 环境变量读取，旧 `{{message}}` 等 `custom_command.command` 模板会导致 settings 加载诊断报错。

## 扩展规则

新增规则放在：

```text
<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为覆盖键。项目规则覆盖全局规则，全局规则覆盖插件默认规则。同一 `id` 且 `enabled: false` 可禁用上层规则。自定义 Stop 规则如果不希望命中子 agent，可添加 `is_subagent == "false"` 条件；如果需要专门匹配子 agent，可使用 `is_subagent == "true"` 或 `agent_type == "subagent"`。

## 更新插件

发布新版本后，先运行 `/plugin marketplace update terr-marketplace` 刷新 marketplace，再通过 `/plugin` 更新 `hook-terr`（或运行 `claude plugin update hook-terr@terr-marketplace`），最后运行 `/reload-plugins` 或重启 Claude Code。运行中的会话会继续使用启动时加载的 plugin cache 路径，只有 reload/restart 后才会切换 hooks/runtime；可运行 `/hook-terr` 核对 `pluginVersion` 和 `pluginRoot`。用户和项目下已有的 `.claude/hook-terr/settings.json` 不会被插件更新覆盖，新 runtime 会继续读取并合并这些配置。

更多说明见 `references/`。
