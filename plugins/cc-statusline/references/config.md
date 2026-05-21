# 配置

修改配置相关逻辑（DEFAULT_CONFIG、configure.md、loadConfig）时阅读本文件。

## 配置文件

**路径**: `~/.claude/cc-statusline.json`

**默认值** (来自 `index.ts` 的 `DEFAULT_CONFIG`):

```json
{
  "showEffort": true,
  "showTokensLine": true,
  "showPath": true,
  "showToolActivity": true,
  "showRunningTools": true,
  "showCompletedTools": true,
  "showAgentTracking": true,
  "showTodoProgress": true,
  "showUsageLimits": true,
  "codexProbeIntervalMinutes": 3,
  "ctxWarnThreshold": 70,
  "ctxDangerThreshold": 90
}
```

## 字段说明

| 字段 | 类型 | 默认 | 说明 |
|------|------|------|------|
| showEffort | boolean | true | 显示 effort 级别 |
| showTokensLine | boolean | true | 显示 token 统计行 |
| showPath | boolean | true | 显示当前路径 |
| showToolActivity | boolean | true | 工具活动行总开关 |
| showRunningTools | boolean | true | 显示运行中工具 (◐ 图标) |
| showCompletedTools | boolean | true | 显示已完成工具 (✓ 计数) |
| showAgentTracking | boolean | true | 显示代理追踪行 |
| showTodoProgress | boolean | true | 显示待办进度 |
| showUsageLimits | boolean | true | 显示使用限制；优先使用 stdin rate_limits，本地代理环境下用 Codex headers fallback 刷新 |
| codexProbeIntervalMinutes | number | 3 | Codex headers fallback 探测间隔，支持 1-10 分钟，超出范围会自动夹取 |
| ctxWarnThreshold | number | 70 | 上下文黄色阈值 |
| ctxDangerThreshold | number | 90 | 上下文红色阈值 |

## 加载逻辑

`index.ts` 的 `loadConfig()`: `{ ...DEFAULT_CONFIG, ...JSON.parse(file) }` — 用户文件只需写要覆盖的字段，缺失字段取默认值。

## settings.json

settings.json 的 `statusLine.command` 字段由 `/cc-statusline:setup` 写入，由 `/cc-statusline:update` 更新路径。不在 plugin.json 中声明（Claude Code 插件系统不支持 statusLine 字段）。

## 同步要求

新增/删除/重命名配置字段时，必须同步更新:
1. `src/types.ts` — `Config` 接口
2. `src/index.ts` — `DEFAULT_CONFIG`
3. `commands/configure.md` — 默认值展示 + 选项列表 + 写入脚本
4. `references/config.md` — 本文件
