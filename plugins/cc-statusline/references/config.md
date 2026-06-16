# 配置

修改 `Config`、`DEFAULT_CONFIG`、`loadConfig()` 或 `commands/configure.md` 时阅读本文件。

## 配置文件

路径：`${CLAUDE_CONFIG_DIR}/cc-statusline.json`；未设置 `CLAUDE_CONFIG_DIR` 时为 `~/.claude/cc-statusline.json`。

runtime 启动时会先执行一次幂等配置迁移，再通过 `loadConfig()` 读取并 normalize 配置；读取失败时使用 `DEFAULT_CONFIG`。`/cc-statusline:update` 和 `/cc-statusline:configure` 也会把用户配置写成完整当前 schema：无配置时创建默认配置，合法旧配置补齐缺失字段，损坏 JSON 先备份为 `cc-statusline.json.bak-*` 再写默认配置。

`config.ts` 是配置 schema、默认值、normalize 和写回的唯一真源。命令层应通过编译后的 `dist/configCli.js` 读取、迁移或 patch 配置，避免在 markdown 命令中复制 schema。

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
  "codexProbeIntervalMinutes": 3,
  "codexProbeAllowedHosts": []
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
| `codexProbeAllowedHosts` | string[] | [] | 允许 Codex fallback 主动探测的非本地 host 或 `host:port` allowlist；本地 `localhost` / `127.0.0.1` / `::1` 始终内建允许 |

## Codex probe hosts

`codexProbeAllowedHosts` 只保存用户显式允许的远程 host identity，不包含 protocol、path 或 query；如果 `ANTHROPIC_BASE_URL` 显式带端口，则保存并按 `host:port` 匹配。normalize 会接受裸 host、`host:port` 或 URL，最终保存小写 hostname / `hostname:port` 并去重。

`/cc-statusline:setup` 会读取当前有效 `ANTHROPIC_BASE_URL`（`settings.json.env` + `process.env`，后者覆盖前者），如果解析到非本地且未授权的 host identity，会询问用户是否加入 allowlist。`/cc-statusline:configure` 只保留该字段，不做域名交互。

## settings.json

`settings.json` 的 `statusLine.command` 由 `/cc-statusline:setup` 写入，由 `/cc-statusline:update` 更新路径。Claude Code 插件元数据不支持直接声明 `statusLine` 字段。

## configCli

`src/configCli.ts` 编译为 `dist/configCli.js`，供 slash command 调用：

| 命令 | 用途 |
|------|------|
| `read` | 输出 normalize 后完整配置 |
| `migrate` | 创建、修复或补齐配置文件 |
| `patch <json>` | 合并部分字段并写回完整配置 |
| `suggest-probe-host` | 基于当前 `ANTHROPIC_BASE_URL` 判断 setup 是否需要询问授权 |
| `allow-probe-host <hostOrUrl>` | 将远程 host 加入 `codexProbeAllowedHosts`，本地 host 不写入配置 |

## 同步要求

新增、删除或重命名配置字段时，同步更新：
1. `src/config.ts` 的 `Config`、`DEFAULT_CONFIG` 和 normalize 逻辑
2. `commands/configure.md` 的展示、选项和写入逻辑
3. `commands/setup.md` / `commands/update.md` 里使用 `dist/configCli.js` 的步骤
4. `references/config.md`
5. 若影响渲染或 feature 行为，同时更新 `references/rendering.md` 或 `references/features.md`
