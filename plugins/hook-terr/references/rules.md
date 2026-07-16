# Rules

规则是 JSON 文件，放在 `defaults/rules/`、`<CLAUDE_CONFIG_DIR-or-~/.claude>/hook-terr/rules/` 或项目 `.claude/hook-terr/rules/`。每个 `when` condition 都必须包含非空字符串 `field`；无效条件会在加载阶段被拒绝，避免 `not_regex` 等操作符意外全局匹配。

## 字段

- `version`: schema 版本，当前为 `1`。
- `id`: 规则唯一键，也是覆盖键。
- `enabled`: 是否启用。
- `event`: `Stop`、`StopFailure`、`SubagentStop`、`PreToolUse`、`PostToolUse` 或 `UserPromptSubmit`。
- `priority`: 数字越大越先匹配。
- `decision`: `allow`、`warn` 或 `block`。
- `match`: `all` 或 `any`，默认 `all`。
- `when`: 条件数组，空数组表示总是匹配。
- `message`: 返回给 Claude 的文本。
- `notify`: 外部通知配置。

## notify

`notify.enabled` 为 true 时会请求执行外部通知，但 runtime 护栏只允许主会话 Stop 和主会话 `PreToolUse`/`AskUserQuestion` 求助场景真正调用通知器。`notify.title` 和 `notify.text` 控制通知文案；返回给 Claude 的 `systemMessage` 来自 `message.text`。

`notify.channels` 是可选的规则级覆盖：

- 未设置时，回退到 `settings.events.<Event>.notifications`。
- 设置为数组时，只使用该数组中的通道。
- 设置为空数组时，规则仍可返回 `systemMessage`，但不执行外部通知。

内置 `stop-notify` 默认关闭，不返回普通 Stop 自检 `systemMessage`；需要外部通知时，用用户或项目规则显式启用 `notify`。

`/hook-terr:configure` 的 `立即生效` 模式会创建或更新 `stop-notify-explicit` 规则，而不是修改内置 `stop-notify` 默认规则。该 explicit rule 只匹配主会话 Stop，并启用 `notify.enabled=true`；默认不写 `notify.channels`，因此会使用 settings 中的 `events.Stop.notifications`。Stop 外部通知规则会被视为 pure external notification，不返回可能让 Claude 继续工作的 Stop `systemMessage`。如果 Stop 先被 documentationReminder 等 runtime feature 拦截，runtime 会先返回该 feature 的响应，不会继续匹配 explicit rule。

## 文档收尾提醒不是规则

项目修改后的文档收尾提醒由 runtime feature `features.documentationReminder` 实现，不是 `defaults/rules/*.json` 规则。它需要跨 `PostToolUse`、`Stop` 和 `UserPromptSubmit` 共享会话状态，因此不能通过创建同 `id` 规则禁用；请在 settings 中设置 `features.documentationReminder.enabled=false`。

## 与 custom_command.command 的区别

规则中的 `message.text`、`notify.title` 和 `notify.text` 仍可使用规则文案模板。禁用的是 settings 中 `notifications.custom_command.command` 的旧模板替换。custom command 如需读取最终通知标题或正文，应使用 `HOOK_TERR_TITLE` 和 `HOOK_TERR_MESSAGE` 环境变量。

## 条件操作符

- `equals`
- `contains`
- `regex`
- `not_regex`
- `in`

## 字段来源

通用字段：`event`、`cwd`。

Stop/SubagentStop：`reason`、`transcript_path`、`is_subagent`、`agent_type`；Stop 另提供 `stop_hook_active`，runtime 自身会在该值为 true 时跳过再次 block。

StopFailure：`error`、`error_details`、`last_assistant_message`、`session_id`、`transcript_path`、`is_subagent`、`agent_type`。

`is_subagent` 在规则匹配中返回字符串 `"true"` 或 `"false"`；条件 `value` 可写字符串或 JSON boolean。`agent_type` 当前返回 `"main"` 或 `"subagent"`。runtime 会优先使用 hook payload 中的显式 `is_subagent` / `agent_type` 字段；缺失时，`SubagentStop` 事件、`isSidechain` 或 `agentId` 会视为子 agent，`Stop` 事件还会用 `transcript_path` 中独立的 `subagents` 路径段作为 fallback。

工具事件：`tool_name`、`command`、`file_path`、`content`、`new_text`、`old_text`。主会话 `PreToolUse` 且 `tool_name == "AskUserQuestion"` 是内置求助通知场景，会复用 Stop 通知通道；普通工具事件即使命中 `notify.enabled=true` 规则也会被 runtime 护栏阻止外部通知。

Prompt：`user_prompt`。
