# Rules

规则是 JSON 文件，放在 `defaults/rules/`、`~/.claude/hook-terr/rules/` 或项目 `.claude/hook-terr/rules/`。

## 字段

- `version`: schema 版本，当前为 `1`。
- `id`: 规则唯一键，也是覆盖键。
- `enabled`: 是否启用。
- `event`: `Stop`、`PreToolUse`、`PostToolUse` 或 `UserPromptSubmit`。
- `priority`: 数字越大越先匹配。
- `decision`: `allow`、`warn` 或 `block`。
- `match`: `all` 或 `any`，默认 `all`。
- `when`: 条件数组，空数组表示总是匹配。
- `message`: 返回给 Claude 的文本。
- `notify`: 外部通知配置。

## 条件操作符

- `equals`
- `contains`
- `regex`
- `not_regex`
- `in`

## 字段来源

通用字段：`event`、`cwd`。

Stop：`reason`、`transcript_path`。

工具事件：`tool_name`、`command`、`file_path`、`content`、`new_text`、`old_text`。

Prompt：`user_prompt`。
