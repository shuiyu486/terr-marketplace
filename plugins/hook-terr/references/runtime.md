# Runtime

`hook-terr` 采用薄 hook 入口和统一 runtime。

## 控制流

1. `hooks/hooks.json` 注册 Claude Code hook 事件。Python hooks 使用 exec form（`command: "python3"` + `args`），避免 Windows/Git Bash shell profile 输出污染 stdout，导致 Claude Code 报 `JSON validation failed`。
2. `hooks/*.py` 读取 stdin JSON，并调用 `core.event_runner.run(event, input_data)`。
3. `context_builder` 将原始 payload 规范化为 `HookContext`，并推导 `is_subagent` 与 `agent_type` 规则字段。
4. `config_loader` 加载 settings 和 rules。
5. `api_error_recovery` 在启用时处理 `StopFailure` API error 恢复，并在正常 `Stop` 或超时后的主会话检查点恢复模型；它只做 WezTerm pane 定向输入副作用，不依赖 hook 输出控制 Claude。
6. `documentation_reminder` 在启用时处理项目修改后的文档收尾提醒：`PostToolUse` 记录项目文件修改，`Stop` 首次返回 block，`UserPromptSubmit` 重置本轮状态。
7. `rule_matcher` 找到当前事件最高优先级命中规则。
8. `action_executor` 解析有效通知通道并执行通知器；runtime 通知护栏只允许主会话 Stop 和主会话 `PreToolUse`/`AskUserQuestion` 求助场景发出外部通知。
9. `response_builder` 输出 Claude Code hook JSON；Stop 外部通知规则是 pure external notification，不再返回可能促使 Claude 继续工作的 Stop `systemMessage`。

## Agent 上下文字段

`context_builder` 会暴露 `is_subagent` 和 `agent_type` 供规则匹配。`SubagentStop` 事件总是视为子 agent；其他事件会综合 payload 显式 `is_subagent=true` / `agent_type=subagent`、`isSidechain=true`、官方 `agent_id`、兼容字段 `agentId`，以及 `transcript_path` 中独立的 `subagents` 路径段。任一明确子 agent 证据都会优先，避免矛盾字段把子 agent 降级为主会话；无法判断时仍按主会话 fail open。

## API error recovery

`features.apiErrorRecovery` 默认关闭且只处理主会话。启用后，主会话 `StopFailure` 命中 `match` 文本时会读取当前 hook 进程环境变量 `WEZTERM_PANE`，并通过 `wezterm cli send-text --pane-id <pane> --no-paste` 向触发错误的 pane 发送恢复命令；子 agent 在副作用入口直接跳过，不会创建或推进恢复状态。状态存储在 `<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/state/api-error-recovery/`，key 由 `session_id + WEZTERM_PANE` 或 `transcript_path + WEZTERM_PANE + cwd` 计算，确保多个 Claude Code 会话和多个 WezTerm tab/pane 隔离。

默认 `recoveryMode=continue_then_fallback`：第一次 `StopFailure` 发送 `continueCommand`；`windowSeconds` 内再次失败时发送 `fallbackModelCommand` 加 `continueCommand`。`continue_only` 会始终只继续，不切模型；`fallback_then_continue` 会第一次失败就发送 `fallbackModelCommand` 加 `continueCommand`。fallback active 后遇到主会话 `Stop` 会优先发送 `primaryModelCommand`；如果长回合暂时没有 Stop，后续主会话 `PreToolUse`、`PostToolUse`、`UserPromptSubmit` 或再次 `StopFailure` 在超过 `restoreAfterSeconds` 后也会触发恢复检查。同一 session/pane 使用 lock 目录串行化，并用 `dedupeSeconds` 避免重复输入。`match` 只检查 `StopFailure` 的 `error` 和 `error_details`，避免 `last_assistant_message` 或 `reason` 中引用类似文字时误触发模型切换；默认只匹配 cyber risk 相关 API error。`modelSwitchConfirmMode=auto` 会在发送 `/model ...` 前后读取当前 pane 文本，只在新出现 `Switch model?` / `Yes, switch to` 时发送确认命令；如果切换前 baseline 读取失败，本次模型切换会 fail closed，避免进入无法安全确认的 `/model` 流程或扫描旧提示后误输入 `1`。模型切换开始前会先写 pending state，切换或后续 `continue` 失败时仍保留 primary 恢复责任。

## 新增事件规则

通常只需要：

- 确认 `context_builder` 暴露所需字段。
- 添加规则 JSON。
- 必要时更新 `references/rules.md`。

## 新增 notifier

需要：

- 在 `notifiers/` 新增实现。
- 在 `notifiers/registry.py` 注册 channel。
- 在 `core/schema.py` 加入合法 channel。
- 更新 `references/notifications.md`。

## 文档收尾提醒

`features.documentationReminder` 默认启用。它只在当前 `cwd` 看起来像项目，且 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改的目标路径位于该项目目录内时记录状态。Stop payload 中 `stop_hook_active=true` 时 runtime 在 recovery 检查后直接放行，避免 documentation reminder 或自定义 block 规则反复阻止会话结束。

状态存储在 `<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/state/documentation-reminder/`，按 `session_id` 优先、`transcript_path` 兜底生成 key，避免多个 Claude Code 会话在同一项目中并发时互相污染。首次 Stop block 前会先标记已提醒；同一轮第二次 Stop 放行。`UserPromptSubmit` 会重置本轮状态。

## Hook 输出协议

- Stop/SubagentStop block 使用 `decision: block`。
- StopFailure 输出和退出码由 Claude Code 忽略；`apiErrorRecovery` 因此只执行 WezTerm 输入副作用并返回 `{}`。
- PreToolUse block 使用 `hookSpecificOutput.permissionDecision: deny`；PostToolUse 和 UserPromptSubmit block 使用顶层 `decision: block` / `reason`。
- warn 使用 `systemMessage`。
- allow 返回 `{}`。
- 通知失败和文档提醒状态异常都 fail open；普通规则通知诊断会追加到 hook `systemMessage`，文档提醒和 `AskUserQuestion` 求助通知诊断会写入 stderr。
