# hook-terr

`hook-terr` 是一个个人工作流 hook runtime 插件，用于在 Claude Code 的 hook 事件中执行可配置规则。内置 Stop 自检提示会提醒 Claude 判断是否需要用户协助；外部提醒可通过启用 `notify` 的规则调用 Windows 提示音、popup 弹窗、tray 通知或自定义命令。

## 特性

- 注册 `Stop`、`SubagentStop`、`PreToolUse`、`PostToolUse`、`UserPromptSubmit` 五类 hook 入口。
- 默认只启用主会话 Stop 自检规则；`SubagentStop` 默认关闭，避免子 agent 结束时弹提示音。
- 规则可匹配 `is_subagent` 与 `agent_type`，用于区分主会话和子 agent。
- 默认启用文档收尾提醒：项目内使用 `Write`、`Edit`、`MultiEdit` 或 `NotebookEdit` 修改文件后，首次 Stop 会提醒 Claude 更新相关文档并完成必要验证。
- 支持插件内默认配置、用户全局覆盖和项目覆盖。
- Stop 外部通知需要通过用户或项目规则显式启用，避免每次 Stop 都误触发。
- 支持 Windows tray 通知、提示音、结构化弹窗和高级自定义命令。
- hook 异常 fail open，通知失败不会阻断 Claude Code 主流程，并会把简要诊断追加到 `systemMessage`。

## Commands

- `/hook-terr` — 显示当前生效的 hook-terr 配置。
- `/hook-terr:configure` — 交互式配置 Stop 通知通道，并可选择创建 explicit Stop notify rule 让配置立即生效；启用 `sound` 时会补齐默认提示音。
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
- 仅在 `is_subagent == "false"` 的主会话 Stop 中生效。
- 不直接触发 Windows `.wav` sound、popup 或 toast，避免非完成/非求助场景误打扰。

默认文档收尾提醒会：

- 仅在当前 `cwd` 看起来像项目，且修改工具命中的文件位于该项目目录内时记录状态。
- 识别 `Write`、`Edit`、`MultiEdit` 和 `NotebookEdit`；不根据 `Bash` 命令猜测文件修改。
- 在同一会话首次 Stop 时返回 `decision: block`，要求 Claude 更新相关文档，并执行必要的测试/验证。
- 同一轮只提醒一次；再次 Stop 会放行。用户或项目 settings 可通过 `features.documentationReminder.enabled=false` 关闭。

Windows notification 仍然可用，但不再由默认 Stop 自检规则触发。`/hook-terr:configure` 可以只保存 Stop 通知通道，也可以在用户确认后创建 explicit Stop notify rule。选择“立即生效”时，会创建 explicit Stop notify rule；当主会话 Stop 未先被 documentationReminder 等 runtime feature 拦截并命中该 rule 时，会使用所选通道触发外部通知。选择“仅保存通道”时，默认 Stop 自检规则仍然不会播放 sound、popup 或 toast。通知进程会独立启动，hook 本身不会等待通知关闭。

## 通知通道

`settings.events.<Event>.notifications` 是事件默认通知通道来源。`rule.notify.channels` 是可选的规则级覆盖；未设置时回退到事件默认通道。默认 `stop-notify` 只做自检提示；需要外部通知时，创建启用 `notify` 的用户或项目规则。

`sound` 默认播放 `C:\\Windows\\Media\\tada.wav`。`/hook-terr:sound` 可跳过试听直接保存默认音效；需要试听时会打开外部 PowerShell picker，用户选好后回填 id、alias 或 wavPath 再写入全局偏好。`popup` 默认可用，但只有启用 notify 的规则选择该通道时才会触发。`custom_command` 是高级能力，默认关闭；启用后等价于执行本机命令，只应配置可信命令；动态消息只能通过 `HOOK_TERR_*` 环境变量读取，旧 `{{message}}` 等 `custom_command.command` 模板会导致 settings 加载诊断报错。

## 扩展规则

新增规则放在：

```text
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为覆盖键。项目规则覆盖全局规则，全局规则覆盖插件默认规则。同一 `id` 且 `enabled: false` 可禁用上层规则。自定义 Stop 规则如果不希望命中子 agent，可添加 `is_subagent == "false"` 条件；如果需要专门匹配子 agent，可使用 `is_subagent == "true"` 或 `agent_type == "subagent"`。

更多说明见 `references/`。
