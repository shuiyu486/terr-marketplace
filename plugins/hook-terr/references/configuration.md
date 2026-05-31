# Configuration

`hook-terr` 使用三层配置：插件默认配置、用户全局覆盖、项目覆盖。

## 加载顺序

```text
defaults/settings.json
~/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

后加载的配置会深度覆盖前面的配置。数组会整体替换，不做按元素合并。

## 规则加载顺序

```text
defaults/rules/*.json
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为唯一键。项目规则覆盖全局规则，全局规则覆盖默认规则。

## 通知通道来源

`settings.events.<Event>.notifications` 是默认通知通道来源。`rule.notify.channels` 是可选的规则级覆盖；未设置时回退到事件默认通道。

settings 中的 Stop channels 只是“通道偏好”，不会单独触发外部通知。真正触发通知的开关是命中规则中的 `notify.enabled=true`。内置 `stop-notify` 默认不执行外部通知，只在 `is_subagent == "false"` 的主会话 Stop 中返回自检 `systemMessage`。`SubagentStop` 默认关闭且不配置通知，避免子 agent 结束时弹提示音。

## Slash commands

- `/hook-terr` 只读取并显示当前生效配置。
- `/hook-terr:configure` 会先询问写入全局还是项目 settings，然后更新 Stop 通知通道。随后会询问是否创建/更新 explicit Stop notify rule：选择 `立即生效` 时写入对应 scope 的 `rules/stop.notify.explicit.json`；当主会话 Stop 未先被 documentationReminder 等 runtime feature 拦截并命中该 rule 时，会触发外部通知。选择 `仅保存通道` 时只修改 settings，内置默认 `stop-notify` 仍不会触发外部通知。选择 `sound` 时，会在目标 settings 层显式初始化 `notifications.sound.wavPath` 为 `C:\\Windows\\Media\\tada.wav`，除非该层已有自定义 wavPath。
- `/hook-terr:sound` 可直接保存默认提示音，或打开外部 PowerShell picker 试听后，将所选 sound 提示音写入全局 settings。

`/hook-terr:configure` settings 写入位置：

```text
~/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

`/hook-terr:configure` 选择 `立即生效` 时的 explicit rule 写入位置：

```text
~/.claude/hook-terr/rules/stop.notify.explicit.json
<project>/.claude/hook-terr/rules/stop.notify.explicit.json
```

`/hook-terr:sound` 始终写入：

```text
~/.claude/hook-terr/settings.json
```

## 文档收尾提醒

`features.documentationReminder` 默认启用，随插件默认 settings 分发；更新插件后，未显式覆盖该配置的机器会自动应用。

默认行为：当当前 `cwd` 看起来像项目，且本会话通过 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改了项目目录内文件时，首次 Stop 会 block 一次，提醒 Claude 更新相关文档并在验证后 commit/push。状态按 `session_id` 或 `transcript_path` 隔离，避免同一项目内多个 Claude Code 会话互相污染。

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

运行时状态存储在 `~/.claude/hook-terr/state/documentation-reminder/`。

## custom_command 配置迁移

`notifications.custom_command.command` 中不再支持旧模板变量：`{{event}}`、`{{title}}`、`{{message}}`、`{{cwd}}`、`{{timestamp}}`。如果用户或项目 settings 包含这些模板，settings 加载阶段会报诊断并跳过该配置层。

请改用 `HOOK_TERR_*` 环境变量，例如 PowerShell 中使用 `$env:HOOK_TERR_MESSAGE`，sh/bash 中使用 `$HOOK_TERR_MESSAGE`。

## Presets

`presets/` 随 marketplace 插件分发，保存开源可复用配置方案。它们不会自动加载，用户可以复制其中内容到全局或项目 settings 中。

## 禁用上层规则

创建同 `id` 规则并设置：

```json
{ "id": "stop-notify", "enabled": false, "event": "Stop", "decision": "allow" }
```

即可在当前层禁用上层同名规则。
