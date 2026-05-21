# cc-statusline 插件 — AI 维护手册

Claude Code 终端状态栏插件。由 Claude Code 主进程每 ~300ms 通过 stdin 推送 `StatusLineData` JSON，插件解析 transcript JSONL 后渲染 ANSI 状态栏输出。

## 运行机制

```
Claude Code 主进程
  │  ~300ms 推送 StatusLineData JSON 到 stdin
  ▼
index.ts (长驻进程 readStdinLoop)
  │  parseTranscript(data.transcript_path)  → ParseResult
  │  render(data, parseResult, cfg)         → ANSI 字符串
  │  fs.writeSync(1, output + "\n")         → 即时 flush 到 stdout
  ▼
Claude Code 终端渲染 ANSI
```

- **长驻进程**：一个 node 进程处理所有更新，消除 Windows Desktop Heap 每周期 spawn 开销
- **stdout flush**：管道模式下 `process.stdout.write()` 不自动 flush，必须用 `fs.writeSync(1, ...)`

## 状态栏每行含义

| 行 | 显示内容 | 数据来源 | 说明 |
|----|---------|---------|------|
| 1 | `model │ ctx:inTok/ctxSize pct%` | stdin `StatusLineData` | 模型名、上下文窗口使用率 |
| 2 | `in:X out:Y │ ses:A/B │ api:Z │ HH:MM:SS` | 混合（见下） | token 统计行 |
| 3 | `usage: 5h ███░░░░░░░ 30% (4h 40m) │ 7d █░░░░░░░░░ 5% (5d 12h)` | stdin `rate_limits` 或 Codex headers fallback | 5 小时与 7 天速率限制（可选） |
| 4 | `tools: ◐ Read file.ts │ ✓ Bash ×3` | JSONL 解析 | 工具活动（最近 20 条） |
| 5 | `agent: ◷ code-reviewer: 审查 PR` | JSONL 解析 | Agent 追踪（最近 10 条） |
| 6 | `todo: ▸ 实现登录 (3/7)` | JSONL 解析 | Todo 进度 |
| 末 | `path:/home/user/project` | stdin `workspace`/`cwd` | 工作目录 |

### Line 2 字段详解（最容易误解）

Line 2 有**三组 token 数据**，来源和语义各不相同：

```
in:41.7w out:0.8w │ ses:3.4w/1.2w │ api:4.6w │ 18:30:45
```

| 标签 | 含义 | 数据来源 | 生命周期 |
|------|------|---------|---------|
| **in** / **out** | 当前上下文窗口中的 token 数 | `StatusLineData.context_window.total_input_tokens` / `total_output_tokens`（stdin 实时快照） | 实时变化 |
| **ses** | **当前 Claude Code session** 的 API token 增量累计 | JSONL transcript 增量解析 + 进程内存 Map/同 session 缓存（`ParseResult.sesIn/sesOut`） | Claude Code 重启或 SessionStart 变化后归零 |
| **api** | **transcript 历史累计** API token 消耗 | JSONL transcript 增量解析 + 缓存恢复（`ParseResult.apiIn/apiOut`） | 跨重启持久（按 transcript UUID 索引） |

**关键区别**：
- `in/out` = Claude 运行时告知的**上下文窗口快照**（实时）
- `ses` = 当前 Claude Code session 内解析到的新 API token 增量累计（优先按 transcript 中最新 SessionStart 标记恢复；缺失时按父进程恢复），同 transcript 跨重启复用时不会恢复旧 `ses`
- `api` = transcript 历史累计 API 消耗，按 transcript UUID 缓存，跨重启持久保留
- `in` ≠ `ses`（来源不同、含义不同、数值通常不同）

## 双数据源架构

```
stdin JSON (StatusLineData)          JSONL Transcript (增量解析)
─────────────────────────           ─────────────────────────
context_window.{total_input_,        assistant message 中的
  total_output_}tokens              usage.{input_, output_}tokens
  → in / out 显示                    → ses / api 显示
                                    （逐行累加，去重，缓存）
rate_limits.{five_hour,seven_day}    tool_use / tool_result
  或 X-Codex-* headers fallback        → tools / agents 显示
  → usage 行显示
                                    TodoWrite/TaskCreate/TaskUpdate
workspace.current_dir / cwd           → todos 显示
  → path 行显示
```

## Token 累积与缓存机制

### 解析逻辑（transcript.ts）

1. `readCache(transcriptPath)` — 从 `os.tmpdir()/cc-statusline-cache/ses-{transcript-UUID}.txt` 读取 `SessionCacheV2`
2. 从 `cache.lineNum` 开始增量遍历 transcript JSONL 新行
3. **先去重再累加**：4 字段（`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`）完全相同则 `continue` 跳过
4. 累加 delta 值到 `apiIn/apiOut`（跨重启持久）和 `sesIn/sesOut`（当前 Claude Code session）
5. `writeCache(transcriptPath, newCache)` 写入缓存（`apiIn/apiOut` 按 transcript 持久；`sesIn/sesOut` 仅在 `sessionKey` 匹配时恢复）

### SessionCacheV2 字段

| 字段 | 含义 |
|------|------|
| `lineNum` | 已解析到的 JSONL 行号（增量起点） |
| `lastIn/lastOut/lastCacheCreate/lastCacheRead` | 上一次非重复 usage 的 4 字段快照（去重用） |
| `sessionKey` | 当前 Claude Code session 标识（优先 latest SessionStart 标记，缺失时使用父进程，用于判断 `ses` 是否可恢复） |
| `apiIn/apiOut` | 会话历史累计 API token（跨重启持久） |
| `sesIn/sesOut` | 当前 Claude Code session 内 API token（仅 `sessionKey` 匹配时恢复） |
| `tools/agents/todos` | 特性数据（最多 20/10 条） |

**注意**：`sesIn/sesOut` 会写入缓存以兼容短生命周期 statusline 进程，但只有 `sessionKey` 匹配当前 Claude Code session 时才恢复；SessionStart 标记或父进程变化后，`ses` 归零。

### 缓存生命周期

- 以 transcript 文件名（UUID）为键
- 同 transcript 跨 Claude Code 重启复用同一缓存 → `lineNum` 持久、SessionStart 标记或父进程导致 `sessionKey` 变化 → 旧 `ses` 不恢复 → `ses` 归零
- `api` 按 transcript 持久累积，跨重启保留
- 旧 PID 键缓存文件（`ses-{pid}.txt`）可安全清理

## 配置

路径：`~/.claude/cc-statusline.json`

```json
{
  "showEffort": true,
  "showTokensLine": true,
  "showPath": true,
  "ctxWarnThreshold": 70,
  "ctxDangerThreshold": 90,
  "showToolActivity": true,
  "showRunningTools": true,
  "showCompletedTools": true,
  "showAgentTracking": true,
  "showTodoProgress": true,
  "showUsageLimits": true,
  "codexProbeIntervalMinutes": 3
}
```

所有字段可选，缺失时使用 `DEFAULT_CONFIG`（index.ts:11-24）。`codexProbeIntervalMinutes` 控制本地 Codex headers fallback 刷新间隔，默认 3 分钟，运行时夹取到 1-10 分钟。

## 关键 Gotchas

### 1. 特性提取必须在 token 去重 continue 之前
`transcript.ts:199-206`：`extractToolEvent/extractAgentEvent/extractTodoEvent` 必须在 token 去重 `continue`（第 217 行）**之前**执行，否则 tool_use/tool_result 事件会在重复 usage 行上被跳过丢失。

### 2. `|| 0` 而非 `?? 0`（本次修复的核心）
`input_tokens=0` 的行（流式中间态，无实际 token 消耗）**缺少** `cache_creation_input_tokens` 和 `cache_read_input_tokens` 字段。`0 + undefined = NaN`。

**错误**：`u.input_tokens ?? 0 + u.cache_creation_input_tokens ?? 0` → 仍然 NaN（`??` 只拦截 null/undefined，`NaN ?? 0` = `NaN`）

**正确**：`(u.input_tokens || 0) + (u.cache_creation_input_tokens || 0)` → `0 + 0 = 0`（`||` 拦截所有 falsy 值包括 NaN）

### 3. 缓存 NaN 污染链
如果一个周期产生 NaN 并写入缓存，下次读取时 `cache.apiIn || 0` 虽然会归零，但在 `|| 0` 修复之前，`NaN` 会通过 `??` 继续传播。**清理旧缓存的命令**：
```bash
rm -rf "$TEMP/cc-statusline-cache/"
```

### 4. 两个插件目录（安装 vs 开发）
- **开发/源码**：`~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/`
- **运行时**：`~/.claude/plugins/cache/terr-marketplace/cc-statusline/{version}/`
- **settings.json** 中 `statusLine.command` 指向**运行时**目录的 `dist/index.js`
- 修改源码后必须**同步到运行时目录**才能生效

### 5. `os.tmpdir()` 跨环境不一致
Windows 上 Git Bash 的 `$TEMP` 可能指向 `/tmp`，而 Node.js 的 `os.tmpdir()` 返回 `C:\Users\...\AppData\Local\Temp`。缓存实际落在 `os.tmpdir()` 返回的路径。

### 6. 版本号三文件同步
`package.json` + `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` 版本号需同步。bugfix → patch，feature → minor。

## 项目结构

```
src/
├── index.ts          # 主入口：加载配置，readStdinLoop → parse → render → flush
├── types.ts          # 所有接口：StatusLineData, UsageEntry, SessionCacheV2, ParseResult, Config
├── transcript.ts     # JSONL 增量解析 + 缓存读写 + token 累积（最复杂）
├── render.ts         # 主渲染：组合各 feature 输出为 ANSI 多行字符串
├── stdin.ts          # 长驻 stdin 循环（readStdinLoop）
├── format.ts         # fmtW 数字格式化（>=1万显示为 X.Xw）
├── colors.ts         # ANSI 256-color 工具
└── features/
    ├── tools.ts      # 工具活动：extractToolEvent + renderTools
    ├── agents.ts     # Agent 追踪：extractAgentEvent + renderAgents
    ├── todos.ts      # Todo 进度：extractTodoEvent + renderTodos
    └── limits.ts     # 速率限制：renderLimits（纯渲染，无提取）
```

## 开发命令

```bash
npm install && npm run build   # 编译
npm run dev                    # 监听编译
echo '{...}' | node dist/index.js  # 手动测试
```

## 版本历史

- **1.3.0** — 拆分 `showToolActivity` 为总开关 + 两个子开关（`showRunningTools`/`showCompletedTools`），可独立控制运行中/已完成工具显示
- **1.2.3** — 修复 ses 重启不归零：缓存键从 Claude PID 改为 transcript UUID，删除 `findClaudePid()` 进程树遍历
- **1.2.2** — ses/api 分离完整实现：dist 编译同步，render 使用 `ctx.sesIn/sesOut` + `ctx.apiIn/apiOut`
- **1.2.1** — 修复 NaN 污染：`??` → `||` 防护缺失字段；拆分 ses/api 为独立计数器（ses 进程启动归零，api 缓存持久）
- **1.2.0** — SessionCacheV2 增量缓存；长驻进程 stdin 循环
- **1.1.x** — 初始版本
