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

内置 `stop-notify` 不写死 channels，让 `/hook-terr:configure` 只改 settings 即可生效。默认 Stop 通道是 `sound + popup`；`SubagentStop` 默认关闭且不配置通知，避免子 agent 结束时弹提示音。

## Slash commands

- `/hook-terr` 只读取并显示当前生效配置。
- `/hook-terr:configure` 会先询问写入全局还是项目 settings，然后更新 Stop 通知通道。选择 `sound` 时，会在目标 settings 层显式初始化 `notifications.sound.wavPath` 为 `C:\\Windows\\Media\\tada.wav`，除非该层已有自定义 wavPath。
- `/hook-terr:sound` 可直接保存默认提示音，或打开外部 PowerShell picker 试听后，将所选 sound 提示音写入全局 settings。

`/hook-terr:configure` 写入位置：

```text
~/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

`/hook-terr:sound` 始终写入：

```text
~/.claude/hook-terr/settings.json
```

## Presets

`presets/` 随 marketplace 插件分发，保存开源可复用配置方案。它们不会自动加载，用户可以复制其中内容到全局或项目 settings 中。

## 禁用上层规则

创建同 `id` 规则并设置：

```json
{ "id": "stop-notify", "enabled": false, "event": "Stop", "decision": "allow" }
```

即可在当前层禁用上层同名规则。
