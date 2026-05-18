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
│   ├── index.ts                  # 主入口：stdin → config → transcript → render
│   └── features/
│       ├── tools.ts              # Tool Activity：extract + render
│       ├── agents.ts             # Agent Tracking：extract + render
│       ├── todos.ts              # Todo Progress：extract + render
│       └── limits.ts             # Usage Limits：render only（数据来自 stdin）
├── references/                   # 按需加载的参考文档
├── dist/                         # 编译输出 (gitignore)
├── package.json                  # 零运行时依赖
└── tsconfig.json                 # ES2020 + commonjs + strict
```

## 数据流

```
stdin JSON (每 ~300ms)
  │
  ├── readStdin() → StatusLineData
  │     ├── .model, .effort, .context_window → render.ts line 1
  │     ├── .rate_limits? → limits.ts render
  │     └── .transcript_path
  │           │
  │           └── parseTranscript(path)
  │                 │ 读取 JSONL + 缓存 SessionCacheV2
  │                 │ 遍历新行 → extractToolEvent / extractAgentEvent / extractTodoEvent
  │                 │ token 累积 + 去重
  │                 │ 写回 JSON 缓存
  │                 └──→ ParseResult { tools, agents, todos, ... }
  │
  └── render(data, parseResult, cfg) → ANSI string → stdout
```

## 核心复杂度

### transcript.ts — 缓存 + 增量解析 + 去重 + 特性提取

- **缓存位置**: `os.tmpdir()/cc-statusline-cache/ses-{PID}.txt`
- **缓存格式**: JSON v2 (`SessionCacheV2`)，包含 tokens + tools + agents + todos；读取兼容旧 CSV
- **PID 查找**: Windows `wmic process ParentProcessId` → Linux/macOS `ps -o ppid=`
- **增量解析**: 从 cache.lineNum 开始
- **去重**: 4 字段相同 (input/output/cache_create/cache_read) 的 usage 行跳过
- **关键**: 特性提取在 token 去重 `continue` **之前**执行，否则 tool_use 事件会丢失

### features/ — 每功能独立提取+渲染

- `tools.ts`: 解析 `tool_use`/`tool_result`，提取 name+target，保留最近 20 条
- `agents.ts`: 解析 `Task`/`Agent` 的 `tool_use`，追踪运行状态+耗时
- `todos.ts`: 解析 `TodoWrite`/`TaskCreate`/`TaskUpdate`，维护 TodoState
- `limits.ts`: 纯渲染，无提取阶段

### stdin.ts — 500ms 超时

- 增量 JSON 解析：每个 data chunk 尝试 parse
- Windows 上正确处理 stdin EOF 避免管道阻塞
- 失败静默退出 (process.exit(0))

### colors.ts

- 独立于 render.ts 以避免 `render.ts ↔ features/*.ts` 循环依赖
- 导出 `color()`, `fg()`, `RESET`, `BOLD`

## 兼容性约束

- Node.js 18+ (ES2020 target)
- Windows 10/11 + macOS
- Claude Code v2.1+ (stdin JSON + transcript_path)
- ANSI 256 色终端
