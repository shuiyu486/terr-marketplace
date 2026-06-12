# Architecture：数据流、缓存、stdin

修改 `src/transcript.ts`、`src/stdin.ts`、`src/index.ts` 的数据流部分时阅读本文件。

## 数据流

```text
stdin StatusLineData
  ├─ model / effort / context_window / workspace → render.ts
  ├─ rate_limits? → limits render；缺失时可由 codexLimits fallback 补齐
  └─ transcript_path
       → parseTranscript(path)
          → 读取 cache
          → 从 cache.lineNum 增量解析 JSONL
          → extractToolEvent / extractAgentEvent / extractTodoEvent
          → usage 去重 + token 累加
          → 写回 SessionCacheV2
```

`index.ts` 的主路径：
1. `migrateConfigFile()` 幂等创建/补全/修复 `${CLAUDE_CONFIG_DIR:-~/.claude}/cc-statusline.json`
2. `loadConfig()` 读取并 normalize 配置，失败时使用 `DEFAULT_CONFIG`
3. `createCodexLimitsService(cfg)` 创建 usage fallback 服务
4. `readStdinLoop(async data => ...)` 读取本次命令 stdin 中的完整 JSON frame
5. 每帧检查配置文件 mtime；变化时重新 `loadConfig()` 并重建 usage fallback 服务
6. `ensureFresh(data, { maxWaitMs: 3000 })` 可选补齐 `rate_limits`
6. `parseTranscript(data.transcript_path)` 得到 `ParseResult`
7. `render(...)` 生成 ANSI 字符串并持久化最后可信 context 快照
8. `fs.writeSync(1, msg + "\n")` 即时输出

## 缓存文件

缓存目录：`os.tmpdir()/cc-statusline-cache/`

| 文件 | 用途 |
|------|------|
| `ses-{transcript-UUID}.txt` | transcript 派生的 session/API/tool/agent/todo 状态 |
| `ctx-{transcript-UUID}-{pathHash}.json` | 最后一次可信 `context_window` 快照；`pathHash` 来自完整 transcript 路径，避免同名文件串会话 |

## SessionCacheV2

缓存位置：`os.tmpdir()/cc-statusline-cache/ses-{transcript-UUID}.txt`

| 字段 | 用途 |
|------|------|
| `version` | JSON cache 版本，当前为 `2` |
| `sessionKey` | 当前 Claude Code session 标识，优先取 transcript 顶层 `sessionId`；缺失时兼容最近 `SessionStart`，最后用 transcript UUID fallback |
| `sessionKeySource` | `sessionKey` 来源：`transcript-session-id` / `session-start` / `transcript-uuid-fallback` |
| `lineNum` | 最后成功处理的非空 JSONL 物理行号；尾部空行不计入 |
| `lastIn/lastOut/lastCacheCreate/lastCacheRead/lastServerToolUseInput` | usage 去重快照 |
| `sesIn/sesOut` | 当前 session 累计 API token，`sessionKey` 匹配时复用 |
| `apiIn/apiOut` | transcript 历史累计 API token |
| `tools/agents/todos` | feature 状态缓存；`tools` 只保留最近事件 |
| `toolCompletedCounts` | tool completed 摘要的 session 累计计数；旧 JSON cache 缺失时按 `lineNum` 前历史重建 |
| `todoCompleted/todoTotal` | todo 统计缓存 |

读取兼容旧 CSV；写入始终使用 JSON v2。

## token 累加顺序

解析每条 JSONL message 时：
1. 先运行 `extractToolEvent` / `extractAgentEvent` / `extractTodoEvent`
2. 再判断 `msg.type === "assistant" && msg.message?.usage`
3. 如果 5 个 usage 字段与上次完全相同，跳过 token 累加：`input_tokens`、`output_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens`、`server_tool_use_input_tokens`
4. 使用 `|| 0` 计算 delta，包含 `server_tool_use_input_tokens`
5. 同时累加到 `api*`；只在 message 属于当前 transcript `sessionId` 时累加到 `ses*`

不能把 feature extraction 放到 token 去重之后，否则重复 usage 行中的 `tool_use` / `tool_result` 会丢失。

## context snapshot fallback

Line 1/2 的 `ctx` 与 `in/out` 是实时快照，不是累计值。渲染层按优先级取可信来源：
1. stdin `context_window.total_input_tokens/total_output_tokens/used_percentage`
2. stdin `context_window.current_usage`
3. transcript 最近一次 `assistant.message.usage`
4. 仍无可信 usage 时显示未知态 `—`

`current_usage` 和 transcript 最近 usage 只可作为显示 fallback；`ses/api` 仍必须只用 transcript 的 assistant usage delta 累计，避免 statusline 多次刷新重复计数。

## ses vs api

- `ses`：当前 Claude Code session 内累计；优先按 transcript 顶层 `sessionId` 区分，`sessionKey` 相同则从 cache / memory map 继续，`sessionId` 变化则归零。
- `api`：当前 transcript 历史累计；按 transcript UUID cache 持久。
- 两者共用同一 delta 计算，但生命周期不同。

## stdin 循环

- Claude Code 会按状态栏刷新重新运行 command，不能依赖 Node module-level 状态跨刷新保留。
- `readStdinLoop(handler)` 是主用路径：累积 chunk，完整 JSON parse 成功后调用 async handler。
- end/error 前必须等待 pending handler，避免一次性 stdin 调用在 Codex probe 完成前退出。
- `readStdin()` 仅用于兼容和手动测试。
- handler 内异常应吞掉单帧错误，不能让单次刷新失败影响后续刷新。

## Codex usage fallback

`features/codexLimits.ts` 只在这些条件下探测：
- stdin 没有可用 `rate_limits.five_hour`
- `ANTHROPIC_BASE_URL` 的 host 是内建本地 host（`localhost` / `127.0.0.1` / `::1`）或显式配置在 `codexProbeAllowedHosts`
- 有可用 token 和 model

服务要求：
- `codexProbeIntervalMinutes` 限频，默认 3 分钟，范围 1–10 分钟。
- `inflight` promise 必须按 host 复用，避免并发探测。
- 24 小时内当前 host 的旧缓存可作为 fallback snapshot。
- Codex fallback 缓存按 host 隔离，避免切换代理后串用额度。
