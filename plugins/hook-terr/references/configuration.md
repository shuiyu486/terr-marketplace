# Configuration

`hook-terr` 使用三层配置：插件默认配置、用户全局覆盖、项目覆盖。

## 加载顺序

```text
defaults/settings.json
~/.claude/hook-terr/settings.json
<project>/.claude/hook-terr/settings.json
```

后加载的配置会深度覆盖前面的配置。

## 规则加载顺序

```text
defaults/rules/*.json
~/.claude/hook-terr/rules/*.json
<project>/.claude/hook-terr/rules/*.json
```

规则以 `id` 为唯一键。项目规则覆盖全局规则，全局规则覆盖默认规则。

## Presets

`presets/` 随 marketplace 插件分发，保存开源可复用配置方案。它们不会自动加载，用户可以复制其中内容到全局或项目 settings 中。

## 禁用上层规则

创建同 `id` 规则并设置：

```json
{ "id": "stop-notify", "enabled": false, "event": "Stop", "decision": "allow" }
```

即可在当前层禁用上层同名规则。
