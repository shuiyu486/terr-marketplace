# Rules

规则是 JSON 文件，放在 `defaults/rules/`、`~/.claude/hook-terr/rules/` 或项目 `.claude/hook-terr/rules/`。

## 字段

- `version`: schema 版本，当前为 `1`。
- `id`: 规则唯一键，也是覆盖键。
- `enabled`: 是否启用。
- `event`: `Stop`、`SubagentStop`、`PreToolUse`、`PostToolUse` 或 `UserPromptSubmit`。
- `priority`: 数字越大越先匹配。
- `decision`: `allow`、`warn` 或 `block`。
- `match`: `all` 或 `any`，默认 `all`。
- `when`: 条件数组，空数组表示总是匹配。
- `message`: 返回给 Claude 的文本。
- `notify`: 外部通知配置。

## notify

`notify.enabled` 为 true 时会执行外部通知。`notify.title` 和 `notify.text` 控制通知文案；返回给 Claude 的 `systemMessage` 来自 `message.text`。

`notify.channels` 是可选的规则级覆盖：

- 未设置时，回退到 `settings.events.<Event>.notifications`。
- 设置为数组时，只使用该数组中的通道。
- 设置为空数组时，规则仍可返回 `systemMessage`，但不执行外部通知。

内置 `stop-notify` 默认 `notify.enabled=false`，只返回自检 `systemMessage`；需要外部通知时，用用户或项目规则显式启用 `notify`。

## 条件操作符

- `equals`
- `contains`
- `regex`
- `not_regex`
- `in`

## 字段来源

通用字段：`event`、`cwd`。

Stop/SubagentStop：`reason`、`transcript_path`。

工具事件：`tool_name`、`command`、`file_path`、`content`、`new_text`、`old_text`。

Prompt：`user_prompt`。
