# hook-terr

`hook-terr` 是一个个人工作流 hook runtime 插件，用于在 Claude Code 的 hook 事件中执行可配置规则。内置 Stop 提醒：当 Claude Code 准备结束本轮任务时，可通过 Windows 提示音、popup 弹窗、tray 通知或自定义命令提醒用户。

## 特性

- 注册 `Stop`、`SubagentStop`、`PreToolUse`、`PostToolUse`、`UserPromptSubmit` 五类 hook 入口。
- 默认只启用主会话 Stop 提醒规则；`SubagentStop` 默认关闭，避免子 agent 结束时弹提示音。
- 支持插件内默认配置、用户全局覆盖和项目覆盖。
- 默认 Stop 通道为 Windows `.wav` sound + popup 弹窗。
- 支持 Windows tray 通知、提示音、结构化弹窗和高级自定义命令。
- hook 异常 fail open，通知失败不会阻断 Claude Code 主流程，并会把简要诊断追加到 `systemMessage`。

## Commands

- `/hook-terr` — 显示当前生效的 hook-terr 配置。
- `/hook-terr:configure` — 交互式配置 Stop 通知通道，并选择写入全局或项目 settings 覆盖层；启用 `sound` 时会补齐默认提示音。
- `/hook-terr:sound` — 直接保存默认 sound 提示音，或打开外部 PowerShell picker 试听后保存全局偏好。

## 配置来源

加载优先级：

```text
defaults/settings.json
~/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

规则加载优先级：

```text
defaults/rules/*.json
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
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

`presets/` 随插件分发，但不会自动加载；需要复制到全局或项目 settings 后才会生效。

## 默认行为

默认 Stop 规则会：

- 返回 `systemMessage`，提醒 Claude 检查是否需要通知用户。
- 尝试播放 Windows `.wav` sound。
- 尝试显示 Windows popup 弹窗。

Windows notification 仍然可用，但不再是默认 Stop 通道；可通过 `/hook-terr:configure` 切换启用。启用后会通过独立启动的 STA PowerShell 通知进程同时投递 WinRT toast 和 tray balloon，hook 本身不会等待通知关闭。

## 通知通道

`settings.events.<Event>.notifications` 是事件默认通知通道来源。`rule.notify.channels` 是可选的规则级覆盖；未设置时回退到事件默认通道。内置 `stop-notify` 不写死 channels，让 `/hook-terr:configure` 只改 settings 即可生效。

`sound` 默认播放 `C:\\Windows\\Media\\tada.wav`。`/hook-terr:sound` 可跳过试听直接保存默认音效；需要试听时会打开外部 PowerShell picker，用户选好后回填 id、alias 或 wavPath 再写入全局偏好。`popup` 默认作为 Stop 通道启用，但仍可在 settings 覆盖层关闭。`custom_command` 是高级能力，默认关闭；启用后等价于执行本机命令，只应配置可信命令。

## 扩展规则

新增规则放在：

```text
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为覆盖键。项目规则覆盖全局规则，全局规则覆盖插件默认规则。同一 `id` 且 `enabled: false` 可禁用上层规则。

更多说明见 `references/`。
