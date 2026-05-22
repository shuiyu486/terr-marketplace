# Runtime

`hook-terr` 采用薄 hook 入口和统一 runtime。

## 控制流

1. `hooks/hooks.json` 注册 Claude Code hook 事件。
2. `hooks/*.py` 读取 stdin JSON，并调用 `core.event_runner.run(event, input_data)`。
3. `context_builder` 将原始 payload 规范化为 `HookContext`。
4. `config_loader` 加载 settings 和 rules。
5. `rule_matcher` 找到当前事件最高优先级命中规则。
6. `action_executor` 执行通知器。
7. `response_builder` 输出 Claude Code hook JSON。

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

## Hook 输出协议

- Stop block 使用 `decision: block`。
- PreToolUse/PostToolUse block 使用 `hookSpecificOutput.permissionDecision: deny`。
- warn 使用 `systemMessage`。
- allow 返回 `{}`。
