# cc-statusline AI 维护路由

只在需要全局判断或不确定该读哪个 reference 时阅读本文件；具体修改应跳到对应文档，避免全量加载上下文。

## 按需路由

| 任务 | 读取 |
|------|------|
| 改 transcript 解析、缓存、stdin 循环、token 累加 | `references/architecture.md` |
| 改行格式、颜色、Line 2 token 显示、路径显示 | `references/rendering.md` |
| 改 `src/features/*.ts` 或新增状态栏功能 | `references/features.md` |
| 改 `Config`、`DEFAULT_CONFIG`、`commands/configure.md` | `references/config.md` |
| 改版本、发布、插件元数据、同步副本 | `references/publish.md` |

## 运行总览

```text
Claude Code stdin StatusLineData
  → index.ts readStdinLoop(async handler)
  → codexLimits.ensureFresh(data) 可选补齐 rate_limits
  → parseTranscript(data.transcript_path)
  → render(data, parseResult, cfg)
  → fs.writeSync(1, output + "\n")
```

关键约束：
- 进程长驻，避免 Windows 每 ~300ms spawn Node.js 的 Desktop Heap 开销。
- stdout 必须用 `fs.writeSync(1, ...)` 即时刷新，不能依赖 pipe 下的 `process.stdout.write()`。
- transcript JSONL 是 tools/agents/todos 与 API token 的来源；stdin 是 model、context、path、rate_limits 的来源。

## Line 2 token 语义

| 标签 | 含义 | 来源 | 生命周期 |
|------|------|------|----------|
| `in/out` | 当前上下文窗口 token 快照 | stdin `context_window.total_*_tokens` | 实时变化 |
| `ses` | 当前 Claude Code session 内 API token 累计 | transcript 增量解析 + `sessionKey` | transcript `sessionId` 变化后归零 |
| `api` | 当前 transcript 历史 API token 累计 | transcript 增量解析 + cache | 按 transcript UUID 持久 |

注意：`in/out`、`ses`、`api` 是三种不同口径，不能相互替代。

## 必守不变量

1. feature extraction 必须在 token 去重 `continue` 前运行，否则重复 usage 行上的 tool 事件会丢失。
2. usage 字段累加用 `|| 0` 防 NaN；不要用 `?? 0` 处理可能已污染的数值链。
3. `SessionCacheV2` 写 JSON v2，缓存键来自 transcript 文件名/UUID，读取兼容旧 CSV。
4. `ses` 会写入 cache，并通过 `sessionKey` 判断是否可复用；`sessionKey` 优先用 transcript 顶层 `sessionId`，禁止退回不稳定的 `ppid`。
5. `api` 始终按 transcript 历史累计；usage 去重必须包含 `server_tool_use_input_tokens`。
6. `lineNum` 只记录最后成功处理的非空 JSONL 物理行号，尾部空行不能推进缓存。
7. Codex usage fallback 只在 stdin 没有 `rate_limits`，且 `ANTHROPIC_BASE_URL` host 是内建本地或显式 allowlist 时探测；必须限频、按 host 复用 in-flight、按 host 隔离缓存，并让一次性 stdin 调用等待 pending handler。
8. `colors.ts` 保持独立，避免 `render.ts ↔ features/*.ts` 循环依赖。
9. 修改 `src/`、`commands/`、`references/` 或用户可见行为时，按 `references/publish.md` bump patch/minor 并同步版本文件。

## 文档维护原则

- 本文件只保留路由和跨模块不变量。
- 模块细节写入对应 reference，不把所有知识堆回这里。
- 新 gotcha 先写入具体 reference；只有高频且会影响操作顺序的规则才提升到本文件。
