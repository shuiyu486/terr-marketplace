# Runtime

`hook-terr` 采用薄 hook 入口和统一 runtime。

## 控制流

1. `hooks/hooks.json` 注册 Claude Code hook 事件。
2. `hooks/*.py` 读取 stdin JSON，并调用 `core.event_runner.run(event, input_data)`。
3. `context_builder` 将原始 payload 规范化为 `HookContext`。
4. `config_loader` 加载 settings 和 rules。
5. `documentation_reminder` 在启用时处理项目修改后的文档收尾提醒：`PostToolUse` 记录项目文件修改，`Stop` 首次返回 block，`UserPromptSubmit` 重置本轮状态。
6. `rule_matcher` 找到当前事件最高优先级命中规则。
7. `action_executor` 解析有效通知通道并执行通知器。
8. `response_builder` 输出 Claude Code hook JSON。

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

`features.documentationReminder` 默认启用。它只在当前 `cwd` 看起来像项目，且 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改的目标路径位于该项目目录内时记录状态。

状态存储在 `~/.claude/hook-terr/state/documentation-reminder/`，按 `session_id` 优先、`transcript_path` 兜底生成 key，避免多个 Claude Code 会话在同一项目中并发时互相污染。首次 Stop block 前会先标记已提醒；同一轮第二次 Stop 放行。`UserPromptSubmit` 会重置本轮状态。

## Hook 输出协议

- Stop/SubagentStop block 使用 `decision: block`。
- PreToolUse/PostToolUse block 使用 `hookSpecificOutput.permissionDecision: deny`。
- warn 使用 `systemMessage`。
- allow 返回 `{}`。
- 通知失败和文档提醒状态异常都 fail open；通知诊断会追加到 hook `systemMessage`，文档提醒诊断会写入 stderr。
