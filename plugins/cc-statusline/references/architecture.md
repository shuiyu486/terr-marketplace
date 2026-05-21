# Architecture

修改 `src/` 下任一文件时，先阅读本文件了解数据流。

## 项目结构

```
cc-statusline/
├── .claude-plugin/plugin.json    # 插件元数据
├── commands/
│   ├── setup.md                  # /cc-statusline:setup
│   ├── configure.md              # /cc-statusline:configure
│   └── update.md                 # /cc-statusline:update
├── src/
│   ├── types.ts                  # 所有接口：StatusLineData, ParseResult, Config, SessionCacheV2
│   ├── colors.ts                 # ANSI 256 色工具 (color, fg, RESET, BOLD)
│   ├── stdin.ts                  # 500ms 超时 stdin JSON 读取
│   ├── format.ts                 # fmtW 万格式化（>=1w→X.XXw）
│   ├── render.ts                 # 主渲染入口，协调各功能行
│   ├── transcript.ts             # JSONL 解析 + SessionCacheV2 缓存 + 特性提取
│   ├── index.ts                  # 主入口：长驻循环 readStdinLoop → config → transcript → render → flush
│   └── features/
│       ├── tools.ts              # Tool Activity：extract + render
│       ├── agents.ts             # Agent Tracking：extract + render
│       ├── todos.ts              # Todo Progress：extract + render
│       ├── limits.ts             # Usage Limits：渲染 5h/7d 窗口
│       └── codexLimits.ts        # Codex headers fallback：低频探测并缓存 X-Codex-*
├── references/                   # 按需加载的参考文档
├── dist/                         # 编译输出 (gitignore)
├── package.json                  # 零运行时依赖
└── tsconfig.json                 # ES2020 + commonjs + strict
```

## 数据流

```
stdin JSON (每 ~300ms)
  │
  │  ┌─────────────────────────────────────┐
  │  │ 长驻模式: 进程启动一次，循环读取     │
  │  │ readStdinLoop(handler)              │
  │  │   ├── data 事件 → 累积 buffer       │
  │  │   ├── JSON.parse 完整 → handler()   │
  │  │   ├── fs.writeSync(1, ...) 即时刷新  │
  │  │   └── end/error → process.exit(0)   │
  │  └─────────────────────────────────────┘
  │
  ├── StatusLineData
  │     ├── .model, .effort, .context_window → render.ts stableContextWindow → line 1
  │     ├── .rate_limits? → limits.ts render
  │     ├── local proxy env → codexLimits.ts interval header probe/cache
  │     └── .transcript_path
  │           │
  │           └── parseTranscript(path)
  │                 │ 读取 JSONL + 缓存 SessionCacheV2
  │                 │ 遍历新行 → extractToolEvent / extractAgentEvent / extractTodoEvent
  │                 │ token 累积 + 去重
  │                 │ 写回 JSON 缓存
  │                 └──→ ParseResult { tools, agents, todos, ... }
  │
  └── render(data, parseResult, cfg) → fs.writeSync(1, ANSI + "\n") → stdout
```

## 核心复杂度

### transcript.ts — 缓存 + 增量解析 + 去重 + 特性提取

- **缓存位置**: `os.tmpdir()/cc-statusline-cache/ses-{transcript-UUID}.txt`
- **缓存格式**: JSON v2 (`SessionCacheV2`)，包含 sessionKey + apiIn/apiOut + sesIn/sesOut + tools + agents + todos；读取兼容旧 CSV
- **缓存键**: transcript 文件名（UUID），同 transcript 跨重启复用，`lineNum` 持久跳过旧行
- **增量解析**: 从 cache.lineNum 开始
- **去重**: 4 字段相同 (input/output/cache_create/cache_read) 的 usage 行跳过
- **关键**: 特性提取在 token 去重 `continue` **之前**执行，否则 tool_use 事件会丢失
- **NaN 防护**: `input_tokens=0` 的行缺少 `cache_creation_input_tokens`/`cache_read_input_tokens` 字段，必须用 `|| 0` 而非 `?? 0`（`NaN ?? 0` = `NaN`）
- **ses vs api**: `apiIn/apiOut` 从缓存恢复（跨重启持久），`sesIn/sesOut` 在 `sessionKey` 匹配当前 Claude Code session 时从缓存/进程内存恢复（SessionStart 标记或父进程变化则归零）。两者共用同一 delta 计算，独立累加

### features/ — 每功能独立提取+渲染

- `tools.ts`: 解析 `tool_use`/`tool_result`，提取 name+target，保留最近 20 条
- `agents.ts`: 解析 `Task`/`Agent` 的 `tool_use`，追踪运行状态+耗时
- `todos.ts`: 解析 `TodoWrite`/`TaskCreate`/`TaskUpdate`，维护 TodoState
- `render.ts`: `stableContextWindow()` 保留上一帧有效上下文，过滤流式输出期间临时 0 输入帧
- `limits.ts`: 纯渲染；`codexLimits.ts` 在本地代理环境下按配置间隔探测并缓存 `X-Codex-*` headers，可覆盖陈旧的 stdin 用量数据，并用 24 小时旧缓存避免刷新前整行消失

### stdin.ts — 500ms 超时 + 长驻循环

- **`readStdin()`** (one-shot, 保留兼容): 单次读取，500ms 超时，用于手动测试
- **`readStdinLoop()`** (长驻模式, 主用): 进程启动一次，stdin 每收到一个完整 JSON 对象调用 handler，stdin 关闭时退出
  - 消除 Windows 上每 ~300ms spawn Node.js 进程的开销（Desktop Heap 碎片化的主因）
  - buffer + drain() 模式: 累积 chunk 直到 JSON.parse 成功
- 失败静默退出 (process.exit(0))

### colors.ts

- 独立于 render.ts 以避免 `render.ts ↔ features/*.ts` 循环依赖
- 导出 `color()`, `fg()`, `RESET`, `BOLD`

## 兼容性约束

- Node.js 18+ (ES2020 target)
- Windows 10/11 + macOS
- Claude Code v2.1+ (stdin JSON + transcript_path)
- ANSI 256 色终端
