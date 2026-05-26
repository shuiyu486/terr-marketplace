# 配置

修改 `Config`、`DEFAULT_CONFIG`、`loadConfig()` 或 `commands/configure.md` 时阅读本文件。

## 配置文件

路径：`${CLAUDE_CONFIG_DIR}/cc-statusline.json`；未设置 `CLAUDE_CONFIG_DIR` 时为 `~/.claude/cc-statusline.json`。

runtime 启动时会先执行一次幂等配置迁移，再通过 `loadConfig()` 读取并 normalize 配置；读取失败时使用 `DEFAULT_CONFIG`。`/cc-statusline:update` 和 `/cc-statusline:configure` 也会把用户配置写成完整当前 schema：无配置时创建默认配置，合法旧配置补齐缺失字段，损坏 JSON 先备份为 `cc-statusline.json.bak-*` 再写默认配置。

## 默认值

```json
{
  "showEffort": true,
  "showTokensLine": true,
  "showPath": true,
  "showToolActivity": true,
  "showRunningTools": true,
  "showCompletedTools": true,
  "showAgentTracking": true,
  "agentDisplayMode": "compact",
  "showTodoProgress": true,
  "showUsageLimits": true,
  "ctxWarnThreshold": 70,
  "ctxDangerThreshold": 90,
  "codexProbeIntervalMinutes": 3
}
```

## 字段说明

| 字段 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `showEffort` | boolean | true | 显示 effort 级别 |
| `showTokensLine` | boolean | true | 显示 token 统计行 |
| `showPath` | boolean | true | 显示当前路径 |
| `showToolActivity` | boolean | true | 工具活动行总开关 |
| `showRunningTools` | boolean | true | 显示运行中工具 |
| `showCompletedTools` | boolean | true | 显示已完成工具聚合 |
| `showAgentTracking` | boolean | true | 显示 agent 追踪行 |
| `agentDisplayMode` | `"compact" \| "multiline"` | `"compact"` | Agent 显示模式；compact 单行摘要，multiline 多行展开并显示 model |
| `showTodoProgress` | boolean | true | 显示 todo 进度 |
| `showUsageLimits` | boolean | true | 显示 usage limits；缺 stdin 数据时可触发 Codex fallback |
| `ctxWarnThreshold` | number | 70 | 上下文黄色阈值 |
| `ctxDangerThreshold` | number | 90 | 上下文红色阈值 |
| `codexProbeIntervalMinutes` | number | 3 | Codex headers fallback 探测间隔，运行时夹在 1–10 分钟 |

## settings.json

`settings.json` 的 `statusLine.command` 由 `/cc-statusline:setup` 写入，由 `/cc-statusline:update` 更新路径。Claude Code 插件元数据不支持直接声明 `statusLine` 字段。

## 同步要求

新增、删除或重命名配置字段时，同步更新：
1. `src/config.ts` 的 `Config`、`DEFAULT_CONFIG` 和 normalize 逻辑
2. `commands/configure.md` 的展示、选项和写入逻辑
3. `commands/update.md` 的配置迁移入口
4. `references/config.md`
5. 若影响渲染或 feature 行为，同时更新 `references/rendering.md` 或 `references/features.md`
