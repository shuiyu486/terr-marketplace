# hook-terr

`hook-terr` 是一个个人工作流 hook runtime 插件，用于在 Claude Code 的 hook 事件中执行可配置规则。首版内置 Stop 提醒：当 Claude Code 准备结束本轮任务时，可通过 Windows 通知、提示音、结构化弹窗或自定义命令提醒用户。

## 特性

- 注册 `Stop`、`PreToolUse`、`PostToolUse`、`UserPromptSubmit` 四类 hook 入口。
- 默认只启用 Stop 提醒规则，其它事件可通过规则文件扩展。
- 支持插件内默认配置、用户全局覆盖和项目覆盖。
- 支持 Windows tray 通知、提示音、结构化弹窗和高级自定义命令。
- hook 异常 fail open，通知失败不会阻断 Claude Code 主流程。

## 配置来源

加载优先级：

```text
plugin defaults/presets < ~/.claude/hook-terr < <project>/.claude/hook-terr
```

随插件分发的默认文件：

```text
defaults/settings.json
defaults/rules/*.json
presets/*.json
```

用户全局覆盖：

```text
~/.claude/hook-terr/settings.json
~/.claude/hook-terr/rules/*.json
```

项目覆盖：

```text
<project>/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/rules/*.json
```

## 默认行为

默认 Stop 规则会：

- 返回 `systemMessage`，提醒 Claude 检查是否需要通知用户。
- 尝试播放短提示音。
- 尝试发送 Windows tray 通知。

非 Windows 平台会正常降级，通知器失败只产生诊断，不会导致 hook 非 0 退出。

## 自定义弹窗和命令

`popup` 是结构化弹窗，只允许配置标题、正文和图标。`custom_command` 是高级能力，默认关闭；启用后等价于执行本机命令，只应配置可信命令。

## 扩展规则

新增规则放在：

```text
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为覆盖键。项目规则覆盖全局规则，全局规则覆盖插件默认规则。同一 `id` 且 `enabled: false` 可禁用上层规则。

更多说明见 `references/`。
