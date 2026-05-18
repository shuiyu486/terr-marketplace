## cc-statusline 插件

Claude Code marketplace 插件，提供模型、effort、上下文、token 统计、session API 消耗、路径、工具活动、代理追踪、待办进度和使用限制的状态栏显示。

### 运行机制

Claude Code 每 ~300ms 通过 stdin JSON 传入 `StatusLineData`，执行 `statusLine.command`（`node dist/index.js`），捕获 stdout 渲染为终端状态栏。

### 项目结构

```
cc-statusline/
├── .claude-plugin/plugin.json    ← 插件元数据（commands: setup, configure）
├── commands/
│   ├── setup.md                  ← /cc-statusline:setup 3步引导
│   ├── configure.md              ← /cc-statusline:configure 交互式配置
│   └── update.md                 ← /cc-statusline:update 一键更新
├── src/
│   ├── types.ts                  ← StatusLineData, ParseResult, Config 等接口
│   ├── colors.ts                 ← ANSI 256 色公共工具
│   ├── stdin.ts                  ← 500ms 超时 stdin JSON 读取
│   ├── format.ts                 ← fmtW 万格式化（>=1w→X.XXw）
│   ├── render.ts                 ← 主渲染入口，协调各功能行
│   ├── transcript.ts             ← JSONL 解析 + SessionCacheV2 + 增量去重
│   ├── index.ts                  ← 主入口：stdin → config → transcript → render
│   └── features/
│       ├── tools.ts              ← Tool Activity：工具使用提取+渲染
│       ├── agents.ts             ← Agent Tracking：子代理追踪提取+渲染
│       ├── todos.ts              ← Todo Progress：待办进度提取+渲染
│       └── limits.ts             ← Usage Limits：使用限制渲染（数据来自 stdin）
├── dist/                         ← 编译输出（gitignore）
├── package.json                  ← 零外部运行时依赖
└── tsconfig.json                 ← ES2020 + commonjs + strict
```

### 常用命令

```bash
npm install && npm run build      # 编译
npm run dev                       # 监听模式编译
```

功能测试（手动）：
```bash
# 基础测试（无新功能数据）
echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":50,"context_window_size":200000,"total_input_tokens":100000,"total_output_tokens":50000},"effort":{"level":"high"},"transcript_path":""}' | node dist/index.js

# 带 rate_limits 测试
echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":50,"context_window_size":200000,"total_input_tokens":100000,"total_output_tokens":50000},"effort":{"level":"high"},"transcript_path":"","rate_limits":{"five_hour":{"used_percentage":75,"resets_at":"2026-05-19T05:00:00Z"}}}' | node dist/index.js
```

### 核心复杂度

**transcript.ts — 缓存 + 增量解析 + 去重 + 特性提取**

- 缓存位置：`os.tmpdir()/cc-statusline-cache/ses-{PID}.txt`
- 缓存格式：JSON v2（`SessionCacheV2`），包含 tokens + tools + agents + todos 状态；读取时兼容旧 CSV 格式
- PID 查找：Windows 用 `wmic` 遍历父进程找 `claude.exe`；macOS/Linux 用 `ps -o ppid= -o comm=`
- 增量解析：从缓存记录的 lineNum 开始，只解析新增行
- Token 去重：4 字段完全相同（input_tokens, output_tokens, cache_creation, cache_read）的 usage 行跳过
- 特性提取：在 token 去重之前执行，确保 tool_use/tool_result 事件不被遗漏

**features/ — 每功能独立提取+渲染**

- `tools.ts`：解析 `tool_use`/`tool_result` 块，提取工具名+目标（文件路径/模式/命令），保留最近 20 条
- `agents.ts`：解析 `Task`/`Agent` 类型的 `tool_use` 块，显示子代理类型+描述+耗时
- `todos.ts`：解析 `TodoWrite`/`TaskCreate`/`TaskUpdate`，追踪 in_progress 任务
- `limits.ts`：纯渲染，数据来自 stdin 的 `rate_limits` 字段（可选，有则显示）

**stdin.ts — 500ms 超时**

- Node.js process.stdin 正确处理 EOF（解决了 Windows 上 PowerShell 的 stdin 管道阻塞问题）
- 增量 JSON 解析：每个 data chunk 尝试 parse，成功即返回
- 失败时静默退出（process.exit(0)）

### 渲染规则

- Line 1: `model │ effort │ ctx:inputTokens/contextSize pct%`
- Line 2-5: 功能行（条件显示，仅当启用且有数据时渲染）
  - `tools: ◐ Edit: auth.ts  │  ✓ Read ×3`
  - `agent: ◷ explore: Finding auth code (2m 15s)`
  - `todo: ▸ Fix bug (2/5)`
  - `usage: ████████░░ 75% (12h 50m)`
- Line N+1: `in:inputTokens out:outputTokens │ ses:sesApi │ api:apiTotal │ timestamp`
- 最后一行: `path: currentDirectory`
- 上下文颜色：>90% 红(196)+粗, >70% 黄(220)+粗, else 绿(82)
- effort 颜色：max=洋红(201)+粗, xhigh=红(196)+粗, high=黄(220)+粗, medium=绿(82), low=青(117)
- 模型名：浅紫(183)

### 配置

用户配置存储在 `~/.claude/cc-statusline.json`，字段：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| showEffort | boolean | true | 显示 effort 级别 |
| showTokensLine | boolean | true | 显示 token 统计行 |
| showPath | boolean | true | 显示当前路径 |
| showToolActivity | boolean | true | 显示工具活动行 |
| showAgentTracking | boolean | true | 显示代理追踪行 |
| showTodoProgress | boolean | true | 显示待办进度 |
| showUsageLimits | boolean | true | 显示使用限制（需要 rate_limits 数据） |
| ctxWarnThreshold | number | 70 | 上下文黄色警告阈值 |
| ctxDangerThreshold | number | 90 | 上下文红色危险阈值 |

settings.json 的 statusLine 字段由 `/cc-statusline:setup` 写入，由 `/cc-statusline:update` 更新路径，不在 plugin.json 中声明（Claude Code 插件系统不支持 statusLine 字段）。

### 修改后验证

1. `npm run build` 编译无错
2. 手动测试：echo JSON | node dist/index.js，检查 ANSI 输出
3. `claude plugin validate ~/.claude/plugins/marketplaces/terr-marketplace` 检查插件结构

### 发布流程

源码位于 terr-marketplace 仓库子目录 `plugins/cc-statusline/`。修改后：

1. 更新 `.claude-plugin/plugin.json` 中的 `version`
2. 同步更新 `.claude-plugin/marketplace.json` 中 cc-statusline 条目的 `version`
3. 提交并推送：
   ```
   cd ~/.claude/plugins/marketplaces/terr-marketplace
   git add plugins/cc-statusline/ .claude-plugin/marketplace.json
   git commit -m "sync: cc-statusline v<version> — <变更说明>"
   git pull --rebase && git push
   ```
4. 用户端执行 `/plugin install cc-statusline` 即可更新

### 兼容性约束

- Node.js 18+（ES2020 target）
- Windows 10/11 + macOS（跨平台 PID 查找）
- Claude Code v2.1+（stdin JSON + transcript_path 字段）
- ANSI 256色终端（WezTerm、Windows Terminal、iTerm2 等）

### CLAUDE.local.md 同步

每次更新本文件时，必须同步到工作目录 `C:\AI\m_projects\cc-statusline\` 和 terr-marketplace 插件目录：

```bash
# 从 terr-marketplace 插件目录同步到工作目录
cp ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/CLAUDE.local.md "C:/AI/m_projects/cc-statusline/CLAUDE.local.md"

# 从工作目录同步到 terr-marketplace 插件目录
cp "C:/AI/m_projects/cc-statusline/CLAUDE.local.md" ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/CLAUDE.local.md
```

两处文件应始终保持一致。
